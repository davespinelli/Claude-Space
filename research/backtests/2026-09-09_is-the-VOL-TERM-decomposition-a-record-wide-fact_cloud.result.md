# Idea 330 — is the VOL-TERM decomposition a record-wide fact?  (cloud, 2026-09-09)

**Verdict: ANSWERED / KILL of the premise. The two-term split is not a record-wide fact, and
it is not a fact about a book at all — it is a fact about the GROSS the book is quoted at.**
No RULES change, no new KEEP claimed; `RULES.md`, `scan.py`, `bot.py`, `baseline.py` and
`PROTOCOL.md` untouched.

## Gates
| gate | what | result |
|---|---|---|
| G1 | idea 43's `fast_backtest` vs `engine.backtest` | max\|d\| **0.000e+00** — PASS |
| G2 | REPORTED, not asserted: lever convention vs engine book-at-g-weights | max\|dret\| **4.902e-03**, max \|dSharpe\| **0.0007** — a convention gap, not an error |
| G3 | idea 43's published H1 split (EWALL g=0.75, 10 bps, 3 panels x 4 numbers) | worst \|d\| **0.0023** vs its 3-dp publication — PASS |
| G4 | identity RETURN = S_b − S_s/λ, VOL = S_s(1/λ − 1), all 270 rows | max\|d\| **4.441e-16** — PASS |
| G5 | sign identity RETURN > 0 ⟺ μ_book > μ_SPY | **270/270** — PASS |

## The decisive table: the same book, the same Sharpe, the opposite headline
Idea 43's own three anchors (EWALL, H1 window, 10 bps). `gap` is identical down each panel's
three rows — Sharpe is gross-invariant, idea 43's own finding — and **only the split moves**:

| panel | gross | S_book | S_SPY | gap | RETURN | VOL | vol-matched Sharpe |
|---|---|---|---|---|---|---|---|
| U56 | 0.75 | 1.0716 | 0.9587 | +0.1129 | **−0.6200** | **+0.7329** | 0.6073 |
| U56 | 1.00 | 1.0718 | 0.9587 | +0.1131 | **−0.1962** | **+0.3093** | 0.8103 |
| U56 | g\*=1.32 | 1.0716 | 0.9587 | +0.1129 | **+0.1129** | **−0.0000** | 1.0716 |
| B136 | 0.75 | 1.1433 | 0.9566 | +0.1867 | −0.4101 | +0.5968 | 0.7041 |
| B136 | 1.00 | 1.1445 | 0.9566 | +0.1878 | −0.0199 | +0.2078 | 0.9403 |
| B136 | g\*=1.22 | 1.1433 | 0.9566 | +0.1867 | **+0.1867** | +0.0000 | 1.1433 |
| SMALL439 | 0.75 | 0.4343 | 0.8907 | −0.4564 | −0.6456 | +0.1892 | 0.3582 |
| SMALL439 | 1.00 | 0.4366 | 0.8907 | −0.4540 | −0.3725 | −0.0815 | 0.4806 |
| SMALL439 | g\*=0.91 | 0.4343 | 0.8907 | −0.4564 | −0.4564 | 0.0000 | 0.4343 |

**A "RETURN term" quoted without the gross it was computed at is uninterpretable.** Idea 43's
"the edge is ENTIRELY a volatility term" is true at gross 0.75 with cash at 0%; the identical
book at its vol-matched gross has a VOL term of exactly zero and the whole edge in RETURN.

## What the split actually contains (G4/G5, exact, 270/270)
With λ = σ_b/σ_s: **RETURN = S_b − S_s/λ** and **VOL = S_s(1/λ − 1)**, so
**RETURN > 0 ⟺ μ_book > μ_SPY** and **VOL > 0 ⟺ σ_book < σ_SPY**. The two-term
decomposition carries no information beyond "does the book out-earn SPY?" and "is it less
volatile?" — it is a restatement of the raw comparison, not a diagnosis of it.

## Is there ANY book whose return term is positive? YES — at the record's own default gross
90 book-windows per gross point (3 panels x 6 books x 5 windows), of which 50 clear the
Sharpe-vs-SPY bar:

| gross | Sharpe-beating rows | RETURN > 0 | VOL > 0 | RETURN range |
|---|---|---|---|---|
| 0.75 (idea 43's, the record's default) | 50 | **7 (14.0%)** | 45 (90.0%) | −1.181 .. **+0.159** |
| 1.00 (fully invested) | 50 | **22 (44.0%)** | 35 (70.0%) | −0.639 .. +0.363 |
| g\* (vol-matched counterfactual) | 50 | **50 (100%)** | 8 (16.0%) | +0.002 .. +0.403 |

The 7 positives at g=0.75 are all NARROW books — U56 CAND n=5 (FULL, H2, OOS), B136 CAND n=5
(H1, IS) and B136 CAND n=10 (H1, IS) — i.e. concentrated books that genuinely out-earn SPY in
absolute terms while running *more* vol. "Wins on vol, loses on return" is the shape of the
WIDE, de-grossed end of the family, not of the family.

## Part A — the record-wide census (published numbers, 54 files with their own SPY row)
11,354 published book rows. **6,088 (53.6%) clear the Sharpe-vs-SPY bar**; of those,
**1,286 (21.1%) also out-earn SPY on CAGR**, in **26 of the 54 files**; 3,733 (61.3%) clear
4b's 70%-of-SPY CAGR floor. CAGR > SPY CAGR is an UPPER BOUND on RETURN > 0 (a lower-vol book
at equal CAGR has lower μ), so the true record-wide rate is at most 21.1% — but it is
emphatically not zero, on the record's own published numbers.

## The queue's conditional does not fire
"If none, PROTOCOL 4b's Sharpe bars are measuring de-grossing and the CAGR floor is the only
bar doing work." There are positives, so the antecedent fails. The consequent fails too, on
this grid: **4a 0/36, 4b 6/36, BOTH 0/36**; binding legs **DD 23, H2 18, H1 16, OOS 16,
CAGR 15**, and CAGR is the SOLE failing leg on only **3/36** points. Drawdown is the bar doing
the work, exactly as ideas 321/527/530 found.

## Rule 8 (PROTOCOL 8): (n, g) chosen on IS ≤ 2016-12-31 by IS Sharpe, 2017– read once
| panel | pick | OOS CAGR / Sharpe / MaxDD | RULES v2 OOS | SPY OOS | 4b |
|---|---|---|---|---|---|
| U56 | BAND (v2 band) g=1.00 | **12.74% / 1.2810 / −15.91%** | 9.51% / 1.2817 / −12.05% | 15.38% / 0.8786 / −33.72% | **pass** |
| B136 | BAND (v2 band) g=1.00 | **10.66% / 1.1174 / −16.16%** | 7.98% / 1.1185 / −12.24% | 15.45% / 0.8820 / −33.72% | **pass** |
| SMALL439 | BAND (v2 band) g=1.00 | 5.04% / 0.5672 / −19.19% | 3.85% / 0.5680 / −14.68% | " | fail H1,H2,OOS,CAGR |

The chooser lands on the LIVE band book at gross 1.00 on all three panels. Its OOS decomposition
is RETURN **−0.359** / VOL **+0.761** (U56) — still "wins on vol" at that gross, and still a
statement about the gross, not the book.

**This is NOT a new KEEP candidate.** It re-derives rows the record already publishes: idea 66
committed `universe.json ew-band3 g=1.00` as a **KEEP 4b on 2026-09-04**, and idea 444 found
**all 54 of its 252-book 4b passes sit at gross 1.00**. Filed here as an independent
replication of that fact through a different route (a decomposition census), not as a promotion.
If the Sunday review ever takes it, the exact RULES wording would be the live v2 clause with
`gross = 1.00` in place of `0.75` and nothing else changed — the Sharpe is unmoved
(1.2037 → 1.2036 full sample on U56), the CAGR rises 8.64% → 11.57%, and the MaxDD worsens
−12.05% → −15.91%, which is precisely the trade PROTOCOL 4a refuses and 4b allows.

## Survivorship
B136 and SMALL439 are CURRENT-constituent lists, so book returns are biased up and vols biased
down; both biases push the RETURN term UP, i.e. they make positive return terms MORE likely
here than in reality. The 14.0% positive rate at g=0.75 is therefore an over-estimate, and the
"YES, positives exist" answer rests on U56 (a fixed ETF/mega-cap list, survivorship-free) as
well as B136, which is the safer half of the evidence. SMALL439 = the 483-name sub-$2B panel
with the 44 tickers whose `max_1d_move >= 1.0` dropped.

## What the record should do with this
The same one-line habit ideas 581/583 asked for on gross, applied here: **a published
RETURN/VOL split must carry the gross it was computed at, and should be quoted at matched vol
if it is meant to say anything about selection.** Without that, the split is a de-grossing
measurement wearing a selection headline.
