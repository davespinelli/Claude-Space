# idea 93 — absorbing-state-audit-of-every-state-dependent-rule (lane B, 2026-09-05)

**Verdict: ANSWERED. The absorbing pathology is CONFIRMED and its diagnosis is CORRECTED and
generalised; the fix the QUEUE proposed (exogenous re-entry) is a KILL as an improvement — it
removes absorption at zero Sharpe benefit and *negative* drawdown benefit. No RULES change, no
new KEEP, nothing promoted.**

Script `2026-09-05_absorbing-state-audit_B.py`; console `…console.txt`; CSVs `…ddctl.csv`
(1452 rows), `…stop.csv` (396), `…ladder.csv` (228), `…walkforward.csv` (78). All grid points
reported. Harness sanity: **both** controls reproduce `engine.backtest` at max|diff| **0.0e+00**
on both universes, and the `V1` control reproduces the live book (u56 @10bps 6.45%/0.664/-13.83%)
and `CAND20` reproduces idea 2's standing KEEP-candidate (12.66%/1.092/-18.31%) to the decimal.

Grid: 3 books (V1 live / CAND20 idea 2 / EWall idea 72) × 2 universes (u56 56, broad 136) × 2 cost
rungs (10, 25 bps) × two families. DDCTL: 5 reset arms × D∈{4,6,8,10,12,15}% × k∈{0,0.25,0.50,0.75}
+ control. STOP: 4 re-entry arms × 2 arming arms × s∈{10,15,20,25}% + control. Exactly 2 tuned
parameters in DDCTL (D, k) and 1 in STOP (s); reset / re-entry / arming are ARMS, run in full, and
every walk-forward selection is confined inside one arm.

---

## 1. P1 — the absorbing state is EXACT, not approximate (CONFIRMED)

At k = 0.00 with an endogenous reset (`high` = new equity high, `recover` = drawdown shallower
than D/2), the book goes entirely to cash while armed, so its equity is constant, so the drawdown
that armed it is frozen below both release thresholds. Empirically, over the 144 (arm, cell, cost)
points at k=0:

| | armed ≥ once | of those, **never disarmed** | mean captured episode | still cut on the last day |
|---|---|---|---|---|
| `high` + `recover`, k=0 | 140 / 144 | **140 / 140 (100%)** | **724 rebalances** (median 844, max 919 = the entire remaining sample) | 140 / 140 |

The 4 exceptions never armed at all (D=15% is never reached by u56/V1 and u56/CAND20 at 10 bps),
so they are not counterexamples. **A drawdown control with equity-conditioned re-entry and a full
cut is a one-way door: it fires once, in 2009–2011 or 2020, and the book is in cash for the rest
of its life.** Any published result for such an arm is a result about a cash position.

## 2. P2 — near-absorption at k > 0 scales as predicted (CONFIRMED)

Mean cut-episode length in rebalances, averaged over all 6 cells × 2 costs:

| k | `high` | `recover` | `spy200` | `t8` | `t26` |
|---|---|---|---|---|---|
| 0.00 | **724.0** | **724.0** | 1.5 | 8.0 | 25.6 |
| 0.25 | 218.2 | 125.8 | 1.7 | 8.0 | 25.8 |
| 0.50 | 108.9 | 55.9 | 2.4 | 8.0 | 25.9 |
| 0.75 | 69.1 | 38.0 | 3.0 | 8.0 | 25.9 |

Episode length under an endogenous reset is roughly ∝ 1/k — the cut is what slows the recovery
that is required to un-cut it. The exogenous arms are flat in k, which is the signature of a
release condition the action cannot touch. Cut-day fraction moves the same way (`high` 76.4% → 39.7%).

## 3. P3 — exogenous re-entry does remove absorption (CONFIRMED)

Over all 288 arms per reset (every k, D, cell, cost):

| reset | absorbed (armed, never released) | armings | releases | escape rate |
|---|---|---|---|---|
| `high` | **86** | 1177 | 1030 | 0.875 |
| `recover` | **76** | 1671 | 1543 | 0.923 |
| `spy200` (exogenous) | **0** | 42152 | 42145 | **1.000** |
| `t8` (exogenous) | **0** | 11393 | 11308 | 0.993 |
| `t26` (exogenous) | **0** | 4724 | 4612 | 0.976 |

## 4. P5 — my sharp claim is FALSIFIED, and the correct diagnosis is narrower than "endogenous"

I pre-registered that a per-name stop whose re-entry reads the NAME's own price would *not* be
absorbing, because the name keeps trading whether or not we hold it. That is wrong. Over the 384
treated STOP arms:

| re-entry | high-water mark? | fires | releases | **release rate** | mean block (trading days) | names still blocked at the end | mean ΔSharpe |
|---|---|---|---|---|---|---|---|
| `free` | no | 27114 | 27088 | **0.999** | 2.6 | 0.27 | -0.014 |
| `spy200` | no | 24162 | 24136 | **0.999** | 35.3 | 0.27 | -0.015 |
| `nhigh` (name's own pre-stop peak) | **yes** | 16428 | 15624 | **0.951** | **250.9** | 8.4 | -0.055 |
| `bookhigh` (book's equity high) | **yes** | 9670 | 8346 | **0.863** | **285.4** | 13.8 | -0.153 |

Both high-water-mark arms are near-absorbing; neither non-HWM arm is, and `spy200` is exogenous
while `free` is not — so **exogeneity is not the operative property**. The operative property is
that the re-entry condition demands the state variable regain a peak it has just fallen away from.
A name stopped out 20% below its high needs +25% to be re-eligible, which is why `nhigh` blocks for
a mean of 251 trading days and leaves 8.4 names permanently out. Idea 22's wording ("a function of
the book's own equity") is too narrow: it exonerates `nhigh`, which this run shows is the second
most absorbing rule the project owns.

The two-tier statement the evidence supports:
1. **High-water-mark re-entry ⇒ near-absorbing**, whatever the state variable (book equity, a name's
   price, anything with a running max).
2. **HWM re-entry on a variable the rule's own action FREEZES ⇒ exactly absorbing** — the k=0 book
   above, 140/140.

**Idea 75's conditional arming, audited on the same 192 paired arms.** Arming the stop only while
SPY is below its own 200d is mildly positive (mean ΔSharpe **+0.0328**, positive in 133 of 192), but
the gain is concentrated on exactly the absorbing arms — `bookhigh` **+0.073**, `nhigh` **+0.045** —
and is near zero on the two non-absorbing ones (`free` +0.007, `spy200` +0.007). Conditional arming
helps by firing a broken rule less often, not by timing anything. It does not rescue the family:
STOP is still Sharpe-negative against its own control in **277 of 384** arms.

## 5. P4 — the fix is not worth owning (CONFIRMED, and worse than predicted)

**5a. Sharpe.** Mean ΔSharpe against each arm's own control, over 288 arms each: `high` **-0.2636**,
`recover` -0.2639, `t26` -0.2450, `t8` -0.1890, **`spy200` -0.2633**. The exogenous fix is
Sharpe-*identical* to the pathology it cures (-0.2633 vs -0.2636). Worse in 267–275 of 288 arms in
every reset; the single best arm in the whole DDCTL grid is +0.0304.

**5b. Drawdown.** De-absorbing also removes the protection: `spy200`'s mean drawdown gain is
**-0.0325** — it makes MaxDD *deeper* than the control on average, in **140 of 288** arms, because
it re-levers as soon as SPY reclaims its 200d, which is mid-drawdown. It also more than doubles
turnover (19.8×/yr vs the control's 15.5× and `high`'s 9.3×). The endogenous arms buy drawdown
(+4.8 / +4.4 pp) precisely by being stuck in cash.

**5c. Idea 74's axis** (pp of CAGR surrendered per pp of MaxDD bought; static-gross ladder = 0.537
pp/pp on the same cells): DDCTL medians `high` 0.905, `recover` 0.936, `t26` 0.924, `t8` 0.772,
`spy200` 0.683 — dominated by the plain gross lever in **67%–90%** of arms. STOP medians: `bookhigh`
1.234 (dominated 91%), `nhigh` 0.822 (69%), `free` 0.351 (38%), `spy200` 0.366 (18%).

**5d. Both KEEP paths.** **0 of 1824 treated arms pass 4a and 4b together.**
- *4b*: every one of the 69 arm-passes sits in the single cell (u56/CAND20 @10bps) **whose control
  already passes 4b**; 20 of the 48 DDCTL passes never fired at all (D=15% unreached), and all 28
  that did fire have **negative** ΔSharpe (best -0.0028). In broad/EWall @10bps the control passes
  4b and **0 of 152** arms do — the instrument destroys the pass. **0 of 12 cells has any arm that
  converts a 4b failure into a 4b pass**, and 0 arms pass on both universes.
- *4a*: 598 of 1824 pass, but mean gross 0.629 vs the controls' 0.743 and mean ΔSharpe -0.1016,
  with only 45 of 598 beating their own control. 4a is being cleared by de-grossing against a
  low-return live book, which is exactly what PROTOCOL rule 4b exists to stop counting.

## 6. PROTOCOL rule 8 — walk-forward (params on 2009–2016 only, OOS 2017–2026 read once)

78 selections (S1 = argmax IS Sharpe inside one arm, control included). SPY OOS 15.45%/0.882/-33.7%;
RULES v1 OOS 7.73%/0.747/-13.8% (u56) and 5.94%/0.576/-21.2% (broad).

- S1 moves off the control in 69 of 78 nominally but **65 materially** (4 picks are the never-firing
  D=15% arm, numerically identical to the control).
- Among the 65 material moves: **mean OOS Sharpe vs control -0.1706**, beats control in **15**,
  worst -0.844, best +0.031. By family: DDCTL 27 moves, mean **-0.3177**, beats control 2, beats SPY
  6 of 30; STOP 38 moves, mean -0.0325, beats control 13, beats SPY 24 of 48.
- The 4b-aware selector S2 **picks nothing in 59 of 78** cells; in the 19 where it picks, mean OOS
  Sharpe 0.859 against the control's 0.979.

Tuning either instrument on in-sample Sharpe is OOS-negative on both families and on both universes.

## 7. What this changes

Nothing in RULES (no KEEP, no candidate). What it changes is how the project may write a
state-dependent rule: see `2026-09-05_absorbing-state-audit_B.memo.md` for the proposed negative
clause and the one-line audit test. The `nhigh` result also puts a footnote on idea 9's per-name
trailing stop: whichever re-entry convention that run used should be checked against §4 before its
numbers are quoted as a stop's numbers rather than a partial-cash book's.

SURVIVORSHIP: universe.json and universe_broad.json are current-constituent lists, so all absolute
CAGRs are optimistic. Every claim here is a within-cell delta on shared days, which is far less
exposed than the levels.
