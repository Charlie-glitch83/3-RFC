#!/usr/bin/env python3
from __future__ import annotations
import json, platform, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RID='G-165-20260810T144936Z'
R=ROOT/'modules/G/runs'/RID
record={
  'run_id':RID,
  'status':'FINAL',
  'operating_system':platform.platform(),
  'hardware':{},
  'software':[],
  'python':sys.version,
  'imports':['argparse','hashlib','json','re','pathlib'],
  'commands':[
    'tools/g165_execute_branch_family.py freeze',
    'director.py wolfram-record G-WL-001/G-WL-002',
    'run_reference_checks.py --module G (manufactured reference only)',
    'tools/g165_execute_branch_family.py execute',
    'tools/g165_independent_verify.py',
    'tools/g165_execute_branch_family.py finalize',
    'tools/scientific_completion_guard.py'
  ],
  'network_policy':'DISABLED_DURING_GENERATION',
  'random_seeds':[],
  'hidden_defaults_audited':True,
  'hidden_defaults_audit':{
    'physical_rate_defaults_used':False,
    'manufactured_reference_values_used_as_physical':False,
    'random_branch_selection_used':False,
    'external_or_public_targets_used':False,
    'unresolved_source_owned_coordinates_preserved':True
  }
}
(R/'ENVIRONMENT.json').write_text(json.dumps(record,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps(record,indent=2))
