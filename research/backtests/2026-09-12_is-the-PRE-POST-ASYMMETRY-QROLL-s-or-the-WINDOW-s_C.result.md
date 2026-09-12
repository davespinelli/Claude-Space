# Idea 834 — is the PRE/POST asymmetry QROLL's or the WINDOW's?
lane C, 2026-09-12 · script `2026-09-12_is-the-PRE-POST-ASYMMETRY-QROLL-s-or-the-WINDOW-s_C.py`

**ANSWER: QROLL's at the record's own split — and the WINDOW's everywhere else.** At split
2016-12-31 QROLL's PRE→POST movement is +4.5σ outside a family-blind relabelling of the same 648
arms (p 0.0010), it survives both ceiling normalisations and, post-hoc, an arm-count-matched
corpus. But the split date is one of the two parameters the queue itself names, and moving it
destroys the claim: at 2018 **not one of 72 cells** is distinguishable (median p 0.9875) and at
2020 the movement is distinguishable with the **opposite sign** (POOLED −0.1597, SMALL663
−0.6181). Over the 360 QROLL-RAW cells of the 3,600 reported QROLL is distinguishable in **161**,
and 93 of the 360 ADV-RAW cells are significant while NEGATIVE. **KILL as a general claim; a
documented PASS at the 2014–2016 cut only.** No KEEP claimed, no book promoted, no memo. `RULES.md`, `PROTOCOL.md`, `research/scan.py`,
`products/bot/bot.py`, `research/baseline.py` untouched.

**The queue's own premise is arithmetically false.** It states ABS "moved further … than QROLL's in
absolute terms"; on 825's published numbers ABS moved +0.4074 and QROLL +0.4491. H_PREMISE was
pre-registered exactly as the queue words it so the record carries the correction.

## The headline (split 2016-12-31, P = 1,000, 10 bps, FULLMATCH, POOLED)

Null = the pooled arm set with **family labels permuted**, family sizes preserved, each arm keeping
its own (PRE, POST) pair. Two-sided p = (1 + #{|null| ≥ |obs|}) / (1 + P).

| stat | family | n | win PRE | win POST | delta | null μ | null σ | z | null 95% | p | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|
| RAW | ABS | 108 | 0.3333 | 0.7407 | +0.4074 | 0.3800 | 0.0513 | +0.53 | [+0.287, +0.482] | 0.3407 | indistinguishable |
| RAW | QEXP | 108 | 0.5833 | 0.6481 | +0.0648 | 0.3789 | 0.0522 | **−6.02** | [+0.278, +0.482] | 1.0000 | indistinguishable |
| RAW | QROLL | 432 | 0.5231 | 0.9722 | **+0.4491** | 0.3774 | 0.0158 | **+4.53** | [+0.347, +0.410] | **0.0010** | **DISTINGUISHABLE** |
| RAW | ADV | 648 | −0.0602 | +0.2315 | **+0.2917** | 0.0072 | 0.0529 | **+5.37** | [−0.090, +0.111] | **0.0010** | **DISTINGUISHABLE** |
| HEADROOM | QROLL | 432 | — | — | +0.9417 | 0.7578 | 0.0190 | +9.67 | [+0.721, +0.794] | 0.0010 | DISTINGUISHABLE |
| LOGODDS | QROLL | 432 | — | — | +3.4233 | 1.9736 | 0.0989 | +14.65 | [+1.789, +2.170] | 0.0010 | DISTINGUISHABLE |

So the asymmetry is **not a ceiling artefact** (QROLL uses 94% of its remaining headroom against a
null of 76%), and the family that is genuinely anomalous in the *other* direction is **QEXP**, 6.0σ
BELOW its own null: the record's "QROLL on top" is as much QEXP standing still as QROLL moving.

## It is a property of the CUT, not of the family — 4 of 12 hypotheses FAIL

| | verdict | evidence |
|---|---|---|
| H_PREMISE the queue's premise \|Δ ABS\| > \|Δ QROLL\| | **FAIL** | 0.4074 vs 0.4491 |
| H_QROLL QROLL distinguishable at the headline | **PASS** | +0.4491 vs null [+0.3472, +0.4097], p 0.0010 |
| H_ANYFAM some family distinguishable | **PASS** | ABS 0.3407, QEXP 1.0000, QROLL 0.0010 |
| H_ADV the adv movement distinguishable | **PASS** | +0.2917 vs [−0.0903, +0.1111], p 0.0010 |
| H_CEILING same verdict under HEADROOM and LOGODDS | **PASS** | p 0.0010 / 0.0010 / 0.0010 |
| H_SPLITFREE same verdict at all 5 splits | **FAIL** | 2012 0.2338 (+0.366), 2014 **0.0010** (+0.472), 2016 **0.0010** (+0.449), 2018 0.8851 (+0.181), 2020 **0.0010 (−0.160)** |
| H_PERMSTAB same verdict at P 200/1000/5000 | **PASS** | 0.0050 / 0.0010 / 0.0002 |
| H_COSTINV same verdict at 0/10/25 bps | **FAIL** | 0 bps 0.0629 (+0.407), 10 bps 0.0010 (+0.449), 25 bps 0.0010 (+0.495) |
| H_MATCH same verdict FULLMATCH / WINMATCH | **PASS** | 0.0010 (+0.449) vs 0.0010 (+0.644) |
| H_PANEL verdict agrees across panels | **FAIL** | U56 0.8292 (+0.292), B136 0.2268 (+0.569), **SMALL663 0.0010** (+0.486) |
| H_LEVEL movement not just convergence on one ceiling | **PASS** | Spearman(win_PRE, Δ) over 3 families −0.50, not −1 |
| H_R8CLAIM rule 8 on the claim | **PASS on significance, FAILS on SIGN** | statistic chosen on IS splits ≤2016 = HEADROOM (mean p RAW 0.0786 / HEADROOM 0.0010 / LOGODDS 0.0010); read ONCE: 2018 p 0.0010 **Δ +0.6842**, 2020 p 0.0010 **Δ −1.6047** |

H_R8CLAIM is the sharpest result in the run and it passes only on a technicality: the IS-chosen
statistic is significant at both later splits, with the effect **reversing sign** between them. A
walk-forward that asks "is it distinguishable" passes; one that asks "is it the same effect" does
not. **The 2016 split is the only cut at which the published direction and significance coexist on
the pooled corpus alongside 2014.**

### QROLL RAW delta and p, by split × panel (10 bps, FULLMATCH, P = 1,000)

| split | U56 | B136 | SMALL663 | POOLED |
|---|---|---|---|---|
| 2012-12-31 | +0.792 (0.0859) | +0.097 (1.0000) | +0.208 (**0.0010**) | +0.366 (0.2338) |
| 2014-12-31 | +0.556 (**0.0010**) | +0.375 (**0.0010**) | +0.486 (**0.0010**) | +0.472 (**0.0010**) |
| **2016-12-31** | +0.292 (0.8292) | +0.569 (0.2268) | +0.486 (**0.0010**) | +0.449 (**0.0010**) |
| 2018-12-31 | +0.111 (0.9890) | +0.403 (0.8531) | +0.028 (0.4785) | +0.181 (0.8851) |
| 2020-12-31 | +0.083 (1.0000) | +0.056 (0.7612) | **−0.618** (0.0589) | **−0.160** (**0.0010**) |

At the record's own split the pooled significance is carried by **SMALL663 alone** — neither large-cap
panel reaches p < 0.05 on its own. Per-split cell tallies over all 72 (P, rung, matching, scope)
cells: 2012 33/72 significant, 2014 70/72, 2016 37/72, **2018 0/72**, 2020 21/72 (of which the
deltas are positive in only 36/72).

## POST-HOC MECHANISM — not an arm-count artefact (declared post-hoc, after the table above)

The corpus hands QROLL 432 of 648 pooled arms against 108 each for ABS and QEXP, so a permuted
QROLL group is two thirds of the pool and its null is mechanically the tightest (σ 0.0158 vs
0.0513). Cutting QROLL to ONE lookback at a time (108 arms, exactly ABS's count) equalises the
null width; all four are reported:

| corpus | n QROLL | null σ (QROLL) | Δ QROLL | z | p | Δ ADV | p |
|---|---|---|---|---|---|---|---|
| w = ALL | 432 | 0.0171 | +0.4491 | +4.13 | 0.0010 | +0.2917 | 0.0010 |
| w = 252 | 108 | 0.0540 | +0.7222 | +6.01 | **0.0010** | +0.5648 | 0.0010 |
| w = 504 | 108 | 0.0518 | +0.5000 | +3.49 | **0.0020** | +0.3426 | 0.0010 |
| w = 1008 | 108 | 0.0510 | +0.3889 | +2.03 | **0.0290** | +0.2315 | 0.0040 |
| w = 2016 | 108 | 0.0473 | +0.1852 | −0.70 | 0.7812 | +0.0278 | 0.7552 |

QROLL survives at **3 of 4** matched-count corpora, so the headline is a family fact and not a
group-size fact — but it is monotone in the lookback (+0.72 → +0.50 → +0.39 → +0.19) and gone at
w = 2016. A side effect worth recording: with only long-w QROLL in the pool the pool mean drops and
**ABS itself becomes distinguishable** (w=1008 z +2.26 p 0.0190, w=2016 z +3.71 p 0.0020) — the
permutation null's location is a property of the corpus, so any published p here is conditional on
which arms are in the pool, and no memo on the record states that.

## Gates

G1 `fast_run` == `engine.backtest` max|d| 1.0e-17 **PASS** · G2 fast metrics == `engine.metrics`
0.0e+00 **PASS** · G3 0.01-grid twin interpolation |dSharpe| 2.0e-08 **PASS**.

G4 **PASS** — this run rebuilds idea 825's committed `.arms.csv` on all 1,944 rows: max|dSharpe|
2.2e-16, max|d twin Sharpe| 2.2e-16, **0 win-flag mismatches**. G5 **PASS** — 825's published
headline leg rates reproduce to 4.8e-05 (ABS 0.3333 / QEXP 0.5833 / QROLL 0.5231 PRE, 0.7407 /
0.6481 / 0.9722 POST, adv −0.0602 / +0.2315). G6 **PASS** — the machinery's observed delta equals
the direct leg difference exactly (0.0e+00), and over 200 deliberately random family relabellings
the share with p < 0.05 is **0.0200** against a nominal 0.05 (binomial 95% band ±0.0302): the null
does not reject itself.

## PROTOCOL rule 8 on the books, and both KEEP paths (10 bps, 324 rule-8 picks)

Dial (level, w) chosen on IS ≤2016-12-31 by IS Sharpe; OOS 2017-01-01.. read once.

| panel | family | OOS CAGR | OOS Sharpe | OOS MaxDD | 4a | 4b |
|---|---|---|---|---|---|---|
| U56 | ABS / QEXP / QROLL | 12.83% / 12.57% / 12.51% | 1.163 / 1.066 / **1.194** | −17.7% / −19.1% / −17.3% | 0/12 each | 3 / 0 / 3 of 12 |
| B136 | ABS / QEXP / QROLL | 11.58% / 12.22% / 11.31% | 1.019 / 1.010 / **1.099** | −20.2% / −20.4% / −15.6% | 0/12 each | 0 / 6 / 6 of 12 |
| SMALL663 | ABS / QEXP / QROLL | 3.49% / 3.91% / 4.77% | 0.330 / 0.328 / **0.404** | −32.2% / −41.8% / −32.0% | 0/12 each | 0/12 each |

Comparands on the same OOS window: **SPY 15.33% / 0.877 / −33.72%**; **RULES v2 (live) 9.47% /
1.278 / −12.05%** on U56 (7.88% / 1.106 / −12.24% B136, 3.75% / 0.560 / −13.89% SMALL663). Full
sample: SPY 15.16% / 0.886 / −33.72%; 4b bars CAGR floor 10.61%, DD cap −20.23%, halves
0.960/0.826, OOS 0.877.

Full-sample KEEP tallies over all 1,944 (panel, arm, rung) rows: **4a 3/1944** (all B136 QROLL at
0 bps), **4b 490/1944** — 162/67/24 on U56 and 143/74/20 on B136 at 0/10/25 bps, **0/216 on
SMALL663 at every rung**. Rule-8 picks: 4a 3/324, 4b 68/324. Of the 10 bps full-sample 4b passers,
45/216 (U56) and 13/216 (B136) have a matched-gross twin that ALSO passes 4b — exposure, not
clause. Best rule-8 pick by OOS Sharpe: B136 `QROLL q0.17 w252 d1.00 D g0.75` at 0 bps, OOS 10.63%
/ 1.397 / −9.32% — but at 0 bps, i.e. off PROTOCOL rule 2's rung, and no arm is promoted. These
figures are identical to 825's by construction (G4); nothing here is a new capital claim.

## Caveats

SURVIVORSHIP: all three panels are current-constituent lists, so every LEVEL is optimistic and
SMALL663 worst — a sub-$2B screen read today cannot see the names that fell out of it
(`data/SMALL_PANEL_README.md`); 52 tickers with `max_1d_move ≥ 1.0` were dropped before anything
was computed. This matters more than usual here: the headline's pooled significance at the record's
split is carried by SMALL663 alone, the most survivorship-contaminated panel. A win RATE is a
within-panel agreement rate, which survivorship moves far less than a level, but the per-panel
disagreement (H_PANEL) should be read with that in mind. The permutation null's LOCATION depends on
which arms are pooled (see the mechanism table), so every p here is conditional on the corpus.

## Follow-ups filed
842 (does any committed PERMUTATION or BOOTSTRAP p-value on the record name the POOL its null was
built from), 843 (is the QROLL→w monotonicity of the PRE→POST delta a LOOKBACK-LENGTH fact or a
WARM-UP fact), 844 (which committed split-date claims reverse SIGN at a second cut).
