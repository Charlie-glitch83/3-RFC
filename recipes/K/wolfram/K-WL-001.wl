ClearAll["Global`*"];
r = {rx, ry, rz};
F12 = g m1 m2 r/(r.r + eps^2)^(3/2);
F21 = -F12;
result = <|"call" -> "K-WL-001", "pairSum" -> FullSimplify[F12 + F21],
 "antisymmetryPass" -> TrueQ[FullSimplify[F12 + F21 == {0,0,0}]]|>;
ToString[result, InputForm]
