ClearAll["Global`*"];
Mrec=<|"qualifiedEnergy"->e,"routes"->{r1,r2},"branchTrace"->b|>;
CIFnext=<|"modalCapacity"->c,"admittedPossibilities"->p|>;
result=<|"call"->"Q-WL-002","memoryKeys"->Keys[Mrec],"sourceKeys"->Keys[CIFnext],
 "notIdentical"->TrueQ[Mrec=!=CIFnext],"rule"->"M_rec may condition but may not impersonate CIF."|>;
ToString[result, InputForm]
