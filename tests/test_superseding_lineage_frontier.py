from pathlib import Path
import json,unittest
ROOT=Path(__file__).resolve().parents[1]
class T(unittest.TestCase):
 def test_packet_order(self):
  q={x['id']:x for x in json.loads((ROOT/'WORK_QUEUE.json').read_text())['items']}
  self.assertEqual(q['B-115']['depends_on'],['B-110']); self.assertEqual(q['C-125']['depends_on'],['B-115']); self.assertEqual(q['D-135']['depends_on'],['C-125']); self.assertEqual(q['E-145']['depends_on'],['D-135']); self.assertEqual(q['F-155']['depends_on'],['E-145']); self.assertEqual(q['G-160']['depends_on'],['F-155'])
 def test_contract_guard_installed(self):
  t=(ROOT/'tools/rfc.py').read_text(); self.assertIn('validate_required_output_contract',t); self.assertIn('OUTPUT_CONTRACT.json',t)
 def test_f_to_g_bindings(self):
  c=json.loads((ROOT/'config/required_output_contracts.json').read_text()); n={x['name'] for x in c['modules']['F']['required_child_bindings']}; self.assertTrue({'plasma_composition','ionization_state','radiation_state','opacity_law','recombination_entry_state'}<=n)
if __name__=='__main__': unittest.main()
