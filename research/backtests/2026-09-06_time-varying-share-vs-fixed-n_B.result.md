# Idea 157 — time-varying-share-vs-fixed-n (lane B, 2026-09-06)

**VERDICT: KILL of the time-varying count `n_t = round(m x E_t)`.  Idea 153's memo clause 7
("Ebar must be a pre-registered constant per universe") is CORRECT and stands.  No RULES
change, no new book, no KEEP-candidate.  RULES.md, scan.py, bot.py and baseline.py untouched.**

Script `research/backtests/2026-09-06_time-varying-share-vs-fixed-n_B.py`; outputs
`.console.txt`, `.grid.csv`, `.gross.csv`, `.peryear.csv`, `.paired.csv`, `.walkforward.csv`.
336 books = 3 panels x 7 book shares x 4 count rules x 2 weight constructions x 2 cost rungs,
weekly, t+1, long-only, 10 and 25 bps.

## Controls, before any result was read

| control | result |
|---|---|
| **[B] the decisive one** — FIX/lit vs idea 153's committed `grid.csv`, all 42 published cells x 7 statistics | **worst \|diff\| 3.55e-15**, m→n map identical on all 21 (panel, m) points → this is idea 153's instrument with one axis added |
| [C] Ebar reproduction (u56 37.5 / broad 91.5 / small 141.2) | 37.50 / 91.46 / 141.23 → MATCH |
| [D] derived cost rung vs a direct `engine.backtest(cost=25)` | **0.000e+00** → the two rungs are the same book bar for bar |
| [E] restated (see below) | lit == norm on every bar where the rankable count covers the slots: **0.000e+00** |

**[E] caught a wrong premise in my own pre-registration, and it is reported rather than
buried.** I wrote that ADAPT "is ALWAYS fully invested" because `n_t = round(m x E_t) <= E_t`.
False: `E_t` counts names that pass the 200d/vol20 gate, but the composite cannot *score* a
name whose 252-day momentum window is still NaN, so the rankable count `R_t <= E_t` and the
adaptive book can be short of slots even at m = 1.00 — on **6.2% of u56 bars, 8.4% of broad
bars and 58.6% of small-panel bars**. Every invested-gross number below is measured, not
assumed. The pre-registration is left verbatim in the script with a labelled post-run
correction; nothing else changed.

## The head-to-head the queue asked for (m = 0.53, the incumbent's share, 10 bps, lit)

| panel | rule | CAGR | Sharpe | MaxDD | H1 / H2 | OOS Sharpe | turnover | 4a | 4b |
|---|---|---|---|---|---|---|---|---|---|
| u56 | **FIX** (incumbent, n=20) | 12.66% | **1.0921** | **-18.31%** | 1.088 / 1.102 | 1.1680 | 9.63x | FAIL | **PASS** |
| u56 | ADAPT (n_t, mean 19.84) | 13.01% | 1.0535 | -19.36% | 0.981 / 1.121 | **1.1763** | 12.80x | FAIL | PASS |
| broad | **FIX** (incumbent, n=48) | 11.70% | **1.0269** | **-18.90%** | 1.123 / 0.940 | **1.0375** | 9.36x | **PASS** | **PASS** |
| broad | ADAPT (n_t, mean 48.46) | 11.47% | 0.9525 | **-23.20%** | 1.019 / 0.892 | 0.9807 | 12.52x | FAIL | **FAIL (DD)** |

**The single decisive number: on `universe_broad.json` the time-varying count takes the book's
drawdown from -18.90% to -23.20% against a 4b cap of -20.23%, so it FAILS 4b by 2.97pp on the
exact panel idea 153's candidate was adopted for.** Idea 153's whole claim was portability —
that a *share* travels across panels where a *count* does not. Making the share time-varying
destroys that claim while costing +3.16x/yr of turnover. SPY is 15.23%/0.889/-33.72%.
Both rules die at 25 bps on both panels (idea 137's wall, reproduced).

## Rule 8 walk-forward — the dial is worth exactly nothing

Parameters chosen on 2009-2016 only, read once on 2017-2026, against the do-nothing incumbent
(FIX at m = 0.53), RULES v1 and SPY.

**S3 (the narrow question: share pinned at 0.53, only the count rule chosen) re-picks FIX in
8 of 8 large-cap cells and therefore adds `d_ctl = +0.0000` OOS Sharpe on every one of them.**
On the small panel it picks ADAPT63 and gains +0.045 / +0.037 (lit) but loses -0.028 / -0.030
(norm) — a coin flip, and all four sit far below SPY's 0.8820. P6 HIT: S3 beats doing nothing
in 0 of 4 large-cap 10 bps cells. The wider selectors are worse: S0 (free choice of m and
rule) averages **-0.0445** OOS Sharpe against doing nothing, and on broad@10bps/lit it picks
`ADAPT|m0.10` for **-0.2904**. Nothing here picks the OOS oracle on either large-cap panel.
This is the **ninth consecutive selection-loses-to-doing-nothing instance** in the record.

## Mechanism — it is a cash question, not a breadth question

Under the incumbent's own `lit` weighting (GROSS/n per name), fixed-n silently holds cash
whenever the eligible list is shorter than n. That buffer is large and it is concentrated
exactly where it matters:

| panel, m=0.53, lit | invested gross, full | 2020 | **2022** |
|---|---|---|---|
| u56 FIX | 0.7168 | 0.6914 | **0.5430** |
| u56 ADAPT | 0.7461 | 0.7436 | **0.7411** |
| broad FIX | 0.7209 | 0.6722 | **0.6216** |
| broad ADAPT | 0.7492 | 0.7488 | **0.7464** |

In 2022 the incumbent held **45.7% of capital in cash on u56** (0.5430 invested against a
0.75 gross target) — **19.8pp more cash than the adaptive book**, which held essentially none.
Splitting the two channels: with cash held equal (`norm`) the mean |dSharpe| between the rules
on the large-cap cells is **0.0422** (P4 HIT, predicted < 0.05) — **breadth-timing per se
carries almost nothing.** Under `lit` the same figure is 0.0641 and ADAPT's drawdown is deeper
in **26 of 28** large-cap cells (mean -4.50pp, P3 HIT). What the fixed count is being paid for
is the cash, not the count.

## 2020 and 2022 separately (the queue's explicit ask) — idea 46 is half right

ADAPT minus FIX, calendar-year return, all 12 (panel, construction, cost) cells:

* **2022: ADAPT wins 12 of 12**, +0.92 to +5.31pp (u56 -5.80% vs -9.02%; broad -6.92% vs
  -10.96%; small -12.63% vs -17.29% at 10 bps/lit). The adaptive count *is* a genuine 2022
  defence, and it is one full-sample Sharpe hides — exactly idea 46's claim.
* **2020: ADAPT wins 4 of 12** — u56 only (+4.58 to +5.80pp); it LOSES on broad (-4.86 to
  -8.22pp) and small (-1.04 to -4.51pp).
* Across all calendar years at m=0.53/10bps/lit: ADAPT beats FIX in 8/18 years on u56
  (mean +0.35pp), **8/18 on broad (mean -0.28pp, worst year 2020 at -7.19pp)** and 9/16 on the
  small panel (mean +0.27pp).

So idea 46's bear defence is real in one bear and reversed in the other. The mechanism is not
the cash (ADAPT holds *less* cash) — it is selectivity: when the eligible list halves, the
adaptive book holds the top half of it while the fixed book holds all of it. That helped in
2022's slow grind and hurt in 2020's V-shaped recovery, when the fixed book's full eligible
list caught the rebound.

## KEEP paths across the whole grid

| | u56 | broad | small |
|---|---|---|---|
| 4b passes, FIX | **7 of 28** | 5 of 28 | 0 of 28 |
| 4b passes, FIXIS | 7 of 28 | 5 of 28 | 0 of 28 |
| 4b passes, **ADAPT** | **4 of 28** | **2 of 28** | 0 of 28 |
| 4b passes, ADAPT63 | 5 of 28 | **6 of 28** | 0 of 28 |

P5 HIT on both halves: ADAPT passes 4b strictly less often than FIX on both large-cap panels,
and the **small panel contributes 0 of 112 at every m, rule, construction and cost rung — the
ninth reproduction of idea 136**. Every 4b pass in the entire grid is a 10 bps pass; 0 of 168
cells pass at 25 bps.

## The one thing that survives, and why it is still not a KEEP

`ADAPT63` (n_t from a 63-bar trailing mean of E_t) is the only arm that beats the incumbent's
4b pass count anywhere: 6 of 28 on broad against FIX's 5, keeping 4b at m = 0.53 (-18.97% DD)
and m = 0.75 (11.01%/1.0409/-16.39%, OOS 1.1072, 4a AND 4b PASS) where raw ADAPT fails both.
It is reported as a by-product and **explicitly NOT proposed**, for three stated reasons:
(i) rule 8 never picks it on either large-cap panel — S3 re-picks FIX in 8/8 cells;
(ii) it dies at 25 bps like everything else; and (iii) the 63-bar window is a **third,
unswept parameter** baked into the arm, so its apparent edge is exactly the kind of unpriced
dial idea 223 has just finished pricing on the trade-date anchor.

## FIXIS — the lookahead audit nobody had run

Idea 153's published Ebar is a **full-sample** mean, so the incumbent's n = 20 (u56) and n = 48
(broad) read the future. `FIXIS` recomputes Ebar on 2009-2016 only and gives n = 19 / 48 / 71.
The cost of removing the lookahead is small but not zero and it is one-directional: u56 Sharpe
1.0921 → 1.0607 (-0.031) and OOS 1.1680 → 1.1280 at m = 0.53/10bps/lit; **broad is unchanged
(n = 48 either way)**; the small panel loses 0.019. The candidate's headline u56 number is
therefore about 0.03 of Sharpe optimistic relative to a rule that could actually have been
written in 2016. This is a caveat on the standing candidate, not a new result, and it is
recorded here because the audit had not been done.

## Predictions

P1 HIT (control B). P2 mostly HIT — ADAPT's invested gross exceeds FIX's by +0.016/+0.017/
+0.018 full-sample on the three panels and by +0.105 (u56, 2022), but not at *every* m
(min -0.0024 at small m where the fixed count rounds up). P3 HIT (26/28). P4 HIT (0.0422).
P5 HIT. P6 HIT (0 of 4).

## Caveats carried, not buried

* **Survivorship:** all three panels are current-constituent lists (idea 54); the small panel
  drops the 44 names with `max_1d_move >= 1.0` and holds SPY out. No level here is an
  attainable return; the FIX-vs-ADAPT *difference* is the durable part.
* Ideas 49/39: the eligibility gate is **inverted** on the small panel, so `E_t` there is the
  count of a gate that does not work. Small-panel numbers are reported, not traded.
* **Idea 223 applies and is not re-measured:** a weekly schedule has 5 trade-date anchors and
  every drawdown number above is one anchor's. The broad 4b failure margin (2.97pp) is larger
  than 182B's measured 8-anchor monthly band (2.51pp), but that band was measured on a monthly
  schedule and is not a bound for this one.
* Idea 38 (calendar-day price index) and idea 126 (t+1 execution only) carry over.
* Costs are a flat linear bps charge; 10 bps on a 439-name sub-$2B panel is not the same
  instrument as 10 bps on u56.
