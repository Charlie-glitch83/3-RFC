ClearAll["Global`*"];
cov = {{1, r}, {r, 1}}; T = {{a, b}, {c, d}};
Cp = FullSimplify[T.cov.Transpose[T], Element[{a,b,c,d,r}, Reals]];
result = <|"call" -> "HI-WL-002", "propagatedCovariance" -> ToString[Cp, InputForm],
 "symmetric" -> TrueQ[FullSimplify[Cp == Transpose[Cp], Element[{a,b,c,d,r}, Reals]]]|>;
ToString[result, InputForm]
