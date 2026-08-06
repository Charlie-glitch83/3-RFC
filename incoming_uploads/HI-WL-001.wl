ClearAll["Global`*"];
T = {{a, b}, {c, d}}; B = DiagonalMatrix[{u, v}]; x = {x1, x2};
inst = B.T;
identity = FullSimplify[inst.x == B.(T.x)];
result = <|"call" -> "HI-WL-001", "instantiated" -> ToString[inst, InputForm],
 "compositionPass" -> TrueQ[identity]|>;
ToString[result, InputForm]
