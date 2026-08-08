ClearAll["Global`*"];
S = {{-1, 1}, {-1, 1}, {1, -1}};
charge = {-1, 1, 0};
result = <|"call" -> "F-WL-001", "chargeResidual" -> charge.S,
 "pass" -> TrueQ[charge.S == {0, 0}]|>;
ToString[result, InputForm]
