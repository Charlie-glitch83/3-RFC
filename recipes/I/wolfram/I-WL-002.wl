ClearAll["Global`*"];
state = {x[t], y[t]};
constraint = x[t] + y[t] - c;
rules = {x'[t] -> f[x[t], y[t]], y'[t] -> -f[x[t], y[t]]};
dc = FullSimplify[D[constraint, t] /. rules];
result = <|"call" -> "I-WL-002", "constraintDerivative" -> ToString[dc, InputForm],
 "preserved" -> TrueQ[dc == 0]|>;
ToString[result, InputForm]
