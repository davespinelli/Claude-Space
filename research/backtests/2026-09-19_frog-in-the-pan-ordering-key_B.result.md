# Idea 1519 (lane B, 2026-09-19) — FROG-IN-THE-PAN as an ordering key on the incumbent: **KILL**

**The question.** Idea 1501 showed the conviction ORDERING inside the standing 2026-09-04 KEEP-4b
incumbent's top 20 is real information but rule-8 unreachable. This run asked whether the same
channel can be bought from a *different* key: frog-in-the-pan information discreteness,
`ID = sign(PRET) x (%down - %up)` over L sessions, blended into the ranking key at weight w.
Dials: L {63, 126, 252} x w {0, 0.10, 0.20, 0.35, 0.50, 0.75, 1.00}; w = 0 IS the frozen
incumbent. 21 cells per panel on U56 / B136 / SMALL, all 63 published in `.grid.csv`.

**The answer is no, and the control is what says so.** Every headline w was scored against a
rank-PERMUTED ID twin (ID permuted across names within each row: same marginal distribution, same
amount of reordering, no cross-sectional information), 20 seeds. Over the 20 control cells the
real book beats the twin mean at **10 of 20 (full)** and **14 of 20 (OOS)** — a coin flip — and
`|z| > 2` at **0 of 20 full**; the one `|z| > 2` (OOS, U56 L=126 w=0.20) runs **against** ID at
-2.05. The grid's own two best ID cells, given their own control after the fact, are
**UNRESOLVED**: U56 (L=252, w=0.10) 1.1745 vs twin 1.1475 +/- 0.0236, z **+1.15**; B136
(L=126, w=1.00) 1.1318 vs 1.0558 +/- 0.0512, z **+1.49**.

**Both KEEP paths.** 4a **0 of 63**. 4b full AND OOS 29 of 63, but the frozen book's own verdict
already decides 26 of them (U56 frozen passes, 19 of 21 U56 cells pass; B136 frozen fails the DD
leg at -20.74% vs the -20.23% cap, 10 of 21 pass). 12 of 54 ID cells strictly dominate the frozen
incumbent on full Sharpe AND OOS Sharpe AND MaxDD; none is resolved.

**Rule 8.** (L, w) by argmax IS Sharpe on warm-up..2016-12-31, 2017-2026 read once: U56 (63, 0.75)
dOOS **-0.1312**; B136 (126, 1.00) **+0.0744**; SMALL (63, 0.35) **-0.1225**. Mean **-0.0598**,
beats doing nothing on **1 of 3** panels — and that one panel's anchor was already failing 4b.
The U56 cell that does improve OOS (L=252, w=0.10, +0.0375) is unreachable by any IS chooser.
H_HINDSIGHT reproduces.

**Why it fails.** On the large panels ID is not even an independent channel: its median
cross-sectional rank correlation with the incumbent's own composite is +0.25 / +0.37 / +0.37
(U56, L = 63/126/252). On SMALL it *is* independent (+0.09) and still delivers nothing.

**The one residual, filed as idea 1523, not claimed.** Random reordering makes U56's MaxDD WORSE
at 9 of 9 control cells (twin mean -20.09% .. -21.21% vs the frozen -19.13%), while the real
w = 1.00 book reaches **-16.46% (U56, L=252)** and **-16.71% (B136, L=126)** at LOWER turnover
(2.42 vs 2.87 x/yr). ID's only candidate channel is the drawdown leg, not Sharpe — and at 20
seeds it is unresolved.

**Survivorship (rule 9).** U56 / B136 are current-constituent lists and SMALL a current sub-$2B
screen. Absolute levels are upper bounds; the headline is a contrast between two orderings of the
same names on the same days, which is first-order immune. The 4b pass counts are not.

**Gates 9/9**, including G1 (the w = 0 cell replays the committed 2026-09-04 U56 anchor
15.80% / 1.1537 / -19.13% full and 1.1857 OOS to 3.7e-05 of Sharpe), G2 (the w = 0 selection
frame is bit-identical across all three L), G6 (max realised weight sum 0.750000) and G8
(bit-identical recompute). RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py untouched.
