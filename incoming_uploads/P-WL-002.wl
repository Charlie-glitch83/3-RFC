ClearAll["Global`*"];
C={{a,b},{b,c}};
conds=Reduce[a>0 && Det[C]>0,{a,b,c},Reals];
result=<|"call"->"P-WL-002","positiveDefiniteConditions"->ToString[conds,InputForm],
 "rule"->"Freeze these covariance admissibility conditions before loading public values."|>;
ToString[result, InputForm]
