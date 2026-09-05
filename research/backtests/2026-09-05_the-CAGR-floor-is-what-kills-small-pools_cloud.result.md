# Idea 156 — the-CAGR-floor-is-what-kills-small-pools (cloud, 2026-09-05)

**ANSWERED, and it is a KILL of the artefact hypothesis in the form it was posed. Mechanically
the CAGR floor IS gross-driven — scaling the 300 books to SPY's volatility removes 106 of the
119 CAGR-bar failures. But the floor is not *removable*: 37 of the 38 books whose ONLY 4b
failure was the CAGR floor convert straight into DD-cap failures, and the corpus-wide 4b pass
count falls from 42 to 2. 4b's CAGR floor and its drawdown cap are one joint risk-budget bar,
not two independent ones, and a book run at SPY's volatility cannot clear a cap set at 60% of
SPY's drawdown.**

The one place the artefact reading survives is exactly where PROTOCOL rule 2 puts the ceiling:
a *partial* vol match at `g = min(g_required, 1.00)` lifts idea 78's k=20 / n=20 cell — the one
that failed on CAGR in 50 of 50 draws — from a 0% to a 12% 4b pass rate, and rule 8 picks it.
Uncapping the same match returns it to 0%. **Idea 148's "the no-leverage ceiling is
load-bearing" is confirmed in a stronger form: the ceiling is not merely a constraint on the
fix, it IS the fix.**

Script `2026-09-05_the-CAGR-floor-is-what-kills-small-pools_cloud.py`; outputs `.console.txt`,
`.grid.csv`, `.flips.csv`, `.lever.csv`, `.walkforward.csv`.

## Reproduction, before any new number was read

| check | target | this run |
|---|---|---|
| [a] STATIC arm vs idea 78's committed `gridB.csv`, all 300 books | identical | **max abs diff 2.2e-16 on CAGR / Sharpe / MaxDD / H1 / H2 / OOS Sharpe; the 4b failing-bar string identical in 100.0% of the 300 books — EXACT** |
| [b] k=20 / n=20 fails 4b on CAGR in 50 of 50 | 100% | **100.0% CAGR-bar failure, 0.0% 4b pass** |
| [b] k=80 / n=20 passes 4b in ~46% | ~46% | **46.0%** |
| [c] the vol match actually lands on SPY's vol | ratio 1.00 | **mean abs(achieved/SPY − 1) = 0.0014** |

Idea 78's sub-panels are reproduced from the same seed stream (`default_rng(78_500 + k)`), so
this is a re-run of its corpus, not a lookalike. Both halves of idea 156's premise hold.

## Corpus and grid

Idea 78's Test B corpus, unchanged: B136, k in {20, 40, 80}, 50 fixed random k-name sub-panels
per k, CAND-n books at n in {5, 20}, 10 bps, weekly, t+1 — **300 books**. `k`, `draw` and `n`
are carried-over corpus axes, not tuned here. **Exactly two tuned parameters**: the gross
convention in {STATIC = 0.75, VM_IS = vol-matched on 2009-2016 only, VM_FULL = vol-matched on
the full sample (look-ahead)} and the leverage ceiling in {CAP = min(g, 1.00), RAW = uncapped}.
**1500 book-arm rows, all in `.grid.csv`.**

## (1) Most of these books need LEVERAGE to reach SPY's volatility

| statistic | VM_IS | VM_FULL |
|---|---|---|
| median required gross | **1.032** | 1.031 |
| range | 0.719 – 2.502 | 0.694 – 2.460 |
| **share of the 300 books needing g > 1.00** | **55.0%** | 54.3% |

Broken out, the driver is **the book's cash weight, not `k`** (this is where prediction P2 was
half wrong — I predicted small-`k`; it is small-`n_elig`):

| cell | realised vol at g=0.75 | median required gross | share needing g > 1 |
|---|---|---|---|
| k=20, n=5 | 13.89% | 0.961 | 30% |
| k=40, n=5 | 15.63% | 0.854 | 0% |
| k=80, n=5 | 17.81% | 0.774 | 0% |
| **k=20, n=20** | **6.94%** | **1.822** (min 1.499, max 2.502) | **100%** |
| k=40, n=20 | 10.70% | 1.213 | 100% |
| k=80, n=20 | 12.55% | 1.047 | 100% |

SPY runs 17.72%. A 20-name book drawn from a 20-name panel holds only the trend-eligible
subset and sits in cash the rest of the time, so it runs **39% of SPY's volatility** and would
need **1.8x leverage** to match it. PROTOCOL rule 2 forbids that. This is the whole answer to
idea 156's title question, and it confirms idea 148 precisely.

## (2) The flip table — the CAGR floor moves, and the DD cap eats the gain

| arm | 4b passes | KILL→KEEP | KEEP→KILL | net | CAGR-bar failures | DD-bar failures | mean ΔCAGR | mean ΔMaxDD | mean ΔSharpe |
|---|---|---|---|---|---|---|---|---|---|
| STATIC/CAP (control) | **42** | – | – | – | **119** | **146** | – | – | – |
| VM_IS/CAP | 10 | 8 | 40 | **−32** | 58 | 246 | +2.40pp | −4.09pp | +0.0004 |
| VM_IS/RAW | **2** | **0** | 40 | **−40** | **13** | **297** | +4.32pp | −7.25pp | −0.0000 |
| VM_FULL/CAP | 9 | 8 | 41 | −33 | 59 | 247 | +2.29pp | −3.91pp | +0.0003 |
| VM_FULL/RAW | 1 | 0 | 41 | −41 | 14 | 298 | +4.34pp | −7.28pp | −0.0001 |

Uncapped vol matching does what the artefact hypothesis said it would: **CAGR-bar failures fall
119 → 13 (89% of them removed).** And it does nothing whatsoever for 4b, because **DD-bar
failures rise 146 → 297 out of 300.**

The 38 books whose *only* 4b failure was the CAGR floor are the cleanest possible test, and the
exchange is one-for-one:

| where the 38 CAGR-only books land | VM_IS/CAP | VM_IS/RAW |
|---|---|---|
| now pass 4b | **8** | **0** |
| now fail on DD alone | 11 | **37** |
| still fail on CAGR | 18 | 0 |
| fail on DD + something else | 1 | 1 |

**Under an uncapped vol match, 37 of 38 CAGR-only failures become DD-only failures and not one
becomes a pass.** Mean Sharpe across arms is 0.8996 / 0.9000 / 0.8994 — unchanged, as idea 66's
lever predicts — so nothing was gained or lost except the position on the risk axis.

The reason is structural, and it is a fact about 4b rather than about these books: **4b asks for
100% of SPY's Sharpe in both halves and out of sample, but only 60% of SPY's drawdown.** A book
scaled to 100% of SPY's *volatility* lands near 100% of SPY's drawdown. The two bars are
mutually inconsistent at SPY-matched risk, which is why the pass count collapses.

## (3) Per-cell: the small pool is the one cell the ceiling rescues

4b pass rate by cell:

| cell | STATIC | VM_IS/CAP | VM_IS/RAW |
|---|---|---|---|
| k=20, n=5 | 0.02 | 0.02 | 0.02 |
| **k=20, n=20** | **0.00** | **0.12** | **0.00** |
| k=40, n=5 | 0.00 | 0.00 | 0.00 |
| k=40, n=20 | **0.34** | 0.04 | 0.00 |
| k=80, n=5 | 0.02 | 0.02 | 0.02 |
| k=80, n=20 | **0.46** | 0.00 | 0.00 |

CAGR-bar failure rate in the same cells: k=20/n=20 goes **1.00 → 0.88 → 0.00**; k=80/n=20 goes
0.10 → 0.00 → 0.00. DD-bar failure rate goes the other way: k=80/n=20 **0.22 → 1.00 → 1.00**.

So the honest decomposition is: **the small-pool cell is the only one the manoeuvre helps, and
only at the ceiling.** Capping at 1.00 gives it a partial vol match — enough extra gross to
clear the CAGR floor, not enough to breach the DD cap — and 6 of its 50 draws pass. Every
larger-pool cell that was passing at static gross is destroyed by the same operation.

## (4) Rule 8 walk-forward — chosen on ≤2016, read once on 2017-2026

| arm | n | selector | pick | OOS CAGR / Sharpe / MaxDD | vs v1 OOS | vs SPY OOS | full-sample 4b |
|---|---|---|---|---|---|---|---|
| STATIC/CAP | 20 | S0 do-nothing | full B136 | 12.49% / 0.892 / -20.05% | +0.316 | +0.010 | H2 |
| STATIC/CAP | 20 | S1 IS-Sharpe | k=20 | 8.37% / 1.104 / -10.54% | +0.528 | +0.222 | **CAGR** |
| STATIC/CAP | 20 | S2 4b-aware (21 adm.) | k=40 | 12.30% / 1.068 / -19.63% | +0.491 | +0.186 | **PASS** |
| **VM_IS/CAP** | 20 | **S1 = S2 (7 adm.)** | **k=20 @ g=1.00** | **11.16% / 1.103 / -13.93%** | **+0.527** | **+0.221** | **PASS** |
| VM_IS/RAW | 20 | S1 = S2 (0 adm.) | k=20 @ **g=1.66 LEVERED** | 18.48% / 1.099 / -22.62% | +0.522 | +0.217 | **DD** |
| VM_IS/CAP | 5 | S2 (1 adm.) | k=40 @ g=0.83 | 13.69% / 0.802 / -31.19% | +0.226 | **−0.080** | H2, OOS, DD |

SPY OOS 15.45% / 0.882 / -33.72%; RULES v1 on B136 OOS 5.94% / 0.576 / -21.19%. VM_FULL rows
are printed in the console with a CONTAMINATED label (their `g` uses OOS volatility) and are
never read for a verdict; they agree with VM_IS to the third decimal anyway.

This is the sharpest single line in the run: **the exact book idea 78's rule 8 selected and
which failed 4b on the CAGR floor (k=20, OOS Sharpe 1.104, MaxDD −10.54%) passes 4b once it is
re-grossed to the no-leverage ceiling — and fails again on drawdown the moment the ceiling is
lifted (g = 1.66).** The 4b verdict on that book is a statement about where g = 1.00 sits, not
about the signal.

## (5) Census

1500 book-arm rows. 4a passes 316, 4b passes **64**. Of the 328 levered rows, **4b passes that
require leverage: 0** — leverage does not buy a single 4b pass anywhere in the corpus, it
removes them.

## Predictions, scored honestly

| | prediction | outcome |
|---|---|---|
| P1 | [a] exact, [b] reproduces 50/50 and ~46% | **HIT** |
| P2 | required gross > 1.00 for the majority, most of all in small-`k` cells | **HALF** — 55% majority is right, but the driver is small `n_elig` (all n=20 cells at 100%), not small `k` (k=20/n=5 is only 30%) |
| P3 | UNCAPPED: most CAGR-only failures flip to a 4b pass | **MISS — 0 of 38.** The mechanism in P5 was stronger than I priced it |
| P4 | CAPPED: few flip | **HIT** — 8 of 38 |
| P5 | the DD cap eats the gain; net pass count rises far less than the CAGR flips imply | **HIT, and understated** — the net *falls*, 42 → 2 |
| P6 | nothing is a KEEP; new passes would require leverage | **HIT on the first clause; the second is wrong-signed** — 0 passes require leverage because leverage destroys every pass |

3.5 of 6. P3 is a clean miss and is recorded as one.

## Verdict

**KILL of the artefact hypothesis as posed.** 4b's CAGR floor is gross-sensitive — that much of
idea 156's premise is right — but it is not separable from the drawdown cap, and removing it by
re-grossing simply relocates every failure onto the cap. No RULES change is requested; no new
book; no KEEP-candidate. The small-pool books remain outside 4b, and the reason is now exact
and quotable: **they would need a median 1.82x of gross to reach SPY's volatility.**

## Three clauses proposed to the Sunday review (no RULES change requested)

1. **State 4b's two risk bars as one joint constraint.** The φ = 0.70 CAGR floor and the
   δ = 0.60 drawdown cap together admit only books running materially *below* SPY's volatility.
   A book at SPY's vol fails the cap in 297 of 300 cases here. PROTOCOL should say this
   explicitly rather than let each run rediscover it.
2. **Record each book's required vol-matching gross alongside its 4b verdict.** It is one number
   (`0.75 × vol_SPY / vol_book`), it costs nothing, and it converts "fails on CAGR" into the
   actionable statement "would need 1.82x gross, which rule 2 forbids".
3. **Idea 148's ceiling clause should be strengthened.** `g = min(g_required, 1.00)` is not just
   a constraint — on the small-pool cell it is the only setting under which the book passes 4b
   at all (0% → 12% → 0% as the ceiling is applied and then lifted).

## Caveats carried

Survivorship: B136 is a current-constituent list (idea 54) and every sub-panel drawn from it
inherits that bias in full. VM_FULL is look-ahead by construction and is labelled contaminated
wherever it appears. Vol matching is not risk matching — that is the run's central finding, not
an oversight. Idea 144: a re-grossed book is the same book, so no verdict flip here is a new
signal. Idea 38 (calendar-day price index) and idea 126 (t+1 execution only) carry over. The
k=20 / n=20 cell holds every eligible name by construction, so its "selection" is a weighting
artefact — idea 78 flagged this and it is reported, not read as a selection result.
