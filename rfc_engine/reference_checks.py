from __future__ import annotations

import hashlib
import json
import math
from dataclasses import dataclass
from typing import Any, Callable

import networkx as nx
import numpy as np
from numpy.typing import NDArray
from scipy.integrate import solve_ivp
from scipy.linalg import expm

EPS = 1e-10


def _jsonable(value: Any) -> Any:
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, np.ndarray):
        return [_jsonable(x) for x in value.tolist()]
    if isinstance(value, dict):
        return {str(k): _jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(x) for x in value]
    return value


def _result(module: str, checks: dict[str, bool], metrics: dict[str, Any], note: str) -> dict[str, Any]:
    clean_checks = _jsonable(checks)
    return {
        "module": module,
        "classification": "MANUFACTURED_REFERENCE_ONLY",
        "overall": "PASS" if clean_checks and all(clean_checks.values()) else "FAIL",
        "checks": clean_checks,
        "metrics": _jsonable(metrics),
        "note": note,
    }


def check_A() -> dict[str, Any]:
    delta, alpha, t, depth = 4.66920160910299, 0.15, 2.0, 64
    lane_ok = all((n + 1) * n - n * (n - 1) == 2 * n for n in range(1, 100))
    raw = np.array([delta ** (-j) * math.exp(-alpha * j * t) for j in range(1, depth + 1)])
    p = raw / raw.sum()
    norm_ok = abs(float(p.sum()) - 1.0) < 1e-13 and bool(np.all(p > 0))
    modes = np.sin(np.arange(1, depth + 1))
    kernel = float(np.dot(raw, modes))
    bound = 1.0 / (delta * math.exp(alpha * t) - 1.0)
    bound_ok = abs(kernel) <= bound + 1e-12
    triad = np.eye(3)
    irreducible = np.linalg.matrix_rank(triad) == 3
    ablations_fail = all(np.linalg.matrix_rank(np.delete(triad, i, axis=0)) == 2 for i in range(3))
    return _result("A", {
        "lane_increment_2N": lane_ok,
        "depth_weights_normalized": norm_ok,
        "kernel_bound_respected": bound_ok,
        "three_roles_independent": irreducible,
        "each_role_ablation_loses_rank": ablations_fail,
    }, {"kernel": kernel, "bound": bound, "depth": depth},
    "Checks the exact algebraic and manufactured invariants used to validate the Module A implementation. It is not the full emergence theorem.")


def _path_laplacian(n: int) -> NDArray[np.float64]:
    L = np.zeros((n, n), dtype=float)
    for i in range(n - 1):
        L[i, i] += 1
        L[i + 1, i + 1] += 1
        L[i, i + 1] -= 1
        L[i + 1, i] -= 1
    return L


def check_B() -> dict[str, Any]:
    delta = 4.66920160910299
    L = _path_laplacian(4)
    Q = np.linalg.inv(np.eye(4) + L / (delta - 1.0))
    eig = np.linalg.eigvalsh(Q)
    x = np.array([1.5, -0.5, 0.75, -1.75])
    x -= x.mean()
    xp = Q @ x
    reopened = np.linalg.solve(Q, xp)
    one = np.ones(4)
    checks = {
        "operator_symmetric": np.allclose(Q, Q.T, atol=1e-12),
        "operator_positive_definite": bool(np.all(eig > 0)),
        "carrier_mode_preserved": np.allclose(Q @ one, one, atol=1e-12),
        "nontrivial_modes_strictly_compressed": np.linalg.norm(xp) < np.linalg.norm(x),
        "no_loss_reopening": np.allclose(reopened, x, atol=1e-12),
        "laplacian_ledger_conserved": np.allclose(L @ one, 0.0, atol=1e-12),
    }
    return _result("B", checks, {
        "operator_eigenvalues": eig.tolist(),
        "compression_ratio": float(np.linalg.norm(xp) / np.linalg.norm(x)),
        "reopening_error": float(np.linalg.norm(reopened - x)),
    }, "Manufactured graph-Laplacian realization of the Big Implosion operator. Actual Module B must consume the exact Module A parent and derive its physical state.")


def check_C() -> dict[str, Any]:
    M = np.array([[2.0, 0.3 + 0.2j], [0.3 - 0.2j, 1.1]], dtype=complex)
    vals, U = np.linalg.eigh(M)
    recon = U @ np.diag(vals) @ U.conj().T
    checks = {
        "mass_operator_hermitian": np.allclose(M, M.conj().T),
        "eigenbasis_unitary": np.allclose(U.conj().T @ U, np.eye(2), atol=1e-12),
        "spectral_reconstruction": np.allclose(recon, M, atol=1e-12),
        "positive_spectrum": bool(np.all(vals > 0)),
    }
    return _result("C", checks, {"eigenvalues": vals.real.tolist()}, "Generic microscopic-constitution manufactured case. It does not import Standard Model labels or values.")


def check_D() -> dict[str, Any]:
    k = 1.7
    def rhs(_: float, y: NDArray[np.float64]) -> NDArray[np.float64]:
        return np.array([-k * (y[0] - y[1]), k * (y[0] - y[1])])
    sol = solve_ivp(rhs, (0, 5), np.array([0.9, 0.1]), rtol=1e-10, atol=1e-12, dense_output=False)
    total = sol.y.sum(axis=0)
    entropy = -np.sum(np.clip(sol.y, 1e-15, None) * np.log(np.clip(sol.y, 1e-15, None)), axis=0)
    checks = {
        "integration_success": bool(sol.success),
        "positive_distributions": bool(np.all(sol.y >= -1e-12)),
        "conserved_total": float(np.max(np.abs(total - total[0]))) < 1e-9,
        "entropy_nondecreasing": bool(np.all(np.diff(entropy) >= -1e-10)),
        "approaches_equilibrium": abs(float(sol.y[0, -1] - sol.y[1, -1])) < 1e-5,
    }
    return _result("D", checks, {"max_total_error": float(np.max(np.abs(total-total[0]))), "final_state": sol.y[:, -1].tolist()}, "Stiff-capable nonequilibrium manufactured exchange system.")


def _integrate_network(S: NDArray[np.float64], rate: Callable[[NDArray[np.float64]], NDArray[np.float64]], y0: NDArray[np.float64], t1: float = 5.0) -> Any:
    return solve_ivp(lambda _t, y: S @ rate(np.clip(y, 0.0, None)), (0, t1), y0, rtol=1e-10, atol=1e-12)


def check_E() -> dict[str, Any]:
    # n + p <-> d manufactured network
    S = np.array([[-1.0, 1.0], [-1.0, 1.0], [1.0, -1.0]])
    baryon = np.array([1.0, 1.0, 2.0])
    charge = np.array([0.0, 1.0, 1.0])
    kf, kr = 0.8, 0.2
    sol = _integrate_network(S, lambda y: np.array([kf*y[0]*y[1], kr*y[2]]), np.array([0.55,0.45,0.0]))
    b = baryon @ sol.y
    q = charge @ sol.y
    checks = {
        "stoichiometric_baryon_conservation": np.allclose(baryon @ S, 0.0),
        "stoichiometric_charge_conservation": np.allclose(charge @ S, 0.0),
        "trajectory_baryon_conservation": np.max(np.abs(b-b[0])) < 1e-8,
        "trajectory_charge_conservation": np.max(np.abs(q-q[0])) < 1e-8,
        "abundances_nonnegative": bool(np.all(sol.y >= -1e-10)),
    }
    return _result("E", checks, {"final_abundances": sol.y[:, -1].tolist()}, "Manufactured reversible reaction-network case; actual rates and species must be source-derived.")


def check_F() -> dict[str, Any]:
    # e + p <-> H; charges [-1,+1,0]
    S = np.array([[-1.0,1.0],[-1.0,1.0],[1.0,-1.0]])
    charge = np.array([-1.0,1.0,0.0])
    sol = _integrate_network(S, lambda y: np.array([0.6*y[0]*y[1],0.1*y[2]]), np.array([0.4,0.4,0.2]))
    q = charge @ sol.y
    checks = {
        "reaction_preserves_charge": np.allclose(charge @ S, 0.0),
        "neutrality_preserved": np.max(np.abs(q)) < 1e-9,
        "composition_nonnegative": bool(np.all(sol.y >= -1e-10)),
        "restart_state_finite": bool(np.all(np.isfinite(sol.y[:, -1]))),
    }
    return _result("F", checks, {"max_charge": float(np.max(np.abs(q))), "final_state": sol.y[:, -1].tolist()}, "Manufactured plasma persistence case.")


def check_G() -> dict[str, Any]:
    z = np.linspace(0, 20, 4001)
    xe = 1.0/(1.0 + np.exp(-(z-8.0)/0.8))
    opacity = 0.15 * xe * (1.0 + z)**0.5
    # optical depth from observer toward high z
    tau = np.concatenate([[0.0], np.cumsum((opacity[1:]+opacity[:-1])*0.5*np.diff(z))])
    visibility = np.exp(-tau) * opacity
    norm = np.trapezoid(visibility, z)
    g = visibility / norm
    checks = {
        "ionization_fraction_bounded": bool(np.all((xe >= 0) & (xe <= 1))),
        "optical_depth_monotone": bool(np.all(np.diff(tau) >= -1e-14)),
        "visibility_positive": bool(np.all(g >= 0)),
        "visibility_normalized": abs(float(np.trapezoid(g,z)) - 1.0) < 1e-10,
    }
    return _result("G", checks, {"visibility_peak_z": float(z[np.argmax(g)]), "normalization": float(np.trapezoid(g,z))}, "Manufactured recombination/visibility profile; actual histories must come from Module F parents.")


def check_HU() -> dict[str, Any]:
    A = np.array([[-0.2,0.05],[0.1,-0.3]])
    t1,t2 = 0.7,1.1
    T12 = expm(A*(t1+t2))
    comp = expm(A*t2) @ expm(A*t1)
    checks = {
        "semigroup_identity": np.allclose(T12,comp,atol=1e-12),
        "identity_at_zero": np.allclose(expm(A*0.0),np.eye(2)),
        "linear_superposition": np.allclose(expm(A*t1)@(np.array([1.,2.])+np.array([-.2,.4])), expm(A*t1)@np.array([1.,2.])+expm(A*t1)@np.array([-.2,.4])),
    }
    return _result("HU", checks, {"operator": expm(A*t1).tolist()}, "Manufactured universal linear-operator identities.")


def check_I() -> dict[str, Any]:
    t = np.linspace(0,10,2001)
    a = 1.0 + 0.1*t + 0.01*t*t
    adot = 0.1 + 0.02*t
    H = adot/a
    horizon = np.concatenate([[0.0],np.cumsum((1/a[1:]+1/a[:-1])*0.5*np.diff(t))])
    checks = {
        "scale_positive": bool(np.all(a>0)),
        "clock_monotone": bool(np.all(np.diff(t)>0)),
        "expansion_finite": bool(np.all(np.isfinite(H))),
        "horizon_monotone": bool(np.all(np.diff(horizon)>=-1e-14)),
        "kinematic_identity": np.max(np.abs(np.gradient(np.log(a),t)-H)) < 1e-4,
    }
    return _result("I", checks, {"final_scale":float(a[-1]),"final_horizon":float(horizon[-1])}, "Manufactured background-geometry kinematic case; it does not choose the RFC dynamical law.")


def check_HI() -> dict[str, Any]:
    A = np.array([[-0.2,0.05],[0.1,-0.3]])
    T = expm(A*0.8)
    background_map = np.diag([1.2,0.7])
    x=np.array([0.4,-0.2])
    instantiated = background_map @ T
    checks = {
        "domain_codomain_shape": instantiated.shape==(2,2),
        "composition_exact": np.allclose(instantiated@x, background_map@(T@x)),
        "parents_unmodified": np.allclose(T,expm(A*0.8)) and np.allclose(background_map,np.diag([1.2,0.7])),
    }
    return _result("HI", checks, {"instantiated_operator":instantiated.tolist()}, "Manufactured immutable operator-instantiation case.")


def check_J() -> dict[str, Any]:
    C=np.array([[1.0,0.35,0.1],[0.35,0.8,0.2],[0.1,0.2,0.5]])
    eig=np.linalg.eigvalsh(C)
    L=np.linalg.cholesky(C)
    rng=np.random.default_rng(20260805)
    samples=rng.standard_normal((20000,3))@L.T
    C_hat=np.cov(samples,rowvar=False)
    real_field=rng.standard_normal(64)
    spectrum=np.fft.rfft(real_field)
    rebuilt=np.fft.irfft(spectrum,n=64)
    checks={
        "covariance_symmetric":np.allclose(C,C.T),
        "covariance_psd":bool(np.all(eig>0)),
        "cholesky_reconstruction":np.allclose(L@L.T,C),
        "ensemble_self_consistency":np.max(np.abs(C_hat-C))<0.03,
        "finite_field_reality":np.allclose(rebuilt,real_field),
    }
    return _result("J",checks,{"covariance_eigenvalues":eig.tolist(),"sample_cov_max_error":float(np.max(np.abs(C_hat-C))),"seed":20260805},"Manufactured covariance and finite-volume field case; seed is provenance, never selected for observational agreement.")


def _pairwise_acc(x: NDArray[np.float64], m: NDArray[np.float64], eps: float=0.05) -> NDArray[np.float64]:
    n=len(m); a=np.zeros_like(x)
    for i in range(n):
        for k in range(i+1,n):
            r=x[k]-x[i]
            inv=(float(r@r)+eps*eps)**(-1.5)
            f=r*inv
            a[i]+=m[k]*f
            a[k]-=m[i]*f
    return a


def _energy(x: NDArray[np.float64],v: NDArray[np.float64],m: NDArray[np.float64],eps:float=0.05)->float:
    ke=float(np.sum(0.5*m[:,None]*v*v)); pe=0.0
    for i in range(len(m)):
        for k in range(i+1,len(m)):
            pe-=m[i]*m[k]/math.sqrt(float(np.sum((x[k]-x[i])**2))+eps*eps)
    return ke+pe


def check_K() -> dict[str, Any]:
    x=np.array([[-1.,0.],[1.,0.],[0.,1.2]])
    v=np.array([[0.,0.22],[0.,-0.22],[-0.15,0.]])
    m=np.array([1.0,1.0,0.7])
    a=_pairwise_acc(x,m)
    net=np.sum(m[:,None]*a,axis=0)
    dt=2e-4; steps=5000; e0=_energy(x,v,m); p0=np.sum(m[:,None]*v,axis=0)
    for _ in range(steps):
        v+=0.5*dt*_pairwise_acc(x,m); x+=dt*v; v+=0.5*dt*_pairwise_acc(x,m)
    e1=_energy(x,v,m); p1=np.sum(m[:,None]*v,axis=0)
    checks={
        "pairwise_momentum_antisymmetry":np.linalg.norm(net)<1e-12,
        "global_momentum_conserved":np.linalg.norm(p1-p0)<1e-10,
        "leapfrog_energy_control":abs((e1-e0)/e0)<2e-6,
        "state_finite":bool(np.all(np.isfinite(x)) and np.all(np.isfinite(v))),
    }
    return _result("K",checks,{"relative_energy_drift":float(abs((e1-e0)/e0)),"momentum_error":float(np.linalg.norm(p1-p0))},"Manufactured softened pairwise nonlinear-gravity check; actual Module K requires the RFC field/metric law, lightcones, and lensing products.")


def check_L() -> dict[str, Any]:
    rho=np.array([1.0,0.7,1.4,0.9])
    flux=np.array([0.2,-0.1,0.05,-0.15])
    dt=0.1
    rho_new=rho-dt*(np.roll(flux,-1)-flux)
    weights=np.exp(-np.array([0.1,0.4,1.0,2.0]))
    birth=weights/weights.sum()
    checks={
        "finite_volume_mass_conservation":abs(float(rho_new.sum()-rho.sum()))<1e-12,
        "density_positive":bool(np.all(rho_new>0)),
        "generated_birth_measure_normalized":abs(float(birth.sum())-1.0)<1e-14,
        "generated_birth_measure_positive":bool(np.all(birth>0)),
    }
    return _result("L",checks,{"mass_before":float(rho.sum()),"mass_after":float(rho_new.sum()),"birth_measure":birth.tolist()},"Manufactured conservation and internally generated birth-measure check. The recovered Module L architecture remains limited to its exact verified scope until executed from physical K.")


def check_M() -> dict[str, Any]:
    # A+A -> B, B+A -> C with conserved nucleon count [1,2,3]
    S=np.array([[-2.,-1.],[1.,-1.],[0.,1.]])
    count=np.array([1.,2.,3.])
    sol=_integrate_network(S,lambda y:np.array([0.3*y[0]**2,0.2*y[1]*y[0]]),np.array([1.,0.,0.]),t1=3.0)
    total=count@sol.y
    checks={
        "stoichiometric_species_count":np.allclose(count@S,0.0),
        "trajectory_species_count":np.max(np.abs(total-total[0]))<1e-8,
        "nonnegative_composition":bool(np.all(sol.y>=-1e-10)),
        "return_packet_finite":bool(np.all(np.isfinite(sol.y[:,-1]))),
    }
    return _result("M",checks,{"final_composition":sol.y[:,-1].tolist()},"Manufactured composition network; no public abundance pattern is used.")


def _classify_scalar_map(f: Callable[[float],float],x0:float,n:int=1000,tol:float=1e-10)->str:
    xs=[x0]
    for _ in range(n): xs.append(float(f(xs[-1])))
    if abs(xs[-1]-xs[-2])<tol: return "FIXED_POINT"
    for period in range(2,9):
        if len(xs)>2*period and max(abs(xs[-k]-xs[-k-period]) for k in range(1,period+1))<tol:
            return f"FINITE_CYCLE_{period}"
    if not math.isfinite(xs[-1]) or abs(xs[-1])>1e12: return "DIVERGENT_OR_NONCONVERGENT"
    return "UNRESOLVED_OR_ATTRACTOR"


def check_KLM() -> dict[str, Any]:
    c1=_classify_scalar_map(lambda x:0.4*x+0.2,1.7)
    c2=_classify_scalar_map(lambda x:1.0-x,0.2)
    c3=_classify_scalar_map(lambda x:2.0*x+1.0,0.1)
    checks={
        "fixed_point_detected":c1=="FIXED_POINT",
        "finite_cycle_detected":c2=="FINITE_CYCLE_2",
        "nonconvergence_preserved":c3=="DIVERGENT_OR_NONCONVERGENT",
        "classifier_does_not_force_fixed_point":len({c1,c2,c3})==3,
    }
    return _result("KLM",checks,{"contraction":c1,"two_cycle":c2,"divergent":c3},"Manufactured recurrence classifier covering allowed outcome classes.")


def check_N() -> dict[str, Any]:
    edges=[("A","B"),("B","C"),("C","D"),("D","E"),("E","F"),("F","G"),("G","HU"),("G","I"),("HU","HI"),("I","HI"),("HI","J"),("J","K"),("K","L"),("L","M"),("K","KLM"),("L","KLM"),("M","KLM"),("KLM","N")]
    g=nx.DiGraph(edges)
    required={"A","B","C","D","E","F","G","HU","I","HI","J","K","L","M","KLM","N"}
    reachable=nx.descendants(g,"A")|{"A"}
    sector=np.array([2.3,1.1,0.6,-0.2]); global_total=float(sector.sum())
    checks={
        "single_connected_causal_graph":required<=reachable,
        "acyclic_execution_graph":nx.is_directed_acyclic_graph(g),
        "all_material_sectors_present":len(sector)==4,
        "global_budget_finite":math.isfinite(global_total),
    }
    return _result("N",checks,{"reachable_nodes":sorted(reachable),"global_budget":global_total},"Manufactured global lineage/compatibility case; directory co-location is not sufficient for real Module N.")


def check_O() -> dict[str, Any]:
    packet={"universe":"U0","predictions":[1.2,3.4],"falsifiers":["F1"]}
    encoded=json.dumps(packet,sort_keys=True,separators=(",",":")).encode()
    h1=hashlib.sha256(encoded).hexdigest(); h2=hashlib.sha256(encoded).hexdigest()
    mutated=dict(packet); mutated["predictions"]=[1.2,3.5]
    hm=hashlib.sha256(json.dumps(mutated,sort_keys=True,separators=(",",":")).encode()).hexdigest()
    checks={"repeat_hash_stable":h1==h2,"mutation_changes_hash":h1!=hm,"hash_length":len(h1)==64}
    return _result("O",checks,{"frozen_hash":h1,"mutated_hash":hm},"Manufactured immutable packet check.")


def check_P() -> dict[str, Any]:
    prediction=np.array([1.0,1.4,0.8]); frozen=hashlib.sha256(prediction.tobytes()).hexdigest()
    synthetic_data=np.array([1.1,1.2,0.9]); cov=np.array([[0.04,0.01,0.],[0.01,0.09,0.],[0.,0.,0.025]])
    inv=np.linalg.inv(cov); r=synthetic_data-prediction; chi2=float(r@inv@r)
    unchanged=hashlib.sha256(prediction.tobytes()).hexdigest()==frozen
    checks={"covariance_psd":bool(np.all(np.linalg.eigvalsh(cov)>0)),"statistic_finite":math.isfinite(chi2),"frozen_prediction_unchanged":unchanged,"no_target_deletion":len(r)==3}
    return _result("P",checks,{"chi_square":chi2,"prediction_hash":frozen},"Synthetic-data comparison harness only. Real public data are forbidden until Module O is frozen and Module P is authorized.")


def check_Q() -> dict[str, Any]:
    terminal={"energy":1.0,"route_memory":["r1","r2"],"branch":"b0"}
    memory={"qualified_energy":terminal["energy"],"routes":tuple(terminal["route_memory"]),"branch_trace":terminal["branch"]}
    source={"modal_capacity":"CIF","admitted_possibilities":None}
    cls=_classify_scalar_map(lambda x:0.5*x+0.1,3.0)
    checks={"memory_is_not_source_object":set(memory)!=set(source),"terminal_information_preserved":memory["qualified_energy"]==terminal["energy"],"route_memory_preserved":memory["routes"]==tuple(terminal["route_memory"]),"terminal_map_classified":cls=="FIXED_POINT"}
    return _result("Q",checks,{"classification":cls,"qualified_memory":memory},"Manufactured terminal-memory case; it forbids identifying an RFL memory packet with a new CIF.")


CHECKS: dict[str, Callable[[], dict[str, Any]]] = {
    "A":check_A,"B":check_B,"C":check_C,"D":check_D,"E":check_E,"F":check_F,"G":check_G,
    "HU":check_HU,"I":check_I,"HI":check_HI,"J":check_J,"K":check_K,"L":check_L,"M":check_M,
    "KLM":check_KLM,"N":check_N,"O":check_O,"P":check_P,"Q":check_Q,
}


def run(module: str) -> dict[str, Any]:
    try:
        return CHECKS[module]()
    except KeyError as exc:
        raise ValueError(f"unknown module: {module}") from exc


def run_all() -> dict[str, Any]:
    results={m:CHECKS[m]() for m in CHECKS}
    return {"overall":"PASS" if all(x["overall"]=="PASS" for x in results.values()) else "FAIL","results":results}
