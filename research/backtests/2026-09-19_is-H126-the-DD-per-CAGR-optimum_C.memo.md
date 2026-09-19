# Idea 1461 (lane C, 2026-09-19) — is H = 126 the DD-per-CAGR OPTIMUM, or a GRID ARTEFACT?

**ANSWERED: GRID ARTEFACT, both ways. The peak MOVES off 126 under refinement AND it does not
resolve. KILL (the claim). One incidental KEEP-4b candidate is carried below and is NOT
recommended; no rules change is proposed here.**

Script `2026-09-19_is-H126-the-DD-per-CAGR-optimum_C.py`, 225 cells (3 panels x 15 H-arms x 5 c),
every one published in `.grid.csv`. All 20 gates pass, including **G2, a cross-script replay of
the statistic under test**: re-forming 1444's coarse ladder reproduces its six published U56
slopes and B136's H = 126 slope to 4.2e-4. 10 bps, t+1, weekly, no leverage, no shorting.

## The answer

1444 read the exchange rate (pp of MaxDD bought per pp of CAGR given up, vs each rung's own
c = 0 anchor) on `{21, 63, 126, 189, 252, 378}` and found it peaked at the incumbent's own
H = 126 on U56 (-0.901) and B136 (-1.047). Refining the ladder to `{100, 112, 126, 142, 160}`:

| panel | H=100 | H=112 | **H=126** | H=142 | H=160 | point argmin |
|---|---|---|---|---|---|---|
| U56 | -0.702 | -0.472 | **-0.901** | **-1.391** | -1.128 | **142** |
| B136 | +0.221 | -0.280 | **-1.047** | -0.066 | **-1.050** | **160** |
| SMALL | +2.753 | +1.785 | +1.685 | +2.151 | **-1.202** | **160** |

**(i) THE PEAK MOVED.** 126 is the argmin on NO panel once its neighbours are 12% away instead
of a factor of 2. On U56 H = 142 is 54% steeper (-1.391 vs -0.901); on B136 H = 160 wins by
0.003. The coarse ladder did not find an optimum, it found the best of six far-apart rungs.

**(ii) THE PEAK ALSO DISSOLVED — and this is the larger finding.** Under a paired circular-block
bootstrap (400 reps, one shared block-start matrix per panel x L, so every rung-to-rung gap is
paired), the slope's own SE is **0.61 .. 8.96** against a total spread across the five rungs of
**0.92** on U56 and **1.27** on B136. The 126-vs-best-rival gap reads **|t| 0.14 .. 0.20** (U56)
and **|t| 0.01 .. 0.09** (B136) at every block length L in {21, 63, 126}; P(argmin = 126) is
**0.038 .. 0.080** on U56 and **0.330 .. 0.338** on B136 (the B = 252 control arm reads 0.028 ..
0.085 and 0.432 .. 0.455). The new argmin is not resolved either: P(argmin = 142) is 0.55 .. 0.75
on U56 and P(argmin = 160) is 0.500 .. 0.520 on B136 — a coin flip between five rungs. **The exchange-rate slope is a ratio of two sub-2-pp
differences and carries no resolving power at this sample length: no "best rung" claim read off
it — 1444's or this run's — is supportable.** Every one of the three pre-registered legs fails on
both large-cap panels, at all three block lengths.

**(iii) THE LOOKBACK CONTROL.** H = 126 also equals the beta lookback B and the composite's
middle momentum leg, so the whole ladder was re-run with B decoupled to 252 (published, never
selected on). U56's argmin stays at 142 and B136's moves *back* to 126 — the location is not a
lookback coincidence, it is noise.

## Capital (both KEEP paths at every cell, rule 8 read once)

**4a: 0 of 225.** 4b FULL 44 of 225, 4b OOS 44, BOTH **44** (U56 36, B136 8, SMALL 0). At the
frozen c = 0.50 on the refined ladder (15 books) 4b BOTH is 4 (U56 H = 126/142/160, B136 H = 126).

RULE 8, H chosen on warm-up..2016-12-31 at c = 0.50, 2017-2026 read ONCE, two pre-registered
choosers (argmax IS Sharpe; steepest IS slope):

| panel | chooser | IS H | OOS CAGR | OOS Sharpe | OOS MaxDD | 4b OOS |
|---|---|---|---|---|---|---|
| U56 | SHARPE | 142 | 17.25% | 1.2350 | -19.47% | **yes** |
| U56 | SLOPE | 142 | 17.25% | 1.2350 | -19.47% | **yes** |
| B136 | SHARPE | 142 | 18.34% | 1.0979 | -26.57% | no (DD) |
| B136 | SLOPE | 160 | 18.99% | 1.1098 | -27.00% | no (DD) |
| SMALL | SHARPE / SLOPE | 112 | 8.69% | 0.5308 | -36.81% | no |

Frozen incumbent OOS on U56 **17.32% / 1.1857 / -19.13%**; SPY OOS 15.26% / 0.8738 / -33.72%;
live RULES v2 OOS 9.46% / 1.2769 / -12.05%. Neither chooser picks H = 126 on any panel (0 of 6).

## The incidental KEEP-4b candidate, and why it is NOT recommended

U56, H = 142, c = 0.50, B = 126: full **15.47% / 1.2103 / -19.47%**, halves **1.302 / 1.158**
against SPY's 0.957 / 0.825; OOS **17.25% / 1.2350 / -19.47%** against the -20.23% cap (+0.76 pp)
and the 10.68% floor (+6.57 pp); turnover 3.42x/yr (34 bp/yr of drag). It clears **path 4b full
sample AND out of sample** and is rule-8 clean (both IS-only choosers pick it). It is carried as
a **PARK**, not a recommendation: against the standing frozen incumbent it buys **+0.049 of OOS
Sharpe at t = +0.55** and **-0.07 pp of OOS CAGR**, while *narrowing* the binding 4b DD margin
from +1.10 pp to +0.76 pp and raising turnover from 2.87 to 3.42x/yr. Its own c = 0 anchor
*fails* 4b (DD margin -1.15 pp), so the pass is bought by the band, i.e. by exactly the device
1436/1444 closed. Nothing here resolves, so nothing here should move capital.

If a future Sunday review nevertheless wanted it, the exact RULES wording would be:

> **4a. Sizing (band variant, U56 only).** Each rebalance, rank the held names by trailing
> 126-day beta to SPY, ascending, and let `z_i = 1 - 2*(rank_i - 0.5)/n` for `n` held names.
> Hold name `i` at `(0.75 / n) * (1 + 0.50 * z_i)` of current NAV — the **lowest**-beta name
> takes the cap, the **highest**-beta name the floor. The weights sum to `0.75` exactly; the
> remaining NAV stays in cash and is never re-spread.
> **5a. Min-hold.** A name entered at rebalance `t` is not sold for `142` trading days unless it
> loses its price; the top-`20` selection refills only the slots that min-hold has released.

**Survivorship (rule 9).** U56 / B136 are current-constituent lists and SMALL a current sub-$2B
screen carried back to 2010, so every absolute level is an upper bound and every 4b pass an
optimistic one. What this run reads is a CONTRAST between books over the same names on the same
days, which the bias cannot manufacture.

## Verdict

**KILL (the claim). No rules change.** 1444's finding #2 — "the incumbent already stands on the
best rung" — does not survive: the peak moves off 126 under a 12%-spaced ladder on every panel,
and the statistic it was read from cannot resolve any rung from any other at |t| > 0.20. The
practical consequence for the record is general: **a "best rung" read off a ladder whose
neighbours are a factor of 2 apart, with no SE on the statistic, is not evidence.**
