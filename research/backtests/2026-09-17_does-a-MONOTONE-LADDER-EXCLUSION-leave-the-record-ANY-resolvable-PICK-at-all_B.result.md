# Idea 1209 — does a MONOTONE-LADDER EXCLUSION leave the record ANY resolvable PICK at all?

**Lane B, 2026-09-17.** Script
`research/backtests/2026-09-17_does-a-MONOTONE-LADDER-EXCLUSION-leave-the-record-ANY-resolvable-PICK-at-all_B.py`,
15 CSVs + console log. 12 of 12 gates pass, 59s, offline, deterministic. No RULES change, no
book promoted, no PROTOCOL edit (rule 6); RULES.md, PROTOCOL.md, engine.py, scan.py, bot.py and
baseline.py untouched.

**SELECTION:** lane B takes the LAST eligible open idea. 1209 was last under `## Open`.

---

## ANSWER = NO. ZERO. AT EVERY TOLERANCE AND EVERY LADDER SET.

The exclusion keeps between **0.286 and 0.476** of the record's picks and **0.000 of its
resolutions** — at all 20 non-control cells of the grid, on both resolution bars. The record's
whole stock of resolved picks sits on GROSS, and GROSS is the ladder the rule deletes first.

| ALL4 (the record's own set) | picks | resolved R_SPREAD | resolved R_ARGMAX |
|---|---|---|---|
| T_NONE (the record's habit) | 168 | **4** (0.024) | **3** (0.018) |
| T_EXACT (\|rho\| = 1) | 80 | **0** | **0** |
| T_095 | 80 | **0** | **0** |
| T_090 | 76 | **0** | **0** |
| T_080 | 59 | **0** | **0** |
| T_060 | 48 | **0** | **0** |

**All 4 resolutions are GROSS. All 3 R_ARGMAX resolutions are GROSS. N contributes 0 of 42,
H 0 of 42, CADENCE 0 of 42.** 1154's concentration finding replicates and strengthens: it read
15 of 17 on GROSS (0.88); this run reads 4 of 4 and 3 of 3 (1.00).

---

## AND THE FOUR RESOLVED PICKS ARE THE ANCHOR

Every one of the 4 resolved GROSS picks names rung **0.75 — the anchor's own gross** — against
runner-up 0.70, on an IS Sharpe gap of **0.00038 to 0.00042**, all four on B136
(folds 2016, 2018, 2019, 2020), at R_obs/q95 of 1.03 to 1.21.

**So the record's entire inventory of "resolved" picks is a re-selection of the book it already
holds, at four ten-thousandths of Sharpe.** This is why `CH_RESOLVED` has a value-move rate of
**exactly 0.000 at all 24 grid cells** and is bit-for-bit `CH_ANCHOR` in every arm of this run —
a chooser that acts only on resolved picks is the do-nothing rule, on this tape, by measurement
rather than by assumption.

---

## THE EXCLUSION IS A RUNG-COUNT RULE WEARING A SHAPE RULE'S CLOTHES

Declared in ARM 0 **before any price was read**: a k-rung ladder is exactly monotone under a
random ordering with probability 2/k!.

| ladder | k | P(\|rho\|=1) | observed exact of 42 | expected | binomial p |
|---|---|---|---|---|---|
| N | 6 | 2.78e-03 | **0** | 0.117 | 1.000 |
| H | 4 | 8.33e-02 | **6** | 3.500 | 0.134 |
| GROSS | 10 | 5.51e-07 | **40** | 0.000 | **3.9e-248** |
| CADENCE | 2 | **1.000** | **42** | 42.000 | 1.000 |

**CADENCE is monotone with probability 1.000 — a two-rung ladder cannot be anything else — so
any monotone exclusion deletes it at 42 of 42 cells for a reason that has nothing to do with the
tape.** GROSS's 40 of 42 against a 5.5e-07 null is not a shape discovery either: it is 1189's
structural fact (Sharpe is invariant to gross at a 0% cash rate; what survives is a monotone cost
drag), which is also why its median realised spread is **0.0018** against N's 0.1604.

**And the two ladders where the rule could do real work do not fire.** N is exactly monotone at
0 of 42 and H at 6 of 42 against an expectation of 3.5 (p = 0.134) — neither exceeds its own
null. The rule deletes exactly the two ladders that are monotone for construction reasons and
keeps the two where monotonicity is indistinguishable from chance. Its 0.476 -> 0.286 pick
attrition is a rung-count effect, not a shape effect.

---

## THE TWO DIALS AND NO MORE (PROTOCOL rule 4; the queue names both)

`MONOTONICITY TOLERANCE` {T_NONE, T_EXACT, T_095, T_090, T_080, T_060} x
`LADDER SET` {ALL4, NG3, NHG, NH} = **24 cells, EVERY ONE PUBLISHED** in `.grid.csv`.

NOT dials, reported at every value: PANEL {U56, B136, SMALL}; the 14 calendar folds; the two
resolution bars {R_SPREAD = observed IS Sharpe spread clears the 95th percentile of the ladder's
OWN recentred block-bootstrap null range; R_ARGMAX = the argmax rung beats its runner-up by more
than 1.96 paired-bootstrap SE}; the three choosers {CH_ANCHOR, CH_WIDEST, CH_RESOLVED}; the 4a
and 4b legs. Frozen at 1207/1214/1223/1226's construction: 3-leg composite (21/252, 0/126,
0/63), above-200d eligibility, max_vol 0.60, anchor N=20 / H=126 / GROSS=0.75 / CADENCE=W,
10 bps (rule 2), lag 1, warm-up 260, block bootstrap B = 63 rows / 800 reps with block starts
SHARED across books, Hartley d2(k).

**THE LEVEL DOES NOT REPRODUCE 1154 AND THIS RUN DOES NOT CLAIM IT DOES.** 1154 read 17 of 72
decisions resolved (0.236); this run reads 4 of 168 (0.024). The bars are different objects:
1154's is a pairwise ladder-against-ladder call, this run's is each ladder against its own
recentred null. **The CONCENTRATION on GROSS is what replicates, and it is the part the queue's
question turns on.** The level is published as a disagreement, not absorbed.

---

## GATES — 12 of 12 PASS

- **G0 PASS** a two-rung ladder is monotone with probability exactly 1.000 (the whole CADENCE
  result, established before the tape was read).
- **G1 PASS** fast runner == `engine.backtest` on the decision-time frame, dev **2.78e-17**.
- **G2 PASS** live RULES v2 U56 MaxDD **-12.0549%** == the record's committed -12.05%.
- **G3 PASS (0.00e+00)** the anchor rung is the SAME book on all four ladders — N=20, H=126,
  GROSS=0.75 and CADENCE=W are one book bit for bit (1227's finding, re-gated here because the
  answer above depends on it: the 4 "resolved" GROSS picks and the anchor are the same object).
- **G4 PASS** `spearman()` returns +1 / -1 on the two monotone orderings, dev 0.
- **G5 PASS (0.00e+00)** the enumerated P(\|rho\|=1 \| k=4) == 2/4! exactly.
- **G6 PASS** block-sum bootstrap == direct Sharpe on the identity tiling, **4.44e-15**.
- **G7 PASS x3** the 14 folds tile U56, B136 and SMALL with no overlap and no gap.
- **G8 PASS** GROSS is exactly monotone at 0.952 of cells (1154's premise, on a wider census).
- **G9 PASS** CADENCE is exactly monotone at 1.000 of cells.

---

## DOES IT PAY? NO — AND THE MATCHED NULL SAYS IT NEVER DID

Mean OOS fold Sharpe over 42 (panel, fold) cells. **Doing nothing = 1.0362.**

| tolerance | CH_WIDEST (ALL4) | move rate | vs anchor |
|---|---|---|---|
| T_NONE | 0.9959 | 0.905 | **-0.0404** |
| T_EXACT | 0.9892 | 1.000 | **-0.0470** |
| T_095 | 0.9892 | 1.000 | **-0.0470** |
| T_090 | 0.9803 | 1.000 | **-0.0560** |
| T_080 | 1.0292 | 0.857 | **-0.0070** |
| T_060 | 1.0649 | 0.810 | **+0.0287** |

`CH_RESOLVED` returns 1.0362 at all 24 cells — it never moves, so it *is* the anchor.
The ladder-set dial changes almost nothing (NG3, NHG and NH reproduce ALL4's column to within
0.011 at every tolerance), which is itself the point: removing GROSS and CADENCE **by hand**
and removing them **by monotonicity** are the same operation.

**THE ONE APPARENT WIN DIES ON ITS OWN NULL.** T_060's +0.0287 is the only positive cell in the
table, and the move-count-matched null (each chooser's OWN destination multiset and OWN move
count re-dealt to random folds, 4,000 reps) puts it at **p = 0.568**. Over the **24** (set, tol,
chooser) cells that move at all, the observed mean sits **ABOVE its own null at 0 of 24**, mean
gap **-0.0593**, and **0 cells reach p < 0.05 against 1.2 expected by chance.** The exclusion
does not select better picks; the stricter it is the fewer it makes, and the ones it keeps are
still on the wrong side of their own null. 1206's, 1221's, 1226's, 1227's, 1230's and 1231's
finding arriving a seventh time.

---

## RULE 8 WALK-FORWARD AND BOTH KEEP PATHS

Every dial and every chooser chosen on the pre-2017 window ONLY, 2017-2026 read once.

Benchmarks: **U56 SPY 15.06% / 0.8815 / -33.72% (halves 0.9600/0.8171), OOS 15.15% / 0.8686 /
-33.72%; U56 LIVE RULES v2 @10 bps 8.60% / 1.1982 / -12.05%, OOS 9.42% / 1.2717 / -12.05%;
B136 SPY 15.16% / 0.8862 / -33.72%, OOS 15.33% / 0.8769; B136 LIVE 7.98% / 1.0994 / -12.24%,
OOS 7.88% / 1.1061; SMALL SPY 14.06% / 0.8582 / -33.72%, OOS 15.33% / 0.8769; SMALL LIVE
4.64% / 0.7130 / -12.18%, OOS 4.47% / 0.6518 / -12.18%.**

- **66 rung books:** 4a **0**; 4b full 17; 4b OOS 18; BOTH 17. 57 distinct on the realised-return
  key (1211's identity) — the GROSS ladder's Sharpe is near-invariant by construction.
- **216 rule-8 rows:** 4a **0 of 216**; 4b full 48; 4b OOS 48; BOTH 48; beats SPY OOS Sharpe 120.
  **All 48 passing rows collapse to ONE distinct book — the frozen U56 anchor N=20**, full
  15.71% / 1.1480 / -19.13%, OOS **17.16% / 1.1759 / -19.13%** against U56 SPY OOS
  15.15% / 0.8686 / -33.72%.
- **216 stitched chooser curves:** 4a **0**; 4b full 52; 4b OOS 52; BOTH 52. The best is
  ALL4/T_NONE/CH_ANCHOR on U56 (OOS 17.16% / 1.1759 / -19.13%) — which is doing nothing.
- Mean OOS Sharpe by chooser over the 216 rule-8 rows: **CH_ANCHOR 0.8845, CH_RESOLVED 0.8845
  (identical, as above), CH_WIDEST 0.8458.**

**CONFIRMATORY, NOT GENERATIVE.** Every 4b pass is a book the record already committed,
re-selected by a rule that declines to move. **NOT PROMOTED, NO MEMO, NO RULES CHANGE.**

---

## SURVIVORSHIP (PROTOCOL rule 9)

U56 (55 names) and B136 (135) are **current-constituent** lists; SMALL is the current output of a
sub-$2B screen less the documented `max_1d_move >= 1.0` exclusion (51 of 715 tickers dropped;
664 investable, SPY as benchmark only). Every LEVEL — CAGR, Sharpe, MaxDD — is optimistic and
every 4a and 4b count is an **upper** bound. The bias largely cancels out of the shape and
resolution statistics, which rank one construction against itself on one tape, but that
cancellation is an argument and not a measurement; the levels sit beside every shape in
`.ladders.csv` and `.books.csv` so a reader can check.

---

## VERDICT

**KILL (capital).** No book promoted, no memo, no RULES or PROTOCOL edit (rule 6).

The transferable result is procedural and belongs in a future run's header rather than in a
chooser: **a monotone-ladder exclusion is not a shape filter on this record — it is a rung-count
filter. It deletes CADENCE (k=2, monotone with probability 1 by construction) and GROSS (k=10,
monotone for 1189's structural reason) at every tolerance, and with them 100% of the record's
resolved picks — of which there are 4 in 168, all on GROSS, all naming the anchor's own rung at
a Sharpe gap of 0.0004. The record does not have resolvable picks to lose.**

**Follow-ups filed: 1232, 1233, 1234.**
