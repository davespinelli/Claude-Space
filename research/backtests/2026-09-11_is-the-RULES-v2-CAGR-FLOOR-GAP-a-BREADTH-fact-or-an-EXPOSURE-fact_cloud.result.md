# Idea 795 — is the RULES v2 CAGR FLOOR GAP a BREADTH fact or an EXPOSURE fact?

**cloud lane, 2026-09-11.** Script: `2026-09-11_is-the-RULES-v2-CAGR-FLOOR-GAP-a-BREADTH-fact-or-an-EXPOSURE-fact_cloud.py`.
PROTOCOL: 10 bps, next-day execution, weekly, no shorting, no leverage (gross ≤ 1.00). RULES.md / PROTOCOL.md / scan.py / bot.py / baseline.py untouched.

## Verdict — **EXPOSURE, decisively. And it produces a KEEP-candidate on path 4b.**

The 1.22 pp OOS CAGR shortfall is an exposure fact, not a breadth fact. Breadth dilution is
**real but self-cancelling**: the band dial does move return per unit of exposure, and in the
expected direction (Spearman(breadth, ubar) **−0.8571**), but every unit of per-unit return it
buys is paid for out of the exposure it gives up, so the band dial's best achievable
improvement at the live gross is **+0.08 pp/yr**. The gross dial's is **+2.84 pp/yr**.

The rule-8 walk-forward then produces something the record has been hunting: a cell chosen on
2009–2016 alone that clears **all five 4b legs on 2017–2026 read once**. It is a 4b KEEP-
candidate, with three caveats stated below that a Sunday review must weigh. **4a fails, 0 of 35.**

## The decomposition

For the band book, held weights are exactly `gross × breadth_t` units of an equal-weight sleeve
of the in-band names, so with `E_t = Σw`, `G_t = Σw·ret`, `u_t = G_t/E_t`, `c_t` = cost:

    ann mean(r) = 252·(Ē·ū)  +  252·cov(E,u)  −  252·mean(c)
                  EXPOSURE×PER-UNIT   TIMING        COST

This is an identity, not a proxy — **G2 measures it at 5.551e-17** over all 35 cells.

| Gate | Reading | |
|---|---|---|
| G1 the live cell IS the live book | (band 0.03, gross 0.75) Sharpe **1.1998**, MaxDD **−12.05%**, OOS CAGR **9.45%** — all == record and == `baseline.rules_v2_weights` | PASS |
| G2 decomposition identity | max residual **5.551e-17** over 35 cells | PASS |
| G3 gross ≈ pure exposure | Ē/gross spread within a band **5.425e-04** relative; ū spread **5.464e-17** pp/yr | PASS |
| G4 comparands are the record's | SPY full CAGR 15.11% / Sharpe 0.8835 / MaxDD −33.72%; OOS CAGR 15.24% / Sharpe 0.8721; 4b floors 10.58% (full) / 10.67% (OOS), DD caps −20.23% | PASS |

## Which leg carries it

Over all 35 cells: **corr(Ē, ann mean r) = +0.9672** against **corr(ū, ann mean r) = +0.0535**.
H_EXP HELD. Pooled over the 34 non-live cells the two-term attribution against the live cell
reads mean |via dĒ| **0.0184** against mean |via dū| **0.0056** — a **3.28x** ratio.

Split by dial, which is the part that answers the queue's question:

| dial (the other frozen at live) | mean \|via dĒ\| | mean \|via dū\| | best Δ ann mean |
|---|---|---|---|
| **BAND** (gross fixed 0.75, 6 cells) | 0.0040 | 0.0063 | **+0.0008** |
| **GROSS** (band fixed 0.03, 4 cells) | 0.0222 | 0.0000 | **+0.0284** |

So the band dial is the one where the per-unit leg *dominates* the exposure leg (0.0063 >
0.0040) — dilution is genuinely the mechanism there — and it is also the dial that **cannot
close the gap**, because the two legs move against each other and nearly cancel. Widening the
band from 0.03 to 0.20 raises ū from **0.1626 to 0.1988/yr** (+22%) while realised breadth falls
**0.711 → 0.609**, and the book's CAGR moves **8.61% → 8.54%**. Concentration works and buys
nothing.

The gross dial has a per-unit leg of **exactly zero** by construction and moves CAGR
**5.72% → 11.52%** (OOS **6.26% → 12.66%**). H_DILUTE HELD; H_EXP HELD.

## 4b footprint on the full sample (all 35 cells reported)

**7 of 35 pass** — every one at **gross 1.00**, at every band on the ladder. The **CAGR floor is
the only binding leg anywhere on the grid** (28 cells fail it; the DD cap, both half-Sharpe legs
and the OOS-Sharpe leg fail 0 cells). **4a passes 0 of 35**: no cell beats the live book's Sharpe
in both halves with MaxDD no worse, because raising gross raises drawdown proportionally and
the live book's −12.05% is the grid's tightest.

**8 of 35** clear the 4b OOS CAGR floor of 10.67% without leverage. H_FLOOR HELD.

## Rule 8 walk-forward — chosen on 2009–2016, 2017–2026 read once

Two pre-registered selectors, both reading IS only. **They pick the same cell.**

* PICK-Sharpe (highest IS Sharpe, gross ≤ 1.00) → **band 0.08, gross 1.00**, IS Sharpe 1.1226.
* PICK-Sharpe | IS-floor (highest IS Sharpe among cells clearing 0.70 × SPY's IS CAGR = 10.47%;
  only **3 of 35** clear it in-sample) → **the same cell**, IS CAGR 10.61%.

| OOS 2017–2026, read once | CAGR | Sharpe | MaxDD | OOS halves |
|---|---|---|---|---|
| **PICK (band 0.08, gross 1.00)** | **12.00%** | **1.1616** | **−19.05%** | 1.2413 / 1.0759 |
| RULES v2 (live) | 9.45% | 1.2747 | −12.05% | — |
| SPY | 15.24% | 0.8721 | −33.72% | 0.9762 / 0.7598 |

**4b legs OOS: Sharpe > SPY PASS · OOS H1 PASS · OOS H2 PASS · MaxDD ≥ −20.23% PASS ·
CAGR ≥ 10.67% PASS → 4b OOS PASS.** H_WF HELD. The same cell also clears all five 4b legs on
the full sample.

### Three caveats the Sunday review must weigh

1. **The gross leg of the pick is a corner solution riding a known convention.** IS Sharpe at
   band 0.08 runs 1.1217 → 1.1226 across a 2x gross range — a **9e-4** spread. That slope is the
   zero-return cash leg (ideas 311 / 576 measured +0.0065/unit), not signal. The selector does
   not *estimate* gross; it always goes to the top of the ladder. What makes gross 1.00 right
   here is the **CAGR floor**, not the Sharpe ranking.
2. **The band leg is noise and the walk-forward paid for it.** At gross 1.00 the IS-chosen band
   0.08 reads OOS **12.00% / 1.1616 / −19.05%** against the live band 0.03's **12.66% / 1.2740 /
   −15.91%**. Tuning the second parameter cost **0.66 pp of OOS CAGR, 0.1123 of OOS Sharpe and
   3.14 pp of OOS drawdown**. It was needed only because no gross at band 0.03 clears the *IS*
   CAGR floor (max 10.16% at gross 1.00 vs a 10.47% bar).
3. **The OOS drawdown margin is thin.** −19.05% against a −20.23% cap is **94% of the budget
   spent** — the live book spends 60%. A single worse episode retires the pass.

**The record's own 2026-09-03 selector has an empty feasible set here** (disclosed post-hoc,
added after the two pre-registered selectors were read): "smallest G whose MaxDD ≤ 60% of SPY's
and CAGR ≥ 70% of SPY's", applied on IS with the band frozen at 0.03, admits **no gross at all** —
low gross fails the CAGR bar, high gross fails the DD bar, because SPY's *IS* MaxDD is only
−22.06% (2008 is outside the panel's scored window) so the IS DD bar of −13.24% is far tighter
than 4b's −20.23%. The KEEP claim does **not** rest on this selector.

## Replication on B136 (reported, never selected)

**SURVIVORSHIP:** `universe_broad.json` is current constituents only, so B136's returns are
biased upward; this is a robustness read, not a capital claim.

corr(Ē, ann mean r) **+0.9776** vs corr(ū, ann mean r) **+0.1349** — exposure dominates, same
direction as U56. Spearman(breadth, ū) **−0.2500** (U56 −0.8571) — the dilution direction
replicates but far weaker, because the broad panel's realised breadth barely moves on the band
dial (0.669–0.710 against U56's 0.609–0.711). The live cell on B136 reads CAGR 8.03%, Sharpe
1.1058, MaxDD −12.24%, OOS CAGR 7.98% against SPY's OOS 15.45% — the same floor gap, one panel over.

## KEEP paths

* **4a (beat the book): FAIL, 0 of 35 cells.** Every cell that raises CAGR raises MaxDD past the
  live book's −12.05%.
* **4b (capital-worthy): KEEP-CANDIDATE.** 7 of 35 cells pass on the full sample; the rule-8
  cell chosen on IS alone passes all five legs OOS. Memo with exact RULES wording:
  `2026-09-11_u56-band008-gross100_4b_cloud_MEMO.md`.

## Artefacts

`.grid.csv` (35 U56 cells × decomposition + IS/OOS metrics), `.broad.csv` (35 B136 cells),
`.attribution.csv` (35 two-term attributions vs the live cell), `.walkforward.csv` (3 selectors),
`.summary.json`, `.console.txt`.
