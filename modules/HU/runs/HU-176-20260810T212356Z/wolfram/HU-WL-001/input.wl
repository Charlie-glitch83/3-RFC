ClearAll["Global`*"];
A = {{-1/5, 1/20}, {1/10, -3/10}};
T[t_] := MatrixExp[A t];
semi = FullSimplify[T[t1 + t2] == T[t2].T[t1]];
x = {x1, x2}; y = {y1, y2};
super = FullSimplify[T[t].(x + y) == T[t].x + T[t].y];
result = <|"call" -> "HU-WL-001", "semigroup" -> TrueQ[semi], "superposition" -> TrueQ[super],
 "generatorEigenvalues" -> (ToString[#, InputForm] & /@ Eigenvalues[A])|>;
ToString[result, InputForm]
