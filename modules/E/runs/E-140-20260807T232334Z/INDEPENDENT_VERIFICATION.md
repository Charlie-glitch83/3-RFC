# Independent Verification — E-140

The verifier reconstructed the E minimal-spine constitutive matrix, composite occupancy energies, binding increments, twelve directional stoichiometric columns, parent-derived forward/reverse coefficients, exact D initial state and three protected carrier invariants without trusting the primary gate summary. It then integrated the reconstructed frozen system independently with SciPy DOP853.

- parent-matrix reconstruction L_inf: `1.1102230246251565e-16`
- stoichiometry reconstruction L_inf: `0.0`
- DOP853 final-state L_inf vs primary: `8.326672684688674e-15`
- independent carrier-invariant drift: `3.885780586188048e-16`
- restart L_inf: `0.0`
- exact-config replay L_inf: `0.0`
- exact replay result-hash match: `True`

**Result: PASS.**

This verifies the internally typed dimensionless RFC MINIMAL_SPINE reaction network only. It does not establish empirical isotope correspondence, measured nuclear rates, Kelvin/MeV scales, or conventional BBN agreement.
