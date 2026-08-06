# Module Closure Standard

A module closes only when:

- exact parents and source hashes are present;
- its derivation is formalized;
- implementation is reproducible;
- physical execution exists where the module owns physical execution;
- mandatory gates pass individually;
- countermodels and ablations behave as predeclared;
- uncertainty/covariance and numerical error are propagated;
- restart/replay and independent reconstruction pass;
- outputs are frozen after all files stop changing;
- the artifact and run registries are updated;
- strongest supported and unsupported claims are stated;
- the GitHub commit SHA and diff are verified.

A module may close at a lower evidence state only when the queue explicitly calls for that lower scope. It may not be called physically complete.
