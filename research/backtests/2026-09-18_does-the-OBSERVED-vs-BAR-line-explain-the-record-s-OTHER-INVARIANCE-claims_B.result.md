# Idea 1251 (lane B, 2026-09-18) — does the OBSERVED/BAR line explain the record's OTHER invariance claims?

**ANSWER: NO — the line survives on the OBSERVED side and COLLAPSES on the bar side.
VERDICT: KILL (capital), NO NEW BOOK.**  Gates 9 of 9.  Runtime 289 s.

## What was run
1242's SAME 72 decisions (PANEL {U56, B136, SMALL} x ANCHOR {A, B} x LADDER {N, H, GROSS,
CADENCE} x CHOOSER {CH_ISSHARPE, CH_ISCAGR, CH_ISDD}), all 18 outputs, at **41 knob cells**
(29 distinct draw matrices per decision) with **L frozen at 63** — the L ladder is replaced by
the record's other three resample knobs plus the seed:

| dial 1 = KNOB | ladder | endpoints |
|---|---|---|
| `K_SEED` | 8 rng streams | (0, 7) — also the NOISE YARDSTICK |
| `K_B` | 125 / 250 / 500 / 1000 / 2000 draws | (125, 2000) |
| `K_DRAW` | MBB (1101/1208's own, no wrap) / CBB (circular) / SB (stationary, same mean L) / IID | (MBB, IID) |
| `K_RECENTRE` | RAW / RECENTRED (each rung column shifted to the observed level) | (RAW, RECENTRED) |

dial 2 = OUTPUT SET {OS_CORE, OS_WIDE, OS_ALL} — 1242's three sets.  **All 12 combinations
published** in `.dialgrid.csv`; every output at every setting in `.outputs.csv` (2,952 rows);
the per-(knob, output) partition in `.partition.csv`; the 4 x 18 cell map in `.cellmap.csv`.
The cell-3 bar (knob swing / own seed swing > 2.0) was DECLARED in the docstring before
measuring, exactly as 1242 declared it.

## The result
**H_OBSFREE SUPPORTED — 20 of 20 OBS (knob, output) cells are structurally free.**  The five
observed-side outputs (O_REACH, O_PICK, O_MARGIN, O_LEVEL, O_GAPRATIO) are bit-identical at
every setting of every knob, and reach reads 14 of 72 at all 41 cells (G5, max dev 0.000e+00).
The observed half of 1242's line generalises perfectly.

**H_LINE REFUTED — only 8 of 52 BAR (knob, output) cells are knob-dependent**, against 13 of 13
L-dependent in 1242.  The line holds in **0 of 12** dial combinations.  Being bar-side does NOT
tell an implementer their number is at risk; it tells them nothing until the knob is named.

**H_SPECIFIC SUPPORTED — 8 of 13 BAR outputs are KNOB-SPECIFIC** (free of one knob, dependent
on another): B_PPICK, B_Q05, B_PMAX, B_RECRANGE, B_BOOT95, B_SD, B_RESOLVED, B_PCTRANK.

Median knob/seed ratio over the 13 bar outputs, by knob (OS_WIDE):

| knob | median ratio | bar outputs in cell 3 | reading |
|---|---|---|---|
| `K_SEED` | **1.000** | 0 of 13 | the yardstick calibrating against itself, exactly as designed |
| `K_B` | **0.618** | 0 of 13 | 125 -> 2000 draws moves NOTHING past its own seed noise |
| `K_RECENTRE` | **1.098** | 1 of 13 (B_PCTRANK, 2.072) | almost inert, and inert for a mechanical reason |
| `K_DRAW` | **2.178** | **7 of 13** | the only knob that is a real dial |

Two mechanical confirmations fall straight out: **B_RECRANGE and B_SD have ratio exactly 0.000
under K_RECENTRE** (a per-column mean shift cannot change a standard deviation or an
already-recentred range), and **B_GAPEXCEEDS is structurally free of all four knobs** although
1242 found it L-dependent on 2 of 72 decisions.

Inside K_DRAW the whole effect is **IID**, not the block family: resolution rate 0.2176 (MBB) /
0.2500 (CBB) / 0.2454 (SB) / **0.1667 (IID)**; mean P_pick 0.6065 / 0.5943 / 0.6035 / **0.5622**;
mean B_RECRANGE 0.4404 / 0.4377 / 0.4265 / **0.5323**.  The three block laws are within seed
noise of each other; dropping serial dependence altogether is what moves the bars.  Recentring
moves two outputs and only two: B_PCTRANK 0.5271 -> 0.4789 and B_MODALMATCH 0.7685 -> 0.8981.

## Census (ARM D) — what the record actually states
34,855 text units scanned (1,198 .md files + LEADERBOARD rows + CHANGELOG paragraphs); 4,247
mention one of the 18 outputs, **987 touch a BAR output and 809 of those carry a verdict word**.
Of those 809: **636 state NO knob at all**, 173 state any, and L is named in 57.  Share stating,
by knob: SEED 11.25%, B 7.91%, **DRAW KIND 6.80%**, RECENTRING 1.36%.  The record's habit is to
name L or nothing — and the knob it names is the second-smallest of the four, while the one it
names least often after recentring (draw kind) is the only one that is a real dial.

## Capital arm (ARM E) — rule 8 + both KEEP paths
1,626 rule-8 rows: every pick made on warm-up..2016-12-31 only, 2017-2026 read once, 10 bps,
next-day execution.  **4a: 0 of 1,626.**  4b full 453, 4b OOS 457, **4b BOTH 452 — collapsing to
25 distinct realised books, every one of them a rung book of the frozen comparison set and
NOT ONE of them produced by any gate in this run.**  Benchmarks: U56 SPY OOS 15.28% / 0.8745 /
-33.72%; LIVE RULES v2 OOS 9.47% / 1.2778 / -12.05%.  The best 4b-BOTH row is U56 anchor B
N=20 — full 11.07% / 1.1387 / -18.01%, OOS 12.48% / 1.1827 / -18.01% — and the committed
2026-09-04 book reproduces as U56 anchor A at full 15.62% / 1.1423 / **-19.13%**, OOS 17.04% /
1.1688 / -19.13%.  Which 4b leg binds over the 162 rung books: **L_DD fails 106**, L_H2 81,
L_OOS 76, L_CAGR 66, L_H1 50 — the drawdown leg again.

**H_MONEY REFUTED, but on a margin smaller than the knob itself.**  Best OBS (knob-free) gate
**0.8531** (SEL_GAPRATIO) vs best BAR (knob-keyed) gate **0.8574** (SEL_PCTRANK, RECENTRED) vs
no gate **0.8426** — the bar-side gate wins by **0.0043** of mean OOS Sharpe.  The spread that
the KNOB CHOICE ALONE opens inside that same gate family is **0.0180** (K_DRAW), 0.0127
(K_SEED), 0.0110 (K_B), 0.0073 (K_RECENTRE).  The dial the record does not state is **four
times the edge the gate buys**.  SEL_RESOLVED's knob spread is <= 0.0004 and SEL_GAPEXCEEDS's is
exactly 0.0000, so the price is specific to the gate, not general.  Paired delta of the best
knob-free gate over no gate: **+0.0105 (t +1.02, n 24)** — not significant either way.

## One warning worth more than the partition
`data/prices.csv` gained the 2026-09-17 close after 1242 ran, and the dividend re-adjustment
moves the whole U56 history by ~1e-7.  Every continuous output replays to **5.3e-05** under
that (G4b), and B136 and SMALL — whose tapes did not move — replay **BIT-EXACT** (G4, 0.000e+00
on 48 rows x 18 outputs).  But **B_PCTRANK jumps by up to 0.030 on 3 of 24 U56 rows for that
1e-7 shift**, all of them CH_ISDD on a 4-rung ladder: the percentile rank of an observed MaxDD
is DISCONTINUOUS, because many block draws reproduce the same worst episode exactly and sit as
an atom right at the observed level.  A committed B_PCTRANK on a drawdown statistic is not
reproducible to better than ~0.03 across a single day of tape, whatever knob is stated.

## Schema line this run supports
> A committed resample-derived number must state its DRAW KIND.  Stating the block length L
> alone is insufficient and stating the draw count B is nearly worthless: over 125..2000 draws
> no bar output moves past its own seed noise (median ratio 0.618), while MBB -> IID moves seven
> of thirteen (median 2.178).  A percentile rank of a DRAWDOWN statistic should not be committed
> at better than 0.03 resolution at all.

## Caveats
Rule 9 survivorship: U56, B136 and SMALL are current-constituent lists, so every LEVEL here —
CAGR, MaxDD, Sharpe and every null built on them — is optimistic, and any 4b pass in ARM E is an
upper bound.  It largely cancels out of the headline, which is a ratio of one construction
against itself on the same tape.  The knob swing for K_B and K_DRAW is averaged over 3 rng
streams and the yardstick over 8; the K_B ladder is nested (B=125 draws are a prefix of
B=1000's stream), which if anything UNDERSTATES the B knob, and it still reads 0.618.
