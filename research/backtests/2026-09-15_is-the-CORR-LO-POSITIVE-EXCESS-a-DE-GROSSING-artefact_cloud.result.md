# Idea 815 — is the CORR-LO positive excess a DE-GROSSING artefact? (cloud, 2026-09-15)

**ANSWERED: NO — AND THE QUEUE'S PREMISE IS INVERTED. The alignment artefact is in idea 606's
HEADLINE families, not in its failed reversal control. KILL for capital.**

Script `2026-09-15_is-the-CORR-LO-POSITIVE-EXCESS-a-DE-GROSSING-artefact_cloud.py`; 3,456 real
arms (3 panels × 8 families × 3 q × 4 w × 3 depths × 2 cadences × 2 grosses) and **172,800
placebo cells** (5 kinds × 10 md5 seeds), weekly/daily gates, 10 bps, t+1, all grid points
reported. Two tuned parameters, the queue's own: **state** and **placebo kind**.

## The question and how it was made answerable

Idea 606's reversal control — fire the gate on the *wrong* tail, keeping the rate and the
clustering and destroying the information — flipped VOL20-LO (−0.0128) and DISP-LO (−0.0204)
but *failed* on CORR-LO (+0.0270, share>0 0.845). The queue's two readings: either the BLOCK
placebo's circular shift destroys a **calendar alignment with 2020/2022 that both tails share**,
or the **low-correlation tail carries real information**. They separate because they predict
different things under a null that *keeps* the calendar. Three such nulls were added to idea
606's two:

| kind | what it preserves | new? |
|---|---|---|
| RAND | rate only (destroys run lengths) | 606 |
| BLOCK | rate + run-length distribution, no calendar | 606 |
| **YEARBLOCK** | the above **+ every firing day stays in its calendar year** | this run |
| **EPISODEFIX** | the above **+ the declared episode days keep the real path's values exactly** | this run |
| **BLOCKPOST** | the above **+ no firing day may move into the pre-threshold warm-up region** | this run |

Declared episodes, fixed in advance: COVID_TIGHT 2020-02-19…2020-03-23, BEAR2022
2022-01-04…2022-10-12 (6.3% of the tape).

## Gates (printed before any new number)

G1 never-firing multiplier ≡ ungated book **0.000e+00** · G2 every placebo's mean effective
multiplier ≡ the real arm's **0.000e+00** (so the matched-gross twin cancels *exactly* and
excess = Sharpe(real) − Sharpe(placebo), no twin term) · G4 determinism, 36 cells re-seeded
**0.000e+00** · G6 fast Sharpe ≡ `engine.metrics()['Sharpe']` **0.000e+00** · **G3 PASS**: idea
606's committed 8-family BLOCK table rebuilt here, **sign agrees 8/8, median |Δ| 0.0037**
(BREADTH-LO +0.0737→+0.0725, CORR-HI +0.0420→+0.0554, CORR-LO +0.0270→+0.0341, DISP-LO
−0.0204→−0.0347). The small panel is a rebuilt cache, not 606's SMALL664, so the U56+B136
column is the like-for-like leg and is printed beside it.

## [1] The decomposition — median excess, n=432 arms per family

| family | fires-in-episode | RAND | BLOCK | YEARBLOCK | EPISODEFIX | BLOCKPOST |
|---|---|---|---|---|---|---|
| BREADTH-LO *(prior)* | 0.314 | +0.2197 | **+0.0725** | +0.0239 | **+0.0041** | +0.0712 |
| BREADTH-HI *(rev)* | 0.004 | +0.2483 | +0.0128 | +0.0531 | +0.0281 | +0.0139 |
| VOL20-HI *(prior)* | 0.154 | +0.1854 | **+0.0203** | −0.0106 | **−0.0279** | +0.0218 |
| VOL20-LO *(rev)* | 0.000 | +0.2113 | −0.0176 | +0.0086 | +0.0010 | −0.0186 |
| DISP-HI *(prior)* | 0.117 | +0.2059 | **+0.0306** | +0.0013 | **−0.0076** | +0.0296 |
| DISP-LO *(rev)* | 0.001 | +0.1709 | −0.0347 | −0.0163 | −0.0181 | −0.0338 |
| CORR-HI *(prior)* | 0.186 | +0.2003 | **+0.0554** | +0.0249 | **−0.0062** | +0.0523 |
| **CORR-LO** *(rev)* | **0.001** | +0.2503 | **+0.0341** | **+0.0568** | **+0.0519** | +0.0294 |

## The four findings

**1. THE QUEUE'S MECHANISM IS FACTUALLY ABSENT.** The two tails of correlation do **not** share
the crash days. CORR-HI spends **18.6%** of its de-grossed days inside the two episodes;
CORR-LO spends **0.1%** — it is structurally *never* de-grossed in a crash. There is no shared
calendar alignment for the circular shift to destroy. H_STRIP **FAILS** in the informative
direction: deleting both episodes from the tape *raises* CORR-LO's excess (+0.0341 → +0.0517),
and it survives all three alignment-preserving nulls (+0.0568 / +0.0519 / +0.0294). H_ALIGN
**FAIL** (8 of 18 cells), H_SPLIT **FAIL** (2 of 12).

**2. THE ARTEFACT IS IN THE OTHER FOUR FAMILIES — the ones idea 606 published as its headline.**
H_INVERT **PASS**: EPISODEFIX removes the excess in **4 of 4 prior-direction families** and **0
of 2** positive-BLOCK reversed families. Idea 606's four headline levels
(+0.0737 / +0.0420 / +0.0280 / +0.0210) become **+0.0041 / −0.0062 / −0.0076 / −0.0279** once
the null is required to sit out the crash exactly as the real arm does. Mechanism, measured:
ρ(share of a gate's de-grossed days inside the two episodes, EPISODEFIX − BLOCK) = **−1.000
across the 8 families and −0.780 across all 3,456 individual arms**. *The more a gate sits on
the crash, the more of its published excess a crash-preserving null takes back.* So idea 606's
reversal control did not fail on CORR — **the reversal control is the wrong test**, because the
null is broken in the opposite direction from the one the queue suspected.

**3. THE WARM-UP CHANNEL IS WORTH NOTHING.** BLOCK is free to roll firing days into the
pre-threshold region where the real arm cannot fire (1.4–1.7% of placebo firing days land
there). Removing exactly that freedom (BLOCKPOST) moves the excess by **−8.5% to +13.6%** on
every family. Ruled out, and reported because it was the run's other candidate explanation.

**4. RAND IS NOT A NULL.** Its excess is **+0.17 to +0.25 on all eight families, share>0 =
1.000 everywhere**, an order of magnitude above BLOCK — it destroys run lengths, so the placebo
pays switch cost on isolated days. Any conclusion drawn from a RAND-differenced excess is a
statement about turnover.

## [4] Rule 8 on the statistic — H_WF **FAIL**, with one exception

Excess fitted on 2009-2016, read on 2017+: ρ(IS, OOS) ≥ +0.30 on **1 of 8** families under
BLOCK. Two families are outright negative (VOL20-HI −0.257, DISP-HI −0.253). The single family
that does persist is **CORR-LO** — ρ **+0.392** (BLOCK) / **+0.468** (YEARBLOCK), IS +0.0414 →
OOS +0.0269 and IS +0.0577 → OOS +0.0572. The one family the queue suspected of being an
artefact is the only one whose excess walks forward.

## [5] Rule 8 on the books — and why this is still a KILL

Comparands @10 bps, weekly, t+1 — U56: SPY 15.13%/0.885/−33.72% (H 0.959/0.824; OOS
15.27%/0.874), RULES v2 8.64%/1.208/−11.90% (OOS 1.286). B136: SPY 15.16%/0.886/−33.72%, RULES
v2 7.98%/1.101/−12.18%. SMALL: SPY 14.06%/0.858/−33.72%, RULES v2 4.30%/0.663/−13.89%.

**The excess is real and the money is not.** CORR-LO's 432 books: **4a 0/432, 4b 0/432**, median
Sharpe 0.972 (against CORR-HI's 1.061), median CAGR 9.80%, best OOS Sharpe 1.127. Of its 36
rule-8 IS-only picks, **1 clears 4b out of sample and 0 beat RULES v2**. Census over all 3,456
grid points: 4a **1**, 4b **378**; 288 rule-8 picks beat SPY OOS in 186, RULES v2 in 16,
clear 4b OOS in 58. Cost ladder on the full-sample 4b legs: 457 (0 bps) → 389 (10) → 330 (25).

**The statistic and the bar are decoupled, and in opposite directions.** CORR-LO has the most
persistent excess of the eight and the worst books; CORR-HI has the excess EPISODEFIX erases and
**131 of 432 4b passes**. Whatever the placebo-differenced excess measures, it is not what 4b
rewards.

**By-product, NOT proposed** (memo written, `2026-09-15_CORR-HI-U56-BYPRODUCT_MEMO.md`): 35 of
288 rule-8 picks clear 4b on the full sample *and* out of sample. Best is **U56 CORR-HI q=0.17
w=504 depth=1.00 daily g=1.00 @10bps: 14.04%/1.240/−15.93%** (H 1.169/1.310), **OOS
15.66%/1.402/−11.31%**, 4b at 0/10/25 bps, 4a FAILS. Its B136 twin reproduces idea 606's
committed by-product (14.04%/1.156/−15.04%, OOS 14.30%/1.210 vs 606's 14.02%/1.154/−15.11%, OOS
14.29%/1.208) — an independent replication on a different tape vintage. It is not promoted: it
is the best of 35 passes read off a 3,456-cell grid, and **this run's own headline says its
family's placebo excess is the episode**.

## Caveats

SURVIVORSHIP: all three panels are current-constituent lists (the small panel additionally drops
the 52 tickers with `max_1d_move` ≥ 1.0 per `data/small_meta.csv`), so CAGR and drawdown
*levels* are optimistic throughout; the placebo differencing and the real-minus-null contrasts
are the durable part. Every panel's binding drawdown is 2020, which is exactly the day set the
EPISODEFIX null holds fixed — that is the point of the test, and it also means the four
prior-direction families have almost nothing left to be measured on once it is held.

## Verdict

**KILL for capital.** No RULES change, no PROTOCOL edit applied. `RULES.md`, `PROTOCOL.md`,
`scan.py`, `bot.py` and `baseline.py` untouched. Follow-ups filed: 869, 870, 871.

## Reconciliation with lane C's concurrent, independent run of the same idea

Lane C ran idea 815 in parallel (commit `eef6ebf`, script `..._C.py`, 10,368 gated / 248,832
placebo cells, 12 placebo kinds including a `BLOCKYEAR`/`BLOCKEP` factorial and a ±shift ladder);
this run's commit landed second and neither saw the other's work. **The two runs agree on every
substantive point, from independently written code and different episode boundaries**
(C: COVID_TIGHT to 2020-04-07; here: to 2020-03-23):

| | lane C | here |
|---|---|---|
| the queue's premise | **refuted** — the tails are calendar-disjoint | **refuted** — same |
| CORR-HI de-grossed days in episodes | 0.2335 | 0.186 |
| CORR-LO de-grossed days in episodes | 0.0000 | 0.001 |
| CORR-LO under a calendar+run-length-preserving null | **+0.0468** (share 0.965), nearly doubles | **+0.0519** (share 0.965), +52% |
| the four prior-direction families | **collapse, three flip sign** | **collapse, three flip sign** (4 of 4 removed) |
| the claim under rule 8 | passes | CORR-LO is the 1 of 8 that persists (ρ +0.392/+0.468) |
| the book | **4b 0 of 1,152, 4a 0** | **4b 0 of 432, 4a 0** |
| verdict | KILL for capital | KILL for capital |

The one difference worth naming: lane C reads the claim as passing rule 8 outright, while this run
reports it as 1 of 8 families passing a ρ ≥ +0.30 bar — the same underlying fact (CORR-LO is the
only family whose excess walks forward), stated against a stricter pre-registered bar here.
Lane C additionally proposes a PROTOCOL line; this run files it as follow-up 871 instead. Neither
run promotes a book.
