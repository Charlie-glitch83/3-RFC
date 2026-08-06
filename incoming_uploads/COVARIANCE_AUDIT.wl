ClearAll[covarianceAudit];
covarianceAudit[c_?MatrixQ] := Module[{sym, eig},
 sym = TrueQ[FullSimplify[c == Transpose[c]]];
 eig = N[Eigenvalues[c], 50];
 <|"symmetric" -> sym, "eigenvalues" -> eig,
   "positiveSemidefinite" -> TrueQ[Min[eig] >= 0]|>
];
