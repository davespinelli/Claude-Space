# Idea 742 — price the STANDING 4b CANDIDATE against an EQUAL-WEIGHT BENCHMARK

**cloud lane, 2026-09-11.** Script `2026-09-11_price-the-STANDING-4b-CANDIDATE-against-an-EQUAL-WEIGHT-BENCHMARK_cloud.py`.
Two tuned parameters: **benchmark form (5) × panel (3)**; every grid point reported (75 full-sample
cells, 75 walk-forward cells). Book fixed at the memo's specification — RULES v2 band 0.03, weekly,
10 bps, next-day, de-gross to cash, **SPY-free frame** — gross moved only inside rule 8.

## ANSWER — the standing candidate's 4b pass is a COMPARAND FACT. It survives **0 of 9** equal-weight bars.

| | B_SPY (PROTOCOL bar) | B_EW | B_EW10 | B_EWBH | B_HALF |
|---|---|---|---|---|---|
| **U56** | **4b PASS** | FAIL (CAGR) | FAIL (CAGR) | FAIL (H1, CAGR) | FAIL (CAGR) |
| **B136** | **4b PASS** | FAIL (H1, H2, CAGR) | FAIL (H1, H2, CAGR) | FAIL (H1, CAGR) | FAIL (CAGR) |
| **SMALL439** | FAIL (H1,H2,OOS,CAGR) | FAIL (H1,H2,OOS,CAGR) | FAIL (H1,H2,OOS,CAGR) | FAIL (H1) | FAIL (H1,H2,OOS,CAGR) |

Full-sample 4b over the whole 75-cell grid: **2/75, and both are B_SPY cells.** Out of sample
(rule 8, gross picked on IS alone): **7/75 overall, 3/15 at the IS pick**, of which the only
equal-weight passer is SMALL439 under `B_EWBH`, a degenerate bar (see caveat 3).

## Gates (all pre-registered, all PASS)

| gate | result |
|---|---|
| G1 memo reproduction (U56 g1.00 full + OOS vs memo lines 3–4) | max&#124;Δ&#124; **4.954e-05** — matches memo line 9c's own 4.95e-05 SPY-free figure exactly |
| G2 PROTOCOL bar (U56 SPY b&h = 15.11% / 0.8835 / −33.72%) | 2.743e-05 |
| G3 EW sanity (1 col == that col; all cols @0bps == mean live return) | 0.000e+00 / 4.163e-17 |
| G4 the bars are distinct (&#124;ΔSharpe(B_EW,B_SPY)&#124; on U56 > 0.01) | **0.2522** (idea 548 measured +0.2388 on its own large-cap pool) |
| G5 blend (B_HALF == ½(B_SPY+B_EW)) | 0.000e+00 |

## The five bars

| panel | bar | CAGR | Sharpe | MaxDD | H1 | H2 | OOS CAGR | OOS Sharpe | 4b CAGR floor | 4b DD cap |
|---|---|---|---|---|---|---|---|---|---|---|
| U56 | B_SPY | 15.11% | 0.8835 | −33.72% | 0.9595 | 0.8211 | 15.24% | 0.8721 | 10.58% | 20.23% |
| U56 | B_EW | 17.94% | 1.1357 | −28.87% | 1.2129 | 1.0743 | 18.64% | 1.1448 | **12.56%** | 17.32% |
| U56 | B_EW10 | 17.94% | 1.1356 | −28.87% | 1.2128 | 1.0742 | 18.64% | 1.1447 | 12.56% | 17.32% |
| U56 | B_EWBH | 23.39% | 1.0326 | −47.31% | 1.3316 | 0.9377 | 27.10% | 1.0124 | 16.37% | 28.39% |
| U56 | B_HALF | 16.55% | 1.0098 | −31.31% | 1.0881 | 0.9466 | 16.96% | 1.0077 | 11.58% | 18.79% |
| B136 | B_SPY | 15.23% | 0.8890 | −33.72% | 0.9566 | 0.8340 | 15.45% | 0.8820 | 10.66% | 20.23% |
| B136 | B_EW | 19.22% | 1.1361 | −32.52% | 1.2469 | 1.0373 | 18.90% | 1.1148 | 13.46% | 19.51% |
| B136 | B_EWBH | 21.08% | 1.0793 | −34.21% | 1.3126 | 0.9677 | 23.01% | 1.0428 | 14.75% | 20.53% |
| B136 | B_HALF | 17.23% | 1.0137 | −33.12% | 1.1031 | 0.9368 | 17.19% | 0.9995 | 12.06% | 19.87% |
| SMALL439 | B_SPY | 14.13% | 0.8615 | −33.72% | 0.8907 | 0.8577 | 15.45% | 0.8820 | 9.89% | 20.23% |
| SMALL439 | B_EW | 14.35% | 0.7249 | −45.61% | 0.8648 | 0.6481 | 13.91% | 0.6725 | 10.04% | 27.36% |
| SMALL439 | B_EWBH | 5.47% | 0.3826 | −42.65% | 0.6208 | 0.2611 | 4.34% | 0.3091 | 3.83% | 25.59% |
| SMALL439 | B_HALF | 14.44% | 0.8188 | −37.53% | 0.9067 | 0.7742 | 14.95% | 0.8010 | 10.11% | 22.52% |

(B136 B_EW10 = 19.22% / 1.1361 / −32.52%; SMALL439 B_EW10 = 14.34% / 0.7246 / −45.61%. Rebalancing
cost is worth **≤ 0.0004 of Sharpe** on every panel, so the 0-bps and cost-matched equal-weight bars
are the same bar — the "EW at zero cost flatters the bar" objection is quantitatively dead.)

## Which leg binds, and by how much

The candidate does **not** lose the Sharpe contest on U56 — it wins it. It loses the **CAGR floor**:

* **U56, B_EW:** candidate 11.55% / 1.2067 / −15.70%, halves 1.2405 / 1.1798. Bar 17.94% / 1.1357 /
  −28.87%, halves 1.2129 / 1.0743. Margins **H1 +0.0277, H2 +0.1055, OOS +0.1380, DD +1.61 pp,
  CAGR −1.00 pp/yr.** Four legs of five pass; the CAGR floor (12.56%) misses by 1.00 pp. OOS the
  miss narrows to **−0.35 pp** (candidate 12.70% vs floor 13.05%) with all four other legs still clear.
* **B136, B_EW:** the candidate loses outright — H1 −0.0146, H2 −0.0523, OOS +0.0047, CAGR −2.72 pp.
  Equal-weighting the same 135 large caps beats the band book on both halves before any cost.
* **SMALL439:** fails under every bar including SPY. Not a candidate panel and never was.

Across the 75 failing-cell legs the binding counts are **CAGR 71 · H1 45 · H2 30 · OOS 20**.

## Rule 8 walk-forward (gross chosen on IS ≤ 2016-12-31 alone, 2017–2026 read once)

The IS selector picks **gross 1.00 on all three panels**, and — as memo line 8 warned — it is a coin
toss: the IS-Sharpe spread across the whole ladder is **1.08e-03 (U56) / 2.22e-03 (B136) /
2.51e-03 (SMALL439)**. At the pick:

| panel | OOS CAGR | OOS Sharpe | OOS MaxDD | vs B_SPY | vs B_EW | vs B_EW10 | vs B_EWBH | vs B_HALF |
|---|---|---|---|---|---|---|---|---|
| U56 | 12.70% | 1.2827 | −15.70% | **PASS** | FAIL (CAGR −0.35 pp) | FAIL (CAGR) | FAIL (H1, CAGR) | **PASS** |
| B136 | 10.66% | 1.1195 | −16.08% | FAIL (CAGR −0.16 pp) | FAIL (H2, CAGR) | FAIL (H2, CAGR) | FAIL (H1, CAGR) | FAIL (CAGR) |
| SMALL439 | 5.02% | 0.5657 | −19.21% | FAIL (H1,H2,OOS,CAGR) | FAIL (H1,H2,OOS,CAGR) | FAIL (H1,H2,OOS,CAGR) | **PASS** | FAIL (H1,H2,OOS,CAGR) |

SPY OOS: 15.24% / 0.8721 / −33.72% (U56 frame), 15.45% / 0.8820 / −33.72% (B136/SMALL439 frames).
RULES v2 (live, g0.75) OOS: U56 9.48% / 1.2834 / −11.90%, B136 7.98% / 1.1206 / −12.18%,
SMALL439 3.84% / 0.5665 / −14.70%.

## KEEP path 4a — untouched by this run, and still 0

4a's comparand is RULES v2, not a benchmark, so no bar swap can move it: **0/75**. On every panel the
candidate's halves beat live RULES v2 by ~0.001 of Sharpe while its MaxDD is 3.8–4.5 pp deeper, which
fails 4a's drawdown leg by construction (gross is a pure scale on a de-grossing book at a zero cash
rate). U56 1.2405/1.1798/−15.70% vs 1.2400/1.1806/−11.90%.

## VERDICT: **KILL the 4b claim as stated.** No new KEEP-candidate; the standing one is downgraded to PARK.

The memo's "4b PASSES" on U56 and its "4b passes full-sample" on B136 are true **only against
cap-weighted SPY**. Against an equal-weight basket of the candidate's own names — the construction
the book itself uses — the pass does not exist on any panel, full-sample or out of sample. Idea 548's
+0.2388 large-cap equal-weighting premium reproduces here at **+0.2522 on U56 and +0.2471 on B136**,
and that premium is larger than every surviving 4b margin the memo quotes.

## Caveats

1. **Survivorship cuts both ways here.** `universe.json` / `universe_broad.json` are current
   constituents and the small panel is a current screen (`data/SMALL_PANEL_README.md`), so every
   absolute number is inflated — but the equal-weight bar is built from *the same survivors as the
   book*, so the **swap** is survivorship-neutral. If anything the bias flatters the bar less than the
   book, since the book concentrates in whichever survivors trended.
2. **SMALL439** drops the 44 names with `max_1d_move >= 1.0` from `data/small_meta.csv` as this run's
   mandate requires; 439 of 483 remain, since 2010.
3. **`B_EWBH` is a degenerate bar and its one OOS pass should not be read as a result.** Buy-and-hold
   equal weight lets the winners run for 16 years, so on U56 it is the hardest bar of all (23.39%
   CAGR) while on SMALL439 it is the easiest (5.47% CAGR, Sharpe 0.3826) — the small panel's
   compounding losers drag a never-rebalanced basket to nothing. The SMALL439 `B_EWBH` OOS "pass" is
   a statement about that bar, not about the book.
4. **Single-anchor reading.** Per memo line 9c(ii), a 4b verdict quoted at one month-end is not the
   same claim as one quoted at the next; `prices.csv` is 2026-09-10, `prices_broad`/`small` 2026-09-04.
5. Both 4b bars remain window-bound and benchmark-relative; this run changes the benchmark, not that.

## PROPOSED (not applied — PROTOCOL rule 6)

PROTOCOL rule 4's 4b path should require **both** margins: *"any 4b claim on an equal-weight book must
quote its margin against an equal-weight basket of the book's own panel alongside the SPY margin, and
a pass under SPY alone is reported as PARK, not KEEP."* RULES.md, PROTOCOL.md, scan.py, bot.py and
baseline.py are untouched by this run.

Memo `2026-09-11_u56-v2band-gross100_4b_cloud_MEMO.md` amended at line 9d with this result.
