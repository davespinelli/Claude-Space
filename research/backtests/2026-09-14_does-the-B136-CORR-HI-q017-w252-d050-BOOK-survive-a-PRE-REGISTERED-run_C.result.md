# Idea 814 (lane C, 2026-09-14) — does the B136 CORR-HI q0.17 w252 d0.50 BOOK survive a PRE-REGISTERED run?

**ANSWERED = HALF. The candidate retires two of the memo's four doubts outright and dies on a third
that nobody had priced: its 4b DRAWDOWN leg — the only leg the gate buys — is a property of SPY's
2020, not of the book. PARK, not KEEP. No RULES change; RULES.md, PROTOCOL.md, scan.py, bot.py and
baseline.py untouched.**

Script `2026-09-14_does-the-B136-CORR-HI-q017-w252-d050-BOOK-survive-a-PRE-REGISTERED-run_C.py`.
Panel B136 (`universe_broad.json`, 136 columns), scored sample 2009-01-13 → 2026-09-11, 10 bps,
weekly book, daily gate, t+1. Two tuned parameters only (the queue's own: level `q` and window `w`),
**all 56 grid points reported** (`.grid.csv`). Deterministic, no network, no RNG.

## 0. Gates (printed before any verdict)

| Gate | Result |
|---|---|
| G1 runner identity — a depth-0 multiplier reproduces `engine.backtest` | max\|d\| **0.000e+00** PASS |
| G2 causality — `min_periods = w`, multiplier decided at t applied at t+1; days with no threshold rise with w | 0 / 0 / 11 / 263 / 515 / 767 / 1271 / 1775 PASS |
| G3 reproduction of idea 606's memo cell | **bit-exact** — full 14.02% / 1.1538 / −15.11%, OOS 14.29% / 1.2080 / −15.11% PASS |
| G4 determinism — grid recomputed | \|dSharpe\| **0.000e+00** PASS |

## 1. Comparands (same scored sample, 10 bps, weekly, t+1)

| | CAGR | Sharpe | MaxDD | H1 / H2 | OOS CAGR / Sharpe / MaxDD |
|---|---|---|---|---|---|
| SPY buy-and-hold | 15.16% | 0.8861 | −33.72% | 0.9596 / 0.8259 | 15.33% / 0.8767 / −33.72% |
| RULES v2 (live baseline) | 7.98% | 1.0993 | −12.24% | 1.2348 / 0.9658 | 7.88% / 1.1059 / −12.24% |
| UNGATED book g = 1.00 (the control) | 14.20% | 1.0211 | −23.09% | 1.1513 / 0.8996 | 13.96% / 1.0094 / −23.09% |

4b bars off SPY: H1 > 0.9596, H2 > 0.8259, OOS Sharpe > 0.8767, MaxDD ≥ −20.23%, CAGR ≥ 10.61%.
4a bars off RULES v2: H1 > 1.2348, H2 > 0.9658, MaxDD ≥ −12.24%.

## 2. The grid — the memo's edge doubt is RETIRED

Idea 606 swept `q ∈ {0.07, 0.12, 0.17}` and `w ∈ {252, 504, 1008, 2016}`, so the candidate's own
dials sat on the TOP edge of one grid and the BOTTOM edge of the other. Extended through the cell on
both sides — `q ∈ {0.05, 0.10, 0.17, 0.25, 0.33, 0.42, 0.50}`, `w ∈ {63, 126, 252, 504, 756, 1008,
1512, 2016}` — the IS-Sharpe argmax is **(0.17, 252)**, q index 2 of 6 and w index 2 of 7:
**INTERIOR in both dials, and it is the memo's own cell.** H_INTERIOR PASS, H_SAME PASS.

It is also a band, not a point: **4b passes on 38 of 56 cells full sample, 37 of 56 read inside the
OOS window, 35 of 56 on both** (H_BAND PASS). The failures are concentrated at the two ends — the
narrowest tail (q = 0.05, gate almost never fires → DD, 8 cells) and the widest (q = 0.50, gate
always de-grossed → CAGR floor, 5 cells; H1+CAGR, 4). **4a passes on 0 of 56**: nothing here ever
beats the live book on its own terms.

## 3. Rule 8 walk-forward — the pick depends on the chooser, and so does the answer

Two choosers pre-stated before the OOS window was read. IS = 2009-01-13 → 2016-12-31; OOS =
2017-01-01 → 2026-09-11, read once.

| | pick (q, w) | interior | FULL CAGR / Sharpe / MaxDD | halves | OOS CAGR / Sharpe / MaxDD | 4b full | 4b in OOS | 4a |
|---|---|---|---|---|---|---|---|---|
| **C1** argmax IS Sharpe | **(0.17, 252)** | yes | **14.02% / 1.1538 / −15.11%** | 1.2097 / 1.0973 | **14.29% / 1.2080 / −15.11%** | PASS | PASS | FAIL |
| **C2** argmax IS Sharpe s.t. IS MaxDD ≤ 60% of SPY's IS MaxDD | (0.42, 504) | yes | 10.73% / 0.9875 / −14.34% | 1.0993 / 0.8719 | 10.59% / 1.0143 / −14.34% | PASS | **FAIL (CAGR)** | FAIL |
| SPY | — | — | 15.16% / 0.8861 / −33.72% | 0.9596 / 0.8259 | 15.33% / 0.8767 / −33.72% | — | — | — |
| RULES v2 | — | — | 7.98% / 1.0993 / −12.24% | 1.2348 / 0.9658 | 7.88% / 1.1059 / −12.24% | — | — | — |

C1 reproduces the memo exactly and clears every 4b leg out of sample. **C2 — the chooser a
drawdown-constrained allocator would actually run, and the one whose own constraint is the 4b leg
this gate exists to buy — lands on a different cell that fails the 4b CAGR floor out of sample.**
H_PICK FAIL: the candidate is rule-8 reachable under one pre-stated convention and not the other,
and nothing in the record picks between them.

## 4. The control that matters — 4b sees the GATE at C1 and the EXPOSURE at C2

| | fires | realised mean gross | GATED | matched-gross TWIN | twin 4b |
|---|---|---|---|---|---|
| C1 (0.17, 252) | 16.57% of days | 0.9172 | 14.02% / 1.1538 / −15.11% | 13.03% / 1.0211 / **−21.33%** | **FAIL (DD)** |
| C2 (0.42, 504) | 34.84% of days | 0.8258 | 10.73% / 0.9875 / −14.34% | 11.73% / 1.0212 / −19.35% | **PASS** |

C1 reproduces the memo's best argument — the ungated book at g = 1.00 (1.0211 / −23.09%) and the
static twin at the arm's own mean gross both fail 4b on drawdown, so at that cell 4b is seeing the
gate. **At C2 the twin passes 4b and has a HIGHER Sharpe and HIGHER CAGR than the gated arm**
(1.0212 vs 0.9875, 11.73% vs 10.73%): the gate is pure cost there, and 4b certifies exposure, as
ideas 502/504/596/674/767/810 said it structurally can. H_GATE FAIL.

## 5. Ladders

C1 passes 4b at **0 / 5 / 10 / 25 bps** (15.46%/1.258, 14.74%/1.206, 14.02%/1.154, 11.90%/0.997) and
fails at 50 bps; it passes at execution lag **1 / 2 / 3** (1.1538 / 1.0829 / 1.0531) — the memo's
ladder claim reproduces exactly. C2 fails at **25 bps** (H1,H2,OOS,CAGR) and at **lag 3** (CAGR).
H_LADDER FAIL, on C2 alone.

## 6. **THE KILL LEG — the drawdown cap is SPY's 2020, not the book's**

The gate's whole case is the drawdown leg. Remove one episode from both sides and read the leg again:

| | book MaxDD | SPY MaxDD | 4b cap (60%) | DD leg |
|---|---|---|---|---|
| C1, full sample | −15.11% | −33.72% | −20.23% | PASS by 5.12 pp |
| **C1, 2020-02→2020-04 removed** | **−15.11%** | **−24.50%** | **−14.70%** | **FAIL by 0.41 pp** |
| C1, 2022 removed | −13.83% | −33.72% | −20.23% | PASS |
| C2, 2020 removed | −14.20% | −24.50% | −14.70% | PASS (by 0.50 pp) |
| C2, 2022 removed | −14.34% | −33.72% | −20.23% | PASS |

**The book's own drawdown does not move when 2020 is removed** (−15.11% either way — its worst
drawdown is not the COVID crash at all). What moves is the COMPARAND: SPY's MaxDD falls from −33.72%
to −24.50%, the cap tightens by 5.53 pp, and the candidate fails. So the 5.12 pp of margin the memo
reports on its DD leg is **borrowed from SPY's February–March 2020**, an episode in which this book
lost −7.26% against SPY's −9.18% — a 1.9 pp edge, with the gate on for 72.6% of the days. Inside
2022 the gate does much more real work (book −7.24% vs SPY −18.18%, gate on 51.4% of days), and
removing 2022 leaves the leg intact. H_EPISODE FAIL.

This is a leg no prior run priced: the 4b drawdown cap is a ratio against a comparand whose own
denominator is one 33-day episode, so a book can clear the cap without ever having controlled its
own drawdown.

## 7. Verdict (pre-registered rule, fixed before any number was read)

> KEEP-candidate iff H_PICK **and** H_GATE **and** H_LADDER. PARK if any pick passes 4b full sample.
> Else KILL.

| hypothesis | result |
|---|---|
| H_REPRO — the memo cell rebuilds inside tolerance | **PASS** (bit-exact) |
| H_INTERIOR — the IS argmax is interior in both dials | **PASS** |
| H_SAME — the IS-alone chooser lands on the memo's cell | **PASS** (C1) |
| H_BAND — ≥ 28 of 56 cells pass 4b full sample | **PASS** (38/56) |
| H_PICK — both choosers' picks pass 4b full and inside OOS | **FAIL** (C2, CAGR floor) |
| H_GATE — every pick's matched-gross twin fails 4b | **FAIL** (C2's twin passes and beats the gated arm) |
| H_LADDER — 4b at 0/5/10/25 bps and lag 1/2/3 | **FAIL** (C2 at 25 bps and lag 3) |
| H_EPISODE — the DD cap survives removing 2020 or 2022 | **FAIL** (C1 fails with 2020 removed) |

**→ PARK.** The candidate is real enough to survive reproduction, the grid-edge doubt and its own
cost and lag ladders under the primary chooser, and it is genuinely rule-8 reachable there. It is
not capital-worthy, because the one leg it wins on is a statement about SPY's 2020 rather than about
the book, and because a second, equally pre-statable chooser lands on a cell where the gate is worse
than doing nothing at the same gross. **NOT proposed for promotion.**

## 8. What this run retires and what it leaves open

Retired: doubt (d) — the dials are not a grid edge. Retired: the reproduction doubt — the cell
rebuilds bit-exact from a script that never saw idea 606's grid. Left open, and now sharper: 4b's
drawdown cap is priced against a single-episode denominator (queued as new ideas below), and the
choice of rule-8 chooser is itself an unpriced degree of freedom that flips this verdict.

## 9. Survivorship (PROTOCOL rule 9)

B136 is `universe_broad.json`'s **current** constituents. Every CAGR above is biased upward and the
4b CAGR floor is easier than it would be on a point-in-time panel. The correlation STATE is
optimistic for the same reason: the names that died are exactly the ones that would have co-moved
hardest in 2020 and 2022, so the gate sees a tamer state than a live book would have seen. The
drawdown leg is the least affected of the three — which is precisely why its failure here counts.
