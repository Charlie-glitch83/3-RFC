ClearAll["Global`*"];
energies = {e1,e2,e3,e4}; beta = Symbol["beta"];
w = Exp[-beta energies]; p = FullSimplify[w/Total[w]];
result = <|"call" -> "L-WL-002", "measure" -> ToString[p, InputForm],
 "normalization" -> ToString[FullSimplify[Total[p]], InputForm],
 "pass" -> TrueQ[FullSimplify[Total[p] == 1]]|>;
ToString[result, InputForm]
