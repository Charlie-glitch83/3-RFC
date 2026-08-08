ClearAll["Global`*"];
G = {{0, -1}, {1, 0}};
X = {{x11, x12}, {x21, x22}};
sol = Reduce[Flatten[Transpose[G].X + X.G == ConstantArray[0, {2, 2}]], {x11, x12, x21, x22}, Reals];
result = <|"call" -> "C-WL-002", "invarianceSolution" -> ToString[sol, InputForm],
 "candidate" -> ToString[FullSimplify[X /. ToRules[sol]], InputForm]|>;
ToString[result, InputForm]
