ClearAll["Global`*"];
cov = {{1, 1/4}, {1/4, 1/2}};
T = {{1, a}, {0, 1}};
Cp = FullSimplify[T.cov.Transpose[T], Element[a, Reals]];
minors = {Cp[[1, 1]], Det[Cp]};
result = <|"call" -> "F-WL-002", "propagated" -> ToString[Cp, InputForm],
 "principalMinors" -> (ToString[#, InputForm] & /@ minors),
 "determinantPreservedNonnegative" -> TrueQ[FullSimplify[Det[Cp] >= 0, Element[a, Reals]]]|>;
ToString[result, InputForm]
