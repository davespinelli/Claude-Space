# Idea 976 (lane B, 2026-09-15) — should a 4b PASS be NON-CERTIFYING above a WITHIN-FAMILY PHASE PASS SHARE?

**ANSWERED = NO, AND THE PROPOSED BAR HAS ITS SIGN BACKWARDS / KILL for idea 964's
non-certifying clause.** Nothing promoted, no RULES change, no PROTOCOL edit applied (rule 6);
`RULES.md`, `PROTOCOL.md`, `scan.py`, `bot.py` and `baseline.py` untouched.

Script: `2026-09-15_should-a-4b-PASS-be-NON-CERTIFYING-above-a-WITHIN-FAMILY-PHASE-PASS-SHARE_B.py`
· runtime 794s · **GATES 8 of 8 PASS.**

---

## THE GRID

3 panels {U56 56, B136 136, SMALL 664} × 5 books {TOP05, TOP10, TOP20, EWELIG, BAND03} × 2 gross
{CORE 0.75, EXT 1.00} × 2 cadences {M 21 phases, Q 63 phases} × 5 cost rungs {0, 5, 10, 25, 50}
= **12,600 scored phase-book rows over 60 families**, plus **30,600 gross-matched coin-flip
book-scorings** (10 draws per family scored on *every* phase for the null's own share
distribution, 100 draws at the canonical phase for each family's 4b base rate), plus a
**84-artifact / 210,684-row census** of the record's committed M/Q 4b passes, plus **36 rule-8
picks**. Two tuned axes only — **BAR** {0.10, 0.25, 0.50, 0.75} and **CLAIM SET**
{STRICT, WIDE, GRID} — every one of the 12 grid points reported, none selected.

## THE ANSWER, IN ONE TABLE

The three families in the whole 60-family grid whose **canonical** phase clears 4b at 10 bps,
each with the cheap statistic (the phase-family share) beside the expensive one it is proposed
to stand in for (the family's own gross-matched coin-flip 4b base rate):

| family | share | null share | **null 4b base rate** | OOS CAGR / Sharpe / MaxDD | bar 0.25 says | the null says |
|---|---|---|---|---|---|---|
| U56 EWELIG CORE M | **0.810** (17/21) | 0.000 | **0.070** | 12.98% / 1.216 / −17.01% | **non-certifying** | a coin flip clears it 7% of the time — *a real pass* |
| U56 BAND03 EXT M | 0.476 (10/21) | 0.095 | 0.050 | 12.82% / 1.225 / −18.81% | **non-certifying** | 5% — *a real pass* |
| U56 TOP20 CORE M | 0.238 (5/21) | 0.762 | **0.800** | 16.67% / 1.283 / −19.51% | **certifying** | **a coin flip clears it 4 times in 5** |

**The bar condemns the two passes the record's own null clears, and clears the one the null
condemns.** The third row is not an obscure cell: it is the standing candidate's monthly cell,
and its 16.67% / 1.283 / −19.51% triple reproduces ideas 926 and 970's committed numbers exactly.
Over the three families where the question is live, Spearman(share, null base rate) is
**−0.5000** — the wrong sign, not merely a weak one.

## PRE-REGISTERED HYPOTHESES (bars fixed before any number was read)

| H | verdict | stat | bar | what |
|---|---|---|---|---|
| H_RELABEL | **FAIL** | +0.0899 | in (0.10, 0.90) | fraction of STRICT committed M/Q 4b passes re-labelled at bar 0.25 |
| H_PROXY | **FAIL** | +0.3668 | ≥ +0.50 | Spearman(family share, family's own gross-matched null 4b base rate), n = 60 |
| H_SEPAR | PASS | +0.4762 | ≥ +0.10 | median share \| canonical passes − median share \| canonical fails |
| H_NULLSHARE | **FAIL** | +0.0000 | ≥ +0.10 | median NULL within-family share − median REAL within-family share |
| H_CHOOSE | **FAIL** | −0.0478 | 4b count AND mean OOS Sharpe both up | rule-8 screen ON (0/18) vs OFF (0/18) |

**H_RELABEL — the clause is INERT at the bar it was proposed at, and the bar is doing all the
work.** At 0.25 it re-labels **9.0% of the 701 STRICT** committed M/Q 4b passes (16.7%
family-weighted; WIDE 8.3% / 15.0%), just under the pre-registered 10% floor. At **0.10** the same
clause re-labels **67.9%**. A threshold whose effect runs 0.679 → 0.090 between two adjacent
round numbers, and which was chosen from a **single** observation (964's 0.413), is a free
parameter, not a finding.

**H_SEPAR is the damning pass, not a supporting one.** The share *does* separate families whose
canonical passes (median 0.476) from those whose canonical fails (0.000, n = 57) — which is
exactly what makes it useless as a certifier. It is measuring **the cell**, not **the claim**:
"lots of phases in this family pass" and "this family's canonical passes" are close to the same
sentence. Paired with H_NULLSHARE below, the share is a cell-difficulty statistic wearing a
certification statistic's clothes.

**H_NULLSHARE — the statistic cannot tell a fluke from a rule.** A gross-matched coin flip's
phase family is **exactly as crowded with passes as a real book's**: median within-family share
0.000 vs 0.000, means REAL 0.058 vs NULL 0.045, and the null's share is **≥ the real book's in
0.783 of the 60 families**. Whatever the share is detecting, a coin flip has it too.

## THE MECHANISM, AND WHY THE SIGN IS BACKWARDS

A high within-family phase pass share means *the book still works when you rebalance on a
different day*. That is **phase robustness**, which is a virtue, not fluke-ness. The clause reads
it as a vice. The rule-8 screen makes the cost of that inversion concrete: screening on IS-only
family share ≤ 0.25 changes the pick in **4 of 18 cells**, and every one of them trades a
low-drawdown CORE-gross book for a concentrated EXT-gross one —

| cell | screen OFF | screen ON |
|---|---|---|
| U56 M C_ISLEGS | TOP10 CORE 17.24% / **1.097** / **−23.22%** | TOP05 EXT 20.50% / 0.832 / −34.61% |
| U56 Q C_ISLEGS | EWELIG CORE 11.53% / **1.034** / **−22.21%** | TOP05 EXT 11.94% / 0.550 / −38.48% |
| B136 M C_ISLEGS | TOP20 CORE 15.55% / 1.000 / **−26.11%** | TOP20 EXT 20.81% / 1.005 / −33.68% |
| B136 Q C_ISLEGS | EWELIG CORE 10.97% / **0.969** / **−24.44%** | TOP05 EXT 23.23% / 0.853 / −36.61% |

The screen throws away exactly the phase-robust books and keeps the fragile ones. Mean OOS
Sharpe falls **0.7527 → 0.7050**; mean OOS CAGR rises 14.05% → 15.23% **and mean drawdown gets
7–16 pp worse in every changed cell**. Adopting this clause would actively degrade selection.

## RULE 8 (required)

36 picks = 3 panels × 2 cadences × 3 IS-only choosers × 2 screens; (book, gross) chosen on
**2009–2016 alone**, 2017–2026 read once, all 36 live (the screen never empties the shelf).

**OOS 4b 0 of 18 screened and 0 of 18 unscreened. OOS 4a 0 of 18 and 0 of 18.** Full-sample 4a
over the whole 2,520-row 10 bps grid: **4**. Best OOS book in the run is B136 M TOP05 EXT at
35.17% / 1.152 / **−39.70%** — it fails 4b on `L4_DD` alone, against a cap of −20.23%. The DD cap
is the binding leg on **every one of the 36 picks**, and on 12 of them it is the *only* leg that
is not also failed.

Comparands, one shared set: **SPY OOS 15.27% / 0.8741 / −33.72%** (4b bars: OOS Sharpe > 0.874,
MaxDD ≥ −20.23%, OOS CAGR ≥ 10.59%). **RULES v2 (live)** full-sample Sharpe / MaxDD: U56 1.201 /
−12.05%, B136 1.099 / −12.24%, SMALL 0.664 / −13.89%.

## THE CENSUS (and a record defect it re-confirms)

**84** committed CSV artifacts carry both a `pass4b` column and a cadence column; **210,684** rows
scanned, **7,055** are a 4b PASS on M or Q. Mapping them onto families:

- **STRICT** (panel + book + gross all present and on-grid, canonical phase): **701 rows (9.9%)**, 9 distinct families
- **WIDE** (panel + book present, gross defaulted to CORE, any phase): **3,913 rows (55.5%)**, 16 families
- **UNMAPPABLE: 3,142 rows** — reported, not dropped. Missing `book` on **3,111** of them, missing `panel` on 894.

Key availability across the 84 artifacts: `panel` 78, `gross` 59, `book` **40**, `phase` **2**.
**44 of 84 artifacts do not say which book they scored**, which is why the strict census covers a
tenth of the record's M/Q passes rather than all of it. That is idea 979's missing-`unit`-column
defect, measured on a second corpus and with a second consequence.

Re-labelling at every bar (row-weighted / family-weighted, idea 973's clause):

| claim set | n rows | med share | bar 0.10 | bar 0.25 | bar 0.50 | bar 0.75 |
|---|---|---|---|---|---|---|
| STRICT | 701 | 0.190 | 0.679 / 0.417 | **0.090 / 0.167** | 0.044 / 0.083 | 0.044 / 0.083 |
| WIDE | 3,913 | 0.143 | 0.700 / 0.350 | 0.083 / 0.150 | 0.074 / 0.050 | 0.074 / 0.050 |
| GRID | 3 | 0.476 | 1.000 | 0.667 | 0.333 | 0.333 |

## THE GRID'S OWN SHAPE (reported, nothing fitted on it)

Only **3 of 60 families** have a canonical that clears 4b, and **all three are U56 monthly**;
B136 is 0 of 20 and SMALL **0 of 20**. **19 of 60** families have *any* phase that passes.
Median within-family share by cell: U56 M 0.095 (max 0.810) · U56 Q 0.016 (max 0.413) ·
B136 M 0.000 (max 0.286) · B136 Q 0.000 (max 0.111) · **SMALL M and Q 0.000 (max 0.000 — the
panel does not clear 4b on any book, any gross, any phase, either cadence).** Median share over
all 60 families is 0.000 at every one of the five cost rungs.

## GATES — 8 of 8 PASS, printed before any result number

- **G0** `offset_mask(·, per, 0)` ≡ `engine.rebalance_mask` on M/Q/W — **0** disagreeing rows
- **G1** fast `Ctx` runner ≡ `engine.backtest` post-warm-up — dret **1.21e-17**, dturn **2.78e-16**
- **G2** `BAND03@0.75` ≡ `baseline.rules_v2_weights` elementwise — **0.000e+00**
- **G3 CROSS-RUN** — idea 964's committed `.grid.csv` reproduced on **all 12,600 of 12,600 rows**,
  max\|d\| **1.776e-15** (on `turn_per_yr`), **0** 4b-verdict disagreements
- **G4** idea 964's published headline — U56/Q/EWELIG/CORE @ 10 bps **26 of 63 = 0.413**, exact
- **G5** null gross match — holding count and per-name weight ≡ the book's on every rebalance row
  of all **2,520** families, **0.000e+00**
- **G6** determinism — subject family rebuilt from scratch, **0.000e+00**
- **G7** every chooser IS-only — **0** disagreements under permuted OOS columns

## SURVIVORSHIP (rule 9)

U56, B136 and SMALL are **current-constituent** lists (SMALL additionally drops the 52 tickers
with `max_1d_move` ≥ 1.0 per `data/small_meta.csv`), so every CAGR and drawdown **level** above is
optimistic and both 4b bars are easier here than on a point-in-time panel. The within-family
share contrasts are the **same names on the same tape under different rebalance days** and are
very nearly immune to it. A coin flip drawn from a survivor panel is a *better* book than one
drawn in real time, so **every null share and base rate above is an UPPER bound** — which cuts
**against** this run's own power hypothesis rather than for it: the true null shares are lower,
and H_NULLSHARE would fail by more, not less. The rule-8 4b levels are read against SPY, which is
not survivorship-inflated, so every 4b PASS is an upper bound and every FAIL is understated.

## WHAT IS PROPOSED (nothing applied — rule 6)

The clause is **rejected, not amended**. A bar in the other direction is *not* proposed either:
H_NULLSHARE shows a coin flip's family is as crowded as a real book's, so the statistic carries no
certification information in either direction, and reversing an uninformative statistic buys
nothing. What the record should keep doing is what idea 942/926 already do — publish the cell's
own gross-matched null base rate beside the pass. This run's own headline is the argument: the
cheap statistic and the expensive one disagree on **2 of the 3** passes that matter.

Follow-ups filed: **980** (is a high within-family phase share a positive robustness signal worth
publishing in its own right), **981** (the DD cap is the binding leg on 36 of 36 rule-8 picks —
is 4b a drawdown test on every panel, not just the quarterly grid 968 asked about), **982**
(44 of 84 committed artifacts carry no `book` column — cost the schema fix on this corpus).
