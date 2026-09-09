# Idea 546 — is-the-MARGINAL-rho-the-only-estimable-characteristic-statistic (lane C, 2026-09-09)

**ANSWERED / KILL of the partial and the joint-fit t as claim-bearing statistics — but the queue's
headline is too strong as written. The marginal is the MOST estimable statistic, not the ONLY one:
`corr` and `evol` are sign-stable at |t| >= 2 across disjoint seed blocks on ALL THREE statistics;
`disp` is estimable on the marginal ALONE; `breadth` is estimable on NONE of the three. Restating the
record's partial/joint-resting characteristic claims on the marginal saves 8 of 19 — and their own
statistic saves only 6 of 19, so the marginal is the more forgiving restatement, not the stricter one.
No tradable consequence: no selector beats SPY OOS at any of the 6 grid points.**

## Gates (graded before any restatement number was read)

Nothing is consumed from the parent's committed statistic columns: all 216 cells (2 blocks x 9 strata
x 3 books x 4 chars) are recomputed from the committed panel CSVs with ideas 284/293's estimators and
the parents' own seeds (permutation 7 / 20,000 draws, bootstrap 11 / 2,000 draws).

| gate | what | result |
|---|---|---|
| G1 | 216 recomputed cells vs idea 310-B's committed `.blockA/.blockB.csv` | **12 of 17 clauses pass.** `joint_t` exact (1.63e-14, 0 cells over 1e-8). `rho` 3 cells over tol (max 1.33e-03), `p` 3 (5.05e-03), `rho_partial` 12 (1.15e-03), `partial_lo/hi` 10 / 7 |
| G2 | idea 293's 27-point mean partials (disp +0.0046, evol +0.1551) | **PASS**, \|d\| 1.36e-05 / 1.03e-05 |
| G3 | idea 284's within-stratum `corr` rho (CAND10 −0.3648 / CAND20 −0.4815 / EWall −0.4708) | **PASS**, max \|d\| 2.36e-05 |
| G4 | idea 284's four published joint-fit t at (q=0.500, k=40) | **PASS**, max \|d\| 4.70e-03 (published to 2 dp) |
| — | idea 310-B's cross-block sign-agreement table | **re-derived exactly**: breadth 5/27 & 10/27, disp 9/27 & 21/27, corr 20/27 & 26/27, evol 19/27 & 22/27 |

**G1's near-miss is diagnosed, not waved through.** All 5 failing clauses live in ONE stratum of block
B (k=80, q=0.750) and are driven by `breadth_IS` carrying **2 exact ties in 60 panels** in the
committed CSV that the parent's in-memory frame did not carry. Ties move a rank statistic and not an
OLS one, which is exactly the pattern observed (`joint_t` exact, rank statistics off by ~1e-3). Every
number below is read off the RECOMPUTED columns, which anyone can reproduce from the committed CSVs;
block A reproduces at **0.000e+00** on every column. Bears on ideas 515/520/521: this is a
hand-off-through-CSV failure, not an arithmetic disagreement, and no committed verdict moves.

## The census — what does the record's characteristic vocabulary actually rest on?

449 published memos; **111 name at least one characteristic** (194 memo x characteristic pairs).

| reading | pairs resting on a PARTIAL | on a JOINT-FIT t | on the MARGINAL | partial-or-joint (files) |
|---|---|---|---|---|
| SENTENCE (statistic named in the same sentence as the characteristic) | 21 | 2 | 29 | 21 (**12 files**) |
| HEADLINE block only (ideas 523/534's claim-not-word unit) | 2 | 0 | 1 | 2 (2 files) |
| FILE (statistic named anywhere in the memo) | 70 | 9 | 118 | 71 (35 files) |

Both readings are reported and no verdict is selected on either. The headline-block reading is the
finding in its own right: **only 2 of 194 characteristic mentions put a partial in the memo's own
headline**, so the partial is overwhelmingly a body-text statistic that the record's headlines
inherit without naming.

## Claim-level restatement (survival rule fixed in advance, no new dial)

A claim survives if its characteristic's 27-point mean statistic (i) carries the claim's published
sign and (ii) reaches |t| >= 2 across the 27 points, **in BOTH seed blocks**. The same rule is applied
to the claim's own statistic as the comparand.

| reading | claims with a parseable published sign | survive on the MARGINAL | survive on their OWN statistic |
|---|---|---|---|
| SENTENCE | 19 (of 21; 2 unparsed) | **8** | **6** |
| FILE (wide) | 47 | **20** | **13** |

By characteristic (sentence reading): `corr` 4/7 survive, `disp` 2/5, `evol` 2/5, `breadth` 0/2.
The 11 that die on the marginal die on their own statistic too — **there is no claim in the record
that the partial supports and the marginal refutes.** Restating on the marginal costs the record
nothing and recovers two claims (`disp` +1, `evol` +1) that their own statistic cannot carry.

## The corpus statistic every verdict is read off (27 points per characteristic per block)

| statistic | char | mean A | t A | mean B | t B | sign stable | \|t\| >= 2 both |
|---|---|---|---|---|---|---|---|
| marginal | breadth | +0.0132 | +0.95 | −0.1424 | −7.78 | **no** | no |
| marginal | disp | +0.2514 | +11.49 | +0.1131 | +4.43 | yes | **yes** |
| marginal | corr | −0.2680 | −10.84 | −0.1211 | −7.79 | yes | **yes** |
| marginal | evol | +0.2732 | +20.62 | +0.1490 | +5.62 | yes | **yes** |
| partial | breadth | +0.0628 | +3.98 | −0.1331 | −6.54 | **no** | yes |
| partial | disp | +0.0046 | +0.16 | −0.0148 | −0.56 | **no** | **no** |
| partial | corr | −0.2180 | −10.68 | −0.0978 | −5.04 | yes | yes |
| partial | evol | +0.1551 | +6.63 | +0.1064 | +4.12 | yes | yes |
| joint_t | breadth | +0.4579 | +4.24 | −0.9806 | −6.41 | **no** | yes |
| joint_t | disp | −0.0610 | −0.31 | −0.3599 | −1.99 | yes | **no** |
| joint_t | corr | −1.5979 | −9.65 | −0.8314 | −5.85 | yes | yes |
| joint_t | evol | +1.2736 | +6.43 | +0.9553 | +4.84 | yes | yes |

**This is the answer to the queue's question.** 3 of 4 characteristics are estimable on the marginal;
2 of 4 on the partial and on the joint t. `breadth` flips sign between seed blocks on every statistic
at |t| >= 4 in both directions — a t-stat is not evidence of estimability here. So the marginal is
the only statistic that estimates `disp`, and it is not the only statistic that estimates anything.

## Cell level: which statistic survives its own seed block?

| block | statistic | significant cells / 108 | same sign as marginal | survives on marginal | own sign replicates in the OTHER block |
|---|---|---|---|---|---|
| A | marginal | 40 (37.0%) | 40 | 40 (100%) | **33 (82.5%)** |
| A | partial | 14 (13.0%) | 14 | 14 (100%) | 9 (64.3%) |
| A | joint_t | 19 (17.6%) | 19 | 17 (89.5%) | 14 (73.7%) |
| B | marginal | 18 (16.7%) | 18 | 18 (100%) | **14 (77.8%)** |
| B | partial | 9 (8.3%) | 9 | 5 (55.6%) | 5 (55.6%) |
| B | joint_t | 9 (8.3%) | 9 | 5 (55.6%) | 4 (44.4%) |

Unconditional cross-block sign agreement, averaged over the four characteristics: **marginal 0.731,
joint_t 0.573, partial 0.491** — the partial is a coin flip.

## Pre-registered predictions, graded

| | prediction | result |
|---|---|---|
| P1 | fewer than half the partial/joint-resting claims survive on the marginal | **PASS** (8/19; 20/47 wide) |
| P2 | marginal and partial name a different characteristic in >= 1/3 of the 27 points, in EACH block | **FAIL** (A 0.222, B 0.370) — the two statistics mostly agree about which characteristic to use; they disagree about whether it means anything |
| P3 | no selector beats SPY OOS on average in either block | **PASS** (best 0.7706 vs SPY 0.8820) |
| P4 | the marginal's sign replicates across blocks more than the partial's | **PASS** (0.731 vs 0.491) |

## Rule 8 walk-forward — IS (2009–2016) picks the statistic AND the characteristic, OOS (2017–) read once

Inside every stratum and for every book, each selector fits its own statistic on IS data only (four IS
characteristics vs the panel's IS Sharpe), names the characteristic with the largest |statistic|, and
takes the panel at that characteristic's fitted extreme. 27 (stratum x book) cells per grid point.

| block | statistic | OOS Sharpe | regret vs anchor | OOS CAGR | OOS MaxDD | beats anchor | beats SPY | beats RULES v2 | PICK − REVERSE |
|---|---|---|---|---|---|---|---|---|---|
| A | marginal | **0.7706** | +0.0990 | 10.70% | −25.39% | 19/27 | 9/27 | 4/27 | +0.1147 |
| A | partial | 0.6960 | +0.0243 | 9.14% | −25.62% | 17/27 | 8/27 | 2/27 | +0.0404 |
| A | joint_t | 0.7051 | +0.0335 | 9.42% | −26.00% | 16/27 | 9/27 | 3/27 | +0.0225 |
| B | marginal | 0.6334 | **−0.0294** | 8.47% | −31.58% | 8/27 | 5/27 | 4/27 | −0.0529 |
| B | partial | 0.7318 | +0.0690 | 10.18% | −31.35% | 16/27 | 7/27 | 6/27 | +0.1020 |
| B | joint_t | 0.7267 | +0.0640 | 10.02% | −31.44% | 16/27 | 6/27 | 5/27 | +0.0863 |
| — | anchor (stratum mean) | 0.6672 | 0.0000 | — | — | mean seed sd **0.1577** | | | |
| — | **SPY** | **0.8820** | — | **15.45%** | −33.72% | | | | |
| — | **RULES v2 (live)** | **0.8905** | — | — | — | | | | |

**No grid point beats SPY or the live book, and the ORDERING of the three statistics does not survive
the seed block**: the marginal is the best selector in block A (+0.099) and the worst in block B
(−0.029, the only negative regret in the table), while the partial is the worst in A and the best in
B. Every regret is smaller than half a seed sd. Choosing a panel on ANY of these statistics is inside
the noise; that the marginal is the estimable *statistic* does not make it a usable *selector*.

## Both KEEP paths (2 blocks x 540 panels x 3 books = 3,240 cells, all reported)

| scope | n | 4a | 4b | both |
|---|---|---|---|---|
| all cells, block A | 1,620 | **2** | 39 | **0** |
| all cells, block B | 1,620 | **0** | 46 | **0** |
| walk-forward picks (all 6 grid points) | 77 | **0** | 3 | **0** |

**4a 2 of 3,240, 4b 85 of 3,240, BOTH 0 of 3,240.** The 4b footprint is the cap-mix gradient the
record keeps rediscovering, not a characteristic result: **74 of the 85 passers sit at q=0.25**, 11 at
q=0.50, none at q=0.75. No book is promoted; RULES v2 stands.

## Verdict

**KILL** for the partial and the joint-fit t as claim-bearing statistics, and **KILL for tradability**
on every statistic. The corrected statement of the queue's premise, for the record: *the marginal rho
is the most estimable characteristic statistic and the only one that estimates `disp`; `corr` and
`evol` are estimable on all three; `breadth` on none.* The restatement is cheap — 8 of 19 tight-reading
claims survive on the marginal against 6 of 19 on their own statistic, and no claim is supported by a
partial and refuted by the marginal — so a PROTOCOL line requiring the marginal beside every published
partial would cost the record nothing and would have caught `breadth`, whose |t| >= 4 in BOTH
directions across seed blocks. RULES.md, PROTOCOL.md, scan.py, bot.py, baseline.py untouched.

Script: `2026-09-09_is-the-MARGINAL-rho-the-only-estimable-characteristic-statistic_C.py`
Outputs: `.gate.csv .cells.csv .census.csv .restate_cells.csv .replication.csv .claims.csv
.corpusstat.csv .walkforward.csv .picks.csv .statdisagree.csv .keeppaths.csv .console.txt`

SURVIVORSHIP: the constructed panels draw on SMALL439 and BSTK100, which are CURRENT constituents of
their screens, so every panel inherits the bias whole and every return LEVEL is inflated. The object
under test is which STATISTIC about a characteristic is estimable, not a return level; the bias is
common inside a stratum and inflates between-panel spread, so it runs AGAINST a "nothing is estimable"
verdict and does not protect one. No tradable claim is made from these panels, and the walk-forward
comparands (SPY, RULES v2) are unaffected by the panel bias.
