ClearAll["Global`*"];
L = {{1, -1, 0, 0}, {-1, 2, -1, 0}, {0, -1, 2, -1}, {0, 0, -1, 1}};
assume = delta > 1;
Q = FullSimplify[Inverse[IdentityMatrix[4] + L/(delta - 1)], assume];
eigs = FullSimplify[Eigenvalues[Q], assume];
carrier = FullSimplify[Q.ConstantArray[1, 4], assume];
result = <|
 "call" -> "B-WL-001",
 "laplacianCarrierResidual" -> L.ConstantArray[1, 4],
 "operator" -> ToString[Q, InputForm],
 "eigenvalues" -> (ToString[#, InputForm] & /@ eigs),
 "carrierPreserved" -> TrueQ[carrier == ConstantArray[1, 4]],
 "symmetric" -> TrueQ[FullSimplify[Q == Transpose[Q], assume]]
|>;
ToString[result, InputForm]
