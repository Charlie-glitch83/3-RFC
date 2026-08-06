ClearAll["Global`*"];
map = {a x + b y + c, d x + e y + f};
fixed = Solve[{x,y} == map, {x,y}];
J = D[map, {{x,y}}];
eigs = Eigenvalues[J];
result = <|"call" -> "KLM-WL-001", "fixedPoints" -> ToString[fixed,InputForm],
 "jacobian" -> ToString[J,InputForm], "eigenvalues" -> (ToString[#,InputForm]& /@ eigs),
 "instruction" -> "Classify each frozen branch by spectral radius; do not force attraction."|>;
ToString[result, InputForm]
