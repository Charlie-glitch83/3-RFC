ClearAll["Global`*"];
p={p1,p2}; d={d1,d2}; C={{c11,c12},{c12,c22}};
r=d-p; chi=FullSimplify[r.Inverse[C].r];
result=<|"call"->"P-WL-001","chiSquare"->ToString[chi,InputForm],
 "predictionIndependentOfData"->TrueQ[FullSimplify[D[p,{d1,d2}]==ConstantArray[0,{2,2}]]]|>;
ToString[result, InputForm]
