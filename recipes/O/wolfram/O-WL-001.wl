ClearAll["Global`*"];
packet=<|"universe"->"U0","predictions"->{6/5,17/5},"falsifiers"->{"F1"}|>;
serialized=ExportString[KeySort[packet],"RawJSON"];
h1=Hash[serialized,"SHA256","HexString"];
mut=ReplacePart[packet,"predictions"->{6/5,7/2}];
h2=Hash[ExportString[KeySort[mut],"RawJSON"],"SHA256","HexString"];
result=<|"call"->"O-WL-001","hash"->h1,"mutatedHash"->h2,"mutationDetected"->TrueQ[h1=!=h2]|>;
ToString[result, InputForm]
