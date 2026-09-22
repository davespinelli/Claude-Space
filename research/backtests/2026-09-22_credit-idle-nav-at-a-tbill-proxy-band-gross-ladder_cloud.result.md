# Idea 2213 (lane cloud, 2026-09-22) — credit the IDLE NAV at a T-BILL PROXY on every committed BAND-BOOK CAGR

**Question.** `engine.backtest` pays 0% on `1 - sum(w)`. The live RULES v2 band book leaves ~47% of NAV
there while its 4b comparand SPY is fully invested, and idea 2119 killed the whole band x gross ladder on
the CAGR floor alone. How much of that shortfall is an accounting convention rather than a book fact?

**Design.** The 2119 ladder unchanged — band c in {0.00,0.02,0.03,0.05,0.08} x gross g in
{0.50,0.60,0.75,0.85,1.00} (2 tuned params, all 25 points published) x panel {U56,B136} x cost
{0,10,25,50} bps x window {FULL,IS,OOS} x weekly offset d in {0,1,2}. Three arms: **CASH** (committed
form, idle at 0%), **SHYFREE** (idle swept into SHY, sweep turnover not charged — the pure convention
read), **SHYTRADED** (the same book with the sweep's own turnover charged). 5,418 published rows.

**Gates.** G1 offset_mask(d=0) == `engine.rebalance_mask(W)`, 0 differing rows, both panels. G2 the
ladder's live cell == `baseline.rules_v2_weights`, max|d| **0.0**. G3 local runner + cost reconstruction
== `engine.backtest` at 10 and 25 bps, max|d| **<= 1.4e-17**. G4 0 clipped weeks at d<=2. G5 with SHY's
own return zeroed the sleeved book collapses onto CASH, max|d| **2.4e-17**. G6 (external) the SHYTRADED
live cell reproduces lane B's independent idea-2221 phi=0 reading **exactly**: +0.50 pp CAGR / +0.067
Sharpe / +0.57 pp MaxDD on U56 and +0.52 / +0.070 / +0.59 on B136. G7 (external) the CASH arm's rule-8
pick reproduces idea 2119's published pick exactly: c=0.08/g=1.00, OOS 12.00% / 1.1625 / -19.05% (U56)
and 10.98% / 1.0921 / -19.50% (B136).

## A. The answer: about a fifth to two thirds of the shortfall, and never enough

At the live cell (c=0.03, g=0.75) the free credit is **+0.613 pp** (U56 FULL) / **+0.799 pp** (U56 OOS) /
+0.627 / +0.834 (B136), against CAGR shortfalls of 1.978 / 1.245 / 2.627 / 2.833 pp — i.e. the convention
accounts for **31.0% / 64.2% / 23.9% / 29.4%** of it. Ladder-wide the median share closed is
**0.200 (U56 FULL), 0.298 (U56 OOS), 0.185 (B136 FULL), 0.294 (B136 OOS)**.

## B. Why it can never rescue a de-grossed cell

The credit is an almost deterministic function of idle NAV — **+0.0139 to +0.0184 pp of CAGR per 1 pp of
idle NAV, rho 0.9933-0.9992** over the 25 cells — but the shortfall it has to close rises
**+0.151 to +0.176 pp per idle pp**, i.e. **8.4x to 11.4x faster**. De-grossing buys idle NAV at ~0.16 pp
of CAGR and a T-bill sells it back at ~0.016. Consequently **0 of 15 cells at g <= 0.75 clear the CAGR
floor in any window, on either panel, under any arm** — idea 2119(B)'s structure survives the fix intact.
The only verdict the sweep moves is at the top of the ladder: U56 OOS g=0.85 goes **1 -> 5 of 5 bands**
and B136 OOS g=1.00 goes **1 -> 5 of 5**, all of it the CAGR leg flipping on cells that were already
marginal. 4b counts of 25 at 10 bps: U56 OOS 6 -> 10 (free) / 10 (traded); B136 OOS 1 -> 5 / 4.

## C. As a rules change it is a 4a gain that the cost ladder retires

The sweep strictly beats the live book: U56 FULL Sharpe **1.2010 -> 1.2820** (free) / 1.2675 (traded),
MaxDD **-12.05% -> -11.47%**, and it passes **4a at 0/10/25 bps** on both panels in all three windows —
but turnover goes **1.77 -> 2.79 x/yr** (U56) and 2.01 -> 3.03 (B136), 4a fails at 50 bps free and at
25/50 bps traded, and the sweep's own cost eats **21-22%** of the credit at 10 bps. This is lane B's
independent idea-2221 KILL of the T-bill sweep, reproduced on a wider grid.

## D. Rule 8 (params on 2009-2016 IS Sharpe only; 2017-2026 read once) — the fix INVERTS the chooser

The habitual chooser flips from **g=1.00 under CASH to g=0.50 under both sweep arms, on both panels**,
because crediting idle NAV raises Sharpe most exactly where idle NAV is largest while IS Sharpe stays
blind to CAGR (2119(D) reproduced with the sign turned against us). U56 SHYFREE C1 pick c=0.08/g=0.50:
OOS **7.17% / 1.3661 / -8.92%** — 4a PASS, **4b FAIL on the CAGR leg alone**, at 3/3 offsets and 4/4 cost
rungs. The legal IS-only chooser restricted to IS-4b passers (C2) picks c=0.08/g=1.00 and does pass 4b in
FULL, IS and OOS on both panels — U56 OOS **12.62% / 1.2158 / -18.85%** (H1 1.331 / H2 1.089), B136 OOS
11.53% / 1.1411 / -19.31%, against SPY OOS 15.29% / 0.8751 / -33.72% and RULES v2 OOS 9.46% / 1.2767 /
-12.05% — but its DD margin (+1.38 pp U56, +0.92 pp B136) is still **inside its own 3-offset spread**
(1.86 / 1.13 pp), which is the condition that killed the identical CASH cell under 914/2119.

**Verdict: KILL of the premise (the shortfall is mostly a book fact, not a convention) + KILL of the
sweep as a rules change (cost ladder) + one PARK 4b candidate, recorded and NOT recommended.**
