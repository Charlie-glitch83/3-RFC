# Module D → Module E Scientific Handoff

## Purpose

This file seals the physical boundary between the completed early thermal history of Module D and the primordial nuclear reaction network of Module E.

It defines only:

- what Module D must export;
- which Module D branches are admissible for nuclear evolution;
- which quantities Module E inherits unchanged;
- which nuclear quantities Module E must derive rather than assume;
- how the neutron–proton, photon, neutrino, plasma, entropy, expansion, and dark-sector histories continue into nuclear formation;
- the exact state Module E must eventually pass to Module F.

It does not import the former run system, gate taxonomy, source-register bureaucracy, acceptance paperwork, or certification machinery.

---

# 1. Boundary statement

Module D owns the physical nonequilibrium thermal history from the Module C microscopic universe to a nuclear-reaction-ready plasma.

Module E owns the formation, destruction, interconversion, freeze-out, and survival of primordial nuclei through a reaction-resolved network.

The boundary is:

```text
Module D:
thermal distributions, weak history, phase transitions,
annihilation, freeze-out, neutrino transport,
photon heating, entropy redistribution,
baryon-photon state, nuclear-readiness surface

                     ↓

Module E:
nuclear species, masses and binding,
reaction graph, forward/reverse rates,
deuterium bottleneck, stiff abundance evolution,
freeze-out, isotope ancestry, post-nuclear composition
```

Therefore:

```text
nuclear-readiness surface != solved nucleosynthesis
neutron/proton history != final isotope composition
deuterium admissibility != deuterium abundance history
reaction-rate law != integrated reaction flux
baryon-photon state != primordial abundance vector
thermal freeze-out != nuclear freeze-out
```

Module E must generate the nuclear history from the Module D state.

---

# 2. Module D scientific export

For each admitted Module D branch `delta` descending from Module C branch `gamma` and Module B branch `beta`, define:

```text
P_D->E(beta,gamma,delta) = (
  G_D,
  T_D,
  A_D,
  Rho_D,
  P_D,
  Sth_D,
  Fgamma_D,
  Fnu_D,
  Fe_D,
  Fp_D,
  Fn_D,
  Wnp_D,
  EtaB_D,
  EtaL_D,
  Mu_D,
  Gstar_D,
  GstarS_D,
  Plasma_D,
  Dark_D,
  Inhom_D,
  Sigma_D,
  Mrec_D,
  Anc_D
)
```

where:

- `G_D` is the inherited and early-evolved geometry/background state used over the nuclear domain;
- `T_D` is the continuous physical-time and temperature history;
- `A_D` is the early scale/expansion history;
- `Rho_D` is the total and sector-resolved energy-density history;
- `P_D` is the total and sector-resolved pressure history;
- `Sth_D` is the thermodynamic entropy and transfer history;
- `Fgamma_D` is the photon phase-space distribution and spectrum;
- `Fnu_D` is the flavor-resolved neutrino and antineutrino distribution state;
- `Fe_D` is the electron and positron distribution state;
- `Fp_D` is the free-proton distribution and density state;
- `Fn_D` is the free-neutron distribution and density state;
- `Wnp_D` is the complete neutron–proton interconversion, weak freeze-out, and neutron-decay history;
- `EtaB_D` is the generated baryon-photon state and its history;
- `EtaL_D` is the generated lepton-asymmetry state and its history;
- `Mu_D` is the chemical-potential and conserved-charge state;
- `Gstar_D` and `GstarS_D` are the generated relativistic energy and entropy degrees-of-freedom histories;
- `Plasma_D` is the screening, transport, conductivity, diffusion, and collective-plasma state;
- `Dark_D` is the inherited visible-dark coupling and transfer state;
- `Inhom_D` is any generated spatial variation, nonthermal tail, defect, magnetic, vortical, turbulent, or shock state that remains material;
- `Sigma_D` is the complete parent covariance and branch uncertainty;
- `Mrec_D` is the protected thermal and recursive-memory state;
- `Anc_D` is complete ancestry through Modules C, B, and A.

All objects remain branch-specific unless physical equivalence has been proved.

---

# 3. Nuclear-readiness surface

Module D must define a physical nuclear-entry surface:

```text
Sigma_E,in = {
  t,
  a,
  T_gamma,
  T_nu,
  H_or_background_rate,
  rho,
  p,
  s,
  f_a,
  mu_a,
  n_n,
  n_p,
  eta_B,
  eta_L,
  g_star,
  g_starS,
  plasma state,
  dark-sector state,
  covariance,
  memory
}_{t=t_E,in}
```

The surface is admissible only when:

1. proton and neutron states are physically defined;
2. the weak interconversion and neutron-decay laws are active and continuous;
3. photon, neutrino, electron, and positron distributions are explicit;
4. the baryon-photon and charge-neutrality states close;
5. the thermal background and expansion variables are explicit;
6. all material energy and entropy transfers are represented;
7. authorized dark-sector effects are explicit;
8. inherited inhomogeneity and nonthermal structure are explicit;
9. conservation and covariance close;
10. Module E can initialize without inventing a missing physical quantity.

The nuclear-entry surface is selected by physical readiness of the generated state, not by inserting a conventional temperature or time.

---

# 4. Quantities inherited unchanged

Module E inherits without redefining:

- universe and cycle identity;
- Big-Implosion ancestry;
- physical-time origin;
- Module C proton and neutron identities;
- particle, antiparticle, photon, neutrino, electron, and positron identities;
- microscopic charge and interaction laws;
- Module D thermal distributions and histories up to the entry surface;
- the neutron–proton conversion law and accumulated history;
- neutron-decay law;
- generated baryon and lepton asymmetries;
- generated baryon-photon state;
- chemical-potential and charge state;
- generated equation-of-state and expansion history;
- authorized visible-dark couplings;
- uncertainty, branch identity, memory, and ancestry.

Module E may continue and couple these quantities through the nuclear era, but it may not replace them with public reference values.

---

# 5. Nuclear quantities Module E must derive

Module D does not supply a solved nuclear universe.

Module E must derive:

- the admitted isotope registry;
- nuclear masses and binding energies not already fully derived by Module C;
- spin, parity, excited-state, and partition-function data at the declared scope;
- nuclear decay and threshold registry;
- the channel-complete directed reaction graph;
- microscopic or effective reaction-rate laws;
- reverse reactions and detailed-balance relations;
- deuterium bottleneck release;
- reaction onset and branch competition;
- coupled abundance trajectories;
- species-specific freeze-out and late-decay state;
- nuclear energy release and feedback;
- isotope-resolved ancestry;
- abundance covariance and channel sensitivities;
- the persistent post-nuclear composition.

Module E may use a nuclear interface only when its status and uncertainty are explicit. An interface value is not a triad-derived nuclear theorem.

---

# 6. Continuity of weak and neutron history

Module E must continue, not restart, the Module D weak history.

The inherited neutron and proton state includes:

- number densities and distributions;
- weak conversion rates;
- neutrino spectral corrections;
- electron and positron distributions;
- neutron-decay state;
- expansion competition;
- covariance.

The state entering nuclear formation must satisfy:

```text
(n_n, n_p)_E,in = continuation of (n_n, n_p)_D
```

No hand-assigned neutron-to-proton ratio is permitted.

The nuclear network must couple nuclear capture and release to the same free-neutron and free-proton reservoirs.

---

# 7. Photon, neutrino, plasma, and entropy continuity

Module E inherits the full distribution state rather than only scalar temperatures.

It must preserve and update where material:

- photon photodisintegration tail;
- photon heating from nuclear binding release;
- neutrino spectral and energy-transfer effects;
- electron and positron distributions;
- Coulomb screening;
- plasma dispersion;
- finite-density and nonideal equation-of-state effects;
- entropy production and transfer;
- expansion/background feedback.

A fixed background approximation may be used only after a quantified sufficiency argument.

---

# 8. Spatial and nonequilibrium continuity

If Module D exports:

- baryon inhomogeneity;
- sector-dependent temperatures;
- nonthermal particle tails;
- defects;
- turbulence;
- shocks;
- magnetic structure;
- local dark-sector injection;

Module E must test whether a homogeneous one-zone network remains sufficient.

It may coarse-grain only when the abundance-relevant effect is below the declared scientific tolerance and the no-loss conditions are satisfied.

Otherwise Module E must solve a transport-reaction system.

---

# 9. Dark-sector continuity

Module E may evolve only the visible-dark effects authorized by Modules B-D.

It must maintain separate ledgers for:

- expansion/background effect;
- visible-dark energy transfer;
- baryon-density modification;
- neutrino-sector modification;
- reaction-threshold modification;
- nonthermal injection;
- spatial effects.

The dark sector may not be introduced or adjusted to repair an abundance residual.

If a dark-sector microscopic identity remains unresolved, Module E may use only the frozen effective interface inherited from Module D.

---

# 10. Entropy and memory typing

Module E must preserve the distinction among:

```text
S_th      thermodynamic entropy
S_comp    nuclear compositional entropy
S_rec     recursive depth/memory entropy
```

Thermodynamic entropy tracks physical heat and irreversible transfer.

Compositional entropy tracks the distribution among nuclear species under a declared normalization.

Recursive memory tracks protected ancestry and inherited relational structure.

None may be used as an undeclared substitute for another.

---

# 11. Branch handling and obstruction

For every admitted Module D branch, Module E may produce:

- one unique nuclear history;
- a gauge- or representation-equivalent family;
- multiple physically distinct nuclear branches;
- obstruction.

Distinct reaction onset, resonance, inhomogeneity, dark-sector, or network branches remain distinct unless a physical equivalence theorem is proved.

Module E may not choose a branch because its abundances resemble public measurements.

A missing material reaction channel, failed conservation law, inconsistent reverse rate, negative abundance, or nonconvergent network is a physical or numerical obstruction rather than a reason to retune the parent state.

---

# 12. Required Module E output to Module F

Module E must eventually export:

```text
P_E->F = (
  physical-time and background continuation,
  full isotope registry,
  isotope abundance trajectories,
  terminal isotope composition and covariance,
  free proton and neutron residuals,
  electron and ion number densities,
  charge-neutrality state,
  photon distribution and temperature state,
  neutrino distributions and temperatures,
  reaction graph and rate registry,
  reaction freeze-out surfaces,
  residual reaction channels,
  radioactive species and decay schedule,
  nuclear energy-release and heat-transfer history,
  thermodynamic and compositional entropy state,
  visible-dark interaction history,
  spatial variation and transport state where represented,
  isotope reaction ancestry,
  branch and recursive memory,
  uncertainty and covariance,
  restartable physical state
)
```

Module F must not need to rerun primordial nucleosynthesis or infer the composition from an abundance label.

---

# 13. Concatenated D→E theorem target

The Module D and Module E plans concatenate coherently when the following statement can be earned:

> Module D supplies a continuous nuclear-reaction-ready plasma whose physical-time, temperature, expansion, photon, neutrino, electron, positron, proton, neutron, weak-rate, baryon-photon, charge, entropy, plasma, dark-sector, uncertainty, memory, and ancestry states are generated and frozen. Module E preserves that parent, derives a channel-complete nuclear species and reaction system, dynamically opens the nuclear reaction era, evolves the coupled abundance network with forward and reverse consistency, carries weak and background feedback continuously, and exports an isotope-resolved post-nuclear plasma state without importing a public thermal history, assigned neutron-proton ratio, fitted reaction rate, or target abundance.

This boundary makes Module E the nuclear child of Module D rather than a replacement for missing thermal physics.