# Idea 921 — the FIVE-LEG cost closing price vs the WINDOW's (cloud, 2026-09-22)

**ANSWERED, and the answer corrects the record in BOTH directions.** 288 freshly priced books
(SHELF MOM/MOMVS/MADIST/LOWVOL x k in {5,10,20,40,ALL} x gross {0.50,0.75,1.00}, plus a BAND
ladder; U56 + B136; weekly + monthly; t+1 fills), each bisected TWICE on the cost axis to
0.05 bps: once for the DD-cap x CAGR-floor **WINDOW** and once for the full **FIVE-LEG** 4b pass.
Gates G1 (no leverage, max gross 1.0000), G2 (the five-leg set never re-opens above its closing
price: 0 re-openings) and G3 (the bisected price is itself open: 0 violations) all PASS.

## What the run found

1. **V1 NO — the 1.6x overstatement is NOT a corpus-wide fact.** Median c_WINDOW / c_5LEG is
   **1.00x** (mean 2.14x, p90 2.49x, max **45.95x**; 43.5% of books above 1.0). The reason is
   mechanical and idea 675 never separated it: on **39 of 69** books with finite prices the leg
   that closes the five-leg set IS a window leg, so the two prices are **identical by
   construction** (100% of that group, ratio exactly 1.00x).
2. **…but conditional on the only regime where it CAN differ, it is worse than 675 reported.**
   On the **30 of 69 books (43.5%)** whose closing leg is a SHARPE leg the window cannot see:
   ratio **median 1.52x, mean 3.61x, p90 4.60x, max 45.95x**, and 0% identical. Among the 45
   books that actually clear 4b at 10 bps, **21 (46.7%)** are in that regime, ratio median
   **1.34x**. The overstatement is a coin flip with an unbounded tail — and **nothing in the
   window itself tells you which side you are on.**
3. **V2 NO — at the protocol rung the window rarely lies about pass/fail.** Only **8 of 288
   books (2.8%)** have the window open at 10 bps while the five-leg pass is already closed;
   **51 of the 59** window-open books (86.4%) do clear all five legs. The window's failure is
   about HEADROOM, not about the verdict at 10 bps.
4. **V3 NO — the closing leg is most often L5_CAGR (52.2%)**, then L1_H1 24.6%, L2_H2 14.5%,
   L4_DD 4.3%, L3_OOS 4.3%. The CAGR floor is what kills a book as costs rise, exactly as the
   binding-leg censuses elsewhere in the record say; the Sharpe legs close 43.5% of books, short
   of the pre-stated 50% bar.
5. **The record's RUNG-QUOTING convention understates tolerance by a median 7.28 bps**, and
   **26.1%** of books with a positive five-leg price would be quoted **0 bps** by the
   {0,10,25,50,100} ladder. So the two conventions err in OPPOSITE directions: window-quoting
   overstates (when a Sharpe leg closes), rung-quoting understates (always).
6. **How much headroom a 4b pass really has:** of the 45 books clearing 4b FULL+OOS at 10 bps,
   the five-leg price runs median **32.2 bps** (min 10.6, p25 20.6, max 112.9). **17 of 45 (38%)
   die before the record's next quoted rung of 25 bps**, 31 of 45 before 50 bps.
7. **V4 YES (capital).** Rule 8 (IS 2009–2016 chooses, 2017–2026 read once) over the 72-book
   corpus per (panel x cadence) with three legal IS-only choosers: **1 of 12 picks clears 4b
   FULL+OOS** — U56 weekly, IS_LEGS, **BAND 0.08 at gross 0.75**, FULL 13.16%/1.1734/−19.70%,
   OOS 14.04%/1.1769/−19.70% vs SPY 15.29%/0.875/−33.72%, five-leg price **62.9 bps**. It is the
   same book idea 2109 reached the same day by IS_MINMARG, and an adjacent rung to idea 2101's
   band-0.10 candidate; no NEW candidate is filed here. 0 of 12 clear 4a.

## Consequence for the record

A 4b pass should be published with its **five-leg** cost closing price, bisected, not with the
window's and not as the largest passing rung. The window price is equal to it on 56.5% of books
and materially higher on the rest, with no ex-ante way to tell which; the rung ladder is
uniformly too pessimistic and reports 0 bps for a quarter of live prices. Proposed for a Sunday
review under rule 6 — nothing in RULES.md, PROTOCOL.md, scan.py, bot.py or baseline.py was
modified here.

**Survivorship (rule 9):** U56 and B136 are current-constituent lists, so every absolute bps
figure and every 4b pass count is optimistic. The object of the run — the RATIO of two prices on
one and the same book and tape — is first-order immune.
