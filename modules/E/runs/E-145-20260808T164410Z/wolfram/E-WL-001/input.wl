ClearAll["Global`*"];
S = {{-1, 1}, {-1, 1}, {1, -1}};
conserved = {{1, 1, 2}, {0, 1, 1}};
residual = conserved.S;
result = <|"call" -> "E-WL-001", "residual" -> residual,
 "pass" -> TrueQ[residual == ConstantArray[0, {2, 2}]],
 "leftNullspace" -> (ToString[#, InputForm] & /@ NullSpace[Transpose[S]])|>;
ToString[result, InputForm]
