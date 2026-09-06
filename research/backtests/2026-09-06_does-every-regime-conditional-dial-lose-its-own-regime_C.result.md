# Idea 246 — does-every-regime-conditional-dial-lose-its-own-regime (lane C, 2026-09-06)

**Verdict: ANSWERED — the queue's CONCLUSION generalises (conditional arms lose more per
armed day than unconditional ones in 122–129 of 136 cells, sign p < 0.0001, for all three
regimes) but its stated MECHANISM is refuted. Idea 75's "conditioning concentrates the
instrument into the regime where it is most expensive" is a property of TRIGGER instruments
(stops), not of conditioning: pooled over 8 instruments the always-on delta is worse in its
own regime in 68/136 cells for `spy200` (a coin flip, p 1.00) and BETTER in 82/136 for
`breadth20` (p 0.020, the wrong sign), and for the two de-grossing instruments the crash
regime is where they PAY (median +12.6 pp/yr for `gross50`, +5.8 for `ddctl8`). An exact
three-way decomposition of the queue's own statistic shows concentration is 13% of it; the
majority, 52%, is LEAK — the conditional arm is not inert on its disarmed days, and dividing
by the armed fraction multiplies that residue by 4.9–10.6x. On the unnormalised total the
sign REVERSES: conditional arms lose LESS than always-on ones in 112–124 of 136 cells.
"Loss per armed day" is therefore not a safe statistic and PROTOCOL should not quote it alone.**

Script: `2026-09-06_does-every-regime-conditional-dial-lose-its-own-regime_C.py`.
594 runs (3 panels x 3 books x (8 instruments x 4 regimes + 1 control) x 2 cost rungs), every
one printed and written to the `.grid.csv`. Exactly TWO tuned parameters: the INSTRUMENT
family and the REGIME family. Every setting inside a family (band width 3%, stop depths
15/25%, D=8%/k=0.5, breadth 20th pct, vol 80th pct, m=0.50) is the project's published one
and is never selected on. Idea 94's harness is imported, not re-implemented.

## 0. Reproduction — exact
With the regime mask all-True, this run's simulator equals idea 94's `run` at
**max|diff| = 0.000e+00** on returns, at both cost rungs, for a gate arm, a stop arm, a
DD-control arm and a gross arm (CHECK (b), 8 assertions). Arming gates the instrument's
ACTION, never its STATE — a disarmed stop still tracks its per-name high, a disarmed DD
control still tracks book equity — so `always` is a strict special case of every conditional
arm, not a re-parameterisation.

## 1. Regime coverage (post-warm-up)
| panel | regime | armed frac | days | IS frac | OOS frac |
|---|---|---|---|---|---|
| u56 / broad | spy200 | 0.171 | 757 | 0.177 | 0.165 |
| u56 | breadth20 | 0.087 | 384 | 0.031 | 0.132 |
| u56 / broad | hivol80 | 0.109 | 482 | **0.033** | **0.171** |
| broad | breadth20 | 0.081 | 359 | 0.025 | 0.127 |
| small | spy200 / breadth20 / hivol80 | 0.153 / 0.123 / 0.175 | 603 / 484 / 690 | 0.134 / 0.049 / 0.077 | 0.165 / 0.169 / 0.236 |

`breadth20` and `hivol80` use EXPANDING quantiles with a 3y minimum, so there is no
full-sample threshold anywhere. The price of that honesty is a coverage asymmetry — `hivol80`
arms 3.3% of IS days against 17.1% of OOS days (~66 armed IS days on u56). Stated, not
corrected; it is the reason section 5's KEEP-path finding is PARKed rather than KEEPed.

## 2. H1 — the queue's claim, on the queue's own statistic: CONFIRMED
`L = [ann return of arm − ann return of its own control] / armed fraction`, pp/yr per unit.

| regime | n | median L(cond) − L(always) | more negative than always-on | sign p |
|---|---|---|---|---|
| spy200 | 136 | **−2.343 pp/yr** | 122/136 (89.7%) | 0.0000 |
| breadth20 | 136 | **−3.358** | 123/136 (90.4%) | 0.0000 |
| hivol80 | 136 | **−2.700** | 129/136 (94.9%) | 0.0000 |

It holds for every one of the 8 instruments separately (14/18 to 18/18 cells each) and at
both cost rungs. On this statistic the queue's general claim is true and not marginal.

## 3. H2 — the queue's MECHANISM: refuted except for stops
Annualised delta of the ALWAYS-ON arm split by regime (`d_on` vs `d_off`, medians over the 18
panel x book x cost cells). Idea 75's claim is `d_on < d_off`.

| instrument | spy200 d_on / d_off | breadth20 d_on / d_off | hivol80 d_on / d_off |
|---|---|---|---|
| stop15 | **−3.75 / −0.69** | **−3.76 / −0.87** | **−5.70 / −0.55** |
| stop25 | −1.24 / −0.21 | −1.59 / −0.25 | −1.99 / −0.13 |
| band3-dg | −1.50 / −0.03 | −0.36 / −0.12 | −2.29 / −0.11 |
| g200-dg | −0.94 / −0.10 | +0.05 / −0.15 | −2.38 / −0.12 |
| abs12-dg | −0.80 / −0.30 | **+1.38 / −0.34** | −0.87 / −0.34 |
| vol60-dg | −1.68 / −1.58 | **0.00 / −1.99** | −5.46 / −1.37 |
| ddctl8 | **+4.79 / −4.57** | **+6.93 / −4.79** | −7.33 / −3.09 |
| gross50 | **+8.81 / −9.24** | **+13.31 / −8.65** | −7.86 / −5.80 |

Pooled over all 136 cells: `spy200` **68/136** on-regime worse (p 1.000), `breadth20`
**54/136** (p 0.020 — significant in the OPPOSITE direction), `hivol80` 121/136 (p 0.0000).
So the mechanism idea 75 measured is real for the instrument it measured — the per-name stop
is dearest in a crash at both depths, in 18/18 and 11/18 cells — and for high-vol arming
generally, but it does not generalise to conditioning as such. **For the two instruments that
purely reduce exposure, the crash regime is the one regime where they earn their keep**, which
is the opposite of the queue's premise and is exactly why idea 6's breadth sleeve and idea 40
were built the way they were.

## 4. The decomposition — what H1 actually is (the decisive section)
Because `ann()` is additive over day sets, with `c_on`/`c_off` the CONDITIONAL arm's own delta
on armed/disarmed days, the queue's statistic splits three ways **exactly**
(`max|residual| = 7.3e-14`):

    L(cond) − L(always)  =  CONC + ACT + LEAK
    CONC = (1−f)(d_on − d_off)     the instrument being dearer in its own regime  [idea 75]
    ACT  = c_on − d_on             the conditional arm acting differently ON armed days
    LEAK = ((1−f)/f) · c_off       its delta on days it is SUPPOSED to be inert, x (1−f)/f

| regime | n | median total | CONC | ACT | LEAK |
|---|---|---|---|---|---|
| spy200 | 144 | −2.343 | **0.000** | −0.782 | **−1.543** |
| breadth20 | 144 | −3.358 | **+0.806** | −1.124 | **−2.919** |
| hivol80 | 144 | −2.700 | −1.922 | 0.000 | −0.395 |
| pooled | 408/354/376 | — | −0.366 (243/408 neg, p 0.0001) | −0.181 (245/354, p 0.0000) | **−1.425 (344/376, p 0.0000)** |
| share of median total | | 100% | **13%** | 7% | **52%** |

The residual `c_off` is small in absolute terms — median |c_off| 0.28 pp/yr (`breadth20`),
0.32 (`spy200`), 0.07 (`hivol80`) — but the `(1−f)/f` factor is 10.6, 4.9 and 8.2, so it
dominates. Its proximate cause is trading: `switch_mult` = (conditional turnover / always-on
turnover) / armed fraction is **5.95 (spy200), 11.57 (breadth20), 9.07 (hivol80)** at the
median, and **> 1 in 432 of 432 cells**. A conditional arm armed a tenth of the time pays
roughly full switching cost, and its holdings on the days after it disarms are not the
control's holdings. That, not concentration, is what the per-armed-day statistic is measuring.

**The normalisation is doing the work.** On the raw, unnormalised loss the answer flips:

| regime | median d_ann(cond) | median d_ann(always) | conditional WORSE in |
|---|---|---|---|
| spy200 | −0.650 pp/yr | −1.465 | 20/132 (p 0.0000) |
| breadth20 | −0.466 | −1.465 | 14/136 (p 0.0000) |
| hivol80 | −0.489 | −1.465 | 12/136 (p 0.0000) |

## 5. H3 — KEEP paths (all 594 rows evaluated on both)
Conditional arms: 145/432 pass 4a, 88/432 pass 4b. Always-on arms: 54/144 and 11/144.
Do-nothing controls: 5/18 and 0/18. **Stops: 0 of 144 arms pass 4b at any depth or regime.**
Conditional arms passing 4b where BOTH their own control AND their own always-on sibling
fail: **56/432** — but only **5/432** for 4a, i.e. these are drawdown-cap passes, which is
idea 94's known result that de-grossing instruments buy drawdown, not a new edge.

**PARK, not KEEP** — `EWall + band3-dg armed only in hivol80` is the one arm worth a follow-up.
u56 @10 bps: CAGR 12.22%, Sharpe 1.2116, MaxDD −15.50%, halves 1.2333/1.1919, OOS 1.2831
(SPY 15.23% / 0.889 / −33.72%, OOS 0.882; 4b bars DD ≤ 20.23%, CAGR ≥ 10.66%). It passes 4b
on u56 AND broad at BOTH cost rungs, its always-on sibling fails 4b (de-grossing to 0.53 mean
gross drops CAGR to 8.66%, under the floor), the neighbouring `g200-dg/hivol80` gives the same
answer, and rule 8 picked it independently on IS in 4 of 18 cells. It is PARKed and not KEEPed
for one disqualifying reason: **`hivol80` arms only ~66 IS days (3.3%) against 17.1% of OOS
days**, so the walk-forward that selected it barely exercised the regime it depends on. The
named next test is in QUEUE as idea 247.

## 6. Rule 8 walk-forward — (instrument, regime) chosen on 2009–2016 IS Sharpe alone
Menu of 32 arms + the do-nothing control per cell, read once on 2017–2026.
Chooser beats do-nothing OOS in **8/18** cells; mean regret **+0.0188**, **median +0.0000**;
median Spearman(IS Sharpe, OOS Sharpe) across the menu **0.174**. It picks a CONDITIONAL arm
in 13/18 cells. Best and worst: u56/EWall @10 bps +0.1474 (band3-dg/hivol80, OOS Sharpe 1.2831
vs 1.1357) and small/TOP20 @10 bps **−0.1765** (vol60-dg/breadth20, 0.6327 vs 0.8091 — OOS
CAGR 11.19% vs the control's 17.10%). This is the **16th** entry in the record's
selection-loses census: a positive mean carried by two EWall cells, a median of exactly zero,
and a single pick that costs 0.18 of Sharpe.

OOS levels at 10 bps (pick / do-nothing / RULES v1 / SPY), CAGR and Sharpe:
u56 EWall 11.77% 1.2831 / 13.82% 1.1357 / 7.73% 0.7471 / 15.45% 0.8820 ·
broad EWall 11.08% 1.2220 / 13.93% 1.1022 / 5.94% 0.5763 / 15.45% 0.8820 ·
small EWall 8.66% 0.6517 / 10.09% 0.6367 / 7.92% 0.5807 / 15.45% 0.8820.
Every pick trails SPY's OOS CAGR; the EWall picks beat SPY's OOS Sharpe on much less drawdown.

## 7. What the project should take from this
1. Idea 75's finding stands but is about **stops**, not about **conditioning**. The record's
   "regime-conditional dials lose" pattern needs a new explanation for the other instruments.
2. **Do not quote "loss per armed day" without its decomposition.** A statistic divided by a
   small armed fraction is dominated by whatever the arm does when it is supposedly off; here
   that is 52% of it, against 13% for the effect the statistic is named after.
3. The same conditional-vs-unconditional comparison answers **opposite ways** depending on
   whether it is normalised by exposure. Both belong beside any such claim.
4. Conditioning still fails the thing that matters: 0/144 stop arms and only 5/432 conditional
   arms clear 4a over their own always-on sibling, and the chooser's median regret is zero.

## Caveats carried, not buried
* SURVIVORSHIP: all three panels are current-constituent lists (idea 54), so every absolute
  CAGR is optimistic. Sections 2–4 are paired deltas on the same panel and the same days and
  are far less exposed; the section 5 and 6 LEVELS are fully exposed and should be read as
  upper bounds.
* The small panel drops the 44 bad-split tickers of `data/small_meta.csv` (439 names) and
  holds SPY as a benchmark only, never as a constituent.
* `spy200`, `breadth20` and `hivol80` are three regimes, not the space of regimes; a regime
  the project has not written down could behave differently.
* `ACT` and `LEAK` are the residuals of an exact identity, not independently modelled
  quantities. The turnover table is evidence for the reading given, not a proof of it.
