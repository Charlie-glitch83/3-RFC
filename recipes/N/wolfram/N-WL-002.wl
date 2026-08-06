ClearAll["Global`*"];
C1={{1,1/5},{1/5,1/2}}; C2={{3/4,1/10},{1/10,2/3}}; X={{x11,x12},{x21,x22}};
C=ArrayFlatten[{{C1,X},{Transpose[X],C2}}];
result=<|"call"->"N-WL-002","globalCovariance"->ToString[C,InputForm],
 "instruction"->"Substitute frozen cross-covariance X and require all eigenvalues nonnegative; do not set X=0 unless independently derived."|>;
ToString[result, InputForm]
