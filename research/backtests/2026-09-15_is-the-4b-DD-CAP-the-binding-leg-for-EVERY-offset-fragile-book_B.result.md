# Idea 944 — is the 4b DD CAP the binding leg for EVERY offset-fragile book in the record?

**lane B, 2026-09-15 · script `2026-09-15_is-the-4b-DD-CAP-the-binding-leg-for-EVERY-offset-fragile-book_B.py` · 10 bps, next-day execution (PROTOCOL rules 1–3) · gates 8 of 8 PASS**

## ANSWERED — NO. **KILL** for "the DD cap is the binding leg of 4b" as a fact about the record.

Idea 938 found all **18 of 25** failing monthly offsets of U56/TOP20 fail on **L4_DD alone**, never on a
Sharpe leg. This run re-derived that exactly (G3: 18 of 25, all DD-alone, DOM MaxDD support
−22.95%…−14.89% = 8.06 pp, DOM CAGR spread 1.95 pp — the published numbers to the digit) and then asked
whether it generalises. It does not.

**Two different questions were separated, and they have opposite answers:**

| question | answer |
|---|---|
| Which leg **binds** when a 4b book fails? | **the CAGR floor**, not the DD cap (68.8% vs 58.3% of the record's FAIL rows) |
| Which leg is a **coin flip on the rebalance date**? | **the DD cap** — flip rate 0.67 against 0.00–0.56 for the others |

938's result is a property of **TOP20 at gross 0.75 on U56** — a book whose Sharpe legs sit comfortably
clear of SPY and whose drawdown sits right on the cap — not a property of PROTOCOL 4b.

## The bars, scored mechanically (pre-registered before any number was read)

| bar | value | verdict |
|---|---|---|
| **B1 CENSUS-AMONG** DD among the binding legs in ≥ 90% of committed 4b FAIL rows (row- *and* file-weighted) | **58.3%** rows / **60.9%** files; **CAGR is the largest at 68.8%** | **FAIL** |
| **B2 CENSUS-ALONE** DD alone is the modal binding set, share ≥ 50% | DD alone **15.1%**; modal set is **`H1,H2,OOS,DD,CAGR`** at **25.3%**; CAGR-alone **16.9%** beats DD-alone | **FAIL** |
| **B3 PRICE-EVERY** DD binds at every failing phase in ≥ 90% of offset-fragile U56 cells | **5 of 6 (83.3%)** — `TOP40_g075` fails on `CAGR` with no DD at 5 of its 14 failing phases | **FAIL** |
| **B4 FLIP-RANK** DD's phase flip rate strictly highest of the five legs | H1 **0.00** · H2 **0.56** · OOS **0.28** · **DD 0.67** · CAGR **0.11** | **PASS** |
| **B5 SENS-RANK** MaxDD is the most phase-sensitive of the five statistics in ≥ 80% of cells | **83.3%** (15 of 18; the other 3 are H2, all on TOP05/TOP10 concentrated books) | **PASS** (reported separately, moves no mechanism verdict) |

**MECHANISM: H_MIXED** (H_DDBINDS required B1+B2+B3+B4).

## The census — 816,550 committed 4b FAIL cells over 472 files

Every `fail4b`-style column in every committed CSV under `research/backtests`, with the record's many
spellings (`H1,H2,OOS,DD,CAGR` · `H1+H2+…` · `H1|H2|…` · `L4_DD` · `DDCAP` · `CAGRFLOOR` · …) normalised
onto the five canonical legs. **G7 coverage 0.9998**; the 181 unmappable cells are listed in the console,
not dropped.

| leg | among (rows) | among (files) | alone (rows) | alone (files) |
|---|---|---|---|---|
| H1 | 0.516 | 0.439 | 0.009 | 0.020 |
| H2 | 0.578 | 0.529 | 0.003 | 0.017 |
| OOS | 0.537 | 0.465 | 0.000 | 0.000 |
| **DD** | **0.583** | **0.609** | **0.151** | **0.193** |
| **CAGR** | **0.688** | **0.615** | **0.169** | **0.196** |

Row- and file-weighting agree, so the answer is not one giant sweep speaking for the record. **No leg is
near-universal.** The modal failure is *all five at once* (25.3%) — i.e. the record's typical 4b failure is
a book that simply does not beat SPY, not a book tripped by one bar.

## The price leg — 9 books × 30 phases × 2 panels @ 10 bps (540 grid points, all reported)

Books: TOP05/TOP10/TOP20/TOP40 at gross 0.75, TOP20 at 1.00, BAND03 at 0.75 and 1.00, BAND06 at 0.75,
RULES v2. Phases: DOM 0–20 (d = 0 **is** the canonical month-end, G0 bit-identical to
`engine.rebalance_mask`), 4W 0–3, DOW 0–4. **G4**: every DOM offset trades 12.02–12.08×/yr.

`TOP40_g075` is the counterexample that kills B3: of its 14 failing DOM phases, **8** bind on `DD,CAGR`,
**5** on `CAGR` alone and **1** on `DD` alone. On `BAND03_g075`, `BAND06_g075` and `RULESV2` the verdict
never flips at all — they fail on the **CAGR floor at all 21 phases**, and their drawdowns are nowhere near
the cap. The DD cap only gets to be "the" binding leg on books that already clear the CAGR floor.

**Phase sensitivity** (normalised spread (max−min)/|median| over the 21 DOM phases, U56): MaxDD
0.276–0.470 against CAGR 0.066–0.229, Sharpe 0.068–0.204, H1 0.064–0.291, H2 0.122–0.378. MaxDD is the
most phase-sensitive statistic on **15 of 18** cells — **B5 confirms 938's second finding** even as B1–B3
kill its first. So the honest reading is: *the DD cap is not the bar that rejects most books, but it is the
bar most likely to change its mind when you move the rebalance date.*

## PROTOCOL rule 8 — walk-forward (phase AND book chosen on 2009–2016 only, 2017–2026 read once)

| chooser | book / phase | IS Sharpe | OOS CAGR | OOS Sharpe | OOS MaxDD | OOS rank | 4b | 4a |
|---|---|---|---|---|---|---|---|---|
| CH_IS_SHARPE_ANY / CH_IS_CAGR_ANY | TOP05_g075 / DOM01 | 1.326 | 19.04% | **0.988** | −25.22% | **257/270** | n | n |
| CH_IS_MINDD_ANY | RULESV2 / DOM19 | 1.102 | 9.73% | 1.234 | −13.60% | 56/270 | n | n |
| CH_CANON_TOP20 (not IS-chosen) | TOP20_g075 / DOM00 | 1.098 | 16.67% | 1.283 | −19.51% | 17/270 | Y | n |
| CH_CANON_RULESV2_W (the live book) | RULESV2 / DOW0 | 1.105 | 9.46% | 1.277 | −12.05% | 20/270 | n | n |
| **SPY (OOS)** | — | — | **15.27%** | **0.874** | — | — | — | — |
| **RULES v2 baseline (OOS)** | — | — | **9.46%** | **1.277** | **−12.05%** | — | — | — |

The IS-Sharpe pick lands at **rank 257 of 270** out of sample — picking the phase in sample is actively
harmful, which is the same lesson 938 drew on one book, now on nine. The phase-blind investor
(`MEAN_DOM_*`, mean over all 21 phases) does better than the IS-chosen point on every book.

**Both KEEP paths evaluated (PROTOCOL rule 4).** **4a: 0 of 540** grid points — no book on any phase beats
RULES v2 in both halves while matching its −12.05% MaxDD. **4b: 64 of 540** points pass on the full
sample (**48 of 270** on the binding U56 panel), but the only IS-blind ways to reach one are the canonical month-end (a free parameter nobody
tuned) or an average over phases, and **no IS-chosen point passes 4b**. **Nothing is a KEEP candidate;
nothing is promoted.** No RULES change, no PROTOCOL edit, no version bump (rule 6); `RULES.md`, `scan.py`,
`bot.py`, `baseline.py` untouched.

## GATES — 8 of 8 PASS

G0 `offset_mask(·,per,0)` ≡ `engine.rebalance_mask` on M and W, **0 differing rows** · G1 fast runner ≡
`engine.backtest` @10 bps, worse of W/M **1.214e-17** · G2 `band_book(0.03,0.75)` ≡ `rules_v2_weights`
**0.0** · **G3** idea 938's committed headline re-derived from this file's code path: 18 of 25 monthly
phases FAIL, 18 DD-alone; MaxDD support −22.95%…−14.89% (8.06 pp); CAGR spread 1.95 pp · G4 phase
fairness, 0 violations · G5 determinism **0.0** · G6 `baseline.compare()` ≡ fast runner **1.353e-04** ·
G7 census coverage **0.9998**.

## SURVIVORSHIP (PROTOCOL 9)

`universe.json` (U56) and `universe_broad.json` (B136) are **current-constituent** lists, so every CAGR,
Sharpe and drawdown **level** above is optimistic and none is a capital claim on its own. Direction for
this run: the phase contrasts and binding-leg tallies are **same-tape, same-names, same-weights**
comparisons that differ only in *which day* the identical book trades, so panel composition does not touch
them. The 4b levels are read against SPY, which is not survivorship-inflated — a survivor panel makes books
look **better** and therefore makes 4b failures **rarer**, which cuts *against* this run finding a
near-universal binding leg, not for it. The census is a census of the record's **text**, and inherits
whatever biases its source runs carried.

## What the record should do with this

The reporting line 938 implied — "4b is really a DD bar" — is **wrong as written**. The two defensible
lines are separate and both belong on a 4b row:
1. **the binding leg**, named (the record's modal binder is the **CAGR floor**, not the DD cap); and
2. **the DD cap's phase flip**, because it is the one leg whose verdict is a coin flip on a parameter
   nobody tuned — 6 of 9 U56 books change their 4b answer on the rebalance date alone.

Follow-ups filed: **954** (should every 4b row name its binding leg and its phase flip), **955** (is the
CAGR floor the record's real gatekeeper — the 68.8% leg — and is it a beta bar in disguise), **956** (does
a phase-AVERAGED 4b verdict, rather than a canonical-date one, change which books in the record pass).
Numbers 951–953 went to the **cloud lane**, which claimed and ran this SAME idea in the same hour on a
different grid (6 books × 3 panels × 26 phases × 4 rungs) and pushed first. **Its verdicts agree with this
run's on both counts**: the plurality of failing rows binds on *all five legs at once* (30.4% there, 25.3%
here) so DD is not the universal binder, and DD is the most phase-fragile leg (flip rate 36.1% there on a
26-phase family, 67% here on 21 DOM phases over 18 cells). Two independent code paths, same two answers.
