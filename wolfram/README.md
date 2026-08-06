# Wolfram Execution Library

Every `.wl` file is self-contained because connected Wolfram kernels may be stateless. The work model must submit the exact file through the connected `WolframLanguageEvaluator`, save the complete returned output, and register its hash.

Do not use Wolfram|Alpha public knowledge during Modules A-O or Q. Use the Wolfram Language evaluator for symbolic algebra, exact simplification, differential equations, matrices, tensors, stability, units, and high-precision numerical checks.

Commands:

```bash
python tools/director.py wolfram-list --module A
python tools/director.py wolfram-show --call A-WL-001
python tools/director.py wolfram-record --run <RUN_ID> --call A-WL-001 --output <captured-output.txt>
```

A Wolfram PASS proves only the obligation named by that call. It never promotes a module to physical execution.
