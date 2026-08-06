# Triad Kernel Formula Compendium

This chapter collects the major formula forms of the triad and kernel.

## Primitive triad

```text
CIF -> QV -> RFL
```

Meaning:

```text
source possibility -> crossing -> memory
```

## First Action

```text
QV(CIF) -> RFL
```

Meaning:

```text
QV acts on CIF to produce RFL
```

This is the primitive event-kernel.

## Recursive kernel

```text
K_f(t)=sum_{j=1}^{N} delta^{-j} f_j(t) e^{-alpha j t}
```

Interpretation:

```text
f_j(t)          = CIF modal content
delta^{-j}      = recursive depth compression/scaling
e^{-alpha j t}  = QV damping/closure envelope
K_f(t)          = RFL stabilized recursive output
```

## Domain modal basis

```text
f_j(t) -> f_{m,j}(t)
```

Meaning:

```text
same kernel skeleton, domain-specific CIF modal content
```

## Recurrence form

```text
QV(CIF)_n -> RFL_n
RFL_n -> M_rec -> CIF_{n+1}
```

Or compactly:

```text
CIF_s -> QV_s -> RFL_s -> M_rec -> CIF_{s+1}
```

## Weighted triad kernel

```text
K_T=(w_QV QV,w_CIF CIF,w_RFL RFL)
```

With locked weights in the weighted source-packet representation:

```text
w_QV  = 0.984868
w_CIF = 0.005085
w_RFL = 0.010047
```

## Closure scalar form

A downstream closure scalar appears in the sources as a weighted combination of packet terms. The critical lesson is that such a scalar is not the whole kernel. It is downstream of the triad and weighted packet.

## Module projection form

```text
CIF_i = w_CIF Phi_i(H_{i-1})
QV_i  = w_QV Psi_i(CIF_i,H_{i-1})
RFL_i = w_RFL Omega_i(QV_i,H_{i-1})
S_i   = Gamma_i(CIF_i,QV_i,RFL_i,K_closure,H_{i-1})
```

Operator interpretation:

```text
Phi   = opens CIF
Psi   = exposes/selects/compresses through QV
Omega = stabilizes/locks as RFL
Gamma = forms the state
```

## Nucleosynthesis cascade form

```text
Y_{n+1}=RFL_n(QV_n(CIF_n(Y_n)))
```

Meaning:

```text
inherited abundance state -> source channel -> selection/stability -> new abundance memory
```

## Arithmetic legal incidence

```text
6k + sigma = qM
sigma in {-1,+1}
q >= 5 prime
M >= 2
```

Meaning:

```text
QV exposure/deletion is legal only when coupled witness exists
```

## Arithmetic state grammar

```text
S_s=(CIF_s,QV_s,RFL_s;K_s)
CIF_s -> QV_s -> RFL_s -> M_rec -> CIF_{s+1}
```

Meaning:

```text
admitted support -> legal exposure -> obstruction/survivor memory -> next source condition
```

## Universal sentence

All formulae reduce to:

```text
admitted source-possibility exposed to witnessed crossing becomes inheritable memory
```
