# idea 194 — abstention-is-the-only-thing-that-ever-helps (cloud, 2026-09-05)

**ANSWERED, and idea 194's literal hypothesis is HALF RIGHT IN THE STRONGEST POSSIBLE WAY.
Abstention is EXACTLY a dilution toward doing nothing — never a source of gain. As a KEEP path
or a rule-8 arm every gate is a KILL. RULES untouched; no new book.**

Script `2026-09-05_abstention-is-the-only-thing-that-ever-helps_cloud.py`; outputs
`.console.txt`, `.cells.csv`, `.gates.csv` (= `.walkforward.csv`), `.record.csv`.

## Corpus and reproduction (2 of 2 exact)

3 panels x 7 keys x 9 shares x 2 cost rungs = **378 books**, weekly, t+1, gross 0.75 `norm`
(ideas 153/159/165/177), rebuilt by importing idea 177's `build_panels()`/`build_base()`.
CELL = (panel, cost, share) → **54 cells**; MENU = the 7 keys; CONTROL = `NONE` (the composite
with no cross-sectional tilt, i.e. "apply no key"); CANDIDATES = the other 6 including idea
159's `RND` scramble.

* **[b] corpus vs idea 165's published `.grid.csv`:** n 0.0, CAGR 9.71e-17, Sharpe 2.22e-16,
  MaxDD 8.33e-17, H1/H2 2.22e-16, OOS_Sharpe 2.22e-16 — **all MATCH**.
* **[c] the ABSTAIN-ALWAYS identity:** max |OOS Sharpe(A∞) − OOS Sharpe(S0)| over 54 cells =
  **0.000e+00**. A pure abstain-always arm is not an approximation of do-nothing, it **is**
  do-nothing, and its gain is 0.0000 by construction.

## The first answer is arithmetic, and it is exact

Because a gate that admits nothing holds the control, and S0 **is** the control, the paired
difference on an abstained cell is identically zero. So

    gain(G) = a·0 + (1 − a)·c        a = abstention rate, c = mean choice effect on picked cells

**[d] the identity holds to 3.47e-18 across all 25 gates.** Abstention therefore contributes
**nothing directly** and acts **only** as a dilution factor (1 − a) on whatever the selector
does. "How much of the gate's gain is explained by its abstention rate alone" has the answer
*none of it, and all of it* — none as a source, all as a scaling.

## Is the abstention CHOICE skilful? (matched-rate random-abstention null, 2000 draws)

**P3 MISS — and the misses are the result.** 5 of 19 testable gates escape their null:

| gate | a | gain | null 95% band | side | p | ungated c₀ |
|---|---|---|---|---|---|---|
| IS_MAXDD τ=0.00 | 0.574 | −0.0219 | [−0.0724, −0.0353] | **above** | 0.000 | −0.1258 |
| IS_MAXDD τ=0.05 | 0.704 | −0.0152 | [−0.0545, −0.0210] | **above** | 0.008 | −0.1258 |
| IS_MAXDD τ=0.10 | 0.796 | −0.0087 | [−0.0413, −0.0116] | **above** | 0.017 | −0.1258 |
| IS_SHARPE τ=0.20 | 0.796 | −0.0104 | [−0.0084, +0.0116] | **below** | 0.020 | +0.0099 |
| IS_CAGR τ=0.20 | 0.796 | −0.0119 | [−0.0078, +0.0133] | **below** | 0.005 | +0.0145 |

The abstention choice carries information in exactly one direction: **it is skilful only where
the selector is broken** (IS_MAXDD, the worst selector in the run, is clawed from −0.1258 to
−0.0087 — and never above zero), and where the selector is decent (IS_SHARPE, IS_CAGR) the
same threshold abstains **below** its own random-abstention null, i.e. it declines in the very
cells the selector would have won. A gate never manufactures a gain; at best it undoes its own
selector's damage, asymptotically approaching do-nothing from below.

## Abstention is pure dilution — 5 of 5

Per selector, `gain ~ a`: **sign(slope) = −sign(c₀) in 5 of 5 selectors.**

| selector | c₀ (ungated) | slope of gain in a | R² | best gain | at a |
|---|---|---|---|---|---|
| IS_SHARPE | +0.0099 | −0.0191 | 0.599 | +0.0099 | 0.000 |
| IS_CALMAR | −0.0126 | +0.0050 | 0.053 | +0.0050 | 0.611 |
| IS_MAXDD | −0.1258 | **+0.1450** | **0.961** | −0.0087 | 0.796 |
| IS_CAGR | +0.0145 | −0.0277 | 0.810 | +0.0145 | 0.000 |
| IS_4B | −0.0033 | +0.0005 | 0.002 | +0.0036 | 0.667 |

**P4 MISS as stated:** pooled across the 25 gates, R² of gain on the abstention rate is
**0.002** — the rate alone explains nothing, because c is not constant across selectors. The
correct statement is the identity: abstention moves every gate toward zero at rate (1 − a), and
whether that reads as "help" depends only on the sign of c₀.

## Rule 8 (everything fitted ≤ 2016-12-31, 2017–2026 read once) — the ninth do-nothing win

* **S0 do-nothing: mean OOS Sharpe 0.7195, 10.31% CAGR, −25.71% MaxDD; OOS 4a 17/54, 4b 12/54.**
* Best of all 27 arms: IS_CAGR ungated **0.7340** (+0.0145, **t +1.09**, 33W/21L) — insignificant.
* Worst: IS_MAXDD ungated 0.5937 (−0.1258, t −6.67, 9W/45L). RANDOM 0.6812 (−0.0383, t −1.91).
* **No arm beats S0 at t > 2 (P5 HIT).** Every one of the 25 gates lies in
  [−0.0219, +0.0145] of S0.
* OOS 4b passes: S0 12/54, best arm 15/54 (P6 HIT). **No book is promoted.**

Benchmarks over the same window — SPY OOS 15.45%/0.8820/−33.72%; RULES v1 OOS @10bps u56
7.73%/0.7471/−13.83%, broad 5.94%/0.5763/−21.19%, small 7.92%/0.5807/−32.84% (@25bps 3.78%/
0.3992, 1.11%/0.1554, 2.67%/0.2501).

## The record back-fill (best-effort, reported as corroboration only)

74 `*.walkforward.csv` scanned; **18 carried a recoverable schema**; **74 published selector
arms** recovered. Abstention rate mean 0.364; 50 of 74 abstain at all, 3 abstain always. OOS
gain vs the file's own control: mean +0.0349 but **median −0.0294, only 24 of 74 positive**.
Among the 50 abstaining arms, `gain = +0.0669 − 0.0451·a`, **R² 0.005** — the same null result
as the fresh experiment. That 56 of 74 files carry no abstention signal at all is itself the
argument for recording it.

## Verdict — KILL (of every gate), and a PROTOCOL clause, not a backtest

Idea 194 asked whether "do not select" is a clause rather than a result. It is: the
abstain-always arm is provably identical to do-nothing, the decomposition is an identity, and
across 25 gates x 54 cells no gate ever produces a positive gain that survives its own
matched-rate null. Proposed rule-8 wording (report-only, **RULES.md untouched**):

> **8b.** A rule-8 arm that declines to pick holds the cell's control book, so an
> abstain-always arm is identically the do-nothing control. Report every gate's ABSTENTION
> RATE `a` beside its OOS gain, and read the gain as `(1 − a)·c`: abstention is a dilution
> toward the control, never a source of edge. A gate may only be claimed to add value if it
> beats a MATCHED-RATE RANDOM-ABSTENTION null at the same `a`.

## Caveats carried

Survivorship: all three panels are current constituents; the small panel is the sub-$2B screen
with the 44 `max_1d_move ≥ 1.0` tickers dropped and a joined, never-selectable SPY — every CAGR
here is optimistic and no level is achievable. The 54 cells share three price panels and are
not independent, so every t-stat is optimistic; the permutation null is the inference this run
leans on. Idea 128: the IS window's SPY drawdown is shallower than the OOS window's, which
works specifically against IS_MAXDD and IS_4B. The record back-fill reads ~70 scripts under no
common schema and is a lower bound, not a census. t+1 execution only (idea 126).
