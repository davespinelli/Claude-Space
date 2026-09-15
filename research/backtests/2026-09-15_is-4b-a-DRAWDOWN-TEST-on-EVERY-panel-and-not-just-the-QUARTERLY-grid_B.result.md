# Idea 981 (lane B, 2026-09-15) — is 4b a DRAWDOWN TEST on EVERY panel, and not just on the QUARTERLY grid?

**ANSWERED = NO. 4b's binding leg is a CADENCE OBJECT, not a constant and not a panel object.
KILL for "4b is simply always the DD cap".** The DD cap's grip is monotone in how slowly the
book rebalances, and idea 976's "`L4_DD` binds on 36 of 36" is reproduced exactly on the M/Q
half of the ladder and collapses to 5 of 18 on D/W. Nothing promoted; no RULES, PROTOCOL,
`scan.py`, `bot.py` or `baseline.py` change.

Script: `2026-09-15_is-4b-a-DRAWDOWN-TEST-on-EVERY-panel-and-not-just-the-QUARTERLY-grid_B.py`
(runtime 108 s, deterministic).

## THE GRID
3 panels {U56, B136, SMALL} × 5 books {TOP05, TOP10, TOP20, EWELIG, BAND03} × 2 gross
{CORE 0.75, EXT 1.00} × the **D / W / M / Q ladder at MATCHED GROSS** × every rebalance phase
inside each cadence (D 1, W 5, M 21, Q 63 = 90 phases per book-gross) = **2,700 phase-books**,
each scored at 5 cost rungs = **13,500 rows**, plus **36 rule-8 picks**. Two tuned axes only —
cadence ladder {CORE4 = D/W/M/Q, COARSE3 = W/M/Q, FINE2 = D/W} and panel set {U56, B136, SMALL,
POOLED} — all **12 points reported, none selected**. Phase machinery, book set, leg alphabet and
4b convention copied verbatim from ideas 938 / 942 / 962 / 964 / 976, which is what makes G3 an
exact cross-run reproduction rather than a resemblance.

## GATES 8 of 8 PASS, printed before any result number
- **G0** `offset_mask(·, per, 0)` == `engine.rebalance_mask` on **D / W / M / Q**, 0 disagreeing rows.
- **G1** fast `Ctx` == `engine.backtest` on returns AND turnover, post warm-up, on D and M: max|d| **2.776e-16**.
- **G2** `BAND03@0.75` == `baseline.rules_v2_weights` elementwise, **0.000e+00**.
- **G3 CROSS-RUN:** idea 976's committed `.grid10.csv` reproduced on **2,520 of 2,520 rows**, max|d|
  **1.776e-15** (on `turn_per_yr`) over 32 shared numeric columns, **0 4b-verdict flips**.
- **G4 CROSS-RUN:** idea 976's published "`L4_DD` binding on 36 of 36 rule-8 picks" recomputed from
  its own committed `.walkforward.csv`: **36 of 36**, exact.
- **G5 MATCHED GROSS:** the target weight matrix is identical across all four cadences on all 30
  (panel, book, gross) triples, max spread **0.000e+00** — only the rebalance mask moves.
- **G6** determinism, one cell rebuilt from scratch: **0.000e+00**. **G7** every rule-8 chooser
  IS-only, 0 disagreements under permuted OOS columns.

## THE ANSWER — a monotone CADENCE gradient, and the panel does not carry it
`L4_DD` fail rate at 10 bps, pooled over panels:

| cadence | L1_H1 | L2_H2 | L3_OOS | **L4_DD** | L5_CAGR | 4b pass | median turn/yr |
|---|---|---|---|---|---|---|---|
| D | 0.733 | 0.533 | 0.600 | **0.633** | 0.533 | 0.033 | 33.49 |
| W | 0.427 | 0.533 | 0.520 | **0.647** | 0.433 | 0.147 | 14.66 |
| M | 0.322 | 0.475 | 0.440 | **0.832** | 0.378 | 0.081 | 6.81 |
| Q | 0.263 | 0.501 | 0.457 | **0.927** | 0.322 | 0.035 | 3.45 |

Pooled over cadences, by panel: U56 **0.799**, B136 **0.918**, SMALL **0.941**.

- **H_ALWAYS FAIL at 0.4600** (bar ≥ 0.80): the minimum `L4_DD` fail rate over the 12
  (panel × cadence) cells is **0.460**, at U56/W. 4b is not a drawdown test everywhere.
- **H_CAD PASS at +0.2937** (bar ≥ 0.20): cadence range 0.633 → 0.927.
- **H_PANEL FAIL at +0.1422** (bar ≥ 0.20): panel range 0.799 → 0.941.
- **H_MODAL FAIL — `L4_DD` is the modal failed leg in 6 of 12 cells.** It is modal on U56 and
  B136 at W/M/Q and **nowhere at D**, where `L1_H1` takes over on all three panels; on SMALL it
  is never modal at any cadence (`L1_H1` / `L1_H1` / `L2_H2` / `L3_OOS` at D/W/M/Q).
- **H_ONLY FAIL at 0.0000** (bar ≥ 0.25 in EVERY cell), and the failure is a SMALL fact: among
  failing books, `L4_DD` is the only failed leg on **U56 0.111 / 0.424 / 0.852 / 0.831** and
  **B136 0.100 / 0.111 / 0.440 / 0.476** at D/W/M/Q, and **0.000 in all four SMALL cells**,
  where the mean book fails **4.5–4.8 of the 5 legs** and nothing is marginal.

**DECISION RULE (fixed in advance) → a CADENCE object.**

## THE MECHANISM, AND IT IS NOT A COST ARTEFACT
At matched gross, median |OOS MaxDD| rises monotonically as the book is slowed from weekly down:
**U56 D 20.15 / W 19.45 / M 23.18 / Q 26.21%** and **B136 D 22.90 / W 22.56 / M 26.62 / Q 28.47%**
(SMALL is the exception and runs D 49.82 / W 37.41 / M 38.90 / Q 41.92%, worst at DAILY).
The 4b cap is fixed at 60% of SPY's −33.72% = **−20.23%**, so the same rule crosses it purely by
being rebalanced less often. **The gradient is already there at ZERO cost** — `L4_DD` fail rate
at 0 bps reads **D 0.567 / W 0.647 / M 0.829 / Q 0.924**, against 0.633 / 0.647 / 0.832 / 0.927
at 10 bps — so this is drift between resets, not the turnover rebate ideas 931 and 943 priced.
Raising the rung to 50 bps moves the D cell (0.567 → 0.800) and barely moves Q (0.924 → 0.931).

**The variance decomposition says the same thing from the other side.** Marginal one-way η² of
each leg's pass indicator (NOT orthogonal — stated):

| leg | cadence | panel | book | gross | phase |
|---|---|---|---|---|---|
| H1 | 0.0191 | **0.7435** | 0.0104 | 0.0000 | 0.0198 |
| H2 | 0.0009 | **0.5991** | 0.0301 | 0.0000 | 0.0513 |
| OOS | 0.0021 | **0.6470** | 0.0415 | 0.0000 | 0.0374 |
| **DD** | **0.0569** | **0.0384** | **0.2027** | 0.0430 | 0.0845 |
| CAGR | 0.0065 | **0.4556** | 0.1481 | 0.0231 | 0.0371 |

The other four legs are overwhelmingly **panel** objects (η² 0.46–0.74): whether a book beats
SPY's Sharpe is decided by which universe it trades. **The DD leg is the one leg the panel does
NOT explain** (0.038, an order of magnitude below the rest); it is carried by the book (0.203),
then the rebalance phase (0.085), then the cadence (0.057). So 4b's five legs split cleanly into
four panel questions and one book-and-schedule question, and the record has been reading the
second as if it were universal.

## RULE 8 — and this is where 976's headline localises
36 picks = 3 panels × 4 cadences × 3 IS-only choosers, (book, gross) chosen on **2009–2016
alone**, 2017–2026 read once, all 36 live.

- **`L4_DD` among the failed legs: M 9 of 9, Q 9 of 9, W 3 of 9, D 2 of 9 = 23 of 36 (0.639).**
  **H_RULE8 FAIL** against its 0.90 bar. The M/Q half is **18 of 18** — idea 976's "36 of 36"
  reproduced exactly on the cadences it ran — and the D/W half is **5 of 18**.
- The only failed leg on 6 picks, all monthly or quarterly (M 4, Q 2), **0 at D and 0 at W**.
- **OOS 4b 4 of 36; OOS 4a 0 of 36.** Full sample over the 2,700-row 10 bps grid: 4b **140**,
  4a **5**. SMALL clears 4b on **0 of 900** rows at every book, gross, phase and cadence.
- Comparands: **SPY OOS 15.27% / 0.874 / −33.72%**; RULES v2 (live) full-sample Sharpe / MaxDD
  U56 **1.201 / −12.05%**, B136 1.099 / −12.24%, SMALL 0.664 / −13.89%.

All four OOS 4b passers are the **same object — U56 / BAND03 / gross 1.00**, picked by two of the
three IS-only choosers at the two fast cadences:

| pick | OOS CAGR | OOS Sharpe | OOS MaxDD | turn/yr |
|---|---|---|---|---|
| U56 BAND03 EXT **daily** | 12.46% | 1.288 | −14.77% | 3.26 |
| U56 BAND03 EXT **weekly** | 12.68% | 1.277 | −15.91% | 2.35 |

The weekly row **independently reproduces idea 973's and idea 982's committed best pick
(12.68% / 1.277 / −15.91%)** on a grid built for a different question — the third independent
arrival at the live book run at gross 1.00. A 10-line memo with exact RULES wording is filed
beside this result as **PROPOSED, NOT APPLIED** (rule 6); both prior runs surfaced the same
object and declined to promote it, and its 4a leg still fails on every panel.

## WHAT THIS CHANGES IN THE RECORD
The record's DD-heavy readings of 4b (968's 89.2% on the quarterly grid, 976's 36 of 36) are
**correct and local**. They are properties of the M/Q grids the record runs most, and they do not
generalise down the ladder: at weekly cadence on U56 the DD cap fails on 0.460 of phase-books and
is the only failed leg on 0.424 of failures; at daily cadence it is not even the modal leg on any
panel. A committed claim of the form "4b is a drawdown test" should carry the cadence it was
measured at. Proposed wording is in the memo; nothing is applied here.

## SURVIVORSHIP (rule 9)
U56 / B136 / SMALL are CURRENT-CONSTITUENT lists (SMALL additionally drops the 52 tickers with
`max_1d_move` ≥ 1.0 per `data/small_meta.csv`), so every CAGR and drawdown LEVEL above is
optimistic. A survivor panel understates drawdown, so **every `L4_DD` fail rate here is a LOWER
bound — which cuts AGAINST this run's own H_ALWAYS rather than for it**: the true rates are
higher and H_ALWAYS would be closer to passing, though the cadence GRADIENT, being the same names
on the same tape under different rebalance SCHEDULES, is very nearly immune. The rule-8 4b levels
are read against SPY, which is not survivorship-inflated, so every 4b PASS is an upper bound and
every FAIL is understated.

## FOLLOW-UPS FILED
983 (is the DD leg's cadence gradient a DRIFT fact — price it against a no-drift daily-reset
control at matched gross), 984 (should every committed 4b claim carry the CADENCE it was measured
at, and how many of the record's claims are M/Q-only), 985 (the four non-DD legs are panel objects
at η² 0.46–0.74 — is 4b's Sharpe alphabet measuring the universe rather than the rule).
