# Idea 316 — is-CONCENTRATION-in-narrow-markets-a-general-clause-or-one-2022 (lane C, 2026-09-07) — **KILL**

Script: `research/backtests/2026-09-07_is-CONCENTRATION-in-narrow-markets-a-general-clause-or-one-2022_C.py`
Console: `..._C.console.txt` · Grid: `..._C.grid.csv` · Effects: `..._C.effects.csv` ·
Episodes: `..._C.episodes.csv` · Yearly: `..._C.yearly.csv`

## The question
Idea 48 killed the conditional fraction clause but isolated one live mechanism inside it: on
narrow-breadth days the hybrid holds FEWER names than its broad leg, worth ~+0.6 pp/yr of book
return on 13.3% of days, bought with 3.2 pp of drawdown — on effectively ONE episode (2022 is
91% narrow on U56). The queue asks whether that effect has a general sign on panels with more
and differently-timed narrow episodes, and pre-registers the consequence: **if the sign does
not survive outside 2022, no fraction clause of any form belongs in RULES.**

## Form (and why it is not idea 48's literal wording)
`ceil(f·E_t)` concentrates on U56 (E_t≈37) but on SMALL439 (E_t≈141) it holds ~50–100 names,
i.e. it would *dilute* a 20-name book. The clause is therefore written multiplicatively,
relative to the book's own broad leg, so it concentrates by construction on every panel:

    k_broad,t = min(20, E_t)
    CONC(q,c): narrow if E_t <= Quantile_q(E_{<=t-1}) (expanding, min 252, shifted — causal)
               -> k_t = max(1, round(c · k_broad,t));  broad -> k_t = k_broad,t
    equal weight GROSS/k_t either way, so realised gross is 0.75 in BOTH regimes.

Exposure is matched by construction, so `d = r(CONC) − r(NF20)` is concentration and nothing
else. Tuned (2): `q ∈ {0.10,0.20,0.30,0.40}` × `c ∈ {0.25,0.35,0.50,0.75}` (k_narrow ≈ 5/7/10/15)
= 16 points on **each** of three panels, **all 48 reported**. Fixed, not searched: n0=20,
gross 75%, scorer without `/sqrt(vol20)`, 200d+vol20<0.60 eligibility, weekly, 10 bps, t+1.
Controls at the pre-registered (q=0.20, c=0.35): NF20 (parent 1), CONC-ALW (parent 2,
concentrate always), **DILUTE** (narrow → `min(40, E_t)` names: the opposite sign — the sign
test), FRAC (idea 48's literal wording, with its realised name count printed), N20.

**Contamination declared:** 2022 sits in rule 8's OOS window and the hypothesis was generated
from 2022, so full-sample and per-year numbers are description. The evidence is the ex-2022
and per-episode signs, the walk-forward, and whether the clause beats both parents.

## Premise — partly false, and stated as such
U56 reproduces idea 48 exactly at q=0.20 (591 narrow days, 13.3%, 91% of 2022). The other two
panels are **not** materially richer in episodes; what they do is dilute 2022's weight:

| panel | q=0.20 narrow days | share | episodes (≥5d) | share of narrow days in 2022 | years with any |
|---|---|---|---|---|---|
| U56 | 591 | 13.3% | 20 | 38.6% | 11/18 |
| B136 | 555 | 12.5% | 17 | 36.4% | 11/18 |
| SMALL439 | 665 | 16.9% | 17 | 25.1% | 14/16 |

## Result — the sign does not generalise
Effect on narrow-state days, annualised (pp/yr on those days), and the book-level consequence:

| panel | narrow-day effect >0 | mean | **ex-2022 >0** | mean ex-2022 | book dSharpe >0 | dMaxDD better | OOS dSharpe >0 |
|---|---|---|---|---|---|---|---|
| U56 | 13/16 | **+5.17** | 13/16 | **+4.45** | 1/16 (−0.020) | 0/16 (−4.92 pp) | 9/16 (+0.004) |
| B136 | 8/16 | −1.46 | **4/16** | **−5.87** | 0/16 (−0.046) | 0/16 (−5.47 pp) | 3/16 (−0.043) |
| SMALL439 | 6/16 | −3.06 | **6/16** | **−2.60** | 6/16 (−0.055) | 3/16 (−5.00 pp) | 5/16 (−0.045) |
| **pooled 48** | **27/48** | — | **23/48** | — | **7/48** | **3/48** | 17/48 |

At the pre-registered (q=0.20, c=0.35) the narrow-day effect is **+6.49 pp/yr on U56**
(idea 48's FRAC wording gives +6.35 there, so this replicates), **−0.16 on B136** (ex-2022
**−7.34**) and **−3.85 on SMALL439** (ex-2022 **−5.53**). Books at that point:

| panel | CONC CAGR/Sharpe/MaxDD | H1/H2 | OOS CAGR/Sharpe/MaxDD | NF20 (clause deleted) | 4a | 4b |
|---|---|---|---|---|---|---|
| U56 | 13.6% / 1.057 / −24.6% | 0.97/1.13 | 16.6% / 1.188 / −24.6% | 12.8% / **1.070** / −18.3%, OOS 1.137 | no | no (DD) |
| B136 | 12.7% / 0.876 / −27.5% | 1.03/0.76 | 12.7% / 0.831 / −27.5% | 13.0% / **0.943** / −20.1%, OOS 0.883 | no | no (H2,OOS,DD) |
| SMALL439 | 5.4% / 0.379 / −40.8% | 0.47/0.31 | 6.6% / 0.427 / −40.8% | 6.4% / **0.449** / −33.5%, OOS 0.464 | no | no (all five) |

SPY over the same sample: 15.2% / 0.889 / −33.7% (SMALL439's calendar: 14.1% / 0.862).
RULES v2 (live) on each panel: 8.7%/1.206, 8.0%/1.106, 3.8%/0.572.

## The four things that kill it
1. **The sign is a coin flip off U56.** 27/48 points positive on narrow days, 23/48 with 2022
   removed; on the two panels the queue nominated, the mean effect is **negative** both with
   and without 2022. On U56 the effect *is* real and *does* survive ex-2022 (13/16, +4.45
   pp/yr) — the "one episode" framing is too strong there — but it is a U56 fact, not a clause.
2. **It never converts into a book.** Even where the narrow-day rate is positive, the extra
   variance costs more than it earns: **book dSharpe > 0 in 7/48** and **drawdown is worse in
   45/48** (mean −5.1 pp). **4a 0/72 rows.** The only 4b passes among the 48 CONC points are
   the four U56 `c=0.75` cells (the weakest possible edit, k_narrow 15 vs 20), and every one is
   dominated by NF20 itself (1.044/1.033/1.035/1.030 vs **1.070**).
3. **The sign test fails.** DILUTE — the same regime flag doing the OPPOSITE thing, holding up
   to 40 names when breadth collapses — beats CONC on all three panels and beats NF20 on U56
   (1.073/−18.0% vs 1.070/−18.3%, 4b pass). If concentration were the mechanism, its negation
   could not be the better book on the panel where the effect was found.
4. **Rule 8 does not select it.** (q,c) on 2009–2016, 2017–2026 read once:

| panel | S1 IS-Sharpe pick | OOS CAGR/Sharpe/MaxDD | 4b | NF20 control OOS | 4b |
|---|---|---|---|---|---|
| U56 | q0.40 c0.25 | 17.2% / 1.106 / **−26.9%** | **fail (DD)** | 14.5% / 1.137 / −18.3% | **pass** |
| B136 | q0.40 c0.25 | 14.9% / 0.859 / −28.4% | fail (H2,OOS,DD) | 12.4% / 0.883 / −20.1% | fail (H2 only) |
| SMALL439 | q0.40 c0.75 | 7.3% / 0.479 / −31.2% | fail (all five) | 6.9% / 0.464 / −33.5% | fail (all five) |

   The chooser lands on the *most* concentrated cell on the two large panels and blows the
   drawdown cap; the clause-deleted control passes on U56 and fails on strictly fewer bars on
   B136. No pick beats the live book's OOS Sharpe (1.285 / 1.119 / 0.568) anywhere.

Parents (pre-registered point, U56/B136/SMALL439): CONC loses to NF20 on Sharpe 3/3
(−0.013/−0.067/−0.070) and beats CONC-ALW only on U56 (+0.086/−0.013/−0.029) — so on the two
nominated panels it loses to **both** parents, failing idea 317's bar harder than idea 48's
clause did.

## Verdict — KILL
The narrow-day concentration effect is **not a general clause**. It is positive on U56 (and
there it is not merely 2022), negative in the mean on B136 and SMALL439 with and without 2022,
a coin flip pooled, and at book level it costs Sharpe on 41 of 48 points and drawdown on 45.
Its own negation is the better book on the panel that generated it, and rule 8 selects cells
that fail 4b where the clause-free control passes. Per the queue's pre-registered rule:
**no fraction clause of any form belongs in RULES.** No RULES change. No memo.

## Caveats
All three panels are current-constituent lists (56 / 136 / sub-$2B screen per
`data/SMALL_PANEL_README.md`, 44 names dropped for `max_1d_move >= 1.0`), so absolute CAGRs are
optimistic; the CONC-vs-NF20 contrast is the durable part. SMALL439 starts 2010 so its IS window
is 2011–2016 and its SPY comparison uses its own calendar. `n0 = 20` is fixed across panels
(the record's count), which is the only reason the SMALL439 broad leg holds 20 of 439 names;
the concentration ratio `c`, not the absolute count, is what is being tested.

## By-products for the queue
* **DILUTE beats CONC on all three panels and NF20 on U56** — widening into narrow markets
  (up to 40 names at constant gross) is the better half of this dial and has never been swept.
  Queued as idea 318.
* **The narrow-day effect is panel-ordered U56 > B136 > SMALL439 (+5.17 / −1.46 / −3.06)** —
  the same U56 > B136 > SMALL439 ordering ideas 51/312 found for the gate premium, on a
  completely different instrument. Queued as idea 319.
