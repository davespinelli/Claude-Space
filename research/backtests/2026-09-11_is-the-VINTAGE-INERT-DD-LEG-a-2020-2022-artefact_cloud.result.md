# Idea 518 (cloud) — is the VINTAGE-INERT DD LEG a 2020/2022 artefact?

**VERDICT: ANSWERED / YES, AND WORSE THAN THE QUEUE'S WORDING — 0 of 5 published-equivalent 4b
passes survive excluding 2020, 1 of 5 survives excluding 2022, 0 of 5 survive excluding both. But
the mechanism is NOT the one idea 514 assumed: the books' own drawdowns barely move; it is SPY,
the comparand in both 4b legs, that moves.** No RULES change, no book promoted, no PROTOCOL edit.
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py untouched.

Script `2026-09-11_is-the-VINTAGE-INERT-DD-LEG-a-2020-2022-artefact_cloud.py`; console + 4 CSVs
(`.troughs`, `.cells`, `.legs`, `.walkforward`) committed. Two parameters, every grid point
reported: **episode ∈ {NONE, drop2020, drop2022, dropBOTH}** (calendar years, as the queue words
it) × **panel ∈ {U56, B136, SMALL439}**, on a fixed 6-book corpus (RULES v2, EWall, CAND-5,
CAND-10, CAND-20 = the 2026-09-04 KEEP 4b construction, CAND-20-INV) = **72 scored cells**.
10 bps, weekly, t+1, gross 0.75, no random draws.

**The exclusion is on RETURNS, not prices.** Signals, eligibility, holdings and costs are computed
on the full price history exactly as the live book sees them; only the scoring window changes, and
every comparand (RULES v2 and SPY) is scored on the identical spliced window. Excluding at the
price level would change the 200d MA and 20d vol on both sides of the gap — a different book, not
a different sample.

**Reproduction gate (recorded, non-raising):** live RULES v2 on U56 @10bps weekly reads
**8.15% / 1.1675 / −11.92%** against idea 415 G2's published **8.66% / 1.2056 / −12.05%**. The gap
is the start date, not the code: this run pins every panel to `start=2010-01-01` so the three
panels share a window, giving U56 a 2011-01-13 first scored day against idea 415's 2009-01-13.
MaxDD, the statistic under test, agrees to **0.13 pp**.

## 1. The premise, tested rather than assumed

**19 of 21** (panel, book) series have their worst drawdown inside 2020 or 2022 — **18 in 2020
alone**, 1 in 2022, and two outside (U56 CAND-5 troughs 2023-03-15, SMALL439 CAND-5 2025-04-08).
Idea 514 assumed all of them; 90.5% is close enough that its inference stands. Every one of those
18 troughs is the **same week** (2020-03-12 / 03-18 / 03-23 / 03-31) from the **same peak**
(2020-02-19), i.e. the record's whole DD leg rests on one fortnight.

## 2. Almost none of the movement is the book's

| | mean book MaxDD | SPY MaxDD | SPY CAGR |
|---|---|---|---|
| NONE | −0.2273 | −0.3372 | 14.45% |
| drop2020 | −0.1941 (**85.3%** retained) | −0.2450 (**72.7%**) | 14.20% |
| drop2022 | −0.2230 (**98.8%**) | −0.3372 (**100.0%**) | **17.00%** |
| dropBOTH | −0.1679 (74.8%) | −0.2025 (60.1%) | 16.91% |

4b's DD leg is a **ratio**, book MaxDD / SPY MaxDD against a 0.60 cap. Dropping 2020 shallows the
books by 15% and SPY by 27%, so the ratio **rises 0.674 → 0.792** and cells under the cap collapse
**10/18 → 4/18**. Dropping 2022 leaves SPY's drawdown untouched and instead lifts SPY's CAGR by
2.5 pp, tightening the **70%-of-SPY CAGR floor**. So the two episodes kill 4b through **different
legs**: 2020 through the DD cap, 2022 through the CAGR floor.

## 3. Verdict survival (the queue's literal ask)

**4a: 0 of 18 at every episode setting** — the live book is not beaten on its own terms anywhere
here, so there are no 4a verdicts to test. That is itself the answer for 4a: its DD leg cannot be
an artefact of anything, because nothing reaches it.

**4b: 5 of 18 at NONE → 0 / 1 / 0.** Per passer, with the leg that kills it:

| panel | book | NONE | drop2020 | drop2022 | dropBOTH |
|---|---|---|---|---|---|
| U56 | EWall | pass | fail **DD + CAGR** | fail **CAGR** | fail DD + CAGR |
| U56 | CAND-10 | pass | fail **DD** | fail H2 + OOS | fail H2 + OOS + DD |
| U56 | **CAND-20** | pass | fail **DD** | **pass** | fail **DD** |
| U56 | CAND-20-INV | pass | fail **DD** | fail **CAGR** | fail all four |
| B136 | EWall | pass | fail **DD** | fail **CAGR** | fail **CAGR** |

The DD cap binds in **4 of 5** kills under drop2020 — **and in every one of those four the book's
own drawdown got SHALLOWER**. They fail because the benchmark's crash, which is what funds a 60%
cap, is gone. Across all 72 cells the DD cap's failure count goes **8 (NONE) → 14 (drop2020)** and
the CAGR floor's **9 → 12 (drop2022)**.

The one survivor is **CAND-20 on U56 — the standing KEEP 4b construction** — and it survives only
the exclusion that does not touch SPY's drawdown. It dies on drop2020 and on dropBOTH, both times
on the DD leg alone.

## 4. PROTOCOL rule 8 (book chosen on IS 2010–2016 only, OOS 2017–2026 read once)

The IS window contains **neither episode**, so the chooser has never seen a crash. Picks: U56 →
CAND-20, B136 → RULES v2, SMALL439 → CAND-20-INV. Pooled OOS, 3 cells:

| episode | pick CAGR / Sharpe / MaxDD | RULES v2 | SPY | beats v2 | beats SPY |
|---|---|---|---|---|---|
| NONE | 8.49% / 0.847 / −21.97% | 7.10% / 0.990 / −12.93% | 15.38% / 0.879 / −33.72% | 0/3 | 2/3 |
| drop2020 | 8.23% / 0.885 / −17.79% | 6.53% / 0.981 / −9.30% | 15.05% / 0.984 / −24.50% | 0/3 | 2/3 |
| drop2022 | 10.90% / 1.042 / −21.97% | 8.71% / 1.165 / −12.93% | 20.04% / 1.142 / −33.72% | 0/3 | 2/3 |
| dropBOTH | 10.91% / 1.131 / −14.02% | 8.27% / 1.191 / −7.97% | 20.28% / 1.397 / −19.35% | 0/3 | 2/3 |

The ordering is stable — the rule-8 pick loses to RULES v2 **0 of 3** at every setting and beats
SPY on Sharpe **2 of 3** at every setting — so the **Sharpe** legs are robust to the episodes in a
way the **DD and CAGR** legs are not. Note SPY's own Sharpe rises from 0.879 to **1.397** once both
episodes are removed: excluding the crashes flatters the benchmark far more than the gated books,
which is exactly why the KEEP bars move.

## 5. What to carry forward

1. **A 4b pass is a statement about March 2020.** Not metaphorically: 18 of 21 troughs are that
   fortnight, and 4 of 5 passes die on the DD leg when it is removed. Any memo proposing real
   capital off a 4b pass should publish the pass's DD ratio **with 2020 excluded** beside it.
2. **The DD leg's vintage-inertness (idea 514's max |dMaxDD| 0.0000) is not stability.** It is
   both sides sharing one trough. Inertia to the data END is not inertia to the data CONTENT.
3. **Proposal for Sunday review — a cheap standing robustness column, NOT a RULES change:**
   report `MaxDD_ex2020 / SPY_MaxDD_ex2020` and `CAGR_ex2020 / SPY_CAGR_ex2020` beside every 4b
   verdict. It costs one re-score of returns already in memory (no re-backtest) and it is the only
   column in this run that separates a book that survives a crash from a book that was measured
   against one.
4. Nothing here is a KEEP. The standing CAND-20/U56 candidate is not damaged as a *book* — its own
   drawdown **improves** to −15.26% ex-2020 — but its 4b certificate does not survive the test.

**SURVIVORSHIP (rule 9):** all three panels are current constituents; SMALL439 drops the 44 names
with `max_1d_move >= 1.0`. The exclusion contrasts are within-book and within-panel, so the bias
sits in the **levels**, not in the survival counts reported here.
