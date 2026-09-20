# Idea 1763 (lane B, 2026-09-20) — DOES A SPY-SOURCED VOL TARGET REPRODUCE THE VOLTGT016 CANDIDATE WITHOUT INHERITING THE PANEL?

**Verdict: ANSWERED / PARK. Two KILLs, one constructive residue. No new book, no rules change.**

Script `2026-09-20_voltgt-sigma-source_B.py`, 720 scored rows, **gates 18 of 18**.
3 panels × 3 sigma SOURCES × 5 targets × 4 conventions (L,d) × 4 cost rungs, every cell published in
`.grid.csv`; pass-shares in `.pass_share.csv`, twin control in `.twin.csv`, rule 8 in `.walkforward.csv`.
Two tuned parameters exactly: **target `t`** and **sigma SOURCE**. 10 bps, weekly, next-day execution,
gross capped at 1.00.

---

## 1. The question, and why it was worth a run

The standing vol-target candidate (`2026-09-20_voltgt-panel_KEEP4b_MEMO.md`, idea 1730; PARK since
idea 1771) sizes the book by `g_t = clip(t / sigma_t, 0, 1)` with `sigma_t` the realised vol of **the
panel's own** unlevered equal-weight portfolio. Its own point 8 names the consequence — the target is
calibrated on a survivorship-selected panel, so the book inherits it — and addendum A2 found it does
not exist on small caps (0 of 96). A target set on **SPY's** realised vol inherits nothing: one public
series, identical for every panel, and no circularity between the sizing signal and the names sized.

## 2. KILL #1 — the panel inheritance is NOT load-bearing for the candidate's pass (V1 REPRODUCES)

At the memo's own cell (`L=20, d=0, t=0.16`, 10 bps), swapping the panel's sigma for SPY's carries the
**same 4b FULL and 4b OOS verdicts on both panels**, at a cost of essentially zero Sharpe:

| panel | source | FULL CAGR / Sharpe / MaxDD | OOS CAGR / Sharpe / MaxDD | 4b FULL | 4b OOS |
|---|---|---|---|---|---|
| U56 | PANEL (memo) | 15.61% / 1.2028 / −19.86% | **15.94% / 1.2196 / −19.86%** | PASS | PASS |
| U56 | **SPY** | 14.79% / 1.1989 / −19.48% | **15.18% / 1.2192 / −19.48%** | PASS | PASS |
| B136 | PANEL (memo) | 15.94% / 1.2050 / −18.76% | **15.36% / 1.1839 / −18.76%** | PASS | PASS |
| B136 | **SPY** | 15.55% / 1.2112 / −18.32% | **14.93% / 1.1986 / −18.32%** | PASS | PASS |

OOS Sharpe moves **−0.0004 on U56 and +0.0147 on B136**; the drawdown gets *shallower* by 0.38 / 0.44 pp
and the CAGR gives up 0.76 / 0.43 pp. SPY buy-and-hold over the same OOS window is 15.26% / 0.8739 /
−33.72%; the live RULES v2 book is 9.46% / 1.2769 / −12.05% (U56) and 7.85% / 1.1019 / −12.24% (B136).

**The mechanism.** The two sigma series are near-duplicates on the large panels: `corr(PANEL, SPY)`
**0.9910 pearson / 0.9746 spearman on U56** and 0.9910 / 0.9803 on B136 (means 0.1438 vs 0.1620 and
0.1518 vs 0.1620). So *the memo's point-8 caveat does not carry the pass.* The reading "the candidate's
4b pass is an artefact of a survivorship-selected panel's own volatility" is **KILLED**: the pass
survives replacing that volatility with a public index's at max |ΔSharpe| 0.015.

**The scalar really is panel-free (gates G5a/G5b).** The SPY-sourced `g_t` is identical on U56 and
SMALL665 to **1.221e-15** (same SPY cache). Against B136 it reads 2.397e-03 — and that is a **CACHE**
fact, not a panel fact: `data/prices.csv` and `data/prices_broad.csv` disagree about SPY by up to
$0.0051 (1.511e-04 of daily return), and re-sourcing B136's sigma onto `prices.csv`'s SPY drives the
residual to **0.000e+00**. The PANEL-sourced scalar, on the same post-warm-up days, disperses by
**max |Δ| 0.2015 (U56 vs B136) and 0.6542 (U56 vs SMALL665)** — two to three orders of magnitude more.

## 3. KILL #2 — but SPY-sourcing is NOT the portable fix, on any of the four axes it was proposed for

* **It does not rescue SMALL (V2 NOT triggered — the idea's own premise, killed on its own terms).**
  **0 of 40** non-PANEL cells clear 4b FULL *and* OOS on SMALL665, at every cost rung 0/10/25/50 bps.
  The binding leg is not the drawdown the source could plausibly move: `L2_H2` (second-half Sharpe vs
  SPY) fails in **1.000** of cells for *every* source, OOS. The SMALL failure is a **panel-return** fact.
  What SPY-sourcing *does* buy there is real but insufficient: OOS Sharpe 0.4022 → **0.5862** at t=0.16
  and 0.4901 → **0.6129** at t=0.20, against the SPY bar of 0.8739; and against the matched constant-gross
  twin the OOS deficit shrinks from **−0.2238 (win 0.000) to −0.0706 (win 0.150)**, i.e. ~68% of the
  panel-sourced damage is repaired and the book still loses to buying less of itself.
* **It is LESS convention-robust, not more (V5 not triggered).** 4b OOS pass-share over the published
  (L,d) conventions on U56+B136: **PANEL 0.700, SPY 0.625, BLEND 0.650.** Idea 1771's finding that the
  memo's pass is a property of its convention cell is not relieved by changing the source.
* **It costs more to run.** Mean turnover 3.06 /yr against PANEL's 2.93; at the memo's own rung on U56,
  **2.07 against 1.83** (+13%). At 50 bps U56 4b OOS drops to 6/20 (SPY) against 9/20 (PANEL).
* **It is strictly worse under rule 8 on U56.** See §4.

## 4. Rule 8 — (t, src) chosen on 2009–2016 only, 2017–2026 read once

42 legal IS-only picks across three arms (FIXEDCONV over (t,src); FREECONV over (t,src,L,d); SRC=x over
t alone). Totals: **4b OOS 16/42, 4a OOS 4/42**; excluding the no-choice control C_MEMO, **13/36 and
4/36**. The matched twin of the same picks clears 4b OOS **3/42**.

The source-level read is the one that matters, at the memo convention on U56:

| arm | chooser | pick | OOS CAGR / Sharpe / MaxDD | 4b OOS |
|---|---|---|---|---|
| SRC=PANEL | argmax IS Sharpe | PANEL t0.16 | 15.94% / 1.2196 / −19.86% | **PASS** |
| SRC=PANEL | argmin IS MaxDD | PANEL t0.08 | 11.38% / 1.2999 / −12.28% | **PASS** |
| **SRC=SPY** | argmax IS Sharpe | **SPY t0.20** | 16.23% / 1.1955 / −20.91% | **fail** |
| **SRC=SPY** | argmin IS MaxDD | SPY t0.08 | 10.18% / 1.2569 / −12.07% | **fail** |
| SRC=BLEND | argmax IS Sharpe | BLEND t0.16 | 15.57% / 1.2207 / −19.78% | PASS |
| SRC=BLEND | argmin IS MaxDD | BLEND t0.08 | 10.73% / 1.2778 / −12.19% | PASS |

**SRC=SPY reaches a 4b-OOS passer 0 of 2 times on U56 where SRC=PANEL reaches one 2 of 2.** The reason
is mechanical and is the same failure idea 1771 documented: SPY's sigma runs ~9% *above* the U56 panel's
(0.1620 vs 0.1438), so the same target buys less gross, IS Sharpe peaks one rung higher, and argmax IS
Sharpe walks the chooser onto **t = 0.20**, which trips the DD cap OOS (−20.91% against −20.23%). And a
chooser given the source as a free dial **buys SPY 14 times out of 18** — it prefers the source that
then fails. On B136 the picture is milder (SPY 1 of 2, PANEL 2 of 2).

## 5. The twin control (V4 not triggered) — the dial still survives

Against each book's own realised-mean-gross-matched constant-gross twin, OOS at 10 bps:

| panel | source | OOS dSharpe | OOS dMaxDD | OOS win share | book 4b OOS | twin 4b OOS |
|---|---|---|---|---|---|---|
| U56 | PANEL | +0.1114 | +8.03 pp | 1.000 | 15/20 | 0/20 |
| U56 | SPY | +0.0927 | +7.66 pp | 1.000 | 12/20 | 3/20 |
| B136 | PANEL | +0.1016 | +11.59 pp | 1.000 | 13/20 | 0/20 |
| B136 | SPY | +0.1112 | +11.20 pp | 1.000 | 13/20 | 0/20 |
| SMALL665 | PANEL | −0.2238 | +4.88 pp | 0.000 | 0/20 | 0/20 |
| SMALL665 | SPY | −0.0706 | +10.52 pp | 0.150 | 0/20 | 0/20 |

This reproduces idea 1771's headline (the vol target is the record's first device to beat its matched
twin at scale) and shows it is **not** a property of the panel-sourced sigma — the public-sigma version
beats the twin just as decisively on U56/B136, and on B136 by slightly more.

## 6. The constructive residue — a source-INVARIANT, convention-ROBUST target band

At **t ∈ {0.10, 0.12}** every one of **24 of 24** cells (3 sources × 2 large panels × 4 conventions)
clears 4b FULL **and** 4b OOS. At the memo's t = 0.16 the same share is 0.500–0.750, and at t = 0.20 it
is 0.250–0.500. Representative (U56, L20 d0, 10 bps): SPY t=0.12 FULL 12.61% / 1.1879 / −16.14%, **OOS
13.53% / 1.2610 / −16.14%**; PANEL t=0.12 OOS 14.56% / 1.2728 / −16.44%. This independently confirms
idea 1771's band `t ∈ {0.10, 0.12}` on a second axis and adds that **inside that band the SOURCE is a
free choice** — which is exactly the condition under which the simpler, public, panel-free wording can
be adopted at zero verdict cost.

**It is not promoted here.** The band is an OOS-visible reading; one of three IS-only choosers
(`C_ISLEGS`, max IS 4b-leg count) does land in it on both panels and passes 4b OOS (U56 PANEL t0.12
14.56% / 1.2728 / −16.44%; B136 SPY t0.12 13.29% / 1.2408 / −15.10%), but that chooser was not
pre-registered as *the* chooser and the other two miss. Certifying t ≈ 0.12 needs its own pre-registered
run, per the standard idea 1771 set for itself.

## 7. Path 4a — the only passers are a PANEL-RESTATEMENT pass, not a beat-the-book pass

**6 of 180** cells clear 4a FULL *and* 4a OOS, all on **B136 at t = 0.08, L = 20** (all three sources,
d ∈ {0,1}); e.g. PANEL t0.08 L20 d0 FULL 10.24% / 1.1673 / −10.86% (halves 1.2668 / 1.0720), OOS
10.97% / 1.2447 / −10.86%. But 4a is scored against the live book **restated on B136**, whose halves are
1.2298 / **0.9671**; the live book actually trades U56, where the same comparand is 1.2279 / **1.1808**
at −12.05%, and there **0 of 60 cells clear 4a** — the U56 twin of that cell posts halves 1.203 / 1.160
at −12.28%, missing on the H1 and the drawdown legs. The 4a pass is a property of the weaker
restatement, not of the book. **Recorded as a KILL for path 4a.**

## 8. Gates (18/18) and caveats

G1 `fast_run == engine.backtest` on all three panels at 10 and 25 bps (≤ 3.469e-17). **G2 the standing
memo's 12 published numbers reproduce at max |Δ| 2.76e-04.** G3 addendum A1 reproduces exactly (U56
PANEL t0.16 L20 d1 → OOS MaxDD −20.7709%, 4b OOS FAIL). G4 twin realised-mean-gross match ≤ 4.441e-16.
G5a/G5b as in §2. G6 no NaN. **G7 addendum A2 reproduces (PANEL-sourced clears 4b 0 of 20 on SMALL665).**

**Survivorship, stated:** U56 and B136 are CURRENT constituents; SMALL665 is a current sub-$2B screen
(54 names with `max_1d_move ≥ 1.0` dropped, 667 columns incl. SPY). Every pass-count above is therefore
the optimistic read. The *source contrasts* are same-tape, same-names and first-order immune to this;
the *pass counts* are not. No chooser statistic reads a row on or after 2017-01-01.

**RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are UNTOUCHED by this run (rule 6).** The
standing candidate's status is unchanged: **PARK**, per ideas 1771 and 1767. This run removes one of its
stated caveats (point 8) and adds one line to any future wording — name the sigma's SOURCE, and note
that inside `t ∈ {0.10, 0.12}` the public SPY series serves as well as the panel's own.
