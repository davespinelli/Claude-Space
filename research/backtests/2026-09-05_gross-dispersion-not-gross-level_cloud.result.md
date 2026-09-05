# Idea 143 — gross-dispersion-not-gross-level (cloud, 2026-09-05)

**Verdict: ANSWERED — the pre-registered separation claim REPRODUCES exactly and cv strictly
dominates the gross LEVEL bar on the frontier, but it is a KILL as an *adequacy* bar and at most
a PARK as a *construction* test. No new book, no KEEP, no RULES change proposed.**

The one-line result: **cv(daily gross) is not a better version of 4b's CAGR floor — it is a
different instrument that answers a different question.** It empties the 342-row static-gross
ladder at κ = 0.025 while saving 25 of 27 floor victims and **11 of 11 Pareto-best** (γ needed
0.68 to empty the ladder and saved 0 of 11 there) — but it does so by **discarding 10 of the
floor's own 29 admissions**, and all 10 are full-gross `-rw` rebuilds. A bar that rejects a book
for *not de-grossing* is not an adequacy bar.

## Reproduction gate (run before any new number was read)

Idea 131's script is **imported**, not re-implemented; its corpus is rebuilt and compared
column-for-column against the committed CSVs.

| check | result |
|---|---|
| 306 arm-rows × 28 numeric columns vs `.grid.csv` | max abs diff **3.55e-15** — PASS |
| 342 ladder rows × 8 numeric columns vs `.ladder.csv` | max abs diff **2.22e-16** — PASS |
| census 306 rows / 29 pass-4b / 27 floor-only / 342 ladder / 97 ladder floor-only | **all exact** — PASS |
| 27 victims, 11 Pareto-best among them | **27 / 11** — PASS |

**One tuned parameter**: κ, the cv bar, on 0.000→0.400 step 0.005 (**81 points, all reported**).
δ (0.60), φ (0.70) and γ (0.50) are held at their published values and never searched.
New relative to idea 131: cv computed on **three windows** (full / IS / OOS) for every arm row
*and* every ladder row — idea 131 carried the full-sample cv only, which cannot answer rule 8.

## Q0 — the queue's premise, checked literally

| family | n | cv min | median | mean | max |
|---|---|---|---|---|---|
| floor's victims | 27 | 0.0028 | 0.2825 | **0.2675** | 0.3351 |
| …of which Pareto-best | 11 | 0.2417 | 0.2855 | 0.2831 | 0.2999 |
| static-gross ladder | 342 | 0.0030 | 0.0111 | **0.0120** | **0.0224** |
| core-admissible ladder | 107 | 0.0048 | 0.0121 | 0.0137 | 0.0222 |

The QUEUE's wording reproduces **to the digit**: 0.268 vs 0.014, max 0.335 vs 0.022, and exactly
**2 of 27** victims sit inside the ladder's cv range — `v1gate-rw` (0.0028) and `g200-rw` (0.0030),
both u56/EWall, both full-gross rebuilds. On the LEVEL axis the same two families overlap
([0.519, 0.750] vs [0.075, 0.672]); on the DISPERSION axis they are 12× apart in the median.

## Q1/Q2 — the separation frontier (81 κ, all in `.frontier.csv`)

| κ | corpus admits | of the floor's 29, lost | victims saved (27) | **Pareto saved (11)** | **ladder admitted (342)** |
|---|---|---|---|---|---|
| 0.000 | 56 | 0 | 27 | 11 | 107 |
| 0.005 | 44 | 10 | 25 | 11 | 105 |
| 0.020 | 44 | 10 | 25 | 11 | 18 |
| **0.025** | **44** | **10** | **25** | **11** | **0** |
| 0.145 | 27 | 27 | 25 | 11 | 0 |
| 0.245 | 25 | 28 | 24 | 10 | 0 |
| 0.300 | 5 | 29 | 5 | 0 | 0 |
| φ = 0.70 (published floor) | 29 | — | 0 | 0 | 10 |
| γ = 0.68 (idea 131's ladder-emptying γ) | 30 | 1 | 2 | 0 | 0 |

**κ doing BOTH jobs (all 27 victims AND 0 ladder points): 0 of 81 grid points** — the same
structural verdict as γ's 0 of 34, and for a *stated mechanism*: `v1gate-rw` and `g200-rw` hold
gross constant by construction, so no statistic of the gross series can tell them from a lever.

But the frontier is not the same frontier. At κ = 0.025 the bar empties the ladder **completely**
while keeping 25 victims and **every** Pareto-best book. γ could not buy that at any price. There
is a wide plateau: κ ∈ [0.025, 0.240] holds 25 / 11 / 0 unchanged (idea 128's plateau reading).

**The disqualifying cost, which no summary statistic shows.** From κ = 0.005 the bar discards
**10 rows the published floor admits**, and all ten are `-rw` arms with mean gross pinned at
0.7502 and cv ≈ 0.0030: u56/EWall `g200/band3/abs12/vol60-rw`, broad/EWall `g200/band3/v1gate-rw`,
plus their 25 bps twins. **Four of the ten also pass 4a.** They are genuinely good books —
broad/EWall `band3-rw` runs 11.7% / 1.069 / −18.5% — rejected solely for staying invested.
γ lost 0–1 admissions doing its job; κ loses 10 doing its job better. **That is the trade, and it
is why this is not an adequacy bar**: 4b's fifth bar exists to certify that a book is *worth
capital*, and "it varies its exposure" is not that claim. What the cv bar actually is, is a
**ladder-exclusion test** — a construction filter, which is exactly the direction idea 131's
closing paragraph and idea 144 point at.

## Q3 — rule 8 (κ re-chosen on 2009–2016 only; picks read once on 2017–2026)

κ* = **0.020**, the smallest κ emptying the ladder **on the IS window** (there 8 of 9 IS victims
survive). No OOS number was read to choose it. Selectors all pick argmax IS Sharpe.

| selector | cells picking | OOS CAGR | OOS Sharpe | OOS MaxDD | beat SPY | beat v1 | beat control | picks moved vs S0 |
|---|---|---|---|---|---|---|---|---|
| S0 no screen (all 18) | 18 | 9.1% | 0.695 | −23.1% | 6/18 | 12/18 | 3/18 | — |
| S1 IS-4b + CAGR floor | 7 | 12.7% | 1.022 | −21.1% | 5/7 | 7/7 | 2/7 | 0 |
| S2 IS-4b, no adequacy bar | 7 | 12.7% | 1.022 | −21.1% | 5/7 | 7/7 | 2/7 | 0 |
| S3 IS-4b + gross level 0.50 | 7 | 12.7% | 1.022 | −21.1% | 5/7 | 7/7 | 2/7 | 0 |
| **S4 IS-4b + cv ≥ 0.020** | 7 | **11.7%** | **1.076** | **−18.5%** | 5/7 | 7/7 | **4/7** | **3** |

Paired on the same 7 cells (S4 enters exactly the cells S1/S2/S3 do): **+0.054 OOS Sharpe,
2.6 pp shallower OOS drawdown, −1.0 pp OOS CAGR.** OOS references: **SPY 15.45% / 0.882 / −33.7%**,
RULES v1 4.86% / 0.451 / −25.3%, ungated control Sharpe 0.762.

**This is the first bar the project has tested that is not selection-inert.** Ideas 131 and 132
found the CAGR floor, the gross-level bar and the IS-4b screen all move **0** picks; the cv bar
moves **3 of 7**, and the sensitivity sweep shows 2–5 moves across κ ∈ [0.01, 0.09] rather than a
single knife-edge.

**What the 3 moves actually are, before anyone quotes the +0.054.** Two are the same swap in the
same book at two cost rungs — u56/EWall, `abs12-rw`/`control` → `band3-dg`, buying 8–10 pp of
OOS drawdown (−12.1% vs −19.9%/−22.5%) and +0.25/+0.12 Sharpe for −2.5/−4.4 pp CAGR. The third
(u56/TOP20, `control` → `ebud-0.20`) is a null: 1.1667 → 1.1667. So the OOS gain is **one
mechanism in one panel-book**, not three independent confirmations. Idea 142 exists because 7
paired cells cannot order selectors; nothing here is claimed as a selector ranking.

## Both KEEP paths, all 306 rows

4a: **97 of 306**. 4b published (φ): **29**, 6 also 4a. 4b with γ = 0.50: **56**, 25 also 4a.
4b with κ* = 0.020: **44**, 21 also 4a (ladder 18 of 342 still in at κ*; 0 at κ = 0.025).
Admitted-set OOS quality — FLOOR n=29 **13.2% / 1.114 / −18.5%**; GROSS(0.50) n=56
**11.2% / 1.112 / −16.6%**; CV(0.020) n=44 **11.0% / 1.117 / −16.1%**. The three admitted sets are
Sharpe-indistinguishable (0.003 apart); the cv set is the shallowest and the smallest of the two
widened ones. **No book is promoted.** This script re-scores an existing corpus under an
alternative bar — the bar is the thing adjudicated.

## Caveats, stated not buried

- **Survivorship** (idea 54): all three panels are current-constituent lists; the small panel is a
  sub-$2B screen run today and back-filled to 2010 (439 names after dropping `max_1d_move ≥ 1.0`
  per idea 118). Absent delistings inflate CAGR most for ungated high-gross books. The Q0/Q1/Q2
  separation result is a statement about the **dispersion of gross**, so it is structurally immune;
  the Q3 OOS numbers are **not**.
- **n is small where it matters**: 11 Pareto victims in 4 cells, all EWall, overlapping return
  series; 7 paired rule-8 cells; 3 moved picks of which 2 are one mechanism and 1 is a null.
- **Idea 128**: the IS window's SPY drawdown is shallower than the full sample's, so every IS
  drawdown cap admits too much — this biases S1–S4 identically and cannot explain a 3-vs-0
  difference in moved picks.
- Ideas **38** (u56/broad calendar-day index) and **126** (t+1 only, no lag band) carry over.
- The ladder remains the **only** control for "is this bar doing its job", and it is narrow: it
  catches static de-grossing, not other ways of gaming a drawdown cap.
- κ = 0.025 is read off the ladder's own maximum (0.0224). It is a **property of this corpus**,
  not a universal constant; a ladder built at finer gross steps would move it.

## What this leaves for PROTOCOL

Nothing to adopt as a fifth 4b bar. The usable output is the **negative pair**: 4b's
exposure-adequacy bar must not be restated as a gross **level** (idea 131) *or* as a gross
**dispersion** (here) — the first cannot separate the ladder, and the second separates it only by
also rejecting every full-gross rebuild. Both failures point the same way, at idea 144's
construction fix: **a static rescaling of an existing book is the same book and should not be a
corpus row at all**, in which case no bar has to do this job. The one thing worth carrying forward
is the rule-8 observation — the cv bar is the project's first **non-inert** screen — which belongs
to idea 142's widened corpus, not to a verdict on 7 cells.

**Determinism:** the corpus is rebuilt from the committed panels each run and gated against idea
131's committed CSVs at 1e-9; the reproduction check is the determinism check.

Script: `research/backtests/2026-09-05_gross-dispersion-not-gross-level_cloud.py`
Console: `.console.txt` · Corpus: `.grid.csv` · Ladder: `.ladder.csv` ·
Frontier: `.frontier.csv` · IS frontier: `.is_frontier.csv` · Walk-forward: `.walkforward.csv` ·
Rule-8 sensitivity: `.sensitivity.csv`
