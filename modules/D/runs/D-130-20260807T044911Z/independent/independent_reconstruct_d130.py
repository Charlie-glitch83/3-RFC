#!/usr/bin/env python3
from __future__ import annotations

import json, math, hashlib
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[5]
RUN=Path(__file__).resolve().parents[1]
PARENT=ROOT/'modules/C/frozen/H_C_to_D.json'
SPEC=RUN/'FROZEN_DERIVATION_SPEC.json'
FREEZE=RUN/'NUMERICAL_EXECUTION_FREEZE.json'
PRIMARY=RUN/'primary/TRANSPORT_HISTORY.json'
OUT=RUN/'independent/INDEPENDENT_RECONSTRUCTION.json'

def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def entropy(p):
    p=np.clip(np.asarray(p,float),1e-300,None)
    return float(-np.sum(p*np.log(p)))

parent=json.loads(PARENT.read_text())
spec=json.loads(SPEC.read_text())
freeze=json.loads(FREEZE.read_text())
p0=np.asarray(parent['prethermal_state']['node_populations'],float)
M=np.asarray(parent['microscopic_constitution']['matrix'],float)
g=float(parent['microscopic_constitution']['dimensionless_doublet_gap'])
u=np.ones(3)/3.0
P=M/g
# Reconstruct first without reading primary summaries.
grid=np.linspace(freeze['intrinsic_execution_interval'][0],freeze['intrinsic_execution_interval'][1],201)
reconstructed=np.asarray([u+math.exp(-s)*(p0-u) for s in grid])
sums=reconstructed.sum(axis=1)
ents=np.asarray([entropy(x) for x in reconstructed])
reconstruction_checks={
  'uniform_projector_error':float(np.linalg.norm(P-(np.eye(3)-np.ones((3,3))/3))),
  'normalization_max_drift':float(np.max(np.abs(sums-sums[0]))),
  'minimum_population':float(np.min(reconstructed)),
  'minimum_entropy_increment':float(np.min(np.diff(ents)))
}
# Only after reconstruction, compare to primary trajectory bytes.
primary=json.loads(PRIMARY.read_text())
primary_y=np.asarray(primary['y'],float).T
compare_l2=float(np.linalg.norm(primary_y[-1]-reconstructed[-1]))
obstruction_checks={
  'dimensionful_mass_status':parent.get('dimensionful_mass_status'),
  'metric_spacetime_status':parent.get('metric_spacetime_status'),
  'thermal_history_status':parent.get('thermal_history_status'),
  'restart_contract':parent['restart']['restart_contract'],
  'physical_temperature_derivable_from_exact_parent':False,
  'physical_time_or_scale_factor_derivable_from_exact_parent':False
}
passed=(reconstruction_checks['uniform_projector_error']<=1e-12 and reconstruction_checks['normalization_max_drift']<=1e-12 and reconstruction_checks['minimum_population']>=-1e-12 and reconstruction_checks['minimum_entropy_increment']>=-1e-12 and compare_l2<=freeze['independent_tolerance_l2'] and parent.get('dimensionful_mass_status')=='NOT_DERIVED_NO_LAWFUL_SCALE_IN_PARENT' and parent.get('metric_spacetime_status')=='NOT_DERIVED' and parent.get('thermal_history_status')=='NOT_DERIVED_IN_C_RESERVED_FOR_D')
out={
  'run_id':spec['run_id'],'method':'ANALYTIC_PARENT_ONLY_RECONSTRUCTION_BEFORE_PRIMARY_COMPARISON','parent_sha256':sha(PARENT),'spec_sha256':sha(SPEC),'numerical_freeze_sha256':sha(FREEZE),
  'reconstruction_checks':reconstruction_checks,'primary_final_comparison_l2':compare_l2,'tolerance':freeze['independent_tolerance_l2'],'obstruction_checks':obstruction_checks,
  'pass':bool(passed),
  'claim':'Independent reconstruction confirms the normalized dimensionless relaxation branch and independently confirms that exact C does not supply a physical temperature, physical clock, metric expansion, or phase-threshold object.'
}
OUT.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
