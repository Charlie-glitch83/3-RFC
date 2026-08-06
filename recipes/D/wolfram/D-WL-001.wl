ClearAll["Global`*"];
sol = DSolveValue[{x'[t] == -k (x[t] - y[t]), y'[t] == k (x[t] - y[t]), x[0] == x0, y[0] == y0}, {x[t], y[t]}, t, Assumptions -> k > 0];
total = FullSimplify[Total[sol], k > 0];
V = (x[t] - y[t])^2;
vdot = FullSimplify[D[V, t] /. {x'[t] -> -k (x[t] - y[t]), y'[t] -> k (x[t] - y[t])}, k > 0];
result = <|"call" -> "D-WL-001", "solution" -> ToString[sol, InputForm],
 "conservedTotal" -> ToString[total, InputForm], "lyapunovDerivative" -> ToString[vdot, InputForm],
 "decayPass" -> TrueQ[FullSimplify[vdot == -4 k V, k > 0]]|>;
ToString[result, InputForm]
