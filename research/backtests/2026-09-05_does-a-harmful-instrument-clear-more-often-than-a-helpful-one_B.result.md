# Idea 192 — does-a-harmful-instrument-clear-more-often-than-a-helpful-one

**lane B, 2026-09-05.** Script `2026-09-05_does-a-harmful-instrument-clear-more-often-than-a-helpful-one_B.py`.
Artefacts: `.arms.csv` (288 rows), `.regression.csv`, `.walkforward.csv` (120 rows), `.reproduction.csv`,
`.repro_T.csv` / `.repro_Tclause.csv` / `.repro_O.csv` (the independent recomputations), `.console.txt`.

## Verdict

**ANSWERED, and it is a KILL of the matched-null clause as a KEEP gate — now with the mechanism and a
p-value, not just a walk-forward loss.** The clause measures **effect size and nothing else**; the sign
tilt idea 186 saw is a property of the *corpus*, not of the test. And the corpus's sign structure runs the
wrong way for capital: **of the 51 arms in the pooled 288 that pass PROTOCOL 4b, exactly 1 clears its own
null band (2.0%), against 31.6% of the 237 that fail** (Fisher p = 9.2e-07). Using the clause to select is
worse than not selecting. **No new book, no KEEP, RULES untouched.**

## What was run

Pooled the two null-clause corpora the queue named, on one schema, one row per real arm:

| corpus | parent | arms | construction |
|---|---|---|---|
| T | idea 181 | 180 | 3 panels x 5 keyed tilts x 2 dirs x 3 strengths x 2 cost rungs; null = 20 random-walk keys |
| O | idea 186 | 108 | 3 panels x 3 overlay families x 3 thresholds x 2 depths x 2 rungs; null = 20 circular rotations |
| | | **288** | clause in both: `clears ⇔ |dSharpe(real)| > max over 20 matched null draws` (one-sided 1/21 = 4.8%) |

**Tuned parameters: 0.** The corpus is fixed and already published; each parent's two dials are carried
through unchanged and every one of the 288 arms and all 24 x 5 walk-forward cells are reported in full.

### Reproduction 4 / 4 (nothing below was read until these passed)

| # | check | result |
|---|---|---|
| a | engine cost identity, 0 bps run → 25 bps run | max abs diff **0.000e+00** |
| b | RULES v1 on u56 @10 bps Sharpe | **0.6642** vs the project's published 0.6642 |
| c | corpus T's u56 slice rebuilt from scratch (5 real + 20 null keys, 2 dirs, 3 strengths, 2 rungs) | 60 arms, max abs dSharpe diff **9.93e-17**, **0 clause mismatches** |
| d | corpus O's U56 DDCTL family rebuilt from scratch (6 arms x 21 draws) | 252 rows, max abs dSharpe diff **4.30e-16**, **0/6 clause mismatches** |

## Q1 — is the clause blind to sign?  **Yes, mechanically. The tilt is the corpus's, not the test's.**

Unconditionally idea 186's suspicion is confirmed:

```
clear rate   NEGATIVE dSharpe  59/184 = 32.1%     POSITIVE dSharpe  17/100 = 17.0%
Fisher exact (two-sided) p = 0.00743
mean |dSharpe|   NEGATIVE 0.1244   POSITIVE 0.0882
```

But the whole gap is magnitude. In the logit, `|dSharpe|` is overwhelming and the sign dummy dies as soon
as it is controlled for:

| model | absd | neg | log(band) | corpus |
|---|---|---|---|---|
| M1 `|d|` only | +21.92 (z +7.80, p 6e-15) | — | — | — |
| M2 sign only | — | **+0.88 (z +2.86, p 0.004)** | — | — |
| M3 `|d|` + sign | +21.45 (z +7.62) | **+0.45 (z +0.98, p 0.33)** | — | — |
| M4 + log(band) | +24.50 (z +7.58) | **+0.71 (z +1.42, p 0.16)** | −0.38 (z −3.83) | — |
| M5 + corpus | +25.49 (z +7.26) | +0.98 (z +1.86, p 0.063) | −0.46 (z −4.27) | −1.23 (z −2.53) |

Model-free confirmation — inside terciles of `|dSharpe|` the sign difference vanishes:

```
low |d|  [0.0000,0.0398]  NEG  0/51 =  0.0%   POS  0/41 =  0.0%   Fisher p 1
mid |d|  [0.0402,0.1031]  NEG 10/58 = 17.2%   POS  4/38 = 10.5%   Fisher p 0.555
high|d|  [0.1038,0.6171]  NEG 49/75 = 65.3%   POS 13/21 = 61.9%   Fisher p 0.80
```

So the clause is exactly what it says on the tin: a magnitude test with a ~4.8% false-positive rate. It
clears harmful arms more often **because this project's instruments, when they have a large effect at all,
usually have a large *harmful* effect** — mean `|d|` is 41% bigger on the negative side of the corpus.

## Q2 — has a clearing arm ever been a positive one?  **Yes: 17 of the 76.**

Idea 186's "all 15 clearing DDCTL points are negative" is a **DDCTL fact, not a clause fact**. All 17
positive clearers live in corpus T, and 12 of them are `PRICE/NEG` — the family that produced idea 181's
only selector win. The largest: `small PRICE/NEG/1 @10bps` (+0.6043 dSharpe, band 0.3552, OOS Sharpe
1.1904) and `broad PRICE/NEG/1 @10bps` (+0.3678, band 0.1328, OOS 1.3493). **None of the 17 passes 4b** —
they are the low-price-tilt cohort idea 185 is queued to separate from survivorship, and their drawdowns
(−21% to −28%) fail 4b's cap.

Clear rate by family, negatives and positives kept apart:

```
T/VOL    10/36 (NEG 10/19, POS  0/17)      O/DDCTL  15/36 (NEG 15/32, POS  0/0)
T/MOM     5/36 (NEG  4/22, POS  1/14)      O/BUDGET  2/36 (NEG  2/18, POS  0/18)
T/R6      9/36 (NEG  9/24, POS  0/12)      O/SLEEVE  0/36 (NEG  0/25, POS  0/11)
T/R3      8/36 (NEG  4/26, POS  4/10)
T/PRICE  27/36 (NEG 15/18, POS 12/18)
```

## Q3 — is it a poor filter for KEEPs?  **It is worse than that: it is anti-correlated with 4b.**

```
PASS4A: 86/288 pass.  clear rate among passes 30/86 = 34.9%  among fails 46/202 = 22.8%
PASS4B: 51/288 pass.  clear rate among passes  1/51 =  2.0%  among fails 75/237 = 31.6%
        of the 51 4b passes, 18 have positive dSharpe; ZERO both clear AND are positive.

                clears   inside band
   4b pass          1            50
   4b fail         75           162        Fisher exact p = 9.23e-07
```

A gate that admits only clearing arms would throw away **50 of the 51 capital-worthy arms** while keeping
75 of the 237 failures. This is the quantitative form of what ideas 181 and 186 each saw from one side
(1 of 33 tilt 4b passes; 0 of 18 overlay 4b passes) and it survives pooling.

## Rule 8 — walk-forward of the sign-aware gate (params chosen ≤ 2016-12-31, 2017-2026 read once)

24 cells (6 tilt: panel x rung; 18 overlay: panel x family x rung), 5 selectors, 120 rows.

| selector | mean OOS Sharpe | vs S0 | t | W/L | OOS CAGR | OOS MaxDD | abstains |
|---|---|---|---|---|---|---|---|
| **S0 do-nothing** | **0.7759** | — | — | — | 10.20% | −23.46% | 0 |
| S1 IS-argmax | 0.8456 | +0.0697 | +1.33 | 12/10 | 11.08% | −24.19% | 0 |
| S2 clause-gated (published) | 0.7457 | **−0.0302** | **−2.26** | 2/10 | 9.74% | −24.42% | 12 |
| **S3 clause + positive sign** | 0.7717 | **−0.0041** | −0.42 | 2/2 | 10.22% | −24.15% | **20** |
| S4 sign only | 0.8488 | +0.0730 | +1.41 | 7/6 | 11.33% | −24.70% | 11 |
| RULES v1 baseline | 0.4619 | | | | 4.80% | −25.26% | |
| SPY buy-and-hold | 0.8820 | | | | 15.45% | −33.72% | |

**Adding the sign repairs the clause only by switching it off.** S3 beats S2 by +0.0260 (P7 hit) but does
it by abstaining in **20 of 24 cells** — it converges to do-nothing and still does not beat it (−0.0041,
t −0.42). This is the **eighth consecutive instance** in this project (110/132/151/166/171/174/175/184) of
an in-sample selector losing to doing nothing, and the **third** of the null clause failing as a gate.
S1 and S4 are nominally ahead but neither is significant, and both are carried by `PRICE/NEG` on the broad
and small panels — the arms idea 185 is queued to test for survivorship.

Both KEEP paths on every walk-forward pick, OOS window, against each cell's own panel:

| selector | 4a-style wins vs RULES v1 | 4b-style wins vs SPY |
|---|---|---|
| S0 do-nothing | **9/24** | **9/24** |
| S1 IS-argmax | 6/24 | 9/24 |
| S2 clause-gated | 5/24 | 8/24 |
| S3 clause + positive | 7/24 | 8/24 |
| S4 sign only | 6/24 | 8/24 |

Do-nothing wins or ties on both paths. No arm here is proposed for capital.

## Pre-registered predictions: 7 of 7 hit

| | prediction | outcome |
|---|---|---|
| P1 | `|dSharpe|` positive and significant | HIT — coef +21.45, z +7.62, p 2.6e-14 |
| P2 | NEG dummy insignificant once `|d|` and band controlled | HIT — coef +0.71, z +1.42, p 0.16 |
| P3 | clearing arms skew negative | HIT — P(d<0 \| clear) 77.6% vs 59.0% |
| P4 | at least one clearing arm is positive | HIT — 17 of 76 |
| P5 | clear rate among 4b passes ≪ corpus rate | HIT — 2.0% vs 26.4% |
| P6 | S3 does not beat do-nothing | HIT — −0.0041 mean OOS Sharpe |
| P7 | S3 ≥ S2 | HIT — +0.0260 |

## What this means for the record (report-only; no RULES change proposed)

1. Clause 11 / 11b stay **report-only**, and their wording should carry this sentence: *clearing the
   matched null band is a statement about effect SIZE only — in this project's corpus it is
   anti-correlated with 4b (1 of 51 passes clear, p 9e-07) and must never be read as evidence for a KEEP.*
2. Idea 186's "all 15 clearers are harmful" should be re-labelled a **DDCTL** result. Pooled, 22% of
   clearers are helpful.
3. `|dSharpe|` and the arm's own band are the two numbers worth back-filling; the sign adds nothing to
   predicting clearance, so idea 191's on-share column and idea 183's anchor-position column are better
   uses of schema space than a sign column.

## Scope and caveats

- Corpus T's arms are equal-weight top-20 composite books with one additive rank tilt; corpus O's are the
  same base book with one overlay. `dSharpe` is measured against each corpus's own control, which differs
  (tilt control = untilted composite book; overlay control = untreated base book). Pooling is therefore a
  pooling of *effect sizes relative to a matched control*, not of raw Sharpes; the corpus dummy in M5
  absorbs the level difference and does not change the sign result.
- The small/broad panels are current constituents (survivorship). Every positive clearing arm outside u56
  lives on those panels, which is precisely why none of them is proposed for capital here.
- Corpus O's 4a/4b flags are its parent's; corpus T's were recomputed in this script against each panel's
  SPY and RULES v1 with idea 181's own bars, so both corpora sit on one footing.
