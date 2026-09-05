# Idea 128 — threshold-plateaus-are-the-general-case (cloud, 2026-09-05)

**Verdict: ANSWERED — the plateau CONFIRMS and generalises, but idea 95's specific wording is
KILLED, and the PROTOCOL proposal has to change with it.** No new book, no KEEP, no RULES change.

Three findings, in the order they force each other:

1. **On Sharpe the constants are worthless.** Across **54 (panel, book, cost, dial) rows** the
   no-instrument control sits **ABOVE every setting of its own instrument in 34**, strictly inside
   the range in **15**, and below in **5**. Median control percentile **0.86**. Idea 95's
   "control INSIDE the range in 7 of 8 cells" is a **special case, not the general one** — the
   general case is worse for the instrument than idea 95 reported.
2. **Tuning them on in-sample Sharpe pays nothing.** Rule 8 (argmax IS Sharpe 2009–2016, OOS read
   once) picks **the control itself in 40 of 54** dial-cells. Mean selection premium over the
   control **−0.0087** OOS Sharpe, positive in **5 of 54**; among the 14 cells where rule 8 picks
   something other than the control, mean **−0.0334** (positive 5 of 14). Plateau width predicts
   none of it: Spearman(Sharpe range, |premium|) = **+0.007**.
3. **And that is the whole point — because these constants are not for Sharpe.** The control is
   the **DEEPEST** drawdown point of its own dial in **41 of 54** cells and the shallowest in
   **0**. Under 4b (which contains the DD cap at 0.60 × |SPY|) the control passes **0 of 54**,
   the published constant passes **12 of 54**, and the full-sample **Sharpe argmax passes only
   3 of 54**. Choosing a drawdown instrument by Sharpe picks the wrong value almost every time.

So the plateau is real and general **on the axis idea 95 measured**, and that axis is the wrong
one. PROTOCOL should not quote "the plateau width" — it should quote the plateau width **of the
bar the constant is adopted for**.

## Design and reproduction

5 constants × their **published** sweeps × 3 panels × 2 base books × 2 cost rungs = **516 dial
points / 54 dial-cells**, weekly, t+1, 75% target gross, de-gross convention, all net.

| constant | published sweep | published value | no-instrument control |
|---|---|---|---|
| band width | 0 / 2 / 3 / 5 / 8 % (idea 57/59) | 3% | no gate |
| position count n | 3 / 5 / 10 / 20 / 40 / all (idea 124/2) | 20 | all (no ranking) |
| gross | 0.10 → 1.00 step 0.05, 19 pts (idea 66/84) | 0.75 | 1.00 (no de-grossing) |
| vol20 threshold | 0.30 / 0.40 / 0.50 / 0.60 / 0.80 / 1.00 / 1.20 / none (idea 95) | 0.60 | none |
| trend lookback K | 50 / 100 / 150 / 200 / 250 / 300 d + no gate | 200 | no gate |

**Tuned parameters: none for the measurement** — every one of the 516 points is reported.
Rule 8 then chooses one value per dial on the IS window only; that is the single tuned parameter,
and its control was fixed in advance.

Idea 94's simulator is **imported**. The parameterised gates here are asserted to equal idea 94's
fixed gates at the published constants: `band3` **0 differing cells**, `g200` **0**, `vol60` **0**
— PASS on all three.

## Q1 — where the control actually sits (54 dial-cells)

| dial | control above all | inside | below all | Sharpe range (median) | ctl pctile (median) | published beats control |
|---|---|---|---|---|---|---|
| K | 8 | 4 | 0 | 0.236 | 0.86 | 3/12 |
| band | 5 | 4 | 3 | 0.039 | 0.67 | 4/12 |
| gross | 10 | 0 | 2 | **0.004** | 0.95 | 2/12 |
| n | 4 | 2 | 0 | 0.209 | 0.83 | 2/6 |
| vol | 7 | 5 | 0 | 0.321 | 0.88 | 3/12 |
| **all** | **34** | **15** | **5** | **0.091** | **0.86** | **14/54** |

Median fraction of a dial's points within 0.05 Sharpe of that dial's own best: **0.71**. The
gross dial is the flattest thing the project has measured — a **0.004** median Sharpe range over
its entire 0.10–1.00 sweep, confirming idea 66's "gross is an exact lever with zero Sharpe
content" on a third occasion and on three panels.

## Q2 — rule 8 (IS 2009–2016 only; OOS 2017–2026 read once)

| dial | sel premium (OOS Sharpe of IS pick − control) | positive | IS pick = control | ρ(IS, OOS Sharpe) median | IS picks seen |
|---|---|---|---|---|---|
| K | +0.0014 | 1/12 | 9/12 | +0.482 | 150, 300, nogate |
| band | +0.0049 | 2/12 | 8/12 | −0.114 | 8%, nogate |
| gross | +0.0000 | 0/12 | **12/12** | +1.000 | 1.00 |
| n | **−0.1123** | 0/6 | 3/6 | −0.143 | 3, 10, all |
| vol | +0.0109 | 2/12 | 8/12 | +0.702 | 0.4, 1.2, none |
| **all** | **−0.0087** | **5/54** | **40/54** | +0.464 (negative in 18/54) | — |

Mean OOS regret against the OOS-best value on the same dial: **0.033**. The n dial is the one
dial where tuning is actively expensive: **−0.112** mean, and its three worst cells are
u56/TOP20@25bps `n=3` (0.869 vs the control's 1.125, **−0.256**), broad/TOP20@10bps `n=10`
(0.853 vs 1.102, −0.249) and u56/TOP20@10bps `n=3` (0.966 vs 1.136, −0.170). That is idea 82's
"ranking subtracts value" arriving from a different direction.

OOS means by dial (IS pick vs control): K 0.934/0.933, band 0.938/0.933, gross 0.933/0.933,
**n 0.840/0.952**, vol 0.944/0.933. OOS references: **SPY 15.45% / 0.882 / −33.7%**; RULES v1
@10bps 7.7%/0.747/−13.8% (u56), 5.9%/0.576/−21.2% (broad), 7.9%/0.581/−32.8% (small); @25bps
3.8%/0.399, 1.1%/0.155, 2.7%/0.250.

## Q3 — does plateau width predict whether tuning pays?  No.

Spearman(Sharpe range, |selection premium|) **+0.007**; (range, premium) **+0.021**;
(range, OOS regret) **+0.086**, n = 54. Splitting at the median range: the narrow half returns
**−0.0220** mean premium (2/27 positive, regret 0.048), the wide half **+0.0047** (3/27, regret
0.018) — i.e. if anything the *narrow* plateaus are the worse place to tune, the opposite of the
intuition that a narrow plateau means the constant matters. **Plateau width is not a robustness
statistic for selection.** Whatever PROTOCOL quotes it for, it must not be that.

## The reconciliation — and both KEEP paths

The Sharpe reading and the 4b reading disagree, and the disagreement is the result.

| position on the dial | 4a passes | 4b passes | control's rank on MaxDD |
|---|---|---|---|
| no-instrument control | 22/54 | **0/54** | deepest point of its dial in **41 of 54**, shallowest in **0** |
| published constant | 31/54 | **12/54** | — |
| full-sample Sharpe argmax | — | **3/54** | — |
| all 516 dial points | 337 | 44 | — |

The control wins on Sharpe and loses 4b outright, because 4b's binding bar for these books is the
**drawdown cap**, and four of these five constants are drawdown instruments. The median control
drawdown is **−25.7%** against the published constant's **−17.3%** (K), **−17.5%** (band),
**−18.4%** (vol) and **−19.8%** (gross). The exception proves it: on the **n** dial the published
constant is **−26.1%**, *deeper* than its control, and the control is the deeper point in only
half those cells — n is a concentration dial, not a drawdown instrument, and it is also the one
dial where rule-8 tuning is actively expensive (−0.112). Measuring
band width, K, vol threshold or gross on Sharpe therefore finds a plateau **by construction** —
it is measuring the instrument on the axis the instrument does not act on.

The 44 four-b-passing points, by width of the passing region: u56/TOP20@10bps band **5 of 6**
values pass (0–8%), vol **5 of 8** (0.4–1.0), gross **5 of 19** (0.70–0.90), K **4 of 7**
(100–250); u56/EWall@10bps vol **3 of 8** (0.5–0.8), gross **1 of 19** (0.85); broad/EWall vol
**2 of 8** (0.5–0.6) at both cost rungs. **That** is the plateau width worth publishing: the
contiguous run of values that clear the bar the constant was adopted for. It is not the Sharpe
range, and on some dials (gross: 1–5 of 19) it is narrow enough to be a real robustness warning.
**Every 4b-passing point here belongs to an already-standing book; nothing is promoted.**

## Proposal for PROTOCOL (amended from the QUEUE's wording)

The QUEUE asked for the Sharpe plateau width beside every adopted constant. This run says that
number is uninformative — it does not predict selection value (ρ = +0.007) and it is measured on
an axis these constants do not move. The amended proposal:

> Beside every constant adopted into RULES, PROTOCOL should quote **(i) the contiguous range of
> values that pass the KEEP bar the constant was adopted for** (for 4b constants, the 4b-passing
> run, e.g. "vol 0.4–1.0 of the 0.30–1.20 sweep, 5 of 8 points"), **and (ii) whether the
> no-instrument control passes that same bar** (here it never does, 0 of 54). The Sharpe range is
> reported as context, not as the robustness statistic.

## Caveats, stated not buried

- **Survivorship** (idea 54): three current-constituent panels; the small panel is a sub-$2B
  screen run today and back-filled to 2010, 439 names after dropping `max_1d_move ≥ 1.0`
  (idea 118). Absent delistings flatter ungated, full-gross, wide-book settings — that is exactly
  the **control** end of every dial, so finding #1 (the control wins on Sharpe) is if anything
  overstated by the bias, while findings #2 and #3 run against it.
- **Sharpe range is a within-cell statistic** and is never pooled by value across panels here —
  only counted.
- The five dials are not independent: band and K are the same trend instrument at different
  speeds, and `band=0` is `K=200`. The 54 cells are a census of this design, not 54 draws.
- **Ideas 38** (u56/broad calendar-day index) and **126** (t+1 only, no lag band) carry over.
- The n dial exists only for the ranked book (6 cells, not 12), which is why the totals are 54
  and not 60.

**Determinism:** the parameterised gates are asserted identical to idea 94's fixed gates at the
published constants; every dial point is recomputed from the committed panels each run.

Script: `research/backtests/2026-09-05_threshold-plateaus-are-the-general-case_cloud.py`
Console: `.console.txt` · All 516 dial points: `.grid.csv` · 54 dial-cells: `.plateaus.csv` ·
Panel references: `.references.csv`
