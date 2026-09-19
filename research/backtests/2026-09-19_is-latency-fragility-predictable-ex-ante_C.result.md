# Idea 1596 — is LATENCY FRAGILITY PREDICTABLE EX ANTE from TURNOVER or HOLDING AGE?
**VERDICT: PARK as pre-registered, KILL on the deflated reading. No new book. What capital should do
is read the latency axis per book, as idea 1590 did — there is no shortcut through these two
statistics.** Gates 48/48. Script: `2026-09-19_is-latency-fragility-predictable-ex-ante_C.py`.

**The object.** 144 real books — 3 panels (U56 56 names, B136 136, SMALL 663-name sub-$2B screen) x
H {21, 42, 63, 126, 252, 504} x cadence {W, M} x gross {0.50, 0.60, 0.75, 1.00} — each run at
execution delay +0 and +1 on top of PROTOCOL rule 2's decide-at-t-1/apply-at-t, at 10 bps: **288
published cells, both KEEP paths at every one, FULL and OOS.** Two tuned parameters: the latency
point (+1, named by the idea) and the regressor set. H / cadence / gross are a published ladder;
N = 20, MAXVOL 0.60, the 200d gate and the cost rung are frozen inheritances. G1 replays the
committed 2026-09-04 U56 anchor to 2e-16 (15.80% / 1.1537 / -19.13% FULL, 1.1857 OOS) and reproduces
1590's headline fragility exactly: **dMaxDD(+1) = -2.44 pp on that book.**

**1. The fragility is real and two-sided.** Over 144 books dSharpe(+1) has mean -0.0005, sd 0.0419,
range -0.1276..+0.0912; dMaxDD(+1) mean +0.15 pp, sd 1.52 pp, range **-3.28..+6.28 pp** — against a
4b DD margin the record decides on at 1.10 pp. Latency makes drawdown **worse in 79 books and better
in 65**, and flips the 4b verdict in **7 of 144 FULL and 11 of 144 OOS**. 1590's alarm is confirmed
on a four-times-larger book set.

**2. Neither regressor is separately identified.** corr(turnover/yr, mean holding age) = **-0.681**
pooled (-0.766 per unit gross): a faster brake mechanically raises turnover *and* lowers age, so the
ladder cannot tell them apart. A coefficient **flips sign between its univariate and its bivariate
fit in 7 of 48 (sample, Y, regressor) triples**, and on U56 turnover's dMaxDD coefficient goes from
+0.338 (t +1.75) alone to +0.097 (t +0.29) beside age. In the pre-registered reading (iii,
gross = 0.75, pooled, panel dummies) both reach |t| > 2 on dMaxDD — t[turn] -2.19, t[age] -2.69 — but
that is two collinear regressors splitting one axis, not two mechanisms.

**3. The R² that clears the pre-registered bar is mostly panel dummies.** Pooled R² = 0.431 on
dMaxDD(+1), but the **dummies alone explain 0.297** on the same 36 rows: the two regressors buy
**dR² = 0.134**. On dSharpe(+1) they buy essentially nothing (pooled R² 0.093, no regressor at
|t| > 2). The bar was written as a pooled R² before the run and is reported as written — hence PARK —
but the honest answer to "how much of the fragility either explains" is **13.4%**.

**4. The killer is in step 3, and it is independent of the regression.** For the ex-ante claim to
work, a book's *in-sample* fragility must survive into the OOS window. It does not:
**rho(IS dSharpe(+1), OOS dSharpe(+1)) = -0.18 pooled and NEGATIVE on all three panels** (-0.36 U56,
-0.21 B136, -0.07 SMALL); rho(IS dMaxDD, OOS dMaxDD) = **-0.07** pooled. Latency fragility measured
on 2009-2016 anti-predicts latency fragility on 2017-2026. No regressor, and no model fit on those
rows, can repair that.

**5. The capital arm (rule 8, 2017-2026 read once) fails as pre-registered.** Four IS-only choosers
over each panel's 48 books. PREDROBUST — the idea's own proposal, minimising the IS-fitted
predicted |dMaxDD(+1)| inside the 2026-09-03 memo's admitted set — picks U56 M/H=42/g=0.60 (FULL
12.16% / 1.1082 / -20.88%, OOS 13.41% / 1.1230 / -20.88%, **4b FALSE on both windows at both
delays**) and B136 W/H=21/g=0.75 (**OOS dMaxDD(+1) = -1.65 pp, the worst of the four choosers**). It
clears 4b FULL+OOS at delay +1 on **0 panels** and beats both rivals' OOS |dMaxDD(+1)| on **1 of 3**
(bar 2). H_USABLE does not fire. SMALL admits 0 of 48 books, so only ISSHARPE exists there.

**6. The one honest positive, stated at its real weight.** REALROBUST — smallest *realised* IS
|dMaxDD(+1)|, IS rows only, no model — picks B136 W/H=126/g=0.50: FULL 10.69% / 1.0632 / -14.17%
(H1/H2 1.279/0.894), **OOS 10.80% / 1.0155 / -14.17%, 4b TRUE on both windows at BOTH delays**, and
latency *helps* it (OOS dMaxDD +0.95 pp), against SPY FULL 15.12% / 0.8845 / -33.72% (bars: DD cap
-20.23%, CAGR floor 10.59%), SPY OOS 15.26% / 0.8739 / -33.72% and RULES v2 OOS 1.1019 Sharpe. U56
PREREG (W/H=504/g=0.60) likewise holds 4b on both windows at both delays. **But with
rho(IS dMaxDD, OOS dMaxDD) = -0.07, one panel out of three is not evidence that reading IS fragility
works** — it is the coin-flip this record has learned to distrust. Path 4a fires **0 of 288 cells**.

**7. A gate that failed, recorded rather than dropped.** G7's first draft asserted the realised
contiguous holding spell was <= H + one cadence gap, and failed on all 144 books. The brake was not
violated: it drops a name at age H, the screen may re-take it the same day, and **30.7% of fresh
picks are such immediate re-entries**, so a spell runs **1.75x H on average (1.02-4.82x)** with no
trade. G7 now asserts the brake's true invariant (max age-since-entry among held names < H, which
holds on all 72 frames) and the age regressor is documented as the *economic* holding age.

**SURVIVORSHIP (rule 9).** U56 and B136 are current-constituent lists and SMALL a current sub-$2B
screen carried back to 2010, so every absolute level and every pass count is an upper bound. The
headline is a *difference* between two execution timings over the same names on the same days, and a
regression of that difference on two same-book statistics; the bias cannot manufacture either.

**WHAT THIS CHANGES.** Nothing in RULES.md (rule 6: Sunday review only). It closes the shortcut idea
1596 proposed: **a book's own turnover path and its own realised holding age do not tell capital
whether that book is latency-robust.** Idea 1592's proposal — restating PROTOCOL 4b on a
latency-averaged or worst-case DD statistic, read directly per book — is the surviving route, and
this run supplies the reason it has to be: 11 of 144 books change their OOS 4b verdict on one day of
timing, and no summary statistic sorts them.
