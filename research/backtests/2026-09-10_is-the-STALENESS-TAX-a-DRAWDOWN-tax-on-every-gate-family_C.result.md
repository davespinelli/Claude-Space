# Idea 665 — is the STALENESS TAX a DRAWDOWN tax on every gate family?

**Lane C, 2026-09-10.** Scripts `2026-09-10_is-the-STALENESS-TAX-a-DRAWDOWN-tax-on-every-gate-family_C.py`
(+ `_C_addendum.py`). 2 tuned params: **gate family × lag**. 288 grid points, all reported.

## Verdict

**KILL for capital. ANSWERED and SPLIT for the record: the queue's "every gate family" is FALSE,
but the mechanism behind it is real and now named.**

The staleness tax is a drawdown tax **exactly to the extent the fresh gate was buying drawdown
protection** — not because it is a gate. Across 84 (panel × family × lag>0) arms at matched gross
0.75: **DD_TAX 51 (60.7%), RETURN_TAX 24 (28.6%), MIXED 9 (10.7%)**, and the split is a family
property, not noise:

| family | DD_TAX | RETURN_TAX | MIXED | median r_DD | median r_CAGR | flip/day (U56) | MaxDD(L=0) |
|---|---|---|---|---|---|---|---|
| TREND (200d ±3% band = RULES v2) | **21/21** | 0 | 0 | **+0.476** | −0.034 | 0.0069 | −12.05% |
| VOL (vol20 < 0.60) | 17/21 | 2 | 2 | +0.316 | +0.014 | 0.0057 | −16.88% |
| BREADTH (≥50% of panel above 200d MA) | 10/21 | 9 | 2 | +0.000 | −0.005 | 0.0262 | −18.7% |
| MOM (12-1 > 0) | 3/21 | **13/21** | 5 | **+0.000** | +0.036 | 0.0223 | −19.67% |

`r_CAGR = −ΔCAGR/|CAGR(0)|`, `r_DD = −ΔMaxDD/|MaxDD(0)|`; DD_TAX iff `r_DD > 2·r_CAGR`
(the 2× bar was fixed in the header before any number was read). At idea 661's own rungs
**L=42 and L=63, DD_TAX is 18/24 (75.0%)** — the queue's headline is right three times in four
and wrong for MOM on every panel.

## The mechanism (n=12 panel × family cells, L=42)

`r_DD` ranks **+0.73 (Spearman; Pearson +0.64)** against the **drawdown protection the fresh gate
buys** (|SPY MaxDD| − |MaxDD(L=0)|: 21.5–21.7 pp for TREND on all three panels, 11.3–16.3 pp for
MOM, −2.0 pp for SMALL484 BREADTH, which protects nothing), **−0.64** against
the gate's **flip rate**, and **+0.05 — nothing — against `off_share`**, how much the gate
de-grosses. A gate that de-grosses a lot but never protected you loses nothing to staleness; the
band gate, the record's best crash brake, loses the most. TREND's staleness is *free in return*
(median r_CAGR −0.034: it slightly **helps** CAGR) and costs up to **−11.00 pp** of MaxDD.

## PROTOCOL rule 8 — the sharpest form of the result

(lag, gross) fitted on 2009–2016 IS Sharpe only, scored 2017–2026 untouched, 12 picks:

- **11 of 12 picks choose a NON-ZERO lag** — in-sample, staleness looks free.
- Against FRESH at the same gross, those 11 picks lose **−0.043 mean OOS Sharpe (9/11 worse)**,
  give up **−4.19 pp mean OOS MaxDD (9/11 deeper)**, and **gain +0.29 pp of OOS CAGR**.
  The fitter buys staleness with return it never had to spend, and pays out of sample in drawdown.
- Worst cases: U56 VOL L=42 (−7.02 pp OOS DD), B136 VOL L=42 (−8.21), SMALL484 TREND L=21
  (−10.31), SMALL484 VOL L=21 (−15.17).
- 8/12 picks beat SPY's OOS Sharpe; **0/12 beat the live book**; **12/12 sit at g=1.00**
  (idea 311/657's gross loophole again).

## KEEP paths (PROTOCOL 4)

**4a 0/288. 4b 14/288. BOTH 0/288.** Every 4b passer is TREND or VOL on U56/B136 at
**L ∈ {0,1,2,5}** (L=0: 4, L=1: 4, L=2: 4, L=5: 2, **L≥10: 0**) and at g ∈ {0.75, 1.00} only —
i.e. the passers are the *fresh* book the record already owns, not a new one. Rule-8 picks
clearing 4b at 0/10/25 bps: **2/2/1 of 12**, both of them TREND at g=1.00 (U56 L=2, B136 L=0),
which is RULES v2 re-grossed. **No new capital-worthy book. KILL.**

## Addendum — a placebo defect found and corrected in-run

The main script's SCRAMBLE placebo reads the gate at a large past offset (252–1008 d). `shift(O)`
is False for the first O rows, so at O=1008 the U56 TREND book is **all cash until 2012-10-15**
(mean ON share 0.115 over 2009–2013 vs 0.676 at O=42). A flat book cannot draw down, so the main
run's "saturated" scale (mean ΔMaxDD −0.03…−0.09 pp) was an **artefact**. `_C_addendum.py`
re-prices the lag ladder *and* the placebo on one warm-up-clean common window
(`index[260+1008]`, ≈2012-10 → 2026):

- **C1 (the queue's question) SURVIVES unchanged**: DD_TAX 54/84 (64.3%) over the ladder and
  **18/24 (75.0%) at L∈{42,63}** — identical to the contaminated window; family split unchanged
  (TREND 21/21 DD_TAX, MOM 15/21 RETURN_TAX).
- **C2 (intermediate staleness worse than TOTAL de-alignment) only HALF survives.** Corrected,
  the scramble costs a real −5 to −9 pp of MaxDD, not ~0. At L∈{21,42,63}, **19 of 36 arms** are
  more than 1 draw-sd worse in MaxDD than their own scramble mean (median frac 1.16, median
  z −1.08); worst B136 VOL L=42 (z −3.45), U56 TREND L=42 (−2.91), SMALL484 VOL L=42 (−2.76).
  So a stale-but-correlated read is *modestly* worse than a random one on about half the arms —
  a real anti-alignment effect, not the dramatic one the artefact suggested.

Rule 8's numbers are unaffected: its OOS window opens 2017-01-01, years past any L ≤ 63 warm-up.

## Gates (all PASS, pre-registered)

G1 TREND@L=0,g=0.75 **is** `rules_v2_weights`: max|ΔW| **0.000e+00**, max|ΔR| **0.000e+00**.
G2 cost-rung identity r(25)=r(0)−turn·25/1e4: **0.000e+00**. G3 lag is a pure shift of the gate
state and no unpriced name is ever held. G4 all 12 (panel × family) gates non-degenerate
(off_share 0.052–0.526, flip 0.0053–0.0489). G5 gross scales the book exactly.

## Caveats

10 bps, next-day execution, weekly, no shorting/leverage; rungs 0/10/25 reported on the rule-8
picks. **SURVIVORSHIP:** B136 and SMALL484 are *current* constituents of their screens
(`data/SMALL_PANEL_README.md`). n=12 for the mechanism correlation — it orders four families on
three panels, it does not establish a law. The four families are the record's committed ones as
named by QUEUE 665; a fifth family could break the ordering.
