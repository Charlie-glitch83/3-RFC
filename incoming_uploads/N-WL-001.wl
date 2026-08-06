ClearAll["Global`*"];
edges = {A->B,B->C,C->D,D->E,E->F,F->G,G->HU,G->I,HU->HI,I->HI,HI->J,J->K,K->L,L->M,K->KLM,L->KLM,M->KLM,KLM->N};
g = Graph[edges,DirectedEdges->True];
required = {A,B,C,D,E,F,G,HU,I,HI,J,K,L,M,KLM,N};
reach = VertexList[NeighborhoodGraph[g,A,Infinity]];
result = <|"call" -> "N-WL-001", "reachable" -> (ToString[#,InputForm]& /@ reach),
 "allReachable" -> TrueQ[SubsetQ[reach,required]], "acyclic" -> AcyclicGraphQ[g]|>;
ToString[result, InputForm]
