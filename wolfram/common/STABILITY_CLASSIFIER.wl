ClearAll[classifyJacobian];
classifyJacobian[j_?MatrixQ] := Module[{e = N[Eigenvalues[j], 50], rho},
 rho = Max[Abs[e]];
 <|"eigenvalues" -> e, "spectralRadius" -> rho,
   "classification" -> Which[rho < 1, "LOCALLY_ATTRACTING", rho == 1, "MARGINAL", True, "UNSTABLE"]|>
];
