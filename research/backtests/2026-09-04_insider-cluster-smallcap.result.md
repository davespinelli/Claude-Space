# Idea 50 — insider cluster buying on the SMALL-CAP panel (rerun of idea 32) — 2026-09-04

Script: `research/backtests/2026-09-04_insider-cluster-smallcap.py` ·
console: `2026-09-04_insider-cluster-smallcap.console.txt` ·
insider cache: `data/form4_purchases_small.csv` (19,566 qualifying purchases, 398 tickers,
3,119 owners, 2012-01-03 → 2026-03-30).
Prices: `baseline.load_universe(small=True, with_spy=True)` → 484 columns, 44 dropped for
`small_meta.csv max_1d_move ≥ 1.0`, **439 tradable small caps** + SPY as benchmark only.
Trading-day index verified in-script (0 weekend rows, 250–253 rows/yr).
Sample **2012-01-01 → 2026-09-03**, weekly rebalance, 10 bps per unit turnover, next-day
execution. Fully offline and deterministic (both the panel and the SEC zips are cached).

## Verdict

**KILL — all 8 arms, both KEEP paths.** Idea 32 was PARK on mega caps because its edge was real
but its 4–8 name book drew down −39.7%. This run made the two changes its memo asked for — a
439-name small-cap panel and CMP's routine/opportunistic split. **The book-size problem is
fixed and the result got worse.**

- **4a (beat the book): FAIL, all 8.** Sharpe beats RULES v1 in both halves everywhere
  (e.g. 1.09 / 0.70 vs 0.60 / 0.54), but MaxDD −48.7% against RULES v1's −32.8%.
- **4b (capital-worthy): FAIL, all 8, on three tests of five.** Best arm (OPP, 6m, EW):
  H2 Sharpe **0.702 < SPY 0.855**, OOS Sharpe **0.770 < SPY 0.937**, MaxDD **−48.7% vs a
  −20.2% cap**. Only the CAGR floor is cleared (19.2% vs 10.6%).
- Not a PARK: unlike idea 32, the Sharpe tests themselves fail. There is no "sizing would fix
  this" story left.

## LEADERBOARD rows

| Date | Idea | CAGR | Sharpe | MaxDD | Sharpe H1 / H2 | Baseline Sharpe (H1/H2) | Verdict | Script |
|---|---|---|---|---|---|---|---|---|
| 2026-09-04 | 50 insider-cluster ALL hold=6m EW100% | 18.8% | 0.83 | -49.4% | 1.08 / 0.69 | 0.57 (0.60/0.54) | KILL | research/backtests/2026-09-04_insider-cluster-smallcap.py |
| 2026-09-04 | 50 insider-cluster ALL hold=6m cap5% | 18.0% | 0.80 | -49.4% | 1.03 / 0.69 | 0.57 (0.60/0.54) | KILL | research/backtests/2026-09-04_insider-cluster-smallcap.py |
| 2026-09-04 | 50 insider-cluster ALL hold=12m EW100% | 16.0% | 0.75 | -49.1% | 0.96 / 0.63 | 0.57 (0.60/0.54) | KILL | research/backtests/2026-09-04_insider-cluster-smallcap.py |
| 2026-09-04 | 50 insider-cluster ALL hold=12m cap5% | 15.2% | 0.72 | -49.1% | 0.91 / 0.63 | 0.57 (0.60/0.54) | KILL | research/backtests/2026-09-04_insider-cluster-smallcap.py |
| 2026-09-04 | 50 insider-cluster OPP hold=6m EW100% | 19.2% | 0.84 | -48.7% | 1.09 / 0.70 | 0.57 (0.60/0.54) | KILL | research/backtests/2026-09-04_insider-cluster-smallcap.py |
| 2026-09-04 | 50 insider-cluster OPP hold=6m cap5% | 18.3% | 0.82 | -48.7% | 1.04 / 0.70 | 0.57 (0.60/0.54) | KILL | research/backtests/2026-09-04_insider-cluster-smallcap.py |
| 2026-09-04 | 50 insider-cluster OPP hold=12m EW100% | 16.1% | 0.75 | -49.1% | 0.96 / 0.63 | 0.57 (0.60/0.54) | KILL | research/backtests/2026-09-04_insider-cluster-smallcap.py |
| 2026-09-04 | 50 insider-cluster OPP hold=12m cap5% | 15.3% | 0.72 | -49.1% | 0.91 / 0.63 | 0.57 (0.60/0.54) | KILL | research/backtests/2026-09-04_insider-cluster-smallcap.py |
| 2026-09-04 | 50 RULES v1 on the small panel, 2012+ - reference | 7.6% | 0.57 | -32.8% | 0.60 / 0.54 | 0.57 (0.60/0.54) | - | research/backtests/2026-09-04_insider-cluster-smallcap.py |
| 2026-09-04 | 50 SPY buy & hold, 2012+ - reference | 15.2% | 0.94 | -33.7% | 1.12 / 0.85 | 0.57 (0.60/0.54) | - | research/backtests/2026-09-04_insider-cluster-smallcap.py |
| 2026-09-04 | 50 EW all 439 small caps, 2012+ - CONTROL | 14.3% | 0.74 | -46.0% | 0.99 / 0.63 | 0.57 (0.60/0.54) | - | research/backtests/2026-09-04_insider-cluster-smallcap.py |

Supporting risk figures, same sample:

| | Vol | Sortino | Calmar |
|---|---|---|---|
| ALL 6m EW100% | 24.4% | 1.18 | 0.38 |
| OPP 6m EW100% | 24.4% | 1.20 | 0.39 |
| ALL 12m EW100% | 23.7% | 1.05 | 0.33 |
| OPP 12m EW100% | 23.7% | 1.05 | 0.33 |
| RULES v1 (small panel) | 14.8% | 0.76 | 0.23 |
| SPY | 16.5% | 1.16 | 0.45 |
| EW all 439 small caps (control) | 21.1% | 1.01 | 0.31 |

## The control is the result

The 439-name panel makes possible the one test idea 32's 4–8 name book could not run: **does
picking the cluster names beat owning the whole panel?** Equal-weighting every tradable small
cap, weekly, same costs, no insider input at all:

| arm | ΔCAGR vs control | ΔSharpe vs control | daily excess t | corr with control |
|---|---|---|---|---|
| ALL 6m EW100% | +4.51% | +0.089 | +2.04 | 0.938 |
| OPP 6m EW100% | **+4.86%** | **+0.102** | **+2.16** | 0.937 |
| OPP 6m cap5% | +4.01% | +0.078 | +1.85 | 0.937 |
| ALL 12m EW100% | +1.70% | +0.008 | +1.18 | 0.962 |
| OPP 12m EW100% | +1.76% | +0.010 | +1.20 | 0.962 |
| OPP 12m cap5% | +0.97% | −0.015 | +0.80 | 0.962 |

At 12 months there is **nothing**: ΔSharpe +0.01, t +1.2, and the 5%-cap version is negative.
At 6 months there is a small, real-looking increment — +4.9pp/yr, t +2.16 — but it comes with
a correlation of 0.94 to simply holding the panel and a −48.7% drawdown. **Roughly 94% of this
book is small-cap beta on a survivorship-flattered panel.** The control itself returns 14.3% at
Sharpe 0.74 and −46.0%, which is most of the way to the strategy's numbers.

## Book size — the fix worked, and it did not help

| arm | avg gross | avg names | median | max | days ≤5 names | days in cash | turnover/yr |
|---|---|---|---|---|---|---|---|
| ALL 6m EW100% | 99.9% | **42.9** | 44 | 80 | 0.9% | 0.1% | 6.4× |
| ALL 12m EW100% | 99.9% | **70.6** | 74 | 113 | 0.9% | 0.1% | 4.4× |
| ALL 6m cap5% | 98.5% | 42.9 | 44 | 80 | 0.9% | 0.1% | 6.0× |
| ALL 12m cap5% | 98.7% | 70.6 | 74 | 113 | 0.9% | 0.1% | 4.1× |
| *(idea 32, mega caps)* | *99.1% / 99.4%* | *4.4 / 7.9* | *4 / 7* | — | *28.5% / 2.4%* | *0.9% / 0.6%* | *6.9× / 4.2×* |

Idea 32's book held 4.4 names at 6m and spent 28.5% of days holding ≤2. This one holds 42.9 and
spends 0.9% of days at ≤5. **Breadth went up roughly 10×; Sharpe went DOWN from 1.27 to 0.84
and MaxDD got 9pp WORSE.** That is the whole finding: idea 32's mega-cap Sharpe was not a
diversifiable concentration penalty waiting to be lifted.

The **5% cap is therefore inert**, which is itself informative: with 43 names the natural weight
is already 2.3%, so the cap only binds when fewer than 20 names are held — essentially 2012
alone (that year drops +15.4% → +4.4% purely from sitting in cash). Average gross falls from
99.9% to 98.5% and Sharpe from 0.83 to 0.80. There is no concentration left for a cap to fix.

**6m now beats 12m**, the reverse of idea 32 — which confirms that memo's point 4: on mega caps
the longer hold won by manufacturing breadth, not because insider signal decays slowly. Given
ample breadth, the fresher signal wins (0.84 vs 0.75).

## Routine vs opportunistic (Cohen–Malloy–Pomorski) — no effect, and here is why

Routine = the same (firm, insider) also bought in the same calendar month in each of the three
prior years; those purchases are dropped in the OPP arm.

| | ALL | OPP | Δ |
|---|---|---|---|
| purchases | 19,566 | 17,815 | −1,751 (8.9%) |
| cluster signal-days | 3,258 | 3,151 | −107 (3.3%) |
| distinct tickers | 335 | 335 | 0 |
| 6m EW Sharpe | 0.829 | 0.841 | **+0.012** |
| 12m EW Sharpe | 0.747 | 0.749 | **+0.002** |

The split is directionally right (CMP predicts it) and economically nil. Two reasons, both
data-side rather than economic:

1. **Only 8.9% of purchases are routine**, and they remove just 3.3% of cluster-days — a cluster
   needs 2 insiders, and dropping one routine leg usually leaves the cluster standing on others.
2. **1,662 of the 1,751 routine flags (95%) are a single ticker, OPK**, and 23 owners in total
   carry every flag. This is not a test of CMP's mechanism; it is a test of whether excluding
   Phillip Frost's metronomic OPK buying matters. It does not.

Routine flags are also **structurally impossible before 2015** (three prior years of purchase
history are needed and the sample starts in 2012), so 2012–2014 is unfiltered by construction.

Deviation from CMP, stated rather than absorbed: CMP classify on an insider's whole trade record
(buys *and* sells); the extract here keeps only code-P purchases, so this is the purchase-only
version the idea brief specifies. A faithful replication needs the sell side too.

## Cluster counts per year

Cluster = ≥2 distinct reporting owners with qualifying open-market purchases (Form 4,
non-derivative table, code P, acquired, shares × price ≥ $10,000) whose **transaction** dates
fall inside a 30-calendar-day window. Signal date = the later of the two **filing** dates, so
nothing is used before it is public (median filing lag 1 day, p90 4 days).

| Year | Purchases | Clusters (ALL) | Tickers | Clusters (OPP) | Tickers |
|---|---|---|---|---|---|
| 2012 | 1,699 | 177 | 43 | 177 | 43 |
| 2013 | 1,397 | 108 | 36 | 108 | 36 |
| 2014 | 1,885 | 183 | 52 | 183 | 52 |
| 2015 | 1,613 | 210 | 65 | 181 | 64 |
| 2016 | 1,390 | 167 | 66 | 154 | 66 |
| 2017 | 1,254 | 217 | 62 | 165 | 62 |
| 2018 | 1,279 | 283 | 89 | 280 | 89 |
| 2019 | 1,202 | 278 | 88 | 277 | 88 |
| 2020 | 1,358 | 307 | 96 | 306 | 95 |
| 2021 | 855 | 166 | 80 | 166 | 80 |
| 2022 | 1,855 | 295 | 89 | 294 | 89 |
| 2023 | 1,080 | 275 | 77 | 273 | 76 |
| 2024 | 1,170 | 262 | 89 | 258 | 89 |
| 2025 | 1,274 | 288 | 96 | 287 | 96 |
| 2026 (to Mar 30) | 255 | 42 | 20 | 42 | 20 |
| **Total** | **19,566** | **3,258** | **335 distinct** | **3,151** | **335** |

Cluster size: 1,700 two-insider, 720 three, 401 four, 437 five-or-more (max 16). **Average book
size 42.9 names (6m) / 70.6 (12m)** — the 20–60 range the idea brief predicted.

Small caps produce **15× the cluster-days of the mega-cap panel** (3,258 vs 215) on 335 names
vs 57 — the density prediction was right. The counter-cyclicality idea 32 found is much weaker
here: 2021 is the lightest year (166) and 2020 the heaviest (307), but the range is 108–307
rather than 5–28.

**Signal concentration:** OPK alone is 30.6% of all qualifying purchases (5,989 rows, 15 owners)
and 11.4% of all cluster signal-days; the top-5 names are 18.2% of cluster-days. Excluding OPK
entirely moves nothing (6m EW 18.8% → 18.9%, Sharpe 0.83 → 0.83), so it is not driving returns —
but any reading of "3,258 clusters" as 3,258 independent observations is wrong.

## Walk-forward (PROTOCOL rule 8)

`hold` chosen on **2012–2018** only, evaluated untouched on **2019–2026**. The split is shifted
from the protocol's 2009–2016 / 2017–2026 because SEC structured Form 4 coverage begins in 2012.
Selection rule fixed before looking at the OOS column: highest in-sample Sharpe, ties to 6m.

| | IS Sharpe | IS CAGR | OOS Sharpe | OOS CAGR | OOS MaxDD |
|---|---|---|---|---|---|
| ALL 6m EW100% *(IS pick)* | 0.983 | 18.6% | 0.757 | 19.0% | −49.4% |
| ALL 12m EW100% | 0.851 | 15.1% | 0.706 | 16.9% | −49.1% |
| **OPP 6m EW100%** *(IS pick)* | **0.995** | **18.9%** | **0.770** | **19.5%** | **−48.7%** |
| OPP 6m cap5% *(IS pick)* | 0.937 | 17.1% | 0.771 | 19.5% | −48.7% |
| OPP 12m EW100% | 0.851 | 15.1% | 0.709 | 17.0% | −49.1% |
| RULES v1 (small panel) | 0.584 | 7.3% | 0.556 | 7.8% | −32.8% |
| SPY | 0.990 | 12.6% | **0.937** | 17.6% | −33.7% |
| EW all 439 small caps (control) | 0.886 | 13.3% | 0.690 | 15.3% | −45.3% |

The in-sample pick (6m, in every family) is also the better arm out of sample, so this is not an
in-sample artefact — but **every arm's OOS Sharpe is below SPY's 0.937**, and the best arm beats
the do-nothing panel control by 0.08 out of sample. Drawdown is stable in and out of sample
(−48.7% vs −48.7%): structural, not a one-off.

## Calendar-year returns

| Year | ALL 6m EW | OPP 6m EW | OPP 12m EW | RULES v1 | SPY | EW panel |
|---|---|---|---|---|---|---|
| 2012 | +15.4% | +15.4% | +14.2% | +8.1% | +16.0% | +18.7% |
| 2013 | +77.3% | +77.3% | +71.8% | +26.6% | +32.3% | +53.0% |
| 2014 | +3.3% | +3.3% | +7.3% | +9.0% | +13.5% | +3.5% |
| 2015 | −15.9% | −16.0% | −16.4% | −12.6% | +1.2% | −9.6% |
| 2016 | +47.9% | +47.4% | +33.8% | +7.1% | +12.0% | +30.7% |
| 2017 | +14.9% | +16.2% | +8.9% | +18.3% | +21.7% | +12.3% |
| 2018 | +8.9% | +10.0% | +3.9% | −0.7% | −4.6% | −4.3% |
| 2019 | +30.1% | +30.1% | +30.6% | +9.0% | +31.2% | +21.5% |
| 2020 | +44.4% | +46.8% | +47.8% | +16.3% | +18.3% | +41.0% |
| 2021 | +12.5% | +12.5% | +16.5% | +30.7% | +28.7% | +25.9% |
| 2022 | −12.7% | −12.7% | −20.3% | −13.2% | −18.2% | −18.9% |
| 2023 | +26.7% | +27.9% | +29.4% | −0.6% | +26.2% | +17.2% |
| 2024 | +14.4% | +14.4% | +10.5% | −5.9% | +24.9% | +11.9% |
| 2025 | +20.4% | +20.3% | +9.7% | +10.8% | +17.7% | +8.7% |
| 2026 (to Sep 3) | +17.8% | +17.8% | +18.4% | +19.0% | +14.0% | +19.1% |

2013 (+77.3% against the panel's +53.0%) and 2016 (+47.9% vs +30.7%) carry a large share of the
full-sample excess; the second half is much flatter against the panel control, which is what the
H2 Sharpe of 0.70 is reporting. The 2022 defensiveness idea 32 flagged does not replicate:
−12.7% here against the panel's −18.9%, a 6pp cushion rather than a positive year.

## Robustness

**Drop the single largest gross contributor** (diagnostic, not a variant):

| arm | dropped | CAGR | Sharpe | MaxDD | halves | (from) |
|---|---|---|---|---|---|---|
| ALL 6m EW | NVAX | 18.2% | 0.81 | −49.4% | 1.03 / 0.69 | 18.8% / 0.83 |
| OPP 6m EW | NVAX | 18.6% | 0.82 | −48.7% | 1.05 / 0.70 | 19.2% / 0.84 |
| ALL 12m EW | CODI | 15.8% | 0.74 | −49.0% | 0.93 / 0.63 | 16.0% / 0.75 |
| OPP 12m EW | CODI | 15.9% | 0.74 | −49.0% | 0.93 / 0.64 | 16.1% / 0.75 |

Top-3 contributors (6m): NVAX +0.11, CODI +0.10, CTEV +0.10 out of a much larger total — far
better spread than idea 32's 4-name book, as expected at 43 names. **The result is not one
ticker; it is the panel.**

**Excluding OPK** (11.4% of cluster-days): 6m EW 18.9% / 0.83 / −50.2%, halves 1.09 / 0.68.
No material change on any arm.

## Data provenance, and what is missing

- **2012-01-01 → 2026-03-31** comes from the SEC's own quarterly Form 345 structured data sets,
  already cached in `data/sec_cache/form345/` — 57 zips covering **all filers**, read with the
  same loader as `2026-09-04_insider-cluster-buying.py`. 30,428 raw purchase rows across the
  439-name panel before the $10k / duplicate filters, 19,566 after. **No network calls; the run
  is fully offline and reproducible.**
- **DATA GAP: 2026-04-01 → 2026-09-03 (5 months) carries no new insider signal.** That quarter
  is not published as a data set yet. The submissions-JSON path is implemented
  (`--crawl-q2`) and was started: it enumerated **6,617 Form 4s / 6,223 after the
  ≥2-per-ticker-month pre-filter** across the 439 tickers, but SEC served it at ~0.7 files/s
  rather than the 7/s throttle, projecting ~2 hours, so it was stopped and the gap is stated
  here instead — the idea brief's second option. Impact is bounded: 6m/12m holds mean positions
  opened from the 42 Q1-2026 clusters still run through the gap (the book is not in cash; 2026
  returns +17.8%), only *new* entries after Mar 30 are absent, and 5 months at the tail of a
  14.7-year sample cannot move a verdict that fails by 0.17 of Sharpe and 28pp of drawdown.
  Anyone re-running for completeness: `--build --crawl-q2 --xml-cap 7000`.
- **Hygiene, not tuning:** 10 rows of 19,576 had `filing_date < trans_date` (a Form 4 filed
  before the trade it reports — an SEC data error) and are dropped. 312 rows have a filing lag
  over 60 days; they are kept, since the signal date is the *filing* date and a late report is
  simply a late-arriving signal, not look-ahead.
- **SURVIVORSHIP — first-order here, not boilerplate.** `data/prices_small.csv.gz` is the
  *current* constituent list of a sub-$2B screen (see `data/SMALL_PANEL_README.md`): every name
  survived to 2026 as a listed, still-sub-$2B company. Insider clusters concentrate in
  *distressed* small caps — exactly the population that gets delisted, acquired or wiped out —
  so this bias runs directly against the signal being tested. The EW-panel control at
  14.3%/yr is itself a flattered number, and the strategy's 19.2% inherits all of it. **The
  KILL is safe against the bias; nothing in this file's absolute returns is achievable.**
- 44 names dropped for `max_1d_move ≥ 1.0` (AMPY, HCWC, DEC, …) per the panel README.

## Memo

1. **Verdict: KILL, all 8 arms, both KEEP paths.** 4a fails on drawdown alone (−48.7% vs RULES
   v1's −32.8%); 4b fails on H2 Sharpe (0.70 vs 0.85), OOS Sharpe (0.77 vs 0.94) *and* drawdown
   (−48.7% vs a −20.2% cap). This closes idea 32 as well: its PARK does not port.
2. **The breadth fix worked and disproved its own premise.** Book size went from idea 32's 4.4
   names to 42.9 (6m) and 70.6 (12m), days-at-≤5-names from 28.5% to 0.9% — and Sharpe fell
   1.27 → 0.84 while drawdown deepened 9pp. Idea 32's mega-cap Sharpe was a small-N artefact,
   not a concentration penalty waiting to be lifted.
3. **Against the honest control the edge is ~nothing at 12m and thin at 6m.** Equal-weighting
   all 439 names with no insider input gives 14.3%/0.74/−46.0%. The best arm adds +4.9pp CAGR
   and +0.10 Sharpe at daily excess t +2.16, correlation 0.94; the 12m arms add +0.01 Sharpe at
   t +1.2. Idea 32 could never run this test with a 4-name book — **it is the single most
   informative number in this file.**
4. **CMP's routine/opportunistic split is not testable on this data and adds +0.01 Sharpe.**
   Only 8.9% of purchases are routine, they remove 3.3% of cluster-days, and 95% of the flags
   are one ticker (OPK). Nothing before 2015 can be flagged at all. A real test needs the sell
   side of the Form 4 record and a longer pre-sample.
5. **The 5% cap is inert, which answers the concentration question directly.** Average gross
   98.5% vs 99.9%, Sharpe −0.02. At 43 names the natural weight is 2.3%; the cap binds only in
   2012. The −49% drawdown is not concentration, it is **small-cap beta in 2015 and 2022** — no
   position-sizing rule reaches it.
6. **6m beats 12m here, the reverse of idea 32, and that confirms idea 32's memo point 4.** The
   longer hold won on mega caps by manufacturing breadth; given ample breadth the fresher signal
   wins (0.84 vs 0.75). Do not read either result as evidence about insider signal decay.
7. **Small caps do deliver the predicted signal density**: 3,258 cluster-days on 335 names vs
   215 on 57 — 15× more. Density was never the binding constraint; **return per cluster is.**
8. **Signal counts are less independent than they look.** OPK is 30.6% of qualifying purchases
   and 11.4% of cluster-days from 15 owners; the top-5 names are 18.2% of cluster-days. Removing
   OPK changes nothing (0.83 → 0.83), so returns are not driven by it, but any t-statistic
   treating 3,258 clusters as independent is overstated.
9. **Survivorship runs against the signal, so the KILL is robust to it.** The panel holds only
   sub-$2B names still listed today; insider clusters concentrate in distressed names, which is
   exactly what the panel is missing. A true panel would make these numbers worse, not better —
   the one direction that cannot rescue the verdict.
10. **Nothing here is worth queueing as a follow-up.** The natural next tweaks — a value or
    trend overlay on cluster names, a purchase-size threshold, a sleeve capped at 20–30% — would
    each be tuning against a signal whose honest increment over "own the panel" is +0.01 to
    +0.10 of Sharpe with a −49% drawdown. **Recommend the Sunday review record insider cluster
    buying as closed on both panels** and not spend a further slot on it. The remaining reusable
    asset is `data/form4_purchases_small.csv` — 19,566 dated, priced, owner-attributed
    open-market purchases on the small-cap panel — which is a genuinely useful input for other
    ideas even though this one fails.

_Research, not investment advice. Past performance is not indicative of future results._
