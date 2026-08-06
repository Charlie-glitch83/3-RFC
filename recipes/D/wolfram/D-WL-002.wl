ClearAll["Global`*"];
J = {{-k1, k2}, {k1, -k2}};
e = FullSimplify[Eigenvalues[J], k1 > 0 && k2 > 0];
result = <|"call" -> "D-WL-002", "eigenvalues" -> (ToString[#, InputForm] & /@ e),
 "conservedModePresent" -> TrueQ[MemberQ[e, 0]],
 "relaxationMode" -> ToString[SelectFirst[e, # =!= 0 &], InputForm]|>;
ToString[result, InputForm]
