# Idea 119 — `V1u-small-negative-price` (lane B, 2026-09-05)

**Verdict: KILL as a citable finding.** The number reproduces exactly, but it is not a price
and it is not a free lunch. The queue's own wording is wrong on the count (5 of 6 priceable
arms, not 6 of 6), the ratio's **denominator has no stable sign** — it flips with the cost
assumption and is a coin flip across name draws — and the whole ±1.7 pp/yr effect is produced
by **1.9% of the book's held name-weeks**. The panel-artefact diagnosis the queue proposed is
half right and for the wrong reason: it is not survivorship and not turnover, it is the
**inverse-vol scaler** interacting with a 5-name book, and the sign is **not** small-panel
specific — it appears on u56 and broad too, at one eighth the size. Nobody should cite it.
One weaker sub-claim survives the audit and is queued, not adopted.

Script `2026-09-05_v1u-small-negative-price_B.py`, console
`2026-09-05_v1u-small-negative-price_B.console.txt`, 11 CSV companions.

## What was on trial

Idea 97's `V1u/small` price column. `V1u` = idea 94's ungated live-rules book: composite
(mean pct-rank of 12-1, 6m, 3m) ÷ √(vol20 clipped at 0.08), top **5** names at 15% each
(75% gross), weekly, next-day execution. `small` = 439 sub-$2B names, SPY held out. Price =
(CAGR_control − CAGR_arm) / (|MaxDD_control| − |MaxDD_arm|) in pp, undefined below 0.10 pp of
drawdown bought. A **negative** price means the gate delivers more CAGR *and* less drawdown.

## A. Reproduction — exact, and the queue's count is wrong

Idea 94's simulator imported unchanged: engine-equivalence max|diff| **0.000e+00**;
`EWall+vol60-dg` on u56 reproduces to 1.133 / 11.6% / −16.9% (published values); the
parameterised book asserts **identical** to `H.targets('V1u', …)` across all 11 specs.
`V1u/small` control @10 bps: **7.05% / 0.537 / −34.02%, 33.3x/yr turnover** (idea 97: 32x).

| arm | dCAGR pp | dMaxDD pp | rate | dSharpe |
|---|---|---|---|---|
| g200-dg | −0.191 | +0.566 | **−0.339** | +0.018 |
| g200-rw | −1.681 | +1.189 | **−1.414** | +0.097 |
| band3-dg | +0.333 | +0.551 | **+0.604** | −0.017 |
| band3-rw | +0.159 | −3.087 | — | −0.028 |
| abs12-dg | −0.130 | +0.051 | — | +0.016 |
| abs12-rw | −1.310 | +3.282 | **−0.399** | +0.084 |
| vol60-dg | +0.138 | −0.000 | — | −0.006 |
| vol60-rw | +0.525 | −0.000 | — | −0.033 |
| v1gate-dg | −0.304 | +0.566 | **−0.537** | +0.027 |
| v1gate-rw | −1.102 | +1.189 | **−0.927** | +0.065 |

Range −1.414…+0.604, dSharpe on the negative arms +0.018…+0.097 — idea 97's −0.34…−1.41 and
+0.02…+0.10 reproduce exactly. But **only 6 of 10 arms are priceable and only 5 of those are
negative**: `band3-dg` prices **+0.604**, and `band3-rw` buys −3.09 pp (makes drawdown worse).
The queue's "**every** gate prices NEGATIVE … 6/6 arms" is **FALSE** — withdraw "every".

## B. Turnover / cost (queue hypothesis 2) — REFUTED for the numerator, CONFIRMED for the denominator

The gate barely changes turnover (control 33.31x/yr, arms 32.6–33.9x), so it saves almost no
cost. Median gate dCAGR is negative at **every** cost — 0 bps −0.112, 5 −0.137, 10 −0.161,
25 −0.228, 50 −0.326 pp, with dCAGR < 0 in **6/10 arms at all five cost levels**. The extra
return is not a commission rebate. **P1 refuted.**

The drawdown half is the opposite. At 0 bps the two headline arms **flip sign**:
`g200-rw` dMaxDD +1.189 pp @10 bps → **−1.274 pp @0 bps** (arm −29.3% vs control −28.0%),
same for `v1gate-rw`; both become unpriceable. `dMaxDD > 0` holds in 5/10 arms at 0 bps and
9/10 at 25 bps. The drawdown "purchase" is an artefact of charging 33x/yr of turnover: costs
deepen the control's drawdown faster than the arm's. **A ratio whose denominator changes sign
between 0 and 10 bps is not a price.**

## C. Concentration × scaler (queue hypothesis 3) — CONFIRMED, and the scaler is the bigger half

n ∈ {5,10,20,40} × inverse-vol scaler {on,off}, gross fixed at 0.75, 32 points all reported.

| | n=5 | n=10 | n=20 | n=40 |
|---|---|---|---|---|
| scaler **on** (V1u) | neg **3/3** priceable | **3/3** | **2/3** | **0/3** |
| scaler **off** | 0/0 | 0/1 | 0/2 | 0/3 |

Negative prices need **both** a 5-name book and the scaler, and decay monotonically in n. With
the scaler off, **not one** of the 6 priceable cells is negative, and the gates buy ≈ 0
drawdown (dMaxDD −0.000 at n=5 and n=10) — unscaled top-5 momentum names are essentially
always above their own 200d MA, so there is nothing for the gate to do.

The level is the real story. Turning the scaler **off** at n=5 takes the control from
**7.05% → 18.72% CAGR** (0.537 → 0.690 Sharpe, MaxDD −34.0% → −39.8%) at *lower* turnover
(33.3x → 21.5x). The
inverse-vol scaler destroys **11.7 pp/yr** of CAGR on this panel; the celebrated free lunch
recovers at most **1.7 pp** of it. It is not an edge — it is a partial repair of a known
defect (CHANGELOG 2026-09-03: "the v1 score has zero cross-sectional IC because /√vol20
cancels momentum"). **P2 confirmed** (with the vanishing point at n=40, not n=20).

## I. Mechanism — the gate binds on 8% of weeks and 1.9% of name-weeks

| arm | dates changed | mean names gated out (of 5) | med vol20 gated out | med vol20 kept |
|---|---|---|---|---|
| g200-* | **66/817 (8.1%)** | 0.094 | **0.095** | 0.173 |
| band3-* | 162/817 (19.8%) | 0.226 | 0.042 | 0.176 |
| abs12-* | 81/817 (9.9%) | 0.111 | 0.129 | 0.174 |
| vol60-* | **6/817 (0.7%)** | 0.013 | 0.660 | 0.173 |
| v1gate-* | 68/817 (8.3%) | 0.105 | 0.120 | 0.173 |

The 200d gate replaces ≈ **77 name-dates out of 4,074 held name-dates (1.9%)**. A 1.7 pp/yr
CAGR difference and a 1.2 pp MaxDD difference generated by 1.9% of the book's holdings is a
handful of trades, not a property of a rule. It also explains the whole `dg`/`rw` spread
(−0.19 vs −1.68 pp on identical binding dates): the difference is entirely *what refills the
slot* — the 6th-ranked name at full weight, versus cash.

And it names the mechanism exactly: the gate removes the book's **lowest-vol** picks
(median vol20 **0.095** vs 0.173 kept). The scaler picks names at median vol20 **0.173**
against a panel median of **0.399** (scaler off: 0.634) — it is a low-vol selector, and the
200d gate's contribution is deleting the small subset of low-vol names that are also in
downtrends. Two known-broken components partly cancelling is not a discovery.

## D. Name sampling — the numerator is robust, the denominator is a coin flip

80 seeded sub-panels of 220 of the 439 names, composite / gates / ranks recomputed inside each
draw, arm `g200-rw` @10 bps:

- dCAGR < 0 (gate adds return): **61/80**, median −0.433 pp, range [−1.72, +1.16]
- dMaxDD > 0 (gate cuts drawdown): **49/80**, median +0.699 pp, range **[−8.75, +7.79]**
- dSharpe > 0: 59/80, median +0.023
- **both** dCAGR<0 **and** dMaxDD>0 — the free lunch as stated: **40/80 = 50.0%**
- rate < 0: 38/47 priceable — but **33 of 80 draws are unpriceable** (|dMaxDD| ≤ 0.10 pp)

**P3 refuted as literally worded** (81% of *priceable* draws are negative) **and the finding
still dies**: the free-lunch condition itself is an exact coin flip, and the denominator's
across-draw range (±8 pp) is seven times the full-panel value (+1.19 pp) it is computed from.
The extra-return half is real and modest; the ratio is not a measurable quantity.

## E. Time structure — the one axis where it holds

Leave-one-year-out on the full-sample price: the sign flips to ≥ 0 in **0 of 16** year
deletions for all five negative arms (g200-dg range [−0.657, −0.030], g200-rw [−1.697,
−0.766]). Not a one-year artefact. Per-episode: the control has 5 drawdown episodes deeper
than 10%; the arms are shallower in 3–4 of 5, and the whole-window MaxDD is set by the last
one (2021-11 → 2026-03, −33.8%), where g200-rw gains +1.19 pp and gives back −0.34 pp in the
2018–2020 episode. **P4 not supported** — dMaxDD is not one episode; it is small and mixed.
Annual returns are *identical to 4 dp* in 2013, 2017 and (for the dg arms) 2021 — the same
non-binding shown in test I.

## G. Portability — the sign is NOT small-panel specific (correction to idea 97)

Same book, same 10 arms, 10 bps: on **u56** 4 of 8 priceable arms price negative
(g200-rw −0.184, band3-rw −0.125, abs12-rw −0.111, v1gate-rw −0.084); on **broad** 2 of 3
(g200-rw −0.118, v1gate-rw −0.076). The two families that price on **all three** panels —
`g200-rw` (−1.414 / −0.184 / −0.118) and `v1gate-rw` (−0.927 / −0.084 / −0.076) — are negative
everywhere; `abs12-rw` is negative where it prices (small −0.399, u56 −0.111) and `band3-rw`
is the exception, +0.152 on broad and unpriceable on small. The queue framed this as a
439-name-panel anomaly; it is not. What is small-panel specific is the
**magnitude** (−1.41 vs −0.18, ~8x), which follows from C: the small panel is where the
scaler's low-vol tilt is most destructive. Idea 97's C1 statement ("per-name gate < static
gross lever") was derived on `EWall`/`TOP20`; on `V1u` it fails on **all three** panels in the
rw convention, not just on `small`. That is a genuine widening of idea 97's caveat.

## F. Capacity — the price cannot be paid at any size

20d median dollar volume of the names actually held, 4,074 name-dates:
**p5 $0.00M · p25 $0.87M · p50 $4.33M · p75 $11.55M · p95 $45.36M**. The book trades **0.64 of
NAV per weekly rebalance** in 15% positions.

| capital | position | % of median held name's daily $ volume |
|---|---|---|
| $1M | $0.15M | 3.5% |
| $10M | $1.50M | **34.6%** |
| $100M | $15.0M | **346%** |

**P6 confirmed.** A −1.7 pp/yr effect produced by 77 substitutions in names with $1–4M of
daily volume is smaller than the impact of the trades that would realise it. The 10 bps
PROTOCOL cost is a fiction on this book, and test B shows the entire drawdown half of the
result is a function of exactly that fiction.

## H. PROTOCOL rules 3, 4, 8

SPY on this window 14.13% / 0.862 / −33.72% (halves 0.891/0.858, OOS 15.45% / 0.882 /
−33.72%). Live RULES v1 on the small panel @10 bps: 8.15% / 0.603 / −32.84% (halves
0.689/0.526, OOS 0.581). 4b bars: Sharpe > 0.891/0.858/0.882, MaxDD ≤ 20.23%, CAGR ≥ 9.89%.

**4b: 0 of 43 arm-points. 4a: 0 of 11.** Every V1u/small arm fails all five 4b tests
simultaneously (H1, H2, OOS, DD *and* CAGR) — the negative price is a comparison between two
books that are both far worse than SPY. Best arm `g200-rw`: 8.73% / 0.634 / −32.84%.

**Rule 8 walk-forward** (parameters on 2010–2016 only, 2017–2026 untouched). Both
pre-registered selectors — S1 (idea 94's argmin IS price among IS dMaxDD ≥ 1 pp) and S2
(argmax IS Sharpe) — pick `g200-rw`:

| | CAGR | Sharpe | MaxDD |
|---|---|---|---|
| **pick `g200-rw` OOS** | 8.86% | 0.631 | −32.84% |
| live RULES v1 OOS | 7.92% | 0.581 | −32.84% |
| **SPY OOS** | **15.45%** | **0.882** | −33.72% |
| pick, full sample | 8.73% | 0.634 | −32.84% |

The pick beats the live book by +0.94 pp CAGR / +0.050 Sharpe at identical drawdown and loses
to SPY by −6.6 pp CAGR / −0.251 Sharpe at the same drawdown. **P5 confirmed.** And the price's
own sign does not survive the split: IS→OOS sign agreement **2/4** (`g200-dg` prices **+0.041
IS → −0.612 OOS**; only 4 arms are priceable in both windows).

## Prediction scorecard

- **P1 REFUTED.** dCAGR stays negative at 0 bps (−0.112 pp). Not a commission rebate — but
  the *denominator* is: dMaxDD flips sign at 0 bps on both headline arms (unpredicted).
- **P2 CONFIRMED**, vanishing at n=40 rather than n=20; the scaler axis is cleaner than the n
  axis (0 negatives in 6 priceable cells with the scaler off).
- **P3 REFUTED as worded** (81% of priceable draws), **but** 33/80 draws are unpriceable and
  the joint free-lunch condition is 40/80 — the intended test passes on the intended meaning.
- **P4 NOT SUPPORTED.** Shallower in 3–4 of 5 episodes, not ≤ 60%.
- **P5 CONFIRMED.** 0/43 4b passes; WF pick OOS Sharpe 0.631 < SPY 0.882.
- **P6 CONFIRMED.** 34.6% of median held-name ADV at $10M.

## Caveats

- **SURVIVORSHIP (queue hypothesis 1) is untestable from inside the panel, and its direction
  is the opposite of the queue's presumption.** The panel is the current constituent list, so
  the missing names are the ones that went to zero — exactly the cohort a 200d/vol gate
  excludes. Their absence flatters the **ungated control** and therefore *understates* the
  gate's advantage. Survivorship cannot manufacture a negative gate price here; it can only
  shrink one. It does inflate every **level** in this run, which is why nothing here is quoted
  as an achievable return. Test D is a composition-risk proxy, not a fix. Settling hypothesis
  1 properly needs a delisting-aware panel (open idea 54).
- 817 rebalance dates and 5 drawdown episodes. The episode counts (3/5, 4/5) carry no weight.
- The 200d/3%-band/0.60-vol/12m constants are inherited from ideas 94/97 and were not
  re-opened; only n and the scaler were swept, and every point is reported.
- The small panel is trading-day indexed and starts 2010, so its IS window is 2010–2016 and it
  misses the 2009 rebound; u56/broad still carry the unfixed calendar-day index (open idea 38).
  Within-cell deltas — everything that is a *result* here — are unaffected.
- Test D resamples names, not time; it bounds composition risk, not regime risk.

## What may and may not be said now

**May not be said:** "on the small panel a per-name gate is free insurance", "gates price
negatively on small caps", or any use of −0.34…−1.41 as a number. The denominator is not
sign-stable across costs (test B), across name draws (test D) or across the rule-8 split
(test H), and the effect is 1.9% of the book's name-weeks (test I) in names that cannot absorb
the trade (test F).

**May be said, with the mechanism attached:** on a top-5 **inverse-vol-scaled** momentum book,
the `g200`/`v1gate` rebuild-in-gate (`-rw`) convention adds CAGR on **all three** panels
(dCAGR −0.156…−1.681 pp, dSharpe +0.001…+0.097), because it deletes the lowest-vol names the
√vol scaler over-promotes. This is further evidence for the project's standing finding that
the scaler is the defect — and the direct fix is worth **11.7 pp/yr**, not 1.7: delete the
scaler.

## Follow-ups (queued)

120. `delete-the-scaler-on-small` — turning off /√vol20 at n=5 on the small panel is worth
     **+11.7 pp of CAGR and +0.15 Sharpe at lower turnover** (18.72%/0.690/−39.8% vs
     7.05%/0.537/−34.0%), the largest single-component effect this project has measured on any
     panel. Sweep n and gross for the unscaled book against 4b's bars with a liquidity screen
     applied first, since test F shows the top-5 small-cap book is uninvestable above ~$1M.
121. `liquidity-screened-small-panel` — every small-panel result in this project (ideas 31,
     38, 49, 50, 51, 54, 97, 119) is computed on names whose median held-name dollar volume is
     $4.3M and whose p25 is $0.87M. Add an ADV floor to `load_universe(small=True)` callers as
     a PROTOCOL clause and re-run the rows whose verdicts could move.
122. `price-denominators-need-a-sign-test` — idea 97 published a price list whose denominator
     (ΔMaxDD) is here shown to flip sign between 0 and 10 bps and to be a coin flip across
     name draws. Propose a PROTOCOL rule that no ratio is quoted unless its denominator's sign
     survives a stated perturbation, and re-check idea 94's u56/broad price list under it.
