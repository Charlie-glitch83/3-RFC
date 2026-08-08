# Module E → Module F Scientific Handoff

## Purpose

This file seals the physical boundary between primordial nuclear formation in Module E and long-duration post-nuclear plasma evolution in Module F.

It defines only:

- what completed Module E must export;
- which Module E branches are admissible for post-nuclear evolution;
- which nuclear, thermal, radiative, plasma, perturbative, dark-sector, memory, and uncertainty objects Module F inherits unchanged;
- which residual reactions and decays Module F must continue;
- how Module F reaches atomic-capture readiness without prematurely solving recombination;
- the exact physical state Module F must eventually pass to Module G.

It does not import the former run system, lifecycle machinery, status taxonomies, source-register bureaucracy, acceptance paperwork, or certificate architecture.

---

# 1. Boundary statement

Module E owns the isotope-resolved primordial nuclear history.

Module F owns the continuous physical persistence and evolution of that post-nuclear universe into a recombination-ready plasma.

The boundary is:

```text
Module E:
nuclear species and properties,
reaction graph and rates,
isotope abundance histories,
freeze-out and late-decay instructions,
post-nuclear plasma composition

                     ↓

Module F:
composition-preserving expansion,
residual reactions and decays,
photon and neutrino persistence,
ion-electron-radiation thermal evolution,
plasma transport, opacity, perturbations,
atomic-state readiness
```

Therefore:

```text
primordial abundance freeze-out != end of all nuclear activity
post-nuclear composition != recombination initial condition by itself
stable isotope abundance != complete plasma state
atomic-state admissibility != completed recombination
opacity readiness != visibility function
recombination-entry surface != last-scattering surface
```

Module F must physically evolve the interval between nuclear freeze-out and the beginning of nonequilibrium atomic recombination.

---

# 2. Module E scientific export

For each admitted Module E branch `epsilon` descending from the Module D branch `delta`, define:

```text
P_E->F(beta,gamma,delta,epsilon) = (
  G_E,
  T_E,
  A_E,
  Rho_E,
  P_E,
  Sth_E,
  Scomp_E,
  Y_E(t),
  Y_E^out,
  SigmaY_E,
  Iso_E,
  Reac_E,
  Decay_E,
  Freeze_E,
  Np_E,
  Ne_E,
  Fgamma_E,
  Fnu_E,
  Fe_E,
  Plasma_E,
  Q_E,
  Dark_E,
  Pert_E,
  Spatial_E,
  Sigma_E,
  Mrec_E,
  Anc_E,
  Restart_E
)
```

where:

- `G_E` is the inherited and nuclear-era geometry/background state;
- `T_E` is the physical-time and temperature continuation;
- `A_E` is the early scale and expansion history;
- `Rho_E` and `P_E` are sector-resolved energy-density and pressure histories;
- `Sth_E` is thermodynamic entropy and transfer history;
- `Scomp_E` is nuclear compositional entropy;
- `Y_E(t)` is the complete isotope abundance history;
- `Y_E^out` is the terminal post-nuclear composition;
- `SigmaY_E` is the abundance covariance;
- `Iso_E` is the nuclear species and property registry;
- `Reac_E` is the directed forward/reverse reaction graph and rate law;
- `Decay_E` is the radioactive and unstable-species decay registry;
- `Freeze_E` is the species- and channel-resolved freeze-out state;
- `Np_E` is the free proton, neutron, and nuclear-reactant residual state;
- `Ne_E` is the electron, positron, ion, and charge-neutrality state;
- `Fgamma_E`, `Fnu_E`, and `Fe_E` are photon, neutrino, and charged-lepton distributions;
- `Plasma_E` is the screening, transport, conductivity, and collective-plasma state;
- `Q_E` is the baryon, charge, lepton, energy, and normalization ledger;
- `Dark_E` is the inherited visible-dark interaction state;
- `Pert_E` is the background-compatible perturbation and covariance state;
- `Spatial_E` is any material inhomogeneity, magnetic, vortical, turbulent, shock, or defect state;
- `Sigma_E` is the complete physical, rate, branch, and numerical uncertainty state;
- `Mrec_E` is nuclear and recursive memory;
- `Anc_E` is complete ancestry through Modules D, C, B, and A;
- `Restart_E` is the complete physical continuation state.

All objects remain branch-specific unless Module E proves physical equivalence.

---

# 3. Conditions for Module F admission

Module F may begin only on a Module E branch satisfying all of the following:

1. the nuclear branch is not obstructed;
2. the isotope registry is complete over the claimed precision domain;
3. isotope abundances are positive and normalized;
4. baryon, charge, nucleon, energy, and abundance ledgers close;
5. every material reaction has a declared forward, reverse, frozen, or conditionally active status;
6. every unstable species has a decay or conversion law;
7. free proton, neutron, electron, ion, photon, and neutrino states are explicit;
8. the photon and neutrino distributions have not been collapsed below the fidelity needed downstream;
9. the post-nuclear background, entropy, and expansion state are explicit;
10. all authorized visible-dark exchanges are explicit;
11. material spatial or nonthermal structure has not been discarded;
12. abundance covariance and cross-sector uncertainty remain attached;
13. source, route, reaction, isotope, branch, scale, and memory ancestry are recoverable;
14. no public abundance, recombination redshift, CMB normalization, ionization history, or visibility curve has entered generation.

A missing required field is a Module E or interface defect. Module F may not replace it with a conventional post-BBN initial condition.

If no admissible Module E branch exists, the universe is obstructed at the E→F boundary.

---

# 4. Quantities inherited unchanged

Module F inherits without redefining:

- universe and cycle identity;
- Big-Implosion ancestry;
- physical-time origin;
- the complete isotope registry;
- terminal primordial abundances and covariance;
- isotope reaction ancestry;
- nuclear masses, charges, bindings, and decay identities;
- the reaction and freeze-out history;
- baryon and charge ledgers;
- free proton and neutron residuals;
- photon, neutrino, electron, positron, and ion identities;
- post-nuclear photon and neutrino distributions;
- the generated baryon-photon state;
- the generated background and equation-of-state state;
- visible-dark coupling permissions;
- perturbation, branch, uncertainty, and recursive-memory state.

Module F may evolve these objects through lawful residual reactions, decays, transport, expansion, thermal exchange, and atomic activation. It may not reset them.

---

# 5. Composition persistence and lawful change

For a stable nuclear species `i` after its active nuclear routes close:

```text
Y_i = n_i / n_B

dY_i/dt = 0
```

apart from explicitly represented late decay, capture, photodissociation, conversion, injection, or other lawful events.

For number density:

```text
dn_i/dt + 3H n_i = C_i^res + D_i^late + I_i
```

where every nonzero term must identify:

- the originating route;
- the destination state;
- the rate law;
- conservation pairing;
- uncertainty;
- branch and ancestry.

Composition change without an admitted event is forbidden.

---

# 6. Residual reaction and decay continuation

Module E freeze-out is species- and channel-specific.

Module F must continue every process whose rate, accumulated flux, energy release, or later activation is material over the post-nuclear interval.

Each residual route must be classified through a generated rate comparison such as:

```text
R_r(t) = Gamma_r(t) / H(t)
```

and through an integrated effect on:

- isotope abundance;
- free-electron or ion state;
- photon spectrum;
- plasma temperature;
- entropy;
- perturbations;
- Module G readiness.

A route may be retired only when its effect is bounded below the declared scientific tolerance.

---

# 7. Continuous background, time, and scale

Module F continues the same physical chronology produced by Modules B-E.

It inherits and evolves:

```text
t_phys,
eta,
a,
H,
rho,
p,
T_s,
n_s,
mu_s
```

for every represented species and sector.

The post-nuclear time-temperature-density-scale relation must be generated from the inherited state and conservation law. It may not be replaced by a standard cosmological table.

Kernel depth, reaction depth, physical time, conformal time, scale, and cycle index remain distinct.

---

# 8. Kinetic, fluid, and multifluid continuation

Module E may export kinetic distributions, moment states, fluid states, or a mixture of representations.

Module F must preserve enough information to use:

- full phase-space evolution;
- moment hierarchies;
- multifluid plasma evolution;
- single-fluid reduction;
- background-only reduction where rigorously sufficient.

Any promotion or reduction must preserve all material conserved quantities, moments, covariance, branch identity, and ancestry.

A fluid approximation may not erase a material spectral tail, velocity slip, anisotropic stress, or composition distinction.

---

# 9. Photon and neutrino continuity

Module F receives complete photon and neutrino states, not only temperatures.

It must preserve and evolve, where material:

- occupation and spectral distributions;
- energy and number density;
- polarization state;
- chemical-potential-like distortions;
- decay or injection features;
- neutrino flavor and propagation state;
- neutrino anisotropic stress;
- free-streaming state;
- covariance and ancestry.

A scalar effective-radiation quantity may be derived as a reduction, but it may not replace the underlying state when that state affects Module G or H.

---

# 10. Plasma, charge, and electromagnetic continuity

Module F inherits the exact global charge state and any material local charge structure.

It must evolve:

- global charge closure;
- local quasineutrality;
- finite Debye-scale charge separation;
- plasma frequency;
- screening length;
- collision frequencies;
- conductivity and resistivity;
- diffusion and thermal conduction;
- electromagnetic fields where present;
- charge-transfer routes;
- numerical charge residual.

A neutrality scalar is insufficient when local plasma dynamics are material.

---

# 11. Atomic-state boundary

Module E exports nuclei, electrons, photons, and the physical laws from which atomic states may become admissible.

Module F owns:

- construction of the atomic carrier and transition seed registry;
- atomic scale promotion and ionization refinement maps;
- rate-based detection that atomic states are becoming dynamically relevant;
- the complete recombination-entry surface.

Module G owns:

- nonequilibrium atomic level-population histories;
- full hydrogen and helium recombination;
- line and continuum radiative feedback;
- optical-depth integration;
- visibility and drag functions;
- physical last-scattering and baryon-drag surfaces.

Therefore Module F may prepare atomic carriers but may not use an equilibrium ionization formula as the final recombination solution.

---

# 12. Perturbation, field, and dark-sector continuity

Module F inherits every material perturbation, magnetic, vortical, turbulent, shock, defect, compression-relic, and dissipative-tail state.

It must evolve or rigorously bound their effects on:

- plasma stability;
- thermal coupling;
- opacity;
- diffusion and damping;
- atomic activation;
- photon and neutrino transport;
- the Module G entry surface.

No such state may be added merely because it improves later agreement.

The dark sectors may not act as free residual sinks or sources.

---

# 13. Entropy and memory typing

Module F must preserve distinct ledgers for:

```text
S_th       thermodynamic entropy
S_gamma    photon entropy
S_nu       neutrino/decoupled-sector entropy
S_comp     compositional entropy
S_rec      recursive depth and ancestry memory
```

Representation reduction must also record any information discarded and prove that it is not materially required downstream.

Recursive memory is not heat and cannot close a thermodynamic residual without a derived physical coupling.

---

# 14. Branch handling and obstruction

For every admitted Module E branch, Module F may produce:

- one unique post-nuclear plasma history;
- a representation-equivalent family;
- multiple physically distinct histories;
- obstruction.

Distinct late-decay, residual-reaction, thermal-coupling, spectral-distortion, magnetic, dark-sector, or atomic-readiness branches remain distinct unless a physical equivalence theorem is proved.

Module F may not choose a branch because it resembles a public ionization or CMB history.

Failed conservation, negative distributions, missing material transport, inconsistent representation overlap, or inability to form a complete Module G parent is an obstruction rather than a reason to retune Module E.

---

# 15. Required Module F output to Module G

Module F must eventually export:

```text
P_F->G = (
  restart time and coordinate registry,
  background and geometry state,
  isotope and persistent-composition state,
  ionic charge-state seeds,
  free-electron and residual-positron distributions,
  photon distribution and spectral-distortion state,
  neutrino and decoupled-species state,
  matter, electron, ion, photon, and neutrino temperatures,
  chemical potentials,
  plasma properties and electromagnetic constraints,
  opacity and scattering registry,
  photon-baryon drag and thermal-coupling state,
  sound-speed, diffusion, conduction, viscosity, and damping state,
  atomic carrier, level, continuum, and transition seed registries,
  atomic promotion and ionization maps,
  recombination-readiness surface and witnesses,
  perturbation and covariance state,
  magnetic or spatial structure where active,
  visible-dark interaction state,
  residual reaction and late-decay state,
  thermodynamic, radiative, compositional, and recursive-memory ledgers,
  uncertainty and covariance,
  route, event, branch, isotope, atomic, scale, and source ancestry,
  restartable physical state
)
```

Module G must not need to reconstruct an omitted post-nuclear history or import a public recombination state.

---

# 16. Concatenated E→F theorem target

The Module E and Module F plans concatenate coherently when the following statement can be earned:

> Module E supplies a complete isotope-resolved post-nuclear universe whose abundance histories, terminal composition, reaction and decay routes, freeze-out states, photon, neutrino, charged-particle, plasma, background, entropy, dark-sector, perturbation, uncertainty, memory, and ancestry states are frozen. Module F preserves every stable nuclear identity except through explicit witnessed residual events, continuously evolves the same universe through expansion, thermal exchange, plasma transport, photon and neutrino persistence, opacity, acoustic and diffusive evolution, perturbation transport, and atomic-state activation, and exports a physically witnessed recombination-ready state without resetting the primordial composition, importing a standard post-BBN background, or assuming a public recombination history.

This boundary makes Module F the continuity and plasma child of Module E rather than a readiness wrapper around an incomplete nuclear state.