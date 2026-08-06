ClearAll["Global`*"];
M = {{a, z + I w}, {z - I w, b}};
assume = Element[{a, b, z, w}, Reals];
herm = ComplexExpand[ConjugateTranspose[M] == M, TargetFunctions -> {Re, Im}];
char = CharacteristicPolynomial[M, lambda];
result = <|
 "call" -> "C-WL-001", "hermitian" -> TrueQ[herm],
 "characteristicPolynomial" -> ToString[char, InputForm],
 "trace" -> ToString[Tr[M], InputForm], "determinant" -> ToString[Det[M], InputForm],
 "eigenvalues" -> (ToString[#, InputForm] & /@ FullSimplify[Eigenvalues[M], assume])
|>;
ToString[result, InputForm]
