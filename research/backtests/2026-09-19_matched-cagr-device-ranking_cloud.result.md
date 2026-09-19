# Idea 1488 (cloud lane, 2026-09-19) — rank the FOUR DD-buying devices at MATCHED CAGR instead of by an unmeasurable ratio

**VERDICT: KILL — the repair does not repair. `0 of 165`.**
Script `research/backtests/2026-09-19_matched-cagr-device-ranking_cloud.py`; 18/18 gates; 75s.

## The question
Idea 1468 (this run's first idea) found the DD-per-CAGR exchange rate resolves **1 rung gap in
144** and **1 cross-family gap in 36** at |t| > 2, and recommended publishing exchange rates as
orderings rather than values. The natural repair is to **stop dividing**: a ratio of two small
tape differences has no usable sampling distribution, but a difference does. So each of the four
DD-buying devices the record has priced has its **own dial solved** to a **common CAGR haircut**
off the frozen 2026-09-04 incumbent, and the resulting **MaxDDs are compared as a paired
difference** on one shared block-start matrix per (panel, L).

Devices (all on the incumbent's frame, all sharing one bit-identical anchor — gate G2, 0.000e+00):
**GROSS** g, 46 rungs 0.75→0.30 · **BAND** beta band c, 41 rungs 0.00→1.00 at B=126 ·
**IVOL** w ∝ vol^(−p), 41 rungs p 0→4 at lookback 63 · **STOP** trailing equity stop, 48 rungs
depth 0.020→0.250 at FRAC 0.50 (FRAC 1.00 excluded — 1468 showed it is an absorbing state).
Tuned: the **haircut ladder h ∈ {0.5, 1.0, 1.5, 2.0, 2.5} pp** and the **block length
L ∈ {21, 63, 126}**. Each device's own dial is *solved*, not chosen; all 534 dense-ladder rungs
are published so the solve can be audited, and every matched cell lands within **0.25 pp** of its
target (gate G7, max residual) with a max pairwise CAGR spread of **≤ 0.50 pp** (gate G12).

## THE ANSWER — 0 of 165, and the difference ruler is not even better on the ordering
**Device-vs-device matched-CAGR MaxDD gaps resolving at |t| > 2: `0 of 165`.** Median |t|
**0.4140**, **max |t| 1.4998** — not one pair on one panel at one block length comes within a
third of the bar. Per panel: U56 **0/81** (median |t| 0.5233), B136 **0/72** (0.2634), SMALL
**0/12** (0.5889). The pre-registered bar — more than half the gaps resolving at L = 63 on U56
and B136 — reads **0 of 51**. **RULER REPAIRED = False.**

Worse for the repair: the **median sign fraction is 0.7575**, *weaker* than the 0.83–0.995 that
1468's ratio produced on the same devices. Removing the division removes the heavy tail and it
removes the ordering with it. **Neither ruler ranks these devices.** The record does not have a
measurement problem it can fix by choosing a better statistic; it has **four devices whose
drawdown effects at matched return are the same size as the tape's own noise.**

**The point estimates still say de-gross, for what that is worth.** Argmax of dMaxDD at each
(panel, haircut): **GROSS 10 of 15, BAND 3, IVOL 2**, and GROSS wins all five SMALL cells by
margins of 2.6–12.0 pp. That is the seventh consecutive run to put the plain de-gross first on
point estimates, and the first to show the margin is unresolvable by a difference as well as by
a ratio.

## Reachability is a result, not a nuisance
**14 of 60 (device, panel, haircut) cells are UNREACHABLE** — the device's entire legal ladder
cannot buy that haircut: **BAND 6, IVOL 5, STOP 3**. On **SMALL, BAND and IVOL cannot buy ANY
haircut**: both *raise* CAGR above the anchor at every legal dial, so no CAGR cost exists to
match against (published, not asserted, in place of gate G8 on that panel). This independently
reproduces ideas 1444 and 1465 — the band raises CAGR at 24 of 24 biting cells on SMALL — from a
different direction, and it means every committed SMALL "exchange rate" for those two devices is
a rate for a cost that is not being paid.

## Capital (PROTOCOL rules 3, 4, 8, 9)
46 matched books, every one published, plus 534 dense-ladder rungs. **4a: 0 of 46.** **4b full:
34 of 46; 4b full AND OOS: 34 of 46** — but every 4b passer is a de-grossed or lightly-banded
copy of the anchor the record already holds, not a new book. Binding legs: L_H2 11 > L_DD 10 >
L_H1 9 = L_CAGR 9.

**Rule 8** (the haircut re-solved on warm-up..2016-12-31 only, each device's dial matched to the
IS CAGR target, 2017-2026 read ONCE, chooser = best IS matched MaxDD):

- the chooser names the **OOS winner in 8 of 15** cells (four devices, so barely above chance),
  and picks GROSS in 12 of 15;
- mean **Δ(OOS Sharpe) vs the frozen anchor −0.0173, beating it 0 of 15** — on U56 the loss is
  0.0001–0.0005 of Sharpe, on SMALL it is up to 0.21;
- mean **Δ(OOS MaxDD) +3.485 pp, improving it 15 of 15.**

That last line is the capital answer and it is not nothing: **at matched CAGR, DD-buying does
work out of sample — every chooser cell cuts drawdown, by 0.51 to 11.94 pp — it just never buys
Sharpe, and which device delivers it is unresolvable.** U56 h = 2.5 pp: GROSS g = 0.62, OOS
14.27% / 1.1852 / **−16.00%** against the anchor's 17.32% / 1.1857 / −19.13%, SPY's 15.26% /
0.8738 / −33.72% and RULES v2's 9.46% / 1.2769 / −12.05%. **No cell clears 4a on any panel, no
new book is proposed, and no RULES memo is written.**

**SURVIVORSHIP (rule 9).** U56 / B136 are current-constituent lists and SMALL a current sub-$2B
screen carried back to 2010 (54 tickers with max_1d_move ≥ 1.0 dropped per `data/small_meta.csv`;
665 investable names remain). Every absolute level is optimistic and the 34-of-46 4b count is
not protected. The headline is a **matched, paired contrast** between books built over the SAME
names on the SAME days at the SAME bootstrap draws, which the bias cannot manufacture.

**Gates 18/18**, including G1/G1b (frozen U56 anchor replays at 15.8028% / 1.1537 / −19.1276%
full, 1.1857 OOS Sharpe), G2 (all four inert rungs bit-identical, 0.000e+00), G6 (no leverage,
no shorting — max weight sum 0.75, min weight ≥ 0 at every c ≤ 1), G7, G9, G10, G11, G12.

**No RULES change.** RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py untouched.
