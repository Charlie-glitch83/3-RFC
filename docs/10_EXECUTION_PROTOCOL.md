# Execution Protocol

## Before execution

Freeze:

- authority and exact parents;
- source register;
- definitions and candidate classes;
- equations, coefficients, dimensions, frames, gauges, clocks;
- environment, software, imports, files, URLs, constants, seeds;
- numerical method, tolerances, stopping rules, expected invariants;
- tests, gates, falsifiers, claim boundary;
- independent-verifier design;
- allowed implementation-only corrective scope.

## During execution

- write checkpoints;
- preserve event, route, branch, and failure history;
- never overwrite a failed attempt;
- keep public network/data disabled in sealed generation;
- capture stdout/stderr and exact commands;
- update generated-output manifest only after outputs stop changing.

## After execution

- semantic countermodels;
- componentwise gates;
- convergence/resolution/volume/time-step/network checks;
- uncertainty/covariance checks;
- restart and earliest-change replay;
- independent reconstruction;
- clean checkout replay;
- evidence-matched closeout;
- freeze and hash;
- verified GitHub commit.
