# Idea 996 (cloud lane, 2026-09-16) — census the record's SCREENED statistics for a NAMED FALLBACK

**ANSWERED = THE RECORD DOES NOT NAME ITS FALLBACK. 180 of 1,039 committed screened
statistics (17.3%) name one; 859 (82.7%) are surviving-picks-only by construction. KILL for
"a published screened gain is a number as quoted" — the same screen reads +0.1429 under the
incumbent convention and −0.4689 with the refusal paid to cash, and the SIGN flips in 31 of 45
(screen, chooser, cost) cells. KILL for "screening buys a certification" (the headline screen
gets 3 OOS 4b passes in 72 against the unscreened control's 5). KEEP as a PROTOCOL rule 4
reporting clause, PROPOSED and not applied (rule 6). Nothing promoted.**

Script: `2026-09-16_census-the-record-s-SCREENED-statistics-for-a-NAMED-FALLBACK_cloud.py`
Artifacts: `.census.csv`, `.census_by_source.csv`, `.census_claims.csv` (6,841 claim units),
`.ladder.csv` (600 rows), `.picks.csv` (1,080), `.paid.csv` (180), `.gates.csv`,
`.hypotheses.csv`, `.console.txt`.

## Gates — 10 of 10 PASS, printed before any hypothesis number

| gate | what | value | bar |
|---|---|---|---|
| G0 | offset-0 mask ≡ `engine.rebalance_mask` on D/W/M/Q | 0 rows | 0 |
| G1 | fast `Ctx` ≡ `engine.backtest` (returns **and** turnover) | 1.67e-16 | 1e-10 |
| G2 | `BAND03@0.75` ≡ `baseline.rules_v2_weights` | 0.00e+00 | 1e-12 |
| **G3** | **CROSS-RUN: idea 993's committed 13,500-row ladder, all 600 phase-0 rows × 14 cols** | **7.11e-15** | 1e-9 |
| G4a | `FB_CASH` is exactly a zero return series | 0.00e+00 | 1e-12 |
| G4b | `FB_SPY` is exactly the panel's SPY series | 0.00e+00 | 1e-12 |
| G4c | `FB_LIVE` ≡ this run's own (BAND03, CORE, W) row, post warm-up | 1.04e-17 | 1e-12 |
| G5 | determinism: U56/TOP20/CORE/M rebuilt from scratch | 0.00e+00 | 0 |
| G6 | SMALL hygiene: `max_1d_move >= 1.0` tickers dropped | 52 | ≥1 |
| G7 | census parse determinism (differing cells on re-parse) | 0 | 0 |

G3 is the load-bearing one: idea 993's ladder reproduces **exactly** on today's tree, so the
ladder this run screens over is the record's own object and not a look-alike.

## (A) The census — 1,039 STRICT screened statistics, 17.3% name a fallback

Claim unit = one LEADERBOARD table row or one CHANGELOG paragraph (6,841 units parsed: 6,360 LEADERBOARD rows + 481 CHANGELOG paragraphs).
Vocabularies were fixed before the corpus was read and are printed verbatim in the console log.

| claim set | claims | name a fallback | surviving-picks-only | explicit surv. vocabulary | locatable on disk |
|---|---|---|---|---|---|
| STRICT (quotes a numeric screened statistic) | 1,039 | 180 (**0.1732**) | 859 (**0.8268**) | 3 | 987 (0.9500) |
| WIDE (any screen/eligibility/decline claim) | 1,149 | 200 (0.1741) | 949 (0.8259) | 4 | 1,082 (0.9417) |

**The defect is concentrated in the TABLE, not the prose.** LEADERBOARD rows name a fallback on
**123 of 927 (13.3%)**; CHANGELOG paragraphs on **57 of 112 (50.9%)** — the narrative record is
nearly four times as complete as the leaderboard that is supposed to be the machine-readable
one. Only **3 of 1,039** claims use surviving-picks vocabulary explicitly, so the convention is
almost never stated even when it is in force: the 859 figure is what the record *does*, not what
it *says*.

- `H_NAMED` **FAILS at 0.1732** (bar 0.50) — 993's defect is the record's default, not an outlier.
- `H_SURV` **PASSES at 0.8268** (bar 0.50).
- `H_LOC` **PASSES at 0.9500** (bar 0.25) — the corpus is re-scorable; what is missing is the
  convention, not the data.

## (B) The price — the fallback is load-bearing, and it flips the sign

24 SLOTS = (3 panels × 4 cadences × 2 gross). Inside a slot the five books (TOP05/TOP10/TOP20/
EWELIG/BAND03) are the candidates. The CONTROL takes the IS-best of all five; the SCREENED arm
takes the IS-best of the ADMITTED ones and REFUSES the slot when nothing is admitted. All
admission and all choosing read 2009–2016 only.

Headline cell (`S_IS4B` × `C_SHARPE` × 10 bps), 15 of 24 slots refused:

| fallback | slots in the denominator | mean ΔSharpe | median ΔSharpe | win rate | mean ΔCAGR | mean Δ&#124;MaxDD&#124; |
|---|---|---|---|---|---|---|
| **FB_DROP** (incumbent) | 9 | **+0.1429** | +0.0801 | 0.556 | −0.0193 | −0.0432 |
| FB_CASH | 24 | **−0.4689** | −0.5487 | 0.208 | −0.0600 | −0.1368 |
| FB_SPY | 24 | +0.0780 | +0.1059 | 0.583 | +0.0356 | +0.0740 |
| FB_LIVE | 24 | +0.0986 | +0.0005 | 0.625 | −0.0195 | −0.0558 |

- `H_DROP` **PASSES at 0.6118** (bar 0.10): the incumbent free-refusal convention overstates the
  headline gain by **0.61 Sharpe units** against cash. Over all 45 (screen, chooser, cost) cells
  the overstatement runs **median +0.0812, max +0.8784, min 0.0000** against FB_CASH, and
  **−0.0315 / −0.0260 median** against FB_SPY / FB_LIVE — i.e. FB_DROP is not uniformly
  optimistic, it is *uninterpretable*: it sits above cash and slightly below the two invested
  fallbacks, and which way it errs depends on what the capital would otherwise have done.
- `H_SIGN` **PASSES at 31 of 45 cells**: the sign of the published gain flips with the fallback
  in more than two thirds of this grid. A screened gain quoted without its fallback is not a
  weak number; it is not a number.
- `H_PAID` **FAILS at −0.4689**: the headline screen's gain is **negative** once the refusal is
  paid to cash. Screening is not free.
- The gap is **cost-monotone and survives every rung**: FB_DROP − FB_CASH runs
  **+0.4631 / +0.4952 / +0.6118 / +0.8112 / +0.8784** at 0 / 5 / 10 / 25 / 50 bps.

## (C) Rule 8 — every pick is IS-only, the OOS window is read once

| screen | OOS 4b, screened | OOS 4b, control | OOS 4a |
|---|---|---|---|
| `S_IS4B` (headline) | **3 of 72** | 5 of 72 | 0 |
| `S_ISSHARPE` | 7 of 72 | 5 of 72 | 0 |
| `S_ISDD` | **10 of 72** | 5 of 72 | 0 |

`H_4B` **FAILS at −1**: the headline screen loses two certifications relative to doing nothing.
The one screen that beats the control is `S_ISDD` (10 vs 5) — **reported, not selected**; it is
one of three published screens and adopting it would be a third tuned dial. Even `S_ISDD` costs
mean ΔSharpe under FB_CASH at one of the three choosers (−0.0872 at `C_ISLEGS`).

Ladder-wide at 10 bps: **OOS 4b 7 of 120 rows, OOS 4a 0 of 120.** The 9 4a passes elsewhere in
the 600-row ladder are all `BAND03/CORE` at **0 and 5 bps** — the live book itself priced more
cheaply than the 10-bps baseline it is compared against, which is an accounting artefact and not
an edge. At the protocol's own cost rung there are none.

**The best screened pick, for completeness** — `U56 / BAND03 / EXT (gross 1.00) / M`, reached by
`S_IS4B` + `C_SHARPE` on 2009–2016 alone: full **11.89% / 1.1731 / −18.81%**, halves
**1.2193 / 1.1357**, **OOS 12.81% / 1.2245 / −18.81%**, 1.64 turns/yr, **OOS 4b PASS, 4a FAIL**.
SPY: full 15.10% / 0.8830 / −33.72% (halves 0.9591 / 0.8208), OOS 15.21% / 0.8713 / −33.72%.
RULES v2 (live): Sharpe 1.2009, MaxDD −12.05%, halves 1.2325 / 1.1762. **This is not a new
candidate** — it is the live band book at gross 1.00, i.e. a monthly point inside the gross
window idea 997 already published on U56 ([1.05, 1.25] on B136, g_CAGR 0.85 / g_DD 1.25 on U56),
and it is quoted here only as corroboration at a cadence 997 did not reach.

## The clause this proposes — for Sunday review, NOT written into PROTOCOL.md (rule 6)

> *"Every screened, eligibility-gated or decline-based statistic states its FALLBACK: what the
> capital does in a slot the screen refuses. The four legal values are `FB_CASH`, `FB_SPY`,
> `FB_LIVE` and `FB_DROP`, and `FB_DROP` — the refused slot leaving the denominator — is
> reportable only beside at least one paid fallback, because it is neither an upper nor a lower
> bound: on this grid it runs +0.08 Sharpe above cash (max +0.88) and −0.03 below SPY and the
> live book, and the sign of the gain flips with the fallback in 31 of 45 cells. A screened
> statistic published without a fallback is a surviving-picks statistic whether or not it says
> so; 859 of the record's 1,039 are."*

## Survivorship (rule 9)

U56 / B136 / SMALL are CURRENT-CONSTITUENT lists; SMALL additionally drops the **52** tickers
with `max_1d_move >= 1.0` per `data/small_meta.csv`. Every CAGR and drawdown LEVEL quoted here
is optimistic and every 4b count is an UPPER bound, most severely on SMALL. The measured object
is a DIFFERENCE between a screened and an unscreened chooser over the SAME names on the SAME
tape, so the bias is shared by both arms and very largely cancels; the LEVELS quoted for
`U56/BAND03/EXT/M` do NOT cancel and are stated as upper bounds.
