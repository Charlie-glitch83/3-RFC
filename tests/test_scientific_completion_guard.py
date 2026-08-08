import importlib.util,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('scientific_completion_guard',ROOT/'tools/scientific_completion_guard.py')
guard=importlib.util.module_from_spec(spec); spec.loader.exec_module(guard)
class GuardTests(unittest.TestCase):
    def test_repaired_g_source_register_does_not_upgrade_global_source_classes(self):
        run=ROOT/'modules/G/runs/G-160-20260808T021341Z'
        self.assertEqual(guard.validate_source_classes(run),[])
    def test_output_template_is_draft(self):
        doc=json.loads((ROOT/'templates/OUTPUT_COMPLETENESS.json').read_text())
        self.assertEqual(doc['overall'],'DRAFT')
        self.assertEqual(doc['required_outputs'],[])
    def test_close_run_is_wired_to_guard(self):
        text=(ROOT/'tools/rfc.py').read_text()
        self.assertIn('scientific_completion_guard.py',text)
        self.assertIn('OUTPUT_COMPLETENESS.json',text)
if __name__=='__main__': unittest.main()
