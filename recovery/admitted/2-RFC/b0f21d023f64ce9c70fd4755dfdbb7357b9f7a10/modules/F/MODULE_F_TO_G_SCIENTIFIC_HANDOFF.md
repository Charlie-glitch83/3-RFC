# Module F → Module G Scientific Handoff

## Purpose

This file seals the physical boundary between the recombination-ready plasma constructed by Module F and the nonequilibrium atomic recombination and CMB-surface physics owned by Module G.

It defines only:

- what completed Module F must export;
- which Module F branches are admissible for recombination;
- which plasma, atomic, radiative, perturbative, dark-sector, uncertainty, memory, and ancestry objects Module G inherits unchanged;
- which atomic and radiative quantities Module G must derive rather than assume;
- how primordial recombination remains distinct from late astrophysical reionization;
- the exact state Module G must eventually pass to Module H.

It does not import the former run system, lifecycle machinery, gate taxonomy, source-register bureaucracy, certificate architecture, or evidence paperwork.

---

# 1. Boundary statement

Module F owns the continuous post-nuclear plasma and the physically witnessed recombination-entry surface.

Module G owns the nonequilibrium formation of atomic states, the decline of free electrons, the generated opacity and optical-depth history, photon decoupling, baryon-drag release, and the finite physical CMB last-scattering structure.

The boundary is:

```text
Module F:
composition-preserving plasma evolution,
residual reactions and late decays,
photon and neutrino persistence,
plasma transport and thermal coupling,
atomic carrier activation,
recombination-entry surface

                     ↓

Module G:
multilevel atomic kinetics,
frequency-dependent radiative transfer,
free-electron history,
opacity and optical depth,
visibility function,
last-scattering and drag surfaces,
recombination radiation and transfer sources
```

Therefore:

```text
atomic carrier readiness != solved recombination
ionization seed != ionization history
opacity kernel != optical-depth history
transparency possibility != visibility function
visibility peak != complete last-scattering structure
photon decoupling != baryon-drag release
primordial recombination != late astrophysical reionization
```

Module G must generate the full recombination and decoupling history from the Module F state.

---

# 2. Module F scientific export

For each admitted Module F branch `phi` descending from Module E branch `epsilon`, define:

```text
P_F->G(beta,gamma,delta,epsilon,phi) = (
  G_F,
  Coord_F,
  Bkg_F,
  Comp_F,
  IonSeed_F,
  Electron_F,
  Positron_F,
  Photon_F,
  Neutrino_F,
  Temp_F,
  Chem_F,
  Plasma_F,
  OpacitySeed_F,
  DragSeed_F,
  Sound_F,
  Diffusion_F,
  Damping_F,
  Atomic_F,
  Transition_F,
  Residual_F,
  Pert_F,
  Field_F,
  Dark_F,
  Entropy_F,
  Sigma_F,
  Memory_F,
  Ancestry_F,
  Restart_F
)
```

where:

- `G_F` is the manifested geometry/pregeometry and background-coupling state active over the recombination domain;
- `Coord_F` is the physical-time, conformal-time, scale, temperature, and internally defined redshift-like coordinate registry;
- `Bkg_F` is the generated expansion, density, pressure, stress-energy, and horizon state;
- `Comp_F` is the complete isotope-resolved nuclear composition and covariance;
- `IonSeed_F` is the ionic charge-state and neutral-capture seed state;
- `Electron_F` and `Positron_F` are the free charged-lepton distributions and densities;
- `Photon_F` is the photon distribution, spectral-distortion state, angular moments, and polarization seed;
- `Neutrino_F` is the flavor-resolved neutrino and decoupled-species state;
- `Temp_F` is the matter, electron, ion, photon, neutrino, and active dark-sector temperature state;
- `Chem_F` is the chemical-potential and conserved-charge state;
- `Plasma_F` is the screening, plasma-frequency, collision, conductivity, viscosity, conduction, diffusion, and collective-mode state;
- `OpacitySeed_F` is the state-derived registry of material scattering and absorption channels available at the recombination boundary;
- `DragSeed_F` is the photon-baryon momentum and energy-coupling state;
- `Sound_F`, `Diffusion_F`, and `Damping_F` are the inherited pre-recombination acoustic and transport histories;
- `Atomic_F` is the atomic, ionic, level, continuum, and superlevel candidate registry;
- `Transition_F` is the capture, ionization, excitation, de-excitation, scattering, and radiative-transition seed graph;
- `Residual_F` is the late-decay and residual nuclear-reaction state;
- `Pert_F` is the baryon, electron, photon, neutrino, metric-interface, and dark-sector perturbation state;
- `Field_F` is any material magnetic, vortical, turbulent, shock, defect, or spatially inhomogeneous state;
- `Dark_F` is the inherited compression-relic and dissipative-tail coupling state;
- `Entropy_F` contains thermodynamic, radiative, compositional, and recursive-memory ledgers;
- `Sigma_F` is the complete physical, atomic-seed, transport, branch, and numerical covariance;
- `Memory_F` is the post-nuclear and plasma-persistence memory state;
- `Ancestry_F` is complete ancestry through Modules E, D, C, B, and A;
- `Restart_F` is the complete physical continuation state.

All objects remain branch-specific unless physical equivalence is proved.

---

# 3. Conditions for Module G admission

Module G may begin only on a Module F branch satisfying all of the following:

1. the branch is not obstructed;
2. the isotope-resolved composition is complete and persistent over the entry interval;
3. every active residual reaction or late decay is represented or explicitly exported;
4. electron, positron, photon, neutrino, ion, and nuclear states are restartable;
5. photon and neutrino distributions retain the frequency, angular, flavor, polarization, and covariance information required downstream;
6. matter, electron, ion, photon, neutrino, and active dark-sector temperatures are explicit;
7. charge, baryon, nuclear-identity, energy, and entropy ledgers close;
8. the plasma and electromagnetic state is explicit at the claimed fidelity;
9. the atomic and ionic candidate registry is complete over the declared precision domain;
10. transition and continuum seed laws are present or transparently marked as unresolved Module G obligations;
11. opacity and momentum-transfer seeds are derived from the inherited composition and interaction law;
12. perturbations and inherited field structures remain attached;
13. visible-dark coupling permissions are explicit;
14. uncertainty, branch identity, memory, and ancestry remain attached;
15. no public ionization history, recombination redshift, optical-depth curve, visibility function, CMB normalization, or public recombination-code state has entered generation.

A missing material field is a Module F or interface defect. Module G may not replace it with a conventional recombination initial condition.

If no admissible Module F branch exists, the universe is obstructed at the F→G boundary.

---

# 4. Recombination-entry surface

Module F must provide a physical entry surface:

```text
Sigma_G,in = {
  t,
  eta,
  a,
  z_F,
  H,
  rho,
  p,
  T_m,
  T_e,
  T_i,
  T_gamma,
  T_nu,
  f_gamma,
  f_nu,
  Y_isotope,
  n_b,
  n_e,
  ionic charge seeds,
  chemical potentials,
  plasma coefficients,
  opacity seeds,
  drag and diffusion state,
  atomic registry,
  transition seed graph,
  perturbations,
  dark state,
  covariance,
  memory
}_{entry}
```

The surface is selected when:

- post-nuclear composition is persistent;
- all material late events are active or explicitly scheduled;
- atomic bound states become dynamically competitive;
- capture, ionization, excitation, emission, absorption, scattering, and escape channels can be initialized;
- Module G can solve the atomic network without importing a public recombination constant or state history.

The entry surface is determined by the generated physical state, not by assigning a familiar redshift or temperature.

---

# 5. Quantities inherited unchanged

Module G inherits without redefining:

- universe and cycle identity;
- Big-Implosion ancestry;
- physical-time origin;
- the isotope registry and primordial abundances;
- nuclear masses, charges, and identities;
- particle and antiparticle identities;
- photon, neutrino, electron, positron, ion, and dark-sector identities;
- microscopic interaction and scattering laws;
- residual reaction and late-decay instructions;
- generated background and coordinate histories through the entry surface;
- generated photon and neutrino states;
- charge and chemical-potential state;
- plasma and transport state;
- perturbation and inherited-field state;
- visible-dark coupling permissions;
- uncertainty, branch, memory, and ancestry state.

Module G may evolve and refine these objects through atomic capture, ionization, radiation transfer, scattering, and decoupling. It may not reset them.

---

# 6. Atomic registry ownership

Module F opens the physically admissible atomic carrier and transition seed space.

Module G must refine it into the complete atomic and ionic system required by the claimed precision.

The minimum physical content includes, where material:

- hydrogen ionic, bound, continuum, and excited states;
- helium doubly ionized, singly ionized, neutral, singlet, triplet, and metastable states;
- deuterium atomic states;
- residual light-element atomic and ionic states;
- free electrons and positrons;
- photon frequency and angular states;
- additional RFC-derived charged or neutral species authorized upstream.

Any reduced atom, superlevel, continuum bin, or effective transition must include a no-loss relation to the underlying physical states and a quantified error domain.

---

# 7. Atomic and radiative quantities Module G must derive

Module F does not supply a solved recombination history.

Module G must derive:

- nonequilibrium level and charge-state populations;
- radiative recombination and photoionization flows;
- bound-bound and bound-free transitions;
- spontaneous, stimulated, and absorptive routes;
- collisional excitation, de-excitation, ionization, and recombination;
- two-photon and forbidden channels;
- resonance-line escape and redistribution;
- continuum and line feedback;
- matter-radiation energy transfer;
- free-electron history;
- total opacity and differential optical depth;
- integrated optical depth;
- normalized visibility function;
- finite-width last-scattering probability structure;
- baryon-drag history and surface;
- photon diffusion and damping histories;
- temperature and polarization source histories;
- recombination radiation and intrinsic spectral distortions;
- perturbation-dependent atomic response;
- the complete Module H transfer parent state.

---

# 8. Conservation and continuity across the boundary

Module G must preserve continuously:

- hydrogen, helium, deuterium, and all represented nuclear identities;
- electric charge;
- baryon number;
- particle accounting;
- total energy and momentum;
- transition energy and photon-frequency relations;
- thermodynamic entropy accounting;
- radiative energy and entropy;
- branch and event identity;
- uncertainty and covariance;
- source, isotope, atomic-transition, route, and memory ancestry.

Atomic capture changes the state of nuclei and electrons but does not create or delete their parent identities.

Photon emission, absorption, and redistribution change the radiation state but must preserve energy and transition ancestry.

---

# 9. Optical-depth and visibility typing

Module G must derive the differential optical depth from the generated electron and opacity state under a declared convention, for example:

```text
dot_tau(eta) = -a(eta) n_e(eta) sigma_T + other material opacity terms
```

The integrated optical depth is generated from the same state:

```text
tau(eta) = integral_eta^eta_ref [-dot_tau(eta')] d eta'
```

and the primordial photon visibility function is:

```text
g(eta) = -dot_tau(eta) exp[-tau(eta)]
```

The exact sign and endpoint convention must remain internally consistent.

The visibility function must be positive under that convention, normalized over the represented primordial scattering domain, converged, uncertainty-bearing, and explicitly separated from late reionization.

The old recursive-entropy transparency curve may be retained only as an internal diagnostic of memory and ordering. It cannot replace the physical opacity calculation.

---

# 10. Photon last scattering and baryon drag

Module G must keep distinct:

```text
photon last-scattering distribution
baryon-drag release distribution
```

The photon last-scattering surface is a finite probability distribution with:

- peak, mean, median, width, skewness, and relevant higher moments;
- spatial and perturbative variation;
- frequency and polarization dependence where material;
- branch, route, and transition ancestry;
- covariance.

The baryon-drag surface follows from momentum-transfer history and may not be forced to coincide with photon last scattering.

---

# 11. Primordial recombination and late reionization

Module G owns only primordial recombination and the physical primary CMB surface.

Later astrophysical reionization requires stars, galaxies, radiation sources, gas transport, and feedback generated in later modules.

Module G may export an extension interface, but it may not:

- impose an observed reionization history;
- fold late optical depth into the primordial visibility solution;
- use late astrophysical parameters to alter primordial recombination;
- claim a final observed CMB surface including later scattering before those sources exist.

---

# 12. Perturbation and field continuity

Module G inherits the perturbation and field state needed to calculate local recombination response.

It must evolve or rigorously bound the effects of:

- baryon-density perturbations;
- electron-density perturbations;
- matter and radiation temperature perturbations;
- velocity divergence and photon-baryon slip;
- metric-interface perturbations;
- isotope and helium-abundance perturbations;
- visible-dark perturbations;
- magnetic, vortical, turbulent, shock, defect, and spatial structures where active.

A homogeneous recombination history is insufficient when Module H requires perturbed source functions.

---

# 13. Dark-sector continuity

The compression-relic and dissipative-tail states remain inherited RFC sectors.

Module G may evolve only predeclared effects on:

- background expansion;
- electron density;
- atomic populations;
- energy deposition or extraction;
- opacity;
- matter temperature;
- perturbations;
- visibility and drag structure;
- recombination radiation.

A dark term may not be added to improve a later CMB comparison.

Null effects should be preserved as witnessed zero-backreaction results rather than omitted silently.

---

# 14. Entropy and memory typing

Module G must preserve distinct ledgers for:

```text
S_th       thermodynamic entropy
S_rad      radiative entropy
S_comp     compositional entropy
S_rec      recursive depth and ancestry memory
```

The physical transparency transition follows from the generated opacity history.

Recursive entropy may correlate with transparency ordering or memory redistribution, but it is not an atomic cross section, ionization rate, or substitute optical depth.

---

# 15. Branch handling and obstruction

For every admitted Module F branch, Module G may produce:

- one unique recombination history;
- a representation- or gauge-equivalent family;
- multiple physically distinct atomic or radiative branches;
- obstruction.

Distinct atomic closure, line-transfer, dark-sector, inherited-field, or perturbative histories remain distinct unless a physical equivalence theorem is proved.

Module G may not choose a branch because its ionization history or visibility shape resembles public results.

Failed charge closure, energy closure, detailed balance, positivity, visibility normalization, atomic convergence, radiative convergence, or Module H restart sufficiency is an obstruction rather than a reason to retune Module F.

---

# 16. Required Module G output to Module H

Module G must eventually export:

```text
P_G->H = (
  coordinate and background histories,
  complete primordial ionization history,
  atomic and ionic level-population histories,
  free-electron and free-proton histories,
  photon distribution and polarization state,
  matter, electron, ion, photon, neutrino, and dark temperatures,
  atomic transition and radiation-transfer histories,
  opacity by process,
  differential and integrated optical depth,
  normalized visibility function and moments,
  finite last-scattering structure,
  baryon-drag history and surface,
  photon-baryon slip and sound-speed histories,
  diffusion, viscosity, conduction, and damping histories,
  temperature and polarization source ingredients,
  recombination-radiation and spectral-distortion state,
  perturbation-dependent recombination response,
  scalar, vector, and tensor seed interfaces where active,
  metric, stress-energy, anisotropic-stress, and momentum-transfer interfaces,
  visible-dark coupling and perturbation state,
  inherited magnetic or spatial state where active,
  uncertainty and covariance,
  conservation, transfer, entropy, route, event, and memory state,
  source, isotope, species, atomic-transition, scale, and branch ancestry,
  restartable physical state
)
```

Module H may construct the linear Boltzmann and transfer operator, but it may not reconstruct an omitted ionization, opacity, visibility, drag, diffusion, or recombination-source history from public tables.

---

# 17. Concatenated F→G theorem target

The Module F and Module G plans concatenate coherently when the following statement can be earned:

> Module F supplies a complete recombination-ready plasma whose isotope composition, particle and radiation distributions, temperatures, charges, plasma and opacity seeds, atomic carrier and transition candidates, perturbations, dark-sector state, uncertainty, memory, ancestry, and physical coordinate history are generated and frozen. Module G preserves that parent, solves the full nonequilibrium atomic and radiative network, derives the free-electron and opacity histories, integrates the optical depth, generates the normalized primordial visibility function, produces finite photon last-scattering and baryon-drag structures, and exports complete transfer-source histories without inserting a public ionization curve, recombination coordinate, visibility function, optical-depth table, or CMB normalization.

This boundary makes Module G the atomic and radiative child of Module F rather than a symbolic transparency wrapper.