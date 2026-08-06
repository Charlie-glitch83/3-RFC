ClearAll[stoichiometryAudit];
stoichiometryAudit[stoich_?MatrixQ, conservedRows_?MatrixQ] := Module[{residual, null},
 residual = FullSimplify[conservedRows.stoich];
 null = NullSpace[Transpose[stoich]];
 <|"conservationResidual" -> residual, "leftNullspace" -> null,
   "pass" -> TrueQ[residual == ConstantArray[0, Dimensions[residual]]]|>
];
