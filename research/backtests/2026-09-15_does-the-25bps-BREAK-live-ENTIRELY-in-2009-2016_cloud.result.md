# Idea 918 (cloud, 2026-09-15) — does the 25 bps BREAK of the FULL-WINDOW 4b reading live ENTIRELY in 2009-2016?

**ANSWER: NO. The "H1 carries the cost break" reading is the SUBJECT BOOK'S OWN GROSS RUNGS, not a
record-wide fact — and it is not a turnover fact at all. KILL for the premise as stated; nothing
promoted, no RULES/PROTOCOL change proposed.**

Census (all re-scored from prices; no committed prose is read): 3 panels × 8 committed arms ×
30 gross rungs × 41 cost rungs = **29,520 scored cells**. A *cost-rung KILL* is a cell that clears
PROTOCOL 4b (convention c670) at the record's own 10 bps rung and fails at a higher rung; it is
attributed to the leg(s) that flip between the rungs. Gates **7 of 7 PASS**, including G4, which
reproduces idea 675's committed headline exactly (window **[0.6241, 0.8337]** vs the committed
[0.6241, 0.8337], |d| 4.0e-05 / 1.0e-05; `L1_H1` failing at **150 of 150** grosses at 25 bps), and
G3, the cost-linearity identity `r(c) = r(0) − turnover·c/1e4` against a fresh `engine.backtest`
(2.1e-17) on which the 41-rung ladder rests.

## The flip census — H_ENTIRELY FAILS at every claim set

| claim set | 10→25 bps | KILLS | H1 in flip | H1 ALONE | OOS-only reading survives |
|---|---|---|---|---|---|
| RECORD8 (670's own 8 rungs, U56) | 7 passers | 6 | 0.6667 | 0.3333 | 0.8333 |
| CORE30 (30 rungs, U56) | 20 passers | 12 | **0.8333** | 0.3333 | 0.7500 |
| WIDE (30 rungs × 3 panels) | 31 passers | 18 | **0.5556** | 0.2222 | 0.5000 |

H_ENTIRELY (every KILL flips `L1_H1`) **FAILS 3 of 3**; H_MOSTLY (≥ 0.80) passes only on CORE30,
the U56-only claim set. At 50 bps the H1 share is 0.71 / 0.87 / 0.78 and `L1_H1` is **never** the
sole flip (0.0000 at every claim set) — by then the whole leg set goes together.

## Which leg actually closes first (per-leg closing prices, 31-cell 10 bps pass set)

`L5_CAGRfloor` **16 of 31 (0.5161)** · `L2_H2` 7 · **`L1_H1` 5 (0.1613)** · `L4_DDcap` 1 ·
alive at 100 bps 2. Median closing price by leg: L5 **27.5** · L1 **25.0** · L2 37.5 · L3 40.0 ·
L4 52.5 bps; the 4b pass itself closes at a median of **22.5 bps** (min 12.5, max 100).
**Panel split: on B136 the first leg to close is `L1_H1` in 0 of 11 cells** (L2_H2 7, L5 4). So the
2009-2016 half is not the record's cost-fragile leg; the **FULL-window CAGR floor** is, and the H1
carry is a U56 phenomenon that holds on only 5 of 20 U56 cells.

## The subject reproduces — and shows why the generalisation fails

U56/CAND20, the standing 2026-09-04 KEEP 4b book, per gross rung (closing price in bps):

| g | first leg | 4b closes | L1_H1 | L2_H2 | L3_OOS | L4_DDcap | L5_CAGRfloor |
|---|---|---|---|---|---|---|---|
| 0.65 | **L5_CAGRfloor** | 15.0 | 22.5 | 37.5 | 40.0 | 90.0 | **15.0** |
| 0.70 | L1_H1 | 22.5 | **22.5** | 37.5 | 40.0 | 80.0 | 22.5 |
| 0.75 (live) | L1_H1 | 22.5 | **22.5** | 37.5 | 40.0 | 70.0 | 27.5 |
| 0.80 | L1_H1 | 22.5 | **22.5** | 37.5 | 40.0 | 57.5 | 35.0 |

675's reading is exactly right *at the published gross*, and wrong one rung below it: the two
binding legs cross each other between g = 0.65 and 0.70, because cost pushes the CAGR floor up
while the H1 leg is flat in gross. "Which half carries it" is therefore a statement about a
(book, gross) cell, not about a book.

## Mechanism — H_SLOPE FALSIFIED: the carrier is the MARGIN, not turnover

Per-half cost slopes (Sharpe per 10 bps) are within **8.0%** on U56 (−0.09473 H1 vs −0.08775 H2,
ratio 1.080, bar 0.10), 6.8% on B136 and 1.1% on SMALL, and H1 turnover is *lower* than H2's on
every panel (ratio 0.920 / 0.902 / 0.814) — the opposite sign to the turnover story. What differs
is the **margin**: on the subject at g = 0.75 and 10 bps, H1 clears SPY by **+0.1146** of Sharpe
and H2 by **+0.2310**, giving breakeven costs of **21.8 bps (H1)** vs **36.1 bps (H2)**. The early
window is not more expensive to trade; it is simply closer to SPY.

## Rule 8 (required) — gross chosen on 2009-2016 only, 2017-2026 read once

U56 / CAND20, three IS-only choosers plus the zero-parameter PICK_LIVE (g = 0.75 fits nothing):

| cost | chooser | g | OOS CAGR | Sharpe | MaxDD | 4b | 4a |
|---|---|---|---|---|---|---|---|
| 10 | PICK_ISMID | 0.784 | 14.98% | 1.123 | −19.08% | Y | n |
| 10 | PICK_ISLO | 0.746 | 14.26% | 1.123 | −18.22% | Y | n |
| 10 | PICK_LIVE | 0.750 | 14.34% | 1.123 | −18.31% | Y | n |
| 25 | PICK_LIVE | 0.750 | **12.44%** | **0.991** | **−18.44%** | **Y** | n |
| 50 | PICK_LIVE | 0.750 | 9.35% | 0.769 | −18.66% | n | n |

SPY OOS 15.27% / 0.874 / −33.72%; RULES v2 (live) OOS 9.46% / 1.277 / −12.05%. Across all panels:
OOS 4b 6 of 8 picks at 0 bps, **3 of 8 at 10**, **1 of 5 at 25**, 0 of 3 at 50; **4a 0 of 24**
everywhere (the live band book's Sharpe is ~0.15 above CAND20's at every rung and gross cannot
close it). Two facts worth carrying: (i) at 25 and 50 bps on U56 **no IS-only chooser exists at
all** — the in-sample level window is empty, so only the zero-parameter PICK_LIVE can be scored,
which is idea 675's "empty IS pass set" fragility appearing again one rung up; (ii) the subject's
**OOS-only reading survives 25 bps** (12.44% / 0.991 / −18.44% against SPY's 0.874) while its
FULL-window reading dies — but that survival generalises to only **0.50** of killed cells on WIDE,
below the pre-registered 0.80 bar, so it too is close to being the one book's property.

## Verdict

**ANSWERED = NO (KILL for the premise).** The 25 bps break lives entirely in 2009-2016 only on the
published book at g ≥ 0.70 on U56; across the record's own committed arm/gross/panel grid the modal
carrier is the FULL-window **CAGR floor** (51.6% of first closes) and the H1 leg carries 16.1%,
never first on B136. The break is a **margin** fact, not a **turnover** fact: the two halves pay
cost at the same rate to within 8%, and 2009-2016 simply starts 0.12 of Sharpe closer to SPY.
PARK for the book (its committed 4b KEEP-candidate status is unchanged and nothing here promotes
or demotes it); no memo proposing a RULES change, and `RULES.md`, `PROTOCOL.md`, `scan.py`,
`bot.py`, `baseline.py` are untouched.

**SURVIVORSHIP:** U56 / B136 / SMALL are current-constituent lists, so every CAGR and drawdown
level is optimistic. A 4b bar is a ratio of the book's level to SPY's and SPY is not
survivorship-inflated, so the bars are not protected by the same-tape argument: every closing
price above is an **upper bound** on the closing price a point-in-time panel would show. SMALL
additionally drops the 52 tickers with `max_1d_move >= 1.0` per `data/small_meta.csv`.

Script: `research/backtests/2026-09-15_does-the-25bps-BREAK-live-ENTIRELY-in-2009-2016_cloud.py`
Artifacts: `.census.csv` (2,880 rows), `.flips.csv` (229), `.closing.csv` (31),
`.mechanism.csv` (720), `.walkforward.csv` (24), `.bars.csv` (6), `.console.txt`.
