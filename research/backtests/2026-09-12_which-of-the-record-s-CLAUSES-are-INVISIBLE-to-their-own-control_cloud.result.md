# Idea 582 — which of the record's CLAUSES are INVISIBLE to their own control?

**ANSWERED, and the queue's own prescription is REFUTED. Two of eight clause families are visible
under NO control on all three panels; the proposed CONSTANT-EXPOSURE control is not stricter than a
second parent, it is LOOSER; 17 of 48 published-style comparisons sit inside the rebalance-weekday
floor of the very books being compared; and the visible/invisible label itself flips out of sample in
32.5% of cells. KILL for capital (4a 0 of 264 books). No RULES change, no book promoted, no KEEP
claimed, no PROTOCOL edit applied (rule 6); RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py
untouched.**

Script `2026-09-12_which-of-the-record-s-CLAUSES-are-INVISIBLE-to-their-own-control_cloud.py`
(254.7 s, deterministic, no network). Tuned: **clause family (8) × control (5) = 40, × 3 panels =
120 cells, all reported**. Pinned: gross 0.75, weekly, 10 bps, t+1, MA 200d, vol 20d, cap 0.60, band
3%, n 10/20. Panels U56 (56), B136 (136), SMALL (663 tradable, 52 max_1d_move ≥ 1.0 tickers dropped
per PROTOCOL).

## Two ways a clause can be invisible, both measured
* **MECH_DEGEN** — after the control the two target-weight paths are the *same matrix*
  (max L1/2 < 1e-9). Idea 317's 4.4e-16.
* **INVISIBLE** — the paths differ but |ΔSharpe| does not clear the **convention floor**: the
  max−min Sharpe spread of the same books over the five weekday offsets of the same 5-day rebalance
  schedule, measured here (U56 0.021–0.082, B136 0.018–0.063, SMALL 0.011–0.127).

## The census (FULL sample; V visible, I invisible, M mechanically degenerate)
| family | U56 RAW / GROSS / VOL / BETA / CONST | B136 | SMALL |
|---|---|---|---|
| TREND | V V V V V | V V V V V | V V V V V |
| VOLCAP | **I I I I I** | **I I I I I** | V V V V V |
| WIDEN | V V V V V | V V V V V | V V V V V |
| CONC | V V V V V | V V V V V | V V V V V |
| GROSS | I **M** I I **M** | I **M** I I **M** | I **M** I I **M** |
| DEFEND | I I I I V | I I I I V | V V V V V |
| BAND | V V V V V | **I I I I** V | V V V V V |
| SPREAD | V V V V V | **I I I I** V | **I I I I** V |

| test | bar | measured | verdict |
|---|---|---|---|
| **H_GROSS** idea 317's collapse generalises | MECH_DEGEN on all 3 panels | L1max 1.6e-16 / 2.1e-16 / 1.4e-16, ΔSharpe 0.0 | **PASS** |
| **H_ONE** every family visible under ≥1 control | all 8 | **6 of 8** — VOLCAP and GROSS visible under **no** control | **FAIL** |
| **H_EXPO** matched exposure kills only exposure clauses | ≥80% of cells visible | **73%** (33 of 45); VOLCAP and DEFEND invisible on U56 and B136 under GROSS/VOL/BETA while moving 27–75% of NAV | **FAIL** |
| **H_CONST** constant exposure is stricter than a parent | ≥1 family | **0** — and CONST is the *only* control under which DEFEND, BAND and SPREAD are visible on all three panels | **FAIL, refuted** |
| **H_FLOOR** the convention floor is material | ≥1 cell | **17 of 48** RAW/matched-GROSS comparisons inside their own floor, with L1 mean up to **0.542** | **PASS** |
| **H_OOS** the label is window-stable | ≤20% flips | **39 of 120 (32.5%)** — SPREAD ×13, TREND ×10, WIDEN ×10, CONC ×5, BAND ×1 | **FAIL** |

## A naming fault in the parent, established by gate G5
Idea 317's book documented as *"MA-DG (only names above their 200d MA, gated weight to CASH)"* is
built `_ew(ma, G).where(ma, 0.0)`, and `_ew` divides by the count of TRUE entries **in the mask it is
given**. Given the gate as its mask, the gated weight is **re-spread over the survivors at full
gross**; the trailing `.where(ma, 0.0)` is a no-op and there is no cash leg. **G5: idea 317's MA-DG
is bit-identical to this file's MA-RS on all three panels (max L1/2 = 0.000e+00)**, and a true
de-gross book runs at mean gross 0.532 (U56) / 0.532 (B136) / 0.409 (SMALL) against 0.750. The same
file's `VOLCAP-DG` (`_ew(elig, G).where(capok, 0.0)`) **is** a genuine de-gross — so two clauses named
"-DG" in one committed script carry opposite weight handling. This file keeps idea 317's book under
its true name (MA-RS) so gate G3 stays apples-to-apples, adds the de-gross book it was named for, and
gives DEGROSS-vs-RESPREAD its own family (SPREAD) — which on this pair the record has never run as
named.

## Gates
G1 fast runner vs engine.backtest, one book per panel: worst **2.776e-17** (bar 1e-9) · G2 no scaled
book exceeds gross 1.000000, worst matched-gross residual **2.665e-15**; VOL-match residual ≤ 6.4e-07
and BETA ≤ 1.0e-05 after two scaling passes (measured, stated, not a bar) · **G3** matched-gross
|ΔSharpe| on U56 against idea 317's committed G3: GROSS **0.0** with L1max 1.6e-16 (hard bar, PASS);
TREND 0.040 vs 0.175, VOLCAP 0.007 vs 0.244, WIDEN 0.079 vs 0.277, CONC 0.145 vs 0.140, DEFEND 0.053
vs 0.061 — a **drift reading, not a pass**: idea 317 took its max over 288 conditional cells' parent
legs, this run compares the parent pair itself · **G5** as above · G4 determinism 0.

## Rule 8
**WF-A** (each window its own backtest, each control's scaling re-derived inside it, OOS read once):
**39 of 120 labels flip**, both directions — TREND and WIDEN fall from VISIBLE to INVISIBLE on U56
(ΔSharpe 0.060 → 0.020 and −0.140 → −0.029), CONC and SPREAD rise from INVISIBLE to VISIBLE. Whether
a clause is visible is therefore a window fact, not a property of the clause.
**WF-B** (264 books, pick by IS Sharpe alone): SMALL/LOWVOL20 under matched gross, IS Sharpe 1.886 →
**OOS CAGR 4.56% / Sharpe 0.603 / MaxDD −23.52%**, against RULES v2 OOS 9.47% / 1.278 / −12.05% and
SPY OOS 15.33% / 0.877 / −33.72%; FULL halves 1.933 / 0.471.
**KEEP paths:** 4a **0** of 264 against RULES v2 on U56 and **0** against RULES v2 on the book's own
panel; 4b **59**; BOTH **0**. The 4b rows are the record's own standard forms at various control
scalings (U56/MA-RS, B136/MA-RS, B136/VOLCAP-DG, B136/BAND-RS), not new candidates, and nothing here
is claimed as a KEEP. The largest of them, B136/VOLCAP-DG — CAGR 12.32%, Sharpe 1.136, halves
1.266/1.012, OOS Sharpe 1.112, MaxDD −18.70% — is a standing form worth a pre-registered look of its
own on that panel; whether that pass is already committed elsewhere in the record is not established
here.

## What this says about PROTOCOL (proposal only — rule 6, Sunday review)
1. A clause comparison should publish the **convention floor of its own books** beside its ΔSharpe.
   17 of 48 published-style comparisons here do not clear it, with the books differing by up to 54%
   of NAV — the gap is real, the Sharpe reading of it is not.
2. "Price an exposure clause against a constant-exposure control" does **not** work as filed: the
   constant-exposure comparand is the *loosest* control in this census (it is the only one under
   which DEFEND, BAND and SPREAD read visible everywhere), because replacing the second parent with
   EWall compares two different *books*, not two settings of one clause. The degeneracy the queue
   wants caught is caught by the **mechanical** test (L1 = 0), which needs no control at all.
3. A clause whose only content is an exposure dial should be named as such — and the census says
   exactly one of the eight is (GROSS), which the L1 test identifies on every panel for free.

## Caveats
* **SURVIVORSHIP:** B136 and SMALL are current constituents; every LEVEL on them is overstated. The
  object measured is a DIFFERENCE between two books on one panel, where the bias largely cancels; the
  KEEP-path and WF-B legs are diagnostics only.
* The VOL and BETA controls are matched by two weight-scaling passes, so the match is approximate
  (residuals above). Scaling is applied to weights and each book re-run, so costs scale with it.
* The floor is one convention (rebalance weekday at fixed 5-day cadence). Other conventions — cost
  rung, calendar alignment, panel vintage — would each have their own floor and are not priced here.
* Eight families is the record's vocabulary as idea 317 fixed it, not an exhaustive list of clauses.
