ClearAll["Global`*"];
A = {{-1, 1}, {1, -1}};
c = {1, 1};
result = <|"call" -> "HU-WL-002", "constraintResidual" -> c.A,
 "conservedLinearFunctional" -> TrueQ[c.A == {0, 0}],
 "zeroMode" -> (ToString[#, InputForm] & /@ NullSpace[A])|>;
ToString[result, InputForm]
