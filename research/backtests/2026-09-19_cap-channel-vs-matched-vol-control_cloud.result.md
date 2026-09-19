# Idea 704 — price the CAP CHANNEL against a MATCHED-VOL control

**2026-09-19, lane cloud. VERDICT: ANSWERED — the whole channel survives, and the confound runs
the WRONG WAY. KILL (capital): no new book, no RULES change.**

Idea 694 measured `CAP = rho(q, OOS Sharpe) = -0.7709` at matched width and matched selection
ratio, worth up to -0.853 of OOS Sharpe, and the queue asked whether it is really a name-vol
story: a small-cap name *is* a more volatile name, so any q ladder is also a vol ladder. Every
definition below — the panel builder, CAND-n, the eligibility gate, the metric row, the KEEP
paths, the Spearman, the rank regression — is imported from the committed scripts that published
them (ideas 276 / 286 / 525), never re-typed.

## Three arms, k = 90, r in {0.05, 0.10, 0.25, 0.50}

| arm | cap mix | name vol | what it isolates |
|---|---|---|---|
| **CAP** | the dial (q = 0 .. 1) | rides along | 694's own ladder — the replay |
| **VOLTWIN** | **free** (origin ignored) | **matched** to the cap panel, within TOL | does a pure vol ladder reproduce the span? |
| **VOLRUNG** | **pinned exactly** | the dial (LO / HI vol half) | the cap-free vol slope |

Every vol used to build or match a panel is measured on warm-up..2016-12-31 only (G6) — the
outcome being explained is OOS Sharpe. That requirement is also why the pools narrow to SMALL
478 (from 665) and BSTK 97 (from 100) and the width to k = 90 rather than 694's 100: a name first
priced after 2016 has no look-ahead-free vol to match on. The dropped names are the post-2016
listings, so the admission makes the SMALL pool **older**, which works *against* finding a
small-cap penalty.

## 1. The channel reproduces

| r (n) | rho(q, OOS Sharpe) | mean OOS Sharpe q=0 -> q=1 | span |
|---|---|---|---|
| 0.05 (4) | -0.6891 | 0.8159 -> 0.3617 | -0.4542 |
| 0.10 (9) | -0.6677 | 0.7697 -> 0.4778 | -0.2919 |
| 0.25 (22) | -0.9097 | 0.9390 -> 0.4677 | -0.4714 |
| 0.50 (45) | -0.9372 | 1.0645 -> 0.3529 | -0.7116 |
| **mean** | **CAP = -0.8009** | | **SPAN = -0.4823** |

694 committed -0.7709 and up to -0.853 on a different seed. G1 asserts sign and size before
anything is decomposed, not the exact figure.

## 2. The matched-vol control carries none of it

Over the same realised vol range (twins 0.276–0.434 vs the cap arm's 0.259–0.430), origin free:

| r | twin span, TOL 0.02 | TOL 0.05 | cap span | share reproduced |
|---|---|---|---|---|
| 0.05 | +0.0220 | -0.0393 | -0.4542 | -4.8% / +8.7% |
| 0.10 | +0.0672 | +0.1302 | -0.2919 | -23.0% / -44.6% |
| 0.25 | +0.0098 | +0.1419 | -0.4714 | -2.1% / -30.1% |
| 0.50 | -0.0377 | +0.0816 | -0.7116 | +5.3% / -11.5% |

**SURVIVAL = -0.1278.** Pooled rho(realised vol, OOS Sharpe) on the twin arm is **+0.1700**.
The twins' realised cap share runs 0.644–0.900 (mean 0.785) because the admissible pool is 83%
small caps — published, because it is exactly why this arm moves cap and vol *together* and
therefore lands flat. It cannot settle the question alone. VOLRUNG can.

## 3. At pinned cap mix, high vol WINS — 12 of 12

| q | mean name vol LO / HI | OOS Sharpe LO / HI (mean over r) | span |
|---|---|---|---|
| 0.50 | 0.239 / 0.441 | 0.2884 / 0.7875 | +0.4991 |
| 0.75 | 0.259 / 0.476 | 0.2159 / 0.7142 | +0.4983 |
| 1.00 | 0.279 / 0.535 | 0.0356 / 0.5387 | +0.5031 |

Positive at **12 of 12** (q, r) cells, +0.3233 .. +0.6783. The rho column reads +0.8729
identically everywhere because a two-level Spearman with 4+4 draws and perfect separation
saturates there; the span is the informative statistic and it is reported as such.

## 4. The pooled decomposition

On ARM CAP alone q and name vol are **+0.9694** collinear — stated in the script header before
any number was read, not discovered afterwards — so no partial can separate them there. Pooling
all three arms drops the collinearity to **+0.5715**:

| r | beta_q | beta_vol | R2 | partial rho q | partial rho vol |
|---|---|---|---|---|---|
| 0.05 | -0.4603 | +0.3973 | 0.161 | -0.3812 | +0.3353 |
| 0.10 | -0.5304 | +0.5142 | 0.234 | -0.4452 | +0.4342 |
| 0.25 | -0.7604 | +0.5024 | 0.394 | -0.6254 | +0.4680 |
| 0.50 | -0.8839 | +0.4477 | 0.529 | -0.7265 | +0.4721 |
| **mean** | **-0.6588** | **+0.4654** | | **-0.5446** | **+0.4274** |

**Cap is a penalty, vol is a premium, and they are positively correlated — so they partly cancel.
694's raw q ladder understates the pure cap penalty rather than overstating it.** The confound
the queue hypothesised is real and measurable, and it points the other way.

## The pre-registered bar

VOL STORY needed SURVIVAL >= 0.70 (got **-0.1278**) and |PARTIAL| < 0.30 (got **0.4756**) — fails
both. CAP STORY needed |PARTIAL| >= 0.30 (holds) and a flat vol slope at pinned cap mix, |rho|
<= 0.15 (got **+0.8729**) — fails the second. The script therefore calls **MIXED** and prints both
numbers rather than rounding to a verdict, which is the honest reading: **the cap channel is not
a vol channel, but vol is a large independent channel of its own, with the opposite sign.**

## Capital (rules 3, 4, 8)

| arm | 4a | 4b |
|---|---|---|
| CAP | 0 of 160 | 16 of 160 (all q <= 0.25) |
| VOLTWIN | 0 of 320 | **0 of 320** |
| VOLRUNG | 0 of 96 | 4 of 96 (q=0.50, HI vol) |
| **all** | **0 of 576** | **20 of 576** |

Rule 8 — (q, r) by argmax IS Sharpe on warm-up..2016-12-31, 2017–2026 read ONCE, run on all
three arms so the comparison is chooser-matched:

| arm | IS pick | OOS CAGR | OOS Sharpe | OOS MaxDD | beats SPY? |
|---|---|---|---|---|---|
| CAP | q=0.00, r=0.10 (n=9) | 12.24% | 0.7697 | -21.68% | no |
| VOLTWIN (TOL 0.02) | q=0.00, r=0.50 (n=45) | 4.10% | 0.4591 | -16.95% | no |
| VOLTWIN (TOL 0.05) | q=0.00, r=0.50 (n=45) | 3.45% | 0.3888 | -18.81% | no |

SPY OOS 15.26% / 0.8737 / -33.72%; RULES v2 OOS 8.45% / 1.1045 / -12.76%. **0 of 3 arms beat SPY
out of sample, so nothing here is a book.**

## Named follow-up (not filed)

The +0.50 OOS-Sharpe HIGH-minus-LOW name-vol premium at **pinned** cap mix, positive at 12 of 12
cells and roughly the same size at every cap mix from 50% to 100% small, is a channel the record
has priced only as a confound and never as a book. It is the obvious next idea and it is named
here rather than filed, so the next lane can take it without re-deriving it.

## Survivorship (rule 9)

BSTK is the current broad-minus-ETF constituent list; SMALL is a current sub-$2B screen carried
back to 2010 (the protocol-mandated `max_1d_move >= 1.0` drop happens inside `M276.small_panel`:
719 screened -> 665). Every absolute level is an upper bound. What this run reads is a contrast
between two ways of drawing the same k names from the same two pools on the same days — the bias
inflates both sides and cannot manufacture the contrast, but cannot cure it either.

Artifacts: `.books.csv` (576 books), `.panels.csv` (144 panels), `.pooled.csv`,
`.walkforward.csv`, `.summary.csv`, `.gates.csv`, `.log.txt`.
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py untouched.
