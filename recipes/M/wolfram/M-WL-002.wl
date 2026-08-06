ClearAll["Global`*"];
ret = {cool[T,Z,d], opacity[T,Z,d]};
J = D[ret, {{T,Z,d}}];
result = <|"call" -> "M-WL-002", "returnJacobian" -> ToString[J,InputForm],
 "required" -> "Substitute the frozen internally derived cooling and opacity laws; then classify signs, singularities, and uncertainty propagation."|>;
ToString[result, InputForm]
