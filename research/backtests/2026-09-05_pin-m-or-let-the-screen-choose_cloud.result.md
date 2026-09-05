# Idea 146 — pin-m-or-let-the-screen-choose · ANSWERED: PIN m in rule 8

**Question (pre-registered).** Idea 144 found rule 8's FAMILY screen is the first non-inert screen
the project has (7 of 18 picks moved, against 0 for POINT-4b) and yet buys no Sharpe: +1.1 pp OOS
CAGR for −1.7 pp of extra drawdown, −0.003 Sharpe. Before any convention lets a screen choose
gross, price that trade on idea 74's axis against the 200d gate and de-grossing, at matched book
and cost, and say whether m should be pinned at the published gross.

**Run.** Idea 94's simulator and idea 144's cell builder are imported, not re-implemented:
3 panels × 3 books × 17 arms × 2 cost rungs = 306 books, each over a 25-point gross family
m ∈ {0.10 … 1.30} = **7,650 runs**. Two tuned parameters, both swept and reported: the m-rule
{point, pin, hi, lo} and the ceiling m_max ∈ {1.00, 1.30}. 4b bars stay at the published
φ = 0.70, δ = 0.60. IS ≤ 2016-12-31 chosen on; OOS ≥ 2017-01-01 read once.

**Reproduction, before anything new was read.** (a) `H.run` vs `engine.backtest` max|diff| = **0.0**;
(b) idea 94's published EWall+vol60-dg u56@10 bps row 11.587% / 1.133 / −16.884%; (c) **0 of 54**
differing S0/S1/S3 picks against idea 144's committed picks file; (d) its paired aggregates exact
(S1 0.127 / 1.022 / −0.211, S3 0.138 / 1.019 / −0.228).

## Answer

1. **The FAMILY screen is not a screen.** In **7 of 7** entering cells it keeps the arm the pinned
   screen picks and moves only m. Its exchange rate is therefore the gross ladder's own local slope
   *by identity*, and the matched-DD control against that same arm is trivially zero — stated here
   rather than presented as a coincidence. Splitting the screen confirms it: PIN (family
   admissibility, m forced to 1.00) equals the incumbent POINT screen in 6 of 7 arms and by 0.001
   Sharpe in the seventh.
2. **On idea 74's axis the trade looks decent and is still not worth taking.** Realised median rate
   **0.668** pp CAGR per pp of |MaxDD| given up; it beats the fitted OOS ladder slope in 7/7 (it
   moves at the steep top of the ladder) and the 200d gate's price (median 0.448) in 7/7. But it
   beats the **IS** ladder slope in **0 of 7** — ex ante the same move was priced at a median
   1.082 pp/pp, 1.6× what it delivered — and it buys **−0.003** Sharpe, improving **0 of 7** cells.
3. **What it costs is exactly what 4b rations.** Going pin → hi at m_max = 1.30 turns **2 of the 3**
   pinned 4b passes into failures (broad/EWall@10 and u56/EWall@10; broad/EWall@25 survives) for
   OOS Sharpe changes between −0.015 and 0.000.
4. **Its m is an artifact of the IS window, not a property of the book.** Within a scale-free arm's
   own family the IS Sharpe range is 0.002–0.004 over all 25 gross points, so the selector's own
   statistic cannot order m at all — the IS *drawdown cap* decides it. And that cap is too loose:
   the IS-admissible m exceeds the OOS-admissible m in **4 of 5** comparable cells (mean +0.100 of
   gross), while in the two broad/TOP20 cells the IS window admits 8–11 gross points where the OOS
   window admits **zero**.
5. **The other direction is no better as a rule.** FAM-lo (min admissible m) gains +0.007 Sharpe and
   3.0 pp of shallower drawdown but gives up 1.9 pp of CAGR. Hi and lo are a coin flip on Sharpe
   and a large, unmandated risk decision on CAGR/drawdown — which is the argument for pinning
   rather than for choosing a direction.

**Verdict: ANSWERED — m should be PINNED at the published gross in rule 8.** Idea 144's family
convention survives for *reporting* (a rescaled book is the same book) and is barred only from
*selection*. Proposed rule-8 wording is in `...memo.md`, for the Sunday review. No RULES change,
no new book, no KEEP candidate.

**Caveats.** Only 7 of 18 cells enter any 4b screen, so the conclusion rests on 7 paired cells and
the small panel contributes none. Survivorship (all three panels are current-constituent lists;
the sub-$2B panel additionally drops `max_1d_move ≥ 1.0` tickers per idea 118) flatters high gross,
i.e. the side this run rules out, so the finding is if anything understated. Idea 144 Q1's warning
carries: the two `ebud` arms are not pure exposure rescales, and they are flagged in the price
table (`fam_scale_free = False`). Idea 38 (calendar-day index on u56/broad) and idea 126 (t+1 only)
carry over. Q3's matched-DD control is hindsight and is labelled as such wherever it appears.
