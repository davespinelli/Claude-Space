# Idea 682 — re-run idea 516 on the 24 UNSAMPLED rc=0 files, and on a FROZEN panel

cloud, 2026-09-11 · script `2026-09-11_re-run-idea-516-on-the-24-UNSAMPLED-rc-0-files-and-on-a-FROZEN-panel_cloud.py`
Console `…_cloud.console.txt` · CSVs `.sweep` `.artefacts` `.scripts` `.grid` `.matched` `.keepflips` `.keeppaths` `.walkforward`

## Verdict: ANSWERED / SPLIT — **idea 516's STATISTIC survives the hold-out; its SAMPLE complaint is overstated; and its ATTRIBUTION is only testable against a vintage the queue named wrongly. Given each script its OWN commit, 14 of 22 reproduce EXACTLY.** No RULES change, no book promoted, no KEEP claimed.

## The three things the queue asked, answered in order

**1. The 24 unsampled files.** Swept, all 24 exit `rc=0` again, none capped.
**91.7% move a RESULT number by more than one restatement step** (5.094e-05), against idea
516's published **97.2%** on its S36. Over the **whole rc=0 population (all 60, no sampling
left)** the figure is **95.0%**. The hold-out is 5.5 pp below the published number and the
population figure sits between them — **the statistic replicates.**

**2. Was the sample drawn by a broken key?** Idea 516 called idea 483's `secs` column
untransferable. With measured runtime now in hand for **60 of 60**, Spearman(idea 483 `secs`,
measured) = **+0.8872**. The column is broken in LEVEL (one 6.0 s file took 332 s) but **not
in RANK** — so the S36 draw was not the arbitrary sample the queue feared, and the hold-out
result above confirms it did not matter. **The queue's first premise is half-refuted.**

**3. The frozen panel.** This is where the answer inverts the question.

## The vintage the queue asked for is the wrong vintage — and that is the finding

The daily-close job left `data/prices.csv` **ending 2026-09-04 from 2026-09-04 through
2026-09-07**. So a script *committed* on 2026-09-08 still published off the **2026-09-04**
panel. The 24-file subsample spans **2 panel vintages — 2026-09-04 (20 scripts) and
2026-09-03 (2)** — and **`9ee888f` (2026-09-08), the vintage idea 513 named and the queue
asked for, is the right panel for ZERO of them.**

That is why pinning it changes nothing. Four arms, same 22 files reached in all four:

| arm | what is frozen | move > 1 restatement step | move at all |
|---|---|---|---|
| TODAY | nothing (panel 2026-09-10, 5,304 artefacts) | **95.5%** | 100.0% |
| PANEL-FROZEN | `prices.csv` → 2026-09-08, today's corpus | **95.5%** | 100.0% |
| FULL-FREEZE | whole tree at `9ee888f` (panel *and* corpus) | **95.5%** | 100.0% |
| **OWN-VINTAGE** | **each script's own publishing commit** | **31.8%** | **31.8%** |

**14 of 22 reproduce at exactly 0.000e+00** once given their own tree — including files whose
TODAY move was enormous (`…does-the-B136-drawdown-cap-admit-any-top-n-book_C` 3.000 → 0.000,
`…a-within-cell-DIFFERENCE-curve…` STRUCTURAL/inf → 0.000). **7 of 22 still move against
their own commit** and are the genuine residue: `…does-a-harmful-instrument-clear-more-often…`
(9.134e-01), `…the-on-share-column_cloud` (inf, shape changed), `…the-pool-mean-as-a-
leaderboard-column_cloud` (inf), `…the-tenth-selection-loses-instance…` (4.286e-01),
`…why-the-035-045-share-window-dips_B` (4.444e-01), `…is-the-value-cost-parallelism-general`
(4.000e-01), `…is-the-pool-sign-the-whole-selector-story_B` (2.534e-02). **2 of 24 hit the
600 s cap in this arm and are reported UNREACHED, never as agreeing.**

PANEL-FROZEN and FULL-FREEZE are not the same arm — they differ on **3 of 24** files, all
census scripts (`…census-every-CROSSING…` 0.9167 → 0.3333, `…does-modal-share-predict-
VARIANCE-not-sign_B` 0.0078 → 0.3333) — the corpus channel is real but small.

**So idea 516's "97.2% silently changed" is a true statement about re-running today and a
FALSE one about irreproducibility: roughly two-thirds of it is curable panel drift, and the
cure is the script's own vintage, which no single frozen snapshot can supply.**

## Gates, all PASS before any sweep
G1 idea 483's `sweepstatus.csv` read not re-typed (81 scripts, 60/17/4). G2 idea 516's 36
read; R24 = the complement, n=24. G3 HEAD panel ends 2026-09-10, `9ee888f` ends 2026-09-08.
G4 of the 5 price/volume panels **only `prices.csv`** moved between the vintages. G5 corpus
growth 1,828 artefacts ADDED / 1 modified, so a committed twin read at HEAD is byte-identical
to the FULL-FREEZE tree's. G6 both worktrees verified. G7 the re-typed vintage reader
reproduces `baseline.load_universe()` at **0.000e+00**. Sandbox: every arm reports **0 `git
status` lines touching the record** — writes under the tree were redirected by idea 483's own
`SITECUSTOMIZE`, imported verbatim; `pair_all`/`pair_csv`/`pair_text`/`scaled_move` are idea
516's, imported, not re-typed.

## Tuned parameters — 2, all grid points reported
**P1 sample** {S36 (read), R24 (fresh), ALL60, NESTED12, NESTED24} × **P2 vintage** {TODAY,
PANEL-FROZEN, FULL-FREEZE, OWN-VINTAGE} — 11 populated points, all in `.grid.csv`. The nested
subsample is ordered by **measured** runtime, not idea 483's stale column. Neither parameter
moves the headline: TODAY is 91.7–95.8% at every sample size, OWN-VINTAGE 30.0% (NESTED12) /
31.8% (NESTED24).

## PROTOCOL 4a/4b re-adjudication of the committed verdict columns
TODAY: 29 adjudicable artefacts, 18,812 book-rows — **4a flips 11 (0.0585%), 4b flips 242
(1.2864%)**. PANEL-FROZEN and FULL-FREEZE: 17 artefacts, 149,360 rows — 4a flips 6 (0.0040%),
**4b flips 0**. A published 4b pass is far more stable than a 4a pass under a vintage step.

## Rule 8, book axis — what one two-day panel step costs the live book
Chosen on 2009–2016, read on 2017–2026 untouched. 10 bps, weekly, next-day.

| vintage | book | CAGR | Sharpe | MaxDD | H1/H2 | OOS CAGR | OOS Sharpe | OOS MaxDD |
|---|---|---|---|---|---|---|---|---|
| 2026-09-10 | RULES v2 (live) | 8.61% | 1.1998 | −12.05% | 1.2349 / 1.1718 | 9.45% | 1.2747 | −12.05% |
| 2026-09-08 | RULES v2 (live) | 8.64% | 1.2037 | −12.05% | 1.2309 / 1.1828 | 9.51% | 1.2817 | −12.05% |
| 2026-09-10 | SPY | 15.11% | 0.8835 | −33.72% | 0.9595 / 0.8211 | 15.24% | 0.8721 | −33.72% |
| 2026-09-08 | SPY | 15.19% | 0.8871 | −33.72% | 0.9587 / 0.8287 | 15.38% | 0.8786 | −33.72% |
| 2026-09-10 | RULES v1 | 6.36% | 0.6554 | −13.83% | 0.6472 / 0.6662 | 7.54% | 0.7309 | −13.83% |

**KEEP paths: 4a 0/3, 4b 0/3 at BOTH vintages** — RULES v2 fails 4b on the CAGR floor (8.61%
vs 0.70×15.11% = 10.58%) at either vintage, and **0 of 3 verdicts flip** across the step.
ΔOOS Sharpe is −0.0070 (v2), −0.0065 (SPY), −0.0099 (v1). **A two-day vintage step is far too
small to move a KEEP verdict on the live book — the instability idea 516 measured lives in the
artefacts, not in the book.**

## Caveats
The OWN-VINTAGE arm's 24 files are the **cheapest 24 by measured runtime** of the 59 rc=0
files present at `9ee888f`; the expensive tail is unswept in that arm and is not claimed. Two
files capped at 600 s. `own_commit` uses the commit that ADDED the script, which is the commit
its artefacts were published in for every file here but is an assumption, not a proof, in
general. The census/book panels are current constituents (survivorship) — unchanged from the
record's standing caveat, and the reported quantity is a WITHIN-file contrast across vintages,
not a level.

## What this implies for the queue
Idea 683 asks for the 4a/4b flip rate "as a function of vintage distance". This run says the
distance that matters is **distance from the script's own publishing vintage**, and that
`data/prices.csv` commit dates are NOT panel dates — the panel sat still for four days inside
this window. Any vintage ladder built on commit dates will mismeasure. Ideas 682/683 should
key on the panel's **last row**, not on the commit.
