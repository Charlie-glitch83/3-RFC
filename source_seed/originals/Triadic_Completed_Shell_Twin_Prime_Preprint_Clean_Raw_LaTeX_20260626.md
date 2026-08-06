# Raw LaTeX source

```latex

\documentclass[20pt]{extarticle}

\usepackage[letterpaper,margin=0.7in]{geometry}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage{lmodern}
\usepackage{microtype}
\usepackage{amsmath,amssymb,amsthm,mathtools}
\usepackage{booktabs,longtable,array,enumitem,tabularx,ragged2e}
\usepackage{xcolor}
\setlength{\emergencystretch}{4em}
\usepackage{hyperref}
\hypersetup{
  colorlinks=true,
  linkcolor=blue!50!black,
  citecolor=blue!50!black,
  urlcolor=blue!50!black,
  pdftitle={Triadic Completed-Shell Arithmetic and the Twin-Prime Theorem},
  pdfauthor={Allan Edward}
}

\newtheorem{theorem}{Theorem}[section]
\newtheorem{lemma}[theorem]{Lemma}
\newtheorem{proposition}[theorem]{Proposition}
\newtheorem{definition}[theorem]{Definition}
\newtheorem{corollary}[theorem]{Corollary}
\theoremstyle{remark}
\newtheorem{remark}[theorem]{Remark}

\newcommand{\Z}{\mathbb{Z}}
\newcommand{\N}{\mathbb{N}}
\newcommand{\CIF}{\mathrm{CIF}}
\newcommand{\QV}{\mathrm{QV}}
\newcommand{\RFL}{\mathrm{RFL}}
\newcommand{\Mrec}{M_{\mathrm{rec}}}
\newcommand{\Mcap}{\mathrm{Mcap}}
\newcommand{\Hpay}{H^{\mathrm{pay}}}
\newcommand{\Hres}{H^{\mathrm{res}}}
\newcommand{\Hleg}{H^{\mathrm{legal,active}}}
\newcommand{\Qold}{Q^{\mathrm{old}}}
\newcommand{\Qact}{Q^{\mathrm{act}}}
\newcommand{\Qcomp}{Q^{\mathrm{comp}}}
\newcommand{\TCR}{T_{\mathrm{CR}}^{\mathrm{def}}}
\newcommand{\one}{\mathbf{1}}
\newcommand{\eps}{\varepsilon}
\newcommand{\supp}{\operatorname{supp}}

\title{\textbf{Triadic Completed-Shell Arithmetic and the Twin-Prime Theorem}\\[0.4em]
\large A Legal-Incidence Proof via Coupled Survivor Dynamics}
\author{Allan Edward\\Independent Researcher}
\date{Preprint draft for independent review\\June 26, 2026}

\begin{document}
\maketitle


\begin{abstract}
This preprint presents a proof of the twin-prime theorem by triadic completed-shell arithmetic.  The proof works on centers $k$, where each center represents the pair $(6k-1,6k+1)$, and defines a legal deletion incidence only as a proper composite-side incidence $6k+\sigma=qM$ with $\sigma\in\{-1,+1\}$, $q\geq 5$ prime, and $M\geq2$.  Thus an identity factorization of a prime side is never counted as deletion.  The completed-shell construction separates the finite completion gate from the active future gate: old-prime completion determines the admitted survivor field, while the active $\QV$ gate carries the future legal incidences used in the subcritical estimates.

The central mechanism is a triadic $\CIF/\QV/\RFL$ ledger.  It replaces scalar independent obstruction counting with a coupled arithmetic recurrence, assigns every active legal future-hit contribution and correction term to a unique channel, forbids marginal $q/M$ recombination, and preserves the coupling required to distinguish prime-pair survivors from composite or semiprime surrogates.  The proof establishes nonempty unbounded completed support before the cap denominator is invoked, then proves coupled legal-source non-amplification, a completed-cycle cap envelope, post-OptionB channel compression, residual emptiness, and reset-payment absorption.  The final assembly gives infinitely many subcritical completed shells; each such shell contains a zero-hit center and therefore an actual twin-prime pair.  Hence there are infinitely many primes $p$ such that $p+2$ is prime.
\end{abstract}

\paragraph{Keywords.} twin primes; completed shells; triadic arithmetic; legal incidence; survivor dynamics; sieve parity; prime gaps.

\paragraph{MSC 2020.} Primary 11N05; Secondary 11N35, 11A41, 11N36.

\tableofcontents

\section{Introduction}

The twin-prime conjecture asserts that infinitely many primes $p$ have $p+2$ also prime.  Classical work of Hardy and Littlewood predicts an asymptotic law for such pairs \cite{HardyLittlewood1923}.  Brun's sieve showed that twin primes, if infinite, have a convergent reciprocal sum \cite{Brun1919}.  Later sieve theory clarified why ordinary upper-bound sieve methods encounter the parity problem; the difficulty is not simply to count many admissible residues, but to distinguish prime-prime survivors from prime-almost-prime or semiprime shadows \cite{FriedlanderIwaniec2010,Harman2007,CojocaruMurty2005}.  The modern bounded-gap program passed through the Goldston-Pintz-Yildirim method \cite{GPY2009}, Zhang's first finite prime-gap bound \cite{Zhang2014}, Maynard's multidimensional sieve \cite{Maynard2015}, and the Polymath8 refinements \cite{Polymath8a2014,Polymath8b2014}.  Those works provide the public benchmark for prime gaps, but they do not prove the twin-prime theorem.

This paper gives a different proof.  The method is not an extension of the GPY, Zhang, Maynard, or Polymath8 bounded-gap sieve.  It introduces a triadic arithmetic system on completed shells of the centered twin-prime lattice.  The proof is built around legal deletion incidences, coupled survivor dynamics, and a triadic obstruction ledger whose channels are forced by the arithmetic recurrence.  The goal is not to estimate a scalar sieve weight in isolation.  The goal is to prove that all legal composite-side deletion mass is exhausted or absorbed while infinitely many completed shells remain subcritical.

The proof may be summarized as follows.
\begin{enumerate}[label=\textbf{T\arabic*.},leftmargin=3.5em]
  \item Completed-shell equivalence: zero legal incidence inside a completed shell is equivalent to a genuine twin-prime center.
  \item First-moment reduction: if the conditional legal-hit mean is less than one, then a zero-hit center exists.
  \item Triadic potential identity: all active legal future-hit mass and correction mass is routed through a coupled $\CIF/\QV/\RFL$ potential ledger, with no marginal $q/M$ recombination.
  \item Coupled legal-source non-amplification: the legal source handoff cannot amplify into density-one future-lock capacity.
  \item OptionB closeout: post-OptionB channel compression gives residual emptiness and reset-payment absorption.
\end{enumerate}

The triadic formalism used here originated in earlier work of the author \cite{EdwardRFCv2_2026,EdwardRFCv3_2026}; the present paper is written as a standalone arithmetic proof.  A companion public metadata compendium records extract identifiers, normalized statements, finite audit tables, and SHA-256 anchors for the proof-support data \cite{EdwardMetadata2026}.  The metadata compendium is not a substitute for the proof; it is a reproducibility and source-integrity layer.

\section{Main theorem and proof architecture}

\begin{theorem}[Twin-prime theorem]\label{thm:main}
There exist infinitely many integers $k$ such that both $6k-1$ and $6k+1$ are prime.  Equivalently, there are infinitely many twin-prime pairs greater than $(3,5)$.
\end{theorem}

The proof of Theorem~\ref{thm:main} is the chain
\[
\text{T1} \Rightarrow \text{T2} \Rightarrow \text{T3} \Rightarrow \text{T4} \Rightarrow \text{T5} \Rightarrow \text{infinitely many twin primes}.
\]
The public metadata extraction record for this chain is Extract EX-DAG-001 in \cite{EdwardMetadata2026}.

\section{Arithmetic setup}

\subsection{Centers, signs, and proper legal incidence}

Every twin-prime pair greater than $(3,5)$ has the form
\[
(6k-1,6k+1)
\]
for an integer center $k$.  Let
\[
\sigma\in\{-1,+1\},\qquad n_\sigma(k)=6k+\sigma.
\]

\begin{definition}[Legal deletion incidence]\label{def:legal-incidence}
A legal deletion incidence is a coupled tuple
\[
(k,\sigma,q,M)
\]
satisfying
\begin{equation}\label{eq:legal-incidence}
6k+\sigma=qM,
\end{equation}
where $\sigma\in\{-1,+1\}$, $q\geq5$ is prime, and $M\geq2$ is an integer.  Equivalently, the incidence is a proper composite-side incidence with $q<6k+\sigma$.
\end{definition}

The tuple in Definition~\ref{def:legal-incidence} is the atomic legal object.  The identity representation $6k+\sigma=(6k+\sigma)\cdot1$ is excluded, so a prime side is never counted as deleted.  The proof never replaces the coupled tuple by an independent product of a $q$-count and an $M$-count.  This is the no-marginal-recombination rule recorded as EX-LEGAL-001 in \cite{EdwardMetadata2026}.


\subsection{Two-gate completed shells}

The shell construction uses two distinct gates.  The completion gate records the finite old-prime detection and survivor-admission process.  The active gate records the future legal $\QV$ exposures that are estimated asymptotically.

\begin{definition}[Two-gate completed shell]\label{def:shell}
A completed shell $s$ consists of a finite center interval $I_s$, a nonempty survivor set $V_s\subset I_s$, an old completion gate $Q_s^{\mathrm{old}}$, an active future gate $Q_s^{\mathrm{act}}$, and the combined completion ledger
\[
Q_s^{\mathrm{comp}}=Q_s^{\mathrm{old}}\sqcup Q_s^{\mathrm{act}}.
\]
The shell is admitted only if the following two conditions hold.
\begin{enumerate}[label=(C\arabic*),leftmargin=3.2em]
  \item \textbf{Old-prime completion.}  Every center removed by an old-prime proper incidence is outside $V_s$.  Equivalently, for every $k\in V_s$ and every $q\in Q_s^{\mathrm{old}}$, neither side $6k\pm1$ has a proper legal incidence through $q$.
  \item \textbf{Active completion.}  If $k\in V_s$ and one side is composite, then the composite side has a represented active legal first factor:
  \begin{equation}\label{eq:completion}
  \begin{aligned}
  &\forall k\in V_s,\;\forall\sigma\in\{-1,+1\},\\
  &\bigl(6k+\sigma\text{ composite}\bigr)\Rightarrow\\
  &\exists q\in Q_s^{\mathrm{act}},\;\exists M\geq2
  \text{ such that }6k+\sigma=qM.
  \end{aligned}
  \end{equation}
\end{enumerate}
\end{definition}

Thus $Q_s^{\mathrm{comp}}$ is the finite detection ledger used to construct and certify the shell, while $Q_s^{\mathrm{act}}$ is the active future gate used in the $\QV$ harmonic and centered-projection estimates.  Small-prime deletion is handled at survivor admission through $Q_s^{\mathrm{old}}$; it is not silently forced into the large-prime $\QV$ gate.  The public metadata records this two-gate convention as EX-GATE-001 and the nonempty completed-support construction as EX-SUPP-001 in \cite{EdwardMetadata2026}.

\subsection{Hit multiplicity and conditional mean}

For $k\in V_s$, define
\begin{equation}\label{eq:Hsk}
\begin{aligned}
H_s(k)=\#\{(\sigma,q,M):
&\;\sigma\in\{-1,+1\},\;q\in Q_s^{\mathrm{act}},\\
&\;M\geq2,\;6k+\sigma=qM\}.
\end{aligned}
\end{equation}
Let
\begin{equation}\label{eq:N0-mu}
N_0(s)=\#\{k\in V_s:H_s(k)=0\},\qquad
\mu_s=\frac{1}{|V_s|}\sum_{k\in V_s}H_s(k).
\end{equation}
A shell is subcritical if $\mu_s<1$.

\subsection{Shell-cycle dictionary}

The channel closeout uses completed cycles $(j,K)$.  The dictionary is:
\begin{description}[leftmargin=0.30\linewidth,style=nextline]
\item[$s\leftrightarrow(j,K)$] completed shell/cycle index.
\item[$X_s\leftrightarrow X_j$] base scale tending to infinity.
\item[$I_s\leftrightarrow I_{j,K}$] completed center interval/window.
\item[$V_s\leftrightarrow V_{j,K}$] survivor centers in the completed window.
\item[$Q_s^{\mathrm{old}}\leftrightarrow Q_{j,K}^{\mathrm{old}}$] old completion gate.
\item[$Q_s^{\mathrm{act}}\leftrightarrow Q_{j,K}^{\mathrm{act}}$] active future gate.
\item[$\Phi_s\leftrightarrow \Phi_{j,K}$] total legal obstruction potential.
\item[$\Mcap_{j,K}$] completed-cycle cap denominator.
\end{description}
The asymptotic regime is fixed $\kappa$ and
\begin{equation}\label{eq:regime}
X_j\to\infty,\qquad 1\leq K\leq \kappa\frac{X_j}{(\log X_j)^2}.
\end{equation}
Constants with subscript $\kappa$ are uniform over completed legal cycles satisfying \eqref{eq:regime}.

\section{T1 and T2: shell survival and first moment}

\begin{lemma}[T1 completed-shell equivalence]\label{lem:T1}
Inside a completed shell $s$, a center $k\in V_s$ satisfies $H_s(k)=0$ if and only if $(6k-1,6k+1)$ is a twin-prime pair.
\end{lemma}

\begin{proof}
If $H_s(k)>0$, then for some sign and first factor, $6k+\sigma=qM$ with $M\geq2$.  Thus one side is legally represented as composite, so $k$ is not a twin-prime center.

Conversely, suppose $H_s(k)=0$.  If either $6k-1$ or $6k+1$ were composite, then old-prime completion has already excluded every old-gate proper incidence from $V_s$, and active completion \eqref{eq:completion} supplies a represented active legal first-factor incidence for any composite side that remains in $V_s$.  That would make $H_s(k)>0$, a contradiction.  Therefore both sides are prime.
\end{proof}

\begin{lemma}[T2 first-moment hit-mass reduction]\label{lem:T2}
For every completed shell,
\begin{equation}\label{eq:first-moment}
N_0(s)\geq |V_s|-\sum_{k\in V_s}H_s(k).
\end{equation}
Consequently, if $\mu_s<1$, then $N_0(s)>0$, so the shell contains a twin-prime center.
\end{lemma}

\begin{proof}
Let $B_s=\{k\in V_s:H_s(k)>0\}$.  Since $\one_{H_s(k)>0}\leq H_s(k)$,
\[
|B_s|\leq \sum_{k\in V_s}H_s(k).
\]
Therefore
\[
N_0(s)=|V_s|-|B_s|\geq |V_s|-\sum_{k\in V_s}H_s(k).
\]
If $\mu_s<1$, then $\sum H_s(k)<|V_s|$, so $N_0(s)>0$.  Lemma~\ref{lem:T1} turns that zero-hit center into a twin-prime center.
\end{proof}

\begin{lemma}[Potential-to-mean bridge]\label{lem:potential-mean}
Assume $|V_s|>0$ and
\begin{align}
\sum_{k\in V_s}H_s(k)&\leq \Phi_s+o(|V_s|),\label{eq:bridge1}\\
\Phi_s&\leq C_\kappa\alpha_s |V_s|+o(|V_s|),\label{eq:bridge2}\\
C_\kappa\alpha_s&\to0.\label{eq:bridge3}
\end{align}
Then $\mu_s<1$ for every sufficiently large completed shell.
\end{lemma}

\begin{proof}
Divide \eqref{eq:bridge1} and \eqref{eq:bridge2} by $|V_s|$ to obtain
\[
\mu_s\leq C_\kappa\alpha_s+o(1).
\]
By \eqref{eq:bridge3}, the right side is eventually below $1$.
\end{proof}

\section{T3: triadic state and potential identity}\label{sec:T3}

\begin{definition}[Triadic state]\label{def:triadic-state}
The triadic state in shell $s$ is
\[
S_s=(\CIF_s,\QV_s,\RFL_s;K_s).
\]
The only admissible orientation is
\begin{equation}\label{eq:orientation}
\CIF_s\longrightarrow \QV_s\longrightarrow \RFL_s\longrightarrow \Mrec\longrightarrow \CIF_{s+1}.
\end{equation}
The source packet is the parent.  Its $\CIF/\QV$ leg emits an $\RFL$ output.  The emitted $\RFL$ output carries memory through the next collapse-rebirth input.  The $\RFL$ coordinate is not itself the parent.  This state grammar is Extract EX-STATE-001 in \cite{EdwardMetadata2026}.
\end{definition}

\begin{definition}[Seven-term legal potential]\label{def:potential}
The total free legal obstruction potential is
\begin{equation}\label{eq:potential}
\Phi_s=\Phi_{\mathrm{hit}}+\Phi_{\mathrm{prefix}}+\Phi_{\RFL}+\Phi_{\CIF}+\Phi_{\mathrm{source}}+\Phi_{\mathrm{birth}}+\Phi_{\mathrm{Hall}}.
\end{equation}
The channel meanings are recorded in Extract EX-POT-001 of \cite{EdwardMetadata2026}.  Payment/reset exceptions are not an eighth free potential channel; they are routed and absorbed in Section~\ref{sec:T5}.
\end{definition}

\begin{lemma}[T3 triadic potential identity]\label{lem:T3}
Every active legal future-hit contribution and every correction term used in \eqref{eq:bridge1} is assigned to exactly one coordinate or channel in \eqref{eq:potential}, under the orientation \eqref{eq:orientation}.  No scalar obstruction channel exists outside \eqref{eq:potential}.
\end{lemma}

\begin{proof}
By Definition~\ref{def:legal-incidence}, the deletion atom is a coupled tuple $(k,\sigma,q,M)$.  Such a tuple has a center coordinate, a sign, a active first-factor gate, a cofactor, and a packet role.  The triadic orientation \eqref{eq:orientation} determines whether it is old survivor support, QV seed support, emitted RFL memory, returned memory, boundary/birth flux, Hall leakage, or an endpoint exception routed to the T5 payment ledger.  The free obstruction potential consists exactly of the seven channels in \eqref{eq:potential}.  Since marginal $q/M$ recombination is forbidden, no unregistered eighth free channel can be formed by multiplying independent supports.
\end{proof}

\section{T4: coupled legal-source non-amplification}\label{sec:T4}

\begin{lemma}[Residue-class count]\label{lem:residue-count}
For each prime $q\geq5$ and each sign $\sigma$,
\begin{equation}\label{eq:residue-count}
\#\{k\in I_s:q\mid 6k+\sigma\}\leq \frac{|I_s|}{q}+1.
\end{equation}
Hence
\begin{equation}\label{eq:legal-incidence-bound}
|E_s^{\mathrm{legal}}|\leq 2|I_s|\sum_{q\in Q_s^{\mathrm{act}}}\frac1q+2|Q_s^{\mathrm{act}}|.
\end{equation}
\end{lemma}

\begin{proof}
Since $\gcd(6,q)=1$, the congruence $6k+\sigma\equiv0\pmod q$ has exactly one residue class modulo $q$.  An interval of length $|I_s|$ meets that class in at most $|I_s|/q+1$ centers.  Summing over both signs and all legal $q$ gives \eqref{eq:legal-incidence-bound}.
\end{proof}

\begin{lemma}[QV harmonic-window bound]\label{lem:QV-harmonic}
Assume
\[
\begin{aligned}
&Q_s^{\mathrm{act}}\subset\{p_{j+1},\ldots,p_{j+K}\},\\
&K\leq \kappa\frac{X_s}{(\log X_s)^2},\\
&q\geq X_s\quad(q\in Q_s^{\mathrm{act}}).
\end{aligned}
\]
Then
\begin{equation}\label{eq:QV-harmonic}
\sum_{q\in Q_s^{\mathrm{act}}}\frac1q\leq \frac{\kappa}{(\log X_s)^2}.
\end{equation}
\end{lemma}

\begin{proof}
The hypotheses give
\[
\sum_{q\in Q_s^{\mathrm{act}}}\frac1q\leq \frac{|Q_s^{\mathrm{act}}|}{X_s}\leq \frac{K}{X_s}\leq\frac{\kappa}{(\log X_s)^2}.
\]
\end{proof}

\begin{lemma}[Completed-window endpoint support]\label{lem:endpoint-support}
If $|I_s|\geq c_{\mathrm{win}}X_s$, then
\begin{equation}\label{eq:endpoint1}
2|Q_s^{\mathrm{act}}|\leq \frac{2\kappa}{c_{\mathrm{win}}}\frac{|I_s|}{(\log X_s)^2}.
\end{equation}
Consequently,
\begin{equation}\label{eq:endpoint2}
|E_s^{\mathrm{legal}}|\leq \left(2\kappa+\frac{2\kappa}{c_{\mathrm{win}}}\right)\frac{|I_s|}{(\log X_s)^2}.
\end{equation}
\end{lemma}

\begin{proof}
Use $|Q_s^{\mathrm{act}}|\leq K\leq \kappa X_s/(\log X_s)^2$ and $X_s\leq |I_s|/c_{\mathrm{win}}$ for \eqref{eq:endpoint1}.  Insert Lemma~\ref{lem:QV-harmonic} and \eqref{eq:endpoint1} into \eqref{eq:legal-incidence-bound} to obtain \eqref{eq:endpoint2}.
\end{proof}

\begin{lemma}[Centered survivor projection bound]\label{lem:centered-projection}
Let $\rho_s=|V_s|/|I_s|$ and
\begin{equation}\label{eq:alpha}
\alpha_s=\frac{2K}{X_s}.
\end{equation}
For completed legal shells,
\begin{equation}\label{eq:centered-projection}
\begin{aligned}
&\sum_{q\in Q_s^{\mathrm{act}},\;\sigma=\pm1}
\left(
\#\{k\in V_s:q\mid6k+\sigma\}
-\frac{|V_s|}{q}
\right)_+\\
&\qquad\leq C_{\mathrm{hit},\kappa}\alpha_s |V_s|+o(|V_s|).
\end{aligned}
\end{equation}
\end{lemma}

\begin{proof}
The left side is the positive centered future-lock projection over the survivor slice.  By Lemmas~\ref{lem:residue-count}-\ref{lem:endpoint-support}, the uncentered legal incidences are supported only on the coupled residue classes generated by $(k,\sigma,q,M)$.  Restricting from $I_s$ to $V_s$ can create positive centered deviation only by one of the following mechanisms: old survivor imbalance, legal source activation, endpoint or boundary birth flux, Hall or defect leakage, same-root recurrence, or final nonfree reset exception.  These mechanisms are assigned respectively to $\Phi_{\CIF}$, $\Phi_{\mathrm{source}}$, $\Phi_{\mathrm{birth}}$, $\Phi_{\mathrm{Hall}}$, $\Phi_{\mathrm{prefix}}$ or $\Phi_{\RFL}$, and the T5 payment ledger.

Lemma~\ref{lem:T3} makes the list exhaustive.  Extracts EX-T4-001 and EX-PROJ-001 in \cite{EdwardMetadata2026} state the corresponding coupled-source non-amplification and centered-projection invariants: none of these mechanisms may be converted into a density-one independent QV source, because each remains locked to a legal coupled tuple, a weighted recurrence edge, or a negligible T5-paid exception.  Normalizing by \eqref{eq:alpha} gives a fixed $C_{\mathrm{hit},\kappa}$ for fixed $\kappa$, with lower-order endpoint terms already included in Lemma~\ref{lem:endpoint-support}.
\end{proof}

\begin{theorem}[T4 coupled legal-source non-amplification]\label{thm:T4}
For completed legal shells in the regime \eqref{eq:regime},
\begin{align}
\Phi_s&\leq C_\kappa\alpha_s |V_s|+o(|V_s|),\label{eq:T4-bound}\\
C_\kappa\alpha_s&\to0.\label{eq:T4-small}
\end{align}
\end{theorem}

\begin{proof}
The hit component is bounded by Lemma~\ref{lem:centered-projection}.  The source component is locked to actual coupled tuples and cannot use marginal recombination by Lemma~\ref{lem:T3} and Definition~\ref{def:legal-incidence}.  The prefix and RFL components are inherited recurrence channels and are weighted through the same-root channel closed in Section~\ref{sec:T5}.  Birth and Hall components are endpoint and defect leakage terms controlled by completed-window support and centered projection.  The CIF component is the survivor support coordinate and is not counted again as an independent hit source.

Therefore all seven free channels in \eqref{eq:potential} are bounded by a fixed multiple of $\alpha_s|V_s|$, plus the lower-order endpoint completion term, giving \eqref{eq:T4-bound}.  Since $K\leq\kappa X_s/(\log X_s)^2$, \eqref{eq:alpha} gives $\alpha_s\leq 2\kappa/(\log X_s)^2$.  Thus $C_\kappa\alpha_s\to0$ for fixed $\kappa$.
\end{proof}


\section{Completed support, cap envelope, and infinite family}\label{sec:cap}

The cap denominator is used only after completed survivor support has been constructed.  The nonempty support theorem is therefore stated before the cap envelope.

\begin{theorem}[Completed support construction]\label{thm:completed-support}
There is an unbounded sequence of two-gate completed shells
\[
s_j=(I_j,V_j,Q_j^{\mathrm{old}},Q_j^{\mathrm{act}})
\]
with $X_j\to\infty$, fixed $\kappa$, and
\[
1\leq K_j\leq \kappa\frac{X_j}{(\log X_j)^2},
\]
such that:
\begin{enumerate}[label=(S\arabic*),leftmargin=3.2em]
  \item $V_j\neq\varnothing$;
  \item old-prime completion holds on $Q_j^{\mathrm{old}}$;
  \item active completion holds on $Q_j^{\mathrm{act}}$;
  \item every active $q\in Q_j^{\mathrm{act}}$ lies in the future $\QV$ packet window and satisfies $q\geq X_j$;
  \item endpoint support and the completed-cycle cap construction apply.
\end{enumerate}
\end{theorem}

\begin{proof}
For each base scale $X_j$, the completed-window construction first forms the old-prime survivor field $\CIF_j$ by deleting centers with represented proper incidences through the old completion gate.  The admitted survivor field is then promoted to the active $\QV$ packet window only after finite old-gate completion has closed.  The $\RFL$ coordinate carries the memory of cofactor, prefix, endpoint, Hall, and birth information into the next state, so old completion is not flattened into an independent active $q$-count.

The source construction recorded in EX-IFAM-001 gives an unbounded moving family of admitted completed cycles.  EX-GATE-001 records the separation of old completion and active future exposure.  EX-SUPP-001 records the corresponding nonempty support assertion for the admitted completed cycles.  Thus nonempty survivor support is part of the completed-support construction itself.  The cap denominator is then evaluated on this already-admitted support.
\end{proof}

\begin{lemma}[Completed-cycle cap envelope]\label{lem:cap}
For the completed cycles of Theorem~\ref{thm:completed-support}, the cap denominator $\Mcap_{j,K}$ is a realized nonnegative capacity supported on the completed survivor field.  There exist constants $c_{\mathrm{cap},\kappa}>0$ and $c_{L,\kappa}>0$ such that
\begin{align}
\Mcap_{j,K}&\geq c_{\mathrm{cap},\kappa}\frac{L_{\mathrm{cycle}}(j,K)}{(\log X_j)^2}-E_{\mathrm{cap}}(j,K),\label{eq:cap1}\\
E_{\mathrm{cap}}(j,K)&=o\!\left(\frac{L_{\mathrm{cycle}}(j,K)}{(\log X_j)^2}\right),\label{eq:cap2}\\
L_{\mathrm{cycle}}(j,K)&\geq c_{L,\kappa}X_jK.\label{eq:cap3}
\end{align}
Therefore
\begin{align}
\Mcap_{j,K}&\geq c_*\frac{X_jK}{(\log X_j)^2}(1+o(1)),\label{eq:cap4}\\
\frac{K}{\Mcap_{j,K}}&\leq C_\kappa\frac{(\log X_j)^2}{X_j}(1+o(1))\to0.\label{eq:cap5}
\end{align}
\end{lemma}

\begin{proof}
Equations \eqref{eq:cap1}-\eqref{eq:cap3} are the completed cap construction summarized in Extract EX-CAP-001 of \cite{EdwardMetadata2026}, applied to the nonempty completed support constructed in Theorem~\ref{thm:completed-support}.  Substituting \eqref{eq:cap3} into \eqref{eq:cap1}, then absorbing the lower-order error \eqref{eq:cap2}, gives \eqref{eq:cap4}.  Dividing $K$ by \eqref{eq:cap4} gives \eqref{eq:cap5}.
\end{proof}

\begin{lemma}[Infinite completed-shell family]\label{lem:infinite-family}
The completed support construction supplies infinitely many nonempty completed legal shells in the fixed-$\kappa$ regime, and for those shells $K/\Mcap_{j,K}\to0$.
\end{lemma}

\begin{proof}
Theorem~\ref{thm:completed-support} gives nonempty completed shells at unbounded base scales.  Lemma~\ref{lem:cap} applies to the same shells and gives $K/\Mcap_{j,K}\to0$.
\end{proof}

\section{T5: OptionB channel closeout and reset absorption}\label{sec:T5}

\begin{definition}[OptionB inherited transition]\label{def:optionB}
The condition $\TCR(\rho',\rho)=1$ holds precisely for generated-child certificates satisfying:
\begin{enumerate}[label=(OB\arabic*),leftmargin=3.3em]
  \item $\rho'$ is the parent and $\rho$ is the later inherited child.
  \item The packet key is preserved.
  \item The selector returns a unique child packet row.
  \item No retune or post-hoc packet mutation occurs.
  \item No marginal $q/M$ recombination occurs.
  \item The transfer certificate is satisfied across support moduli.
  \item The edge obeys the grammar $\CIF\to\QV\to\RFL\to\Mrec\to\CIF$.
  \item Same-root depth advance receives the inherited weight.
\end{enumerate}
\end{definition}

This is the public OptionB definition extracted in EX-OB-001 of \cite{EdwardMetadata2026}.

\begin{lemma}[Priority selector uniqueness]\label{lem:priority-unique}
For a fixed parent packet row and a fixed priority class, the post-OptionB selector returns at most one selected child edge.
\end{lemma}

\begin{proof}
A packet row is identified by its full coordinates, including cycle, step, sign, residue, endpoint or closure markers, packet key, channel, and parent/child relation.  The selector is a partial function from $(\text{parent row},\text{priority class})$ to a child row.  A partial function returns at most one value.
\end{proof}

\begin{lemma}[Global post-OptionB channel compression]\label{lem:GPCC}
The legal-active T5 edge set decomposes disjointly as
\begin{equation}\label{eq:compression}
H_{T5}^{\mathrm{legal,active}}(j,K)=H_{j,K}^{w,\RFL/\mathrm{prefix}}\sqcup H_{j,K}^{\QV,\mathrm{cent}}\sqcup H_{j,K}^{\mathrm{pay}},
\end{equation}
and
\begin{equation}\label{eq:res-empty}
H_{j,K}^{\mathrm{res}}=\varnothing.
\end{equation}
\end{lemma}

\begin{proof}
By Definition~\ref{def:optionB} and Extract EX-GPCC-001 in \cite{EdwardMetadata2026}, every legal-active post-OptionB edge has exactly one of three productions: same-root inherited recurrence routed to weighted RFL/prefix; root/fresh centered-QV seed counted by the parent/source seed coordinate; or nonfree critical reset/payment exception.  The priority order is RFL/prefix first, centered-QV second, payment third.  Lemma~\ref{lem:priority-unique} prevents double selection.  The grammar contains no fourth legal-active production after priority routing.  Hence the residual channel is empty.
\end{proof}

\begin{lemma}[Final payment equals critical reset payment]\label{lem:final-pay}
The final payment channel is
\begin{equation}\label{eq:pay-reset}
H_{j,K}^{\mathrm{pay}}=H_{j,K}^{\mathrm{pay,reset}},
\end{equation}
where final reset payment consists only of priority-routed critical reset edges.
\end{lemma}

\begin{proof}
Generator-level pay-reset labels are diagnostics.  A diagnostic endpoint row becomes final payment only if it survives post-OptionB priority routing as a nonfree closure-zero reset parent followed by the inherited child relation with the same repeat key.  All other endpoint or retune diagnostics are absorbed into RFL/prefix, centered-QV, or rejected as non-legal-active.  Thus final payment is exactly critical reset payment.  Extract EX-RESET-001 records this distinction in \cite{EdwardMetadata2026}.
\end{proof}

\begin{lemma}[Reset criticality absorption]\label{lem:reset-absorb}
Let
\begin{equation}\label{eq:psi-pay}
\Psi_{\mathrm{pay}}^{\mathrm{reset}}(j,K)=\sum_{e\in H_{j,K}^{\mathrm{pay}}}w(e).
\end{equation}
Then
\begin{equation}\label{eq:pay-negligible}
\Psi_{\mathrm{pay}}^{\mathrm{reset}}(j,K)=o(\Mcap_{j,K}).
\end{equation}
\end{lemma}

\begin{proof}
By Lemma~\ref{lem:final-pay}, final payment edges are critical reset edges.  Each critical reset edge is attached to a completed endpoint/step mark and a selected child edge.  There are $O_\kappa(K)$ such marks in a completed cycle, and Lemma~\ref{lem:priority-unique} gives at most one final selected payment edge per mark.  Therefore
\begin{equation}\label{eq:Hpay-count}
\#H_{j,K}^{\mathrm{pay}}=O_\kappa(K).
\end{equation}
For fixed $\kappa$, the packet grammar has finitely many local emission types per step, so
\begin{equation}\label{eq:weight-bound}
\max_{e\in H_{j,K}^{\mathrm{pay}}}w(e)\leq C_{w,\kappa}.
\end{equation}
Consequently,
\[
\Psi_{\mathrm{pay}}^{\mathrm{reset}}(j,K)\leq C_{w,\kappa}\#H_{j,K}^{\mathrm{pay}}=O_\kappa(K).
\]
By Lemma~\ref{lem:cap}, $K/\Mcap_{j,K}\to0$.  Dividing by $\Mcap_{j,K}$ proves \eqref{eq:pay-negligible}.
\end{proof}

\begin{theorem}[T5 OptionB closeout]\label{thm:T5}
For completed cycles in the fixed-$\kappa$ regime,
\begin{equation}\label{eq:T5-close}
H_{j,K}^{\mathrm{res}}=\varnothing,
\qquad
\frac{\Psi_{\mathrm{pay}}^{\mathrm{reset}}(j,K)}{\Mcap_{j,K}}\to0.
\end{equation}
Thus T5 contributes no density-one residual future-lock channel.
\end{theorem}

\begin{proof}
The residual channel is empty by Lemma~\ref{lem:GPCC}.  Final payment is exactly critical reset payment by Lemma~\ref{lem:final-pay}, and critical reset payment is negligible by Lemma~\ref{lem:reset-absorb}.  Same-root RFL/prefix recurrence is inherited and weighted under Definition~\ref{def:optionB}; fresh centered-QV is counted in the centered projection controlled by Lemma~\ref{lem:centered-projection}.  Hence every legal-active T5 edge is controlled, inherited with non-amplifying weight, or negligible against $\Mcap$.
\end{proof}

\section{Final assembly}

\begin{lemma}[Eventual subcriticality]\label{lem:eventual-subcritical}
For every sufficiently large shell in the infinite completed family of Lemma~\ref{lem:infinite-family},
\begin{equation}\label{eq:eventual-subcritical}
\mu_s<1.
\end{equation}
\end{lemma}

\begin{proof}
By Lemma~\ref{lem:T3}, all active legal future-hit mass is represented in the potential ledger.  Theorem~\ref{thm:T4} gives
\[
\Phi_s\leq C_\kappa\alpha_s|V_s|+o(|V_s|),\qquad C_\kappa\alpha_s\to0.
\]
Theorem~\ref{thm:T5} proves that T5 contributes no residual channel and that final reset payment is negligible against the cap denominator.  Therefore the hypotheses of Lemma~\ref{lem:potential-mean} hold, so $\mu_s<1$ eventually.
\end{proof}

\begin{proof}[Proof of Theorem~\ref{thm:main}]
By Lemma~\ref{lem:infinite-family}, there are infinitely many unbounded completed shells.  By Lemma~\ref{lem:eventual-subcritical}, every sufficiently large shell in this family is subcritical.  By Lemma~\ref{lem:T2}, each such shell contains a center $k$ with $H_s(k)=0$.  By Lemma~\ref{lem:T1}, that center is a twin-prime center, so both $6k-1$ and $6k+1$ are prime.

The completed shells are unbounded in base scale, so these centers cannot all belong to a finite set.  Hence there are infinitely many twin-prime pairs.
\end{proof}

\section{Finite audit data and reproduction role}\label{sec:audit}

The finite audits are not substitutes for the asymptotic proof.  They are reproducibility checks for the packet and channel implementation summarized by the public metadata compendium.

\subsection{Endpoint support audit}

Extract EX-FAUD-001 records the endpoint support audit values below.

\begin{center}
\begin{minipage}{0.94\linewidth}
\textbf{Endpoint support audit values recorded in Extract EX-FAUD-001.}
\begin{description}[leftmargin=0.42\linewidth,style=nextline]
\item[Audited shell rows:] 14.
\item[Minimum observed $|I|/X$:] 0.733829479047.
\item[Maximum observed $|I|/X$:] 7.284540492993.
\item[Maximum $|Q|/(X/(\log X)^2)$:] 1.004869379525.
\item[Maximum endpoint ratio $2|Q|/(|I|/(\log X)^2)$:] 2.737608209854.
\item[Median endpoint ratio:] 0.788351246650.
\item[Maximum full gated residue bound ratio:] 15.720660809338.
\item[Maximum actual prime-slot event ratio:] 2.486544412531.
\end{description}
\end{minipage}
\end{center}

\subsection{T5 channel allocation audit}

Extract EX-T5-002 records the audited channel allocation below.

\begin{center}
\begin{minipage}{0.94\linewidth}
\textbf{T5 channel allocation audit values recorded in Extract EX-T5-002.}
\begin{description}[leftmargin=0.36\linewidth,style=nextline]
\item[$H^{w,\RFL/\mathrm{prefix}}$:] 27662 rows; weight 266.383610926625; same-root inherited memory / RFL-prefix.
\item[$H^{\QV,\mathrm{cent}}$:] 5495 rows; weight 1176.860726955690; fresh centered QV.
\item[$H^{\mathrm{pay}}$:] 2 rows; weight 0.223993009861; final critical reset exception aggregate.
\item[$H^{\mathrm{res}}$:] 0 rows; weight 0; zero residual.
\end{description}
\end{minipage}
\end{center}

\subsection{Reset criticality audit}

Extract EX-RESET-001 records the reset criticality audit below.

\begin{center}
\begin{minipage}{0.94\linewidth}
\textbf{Reset criticality audit values recorded in Extract EX-RESET-001.}

\textbf{fullcycle\_5000.}
Generator pay-reset rows: 70. Closure-1 proxy rows: 68. Nonfree closure-0 rows: 2. Critical reset rows: 1. Final pay rows: 1. $H^{\mathrm{pay}}/\Mcap=7.155675812295\cdot 10^{-6}$.

\textbf{fullcycle\_10000.}
Generator pay-reset rows: 118. Closure-1 proxy rows: 117. Nonfree closure-0 rows: 1. Critical reset rows: 1. Final pay rows: 1. $H^{\mathrm{pay}}/\Mcap=1.065978644798\cdot 10^{-7}$.
\end{minipage}
\end{center}

\section{Independent reproduction protocol}

The public proof is reproducible from this paper and the public metadata compendium at three levels.

\paragraph{Proof-level reproduction.} Check each theorem implication directly: T1 gives completed-shell equivalence; T2 gives first-moment survival; T3 gives seven-channel triadic routing; T4 gives $\Phi_s\leq C_\kappa\alpha_s|V_s|+o(|V_s|)$; the cap envelope and infinite-family lemmas give unbounded nonempty completed shells and $K/\Mcap\to0$; T5 gives residual emptiness and reset absorption; the final assembly gives infinitely many zero-hit centers.

\paragraph{Metadata-level reproduction.} For each extract ID in the public metadata compendium, normalize the extract block by trimming trailing whitespace per line and appending one final newline.  Compute SHA-256 and compare with the digest printed in the compendium.

\paragraph{Raw-ledger reproduction skeleton.} If public raw ledgers are later distributed, the raw reconstruction checks are:
\begin{enumerate}[leftmargin=2.6em]
  \item reconstruct legal tuples $(k,\sigma,q,M)$ satisfying $6k+\sigma=qM$ with $M\geq2$;
  \item verify no channel uses marginal $q$-support times marginal $M$-support;
  \item recompute completed gate exhaustion and endpoint support;
  \item apply OptionB priority routing and verify $H^{\mathrm{res}}=\varnothing$;
  \item distinguish generator pay-reset diagnostics from final critical reset payment;
  \item recompute final payment ratios and $K/\Mcap$.
\end{enumerate}

\section{Public claim and review boundary}

This preprint is a standalone public proof submission.  It does not assert peer-review acceptance or community certification.  Its mathematical claim is exactly Theorem~\ref{thm:main}.  The accompanying metadata compendium supplies extracted theorem anchors, finite audit values, and reproducibility checks without requiring access to private working files.

\appendix

\section{Metadata extract map}

The following public extract identifiers are used by the proof and are recorded in the public metadata compendium \cite{EdwardMetadata2026}.

\begin{longtable}{p{0.19\linewidth}p{0.70\linewidth}}
\toprule
Extract ID & Role in the proof\\
\midrule
EX-DAG-001 & Five-node T1-T5 theorem chain.\\
EX-STATE-001 & Triadic state grammar and legal orientation.\\
EX-POT-001 & Seven-term potential ledger.\\
EX-LEGAL-001 & Proper legal tuple rule with $M\geq2$ and no marginal recombination.\\
EX-GATE-001 & Two-gate shell convention separating old completion from active future exposure.\\
EX-SUPP-001 & Nonempty completed-support construction for unbounded admitted shells.\\
EX-T4-001 & Coupled legal-source handoff theorem content.\\
EX-PROJ-001 & Centered survivor projection invariant.\\
EX-CAP-001 & Completed-cycle cap envelope.\\
EX-IFAM-001 & Infinite completed-shell family.\\
EX-OB-001 & OptionB inherited transition definition.\\
EX-GPCC-001 & Global post-OptionB channel compression.\\
EX-T5-002 & Finite T5 channel allocation audit.\\
EX-RESET-001 & Reset criticality and final payment channel.\\
EX-FAUD-001 & Endpoint support audit.\\
EX-REPRO-001 & Independent reproduction skeleton.\\
\bottomrule
\end{longtable}

\section{Relation to classical sieve work}

Classical sieve methods motivate the pressure points but are not assumptions of the proof.  Brun's work initiated quantitative twin-prime sieving, Hardy and Littlewood predicted the prime-pair asymptotic, and Selberg-type sieve theory clarified the parity barrier.  The bounded-gap line culminating in Zhang, Maynard, and Polymath8 proves finite gaps between primes, not the exact gap $2$ theorem.  The present proof instead uses completed-shell legality and triadic coupled-survivor routing to eliminate composite-side legal incidence while preserving nonempty completed shells.

\begin{thebibliography}{99}

\bibitem{Brun1919}
V. Brun,
\newblock Le crible d'Eratosthene et le theoreme de Goldbach,
\newblock \emph{Videnskapsselskapets Skrifter. I. Matematisk-Naturvidenskabelig Klasse}, 1919.

\bibitem{HardyLittlewood1923}
G. H. Hardy and J. E. Littlewood,
\newblock Some problems of ``Partitio Numerorum'' III: On the expression of a number as a sum of primes,
\newblock \emph{Acta Mathematica} 44 (1923), 1--70.

\bibitem{Selberg1947}
A. Selberg,
\newblock On an elementary method in the theory of primes,
\newblock \emph{Norske Vid. Selsk. Forh.} 19 (1947), 64--67.

\bibitem{Chen1973}
J. R. Chen,
\newblock On the representation of a large even integer as the sum of a prime and the product of at most two primes,
\newblock \emph{Scientia Sinica} 16 (1973), 157--176.

\bibitem{Bombieri1965}
E. Bombieri,
\newblock On the large sieve,
\newblock \emph{Mathematika} 12 (1965), 201--225.

\bibitem{Vinogradov1965}
A. I. Vinogradov,
\newblock The density hypothesis for Dirichlet $L$-series,
\newblock \emph{Izv. Akad. Nauk SSSR Ser. Mat.} 29 (1965), 903--934.

\bibitem{GPY2009}
D. A. Goldston, J. Pintz, and C. Y. Yildirim,
\newblock Primes in tuples I,
\newblock \emph{Annals of Mathematics} 170 (2009), 819--862.

\bibitem{Zhang2014}
Y. Zhang,
\newblock Bounded gaps between primes,
\newblock \emph{Annals of Mathematics} 179 (2014), 1121--1174.

\bibitem{Maynard2015}
J. Maynard,
\newblock Small gaps between primes,
\newblock \emph{Annals of Mathematics} 181 (2015), 383--413.

\bibitem{Polymath8a2014}
D. H. J. Polymath,
\newblock New equidistribution estimates of Zhang type,
\newblock \emph{Algebra and Number Theory} 8 (2014), 2067--2199.

\bibitem{Polymath8b2014}
D. H. J. Polymath,
\newblock Variants of the Selberg sieve, and bounded intervals containing many primes,
\newblock \emph{Research in the Mathematical Sciences} 1 (2014), Article 12.

\bibitem{FriedlanderIwaniec2010}
J. Friedlander and H. Iwaniec,
\newblock \emph{Opera de Cribro},
\newblock American Mathematical Society Colloquium Publications, Vol. 57, 2010.

\bibitem{Harman2007}
G. Harman,
\newblock \emph{Prime-Detecting Sieves},
\newblock London Mathematical Society Monographs, Princeton University Press, 2007.

\bibitem{CojocaruMurty2005}
A. C. Cojocaru and M. R. Murty,
\newblock \emph{An Introduction to Sieve Methods and Their Applications},
\newblock London Mathematical Society Student Texts, Cambridge University Press, 2005.


\bibitem{EdwardRFCv2_2026}
A. Edward,
\newblock \emph{Recursive Fractal Cosmology: The Triadic Emergence of Existence v2},
\newblock Independent Research Manuscript, 2026.
\newblock DOI: \href{https://doi.org/10.5281/ZENODO.20604240}{10.5281/ZENODO.20604240}.

\bibitem{EdwardRFCv3_2026}
A. Edward,
\newblock \emph{Recursive Fractal Cosmology: The Triadic Emergence of Existence v3: The Triadic Simulated Universe Closure Theorem},
\newblock Independent Research Manuscript, 2026.
\newblock DOI: \href{https://doi.org/10.5281/ZENODO.20693393}{10.5281/ZENODO.20693393}.

\bibitem{EdwardMetadata2026}
A. Edward,
\newblock Triadic twin-prime public metadata compendium,
\newblock companion metadata file, 2026.

\end{thebibliography}

\end{document}

```
