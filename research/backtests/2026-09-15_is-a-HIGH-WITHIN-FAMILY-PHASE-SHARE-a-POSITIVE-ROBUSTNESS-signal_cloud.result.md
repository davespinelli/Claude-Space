# Idea 980 (cloud, sprint of 2026-09-15, finished 2026-09-16) — is a HIGH WITHIN-FAMILY PHASE SHARE a POSITIVE robustness signal worth PUBLISHING?

**ANSWER = YES AS A DRAWDOWN SIGNAL, NO AS A 4b/4a GENERATOR. PARK, not KEEP.** The legal
IS-only share (`S_IS4B`) used as a positive floor improves median OOS MaxDD by **+0.108 to
+0.133** and median OOS Sharpe by **+0.043 to +0.148** against a **cell-matched** unscreened
control, at **every** floor that leaves the grid non-empty, and beats **0.958–0.998** of
size-matched random screens on drawdown. But it yields an OOS 4b pass at only **2 of 6** floors
and **never** an OOS 4a — 0 of 18 at every one of the 18 (floor × basis) points. **KEEP is
refused on both paths.** Separately, **964's non-certifying bar is confirmed sign-backwards:**
the positive screen moves rule-8 picks *to* CORE 5–8 times against 0–2 *to* EXT, the exact
mirror of what 976 found the negative bar did. Nothing promoted; `RULES.md`, `PROTOCOL.md`,
`scan.py`, `bot.py`, `baseline.py` untouched.

## The grid and the legality problem

The ladder ideas 976 / 981 / 984 / 986 built: 3 panels × 5 books × 2 gross × D/W/M/Q at
**matched gross** × every phase (1/5/21/63) = **2,700 phase-books** × 5 cost rungs = **13,500
rows**. A FAMILY is one (panel, book, gross, cadence); the idea's **60-family grid is the M/Q
half** and is the pre-declared headline, with D/W published beside it.

**A within-family share computed on the full sample reads the 2017–2026 tape and is therefore
not a legal rule-8 screen** — nobody standing at 2016-12-31 can compute it. So the share is
built three ways and all three are reported: `S_IS4B` (phases passing 4b on **2009–2016
alone** — LEGAL), `S_ISLEG4` (phases with ≥ 4 of 5 IS legs — a softer legal form), `S_FULL4B`
(phases passing 4b on the full sample — the **LEAKY control**, run so the leak can be priced,
not used). Two tuned axes only — floor {0.00, 0.10, 0.25, 0.40, 0.50, 0.75, 0.90} × basis —
**all 21 points reported, none selected**.

## What the screen does, MQ60, 10 bps

| basis | floor | slots filled | OOS 4b | OOS 4a | med OOS Sharpe | med OOS MaxDD | to CORE / to EXT |
|---|---|---|---|---|---|---|---|
| — (unscreened control) | 0.00 | 18/18 | **0** | **0** | 0.8312 | **−34.14%** | — |
| `S_IS4B` | 0.10 | 12/18 | 0 | 0 | 1.0166 | −23.83% | 8 / 0 |
| `S_IS4B` | 0.25 | 12/18 | 0 | 0 | 1.0166 | −23.83% | 8 / 0 |
| `S_IS4B` | **0.40** | 12/18 | **3** | 0 | **1.0590** | **−21.35%** | 5 / 2 |
| `S_IS4B` | 0.50 | 12/18 | **3** | 0 | **1.0590** | **−21.35%** | 5 / 2 |
| `S_IS4B` | 0.75 | 6/18 | 0 | 0 | 1.0274 | −22.47% | 2 / 1 |
| `S_IS4B` | 0.90 | 0/18 | 0 | 0 | — | — | — |
| `S_ISLEG4` | any | 18/18 → 9/18 | 0–1 | 0 | 0.71–0.97 | −29.9…−34.6% | ≤ 4 / ≤ 2 |
| `S_FULL4B` (LEAKY) | 0.25–0.75 | 9/18 → 3/18 | 3 | 0 | 1.085–1.215 | −20.5…−17.0% | ≤ 2 / ≤ 2 |

## The two controls that decide it

**1. Cell-matched control (the panel trap).** At floor 0.40 the screen empties the whole SMALL
panel — 6 of 18 slots — so a raw comparison against the 18-slot control partly measures *which
panels survived*, not which books. Re-running the unscreened control on **exactly the cells the
screen left non-empty**: median OOS Sharpe 0.9111 → 1.0590 (**+0.1479**) and median OOS MaxDD
−34.61% → −21.35% (**+0.1326**). The gain survives, and it survives at all five S_IS4B floors
that fill slots (ΔSharpe +0.105 / +0.105 / +0.148 / +0.148 / +0.043; ΔMaxDD +0.108 / +0.108 /
+0.133 / +0.133 / +0.127). **It is a book effect, not a panel effect.**

**2. Size-matched random-screen null (the shrinkage trap).** A floor does two things at once —
it selects on the share AND it shrinks the candidate set, and shrinking alone helps if the
books it happens to drop are bad. The null keeps, in every (panel, cadence) cell, the **same
number** of candidates the real screen kept, drawn uniformly at random, **2,000 draws, seed
980**. On drawdown the share beats **0.998 / 0.993 / 0.995 / 0.989 / 0.958** of draws across
the five live floors, and on Sharpe **0.912 / 0.867 / 0.951 / 0.953 / 0.985**. **The share
carries real information.** On the OOS 4b COUNT it does not: 0.958 and 0.954 at floors 0.40 and
0.50 (barely over the 0.95 bar), and **0.28 / 0.30 / 0.50** at floors 0.10, 0.25 and 0.75 —
below chance. The 4b passes are a knife-edge of the floor, not a property of the screen.

## Why this is PARK and not KEEP

- **OOS 4a: 0 of 18 at every one of the 21 grid points.** Path 4a is refused outright.
- **OOS 4b: 2 of 6 floors**, and the null cannot distinguish those two from chance at any
  comfortable margin. H_CONSIST FAILS (2 of 6). A screen whose headline depends on landing
  between 0.40 and 0.50 is a tuned parameter wearing a result's clothes.
- **It costs a third of the grid.** 6 of 18 slots empty at floor 0.40, 12 of 18 at 0.75, 18 of
  18 at 0.90. A rule that declines to pick is not the same as a rule that picks better, and the
  record should never score the two the same way.
- The 3 passing SLOTS at floors 0.40/0.50 are only **two distinct books**, both U56/M and both
  already in the record: **`TOP20`@0.75 16.68% / 1.283 / −19.51%** (chooser C_CAGR) and
  **`BAND03`@1.00 12.81% / 1.225 / −18.81%** (choosers C_SHARPE and C_ISLEGS). No new book.

## The leak, priced

The LEAKY `S_FULL4B` reaches the **same** best OOS 4b count as the legal `S_IS4B` (3 and 3), so
**the share's value is not the leak** — H_LEGAL PASS. What the leak buys is concentration: it
empties 15 of 18 slots at floor 0.50 to get there, against the legal basis's 6. That is worth
recording: a full-sample share looks stronger only because it is allowed to throw more away.

## Rule 8 and the comparands

The whole experiment is a rule-8 walk-forward: (book, gross) chosen on **2009–2016 alone**,
2017–2026 read once, 3 panels × 4 cadences × 3 IS-only choosers. The floor-0 control reproduces
idea 986's committed 36 picks book-for-book (G3b). Comparands: **SPY OOS 15.21% / 0.8713 /
−33.72%** (full-sample MaxDD); RULES v2 (live) full-sample Sharpe / MaxDD **U56 1.2009 /
−12.05%**, **B136 1.0994 / −12.24%**, **SMALL 0.6637 / −13.89%**. Across the whole run — any
floor, any basis, any cadence — the OOS 4b passers are six objects and **all six are U56**:
D/W `BAND03`@1.00 (12.45% / 1.287 / −14.77% and 12.67% / 1.276 / −15.91%), W `TOP20`@0.75
(14.26% / 1.162 / −18.31%), and the three M/Q books above. **None passes 4a.**

## Gates — 9 of 9 PASS, printed before any result number

G0 `offset_mask(·,per,0)` ≡ `engine.rebalance_mask` on D/W/M/Q, 0 rows. G1 fast `Ctx` ≡
`engine.backtest` on returns AND turnover, D and M, max|d| **2.498e-16**. G2 `BAND03@0.75` ≡
`baseline.rules_v2_weights` **0.000e+00**. **G3a CROSS-RUN: idea 986's committed 13,500-row
ladder reproduced on 13,500 of 13,500 rows over 34 shared numeric columns, max|d| 7.105e-15.**
**G3b CROSS-RUN: 986's 36 unscreened rule-8 picks reproduced book-for-book and gross-for-gross,
0 disagreements.** G4 matched gross (30 target matrices built once, reused across all four
cadences). G5 determinism 0.000e+00. **G6a IS-PURITY: every LEGAL share and every screened pick
is invariant under permuted OOS columns, 0 disagreements** — the legality claim is demonstrated,
not asserted. G6b the leaky basis is declared and excluded from every verdict.

## Survivorship (rule 9)

U56 / B136 / SMALL are current-constituent lists (SMALL additionally drops the 52 tickers with
`max_1d_move` >= 1.0 per `data/small_meta.csv`), so every CAGR and drawdown LEVEL is optimistic
and **every 4b pass count here — screened and unscreened alike — is an UPPER bound.** A screen
that buys no 4a on optimistic data buys none on honest data. The drawdown *improvement* is a
difference between two selections from the same ladder and is far more robust than the levels.
One caveat with teeth: the screen's biggest single act is dropping SMALL, the panel whose
survivorship bias is largest, so the cell-matched control above is the only comparison in this
run that is not partly a bias artefact — and it is the one the verdict rests on.

## Limits, stated

The "best legal point" is chosen on OOS 4b count, which is a scan over 12 legal points against
an OOS tape read once — hence the null and the consistency test, and hence PARK. Floors are a
tuned axis; 0.40 and 0.50 give identical picks because no family's share falls between them.
`S_ISLEG4` is reported and does essentially nothing (ΔSharpe 0.0000 at four of six floors),
which localises the effect to the 4b-based share specifically.

## Follow-ups filed

992 (does the S_IS4B floor still beat its cell-matched control on D/W, where 986 showed the
binding leg changes?), 993 (price the emptied-slot cost: is "decline to pick" better than the
unscreened pick, on a grid where declining is scored), 994 (964's bar is sign-backwards —
propose the reporting clause in exact PROTOCOL wording).
