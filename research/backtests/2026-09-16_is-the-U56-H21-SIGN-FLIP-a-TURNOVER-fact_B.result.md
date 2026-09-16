# Idea 1106 (lane B, 2026-09-16) — is the U56 H=21 SIGN FLIP a TURNOVER fact?

**ANSWERED = NO. KILL of 1106's premise.** `GATE = EDGE_OPEN − EDGE_ELIG` does not scale with the
null's re-draw frequency. The re-draw arithmetic the queue line asserts is exactly right — a
21-day min hold does let a random ordering re-draw **4.18x** as often as a 126-day one, and
dropping to H=5 re-draws **4.18x** more again — but GATE does not follow it. **4 of 6 declared
hypotheses FAIL, and the two that pass do not rescue the premise.**

## The two dials, and what is not a dial
`H ∈ {5, 10, 21}` (walked) × `PANEL ∈ {U56, B136}`. 1086's committed `H ∈ {63, 126}` rungs are
carried as CONTEXT and used as cross-run reproduction gates, not tuned. The `N` ladder
`{5,8,10,12,15,20,25,30,40}` is 1082/1086's committed coordinate set; every rung is published.
Frozen at 1082/1085/1086's construction: CAND20 legs, cap INF, REBUILT DD-match, 40 seeds, 34
bisection steps, max_vol 0.60, gross 0.75, W cadence, 10 bps, LAG 1. **90 cells, 180 prices.**

**The null seed recipe contains no H**, so the same 40 random orderings are replayed at every
rung: a move in GATE along H is the min hold moving, not a different draw.

## GATES 13 of 13 PASS, printed before any result number
G1/G1b/G1c fast runner, `gross_rescaler(1.0)` and its turnover path all ≡ `engine.backtest` at
1.39e-17 / 0.00e+00. G2 936/1071/1082's committed W/H126 N=20 triple 3.18e-07. G3 SPY OOS
triples 1.70e-04 / 4.05e-05. G4 live RULES v2 MaxDD ≡ −12.05% / −12.24%. **The suite's point is
G5–G7: 1097's 54 committed `EDGE_OPEN`/`EDGE_ELIG` figures at 1.78e-15, its 54 book
CAGR/MaxDD/turnover triples at 1.78e-15, and its headline — U56 H=21 carries 6 of 9 positive
GATE rungs — at 0.00e+00.** The H=21/63/126 columns are literally 1097's numbers; the H=5 and
H=10 columns are the only new measurement.

## The answer

| H | U56 pos/9 (decisive ±) | U56 mean GATE | U56 NTURN(OPEN) | B136 pos/9 (decisive ±) | B136 mean GATE | B136 NTURN(OPEN) |
|---|---|---|---|---|---|---|
| 5 | **8/9** (7+ / 0−) | **+0.907** | 43.76 | 3/9 (1+ / 4−) | −0.575 | **56.76** |
| 10 | 5/9 (2+ / 1−) | −0.050 | 22.45 | 0/9 (0+ / 9−) | −2.075 | 29.02 |
| 21 | 6/9 (2+ / 1−) | +0.216 | 11.10 | 0/9 (0+ / 9−) | −1.902 | 14.17 |
| 63 | 0/9 (0+ / 6−) | −0.872 | 4.65 | 0/9 (0+ / 9−) | −1.815 | 5.84 |
| 126 | 0/9 (0+ / 2−) | −0.465 | 2.70 | 1/9 (0+ / 6−) | −0.869 | 3.31 |

**H_TURNOVER FAILS.** `Spearman(GATE, NTURN_raw OPEN)` = **+0.0775 pooled, +0.4924 on U56,
−0.0572 on B136**. The two panels disagree in sign, which is the declared refutation.

**H_DTURN FAILS, and it fails at its own mechanism.** The premise names a channel: the
*gate-free* null must be the one turning over more, so the gate must cost a random book a
turnover cost. `DTURN = NTURN(OPEN) − NTURN(ELIG)` is **positive at only 40 of 90 cells**, mean
+0.755, range [−3.139, +9.356]. It is **negative at every rung H ≥ 21 on both panels** — there
the *gated* null turns over MORE, the exact reverse of the premise — and only turns positive at
H = 5 and 10. `rho(GATE, DTURN)` = +0.204 pooled.

**H_MONOTONE FAILS with 2 inversions.** U56 mean GATE down the ladder 126 → 63 → 21 → 10 → 5:
**−0.465 → −0.872 → +0.216 → −0.050 → +0.907**. Null turnover rises monotonically across those
same rungs (2.70 → 4.65 → 11.10 → 22.45 → 43.76); GATE does not.

**H_FLIP_EXTENDS FAILS.** U56 positive-GATE rungs go 6/9 at H=21 → **5/9** at H=10 → 8/9 at H=5.
Halving the hold from 21 to 10 — doubling the re-draw rate — makes the flip *weaker*, not
stronger. The declared prediction was "more at both".

**H_REDRAW PASSES, and this is what makes the failure clean.** Names newly taken per rebalance:
15.35 at H=5, 3.68 at H=21, 0.68 at H=126 — ratios **4.18x (5/21) and 22.7x (5/126)**, inside
the declared [3, 5] band at all four panel × gate arms. The re-draw frequency the premise names
is real, measured, and moves by a factor of 22 across the ladder. GATE moves by 1.4 pp,
non-monotonically, with the wrong cross-panel sign.

**H_PANEL PASSES ON ITS DECLARED WORDING ONLY.** It asks whether B136 flips positive *anywhere*;
it does, at 3 cells (H=5) and 1 (H=126). **D1, post-hoc and labelled: the directional contrast
is the one that bites, and it runs the wrong way.** B136's nulls re-draw MORE than U56's at
**every one of the 5 rungs**, and B136's mean GATE is MORE NEGATIVE than U56's at **every one of
the 5 rungs**. Two panels matched on construction, cadence, cost, seeds and DD convention order
themselves by *composition*, not by turnover. Over the walk rungs: U56 19/27 positive, B136 3/27.

**D2, post-hoc and labelled — "turnover" is two axes and they pull opposite ways.** The +0.49 on
U56 is ACROSS rungs (the H axis). WITHIN a rung, where the only turnover variation is the N
axis, `rho(GATE, NTURN)` is **NEGATIVE at 9 of 10 (panel, H) slices**, as low as −0.967. More
null turnover raises GATE when it comes from a shorter hold and lowers it when it comes from a
smaller book. No single "GATE scales with re-draw frequency" claim can carry both signs. The
best of the eight explanators tried is the literal re-draw count (`NEW_per_reb`, pooled +0.302,
U56 +0.615, B136 +0.167) and it is still weak and still panel-inconsistent.

**What the flip actually is, stated as the limit of what this run establishes:** a U56 property
that strengthens as the hold shortens. It is decisive where it is largest — **7 of 9 U56 H=5
cells are positive at 2 SE with none decisively negative** — so it is not noise. But it does not
generalise to the panel with more turnover, and turnover is not the variable that carries it.

## Rule 8 walk-forward — parameters on 2009–2016 only, 2017–2026 read once
Two IS choosers declared in advance. **H_WF: 1 of 4 picks clears 4b out of sample, and it is not
an EDGE chooser.**

| panel | chooser | IS pick | OOS CAGR / Sharpe / MaxDD | vs RULES v2 (live) | vs SPY | OOS 4b |
|---|---|---|---|---|---|---|
| U56 | C_SHARPE | H=21, N=12 | **17.57% / 1.1426 / −19.48%** | 9.45% / 1.2762 / −12.05% | 15.21% / 0.8711 / −33.72% | **PASS** |
| U56 | C_EDGE | H=10, N=5 | 20.69% / 1.0614 / −21.75% | " | " | FAIL (O_DD) |
| B136 | C_SHARPE | H=63, N=5 | 20.46% / 0.9156 / −28.62% | 7.88% / 1.1059 / −12.24% | 15.33% / 0.8767 / −33.72% | FAIL (O_DD) |
| B136 | C_EDGE | H=63, N=5 | 20.46% / 0.9156 / −28.62% | " | " | FAIL (O_DD) |

The single passing pick is **U56 N=12 / H=21 — a cell 1082/1086/1097 already committed and
already parked**, reproduced here at 1.78e-15. It is 1097's own rule-8 result, not a new
candidate, and is not re-proposed. Both EDGE choosers again pick a losing cell and fail on the
drawdown leg, reproducing 1082's, 1084's and 1097's reading from a fourth direction.

GATE is a statement about the comparand, not the book, so the walk-forward tests the H dial, not
the gate. For completeness: OOS GATE ≤ 0 at 24/45 (U56) and 41/45 (B136); sign agrees between
full sample and OOS at **41/45 and 43/45**.

## Both KEEP paths at all 90 cells (PROTOCOL rule 4)
**4a: 0 of 90.** `A_DD` is 0/90 — no cell in this grid clears the live book's −12.05% drawdown.
A book fact, unchanged by anything here.

**4b: 25 of 90 full-sample, 28 of 90 OOS, 25 of 90 both.** `L_CAGR` 90/90, `L_H1` 89/90,
`L_OOS` 73/90, `L_H2` 66/90, **`L_DD` 28/90 — the sole failing leg at 40 of the 65 failures.**

**The new rungs are where the passes concentrated: 17 of the 25 are H=5 or H=10 cells (15 U56,
2 B136), books the record had not built.** And the H dial trades one 4b leg against the other:

| H | 4b full/OOS | DD headroom (median) | CAGR headroom (median) |
|---|---|---|---|
| 5 | 10 / 12 of 18 | **+2.08 pp** | +2.23 pp |
| 10 | 7 / 7 of 18 | +1.13 pp | +2.94 pp |
| 21 | 5 / 5 of 18 | +0.55 pp | +4.55 pp |
| 63 | 0 / 0 of 18 | — | — |
| 126 | 3 / 4 of 18 | +0.57 pp | +6.17 pp |

Removing the min hold entirely (H=5 is a full weekly re-rank: nothing is ever young at the next
rebalance) buys the widest drawdown margin in the grid — U56 H=5 N=40 sits **3.56 pp inside the
cap** against the 0.01–1.45 pp the committed cells manage — and pays for it in CAGR, where the
same cell clears the floor by **0.34 pp**. Shortening the hold moves the binding leg from `L_DD`
to `L_CAGR` without ever clearing both by a margin this tape can resolve.

**NOTHING IS PROPOSED AND NO MEMO IS WRITTEN.** Best headroom anywhere in the grid is +3.56 pp on
drawdown and +7.14 pp on CAGR; idea 1083 measured the 90% width of the drawdown-margin quantity
itself at **4.1–7.2 pp** on this tape. Every pass here is inside its own resolution. The H=5
slice is also not rule-8 reachable: the honest IS-Sharpe chooser picks H=21, and the IS-EDGE
chooser picks H=10 N=5, which fails OOS on drawdown.

## A defect this run found in its own first pass, and paid for
Turnover is **not** exactly `lam ×` the `lam=1` turnover under the REBUILT DD-match. The cost
term is `lam · |W − A/V(lam)|` and the cash sleeve inside `V` does not scale, so recovering the
raw turnover by dividing the matched path by `lam` carries an error measured here at **1.31e-02,
1.75% of peak rebalance turnover**. The first pass computed `NTURN_raw` that way and declared a
gate asserting exact linearity, which duly FAILED. `NTURN_raw` now comes from a direct `lam=1`
evaluation and G1d publishes the size of the error the shortcut would have carried. The headline
correlations move in the fourth decimal (+0.0780 → +0.0775), so no conclusion here rested on it —
but it would have been invisible without the gate, and the gate only existed because it was
declared before the numbers.

## Survivorship (PROTOCOL rule 9)
U56 and B136 are CURRENT-CONSTITUENT lists. Every level is optimistic and every 4a/4b count is
an UPPER bound. GATE, DTURN and the EDGE contrasts are within-pool over one tape and the bias
very largely cancels out of them; it does NOT cancel out of the 4b legs, which are measured
against SPY, a real index, so the 25 parked passes are flattered by it.

## Files
`2026-09-16_is-the-U56-H21-SIGN-FLIP-a-TURNOVER-fact_B.py`, plus `.grid.csv` (90 cells × 66
cols), `.rungs.csv`, `.explanators.csv`, `.walkforward.csv`, `.hypotheses.csv`, `.gates.csv`,
`.benchmarks.csv`, `.redraw.csv`, `.console.txt`.
