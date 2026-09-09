# Idea 320 — is-the-UNCONDITIONAL-width-dial-a-B136-fact-or-a-panel-ordering

**Lane B, 2026-09-09.** Script: `2026-09-09_is-the-UNCONDITIONAL-width-dial-a-B136-fact-or-a-panel-ordering_B.py`

**Verdict: ANSWERED — the queue asked a FALSE DICHOTOMY. KILL of the H4 "units artefact" remedy.
No RULES change, no book promoted, no KEEP claimed. RULES.md, scan.py, bot.py, baseline.py untouched.**

---

## What was run

One dial: unconditional book width. Rank the eligible names (above 200d MA, vol20 < 0.60), hold the
top `k` at `gross/k` each, `k = min(n0, E_t)`, **gross 0.75 every day**, weekly, 10 bps, t+1,
vol-scaler off. The dial is read in **two units** — absolute `n0 ∈ {20, 30, 40, 60, E_t}` (the queue's
grid) and relative coverage `c ∈ {0.25, 0.50, 0.75, 1.00}` with `k = round(c·E_t)`. Three panels
(U56, B136, SMALL439) as a reporting axis. **27 grid points, all reported**, plus a 12-book fill
control. Rule 8: dial chosen on IS ≤ 2016-12-31, OOS 2017– read once, two choosers.

Panels truncated to the **common end 2026-09-04** (the last bar `prices_broad.csv` and
`prices_small.csv` carry, and the vintage the record's RULES v2 number was computed on).

**Survivorship:** B136 and SMALL439 are current constituents only; only within-panel dial
differences are read as evidence.

## Gates — five, all pre-registered, all pass

| Gate | Result |
|---|---|
| G1 `fast_backtest` == `engine.backtest`, 3 panels | **1.388e-17** PASS |
| G2 live RULES v2 on U56 @ 2026-09-04 | **8.66% / 1.2056 / -12.05% (1.2259/1.1909)** — the record to every digit. PASS |
| G3a mean TARGET gross within 1 pp of 0.75, all 27 points | **0.650 pp** PASS |
| G3b realised-gross spread across any panel's dial | **≤ 0.598 pp** vs idea 321's 12.78 pp. PASS |
| G4 idea 318 provenance, B136 OOS Sharpe at n0=20/40/60/E_t | 0.8832 / 0.9714 / 1.0033 / 1.0192 vs published 0.883 / 0.971 / 1.003 / 1.019, max dev **0.0004**. PASS |
| G5 the 4b passer vs the record | U56 n0=20 = **12.8% / 1.07 / -18.3% / 1.08 / 1.07**, identical to LEADERBOARD lines 288 (idea 46) and 2925 (idea 48). PASS |

G2 vintage note: the un-truncated U56 cache now runs to 2026-09-08 and gives 8.64% / 1.2037 — a
−0.0019 Sharpe drift from one extra bar, not a code difference.

G3a is **not** an identity and is censused rather than assumed. Two causes:
(i) **unrankable eligibles** — a name above its 200d MA with vol20 under the cap but with no
composite score yet (the 12m momentum leg needs 252 bars) is counted in `E_t` and cannot be ranked;
binds at the **wide** end, worst **58.33% of days at SMALL439 `n0=E_t`** (mean target gross 0.7441,
0.59 pp short). (ii) **rank ties** — the composite is the mean of three pct-ranks and is therefore
discrete; U56 carries tied ranks on **68.7%** of days and loses ~1 name on 8.3% of them; binds at the
**narrow** end, sub-1 pp. Both inherited from idea 318's construction and kept unchanged so G4 is exact.

Because (i) concentrates exactly where the SMALL result lives, the **fill control** below is required
before that result can be read.

## The answer

| | ordering |
|---|---|
| **LEVEL** (mean OOS Sharpe across the ABS dial) | U56 **1.131** > B136 **0.955** > SMALL439 **0.416** |
| **SLOPE** (d OOS Sharpe / d coverage) | B136 **+0.190** > U56 **−0.061** > SMALL439 **−0.216** |

**Neither.** Not the same ordering (B136 and U56 swap), and not the reverse (SMALL439 is **last in
both**). Level and slope are two different orderings that happen to share a last place, so "widening
helps B136" neither restates nor inverts the record's familiar panel-quality ordering — it is a
third, independent fact about the panels. The level ordering *is* the one ideas 51/312/316 keep
finding; the queue's error was assuming the slope had to be that ordering or its mirror.

## Hypotheses

- **H1 (the premise) — CONFIRMED on 2 of 3 panels, and the third is UNIT-DEPENDENT.** B136 positive
  and monotone in both units (OOS Sharpe 0.8832 → 1.0192); SMALL439 negative in both (0.4640 →
  0.2855, and MaxDD deteriorates −33.48% → −40.21%). U56 is so nearly flat that its slope **sign
  flips with the unit** (ABS −0.061, REL +0.070). "Flat on U56" is real but is not a *signed*
  finding: no claim about U56's width direction should be published without naming the unit.
- **H3 (saturation) — CONFIRMED as a defect of the grid, REJECTED as the explanation.** U56 offers
  only **37.5** eligible names on an average day, so saturation hits **1.000 already at n0=60** and
  the `n0=60` and `n0=E_t` books are **bit-identical** (max\|dW\| = 0.000e+00): **1 of the queue's 4
  ABS dial steps on U56 is a literal no-op.** But de-saturating the dial closes only **10.7%** of the
  B136-minus-U56 slope gap (+0.2505 → +0.2237). The panel difference survives the fix almost intact.
- **H4 (collapse) — KILLED, in the direction opposite to the one proposed.** Re-based on each panel's
  own narrow end, the cross-panel SD of the width curve is **0.0643 in ABS units and 0.1258 in REL
  units**: coverage units make the panels disagree **~2× more**. The width response is genuinely
  panel-specific, so idea 336/400's "an absolute cut on a panel-dependent distribution measures the
  frequency, not the signal" critique does **not** extend to this dial. The absolute grid is a worse
  *ruler* (H3) but not a confounded *measurement*.
- **FILL CONTROL — PASSES.** Re-running the REL dial with `k = round(c·R_t)` (R_t = ranked count) so
  gross is an exact identity removes cause (i) entirely — at c=1.00 every panel now holds exactly
  0.7500 with 0.00% of days off, against SMALL439's 0.7441 / 58.33%. **All three slope signs are
  preserved** and the largest slope change is **0.0094** (~4% of the B136−U56 gap).

## Mechanism (new)

Idea 330's two-term split (`Sharpe = ann_ret / ann_vol`) applied to the width dial over 6 (panel,
unit) cells:

**Widening is a volatility instrument with a return tax, and the panels differ in the tax, not the
benefit.** The vol term is positive in **6 of 6** cells and tightly bunched (**+0.190 … +0.443**,
spread 0.252); the return term is negative in **6 of 6** and **1.5× more dispersed** (**−0.546 …
−0.149**, spread 0.398). B136's Sharpe gain is the vol term outrunning a small tax (+0.290 vs
−0.207); SMALL439's collapse is a large tax outrunning the same benefit (−0.546 vs +0.246). This
extends idea 330's "wins on vol, loses on return" shape from the eligible-equal-weight family to the
width dial specifically, and it explains H4: what is panel-specific is the **tax**.

## Rule 8 and KEEP paths

**4a 0/27, 4b 8/27, BOTH 0/27.** Binding-leg counts across the failures: DD 15, CAGR 12, H2 12,
OOS 10, H1 9.

Rule 8 (12 picks = 3 panels × 2 units × 2 choosers): **3 pass 4b, 0 pass 4a**, and the IS-4b-gated
chooser finds **no admissible point at all** on U56 or SMALL439 — 4 of 12 picks are the empty set.

| panel | pick | OOS CAGR / Sharpe / MaxDD | RULES v2 OOS | SPY OOS |
|---|---|---|---|---|
| U56 (ABS) | n0=20 | **14.49% / 1.1369 / −18.31%** | 9.53% / **1.2851** / −12.05% | 15.45% / 0.8820 / −33.72% |
| B136 (REL) | c=1.00 | **10.59% / 1.0192 / −17.69%** | 7.98% / **1.1185** / −12.24% | 15.45% / 0.8820 / −33.72% |
| SMALL439 (ABS) | n0=20 | 6.92% / 0.4640 / −33.48% | 3.85% / **0.5680** / −14.68% | 15.45% / 0.8820 / −33.72% |

The **two units disagree on the pick in 2 of 3 panels** (U56 n0=20 vs c=1.00; B136 n0=30 vs c=1.00),
and on B136 that disagreement is the whole verdict: the ABS pick fails 4b on H2,DD while the REL pick
passes. That is a reportable fragility of the record's rule-8 machinery on this dial.

**No promotion, no memo.** G5 shows the 4b passers are exact re-derivations of rows the record
already published and already declined to adopt (U56 n0=20 = LEADERBOARD 288 and 2925; B136 EWALL =
idea 318's 1.019). All 8 fail 4a, and every one is beaten by the live RULES v2 on both bars 4a cares
about — the U56 pick gives up **−0.148** OOS Sharpe and **−6.3 pp** MaxDD to v2 while buying
+4.96 pp OOS CAGR.

## Files

`.grid.csv` (27 points + 9 benchmark rows) · `.fillcontrol.csv` (12) · `.curves.csv` (30 slopes) ·
`.saturation.csv` · `.collapse.csv` · `.decomposition.csv` · `.walkforward.csv` (12 picks) ·
`.gates.csv` · `.console.txt`

## Follow-ups proposed

588, 589, 590 — see QUEUE.md.
