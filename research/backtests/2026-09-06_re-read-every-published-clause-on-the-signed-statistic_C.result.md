# Idea 211 — re-read every published clause on the signed statistic (lane C, 2026-09-06)

**ANSWERED. KILL of the two-sided `|dSharpe|` reading of clause 11/11b; the signed reading
replaces it as the REPORT-ONLY column. Still a KILL as a selection gate under BOTH statistics.
No RULES change, no new book, no KEEP candidate.**

Script `2026-09-06_re-read-every-published-clause-on-the-signed-statistic_C.py`.
Outputs: `.console.txt`, `.reread.csv` (1090 verdicts x 4 arms), `.summary.csv`,
`.mechanism.csv`, `.walkforward.csv`, `.keep.csv`, `.grid.csv.gz` (the 10,980-row
per-draw grid **with signs** — the thing the record never committed).

## The two readings

    published (clause 11b)   clears  <=>  |d_real| >  band_K( |d_null| )     two-sided, "differs"
    signed (idea 190)        clears  <=>   d_real  >  band_K(  d_null  )     one-sided, "helps"

Same nominal size under exchangeability (`MAX` = 1/(K+1); `Q95` = 5%), different alternative.
2 tuned parameters — statistic {ABS, SIGNED} x band {MAX, Q95} — 4 arms, all reported on
every corpus. K held at the **published** draw count (idea 207 already swept K).

## Corpora and reproduction (nothing was read until all three passed)

| corpus | source | verdicts | how | reproduction |
|---|---|---|---|---|
| T | idea 181 keyed tilts | 360 (180 arms x F/IS) | pure re-read of the committed `grid.csv` (720 signed null rows) | published `clears` == ABS/MAX recomputed **360/360**, max\|band−committed\| **0.0e+00** |
| S | idea 190 sleeve substitution | 192 (96 Sharpe + 96 MaxDD) | pure re-read of the committed 10,344-row `null.csv` | ABS/MAX == `clears_S_strict` **96/96**; SIGNED/MAX == `argmax_full` **96/96**; max\|dSharpe−committed\| **2.8e-16** |
| O | ideas 186/191/201/207 overlays | 538 of 540 | signs **regenerated** with idea 201's `zlib.crc32` seed (idea 191's own seed is salted — idea C's null audit) | bands/dSharpe/dMaxDD vs idea 201's committed `clause.csv` **≤ 9.99e-17 on all 180 rows**; published verdicts == ABS/MAX **538/538** |

2 of 540 O verdicts dropped, counted, never imputed: SMALL439/BUDGET tau=0.05/skip at both
cost rungs have an undefined IS Sharpe (idea 207's documented cells).

**Coverage gap, stated rather than skipped:** idea 186's `null.csv` (2 summary rows per
config), idea 191's `clause.csv` (bands only, salted seed — superseded by idea 201, which
reproduces exactly), idea 207's `flip/zone/band.csv` and the 11b enumeration `exact.csv`
(K-counts on `|d|` — the enumeration **discarded the signs**). Idea 192's `repro_Tclause.csv`
is a subset of T and is counted once, inside T. The 6-row selector null of
`does-a-random-screen-de-concentrate-just-as-well_B` already publishes a signed band and
cannot move; it is listed in the console.

## Q1 — the census (1090 verdicts)

| arm | clears | gained 0→1 | lost 1→0 | of the losses, d<0 | moved |
|---|---|---|---|---|---|
| ABS/MAX (published) | 216 (19.8%) | 0 | 0 | – | 0 |
| ABS/Q95 | 300 (27.5%) | 84 | 0 | – | 84 (7.7%) |
| **SIGNED/MAX** | **182 (16.7%)** | **99** | **133** | **133 = 100%** | **232 (21.3%)** |
| SIGNED/Q95 | 239 (21.9%) | 156 | 133 | 133 = 100% | 289 (26.5%) |

**The direction is the result.** Every one of the 133 verdicts the signed reading revokes is
an arm with `d_real < 0` — a HARMFUL instrument that the published clause certified as
clearing a significance band (mean d **−0.2259** of Sharpe). Nothing with a positive effect
loses its verdict. And in **100%** of the 99 verdicts the signed reading grants, the
two-sided band's largest draw was **negative**: the record understated a real positive
effect (mean d **+0.0860**) because a harmful rotation set the bar.

By corpus (SIGNED/MAX): T Sharpe 96/360 moved (26.7%, +37/−59) · O Sharpe 56/358 (15.6%,
+0/−56) · O MaxDD 24/180 (13.3%, +6/−18) · S Sharpe 56/96 (58.3%, +56/−0) · S MaxDD 0/96.

## Q2 — the mechanism, generalised from idea 190 to the whole record

Pooled over 1090 verdicts: the two-sided band's largest-magnitude draw is **negative in
64.6%**, and the null population's mean is **negative in 65.5%**. Per corpus:
T 91.7% / 93.1% · S-Sharpe 86.5% / 89.6% · O-Sharpe 57.0% / 59.8% · O-MaxDD 48.3% / 43.9% ·
S-MaxDD 0.0% / 0.0% (drawdown nulls are the one place the band is built from helpful draws,
which is why S's drawdown verdicts do not move at all).

## Q3 — rule 8 (clause read on ≤2016-12-31 only; 2017-2026 read once)

corpus O, 18 cells (3 panels x 3 families x 2 cost rungs), mean OOS:

| selector | CAGR | MaxDD | Sharpe | dOOS vs do-nothing | t | wins |
|---|---|---|---|---|---|---|
| S0 do-nothing | 10.22% | −23.53% | 0.7766 | — | — | — |
| S1 IS-argmax, no gate | 9.55% | −25.52% | 0.7405 | −0.0361 | −1.68 | 5/18 |
| gate ABS/MAX (published) | 9.63% | −23.84% | 0.7458 | −0.0308 | −2.05 | 2/18 |
| gate ABS/Q95 | 9.47% | −24.97% | 0.7302 | −0.0464 | −3.30 | 2/18 |
| gate SIGNED/MAX | 10.26% | −23.86% | 0.7732 | −0.0034 | −0.49 | 2/18 |
| gate SIGNED/Q95 | 10.07% | −24.66% | 0.7567 | −0.0199 | −1.64 | 2/18 |
| REF RULES v1 | 4.94% | −24.93% | 0.4750 | −0.3017 | −4.20 | 3/18 |
| REF SPY | 15.45% | −33.72% | 0.8820 | +0.1054 | +1.44 | 12/18 |

corpus T, 36 cells (3 panels x 2 dirs x 3 tilt strengths x 2 cost rungs), mean OOS:

| selector | CAGR | MaxDD | Sharpe | dOOS vs do-nothing | t | wins |
|---|---|---|---|---|---|---|
| S0 do-nothing | 10.12% | −23.25% | 0.7736 | — | — | — |
| S1 IS-argmax, no gate | 12.19% | −22.46% | **0.9060** | **+0.1324** | +4.03 | 28/36 |
| gate ABS/MAX (published) | 8.69% | −24.21% | 0.7013 | **−0.0723** | −3.26 | 2/36 |
| gate ABS/Q95 | 9.57% | −24.90% | 0.7612 | −0.0125 | −0.32 | 7/36 |
| gate SIGNED/MAX | 11.42% | −23.17% | 0.8647 | **+0.0911** | +2.71 | 15/36 |
| gate SIGNED/Q95 | 11.65% | −23.14% | 0.8770 | +0.1034 | +3.06 | 19/36 |
| REF RULES v1 | 4.39% | −26.24% | 0.4229 | −0.3507 | −8.91 | 6/36 |
| REF SPY | 15.45% | −33.72% | 0.8820 | +0.1084 | +2.12 | 18/36 |

**P5 missed, and the miss is informative but is not a promotion.** On corpus T the signed
gate beats do-nothing (+0.0911, t +2.71) where the published gate destroys value (−0.0723,
t −3.26). But paired against the **ungated** IS-argmax every gate still loses, on both
corpora and both statistics: T ABS/MAX −0.2047 (t −4.34), ABS/Q95 −0.1448 (t −3.48),
SIGNED/MAX −0.0413 (t −3.24), SIGNED/Q95 −0.0290 (t −2.75); O ABS/MAX +0.0053 (t +0.18),
SIGNED/MAX +0.0327 (t +1.36), neither significant. So the thirteenth consecutive reading
holds — **the clause is not a selector under either statistic**; what the signed reading
buys is that filtering costs **5x less** (−0.041 vs −0.205 of OOS Sharpe on T).

## Q4 — both KEEP paths

360 real arms: **4a 99** (O 37, T 62), **4b 61** (O 28, T 33). Of the 61 4b passes, the
IS-window clause flags ABS/MAX 5, ABS/Q95 6, **SIGNED/MAX 10**, SIGNED/Q95 11 — so the
column still strips the significance claim from 51 of 61 (vs 56 of 61 under the published
reading). 4a/4b are computed from returns and are clause-independent by construction: the
statistic change moves **zero** KEEPs. Nothing here is a new book.

## What PROTOCOL should carry (proposal only — clause changes go via Sunday review)

Clause 11/11b should be read **signed**: `clears  <=>  d_real > band_K(d_null)`, with
`d` oriented so that positive = helps (Sharpe up, drawdown shallower). The two-sided form
should be retired as a certification, because on this record it certifies 133 harmful arms
and hides 99 helpful ones. Both columns are cheap to publish and `.reread.csv` carries them
for every one of the 1090 verdicts; nothing needs re-running to back-fill.

## Caveats carried

* SURVIVORSHIP (idea 54): every panel is current constituents; all LEVELS are biased upward
  and are not tradable estimates. Real and null draws inherit it identically, so the CLAUSE
  reading is unaffected.
* SIGNED is one-sided by construction: an arm with `d<0` can never clear it. That is the
  intent, and it means the 133 losses are **not** 133 errors — they are 133 places where a
  two-sided "differs" claim was doing duty as a "worth something" claim. Both readings are
  printed per row so either can be taken.
* Corpus O's rotations are neighbouring circular shifts and are correlated (idea 207), so
  1/(K+1) is nominal, not realised; idea 191 measured 4.8% realised on a zero-information
  control, so the approximation is good on that corpus but is an approximation.
* BUDGET-skip does not preserve turnover between real and null (idea 203); inherited.
* Idea 38: calendar-day index after 2014-09-17 on U56/BROAD136. Idea 126: t+1 only.
* PROTOCOL 2: 10 bps is binding; 25 bps carried as a reported axis.

5 of 6 pre-registered predictions hit (P5 missed; see Q3). Run time 581s regenerating,
19s from the committed grid; the cached path reproduces the regenerating run line for line
(band agreement 3.2e-16 vs 9.7e-17, both inside the 1e-12 gate).
