# Idea 675 (cloud, 2026-09-15) — is U56/CAND20's SINGLE-RUNG 4b pass a KNIFE EDGE or a real window?

**ANSWERED = A REAL WINDOW, AND THE "SINGLE RUNG" WAS A LADDER ARTEFACT. The 4b pass window is
`g ∈ [0.6241, 0.8337]` — 0.2095 of gross, 4.2 rungs of the record's own 0.05 ladder, 21 of 150
rungs at the queue's asked-for 0.01 resolution — and the published g = 0.75 is interior by 0.126
below and 0.084 above. Idea 670's ladder {0.20, 0.35, 0.50, 0.60, 0.75, 0.85, 0.95, 1.00} simply
never tests 0.65, 0.70 or 0.80. It survives rule-8 selection: all three IS-only choosers land
inside the OOS window and pass 4b out of sample at 10 bps. It does NOT survive the cost sweep —
EMPTY at 25 bps — and it does NOT travel: EMPTY on B136 and on SMALL. PARK, not KEEP: nothing new
is promoted, and the exact wording already on the shelf is unchanged.**

No RULES change, no PROTOCOL edit (rule 6). `RULES.md`, `PROTOCOL.md`, `scan.py`, `bot.py` and
`baseline.py` untouched. One CONFIRMATION memo written, explicitly proposing nothing:
`2026-09-15_u56-cand20-weekly-g075_4b_WINDOW_CONFIRMATION_MEMO.md`.

**SELECTION.** Last eligible Open idea in QUEUE.md (this run's claim rule); the entries below it
carry standing cloud SKIP notes as prose censuses with no book to price. Price-only, so runnable
in the cloud sandbox.

## What was asked and what was measured

Idea 670 found the record's own 2026-09-04 KEEP 4b book — `CAND20`, top-20 equal weight, **no vol
scaler**, weekly, 10 bps, t+1 — passing 4b at **exactly g = 0.75 and nowhere else** on its 8-rung
ladder. Idea 804 then established over 24 of 24 bands that a 4b band's lower edge is the **CAGR
floor alone** and its upper edge the **DD cap alone**, both monotone in g, with the Sharpe legs
flat in gross. Two monotone crossings bound an **interval** — so "one rung" is a claim about the
ladder unless the interval is genuinely narrower than a rung. This run solves for the interval
instead of sampling it.

**TUNED 1** gross resolution, 5 levels all reported: `RECORD8` (670's own 8 rungs) · `STEP05` (30)
· `STEP01` (150) · `STEP002` (750) · `EXACT` (bisection to 1e-6 of gross). **TUNED 2** cost rung
{0, 10, 25, 50} bps. Reported-not-tuned: window FULL/IS/OOS, panel U56/B136/SMALL, the 5 phases of
a 5-trading-day rebalance schedule (idea 806's convention axis), and 7 companion arms including
the zero-signal control `SPYBH` = g × SPY. 31,800 book-rows in `.ladder.csv`, 168 exact-endpoint
rows in `.exact.csv`, plus `.resolution.csv` / `.walkforward.csv` / `.gate670.csv`.

**A convention distinction the record should keep straight.** Two 4b readings are reported
throughout: `c670` — halves and levels on the FULL window plus a separate OOS-Sharpe leg, which is
the convention the "passes at exactly 0.75" claim lives in — and `cwin`, the window-local form the
record's rule-8 runs use. Also: this is the **weekly g = 0.75** descendant of the 2026-09-04 KEEP,
not the **monthly g = 0.65** form idea 898 confirmed last week. Same selection rule, different
cadence and gross.

## GATES 7 of 8 PASS — and the one that fails is named, not smoothed

| gate | what | result |
|---|---|---|
| G1 | fast `Book.at` ≡ `engine.backtest` | BAND03 max\|Δr\| 1.041e-17; **CAND20 max\|Δr\| 2.082e-17, max\|Δturn\| 4.441e-16** |
| G2 | BAND03 at g=0.75 ≡ `baseline.rules_v2_weights` | max\|Δw\| **0.000e+00** |
| **G3** | **idea 670's committed `.grid.csv` CAND20 rows** | **FAIL overall.** `G3[U56]` **8 of 8 rows exact** on every leg and both verdicts, worst metric deviation **4.33e-03** (under the 5e-3 vintage bar) — **the subject panel reproduces completely**. `G3[B136]` **5 of 8**, worst deviation **1.87e-02** |
| G4 | committed U56 triples | SPY 15.13%/0.8845/−33.72%; RULES v2 8.62%/1.2013/−12.05% |
| G5 | monotonicity on the 750-rung ladder | CAGR(g) non-decreasing **749/749**, \|MaxDD(g)\| non-decreasing **749/749**; Sharpe spread over the whole ladder FULL **0.0022** / IS 0.0010 / OOS 0.0034 |
| G6 | bisection ≡ ladder | worst endpoint overshoot **0.000e+00** |
| G7 | determinism | **0.000e+00** |
| G8 | analytic ray, SPYBH: \|MaxDD(g)\|/\|MaxDD(SPY)\| must read g | worst deviation **3.63e-02** over 3×4 |

**Why G3 fails, exactly.** 670's own note says its B136 cache ended 2026-09-04; today's ends
2026-09-11, and U56's runs to 2026-09-14. On B136 the extra tape moves the metrics by 1.87e-02 and
**flips `L3_OOS` at g = 0.60 / 0.75 / 0.85** — because in 670's own committed numbers that leg's
margin on B136 is **+0.0016 of Sharpe** (CAND20 OOS 0.8836 against SPY's 0.8820). A leg held by
0.0016 is a date, not a property, and this gate is how the record finds that out. `pass4b` still
matches on all 16 rows (B136 fails `L2_H2` regardless), so the **U56 claim this run is about is
reproduced intact** — but the pre-registered bar covered all 16 rows and it is reported FAILED.

## The answer: H_LADDER and H_KNIFE

U56/CAND20, 10 bps, convention c670:

| resolution | rungs | passing | g_lo | g_hi | width |
|---|---|---|---|---|---|
| RECORD8 (670's own) | 8 | **1** | 0.7500 | 0.7500 | 0.0000 |
| STEP05 | 30 | 4 | 0.6500 | 0.8000 | 0.1500 |
| **STEP01** (the queue's ask) | 150 | **21** | 0.6300 | 0.8300 | 0.2000 |
| STEP002 | 750 | 104 | 0.6260 | 0.8320 | 0.2060 |
| **EXACT** (bisection) | — | — | **0.6241** | **0.8337** | **0.2095** |

The pass set is a **contiguous interval at every resolution**. **H_LADDER: the single rung is a
ladder artefact** — 1 passing rung becomes 21 of 150. **H_KNIFE: a real window** — 0.2095 of gross
is 4.2 rungs of the record's own 0.05 ladder against a 1-rung bar. **H_INTERIOR: interior** — 0.75
sits **+0.1259** above the CAGR-floor edge and **+0.0837** below the DD-cap edge, both over the
0.02 bar.

The leg census over the 750-rung ladder confirms idea 804's mechanism on this book exactly: at 10
bps `L1_H1`, `L2_H2` and `L3_OOS` pass at **750 of 750** rungs (they never bind), `L4_DDcap` at 416
and `L5_CAGRfloor` at 438 — **the two level legs are the whole window**, and the Sharpe spread over
the entire ladder is 0.0022.

## H_COST FAILS, and a gross-flat Sharpe leg is what does it

| cost | g_min (CAGR floor) | g_max (DD cap) | level window | Sharpe legs | **4b window** |
|---|---|---|---|---|---|
| 0 bps | 0.5699 | 0.8379 | 0.2681 | pass | **0.2681** |
| 10 bps | 0.6241 | 0.8337 | 0.2095 | pass | **0.2095** |
| 25 bps | 0.7295 | 0.8274 | 0.0979 | **FAIL** | **EMPTY** |
| 50 bps | 1.0307 | 0.8172 | inverted | **FAIL** | **EMPTY** |

Turnover is 11.01×/yr at g = 0.75, so each 10-bps rung costs 1.10 pp of CAGR there; that lifts the
CAGR-floor edge 0.57 → 0.62 → 0.73 while the DD-cap edge barely moves (0.838 → 0.827). **But the
window does not die by squeeze.** At 25 bps the level window is still 0.0979 wide and the book
fails `L1_H1` — the 2009-2016 half-sample Sharpe against SPY's — at **0 of 750 rungs**, a leg that
is flat in gross and therefore cannot be bought back with exposure. Reported because the two
readings differ and only one is the 4b window: a bisection on the level legs alone would have
over-reported a window that is not there.

**The nuance that matters for capital:** the 25-bps break is *in the first half*. On the OOS window
alone (`cwin`/OOS) the 4b window at 25 bps is **[0.6440, 0.8274], width 0.1834, Sharpe legs
passing**, and it contains 0.75. The book's cost fragility lives in 2009-2016, not in 2017-2026.

## H_OFFSET — the lower edge is resolved, the upper edge is not

Across the 5 phases of a 5-trading-day schedule at 10 bps: lower-edge spread **0.0358** (17% of the
window width — **resolved**), upper-edge spread **0.2004** (**96% of the width — not resolved by
this data**). Width (W schedule) 0.2095 exceeds the largest edge spread by **+0.0091, i.e. +4%**, so
idea 806's clause reads HOLDS *on the pooled comparison and marginally*. Read edge by edge, which is
the honest form, the DD-cap edge ranges from **0.7565** (phase 1) to **0.9570** (phase 3). Every
offset keeps a non-empty window (5 of 5, widths 0.1724–0.3461) and every offset's window contains
0.75 — so the *existence* of the window and the interiority of 0.75 are offset-robust, while the
*upper endpoint* is not a number this data resolves.

## H_WF / RULE 8 — the window survives selection

**First, the fact that decides how the choosers are read.** Under the window-local convention the
strict IS 4b pass set is **EMPTY at every gross and every cost rung**, and one leg does it:
`L1_H1` **0 of 750** at all four rungs (the first half of 2009-2016 against SPY's first half). So
no IS-only chooser can be "the IS 4b pick"; the three choosers below select on the IS **level**
legs and are labelled as such. Under 670's own convention (halves on the FULL window) the same legs
pass at every gross — this is an artefact of reading halves inside an 8-year window, not a property
of the book, and it is stated rather than worked around.

IS level window at 10 bps **[0.7263, 0.8409]**; OOS 2017-2026 read once:

| cost | chooser | g | OOS CAGR | OOS Sharpe | OOS MaxDD | OOS H1/H2 | 4a | 4b |
|---|---|---|---|---|---|---|---|---|
| 0 | IS_MID | 0.773 | 16.10% | 1.211 | −18.74% | 1.318/1.104 | n | **y** |
| 0 | IS_GMAX | 0.882 | 18.42% | 1.212 | −21.23% | 1.318/1.105 | n | n |
| 0 | IS_SHARPE | 0.660 | 13.71% | 1.211 | −16.13% | 1.319/1.104 | n | **y** |
| **10** | **IS_MID** | **0.784** | **14.98%** | **1.123** | **−19.08%** | **1.235/1.011** | n | **y** |
| **10** | **IS_GMAX** | **0.831** | **15.89%** | **1.123** | **−20.17%** | **1.235/1.012** | n | **y** |
| **10** | **IS_SHARPE** | **0.810** | **15.49%** | **1.123** | **−19.69%** | **1.235/1.012** | n | **y** |
| 25 / 50 | — | IS level window EMPTY | | | | | | |

Comparands, same OOS window: **SPY 15.27% / 0.874 / −33.72%** (halves 0.980/0.759); **RULES v2
(live) 9.46% / 1.277 / −12.05%** (halves 1.410/1.132). Full sample: SPY 15.13% / 0.885 / −33.72%
(halves 0.959/0.824); RULES v2 8.62% / 1.201 / −12.05% (halves 1.232/1.177). The book at the
published g = 0.75, weekly, 10 bps, on today's tape: **12.73% / 1.060 / −18.31%** full sample
(halves 1.073/1.055), **OOS 14.34% / 1.123 / −18.31%**, turnover 11.01×/yr.

**Rule 8: 4b 5 of 6 (chooser × cost) picks, 4a 0 of 6.** All three 10-bps choosers pass, and
IS [0.7263, 0.8409] overlaps OOS [0.5607, 0.8337] by **0.1074** — the IS window does not *contain*
the OOS one, but every IS-only pick lands inside it. 4a fails on MaxDD against the low-vol live
book, as every growth candidate in this record does.

## H_TRAVEL FAILS

Same measurement, 10 bps, c670, on 24 (panel × arm) cells:

| panel | CAND20 | CAND20_VS | CAND10 | CAND05 | CAND20_NOCAP | EWELIG | BAND03 (RULES v2) | SPYBH |
|---|---|---|---|---|---|---|---|---|
| U56 | **0.2095** | 0.0851 | EMPTY | EMPTY | 0.1509 | 0.2001 | 0.3675 | EMPTY |
| B136 | **EMPTY** | EMPTY | EMPTY | EMPTY | 0.0822 | 0.1192 | 0.2692 | EMPTY |
| SMALL | **EMPTY** | EMPTY | EMPTY | EMPTY | EMPTY | EMPTY | EMPTY | EMPTY |

The subject's window is **the widest on U56 among the ranked books** and the only one containing
0.75 there, but it is **empty on B136** (level window [0.6115, 0.7571] with a Sharpe leg failing —
670's own `L2_H2` finding) and **empty on SMALL** (level window inverted). The zero-signal control
`SPYBH` is empty on all three panels at every cost, which is the right answer for a book with no
signal and is how the machinery is checked independently of the result.

## Verdict — PARK

The queue's question answers cleanly: **a real window, 0.2095 of gross, with the published rung
interior, and the "single rung" was a resolution artefact of 670's irregular ladder.** It survives
rule-8 selection — three independent IS-only choosers, all passing 4b out of sample at 10 bps — and
it fails the other two robustness legs the queue asked for: **empty at 25 bps** (via a first-half
Sharpe leg, not the level legs) and **empty on both other panels**. Nothing is promoted; this is
the already-committed shelf book seen at higher resolution, and the confirmation memo adds no
clause and no parameter.

Follow-ups filed: 918 (does the 25-bps break of the FULL-window reading live entirely in
2009-2016), 919 (re-read every committed gross band in the record at 0.01 resolution), 920 (should
the record publish a leg's MARGIN beside every committed L3_OOS verdict, after G3 found one held by
0.0016).

## Survivorship

`research/universe.json`, `universe_broad.json` and the SMALL screen are current-constituent lists
(SMALL additionally drops the 52 tickers with `max_1d_move ≥ 1.0` per `data/small_meta.csv`), so
every CAGR and drawdown **level** above is optimistic. A 4b bar is the book's level against SPY's
and SPY is **not** survivorship-inflated, so these bars are *not* protected by the usual same-tape
argument: **every width above is an upper bound** on what a point-in-time panel would show. The
offset spread, the cost sweep and the resolution comparison are same-book contrasts and are
unaffected.
