from __future__ import annotations
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from rfc_engine.reference_checks import run_all

class ExecutionReadyTests(unittest.TestCase):
    def test_all_module_recipes_exist(self):
        modules=json.loads((ROOT/'config/module_graph.json').read_text())['module_order']
        catalog=json.loads((ROOT/'recipes/CATALOG.json').read_text())['modules']
        self.assertEqual(set(modules),set(catalog))
        for m in modules:
            self.assertTrue((ROOT/catalog[m]['recipe']).is_file())
            self.assertTrue((ROOT/catalog[m]['work_order']).is_file())

    def test_wolfram_calls_are_unique_and_self_contained(self):
        calls=json.loads((ROOT/'config/WOLFRAM_CALLS.json').read_text())['calls']
        ids=[c['call_id'] for c in calls]
        self.assertEqual(len(ids),len(set(ids)))
        self.assertGreaterEqual(len(ids),2*len(json.loads((ROOT/'config/module_graph.json').read_text())['module_order']))
        for c in calls:
            text=(ROOT/c['code_path']).read_text()
            self.assertIn('ToString[result, InputForm]',text)
            self.assertNotIn('http://',text)
            self.assertNotIn('https://',text)

    def test_reference_matrix(self):
        result=run_all()
        self.assertEqual(result['overall'],'PASS')
        self.assertTrue(all(r['classification']=='MANUFACTURED_REFERENCE_ONLY' for r in result['results'].values()))

    def test_director_doctor(self):
        cp=subprocess.run([sys.executable,'tools/director.py','doctor'],cwd=ROOT,text=True,capture_output=True)
        self.assertEqual(cp.returncode,0,cp.stdout+cp.stderr)
        self.assertIn('PASS',cp.stdout)

    def test_prebuilt_theory(self):
        self.assertTrue((ROOT/'theory/SCIENTIFIC_CONSTITUTION.md').is_file())
        terms=json.loads((ROOT/'theory/TERMINOLOGY_LOCK.json').read_text())
        self.assertEqual(terms['canonical']['CIF'],'Cosmic Infinite Field')
        self.assertEqual(terms['canonical']['QV'],'Quantum Vacuum')
        self.assertTrue((ROOT/'theory/ENHANCEMENT_CROSSWALK.json').is_file())

    def test_administrative_work_unit_packs_are_complete(self):
        registry=json.loads((ROOT/'config/WORK_UNIT_PACKS.json').read_text())['work_units']
        queue=json.loads((ROOT/'WORK_QUEUE.json').read_text())['items']
        modules=set(json.loads((ROOT/'config/module_graph.json').read_text())['module_order'])
        expected={item['id'] for item in queue if item['module'] not in modules}
        self.assertEqual(expected,set(registry))
        for work_id,entry in registry.items():
            recipe_path=ROOT/entry['recipe']
            work_order_path=ROOT/entry['work_order']
            self.assertTrue(recipe_path.is_file(),work_id)
            self.assertTrue(work_order_path.is_file(),work_id)
            recipe=json.loads(recipe_path.read_text())
            self.assertEqual(recipe['work_unit'],work_id)
            self.assertTrue(recipe['exact_sequence'])
            self.assertTrue(recipe['componentwise_gates'])

    def test_hyper_realism_matrix_is_prechewed(self):
        matrix=json.loads((ROOT/'work_units/HR-255/EXECUTION_MATRIX.json').read_text())
        self.assertGreaterEqual(len(matrix['rows']),20)
        required={'id','domain','required_truth_outputs','required_synthetic_outputs','numerical_matrix','independent_verification','hard_stop'}
        for row in matrix['rows']:
            self.assertTrue(required.issubset(row),row.get('id'))
        self.assertTrue((ROOT/'work_units/HR-255/WORK_MODEL_PROMPT.md').is_file())

if __name__=='__main__':
    unittest.main()
