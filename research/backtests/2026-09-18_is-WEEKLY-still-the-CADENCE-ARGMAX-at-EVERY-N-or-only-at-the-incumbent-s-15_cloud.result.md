# Idea 1354 (lane cloud, 2026-09-18) — is WEEKLY still the CADENCE ARGMAX at EVERY N, or only at the incumbent's 15?

**ANSWERED: ONLY AT 15. THE CADENCE ARGMAX MOVES WITH N ON 3 OF 3 PANELS, AND W IS THE ARGMAX IN
ONLY 4 OF 12 (panel, N) CELLS. IDEA 1335's "WEEKLY WINS" IS AN N=15 FACT, NOT A CADENCE FACT.**

**AND THE RUN TURNED UP A KEEP-4b CANDIDATE: (N=30, QUARTERLY) at gross 0.60 passes 4b on every
full-sample AND every out-of-sample leg on TWO of three panels, is the rule-8 IS argmax on U56,
carries the LOWEST turnover in the whole grid (1.05/yr), and beats the frozen incumbent's OOS
Sharpe by +0.0645 — but the IS margin that selects it over the incumbent is +0.00031, two orders
of magnitude below the ~7e-3 resolution floor this lane measured today. Memo below; the Sunday
review decides, and the caveats are not decoration.**

Script: `..._is-WEEKLY-still-the-CADENCE-ARGMAX-at-EVERY-N-or-only-at-the-incumbent-s-15_cloud.py`
(offline, deterministic, 17s). All 60 cells in `.grid.csv`, rule 8 in `.walkforward.csv`, both
argmax directions in `.argmax.csv`, gates + tape stamps in `.gates.csv`, console in
`.console.txt`. RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py untouched (rule 6).

## The instrument

Two dials and no more (rule 4): **N {10, 15, 20, 30} x CADENCE {D, W, 2W, M, Q}**, 20 cells per
panel, 60 in all, every one published. Gross is frozen at the incumbent's 0.60 and cost at
PROTOCOL's 10 bps — idea 1335 already showed the cadence ranking is invariant to the cost rung on
all three panels, so re-sweeping it would add a third dial and no information. The book is
otherwise the record's frozen incumbent (3-leg composite, above-200d AND vol20 < 0.60, equal
weight, H=126 min hold, t+1). **Gate G1: the (N=15, W) cell replays idea 1335's committed U56
W/10bps row to < 5e-6 on all eight statistics including turnover — 9 of 9 asserted gates pass.**

## 1. The answer: weekly is an N=15 coordinate

Full-sample Sharpe argmax over the 5 cadences, at each N:

| panel | N=10 | N=15 | N=20 | N=30 | stable? |
|---|---|---|---|---|---|
| U56 | **M** 1.1210 (W 1.1075) | **W** 1.1717 | **W** 1.1532* | **Q** 1.2097 (W 1.1493) | **MOVES** |
| B136 | **M** 1.0793 (W 1.0627) | **M** 1.0950 (W 1.0630) | **M** 1.0793 (W 1.0641) | **W** 1.0894 | **MOVES** |
| SMALL | **M** 0.6076 (W 0.5302) | **W** 0.5570 | **2W** 0.5251 (W 0.5084) | **2W** 0.5021 (W 0.4980) | **MOVES** |

\* U56 N=20 is the run's one near-tie: W 1.153200 against Q 1.151634, a +0.00157 full-sample edge
for W that **reverses out of sample** (Q 1.188840 against W 1.185065). Both margins are below the
~7e-3 resolution floor of §3 caveat 1, so N=20 should be read as "W and Q are indistinguishable",
not as a win for either.

**The argmax moves with N on 3 of 3 panels; W holds it in only 4 of 12 (panel, N) cells.** Out of
sample it is worse for W: W ranks 1 of 5 in only **2 of 12** (panel, N) cells (U56 N=15, B136
N=30). Contrast idea 1335, which found the same argmax perfectly STABLE across the whole
0-50 bps cost ladder on all three panels. **The cadence coordinate is robust to what the tape
charges and fragile to how wide the book is** — so 1335's headline was true and narrower than it
read.

## 2. Which dial binds

Mean within-panel Sharpe spread commanded by each dial (full sample | OOS):

- U56: CADENCE 0.1490 vs N 0.0974 (**1.53x**) | OOS CADENCE 0.1883 vs N 0.1318 (1.43x)
- B136: CADENCE 0.1062 vs N 0.0661 (**1.61x**) | OOS CADENCE 0.1715 vs N 0.1184 (1.45x)
- SMALL: CADENCE 0.2112 vs N 0.1465 (**1.44x**) | OOS CADENCE 0.3501 vs N 0.1663 (2.11x)

Cadence commands 1.4-1.6x the Sharpe spread N does on every panel, in sample and out — and yet
*which* cadence wins is decided by N. The two dials interact; neither is a nuisance parameter for
the other, which is exactly why the record's habit of freezing one and tuning the other produces
coordinates nobody chose.

## 3. The KEEP-4b candidate: (N=30, QUARTERLY), gross 0.60, 10 bps

Three cells beat the frozen (N=15, W) incumbent on full-sample Sharpe *and* pass 4b full+OOS:
U56 N=30/Q (+0.0380), B136 N=30/W (+0.0264), B136 N=20/W (+0.0011). Only the first also wins out
of sample, and **(N=30, Q) is the rule-8 IS argmax on U56.**

| | CAGR | Sharpe | MaxDD | H1 / H2 | turn/yr | OOS CAGR / Sharpe / MaxDD | 4b full | 4b OOS |
|---|---|---|---|---|---|---|---|---|
| **U56 (N=30, Q)** | 12.23% | **1.2097** | -18.21% | 1.2543 / 1.1945 | **1.05** | 13.93% / **1.2610** / -18.21% | PASS 4/4 | PASS |
| U56 incumbent (15, W) | 13.67% | 1.1717 | -16.38% | 1.2527 / 1.1219 | 2.46 | 15.15% / 1.1965 / -16.38% | PASS 4/4 | PASS |
| **B136 (N=30, Q)** | 11.50% | 1.0332 | -18.81% | 1.1426 / 0.9568 | 1.53 | 12.49% / 1.0461 / -18.81% | PASS 4/4 | PASS |
| SMALL (N=30, Q) | 4.66% | 0.4135 | -30.41% | 0.4524 / 0.3896 | 1.88 | 5.03% / 0.4201 / -30.41% | **FAIL 0/4** | FAIL |
| SPY | 15.12% | 0.8844 | -33.72% | 0.9600 / 0.8236 | — | 15.26% / 0.8738 / -33.72% | — | — |
| RULES v2 live @10bps | 9.46%* | 1.2011 | -12.05% | 1.2591* / — | — | 9.46% / 1.2769 / -12.05% | — | — |

\* the live-book row is the U56-panel run of `rules_v2_weights`; see `.grid.csv` for each panel's.

**4b legs on U56, with margins:** H1 1.2543 > SPY 0.9600 ✓; H2 1.1945 > 0.8236 ✓; MaxDD -18.21%
vs the cap 0.60 x -33.72% = **-20.23% (2.02 pp of room)**; CAGR 12.23% vs the floor 0.70 x 15.12%
= **10.59% (1.64 pp of room)**. OOS all four hold (DD -18.21% vs -20.23%, CAGR 13.93% vs 10.68%).
**4a fails** (the live book's MaxDD is -12.05%), as it does for all 60 cells.

**What makes this more than one lucky cell:** the U56 Q ladder is **monotone in N in both
windows** — Sharpe 0.9528 / 1.0292 / 1.1516 / 1.2097 and OOS Sharpe 0.9611 / 1.0110 / 1.1888 /
1.2610 at N = 10 / 15 / 20 / 30 — and (N=30, Q) carries the **lowest turnover in the entire
60-cell grid, 1.05/yr (10.5 bp/yr of drag)**, which by idea 1335's cost-ladder result makes it
the cell least exposed to the cost rung. It passes 4b on 2 of 3 panels. H_HINDSIGHT does **not**
fire on U56: the IS pick *is* the ex-post best OOS cell, which is rare in this record.

**What argues against adopting it now, stated plainly:**
1. **The selection is not decidable.** Its IS Sharpe is 1.148502 against the incumbent's
   1.148194 — a margin of **+0.00031**, roughly 1/23rd of the ~7e-3 half-sample resolution floor
   that idea 1335 measured *today* from a single daily tape rewrite. Rule 8 "chose" it, but the
   in-sample evidence separating it from doing nothing is noise. The gradient in N along Q is the
   real evidence; the argmax is not.
2. **It fails outright on SMALL** (0 of 4 legs, -30.41% MaxDD), so this is a large-cap fact.
3. **It is 1 cell of 60** and the run reports all 60; no multiplicity correction is applied.
4. **It buys Sharpe with 1.44 pp of full-sample CAGR** (12.23% vs the incumbent's 13.67%) and
   1.22 pp out of sample.
5. **Quarterly means 75 rebalance decisions in 18.7 years.** Rebalance PHASE (which day inside
   the quarter an implementer actually trades) is unpriced and is a *larger* dial at Q than at W;
   idea 1253, still in progress, is asking exactly that of the weekly book.

## 4. Rule 8 (the (N, CADENCE) PAIR chosen on warm-up..2016-12-31 by argmax IS Sharpe; 2017-2026 read ONCE)

| panel | IS pick | OOS CAGR / Sharpe / MaxDD | vs frozen (15, W) | d Sharpe | 4b OOS |
|---|---|---|---|---|---|
| U56 | **(30, Q)** | 13.93% / **1.2610** / -18.21% | 15.15% / 1.1965 / -16.38% | **+0.0645** | PASS |
| B136 | (10, W) | 13.48% / 0.9186 / -16.41% | 14.03% / 1.0387 / -15.97% | **-0.1201** | PASS |
| SMALL | (30, M) | 3.89% / 0.3317 / -29.55% | 6.38% / 0.4728 / -32.63% | **-0.1411** | FAIL (Sharpe, DD, CAGR) |

The IS chooser lands on the frozen incumbent on **0 of 3** panels. Choosing the pair is worth a
mean **-0.0656 of OOS Sharpe** (min -0.1411, max +0.0645) and -1.42 pp of OOS CAGR, and beats the
incumbent on **1 of 3** panels. 4b on every OOS leg after rule 8: **2 of 3**. H_HINDSIGHT fires
on 2 of 3 panels (B136's ex-post best is (15, M) at 1.1196; SMALL's is (10, 2W) at 0.6810).

## 5. KEEP-path census over all 60 cells

**4a 0 of 60.** **4b 22 of 60 full-sample and 22 of 60 full AND OOS** (U56 16/20, B136 6/20,
SMALL 0/20). By N: 4/15, 6/15, 7/15, 5/15 at N = 10/15/20/30. By cadence: D 2/12, W 8/12,
2W 2/12, M 4/12, **Q 6/12** — W still passes 4b most often even where it is not the argmax,
because the cells that out-Sharpe it mostly do so by taking drawdown.

---

# MEMO FOR THE SUNDAY REVIEW — candidate RULES change (path 4b), 10 lines

1. **Candidate.** Replace the incumbent's width and cadence only: **N = 30 names and a QUARTERLY
   rebalance**, everything else in RULES v2 unchanged (gross 0.60, above-200d + vol20 < 0.60
   eligibility, 126-day minimum hold, equal weight, t+1, 10 bps).
2. **Exact RULES wording, if adopted:** *"Hold the top 30 eligible instruments by the composite
   score at gross/30 of NAV each. Eligible = priced, above its 200-day moving average, and
   20-day annualised volatility below 0.60. Rebalance on the last trading day of each calendar
   QUARTER, applying targets at the next close; a name once held is not sold for 126 trading days
   unless it leaves the eligible set. Gated-out weight goes to CASH, never re-spread."*
3. **KEEP path: 4b.** U56 full sample 12.23% / 1.2097 / -18.21%, halves 1.2543 / 1.1945; all four
   legs pass with 2.02 pp of drawdown room and 1.64 pp of CAGR room against SPY's 15.12% / 0.8844
   / -33.72%.
4. **Rule 8 (2017-2026 read once).** OOS 13.93% / **1.2610** / -18.21% against the frozen
   incumbent's 15.15% / 1.1965 / -16.38% and SPY's 15.26% / 0.8738 / -33.72%: **+0.0645 of OOS
   Sharpe for -1.22 pp of OOS CAGR**, and it is the rule-8 IS argmax on U56.
5. **It replicates on a second panel.** B136 11.50% / 1.0332 / -18.81%, OOS 12.49% / 1.0461 /
   -18.81%, 4b passing on all four legs full sample and out of sample.
6. **It is the cheapest book in the grid.** Turnover 1.05/yr against the incumbent's 2.46, i.e.
   10.5 bp/yr of drag — by idea 1335's cost ladder, the cell least sensitive to the cost rung.
7. **It is not an isolated cell.** The Q ladder rises monotonically in N in both windows
   (Sharpe 0.9528 -> 1.2097; OOS 0.9611 -> 1.2610 at N = 10 -> 30).
8. **DO NOT ADOPT ON THE SELECTION.** Its IS Sharpe beats the incumbent's by **+0.00031**, about
   1/23rd of the ~7e-3 half-sample resolution floor idea 1335 measured today from one daily tape
   rewrite; rule 8's argmax here is a coin flip and the N-gradient is the only real evidence.
9. **Known failures and unpriced dials.** 0 of 4 legs on SMALL (-30.41% MaxDD); 4a fails on all
   60 cells; **rebalance PHASE inside the quarter is unpriced** and matters more at Q than at W
   (idea 1253 is asking it of the weekly book); 1 cell of 60 with no multiplicity correction.
10. **Recommendation.** **PARK for capital, do not swap the live book this Sunday.** Price the
    quarterly phase dial (all 63 offsets) and re-confirm on a second tape vintage first; if both
    hold, this is the strongest 4b candidate the record has, because it buys Sharpe with LESS
    trading rather than more risk.

## Survivorship (rule 9)

U56 / B136 / SMALL are CURRENT-constituent lists. SMALL is a sub-$2B screen carried back to 2010
with the protocol-mandated 52 `max_1d_move >= 1.0` tickers dropped (663 of 715 priced names kept),
so its levels are an upper bound — and it fails 4b on all 20 cells anyway. A current-constituent
large-cap list flatters a wide momentum book, so the (N=30, Q) candidate's own CAGR is the number
the bias inflates most; its *drawdown* margin, which is what the memo leans on, is the less
affected leg.

## Tape stamp (the caveat idea 1335 measured, idea 1350 filed to chase)

U56 4708 rows 2008-01-02..2026-09-18; B136 4708 rows 2008-01-02..2026-09-18; SMALL 4203 rows
2010-01-04..2026-09-18. Published, not asserted — every number above is on this vintage of
`data/prices*.csv` and on no other.
