# Idea 244 — how-many-published-count-dials-are-gross-dials (cloud, 2026-09-08)

**SPLIT. The channel is REAL, it is undisclosed in half the record's count-dial files, and it flips
verdicts — but its size is a function of PANEL BREADTH, not of the count dial, so idea 240's "the
channel halves the width premium" is a u56 statement and does not generalise. No RULES change, no
book promoted, no KEEP claimed; RULES.md, scan.py, bot.py, baseline.py and PROTOCOL.md untouched.**

Two ways to hold "the top n at equal weight" differ only when fewer than n names are admitted:
**FIXED** `w = g/n` on every admitted name (idea 73's published construction; realised gross
`g·k_t/n`) and **NORM** `w = g/k_t` (gross pinned). Widening n under FIXED therefore de-grosses the
book exactly when breadth is low — a breadth-conditional exposure overlay no count sweep names.

Gates first, all PASS: `fast_bt` vs `engine.backtest` on returns AND turnover **0.000e+00**; the
cost-rung identity **0.000e+00**; FIXED at n=5, g=0.75 nests `baseline.rules_v1_weights` at
**0.000e+00**; **NORM ≡ FIXED on every day with k_t = n** (2.776e-17, 4,434 of 4,699 days at n=5)
— the channel is provably closed off saturation. Note found at the gate and carried: `rank <= n`
drops TIED names, so k_t < n on 265 days at n=5 even where E_t ≥ n; both conventions share that
selection, so the contrast is unaffected, and saturation below is measured on **k_t**, not E_t.

## PART A — census of the committed record (source regex + committed CSVs)

424 committed scripts scanned; **127 carry a count dial in their own source**. Construction:
**FIXED 25 (20%), BOTH 28 (22%), NORM 27 (21%), UNKNOWN 47 (37%)** — UNKNOWN counted, never
guessed. **53 files (42%) contain the FIXED `g/n` construction.**

- **Gross coverage (P1 MISS, narrowly).** **62 of 127 (48.8%)** count-dial files publish no
  realised-gross column — just under the majority predicted. Restricted to FIXED/BOTH files it is
  **27 of 53 (50.9%)**.
- **Exposed population.** 68 count-dial files actually sweep a count column over ≥3 values in
  their committed CSVs; max swept n ≥ 40 in 44 of them and ≥ 60 in 31. **FIXED/BOTH construction
  AND a swept n ≥ 40 — where u56's eligible set runs out — is 17 files, of which 5 publish no
  gross column and are therefore un-checkable from their own artefacts.** That is the answer to
  "how many published count findings are gross-ladder points": at most 17 are exposed to the
  channel, 5 cannot be checked at all, and the rest publish the gross that would settle it.

## PART B — measurement, both constructions built side by side (216 grid points, all reported)

Panels u56 / broad136 / small439 (the 44 `max_1d_move ≥ 1.0` names dropped first); n ∈
{5,10,20,40,60,90}, g ∈ {0.50,0.75,1.00}, weekly, next-day, 10 and 25 bps.

**The channel, realised gross at nominal g = 1.00 (mean over rebalance days) and saturation share:**

| n | u56 | broad136 | small439 |
|---|---|---|---|
| 5 | 0.999 (0.3% sat) | 1.000 (0.1%) | 0.996 (0.5%) |
| 20 | 0.959 (10.7%) | 0.989 (2.4%) | 0.994 (1.0%) |
| 40 | 0.864 (43.5%) | 0.972 (6.9%) | 0.988 (3.1%) |
| 60 | **0.623 (100%)** | 0.947 (13.1%) | 0.974 (7.2%) |
| 90 | **0.415 (100%)** | 0.893 (33.1%) | 0.944 (16.2%) |

Realised gross is **monotone decreasing in n on 6 of 6 grid steps on all three panels**, but P2 is
scored **MISS** on its own wording twice over: its tail condition ("n past the panel's median
eligible count", 41 / 99 / 147) leaves fewer than two grid points on broad136 and small439, and
realised gross falls below 0.6·g at the widest n on **one** panel, not two. The honest statement
is the one the table makes: **the channel is a u56 fact.** With a 56-name panel and a median 41
eligible, n = 60 saturates on 100% of rebalance days and the "n = 60 book" is a 0.62-gross book.

- **Width premium (P3 HIT 3/3).** |Sharpe(n=90) − Sharpe(n=20)| at 10 bps: u56 **0.1266 FIXED vs
  0.0787 NORM (the channel is 38% of the published magnitude)**, broad136 0.2073 vs 0.1794 (13%),
  small439 0.0765 vs 0.0618 (19%). The direction of idea 240's finding replicates everywhere; its
  magnitude ("halves") is u56-sized and roughly a fifth to an eighth elsewhere.
- **Sign flips.** Of 270 pairwise width comparisons (is n₂ better than n₁?), **18 (6.7%) flip sign
  when the channel is closed** — 12 of 90 on u56, 6 of 90 on small439, **0 of 90 on broad136**.
- **Verdict flips (P4 HIT).** Of 108 (panel, n, g, rung) cells, **4 flip their 4b verdict** and 0
  flip 4a. FIXED passes 4b twice, NORM twice — different points. The flips:
  `u56 n=40 g=1.00 @10bps and @25bps` (FIXED passes, NORM fails), `u56 n=10 g=1.00 @10bps` and
  `broad136 n=90 g=0.75 @10bps` (NORM passes, FIXED fails).
- **The cross-link that makes this concrete.** The single 4b-clearing ranked point idea 459 found
  this morning — u56 TOP40 g=1.00, 12.68% / 1.1242 / −18.16% — **is a gross-ladder point**. Its
  realised gross is 0.864, not 1.00; closing the channel restores MaxDD to −21.68%, which is
  outside SPY's 60% bar (−20.23%), and the 4b pass disappears. The count label was carrying a
  gross decision.
- **4a: 0 of 216.** No arm under either convention beats live RULES v2 in both halves with no
  worse MaxDD.

## Rule 8 (n and g chosen on IS ≤ 2016-12-31 by IS Sharpe, 2017–2026 read once) — P5 HIT

| panel @10bps | FIXED pick → OOS CAGR / Sharpe / MaxDD | NORM pick → OOS | RULES v2 | SPY |
|---|---|---|---|---|
| u56 | n=40 g=1.00 → 14.57% / 1.249 / −18.16% | n=60 g=1.00 → 15.15% / 1.113 / −20.88% | 9.53% / 1.285 / −12.05% | 15.45% / 0.882 / −33.72% |
| broad136 | n=40 g=1.00 → 11.94% / 0.871 / −24.30% | n=90 g=1.00 → 14.10% / 1.005 / −23.69% | 7.98% / 1.119 / −12.24% | 15.45% / 0.882 / −33.72% |
| small439 | n=20 g=1.00 → 4.87% / 0.362 / −36.99% | n=20 g=1.00 → 4.47% / 0.333 / −43.73% | 3.85% / 0.568 / −14.68% | 15.45% / 0.882 / −33.72% |

**The convention changes the IS-chosen n on 2 of 3 panels at 10 bps** (u56 40→60, broad136 40→90)
and on 1 of 3 at 25 bps. FIXED minus NORM OOS Sharpe: +0.136 / −0.134 / +0.028 at 10 bps and
+0.189 / +0.104 / +0.020 at 25 bps — the channel is worth more than a tenth of a Sharpe point in
either direction, i.e. it is not a rounding term in a published count finding. Neither convention
beats RULES v2 OOS on any panel (0/6); NORM beats SPY OOS on 4 of 6 cells, FIXED on 3 of 6.

## What this licenses (proposed, not adopted — PROTOCOL 6 is a Sunday matter)

A one-line reporting clause, zero new parameters: **any published count/width sweep must quote the
realised gross of each arm beside its Sharpe, or state that its construction pins gross.** 42% of
the record's count-dial files use the exposed construction and half of those publish no gross
column; the fix costs one column.

## Caveats carried

- **SURVIVORSHIP (idea 54):** all three panels are current-constituent lists with no delistings.
  Every arm inherits it equally, so the FIXED-minus-NORM contrast is largely protected; every
  level is biased upward and none is a tradable estimate. No book is proposed.
- The Part-A construction census is a **regex over committed source**. Anything expressed through
  a helper it cannot read is UNKNOWN (47 of 127) and is counted as UNKNOWN, not inferred. No
  file's verdict is read from its prose.
- Realised gross is the mean over rebalance days of the target weight sum; a book drifts between
  rebalances, so instantaneous gross differs. Both conventions are measured identically.
- 4b verdicts here are functions of SPY's numbers over each panel's own window; cross-panel
  verdict counts are not strictly commensurable.
- Idea 144: a re-dialled book is the same book. Nothing here proposes a new signal.

Artefacts: `.console.txt` `.census.csv` `.channel.csv` `.grid.csv` `.flips.csv` `.walkforward.csv`
`.params.csv`
