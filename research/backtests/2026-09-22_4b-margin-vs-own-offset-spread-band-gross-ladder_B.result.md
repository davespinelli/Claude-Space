# Idea 2119 (lane B, 2026-09-22) — how many 4b PASSES on a BAND × GROSS ladder survive their own OFFSET SPREAD?

**Script:** `research/backtests/2026-09-22_4b-margin-vs-own-offset-spread-band-gross-ladder_B.py`
**Console:** `…_B.console.txt` · **Artifacts:** `.grid.csv.gz` (3,000 rows, every point — the script writes it uncompressed and it is committed gzipped), `.spreads.csv.gz`, `.summary.csv`, `.costladder.csv`, `.walkforward.csv`, `.gates.csv`

## ANSWER — SPLIT, AND NO NEW KEEP.
1. **914's fragility does NOT generalise as a DD-leg fact.** 12 of the 16 d=0 4b passes (FULL+OOS, both panels, 10 bps) have a DD margin **bigger** than their own five-offset weekday spread. The record's DD margins are mostly real.
2. **It DOES generalise as a VERDICT fact.** Only **6 of 16** clear the spread on *every* leg and only **7 of 16** are still a 4b PASS at 5 of 5 offsets. Per leg: H1 16/16, H2 16/16, **DD 12/16, CAGR 9/16**.
3. **The one cell rule 8 can actually reach is, on BOTH panels, exactly a weekday-contingent pass.** KILL as a KEEP; PARK with the wording in the memo.

## Gates (printed before any hypothesis was read)
| gate | result | bar | |
|---|---|---|---|
| G2 | 0 differing rows | `offset_mask(idx,0) == engine.rebalance_mask(idx,'W')` | PASS |
| G3 | max\|d\| **0.000e+00** | ladder cell (0.03, 0.75) == `baseline.rules_v2_weights` | PASS |
| G1 | max\|d\| **0.000e+00** over 4,706 rows | local `run()+net()` == `engine.backtest` | PASS |
| G4a | d0..d4 = 52.3 trades/yr each | 50–53 | PASS |
| G4b | clipped weeks d0/d1/d2/d3/d4 = 0/0/0/**2**/**175** | 0 | **FAIL — structural** (short holiday weeks); published, and every headline is re-read clip-free on {0,1,2} as B1c rather than the bar being widened |
| G5 | `rules_v2_weights` + SPY buy-and-hold | baseline's own | PASS |

4 of 5. G4b's failure is a property of the calendar, not of the run; B1c moves no conclusion (U56 OOS DD 5/6 → 5/6, all-leg 4/6 → 4/6).

## B1 / B2 / B3 — the filed question (d=0, 10 bps)
| panel | window | 4b pass | B1 DD | B1 CAGR | B2 all-leg | B3 5-of-5 offsets |
|---|---|---|---|---|---|---|
| U56 | FULL | 5 | 4/5 | 3/5 | 2/5 | 3/5 |
| U56 | IS | 1 | 0/1 | 0/1 | 0/1 | 0/1 |
| U56 | OOS | 6 | 5/6 | 5/6 | 4/6 | 4/6 |
| B136 | FULL | 4 | 3/4 | 1/4 | 0/4 | 0/4 |
| B136 | IS | 4 | 3/4 | 1/4 | 0/4 | 0/4 |
| B136 | OOS | 1 | 0/1 | 0/1 | 0/1 | 0/1 |

**Every one of the 16 FULL+OOS passes sits at gross = 1.00.** De-grossing below 1.00 kills the CAGR floor on both panels at every band — the DD leg is never what stops a de-grossed cell.

There is a clean trade-off along the band axis, and it is why the all-leg clause bites:
small bands (0.00–0.05) buy a large DD margin (+2.9 to +4.6 pp) and a razor-thin CAGR margin
(+0.02 to +0.9 pp); the widest band (0.08) reverses it (DD +0.73 to +1.18 pp, CAGR +0.30 to
+1.30 pp). **No cell on either panel has both margins comfortably clear of their spreads except U56 band 0.02 and 0.03 at gross 1.00.**

## B4 — cost ladder (0/10/25/50 bps)
Monotone and unhelpful to the candidate: U56 FULL passes 5 → 5 → 4 → 1; B136 OOS 4 → 1 → 1 → 0.
The B1 DD share is stable (U56 OOS 6/7, 5/6, 4/5, 3/4), so nothing here is a cost story.

## B5 — RULE 8 (band, gross chosen on IS Sharpe only, 2017–2026 read ONCE, 10 bps)
| | CAGR | Sharpe | MaxDD | H1 / H2 |
|---|---|---|---|---|
| **U56 pick** band 0.08 / gross 1.00 — OOS | **12.00%** | **1.1625** | **−19.05%** | 1.267 / 1.048 |
| RULES v2 (live) — OOS | 9.46% | 1.2767 | −12.05% | 1.432 / 1.106 |
| SPY — OOS | 15.29% | 0.8751 | −33.72% | 0.991 / 0.750 |
| **B136 pick** band 0.08 / gross 1.00 — OOS | **10.98%** | **1.0921** | **−19.50%** | 1.230 / 0.934 |
| RULES v2 (live) — OOS | 7.85% | 1.1017 | −12.24% | 1.291 / 0.878 |
| SPY — OOS | 15.26% | 0.8737 | −33.72% | 0.991 / 0.747 |

FULL: U56 11.37% / 1.1445 / −19.05%; B136 11.35% / 1.1150 / −19.50%.
**4b PASS on FULL, IS and OOS on both panels; 4a FAIL on both** (the live book's Sharpe is higher in both halves and its drawdown is 7 pp shallower).

**And that pass is a weekday.** On both panels the DD margin is *inside* its own spread —
U56 **+1.180 pp vs 2.136 pp**, B136 **+0.730 pp vs 2.078 pp** — and moving the rebalance one
trading day earlier (d=1) flips MaxDD to **−20.32%** (U56) and **−20.65%** (B136) against the
−20.23% cap, i.e. **4b FAIL at d=1 on both panels in both windows**. This is precisely the
condition under which idea 914 killed idea 910's candidate this morning; applied consistently,
it denies this one.

## The rule-8 chooser cannot see the dial that decides the verdict
IS Sharpe moves **0.0013** (U56) / **0.0026** (B136) across the *whole* gross ladder at a fixed
band, against 0.0684 / 0.0874 across the grid. Gross is invisible to the chooser — yet at band
0.08 **only** gross = 1.00 clears 4b, every lower rung failing the CAGR floor. The chooser
resolves band, is indifferent to gross, and the cell it lands on is the single one on the ladder
whose DD margin is smaller than its own weekday noise. Idea 1713/1715's "the IS objective cannot
see the dial it is picking" reproduced on a new family.

## B8 — the two cells that survive everything, and why they are not a KEEP
| panel | band | gross | FULL | OOS | IS 4b | IS Sharpe rank |
|---|---|---|---|---|---|---|
| U56 | 0.02 | 1.00 | 11.33% / 1.1934 / −15.65% | 12.53% / 1.2784 / −15.65% | FAIL | 11 of 25 |
| U56 | 0.03 | 1.00 | 11.53% / 1.2009 / −15.91% | 12.67% / 1.2760 / −15.91% | FAIL | 6 of 25 |

Both clear every leg's own spread and stay a PASS at 5 of 5 offsets on FULL *and* OOS — the only
2 of 50 cells that do. **Neither is reachable**: both FAIL 4b in the IS window (U56 0.03/1.00 IS
CAGR margin −0.31 pp) and neither is the IS-Sharpe argmax. Selecting them requires having read
2017–2026, so under rule 8 they are PARK, not KEEP, and they are reported rather than proposed.

## The live book's own cell (band 0.03 / gross 0.75)
FAILS 4b on the **CAGR floor alone**, on both panels in every window — margins −1.98 / −1.25 pp
(U56 FULL/OOS) and −2.63 / −2.83 pp (B136) — while its DD margin is **+8.18 pp / +7.99 pp**, four
times its own 1.80 / 1.70 pp weekday spread. Idea 1454's reading reproduced exactly: the live
book's one failing leg is return, not risk, and the drawdown budget it is not spending is real
(it is far outside the scheduling noise), not an artefact of which weekday it trades.

## What this run cannot do (stated, not repaired)
One book FORM (RULES v2's band + equal weight + de-gross), one cadence (weekly), one offset
family (the 5 weekday phases of a weekly rebalance); monthly and quarterly books are not priced
here and a different form could carry different spreads. The 16-pass population is this ladder's,
not a harvest of the record's committed passes, so B1's 12/16 bounds *this* family and does not
re-score any previously published verdict. **SURVIVORSHIP (rule 9):** U56 and B136 are
current-constituent lists, so every absolute level is optimistic; the offset contrast is
within-tape — same names, same dates, only the weekday moves — and does not repair the level.

## Verdict
**KILL** for capital. No new KEEP, no RULES change (rule 6; RULES.md, PROTOCOL.md, scan.py,
bot.py and baseline.py untouched). One PARK memo filed for the rule-8 pick.
