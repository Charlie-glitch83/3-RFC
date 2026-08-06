ClearAll["Global`*"];
rho = Array[r,4]; flux = Array[f,4];
update = Table[rho[[i]] - dt (flux[[Mod[i,4]+1]] - flux[[i]]), {i,1,4}];
residual = FullSimplify[Total[update] - Total[rho]];
result = <|"call" -> "L-WL-001", "massResidual" -> ToString[residual, InputForm],
 "conservationPass" -> TrueQ[residual == 0]|>;
ToString[result, InputForm]
