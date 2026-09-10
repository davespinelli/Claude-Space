# Idea 618 — is the INTERCEPT of the width law a DEFENSIVE-SLEEVE statistic?  (lane C, 2026-09-10)

**VERDICT: SPLIT.** Sleeve — yes. Drawdown — no. Capital — none.

**Setup.** `width = intercept(panel, book, sleeve) - slope x drag`, re-measured with the sleeve asset
set swept: 10 pre-registered sleeves (CASH, SHY, IEF, TLT, GLD, UUP, ETF3, BOND2=TLT+IEF,
DEFEQ=XLU+XLP, SPY1) x 2 panels (u56, broad136) x 2 books (TOP20, EWALL) x 8 lambdas x 11 f, read
at 6 cost rungs = **21,120 arm-rows / 40 law cells**. Tuned parameters are the queue's two (sleeve
set, f); both swept in full, every point reported. Weekly, t+1, gross 0.75, IS <= 2016-12-31.
At f = 0 every sleeve collapses to the same book, so **base_to is sleeve-invariant to 0.000e+00** and
the drag axis is literally the same x-axis for all ten sleeves.

**Gates.** All five pass. G3 reproduces every one of idea 613's published width levels and slope
pairs off its committed artefact exactly (u56/TOP20 6.90 ETF3 vs 4.35 CASH, rho -0.923/-0.847;
broad/EWALL 3.67 vs 0.06, rho -0.930/-0.374).

**H1 — it is a sleeve statistic.** R^2(sleeve label) on the intercept **0.731** vs R^2(panel x book)
**0.184** (panel alone 0.055). The queue's premise holds. It does *not* hold for the slope once the
level is divided out: b_norm is R^2 0.058 on sleeve and **0.831 on panel x book**.

**H2 (the ask) — it is NOT a drawdown statistic.** rho(intercept, the sleeve's own MaxDD) =
**-0.156, perm p 0.614** (ex-CASH -0.109, p 0.733). The two deepest-drawdown sleeves in the set,
GLD (-33.4%) and TLT (-33.1%), carry the **first and third widest** intercepts. What separates the
cells is CO-MOVEMENT with the book: `sl_corr > 0.5` classifies the inert-vs-not binary **40 of 40**
(**AUC 1.000**), naming exactly DEFEQ (+0.524) and SPY1 (+0.823) as the sleeves with no window
anywhere, while **AUC(sl_MaxDD) = 0.312 — worse than a coin flip**. Crash-day cushion is the
strongest ranking column (+0.504, p 0.075) but GLD breaks it (cushion -23.8 bps/day, widest
intercept), so the defensible statement is correlation, not payoff-in-crashes. **None of the six
sleeve columns clears 5% on ten sleeves** — the effect is an ordering, not a fitted law.

**H3 — 613's slope stability replicates in rank units only.** Pooled CV: rank slope rho **0.166**
vs intercept **0.709** (4.3x, as claimed); in raw width units the slope is the *more* dispersed
term (CV 1.102), because b_ols scales with the level it multiplies.

**KEEP paths.** 4a **55/21,120**, 4b **5,531/21,120**, **BOTH 12/21,120 — all ETF3, all u56, all at
0 and 5 bps. At PROTOCOL's own 10 bps rung and above, BOTH = 0.** Same shape as idea 403 (12/4,224)
and idea 613 (12/5,280). DEFEQ and SPY1 take **0 of 352** 4b passes each at 10 bps.

**Rule 8.** (f, sleeve) chosen on 2009-2016 alone, 2017-2026 read once, 5 selectors x 192 cells =
960 picks. **OOS 4a 0/960; OOS 4b 7/960, every one at 0 or 5 bps (0/960 at 10 bps and above).**
Best selector at 10 bps is S2 (min sleeve IS drawdown): OOS CAGR 14.35%, Sharpe 1.094, MaxDD -22.8%
against SPY OOS 15.32%/0.876/-33.7% (u56), 15.45%/0.882/-33.7% (broad) and RULES v2 OOS
9.48%/1.279/-12.1% (u56), 7.98%/1.119/-12.2% (broad). **The sleeve column does not reach the
decision:** S2 (picks CASH, cushion 0.0) and S3 (picks SPY1, cushion -153.1 bps/day) are the two
maximally opposite sleeve choices in the set and their OOS Sharpes sit **0.0107 apart on average,
0.0209 at worst** across all 192 paired cells; both win by spending the parameter as little as
possible (median f = 0.05).

**Caveats carried.** Survivorship (idea 54) on both panels — current constituents. SMALL439
excluded: it prices no ETF, so 9 of 10 sleeves do not exist on it, and idea 613 already found both
its cells inert. Sleeve assets are also investable names in both panels (403/613's convention).
lambda can only lower turnover. MaxDD is one number off one path (idea 321). Ten sleeves is a small
population for a rank correlation, which is why a sleeve-label permutation p is printed beside every
headline rho.

**Nothing promoted.** RULES.md, PROTOCOL.md, scan.py, bot.py, baseline.py untouched.
