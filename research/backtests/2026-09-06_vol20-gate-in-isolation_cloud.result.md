# Idea 56 — vol20-gate-in-isolation (2026-09-06, cloud)

**Verdict: KILL of `vol20 < 0.60` as part of the RETURN edge on the large-cap universes, plus a
MECHANISM finding — the 200d clause is nearly INERT there, and vol20's whole contribution is name
SELECTION, not de-grossing. One PARK by-product: dropping vol20 from idea 2's candidate improves it
on U56 (4b PASS) but fails on B136 and is not the rule-8 pick.**

Idea 38 found vol20 the larger destroyer on the small panel (n=40: no gate 0.797 Sharpe, 200d only
0.693, vol20 only 0.524, both 0.441). It had never been tested alone on universe.json, where it is
assumed to be part of the edge. 4-way decomposition (NONE / MA200 / VOL20 / BOTH) at idea 2's
construction — composite score, no vol scaler, top-n EW @75% gross, weekly, 10 bps, next-day — on
U56 and B136. Grid = 4 gates × 3 n × 2 universes × 2 gross conventions = **48 cells, all reported**.

## 1. The 200d clause is inert on both large-cap universes

dSharpe vs NONE at the same n, over all 12 (universe, convention, n) cells: **0.000 to −0.044**;
dMaxDD 0.00% to +2.18%; dCAGR 0.00 to −1.00pp. At **n=5 it is exactly identical to NONE in all four
(universe, convention) cells** — zero difference to 3 decimals on every metric.

Mechanism: `research/scan.py`'s composite already multiplies by `(0.5 + 0.5·above200)`, so the 200d
condition is baked into the ranking as a soft tilt. At the top of that ranking the hard gate has
almost nothing left to exclude. **The 200d clause of RULES v1 is doing no work on large caps that the
score is not already doing.** This is a decomposition result, not a proposal to remove it — see §4.

## 2. vol20 is a DRAWDOWN instrument on large caps, not a return edge

vs NONE at the same n (dg convention shown; rw is within 0.03 Sharpe everywhere):

| universe | n | dSharpe | dCAGR | dMaxDD |
|---|---|---|---|---|
| U56 | 5 | −0.175 | −6.36pp | **+8.35pp** |
| U56 | 10 | −0.118 | −3.26pp | **+5.79pp** |
| U56 | 20 | −0.065 | −1.94pp | **+3.12pp** |
| B136 | 5 | −0.097 | −4.65pp | **+5.96pp** |
| B136 | 10 | −0.054 | −2.63pp | **+4.57pp** |
| B136 | 20 | −0.064 | −2.07pp | **+3.31pp** |

**dSharpe negative in 12/12 cells, dCAGR negative in 12/12, dMaxDD positive (better) in 12/12.** So
the answer to the idea as posed: on universe.json, vol20 is *not* part of the return edge — it costs
Sharpe and CAGR everywhere it is applied. It differs from idea 38's small-panel result in that here
the money buys something: 3–8pp of drawdown. Exchange rate at idea 2's own width (n=20, U56):
**1.94pp of CAGR and 0.065 of Sharpe per 3.12pp of MaxDD.**

## 3. It is SELECTION, not cash-timing

`rw` (always deploy 75% across whatever survives) isolates name selection; `(dg − rw)` at the same
(gate, n) is what the clause earns purely by sitting in cash. Over all 18 (universe, gate, n) triples
the cash effect is **−0.016 to +0.028 Sharpe**, |·| ≤ 0.028 everywhere, and mean deployed gross under
dg never falls below **0.717** (of a 0.750 maximum). The gate essentially never empties on large caps.
Unlike the band books of ideas 57/58, where de-grossing was the whole story, **vol20 here changes
which names you hold, not how much you hold.** Any claim that reads it as a crash-cash instrument on
this universe is reading the small panel's mechanism onto a panel that does not have it.

## 4. KEEP paths and the PARK by-product

**4a 0/48** — nothing beats live RULES v2 (U56 1.213, B136 1.108) anywhere. **4b 5/48**, every one at
n=20 on U56; first-failing 4b bar over the 43 failures: DD 19, H2 16, H1 8.

| U56, n=20, dg | CAGR | Sharpe | MaxDD | H1 | H2 | OOS CAGR/Sharpe | 4b |
|---|---|---|---|---|---|---|---|
| NONE | 15.40% | 1.177 | −21.27% | 1.276 | 1.111 | 16.50% / 1.170 | fail (DD) |
| **MA200** | **14.40%** | **1.158** | **−19.09%** | **1.222** | **1.118** | **15.85% / 1.181** | **PASS** |
| VOL20 | 13.47% | 1.112 | −18.15% | 1.153 | 1.083 | 14.56% / 1.145 | PASS |
| BOTH *(idea 2's candidate)* | 12.74% | 1.098 | −18.15% | 1.097 | 1.104 | 14.36% / 1.168 | PASS |

SPY 15.23% / 0.889 / −33.72% (H1 0.957, H2 0.834, OOS 0.882); 4b bars on this window: MaxDD ≥ −20.23%,
CAGR ≥ 10.66%.

**MA200/n=20 dominates idea 2's published BOTH/n=20 candidate on 5 of 6 4b metrics** — CAGR +1.66pp,
Sharpe +0.060, H1 +0.125, H2 +0.014, OOS Sharpe +0.013 — losing only 0.94pp of MaxDD, which stays
1.14pp inside the cap. It is nonetheless **PARK, not KEEP**: it fails 4b on B136 (14.74% / 0.995 /
−24.00%, first-failing bar DD, exactly as NONE does), and rule 8's own chooser does not select it.

## 5. Rule 8 walk-forward (choose gate and n on ≤2016, read 2017–2026 once, inside each cell)

| cell | IS pick | IS Sharpe | OOS CAGR/Sharpe/MaxDD | anchor BOTH/n=20 OOS Sharpe | edge | best OOS cell | regret |
|---|---|---|---|---|---|---|---|
| U56/dg | NONE, n=5 | 1.327 | 23.23% / 1.044 / −28.45% | 1.168 | **−0.124** | MA200 n=20 (1.181) | −0.137 |
| U56/rw | NONE, n=5 | 1.305 | 23.87% / 1.052 / −28.45% | 1.136 | **−0.084** | NONE n=20 (1.158) | −0.106 |
| B136/dg | NONE, n=10 | 1.201 | 15.76% / 0.835 / −26.01% | 0.895 | **−0.061** | NONE n=20 (0.935) | −0.101 |
| B136/rw | NONE, n=10 | 1.204 | 15.92% / 0.839 / −26.01% | 0.888 | **−0.050** | MA200 n=20 (0.942) | −0.103 |

SPY OOS 15.45% / 0.882 / −33.72%; RULES v2 OOS 1.294 (U56) / 1.121 (B136).

**The IS chooser picks a gate containing vol20 in 0 of 4 cells** — in-sample, dropping the gate always
looks best — **and it loses to the pre-registered anchor in 4 of 4** (edge −0.050 to −0.124). It beats
SPY OOS in 2/4 and the live RULES v2 in 0/4. So the walk-forward does not rescue vol20, but neither
does it endorse deleting the gate: the anti-tuning reading is that this whole dial does not walk
forward, and the pre-registered choice beats the fitted one everywhere.

## Reading against idea 38

Same clause, opposite mechanism by panel. On the small panel it destroyed Sharpe *and* left drawdown
alone; on large caps it destroys Sharpe and *buys* drawdown. Both facts are consistent with vol20
being a low-volatility tilt: on large caps the low-vol names are a genuinely defensive slice, on
sub-$2B names they are not. Any cross-panel statement about "the gate" should quote which of the two
it means — cf. idea 276's census, run the same day.

Script: `research/backtests/2026-09-06_vol20-gate-in-isolation_cloud.py`
Artifacts: `.grid.csv` (48 cells), `.walkforward.csv`, `.console.txt`, `.memo.md`
