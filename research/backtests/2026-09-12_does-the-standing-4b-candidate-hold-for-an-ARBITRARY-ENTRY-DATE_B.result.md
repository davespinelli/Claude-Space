# Idea 829 (lane B, 2026-09-12) — does the standing 4b candidate hold for an ARBITRARY ENTRY DATE?

**ANSWERED = NO AT A REALISTIC HOLDING HORIZON, AND THE MISSING LEG IS THE CAGR FLOOR AGAINST
A POST-GFC SPY, NOT RISK. KILL of H_ENTRY and H_WORST; H_GROSS PASSES 8 of 8. No RULES change,
no new book, no PROTOCOL edit (rule 6). RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py
untouched.**

Script `2026-09-12_does-the-standing-4b-candidate-hold-for-an-ARBITRARY-ENTRY-DATE_B.py`,
console `…_B.txt`, grid `…_B.grid.csv`, per-window census `…_B.census.csv.gz` (4,520 rows),
gates `…_B.gates.csv`, books `…_B.books.csv`, walk-forward `…_B.wf.csv`.

## Gates — 3 of 3 PASS (printed before any new number)

| gate | published | this run |
|---|---|---|
| CAND g=1.00 full | 11.52% / 1.1996 / −15.91% | **11.54% / 1.2017 / −15.91%** |
| CAND g=1.00 OOS 2017– | 12.66% / 1.2740 / −15.91% | **12.70% / 1.2775 / −15.91%** |
| SPY full | 15.16% / 0.8860 / −33.72% | **15.16% / 0.8861 / −33.72%** |

Tolerance declared up front (|ΔCAGR| ≤ 1.00 pp, |ΔSharpe| ≤ 0.060, |ΔMaxDD| ≤ 2.00 pp) because
`data/prices.csv` was re-cached 2026-09-12 and the memo ran on the 2026-09-10 vintage. The
candidate reproduces to 0.02 pp of CAGR and 0.0021 of Sharpe — unlike the small panel (idea 823),
U56's vintage drift is negligible.

## The fixed window reproduces the record exactly, and says what the record says

| book | full CAGR / Sharpe / MaxDD | halves | OOS CAGR / Sharpe / MaxDD | OOS halves | 4b (fixed window) | 4a |
|---|---|---|---|---|---|---|
| CAND g=1.00 | 11.54% / 1.2017 / −15.91% | 1.2354 / 1.1749 | 12.70% / 1.2775 / −15.91% | 1.4077 / 1.1348 | **PASS**, all 7 legs | KILL |
| LIVE g=0.75 (RULES v2) | 8.63% / 1.2018 / −12.05% | 1.2349 / 1.1757 | 9.47% / 1.2782 / −12.05% | 1.4098 / 1.1340 | FAIL (CAGR floor, full **and** OOS) | — |
| RULES v1 | 6.41% / 0.6602 / −13.83% | 0.6510 / 0.6718 | 7.60% / 0.7361 / −13.83% | 1.0293 / 0.4234 | FAIL (5 legs) | KILL |
| SPY | 15.16% / 0.8861 / −33.72% | 0.9595 / 0.8259 | 15.33% / 0.8767 / −33.72% | 0.9802 / 0.7650 | — | — |

Sharpe is flat across gross to 0.0001 (1.2017 vs 1.2018) — gross buys CAGR and drawdown, nothing
else, exactly as the memo's caveat (a) says.

## THE ENTRY-DATE CENSUS — all 8 grid points (H × s), every point reported

Window-local 4b against SPY over the *same* window: Sharpe, both window-local halves,
MaxDD ≤ 60% of SPY's, CAGR ≥ 70% of SPY's.

### CAND g=1.00 (the standing candidate)

| H | s | n | **joint 4b** | Sharpe leg | halves leg | DD leg | CAGR leg | med CAGR | med Sharpe |
|---|---|---|---|---|---|---|---|---|---|
| 756d (3y) | 21 | 176 | **0.3977** | 0.9148 | 0.5170 | 0.8636 | 0.7273 | 10.65% | 1.1875 |
| 756d | 63 | 59 | 0.3390 | 0.9322 | 0.4915 | 0.8814 | 0.7119 | 10.63% | 1.1759 |
| 1008d (4y) | 21 | 164 | **0.5610** | 0.9878 | 0.6402 | 0.8963 | 0.7561 | 10.87% | 1.1732 |
| 1008d | 63 | 55 | 0.5636 | 0.9818 | 0.6364 | 0.9091 | 0.7455 | 10.87% | 1.1729 |
| **1260d (5y, headline)** | **21** | **152** | **0.6513** | **1.0000** | 0.7829 | 0.9276 | 0.7961 | 11.03% | 1.2128 |
| 1260d | 63 | 51 | 0.6863 | 1.0000 | 0.8235 | 0.9412 | 0.7843 | 10.96% | 1.2125 |
| 1890d (7.5y) | 21 | 122 | **0.9344** | 1.0000 | 0.9508 | 1.0000 | 0.9344 | 10.97% | 1.1689 |
| 1890d | 63 | 41 | 0.9268 | 1.0000 | 0.9512 | 1.0000 | 0.9268 | 11.03% | 1.1800 |

### Joint 4b pass share, all three books, all 8 points

| H | s | CAND g=1.00 | LIVE g=0.75 | RULES v1 |
|---|---|---|---|---|
| 756 | 21 | 0.3977 | 0.1875 | 0.0114 |
| 756 | 63 | 0.3390 | 0.1695 | 0.0000 |
| 1008 | 21 | 0.5610 | 0.1768 | 0.0061 |
| 1008 | 63 | 0.5636 | 0.1818 | 0.0000 |
| 1260 | 21 | 0.6513 | 0.1184 | 0.0263 |
| 1260 | 63 | 0.6863 | 0.1569 | 0.0196 |
| 1890 | 21 | 0.9344 | 0.0410 | 0.0082 |
| 1890 | 63 | 0.9268 | 0.0488 | 0.0244 |

## Pre-registered hypotheses

| | verdict | reading |
|---|---|---|
| **H_ENTRY** joint 4b ≥ 0.80 at headline | **FAIL** | 0.6513 (152 windows). One entrant in three would not have seen 4b hold over their own 5 years. |
| **H_SHARPE** Sharpe leg ≥ 0.90 | **PASS** | **1.0000** — the candidate out-Sharpes SPY in **every** 5-year window, and in every 4y and 7.5y window. |
| **H_WORST** DD leg = 1.0000 at headline | **FAIL** | 0.9276 — 11 of 152. But see below: one episode, by ≤ 0.58 pp. |
| **H_GROSS** CAND > LIVE at all 8 points | **PASS** | 8 of 8, by +0.21 to +0.89 of pass share. Raising gross 0.75 → 1.00 is the right direction for an arbitrary entrant, not only on the record's one window. |

## What actually fails, and when

53 of 152 headline windows fail. Binding legs among them: **halves 33, CAGR 31, DD 11, Sharpe 0.**

- **Every failing entry date is 2009-01-13 … 2017-06-16.** Zero failures for any entry after
  2017-06-16; pass share for entries ≥ 2015-01-01 is **0.9750** (78 of 80). The candidate's
  4b pass is, entry-date-wise, a **post-2014 fact** — the same second-window character the record
  keeps finding elsewhere (ideas 605/609/825).
- **The CAGR floor is the binding leg and SPY is what binds it.** All 31 CAGR-leg failures sit in
  windows where SPY compounded **9.70%–22.15%/yr**; the candidate's own CAGR is near-constant
  across windows (median 10.65%–11.03% at every horizon, i.e. it is the *comparand* that moves,
  not the book). Against a 15–22%/yr SPY a 70% floor is 10.6–15.5%/yr and an 11% book loses.
- **The DD-leg failures are a single knife-edge episode, not a structural break.** All 11 are
  consecutive 2013 entries (2013-02-14 … 2013-12-13) whose windows end in 2018 — the sample's
  *shallowest* 5-year SPY drawdown, −13.02%, so the cap is −7.81% and the book's −8.39% misses by
  **0.58 pp**. The 4b DD cap is generous when SPY falls 34% and binding when SPY is calm; this is
  a property of the bar, not of the book.
- **The worst window by ΔSharpe still wins on Sharpe**: 2011-09-13 → 2016-09-14, CAND
  8.98% / 1.1070 / −7.75% against SPY 15.17% / 1.0640 / −13.02% — the book is better risk-adjusted
  and shallower and still fails 4b, on the halves leg and the CAGR floor.

## Rule 8

**(a) On this run's own tuned parameter (H), picked on IS entries alone, OOS read once:**

| H | n IS | IS pass | n OOS | OOS pass |
|---|---|---|---|---|
| 756 | 60 | 0.2500 | 80 | 0.5375 |
| 1008 | 48 | 0.2083 | 68 | 0.8088 |
| 1260 | 36 | 0.0278 | 56 | 0.9643 |
| 1890 | 6 | 0.3333 | 26 | 1.0000 |

IS-chosen H = 1890 → OOS 1.0000. **H_WF FAILS**, |OOS − IS| = 0.6667 against a 0.10 bar. Stated
honestly in both directions: the failure is (i) in the *generous* direction at every horizon
(OOS ≥ IS by +0.29 to +0.94), and (ii) not really a selection at all — a 7.5-year window cannot
close inside 2009–2016, so the IS leg rests on 6 windows. H is **not selectable on IS**, and the
honest reading of the ladder is the monotone one: pass share rises with horizon at both spacings.

**(b) Mandated book leg — OOS 2017-01-01 … 2026-09-11, nothing fitted:** CAND **12.70% / 1.2775 /
−15.91%** vs RULES v2 baseline 9.47% / 1.2782 / −12.05% vs RULES v1 7.60% / 0.7361 / −13.83% vs
SPY 15.33% / 0.8767 / −33.72%. CAND clears all of 4b OOS; 4a fails OOS as it does full sample
(MaxDD −15.91% worse than the live book's −12.05%).

## Conventions and sensitivities

- **S1 cold start** (charge gross × 10 bps on the entry day, since a real entrant starts in cash):
  CAND 0.6513 → **0.6513**, LIVE 0.1184 → 0.1118. Joining-vs-starting is worth nothing at the
  headline; the census convention C1 is not load-bearing.
- **S2 / C3**: **zero** of the 4,520 windows has SPY CAGR ≤ 0 at any (H, s), so the literal
  negative-floor convention is never exercised and S2 ≡ literal at all 8 points. Worth saying
  plainly: **this sample contains no losing 3-year-or-longer SPY window**, which is itself the
  strongest caveat on every 4b verdict in the record.
- Weights decided at close t, applied t+1; 10 bps per unit turnover; weekly; warm-up to
  `px.index[260]`; 2 tuned parameters (H, s), both swept, all 8 points reported.

## Verdict

**KILL** — of the hypothesis, not of the candidate. The standing 4b candidate's pass is real on the
record's fixed window and reproduces to 0.02 pp, and its *risk* legs are entry-date-robust (Sharpe
beats SPY in 152 of 152 five-year windows; the only DD failures miss by 0.58 pp in one 2013 entry
block). What is **not** entry-date-robust is the **CAGR floor**: at a realistic 3–5 year horizon
only 0.40–0.65 of entrants would have cleared 4b, and it takes a **7.5-year** horizon to reach
0.93. Any promotion of this book to real capital should be stated with the horizon attached.
The one result this run adds in the candidate's favour is **H_GROSS at 8 of 8**: the 0.75 → 1.00
gross move raises the entrant pass share from 0.118 to 0.651 at the headline and dominates at
every grid point, so the memo's single proposed change is the right direction by a second,
entry-date-robust measure.

**Caveats carried forward unchanged:** `universe.json` is current-constituent survivorship-biased;
2009–2026 is one QQQ-favourable regime with no losing 3-year SPY window; the live paper record is
~1 week old. Nothing here justifies real capital.
