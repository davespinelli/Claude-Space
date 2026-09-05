# idea 177 — publish-the-failing-bar-not-the-required-gross (cloud, 2026-09-05)

**ANSWERED, and for once the answer is YES: the failing-bar string is the first proposed
LEADERBOARD column in this project that carries real decision content. It earns a REPORT-ONLY
schema column. It is NOT a KEEP and promotes no book; and the run's rule-8 arm breaks the
project's do-nothing streak — but it breaks it with a pre-registered CONSTANT, not a selector.**

Script `2026-09-05_publish-the-failing-bar-not-the-required-gross_cloud.py`; outputs
`.console.txt`, `.grid.csv`, `.repro.csv`, `.repair.csv`, `.naming.csv`, `.walkforward.csv`.

## Corpus and reproduction (2 of 2 exact)

Idea 165's corpus, rebuilt not read: 3 panels x 7 keys x 9 shares = 189 genuine weight paths
x 2 cost rungs = **378 books**, weekly, t+1, gross 0.75 `norm` construction. Plus 4 repair
instruments x 2 dials x 189 paths = **1512 further genuine backtests** (1701 in total, 2056 s).

* **[a] cost identity** — the second cost rung is derived as `r0 − turnover·bps/1e4` from one
  0 bps run; against genuine `cost_bps=25` re-runs on 9 books, max |diff| **0.000e+00**.
* **[b] against idea 165's published `.grid.csv`** — 378 of 378 rows matched; n 0.0, CAGR
  9.71e-17, Sharpe/H1/H2/OOS_Sharpe 2.22e-16, MaxDD 8.33e-17. **All MATCH. P1 HIT.**

## The column is not degenerate (P2 HIT)

**55 of 378 books pass 4b on the full sample; 323 fail, across 19 distinct failing strings.**
Bars failed per failing book: 1→49, 2→54, 3→40, 4→44, **5→136**. **84.8% fail ≥ 2 bars**, so
"first-named" is a real choice and the naming rule is a genuine parameter. The commonest string
is the total failure `H1|H2|OOS|DD|CAGR` (136), then `H1|H2|OOS|CAGR` (25), `H1` (21),
`H2|OOS|DD` (21).

First-named bar by naming rule (failing books only) — the rules disagree sharply:

| bar | CANON | TIGHT | TIGHTZ |
|---|---|---|---|
| H1 | 238 | 96 | 91 |
| H2 | 59 | 166 | 68 |
| OOS | 0 | 25 | 13 |
| DD | 15 | 23 | **107** |
| CAGR | 11 | 13 | 44 |

**P4 SPLIT.** DD *is* the modal first-named bar under TIGHTZ (107 of 323) — first clause HIT.
But the corpus-modal fixing instrument is **WIDE** (52 books fixed) and **SLOW** (38), not GDN
(19) or GUP (6) — second clause MISS.

## Does the first-named bar predict the repair? (P3 MISS — reading (A) survives)

Books fixed to a full-sample 4b pass, of the 323 failing:

| instrument | MILD | STRONG |
|---|---|---|
| GUP raise gross | 5 | 1 |
| GDN cut gross | 13 | 6 |
| WIDE more names | 16 | 36 |
| SLOW monthly/quarterly | 38 | 0 |

Accuracy of the corpus-modal `bar1 → instrument` map against a base-rate control and a
2000-draw permutation null on the bar1 labels:

| naming | dial | scope | n | acc | base rate | lift | perm p |
|---|---|---|---|---|---|---|---|
| CANON | MILD | FIXABLE | 61 | 0.885 | 0.623 | **+26.2pp** | 0.0000 |
| TIGHT | MILD | FIXABLE | 61 | 0.885 | 0.623 | **+26.2pp** | 0.0000 |
| TIGHTZ | MILD | FIXABLE | 61 | 0.885 | 0.623 | **+26.2pp** | 0.0000 |
| TIGHTZ | MILD | ALL_FAILING | 323 | 0.616 | 0.368 | **+24.8pp** | 0.0000 |
| CANON/TIGHT | MILD | ALL_FAILING | 323 | 0.467 | 0.368 | +9.9pp | 0.0000 |
| all three | STRONG | FIXABLE | 41 | 0.829 | 0.829 | +0.0pp | 1.0000 |

**At the MILD dial reading (A) DIAGNOSTIC wins under all three naming rules: +26.2pp over the
base rate at p < 0.0005, with a stable and mechanically sensible map
`CAGR→SLOW, DD→GDN, H1→SLOW, H2→WIDE`.** At the STRONG dial reading (B) BOOKKEEPING wins: the
map collapses to "WIDE everywhere", lift 0.0pp, p 1.0 — a strong instrument dominates every
book regardless of what failed. **P3 was pre-registered as a conjunction ("lift < 10pp under
every naming rule AND p > 0.05 under at least one"); it is a MISS.**

The weaker target confirms the mechanism directly — P(instrument clears bar B | book fails
bar B), MILD dial: `CAGR` is cleared by GUP 0.305 / SLOW 0.329 and by GDN 0.000; `DD` by GDN
0.287 and by SLOW 0.005; `H1/H2/OOS` by SLOW 0.44/0.42/0.36 and by GDN 0.000. **The bars are
not five readings of one quantity: each names a different lever, and the wrong lever clears it
essentially never.**

## Rule 8 (bar1 and the map fitted on IS ≤ 2016-12-31; 2017–2026 read once, 361 cells)

| dial | arm | OOS Sharpe | OOS CAGR | OOS MaxDD | Δ vs S0 (t, W/L) | OOS 4a | OOS 4b |
|---|---|---|---|---|---|---|---|
| — | **S0 do-nothing** | **0.6856** | 9.58% | −26.17% | — | **107** | **67** |
| MILD | S1 map (CANON) | 0.8009 | 11.73% | −28.14% | +0.1153 (t +16.96, 284/77) | 86 | 53 |
| MILD | **S2 constant = SLOW** | **0.8113** | **12.19%** | −28.74% | **+0.1257 (t +18.56, 303/58)** | 69 | 51 |
| MILD | S3 random | 0.7184 | 9.88% | −26.40% | +0.0328 (t +6.50, 209/152) | 103 | 40 |
| STRONG | S1 map (CANON) | 0.6647 | 9.50% | −31.08% | −0.0209 (t −2.82, 168/193) | 51 | 3 |
| STRONG | S2 constant = SLOW | 0.6555 | 9.94% | −32.37% | −0.0301 (t −4.01, 165/196) | 21 | 0 |
| STRONG | S3 random | 0.6874 | 8.98% | −26.43% | +0.0018 (t +0.39, 176/185) | 97 | 27 |

Benchmarks over the same window — SPY OOS 15.45%/0.8820/−33.72%; RULES v1 @10bps u56
7.73%/0.7471/−13.83%, broad 5.94%/0.5763/−21.19%, small 7.92%/0.5807/−32.84% (@25bps
3.78%/0.3992, 1.11%/0.1554, 2.67%/0.2501).

**P5 MISS — the eight-run do-nothing streak breaks here, but read what beat it.** The winner is
**S2, a pre-registered CONSTANT ("rebalance monthly")**, not a fitted selector: S2 > S1 at every
naming rule and every dial, exactly as ideas 175/189 predict. The fitted map beats do-nothing
only because it inherits SLOW from the constant. And the Sharpe gain is **bought with
drawdown**: MaxDD deepens from −26.17% to −28.74%, and both KEEP-path counts FALL (4a 107→69,
4b 67→51). **On the bars that decide capital, do-nothing still wins.**

**P6 MISS** — 55 of 378 untreated books pass full-sample 4b, above the pre-registered < 40.
**No book is promoted by this run**; no treated cell beats its own untreated 4b count.

## Verdict — REPORT-ONLY schema column (not a KEEP, not a gate)

Idea 165's `g_req` cost ~2000 backtests and re-labelled ≤ 2.3% of CAGR-floor KILLs. The failing
bar string costs **nothing** — every backtest already computes it — and at the MILD repair dial
it predicts the repairing instrument at +26.2pp over the base rate with p < 0.0005. Proposed
wording (report-only, **RULES.md untouched**):

> **5b.** Every LEADERBOARD row that fails 4b records `failing` — the failed bars in the
> canonical order `H1|H2|OOS|DD|CAGR` — and `bar1`, the tightest bar by margin scaled by that
> bar's corpus SD (TIGHTZ). The column is DIAGNOSTIC, not a gate: it names the lever most
> likely to repair the book (`CAGR→slower cadence or more gross`, `DD→less gross`,
> `H1/H2/OOS→slower cadence`, ties→more names), and it is informative only for SMALL changes to
> the book. A large enough change to any dial dominates every book regardless of which bar
> failed, so no verdict may be taken from `bar1` at a strong dial.

## Predictions: P1 HIT, P2 HIT, P3 MISS, P4 SPLIT, P5 MISS, P6 MISS

## Caveats carried

Survivorship: all three panels are current constituents (idea 54); the small panel is the
sub-$2B screen with the 44 `max_1d_move ≥ 1.0` tickers dropped and a joined, never-selectable
SPY. Absent delistings inflate every CAGR here, so every 4b CAGR-floor margin is optimistic and
**no level in this file is an achievable return.** Idea 128: the IS window's SPY drawdown is
shallower than the OOS window's, so the IS-read DD bar sits on a window that cannot express a
deep drawdown — this works against P4 in the walk-forward and is not adjusted for. Idea 165:
CAGR is not monotone in gross under `engine.py`, so GUP/GDN are scans, not levers, and "the
instrument that fixes it" is always relative to the two dial values tested. The 361 rule-8
cells share three price panels and are not independent, so every t-stat above is optimistic.
t+1 execution only (idea 126). This run classifies existing books; it cannot promote one.
