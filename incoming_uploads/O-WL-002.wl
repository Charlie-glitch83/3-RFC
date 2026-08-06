ClearAll["Global`*"];
g=Graph[{O->P,O->Q},DirectedEdges->True];
result=<|"call"->"O-WL-002","OtoP"->TrueQ[GraphDistance[g,O,P]<Infinity],
 "OtoQ"->TrueQ[GraphDistance[g,O,Q]<Infinity],"PtoO"->TrueQ[GraphDistance[g,P,O]===Infinity],
 "PtoQ"->TrueQ[GraphDistance[g,P,Q]===Infinity]|>;
ToString[result, InputForm]
