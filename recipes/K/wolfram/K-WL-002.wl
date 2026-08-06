ClearAll["Global`*"];
(* velocity-Verlet map for harmonic oscillator, unit mass *)
pHalf = p - dt k q/2;
qNew = q + dt pHalf;
pNew = pHalf - dt k qNew/2;
J = D[{qNew,pNew}, {{q,p}}];
result = <|"call" -> "K-WL-002", "jacobian" -> ToString[J, InputForm],
 "determinant" -> ToString[FullSimplify[Det[J]], InputForm],
 "symplecticVolumePass" -> TrueQ[FullSimplify[Det[J] == 1]]|>;
ToString[result, InputForm]
