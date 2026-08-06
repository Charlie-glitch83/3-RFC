ClearAll["Global`*"];
S = {{-2,-1},{1,-1},{0,1}};
count = {1,2,3};
result = <|"call" -> "M-WL-001", "residual" -> count.S,
 "pass" -> TrueQ[count.S == {0,0}], "leftNullspace" -> (ToString[#,InputForm]& /@ NullSpace[Transpose[S]])|>;
ToString[result, InputForm]
