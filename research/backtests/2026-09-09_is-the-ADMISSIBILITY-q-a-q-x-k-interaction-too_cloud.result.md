# Idea 526 — is the admissibility q a (q × k) interaction too? (cloud, 2026-09-09)

Run: `research/backtests/2026-09-09_is-the-ADMISSIBILITY-q-a-q-x-k-interaction-too_cloud.py`
(re-runnable analysis-only with `--reuse`; artefacts `.arms.csv` 1,260 rows, `.grid.csv` 85 cells,
`.ewall.csv`, `.pairs.csv` 175 pairs, `.rho.csv`, `.walkforward.csv`, `.keeppaths.csv`, `.console.txt`).

**VERDICT: ANSWERED — YES, PARTLY, AND ONLY FOR TWO OF THE FIVE BARS. The two bars idea 285 found
reversing across book size (the DD cap and the CAGR floor) are ordered by CONCENTRATION n/k, not by
n; the three Sharpe bars (H1, H2, OOS) are ordered by n, not by n/k. There is therefore no single
"binding bar is a function of X" statement: the admissibility surface is (q × k × n) and the answer
to the queue's either/or is BOTH, split by which bar you ask about. KILL as a candidate — no KEEP,
no memo, no RULES change.**

## What was run

Idea 276's MIX rebuilt exactly as ideas 285/286 rebuilt it: k names per panel, a share q drawn from
the sub-$2B panel and 1−q from the large-cap **stock** pool (the 38 ETFs excluded), one common
window (the small panel's trading days, 2010-01-04 .. 2026-09-04, 4,194 rows), SPY joined as a
benchmark column only. 10 bps, weekly, next-day execution, 260-day warm-up skip. 44 small-cap
tickers with `max_1d_move ≥ 1.0` in `data/small_meta.csv` dropped first (439 usable).

Two tuned parameters, every grid point reported: **k ∈ {20, 40, 80, 100}** and **n ∈ {5, 10, 20, 25,
40, 50}** (n ≤ k). q is *not* tuned — it is held at the five fixed rungs {0, 0.25, 0.5, 0.75, 1.0}
the queue asked for. 4 k × 5 q × 12 draws = **240 panels**, 17 top-n arms + an EWall control +
RULES v2 as the 4a comparand = **1,260 arm-rows**.

**k=136 is not reachable and is reported as k=100.** The queue's "136" is B136's column count, but 36
of those are ETFs and this MIX excludes ETFs from the large-cap pool, leaving **100** large-cap
stocks. A k=136 panel cannot exist at q=0, and a ladder whose top rung only exists above q≈0.27 is
not comparable across q. k=100 is the largest panel that exists at *every* rung.

## 1. The test the queue asked for — matched pairs

Same q, different k; matched either on concentration n/k or on n itself. If concentration governs,
the MATCHED-CONC pairs agree on which bar binds.

| pairing | pairs | binding bars agree | mean \|Δ\| across the five bar pass rates |
|---|---|---|---|
| **MATCHED-CONC** (same n/k) | 70 | **0.6571** | **0.1250** |
| MATCHED-N (same n) | 105 | 0.5429 | 0.1660 |

Concentration wins on both readings, but neither is a law. **Honest caveat: `binding` is an argmin,
and at 12 draws a pass rate of 1.000 or 0.000 is common, so only 25 of 85 cells have a unique
minimum.** Restricted to pairs where *both* cells have a unique minimum the gap widens sharply but
the sample collapses: MATCHED-CONC **0.667 (12 pairs)** vs MATCHED-N **0.250 (12 pairs)**. The
tie-free column (mean |Δ| in the five pass rates, which needs no argmin at all) points the same way
at full sample size: 0.1250 vs 0.1660.

## 2. The result that actually matters — the split is BY BAR

|ρ| of each bar's pass rate against each predictor, averaged over the five q rungs (17 cells per rung):

| bar | vs log n | vs log(n/k) | vs log k | ordered by |
|---|---|---|---|---|
| **DDcap** | 0.746 | **0.897** | 0.227 | **concentration** |
| **CAGRfloor** | 0.392 | **0.685** | 0.470 | **concentration** |
| H1 | **0.592** | 0.385 | 0.219 | book size |
| H2 | **0.541** | 0.514 | 0.233 | book size (marginal) |
| OOS | **0.563** | 0.505 | 0.106 | book size (marginal) |
| joint 4b | 0.405 | 0.425 | 0.064 | neither |
| 4a | 0.078 | 0.388 | 0.371 | (1 pass in 1,260 — no content) |

The two bars idea 285 reported reversing across n are exactly the two that are concentration
statements; the three Sharpe bars are not. So idea 285's headline ("the binding order reverses
across book size") is **restated, not overturned**: at fixed k, changing n changes n/k too, and the
reversal it saw travels with n/k, while the Sharpe bars it saw travel with n.

## 3. Rule 8 walk-forward (PROTOCOL 8) — the (k, n) cell chosen on IS Sharpe ≤ 2016-12-31, 2017-01-01 .. 2026-09-04 read once

| q | pick k / n / conc (median) | OOS CAGR | OOS Sharpe | OOS MaxDD | RULES v2 OOS Sharpe | SPY OOS Sharpe | beats SPY | beats v2 |
|---|---|---|---|---|---|---|---|---|
| 0.00 | 60 / 10 / 0.25 | 12.4% | 0.949 | −20.5% | 1.142 | 0.882 | 58.3% | 0.0% |
| 0.25 | 80 / 20 / 0.25 | 11.1% | 0.906 | −19.5% | 1.085 | 0.882 | 58.3% | 0.0% |
| 0.50 | 60 / 20 / 0.50 | 9.4% | 0.774 | −16.5% | 0.934 | 0.882 | 33.3% | 16.7% |
| 0.75 | 40 / 5 / 0.25 | 5.2% | 0.465 | −27.6% | 0.644 | 0.882 | 0.0% | 16.7% |
| 1.00 | 100 / 32.5 / 0.40 | 1.9% | 0.225 | −26.7% | 0.496 | 0.882 | 0.0% | 8.3% |

SPY OOS: CAGR 15.45%, Sharpe 0.882, MaxDD −33.7%. Full common window SPY: CAGR 14.13%, Sharpe 0.862,
MaxDD −33.7%. **Pooled over all 5 rungs × 12 draws the chooser beats SPY OOS on 30.0% of draws and
RULES v2 OOS on 8.3%; joint 4b 8.3%, 4a 0.0%.** A chooser that loses to SPY on 70% of draws and to
the live book on 92% is not a candidate.

## 4. Both KEEP paths on the full grid (no selection: all 1,260 arm-rows)

**4a passes 1/1,260 (0.1%); 4b passes 99/1,260 (7.9%)**, and every 4b pass sits at q ≤ 0.5. The
highest 4b rates in the grid are the *low-concentration* books on the *large* panels — k=100 top50
(0.367), k=80 top40 (0.300), k=100 top40 (0.267) — all at n/k ≈ 0.4–0.5, which is the same
concentration band the 2026-09-04 KEEP 4b candidate (U56 top-20) sits in. No arm clears both halves,
the OOS leg, the DD cap and the CAGR floor at a rate that survives idea 486's random-draw base rate,
so nothing here is promoted.

## Caveats

- **Ties.** 60 of 85 cells have ≥2 bars tied at the minimum pass rate; the argmin reading is only
  as sharp as 12 draws allow. Both the tie-restricted and the tie-free readings are reported above
  and both agree in direction.
- **k=136 → k=100** substitution, stated in §"What was run".
- **SURVIVORSHIP.** The sub-$2B panel and B136 are *current* constituents of their screens, so both
  ends of the q ladder are survivor sets and the LEVEL of every number here is optimistic — in
  particular the q=1 rung's CAGR is biased upward, which makes the CAGR-floor result *conservative*
  and the DD-cap result unsigned. The (q, k, n) CONTRAST is the only thing claimed.
- Two tuned parameters (k, n), all 85 (k, n, q) cells and all 1,260 arm-rows reported; nothing was
  searched over and then quoted at its argmax.

RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py untouched. No memo (no KEEP candidate).
