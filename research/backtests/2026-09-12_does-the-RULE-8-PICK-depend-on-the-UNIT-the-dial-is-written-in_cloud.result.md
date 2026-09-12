# Idea 590 — does-the-RULE-8-PICK-depend-on-the-UNIT-the-dial-is-written-in (cloud, 2026-09-12)

**ANSWERED = THE UNIT CHANGES THE BOOK BUT NOT USUALLY THE VERDICT — and the queue's premise is
NARROWED, not confirmed. Over 3 panels × 3 dials × 2 units × 9 rungs = 162 books: the ABS and REL
picks are materially different books in 8 of 9 cells (median 17.3% of NAV differs), but the
full-sample 4b verdict moves in only 1 of 9 (B136/VOLCAP — idea 320's flip, reproduced on a
different dial), and the OOS Sharpe gap between units clears the books' own calendar noise floor in
only 4 of 9. H_PROTO FAILS: on this evidence PROTOCOL 8 does not need to name the unit. It needs to
name something else — 15 of 18 rule-8 picks land on a GRID ENDPOINT, and the IS Sharpe ordering
barely survives into OOS (median Spearman 0.158, negative in 8 of 18 ladders). KILL for capital:
4a 0 / 4b 43 / BOTH 0 of 162 books.**

Script: `2026-09-12_does-the-RULE-8-PICK-depend-on-the-UNIT-the-dial-is-written-in_cloud.py`
Artefacts: `.ladders.csv .picks.csv .floors.csv .keeppaths.csv .console.txt`

## The three dials, each in two units (stated before any number)

| dial | ABS unit | REL unit |
|---|---|---|
| WIDTH | hold top **n** names (5…60) | hold top **c**-fraction of the eligible set (0.05…0.90) |
| VOLCAP | admit vol20 < **v** (0.20…0.80) | admit vol20 below the **q**-th cross-sectional percentile (0.10…1.00) |
| TREND | 200d band = **b**, same ±b% for every name (0.00…0.10) | band = **k** × the name's own daily sigma (0…4) |

Gross 0.75, weekly, 10 bps, 6-month-return ranking: all fixed, reported, never selected on.

## The picks, side by side (rule 8: IS Sharpe alone, OOS read once)

| panel | dial | ABS pick | REL pick | common currency ABS / REL | moved > 1 step | span overlap | book distance (L1/2 of NAV) | 4b verdict moved |
|---|---|---|---|---|---|---|---|---|
| U56 | WIDTH | n=5 | c=0.10 | 5.00 / 3.85 names | no | 0.88 | **0.173** | no |
| U56 | VOLCAP | v=0.80 | q=1.00 | 0.989 / 1.000 admitted | no | 0.46 | 0.008 | no |
| U56 | TREND | b=0.10 | k=4.0 | 0.690 / 0.714 days IN | **yes** | 0.17 | **0.137** | no |
| B136 | WIDTH | n=5 | c=0.10 | 5.00 / 9.33 names | no | 0.66 | **0.350** | no |
| B136 | VOLCAP | v=0.20 | q=1.00 | 0.507 / 1.000 admitted | **yes** | 0.55 | **0.370** | **YES** |
| B136 | TREND | b=0.10 | k=4.0 | 0.713 / 0.716 days IN | **yes** | 0.60 | **0.108** | no |
| SMALL | WIDTH | n=15 | c=0.90 | 15.0 / 257.4 names | **yes** | 0.19 | **0.697** | no |
| SMALL | VOLCAP | v=0.20 | q=0.10 | 0.197 / 0.128 admitted | no | 0.85 | **0.342** | no |
| SMALL | TREND | b=0.10 | k=4.0 | 0.562 / 0.554 days IN | **yes** | 0.52 | **0.084** | no |

The one verdict flip is **B136 / VOLCAP**: ABS picks v=0.20 and fails 4b on H2, OOS and CAGR (OOS
4.93% / 0.68 / −17.1%); REL picks q=1.00 and **passes 4b** (OOS 11.84% / 1.06 / −20.1%). The OOS
Sharpe gap is 0.3729 against that book's convention floor of 0.0651 — this one is **real**, not
calendar. It is the same panel and the same direction as idea 320's flip, on a different dial.

## The four pre-registered hypotheses: 1 of 4 PASS

| H | verdict | measured |
|---|---|---|
| H_MOVE | **FAIL** | the pick moves > one grid step in **5/9** cells (bar ≥ 6/9) |
| H_BOOK | **PASS** | the two picked books differ by ≥ 5% of NAV in **8/9** cells; median **0.173** (bar ≥ 6/9) |
| H_VERDICT | **FAIL** | the 4b verdict differs between units in **1/9** cells (bar ≥ 3/9) |
| H_OOS | **FAIL** | the OOS Sharpe gap clears the book's own convention floor in **4/9** cells; median gap 0.105 vs median floor 0.069 (bar ≥ 5/9) |
| H_PROTO | **FAIL** | decided by H_MOVE and H_VERDICT together — PROTOCOL 8 does not need to name the unit on this evidence |

**G4 convention floor** (max−min OOS Sharpe over the five weekday offsets of the same 5-trading-day
cadence) ranges 0.020–0.372 across the 18 picked books. Five of the nine unit gaps are smaller than
their own book's floor — i.e. they are the calendar, not the unit. Reading any of those five as a
unit effect would be an error the record has made before.

**G3 caveat, stated rather than buried.** The ABS and REL ladders do not always cover the same book
space: span overlap is 0.17 on U56/TREND and 0.19 on SMALL/WIDTH. In those cells a disagreement is
confounded with where each grid was stopped, and the disagreement is read with that caveat attached.

## What the run found instead (read off the published ladders, NOT pre-registered)

1. **15 of 18 rule-8 picks land on a grid ENDPOINT** — the first or the last rung of their own
   ladder (the three interior picks are U56/WIDTH/REL, B136/WIDTH/REL and SMALL/WIDTH/ABS). The
   "parameter chosen on the in-sample window" is in most cases being chosen by **where the author
   stopped the grid**, in either unit. That is a larger hole in rule 8 than the unit is, and it is
   invisible to a census that only reads the published value.
2. **The IS Sharpe ordering barely survives into OOS.** Median Spearman(IS rank, OOS rank) over the
   nine rungs of a ladder is **0.158**, and it is **negative in 8 of the 18 ladders**. The IS pick
   costs a median 0.023 of OOS Sharpe against the ladder's own best OOS rung, worst −0.59
   (B136/TREND/REL). Rule 8's selector is weak in both units, which is exactly why rewriting the
   unit moves the book so much and the verdict so little.
3. Both of these say the same thing: on these dials the IS window does not contain enough signal to
   locate an interior optimum, so the pick defaults to an endpoint and the unit mostly decides which
   endpoint you land on.

**Proposed PROTOCOL amendment (NOT applied — rule 6 reserves that for the Sunday review):** rule 8
should require that a reported pick be **interior to the swept grid**, and that the grid's endpoints
be published beside it. Naming the unit is the weaker of the two fixes on this evidence; requiring
interiority would have flagged 15 of these 18 picks.

## KEEP paths

Over all 162 books: **4a 0 | 4b 43 | BOTH 0.** No book beats live RULES v2 in both halves without a
worse drawdown, so 4a is empty by construction on these panels. The 43 4b passes are concentrated in
U56/TREND (17 of 18 rungs across both units) and B136/TREND (13 of 18) — i.e. in the dial whose two
units produce nearly the same book (L1/2 of 0.084–0.137), which is the opposite of a unit effect.
**No KEEP is claimed:** every 4b pass here is a full-sample read on a rung that was not itself
chosen out of sample, and the rule-8 picks that WERE chosen out of sample pass 4b in only 4 of the
18 ladders (U56/VOLCAP both units, U56/TREND both units).

## Caveats

**SURVIVORSHIP.** U56 and B136 are current constituents of `universe.json` / `universe_broad.json`;
SMALL is the current constituent list of its sub-$2B screen with the 52 tickers whose
`max_1d_move ≥ 1.0` dropped first (663 tradable). Dead names are absent from all three, so every
CAGR above is biased upward and every 4b CAGR-floor pass is easier than it would be on a
point-in-time panel. The bias is worst on SMALL, which is also the panel where the two units
disagree most about the book (L1/2 0.697 on WIDTH).

**Gates.** G1 fast_backtest vs engine.backtest max|Δ| = 1.4e-17 (bar 1e-9). G2 comparands printed
per panel. G3 span overlap published per cell. G4 convention floor published per picked book.

**PROTOCOL.** 10 bps per unit turnover, next-day fills, no shorting, no leverage, gross 0.75,
weekly. RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py untouched; the PROTOCOL amendment
above is a proposal for the Sunday review, not an edit.
