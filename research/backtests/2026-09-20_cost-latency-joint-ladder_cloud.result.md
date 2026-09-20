# Idea 2046 (lane cloud, 2026-09-20) — DOES THE DUAL-PATH 4a PASS SURVIVE THE COST AND LATENCY LADDERS **JOINTLY**?

**ANSWERED — SPLIT, PLUS A METHOD RESULT. 4b is ROBUST on the whole joint plane (9 of 9, t+3 and
50 bps included). 4a is an ARTEFACT (2 of 9) and dies on LATENCY ALONE: it needs t+1 execution at
any cost. AND THE TWO LADDERS ARE ADDITIVE — the joint cross carries no information the two
separate ladders did not already carry (worst Sharpe interaction 0.0036 = 2.8% of the larger main
move, MaxDD 0.67 pp).**

## The question
Idea 2034's dual-path cell (`B136, VOLTGT t = 0.10, DRIFT h = 0.08, trade weekly`) had cost and
latency moved only **separately**: 2034 walked COST {0, 10, 25, 50} at t+1, 2054 walked DELAY
{t+1, t+2} inside a wider four-axis cross. Neither walked them together and neither went past t+2.
A rule you cannot execute same-week is not a rule you can run.

## The construction
Whole vol-target corpus on the joint cross: PANEL {U56, B136, SMALL665} x `t` {0.08 .. 0.20} x
[DRIFT `h` 10 rungs | CAL `R` {D, W, M, Q}] x **DELAY {t+1, t+2, t+3}** = **630 books**, x **COST
{10, 25, 50} bps** = **1,890 scored cells**. Cadence held at W and phase at the engine mask (idea
2054 owns those axes). Baselines held at the LIVE convention (RULES v2 weekly t+1 at 10 bps, and
SPY), so a slower, dearer idea must beat the undelayed cheap live book. **TUNED: 2, both inherited**
(`t` and the dial). **t+3 had never been priced in this record.** Gates **8 of 8**; the candidate
reproduced to max |d| = **8.327e-17** and the standing VOLTGT memo to 4.605e-05.

## V2 — 4b IS ROBUST, 9 OF 9 (100.0%)
The binding-leg column reads `none` at every one of the nine points. Worst corner (50 bps, t+3):
**10.79% / 1.0536 / -13.98%** against a `0.70 x SPY` CAGR floor of **10.59%** and a `0.60 x SPY`
MaxDD cap of **-20.23%**. The CAGR leg is the thin one, as always: +0.20 pp of margin at the worst
corner, against +1.92 pp at the discovery corner.

| delay | 10 bps | 25 bps | 50 bps |
|---|---|---|---|
| t+1 | 12.51% / 1.2286 / -11.81% — **4a+4b** | 11.98% / 1.1812 / -12.01% — **4a+4b** | 11.11% / 1.1020 / -12.71% — 4b only (H1) |
| t+2 | 12.36% / 1.2027 / -12.82% — 4b only (MaxDD) | 11.82% / 1.1556 / -12.92% — 4b only (MaxDD) | 10.94% / 1.0770 / -13.25% — 4b only (H1) |
| t+3 | 12.19% / 1.1767 / -13.74% — 4b only (MaxDD) | 11.67% / 1.1306 / -13.83% — 4b only (H1) | 10.79% / 1.0536 / -13.98% — 4b only (H1) |

## V1 — 4a IS AN ARTEFACT, 2 OF 9 (22.2%), AND LATENCY IS THE BINDING AXIS
The 4a frontier: **t+1 clears 4a up to 25 bps; t+2 and t+3 clear it at NO cost, not even 0-to-10
bps.** Failure modes: H1 Sharpe x4, MaxDD x3. The mechanism is the one idea 2054 named — one extra
day of latency pushes MaxDD from -11.81% through the live book's **-12.24%** (to -12.82% at t+2,
-13.74% at t+3) while both Sharpe halves still clear; adding cost then takes the H1 leg as well.
This independently reproduces 2054's 22.2% on a different slice of axes, and extends it: **t+3 does
not rescue anything** (4a 0 of 3; corpus-wide 4a falls 21 -> 2 of 210 from t+1 to t+3 at 10 bps).

## V3 — THE TWO LADDERS ARE ADDITIVE (the method result)
Sharpe move from the (10 bps, t+1) corner, decomposed into cost-only + delay-only + interaction:
the worst interaction over the four genuinely joint points is **+0.0036 Sharpe = 2.8%** of the
larger main move (bar was 20%); on MaxDD, **0.67 pp**. Cost owns -0.1266 of Sharpe at 50 bps and
latency -0.0519 at t+3; they simply add. **So the record's habit of pricing cost and latency on
separate corpora was legitimate here** — but the additivity also means latency cannot be bought
back with cheaper execution, which is exactly why 4a has no surviving cell off t+1.

## Corpus census, by (delay, cost), 210 cells each
4b: 91 / 81 / 62 (t+1), 88 / 83 / 67 (t+2), 77 / 66 / 48 (t+3) — a 47% decay to the worst corner.
4a: 21 / 4 / 0, 14 / 0 / 0, 2 / 0 / 0 — **zero at every point except the two cheapest t+1/t+2
corners.** By panel: B136 4b 357/630 4a 37/630; U56 306/630 and 4/630; **SMALL665 0 of 630 on BOTH
paths — a seventh independent confirmation that this family does not work on small caps.**

## Rule 8 (parameters chosen on 2009-2016 only; 2017-2026 read ONCE)
108 legal picks (3 panels x 3 delays x 3 costs x 2 families x 2 IS-only choosers). **1 of 108
clears BOTH paths** — `B136, t+1, 10 bps, DRIFT, CH_ISMINLEG -> t = 0.10, h = 0.08`, i.e. the
candidate itself, OOS **13.01% / 1.2928 / -11.81%** (SPY OOS 15.26% / 0.8737 / -33.72%; live RULES
v2 OOS 7.85% / 1.1017 / -12.24%). **39 of 108 clear 4b only**, spread across all three delays and
all three costs on U56 and B136 and none on SMALL665. A legal chooser lands on the candidate at 1
of 108 — it is reachable, and only at the discovery corner.

## What it changes
1. The standing KEEP-candidate memo gains a second addendum: the **4b** leg now carries a
   **45-of-45 joint stress record** (36 from idea 2054 + 9 here, t+3 newly included), and the
   **4a** downgrade is re-confirmed on an independent slice with the axis named: **latency, not
   cost**. `t+1` is a load-bearing clause of the rule, not a convention.
2. NEW STANDING NOTE: because cost and latency are additive on this family, they may go on being
   priced separately — but any 4a claim must state its EXECUTION DELAY, because that is the axis
   that kills it at every cost.
3. No rules change. Sunday review decides.

## Survivorship
U56 / B136 are CURRENT-constituent lists and SMALL665 a CURRENT sub-$2B screen (54 tickers with
`max_1d_move >= 1.0` in `data/small_meta.csv` dropped first). Every CAGR and drawdown LEVEL above
is optimistic and both 4b bars are easier here than on a point-in-time panel. The (cost x delay)
CONTRASTS are same-tape / same-names / same-grid and first-order immune; the PASS COUNTS are not.
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are untouched.

## Evidence
`research/backtests/2026-09-20_cost-latency-joint-ladder_cloud.py` / `.log.txt` / `.console.txt` /
`.grid.csv.gz` (1,890 rows) / `.candidate.csv` (9) / `.frontier.csv` / `.interaction.csv` /
`.census.csv` / `.walkforward.csv` (108) / `.gates.csv` (8/8).
