# Idea 659 — publish-the-SIGN-BALANCE-of-every-fitted-SELECTOR-TARGET (lane C, 2026-09-10)

**ANSWERED. The constancy half of the premise is CONFIRMED and quantified; the flip half is
FALSIFIED. Across 3,104 committed CSVs, 721 files carry a paired-difference selector target —
1,723 targets in all — and their median sign balance is 0.8438; **495 (28.7%) are exactly
one-signed, i.e. no choice exists at all**. Refitted out of fold on their own study's
properties, 561 of 1,617 (34.7%) fitted selectors emit ONE value on every row and 616 (38.1%)
add nothing over the best constant, with the literal-constant rate rising monotonically
0.0% → 1.4% → 4.8% → 9.1% → 21.1% → 63.8% → 100% across sign-balance buckets
(Spearman(sign balance, OOF lift) = **−0.8706**). But idea 497's IS→OOS *sign flip* is an
OUTLIER, not the record's habit: over the 90 targets committed as a matched IS/OOS pair the
majority side flips on **6/90 = 6.7%** and Spearman(IS share>0, OOS share>0) is **+0.9308**.
Rule 8 run live reproduces the collapse: 8 of 16 fitted property→dial selectors pick one dial
value for both buckets, all 8 onto the IS-argmax constant, and the fitted set beats its own
constant OOS 1/16 of the time (mean OOS Sharpe 1.1566 vs 1.1958). 4a 1/31 arms, 4b 3/31 —
and **every one of those passes is a constant**. No KEEP claimed, no RULES change; RULES.md,
PROTOCOL.md, scan.py, bot.py and baseline.py untouched.**

Script `2026-09-10_publish-the-SIGN-BALANCE-of-every-fitted-SELECTOR-TARGET_C.py`; console
`.console.txt`; CSVs `.targets.csv` (1,723 targets), `.censusgrid.csv` (18 grid points),
`.constancy.csv` (1,617 OOF refits), `.grid.csv` (16 live selectors), `.walkforward.csv`
(31 arms). Standalone, deterministic (seed 659), ~2 min. Reads only committed artefacts +
`research/baseline.py`.

---

## (0) Gates — both pass

**G1.** `RULES.md`'s acceptance table was computed on the **2026-09-04** price vintage; the
committed cache now runs to 2026-09-09. On the published vintage the live book reproduces at
8.6601% / 1.2056 / −12.0549% / 1.2259 / 1.1909 against the published 8.66% / 1.2056 /
−12.05% / 1.2259 / 1.1908 — **max |Δ| 5.13e-05**. On the current vintage (used everywhere
below) it reads 8.6317% / 1.2021 / −12.0549% / 1.2309 / 1.1798: three extra sessions move the
halves split by +0.0049 / −0.0110. That is a data-vintage fact, reported not hidden.

**G2 (provenance).** Idea 497's own target, `IS_Sharpe(M) − IS_Sharpe(6W)`, rebuilt from idea
175's committed `ladder.csv` over its 115 books: IS share>0 **0.9478** (published 0.948), OOS
**0.2696** (published 0.270), Spearman **−0.1801** (published −0.1801) — max |Δ| 4.35e-04.

## The instrument

A *selector target* is a per-row **paired difference** committed to a CSV — the number whose
sign says which arm a chooser should pick. For each one,

    sign_balance = max(share(t > 0), share(t < 0))    over finite non-zero rows
    headroom     = 1 − sign_balance

is the largest share of rows any non-constant selector could ever add over the best constant
arm. "Constant in disguise" is then **measured, not asserted**: the target's sign is refitted
out of fold (K=5, seed 659, standardised ridge λ=1, standardisation on the TRAIN fold only) on
that study's own numeric columns and ≤10-level categoricals, **excluding every other paired
difference** (another delta is an outcome, not a property) **and anything reconstructing the
target at |corr| ≥ 0.99**. LITERAL = the OOF rule emits one value on every row; NO LIFT = its
OOF accuracy does not beat the OOF best constant.

**Params (2): study set ∈ {CHOOSER, SELECTOR, ALL}, sign-balance bar b ∈ {0.60 … 0.99}.**

## (1) The census — 18 grid points, all reported

| study set | files | targets | b=0.60 | 0.70 | 0.80 | 0.90 | 0.95 | 0.99 |
|---|---|---|---|---|---|---|---|---|
| CHOOSER (stem text) | 96 | 223 | 198 (88.8%) | 160 (71.7%) | 121 (54.3%) | 97 (43.5%) | 90 (40.4%) | 84 (37.7%) |
| **SELECTOR (artefact)** | 132 | 250 | 210 (84.0%) | 168 (67.2%) | 134 (53.6%) | 113 (45.2%) | **105 (42.0%)** | 100 (40.0%) |
| ALL | 721 | 1723 | 1505 (87.3%) | 1283 (74.5%) | 1001 (58.1%) | 708 (41.1%) | 591 (34.3%) | 508 (29.5%) |

CHOOSER is a **static stem match** and is reported only because the queue names that
population; SELECTOR (the file carries a committed `pick`/`selector`/`chosen` column) is
artefact evidence and is the set to quote. The two agree to within 2.6pp at every bar, which
is the one place a static flag has survived a re-read in this record.

sign_balance over all 1,723 targets: min 0.5000, q25 0.6959, **median 0.8438**, q75 1.0000.

## (2) How many fitted selectors are constants in disguise

1,617 targets refit out of fold (median 21 predictors). **Literal 561 (34.7%), no lift 616
(38.1%).** Spearman(sign_balance, OOF lift) = **−0.8706**.

| sign-balance bucket | n | literal | no lift | mean OOF lift |
|---|---|---|---|---|
| [0.50,0.60) | 205 | 0.0% | 0.5% | +0.3252 |
| [0.60,0.70) | 211 | 1.4% | 5.2% | +0.2279 |
| [0.70,0.80) | 273 | 4.8% | 6.2% | +0.1615 |
| [0.80,0.90) | 285 | 9.1% | 14.4% | +0.0794 |
| [0.90,0.95) | 114 | 21.1% | 37.7% | +0.0224 |
| **[0.95,1.00)** | **94** | **63.8%** | **72.3%** | **+0.0060** |
| = 1.00 (degenerate) | 435 | 100.0% | 100.0% | +0.0000 |

The last row is a tautology — with every row one-signed a constant is the only possible
answer — so it is separated, not folded in. Dropping those 435, the record's rate is literal
10.7% / no lift 15.3% over 1,182 targets; **the non-tautological finding is the 94 targets at
0.95 ≤ sb < 1, where a choice does exist and 63.8% of fitted selectors still emit one value
and 72.3% add nothing.** Sign balance is therefore a *pre-registrable* screen: publish it
beside a selector and a reader knows, before reading the fit, roughly whether the fit can be
anything but a constant.

## (3) The IS→OOS flip is idea 497's outlier, not the record's habit

90 targets over 69 files are committed as a matched IS/OOS pair of the same quantity. IS
sign_balance median 0.8037, OOS 0.8433; **the majority side flips on 6/90 = 6.7%** and
Spearman(IS share>0, OOS share>0) = **+0.9308**. Idea 497's own pair (0.9478 → 0.2696,
Spearman −0.1801) sits far outside that distribution. So the queue's implied generalisation —
that one-signed IS targets routinely reverse out of sample — is **false**. What generalises is
the *constancy*, not the *reversal*: a one-signed target makes the selector a constant either
way, and whether that constant then loses OOS is a separate, much rarer event.

## (4) PROTOCOL rule 8 — the same question run live on prices

Four weight-level dials × four market properties, 31 arms in `.walkforward.csv`. Bucket
threshold = IS median of the property, per-bucket arm = IS-Sharpe argmax, **everything fitted
on 2009-2016 only**, 2017-2026 untouched.

- **8/16 fitted selectors collapsed** (both buckets picked the same dial value); **all 8 onto
  the IS-argmax constant arm**.
- IS sign balance of rival-minus-constant is 0.5320 at day granularity but **0.6250 at the
  126-day book granularity a chooser actually reads** (gross 0.733, volcap 0.667, topn 0.567,
  band 0.533) — the census's unit matters, and Spearman(sb_window, collapsed) = +0.2236 over
  only 16 selectors is far too thin to carry the census's −0.8706. Stated as a limit, not a
  confirmation.
- The fitted selector beats its own constant-dial arm OOS **1/16 = 6.2%**; mean OOS Sharpe
  **1.1566 vs 1.1958 (Δ −0.0392)**.

| arm | CAGR | Sharpe | MaxDD | H1 / H2 | OOS CAGR | OOS Sharpe | 4a | 4b |
|---|---|---|---|---|---|---|---|---|
| LIVE RULES v2 | 8.63% | 1.202 | −12.05% | 1.231 / 1.180 | 9.48% | 1.279 | — | — |
| SPY | 15.15% | 0.886 | −33.72% | 0.959 / 0.826 | 15.32% | 0.876 | — | — |
| gross:g=1.00 (constant) | 11.55% | 1.202 | −15.91% | 1.231 / 1.179 | 12.71% | 1.278 | 0 | **1** |
| gross←BREADTH *(collapsed to g=1.00)* | 11.55% | 1.202 | −15.91% | 1.231 / 1.179 | 12.71% | 1.278 | 0 | **1** |
| gross←SPYTREND *(collapsed to g=1.00)* | 11.55% | 1.202 | −15.91% | 1.231 / 1.179 | 12.71% | 1.278 | 0 | **1** |
| band←SPYVOL *(LOW b=0.01, HIGH b=0.03)* | 8.72% | 1.219 | −12.05% | 1.237 / 1.207 | 9.61% | 1.302 | **1** | 0 |
| topn:n=5 (constant) | 30.78% | 1.137 | −36.53% | 1.292 / 1.046 | 30.98% | 1.057 | 0 | 0 |

**KEEP paths: 4a 1/31, 4b 3/31.** All three 4b passes are `gross = 1.00` — the constant — or an
arm that *collapsed onto* it, so **every 4b pass here is a pure exposure fact and not a
chooser result** (which is idea 657's open question, answered here for this grid).

**The single 4a pass is not a KEEP.** `band←SPYVOL` clears 4a only because its MaxDD **ties**
the live book to 6dp (−0.120549 vs −0.120549) and PROTOCOL's `≥` passes ties silently (idea
603/594's point). Its Sharpe margin over the book it must replace is +0.0170 full-sample, it
is **1 of 16 fitted arms**, its H1 leg is scored on the window it was fitted on, and on the
cost ladder `RULES.md`'s own acceptance requires it holds 4a at 5 and 10 bps and **fails at 25
and 50 bps** (1.1724 vs 1.1645 is a Sharpe win but the DD leg goes; at 50 bps it loses outright,
1.0945 vs 1.1018). Reported, not promoted: no memo, no Sunday-review item.

## What to carry forward

1. `sign_balance` is cheap, pre-registrable, and predicts selector constancy at −0.87. It
   belongs beside every published selector, exactly as the queue asked.
2. 28.7% of the record's selector targets admit **no choice at all**. Those studies did not
   find that a property cannot choose a dial; they never posed a choice.
3. Idea 497's IS→OOS reversal does **not** generalise (6.7% of matched pairs). Do not quote
   0.948→0.270 as a property of the record.

## Caveats

Survivorship: `research/universe.json` is current constituents (56 names). The live leg's
16 selectors are one bucketing (IS median, two buckets) of four dials and four properties, and
`sb_window` on 16 points cannot confirm the census relation — only fail to contradict it. The
census's DELTA regex is a column-name instrument: a paired difference committed under a name it
does not match is invisible to it, so 1,723 is a lower bound on the record's selector targets.
