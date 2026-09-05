# idea 173 — is-the-ladder-endpoint-a-general-selector-artefact (cloud, 2026-09-05)

**Verdict: SPLIT. KILL of the QUEUE's generalisation — the endpoint signature is NOT a property
of ladders, it is a property of (monotone ladder) × (incumbent parked at the far end).
KEEP of the underlying worry for three of five dials. One 4b by-product, PARKed.**

Script `2026-09-05_is-the-ladder-endpoint-a-general-selector-artefact_cloud.py`.
234 engine runs → 468 ladder-point rows (`.grid.csv`, every point reported), 90 ladder
instances (`.instances.csv`), 90 rule-8 walk-forwards (`.walkforward.csv`), the anchor-position
control (`.anchorposition.csv`) and the textual census (`.census.csv`). Deterministic, seed 173.

## Corpus

3 panels (u56 56 cols · broad 136 · small 440 after dropping the 44 tickers with
`max_1d_move >= 1.0`) × 3 signals (COMP / MOM / R6) × 2 cost rungs (10, 25 bps, derived exactly
from the 0 bps run and the engine's own turnover series) = 18 book-cells. Each is laddered on
five dials, one at a time, everything else at the anchor **n=20, g=0.75, freq=W, max_vol=0.60,
p=0.5** — which is **interior in all five ladders** (rank 3/7, 3/5, 2/4, 3/5, 3/5). Book is one
convention only: `w = (rank<=n) * g/n` on `(px > 200d MA) & (vol20 < max_vol)`, cash for empty
slots, t+1 execution. Exactly one tuned parameter per row.

Reference books: SPY 15.23% / **0.889** / −33.72% (H1 0.957 / H2 0.834, OOS 0.882);
RULES v1 @10bps u56 6.45% / 0.664 / −13.83%, broad 6.39% / 0.635, small 7.41% / 0.565.

## m1 — endpoint share of the OOS oracle (18 cells per ladder)

| ladder | K | null 2/K | oracle@end | IS@end | IS=oracle | null 1/K |
|---|---|---|---|---|---|---|
| GROSS | 7 | 0.286 | 0.611 | 0.556 | 0.444 | 0.143 |
| COUNT | 5 | 0.400 | 0.667 | 0.333 | 0.111 | 0.200 |
| CADENCE | 4 | 0.500 | **0.000** | 0.333 | 0.556 | 0.250 |
| VOLCAP | 5 | 0.400 | 0.722 | 0.556 | 0.333 | 0.200 |
| VOLPOW | 5 | 0.400 | 0.722 | 0.556 | 0.389 | 0.200 |

Which end: COUNT high 12/18 (never low), VOLCAP high 13/18 (never low), VOLPOW **low 10/18**,
GROSS split 5 low / 6 high / 7 interior, CADENCE **interior 18/18**.

## m2 — monotonicity, Spearman(ladder rank, OOS Sharpe)

| ladder | mean within-cell rho | rho(rank, MEAN OOS) | mean OOS Sharpe by ladder point |
|---|---|---|---|
| GROSS | −0.028 | +0.21 | 0.45 **0.720** · 0.60 0.720 · 0.75 0.720 · 0.90 0.721 · 1.05 0.721 · 1.20 0.720 · 1.35 0.720 |
| COUNT | +0.533 | **+1.00** | 5 0.599 · 10 0.676 · 20 0.720 · 40 0.818 · 80 **0.863** |
| CADENCE | +0.378 | +0.40 | D 0.476 · W 0.720 · M **0.831** · Q 0.649 |
| VOLCAP | +0.811 | **+1.00** | 0.30 0.569 · 0.45 0.664 · 0.60 0.720 · 0.80 0.746 · none **0.784** |
| VOLPOW | −0.456 | **−1.00** | 0.00 **0.782** · 0.25 0.752 · 0.50 0.720 · 0.75 0.686 · 1.00 0.684 |

**Three of five dials are perfectly monotone in the across-book mean.** Their published
"the argmax is X" claims are grid-edge statements: X is wherever the project stopped the grid.
**GROSS is not monotone — it is FLAT.** Its entire mean OOS Sharpe range over a 3× gross span
is **0.003** (0.720 → 0.721), so its argmax is decided by noise; the 67% of GROSS cells with
|rho| ≥ 0.9 point in inconsistent directions and cancel to a mean rho of −0.028.

## m3 — capture of the oracle, IS-argmax vs RANDOM (paired, 18 cells per ladder)

| ladder | ΔIS | t | ΔRANDOM | t | Δoracle | cap_IS (med) | cap_RND (med) | IS>RND |
|---|---|---|---|---|---|---|---|---|
| GROSS | +0.0002 | 0.42 | −0.0002 | −1.47 | 0.0011 | 0.000 | −0.616 | 0.611 |
| COUNT | +0.0387 | 0.97 | +0.0149 | 0.98 | 0.1862 | 0.000 | +0.097 | 0.333 |
| CADENCE | +0.0462 | 1.44 | **−0.0513** | **−5.33** | 0.1155 | **1.000** | −0.323 | **0.833** |
| VOLCAP | +0.0142 | 0.50 | −0.0239 | −3.15 | 0.0706 | 0.495 | −0.221 | 0.722 |
| VOLPOW | +0.0400 | **2.27** | +0.0043 | 0.63 | 0.0785 | 0.112 | −0.086 | 0.722 |

## m4 — the decisive control: is it the ladder, or where the constant sits on it?

Idea 171 measured "RANDOM also beats the constant" with the constant at **f = 0, the LOW end**
of a sleeve-fraction ladder. Re-pricing RANDOM on these same 468 points against three reference
constants settles it:

| ladder | anchor rank | Δrand vs ANCHOR (interior) | win | vs LOW end | win | vs HIGH end | win |
|---|---|---|---|---|---|---|---|
| GROSS | 3/7 | −0.0002 | 0.33 | +0.0004 | 0.61 | +0.0003 | 0.61 |
| COUNT | 3/5 | +0.0149 | 0.67 | **+0.1362** | **0.94** | −0.1275 | 0.28 |
| CADENCE | 2/4 | −0.0513 | 0.11 | **+0.1934** | **0.94** | +0.0199 | 0.61 |
| VOLCAP | 3/5 | −0.0239 | 0.22 | **+0.1276** | **1.00** | −0.0876 | 0.00 |
| VOLPOW | 3/5 | +0.0043 | 0.28 | −0.0576 | 0.22 | +0.0407 | **0.72** |

**Pooled over all 90 instances: RANDOM beats an INTERIOR constant in 0.32 of them, a LOW-end
constant in 0.74, a HIGH-end constant in 0.44.** VOLPOW is the sign-consistent exception — its
ladder runs downhill (rho −1.00), so its bad end is the HIGH one and RANDOM beats a high-end
constant 0.72 of the time there. In every case RANDOM's "win" tracks which end the constant
sits on, not the ladder's existence. Idea 171's random-beats-constant result reproduces
**only** in the low-end-constant column, which is exactly where f = 0 sits.

## PROTOCOL rule 8 — the IS pick read ONCE on 2017–2026 (90 instances)

| | IS pick | anchor (do-nothing) | RULES v1 | SPY |
|---|---|---|---|---|
| mean OOS Sharpe | 0.7483 | 0.7205 | 0.4229 | **0.8820** |
| mean OOS CAGR | 10.30% | 8.81% | 4.39% | 15.45% |
| mean OOS MaxDD | −26.13% | −22.80% | −26.24% | −33.72% |

Selection beats the do-nothing control by **+0.028** of mean OOS Sharpe, and per dial only
VOLPOW reaches t = 2.27 (uncorrected, 5 tests); CADENCE t = 1.44, GROSS t = 0.42. IS pick beats
SPY's OOS Sharpe in 42/90, anchor 35/90. Both KEEP paths, all 90: **4a(full) 28/90 (anchor 35),
4b(full) 18/90 (anchor 15), 4b(OOS window) 17/90 (anchor 15)** — pre-registered P5 predicted
fewer than 10 and was wrong. 15 of the 17 OOS-window passes are the u56 panel.

## Predictions

* **P1 FAILS at its own bar.** No dial reaches oracle-endpoint ≥ 0.80 with |rho_mean| ≥ 0.9;
  the closest are VOLCAP and VOLPOW at 0.72 with |rho_mean| = 1.00.
* **P2 FAILS, informatively.** GROSS is not the monotone-endpoint dial; it is a flat ladder
  whose argmax is noise (range 0.003 over 3× of gross). A different pathology, arguably worse:
  46 of the 104 published `argmax` claims concern it.
* **P3 HOLDS.** CADENCE's oracle is interior in **18/18** against a 0.50 chance null,
  independently confirming idea 175's 96.2% on a different corpus, and monthly is the mean-best
  point (0.831 vs W 0.720, Q 0.649, D 0.476) — idea 107's evidence, from three panels.
* **P4 FAILS.** RANDOM's capture is negative on four of five dials. m4 explains why: with the
  constant interior it has nothing to win; the prediction silently assumed a far-end constant.
* **P5 FAILS.** 17, not <10.

## Census of published claims

104 textual `argmax` claims across CHANGELOG / QUEUE / LEADERBOARD; by dial mentioned in
context (non-exclusive): **GROSS 46**, COUNT 19, SLEEVE 10, CADENCE 9, VOLCAP 8, VOLPOW 7,
other 34. **66 of 104 concern a dial re-run here.** Measured oracle-endpoint share on those
dials: GROSS 0.61, COUNT 0.67, CADENCE 0.00, VOLCAP 0.72, VOLPOW 0.72. This is a text census —
it counts which dial each claim is about; it does not re-verify each claim individually, and it
says nothing about the 10 sleeve claims or the 34 unclassified ones.

## By-product, PARKed not promoted

18 of 90 instances clear 4b on the full sample. The strongest, and the only construction that
clears 4b on the full sample **and** the OOS window at **both** cost rungs, is
**u56 · R6 · top-20 EW · g = 0.75 · MONTHLY**: full 13.61% / **1.1557** / −18.81%
(H1 1.2279 / H2 1.1017), OOS 14.56% / **1.1695** / −18.81%, turnover 4.8×/yr; at 25 bps
12.79% / 1.0937 / −18.90%, OOS 13.72% / 1.1102. MOM at the same point: full 13.27% / 1.1228 /
−18.65%, OOS 13.93% / 1.1127. Against SPY's 15.23% / 0.889 / −33.72% every 4b bar clears
(CAGR floor 10.66%, DD cap −20.23%).

**Why this is PARK and not KEEP.** (1) It is one of 90 selections made in a run whose purpose
was an audit — the multiplicity is unpriced. (2) It fails the universe change: the same
construction on **broad** gives 15.95% / 1.1298 / **−24.51%**, missing 4b's drawdown cap by
4.3pp with the halves and CAGR floor clear; on **small** it is 7.18% / 0.4934 / −38.23% and not
close. Idea 53's warning applies exactly. (3) Its distinguishing dial is CADENCE, the one dial
this run finds genuinely selectable — which makes it interesting, not proven. A dedicated
single-hypothesis test is queued (idea 182).

## Caveats

Survivorship: all three panels are current constituents; the small panel is today's sub-$2B
screen with delisted names absent, so every CAGR here is optimistic and no level in this file is
an achievable return. Window composition (idea 111): the IS window is the calmer regime and the
small panel's IS window is only 2011–2016. Only the five dials re-run here are audited. Every
row is t+1 execution at 10 or 25 bps.
