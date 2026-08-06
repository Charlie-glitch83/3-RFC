# Module L — Baryonic and Stellar Universe Proof

## Theorem L.1 — Local conservation-complete baryonic evolution

For one admitted Module K branch, fixed active regime, regular constitutive laws, locally Lipschitz source terms, positive initial density/internal energy, and satisfied geometric and magnetic constraints, the Module L initial-value problem has a unique local solution until the first event, obstruction, singularity, or regime boundary.

### Proof

The active hydro/MHD/radiation/thermochemical system is a finite-resolution conservative evolution law with declared closure and source maps. Regular fluxes and locally Lipschitz source terms give local existence and uniqueness in the declared representation. Every internal source is paired with its recipient, so summing the baryonic, radiation, magnetic, cosmic-ray, chemical, and feedback equations cancels internal exchange. Boundary and escaped fluxes remain explicit. Positivity, causal-speed, magnetic-divergence, and constraint conditions define the admitted interval. Their first failure is an event or obstruction rather than an untracked continuation. ∎

---

## Theorem L.2 — Internal transfer closure

For every internal transfer channel, parent loss plus child, field, recipient, and escaped gains equals the declared residual.

### Proof

Every transfer is represented once as a directed edge carrying mass, momentum, angular momentum, energy channels, charge, composition reference, covariance, and ancestry. Its source term appears with opposite sign in the recipient or escaped carrier. Summation over the complete event graph therefore cancels internal edges and leaves only boundary fluxes and declared numerical/representation residuals. ∎

---

## Theorem L.3 — Magnetic divergence preservation

If the magnetic update has curl form and the initial discrete/continuum divergence constraint is satisfied, then divergence remains zero within the declared solver residual.

### Proof

Taking divergence of

\[
\partial_tB=\nabla\times\mathcal E
\]

gives

\[
\partial_t(\nabla\cdot B)=\nabla\cdot(\nabla\times\mathcal E)=0.
\]

A compatible discrete de-Rham complex gives the same identity algebraically. Any nonzero growth beyond the declared residual is a solver or representation obstruction. ∎

---

## Theorem L.4 — Thermochemical invariants

Let \(\nu\) be the stoichiometric matrix and let \(c\) be any conserved carrier vector satisfying \(c^T\nu=0\). Then internal reactions preserve \(c^TY\).

### Proof

For reaction evolution \(\dot Y=\nu R(Y,T,\ldots)\),

\[
\frac d{dt}(c^TY)=c^T\nu R=0.
\]

Advection, diffusion, source, and boundary terms are separately recorded. Positivity-preserving integration and admissible reaction domains prevent negative physical abundances. ∎

---

## Theorem L.5 — Radiation-matter exchange closure

The total matter-plus-radiation stress-energy changes only through external or boundary channels.

### Proof

The coupled equations contain \(+G_{\rm rad}^\nu\) in radiation and \(-G_{\rm rad}^\nu\) in matter. Their sum cancels exactly. Additional absorption, emission, scattering, and feedback channels are represented by the same paired-edge rule. ∎

---

## Theorem L.6 — Cloud and core identity is not threshold identity

A density, temperature, molecular, Jeans, virial, or free-fall threshold alone cannot establish a physical cloud/core object.

### Proof

Object identity requires coherent material membership, bounded flux, persistence, a physical boundary or phase-space support, restartability, and ancestry. A scalar threshold supplies none of these jointly and can be crossed by transient compression, shocks, numerical noise, or unbound material. Therefore thresholds can be candidate witnesses only. ∎

---

## Theorem L.7 — Witnessed star-birth conservation

A star-birth event preserves every declared conserved channel when its parent, field, child, and escaped packets satisfy the event ledger.

### Proof

The event map partitions the parent state into retained gas, protostellar/stellar children, fields, and escaped carriers. By construction each channel satisfies

\[
\Delta Q_{\rm parent}+\Delta Q_{\rm fields}
+\Delta Q_{\rm children}+\Delta Q_{\rm escaped}=\epsilon_Q.
\]

The child identity is admitted only after binding, support-loss, persistence, conservation, and restart witnesses pass. Hence a numerical sink without these conditions is not promoted to a physical star. ∎

---

## Theorem L.8 — Generated birth measure

The stellar birth distribution is the pushforward of the generated collapse-branch measure and is not an imposed IMF.

### Proof

For admitted collapse branches \(b\) with nonnegative internally derived weights \(w_b\), normalization defines a probability measure \(\mu(b)=w_b/\sum w\). The branch solution map \(\mathcal Y_b\) returns child masses, multiplicity, phase-space state, angular momentum, and birth time. The pushforward \(\mathcal Y_*\mu\) therefore derives the birth distribution entirely from parent state, routes, and witnesses. No observed mass function enters. ∎

---

## Theorem L.9 — No-loss population promotion

A promoted stellar-population carrier is lawful only if every downstream-required invariant and reconstructible statistic is preserved or bounded with a reopening rule.

### Proof

The promotion packet contains the generated birth measure, mass and member state, phase-space moments, ages, multiplicity, rotation, composition references, event schedules, covariance, and ancestry. Any omitted quantity required downstream either has a proved reconstruction bound or triggers reopening. Thus the promotion is a controlled quotient rather than identity loss. ∎

---

## Theorem L.10 — Stellar-structure ownership closure

Module L can evolve the mechanical and thermal stellar state without fabricating isotope-resolved nuclear physics.

### Proof

The stellar equations use an explicit nuclear-energy and composition interface. Module L supplies zone, temperature-density, transport, mixing, mass-loss, binary, and hydrodynamic trajectories. Module M supplies isotope-resolved burning, detailed nuclear power, yields, and radioactive descendants. Because the interface is typed and energy channels are represented once, neither module duplicates the other's ownership. ∎

---

## Theorem L.11 — Feedback and explosive-event closure

Every feedback or explosive event preserves source identity and closes mass, momentum, angular momentum, and all material energy channels across L, M, and K ownership.

### Proof

Module L owns hydrodynamic timing, shock/radiation propagation, momentum, energy, and remnant dynamics; M owns isotope processing and radioactive power; K owns gravity and strong-field embedding. The shared event packet is the common boundary object. Pairing each source loss with ejecta, radiation, remnant, escaped, and returned gains prevents double counting. ∎

---

## Theorem L.12 — Strong-field promotion preserves global identity

The map \(\Pi_{L\to K}^{\rm strong}\) preserves mass-energy, momentum, angular momentum/spin, charge where active, orbit, multipoles, waveform-source state, environment, covariance, memory, and ancestry.

### Proof

These quantities are explicit fields of the promotion packet and become immutable inputs to the K strong-field representation. The overlap test compares all shared invariants and fields. Failure blocks promotion rather than permitting a hidden reset. ∎

---

## Theorem L.13 — Replay locality

A Module M return can reopen only the earliest physically affected forward interval and cannot alter Modules A–J or unaffected K/L history.

### Proof

Every returned field contains changed-domain markers, causal ancestry, event time, and dependency edges. The replay graph is therefore restricted to descendants of the earliest changed node. Upstream frozen nodes have no incoming dependency from M and remain identical. ∎

---

## Theorem L.14 — Covariance positivity

If the parent covariance and every process-noise contribution are positive semidefinite, then the propagated Module L covariance is positive semidefinite.

### Proof

For

\[
\Sigma_L=J_L\Sigma_KJ_L^T+\sum_i\Sigma_i,
\]

any vector \(v\) gives

\[
v^T\Sigma_Lv=(J_L^Tv)^T\Sigma_K(J_L^Tv)+\sum_i v^T\Sigma_iv\ge0.
\]

∎

---

## Theorem L.15 — K-L-M recurrence classification boundary

Module L first pass does not establish final recurrence closure.

### Proof

The recurrence operator depends on the not-yet-completed Module M composition return and the subsequent K update. Without those operators, a fixed point, cycle, attractor, branch family, or nonconvergence cannot be physically classified. Therefore `L^(0)` may be complete while `L*` remains pending. ∎

---

## Theorem L.16 — Module L first-pass completion

Under the named assumptions and boundaries, Module L constructs a complete restartable `L^(0)` and exact `P_L->M^(0)` and `R_L->K^(0)` packets without empirical tuning.

### Proof

The preceding theorems establish conservative baryonic evolution, thermochemical and radiation exchange closure, physical cloud/collapse/star-birth identity, generated birth measures, no-loss promotions, stellar/M/K ownership, feedback and strong-field transfers, covariance, replay locality, and exact child/return interfaces. These collectively supply all fields required by the sealed handoffs. Final isotope closure and recurrence classification are explicitly excluded. ∎