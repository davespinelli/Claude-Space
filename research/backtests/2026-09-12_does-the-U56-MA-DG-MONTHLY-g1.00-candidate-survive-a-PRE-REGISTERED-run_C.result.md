# Idea 805 (lane C, 2026-09-12) — does the U56 / MA-DG / MONTHLY g=1.00 candidate survive a pre-registered run?

**VERDICT: PARK, not KEEP. 5 of 6 pre-registered hypotheses pass; the one that fails is the one the
4b verdict rests on.** No RULES change, no KEEP claimed, no PROTOCOL edit applied (rule 6).
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py untouched.

## The book, fixed before any number was read
U56 (56 names, `research/universe.json`, SPY tradable as well as comparand — 804's construction,
unchanged) / **MA-DG**: `w = g/N` over every priced name, zeroed to **cash** where the name is below
its 200-day MA (never re-spread) / **MONTHLY** last-trading-day rebalance / next-day fills / 10 bps.
Gross is the only dial. **G2 reproduces idea 804's published triple field-by-field** (max deviation
7.4e-04 on OOS Sharpe, against a 5e-03 tolerance set by the 2-dp precision of the published number).

## What survived
| arm | result |
|---|---|
| **gross band** | `{0.90, 0.95, 1.00}` — **exactly** idea 804's published band. Choosing this book off a 50-book grid did not read a neighbour. |
| **cost** | 4b passes at every rung 0–50 bps; **breakeven 70 bps per unit turnover, 7× PROTOCOL** (failing leg: CAGR). Turnover is only 1.98×/yr. |
| **execution delay** | 4b passes with the fill delayed 1 and 2 extra trading days; lag 2 *improves* OOS Sharpe to 1.284 and MaxDD to −13.64%. Not a same-day-close artefact. |
| **rule 8** | IS-SHARPE and IS-BAND-MIDPOINT, both fitted on ≤2016 alone, both pick **g = 1.00**; OOS passes all five 4b legs. The IS band `{0.95, 1.00}` is *narrower* than the OOS band `{0.90, 0.95, 1.00}`, so IS was the stricter window. |

## What killed it
Shift the monthly rebalance **k trading days off month end** (k = 0…20 — 21 conventions, all equally
arbitrary, none of them a parameter of the rule):

* 4b passes at **13 of 21 offsets (61.9%)**, against a pre-declared 90% bar → **H_CAL FAILS**.
* All 8 failures die on the **DD leg alone**, MaxDD −20.50% … −23.85% against the −20.23% cap,
  in one contiguous block k = 9…16.
* **DD-cap margin at k=0 is 4.74 pp; the calendar spread in MaxDD is 8.37 pp.** The margin is
  smaller than the convention floor, so the leg is not measurable at this cadence.
* The band itself is a calendar object: width 3 at k=0, 4 at k=7, 1 at k=9, **EMPTY at k = 11…16**.
* CAGR is by contrast stable (1.51 pp spread; the worst offset still clears the floor by +0.43 pp)
  and **no Sharpe leg fails at any offset**.

This matters because the drawdown cap is the *only* 4b leg this book beats SPY on — it gives up
3.24 pp of CAGR (11.92% vs 15.16%) and buys a −15.49% drawdown against SPY's −33.72%. A drawdown
advantage whose measurement error exceeds its margin is not an advantage you can size.

## Numbers (PROTOCOL cell: g=1.00, 10 bps, next-day fill, month-end)
| | CAGR | Sharpe | MaxDD | H1 / H2 |
|---|---|---|---|---|
| candidate, full | 11.92% | 1.210 | −15.49% | 1.258 / 1.166 |
| candidate, OOS 2017– | 12.65% | 1.269 | −15.49% | — |
| SPY, full | 15.16% | 0.886 | −33.72% | 0.960 / 0.826 |
| SPY, OOS | 15.33% | 0.877 | −33.72% | — |
| RULES v2 (live), full | 8.63% | 1.20 | −12.05% | 1.235 / 1.176 |
| RULES v2 (live), OOS | 9.47% | 1.278 | −12.05% | — |

**KEEP paths:** 4b passes 44 of 357 main-grid cells and 63 of 714 offset cells; 4a passes 12 of 357
and **fails at the PROTOCOL cell** (RULES v2's −12.05% MaxDD is tighter). BOTH: 0.

## Disclosed change to a gate
G2 was written with a single 5e-04 bar on every field and read FAIL at 7.41e-04. That bar is tighter
than the 2-dp precision of the published Sharpe ("1.27"), so no reproduction however exact could
meet it — a defect of the bar, not a disagreement about the book. It was re-specified to half a unit
in the last published digit per field and the original reading is printed beside it in the console
log. No leg, hypothesis or verdict depends on either bar.

## Survivorship
U56 is the **current** constituent list. Dead names are absent, so every CAGR here is biased upward
and the 4b CAGR floor (0.70 × SPY's own survivor-free CAGR) is easier to clear than on a
point-in-time panel. The DD cap is biased the same way. Nothing above is corrected for this.

## Follow-up (queued, not done here)
1. Publish the **rebalance-offset spread beside every monthly 4b claim** on the record, as the
   weekday-offset convention floor already is for weekly books.
2. Re-run this book as a **21-offset ensemble** (1/21 of NAV on each calendar) — the drawdown of the
   ensemble is the object a real portfolio would run, and it is not the k=0 number.
3. Census how many committed monthly 4b passes have a DD margin smaller than their own offset
   spread.

Outputs: `.grid.csv` (357 cells) `.offsets.csv` (714 cells) `.walkforward.csv` `.keeppaths.csv`
`.console.txt`.
