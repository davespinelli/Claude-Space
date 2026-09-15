# Idea 879 — is the CAGR floor as convention-sensitive as the DD cap once its margins are centred?

**Lane B, 2026-09-15. ANSWERED: YES — the queue's premise is right, and the reason is worse than the
queue guessed: 4b's two LEVEL legs are ONE scalar read from two ends. KILL for capital. Nothing
promoted; RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py untouched (rule 6).**

SELECTION: idea 879 is the LAST entry under `## Open` and is lane B's claim by the sprint's own rule.
It has a price leg (books, calendars, both KEEP paths), so unlike 876/877 it carries rule 8 directly.

Script: `2026-09-15_is-the-CAGR-FLOOR-as-CONVENTION-SENSITIVE-as-the-DD-CAP-once-CENTRED_B.py`
Outputs: `.cells.csv` (48,840 rows) `.legs.csv` (19,800) `.centred.csv` `.loc.csv` `.walkforward.csv`
`.ladder.csv` `.console.txt` `.post.txt`

## What was run

**110 books × 26 calendars × 2 lags × 2 cost rungs × 3 windows = 48,840 cells, every one published.**
5 forms (MADG, TOP20, TOP40, EWELIG, RULESV2 — idea 808's six books are five forms, since its
MADG100/MADG075 are one form at two rungs of this very dial) × a FIXED gross ladder
g = 0.50…1.00 step 0.05 × panels U56 (`load_universe()`) and B136 (`load_universe(broad=True)`).
Calendars: 21 monthly trading-day offsets (idea 805/808's own family), the k ≤ 10 subset of it, and
5 weekly ones. Idea 808's own 12 books are 12 of these 110 — the (form, gross) pairs it declared —
taken out of the same grid rather than re-run, so gate G2 and every hypothesis read identical return
paths. SPY is a tradable constituent of both panels AND the 4b comparand (the record's construction,
not changed here).

Two tuned parameters, the queue's own: **margin band** {0.5, 1.0, 2.0} pp × **offset grid**
{MONTHLY-21, MONTHLY-11, WEEKLY-5}; all 9 points reported for every hypothesis. Panel, form, gross
rung, cost rung, lag, window and both KEEP paths are reported and never selected on.

## Gates

| Gate | Result |
|---|---|
| G1 engine | `fast_run` vs `engine.backtest` max abs diff **2.082e-17** (bar 1e-9) — PASS |
| G2 repro of 808 | **6 of 6 EXACT.** median ratio DD **0.46634** (published 0.466) / CAGR **0.87697** (0.877); books ratio<1 DD **10/12**, CAGR **8/12**; offset flips DD **52**, CAGR **3** — all on the nose |
| G3 bars | U56: SPY 15.13% / 0.885 / −33.72% → DD cap −20.23%, CAGR floor 10.59%; RULES v2 8.62% / 1.201 / −12.05%. B136: SPY 15.16% / 0.886 / −33.72% → cap −20.23%, floor 10.61%; RULES v2 7.98% / 1.099 / −12.24% |
| G4 census | band 0.5pp admits 11 CAGR-centred / **4 DD-centred (underpowered, flagged)**; 1.0pp admits 24 / 10; 2.0pp admits 48 / 19, of 110 |

## 1. H_RAW CONFIRMED — 808's 52-vs-3 is a LOCATION fact

Median |ratio| = |margin at k=0| / offset spread, MONTHLY-21, FULL, 10 bps, lag 1:

| book set | CAGR | DD | multiple |
|---|---|---|---|
| idea 808's own 12 books (the set the queue quotes) | **1.844** | **0.594** | **×3.10** |
| this run's 110-book gross grid | 1.934 | 0.737 | ×2.62 |

The shelf's CAGR margins sit three times further from their floor, in units of their own calendar
noise, than its DD margins sit from the cap. That, not a property of the leg, is what produced
52 flips against 3.

## 2. H_CONVERGE CONFIRMED — centre the CAGR leg and its flip rate multiplies by 25

Flip rate = offsets on which the leg's own pass/fail disagrees with PROTOCOL's own calendar (k=0).

| band | offset grid | CAGR-centred n / rate | DD-centred n / rate | gap |
|---|---|---|---|---|
| 0.5 | MONTHLY-21 | 11 / 0.528 | 4 / 0.417 | +11.1 pp |
| 0.5 | MONTHLY-11 | 11 / 0.405 | 4 / 0.500 | −9.5 pp |
| 0.5 | WEEKLY-5 | 16 / 0.225 | 5 / 0.520 | −29.5 pp |
| **1.0** | **MONTHLY-21 (headline)** | **24 / 0.296** | **10 / 0.333** | **−3.8 pp** |
| 1.0 | MONTHLY-11 | 24 / 0.235 | 10 / 0.309 | −7.4 pp |
| 1.0 | WEEKLY-5 | 27 / 0.141 | 8 / 0.400 | −25.9 pp |
| 2.0 | MONTHLY-21 | 48 / 0.163 | 19 / 0.298 | −13.6 pp |
| 2.0 | MONTHLY-11 | 48 / 0.127 | 19 / 0.234 | −10.8 pp |
| 2.0 | WEEKLY-5 | 50 / 0.076 | 18 / 0.278 | −20.2 pp |

The headline is inside the ±10 pp bar and **H_SPREADEQ (CAGR intrinsically safer) is REFUTED**. In
raw terms: on 808's own books the CAGR leg flipped **3 of 252** offsets (1.2%); on this 110-book grid
uncentred it flips **164 of 2,310** (7.1%); once centred at 1 pp it flips **149 of 504 (29.6%)** —
a 25× rise, landing within 3.8 pp of the DD leg's own centred rate.

**The honest qualification, stated rather than buried: only 3 of the 9 grid points sit inside the
bar.** Every WEEKLY-5 point has CAGR 20–30 pp below DD, and the 0.5 pp band is underpowered on the
DD side (4 books). The two families are not equivalent measurements: WEEKLY-5 resolves flips in
steps of 20% and its spreads are 0.37–0.70× the monthly ones (808's H_CADENCE), so a low weekly rate
is largely a resolution fact. The convergence claim is a MONTHLY claim, at the band the queue named.

## 3. H_LOC REFUTED — the single-index law breaks exactly where it matters

Flip rate binned on |ratio| alone, both legs pooled:

| |ratio| bin | CAGR n / rate | DD n / rate | gap |
|---|---|---|---|---|
| [0, .25) | 7 / **0.646** | 17 / **0.336** | **+31.0 pp** |
| [.25, .5) | 8 / 0.274 | 20 / 0.226 | +4.8 |
| [.5, .75) | 6 / 0.135 | 19 / 0.140 | −0.5 |
| [.75, 1) | 11 / 0.026 | 14 / 0.054 | −2.8 |
| [1, 1.5) | 10 / 0.000 | 20 / 0.000 | 0.0 |
| [1.5, 2) | 14 / 0.000 | 13 / 0.000 | 0.0 |
| ≥ 2 | 54 / 0.000 | 7 / 0.000 | 0.0 |

`R²(|ratio|) = 0.2860`, `R²(|ratio| + leg dummy) = 0.3081`, delta 0.0221 — inside the 0.05 bar — but
the bin test fails on one bin, **the tightest one**: at |ratio| < 0.25 the CAGR leg flips nearly
twice as often as the DD leg. So the two legs share one curve everywhere except at the bar itself,
where the CAGR leg is the MORE fragile of the two. A ratio ≥ 1 is a clean sufficient condition for
zero flips on both legs (0 flips in 118 book-legs), which is the one clause-shaped fact here.

## 4. The mechanism (post pass, `.ladder.csv`) — 4b's two level legs are ONE scalar

Across the 11-rung gross dial, per (panel, form), with 4b's own bars:

**corr(CAGR margin, DD margin) = −0.9997 to −0.9999 on all 10 cells**, while Sharpe moves by a
median sd of **0.0012 over the whole dial**. d(CAGR margin) per 5 pp of gross: +0.56 to +1.11 pp;
d(DD margin): −0.75 to −1.57 pp. Only **27 of 110** books have both level legs positive at all
(0 of 11 rungs on B136 EWELIG and B136 RULESV2).

The U56 TOP20 ladder — the record's own 2026-09-04 first KEEP 4b — shows it in one table:

| gross | 4b / 21 offsets | CAGR | Sharpe | MaxDD | m_CAGR | m_DD | offsets failing CAGR / DD |
|---|---|---|---|---|---|---|---|
| 0.50 | 0/21 | 9.71% | 1.200 | −13.40% | −0.89 | +6.83 | 21 / 0 |
| 0.55 | 2/21 | 10.70% | 1.200 | −14.65% | +0.10 | +5.58 | 19 / 0 |
| 0.60 | 16/21 | 11.69% | 1.201 | −15.89% | +1.10 | +4.34 | 5 / 0 |
| **0.65** | **21/21** | 12.69% | 1.201 | −17.11% | +2.09 | +3.12 | 0 / 0 |
| 0.70 | 16/21 | 13.69% | 1.202 | −18.32% | +3.09 | +1.91 | 0 / 5 |
| 0.75 (the shelf's KEEP) | 7/21 | 14.69% | 1.202 | −19.51% | +4.10 | +0.72 | 0 / 14 |
| 0.80 | 3/21 | 15.69% | 1.203 | −20.68% | +5.10 | −0.45 | 0 / 18 |
| 0.85 … 1.00 | 1/21 | 16.70 … 19.75% | 1.203 … 1.205 | −21.85 … −25.25% | +6.11 … +9.16 | −1.62 … −5.02 | 0 / 20 |

Sharpe is **flat to 0.005 across the entire ladder**. So "which leg is convention-sensitive" is not a
property of a leg at all: it is a read-out of where on one gross dial the book was parked. De-gross
and the CAGR leg becomes the fragile one; re-gross and the DD leg does. This subsumes the queue's
question and ideas 662/866/676/311/321's channel, now measured inside 4b's own two bars.

## 5. H_NOFREE REFUTED — but 21 of 24 centred books do fail the majority

3 of the 24 CAGR-centred books at the 1 pp band still pass 4b on a strict majority of their 21
calendars (U56 MADG@095 15/21, U56 RULESV2@095 14/21, U56 TOP40@080 14/21). Centring does not
mechanically make a verdict a coin toss, because a book can sit 1 pp above the CAGR floor with a
1.4 pp CAGR spread and clear it on most offsets anyway. The other 21 do fail it, and **60 of the
110 books pass 4b on 0 of 21 calendars**. 4a passes on **0** of the 24 centred books.

## 6. Rule 8 walk-forward — the SELECTOR does not transfer, the FINDING does

IS = window start…2016-12-31, fitted. OOS = 2017-01-01…, read once.

**H_WF REFUTED.** rho(IS CAGR margin, OOS CAGR margin) over the 110 books is **+0.932** and
rho(IS spread, OOS spread) **+0.963** — the RANKING is almost perfectly portable — but the LEVEL is
not, and the band is a level test: of the books centred in sample, still centred out of sample
**23.1% at 0.5 pp, 44.4% at 1.0 pp (bar 50%), 69.4% at 2.0 pp**. So "this book sits near the CAGR
floor" is not knowable before the outcome window is read at the band the queue named, and no clause
conditioned on it can be applied ex ante. That is the same shape as 808's finding on the DD leg.

**The result itself, however, walks forward cleanly.** Centring done on IS only, flip rates then read
on the OOS window's own offsets: gap CAGR − DD = **+2.0 pp (0.5), −2.9 pp (1.0), −5.6 pp (2.0)** —
inside the ±10 pp bar at all three bands, which the full-sample version manages at only 3 of 9 points.

### Rule 8 (b) — the books

Declared IS-ONLY selector: per (form, panel), the gross rung MINIMISING |CAGR margin| on IS.
MONTHLY-21 k=0, 10 bps, lag 1. OOS read once.

| panel | form | g*_IS | OOS CAGR / Sharpe / MaxDD | FULL CAGR / Sharpe / MaxDD | 4a | 4b |
|---|---|---|---|---|---|---|
| U56 | TOP20 | 0.65 | **14.38% / 1.281 / −17.11%** | 12.69% / 1.201 / −17.11% | ✗ | **✓** |
| U56 | TOP40 | 0.85 | 13.62% / 1.291 / −15.47% | 12.28% / 1.190 / −15.47% | ✗ | ✓ |
| U56 | RULESV2 | 0.95 | 12.17% / 1.225 / −17.93% | 11.29% / 1.173 / −17.93% | ✗ | ✓ |
| U56 | MADG | 0.95 | 11.97% / 1.266 / −14.76% | 11.30% / 1.208 / −14.76% | ✗ | ✓ |
| U56 | EWELIG | 0.75 | 12.98% / 1.216 / −17.01% | 11.79% / 1.139 / −17.01% | ✗ | ✓ |
| B136 | TOP40 | 0.60 | 11.57% / 1.097 / −19.32% | 11.18% / 1.102 / −19.32% | ✗ | ✓ |
| B136 | TOP20 | 0.50 | 10.32% / 0.995 / −18.00% | 10.72% / 1.089 / −18.00% | ✗ | ✓ |
| B136 | EWELIG | 0.70 | 11.21% / 1.074 / −20.32% | 10.86% / 1.064 / −20.32% | ✗ | ✗ |
| B136 | RULESV2 | 0.95 | 10.48% / 1.085 / −19.55% | 10.60% / 1.087 / −19.55% | ✗ | ✗ |
| B136 | MADG | 0.90 | 9.89% / 1.142 / −14.57% | 10.08% / 1.128 / −14.57% | ✗ | ✗ |

Comparands — U56 OOS: RULES v2 (live) 9.46% / 1.277 / −12.05%, SPY 15.27% / 0.874 / −33.72%.
B136 OOS: RULES v2 7.88% / 1.106 / −12.24%, SPY 15.33% / 0.877 / −33.72%.

Selected: **4a 0 of 10, 4b 7 of 10.** Unselected base rate over all 110 books at k=0:
**4a 4.5%, 4b 24.5%** (U56 4a 0.0% / 4b 40.0%; B136 4a 9.1% / 4b 9.1%). **BOTH paths: 0 of 110.**
The five 4a passes are all B136 MADG at g = 0.50–0.70, and every one of them misses the 4b CAGR
floor by 2.80–5.05 pp — de-grossing far enough to out-Sharpe the live book is de-grossing past the
return bar, the record's standing result.

**B136 TOP20@050 is the casualty that answers the queue's question with a name.** The IS-only
selector picks it; at PROTOCOL's own calendar it reads as a 4b PASS; its CAGR margin is **+0.10 pp**
against a 1.76 pp spread (ratio 0.060) and it **flips the CAGR leg on 20 of 21 offsets**, passing 4b
on **1 of 21** calendars. That is a published 4b pass that is a date, on the leg 808 found innocent.

Whole-grid 4b over all 2,310 monthly book-calendar cells: 332 (10 bps, lag 1), 288 (10 bps, lag 2),
235 (25 bps, lag 1), 212 (25 bps, lag 2); 4a 18 / 13 / 4 / 0. Robustness of the headline gap:
−3.8 pp (10 bps, lag 1), −28.4 (10, lag 2), −10.9 (25, lag 1), −36.8 (25, lag 2) — **at lag 2 the
convergence does not hold**, because the DD-centred set shrinks to 7 books and its rate rises.

## 7. The one 4b KEEP-candidate, and why it is not promoted

**U56 TOP20 at gross 0.65 is the only book of the 110 that passes 4b on all 21 monthly offsets**
(and at 25 bps 21/21, at lag 2 21/21, weekly 4/5) — and it is the IS-only pick, not a post-hoc
choice. FULL 12.69% / 1.201 / −17.11%, OOS 14.38% / 1.281 / −17.11%; margins H1 +0.256, H2 +0.374,
OOS +0.407, DD +3.12 pp, CAGR +2.09 pp; realised gross 0.623, turnover 3.76×/yr.
A memo with exact RULES wording is filed at
`2026-09-15_u56-top20-g065_4b_B_MEMO.md` and **explicitly does not propose adoption**, because
§4 is the reason it passes: it is the rung that maximises the smaller of two margins on a dial along
which Sharpe is flat to 0.005, it is **one rung wide** (0.60 → 16/21, 0.70 → 16/21, 0.75 → 7/21), it
fails 4a at every offset, its OOS CAGR (14.38%) is below SPY's (15.27%) and its OOS Sharpe (1.281)
ties the live book's (1.277). It is the shelf's existing TOP20 de-grossed, not a new edge.

## Verdict

**ANSWERED: YES. KILL for capital.** The CAGR floor is as convention-sensitive as the DD cap once
centred (29.6% vs 33.3% flip rate, gap −3.8 pp at the queue's own band and family), 808's 52-vs-3 is
a location artefact (|ratio| ×3.10), and the deeper reason is that the two level legs are one gross
scalar read from opposite ends (corr −0.9999 on 10 of 10 cells, Sharpe sd 0.0012 across the dial).
A clause conditioned on "near the floor" cannot be written, because being near the floor is not
knowable in sample (44.4% at the 1 pp band, bar 50%). The clause-shaped fact that survives is
|ratio| ≥ 1 — zero flips on both legs, 118 of 118 book-legs.

**PROPOSED, NOT APPLIED (rule 6):** 4b's level legs should be published as ratios, not booleans —
margin ÷ the book's own rebalance-calendar spread — and the DD-specific wording in idea 808's
proposed clause should be widened to both level legs. Deciding between that and 808's SD2 form is a
Sunday-review question, not this run's.

**LIMITS.** The centred sets are between-book comparisons: the gross dial moves both level margins at
once, so no single book can be centred on both legs and the like-for-like test has to be across
books. n is small at the tight band (11 CAGR / 4 DD at 0.5 pp, flagged underpowered). The WEEKLY-5
family and lag 2 both refuse the convergence and are printed rather than dropped. SURVIVORSHIP: U56
and B136 are CURRENT-constituent lists, so every CAGR is biased upward and both level bars are
easier here than on a point-in-time panel; the headline quantities are within-book spreads and flip
rates and are far less exposed than the levels in §6 and §7, which are not corrected for it.
Deterministic, standalone, no network; the post pass re-reads the committed `.cells.csv` read-only.
