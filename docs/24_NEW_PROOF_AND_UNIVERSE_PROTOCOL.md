# New Proof and Universe Protocol

The repository can host new triadic proofs and isolated universes without contaminating the canonical build.

## New proof

```bash
python tools/rfc.py new-proof <slug> --title "<title>"
```

The proof must establish exact source, triadic descent, domain state space, witnesses, routes/events/branches, memory/reopening, countermodels, falsifiers, and evidence boundary. It remains noncanonical until an active queue unit admits it.

## New universe or cycle

```bash
python tools/rfc.py new-universe <slug> --title "<title>"
```

An isolated universe receives its own A-Q state. It may inherit a frozen source or terminal memory packet only through exact hash admission. It may not read Module P results from another universe during generation.

## Infinite manifestation

New proof lanes are demonstrations of lawful manifestation, not permission to attach triadic labels to arbitrary mathematics. Each lane must pass the manifestation countermodels in `docs/03_TRIAD_AND_MANIFESTATION.md`.
