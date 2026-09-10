# Idea 400 — census the record's ABSOLUTE thresholds for the firing-RATE artefact

**lane B, 2026-09-10** · script `2026-09-10_census-the-record-s-ABSOLUTE-thresholds-for-the-firing-RATE-artefact_B.py`

## VERDICT — **KILL of the queue's screening rule, and the record is CLEANER than the queue feared.**

The queue proposed: *"any claim whose cross-panel firing-rate spread exceeds idea 336's ABS
spread is a rate artefact until re-priced."* Run as written it flags **0 of the record's 7
genuinely published panel-level absolute cuts** at idea 336's median ABS spread (0.413) and
2 of 7 at its minimum (0.193). The rule is not adoptable for a second, worse reason: the
machine extraction it would have to run on is **17.9% precise**. No RULES change, no book
promoted, no KEEP claimed; RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py untouched.

## Gates — four, pre-registered, printed before any hypothesis number

| gate | value | bar | verdict |
|---|---|---|---|
| G1 `fast_backtest` vs `engine.backtest`, 6 real books, returns **and** turnover | **2.776e-17** | 1e-12 | PASS |
| G2 idea 486's U56/RULES v1 triple **at its own vintage 2026-09-08**: 6.4194% / 0.66110 / −13.8278% | **4.421e-07** | 1e-4 | PASS |
| G3 a clause forced always-ON reproduces the ungated EWALL parent | **0.000e+00** | 1e-15 | PASS |
| G4 all four panel statistics inside their domains, all 3 panels | **0** | — | PASS |

G2 is load-bearing on the panel stamp (idea 328/514): this run truncates all three panels to
the common last date **2026-09-04**, and the same book on the truncated U56 reads
6.4585% / 0.66470 / −13.8278% — a **3.605e-03** drift with MaxDD identical. The reproduction
gate therefore had to be run at the published vintage, and both numbers are published.

## B. The census, and why its output cannot be used raw

4,314 LEADERBOARD table lines scanned. 107 carry a panel-dependent statistic; **118 threshold
hits** extracted (15 flagged relative/quantile, **103 absolute**, 37 of those cross-panel).
39 absolute hits fall inside their family's domain — and every one of those 39 was **read by
hand** and committed to `.audit.csv`:

| class | n | what it is |
|---|---|---|
| **PANEL** | **7** | a real absolute cut on a panel-AGGREGATE statistic — the thing idea 336 priced |
| **NAME** | **12** | a real absolute cut applied per NAME in the cross-section (all 12 are `vol20 < 0.60`) |
| **FALSE** | **20** | not a threshold at all — a reported level (`breadth flat 0.6821→0.6750`), a range, a regression loading (`breadth l=0.58`), a gross formula (`g = 0.75 × vol_spy/vol`), a Sharpe compare (`h1 1.294 > 0.959`), a between-book correlation (idea 103's `corr<0.20` is the arm's correlation with S9, not a panel statistic) |

**Machine precision 7/39 = 17.9%** for "absolute cut on a panel statistic", 48.7% for "a
genuine absolute cut of any kind". A screening rule that fires on the raw extraction would
re-price five wrong things for every right one. That is the primary reason the queue's rule
is KILLed rather than adopted.

## C. The answer — the 7 audited published cuts, and their realised firing rate

| line | cut | U56 | B136 | SMALL439 | spread |
|---|---|---|---|---|---|
| 4340 | `breadth >= 0.20` | 0.9732 | 0.9725 | 0.9631 | 0.0101 |
| 4365 | `breadthcash@0.30` | 0.9376 | 0.9410 | 0.8866 | 0.0543 |
| 3088 | `breadth gate b=0.40` | 0.8898 | 0.8998 | 0.7603 | 0.1395 |
| 3115 | `breadth gate b=0.40 depth 0.50` | 0.8898 | 0.8998 | 0.7603 | 0.1395 |
| 2795 | `breadth<0.5` (classifier) | 0.8439 | 0.8581 | 0.5541 | **0.3039** |
| 2812 | `breadth<0.5` (cap-mix line) | 0.8439 | 0.8581 | 0.5541 | **0.3039** |
| 4251 | `c_bar >= 0.5` | 0.8968 | 0.8824 | 1.0000 | 0.1176 |

**0 of 7 exceed 0.413** (idea 336's median ABS spread, the pre-registered bar); **2 of 7**
exceed its minimum 0.193; **0 of 7** exceed its maximum 0.686.

**But the record is lucky, not careful.** Over the full dial — the 4 families × the union of
a pre-registered ladder and every census level, **37 cells, all reported** in `.rates.csv` —
**14 of 37 (37.8%) exceed the bar**: DISP 4/7 (max 0.8964 at `disp<0.10`), VOL20 4/8 (max
0.8118 at `vol20<0.25`), BREADTH 4/11 (max 0.5126), CORR 2/11 (max 0.6408). The record's
published cuts happen to sit in the loose part of every dial, where all three panels fire
86–97% of days. That is a different pathology — **an inert clause**, not a rate artefact —
and `breadth >= 0.20`, the record's own 4b passer at line 4340, fires on 96–97% of days on
every panel.

**The most-cited cut is one rung from the cliff.** `vol20 < 0.60` (12 of the 39 hits) is a
per-NAME filter, so the panel-median denominator is the wrong one; on its own denominator —
the cross-sectional admission share — it reads 0.9593 / 0.9642 / 0.7835, spread **0.1807**,
under the bar. Its own ladder crosses the bar at the very next rung: `vol20 < 0.30` reads
0.7568 / 0.7419 / 0.3029, spread **0.4539**.

## The mechanism generalises even where the spread does not

Decomposing each cell's Sharpe against its ungated EWALL parent as `total = rate + form`
(rate = a per-panel frozen level at the pooled rate, look-ahead control; form = what the
absolute level adds at that same rate), over the 56 material cells of 111: median |rate|
**0.2371** vs median |form| **0.1423**, median **rate_share 60.0%** full-sample / **52.6%**
OOS. By family: BREADTH **84.4% / 70.8%**, CORR 58.8% / 60.6%, DISP 60.0% / 43.7%, VOL20
43.8% / 41.3%. Idea 336's finding — that what an absolute cut buys is mostly the admission
*rate* — reproduces on three new families and holds even at the levels whose cross-panel
spread is small.

## KEEP paths (PROTOCOL 4) over all 333 books — every grid point reported

333 books = 3 panels × 4 families × (5 ladder ∪ census levels) × 3 arms (ABS / CQTL / MATCH),
EWALL gross 0.75, de-gross to cash, weekly, 10 bps, t+1.

**4a 1/333. 4b 50/333.** The single 4a passer is SMALL439 `BREADTH@0.675` ABS — 4.1% / 0.788
/ −8.95%, H1 0.785 / H2 0.794, on-share 18.3% — a book held in cash four days in five, which
fails 4b on CAGR alone (4.1% against the 0.70 × 14.13% = 9.9% floor). Of the 50 4b passers,
35 beat their own ungated EWALL parent's full-sample Sharpe and 25 beat RULES v2's; every one
buys the DD leg by de-grossing (the ungated parents themselves fail 4b on DD: −22.5% / −25.4%
/ −36.2% against the −20.2% cap). Passes split ABS 19 / CQTL 17 / MATCH 14 and **0 of 111 on
SMALL439**, the same U56 ≈ B136 ≫ SMALL ordering ideas 51/312/316/322 keep finding.

## Rule 8 (PROTOCOL 8) — (family, level) chosen on IS ≤ 2016-12-31 by IS Sharpe, 2017+ read once

Tradable arms only; MATCH is a look-ahead control and is excluded from the chooser.

| panel | arm | pick | IS Sh | OOS CAGR / Sharpe / MaxDD | own parent OOS | RULES v2 OOS | SPY OOS | full (H1/H2) | 4a | 4b |
|---|---|---|---|---|---|---|---|---|---|---|
| U56 | ABS | CORR@0.5 | 1.2495 | 10.36% / **1.0540** / −22.91% | 1.1404 (13.86%) | 1.2851 | 0.8820 | 11.34% / 1.1426 / −22.91% (1.339/0.961) | no | no |
| U56 | CQTL | CORR@0.3436 | 1.2315 | 9.10% / **1.1016** / −11.51% | 1.1404 | 1.2851 | 0.8820 | 10.20% / 1.1622 / −12.04% (1.331/0.986) | no | no |
| B136 | ABS | VOL20@0.3 | 1.3529 | 8.55% / **0.9399** / −16.96% | 1.1038 (13.95%) | 1.1185 | 0.8820 | 10.69% / 1.1309 / −16.96% (1.463/0.807) | no | no |
| B136 | CQTL | CORR@0.3436 | 1.2504 | 9.13% / **1.0771** / −11.46% | 1.1038 | 1.1185 | 0.8820 | 10.68% / 1.1587 / −13.27% (1.362/0.938) | no | **yes** |
| SMALL439 | ABS | BREADTH@0.4 | 0.9138 | 5.30% / **0.4886** / −28.25% | 0.6367 (10.09%) | 0.5680 | 0.8820 | 6.74% / 0.6316 / −28.25% (0.841/0.471) | no | no |
| SMALL439 | CQTL | BREADTH@0.5 | 0.9998 | 5.31% / **0.5045** / −27.54% | 0.6367 | 0.5680 | 0.8820 | 6.62% / 0.6575 / −27.54% (0.951/0.455) | no | no |

**4a 0/6. 4b 1/6, and it is NOT filed as a candidate.** B136 CQTL CORR@0.3436 loses out of
sample to its own ungated EWALL parent (1.0771 vs **1.1038**, and 9.13% vs **13.95%** CAGR)
and to the live RULES v2 book (1.1185) — it fails the parents test idea 317/322 proposed as
PROTOCOL 4c, and its level 0.3436 is a number the census scraped out of a *reported* value in
idea 277's row, not a threshold anyone chose. Every one of the six IS-chosen clauses loses to
its own ungated parent on OOS Sharpe **and** OOS CAGR: the chooser is buying drawdown with
return, in every cell, on every panel.

## What this run proposes (not applied, Sunday review's call)

1. **Do not adopt the queue's screening rule as stated.** On the record's audited absolute
   cuts it flags nothing at the bar it names, and the extraction it depends on is 17.9%
   precise. The re-pricing it would trigger is mostly re-pricing false positives.
2. **Publish the realised firing rate beside any absolute cut, in place of the rule.** Two
   columns — `rate` per panel and `spread` — are cheap, exact, and settle both pathologies at
   once: a spread above 0.19 marks a rate artefact, and a min-panel rate above 0.90 marks an
   inert clause. On the audited seven this run finds one of each.
3. **Name the denominator.** 12 of the 39 in-domain hits are per-NAME cuts whose panel-median
   rate is meaningless; `vol20 < 0.60` reads 0.18 spread on the right denominator and would
   have read 0.04 on the wrong one.

## Caveats

All three panels are current-constituent lists (SURVIVORSHIP), so 4b's CAGR floor is tested
in the book's favour; SMALL439 = 44 names with `max_1d_move >= 1.0` dropped from the 484-name
sub-$2B screen, per `data/SMALL_PANEL_README.md`. SMALL439's halves are not calendar-aligned
with U56/B136's (it starts 2010-01-04). The MATCH arm carries look-ahead in its level by
construction and is a control only — it never enters the rule-8 chooser. The census covers
`research/LEADERBOARD.md` only, not CHANGELOG.md or the per-idea `.result.md` files, and its
recall is unmeasured: the 17.9% figure is precision, and a hit the regex never made would not
appear anywhere in this run. **Line numbers are a vintage, not an identifier:** every `line`
in `.census.csv` / `.audit.csv` / `.audited_rates.csv` indexes `LEADERBOARD.md` as it stood at
commit `77db351` (4,314 table lines), before this run's own six rows and lane A/C's same-day
rows were appended. Re-running the script against a later LEADERBOARD will shift them, and the
hand-audit table is keyed on those numbers — so the audit must be re-keyed, not merely re-run,
if the census is ever repeated.

**Artefacts:** `.gates.csv` `.census.csv` (118 rows) `.audit.csv` (39 rows, hand-classified)
`.rates.csv` (37 cells) `.audited_rates.csv` (7) `.pername.csv` (5) `.books.csv` (333)
`.decomp.csv` (111) `.walkforward.csv` (6) `.console.txt`.
