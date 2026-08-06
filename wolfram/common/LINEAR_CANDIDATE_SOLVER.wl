(* Generic exact solver for a linear candidate operator from frozen constraints.
   Bind basisMatrices, coefficientSymbols, and linearConstraints before use. *)
ClearAll[solveLinearCandidate];
solveLinearCandidate[basisMatrices_List, coefficientSymbols_List, linearConstraints_List] := Module[
  {candidate, solution, branches},
  candidate = Total[MapThread[#1 #2 &, {coefficientSymbols, basisMatrices}]];
  solution = Reduce[linearConstraints, coefficientSymbols, Reals];
  branches = ToRules /@ LogicalExpand[solution];
  <|"candidate" -> candidate, "solution" -> solution, "branches" -> branches|>
];
