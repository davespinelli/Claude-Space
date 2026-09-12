# Idea 826 — adjudicate the THREE 2026-09-12 runs of idea 609 against each other (lane C, 2026-09-12)

**ANSWERED = THE THREE NUMBERS ARE ONE NUMBER, AND THE DISAGREEMENT IS A SCORING ARTEFACT OVER
CELLS WHERE THE GATE NEVER FIRES.** All three published headlines reproduce EXACTLY on a fourth
independent implementation (0.0847 / 0.3220 / 0.3125, all at ≤ 4.6e-05). The spread between them
is **100% the twin MATCHING CONVENTION and 0.0% the panel vintage**. Drop the (arm, window) cells
whose gate never fires inside the window — **31.25% of the census**, and the cells for which
WINMATCH makes the twin the arm itself — and the two conventions return **the identical number at
17 of 18 grid points, gap 0.0000 at the headline cell** (the 18th differs by 0.0076). The record
should quote **0.3409 (15 of 44)**, and idea 609's verdict is unchanged: the published order
QROLL > QEXP > ABS is a minority reading under every convention. **KILL for capital: 4a 0 of 648
at 10 bps; the 141 arms clearing 4b are idea 605's own committed passes reproduced, not a new
book.** No new KEEP-candidate, so no memo with RULES wording.

Script `2026-09-12_adjudicate-the-THREE-2026-09-12-runs-of-idea-609-against-each-other_C.py`.
No RULES change, no book promoted, no PROTOCOL edit applied (rule 6); RULES.md, PROTOCOL.md,
scan.py, bot.py and baseline.py untouched.

## 0. Gates — 6 of 6 pass, including all three disputed headlines

| gate | what | result |
|---|---|---|
| G1 | derived gate ladder `r(c) = m·r0 − (c/1e4)(m·t0 + g·\|dm\|)` vs live `engine.backtest` through idea 399's `apply_gate` | max \|d\| **1.041e-17** — PASS (bar 1e-12) |
| G2 | fast CAGR/Sharpe/MaxDD vs `engine.metrics` | **0.000e+00** — PASS |
| G3 | 0.01 twin-gross grid + quadratic-in-λ window variance vs an EXACT twin run at g = 0.6237 | \|dSharpe\| **2.010e-08** — PASS (bar 1e-6) |
| G4 | idea 84's ungated EWALL U56 g=0.85 @ 10 bps | **11.75% / 1.046 / −17.89%** vs published 11.8% / 1.05 / −17.9% — PASS |
| G5 | O(1) cumsum window Sharpe (gate **and** twin) vs direct numpy, 400 slices | max \|d\| **2.287e-14** — PASS (bar 1e-9) |

**GR1–GR3 — the three numbers under adjudication, rebuilt inside one code path:**

| gate | source | convention | vintage | W / step | published | this run | n | \|diff\| | |
|---|---|---|---|---|---|---|---|---|---|
| GR1 | aa87884 (lane B) | WINMATCH | ASOF | 756 / 63 | 0.0847 | **0.0847** | 59 | 4.58e-05 | PASS |
| GR2 | 2c96cad (cloud) + `_B2` | FULLMATCH | TODAY | 756 / 63 | 0.3220 | **0.3220** | 59 | 3.39e-05 | PASS |
| GR3 | `_B2` dense census | FULLMATCH | TODAY | 756 / 21 | 0.3125 | **0.3125** | 176 | 0.00e+00 | PASS |

The ASOF corpus is rebuilt independently from lane B's: `prices.csv` / `prices_broad.csv`
truncated to idea 605's last dates and `prices_small.csv.gz` + `small_meta.csv` restored from git
blob `e02949d`. It returns **U56 4441 eval days, B136 4439, SMALL 439 tradable names** — idea
605's panel shapes exactly. Lane B's other two 2×2 cells (ASOF/FULL 0.3390, TODAY/WINDOW 0.1017)
also reproduce to the digit, so this run agrees with all four of its cells and with both of the
other runs. **Nothing in the record's three numbers is an implementation difference.**

## 1. The 2×2, and what actually moves it

Headline cell: 756d window, step 63, 10 bps, POOLED over three panels, ALL cells.

| vintage | convention | n | exact | QR>QE | QE>AB | QR>AB | mean ρ |
|---|---|---|---|---|---|---|---|
| ASOF | FULLMATCH | 59 | 0.3390 | 0.7288 | 0.6102 | 0.8814 | +0.5655 |
| ASOF | **WINMATCH** | 59 | **0.0847** | 1.0000 | 0.0847 | 0.7458 | +0.3462 |
| TODAY | **FULLMATCH** | 59 | **0.3220** | 0.6949 | 0.6271 | 0.9492 | +0.6271 |
| TODAY | WINMATCH | 59 | 0.1017 | 1.0000 | 0.1017 | 0.8305 | +0.4479 |

**Decomposition of the disputed spread 0.0847 → 0.3220 (+0.2373):**

| leg | value | share of spread |
|---|---|---|
| **CONVENTION** (WINMATCH → FULLMATCH, mean over vintages) | **+0.2373** | **100.0%** |
| VINTAGE (ASOF → TODAY, mean over conventions) | +0.0000 | 0.0% |
| interaction | −0.0339 | — |

The vintage leg is exactly zero because the 439→663 small-panel rewrite moves the census
**+0.0169 under WINMATCH and −0.0169 under FULLMATCH**. The queue's premise — "the spread is the
twin MATCHING SAMPLE" — is confirmed, and the panel drift that wrecked idea 609's G4b does not
touch this verdict.

**All 9 (window, step) points × both conventions, POOLED, 10 bps, nothing selected on:**

| vintage | W | FULL/21 | WIN/21 | FULL/63 | WIN/63 | FULL/126 | WIN/126 |
|---|---|---|---|---|---|---|---|
| ASOF | 504 | 0.2819 | 0.0585 | 0.2857 | 0.0635 | 0.2500 | 0.0312 |
| ASOF | **756** | 0.3409 | 0.0909 | **0.3390** | **0.0847** | 0.2667 | 0.0333 |
| ASOF | 1008 | 0.2927 | 0.1280 | 0.3455 | 0.1091 | 0.3571 | 0.0714 |
| TODAY | 504 | 0.2340 | 0.0585 | 0.2381 | 0.0635 | 0.1875 | 0.0312 |
| TODAY | **756** | **0.3125** | 0.0909 | **0.3220** | 0.1017 | 0.3000 | 0.0667 |
| TODAY | 1008 | 0.2805 | 0.1037 | 0.2727 | 0.0727 | 0.2857 | 0.0357 |

n windows: 504 → 188/63/32, 756 → 176/59/30, 1008 → 164/55/28. Cost ladder (756/63, POOLED):
ASOF FULL 0.3220 / 0.3390 / 0.3220 and WIN 0.0678 / 0.0847 / 0.1356 at 0 / 10 / 25 bps; TODAY
FULL 0.2712 / 0.3220 / 0.3051 and WIN 0.0508 / 0.1017 / 0.1186. Per scope at the headline cell
(TODAY): B136 **0.2542 / 0.0000**, U56 0.2542 / 0.1186, SMALL 0.2642 / 0.2264, POOLED_REPRO
0.2373 / 0.1017 (FULL / WIN).

## 2. The deciding test — the convention gap is entirely never-firing cells

Idea 824 (7df829b) found 714 of 717 verdict flips between the conventions are arms whose gate
never fires in the window: WINMATCH then sets `g_eff` to the arm's own gross, so **the twin IS the
arm**, `dSharpe` is identically 0, and `win = dSharpe > 1e-12` scores it a **LOSS**; FULLMATCH
holds the twin at a different gross and returns a win by ≤ 1.31e-03. That diagnosis had never been
applied to the rolling census. It is decisive here.

**Cell counts at the headline cell (TODAY, POOLED, 756/63/10 bps):**

| family | ALL cells | FIRE cells | never fires | share never |
|---|---|---|---|---|
| QROLL | 24,624 | 17,856 | 6,768 | 0.2749 |
| **QEXP** | 6,156 | 2,784 | 3,372 | **0.5478** |
| ABS | 6,156 | 4,752 | 1,404 | 0.2281 |
| **TOTAL** | 36,936 | 25,392 | 11,544 | **0.3125** |

QEXP's expanding-quantile threshold is silent in **more than half** of its (arm, window) cells.
That is the whole mechanism: under WINMATCH every one of those silent cells is booked a loss, so
QEXP's window win rate collapses (0.2385) and `QEXP > ABS` falls to 0.0847 — the exact leg lane B
reported as broken.

**The same census on FIRE-only cells:**

| vintage | conv | pop | n | exact | QR>QE | QE>AB | QR>AB |
|---|---|---|---|---|---|---|---|
| TODAY | FULLMATCH | ALL | 59 | 0.3220 | 0.6949 | 0.6271 | 0.9492 |
| TODAY | WINMATCH | ALL | 59 | 0.1017 | 1.0000 | 0.1017 | 0.8305 |
| TODAY | FULLMATCH | **FIRE** | 44 | **0.3409** | **0.9545** | 0.3864 | 0.9091 |
| TODAY | WINMATCH | **FIRE** | 44 | **0.3409** | **0.9545** | 0.3864 | 0.9091 |
| ASOF | FULLMATCH | FIRE | 44 | 0.3864 | 0.9545 | 0.4318 | 0.9091 |
| ASOF | WINMATCH | FIRE | 44 | 0.3864 | 0.9545 | 0.4318 | 0.9091 |

**Convention gap at the headline cell: ALL cells 0.2203 → FIRE-only 0.0000.** Over all 18
(vintage × window × step) points at 10 bps the two conventions return an **identical exact-match
share at 17**, and the 18th (ASOF 756/21) differs by **0.0076**. The FIRE-only share spans
**0.2500–0.3864** across those 18 points — a band that contains both 0.3220 and 0.3390 and
excludes 0.0847 entirely.

On firing cells the underlying family win rates still differ slightly between conventions (TODAY:
QROLL 0.6917 both, QEXP 0.4639 vs 0.4618, ABS 0.5103 both) — the twin is genuinely a different
object there — but never by enough to reorder the families in any window. That is the sense in
which the number is convention-free. Contrast the ALL-cell rates, where WINMATCH cuts QEXP from
**0.5403 to 0.2332** while barely touching ABS (0.4427 → 0.4228): the whole gap is booked losses
on silence. Lane B's committed 0.2385 for QEXP (ASOF, WINMATCH) reproduces here exactly.

## 3. Rule 8

**(a) On the claim.** Windows ending ≤ 2016-12-31 are IS; windows starting ≥ 2017-01-01 are read
once. At the headline grid point: IS exact **0.0000** (WINMATCH, both vintages) and **0.1500**
(TODAY FULLMATCH) against OOS **0.1852** and **0.3333**; on FIRE-only cells IS **0.0000** (5
windows) against OOS **0.4074**. Worst \|OOS − IS\| over all 9 grid points × 3 rungs: WINMATCH
mean 0.099 / max 0.259, FULLMATCH mean 0.194 / max 0.417, FIRE-only mean 0.26–0.35 / max 0.52.
**H_WF FAILS under every convention**, in the same direction lane B found: *the published ordering
is not a reading a pre-2017 reader could have had at all.* The IS leg rests on 20 windows (5 on
FIRE-only), which is itself a caveat — a 3-year window barely closes inside 2009–2016.

**(b) On a book.** The IS rolling census picks the family, IS Sharpe picks the arm inside it,
2017–2026 is read once. 108 picks (2 vintages × 2 conventions × 9 grid points × 3 panels) at
10 bps:

| vintage | conv | n | names OOS-leading family | mean OOS Sharpe | mean OOS CAGR | mean OOS MaxDD | beats RULES v2 | beats SPY | 4b OOS |
|---|---|---|---|---|---|---|---|---|---|
| ASOF | FULLMATCH | 27 | 0.2963 | 0.8308 | 10.48% | −25.75% | 0.2963 | 0.6667 | 0.2963 |
| ASOF | WINMATCH | 27 | 0.6296 | 0.8299 | 9.23% | −22.22% | 0.3333 | 0.6667 | 0.6296 |
| TODAY | FULLMATCH | 27 | 0.2963 | 0.8369 | 10.67% | −28.61% | 0.2963 | 0.6667 | 0.2963 |
| TODAY | WINMATCH | 27 | 0.6667 | **0.8959** | 10.09% | −20.23% | 0.3333 | 0.6667 | 0.6296 |

Comparands, OOS 2017–2026 at 10 bps: RULES v2 **1.2782** (U56) / 1.1059 (B136) / 0.5600 (SMALL);
RULES v1 0.7361 / 0.5702 / 0.7059; SPY **0.8767 / 15.33% / −33.72%**. **H_BOOK FAILS** — the
selector beats the live book in 34 of 108 picks and SPY in 72 of 108, and its mean OOS Sharpe
(0.83–0.90) sits below RULES v2 on both large panels. Lane B's 9/27 and 17/27 reproduce as
0.3333 and 0.6296 on the same (ASOF, WINMATCH) cell.

## 4. KEEP paths — all 648 arms × 3 rungs, per vintage

| corpus | rung | 4a | 4b |
|---|---|---|---|
| ASOF | 0 bps | **3** (B136) | 306 (B136 144, U56 162, SMALL 0) |
| ASOF | **10 bps** | **0 of 648** | **142** (B136 76, U56 66, SMALL 0) |
| ASOF | 25 bps | 0 | 45 |
| TODAY | 0 bps | 3 (B136) | 305 |
| TODAY | **10 bps** | **0 of 648** | **141** (B136 74, U56 67, SMALL 0) |
| TODAY | 25 bps | 0 | 44 |

The ASOF 142 and TODAY 141 are idea 605's committed **141** reproduced (lane B got the same
142/141 split). **No new book.** 4b failure legs at 10 bps (TODAY): the full set ×210, CAGR ×188,
none ×141, DD ×91, H1+CAGR ×6, H1,H2,OOS,CAGR ×6, H1+DD ×3, H1 ×3.

The record's standing 4b candidate (B136 QROLL q0.17 w252 depth 0.50 daily g=1.00) is re-read for
continuity, **not proposed**: 0 bps 14.82% / 1.2494 / −15.06%; **10 bps 13.29% / 1.1336 /
−15.19%, OOS 13.33% / 1.1897 / −15.19%**; 25 bps 11.03% / 0.9593 / −16.33%. 4b True and 4a False
at all three rungs — the record's published triple to the digit. (Lane B's idea 829 killed its
entry-date leg today; nothing here changes that.)

## 5. Pre-registered hypotheses — 8 of 11 pass

| | | |
|---|---|---|
| GR1 | lane B 0.0847 reproduces (≤ 1e-4) | **PASS** — 4.58e-05 |
| GR2 | cloud/`_B2` 0.3220 reproduces | **PASS** — 3.39e-05 |
| GR3 | `_B2` step-21 0.3125 reproduces | **PASS** — 0.00e+00 |
| H_CONV | convention leg ≥ 0.15 on both vintages | **PASS** — ASOF +0.2542, TODAY +0.2203 |
| H_VINT | vintage leg ≤ 0.05 on both conventions | **PASS** — WINMATCH +0.0169, FULLMATCH −0.0169 |
| H_STEP | step span ≤ 0.10 at fixed (window, conv) | **PASS** — worst 0.0742 |
| **H_FIRE** | **conventions agree within 0.05 on FIRE-only cells** | **PASS — gap 0.0000** (ALL-cells gap 0.2203) |
| H_DEGEN | never-firing cells ≥ 0.20 of the census | **PASS** — 0.3125 |
| H_ONE | QROLL > QEXP ≥ 0.90 under both conventions | **FAIL** — min 0.6949 (FULLMATCH, ALL cells). On FIRE-only it is **0.9545 under both** |
| H_WF | \|OOS − IS\| exact share ≤ 0.10 | **FAIL** — worst 0.1852 (ALL), 0.4815 (FIRE) |
| H_BOOK | IS book beats RULES v2 AND SPY on OOS Sharpe | **FAIL** — 0.3148 and 0.6667 |

## 6. What the record should do

1. **Quote one number, and quote the FIRE-only one: `0.3409` (15 of 44 rolling 3-year windows,
   TODAY, 756/63, 10 bps, POOLED).** It is convention-free — FULLMATCH and WINMATCH return it to
   the digit, and to the digit at 17 of the 18 grid points — so it is the only one of the four
   published cells that does not need a convention footnote. The two ALL-cell numbers (0.3220 and
   0.1017/0.0847) should be retained as the convention-dependent readings they are, never as
   rival answers.
2. **Retire "QROLL > QEXP holds 59 of 59 (1.0000)".** That 1.0000 is itself the WINMATCH
   degeneracy: 27.5% of QROLL's cells and 54.8% of QEXP's never fire, and booking every silent
   cell a loss is what makes the leg look perfect. The defensible statement is **QROLL > QEXP in
   42 of 44 firing windows (0.9545), under both conventions** — still the most invariant leg on
   the record, but not exact.
3. **A twin claim must publish its FIRING POPULATION, not just its matching convention.** Idea
   609's recommendation ("a twin claim needs its matching convention stated") is necessary and
   not sufficient: once never-firing cells are excluded the convention stops mattering at all.
   Proposed PROTOCOL line, for a Sunday review (rule 6 — **not applied here**): *any win-rate or
   ordering statistic over gated arms must report the share of (arm, window) cells whose gate
   never fires, and the statistic restricted to firing cells.*
4. **Idea 609's verdict is unchanged and now un-appealable.** Under every convention, every
   vintage, all 9 grid points and all 3 cost rungs, the published order QROLL > QEXP > ABS is a
   **minority** reading — 0.25–0.39 on firing cells, 0.03–0.35 on all cells. The three committed
   runs were never in conflict about that.

_Survivorship: all three panels are current-constituent lists, so CAGR and drawdown LEVELS are
optimistic — SMALL worst. Every statistic above is either a within-panel contrast between arms
sharing a panel or a count of orderings, neither of which the bias moves._

Outputs: `_C.txt` (console), `_C.census.csv.gz` (every window × scope × convention × rung × pop),
`_C.grid.csv`, `_C.walkforward.csv`, `_C.picks.csv`, `_C.arms.csv.gz`.
