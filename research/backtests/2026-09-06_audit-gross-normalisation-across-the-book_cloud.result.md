# idea 81 — audit-gross-normalisation-across-the-book (cloud, 2026-09-06)

**Verdict: ANSWERED / CONFIRMED and MUCH larger than idea 73 suggested — 16 of the 21 `GROSS/n`
4b passes in this run's own grid do not survive gross-normalisation.**

Script: `research/backtests/2026-09-06_audit-gross-normalisation-across-the-book_cloud.py`
Artefacts: `.console.txt`, `.grid.csv` (588 rows), `.gross.csv`, `.flips.csv`, `.walkforward.csv`

## What was run

Three weightings of **the same names on the same days**:

* **LIT** `w = (rank <= n) * GROSS/n` — the published construction. Realised gross is
  `GROSS * k_t / n` where `k_t <= n` is the number of names the 200d/vol20 gate leaves eligible.
* **NORM** `w = (rank <= n) / k_t * GROSS` — always fully invested; the channel is closed.
* **MATCH** NORM rescaled to LIT's own mean realised gross (idea 135/244's control), which
  separates *varying* the gross from *lowering* it.

n in {3,5,10,20,30,40,60} x 7 panels (idea 78's U56/ETF36/ETF24/STK20/B136/BSTK100, plus
SMALL480 rebuilt with the `max_1d_move >= 1.0` screen) x 2 books (CAND = idea 2's composite;
V1 = the live vol-scaled key) x 2 cost rungs = **588 arms**, every grid point printed. Two tuned
dimensions only: n and the convention.

**Gates (all asserted before any result was read):** LIT(CAND,n) == idea 78's `weights_cand`
max|dw| **0.0**; LIT(V1,n=5) == `baseline.rules_v1_weights` max|dw| **0.0**; engine agreement
max|dret| **0.0**; and idea 73's headline reproduced exactly — **STK20/CAND-20 LIT mean realised
gross 0.4920** against its published 0.492.

## The size of the channel

Mean realised gross under LIT, CAND book (target 0.75):

| panel | n=3 | 5 | 10 | 20 | 30 | 40 | 60 |
|---|---|---|---|---|---|---|---|
| STK20 | 0.719 | 0.719 | 0.691 | **0.492** | **0.328** | **0.246** | **0.164** |
| ETF24 | 0.700 | 0.694 | 0.669 | 0.608 | **0.427** | **0.320** | **0.214** |
| ETF36 | 0.729 | 0.738 | 0.719 | 0.676 | 0.596 | **0.455** | **0.304** |
| U56 | 0.737 | 0.741 | 0.737 | 0.717 | 0.688 | 0.648 | **0.467** |
| B136 | 0.741 | 0.745 | 0.745 | 0.739 | 0.735 | 0.728 | 0.709 |
| BSTK100 | 0.735 | 0.737 | 0.735 | 0.733 | 0.726 | 0.715 | 0.685 |
| SMALL480 | 0.748 | 0.747 | 0.747 | 0.745 | 0.744 | 0.741 | 0.731 |

A "top-60 book at 75% gross" on ETF24 is a **21% gross book**. The row does not say so.

## The queue's own instance reproduces exactly

u56 / CAND / n=20 @10 bps: premium over EWall **LIT +0.0431, MATCH +0.0145, NORM +0.0145**
against the queue's published **+0.043 literal vs +0.014 matched**.

Across the whole grid the LIT premium exceeds the NORM premium in **167 of 196 cells (85.2%)**;
mean Sharpe gap **NORM − LIT = −0.0517** (NORM higher in only 29 of 196). Under LIT the premium
*rises with n* and turns positive at n ≥ 20 on five of seven panels; under NORM it collapses to
~0 (U56 n=60: **+0.0743 → +0.0001**; STK20 n=60: **+0.0885 → −0.0028**). **The "wider ranked
books beat EWall" pattern in the record is the de-grossing, not the ranking.**

**Which channel:** on Sharpe the LEVEL term (MATCH − NORM) is **exactly 0.0000** — a constant
rescale is a pure lever with no risk-adjusted content, idea 66 re-derived here as an identity —
so **100% of the LIT-vs-NORM Sharpe gap is TIMING**: the literal book holds less *precisely when
the gate is cutting names*. On CAGR and MaxDD the level term is the larger one
(CAGR mean |TIMING| 0.0033 vs |LEVEL| 0.0158; MaxDD 0.0409 vs 0.0366).

## Rows whose verdict changes

Of 196 (panel, book, cost, n) cells: **4a verdict flips in 76 (38.8%)**, **4b verdict flips in
18 (9.2%)**. Seventeen of the eighteen 4b flips are KEEP-under-LIT → KILL-under-NORM (the one
exception is U56/CAND/n=40 @10 bps, KILL → KEEP). The flip rate is monotone in how much the
literal book was actually de-grossed:

| LIT realised gross | cells | 4a flip rate | 4b flip rate | mean dSharpe |
|---|---|---|---|---|
| < 0.45 | 28 | **1.00** | 0.00 | −0.114 |
| 0.45–0.60 | 16 | **1.00** | **0.25** | −0.153 |
| 0.60–0.70 | 30 | 0.63 | 0.23 | −0.080 |
| 0.70–0.745 | 88 | 0.15 | 0.08 | −0.023 |
| ≥ 0.745 | 34 | **0.00** | **0.00** | −0.002 |

**A published row is exposed exactly to the extent its book was silently de-grossed, and not
otherwise** — which makes realised gross a sufficient screening column for the whole record.

Counting KEEP passes rather than flips: **4b passes LIT 21 / MATCH 3 / NORM 5 of 196**;
4a passes **LIT 91 / MATCH 44 / NORM 15**. Among the casualties is the leaderboard's own
`73 STK20/CAND-n20 (inv 49.2%) … KEEP 4a/KEEP 4b` row: at n=20 its 4b passes under LIT and
**fails under NORM**, and the same holds at n=10 on both books.

## Rule 8 — the convention changes the rule, not only the number

n chosen on 2009–2016 only, 2017–2026 read once, against the EWall do-nothing control:

| convention | IS pick beats do-nothing OOS | mean OOS Sharpe | EWall control | mean regret |
|---|---|---|---|---|
| LIT | **18 of 28** | 0.8912 | 0.8321 | +0.0844 |
| NORM | **11 of 28** | **0.7607** | 0.8321 | +0.1061 |
| MATCH | 11 of 28 | 0.7607 | 0.8321 | +0.1061 |

Under the honest convention the n dial **loses to doing nothing** (0.761 vs 0.832 mean OOS
Sharpe). The IS-chosen n itself differs between LIT and NORM in **11 of 28** cells, and the
Sharpe argmax n differs in 5 of 28 (down 4, up 1).

## Is anything left standing?

Three NORM arms clear 4b: U56/CAND at n=20, 30, 40 @10 bps
(**12.79% / 1.064 / −18.3%**, halves 1.068/1.066, OOS 1.131, gross 0.750, 11.0x turnover —
against SPY 15.2% / 0.889 / −33.7%, halves 0.957/0.834, OOS 0.882, and RULES v1 6.5% / 0.664 /
−13.8%). They are **not a KEEP-candidate**: rule 8's own IS chooser picks n=3 on that cell,
which fails, so the surviving arms are visible only with hindsight. Recorded as a PARK.

## Predictions, scored

* P1 LIT gross < 0.60 on STK20 at n ≥ 20 — **TRUE** (0.492 / 0.328 / 0.246 / 0.164)
* P2 wide panels at small n within 0.01 of Sharpe — **TRUE** (24/24, max |dSharpe| 0.0073)
* P3 ≥10% of cells change their 4b verdict — **NARROWLY FALSE** (9.2%; 4a flips 38.8%)
* P4 LIT premium > NORM premium in the majority — **TRUE** (85.2%)
* P5 the LIT−MATCH term dominates — **TRUE on its stated quantity**, but P5's labels were
  swapped: LIT−MATCH is the *timing* term and MATCH−NORM is a pure rescale, zero on Sharpe by
  identity. Recorded rather than quietly relabelled.
* P6 argmax moves in a minority, upward under NORM — **PARTLY** (moves in 17.9%, but down 4 / up 1)

## Exposure of the record

**1633 of 3824** LEADERBOARD rows (42.7%) quote a count-based construction (CAND-n / top-n /
n = k / STK20 / V1u). Not all use the literal `GROSS/n` weighting, but each is a row whose
premium has to be read against the table above before it is believed. The cheap screen this run
recommends: **a row is safe if its book's realised gross is ≥ 0.745; it is suspect below 0.70
and is not interpretable below 0.60.** Realised mean gross belongs in the leaderboard schema.

## Caveats

NORM is not automatically the "right" convention — a book that de-grosses when its own gate cuts
names is a real, tradable book; it is just not the book its row claims to be. This run says which
number a row is quoting, not which one to want. SURVIVORSHIP: all panels are current-constituent
lists with no delistings; the bias is common to both arms and cancels in the LIT-vs-NORM
difference, but not in any level quoted here. MaxDD differences between conventions are
differences of single realised extrema (idea 117). U56/STK20/ETF24 saturate at large n and a
saturated rung is the same book at every n above it. The small panel is secondary (ideas
39/49/136). Costs are flat linear bps on turnover (idea 126). No level here is a tradable
estimate.
