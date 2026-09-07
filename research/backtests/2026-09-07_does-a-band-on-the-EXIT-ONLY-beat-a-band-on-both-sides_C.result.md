# Idea 349 — does a band on the EXIT ONLY beat a band on both sides?

**Lane C, 2026-09-07. Verdict: SPLIT — the queue's premise is FALSIFIED and the answer is YES, the
exit side carries it. The ENTRY side is not a turnover dial at all; it is a CONCENTRATION dial.
Rules unchanged. One 4b KEEP-candidate, PARK-recommended (memo written).**

Script `2026-09-07_does-a-band-on-the-EXIT-ONLY-beat-a-band-on-both-sides_C.py`;
console `.console.txt`; data `.grid.csv` (126 rows), `.marginals.csv`, `.matched.csv`,
`.additivity.csv`, `.walkforward.csv`.

## Pre-registration

Book fixed at idea 331's convention and never tuned: top-20 eligible by the RULES v1 composite
with the vol scaler OFF, RULES v1 eligibility (above the 200d MA, vol20 < 0.60), NORM weights
`w_i = g/k_t` at g = 0.75, next-day execution, **weekly throughout** (the idea fixes cadence).
The single band dial `m` is split into two thresholds around the same centre n = 20:

* **entry buffer e** — an unheld name is bought only if its rank `<= n - e`;
* **exit buffer x** — a held name is sold only once its rank `> n + x`.

Exactly two tuned parameters: `e in {0,2,4,6,8,12,16} x x in {0,5,10,20,40,80}` = **42 cells**.
Panel `{U56, B136, SMALL439}` and cost rung `{0, 10, 25}` bps are REPORTED axes, not tuned
choices — **all 126 cells x 3 rungs are printed and committed to `.grid.csv`**.
`(e,x) = (0,0)` is the hard rank cut; `(0,20)` is idea 331's weekly band cell.

## Reproduction gates — 4 of 4 EXACT, before any new number was read

| gate | result |
|---|---|
| G1 `fast_backtest` vs `engine.backtest` (returns, turnover) | max\|dr\| **0.000e+00**, max\|dturn\| **0.000e+00** |
| G2 derived rung `r(25) = r(0) - turnover*25/1e4` vs `backtest(cost_bps=25)` | max\|d\| **0.000e+00** |
| G3 `sel_ex(0,0)` nests `sel_hard(20)` | **0 disagreements** of 54,600 / 132,600 / 382,800 (975 / 975 / 870 weekly rebalance days) |
| G4 idea 331's committed weekly `.grid.csv` rows (U56/B136 x m in {0,20}) | \|dSharpe\| ≤ **1.1e-16**, \|dCAGR\| ≤ 5.6e-17, \|dturn\| ≤ 1.8e-15, \|dOOS\| ≤ 1.1e-16 |

## [B1] The mechanism: the two sides are not the same kind of dial

Marginal dSharpe against the `(0,0)` hard cut at 10 bps, with turnover and mean holdings attached:

| side | mean dSharpe | positive | mean dOOS | spearman(dial, turnover) | spearman(dial, **names**) |
|---|---|---|---|---|---|
| ENTRY e | +0.0320 | 15/18 | +0.0121 | **-0.298** | **-0.988** |
| EXIT x | +0.0577 | **15/15** | +0.0387 | **-0.562** | **+0.000** |

That last column is the finding. The exit buffer is **name-count-neutral by construction** (the
`k_t` cap absorbs it: 19.11 names on U56 at every x) and cuts turnover 11.00 -> 5.07x/yr. The
entry buffer barely moves turnover (11.00 -> 7.68x/yr on U56) and instead **collapses the book
from 19.1 names to 7.6** — it is a concentration dial wearing a band's clothes. On U56 its mean
marginal Sharpe over the six rungs is **+0.0005**, i.e. nothing; its apparent lift lives entirely
on B136 (+0.035 mean) and SMALL439 (+0.060 mean), the two panels where a top-20 book is diluted.

## [B2] Turnover-matched, entry vs exit — the decisive reading

| direction | wins | median dS | mean dS | OOS wins |
|---|---|---|---|---|
| ENTRY cell vs nearest-turnover EXIT cell | **8/18** | **-0.0142** | -0.0017 | **5/18** |
| EXIT cell vs nearest-turnover ENTRY cell | **9/15** | **+0.0318** | +0.0244 | **10/15** |

Both readings point the same way and the OOS column points harder. **Idea 331's 10-of-18
turnover-matched win is carried by the EXIT side.** Adding an entry buffer at matched turnover is
a coin flip in sample and a loss out of sample.

## [B3] The two sides are NOT separable

Interaction `dS(e,x) - dS(e,0) - dS(0,x)` at 10 bps over all 90 (e>0, x>0) cells: mean
**-0.0312**, sd 0.0359, **negative in 79/90**, and \|mean interaction\| is **0.332x** the mean
absolute marginal. The additive model explains **R2 0.618**. The two buffers are substitutes, not
complements — they compete for the same trades, so idea 331's single dial was not a mis-specification.

## [B4] / [C] Admission and cost tolerance (all 126 cells, all three rungs)

* **4a: 0/126 at every rung** on all three panels — the 4a pathology again (idea 136); nothing
  here comes near the live book's -12.05% drawdown.
* **4b: 43/126 @0 bps, 39/126 @10, 36/126 @25.** Every pass at 10 and 25 bps is **U56**. B136
  passes 4/42 at 0 bps and **0/42 at 10 and 25**; SMALL439 passes **0/42 at every rung**.
* **No new panel.** 33 of U56's 39 passes carry e > 0, but 6 e=0 cells already pass, so the entry
  buffer opens **no panel and no rung** that the exit buffer alone does not already open.
* Binding 4b bars over the failures @10 bps: H2 83, DD 80, OOS 56, H1 42, CAGR 41.
* **Breakeven c\*** (largest whole bps at which all five 4b bars hold): the record's weekly high
  moves from idea 331's **47** to **60 bps** — U56 `(e=16, x=40)`, first failing bar DD. The four
  highest c* cells all carry e >= 8, so the entry buffer does buy cost tolerance even though it
  buys no admission.
* Saturation, stated: on U56 (mean 37.5 eligible names/day) `x=40` and `x=80` are the **identical
  book** — once `n+x` exceeds the eligible count the exit buffer stops biting. B136 and SMALL439
  are wide enough that they do not saturate.

## [D] Rule 8 walk-forward — the honest version of "which side carries it"

`(e,x)` chosen on 2008-2016 IS Sharpe @10 bps, 2017-2026 read once, on three menus.
SPY OOS 0.882 (15.45% CAGR, -33.72% MaxDD).

| menu | mean OOS Sharpe | mean regret | beats anchor (0,0) | beats idea 331 (0,20) | beats SPY | beats LIVE |
|---|---|---|---|---|---|---|
| FULL (42 cells) | 0.8410 | -0.0887 | 2/3 | 1/3 | 1/3 | 1/3 |
| **EXIT-ONLY (e=0, 6 cells)** | **0.8836** | **-0.0461** | **3/3** | **3/3** | **2/3** | 0/3 |
| ENTRY-ONLY (x=0, 7 cells) | 0.8335 | -0.0962 | 2/3 | 1/3 | 1/3 | 0/3 |

**Removing the entry dial from the chooser's menu is worth +0.0426 of mean OOS Sharpe and halves
its regret**, and the exit-only menu is the only one that beats the (0,0) anchor and idea 331's
own cell on all three panels. On U56 the exit-only menu picks the OOS-best cell exactly (regret
0.000); the full menu's entry-buffered pick carries regret -0.021. On B136 the full menu's pick
`(16,10)` lands at OOS 0.772 — **below SPY** — against the exit-only menu's 0.936. This is the
13th instance in the record of an IS chooser missing the OOS-best cell, and it is the second
(after idea 331) where the fix is to take an instrument OFF the menu. Every menu loses to the
live RULES v2 book out of sample on U56 and B136.

## KEEP-candidate (4b), PARK-recommended

`U56, n=20, enter at rank <= 4 (e=16), exit at rank > 60 (x=40), NORM g/k_t at g=0.75, WEEKLY`
— 16.52% / **1.164** / -19.02%, H1/H2 **1.245 / 1.096**, OOS **1.168** (17.18% CAGR, -19.02% DD),
turnover 5.45x/yr, ~11.1 names, **4b PASS at 0, 10 AND 25 bps**, **c\* = 60 bps** (the record's
highest weekly breakeven). It is the FULL menu's own rule-8 pick, so its OOS number is untouched
by hindsight. Fails 4a on H2 (-0.095) and drawdown (-0.070; -19.02% vs the live book's -12.05%).

**PARKed, and the PARK is the point of the run:** the identical construction fails 4b on B136 and
SMALL439 at every rung; the cell is ~11 names rather than 20, so it is a concentration bet the
band framing hides; and this run's own rule-8 evidence says an ex-ante chooser is **better off
without the dial that produced it**. Adopting it would mean writing into RULES the one instrument
whose presence on the menu costs OOS Sharpe on 2 of 3 panels. Memo: `.memo.md`.

## Caveats

1. **SURVIVORSHIP** — all three panels are current-constituent lists, so every CAGR *level* is
   optimistic. The e- and x-*differences* this run measures are far less exposed, but the
   concentration finding in [B1] is the most exposed of them: a 7-to-11-name book drawn from a
   survivor list is flattered more than a 20-name one.
2. SMALL439 starts 2010-01-04, so its halves are not the same calendar halves as U56/B136, and
   rule 8's IS window is effectively 2010-2016 there (idea 111's sample-start caveat applies).
3. The entry buffer changes the number of holdings; gross stays at 0.75 by construction, so this
   is concentration, not leverage. `names` is printed for every cell so the reader can price it.
4. `x = 40` and `x = 80` are the same book on U56 (saturation, above); the U56 exit ladder is
   therefore 5 distinct points, not 6.

## Follow-ups queued

**357** — is the entry buffer just `n` in disguise? (`e` at fixed `n` vs a plain top-(n-e) cut).
**358** — does the exit buffer's name-count neutrality survive a cap of `n` instead of `k_t`?
**359** — census: how many of the record's "band" rows are concentration changes in disguise?
