ClearAll["Global`*"];
kappa[t_] := 1;
tau[t_] := Integrate[kappa[s], {s, 0, t}];
g[t_] := Exp[-tau[t]] kappa[t];
norm = Integrate[g[t], {t, 0, Infinity}];
result = <|"call" -> "G-WL-001", "tau" -> ToString[tau[t], InputForm],
 "visibility" -> ToString[g[t], InputForm], "normalization" -> ToString[norm, InputForm],
 "pass" -> TrueQ[norm == 1]|>;
ToString[result, InputForm]
