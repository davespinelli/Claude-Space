# Idea 1257 (lane C, 2026-09-17) — is the 2026-09-04 KEEP 4b BOOK a THREE-LEG COMPOSITE or ONE LEG WEARING THREE?

**VERDICT: KILL (capital).** No RULES change, no book promoted, no PROTOCOL edit, no memo.
4 of 4 gates, 42 of 42 grid points published, 16s, offline, deterministic.

## Why this idea and not one from `## Open`
Every item standing in QUEUE.md's Open section at the start of this run is a record-bookkeeping
question (schema clauses, censuses of committed text, resample-knob partitions). None can produce
this protocol's step-3 deliverables — a weights function run against the baseline and SPY, 4a/4b
verdicts, rule-8 OOS. The sprint's documented fallback (precedent: idea 1253's run, CHANGELOG
2026-09-17) was used: three new price-only ideas stress-testing the standing 2026-09-04 KEEP 4b
book were filed as **1256 / 1257 / 1258**, the bookkeeping items were left open and unclaimed, and
this lane claimed the second (1257) per the lane rule.

## What was run
The frozen 2026-09-04 candidate rebuilt from scratch with **only its ranking signal replaced**.
Everything else is held: eligibility (above own 200d MA AND vol20 < 0.60), N = 20, H = 126,
GROSS = 0.75, weekly cadence (decide Friday / trade Monday), gated-out weight to CASH, 10 bps,
t+1 execution, 260-row warm-up.

**The two dials and no more (rule 4):** `LEG SUBSET` — all 7 non-empty subsets of
{M12_1 = (skip 21, look 252), M6 = (0,126), M3 = (0,63)} — x `COMB RULE` {MEAN (the record's,
average of the legs' cross-sectional percentile ranks), MIN (consensus: a name ranks at its
weakest leg)} = **14 cells per panel, 42 in all, EVERY ONE PUBLISHED** in `.grid.csv`.
NOT dials, reported at every value: PANEL {U56, B136, SMALL663}; the 4a and 4b legs individually;
full / halves / IS / OOS; annual turnover; the rule-8 chooser and its do-nothing control.

**G1_ANCHOR PASS at 4.67e-05:** the (M12_1, M6, M3)/MEAN cell reproduces the committed anchor
triple **15.71% / 1.1480 / -19.13%**, so this prices the committed number and not a relative.
**G2 PASS on all three panels at exactly 0.00e+00:** MEAN and MIN coincide bit-for-bit on every
singleton, as they must by construction.

## (1) The three legs are NOT collinear — pre-declared outcome (A) FAILS
Mean cross-sectional Spearman between the legs' percentile ranks, sampled monthly, per panel:

| pair | U56 | B136 | SMALL663 |
|---|---|---|---|
| M12_1 vs M6 | +0.6055 | +0.5832 | +0.5607 |
| M12_1 vs M3 | **+0.3541** | **+0.3335** | **+0.3096** |
| M6 vs M3 | +0.6522 | +0.6613 | +0.6544 |

Minimum over all panels **+0.3096**. Outcome (A) required rho >= 0.70 for every pair AND a U56
OOS Sharpe spread < 0.10; both clauses fail (spread 0.1547). **The composite is genuinely three
readings, not one leg wearing three.** The premise that motivated the idea is refuted, and is
reported as refuted rather than re-cut.

## (2) But the composite does NOT buy return — it buys DRAWDOWN, and that is the whole 4b pass
On U56, ordered by full-sample MaxDD (the binding leg), the incumbent is **the single best
drawdown of all 14 cells** while being only the **third best Sharpe**:

| cell | full CAGR | full Sharpe | full MaxDD | OOS Sharpe | ann. turn | 4b |
|---|---|---|---|---|---|---|
| **M12_1+M6+M3 / MEAN (the incumbent)** | 15.71% | 1.1480 | **-19.13%** | **1.1759** | 2.76 | **PASS** |
| M12_1+M6 / MEAN | 16.08% | 1.1582 | -19.95% | 1.1133 | 2.63 | PASS |
| M12_1+M3 / MEAN | 15.21% | 1.1161 | -20.2339% | 1.1401 | 2.81 | fail DD |
| **M12_1 alone** | **16.71%** | **1.1893** | -20.58% | 1.1545 | **2.52** | fail DD |
| M6+M3 / MEAN | 15.20% | 1.1020 | -21.71% | **1.1672** | 3.11 | fail DD |
| M3 alone | 14.59% | 1.0932 | -22.23% | 1.1094 | 3.30 | fail DD |
| M6 alone | 15.56% | 1.1068 | -22.74% | 1.1164 | 3.07 | fail DD |

**All 12 U56 failures fail on the DD leg and on the DD leg ONLY.** Every other 4b leg (both
halves, OOS Sharpe, the CAGR floor) passes at all 14 cells. **12-1 momentum ALONE beats the
committed book on full-sample Sharpe by +0.0413, on CAGR by +1.00pp and on turnover by 0.24/yr,
and is disqualified solely by 1.45pp more drawdown.** So the third and second legs are not adding
signal; they are a drawdown diversifier bought at ~1pp of CAGR. This is the fourth consecutive
dial — phase (1253), years (1254), names (1255), now the signal itself — on which the committed
4b pass is decided by the drawdown leg alone.

## (3) A reporting defect in 4b's DD leg, found here and published rather than smoothed over
The exact cap on U56 is `0.60 x SPY's -0.3371723528 = -0.2023034117`. The **M12_1+M3 / MEAN** cell
lands at **-0.2023392**: it fails 4b by **3.58e-05 of drawdown — 0.0036 percentage points**, the
sixth decimal place. Against it, the incumbent's own DD margin is +1.103e-02, i.e. **308x wider**.
1 of 14 U56 cells is decided at a precision no tape supports. Nothing is re-scored on this basis
(the cell is reported as it fell, FAIL); it is filed as a PROTOCOL reporting question for the
Sunday review (rule 6) — **a 4b DD pass or fail inside its own rounding should be published as
UNRESOLVED beside the verdict, never silently as a binary** — and as a reporting line only,
never as a chooser. Filed as idea 1259.

## (4) Rule 8 walk-forward: the chooser loses to doing nothing
Cell chosen by IS Sharpe on warm-up..2016-12-31 ONLY; 2017-2026 read ONCE. Do-nothing control =
always take the record's 3-leg MEAN.

| panel | IS argmax | its OOS Sharpe | do-nothing OOS | delta | SPY OOS | LIVE v2 OOS |
|---|---|---|---|---|---|---|
| U56 | M12_1 (IS 1.2494) | 1.1545 | 1.1759 | **-0.0215** | 0.8686 | 1.2717 |
| B136 | M6 (IS 1.3297) | 1.0301 | 1.0240 | +0.0061 | 0.8769 | 1.1061 |
| SMALL663 | M3 (IS 0.8353) | 0.3602 | 0.4534 | **-0.0932** | 0.8769 | 0.6518 |

**Mean delta -0.0362; the chooser reaches the incumbent at 0 of 3 panels and beats it at 1 of 3,
by +0.0061.** On U56 the IS window names 12-1 alone — the cell with the best full-sample Sharpe of
all 14 — and it arrives out of sample 0.0215 BEHIND the book it replaced. The signal axis is
another dial this tape cannot resolve.

## Both KEEP paths, all 42 grid points
- **4a: 0 of 42.** Live RULES v2's -12.05% MaxDD is not beatable by a growth book — rule 4's own
  stated reason for path 4b existing.
- **4b: 7 of 42.** U56 **2 of 14** (the incumbent and M12_1+M6/MEAN, which is strictly worse OOS
  at 1.1133); B136 **5 of 14** (M3, M3/MIN, M12_1+M3/MEAN, M6+M3/MEAN, M6+M3/MIN — all against
  B136's lower bar, best OOS 1.0857, none within 0.09 of the U56 incumbent's 1.1759);
  **SMALL663 0 of 14, failing ALL FIVE 4b legs at every one of the 14 cells.**
- Nothing here is a candidate. The only U56 passer that is not the incumbent is worse out of
  sample; the B136 passers do not reach the incumbent; SMALL663 is not rescuable by any leg subset
  or combination rule.

## Pre-declared outcomes, scored as they fell (rule 7)
(A) DEGENERATE **= False** — legs are not collinear (min rho +0.3096) and the U56 spread is 0.1547.
(B) BLEND-CARRIED **= True** — subsets lose the 4b pass while the 3-leg MEAN keeps it, and the
3-leg MEAN is the best U56 OOS Sharpe of all 14 (so the "within 0.02 of best" clause holds at 0.0000).
(C) SINGLE-LEG-SIMPLIFICATION **= True**, but ONLY as literally written and only on B136, by
**+0.0061** — and on U56, where the single leg genuinely does have the better full-sample Sharpe,
rule 8 reaches it and it LOSES by -0.0215 out of sample.
(D) CHOOSER-LOSES-TO-DOING-NOTHING **= True** on 2 of 3 panels.
**The outcome set as pre-declared was not mutually exclusive: (C) and (D) both fired.** That is a
defect in this run's own pre-registration and is stated rather than resolved by choosing the
flattering reading. The capital verdict follows (D), because (C)'s entire content is a +0.0061 on
the panel with the lower bar.

## MEAN vs MIN
MIN is worse on the large-cap panels and better on SMALL663, where nothing passes anything.
U56 3-leg: MEAN OOS 1.1759 vs MIN 1.0968 (**-0.0791**). B136 3-leg: MEAN 1.0240 vs MIN 1.0460.
SMALL663 3-leg: MEAN 0.4534 vs MIN 0.5078. A consensus rule is not an improvement on the panel
the incumbent lives on.

## Survivorship (rule 9)
U56 and B136 are current-constituent lists; SMALL663 is a current sub-$2B screen (52 of 715
dropped for max_1d_move >= 1.0). Every level above is optimistic and every 4b pass is an upper
bound. The headline is a DIFFERENCE between signal variants scored on the SAME panel with the
same eligibility and the same N, so it is first-order immune to a level bias moving all 14 cells
together; 1255 prices the panel bias itself.

## What the record should take, in one sentence
**The 2026-09-04 book's three momentum legs are not redundant, but what the extra two legs buy is
DRAWDOWN and not RETURN — 12-1 alone earns more at less turnover and is disqualified only by the
4b cap — so the committed pass is, for the fourth dial running, a statement about the drawdown leg.**

## Artefacts
- `2026-09-17_is-the-2026-09-04-KEEP-4b-BOOK-a-THREE-LEG-COMPOSITE-or-ONE-LEG-WEARING-THREE_C.py`
- `.grid.csv` (42 rows, every cell), `.legcorr.csv` (9 rows), `.walkforward.csv` (6 rows),
  `.gates.csv` (4 rows), `.console.txt` (full run log)
