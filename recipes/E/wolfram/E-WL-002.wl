ClearAll["Global`*"];
rates = {kf n p, kr d};
S = {{-1, 1}, {-1, 1}, {1, -1}};
rhs = S.rates;
J = D[rhs, {{n, p, d}}];
result = <|"call" -> "E-WL-002", "rhs" -> ToString[rhs, InputForm],
 "jacobian" -> ToString[J, InputForm], "conservationCheck" -> ToString[FullSimplify[{1, 1, 2}.rhs], InputForm]|>;
ToString[result, InputForm]
