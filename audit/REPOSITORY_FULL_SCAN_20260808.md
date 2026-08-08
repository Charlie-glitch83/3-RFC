# Full repository pre-repair scan — 2026-08-08

Every tracked file on `agent/frontier-050-execution` was opened as bytes and SHA-256 inventoried before the B-G repair. Text files were decoded and line-counted where UTF-8; binary files were hashed; ZIPs were opened and member-counted. This machine inventory complements the file-by-file semantic soak that preceded the repair.

- tracked files scanned: `1127`
- read errors: `0`
- pre-repair Git head: `94e62d99a68f31c60714928bbc98aaba488aa618`

See `audit/REPOSITORY_FULL_SCAN_20260808_PRE_REPAIR.json` for the complete path/hash inventory.
