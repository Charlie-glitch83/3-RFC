ClearAll["Global`*"];
f[x_]:=a x+b;
fixed=Solve[x==f[x],x];
derivative=D[f[x],x];
result=<|"call"->"Q-WL-001","fixedPoint"->ToString[fixed,InputForm],
 "derivative"->ToString[derivative,InputForm],
 "attractionCondition"->ToString[Reduce[Abs[derivative]<1,a,Reals],InputForm]|>;
ToString[result, InputForm]
