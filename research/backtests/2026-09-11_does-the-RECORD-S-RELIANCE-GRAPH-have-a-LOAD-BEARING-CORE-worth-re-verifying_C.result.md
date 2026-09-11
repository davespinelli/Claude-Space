# Idea 790 — does the RECORD'S RELIANCE GRAPH have a LOAD-BEARING CORE worth re-verifying?

lane C, 2026-09-11. Scripts:
`2026-09-11_does-the-RECORD-S-RELIANCE-GRAPH-have-a-LOAD-BEARING-CORE-worth-re-verifying_C.py`
(runtime 88 s) and its `_addendum.py` (EXACT-leg restatement, arithmetic on the main run's own
committed csv). 10 bps, next-day execution. Two tuned parameters — RANK STATISTIC
(NAMED / ECHOED / SUM / MAXLEG / CTRL) × TOP SHARE (0.02 / 0.05 / 0.10 / 0.20 / 0.25) — all
25 grid points published.

**ANSWER: NO, TWICE OVER — KILL. (1) There is no core to rank: on the record's own ECHO leg
the reliance graph is nearly complete (median in-degree 366 of 687 runs, 1.9% isolated), so
the top decile by the summed degree holds just 16.4% of the mass. The one concentrated leg
(NAMED, gini 0.7348, top decile 59.6% of mass) picks an almost disjoint set — Jaccard 0.0534,
rank Spearman 0.0172 — so "the record's core" is a choice of statistic, not a fact about the
record. (2) The re-verification the idea asks for cannot be run strongly on the artefacts as
committed: only 1.6–7.7% of core headline numbers appear VERBATIM in their own run's data
files, and the tolerant leg that does reach ~90% has a measured 46.0% chance floor. No RULES
change, no book promoted, no KEEP claimed; RULES.md, PROTOCOL.md, scan.py, bot.py and
baseline.py untouched.**

## GATES — all PASS, printed before any answer was read

| gate | reading | bar |
|---|---|---|
| G1 corpus | 1,518 committed text files (34.7 MB), **687 rankable runs**, 780 narratives, self-edges **0** | exact |
| G2 anchor | idea 779's committed `.reliance.csv` re-read: cited-by **0..79**, mean **1.8353**, median **0**; VENUE **71.99%** CITED **27.35%** ECHO **44.48%** STRICT **40.20%** — the queue's quoted numbers, exactly | exact |
| G3 identity | `fast_backtest` vs `engine.backtest`, max \|dret\| **0.000e+00** | 1e-12 |
| G4 verifier | PLANT-TRUE **100.0%** of 1,166; PLANT-FALSE **46.0%** of 1,175 | TRUE ≥ 95%, FALSE lower |
| G5 graph | self-edges 0, INDEX docs excluded as citers; NAMED 0..154 (mean 2.66, median 1), ECHOED 0..581 (mean 313.86, **median 366**), CTRL 0..4 | non-constant |

**G4 is the gate that decides how this result must be read.** The ROUND leg (a committed value
within the token's own rounding tolerance) matches a *randomly drawn* token of the same shape
**46.0%** of the time, because a run's artefacts hold millions of numbers. Every ROUND-inclusive
share below sits on that floor.

## PART 1 — CONCENTRATION: H_CONC **FALSIFIED**

| statistic | total degree | zero-share | gini | mass@2% | mass@5% | **mass@10%** | mass@20% | mass@25% |
|---|---|---|---|---|---|---|---|---|
| NAMED | 1,828 | 0.3450 | **0.7348** | 0.3315 | 0.4655 | **0.5963** | 0.7527 | 0.8063 |
| ECHOED | 215,622 | 0.0189 | 0.2897 | 0.0355 | 0.0837 | 0.1648 | 0.3147 | 0.3882 |
| **SUM** | 217,450 | 0.0087 | 0.2868 | 0.0354 | 0.0834 | **0.1643** | 0.3136 | 0.3868 |
| MAXLEG | 215,787 | 0.0087 | 0.2889 | 0.0354 | 0.0836 | 0.1647 | 0.3145 | 0.3879 |
| CTRL | 1,297 | 0.0146 | 0.2330 | 0.0332 | 0.0794 | 0.1604 | 0.3177 | 0.3986 |

THE MECHANISM: ECHOED's total degree is **118× NAMED's** (215,622 vs 1,828), so SUM *is*
ECHOED (Jaccard 0.9437 at the decile). Idea 779's ECHO leg was a per-CLAIM object — a claim
carries a handful of numbers. Promoted to the FILE level a run offers up to 500 distinctive
tokens (median 29, 16,084 in total over the verified set), and one match anywhere is an edge,
so the echo graph saturates. **Echo does not scale from claim to file.**

## PART 2 — AGREEMENT: H_AGREE **FALSIFIED**

Jaccard between top-10% cores: NAMED×ECHOED **0.0534**, NAMED×SUM 0.0698, NAMED×CTRL 0.1695,
ECHOED×MAXLEG 1.0000. Full-ranking Spearman: NAMED vs ECHOED **0.0172**, SUM vs CTRL 0.0333.
The two legs the record calls "reliance" rank the same 687 runs essentially independently.

## PART 3 — RE-VERIFICATION: 457 runs, 543 MB of their own artefacts re-read

H_SOUND **HOLDS on the tolerant leg**: at the headline point (SUM @ top 10%, n = 69) the core's
headline tokens verify **93.5%** against its own committed data vs **89.4%** for the seeded
non-core sample of 120 (lift **+4.1 pp**); console-inclusive 97.7% vs 98.1%. The mean
ANY-minus-DATA gap is **7.03 pp** — that share of headline numbers exists only in a run's own
printout. **16 runs committed no data artefact at all**, one of them inside the headline core
(`2026-09-07_u56-top20-band-m20_4b_B_MEMO`); 12 verified runs sit below 50%.

The one inversion worth naming: the **most-NAMED** runs — the leg that actually is concentrated,
i.e. the only candidate "load-bearing core" — verify **worst**: NAMED@2% **75.94%** vs base
89.36% (**−13.4 pp**), NAMED@5% 88.03% (−1.3 pp). Worst in the headline core:
`2026-09-08_is-the-top-decile-trim-a-drop-the-worst-rule_B` 0.5294,
`2026-09-10_re-read-every-chooser-result-on-the-OOS-RANK-of-its-constant-arm_B` 0.7391.

**The EXACT-leg addendum is the honest bottom line.** Verbatim presence in the run's own data
files (no rounding tolerance, hence no 46% floor):

| point | core EXACT in own DATA | non-core | core EXACT incl. console |
|---|---|---|---|
| SUM @ 10% | **1.56%** | 6.59% | 58.36% |
| NAMED @ 2% | **7.69%** | 6.59% | 81.54% |
| ECHOED @ 2% | **0.15%** | 6.59% | 64.87% |

Headline numbers live in the console printout, not in the committed data: 58–81% verbatim there
against 0.2–7.7% in the csv/json. The ~90% ROUND-leg reading is therefore a weak test sitting on
a 46% chance floor, and the difference between core and tail on it (±5 pp) is not evidence that
the record's most-relied-on arithmetic has been checked.

## PRICE LEG (REAL panels, 36 books)

| panel | RULES v2 CAGR / Sharpe / MaxDD (OOS Sharpe, OOS CAGR) | SPY |
|---|---|---|
| U56 | 8.61% / 1.1998 / −12.05% (1.2747, 9.45%) | 15.11% / 0.8835 / −33.72% (0.8721, 15.24%) |
| B136 | 8.03% / 1.1058 / −12.24% (1.1185, 7.98%) | 15.23% / 0.8890 / −33.72% (0.8820, 15.45%) |
| SMALL439 | 3.81% / 0.5725 / −14.68% (0.5680, 3.85%) | 14.13% / 0.8615 / −33.72% (0.8820, 15.45%) |

4a **0/36**, 4b **3/36** (U56/MA-RS/g0.75/W, U56/MA-RS/g0.75/M, B136/MA-RS/g0.75/W — the
record's standing candidates, not new ones), BOTH 0/36. Binding 4b legs: DD 13, CAGR 8.

## RULE 8 WALK-FORWARD

**WF-A (the answer out of sample).** Corpus split at vintage 2026-09-08 (347 early-vintage
rankable runs; 776 EARLY citers, 742 LATE citers), the same runs ranked twice — once by EARLY
citers only, once by LATE citers only. SUM @ 10%: Jaccard **0.3462** on k = 35 (rank Spearman
0.8840); NAMED @ 10%: Jaccard **0.2069** (Spearman 0.3758). DATA-verification of the early core
96.4% vs the late core 95.6%. **The core is not the same set out of sample** — it is a
vintage-specific object, on the leg that is concentrated most of all.

**WF-B (the core priced as a decision rule, OOS read once).** Act on the IS-best parent only if
its backing claims (idea 779's committed 607-claim census: U56 120, B136 119, SMALL439 82) come
from an EARLY-ranked core run whose headline verifies ≥ 90% on the DATA leg; else stand down to
RULES v2 on U56.

| book | OOS CAGR | OOS Sharpe | OOS MaxDD |
|---|---|---|---|
| every acting decision book (20 of 25 points) | 13.00% | 1.1567 | −18.40% |
| every standing-down book (5 of 25) | 9.45% | 1.2747 | −12.05% |
| ALWAYS-ACT control | 13.00% | 1.1567 | −18.40% |
| FULL-STAND-DOWN control = RULES v2 U56 | 9.45% | 1.2747 | −12.05% |
| SPY | 15.24% | 0.8721 | −33.72% |

**0/25 beat RULES v2 U56's OOS Sharpe (1.2747); 25/25 beat SPY's (0.8721).** Every decision book
is byte-identical to one of the two controls: the core filter never separated a cell, so it
carries **zero** book-level information. Decision books: 4a **0/25**, 4b **16/25** (all of them
the ALWAYS-ACT control in disguise), BOTH **0/25**.

## VERDICT — **KILL**

No core, no agreement between the legs that would define one, no out-of-sample stability of the
set, no book-level information, and — the part that matters for any future "re-verify the
record" work — no strong verification is available from the artefacts as committed. The two
reportable facts for the record are the ECHO-saturation mechanism (echo does not scale from
claim to file) and the EXACT/ROUND split: headline numbers are recoverable from a run's own
printout, essentially never verbatim from its data.

SURVIVORSHIP: universe.json / universe_broad.json / the small panel are current constituents, so
every stock-side level carries a survivorship premium; the three parents start on different
dates (U56/B136 2008, SMALL 2010). The non-core base rate is a seeded SAMPLE of 120 runs
(111 of which fell outside every top-25% core), not a census.

Artefacts: `.graph.csv` (687 runs), `.verify.csv` (457), `.coregrid.csv` (25),
`.concentration.csv`, `.grid.csv` (36), `.walkforward.csv` (79), `.keeppaths.csv`,
`.unverifiable.csv` (16), `.console.txt`; addendum `_addendum.exactleg.csv`, `.console.txt`.
