#!/usr/bin/env python3
from __future__ import annotations

import hashlib, json, math
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[5]
RUN = Path(__file__).resolve().parents[1]
PARENT = ROOT / 'modules/C/frozen/H_C_to_D.json'
SPEC = RUN / 'FROZEN_DERIVATION_SPEC.json'
PRIMARY = RUN / 'primary/DISTRIBUTION_HISTORY.json'
OUT = RUN / 'independent/INDEPENDENT_RECONSTRUCTION.json'

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def entropy(p):
    p=np.clip(np.asarray(p,float),1e-300,None)
    return float(-np.sum(p*np.log(p)))

parent=json.loads(PARENT.read_text())
spec=json.loads(SPEC.read_text())
p0=np.asarray(parent['prethermal_state']['node_populations'],float)
M=np.asarray(parent['microscopic_constitution']['matrix'],float)
g=float(parent['microscopic_constitution']['dimensionless_doublet_gap'])
u=np.ones(3)/3.0
P=M/g
controls=spec['numerical_controls']
# Reconstruct independently before reading any primary result or gate summary.
grid=np.linspace(controls['execution_interval'][0],controls['execution_interval'][1],257)
reconstructed=np.asarray([u+math.exp(-s)*(p0-u) for s in grid])
sums=reconstructed.sum(axis=1)
ents=np.asarray([entropy(x) for x in reconstructed])
exc=np.asarray([0.5*x@M@x for x in reconstructed])
checks={
  'projector_exact_form_l2':float(np.linalg.norm(P-(np.eye(3)-np.ones((3,3))/3))),
  'normalization_max_drift':float(np.max(np.abs(sums-sums[0]))),
  'minimum_population':float(np.min(reconstructed)),
  'minimum_entropy_increment':float(np.min(np.diff(ents))),
  'maximum_excitation_increment':float(np.max(np.diff(exc)))
}
# Only after reconstruction is fixed do we read the primary trajectory for comparison.
primary=json.loads(PRIMARY.read_text())
primary_y=np.asarray(primary['populations'],float).T
comparison_l2=float(np.linalg.norm(primary_y[-1]-reconstructed[-1]))
obstruction={
  'thermal_history_status_in_parent':parent['thermal_history_status'],
  'metric_spacetime_status_in_parent':parent['metric_spacetime_status'],
  'dimensionful_mass_status_in_parent':parent['dimensionful_mass_status'],
  'restart_contract':parent['restart']['restart_contract'],
  'physical_temperature_map_present':False,
  'physical_clock_or_scale_factor_present':False,
  'phase_order_parameter_threshold_present':False
}
passed=(checks['projector_exact_form_l2']<=1e-12 and checks['normalization_max_drift']<=1e-12 and checks['minimum_population']>=-controls['positivity_tolerance'] and checks['minimum_entropy_increment']>=-1e-12 and checks['maximum_excitation_increment']<=1e-12 and comparison_l2<=controls['analytic_numeric_l2_tolerance'])
out={
  'run_id':spec['run_id'],'method':'ANALYTIC_PARENT_ONLY_RECONSTRUCTION_BEFORE_PRIMARY_COMPARISON',
  'parent_sha256':sha(PARENT),'spec_sha256':sha(SPEC),'checks':checks,
  'primary_final_comparison_l2':comparison_l2,'comparison_tolerance':controls['analytic_numeric_l2_tolerance'],
  'obstruction_checks':obstruction,'diagnostic_pass':bool(passed),'full_physical_module_D_pass':False,
  'conclusion':'The normalized dimensionless transport orbit is independently reproduced. The exact parent still lacks a physical temperature/energy scale, physical clock/metric expansion, and phase-threshold object; no physical D-to-E handoff is independently supported.'
}
OUT.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
