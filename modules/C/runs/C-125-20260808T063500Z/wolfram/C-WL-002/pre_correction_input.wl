m = {{0, 0, 0}, {0, 2, -1}, {0, -1, 2}};
g = {{0, 0, 0}, {0, 0, -1}, {0, 1, 0}};
comm = FullSimplify[m.g - g.m];
eval = N[Eigenvalues[m], 50];
<|"call" -> "C-WL-002", "commutator" -> comm, "eigenvalues" -> eval, "invariant" -> TrueQ[comm == ConstantArray[0, {3, 3}]]|>
