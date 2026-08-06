# REC-040 Independent Verification

Nine branch heads were independently discovered. Seven point to `b0f21d023f64ce9c70fd4755dfdbb7357b9f7a10` and two to the later lineage. A fresh exact checkout of `b0f21d023f64ce9c70fd4755dfdbb7357b9f7a10` produced 161 tracked-file hashes and five byte-identical admitted source objects. Historical state/PASS labels were never trusted. The stale validator returned 2; that failure is preserved rather than hidden.

**Verdict: PASS.** Exact source recovery is valid at limited scope only.
