# Idea 591 — is AMPLITUDE the record's real clause taxonomy?

**Cloud lane, 2026-09-09.  Verdict: KILL of the queue's proposal.  The amplitude label is not a
better taxonomy than the record's level word — at the cardinality of the record's own labels it
IS the record's label, cell for cell: Cramér's V(SD/q3, SHAPE) = 1.0000 over all 324 cells, and
the two columns' skill numbers agree to the printed digit on every outcome.  The 2-bin amplitude
split does not cross the name/market line either; it cuts INSIDE "name", separating the RS arms —
whose amplitude is ~0 BY CONSTRUCTION (gross-matched k ≡ 1, gate G5) — from the de-grossed ones.
The only apparent wins come from k=4 binnings, finer than any label the record uses, and 2 of the
3 do not clear their own arm-permutation noise floor.  No RULES change; no book promoted; no
memo.  RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py untouched.**

## Gates (all PASS, run before anything was measured)

| gate | what it checks | result |
|---|---|---|
| G1 | vectorised Runner vs `engine.backtest`, 4 books | max abs return diff **1.39e-17** |
| G2 | matched gross, asserted cell by cell on all 324 cells | **< 1e-12** |
| G3a | **PROVENANCE**, frozen-vintage panels (B136+SMALL439, 216 cells) vs idea 584 | max abs Δ **2.22e-16**, verdict disagreements **0** |
| G3b | **VINTAGE**, U56 (108 cells) — `data/prices.csv` gained 2026-09-09 in `7a93b07` | max abs Δ **2.78e-03**, verdict disagreements **0** |
| G4 | the label machinery itself (apply==fit, q2 balance, constant-label Brier) | 0 disagreements, share 0.5000, error **0.00e+00** |
| G5 | RS degeneracy: gross-matched k ≡ 1, so amplitude ≈ 0 by construction | max abs(k−1) **1.11e-15**, max SD **4.87e-03** |

G3 is split because the vintage moved under this run: idea 584 ran on a U56 panel of 4700 rows,
this one on 4701.  Per idea 514 that is a one-step vintage ladder, and the number that matters is
that **no published verdict flips on it** — every flip flag, `pass4a` and `pass4b` is identical.
The frozen panels reproduce to machine precision.  G5 is the gate that licenses the
"two thirds of the amplitude ordering is a construction artefact" reading below.

Corpus: 9 clause arms × 4 dials × 3 gross × 3 panels = **324 books**, the same grid idea 581 and
idea 584 published.  Whole-grid keep counts reproduce exactly: **4a 6, 4b 50, BOTH 0**.

## What is being predicted, and why it is not what 584 predicted

584's outcome was a FLIP (does a clause-vs-control sign survive gross-matching).  591's outcomes
are the things the record actually publishes and acts on:

| outcome | definition | n positive / 324 |
|---|---|---|
| `pass4a` | PROTOCOL 4a vs live RULES v2, full sample | **6** (1.85%) |
| `pass4b` | PROTOCOL 4b vs SPY, full sample + OOS leg | **50** (15.4%) |
| `sign_holds` | sign(ΔSharpe vs control) on 2009-16 == on 2017-26 | **189** (58.3%) |

Two tuned parameters as the queue specifies: STATISTIC ∈ {SD, IQR, SDDIFF, MAD} × BINNING ∈
{q2, q3, q4, e2, e3, e4} = **24 grid points, all 24 reported** in `.skill.csv` and the console,
IS and OOS, against both record labels (LEVEL name/market; SHAPE nameRS/nameDG/marketDG).

Skill = 1 − Brier(label)/Brier(no label), **out of fold** (leave-one-panel-out, and separately
leave-one-family-out).  An in-sample column is printed beside it only to show the size of the
degrees-of-freedom gift a finer label collects.

## PART A — the structural fact that decides the question

| form | level | shape | SD | IQR | SDDIFF | MAD | gross gap | 4a | 4b | sign |
|---|---|---|---|---|---|---|---|---|---|---|
| MA-DG | name | name-DG | 0.1903 | 0.2240 | 0.0320 | 0.1494 | 0.2745 | 0 | 3 | 0.667 |
| VOL-DG | name | name-DG | 0.1132 | 0.0992 | 0.0189 | 0.0726 | 0.1186 | 3 | 6 | 0.667 |
| BAND-DG | name | name-DG | 0.1894 | 0.2133 | 0.0186 | 0.1478 | 0.2720 | 2 | 7 | 0.444 |
| BREADTH-DG | market | market-DG | 0.3926 | 0.5000 | 0.1136 | 0.3222 | 0.1738 | 1 | 6 | 0.500 |
| SPYTR-DG | market | market-DG | 0.3981 | 0.5000 | 0.1189 | 0.3303 | 0.1801 | 0 | 7 | 0.583 |
| DD-DG | market | market-DG | 0.3990 | 0.3333 | 0.1242 | 0.3301 | 0.1771 | 0 | 5 | 0.389 |
| MA-RS | name | name-RS | 0.0016 | 0.0006 | 0.0015 | 0.0007 | 0.0000 | 0 | 6 | 0.833 |
| VOL-RS | name | name-RS | 0.0012 | 0.0004 | 0.0011 | 0.0004 | 0.0000 | 0 | 4 | 0.500 |
| BAND-RS | name | name-RS | 0.0016 | 0.0006 | 0.0015 | 0.0007 | 0.0000 | 0 | 6 | 0.667 |

**SD/q3 and the record's SHAPE word are the same partition.**  Cramér's V = **1.0000**: bin 0 is
the 108 name-RS cells, bin 1 the 108 name-DG cells, bin 2 the 108 market-DG cells, exactly.  Their
skill columns are consequently identical on all three outcomes (0.0062 / −0.0008 / 0.0115,
panel folds).  A relabelling that reproduces the old labels to the cell is a **synonym**.

**SD/q2 does not cut where the level word cuts.**  Cramér's V vs LEVEL = 0.7071, and the crosstab
shows why: bin 0 is 162 name cells and 0 market cells; bin 1 is all 108 market cells plus 54 name
cells.  The amplitude ordering's first cut is RS-vs-DG, and gate G5 says that cut is a property of
the WEIGHT CONVENTION (an RS book re-spreads to the same gross, so u_t ≡ 1), not of the clause.
**Two of the three amplitude tiers are a construction artefact.**

## PART B/D — the 24 grid points, and the rule-8 walk-forward

Rule 8 as applied to the label question: the amplitude statistic is measured on the **2009–2016
gross path only**, bin edges are fitted on **2009–2016 verdicts**, and the chosen pair is scored
**once** on 2017–2026 verdicts, which no choice touched.

| IS → OOS outcome | rule-8 amplitude pick | pick OOS skill | LEVEL OOS | SHAPE OOS |
|---|---|---|---|---|
| pass4a_is → pass4a_oos | SDDIFF/e4 | **+0.0605** | +0.0129 | +0.0148 |
| pass4b_is → pass4b_oos | IQR/e4 | **+0.0380** | −0.0014 | −0.0013 |
| sign_holds_is → sign_holds | SDDIFF/e4 | **+0.0760** | +0.0107 | +0.0115 |

Read alone this table says "amplitude wins 3/3", and that is exactly the reading this run was
built to stress.  Every winner is a **k = 4** binning — finer than either record label — and
under leave-one-**family**-out folds the winners change and several go negative (pass4a: SD/e4
**−0.0220**; pass4b: SD/q4 −0.0063; sign_holds: SD/e3 −0.0436).  A label whose identity depends
on the fold is not a taxonomy.

## PART D2 — the dial control: inside a gate family, "amplitude" IS the strictness dial

| outcome | market-DG AUC(SD) | market-DG AUC(dial rank) | name-DG AUC(SD) | name-DG AUC(dial rank) |
|---|---|---|---|---|
| pass4a | 0.3458 | 0.3738 | 0.4583 | 0.4214 |
| pass4b | 0.2343 | 0.2667 | 0.5870 | 0.5000 |
| sign_holds | **0.9048** | **0.8473** | 0.3931 | 0.4233 |

Spearman(SD, dial rank) inside market-DG is **+0.9685** (BREADTH +0.9716, SPYTR +0.9716, DD
+0.9688).  The one strong within-group number in the whole run — SD at 0.9048 for OOS sign
stability inside the market gates — is matched to within **0.0575** by the bare dial rank, an
integer 0–3 that needs no path, no gross series and no statistic.  Inside name-DG, amplitude is
at or below a coin on all three outcomes.  **H_WITHIN FAILS.**

## PART D3 — the noise floor (this is the part the queue's framing was missing)

Amplitude is near-constant inside a clause arm, so the corpus has **9 effective units, not 324**.
The null permutes whole ARM PROFILES: arm *a* receives the amplitude profile of arm π(*a*) at the
same (panel, gross, dial position).  That preserves the multiset of amplitudes and all within-arm
structure exactly and breaks only the arm↔outcome link.  500 permutations; the full best-of-24
rule-8 procedure is re-run inside each one.

| outcome | observed pick OOS | null mean | null p95 | null max | **p** | verdict |
|---|---|---|---|---|---|---|
| pass4a_oos | +0.0605 | −0.0038 | +0.0208 | +0.0605 | **0.004** | survives |
| pass4b_oos | +0.0380 | **+0.0201** | +0.0526 | +0.0569 | **0.192** | chance |
| sign_holds | +0.0760 | +0.0043 | +0.0873 | +0.1417 | **0.078** | chance |

The null mean for `pass4b` is +0.0201 — **a best-of-24 search on a randomised label scores +0.02
by construction**, which is more than half the observed +0.0380.  Any future run that quotes a
best-of-K label skill without this floor is quoting the search, not the label.

The one survivor, `pass4a`, rests on **6 positive cells in 3 arms on 2 panels**.  With
leave-one-panel-out folds one fold has no positives at all, and the same pick scores −0.0220
under family folds.  It is reported as it stands and it is **not** enough to carry a taxonomy.

## PART E — both KEEP paths (PROTOCOL rule 4), and the rule-8 book picks

Whole grid, no selection: **4a 6, 4b 50, BOTH 0** of 324 — identical to idea 581's and idea 584's
committed counts, as gate G3 requires.  **Every one of the 50 is a re-derivation of an
already-published, already-declined row; nothing new is proposed and no memo is filed.**

4b passes split by the amplitude bin the queue proposes (SD/q3) and by the record's level word:

| SD/q3 bin | 4b pass | 4b fail | | level | 4b pass | 4b fail |
|---|---|---|---|---|---|---|
| 0 (name-RS) | 16 | 92 | | market | 18 | 90 |
| 1 (name-DG) | 16 | 92 | | name | 32 | 184 |
| 2 (market-DG) | 18 | 90 | | | | |

**The 4b pass rate is flat in amplitude: 14.8% / 14.8% / 16.7%.**  That is the practical form of
the queue's question and the answer is that the proposed label does not sort the verdict at all.

Rule-8 book picks (9 arms × 3 panels, (dial, gross) chosen on 2009–2016 IS ΔSharpe against the
unmatched control, 2017–2026 read once): IS sign holds OOS on **16/27** (59.3%), **4a 1/27,
4b 3/27**.  The three 4b picks are again the already-PARKed books:

| pick | full CAGR / Sharpe / MaxDD | H1 / H2 | OOS CAGR / Sharpe / MaxDD |
|---|---|---|---|
| U56 BREADTH-DG q=0.20 g=1.00 | 15.99% / 1.2566 / −16.48% | 1.187 / 1.354 | 16.35% / **1.4533** / −14.16% |
| U56 DD-DG q=0.10 g=0.75 | 11.80% / 1.2015 / −14.94% | 1.185 / 1.238 | 11.40% / 1.3407 / −14.94% |
| B136 BREADTH-DG q=0.20 g=1.00 | 15.17% / 1.1356 / −20.02% | 1.248 / 1.014 | 12.58% / 1.1553 / −15.32% |

against **RULES v2** (U56 8.63% / 1.2021 / −12.05%, OOS Sharpe 1.2788; B136 8.03% / 1.1058, OOS
1.1185) and **SPY** (U56 15.15% / 0.8855 / −33.72%, OOS Sharpe 0.8758).  All three fail 4a; the
one 4a pass (B136 VOL-DG cap 0.45 g=0.50) fails 4b on CAGR.

## Reference levels (survivorship: B136 and SMALL439 are CURRENT constituents; LEVELS biased up)

| panel | SPY CAGR / Sharpe / MaxDD | RULES v2 CAGR / Sharpe / MaxDD | SPY OOS Sharpe | v2 OOS Sharpe |
|---|---|---|---|---|
| U56 | 15.15% / 0.886 / −33.72% | 8.63% / 1.202 / −12.05% | 0.876 | 1.279 |
| B136 | 15.23% / 0.889 / −33.72% | 8.03% / 1.106 / −12.24% | 0.882 | 1.119 |
| SMALL439 | 14.13% / 0.862 / −33.72% | 3.81% / 0.572 / −14.68% | 0.882 | 0.568 |

Every claim here is a LABEL-vs-VERDICT statement on a fixed panel, which the survivorship bias
does not move; the levels are quoted so a reader can see the bias.

## What this is worth to the record

1. **Do not adopt the amplitude label.**  At three bins it is the record's own SHAPE word, cell
   for cell (V = 1.0000); at two bins it splits RS from DG, which gate G5 shows is a weight
   convention, not a clause property.  The queue's "re-label every clause family" would rename
   the columns and change nothing.
2. **Idea 584's SD result does not transfer from flips to verdicts.**  SD orders which forms
   flip (AUC 0.9075) and does not order whether they PASS: 4b pass rate 14.8/14.8/16.7% across
   the three amplitude tiers, and the whole-corpus AUC for `pass4b` is **0.4925** — a coin.
3. **A best-of-K label search has a large positive noise floor and the record has not been
   quoting it.**  Randomising the arm↔outcome link and re-running the same best-of-24 search
   scores **+0.0201** mean on `pass4b`.  Two of this run's three nominal wins are inside that
   floor.  Proposal for PROTOCOL (not adopted here, filed as an idea): any claim of the form
   "statistic X predicts verdict Y better than label Z" must publish the permutation floor of
   its own search width beside it.
4. **Within a gate family, path amplitude is the strictness dial.**  Spearman +0.9685.  Future
   runs should quote the dial rank, which is free, rather than a path statistic that reproduces
   it.

Outputs: `.console.txt` `.cells.csv` `.labels.csv` `.skill.csv` `.within.csv` `.dialcontrol.csv`
`.null.csv` `.walkforward.csv` `.keeppaths.csv`
