ClearAll["Global`*"];
n = 8; modes = Array[z, n];
paired = Table[If[k == 1 || k == n/2 + 1, Re[modes[[k]]], Conjugate[modes[[Mod[n-k+1,n]+1]]]], {k,1,n}];
result = <|"call" -> "J-WL-002", "rule" -> ToString[paired, InputForm],
 "note" -> "Actual finite-volume implementation must enforce conjugate pairing and preserve the frozen seed."|>;
ToString[result, InputForm]
