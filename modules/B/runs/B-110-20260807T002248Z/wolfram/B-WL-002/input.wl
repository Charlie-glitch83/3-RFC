ClearAll["Global`*"];
lap = {{1, -1, 0, 0}, {-1, 2, -1, 0}, {0, -1, 2, -1}, {0, 0, -1, 1}};
d = N[1 + Sqrt[5], 80];
op = Inverse[IdentityMatrix[4] + lap/(d - 1)];
x = SetPrecision[{3/2, -1/2, 3/4, -7/4}, 80];
y = op.x;
reopened = LinearSolve[op, y];
result = <|
 "call" -> "B-WL-002",
 "meanBefore" -> N[Mean[x], 40], "meanAfter" -> N[Mean[y], 40],
 "normBefore" -> N[Norm[x], 40], "normAfter" -> N[Norm[y], 40],
 "strictCompression" -> TrueQ[N[Norm[y], 40] < N[Norm[x], 40]],
 "reopeningResidual" -> N[Norm[reopened - x], 40],
 "reopeningPass" -> TrueQ[Chop[N[Norm[reopened - x], 40], 10^-35] == 0]
|>;
ToString[result, InputForm]
