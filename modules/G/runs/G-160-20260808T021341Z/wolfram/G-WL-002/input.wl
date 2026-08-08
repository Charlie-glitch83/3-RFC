ClearAll["Global`*"];
S = {{-1, 1}, {-1, 1}, {1, -1}};
number = {1, 1, 2}; charge = {-1, 1, 0};
result = <|"call" -> "G-WL-002", "numberResidual" -> number.S,
 "chargeResidual" -> charge.S, "numberPass" -> TrueQ[number.S == {0, 0}],
 "chargePass" -> TrueQ[charge.S == {0, 0}]|>;
ToString[result, InputForm]
