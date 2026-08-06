# GitHub Execution Protocol

## Install

1. Confirm `Charlie-glitch83/3-RFC` is the selected repository.
2. Place the scaffold at its root.
3. Run `bash bootstrap.sh`.
4. Commit with the queue message.
5. Fetch the file and compare the branch.
6. Record the SHA with `python tools/rfc.py record-commit`.

## Every later unit

- work on the configured branch;
- make small coherent commits tied to one work unit or run;
- never mix public-comparison changes with generation changes;
- never force-push over frozen scientific history;
- preserve failed runs;
- use PRs when useful, but do not let PR prose replace repository evidence;
- after every connector write, verify the SHA and diff immediately;
- if the connector cannot write, use local git/gh if available or stop with an exact blocker.

## Commit proof

A closeout is incomplete without:

```text
repository
branch
commit SHA
changed files
diff verification
validation status
```
