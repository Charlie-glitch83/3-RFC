# Module HU — Frozen Universal Linear Transfer Operator

**Objective:** Derive and freeze the background-independent portion of the linear transfer machinery before instantiation on a realized geometry.

**Parents:** G

**Children:** HI

**N-body mode:** `RELATIONAL_GRAMMAR_ACTIVE`

## Required outputs

- typed operator
- domain and codomain
- gauge/frame contracts
- conservation and constraint identities
- operator uncertainty
- frozen H_HU_to_HI

## Mandatory gates

- no realized-background values smuggled into universal operator
- linearity-domain proof
- symbolic identity verification
- hash freeze

## Forbidden shortcuts

- importing a public Boltzmann transfer table
- retuning after I

## Claim boundary

Universal RFC transfer law at declared linear scope.

## Working rule

Create run workspaces only with `python tools/rfc.py new-run HU`. State is held centrally in `STATE.json`.
