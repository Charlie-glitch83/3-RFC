ClearAll["Global`*"];
a[t_] := 1 + h t + q t^2;
H[t_] := FullSimplify[D[Log[a[t]], t]];
eta[t_] := Integrate[1/a[s], {s, 0, t}, Assumptions -> h > 0 && q >= 0 && t >= 0, GenerateConditions -> False];
identity = FullSimplify[H[t] == a'[t]/a[t]];
result = <|"call" -> "I-WL-001", "H" -> ToString[H[t], InputForm],
 "horizon" -> ToString[eta[t], InputForm], "kinematicIdentity" -> TrueQ[identity]|>;
ToString[result, InputForm]
