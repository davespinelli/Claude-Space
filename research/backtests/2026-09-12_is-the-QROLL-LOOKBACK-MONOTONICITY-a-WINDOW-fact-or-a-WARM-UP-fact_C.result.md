# Idea 843 — is the QROLL PRE/POST delta's LOOKBACK MONOTONICITY a WINDOW-LENGTH fact or a WARM-UP fact?
lane C, 2026-09-12 · `2026-09-12_is-the-QROLL-LOOKBACK-MONOTONICITY-a-WINDOW-fact-or-a-WARM-UP-fact_C.py`

## THE ANSWER: **NEITHER, cleanly — and the monotonicity is not a stable object.**
The warm-up channel is arithmetically real and is worth **24.1% of the profile's spread in level and
essentially 100% of its significance for w ≥ 504**; the window channel survives the live-day
restriction in level (ρ(w, δ) still −1.0000 over the three w that remain readable); and the w = 2016
endpoint that anchors the whole profile **is not a measurement of the gate at all under either twin-
matching convention** — its PRE win rate is **0.7778 under FULLMATCH and exactly 0.0000 under
WINMATCH**, on a leg where the arm is 87.5% (U56/B136) to 100% (SMALL663) the ungated book.
Of the four grid points the queue quotes, exactly **one (w = 252) survives every convention and the
liveness restriction.** **KILL** of the monotonicity as a publishable object. No KEEP, no memo, no
book promoted, no RULES change.

## GATES (all printed before any verdict) — 4 of 4 PASS, plus G1–G3 at 1e-17/0/2e-8
| gate | what | result |
|---|---|---|
| G4 | corpus rebuilds idea 834's **committed** `.arms.csv`, 1,944 rows | max │dSharpe│ **2.220e-16**, max │d twin Sharpe│ 2.220e-16, **0** win-flag mismatches — PASS |
| G5 | reproduces 834's **committed** per-w deltas (the four numbers idea 843 quotes) | +0.7222 / +0.5000 / +0.3889 / +0.1852, max │d│ **5.551e-17** — PASS (**H_REPRO**) |
| G6 | **the inertness identity**: before its threshold exists a QROLL arm's gate multiplier is 1.0 and its daily return equals the ungated EWALL book's | max │d│ **0.000e+00** on 432 QROLL arms across three panels — PASS |
| G7 | the family-blind null is calibrated | identity permutation 0.000e+00; 200 random relabellings reject at **0.0400** (expected 0.05, band ±0.0302+0.0050) — PASS |

G6 is what turns "warm-up" from a story into arithmetic: on 87.5% of its PRE leg at the record's
split, a "w2016 QROLL arm" **is** the ungated book, bit-identically.

## THE WARM-UP ACCOUNTING (share of the PRE leg on which the threshold exists)
| panel | split | w252 | w504 | w1008 | w2016 |
|---|---|---|---|---|---|
| U56 / B136 | 2016-12-31 | 0.9995 | 0.8784 | 0.6273 | **0.1251** |
| SMALL663 | 2016-12-31 | 0.9993 | 0.8375 | 0.5020 | **0.0000** |
| U56 / B136 | 2020-12-31 | 0.9997 | 0.9190 | 0.7518 | 0.4174 |

SMALL663 — the panel 834 found carries the pooled significance at the 2016 cut — has **zero** live
days at w2016. The queue's premise ("its PRE leg is nearly empty at every split ≤2016") is confirmed
and is stronger than stated: on SMALL663 it is exactly empty.

## THE PROFILE, under the three leg rules (headline split 2016-12-31, 10 bps, FULLMATCH, POOLED, arm-count-matched at 108 arms/family)
| rule | w252 | w504 | w1008 | w2016 | spread | ρ(w, δ) |
|---|---|---|---|---|---|---|
| RAW (834's) | **+0.7222** p0.0010* | **+0.5000** p0.0010* | **+0.3889** p0.0310* | +0.1852 p0.7842 | 0.5370 | **−1.0000** |
| LIVE (the queue's) | +0.7222 p0.0010* | +0.4259 p0.1798 | +0.3148 p0.2438 | *leg too short* | 0.4074 | −1.0000 |
| COMMON | *leg too short* | *leg too short* | *leg too short* | *leg too short* | — | — |

**At the record's own split the question is not answerable for w = 2016.** Once the leg must start
where the threshold exists, the PRE leg is **251 trading days** on U56/B136 (one day under the
252-day floor) and **negative** on SMALL663. The RAW cell exists only because the convention lets a
gate be scored on days it cannot fire.

Restricting to live days costs the two readable mid-w cells **their significance**, not much of their
level: w504 p 0.0010 → **0.1798**, w1008 p 0.0310 → **0.2438**, deltas moving only −0.074 each. PRE
win rates *rise* when the dead days are dropped (w504 0.4630 → 0.5370, w1008 0.5741 → 0.6481), which
is the warm-up channel's signature: dead days depress the PRE rate and inflate δ.

## THE CONVENTION FINDING (this run's own, post-hoc, flagged as such)
Same arms, same legs, one axis changed — the twin-matching convention:

| matching | w252 | w504 | w1008 | w2016 | ρ(w, δ) |
|---|---|---|---|---|---|
| FULLMATCH | +0.7222 p0.0010* | +0.5000 p0.0010* | +0.3889 p0.0310* | +0.1852 p0.7842 | **−1.0000** |
| WINMATCH | +0.7222 p0.0030* | +0.5000 p0.6633 | +0.3889 p0.9740 | **+0.9630 p0.0010*** | **+0.2000** |

w2016's PRE win rate is **0.7778 (FULLMATCH)** or **0.0000 (WINMATCH)** — 84 of 108 arms winning, or
none of them — because on a 87.5%-dead leg the arm's own realised gross *is* the twin's, so WINMATCH
makes it a tie (not a win) while FULLMATCH scores an ungated book against a lower static gross over a
bull leg. Neither number measures a gate. The monotonicity also fails at **0 bps** (ρ −0.6325) and on
**U56 alone** (ρ −0.4000, nothing significant); it holds on B136 (−1.0000) and SMALL663 (−1.0000),
and only SMALL663 carries significance (0.8333*/0.7222*/0.5000*/−0.1111) — the panel with no live
w2016 days at all. Under the ceiling-normalised readings the decline persists but **every** w is
distinguishable, w2016 included (HEADROOM 1.0000*/0.9310*/0.9130*/0.8333*; LOGODDS
+6.33*/+3.29*/+2.85*/+1.91*), so "insignificant at w2016" is a property of the RAW statistic, not of
the family.

## WHERE LIVENESS *CAN* BE CONTROLLED (2018-12-31 and 2020-12-31, the only splits at which all four w are feasible under LIVE and COMMON)
At 2020-12-31 every delta has already turned **negative** and ρ = **−0.8000 under all three rules**
(RAW spread 0.2037, LIVE 0.2222, COMMON 0.1481): with the calendar held fixed and every threshold
alive, the residual profile is neither monotone nor a warm-up artefact — it is small, negative and
convention-stable. At 2018-12-31 COMMON flattens the profile to +0.1667/+0.0278/+0.0833/+0.0556 (all
insignificant) against RAW's +0.5370*/+0.1852/+0.0926/−0.0926, but that leg is 2016-2018 only, so the
flattening is as much calendar as liveness — which is why COMMON is reported and not used as the
headline.

**Significance census over all QROLL RAW-statistic cells:** RAW **266 of 600** significant, LIVE **127
of 408**, COMMON **33 of 210** — 44% → 31% → 16% as the leg is forced onto live days.

**H_LIVEFIT fails:** across the 60 (panel, split, w) per-panel RAW cells, log w explains δ slightly
better than live share (ρ −0.4240 / R² 0.1570 against +0.3427 / 0.0844), and only **one** w (252) is
ever fully live, so the two regressors cannot be separated within this corpus. The decisive evidence
against a pure warm-up reading is not the fit, it is that δ keeps its −1.0000 ordering over the three
w that *are* readable on live days.

## HYPOTHESES — 4 of 12 PASS
| | verdict | reading |
|---|---|---|
| H_REPRO | **PASS** | max │this run − 834's committed δ│ 5.55e-17 |
| H_MONO_RAW | **PASS** | ρ(w, δ) = −1.0000 under RAW at the headline |
| H_WARMUP | FAIL | spread 0.5370 → 0.4074, **24.1%** shrink against a 50% bar |
| H_WINDOW | FAIL | at 2020-12-31 COMMON ρ −0.8000 (RAW −0.8000): not strictly monotone either way |
| H_WARMUP_CAL | FAIL | at 2020-12-31 spread RAW 0.2037 → COMMON 0.1481 (27%) |
| H_LIVEFIT | FAIL | ρ │live│ 0.3427 vs │log w│ 0.4240; R² 0.0844 vs 0.1570 |
| H_W2016SIG | FAIL | w2016 RAW p 0.7842 → LIVE p 0.1189 (read at 2020-12-31; its headline LIVE leg does not exist) |
| H_COSTINV | FAIL | ρ = −0.6325 / −1.0000 / −1.0000 at 0 / 10 / 25 bps |
| H_MATCH | FAIL | FULLMATCH −1.0000, **WINMATCH +0.2000** |
| H_PANEL | FAIL | U56 −0.4000, B136 −1.0000, SMALL663 −1.0000 |
| H_R8CLAIM | **PASS** | IS mean spread RAW 0.6049 / LIVE 0.3364 → pick LIVE; OOS mean spread LIVE 0.3889 < RAW 0.4167 |
| H_R8PICK | **PASS** | the warm-up-aware chooser moves the w pick in **14 of 108** (LIVE50) and **82 of 108** (LIVELEG) QROLL cells |

## PROTOCOL RULE 8 — on the books (dial chosen on IS ≤2016-12-31, OOS 2017-01-01…2026-09-11 read once)
| chooser | picks | 4a | 4b | med OOS CAGR | med OOS Sharpe | med OOS MaxDD |
|---|---|---|---|---|---|---|
| BLIND (834's) | 324 | **3** | **68** | 10.45% | 1.009 | −20.88% |
| LIVE50 (w live ≥50% of IS) | 324 | 3 | 68 | 10.42% | 1.009 | −20.88% |
| LIVELEG (IS Sharpe on the arm's own live leg) | 324 | **0** | **78** | 10.49% | 1.009 | −20.75% |

Benchmarks on the same OOS window: **RULES v2 (live) 9.67% / 1.303 / −12.03%; SPY 15.33% / 0.877 /
−33.72%.** BLIND reproduces 834's committed rule-8 counts (4a 3, 4b 68 of 324) exactly. Making the
chooser warm-up-aware is not free: it moves the w pick in 82 of 108 QROLL cells, lifts 4b passes
68 → 78 and **kills all three 4a passes**. At PROTOCOL's 10 bps: **0 of 324 picks pass 4a under any
chooser**, 18 / 18 / 23 of 108 pass 4b, and **0 pass both**. Best 10 bps rule-8 4b passer — U56 QROLL
L0.17 w1008 d1.00 W g1.00 via LIVELEG, OOS **15.99% / 1.390 / −12.77%** against v2 9.67% / 1.278 and
SPY 15.33% / 0.877 — **is not a candidate: its matched-gross static twin also passes 4b** (exposure,
not clause), and it is one of the 490 rows 834 already committed and declined.

**BOTH KEEP PATHS over all 1,944 (panel, arm, rung) rows:** 4a **3**, 4b **490**, BOTH **1** — and the
single BOTH row is at **0 bps** (B136 QROLL L0.17 w252 d0.50 D g0.75), so it is not a capital claim
under PROTOCOL rule 2. 4b passers: U56 253, B136 237, **SMALL663 0**; **266 of 490 have a twin that
also passes 4b**, leaving 224 clause-attributable. Binding 4b legs: CAGR 292, DD 207, all-five 627.
The corpus is identical to 834's by G4, so these counts are 834's counts, re-derived, not new books.

## WHAT THE RECORD SHOULD CARRY
1. **Idea 834's w-profile should not be cited as a lookback fact.** One of its four points (w252) is a
   gate measurement; w504/w1008 lose significance on live days; w2016 is a convention reading of an
   ungated book and flips to the *largest* delta of the four under WINMATCH.
2. **Any rolling-window claim needs its live share printed beside it.** The corpus makes this cheap:
   one column, `share of the leg on which the threshold exists`.
3. **The record's rule-8 chooser is warm-up-blind.** It can and does pick a lookback that did not
   exist for 37–87% of the window it was chosen on; a live-leg chooser moves the pick in 76% of QROLL
   cells and changes both KEEP-path counts.

15 tuned points (5 w-corpora × 3 leg rules), **12,202 grid rows** written covering every split, cost
rung, twin matching, scope and statistic; 225 liveness rows. Survivorship: all three panels are
current-constituent lists (SMALL663 worst); no Sharpe or CAGR here is a capital claim.
RULES.md, PROTOCOL.md, research/scan.py, products/bot/bot.py and research/baseline.py untouched.
