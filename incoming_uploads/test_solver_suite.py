from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import numpy as np

from rfc_engine.solvers.big_implosion import run_big_implosion
from rfc_engine.solvers.nbody import run_nbody
from rfc_engine.solvers.utils import unresolved_placeholders
from tools.run_configured_solver import execute

ROOT = Path(__file__).resolve().parents[1]


class SolverSuiteTests(unittest.TestCase):
    def test_every_manufactured_configuration_passes(self):
        configs = sorted((ROOT / "configured_runs/examples").glob("*.json"))
        self.assertGreaterEqual(len(configs), 15)
        for path in configs:
            with self.subTest(path=path.name):
                result = execute(json.loads(path.read_text()))
                self.assertTrue(result.get("success"), result)
                self.assertNotEqual(result.get("classification"), "PHYSICAL_RFC_RESULT")

    def test_every_template_is_deliberately_unbound(self):
        templates = sorted((ROOT / "configured_runs/templates").glob("*.json"))
        bindings = json.loads((ROOT / "config/EXECUTION_BINDINGS.json").read_text())["modules"]
        expected = sum(len(record["bindings"]) for record in bindings.values())
        self.assertEqual(len(templates), expected)
        for path in templates:
            doc = json.loads(path.read_text())
            self.assertEqual(doc["classification"], "UNBOUND_EXECUTION_TEMPLATE")
            self.assertTrue(unresolved_placeholders(doc), path.name)
            with self.assertRaises(ValueError):
                execute(doc)

    def test_binding_materializer_produces_executable_config(self):
        import subprocess, sys
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "bound.json"
            completed = subprocess.run([
                sys.executable, str(ROOT / "tools/materialize_solver_config.py"),
                "--template", str(ROOT / "configured_runs/templates/A_triad_kernel.template.json"),
                "--binding-sheet", str(ROOT / "configured_runs/examples/binding_demo/A_triad_kernel.bindings.json"),
                "--output", str(output),
            ], cwd=ROOT, text=True, capture_output=True)
            self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
            document = json.loads(output.read_text())
            self.assertEqual(document["classification"], "PROVENANCE_BOUND_EXECUTION_CONFIG")
            result = execute(document)
            self.assertTrue(result["success"], result)

    def test_nbody_requires_explicit_coupling(self):
        cfg = json.loads((ROOT / "configured_runs/examples/K_nbody.json").read_text())["model"]
        cfg.pop("coupling_constant")
        with self.assertRaisesRegex(ValueError, "coupling_constant"):
            run_nbody(cfg)

    def test_big_implosion_reopens_exact_parent_numerically(self):
        cfg = json.loads((ROOT / "configured_runs/examples/B_big_implosion.json").read_text())["model"]
        result = run_big_implosion(cfg)
        self.assertTrue(result["success"], result)
        self.assertLessEqual(result["reopening_error"], cfg["tolerance"])
        self.assertLess(result["compression_ratio"], 1.0)

    def test_public_comparison_cannot_run_in_generation_mode(self):
        cfg = json.loads((ROOT / "configured_runs/examples/P_gaussian_comparison_synthetic.json").read_text())
        cfg["generation_mode"] = "GENERATION_SEALED"
        with self.assertRaisesRegex(ValueError, "Module P"):
            execute(cfg)

    def test_negative_covariance_is_rejected_without_projection(self):
        result = execute({
            "generation_mode": "GENERATION_SEALED",
            "solver": "covariance",
            "model": {"covariance": [[1.0, 2.0], [2.0, 1.0]], "seed": 1, "sample_count": 100},
        })
        self.assertFalse(result["success"])
        self.assertIn("do not silently project", result["error"])

    def test_freeze_hash_changes_when_content_changes(self):
        from rfc_engine.solvers.freeze_packet import run_freeze_packet
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "a.txt").write_text("first")
            first = run_freeze_packet({"root": str(root), "required_relative_paths": ["a.txt"]})
            (root / "a.txt").write_text("second")
            second = run_freeze_packet({"root": str(root), "required_relative_paths": ["a.txt"]})
            self.assertNotEqual(first["universe_hash"], second["universe_hash"])


if __name__ == "__main__":
    unittest.main()
