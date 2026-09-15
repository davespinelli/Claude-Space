# Idea 890 — is BIT-FOR-BIT reproduction of a committed run POSSIBLE at all on a GROWING panel?
Lane C, 2026-09-15. Script `2026-09-15_is-BIT-FOR-BIT-reproduction-POSSIBLE-on-a-GROWING-panel_C.py`.

**ANSWERED — NO, AND THE BLAME IS MISPLACED. Bit-for-bit is unreachable, but not for the reason
idea 886 gave: growth is the one channel a stamp closes EXACTLY (max |d_return| 0.000e+00 over
570 re-runs). What a date stamp cannot reach is the panel's PAST — 9 of 10 committed
`data/prices.csv` revisions disagree with today's file on 8.9–12.5% of the cells they share,
back to 2008-01-02. That restatement costs a published metric ≤ 0.0001 pp of CAGR, but a
CALENDAR revision inside the same committed history costs 3.84 pp of CAGR and 0.226 of Sharpe at
the SAME end date. PROTOCOL clause PROPOSED, NOT APPLIED (rule 6): stamp the end date AND the
file hash. KILL for capital — nothing promoted; `RULES.md`, `PROTOCOL.md`, `scan.py`, `bot.py`
and `baseline.py` untouched.**

## Setup
2 tuned params, exactly: **P1 run set = 6 books** (`baseline.py` primitives and committed-memo
books only: LIVE `rules_v2_weights` band 0.03 g0.75 W; the same at g1.00; `rules_v1_weights` n=5
W; the 2026-09-04 first-KEEP-4b TOP20 composite-no-vol-scaler monthly at g0.65 and g0.75; SPY
buy-and-hold) × **P2 stamp granularity {DAY, WEEK, MONTH, QUARTER, YEAR}** = **30 cells, all
published** (§4). Reported axes, never selected over: rung date, window, metric. Panel U56,
4,704 rows × 56 cols, 2008-01-02 → 2026-09-14, `sha256(prices.csv)[:16] = f52c545bf9d851b7`,
warm-start 2009-01-13, 10 bps, next-day fills, no shorting or leverage.
**3,947 daily rungs × 6 books = 23,682 metric readings; 570 TRUE re-runs; 10 committed price-file
revisions re-read cell by cell.**

Gates, printed before any hypothesis: **G1** the committed TOP20-g065-M memo triple rebuilt from
`baseline.score` 12.6853% / 1.2012 / −17.1098% vs memo 12.69 / 1.201 / −17.11, max|d| **4.686e-05**
· **G2** LIVE and SPY anchors **4.948e-05** · **G3** truncation ≡ prefix, 12 re-runs
**0.000e+00** · **G4** determinism **0.000e+00** · **G5** 10 committed `prices.csv` revisions,
history un-shallowed to the repo's first commit. **5 of 5 PASS.**

## 1. CHANNEL A (length) is exactly closed by a stamp — and it is the only one that is
Re-running a book on the panel cut at date T reproduces the full run's prefix to **0.000e+00**,
on returns (G3, 12 re-runs) and on all three published metrics (570 true re-runs across 95
rungs × 6 books, max |true − prefix| = **0.000e+00** for CAGR, Sharpe and MaxDD). So every number
below is a measurement, not an approximation, and the daily curve is licensed.

## 2. What ONE added month of panel does to a published number (H_DRIFT **FAIL**)
| per-month |Δ| , month-end rungs | med \|dCAGR\| | p90 \|dCAGR\| | med \|dSharpe\| | med \|dMaxDD\| | med \|dH1\| | med \|dH2\| |
|---|---|---|---|---|---|---|
| pooled, 2011+ (188 months × 6 books) | **0.2084 pp** | 0.65 pp | **0.01909** | **0.0000 pp** | 0.0223 | 0.0469 |
| pooled, last 24 months | 0.0929 pp | 0.26 pp | 0.00810 | 0.0000 pp | 0.0135 | 0.0220 |
| LIVE book, last 24 months | 0.0700 pp | 0.18 pp | 0.00934 | 0.0000 pp | 0.0094 | 0.0240 |

Bars were 0.05 pp / 0.005 / 0.05 pp. **H_DRIFT fails on CAGR and Sharpe by 2–4×** even at today's
panel length: at the live book's current rate a published CAGR moves one 0.1 pp rounding unit in
**about six weeks**, and a Sharpe quoted to three decimals is stale within days.

Two structural readings the record has not published:
- **MaxDD is ONE-DIRECTIONAL.** Share of months it moves up: **0.000 in all six books**, median
  move 0.0000 pp. A published MaxDD can only ever get worse; a stale CAGR or Sharpe is a coin
  toss (up-share 0.468–0.580).
- **H2 moves 2.1× H1** (0.0469 vs 0.0223 per month). Growth lands entirely in the second half,
  and `len(r)//2` then walks the split point, so the H2 leg of every 4a/4b claim is the leg
  that goes stale first — the same asymmetry idea 893 read as a convention property.

## 3. Verdicts are far more stable than the numbers (H_FLIP **PASS**)
| book | 4a flips / 188 | 4b flips / 188 | 4a today | 4b today | months today's verdict has held |
|---|---|---|---|---|---|
| LIVE-v2-g075-W | 0 | 0 | FAIL | FAIL | 188 / 188 |
| v2-g100-W | 0 | 9 | FAIL | **PASS** | 188 / **75** |
| RULESv1-n5-W | 0 | 0 | FAIL | FAIL | 188 / 188 |
| TOP20-g065-M | 0 | 9 | FAIL | **PASS** | 188 / 120 |
| TOP20-g075-M | 0 | 7 | FAIL | **PASS** | 188 / 136 |
| SPY-BH-W | 0 | 0 | FAIL | FAIL | 188 / 188 |

**0 flips in the last 12 months** over 6 books × 2 paths. Every flip is old and every one is on
4b: the last 4b flip is **2020-06-30** (v2-g100-W), **2016-09-30** (TOP20-g065-M) and
**2015-05-29** (TOP20-g075-M) — all when the panel was under 12 years long. 4a never flips for
any book, on any rung. The honest summary: the *numbers* the record publishes are
stale within weeks, the *verdicts* it publishes are not — which is why an unstamped record is
misleading in its decimals and sound in its conclusions.

## 4. P1 × P2, all 30 cells: what a stamp of each granularity leaves open (H_STAMP **FAIL**)
Median (and max) spread of the metric across the trading days sharing one stamp, rungs 2017+:

| grain | buckets | med \|spread\| CAGR | max CAGR | med Sharpe | max Sharpe |
|---|---|---|---|---|---|
| DAY | — | **0.0000 pp** | 0.0000 pp | **0.00000** | 0.00000 |
| WEEK | 506 | 0.064–0.139 pp | 1.57 pp | 0.0069–0.0088 | 0.0932 |
| MONTH | 117 | 0.199–0.405 pp | **3.43 pp** | 0.0203–0.0281 | **0.2271** |
| QUARTER | 39 | 0.400–0.738 pp | 4.30 pp | 0.0383–0.0555 | 0.2843 |
| YEAR | 10 | 0.793–1.514 pp | 4.30 pp | 0.0804–0.0983 | 0.2843 |

Per-book rows are in `.stamp.csv` and the console. **Only DAY granularity is worth writing
down**: a MONTH stamp leaves a median 0.287 pp of CAGR and 0.026 of Sharpe undetermined — larger
than most margins the record's 4b passes are decided by.

## 5. CHANNEL B — the panel's PAST moves, and it costs almost nothing
Every committed revision of `data/prices.csv`, cell by cell against today's file on shared
dates × tickers:

| rev | date | rows | changed cells | share | tickers | max rel | earliest changed date |
|---|---|---|---|---|---|---|---|
| b2528b96f7 | 2026-09-14 | 4,704 | 0 | 0.0000% | 0 | — | — |
| 56e08b10c5 | 2026-09-11 | 4,703 | 22,946 | 8.87% | 48 | 0.095% | 2008-01-02 |
| 60e8c36a52 | 2026-09-10 | 4,702 | 27,980 | 10.82% | 48 | 0.159% | 2008-01-02 |
| 7a93b0753d | 2026-09-09 | 4,701 | 27,792 | 10.75% | 49 | 0.291% | 2008-01-02 |
| 9ee888f453 | 2026-09-08 | 4,700 | 27,649 | 10.70% | 48 | 0.159% | 2008-01-02 |
| f138ee9ae9 | 2026-09-07 | 4,699 | 27,602 | 10.68% | 46 | 0.159% | 2008-01-02 |
| 50585c8670 | 2026-09-04 | 4,699 | 32,403 | 12.54% | 48 | 0.181% | 2008-01-02 |
| c006b43930 | 2026-09-04 | 4,698 | 32,129 | 12.44% | 48 | 4.886% | 2008-01-02 |
| 0ede228245 | 2026-09-03 | 6,060 | 32,329 | 12.51% | 58 | 6.295% | 2008-01-02 |
| fb20817495 | 2026-09-03 | 6,059 | 32,268 | 12.49% | 58 | 8.206% | 2008-01-02 |

**Only 1 of 10 revisions (today's own) leaves every shared cell identical.** `cache_prices.py`
re-downloads the whole history daily with `auto_adjust=True`, so every dividend restates the
level series backwards — 11 days of history is enough to move a tenth of the panel.

**And it is nearly free.** Re-running each revision at its OWN end date (a perfect stamp
assumed) against today's file cut to the same date: median |dCAGR| **0.0000 pp**, max
**0.0001 pp**, max |dSharpe| **0.00002**, max |dMaxDD| 0.0000 pp on the eight same-calendar
revisions. A restated adjusted close rescales a level path and the book reads *returns*; the
rescale cancels everywhere except the ex-dividend bar.

## 6. CHANNEL C — the calendar itself was revised, and that is the expensive one
The two 2026-09-03 revisions carry **6,059–6,060 rows including 1,248 weekend rows** and 58
columns: the pre-2026-09-04 cache kept the crypto tickers and their weekend bars. Re-run at the
SAME end date (2026-09-04):

| revision | book | as committed | cut to today's calendar |
|---|---|---|---|
| 0ede228245 | LIVE-v2-g075-W | **−2.7284 pp CAGR / −0.22256 Sharpe** | +0.0132 pp / +0.00174 |
| 0ede228245 | TOP20-g065-M | **−3.8139 pp / −0.22320** | +0.0101 pp / +0.00087 |
| fb20817495 | TOP20-g065-M | **−3.8408 pp / −0.22586** | −0.0125 pp / −0.00104 |
| fb20817495 | SPY-BH-W | −3.7992 pp / −0.11324 | −0.0429 pp / −0.00203 |

**98.9% of the gap is the calendar convention** (`metrics()` divides by `len(r)/252`, and 1,248
ffilled weekend bars inflate the row count, and so `metrics()`'s year count, by 29%); the **0.043 pp / 0.0021 residual is
CHANNEL B on an older cache — 400× its same-calendar cost.** An end-date stamp is blind to both.
A number published on 2026-09-03 is **not reproducible today at any stamp granularity**, and the
error is two orders of magnitude larger than anything panel growth does in a month.

## 7. RULE 8 — walk-forward, both legs
**Book leg.** IS = warm-start..2016-12-31 (selector sees this only), OOS = 2017-01-01..2026-09-14,
read once. IS-only selector = max IS Sharpe among the 5 non-SPY books → **v2-g100-W**.

| | CAGR | Sharpe | MaxDD | halves |
|---|---|---|---|---|
| pick `u56-band003-gross100-W` OOS | **12.68%** | **1.276** | **−15.91%** | 1.408 / 1.133 |
| RULES v2 (live) OOS | 9.46% | 1.277 | −12.05% | 1.410 / 1.132 |
| SPY OOS | 15.27% | 0.874 | −33.72% | 0.980 / 0.759 |

**PATH 4a FAIL · PATH 4b PASS** — and the book is **already memo'd twice**
(`2026-09-10_MEMO_rules-v2-at-gross-1.00.md`, `2026-09-11_u56-band003-gross100_4b_B_MEMO.md`), so
no new memo is written and nothing is promoted. It is also this run's own best illustration: that
2026-09-11 memo published OOS **12.66% / 1.2740 / −15.91%** and full **11.52% / 1.1996**; the same
book, same code, **four trading days later**, reads OOS **12.6815% / 1.2765** and full
**11.5371% / 1.2011**. Nothing changed but the panel.

**Drift-law leg (H_WF FAIL in levels, PASS in law).** Per-month drift is **2.1–2.8× larger in
sample than out of sample** (ratios 0.36–0.47), so 0 of 6 books land within 2× — spearman across
books +0.7143. But the miss is deterministic, not noise: a metric averaged over T years should
move ~1/T per added month. Fitting log|dCAGR| = a + b·log(panel years) per book gives median
**b = −0.923** against the parameter-free prediction −1 (miss 0.077, R² 0.12–0.20 — the month-to-
month value is noisy, the level is not), and rescaling the IS estimate by (12.87/5.01)^b puts
**6 of 6 books within 2× (ratios 0.79–1.12)** against 0 of 6 in levels. **The drift LEVEL does not
walk forward; the drift LAW does** — which is what makes the clause below pre-registrable.

## 8. The PROTOCOL clause, priced (PROPOSED, NOT APPLIED — rule 6)
Proposed wording: *"Every published metric states the panel's last trading date and the first 16
hex of `sha256` of the price file it was computed from; a number without both is quoted as
irreproducible."*

| channel | what it costs an unstamped number | what a DAY stamp buys | what the hash buys |
|---|---|---|---|
| A length | 0.093 pp CAGR / 0.0081 Sharpe per month at today's T (0.208 pp / 0.019 pooled) | **all of it, exactly (0.000e+00)** | — |
| B restatement | 10.8% of cells at the median revision | **nothing** | detection; cost is ≤0.0001 pp anyway |
| C calendar/universe | **3.84 pp CAGR / 0.226 Sharpe** at the same end date | **nothing** | **detection — the only instrument** |

Cost of the clause: one date and one 16-char hash per published number. Today the record carries
an explicit panel end-date on **4 of 917** committed `.md` files (0.4%) and any file hash on **14**
(1.5%). Not applied here: rule 6 reserves PROTOCOL edits for the Sunday review.

## Verdicts
**H_BIT FAIL · H_DRIFT FAIL · H_FLIP PASS · H_STAMP FAIL · H_WF FAIL in levels, PASS as a law.**
Gates 5/5. **KILL for capital**: no book is promoted, the rule-8 pick passes 4b but is a
twice-memo'd de-grossing rung of the live book, and this run's product is a reporting clause, not
an edge. Runtime 492 s, deterministic.

## Caveats
- The committed `prices.csv` history is **10 revisions over 11 calendar days** (the repo's entire
  history — `git log` un-shallowed to the first commit, G5). CHANNEL B is measured over 11 days,
  not a year; a longer history would find more restated cells, not fewer.
- CHANNEL C is measured on the **one** convention change the record contains (crypto rows removed
  2026-09-04). n = 2 revisions. Its magnitude is a fact about that change, not a general rate.
- The drift law is fitted post-hoc against a parameter-free prediction (b = −1); it is scored on
  the same unchanged rung grid, with no new axis and no new tuning, but it was not pre-declared.
- Panel is U56 only; broad/small panels are untested here.
