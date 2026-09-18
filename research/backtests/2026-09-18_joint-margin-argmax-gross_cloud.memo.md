# KEEP-4b candidate memo for the Sunday review — the JOINT-MARGIN ARGMAX in GROSS
(idea 1290, lane cloud, 2026-09-18. Rule 6 reserves enactment for the Sunday review; nothing is enacted
here. This CONFIRMS the standing U56 / N=20 / g=0.65 candidate by a SECOND, INDEPENDENT chooser and
proposes nothing new for U56; the B136 cell below is filed as PARK, not KEEP.)

1. **What was solved.** With the incumbent's construction frozen (U56, top N = 20 on the 21/252 + 0/126 +
   0/63 composite among names above their 200d MA with vol20 < 0.60, min-hold H = 126, equal weight,
   weekly decide / trade next session, 10 bps), gross was walked 0.20 → 1.00 in 17 rungs on three panels
   and the gross maximising **J = min(4b's DD margin, 4b's CAGR floor margin)** was solved for on each
   window separately. 51 cells published.
2. **Gross is a pure sizing dial: it moves the two binding legs and nothing else.** Sharpe is flat across
   the whole U56 ladder (1.1509 at g = 0.20 → 1.1533 at g = 1.00, range 0.0024) because de-grossing to
   cash scales returns and costs together. Only the MaxDD cap and the CAGR floor move — in opposite
   directions — so J has a genuine interior maximum, and the three Sharpe legs of 4b never bind on it.
3. **The argmax is STABLE in-sample vs out.** U56 g\*(IS) = g\*(OOS) = **0.65**, regret 0.00 pp,
   rho(J_IS, J_OOS) = **1.0000** over the 17 rungs. B136 g\*(IS) = g\*(OOS) = **0.60**, regret 0.00 pp,
   rho **0.9828**. It is the whole J profile that is stable, not just its peak.
4. **The chooser reaches the standing book by a different road.** Choosing gross on warm-up..2016 ONLY by
   argmax J(IS, g) — a chooser that never looks at Sharpe — lands on U56 g = **0.65**, the same cell idea
   1292 reached by highest worst-case IS Sharpe over its 15-point stress ensemble. OOS (2017–2026, read
   once): **14.95% / 1.1833 / −16.73%**; full sample 13.66% / 1.1526 / −16.73%, halves 1.2130 / 1.1129.
   SPY on the same dates: 15.28% CAGR / 0.8745 OOS Sharpe / −33.72% MaxDD. Full 4b **PASS**.
5. **The incumbent gross 0.75 is the worse choice on both panels, by the panel's own arithmetic.** It
   gives up **2.40 pp** of J on U56 (1.10 vs 3.50) and **2.82 pp** on B136 (−0.51 vs 2.31), where it fails
   4b outright. Maximising IS Sharpe instead picks g = 1.00 on all three panels — the highest OOS Sharpe
   available (1.1845) and a full-sample 4b **FAIL** at −24.93% MaxDD. IS Sharpe cannot size a book.
6. **One rung of optimism at the anchor.** J here is read at one phase and one lag (Fri / t+1). Against
   idea 1292's 15-point ensemble at N = 20, the ensemble-worst J peaks at g = 0.65 on U56 (+0.52 pp) —
   the same rung — but at g = **0.55** on B136 (+0.77 pp, 15 of 15 robust) against this run's 0.60. Read
   at a single point, the joint argmax is biased **high** in gross by up to one 0.05 rung.
7. **B136 g = 0.60 is PARK, not KEEP.** It clears 4b on the full sample with OOS 13.04% / 1.0231 /
   −16.84% against SPY 0.8767 — but its H2 Sharpe clears SPY's by only 0.8986 vs 0.8259, it has not
   been run through the phase × delay ensemble, and its
   neighbours straddle it: 1292 found B136/N=20 robust at 15 of 15 at g = 0.55 and at only 5 of 15 at
   g = 0.65. Nothing on B136 should be funded until that cell is stress-run.
8. **SMALL is DEGENERATE and that is the honest headline for it.** On the sub-$2B panel no rung has
   J > 0 on any window — the DD cap and the CAGR floor never clear together — so 4b passes at **0 of 17**
   rungs. The argmax exists arithmetically (0.40 IS, 0.50 OOS) and certifies nothing.
9. **4a is 0 of 51**, as it is everywhere in this family: the live RULES v2 book's −12.05% MaxDD is out of
   reach for any growth book, and RULES v2 still wins OOS Sharpe (1.2778 vs 1.1833) at 9.47% OOS CAGR
   against 14.95%. That trade is the reviewer's decision, not this run's.
10. **Exact RULES wording, if a Sunday review enacted it** (identical to idea 1292's — this run proposes
    no change to it, only a second independent reason to believe the 0.65): *"Each week at the close of
    the last trading session, rank every instrument in the mega-cap/ETF universe that is above its own
    200-day moving average and has 20-day annualised volatility below 0.60, by the equal-weighted average
    of its percentile ranks on (t−21 / t−252), (t / t−126) and (t / t−63) total return. Hold the top 20,
    equally weighted, at 0.65 of NAV with the remainder in cash; a holding is retained for at least 126
    trading days from the session it was bought, and a retained holding keeps its slot. Trade at the next
    session's close."*

**Survivorship (rule 9).** U56 / B136 are current-constituent hand-kept lists and SMALL is a current
sub-$2B screen (tickers with max_1d_move ≥ 1.0 dropped). Delisted, acquired and bankrupt names are absent
from all three, which flatters momentum books and the drawdown leg specifically — so every J here is an
upper bound. The claims above are within-grid differences on fixed panels and identical dates.

Script: `research/backtests/2026-09-18_does-the-4b-MaxDD-CAP-and-CAGR-FLOOR-have-a-JOINT-MARGIN-ARGMAX-in-GROSS_cloud.py`
