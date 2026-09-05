# Idea 172 — the-20-percent-oracle-ceiling (lane C, 2026-09-05)

**ANSWERED, and idea 172's "if so" branch is only THREE-QUARTERS true. KILL of the strong
recommendation ("stop pricing gross"); the ladder survives, but as a CAGR-floor and drawdown
instrument only. No RULES change, no new book, no KEEP.**

Script `2026-09-05_the-20-percent-oracle-ceiling_C.py`; console, `.ladder.csv` (3000 rows),
`.books.csv` (300), `.tolerance.csv` (2700), `.walkforward.csv` (24) alongside.

## Corpus and reproduction

Idea 78's Test B re-run through the engine, identical to idea 166's: B136, k ∈ {20,40,80},
50 seeded sub-panels per k, CAND-n at n ∈ {5,20}, 10 bps, weekly, t+1, ladder
{0.20…1.00} (10 points, PROTOCOL rule 2 caps it at 1.00). **300 books × 10 points = 3000
genuine backtests**, runtime 1736s.

**Reproduction 3 of 3, asserted before any new number was read:**

* **[a]** vs idea 166's committed `.ladder.csv`, all 3000 rows, index identical: max |diff|
  **2.220e-16** on IS_margin / full_margin / Sharpe / IS_Sharpe, 1.110e-16 on OOS_margin,
  9.714e-17 on CAGR and MaxDD; the OOS failing-bar string identical in **100.0%** of 3000.
* **[b]** Idea 172's own premise: **60 of 300 books (20.0%)** have some ladder point passing the
  OOS-window 4b (114 of 3000 points; 74 of 300 on the full sample).
* **[c]** The failing-bar string rebuilt from the five per-bar relative slacks matches idea
  166's independently-built string in **100.0%** of 3000 rows.

## (1) The answer: not always a Sharpe bar — but the bar that is never unreachable is the DD cap

Of the **240** books outside 4b at every legal gross:

| class | books | share of 240 |
|---|---|---|
| SHARPE-ONLY (U ⊆ {H1,H2,OOS}) | **177** | 73.8% |
| MIXED (both kinds) | 42 | 17.5% |
| GROSS-ONLY (U ⊆ {DD,CAGR}) | 16 | 6.7% |
| MISALIGNED (U empty, still no passing point) | **5** | 2.1% |

So the unreachable set is a subset of the SHARPE bars in **177 of 240 (73.8%)** and involves a
gross-sensitive bar in **58 of 240 (24.2%)**. Idea 172's premise is directionally right and
quantitatively short of "always".

**The sharper finding is per-bar.** Unreachability among the 240:

| bar | kind | unreachable | median best slack | median slack RANGE over the ladder | median relaxation needed |
|---|---|---|---|---|---|
| H1 | SHARPE | **157** (65.4%) | −0.0698 | 0.0076 | 0.1309 |
| H2 | SHARPE | 143 (59.6%) | −0.0543 | 0.0042 | 0.1482 |
| OOS | SHARPE | 141 (58.8%) | −0.0364 | 0.0050 | 0.1318 |
| **DD** | GROSS | **0 (0.0%)** | **+0.7174** | 1.0363 | — |
| CAGR | GROSS | 58 (24.2%) | +0.2824 | 1.0170 | 0.1448 |

**The drawdown cap is unreachable in ZERO of 240 books.** Every gross-sensitive exclusion in the
corpus is the CAGR floor (all 58; the 16 GROSS-ONLY books are `U = {CAGR}` exactly). That is the
half of idea 172's hypothesis that holds outright — with the honest caveat that DD's
reachability is partly mechanical: its modal ladder argmax is **g = 0.20**, the ladder's floor,
because de-grossing far enough always shrinks drawdown. CAGR's modal argmax is **g = 1.00**. The
two gross-sensitive bars are reachable at OPPOSITE ends, which is exactly why idea 184 found 4b
admission to be a contiguous interval — the ladder's whole job is locating the overlap.

**MISALIGNED is 5 of 240 (2.1%)** — the only class a finer or wider ladder could ever rescue.
All 5 sit in k=40/n=20; all 16 GROSS-ONLY books sit in k=20/n=20, the cell that holds every
eligible name by construction (idea 78's flag).

## (2) Gross-invariance of the Sharpe bars, measured (P5)

Median slack range over the 6.75× gross span, all 300 books: **H1 0.0071, H2 0.0040, OOS
0.0042** against **DD 1.0153, CAGR 1.0524** — a factor of **150–250×**. This is idea 66/173/176's
flat-Sharpe result re-derived on the exclusion side, and it is why 177 books are hopeless: the
bar that blocks them cannot be moved by the only dial being priced.

## (3) How far outside — the signed tolerance sweep (tuned param 2)

A bar counts as met iff its relative slack > τ; τ < 0 relaxes, τ > 0 tightens.

| τ | REACHED | SHARPE-ONLY | GROSS-ONLY | MIXED | MISALIGNED |
|---|---|---|---|---|---|
| −0.20 | 192 | 86 | 7 | 15 | 0 |
| −0.10 | 131 | 131 | 14 | 21 | 3 |
| −0.05 | 87 | 159 | 16 | 34 | 4 |
| −0.02 | 72 | 170 | 15 | 40 | 3 |
| **0.00** | **60** | **177** | **16** | **42** | **5** |
| +0.02 | 47 | 177 | 14 | 47 | 15 |
| +0.05 | 32 | 190 | 11 | 54 | 13 |
| +0.10 | 6 | 201 | 11 | 64 | 18 |
| +0.20 | 0 | 195 | 4 | 94 | 7 |

Relaxing every bar by 0.05 rescues **18 of the 177 SHARPE-ONLY books (10.2%)**; by 0.10, 30.5%;
by 0.20, 59.9% (**P6 HIT**). Median relaxation needed for an unreachable Sharpe bar is
0.13–0.15 — these are not near-misses. In the other direction the 60 REACHED books are fragile:
tightening by only 0.02 costs 13 of them and by 0.10 costs 54 of 60, and they pass at a mean of
**1.90 of 10** ladder points, clustered at g = 0.70/0.75 (31 and 33 of 60) — the incumbent gross.

*(Correction logged in the script header: the first execution swept τ ≥ 0 only, reading P6 in
the tightening direction rather than the relaxation P6 states. The sweep was made signed and the
run repeated in full. Reproduction, decomposition and walk-forward numbers were unchanged.)*

## (4) Rule 8 walk-forward — everything chosen ≤ 2016-12-31, 2017-2026 read once, 6 cells

| selector | mean OOS Sharpe | OOS CAGR | OOS MaxDD | 4a | full 4b | OOS-window 4b | mean g |
|---|---|---|---|---|---|---|---|
| S0 do-nothing (full B136 @0.75) | 0.8529 | 14.27% | −21.71% | 3 | 0 | 0 | 0.75 |
| S1 IS-Sharpe argmax @0.75 | **0.9394** | 12.53% | −19.53% | 4 | 1 | 1 | 0.75 |
| S2 IS-reachability screen | **0.9394** | 12.53% | −19.53% | 4 | 1 | 1 | 0.75 |
| S3 price the gross | 0.9373 | 9.38% | **−14.53%** | **6** | **3** | **2** | 0.583 |

Benchmarks over the same window: **SPY OOS 15.45% / 0.882 / −33.72%**, **RULES v1 on B136 OOS
5.94% / 0.576 / −21.19%**. Paired vs S0: S1/S2 **+0.0865** (t 1.90, 4W/2L), S3 **+0.0844**
(t 1.82, 4W/2L).

Two readings, both honest:

* **Pricing the gross does not buy risk-adjusted return.** S3 − S1 = **−0.0021** of OOS Sharpe
  while surrendering **3.15pp of OOS CAGR**. As a Sharpe instrument the ladder is a do-nothing,
  a ninth consecutive such reading (110/132/151/166/171/174/175/184/186/192 line).
* **It does buy drawdown, and drawdown moves 4b.** S3 cuts OOS MaxDD by **5.0pp** and turns
  4a 4→6, full 4b 1→3 and OOS-window 4b 1→2 of 6 cells. The ladder is a DRAWDOWN dial that 4b
  happens to score, which is idea 163's hypothesis arriving from the gross side.
* **The IS-reachability screen changes no pick.** It admits 95 of 300 books (31.7%) and selects
  the identical book in **6 of 6** cells — a fourth reproduction of ideas 132/140/151's
  "the IS screen changes zero picks".

## (5) Both KEEP paths, all 3000 book-ladder rows

**4a 1974 / 3000; full-sample 4b 157; OOS-window 4b 114.** Best full-4b row is k=20 draw=19
n=20 at g=0.90 — 11.19% / 1.204 / −12.58%, OOS 10.04% / 1.104 / −12.58% — which is idea 166's
MIDPOINT pick re-derived, a **re-grossing of a CAND-20 book** (idea 144) that fails the
OOS-window CAGR floor (10.04% vs the required 10.82%). The one prospective pick clearing every
bar on both windows (k=40/n=20 draw=42 @0.75, OOS 12.30% / 1.068 / −19.63%, OOS margin +0.0299)
is the top-20 of a **seeded random 40-name sub-panel** — not an implementable universe, and 1 of
50 draws chosen by an IS argmax. **No book is proposed. No KEEP.**

## Predictions: 7 of 8 HIT

P1 ✓ (reproduction 3/3) · P2 ✓ (73.8% SHARPE-ONLY, 58 with a gross-sensitive bar) ·
P3 ✓ (MISALIGNED 2.1% < 15%) · **P4 MISS** (H1 is the most frequently unreachable bar at
157/240, not H2 — the OOS window's own first half, 2017-2021, is where these books lose) ·
P5 ✓ (150–250×) · P6 ✓ (10.2% < 25%) · P7 ✓ (0.9373 ≤ 0.9394) · P8 ✓ (no new book).

## Recommendation (report-only; RULES and PROTOCOL untouched by this run)

Idea 172 proposed "stop pricing gross". The corpus does not support that, and supports a
narrower clause instead:

> **The gross ladder must never be run to satisfy the DRAWDOWN cap.** On 240 books excluded at
> every legal gross the DD cap is unreachable in 0, at a median best slack of +0.72; the only
> gross-sensitive bar that ever excludes a book is the CAGR floor (58 of 240). Combined with
> idea 184's finding that admission is a contiguous interval recoverable from one run, a book's
> gross should be published as **the admissible interval plus the CAGR-floor-binding endpoint**,
> and the compute saved spent on cadence (idea 175) rather than on gross.

For 177 of the 240 (73.8%) no gross clause of any kind helps: the blocking bar moves 0.004 over
the whole ladder and needs 0.13–0.15 of relaxation to close. Those books are not gross problems.

## Caveats

Survivorship (B136 is a current-constituent list, idea 54) · idea 144 (a re-grossed book is the
same book) · idea 38 (calendar-day price index) · idea 126 (t+1 only) · "unreachable" means
unreachable on this 10-point ladder bounded by PROTOCOL rule 2's no-leverage cap, so a bar
closable only at g > 1.00 is correctly counted unreachable · the k=20/n=20 cell is degenerate by
construction · the 300 sub-panels overlap, so every t is a magnitude cue, not a test.
