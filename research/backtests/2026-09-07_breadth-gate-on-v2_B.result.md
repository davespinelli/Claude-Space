# Idea 42 — breadth-gate-on-v2 (lane B, 2026-09-07)

**Verdict: KILL of the queue's premise, on the sharpest possible evidence — 0 of 486 grid
points move the book in the direction of the bar it fails.** No KEEP-candidate, no new book,
rules unchanged. One reproduction gate passed; one bounded, panel-specific by-product.

Script: `2026-09-07_breadth-gate-on-v2_B.py` ·
data: `.grid.csv`, `.deltas.csv`, `.matched.csv`, `.walkforward.csv`, `.breakeven.csv`,
console: `.console.txt`

## The question

The queue pairs two 4b near-misses that fail on **opposite** bars and proposes carrying the
instrument from one to the other: idea 40's top-n book misses the **drawdown cap** by 0.4pp
and is fixed by a 200d-breadth gate; idea 28's EWALL book (equal-weight every eligible name)
misses the **CAGR floor** by 0.23pp "with drawdown to spare". Does the gate close the second
miss too?

## Design

* **Book (fixed, not tuned)** `EWALL(G)`: eligible = above own 200d MA and vol20 < 0.60
  (RULES v1's filter); hold every eligible name at `G / E_t`; weekly; next-day; cash otherwise.
* **Overlay (idea 40's instrument, verbatim)** `GATE(B, depth)`: carry the book at
  `1 - depth` of its exposure whenever panel breadth (share of names above their own 200d MA)
  is below `B`, the rest in cash at 0%. Decided at t, effective t+1, paying the cost rung on
  `|Δmult| · G` of notional.
* **Tuned (2, PROTOCOL rule 4):** `B ∈ {0.30, 0.40, 0.50}` × `depth ∈ {0.25, 0.50, 1.00}`.
  All 9 points reported.
* **Reported, never selected on:** gross {0.75, 0.85, 1.00} (idea 28's required axis),
  cadence {daily, weekly}, cost {0, 10, 25} bps, panels {U56, B136, SMALL484}.
  **486 gate rows + 27 ungated controls + 27 references, all reported.**
* Three predictions were written into the script header **before any number was read**:
  P1 the gate cannot raise CAGR; P2 any 4b rescue must come from a *risk* bar, not the CAGR
  bar; P3 the honest comparand is a static gross at the same mean exposure.

## Reproduction gate

Idea 84 (2026-09-04, `which-4b-bar-binds_B`) published the ungated EWALL book on U56 at
g = 0.85, 10 bps as **11.8% / 1.05 / −17.9% / H 1.07 / 1.04**. This run, from an independently
written harness: **11.8% / 1.05 / −17.9% / H 1.07 / 1.03** — MATCH at published precision.

## Results

**P1 — the gate cannot raise CAGR: 0 of 486.** Every gate point loses CAGR to its own ungated
parent at the same panel/gross/rung/cadence. Median ΔCAGR **−1.05pp**, best case **−0.01pp**,
worst **−8.29pp**. By depth: −0.5 / −1.1 / −2.3pp at depth 0.25 / 0.50 / 1.00. The instrument
the queue proposed only ever moves the book *away* from the bar it fails. ΔSharpe is a coin
flip (198/486 positive, median −0.0091); the gate does buy drawdown (345/486 shallower,
median +1.06pp) — the axis the book already had to spare.

**The near-miss reproduces, and was already closed by the gross dial two days earlier.**
Ungated EWALL on U56 at g = 0.75, 10 bps: 10.4% / 1.049 / −15.9%, failing 4b on the **CAGR
bar alone** by 0.3pp with 4.4pp of drawdown margin unused — the queue's number. At g = 0.85
the same book clears all five 4b bars (11.8% / 1.049 / −17.9%, halves 1.069/1.035, OOS 1.112
vs SPY 0.882); at g = 1.00 it breaches the DD cap. B136 clears 4b ungated at both g = 0.75
(10.7% / 1.026 / −17.7%, OOS 1.019) and g = 0.85. SMALL484 fails all five bars at every gross.

**P2 — every rescue is a drawdown rescue: 21 of 21.** Across the whole grid the gate turns a
failing parent into a 4b pass 21 times. In **all 21** the parent's failing bar is `DD`, and
**all 21 sit at gross = 1.00** — i.e. the gate is being used to buy back the drawdown that
raising gross created. **Zero** rescues of a CAGR failure, at any panel, gross, cadence or
rung. KEEP-path footprint: 4b at 10 bps **gate 34/162, control 3/9**; at 25 bps **0/162 and
0/9**; 4a **0/486 and 0/27** everywhere.

**P3 — against a matched-gross static twin the gate is a coin flip, and a panel-specific one.**
Replacing `GATE(B, depth)` at g = 0.75 with a static gross equal to the gate's own realised
mean exposure: gate wins on Sharpe **24/54**, median **−0.0108**. By panel: U56 **15/18,
median +0.0216**; B136 7/18, −0.0068; SMALL484 2/18, −0.0425. 4b: gate 0/54, static 0/54.
So whatever the gate is worth, it is worth ~2 Sharpe points on one panel of three and is
negative on the other two.

**Cost tolerance — the gate never buys any.** Breakeven `c*` (highest rung in 10–40 bps still
inside 4b), pre-registered arms only: U56 g = 0.85 ungated **c\* = 20 bps** (first fail 22);
B136 g = 0.75 **10**, g = 0.85 **18**; SMALL484 nowhere. Gate `c*` beats its parent's in
**4/27** arms — all four at g = 1.00, where the parent fails the DD cap at every rung —
equal in 14, worse in 9, median gap **−6 bps**. The best `c*` any gated arm reaches anywhere
(U56 g = 1.00, B = 0.40, depth 0.50: **20 bps**) is **exactly** the plain gross dial's 20 bps
at g = 0.85, reached with two fewer tuned parameters and one fewer instrument.

**Rule 8 walk-forward** — (B, depth) chosen on 2009–2016 IS Sharpe at g = 0.75, 2017–2026 read
once, 18 cells (3 panels × 3 rungs × 2 cadences). The chooser beats **doing nothing** in
12/18, but by a median of **+0.0100** Sharpe; it beats the grid-mean anchor in only **3/18**,
median regret vs the best OOS point **−0.0874**; it clears SPY OOS in 12/18. U56 @10 bps
(daily): picks B = 0.40 / depth 0.25, OOS **11.1% / 1.156 / −15.1%** against the ungated
parent's **11.3% / 1.112** and RULES v2's OOS 1.285. On SMALL484 the chooser picks
depth = 1.00 at every rung and loses **−0.403** of OOS Sharpe to doing nothing (OOS CAGR
−0.3% vs +5.1%) — another entry in the record's running tally of an IS chooser losing to
doing nothing (ideas 141/151/155/229/246), and the largest yet on this instrument.

## What this settles

1. A **de-grossing instrument cannot repair a CAGR-floor miss.** This is now measured, not
   argued: 0/486, on three panels, three gross levels, three cost rungs and two cadences.
   The queue's "the two near-misses fail on opposite tests" is exactly why the transfer had
   to fail — the instrument only moves the axis that was already passing.
2. The EWALL book's CAGR miss is a **gross-level artefact**, closed at g = 0.85 (U56) and
   already at g = 0.75 (B136), reproducing idea 84 to published precision. It is not a new
   candidate: it dies between 20 and 22 bps on U56 and between 18 and 20 on B136, joining
   the record's standing class of 10-bps objects (ideas 44/47/323).
3. The gate's residual value, honestly bounded, is **+0.02 Sharpe on U56 at matched exposure
   and nothing anywhere else** — not enough for two tuned parameters.

## Caveats

Survivorship: all three panels are current-constituent lists, so absolute CAGRs are
optimistic; the gated-vs-ungated and gated-vs-matched-gross contrasts are the durable parts.
SMALL484's breadth series sits on a different level entirely (mean 0.386 vs 0.687) so
B ∈ {0.30, 0.40, 0.50} fires on 26%/52%/84% of its days against 7%/12%/17% on U56 — its
depth = 1.00 arms are a near-permanent cash position, which is why they collapse. That is a
property of a fixed absolute threshold on a panel with different breadth, and is reported
rather than repaired (repairing it would be a third tuned parameter).
