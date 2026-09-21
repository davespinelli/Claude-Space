# Idea 2060 (lane B, 2026-09-21) — **IS THE STANDING KEEP-4b CELL'S CAGR-FLOOR MARGIN RESOLVABLE? NO.**

**Cell (inherited, nothing tuned):** VOLTGT-DRIFT on B136, `t = 0.10`, `h = 0.08`, trade W, 10 bps,
t+1, gross ≤ 1.00, sigma (L=20, d=0) — the standing KEEP-candidate of
`2026-09-20_voltgt-drift-b136_KEEP4b_MEMO.md`. **Gates 8 of 8 PASS**; the cell reproduces every
published number in that memo to max |d| **4.3e-05** (points 2, 4, 5, the SPY comparand and all
five leg margins), and the live-v2 comparand to 1.1e-05.

**Two tuned parameters, all 30 grid points reported:** block length `B ∈ {5, 10, 21, 63, 126}` ×
seed `∈ {11, 22, 33}`, nboot 4000 each. Paired circular-block resample: book and SPY share the
block offsets inside a draw, and each 4b leg is resampled on the calendar window it is read on.

## THE ANSWER — NO. THE +1.92 pp IS A POINT ESTIMATE AND STAYS ONE.

| | observed | SE (min–max over 30 points) | bootstrap t | two-sided p | fail_share |
|---|---|---|---|---|---|
| **L5 CAGR floor, B136 FULL** | **+1.92 pp** | **1.10 – 1.46 pp** | **+1.32 … +1.76** | 0.068 – 0.181 | 0.041 – 0.099 |
| L1 H1 Sharpe | +0.3600 | 0.139 – 0.148 | +2.43 … +2.60 | — | 0.004 – 0.005 |
| L2 H2 Sharpe | +0.3166 | 0.118 – 0.172 | +1.84 … +2.68 | — | 0.006 – 0.035 |
| L3 OOS Sharpe | +0.4191 | 0.134 – 0.169 | +2.48 … +3.12 | — | 0.001 – 0.006 |
| L4 DD cap | +8.42 pp | 3.34 – 3.86 pp | +2.18 … +2.52 | — | **0.099 – 0.279** |

The CAGR leg **never reaches |t| ≥ 2 at any block length or any seed**. Its 95% percentile band at
the longest block straddles zero: **[−0.30 pp, +4.02 pp]**. The three Sharpe legs do reach it (or
sit on it), so the memo's caveat 7 named the right leg — it just understated the result: the leg is
not *thin*, it is **indistinguishable from a bare pass** at this tape's resolution.

**The SE is a TAPE fact, not a draw-count fact.** Max SE spread across seeds at a fixed `B` is
**0.033 pp** against an SE of 1.41 pp — a factor of 43. The seed axis is a resolution control and
it moves nothing; `B` is the only axis that does (SE falls 1.46 → 1.10 pp from B=5 to B=126, i.e.
longer blocks *help* the margin, and it still fails to resolve).

## THE BY-PRODUCT THE MEMO DOES NOT CARRY — **THE DD LEG IS THE WORST-RESOLVED, NOT THE CAGR LEG.**

By `t`, L4 looks safe (+2.18 … +2.52). By the share of draws in which the leg actually **fails**,
it is the worst of the five: **0.099 – 0.279**, two-to-three times the CAGR leg's 0.041 – 0.099.
The two readings disagree because the bootstrap distribution of a MaxDD contrast is heavily
skewed, so `obs/SE` is the wrong summary for it. **A published "+8.42 pp of drawdown headroom" is
the least reliable of the five legs and no committed row says so.** This is a KILL of the implicit
convention that a leg's `t` ranks its risk.

## THE JOINT READING — **4b IS A ~70% PROPOSITION, NOT A FACT.**

Requiring all five legs *in the same draw*: **joint 4b pass rate 0.635 – 0.856, median 0.715**
(B136) and 0.643 – 0.836 (U56). The point-estimate PASS is real; the record has been quoting it
without the 3-in-10 it comes with.

## COST LADDER (reported, not tuned; B=21, seed=11)

| panel | 0 bps | 10 bps | 25 bps | 50 bps |
|---|---|---|---|---|
| B136 margin / t / joint4b | +2.28 pp / +1.61 / 0.766 | +1.92 pp / +1.36 / 0.716 | +1.40 pp / +0.98 / 0.618 | **+0.52 pp / +0.37 / 0.396** |
| U56 margin / t / joint4b | +2.28 pp / +1.55 / 0.772 | +1.94 pp / +1.31 / 0.719 | +1.43 pp / +0.97 / 0.630 | +0.58 pp / +0.39 / 0.418 |

The SE is flat across the cost ladder (1.42 pp at every rung); the **margin** is what the ladder
spends. **This restates the 2026-09-20 addendum's "4b: 36 of 36 points, 100.0%".** That census is a
point-estimate census: at its own worst corner the joint-leg pass is a **coin flip (0.396)**.

## RULE 8 — WALK-FORWARD, 2017–2026 READ EXACTLY ONCE (all 45 (t, h) cells published per panel)

* **B136.** IS-only chooser (argmax min IS 4b-leg slack, 2009–2016) lands on **`t = 0.10, h = 0.08`
  — the memo's own cell**, reproducing its provenance. OOS read once: **13.01% / 1.2928 / −11.81%**
  vs SPY **15.26% / 0.8737 / −33.72%** vs live RULES v2 **7.85% / 1.1017 / −12.24%**.
  OOS CAGR-floor margin **+2.33 pp**, bootstrap **SE 1.50–2.10 pp, t +1.11 … +1.55**,
  fail_share 0.064–0.147. **The OOS margin does not resolve either.**
* **U56.** The same chooser picks a *different* cell, `t = 0.12, h = 0.25`. OOS **13.55% / 1.2113 /
  −16.49%**; margin **+2.87 pp**, SE 1.35–1.80 pp, **t +1.60 … +2.13** — the only reading in this
  run that touches 2, and only at the longest block.

## BOTH KEEP PATHS (10 bps, t+1)

* **B136 — 4a PASS** (halves 1.3171 / 1.1415 vs live 1.2296 / 0.9669; MaxDD −11.81% vs −12.24%),
  **4b PASS at the point estimate**, held in **71.6%** of paired draws.
* **U56 — 4a FAIL** (MaxDD −13.49% vs live −12.05%), **4b PASS at the point estimate**, held in
  **71.9%** of draws.

**NO NEW KEEP IS FILED.** The book is not new — it is the standing candidate, re-scored. Nothing
here promotes or demotes it on the point estimate; what changes is that the CAGR-floor pass now
carries an error bar, and the error bar contains zero.

## WHAT THIS RUN CANNOT DO (stated, not repaired)

The four calendar windows (H1, H2, OOS, FULL) are resampled independently of each other, which is
an assumption about their joint behaviour, not a fact. A circular-block bootstrap of a drawdown
breaks the single longest loss run by construction, so L4's distribution is conservative-to-noisy —
that is *why* its `t` and its fail_share disagree, and this run reports both rather than choosing.
**SURVIVORSHIP:** B136 and U56 are CURRENT-constituent lists, so every level is optimistic and both
4b bars are easier than on a point-in-time panel; the SE is a same-tape, same-names, paired
contrast and is first-order immune, but the *margin* it is an error bar on is not.

**RESIDUE for the Sunday review (rule 6; RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py
untouched):** a published 4b verdict should carry its **joint-draw pass rate**, and any leg quoted
as headroom should carry its **fail_share** and not only its `t` — the DD leg here is the case where
the two rankings invert.
