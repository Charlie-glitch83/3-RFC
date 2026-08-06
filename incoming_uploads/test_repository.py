import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class RepositoryTests(unittest.TestCase):
    def test_doctor(self):
        proc = subprocess.run([sys.executable, str(ROOT / "tools/rfc.py"), "doctor"], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)

    def test_exactly_one_active_queue_item(self):
        queue = json.loads((ROOT / "WORK_QUEUE.json").read_text())
        active = [x for x in queue["items"] if x["status"] == "ACTIVE"]
        self.assertEqual(len(active), 1)
        state = json.loads((ROOT / "STATE.json").read_text())
        self.assertEqual(active[0]["id"], state["active_work_unit"])

    def test_canonical_terms(self):
        project = json.loads((ROOT / "config/project.json").read_text())
        self.assertEqual(project["canonical_terms"]["CIF"], "Cosmic Infinite Field")
        self.assertEqual(project["canonical_terms"]["QV"], "Quantum Vacuum")
        self.assertEqual(project["canonical_terms"]["RFL"], "Recursive Fractal Lattice")

    def test_all_module_specs_exist(self):
        graph = json.loads((ROOT / "config/module_graph.json").read_text())
        for mod in graph["module_order"]:
            self.assertTrue((ROOT / "modules" / mod / "spec.json").exists(), mod)
            self.assertTrue((ROOT / "modules" / mod / "README.md").exists(), mod)

    def test_seed_manifest_hashes(self):
        import hashlib
        manifest = json.loads((ROOT / "source_seed/SOURCE_SEED_MANIFEST.json").read_text())
        for rec in manifest["files"]:
            p = ROOT / "source_seed" / rec["filename"]
            self.assertTrue(p.exists(), rec["filename"])
            self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(), rec["sha256"])


    def test_protected_dependencies(self):
        queue = json.loads((ROOT / "WORK_QUEUE.json").read_text())
        deps = {x["id"]: set(x.get("depends_on", [])) for x in queue["items"]}
        self.assertEqual(deps["HI-190"], {"HU-170", "I-180"})
        self.assertEqual(deps["HR-255"], {"N-250"})
        self.assertEqual(deps["O-260"], {"HR-255"})
        self.assertEqual(deps["P-270"], {"O-260"})
        self.assertEqual(deps["Q-280"], {"O-260"})
        self.assertNotIn("P-270", deps["Q-280"])
        self.assertEqual(deps["FINAL-290"], {"P-270", "Q-280"})

    def test_module_evidence_history_and_requirements(self):
        state = json.loads((ROOT / "STATE.json").read_text())
        req = json.loads((ROOT / "config/module_evidence_requirements.json").read_text())["modules"]
        for mod, rec in state["modules"].items():
            self.assertEqual(rec["evidence_state"], "DESIGN")
            self.assertEqual(rec["evidence_history"][0]["state"], "DESIGN")
            self.assertIn(mod, req)

    def test_module_work_units_have_targets(self):
        queue = json.loads((ROOT / "WORK_QUEUE.json").read_text())
        modules = set(json.loads((ROOT / "config/module_graph.json").read_text())["module_order"])
        for item in queue["items"]:
            if item["module"] in modules:
                self.assertIn("required_evidence_state", item)
                self.assertIn("required_fidelity", item)

    def test_required_governed_run_templates(self):
        names = [
            "RUN_PLAN.md", "SOURCE_REGISTER.json", "PRE_EXECUTION_LOCK.json", "ENVIRONMENT.json",
            "CHECKPOINT_RECORD.json", "GENERATED_OUTPUT_MANIFEST.json", "REPLAY_RECORD.json",
            "GATE_RESULTS.json", "INDEPENDENT_VERIFICATION.md", "CLOSEOUT.md"
        ]
        for name in names:
            self.assertTrue((ROOT / "templates" / name).exists(), name)

    def test_core_thesis_is_explicit(self):
        readme = (ROOT / "README.md").read_text()
        self.assertIn("does **not** claim that every manifestation of existence obeys one literal equation", readme)
        self.assertIn("Cosmic Infinite Field", readme)
        self.assertIn("Quantum Vacuum", readme)
        self.assertIn("Recursive Fractal Lattice", readme)
        self.assertIn("Preserve evidence of prior failures", readme)

    def test_next_command_is_deterministic(self):
        proc = subprocess.run([sys.executable, str(ROOT / "tools/rfc.py"), "next"], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("ACTIVE: BOOT-000", proc.stdout)

    def test_firewall_scan_does_not_flag_protocol_prohibitions(self):
        proc = subprocess.run([sys.executable, str(ROOT / "tools/rfc.py"), "firewall-scan"], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("PASS", proc.stdout)

    def test_bundle_manifest_if_present(self):
        import hashlib
        import os
        import re
        path = ROOT / "BUNDLE_MANIFEST.json"
        if not path.exists():
            self.skipTest("bundle manifest generated at packaging step")
        manifest = json.loads(path.read_text())
        records = manifest.get("files", [])
        paths = [rec["path"] for rec in records]
        self.assertEqual(len(paths), len(set(paths)))
        self.assertGreater(len(paths), 100)
        for rec in records:
            target = ROOT / rec["path"]
            self.assertTrue(target.exists(), rec["path"])
            self.assertRegex(rec["sha256"], r"^[0-9a-f]{64}$")
            self.assertGreaterEqual(rec.get("size_bytes", -1), 0)
            if os.environ.get("RFC_VERIFY_DISTRIBUTION") == "1":
                self.assertEqual(hashlib.sha256(target.read_bytes()).hexdigest(), rec["sha256"])


if __name__ == "__main__":
    unittest.main()
