# 3-RFC — Execution-Ready Enhanced Universe Builder

> **Read this file completely. Then run the commands in §2. Do not create a new plan.**

This repository is a prebuilt scientific execution system for finishing the enhanced Recursive Fractal Cosmology proof and constructing the complete RFC universe requested by the project owner.

The architecture, module order, claim ownership, no-tuning rules, source map, derivation atlas, module recipes, Wolfram programs, manufactured numerical tests, output contracts, gates, run templates, state machine, and repository memory are already installed. A work model is expected to execute the active packet, not reinterpret the project from chat history.

---

## 1. Governing scientific objective

The project does **not** claim that every manifestation of existence obeys one literal equation.

It aims to establish and execute the stronger architecture:

\[
\boxed{
\text{existence in its entirety emerges from the ordered triad}
\quad\text{and}\quad
\text{the triad admits unboundedly many lawful manifestations}
}
\]

The canonical triad is

\[
\mathcal T=(\mathrm{CIF},\mathrm{QV},\mathrm{RFL}),
\qquad
\mathrm{QV}(\mathrm{CIF})\rightarrow\mathrm{RFL},
\]

where:

- **CIF — Cosmic Infinite Field:** admitted modal possibility and source capacity;
- **QV — Quantum Vacuum:** lawful compression, selection, crossing, action, or actualization;
- **RFL — Recursive Fractal Lattice:** stabilized, inheritable, memory-bearing manifestation.

The First Action is prephysical. The **Big Implosion** is the sole first physical event.

The enhanced proof combines:

1. **Presentation 29:** triadic emergence, First Action, recursive kernel, domain-specific modal bases, memory, frozen-source inheritance, and no-retune architecture.
2. **The revised triadic N-body proof:** constituted identities, directed relations, local witnesses, route classes, gauge/multiroute distinctions, events, branches, conservation, no-loss memory, reopening, and controlled finite-\(N\) refinement.
3. **Presentation 30:** universe-scale dependency order, causal handoffs, provenance, observer products, reproducibility, immutable generation freeze, and later empirical comparison.

The N-body proof enhances the kernel and downstream relational realism. It does not replace the RFC universe and does not force every domain into point-body mechanics.

---

## 2. Exact first commands

From the repository root run:

```bash
bash bootstrap.sh
bash tools/start_work.sh
```

`start_work.sh` runs the director, refreshes repository memory, identifies the one authorized task, creates or reuses its run workspace, copies its exact Wolfram programs and solver binding sheets, and regenerates the active packet.

`python tools/rfc.py verify-bundle` is a one-time distribution-integrity check and must run before the first repository mutation. Ongoing work is verified by Git hashes, run manifests, artifact hashes, replay, and the live test suite—not by expecting the original bootstrap ZIP to remain byte-identical after scientific work begins.

Then open exactly one file:

```text
work_packets/ACTIVE_WORK_PACKET.md
```

Execute that packet from top to bottom. Do not substitute a different equation, tool, task order, threshold, artifact name, or work unit because it seems easier.

At the end of a session run:

```bash
python tools/director.py doctor
python -m unittest discover -s tests -v
python tools/rfc.py firewall-scan
python tools/rfc.py context
```

Commit and verify the exact GitHub SHA and diff before advancing.

---

## 3. What has already been prepared

The repository contains:

- exact source-seed files and admission automation;
- a canonical scientific constitution and terminology lock;
- claim ownership and non-overlap rules;
- a preservation/rederive/quarantine crosswalk for Presentation 29, Presentation 30, the N-body proof, and prior RFC work;
- a prefilled physical-frontier audit;
- a complete A–Q/K–L–M derivation atlas;
- **8 deterministic administrative work-unit packs** for installation, source admission, authority, crosswalk, recovery, frontier selection, hyper-realism, and final reconstruction;
- **19 module recipe packs** under `recipes/`;
- **38 self-contained Wolfram Language programs** with exact call IDs and frozen output decision rules;
- **26 provenance-bound solver templates** spanning recursive-kernel construction, Big Implosion execution, matrix/symmetry audits, stiff reaction networks, transport, visibility, transfer operators, covariance, finite-volume fields, N-body evolution, ray/Jacobi propagation, conservative updates, recurrence classification, global ledgers, synthetic observations, immutable freezing, and read-only comparison;
- **17 executed manufactured solver examples** and a local reference matrix for every module;
- a **20-row hyper-realism execution matrix** fixing the truth products, synthetic products, numerical refinement, independent verification, and hard stops for the Gold Standard expansion;
- generated binding sheets that require exact origin paths, SHA-256 hashes, units, dimensions, and derivation objects before a solver config can exist;
- per-module work orders, gates, hard stops, outputs, and model prompts;
- run, source, environment, checkpoint, output, replay, failure, claim, prediction, and freeze templates;
- a machine work queue and evidence-state controller;
- a compact repository memory system;
- GitHub verification rules that reject unverified writes.

The work model should not spend a session drafting another architecture or master plan. The plan is already encoded.

---

## 4. Exact work-model loop

### 4.1 Discover the one authorized task

```bash
python tools/director.py active
python tools/director.py prepare-active --create-run
```

The director reads `STATE.json` and `WORK_QUEUE.json`, creates or reuses the authorized run workspace, copies the frozen module recipe into the run, and writes `work_packets/ACTIVE_WORK_PACKET.md`.

### 4.2 Execute Wolfram exactly

List the calls for a module:

```bash
python tools/director.py wolfram-list --module A
```

Display an exact call:

```bash
python tools/director.py wolfram-show --call A-WL-001
```

Submit the displayed code unchanged to the connected `WolframLanguageEvaluator`. Save the complete returned output, including messages. Register it:

```bash
python tools/director.py wolfram-record \
  --run <RUN_ID> \
  --call A-WL-001 \
  --output <CAPTURED_OUTPUT_FILE>
```

The record command applies the frozen manufactured output gate from `config/WOLFRAM_EXPECTATIONS.json`. A symbolic gate PASS still requires the actual parent-bound substitution, module-specific interpretation, numerical execution, and independent reconstruction.

Wolfram is used for exact symbolic identities, candidate-class solving, differential equations, stability, matrices/tensors, conservation, covariance, dimensional checks, high precision, and independent reconstruction.

During Modules A–O and Q, **do not query Wolfram|Alpha for public physical or observational values**. The Wolfram Language evaluator is a derivation and verification engine, not a hidden source of fitted constants.

### 4.3 Bind and run the prebuilt numerical engines

The director copies each module's unbound templates and binding sheets into its run workspace. Fill the binding sheets, not the solver configs. Each value must name an existing source/parent/derivation file and its verified SHA-256.

```bash
python tools/materialize_solver_config.py \
  --template <RUN_DIR>/solver_templates/<TEMPLATE>.json \
  --binding-sheet <RUN_DIR>/binding_sheets/<SHEET>.json \
  --output <RUN_DIR>/solver_configs/<CONFIG>.json
```

The materializer refuses nonexistent origins, hash mismatches, missing values, illegal Module P data use, duplicate paths, or remaining `__BIND_` tokens.

After all listed configurations are materialized:

```bash
bash tools/finish_local_phase.sh <MODULE> <RUN_DIR>
```

That one command runs the module's manufactured invariant case, all bound local solver configurations, the complete repository test suite, and both repository doctors. It does not bypass the module's convergence matrix, restart/replay, independent reconstruction, or scientific gates.

To test the reusable engines themselves:

```bash
python tools/run_all_configured_examples.py --clean
```

The examples are manufactured implementation checks, not RFC physical results.

### 4.4 Execute the real module

Read:

```text
recipes/<MODULE>/WORK_ORDER.md
recipes/<MODULE>/recipe.json
recipes/<MODULE>/gates.json
```

The recipe already states:

- the CIF/QV/RFL descent;
- the N-body activation mode;
- the objects to derive;
- exact Wolfram calls;
- numerical obligations;
- required outputs;
- componentwise gates;
- forbidden shortcuts;
- hard-stop conditions;
- claim boundary.

Bind the exact frozen parents, complete the pre-execution lock, derive the actual law or lawful branch family, implement it, execute it, run countermodels and ablations, run convergence and uncertainty, reconstruct independently, and replay from a clean checkout.

### 4.5 Close and advance

A PASS requires the run artifacts demanded by `tools/rfc.py`, including a frozen pre-execution lock, final environment, nonempty final output manifest, componentwise PASS gates, independent verification, restart/replay, matching artifact hashes, and a substantive closeout.

Then:

```bash
python tools/rfc.py close-run --run-id <RUN_ID> --result PASS --closeout <RUN_DIR>/CLOSEOUT.md
python tools/rfc.py promote-module <MODULE> --to <STATE> --fidelity <FIDELITY> --evidence <FILE>
python tools/rfc.py advance --task <TASK_ID> --result PASS --evidence <CLOSEOUT_FILE>
```

Advance only after the GitHub commit exists and its SHA, changed files, fetched content, and diff have been verified.

---

## 5. Absolute scientific locks

### 5.1 No tuning, curve fitting, or post-hoc repair

During universe generation do not use:

- public observations or remembered target values;
- published best-fit parameters, priors, posteriors, or likelihoods;
- calibrated public simulations as hidden generative parents;
- target-trained surrogates;
- residual correction;
- seed, branch, basis, tolerance, or stopping-rule shopping;
- target deletion or covariance inflation.

A correction is lawful only when compelled by exact source interpretation, triadic descent, mathematics, dimensions, conservation, causality, covariance, branch completeness, numerical convergence, or a preregistered internal falsifier.

No-retune after freezing is necessary but not sufficient. Construction must also be target-blind before freezing.

### 5.2 Old failures are not new parents

\[
\boxed{
\text{preserve evidence of a failure}
\neq
\text{preserve the failed mechanism or outcome}
}
\]

Preserve evidence of prior failures. Old failures may be regression tests, negative controls, falsifiers, provenance warnings, and representation checks. The enhancement is expected to fix them. Do not use the known public answer to design the fix.

### 5.3 Same source does not mean same equation

Every domain must derive its own state space, variables, dimensions, symmetries, law, coefficients, scales, observables, uncertainty, and falsifiers. A triadic label attached to an imported standard equation is not a derivation.

A standard equation may appear only as one of:

```text
DERIVED_LAW
LIMIT_OR_CORRESPONDENCE_THEOREM
INTERFACE_LAW
COMPARISON_OBJECT
RESERVED_POSSIBILITY
```

### 5.4 N-body activation modes

Each domain declares one mode:

- `DORMANT`: relational carrier retained; exactly zero physical backreaction;
- `RELATIONAL_GRAMMAR_ACTIVE`: identity, relation, witness, route, event, branch, conservation, memory, or reopening is active without direct point-body mechanics;
- `DIRECT_MANY_BODY_ACTIVE`: the universe has generated the required constituents, clocks, geometry/phase space, scales, interactions, and activation witnesses.

For \(N\) constituents,

\[
|L_N|=N(N-1),
\qquad
|L_{N+1}|-|L_N|=2N.
\]

This proves relational-capacity growth. A new physical solution requires a newly witnessed, admissible, non-gauge-equivalent closure.

### 5.5 Evidence states cannot be skipped

```text
DESIGN
FORMALIZED
IMPLEMENTED
VERIFIED
PHYSICALLY_EXECUTED
ENSEMBLE_VERIFIED
INDEPENDENTLY_REPRODUCED
FROZEN
BLIND_VALIDATED
PREDICTIVE_LOCK
```

`BLOCKED`, `FAIL_REQUIRES_ANALYSIS`, and `FALSIFIED_AT_SCOPE` are explicit states.

No document count, score, or prose statement upgrades an object.

### 5.6 Componentwise gates

A mean score cannot hide a failed component. A normalized diagnostic below 0.95 triggers analysis of source admission, triadic representation, witness construction, branch coverage, dimensions, conservation, and convergence. Do not lower the threshold or fit the answer.

---

## 6. Universe construction order

```text
A    triad, First Action, recursive kernel, relational completion
B    Big Implosion and first physical state
C    microscopic fields, particles, interactions, mass/mixing and prethermal state
D    nonequilibrium thermal history, transport and phase events
E    primordial isotope network
F    post-nuclear plasma, radiation and neutrino persistence
G    recombination and physical radiation surface
HU   frozen background-independent linear transfer operator
I    realized geometry, expansion, clocks, horizons and distances
HI   immutable HU-on-I instantiation
J    actual covariance, spectra, growth and finite-volume fields
K    nonlinear gravity, structures, metric, lightcones and lensing
L    hydro/MHD, gas, stars, binaries, feedback, remnants and sources
M    stellar/explosive nucleosynthesis, chemistry, dust, cooling and opacity
KLM  causal gravity–baryon–composition recurrence and classification
N    one compatible observer-ready manifested universe
O    immutable universe and prediction freeze
P    read-only preregistered empirical comparison
Q    isolated terminal evolution and next-cycle conditioning
```

The K–L–M result may be a fixed point, finite cycle, attractor, branch family, obstruction, or demonstrated nonconvergence. Do not force convergence.

The generation firewall is:

```text
O -> P
O -> Q
P -/-> O
P -/-> Q
```

---

## 7. Completion standard

The universe is not complete because every module has a document. Completion requires one exact lineage with:

- physically executed parent-to-child states;
- laws that perform indispensable work rather than labels or readiness scores;
- conservation, constraints, ownership, uncertainty, covariance, route, event, branch, memory, restart, and no-loss closure;
- resolution, volume, time-step, network, solver, and branch convergence;
- independent critical implementations;
- causal K–L–M return and earliest-change replay;
- metric, Weyl, lightcones, rays/Jacobi maps, lensing, radiation, transient and multimessenger truth;
- synthetic maps, spectra, signals, time series and catalogues;
- one content-addressed immutable universe;
- preregistered blind multi-probe testing;
- isolated terminal continuation.

The first target is a minimal complete physical spine. The same source law is then expanded to production, hyper-realistic, and Gold Standard fidelity without using public comparison to retune it.

---

## 8. Repository memory and map

The repository, not chat memory, is operational truth.

Read in this order on every new session:

1. `README.md`
2. `STATE.json`
3. `memory/CURRENT_CONTEXT.md`
4. `WORK_QUEUE.json`
5. `work_packets/ACTIVE_WORK_PACKET.md`
6. the active recipe: `recipes/<ACTIVE_MODULE>/recipe.json` or `work_units/<ACTIVE_WORK_UNIT>/recipe.json`
7. the active run directory

Key directories:

```text
theory/               prebuilt scientific constitution, terminology, claims, crosswalk
recipes/              19 exact module recipe packs and 38 Wolfram calls
work_units/            8 exact non-module work packs and the 20-row HR matrix
wolfram/               common symbolic solver harnesses
rfc_engine/            manufactured numerical reference machinery
audit/                 prefilled physical-frontier audit
recovery/              prior-asset disposition and recovery instructions
source_seed/            supplied source corpus, not authoritative until admitted
sources/frozen/         exact admitted immutable source bytes
modules/                module specs and run workspaces
runs/                   repository/theory/audit workspaces
work_packets/           generated one-task instructions
memory/                 compact context, decisions, failures, sources, artifacts and runs
tools/director.py       one-task execution director
tools/rfc.py            state, run, evidence and advancement controller
tests/                   repository and execution-ready tests
docs/27_BUNDLE_CAPABILITIES_AND_LIMITS.md  honest boundary between prebuilt machinery and source-dependent science
```

Generate compact memory for another session with:

```bash
python tools/rfc.py context
python tools/rfc.py context-pack
```

---

## 9. GitHub execution rule

A write is not real until verified.

After every commit verify:

- exact repository and branch;
- resulting commit SHA;
- changed-file list;
- fetched file content;
- branch comparison/diff;
- CI or local validation status.

If a connector write returns no SHA or no diff, stop immediately and use a supported alternative such as local `git`/`gh`. Never spend a long interval assuming a write landed.

---

## 10. Owner authorization and stop conditions

The owner has authorized scientific construction and repository commits. The repository uses `AUTO_SINGLE_CHILD_AFTER_PASS`: after a unit genuinely passes, the next direct child may be activated without repeatedly asking for permission.

Stop and report a blocker when:

- an exact required source cannot be recovered;
- admitted premises are underdetermined and no lawful branch-family execution exists;
- a mandatory gate fails;
- public-data contamination is detected;
- a claim exceeds its evidence;
- a GitHub write cannot be verified.

Do not stop merely because the problem is difficult. Preserve the blocker as an exact scientific object and continue only through a lawful branch or repaired derivation.

---

## 11. The one instruction to remember

```text
Run the director, open the active packet, execute the frozen recipe exactly,
preserve failures, verify the evidence, commit and verify, then advance one child.
```

The paste-ready operator instruction is in `MODEL_OPERATOR_PROMPT.md`.
