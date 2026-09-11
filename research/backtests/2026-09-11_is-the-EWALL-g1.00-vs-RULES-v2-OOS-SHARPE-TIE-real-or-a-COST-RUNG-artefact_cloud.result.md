# Idea 733 — is the EWALL-g1.00 vs RULES-v2 OOS-Sharpe TIE real, or a COST-RUNG artefact?

**2026-09-11, cloud.  ANSWERED: the tie is REAL and survives every cost rung — but it is not a
contest between two books.  Idea 727's "EWALL g1.00" IS the live book's own gate at a different
gross, so the dead heat is Sharpe's gross-invariance on a de-grossing book, not evidence about a
rival rule.  The run's substantive by-product is a 4b KEEP-candidate: the live book at gross
1.00 instead of 0.75.  No RULES change applied (rule 6, Sunday review only).**

Script: `2026-09-11_is-the-EWALL-g1.00-vs-RULES-v2-OOS-SHARPE-TIE-real-or-a-COST-RUNG-artefact_cloud.py`
Artefacts: `.grid.csv` (288 cells, every grid point) · `.walkforward.csv` · `.gates.csv` · `.console.txt`

## Setup
Two tuned parameters, both published in full: **gross** g ∈ {0.50, 0.60, 0.70, 0.75, 0.80, 0.90,
1.00, 1.10, 1.25} × **cost** c ∈ {0, 5, 10, 15, 20, 25, 35, 50} bps.  Reported axes (never tuned):
panel ∈ {U56 = `load_universe()`, 55 tradables; B136 = `load_universe(broad=True)`, 135 tradables},
gate ∈ {EW_BAND = RULES v2's 200d ±3% hysteresis band; EW_ELIG = RULES v1's un-ranked eligibility,
above 200d AND vol20 < 0.60}.  Weekly cadence, t+1 execution, 260-day warm-up skip (scored from
2009-01-13), IS/OOS boundary 2016-12-31.  Both books **de-gross**: g/N_priced per name when the
name's own gate is ON, 0.0 otherwise, so gated-out weight becomes CASH and is never re-spread.
SPY is a benchmark column only and is dropped from every weight frame.
**PROTOCOL 2** (no leverage unless the idea says so — it does not): only g ≤ 1.00 is **admissible**;
g ∈ {1.10, 1.25} is carried as a reported ladder extension and excluded from every KEEP tally and
every rule-8 pick.

## Gates
| gate | result |
|---|---|
| G1 cost linearity (r(c) = r(0) − turnover·c/1e4) | **max\|gap\| 0.000e+00** on all 3 probe cells, both panels — every cost rung is derived exactly |
| G0b idea 727's published pair, **EW_BAND** g1.00 @10bps | U56 **1.2827** vs published 1.2827 (**d +0.0000**); B136 **1.1195** vs 1.1195 (**d +0.0000**) — **MATCH** |
| G0b idea 727's published pair, **EW_ELIG** g1.00 @10bps | U56 1.2459 (d −0.0368); B136 1.0834 (d −0.0361) — **no match** |
| G0b published RULES v2 comparand | U56 **1.2834** vs 1.2834; B136 **1.1206** vs 1.1206 — **MATCH** |
| G0a SPY-denominator convention (idea 740) | `baseline.rules_v2_weights` counts SPY in its N_priced denominator: N-incl-SPY reproduces the helper **exactly (0.000e+00)**, N-excl-SPY differs by **6.542e-04** (U56) / **2.562e-04** (B136) in daily returns, worth **1e-4 of OOS Sharpe** (1.2834 vs 1.2835 on U56, identical 1.1206 on B136) |

**G0b settles the identification the QUEUE entry left open.** The record's "EWALL" in idea 727 is
the *band* gate, i.e. the live book's own clause, not the v1 eligibility mask.  So the published
0.0007 / 0.0011 gaps compare **RULES v2 at gross 1.00 against RULES v2 at gross 0.75** — one dial,
one book.

## 1. The tie is real, holds at every cost rung, and is a gross-invariance identity
`d(OOS Sharpe) = EW_BAND g1.00 − RULES v2 g0.75`, all 8 cost rungs:

| panel | 0 | 5 | 10 | 15 | 20 | 25 | 35 | 50 bps | sign | \|d\| max |
|---|---|---|---|---|---|---|---|---|---|---|
| U56 | −0.0008 | −0.0008 | −0.0007 | −0.0007 | −0.0006 | −0.0005 | −0.0004 | −0.0002 | −/−/−/−/−/−/−/− | **0.0008** |
| B136 | −0.0013 | −0.0012 | −0.0011 | −0.0010 | −0.0009 | −0.0009 | −0.0007 | −0.0004 | −/−/−/−/−/−/−/− | **0.0013** |

Negative at all 16 (panel, cost) points and **never larger than 0.0013** — so the dead heat is not
the 10 bps rung's doing; if anything it *narrows* with cost (on full-sample Sharpe it flips sign at
25 bps, −0.0002 → +0.0004), because turnover scales with gross (2.37 vs 1.79/yr on U56; 2.68 vs
2.02/yr on B136) at almost exactly the same ratio as vol, so the cost drag is itself nearly
gross-invariant.

The mechanism, measured directly at 10 bps over the admissible range g 0.50 → 1.00:

| panel · gate | full Sharpe | spread | OOS Sharpe | spread | CAGR | MaxDD |
|---|---|---|---|---|---|---|
| U56 EW_BAND | 1.2070 → 1.2067 | **0.0002** | 1.2840 → 1.2827 | 0.0013 | 5.73% → **11.55%** | −8.01% → **−15.70%** |
| U56 EW_ELIG | 1.1129 → 1.1128 | 0.0001 | 1.2470 → 1.2459 | 0.0012 | 4.85% → 9.74% | −7.35% → −14.41% |
| B136 EW_BAND | 1.1078 → 1.1077 | 0.0001 | 1.1216 → 1.1195 | 0.0021 | 5.34% → **10.73%** | −8.20% → **−16.08%** |
| B136 EW_ELIG | 1.0568 → 1.0562 | 0.0005 | 1.0860 → 1.0834 | 0.0026 | 4.80% → 9.62% | −8.15% → −15.95% |

Doubling gross moves Sharpe by 1–5 units in the fourth decimal while **doubling both CAGR and
MaxDD**.  The tie therefore carries no information about the books: for a de-grossing book at zero
cash rate, gross is a pure scale on return *and* vol, and the record's 0.0007 is the rounding
residue of that identity — only ~7x the 1e-4 that the SPY-denominator convention alone is worth.

**The tie does NOT extend to the other reading.** The EW_ELIG book is a genuinely different and
worse book, and the gap widens monotonically with cost: **−0.0115 → −0.1422 OOS Sharpe** on U56
and **−0.0135 → −0.1325** on B136 from 0 to 50 bps, because it turns over **4.40 / 4.57 per year**
against the band book's 1.79 / 2.02.  Had idea 727 run the eligibility gate, there would have been
no tie to ask about.

## 2. KEEP paths over the 224 admissible cells
**4a: 0 / 224** (and 0/224 on the OOS restatement) — a higher-gross copy of the live book cannot
beat the live book's MaxDD leg by construction.
**4b: 11 / 224 full-sample, 20 / 224 on the OOS-window restatement.** All 11 are EW_BAND;
**EW_ELIG passes 4b nowhere on either panel at any gross or cost.**
(Inadmissible leverage rungs, reported only: 4b 49/64 full.)

At the PROTOCOL **10 bps** rung exactly **two** admissible cells clear 4b full-sample, and both are
the same change:

| cell | CAGR | Sharpe | MaxDD | H1 / H2 | OOS Sharpe | OOS CAGR | OOS MaxDD | turn/yr | dies above |
|---|---|---|---|---|---|---|---|---|---|
| **U56 EW_BAND g1.00** | **11.55%** | 1.2067 | **−15.70%** | 1.2405 / 1.1798 | **1.2827** | 12.70% | −15.70% | 2.37 | **35 bps** |
| **B136 EW_BAND g1.00** | **10.73%** | 1.1077 | **−16.08%** | 1.2323 / 0.9850 | **1.1195** | 10.66% | −16.08% | 2.68 | **10 bps** |
| live RULES v2 g0.75 (U56) | 8.63% | 1.2069 | −11.90% | 1.2400 / 1.1806 | 1.2834 | 9.48% | −11.90% | 1.79 | — |
| live RULES v2 g0.75 (B136) | 8.03% | 1.1078 | −12.18% | 1.2312 / 0.9861 | 1.1206 | 7.98% | −12.18% | 2.02 | — |
| SPY (U56 window) | 15.11% | 0.8835 | −33.72% | — | 0.8721 | 15.24% | −33.72% | — | — |

The live book at g0.75 **fails 4b on the CAGR floor** (8.63% vs the 10.58% bar = 70% of SPY's
15.11%; B136 8.03% vs 10.66%) and nothing else.  4a fails for g1.00 on **both** legs, not just
MaxDD: H2 1.1798 vs the live book's 1.1806.  Because Sharpe is flat in gross and CAGR is proportional to it, **gross
is the only dial that moves the binding bar**, and g=1.00 clears it while MaxDD (−15.70% / −16.08%)
stays inside the 60%-of-SPY cap (−20.23%).  That is the whole of the finding.

## 3. Rule-8 walk-forward (gross chosen on IS ≤ 2016 only; 2017–2026 untouched)
| panel · gate | selector | pick | OOS Sharpe | OOS CAGR | OOS MaxDD | vs RULES v2 OOS (1.2834 / 9.48% / −11.90% · 1.1206 / 7.98% / −12.18%) | vs SPY OOS (0.8721 / 15.24% · 0.8820 / 15.45%, −33.72%) | 4b OOS |
|---|---|---|---|---|---|---|---|---|
| U56 EW_BAND | S1 max IS Sharpe, admissible | **g1.00** | 1.2827 | **12.70%** | −15.70% | −0.0007 Sharpe, **+3.22 pp CAGR** | +0.41 Sharpe, −2.54 pp CAGR, **half the drawdown** | **PASS** |
| U56 EW_BAND | S2 memo's pre-stated rule | — | — | — | — | — | — | **INFEASIBLE** |
| B136 EW_BAND | S1 max IS Sharpe, admissible | **g1.00** | 1.1195 | 10.66% | −16.08% | −0.0011 Sharpe, **+2.68 pp CAGR** | +0.24 Sharpe, −4.79 pp CAGR, half the drawdown | **FAIL** (CAGR 10.66% vs bar 10.82%, by **0.16 pp**) |
| B136 EW_BAND | S2 memo's pre-stated rule | g1.00 | 1.1195 | 10.66% | −16.08% | same cell | same cell | **FAIL**, same 0.16 pp |
| U56 EW_ELIG | S1 max IS Sharpe, admissible | g1.00 | 1.2459 | 11.02% | −14.41% | −0.0375 Sharpe | +0.37 Sharpe | fails 4b full |
| B136 EW_ELIG | S1 max IS Sharpe, admissible | g1.00 | 1.0834 | 9.59% | −15.95% | −0.0372 Sharpe | +0.20 Sharpe | fails 4b full |

**Two honest qualifications on the walk-forward, both against the candidate:**
1. **The selector is indifferent, not discriminating.** IS Sharpe across the admissible gross range
   spans ~1e-4, so "max IS Sharpe picks g=1.00" is decided in the fourth decimal place — noise, not
   selection.  The candidate's case rests entirely on the pre-stated *mechanism* (the CAGR floor is
   the only binding bar and gross is the only dial that moves it), not on the IS pick.
2. **The memo's own pre-stated selector is infeasible in-sample on U56.** "Smallest G whose MaxDD ≤
   60% of SPY's and CAGR ≥ 70% of SPY's", read on the IS window alone, returns **no admissible
   gross** on U56 (g1.00's IS CAGR 10.18% misses the IS bar of 10.47% by 0.29 pp) and g1.00 on B136.
   The live 0.75 was set by that rule's *fallback* clause, not by the rule.

## Verdict
**ANSWERED (the QUEUE question) + 4b KEEP-CANDIDATE (the by-product), PARK on B136.**
The tie is real, cost-rung-independent, and uninformative — it is one book at two grosses. The
candidate it exposes is `RULES v2 at gross 1.00`: 4b-clean on U56 at 10 bps in both halves and
out-of-sample and robust to 35 bps, 4b-clean on B136 full-sample but **0.16 pp short on the OOS
CAGR floor** and dead above 10 bps there.  Memo written with exact RULES wording.
Nothing applied: RULES.md, PROTOCOL.md, scan.py, bot.py, baseline.py untouched (rule 6).

## Caveats
Survivorship: `universe.json` / `universe_broad.json` are **current** constituents, which favours
the momentum/trend sleeve this book is.  The scored window starts **2009-01-13** (260-day warm-up),
so **2008 is excluded** — a de-grossing book at gross 1.00 has no cash cushion and its behaviour in
a 2008-style event is untested here; the worst drawdown in sample is −15.7% / −16.1% against SPY's
−33.7%.  Only 2020 and 2022 are genuine stress tests.  The 4b CAGR and DD bars are both SPY-relative
and SPY's own numbers are window-dependent.  g=1.00 is full investment, not leverage (PROTOCOL 2
respected), but it removes the 25% cash buffer the live book currently carries.
