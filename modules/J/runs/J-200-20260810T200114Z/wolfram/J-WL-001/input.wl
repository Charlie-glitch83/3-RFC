ClearAll["Global`*"];
covMat = {{1, 7/20, 1/10}, {7/20, 4/5, 1/5}, {1/10, 1/5, 1/2}};
e = Eigenvalues[covMat]; chol = CholeskyDecomposition[covMat];
result = <|"call" -> "J-WL-001", "eigenvalues" -> (ToString[#, InputForm] & /@ e),
 "positiveDefinite" -> TrueQ[And @@ Thread[e > 0]],
 "reconstructionPass" -> TrueQ[FullSimplify[ConjugateTranspose[chol].chol == covMat]]|>;
ToString[result, InputForm]
