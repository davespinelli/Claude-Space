# Idea 839 — is the NEGATIVE NEXT-WINDOW sign a MEAN-REVERSION fact or a CONDITIONING artefact? (cloud lane, 2026-09-12)

*(Numbering note: a concurrent lane filed a different idea also numbered 839 the same day. This
is the MEAN-REVERSION entry, disambiguated by title.)*

**ANSWERED: NEITHER — and the conditioning was hiding the sign, not making it.** Dropping idea
832's conditioning makes the negative sign **stronger** (−0.1067 against −0.0628), and it
survives non-overlapping entries (−0.1620 on 288 disjoint pairs). But it is **not a fact about
any book**: the book-label-permuted null produces a **more** negative mean per-book delta than
the real labels do, only 7 of 12 books carry it, at H=1260 the per-book mean is **positive**
(+0.0489) while the pooled number stays negative, and the 12 tilings of the same data span
**−0.6842 to +0.3889**. The one statement the corpus supports: **the halves clause's verdict is
never positively informative** — 48 of 48 cells at the PROTOCOL rung have delta < 0.
**KILL for the mean-reversion reading and for the artefact reading alike. No KEEP claimed, no
book promoted, no memo.**

Script: `2026-09-12_is-the-NEGATIVE-NEXT-WINDOW-sign-a-MEAN-REVERSION-fact-or-a-CONDITIONING-artefact_cloud.py`
(`.txt`, `.books.csv`, `.pairs.csv.gz`, `.grid.csv`, `.perbook.csv`, `.null.csv`, `.wf.csv`).
Two tuned parameters: **P1 conditioning** (NONE / OTHER3 / DDCAGR / SHARPE), **P2 permutation
count** (1,000 and 10,000). Horizon {756, 1260}, entry scheme {OVERLAP21, CHAIN, DISJOINT},
12 tiling offsets, cost {0, 10, 25} bps and memo set {MEMO8, MEMO12} are **reported at all 144
grid cells**, not selected.

## Gates

| gate | result |
|---|---|
| G1+G2 books reproduce their own committed triples | **12 of 12 PASS**; LIVE 8.63% / 1.2018 / −12.05% |
| G3 vectorised window metrics vs `engine.metrics` | max \|diff\| **2.220e-16** vs bar 1e-10 — PASS |
| **G4 reproduce idea 832's committed H_INFO cell** | **EXACT**: H=756 n **627**, 0.3182 / 0.3810 / **−0.0628**; H=1260 n **419**, 0.7072 / 0.7838 / **−0.0765** — PASS |
| G5 DISJOINT tilings disjoint, each window used once | **0** overlapping-or-reused windows — PASS |
| G6 BOOKLAB leaves the pooled delta invariant | max \|d\| **0.000e+00** over 100 draws — by construction (see below) |

**One committed number does not reproduce, and it is prose, not data.** The queue records
"9 of 11 books carrying the sign". The per-book table reproduces idea 832's committed values
bit-for-bit, and it reads **8 strictly negative, 1 positive, 2 exactly zero** of 11 defined
(K7 has 1 pair and no defined delta). The correct count at that cell is **8 of 11**.

## P1 — the conditioning is not the culprit; it was understating the effect

OVERLAP21, H=756, MEMO12, 10 bps:

| conditioning | pairs | P(next PASS \| halves PASS) | \| halves FAIL | **delta** |
|---|---|---|---|---|
| **NONE** | 1680 | 0.2549 | 0.3616 | **−0.1067** |
| OTHER3 (idea 832's) | 627 | 0.3182 | 0.3810 | **−0.0628** |
| DDCAGR | 627 | 0.3182 | 0.3810 | −0.0628 |
| SHARPE | 1472 | 0.2549 | 0.3818 | −0.1269 |

`|delta(NONE)| / |delta(OTHER3)| = 1.700` against a pre-registered bar of 0.5 — **H_COND FAILS in
the informative direction**. (OTHER3 and DDCAGR coincide exactly at 10 bps: on this corpus the
full-window Sharpe leg is implied by the two ratio legs at that rung. They separate at 0 bps,
676 vs 678 pairs.)

## Non-overlapping entries: the sign survives, the *number* does not

| scheme, H=756, MEMO12, NONE | pairs | delta |
|---|---|---|
| OVERLAP21 (832's pooling) | 1680 | −0.1067 |
| CHAIN (disjoint windows, each in 2 pairs) | 564 | −0.1149 |
| **DISJOINT (each window used once)** | **288** | **−0.1620** |

**48 of 48 cells at 10 bps are negative** (min −0.2062, max −0.0036, median −0.1273). Across all
three cost rungs, 120 of 144 — at 0 bps 40 of 48 and at 25 bps only 32 of 48, so the
*universality* is a 10-bps statement, not a general one.

But the same 288 pairs re-tiled at the 12 offsets give deltas spanning **−0.6842 … +0.3889**,
median −0.0294, with only **7 of 12 offsets negative**. Offsets are the same data re-cut, not
independent draws — which is exactly why the pooled −0.1620 is not a quotable quantity.

## The nulls (10,000 permutations)

| cell | pooled delta | WITHIN-book band | p | mean per-book delta | BOOKLAB band | p |
|---|---|---|---|---|---|---|
| DISJOINT/756/NONE | **−0.1620** | [−0.1620, +0.0313] | **0.0386** | −0.1146 | [−0.1882, −0.1349] | 0.9983 |
| OVERLAP21/756/NONE | −0.1067 | [−0.0591, +0.0196] | **0.0000** | −0.0867 | [−0.1104, −0.1031] | 1.0000 |
| OVERLAP21/756/OTHER3 | −0.0628 | [+0.0058, +0.1291] | 0.5414 | −0.1456 | [−0.0964, −0.0287] | 0.0000 |
| CHAIN/756/NONE | −0.1149 | [−0.0866, +0.0553] | 0.0039 | −0.0984 | [−0.1257, −0.1040] | 0.9980 |
| DISJOINT/1260/NONE | −0.1276 | [−0.2728, −0.0696] | 0.8923 | **+0.0489** | [−0.1789, −0.0670] | 0.9922 |

Two readings of the headline cell disagree at the boundary: the two-sided p is **0.0386**, but
the null's 2.5% quantile **equals** the observed −0.1620 (the permutation distribution is
discrete at n=288 with heavy within-book dependence), so the pre-registered "strictly outside the
band" reading records a FAIL. Reported both ways; the honest summary is *marginal*.

**The BOOKLAB null is the decisive one, and it points the other way.** The observed mean per-book
delta (−0.1146) lies **outside** its band — but on the side of being **less negative than a
random relabelling** (band [−0.1882, −0.1349], p 0.9983). Shuffling which book a pair belongs to
makes the effect **stronger**. The negativity is therefore a property of the pooled pair
population, not of the books; the real book labels work *against* it.

Note G6: a book-label permutation leaves the **pooled** delta exactly invariant (0.000e+00 over
100 draws) because the pooled statistic never reads a label. A book-label null can only be run
on a label-using statistic — which is why it is run here on the equal-weight mean of per-book
deltas, and why the pooled −0.0628 in the record cannot be defended with that null at all.

## Simpson: composition masks the effect at H=756 and creates it at H=1260

| cell | pooled | pair-weighted within-book mean | composition part |
|---|---|---|---|
| OVERLAP21/756/OTHER3 (832's) | −0.0628 | **−0.1584** | **+0.0957** |
| DISJOINT/756/NONE | −0.1620 | −0.1146 | −0.0474 |
| DISJOINT/1260/NONE | −0.1276 | **+0.0489** | **−0.1765** |

At idea 832's own cell the within-book effect is **twice as negative** as the number it
published — composition was hiding it. At H=1260 with disjoint entries the sign **reverses**
between the two readings: pooled −0.1276, per-book +0.0489, with only 2 of 9 defined books
negative. H_SIMPSON FAILS at the 0.05 bar in both directions.

## Per-book, DISJOINT / H=756 / NONE (24 pairs each)

7 negative (R1 −0.7222, K4 −0.4222, K5 −0.3950, R2 −0.2632, K2 −0.2222, K1 −0.1875, R4 −0.1429),
4 positive (K8 +0.5000, K3 +0.3333, K6 +0.1111, R3 +0.0350), 1 exactly zero (K7).
**7 of 12 against the pre-registered bar of 9 — H_BOOKS FAILS.**

## Rule 8 — cell chosen on IS pairs only, OOS read once

| conditioning, H | n IS | IS delta | n OOS | OOS delta |
|---|---|---|---|---|
| **NONE, 756** (IS pick, most negative) | 96 | **−0.1209** | 48 | **−0.1667** |
| SHARPE, 756 | 68 | −0.0899 | 46 | −0.1364 |
| OTHER3 / DDCAGR, 756 | 19 | +0.0000 | 33 | +0.0789 |
| any, 1260 | 0 | — | 0 | — |

The IS pick is also the OOS-most-negative cell, gap 0.0458 against a 0.10 bar — **H_WF PASSES**.
(H=1260 admits no IS pairs at all under DISJOINT: a 5-year predictor plus a 5-year target does
not fit inside 2009–2016.)

**Mandated book leg**, 10 bps, OOS = 2017-01-01..: LIVE **9.47% / 1.2782 / −12.05%**,
SPY **15.33% / 0.8767 / −33.72%**. Books' OOS CAGR / Sharpe / MaxDD run
14.4/15.2/13.8/12.7/12.7/15.1/6.4/**16.0**/12.0/12.4/16.0/14.5% and
1.130/1.235/1.286/1.269/1.278/1.261/1.187/**1.394**/1.165/1.106/1.215/1.040 at
−18.3…−20.0% (K1..K8, R1..R4). **Fixed window: 4a 0 of 12, 4b 11 of 12; OOS-only 4b 11 of 12**
(only K7 fails, on the CAGR floor). 4a fails on `DD<=LIVE` at 11 of 12 books.

## Pre-registered hypotheses: 4 of 8 PASS

| | verdict | number |
|---|---|---|
| H_REPRO | PASS | idea 832's cell reproduces exactly, both horizons |
| H_SURVIVE | PASS | DISJOINT/756/NONE = −0.1620 on 288 pairs |
| H_COND | **FAIL** | ratio 1.700 vs bar 0.5 — dropping the conditioning strengthens the sign |
| H_WITHIN | **FAIL** (boundary) | p 0.0386 but observed == the band's 2.5% quantile |
| H_SIMPSON | **FAIL** | composition part +0.0957 vs bar 0.05 |
| H_BOOKS | **FAIL** | 7 of 12 vs bar 9 |
| H_BOOKLAB | PASS *in form only* | outside the band **on the wrong side**: relabelling is more negative (p 0.9983) |
| H_WF | PASS | IS pick = OOS-most-negative cell, gap 0.0458 |

## What this establishes, and what it does not

**Establishes:** idea 832's negative sign is not an artefact of its conditioning (removing it
makes the sign larger) and not an artefact of overlapping entries (it survives a strict
one-window-one-pair tiling). At the PROTOCOL rung, no reading of the clause is positively
informative about the next window — 48 of 48 cells negative.

**Does not establish:** that any book mean-reverts. The corpus cannot call it at the book level —
7 of 12 books at the strict cell, 12 re-tilings of the same data spanning −0.68 to +0.39, a
book-label null that beats the real labels, and a sign that reverses between pooled and per-book
readings at H=1260. n is 18–288 pairs at the strict cells; nothing here separates a −0.15 delta
from the structure of a 0.35 base rate.

Survivorship: `universe.json` and `universe_broad.json` are current-constituent lists, so every
LEVEL is optimistic; the object here is a within-corpus conditional contrast, which survivorship
does not cancel out of.

## Follow-ups filed (PROTOCOL.md NOT modified — Sunday review decides)

842 (is the negative sign a BASE-RATE identity?), 843 (how many committed per-book counts in the
record disagree with their own committed tables, as this one's "9 of 11" does?).
