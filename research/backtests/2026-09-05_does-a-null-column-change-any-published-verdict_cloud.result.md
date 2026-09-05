# idea 181 — does-a-null-column-change-any-published-verdict (cloud, 2026-09-05)

**Verdict: ANSWERED, and the answer splits the clause in two. As a REPORTING column it is not
bookkeeping — it would flag 32 of 33 tilt-based 4b passes as magnitudes indistinguishable from
noise. As a VERDICT-mover it is exactly zero. As a SELECTION gate it is actively harmful and is
a KILL.** Rules unchanged; a report-only PROTOCOL clause proposed with its price attached.

Script `2026-09-05_does-a-null-column-change-any-published-verdict_cloud.py`. 453 engine runs →
906 rows (`.grid.csv`), plus `.clause.csv`, `.verdicts.csv`, `.swap.csv`, `.walkforward.csv`,
`.keyic.csv`, `.census.csv`. Deterministic, seed 181; the re-run reproduces every printed digit.

## The clause, written down before it was priced

> A claim resting on the realised magnitude of a keyed tilt may be reported only if
> `|dSharpe(real key)| > max over B matched null draws of |dSharpe(null key)|`

B = 20, so a one-sided 1/21 = 4.8% threshold. Three questions, reported separately because they
disagree: **Q1** does the magnitude clear the band, **Q2** does the KEEP/KILL verdict move when
the key is swapped for noise, **Q3** does rule 8's pick and its OOS result change under the
clause. Idea 158 measured Q1. Idea 181 asks Q2.

## Corpus

3 panels × (5 real keys + **20 null draws**) × 2 directions × 3 tilt strengths m ∈ {0.20, 0.50,
1.00} + 1 untilted control per panel = 453 books, × 2 cost rungs (10/25 bps, derived exactly
from the 0 bps run and the engine's turnover series) = 906 rows. Book fixed at top-20 EW,
g = 0.75, weekly, `(close > 200d MA) & (vol20 < 0.60)`, t+1 execution. Score
`s = comp + dir·m·key`, both terms pct-ranks. Exactly two tuned parameters (m, direction).

**The null keys really are null** (realised monthly rank IC vs 21-day forward return):
mean +0.0002 / +0.0006 / +0.0007 on u56 / broad / small, |t| > 2 in 2/20, 1/20, 0/20 draws —
the ~5% a noise key should give. Real keys: VOL +0.0803 (t +4.22) u56, +0.0609 (t +3.84) broad,
−0.0232 (t −2.38) small; PRICE **−0.0391 / −0.0375 / −0.0380 (t −2.78 / −4.09 / −5.42)**;
MOM +0.0439 (t +2.13) u56 falling to +0.0048 (t +0.50) small; R6 +0.0402 → +0.0003.

## Q1 — magnitude: 59 of 180 real-key arms (32.8%) clear their own null band

| key | clears | mean \|dSharpe\| | mean null max | mean null percentile |
|---|---|---|---|---|
| **PRICE** | **27/36** | **0.2473** | 0.1467 | **0.944** |
| VOL | 10/36 | 0.0947 | 0.1467 | 0.660 |
| R6 | 9/36 | 0.1155 | 0.1467 | 0.650 |
| R3 | 8/36 | 0.0795 | 0.1467 | 0.579 |
| MOM | 5/36 | 0.0950 | 0.1467 | 0.622 |

Every POS direction except PRICE clears in **0** of its 3-per-cell rows on every panel. **P1
holds**: two thirds of the project's tilt magnitudes are not distinguishable from a key with
zero information, at a threshold made deliberately easy by using only 20 draws.

**P3 FAILS, and the failure strengthens the standing conclusion.** VOL/NEG — the live
`/sqrt(vol20)` scaler's own key and direction — *does* clear the clause, in 4/6 u56 rows and
**6/6 broad rows**, and its dSharpe is **negative in all 12 large-cap rows** (−0.0600 to
−0.3860, monotone in m). The live scaler's effect is not noise; it is reliably, measurably
harmful. **Ninth independent delete-the-scaler reading** (after 1, 2, 72, 82, 141, 159, 160,
168, 158B), and the first to show the effect is significant rather than merely negative. On the
small panel VOL/NEG clears in 0/6 and its sign is mixed.

## Q2 — verdict: the swap changes nothing

Real key vs each of its 20 matched null draws in the same cell, 3600 comparisons per bar:

| bar | verdict identical | real pass & null pass | real pass, null fail | real fail, null pass |
|---|---|---|---|---|
| 4a | **0.843** | 0.262 | 0.083 | 0.074 |
| 4b (full) | **0.888** | 0.135 | 0.048 | 0.064 |
| 4b (OOS window) | **0.877** | 0.241 | 0.048 | 0.076 |

**Pass rates: null-key arms 4a 33.6% / 4b 19.9% / 4b-OOS 31.7% (n=720); real-key arms 34.4% /
18.3% / 28.9% (n=180).** A zero-information key clears 4b *more often* than a real one. **P2
holds** (11.2% of 4b statuses move, under the predicted 15%); **P5 holds** — 143 null arms clear
4b on the full sample and 228 on the OOS window. The 33 real-key 4b passes are 28 u56, 5 broad,
**0 small**, spread over every key and both directions (PRICE/NEG 6, R3/POS 5, R6/POS 5,
MOM/POS 4, VOL/POS 3, MOM/NEG 3, PRICE/POS 2, R3/NEG 2, R6/NEG 2, VOL/NEG 1) — the pattern of a
bar being met by the base book and the panel, not by the key.

**What the clause would actually do.** Of 62 real-key 4a passes, 29 (46.8%) also clear the
clause; of **33 4b passes, 1 (3.0%)**; of 52 4b-OOS passes, 3 (5.8%). So the clause would attach
a "magnitude not distinguishable from a null key" flag to **32 of 33** tilt-based 4b passes —
and change **none** of them, because a KEEP path is decided by the bars, not by the tilt's size.
That is the precise answer to the QUEUE's "if it is near zero the clause is bookkeeping": it is
near zero for verdicts and nowhere near zero for claims.

## Q3 — selection: the clause as a gate is a KILL

Selectors read the IS window only, each read once on 2017–2026, 6 (panel, cost) cells:

| selector | OOS CAGR | OOS Sharpe | OOS MaxDD | 4b(OOS) | paired vs S0 |
|---|---|---|---|---|---|
| S0 do-nothing (untilted control) | 10.12% | 0.7736 | −23.25% | 2/6 | — |
| **S1 IS-argmax, no null column** | **16.48%** | **1.1823** | −22.38% | 2/6 | **+0.4086, wins 6/6** |
| S2 clause-gated | 9.99% | 0.7612 | −24.88% | 2/6 | −0.0124, wins 2/6 |
| RULES v1 | 4.39% | 0.4229 | −26.24% | | |
| SPY | 15.45% | 0.8820 | −33.72% | | |

**P4 FAILS.** S1 beats do-nothing in 6 of 6 cells — the first selector in this project to do so
(ideas 110/132/151/166/171/174 all found the opposite) — and S2's picks differ from S1's in 6 of
6 while losing to doing nothing. Requiring a tilt to beat its null band **removes the arm the
selector wanted** and buys nothing: on u56 the clause admits 4 arms and the IS-best of them is
PRICE/**POS**/0.2, the opposite direction from S1's PRICE/NEG/0.5; on small@10bps it admits none.

**But S1's whole edge is one key.** All six S1 picks are PRICE/NEG. That is not a rule this
project should adopt on this evidence, and the reason is in the caveats, not in the bars: share
price level is a split-history artefact on u56 and broad, and on the small panel a
low-share-price tilt points straight at the beaten-down cohort that survivorship bias
over-represents (idea 54) — small@10bps PRICE/NEG/1.0 returns 20.59% OOS at Sharpe 1.19 from a
panel that contains no delistings at all. It also fails to travel: PRICE/NEG clears 4b in 6/6
u56 rows and **0/6** on broad (drawdown −21.4% to −22.5% against 4b's −20.23% cap) and 0/6 on
small (H1 0.535–0.821 against SPY's 0.891). Queued as idea 185, not proposed.

## Leaderboard census

3315 LEADERBOARD rows; **76 (2.3%) rest on the realised magnitude of a keyed tilt** and are
written with their verdicts to `.census.csv`. They are dominated by sleeve-separation rows
(`u56/EWall sep f=0.50`, `broad/top20 sep f=0.75`, …), entry-budget rows (`broad CAND20
entry-budget B=0.10`) and drawdown-control rows (`u56 V1 + DD-control 8%/halve/new-high`). This
classifies **text**: the rows whose construction is inside this run's grid — a tilt of the
RULES v1 composite by VOL/MOM/R6/R3/PRICE on these three panels at 10 or 25 bps — are the ones
priced above. Rows built on sleeves, gates, entry budgets or book-share ladders are **not**
re-run here and no claim is made about them; idea 186 is queued to extend the null column to
instrument arms that are not keyed tilts.

## Proposed PROTOCOL clause (REPORT-ONLY, not adopted here)

> **11. Null-key column (reporting only).** Any claim that rests on the realised magnitude of a
> keyed tilt must quote, alongside the magnitude, the max |dSharpe| of at least 20 matched
> zero-information keys drawn in the same cell, and state whether the real magnitude exceeds it.
> This column never gates a KEEP/KILL verdict and never gates rule 8's selection: measured over
> 3600 real-vs-null swaps the verdict is unchanged in 84–89% of cases, and gating rule 8 on the
> clause loses to doing nothing (−0.0124 mean OOS Sharpe, 2 of 6 cells).

## Caveats

Survivorship on all three panels (current constituents; the small panel is today's sub-$2B
screen with delisted names absent), so every CAGR is optimistic and no level here is an
achievable return; the PRICE result above is the case where this matters most. B = 20 gives a
coarse band and makes the clause *easier* to clear, which works against P1 and P3 — idea 180 is
the one asking for 100 draws. Window composition (idea 111): the IS window is the calmer regime
and the small panel's IS window is only 2011–2016. The null keys are noise with R6's functional
form, so "a real key beats noise" is weaker than "a real key beats a rival real key". Every row
is t+1 execution at 10 or 25 bps. The `kind` column labels null arms `nullkey`, not `null`,
because pandas reads the bare string back as NaN.
