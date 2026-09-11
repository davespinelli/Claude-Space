# Idea 673 — how much of the record's CAND-vs-EWall premia is EXPOSURE

**Run:** 2026-09-11 UTC, lane C. **Script:** `2026-09-11_how-much-of-the-record-s-CAND-vs-EWALL-premia-is-EXPOSURE_C.py`
(console `.console.txt`, artefacts `.census.csv` / `.claims.csv` / `.grid.csv` / `.legs.csv` /
`.repriced.csv` / `.walkforward.csv`)

**Verdict: ANSWERED / SPLIT — the queue's premise is a U56 fact, not a record fact, and the
record's own "matched" label is NOMINAL, not realised.** On a fresh grid where the matched
control exists by construction, the exposure leg is larger than the selection leg in **5 of 21
panel×n cells at 10 bps — and all five are U56**, the narrow panel where a fixed-weight top-n
book runs out of eligible names. On B136 and SMALL439 exposure is +0.0004..+0.0268 Sharpe while
selection runs −0.2853..+0.1491: there, selection is the story. Of the **9 positive premia** on
the grid, the sign survives a matched control in **6 (MR-EWMG) / 8 (MR-CANDRG)** — and the two
matching rules disagree on **2 of 9**, so "at a matched gross" is not one number.
**4a 0/66, 4b 15/66, BOTH 0/66. No book promoted, no RULES/PROTOCOL change applied.**

## Gates (pre-registered, printed before any new number was read)

| Gate | Result |
|---|---|
| G1 `Panel.run` == `engine.backtest` @10 bps | **6.939e-18** PASS |
| G2 `band_book(0.03,0.75)` == `baseline.rules_v2_weights` | **0.000e+00** PASS |
| G3 CAND20 on FULL U56 == the 2026-09-04 KEEP-4b incumbent | got **12.63% / 1.0903 / −18.31%** vs published 12.66% / 1.0921 / −18.31%, max\|d\| **1.777e-03** PASS |
| G4 EWall holds gross 0.75 whenever any name is eligible | **2.220e-16** PASS |
| G4b EWmg's daily gross == CANDn's, every n, every day | **2.220e-16** PASS |
| G4c CANDrg holds gross 0.75 whenever any name is eligible | **1.110e-16** PASS |
| G5 cost-rung identity net(25) vs a live `backtest(cost_bps=25)` | **6.939e-18** PASS |
| G6 SMALL439 drops every ticker with `max_1d_move >= 1.0` | PASS (483 → 439 tradable) |

The decomposition is **exactly additive by construction** (all three legs are Sharpe differences
of the same three books): max\|PREMIUM − (SEL + EXP)\| = **1.110e-16** under both matching rules.

## Design

**TUNED (2): CLAIM SET × MATCHING RULE**, both read in full.
`n ∈ {3,5,10,15,20,30,40}` and `panel ∈ {U56, B136, SMALL439}` are structural axes, every point
reported; 10 bps is the only verdict rung (0 / 25 bps are a labelled appendix, free because the
gross-return and turnover streams are shared).

Four books per panel, all through the incumbent's own gate (above the 200d MA, vol20 < 0.60,
composite with NO vol scaler), weekly, next-day execution:
`CANDn` (top n, **fixed 0.75/n**, de-grosses to cash below n eligible) · `EWall` (every eligible
name at a **full 0.75** — the record's comparand) · `EWmg` (every eligible name at **CANDn's own
gross that day**) · `CANDrg` (CANDn's names **renormalised to 0.75**). Hence two decompositions
of the same published premium:
**MR-EWMG** = SEL(CANDn−EWmg) + EXP(EWmg−EWall) and **MR-CANDRG** = SEL(CANDrg−EWall) +
EXP(CANDn−CANDrg).

## (1) PART A — the census: what the record actually publishes

3,197 committed CSVs scanned (this run's own outputs excluded), 0 skipped. **17 files publish a
CAND-vs-EWall premium, 14,240 premium rows** (12,322 FORM A explicit `dSharpe_vs_EWall`-type
columns, 1,918 FORM B `Sharpe` vs `EW*_Sharpe` pairs). **18.6% (2,647) are positive**; the
RANKED-labelled population (12,558 rows) has median premium **−0.1168** and is positive 17.9% of
the time — the record's typical "book vs EW-all" row already loses.

| gross-match status | FORM A | FORM B | ALL |
|---|---|---|---|
| MATCHED (control at the same cell, same published gross) | 3,386 | 0 | **3,386** |
| UNMATCHED (control at the same cell, **different** gross) | 6,838 | 0 | **6,838** |
| UNKNOWN_NOCTRL (no EW control row at that cell) | 198 | 1,312 | 1,510 |
| UNKNOWN_NOGROSS (file publishes no gross at all) | 1,900 | 606 | 2,506 |

**6,838 rows quote a premium against a control at a different gross, median \|Δgross\| 0.2500.**
Re-priceable (control **and** gross present) = **10,224 of 14,240 (71.8%)**; the other 4,016
cannot be re-priced from the record at all. Panel resolution is the second limit: **9,798 of the
10,224 carry a panel label this run could not resolve**, 9,396 of them from two files whose
column *named* `panel` holds a draw/arm identifier (`cvol~POOL~L0.247206~0`), not a panel — so
those rows get a pooled slope, not their own. Counted, not guessed.

## (2) PART B — the fresh grid, 10 bps (all 21 cells reported)

| panel | n | gross(CAND) | PREMIUM | = SEL(EWmg) | + EXP(EWmg) | SEL(CANDrg) | EXP(CANDrg) |
|---|---|---|---|---|---|---|---|
| U56 | 3 | 0.7363 | −0.0004 | +0.0330 | −0.0333 | +0.0407 | −0.0411 |
| U56 | 5 | 0.7407 | −0.0914 | −0.1228 | +0.0315 | −0.1205 | +0.0291 |
| U56 | 10 | 0.7368 | −0.1157 | −0.1062 | −0.0095 | −0.1120 | −0.0037 |
| U56 | 15 | 0.7289 | +0.0003 | −0.0151 | +0.0154 | −0.0077 | +0.0080 |
| **U56** | **20** | **0.7166** | **+0.0462** | **+0.0045** | **+0.0417** | +0.0177 | +0.0285 |
| U56 | 30 | 0.6878 | +0.0496 | −0.0112 | +0.0608 | +0.0047 | +0.0449 |
| U56 | 40 | 0.6475 | +0.0741 | −0.0086 | +0.0827 | +0.0017 | +0.0724 |
| B136 | 3 | 0.7407 | −0.3051 | −0.2853 | −0.0199 | −0.3089 | +0.0038 |
| B136 | 5 | 0.7448 | −0.1450 | −0.1571 | +0.0120 | −0.1493 | +0.0043 |
| B136 | 10 | 0.7444 | −0.1323 | −0.1358 | +0.0036 | −0.1307 | −0.0016 |
| B136 | 15 | 0.7416 | −0.1023 | −0.1194 | +0.0171 | −0.1149 | +0.0126 |
| B136 | 20 | 0.7388 | −0.0683 | −0.0880 | +0.0197 | −0.0821 | +0.0137 |
| B136 | 30 | 0.7343 | −0.0533 | −0.0801 | +0.0268 | −0.0727 | +0.0194 |
| B136 | 40 | 0.7279 | −0.0218 | −0.0450 | +0.0232 | −0.0366 | +0.0148 |
| SMALL439 | 3 | 0.7479 | −0.1839 | −0.1793 | −0.0045 | −0.1818 | −0.0020 |
| SMALL439 | 5 | 0.7473 | −0.0186 | −0.0124 | −0.0061 | −0.0152 | −0.0033 |
| SMALL439 | 10 | 0.7464 | +0.1421 | +0.1412 | +0.0009 | +0.1416 | +0.0005 |
| SMALL439 | 15 | 0.7457 | +0.1615 | +0.1491 | +0.0123 | +0.1519 | +0.0095 |
| SMALL439 | 20 | 0.7451 | +0.1271 | +0.1106 | +0.0165 | +0.1142 | +0.0129 |
| SMALL439 | 30 | 0.7435 | +0.0773 | +0.0634 | +0.0139 | +0.0658 | +0.0116 |
| SMALL439 | 40 | 0.7407 | +0.0809 | +0.0743 | +0.0066 | +0.0743 | +0.0066 |

**504 replicates on the FULL panel:** U56 n=20 is +0.0462 = SEL **+0.0045** + EXP **+0.0417**
against 504's 1,000-draw medians of +0.0587 = −0.0007 + **+0.0594**.

**The exposure leg is a de-grossing statistic, and de-grossing is a panel-width statistic.** U56
has mean 37.5 eligible names, so a fixed-weight top-n book cannot fill its book as n rises:
realised gross falls **0.7363 → 0.6475** from n=3 to n=40 and the exposure leg rises
**−0.0333 → +0.0827**. On B136 (91.5 eligible) and SMALL439 (142.1) the book always fills:
realised gross never drops below 0.7279 / 0.7407 and the exposure leg never exceeds **+0.0268**.
\|EXP\| > \|SEL\| in **5 of 21 cells under both matching rules, and all five are U56**.

Sign survival of the 9 positive premia: **6/9 (MR-EWMG), 8/9 (MR-CANDRG)**. The rules disagree on
U56 n=30 and n=40 (exposure carries 122% and 112% of the premium under EWMG, 91% and 98% under
CANDRG) — publishing one matching rule alone reproduces the error the census is about.
*Appendix (labelled, not a tuned axis):* 0 bps 11/21 positive, 8 / 11 survive; 25 bps 8/21
positive, 5 / 8 survive; the median exposure leg is cost-inert (+0.0143 / +0.0133).

## (3) PART D — re-pricing the committed record

Exposure slope (Sharpe per unit gross deficit, through the origin, 10 bps): **U56 +0.8355
(R² 0.778), B136 +1.1120 (0.534), SMALL439 +1.3399 (0.489)** — but every panel's **per-cell slope
bracket straddles zero** (U56 [−2.44, +3.39]), which is itself the finding: a fitted exposure
correction is a point estimate with no robust sign.

| population | rows | survives at the PUBLISHED (nominal) gross | survives once REALISED de-grossing is priced | robust to the slope bracket |
|---|---|---|---|---|
| MATCHED | 3,386 | 3,386 (100.0%) | **3,308 (97.7%)** | 3,011 (88.9%) |
| UNMATCHED | 6,838 | 4,046 (59.2%) | **4,089 (59.8%)** | **65 (1.0%)** |
| ALL re-priceable | 10,224 | 7,432 (72.7%) | **7,397 (72.3%)** | 3,076 (30.1%) |

Of the 1,271 **positive** UNMATCHED premia, **only 673 (53.0%) stay positive** — the record's
"beats EW-all" sentence is a coin flip on the population that was never gross-matched. And
"MATCHED" in the record means **nominal**: the fresh grid shows a book at nominal 0.75 actually
runs 0.6475–0.7479, a realised deficit of 0.0043 (SMALL439) to 0.0211 (U56, median over n) that
the nominal column cannot see; pricing it flips **78 of 3,386** nominal-matched rows and **12.3%
of their positives**. The FORM A / FORM A+B claim-set readings do not separate here, because
every FORM B file publishes no gross at all.

## (4) Rule 8 walk-forward (n picked on 2009–2016 IS Sharpe, 2017–2026 read once)

| panel | CAND pick | OOS CAGR / Sharpe / MaxDD | SPY OOS | RULES v2 OOS | OOS PREMIUM = SEL + EXP |
|---|---|---|---|---|---|
| U56 | n=3 | 24.17% / **1.069** / −25.81% | 15.24% / 0.872 / −33.72% | 9.45% / **1.275** / −12.05% | −0.0358 = +0.0046 − 0.0403 |
| B136 | n=30 | 11.54% / 0.903 / −20.30% | 15.45% / 0.882 / −33.72% | 7.98% / 1.119 / −12.24% | −0.1159 = −0.1296 + 0.0137 |
| SMALL439 | n=15 | 8.37% / 0.528 / −27.70% | 15.45% / 0.882 / −33.72% | 3.85% / 0.568 / −14.68% | +0.2379 = +0.2206 + 0.0173 |

**Out of sample the ranked book beats its own matched control on 1 of 3 panels** (SMALL439, the
panel with the worst absolute Sharpes), ties on U56 (+0.0046) and loses on B136 (−0.1296). No
pick beats RULES v2's OOS Sharpe on any panel, and every CAND pick draws down 1.7–2.1× the live
book out of sample. On U56 the gross-matched control `EWmg` (OOS 1.161) beats the ranked pick (1.069).

## (5) KEEP paths

**4a 0 / 66 book-cells at 10 bps. 4b 15 / 66. BOTH 0 / 66.** The 4b passers are
U56 CAND15/20/30 and CANDrg15/20/30/40, B136 EWall, EWmg5/10/15/20/30 and CAND40/CANDrg40 — i.e.
on B136 the **un-ranked** control passes 4b where the ranked book does not, and on U56 the
standing 2026-09-04 incumbent (CAND20) re-passes with a selection leg of **+0.0045, 9.7% of its
own premium**. Rule 8's pick on U56 (n=3) fails 4b, so per PROTOCOL rule 8 nothing here is a KEEP
— it would be PARK at best. **No memo, no book promoted, no RULES/PROTOCOL edit applied.**

## Proposed for Sunday review (wording only, not applied)

Any published premium against an EW-all comparand should carry **(i)** the realised mean gross of
both books, not the nominal dial, and **(ii)** the matching rule used, since MR-EWMG and MR-CANDRG
disagree on sign in 2 of 9 positive cells here. A premium quoted against a control at a different
gross should be labelled an EXPOSURE-INCLUSIVE premium.

## Stated limitations

Coverage is binding: 28.2% of committed premium rows cannot be re-priced at all, 95.8% of the
re-priceable ones carry an unresolvable panel label and take a pooled slope, and the slope
brackets straddle zero, so only the point-estimate reading stands (the 1.0% bracket survival on
UNMATCHED rows is the honest robust number). The re-price is a **model** — a fitted exposure
slope applied to a published gross deficit — not a re-run of each committed book; re-running
14,240 committed books was not attempted and is not claimed. **SURVIVORSHIP (PROTOCOL 9):** B136
and SMALL439 are today's constituents only, so all levels on them are biased up; every leg here
is a within-panel difference over the same names and days, but the 4b pass counts are levels
against SPY and are not protected.
