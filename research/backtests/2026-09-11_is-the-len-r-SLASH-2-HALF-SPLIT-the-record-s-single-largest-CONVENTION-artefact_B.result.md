# IDEA 697 (lane B, 2026-09-11) — is-the-len(r)//2-HALF-SPLIT-the-record-s-single-largest-CONVENTION-artefact

**VERDICT: SPLIT — CONFIRMED IN MAGNITUDE, KILLED AS A VERDICT RISK. No RULES change, no
book promoted, no KEEP claimed, no PROTOCOL change applied; RULES.md, PROTOCOL.md, scan.py,
bot.py and baseline.py untouched.**

The queue asked whether `baseline._row`'s `h = len(r) // 2` is the record's single largest
convention artefact. Re-cutting the same return series at a fixed calendar date moves the
H-legs by **up to 0.31 Sharpe** — 11x idea 517's published 0.0275 cross-panel calendar
floor — and flips **13 of 126** PROTOCOL 4a Sharpe legs (10.32%), one of them on a **3
calendar-day** boundary move. But **0 of 126** full 4a verdicts and **0 of 126** full 4b
verdicts change, because on this claim slice both paths are decided by legs that do not
contain a half at all. The convention is loud and unpublished; it is not, today, what is
deciding the record's KEEP/KILL calls.

## Gates (five, pre-registered, all PASS — printed before any result was read)

| gate | value |
|---|---|
| G1 `fast_bt` vs `engine.backtest`, 3 panels x 2 books, returns AND turnover | **2.429e-17 / 0.000e+00** |
| G2 live RULES v2 on U56 @10 bps vs idea 523's G3b constant (8.61% / 1.1998 / -12.05%) | **8.61% / 1.1998 / -12.05%** |
| G3 cost-rung identity `net(25) = net(0) - turn*25/1e4` vs a live 25 bps run | **0.000e+00** |
| G4 **load-bearing:** `halves_at(NATIVE)` == `baseline._row`'s H1/H2, 3 panels x 3 books | **0.000e+00** |
| G5 structural: NATIVE boundary is panel-dependent and is not the calendar midpoint | spread **368 d**, max offset from CALMID **6 d** |

G4 is the gate the whole run rests on: without it, nothing below is a statement about the
record's own convention rather than about a re-implementation of it.

## Design

Two tuned parameters, exactly the ones the queue names, all grid points reported.

- **PARAM 1 — split date (8 rungs):** `NATIVE` (= `len(r)//2`, the record's convention
  verbatim), `CALMID` (calendar midpoint of the series' own span), and six fixed calendar
  dates 2014-01-01 … 2019-01-01 that do not depend on the loaded window at all.
- **PARAM 2 — claim set (4 rungs):** `LIVE` (BAND03 = live RULES v2, BAND08), `RANKED`
  (TOP20, TOP10), `EWGATE` (the Sep-3 memo's gated equal-weight book), `CONTROL` (SPYBH —
  one asset, zero signal, zero parameters).

Panel (U56 / B136 / SMALL439) is **reported, not tuned** — all three, every cell. 8 x 6
books x 3 panels = **96 grid cells**, each printed with H1, H2, both comparands' halves, and
both KEEP predicates. 10 bps, weekly, t+1, warm-up 260 kept verbatim from `compare`.
Deterministic, no network, no RNG.

## Result 1 — the exposure is near-total, and the boundary is unpublished

531 of 600 committed price-loading backtest scripts (**88.5%**) produce their H-legs from an
index-length split (524 carry their own `len(x)//2`, 26 call `baseline.compare`). 98.2%
mention H1/H2 at all.

Where the boundary actually lands, on the full native window:

| panel | n | window | NATIVE boundary | CALMID boundary | offset | H1 cal-days | H2 cal-days |
|---|---|---|---|---|---|---|---|
| U56 | 4442 | 2009-01-13 → 2026-09-10 | **2017-11-07** | 2017-11-13 | -6 d | 3220 | 3229 |
| B136 | 4439 | 2009-01-13 → 2026-09-04 | **2017-11-03** | 2017-11-09 | -6 d | 3216 | 3227 |
| SMALL | 3934 | 2011-01-13 → 2026-09-04 | **2018-11-06** | 2018-11-09 | -3 d | 2854 | 2859 |

On an untruncated panel `len(r)//2` is within 6 days of the calendar midpoint — the
convention is *not* badly behaved in itself. Its two real problems are that the boundary is
**368 calendar days apart across the three live panels** (so a cross-panel "both halves"
claim compares two different eras), and that it is **never printed**, so no committed
half-split number in the record can be checked without re-running the script.

## Result 2 — the queue's question, answered: 10.32% of 4a legs, 0% of verdicts

Unit = one book x panel pair, i.e. one published verdict. 126 comparisons per leg.

| leg | moves vs NATIVE | rate |
|---|---|---|
| 4a Sharpe leg (`H1>v2.H1 and H2>v2.H2`) | **13 / 126** | **10.32%** |
| 4b Sharpe leg (`H1>SPY.H1 and H2>SPY.H2`) | 0 / 126 | 0.00% |
| **full 4a verdict** | **0 / 126** | **0.00%** |
| **full 4b verdict** | **0 / 126** | **0.00%** |

Mean |ΔH1| by split rule runs 0.0104 (CALMID) to 0.1255 (2019-01-01); by claim set the mean
is 0.0749 (LIVE) / 0.0882 (RANKED) / 0.0622 (EWGATE) / 0.0547 (CONTROL), with a **max |ΔH1|
of 0.3100** (RANKED). The zero-signal control is decisive on magnitude: SPY held one way,
same data, moves its **own** H1 by **0.1529 / 0.1941 / 0.1529** across the eight rungs. That
is 100% convention and 0% book, and it is **7x idea 517's 0.0275 cross-panel calendar floor**.

**The sharpest single fact:** TOP20 on SMALL439 flips its 4a Sharpe leg False → True when
the boundary moves **3 calendar days** (2018-11-06 → 2018-11-09, ΔH1 -0.0203 / ΔH2 +0.0134).
Neither date appears anywhere in the record.

## Result 3 — why no full verdict moves (and this is the honest half of the answer)

The half-split legs are not what is binding. Over the 18 book x panel pairs:

- 4a's **MaxDD leg** passes **3 of 18** — and all three are BAND03 against itself (the book
  *is* the baseline), so on a non-identity book it passes **0 of 15**.
- 4b's **DD cap** passes 8 of 18, its **CAGR floor** 10 of 18, its **OOS leg** 10 of 18.

All four are split-invariant by construction. So every 4a verdict on this slice is already
dead on drawdown before its halves are consulted, and the one 4b passer (EWALL on B136)
clears its halves by a margin no split rule on the ladder closes. This replicates ideas
530/531 — the DD cap does the cutting — from a new direction, and it is the reason the
queue's "single largest convention artefact" framing is **refuted at the verdict level**.

## Result 4 — the mechanism is window mix, NOT stress-year reallocation

2020 and 2022 sit in H2 under **all 8 split rules on all 3 panels** (0 exceptions in 48
checks), because the pre-registered ladder tops out at 2019-01-01. So the H-leg movement
measured above is not the stress years changing sides; it is how much of the quiet 2013–2016
bull is counted in H1. A split date at or after 2020 would move the stress years and should
be larger — that is outside this run's grid and is **not claimed here**; it is left to the
queue.

## Result 5 — PROTOCOL 8 walk-forward, both KEEP paths, 24 rows

Band picked on 2009–2016 IS Sharpe only, evaluated on 2017–2026 untouched. IS ladders:
U56 0.00:1.0548 / 0.03:1.1043 / 0.05:1.0625 / **0.08:1.1222** / 0.12:1.1202 → pick 0.08;
B136 1.0568 / 1.0912 / 1.0754 / **1.1412** / 1.1357 → pick 0.08;
SMALL 0.4625 / 0.5308 / 0.5767 / 0.6006 / **0.6437** → pick 0.12.

| panel | pick | OOS CAGR | OOS Sharpe | OOS MaxDD | v2 OOS (CAGR/Sh/DD) | SPY OOS (CAGR/Sh/DD) |
|---|---|---|---|---|---|---|
| U56 | 0.08 | 8.97% | 1.1627 | -14.47% | 9.45% / 1.2747 / -12.05% | 15.24% / 0.8721 / -33.72% |
| B136 | 0.08 | 8.36% | 1.1095 | -14.81% | 7.98% / 1.1185 / -12.24% | 15.45% / 0.8820 / -33.72% |
| SMALL | 0.12 | 4.92% | 0.6888 | -15.59% | 4.55% / 0.6629 / -12.09% | 15.45% / 0.8820 / -33.72% |

**4a passes 0 of 24. 4b passes 0 of 24.** Identical under every split rule — each panel is
`split-invariant`. The rule-8 OOS window is fixed by PROTOCOL 8 and does not move with the
split rule; what the split rule moves is the full-sample H-legs *inside* the predicates. The
picked books beat SPY on Sharpe and drawdown but land at 58.9% (U56), 54.1% (B136) and
31.8% (SMALL) of SPY's OOS CAGR against a 70% floor, so 4b fails on the floor, not on
anything this run tuned.

## What this does and does not license

- It does **not** license a PROTOCOL change. The convention is unpublished and moves legs,
  but on the 126 verdicts re-cut here it changed none of them. Proposing a fixed-date split
  on this evidence would be trading a measured-inert artefact for a new tuned constant.
- It **does** license one cheap, zero-parameter hygiene ask, which is recorded here and not
  applied: **print the half boundary next to every published H1/H2.** It costs one field,
  it makes 88.5% of the record's H-legs checkable from the committed numbers, and it would
  have let idea 517 attribute its 14-of-18 flips without re-running anything.
- The 368-day cross-panel boundary spread is the live risk: any claim of the form "book X's
  halves beat book Y's halves" **across panels** is comparing 2017-11 against 2018-11. Every
  comparison in this run was held within a single panel for exactly that reason.

## Caveats

Current-constituent survivorship in all three panels. Only 2020 and 2022 are real stress
tests, and on this ladder both always sit in H2. The claim slice is six pre-registered books,
not a literal re-run of every committed leaderboard row — the 88.5% exposure census is the
denominator for how far the finding could reach, not a count of verified flips. SPY's OOS
CAGR of 15.4% reflects a QQQ/large-cap-favourable 2017–2026.

Artefacts: `.geometry.csv`, `.census.csv`, `.grid.csv` (all 96 cells), `.moves.csv`,
`.claimsets.csv`, `.flippedcells.csv` (the 13, named), `.bindinglegs.csv`, `.regimes.csv`,
`.walkforward.csv`, `.console.txt` (full run log).
