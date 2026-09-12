# Idea 846 — is the TIE CONVENTION doing the work in every committed TWIN WIN RATE?
lane C, 2026-09-12 · `2026-09-12_is-the-TIE-CONVENTION-doing-the-work-in-every-committed-TWIN-WIN-RATE_C.py`

## THE ANSWER

**NO to "every", YES to the part the record actually publishes.** Pooled over **310,128 committed
twin cells in 36 win columns across 25 files**, the tie convention is worth **+0.0309** of win rate
(LOSS `0.3634` → WIN `0.3943`, EXCLUDED `0.3753`) — a third-decimal correction, not a headline.
But **30 of those 36 columns carry at least one tie, and all 11 whose rate a sibling memo actually
quotes move.** And the objects the record publishes are not pooled rates, they are **ORDERINGS**,
and those do break: **only 34 of 54 (panel × rung × window × matching) family orderings survive all
three tie rules — and on the WINMATCH/IS cell, 0 of 9 survive.**

The mechanism is exact, not statistical. **G5a: over 594 never-firing (arm, window, rung) cells the
arm's net path and its WINMATCH twin are the same array, `max|d| = 0.000e+00`.** A gate that never
fires inside a window IS the ungated EWALL book its twin is, so `dSharpe` is exactly `0.0`, and
every committed verdict in this repository — `win = dSharpe > 1e-12` — books that as a **LOSS**.
The record has documented the comparand everywhere and the tie rule nowhere.

**KILL for capital. No book promoted, no KEEP claimed, no RULES change.** One PROTOCOL line is
PROPOSED for a Sunday review and NOT applied.

## THE DECISIVE FACT: TIES ARE AN IN-SAMPLE, WARM-UP OBJECT

| matching | mean tie share IS | mean tie share OOS | max&#124;d&#124; | rule 8 on the claim |
|---|---|---|---|---|
| FULLMATCH | 0.0556 | 0.0556 | 0.0000 | PASS |
| WINMATCH | **0.3056** | **0.0556** | **0.6667** | **FAIL** |

Under WINMATCH a rolling-quantile arm has no threshold until its own lookback exists, so it is inert
for most of 2009–2016 and tie-scored there — **in exactly the window rule 8 chooses parameters on**,
and almost nowhere in the window it reads. "Score a tie as a loss" therefore silently restates *"this
dial did not exist yet"* as *"this family lost"*, and does it only in sample. That is why the IS
orderings are the ones that fall over: FULLMATCH/IS 6 of 9 survive, **WINMATCH/IS 0 of 9**.

## WHICH PUBLISHED ORDERINGS SURVIVE ALL THREE (the queue's question)

| | FULL | IS | OOS |
|---|---|---|---|
| FULLMATCH | 8/9 | 6/9 | 6/9 |
| WINMATCH | 8/9 | **0/9** | 6/9 |

At the headline rung (10 bps) the survivors and casualties are:

* **U56 FULL and OOS, both conventions — SURVIVE.** `QROLL>ABS>QEXP` at 1.000/0.833/0.667 under all
  three rules, tie share 0.0000. The record's most-quoted panel is clean.
* **U56 IS / WINMATCH — FAILS.** `QROLL>ABS>QEXP` (LOSS, QEXP `0.000`) vs `QROLL>QEXP>ABS` (WIN,
  QEXP `0.667`). QEXP's entire in-sample win rate on that cell is the tie convention.
* **B136 IS / WINMATCH — FAILS.** `QROLL>ABS>QEXP` vs `QEXP>QROLL>ABS`: the top family changes.
* **B136 OOS, both conventions — FAILS** at 0.0556 ties: `QROLL>ABS>QEXP` (LOSS) vs `QROLL>QEXP>ABS`
  (WIN and EXCLUDED). QROLL stays on top; the 2nd/3rd places swap on 2 arms out of 36.
* **SMALL IS — FAILS under both conventions.** LOSS says `ABS>QEXP>QROLL`, WIN says `QEXP>ABS>QROLL`.

**Reading:** the one ordering leg the record leans on — QROLL on top out of sample — survives all
three tie rules on every panel and rung. Everything *below* first place, and everything read in
sample, does not.

## GATES (all PASS)

| gate | number | verdict |
|---|---|---|
| G1 `fast_run` == `engine.backtest` | max&#124;d&#124; 1.041e-17 | PASS |
| G2 fast metrics == `engine.metrics` | max&#124;d&#124; 0.000e+00 | PASS |
| G3 0.01 gross-grid interpolation vs an exact run | &#124;dSharpe&#124; 2.010e-08 | PASS |
| G4 committed corpus rebuilds, **U56 (required)** | max&#124;d dSharpe&#124; 2.8e-03 / 3.3e-03 / 4.1e-03, **0 win flips** | PASS |
| G5a INERTNESS IDENTITY vs an exactly-run twin | **0.000e+00** over 594 cells | PASS |
| G5b same vs the record's 0.01 interpolation grid | 6.939e-18 (g=1.00 endpoint, 1.4e5× below the 1e-12 tolerance) | PASS |
| G6 the three rules coincide on the tie-free subpopulation (5,670 cells) | 0.000e+00 | PASS |

**G4 is reported, not tolerated, on the other two panels:** B136 drifts 1.6e-02–1.8e-02 with 0/2/3
win flips (weekly `prices_broad.csv` re-cache) and SMALL drifts 2.2e-01–2.8e-01 with 18/38/77 flips —
the committed corpus is **SMALL439** against today's **SMALL663** (ideas 609 G4b, 825, 843). Those two
panels are re-priced here on today's cache and their numbers are today's, not the corpus's.

## THE CENSUS (PART A), 9 tuned points, all reported

| claim set | tie rule | cols | cells | tie share | pooled rate | vs LOSS | cols moved | max col move |
|---|---|---|---|---|---|---|---|---|
| ALL | LOSS | 46 | 315,212 | 0.0330 | 0.3654 | — | 0 | 0.0000 |
| ALL | WIN | 46 | 315,212 | 0.0330 | 0.3984 | +0.0330 | 33 | 0.5000 |
| ALL | EXCLUDED | 46 | 315,212 | 0.0330 | 0.3779 | +0.0125 | 32 | 0.5000 |
| **TWIN** | **LOSS** | **36** | **310,128** | **0.0309** | **0.3634** | — | **0** | **0.0000** |
| TWIN | WIN | 36 | 310,128 | 0.0309 | 0.3943 | +0.0309 | 30 | 0.1818 |
| TWIN | EXCLUDED | 36 | 310,128 | 0.0309 | 0.3753 | +0.0116 | 30 | 0.0584 |
| HEADLINE | LOSS | 11 | 143,910 | 0.0303 | 0.2368 | — | 0 | 0.0000 |
| HEADLINE | WIN | 11 | 143,910 | 0.0303 | 0.2670 | +0.0303 | **11 of 11** | 0.1818 |
| HEADLINE | EXCLUDED | 11 | 143,910 | 0.0303 | 0.2441 | +0.0074 | **11 of 11** | 0.0393 |

`win == (d > 1e-12)` holds exactly on **42 of 46** committed win columns, confirming LOSS is the
record's universal convention. The four exceptions are `..._price-the-EW-ALL-control-..._cloud.summary.csv`
(`win`, `win_OOS`, `mg_win`, agreement 0.50–0.61) and `..._price-the-levered-sleeve-..._C.region.csv`
(`LEV_win`, 0.906) — columns whose win flag is not the paired delta's sign at all, which is a separate
defect this run only flags.

**eps ladder (TWIN set):** tie share 0.0301 at exact 0 → 0.0309 at 1e-12 and 1e-9 → 0.0333 at 1e-6 →
0.0408 at 1e-4 → 0.0570 at 1e-3; spread 0.0301 → 0.0570. Ties are genuinely **exact**, not
near-misses: raising the tolerance nine orders of magnitude adds 0.8 pp of tie population.

**Worst two columns, both quoted:** `2026-09-10_the-stop-family-never-beats-its-own-exposure_cloud`
`.placebo.csv.win` **0.1769 → 0.3588** and `.arms.csv.win` **0.1027 → 0.2845**, each 18.18% ties —
the record's "the stop family never beats its own exposure" headline is read on a population where
one cell in five is a stop that never triggered.

## RULE 8

**(a) on the claim — SPLIT.** FULLMATCH PASSES (IS 0.0556 → OOS 0.0556, max|d| 0.0000, ρ 1.000);
**WINMATCH FAILS** (0.3056 → 0.0556, max|d| 0.6667, ρ 0.763). H6 FAIL. The tie share is not a
transferable property of a claim under the convention a reader holding one window would build.

**(b) on the books.** A twin-win selector picks, inside each (panel, rung, family, gross, depth,
cadence) cell, the highest-IS-Sharpe arm eligible under the tie rule; parameters chosen on
2009-2016 only, 2017-2026 read once. 324 cells per (matching, tie rule).

| matching | tie rule | picks moved vs LOSS | OOS CAGR | OOS Sharpe | OOS MaxDD | 4a | 4b |
|---|---|---|---|---|---|---|---|
| FULLMATCH | LOSS | — | 9.33% | 0.842 | −23.21% | 3 | 70 |
| FULLMATCH | WIN | **54 (16.7%)** | 9.32% | 0.836 | −23.87% | 3 | **68** |
| FULLMATCH | EXCLUDED | 0 | 9.33% | 0.842 | −23.21% | 3 | 70 |
| WINMATCH | LOSS | — | 9.32% | 0.836 | −23.85% | 3 | 68 |
| WINMATCH | WIN | 1 (0.3%) | 9.32% | 0.836 | −23.87% | 3 | 68 |
| WINMATCH | EXCLUDED | 0 | 9.32% | 0.836 | −23.85% | 3 | 68 |

H7 PASSES on the count and the finding is that **the count is all there is**: the tie rule moves
16.7% of FULLMATCH picks and costs those picks a mean **−0.0056** of OOS Sharpe (max |d| 0.1043) and
two 4b passes. **LOSS and EXCLUDED select identically by construction** (both require a strict IS win),
so the convention is a 3-level dial for a *rate* and a 2-level dial for a *selector*.

**Both KEEP paths over the whole rebuilt corpus (1,944 arm rows):** 4a **3 of 1,944** (all B136, all
at 0 bps, 1 also 4b); 4b **305 of 1,944** at 0 bps, **141** at 10 bps, **44** at 25 bps; SMALL **0 at
every rung**.

**Best rule-8 4b pick at 10 bps — reported, NOT claimed** (U56 `QROLL L0.17 w504 d1.00 D g1.00`):

| | CAGR | Sharpe | MaxDD | H1 / H2 | OOS CAGR | OOS Sharpe | OOS MaxDD |
|---|---|---|---|---|---|---|---|
| pick | 12.69% | 1.154 | −17.86% | 1.183 / 1.126 | **13.46%** | **1.232** | −17.86% |
| RULES v2 (live) | 8.63% | 1.202 | −12.05% | 1.235 / 1.176 | 9.47% | 1.278 | −12.05% |
| SPY | 15.16% | 0.886 | −33.72% | 0.960 / 0.826 | 15.33% | 0.877 | −33.72% |

**4a FAILS** (both halves below RULES v2, and MaxDD worse). **4b passes** full sample and OOS — but
this is a pre-existing arm of the record's own 216-arm corpus, selected here only to price the tie
dial, and it is the same breadth-QROLL cell ideas 609/824/843 have already swept. Nothing is promoted.

## PRE-REGISTERED SCORECARD — 5 of 8 PASS

| | hypothesis | verdict |
|---|---|---|
| H1 | tie share ≥ 10% of the TWIN claim set | **FAIL** (0.0309 — the premise's scale was wrong) |
| H2 | the canonical FULL/FULLMATCH win column has tie share < 1% | **FAIL** (0.0278; 0.6694 → 0.6972 under WIN) |
| H3 | a published family ordering differs between tie rules | PASS (20 of 54 cells) |
| H4 | EXCLUDED closes the FULLMATCH/WINMATCH gap below 0.05 on OOS | PASS (gap +0.0000 on FULL and OOS; **+0.2238 LOSS → +0.1455 EXCLUDED → +0.0015 WIN on IS**) |
| H5 | every WINMATCH tie is EXACT | PASS (0.000e+00) |
| H6 | IS tie share predicts OOS to within 0.10 | **FAIL** (WINMATCH 0.6667) |
| H7 | the tie rule moves ≥ 10% of selector picks | PASS (16.7%) |
| H8 | 843's 0.7778 → 0.0000 collapse rebuilds | PASS |

**H8 detail.** 843's collapse reproduces but is **narrower than 843's memo implies**: of 12
(panel, lookback) QROLL/IS legs, the exact-0.0000 WINMATCH read occurs in **1** (SMALL w2016, 100%
ties, EXCLUDED undefined), and two more (U56 w2016, B136 w2016) go 0.6667 → **0.0000** at 66.7% ties.
Every w ≤ 1008 leg has **zero** ties and is convention-invariant. **The tie artefact is entirely a
w2016 fact** — the one lookback that needs eight years of warm-up on a sample starting in 2009.
EXCLUDED agrees across conventions in 9 of 12 legs.

## PROPOSED, NOT APPLIED (rule 6 — Sunday review only)

> **PROTOCOL 4c.** Any published win rate, twin verdict or family ordering must print, beside it,
> the **TIE SHARE** of its population at the tolerance used, and must state the tie rule. Where the
> tie share exceeds 0.05, the rate must also be published with ties EXCLUDED. A tie between an arm
> and its control is the statement *"these are the same book"*, which is not a loss.

## CAVEATS

Survivorship: U56, B136 and SMALL are all current-constituent lists; every CAGR above is biased
upward, SMALL worst. B136 and SMALL are re-priced on today's caches and do not reproduce the
committed corpus (documented above). `data/prices.csv` re-download drift bounds U56 reproduction at
4.1e-03 of Sharpe. The census classifies a column as TWIN by name and as HEADLINE by whether a
sibling `.md`/`.txt` contains its rate formatted to 4 dp, 3 dp or 1 dp percent — a detector, not a
proof of citation. `RULES.md`, `PROTOCOL.md`, `research/scan.py`, `products/bot/bot.py` and
`research/baseline.py` are untouched.
