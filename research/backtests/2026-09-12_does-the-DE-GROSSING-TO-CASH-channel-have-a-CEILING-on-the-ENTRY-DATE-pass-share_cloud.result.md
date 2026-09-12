# Idea 830 — does the DE-GROSSING-TO-CASH channel have a CEILING on the ENTRY-DATE pass share? (cloud lane, 2026-09-12)

**ANSWERED: YES — AND IT IS 0.6250, WITH THE CHANNEL'S TWO DIALS ACTING ON EVERY 4b LEG EXCEPT
THE ONE THE CHANNEL EXISTS TO BUY.** Sweeping band width × cash rung (32 cells) takes MA-DG's
3-year entry-date 4b pass share from **0.3977** (the live band at zero cash, reproducing idea
829's headline exactly) to a peak of **0.6250** at band 0.01 / cash 500 bps — an interior argmax,
never 0.80. Over **all 384** cells at the PROTOCOL cost rung and the queue's 3-year horizon
(3 panels × 2 grosses × 2 spacings × 32 cells) the ceiling is **0.6989 and NOT ONE cell reaches
0.80**. The queue's mechanism is wrong: the leg that closes first is **not** one of 4b's two ratio
legs but its **HALVES clause** (binding at 23 of 32 cells, 0.7670 at the argmax), the very clause
ideas 832/838/839 have already shown to be inert, uninformative and unmeasurable. And the drawdown
leg — the whole reason MA-DG survives gross 1.00 — sits at **exactly 0.8636 at all 16 cells with
band ∈ {0.01, 0.02, 0.03, 0.05}, perfectly invariant to the cash rung and flat across a 5×
band range**: the channel's advantage is a plateau neither dial can push. What the cash rung
actually buys is the CAGR floor and the halves clause (at band 0.01: leg_halves 0.4943 → 0.7670,
leg_cagr 0.6932 → 0.8352, leg_sharpe 0.9034 → 0.9886, **leg_dd 0.8636 → 0.8636**) — it is a
**return subsidy, not a de-grossing effect**. **KILL. No KEEP claimed, no book promoted, no memo,
no RULES/PROTOCOL change (rule 6); RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py
untouched.**

Script: `2026-09-12_does-the-DE-GROSSING-TO-CASH-channel-have-a-CEILING-on-the-ENTRY-DATE-pass-share_cloud.py`
(`.txt`, `.grid.csv`, `.legs.csv`, `.census.csv.gz`, `.fixed.csv`, `.wf.csv`). Runtime 103s.
Two tuned parameters: **P1 band** ∈ {0.00, 0.01, 0.02, 0.03, 0.05, 0.08, 0.12, 0.20},
**P2 cash rung** ∈ {0, 150, 300, 500} bps/yr — all 32 cells reported, none dropped. Gross
{0.75, 1.00}, H {756, 1260}, spacing {21, 63}, cost {10, 25} bps and panel {U56, B136, SMALL}
are reported axes, fixed at the record's committed values.

## Gates

| gate | result |
|---|---|
| G1 `fast_backtest` vs `engine.backtest` at cash 0 (returns AND turnover, 3 cells) | max \|dret\| **1.388e-17**, \|dturn\| **2.776e-16** vs bar 1e-12 — PASS |
| G2 `fmet` vs `engine.metrics` on 200 real windows | max \|diff\| **2.220e-16** vs bar 1e-10 — PASS |
| **G3 reproduce idea 828/829's committed headline** | **6 of 6 EXACT** (diff 0.000000): pass **0.397727**, leg_sharpe 0.914773, leg_halves 0.517045, leg_dd **0.863636**, leg_cagr 0.727273, n **176**. 828's MA-RS control also reproduces: leg_dd **0.005682** — PASS |
| G4 the committed candidate memo's fixed-window triple | 8 of 8 within 0.010: 11.54% / 1.2017 / −15.91% full, 12.70% / 1.2775 OOS; SPY 15.16% / 0.8861 / −33.72% — PASS |
| **G5 the C-CASH convention is exact, not a shortcut** | max \|exact − additive\| pass share over 32 cells **0.0000**; max full-sample CAGR difference **0.09 bps/yr** — PASS |
| G6 the credit has the right sign (median window CAGR monotone in the cash rung at every cell) | **0 violations** — PASS |

**C-CASH declared:** the de-grossed balance compounds *inside* each rebalance segment
(`cash_t = cash_0 (1+rc)^(t−t_0)`), enters the weight drift and the turnover calculation, and no
turnover cost is charged on the cash leg — which is what makes the cash = 0 column bit-identical
to idea 828's MA-DG column. G5 shows the cheaper additive shortcut would have changed nothing
(0.09 bps/yr), so this axis is not a convention artefact either way.

## The sweep: joint 4b pass share, band × cash (U56, gross 1.00, H = 756, s = 21, 10 bps, n = 176)

| band | cash 0 | 150 | 300 | 500 |
|---|---|---|---|---|
| 0.00 | 0.3523 | 0.4375 | 0.5170 | 0.5398 |
| **0.01** | 0.3693 | 0.4602 | 0.5511 | **0.6250** |
| 0.02 | 0.3636 | 0.4659 | 0.5000 | 0.6193 |
| **0.03 (LIVE)** | **0.3977** | 0.4659 | 0.5000 | 0.5625 |
| 0.05 | 0.3239 | 0.3977 | 0.4716 | 0.5284 |
| 0.08 | 0.3295 | 0.3636 | 0.3693 | 0.3977 |
| 0.12 | 0.1989 | 0.2159 | 0.2216 | 0.2557 |
| 0.20 | 0.1648 | 0.2443 | 0.2955 | 0.3580 |

Median over the 32 cells **0.3977**, min 0.1648, **max 0.6250**.

- **H_830 (some cell ≥ 0.80) FAIL.** **H_CEIL: the channel's ceiling is 0.6250** at the headline
  cell and **0.6989** over all 384 cells at 10 bps and H = 756, where **0 of 384 reach 0.80**.
- **H_BAND PASS** — the argmax band 0.01 is interior to the swept grid, so the peak is real and
  not a grid edge. It is also *not* the live band: 0.03 peaks at 0.5625.
- **H_CASH PASS** — band-wise `share(500) − share(0)` runs **+0.0568 to +0.2557** (max at band
  0.01), comfortably over the 0.10 bar, so the cash rung is a live dial and not a rounding effect.
  It is not, however, the *stronger* dial: the cash-wise band spread reaches **0.3693** (at cash
  500) against the band-wise cash gain's 0.2557, so choosing the band moves the share more than
  paying interest does. Neither is enough.
- **H_CLOSE FAIL** — binding leg at the argmax is **`leg_halves` (0.7670)**, a RANK leg. Over the
  32 cells: **`leg_halves` binds 23 times, `leg_dd` 9 times** (only at bands ≥ 0.08), and
  `leg_cagr` and `leg_sharpe` bind **never**. The queue's "4b's two ratio legs close before it
  does" is not what happens.

## The leg that does not move: the drawdown plateau

| band | leg_dd at cash 0 / 150 / 300 / 500 | distinct values |
|---|---|---|
| 0.00 | 0.7102 / 0.8636 / 0.8636 / 0.8636 | 2 |
| **0.01 – 0.05** | **0.8636 / 0.8636 / 0.8636 / 0.8636** | **1** |
| 0.08 | 0.5795 / 0.5795 / 0.7330 / 0.7330 | 2 |
| 0.12 | 0.3523 (all four) | 1 |
| 0.20 | 0.3807 (all four) | 1 |

`leg_dd` is **exactly 0.863636 at 19 of 32 cells** and at *every* cell with band ∈ {0.01, 0.02,
0.03, 0.05}. So the de-grossing channel's one genuine advantage — idea 828's finding that MA-DG
is the only form whose DD leg survives gross 1.00, `leg_dd` 0.8636 against ≤ 0.0057 for every
re-spreading form — is a **step function with a wide plateau**, insensitive to both of the dials
the queue proposed for pushing it. The re-spreading twin confirms the channel is the DD leg and
nothing else: **MA-RS's ceiling over the same 32 cells is 0.0057, and its `leg_dd` ceiling is
0.0057 against MA-DG's 0.8636** — the cash rung cannot rescue a re-spread book at all, because a
re-spread book has no cash to credit.

## Every reported axis: where 0.80 *is* reachable, and why it does not count

| slice | ceiling | argmax (band, cash) |
|---|---|---|
| U56 g1.00 H756 s21 10bps *(headline)* | **0.6250** | (0.01, 500) |
| U56 g0.75 H756 s21 10bps | 0.6989 | (0.20, 500) |
| B136 g1.00 H756 s21 10bps | 0.6080 | (0.02, 500) |
| SMALL g1.00 H756 s21 10bps | **0.1776** | (0.12, 500) |
| U56 g1.00 **H1260** s21 10bps | **0.9013** | (0.03, 500) |
| B136 g0.75 **H1260** s21 10bps | **0.9342** | (0.08, 500) |

Over all **1,536** MA-DG cells the maximum is **0.9342** and **62 cells sit at or above 0.80** —
but **every one of the 62 is at H = 1260, on U56 or B136, and NOT ONE is at cash = 0**. Clearing
the bar therefore requires *both* lengthening the horizon past the 3 years the queue asked about
*and* paying interest on the cash leg. At the 3-year horizon and PROTOCOL's cost rung the count is
**0 of 384**. On the SMALL panel the ceiling is **0.1776** — the channel is a large-cap
phenomenon.

**The anachronism that disqualifies the cash rung as a fix (idea 642's caveat, now binding).** A
flat 500 bps credited over 2009–2026 is not a cash rate that existed: T-bills paid roughly 10 bps
to 2015 and ~500 only after 2022, so a flat 500 bps back-pays ~5%/yr on the de-grossed fraction
through the entire ZIRP era. That is exactly where the gain lands: the cash rung's contribution is
a level shift in CAGR (median window CAGR 10.28% → 11.93% at band 0.01) and every one of the 62
cells ≥ 0.80 depends on it. **The honest reading of the P2 axis is a sensitivity, not a
prescription** — and even taken at face value it stops at 0.6250 on the 3-year horizon.

## RULE 8 — (band, cash) chosen on IS entry dates only, read once on OOS entry dates

IS = entry ≤ 2016-12-31 (96 windows), OOS = entry ≥ 2017-01-01 (80 windows).

| | band | cash | IS share | OOS share |
|---|---|---|---|---|
| **IS pick** (best IS) | 0.01 | 500 | **0.4167** | **0.8750** |
| OOS-best cell | 0.02 | 500 | 0.3958 | 0.8875 |
| live band, zero cash | 0.03 | 0 | 0.2812 | 0.5375 |

**H_R8 PASS** — regret **0.0125** against a 0.15 bar, and `Spearman(IS share, OOS share) =
+0.8298` over the 32 cells, so the axis is selectable in sample. **But the OOS share is not the
answer to the queue's question, for two reasons stated together:** (i) every IS share is far below
its OOS twin (0.4167 vs 0.8750 at the same cell; the whole grid's IS ceiling is 0.4167) so the
split is measuring a regime difference, not a selection skill; and (ii) the OOS window
2017–2026 is precisely where a flat 500 bps cash credit is most anachronistic, which is the same
confound as above. The full-sample number the bar should be read on is **0.6250**.

**Mandated book leg, IS-picked cell (MA-DG band 0.01, gross 1.00, cash 500):**
full **12.77% / 1.3375 / −15.78%**; **OOS 13.92% / 1.4156 / −15.78%** against LIVE OOS
9.47% / 1.2782 / −12.05% and SPY OOS 15.33% / 0.8767 / −33.72%.
KEEP paths: **4a FAIL** (DD ≤ LIVE), **4b PASS**, **OOS-only 4b PASS** — a 4b pass bought with
back-paid interest, which is why it gets no memo.

## BOTH KEEP PATHS (fixed window from trading day 260; OOS from 2017-01-01)

| book | full CAGR / Sharpe / MaxDD (H1/H2) | OOS CAGR / Sharpe / MaxDD (H1/H2) |
|---|---|---|
| MA-DG b0.01 g1.00 **c0** | 11.19% / 1.1858 / −15.86% (1.210/1.167) | 12.35% / 1.2701 / −15.86% (1.443/1.079) |
| MA-DG b0.01 g1.00 **c500** | 12.77% / 1.3375 / −15.78% (1.367/1.314) | 13.92% / 1.4156 / −15.78% (1.561/1.256) |
| MA-DG b0.03 g1.00 c0 *(candidate)* | 11.54% / 1.2017 / −15.91% (1.235/1.175) | 12.70% / 1.2775 / −15.91% (1.408/1.135) |
| RULES v2 LIVE (b0.03 g0.75) | 8.63% / 1.2018 / −12.05% (1.235/1.176) | 9.47% / 1.2782 / −12.05% (1.410/1.134) |
| SPY | 15.16% / 0.8861 / −33.72% (0.960/0.826) | 15.33% / 0.8767 / −33.72% (0.980/0.765) |

Across the 64-cell MA-DG fixed-window grid: **4a 15 PASS, 4b 40 PASS, OOS-only 4b 42 PASS.**

**The 4a passes are worth naming precisely, because they are the one place this run produces a
result the record does not already have — and they are bought entirely with back-paid interest.**
All **15 are gross 0.75** and **every one has cash > 0** (6 at 500 bps, 5 at 300, 4 at 150);
**0 of the 16 cash-0 cells passes 4a**. The mechanism is transparent: at gross 0.75 the book's
MaxDD is already at the live book's −12.05%, so the cash credit lifts both Sharpe halves above the
live book's 1.2349 / 1.1757 without touching the drawdown leg — e.g. MA-DG b0.03 g0.75 c500 reads
**11.13% / 1.5233 / −11.93% (halves 1.5730 / 1.4831)** against LIVE 8.63% / 1.2018 / −12.05%
(1.2349 / 1.1757). That is not a rule worth capital: it says *the live book plus 5%/yr risk-free
on its cash beats the live book earning 0% on its cash*, which is an accounting change, not an
edge, and at a rate that did not exist for two-thirds of the sample. **No memo, no promotion —
this is logged as a 4a-path artefact of the cash convention, and it is the strongest argument in
this run that PROTOCOL should fix a declared cash rate before any 4a verdict is read again.**

`baseline.compare()` at 10 bps weekly, cash 0: band 0.01 **11.2% / 1.19 / −15.9%** (1.21/1.17)
and band 0.03 **11.5% / 1.20 / −15.9%** (1.24/1.17) against RULES v2 8.6% / 1.20 / −12.1%
(1.23/1.18) and SPY 15.2% / 0.89 / −33.7% (0.96/0.83) — **at cash 0 both are 4a KILL on the
drawdown leg** and neither beats the live book's Sharpe in both halves. The fixed-window picture
at the record's own zero-cash convention is unchanged by the channel: this run promotes nothing.

## R7 (reported, not a gate) — daily cadence

Weekly ceiling **0.6250** against a daily-cadence ceiling of **0.5682** (band 0.02, cash 500);
max \|weekly − daily\| pass share 0.1307, median 0.0341. Declared: a daily book re-rebalances
every day and pays turnover for it, so this is a comparison between two different books, not a
check on the cash convention (that is G5, which passes at 0.0000). **Neither cadence reaches 0.80.**

## Pre-registered scorecard

| hypothesis | bar | result | verdict |
|---|---|---|---|
| H_830 | some cell ≥ 0.80 at the headline | max 0.6250 | **FAIL** |
| H_CEIL | report the ceiling | **0.6250** headline, 0.6989 over all 3-year cells | reported |
| H_CLOSE | binding leg at the argmax is a RATIO leg | `leg_halves` at 0.7670 (23 of 32 cells) | **FAIL** |
| H_CASH | max band-wise share(500) − share(0) ≥ 0.10 | +0.2557 | **PASS** |
| H_BAND | argmax band interior | band 0.01, interior | **PASS** |
| H_R8 | IS→OOS regret ≤ 0.15 | 0.0125 (ρ +0.8298) | **PASS** |

**3 of 5 testable hypotheses PASS, and the two failures are the two that carry the question.**

## What this leaves standing, and what it retires

**Standing.** Idea 828's finding is confirmed on a 32-cell sweep of the channel itself: the
de-grossing-to-cash form is the only one whose 4b drawdown leg survives, at `leg_dd` 0.8636
against the re-spreading twin's 0.0057 at every band and every cash rung.

**Retired.** The hope in the queue's rationale — *828 showed gross cannot buy the bar; this asks
whether the de-grossing channel can*. **It cannot.** Both of the channel's dials are exhausted
well short of 0.80 at the 3-year horizon (0 of 384 cells at PROTOCOL's cost rung), the dial that
moves the number most (the cash rung) works through the CAGR floor rather than through
de-grossing and is an anachronism at the level that would be needed, and the plateau in `leg_dd`
says the channel's own advantage is already maxed out at the live band. Also retired is the
queue's framing that **4b's two ratio legs** are what close first: the binding constraint is the
**halves clause**, which ideas 832 (inert on the fixed window), 838 (no callable sub-window
length exists) and 839 (never positively informative) have independently shown carries no
information. **Three runs now converge on the same object: the entry-date pass share is capped by
4b's least meaningful clause.** The next question worth asking is not how to raise the share but
whether the halves clause belongs in 4b at all — and that is a rule-6 Sunday-review question, not
a backtest.

**SURVIVORSHIP:** U56 and B136 are current constituents of `research/universe.json` and
`universe_broad.json`; the SMALL panel is current constituents of a sub-$2B screen that is
rewritten nightly (this run's vintage: **663 names after dropping 52 tickers with
`max_1d_move` ≥ 1.0** from `data/small_meta.csv`, against the 439 and 483 earlier runs read —
ideas 824/826). All three panels bias every book **and every pass share** upward. Nothing here is
investment advice.
