# Idea 926 — does the zero-cost pass↔base-rate inversion hold on MONTHLY 4b passes? (lane B)

**ANSWERED = YES, IT HOLDS, AND AT PROTOCOL'S OWN COST RUNG.** The queue's premise is
**CONFIRMED**, and the consequence is a **KILL for idea 680's generalisation**: 680's
"PROTOCOL rule 2's 10 bps already does the entire job a base-rate clause would do" is a
**WEEKLY-ONLY fact**. Re-running 680's own 30 cells on a monthly rebalance grid,
ρ(4b pass, null base rate) at 10 bps reads **+0.4470** against weekly's **−0.0728**, the
inversion's zero crossing moves from **9.33 bps to 47.76 bps (5.12×)**, and the single
strongest book in the whole run — `U56/M/CORE/TOP20`, which clears every 4b leg on the FULL
sample **and** on the rule-8 OOS window at 10 bps — sits inside a **40.5%** coin-flip base
rate. Nothing promoted, no RULES change, no PROTOCOL edit applied (rule 6). `RULES.md`,
`PROTOCOL.md`, `scan.py`, `bot.py`, `baseline.py` untouched. **Gates 9 of 9.**

SELECTION: the LAST Open idea carrying a price leg. 904 (the last line) is a census of
committed placebo numbers against a seed-count floor — no book to price — and carries a
standing SKIP note; a SKIP note was appended and 926 claimed.

Script: `2026-09-15_does-the-ZERO-COST-pass-to-BASE-RATE-inversion-hold-on-MONTHLY-4b-passes_B.py`
(1,171 s, seed base 926, 400 draws). Artifacts: `.books.csv` (540), `.nulls.csv` (1,620),
`.draws.csv` (36,000), `.rho.csv` (18), `.walkforward.csv` (180), `.console.txt`.

---

## WHAT WAS RE-RUN

Idea 680's 30 cells, construction unchanged: 3 panels (U56 / B136 / SMALL439) × 2 claim sets
(CORE gross 0.75, EXT gross 1.00) × 5 books (TOP5, TOP10, TOP20, EWELIG, BAND03), each against
its own **gross-matched rotating coin-flip null** — same name count, same per-name weight, same
pool, selection replaced by a draw. **G5 gross match = 0.0000 on all 90 (cadence × cell)
families**, exact rather than approximate. The only thing that changes is the rebalance grid.

**TUNED (2):** cadence (W / M / Q) and cost rung (0 / 2 / 5 / 10 / 25 / 50 bps). All 18 grid
points published below. Draws fixed at 400 (nested 100/200/400 convergence printed, never
chosen). W is the reproduction arm, not a free choice.

**The queue's own premise is 35% off and is reported as measured, not assumed.** G9: mean book
turnover W → M → Q reads **11.93× → 5.36× → 2.88×** (U56), 14.65 → 6.68 → 3.48 (B136),
21.66 → 9.78 → 4.29 (SMALL439). Monthly is **2.2× slower than weekly, not "a third as fast"**
(3×), uniformly across all three panels.

## THE ANSWER — ρ(4b pass, null base rate) at every cadence × rung (30 cells each, 400 draws)

| cadence | 0 bps | 2 bps | 5 bps | **10 bps** | 25 bps | 50 bps |
|---|---|---|---|---|---|---|
| **W** (680's grid) | **+0.5596** | +0.5634 | +0.4722 | **−0.0728** | n/a¹ | n/a¹ |
| **M** (the object) | +0.3903 | +0.3974 | +0.4187 | **+0.4470** | **+0.5043** | −0.0496 |
| **Q** | n/a¹ | n/a¹ | n/a¹ | n/a¹ | n/a¹ | n/a¹ |

¹ ρ is undefined where the pass indicator has no variance: W has 2 of 30 passers at 25 bps and
0 at 50; **Q has 0 of 30 4b passes at every rung**, so the cadence ladder *terminates* rather
than extrapolating. Stated rather than interpolated — Q is not evidence for a monotone cadence
law, it is the point where the bar stops being clearable at all.

**The monthly inversion does not merely survive the cost rung — it STRENGTHENS through it**,
rising monotonically +0.3903 → +0.4470 → +0.5043 from 0 to 25 bps before collapsing at 50.
Weekly's dies between 5 and 10 bps.

### The same fact in the currency that matters for a reader of a 4b row

Cells whose gross-matched coin flip clears 4b more than 1 time in 20, **at PROTOCOL's own
10 bps**:

| cadence | cells with base rate > 0.05 | max base rate | mean base rate |
|---|---|---|---|
| **W** | **0 of 30** | 0.8% | 0.0003 |
| **M** | **4 of 30** | **40.5%** | 0.0343 |
| **Q** | 4 of 30 | 13.5% | 0.0126 |

680's all-clear is exactly right on the panel it was measured on and **wrong by two orders of
magnitude in the mean on the one next door.**

## THE CAPITAL-RELEVANT CELL

Of the 7 cells clearing 4b on the full sample at 10 bps, 5 also clear every 4b leg on the
rule-8 OOS window. The best of them is the one this run exists to warn about:

| cell | full sample | rule-8 OOS window | OOS 4b | null base rate @10 bps |
|---|---|---|---|---|
| **U56 `M/CORE/TOP20`** | **14.69% / 1.203 / −19.51%** (halves 1.216/1.198) | **16.67% / 1.283 / −19.51%** | **PASS** | **40.5%** |
| U56 `M/CORE/EWELIG` | 11.79% / 1.139 / −17.01% | 12.98% / 1.216 / −17.01% | PASS | 6.0% |
| U56 `M/EXT/BAND03` | 11.90% / 1.174 / −18.81% | 12.82% / 1.225 / −18.81% | PASS | **2.8%** ✔ |
| U56 `W/CORE/TOP20` (the standing candidate) | 12.60% / 1.088 / −18.31% | 14.24% / 1.161 / −18.31% | PASS | 0.0% ✔ |
| U56 `W/EXT/BAND03` | 11.54% / 1.201 / −15.91% | 12.68% / 1.277 / −15.91% | PASS | 0.0% ✔ |

Comparands, same tapes: **SPY full 15.13% / 0.885 / −33.72%, OOS 15.27% / 0.874 / −33.72%**;
**RULES v2 (live, weekly) full 8.62% / 1.201 / −12.05%, OOS 9.46% / 1.277 / −12.05%** (U56).

`U56/M/CORE/TOP20` is the highest-CAGR, highest-Sharpe, both-windows-4b-clearing book in the
run, and **2 of every 5 gross-matched coin flips from its own candidate set clear the identical
bar at the identical cost**. Its weekly twin — the same book, the same gross, the same gate,
rebalanced weekly — has a base rate of **0.0%**. Nothing about the *rule* changed; only how
often it trades. **It is PARKed, disqualified by this run's own headline, not promoted.**

## MECHANISM — it is NOT (only) a turnover fact: H_DRAG FAILS

Pre-registered: if the inversion is a realised-cost-**drag** fact (cost_bps × turnover/yr), the
cadences' zero crossings should agree in drag. They do not, and the gap is reported both ways:

| | W | M | ratio |
|---|---|---|---|
| ρ zero crossing in **COST** | 9.33 bps | 47.76 bps | **5.12×** |
| ρ zero crossing in **DRAG** | 150.1 bps/yr | 347.4 bps/yr | **2.31×** |

Re-expressing the rung as drag **shrinks the cadence gap by 48.6% of its log spread and leaves
2.3× standing**, against a pre-registered 2.0× bar. **H_DRAG FAIL.** Turnover is about half the
story; the rest is that a slower null is a *different* null — it holds each random name for a
month, so its return stream is less diversified across draws and its upper tail reaches further.
Idea 925's RANDROT/RANDFIX question is the same axis seen from the other end, and this run says
its answer will not be "turnover alone" either.

**H_SURVIVE PASS** as pre-registered: ρ_M(10 bps) = +0.4470 > 0 and > ρ_W(10 bps) = −0.0728.

## RULE 8 — walk-forward, parameters chosen on 2009–2016 only, 2017–2026 read once

4 IS-only choosers × 3 panels × 4 cadence scopes × 6 rungs = 180 cells, **158 live picks (22 IS
sets EMPTY)**. Totals: **4b 15 of 158, 4a 0 of 158.**

| chooser | OOS 4b | mean OOS Sharpe | mean OOS CAGR |
|---|---|---|---|
| CH_SHARPE (best IS Sharpe, no clause) | 6 / 54 | 0.781 | 12.63% |
| CH_4bIS (best IS Sharpe among IS 4b-level passers) | 4 / 32 | 0.993 | 12.05% |
| CH_BASE (IS base rate ≤ 0.05, then best IS Sharpe) | 5 / 54 | 0.777 | 12.55% |
| **CH_ANYCAD (cadence itself chosen in sample)** | **0 / 18** | **0.671** | 13.75% |

**Two results that cut against this run's own direction and are reported anyway.**

1. **CH_ANYCAD is 0 for 18.** Letting the *cadence* be chosen in sample picks `Q/EXT/TOP5` on
   U56 and B136 at 5 of 6 rungs (IS Sharpe 1.30 / 1.43) and delivers OOS **11.94% / 0.550 /
   −38.48%** and **23.23% / 0.853 / −36.61%** — 4b fail on the drawdown cap both times. The
   monthly books that look best in *this* run's full-sample table are **not** what an honest
   in-sample cadence chooser reaches for. No monthly book is promotable on rule 8 here.
2. **The base-rate clause is still nearly inert as a chooser, even at monthly.** On U56/M at
   10 bps CH_BASE and CH_SHARPE pick identically (`M/EXT/TOP5`, IS base rate 0.0%). It differs
   at 10 bps only on SMALL439/M, where it steers `M/EXT/BAND03` → `M/CORE/BAND03`: OOS CAGR
   5.43% → 4.12% (**−1.31 pp**) for 5.15 pp less drawdown, both 4b fail. So 680's *second*
   conclusion — that the clause is not worth adopting as a **chooser** — survives this run
   intact. What does **not** survive is its first: that 10 bps makes the base rate
   **unnecessary to report**.

Best OOS cells among live picks: U56 `W/EXT/BAND03` at 0–5 bps (OOS **12.95% / 1.301 /
−15.88%**, 4b PASS, 4a fail) — an already-published weekly book, unchanged by this run.
**4a is 0 of 158**: nothing beats the live book's drawdown, which is why PROTOCOL 4b exists.

## GATES — 9 of 9 PASS

`G1` ctx.run ≡ `engine.backtest` @10 bps on **every** cadence, worst **2.082e-17** ·
`G2` band_book(0.03, 0.75) ≡ `rules_v2_weights` **0.000e+00** ·
**`G3` idea 680 REPRODUCTION from this file's code path**: weekly 4b pass counts
**{0 bps: 7, 10: 4, 25: 2}** vs published {7, 4, 2}, **exact**; ρ@0 bps **+0.5596** vs
published +0.6387 (|Δ| 0.0791, bar 0.10 — 400 draws here vs 680's 1,000); ρ@10 bps **−0.0728**
vs −0.1048 (|Δ| 0.0320); mean base rate @0 bps **0.1975** vs 0.1953 (|Δ| 0.0022) ·
`G3b` the 2026-09-04 KEEP-4b incumbent: **12.60% / 1.0881 / −18.31%** vs published
12.66% / 1.0921 / −18.31%, max|Δ| **3.958e-03** · `G4` panel triples printed for all 3 panels ×
3 cadences, both windows · `G5` gross match **0.0000** worst over 90 families ·
`G6` determinism **0.000e+00** · `G7` SMALL439 screen: 52 tickers with `max_1d_move ≥ 1.0`
dropped (**663 names + SPY** — the `439` label remains vintage, as 680 noted) ·
`G8` nesting: the 100/200 base rates are exact prefixes of the same 400 draw streams ·
`G9` turnover strictly decreasing W > M > Q on every panel.

**Honest limits.** ρ@0 bps reproduces 680 to 0.079, not to the third decimal, because 400 draws
carry sampling noise that 1,000 does not; the direction, the pass counts and the mean base rate
all reproduce, and every headline contrast in this run is *within* the 400-draw grid, so the
noise is common to both sides of it. Q's ρ is undefined at all six rungs, so the cadence axis
has **two usable points, not three** — the 5.12× / 2.31× crossing ratios are a W-vs-M contrast
and are labelled as such, not as a fitted law.

## SURVIVORSHIP (PROTOCOL 9)

`universe.json`, `universe_broad.json` and the SMALL screen are current-constituent lists, so
every CAGR and drawdown LEVEL above is optimistic. The direction is the same one 680 stated and
again works against the incumbents: a coin flip drawn from a survivor panel is a **better** book
than one drawn in real time, so **every null base rate above is an UPPER bound** and every
book's percentile inside its null a **lower** bound — including the 40.5%. The 4b bar is against
SPY, which is not survivorship-inflated, so the 4b LEVELS are not protected by the usual
same-tape argument; the ρ curves, the cadence contrasts and the base rates are all same-tape
comparisons and are unaffected.

## WHAT THIS MEANS FOR CAPITAL

Nothing changes in the live book (weekly, and 680's all-clear covers it exactly). The
operational consequence is narrow and is **proposed, not applied** (rule 6): **a 4b row quoted
for a book that rebalances slower than weekly is not evidence about a rule unless its own null's
base rate is quoted beside it**, because 10 bps stops protecting the bar somewhere between the
weekly and monthly grids — nearer 48 bps than 10. The record's monthly-cadence 4b block
(`BAND03_M`, the `CAND` ladders at `freq='M'`, idea 919's line) is inside that gap.

Follow-ups filed: 930 (does the base rate depend on HOLD LENGTH separately from turnover — split
the cadence axis into rebalance frequency and per-name holding period, the residual H_DRAG could
not explain), 931 (re-score the record's committed `freq='M'` 4b PASS rows against their own
monthly nulls — the census 680 could not do, now that the monthly gap is measured), 932 (why does
`U56/M/CORE/TOP20` beat its weekly twin by 2.09 pp of CAGR at 45% of the turnover — is the
monthly grid a real edge or a rebalance-offset artefact in the sense of idea 922/925).
