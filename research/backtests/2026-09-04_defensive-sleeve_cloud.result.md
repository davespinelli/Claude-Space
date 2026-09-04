# Idea 6 — defensive-sleeve: KILL (cloud lane, 2026-09-04)

**Script:** `research/backtests/2026-09-04_defensive-sleeve_cloud.py` ·
**Console:** `2026-09-04_defensive-sleeve_cloud.console.txt`

## Verdict

**KILL for the breadth trigger, and a warning about the sleeve it turns on.** 44 grid
points (2 universes x 2 books x [B in {30,40,50,60}% x L in {63,126}d, plus B=0 plain and
B=100 always-on controls]) plus 16 sleeve-definition controls, all reported. **1 of the
40 triggered arms passes 4b** — universe.json / top20 / B=30 / L=63, at a *lower* Sharpe
(1.047) than the plain book it is an overlay on (1.093), and it fails on the broad list
(-20.4% MaxDD vs the -20.2% cap), so it is a weaker version of the candidate it sits on,
not an improvement. The harness reproduces idea 2's KEEP row exactly (12.7%/1.093/-18.3%,
halves 1.088/1.103).

## The trigger does nothing

Paired daily difference vs the same book with the sleeve switched off — same names, same
days, same gross:

| book / universe | best arm | worst arm | range of paired t |
|---|---|---|---|
| v1 / universe.json | +0.30pp CAGR (B=60,L=126) | +0.02pp (B=40) | +0.11 .. +0.60 |
| top20 / universe.json | +0.29pp (B=60,L=63) | -0.27pp (B=40,L=126) | -0.14 .. +0.33 |
| v1 / broad | +0.21pp (B=30,L=63) | -0.18pp (B=50,L=63) | -0.24 .. +0.57 |
| top20 / broad | +0.21pp (B=30,L=63) | -0.31pp (B=50,L=126) | -0.25 .. +0.29 |

Nothing clears |t| = 0.6, the sign flips between adjacent B values and between the two
universes, and the Sharpe delta is **negative in all 16 triggered top20 arms**.

## It fails in exactly the year it was designed for

The trigger is overwhelmingly a 2022 instrument — at B=40 it is on 71% of 2022 days
(universe.json) and 57% (broad), against 13.2% / 11.4% of all days. **2022 is where it
loses the most:** top20 B=40 returns **-14.1% vs the plain book's -9.0%** on
universe.json and **-14.0% vs -10.9%** on broad (SPY -18.2%). TLT and GLD fell alongside
equities in 2022, so the sleeve concentrated the loss instead of hedging it. Its largest
gain is 2020 (+25.6% vs +15.4% on universe.json) and that is GLD's 2020 rally, not a
breadth effect — the always-on control captures the same gain with no trigger at all.

## Being out of cash is worth something; the breadth rule and the momentum pick are not

The **B=100 always-on** control is the best arm in all four (book, universe) cells:
+1.15 to +1.66pp CAGR, paired t +0.93 to +1.60 — still not significant, and it fails 4b
on drawdown in both top20 cells (-20.4% and -21.1% vs the -20.2% cap). And "best-of-3 by
L-day momentum" is a **negative-value selection**: at the idea's own setting (B=40,
L=63), naive equal-weight of the three sleeve assets beats it on Sharpe in 4 of 4 cells
(u.json top20 1.092 vs 1.031; broad top20 0.979 vs 0.943), and SHY-only — i.e. staying in
cash-equivalents — also beats it in 3 of 4. The slower lookback is worse: L=126 loses to
L=63 in 13 of 16 matched pairs.

## It damages the standing candidate

On universe.json the plain top20 book passes 4b (12.7%/1.093/-18.3%, halves 1.088/1.103,
OOS 1.170). **7 of its 8 triggered arms fail 4b, and all 7 fail on H1 alone**: the
overlay drops H1 Sharpe from 1.088 to 0.911-0.984 while H2 improves, because 2009-2011 is
the other low-breadth period and the sleeve sat in bonds through the recovery (2009
+10.4% vs +16.9%, 2011 -2.4% vs +0.5%). Turnover rises 9.6x -> 11.6x for a sleeve that is
on 13% of days.

## Walk-forward (rule 8, IS <= 2016, OOS >= 2017)

**Rule 8 rejects the overlay in 4 of 4 books.** The plain-Sharpe rule picks the plain
book (B=0) every time — both universes, both books. The 4b-aware rule picks NOTHING in
3 of 4 (no IS point met the IS bars Sharpe>0.899 / MaxDD>=-13.2% / CAGR>=10.5%) and picks
the plain book in the fourth. OOS reference: SPY 15.5%/0.884/-33.7%, RULES v1
7.8%/0.751/-13.8% (u.json) and 6.0%/0.581/-21.2% (broad).

## Honest limits

Survivorship: both lists are current constituents, so absolute CAGRs are optimistic; the
overlay-vs-plain comparison holds names, days and gross fixed and is far less exposed
(the three sleeve assets are ETFs that existed throughout). The KILL rests on a null
result plus one adverse year, and 2022 is a single episode — but it is the only deep
broad-market drawdown in the sample with a rising-rate character, which is precisely the
regime a bond-heavy defensive sleeve is exposed to, and no B or L setting escapes it.
