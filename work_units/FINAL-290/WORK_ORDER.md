# FINAL-290 — Final Repository, Reproducibility, and Claim Audit

## Objective

Prove that the repository can reconstruct the frozen universe, its empirical audit, and terminal continuation from a clean checkout without chat history.

## Exact sequence

1. Reconstruct from a clean checkout with no chat history.
2. Verify every source, run, artifact, environment, universe, P, and Q hash.
3. Audit each claim against owning evidence.
4. Package publication artifacts without mutating O, P, or Q.
5. Run clean reconstruction.
6. Verify source, artifact, environment, and run manifests.
7. Rebuild context from machine state.
8. Audit all claims against evidence ownership.
9. Package publication-ready proof/universe artifacts without changing frozen science.

## Commands

```bash
python tools/director.py doctor
python -m unittest discover -s tests -v
python tools/rfc.py firewall-scan
python tools/rfc.py context
```

## Deliverables

- FINAL_RECONSTRUCTION.md
- FINAL_CLAIM_AUDIT.json
- FINAL_TREE_MANIFEST.json
- runs/FINAL-290/CLOSEOUT.md

## Componentwise gates

- clean checkout reconstruction
- all hashes match
- no hidden inputs
- claim audit passes
- P and Q isolation verified

## Hard stops

- required source or parent hash is missing
- a public target would influence a generation decision
- a claimed artifact cannot be fetched and independently verified
- a componentwise gate fails

## Commit

`Complete the reproducible enhanced RFC universe`
