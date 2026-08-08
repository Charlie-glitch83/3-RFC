# E-140 Closeout

## Result

PASS at `MINIMAL_SPINE`. Module E now physically materializes the source-owned primordial-composite reaction network required by the active repository packet from the exact frozen Module-D parent. The run derives the internally typed seven-state composite registry, positive-binding admission law, six reversible witnessed association families, parent-derived forward/reverse rates, full abundance trajectory, exact internal carrier ledgers, constitutive-energy/RFL-memory transfer, freeze-out witness, inherited covariance propagation, checkpoint/restart, clean replay, semantic countermodels, route-withholding trajectories, and canonical `H_E_to_F`.

The first verification attempt is preserved: it incorrectly tested route materiality only by terminal equilibrium change and therefore returned FAIL. The frozen falsifier requires a detectable route effect, not a terminal-only effect. The implementation-only correction reran the full frozen matrix and measured full-trajectory route effects without changing species, rates, thresholds, initial state, interval, tolerances, gates, falsifiers, or claim boundary. All six withheld route families materially change the trajectory by `0.0560` to `0.0938`, far above the frozen `1e-8` threshold, while converging to the same detailed-balance terminal equilibrium.

## Key generated state

- terminal internal RFC composition: `[0.01586715781451039, 0.0021566344122218237, 0.0012624268897508102, 0.006667156204078111, 0.003902746437921267, 0.0005304539961466856, 0.319504355869066]`
- freeze witness: `tau_E=7489.242801811339` with final RHS norm `4.235164736271502e-22`
- final constitutive energy: `0.009112509972599138`
- final RFL binding-memory transfer: `0.2907735333309454`
- finest-two convergence L_inf: `1.1102230246251565e-16`
- tightened-tolerance L_inf: `9.658940314238862e-15`
- independent endpoint L_inf: `8.548717289613705e-15`
- restart L_inf: `1.734723475976807e-18`
- clean exact-config replay: `PASS`
- covariance: `PASS`, minimum eigenvalue `9.246045580407306e-29`
- canonical handoff SHA-256: `975c4fcdfa2f4f861dd3085e14678116377bbe4d0fc23dd4e51f4373f9c2ecbf`

## Componentwise gates

All mandatory E gates PASS: internal carrier/constitutive-energy accounting, network convergence, rate-source audit, no scalar-channel collapse, and withheld-reaction/independent-implementation checks. Aggregate scoring does not override componentwise gates.

## Failures preserved and corrections made

`verification/failures/attempt_001/GATE_RESULTS.json` preserves the first failed verification. The only correction was the route-materiality verifier: terminal-equilibrium-only comparison was replaced by the frozen gate's actual full-trajectory detectable-effect criterion. No scientific definition or threshold changed.

## Independent reconstruction

The independent verifier rebuilt `M_C`, composite occupancy energies, binding increments, the twelve directional stoichiometric columns, `Q0/Q1/Q2`, all four rate coefficients, and the initial state directly from the frozen C/D parents, then integrated with DOP853. Result: PASS.

## Strongest supported claim

From the exact frozen D three-carrier state, RFC now has a generated, physically executed, independently reconstructed and cleanly replayed Module-E MINIMAL_SPINE primordial-composite reaction history with source-owned composite admission, reversible rates, exact carrier accounting, positive abundance dynamics, material route witnesses, constitutive binding-memory transfer, freeze-out and covariance.

## Strongest unsupported claim

Module E does not establish Standard Model proton/neutron/isotope correspondence, measured nuclear masses/bindings/cross sections/lifetimes, Kelvin/MeV calibration, conventional precision BBN, empirical primordial abundance agreement, metric/FRW expansion, or full hyper-realistic nuclear physics.

## Exact next child

Controller-owned. After E is closed and promoted to `FROZEN / MINIMAL_SPINE`, `rfc.py advance --task E-140 --result PASS` may activate only direct child `F-150` under `AUTO_SINGLE_CHILD_AFTER_PASS`. This closeout itself does not manually activate F.
