# Idea 581 — how many published clause-vs-control comparisons are GROSS-UNMATCHED, and how many flip SIGN when matched?

**Lane C, 2026-09-09.  Verdict: KILL of the strong reading.  Gross-unmatchedness is pervasive
(60.5% of the record's comparison files) but it moves MAGNITUDE, not SIGN: 0/324 rebuilt
comparisons flip on Sharpe, 7/324 on CAGR, 28/324 on drawdown.  Rules unchanged; no book
promoted; one 4b passer PARKed with a memo.  RULES.md, scan.py, bot.py, baseline.py untouched.**

## Gates (all PASS, run before anything was measured)

| gate | what it checks | result |
|---|---|---|
| G1 | numpy runner vs `engine.backtest`, 6 books over 3 panels | max abs return diff **2.78e-17** |
| G2 | matched gross equal to < 1e-12, and max gross ≤ 1.0 | asserted on all 324 cells |
| G3 | a NULL clause (mask always True) must give k = 1 and a zero delta | k = 1.000000000000, diff **0.000e+00** |

G3 is the one that matters for this question: the matching machinery cannot manufacture a flip
on its own.  The RS arms are the same control at the book level — 0 flips out of 108 — which is
the second, independent check on the same point.

## Part A — the census (1,411 committed comparison CSVs, 446 scripts)

| tier | what the FILE lets a reader check | count | share |
|---|---|---|---|
| T1 | publishes a per-arm gross, and the arms carry DIFFERENT values | 329 | 23.3% |
| T2 | publishes a per-arm gross, arms AGREE on it | 5 | 0.4% |
| T3 | publishes no gross column at all | 1,077 | 76.3% |

- Sibling script contains a **DE-GROSS clause** (gated weight → cash, never re-spread): **747 (52.9%)**.
- Sibling script mentions matched gross / rescaling **at all: 291 (20.6%)**.
- **Unmatched in REALISED gross — visibly, or by de-gross construction: 854 (60.5%).**
- Neither published nor mechanically classifiable: 555 (39.3%).  That is the census FLOOR, not a
  claim that those 555 are matched.

The decisive point the census makes on its own: **nominal gross equality is not gross matching.**
A de-gross clause holds strictly less exposure than its clause-OFF control at the same nominal
gross on every day the gate fires, so the 5 files in T2 are not evidence of matching either.
Three quarters of the record's comparison files publish nothing a reader could check.

## Part B — the sign test (324 rebuilt comparisons: 9 arms × 4 dials × 3 gross × 3 panels)

Mean control scale factor k = **0.734** (min 0.415); mean gross gap **+0.133** of nominal, and the
control holds MORE in every de-gross arm.  So the comparisons really are unmatched, and by a lot.

| metric | mean delta unmatched → matched | mean abs delta | share of abs delta that is EXPOSURE | SIGN FLIPS |
|---|---|---|---|---|
| dSharpe | −0.0822 → −0.0822 | 0.1054 → 0.1056 | **−0.2%** | **0 / 324 = 0.0%** |
| dCAGR | −0.0400 → −0.0188 | 0.0400 → 0.0190 | **52.5%** | **7 / 324 = 2.2%** |
| dMaxDD | +0.0845 → +0.0371 | 0.0874 → 0.0465 | **46.8%** | **28 / 324 = 8.6%** |

Flips on ANY of the three: **35 / 324 = 10.8%**.

**Sharpe is exposure-blind.**  Not approximately — 0 flips and the mean absolute delta moves by
0.2%.  Every Sharpe-based clause-vs-control claim in the record is safe from this criticism.

**Where the flips live — all 35, with no exceptions:**

| arm group | comparisons | flips | CAGR-win U→M | DD-win U→M |
|---|---|---|---|---|
| market-level DG (BREADTH, SPYTR, DD) | 108 | **35** | 0.0% → 6.5% | 100.0% → **74.1%** |
| name-level DG (MA, VOL, BAND) | 108 | 0 | 0.0% → 0.0% | 100.0% → 100.0% |
| name-level RS (re-spread, matched by construction) | 108 | 0 | — | — |

A whole-book timing gate is the only clause form whose published comparison is at risk, because
it is the only one whose gross gap is a large blockwise on/off (fire rates 21–28%) rather than a
smooth cross-sectional thinning.

**On idea 48's own metric (drawdown), which is what idea 317 re-priced:** the clause wins on
drawdown in **91.7%** of comparisons unmatched and still **83.0%** matched (74.1% for the
market-level gates).  Idea 317's headline — 0/16 flipping to 51.7% — is NOT what the record-wide
population does.  Here 8.6% flip.  What replaces it is quieter and more useful: **about half of
every published drawdown and CAGR edge is exposure** (46.8% and 52.5% of the mean absolute
delta), so the sizes in the record are roughly 2x too big even where the signs hold.

**One claim in the record that this does re-price by direction, not size:** "gated books lose
CAGR to their own control" is 0.0% winners unmatched and still only 3.2% matched over the 216
de-gross comparisons — the direction survives matching, the magnitude halves.

## Part C — rule 8 walk-forward (54 picks: 9 arms × 3 panels × 2 conventions)

Params picked on 2009–2016 only, evaluated on 2017–2026 untouched, once by the UNMATCHED dSharpe
(the record's own selection rule) and once by the MATCHED dSharpe.

- **The pick is convention-invariant: 26 of 27 (panel × arm) cells choose the SAME (dial, g)
  under both conventions.**  The single exception is B136 VOL-DG (0.45 unmatched vs 0.35 matched).
  Matching gross changes what the record *says*; it barely changes what the record *selects*.
- IS delta sign holds OOS: **59.3% unmatched, 63.0% matched** — matching buys +3.7 pp of
  out-of-sample sign stability, which is inside the noise of 54 picks.
- **KEEP paths on the 54 OOS picks: 4a 2/54, 4b 6/54.**  Over all 324 grid points with no
  selection at all: 4a 6, 4b 50 — the usual gap between a grid point and a walk-forward pick.

The six 4b picks are three books counted under both conventions: U56 BREADTH-DG q=0.20 g=1.00,
U56 DD-DG q=0.10 g=0.75, B136 BREADTH-DG q=0.20 g=1.00.  See the memo — PARKed, not promoted:
they are re-discoveries of a family the record priced on 2026-09-09, and this run's grid was
tuned for the census, not for capital.

## Reference levels (survivorship: B136 and SMALL439 are CURRENT constituents; LEVELS biased up)

| panel | SPY CAGR / Sharpe / MaxDD | RULES v2 CAGR / Sharpe / MaxDD |
|---|---|---|
| U56 | 15.19% / 0.887 / −33.72% | 8.64% / 1.204 / −12.05% |
| B136 | 15.23% / 0.889 / −33.72% | 8.03% / 1.106 / −12.24% |
| SMALL439 | 14.13% / 0.862 / −33.72% | 3.81% / 0.572 / −14.68% |

## What this is worth to PROTOCOL

The idea proposed that unmatched gross may have broken the record's comparisons.  It has not.
What it has done is inflate them, roughly 2x, on the two metrics that are not scale-free, and it
can reverse a drawdown claim about a whole-book timing gate about a quarter of the time.  The
narrow, cheap rule that follows: **a clause-vs-control comparison reported on CAGR or MaxDD must
publish both arms' mean realised gross**; a Sharpe comparison need not.  That is a reporting
requirement, not a new test, and it costs one column.

Outputs: `.console.txt` `.census.csv` `.cells.csv` `.walkforward.csv` `.keeppaths.csv` `.memo.md`
