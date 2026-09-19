# Idea 1530 (lane cloud, 2026-09-19) — is SCALE vs COMPOSITION the RIGHT TAXONOMY for every LADDER the record owns?

**ANSWERED — NO. THE DICHOTOMY IS REFUTED ON ALL THREE PRE-REGISTERED BARS, AND HOLDINGS OVERLAP
DOES NOT EVEN ORDER THE BLEND GAPS. ONE CONSTRUCTIVE REPLACEMENT (a THIRD axis) AND ONE METHOD
FINDING (the record's naive blend charge UNDER-costs a real blend). KILL FOR CAPITAL. NO RULES
CHANGE PROPOSED.**

## What was run
8 ladders off the frozen 2026-09-04 KEEP-4b incumbent (N = 20, H = 126, gross 0.75, MAXVOL 0.60,
200d MA gate, weekly Fri-decide / Mon-trade, 10 bps, t+1), each moving exactly ONE dial:
`L_G` gross, `L_T` vol target, `L_S` trailing-equity stop (all three **pre-registered SCALE**);
`L_N` N, `L_H` min-hold, `L_C` cadence, `L_V` MAXVOL, `L_B` MA band (all five **pre-registered
COMPOSITION**). 34 rungs, 26 adjacent pairs, 3 blend weights per pair -> **112 cells per panel,
336 in all on U56 / B136 / SMALL, every one published** in `.grid.csv`. Two dials and no more:
blend weight lambda {0.25, 0.50, 0.75} and overlap statistic {OV_HOLD, OV_CAP}. All **10 gates
pass**; G1 replays the committed 2026-09-04 U56 anchor (15.80% / 1.1537 / -19.13% full;
17.32% / 1.1857 / -19.13% OOS) to **3.7e-05**, and G2 confirms that anchor is **bit-identical
(0.000e+00)** wherever it appears — it sits on all 8 ladders on all 3 panels.

## (1) 1509's mechanism replays exactly, and then stops generalising
G7: the lambda-blend of gross rungs 0.50 and 1.00 equals the single gross rung at the blended
exposure to **|dSharpe| 0.000e+00**. `L_G` measures mean D **-0.0001**, max |D| **0.0002** — the
blend IS the rung, exactly as 1509 found. `L_T` (vol target) behaves the same way: OV_HOLD 1.0000,
max |D| **0.0031**. Two SCALE ladders, confirmed.

## (2) BUT THE COMPOSITION SIDE IS EMPTY — every composition ladder ALSO measures as SCALE
`D = Sharpe(blend) - [lam*Sharpe(A) + (1-lam)*Sharpe(B)]`, the gap the taxonomy exists to predict.
Across the five pre-registered COMPOSITION ladders the gap never becomes material: max |D| is
**0.0074** (`L_B`), **0.0165** (`L_N`, `L_V`), **0.0249** (`L_C`), **0.0255** (`L_H`). **93% of the
69 non-stop pairs sit below |D| = 0.02.** The pre-registered label agrees on **26 of 78 pairs
(33.3%)**, and every one of those 26 is a SCALE label.

## (3) THE ONE LADDER THAT DOES OPEN A GAP WAS PRE-REGISTERED AS *SCALE*
`L_S`, the trailing-equity stop, has OV_HOLD **1.0000** — whenever both rungs are invested they
hold *identical* portfolios — yet mean D **+0.1247** and max D **+0.5421** (B136, 0.15 -> 0.10:
Sharpe -0.3802 and 0.8374 blend to **0.7707**). Overlap does not even ORDER the gaps: the pair with
the LOWEST holdings overlap in the whole run (SMALL `L_C` M -> Q, OV_HOLD **0.2915**) opens a gap of
**+0.0165**, thirty-three times smaller than a pair at overlap 1.0000.

## (4) ALL THREE PRE-REGISTERED SUFFICIENCY BARS FAIL, ON BOTH DIAL-2 STATISTICS
| fit (78 pairs, lam = 0.50) | R^2 | + ladder identity | dR^2 | worst ladder residual |
|---|---|---|---|---|
| D ~ 1 - OV_HOLD | **0.0154** | 0.3258 | **+0.3104** | `L_S` **t +4.30** |
| D ~ 1 - OV_CAP  | **0.1117** | 0.4443 | **+0.3326** | `L_S` **t +4.65** |

S1 (R^2 >= 0.80) FAIL, S2 (dR^2 < 0.05) FAIL, S3 (no ladder |t| > 2) FAIL — twice over.

## (5) RULE 8 ON THE TAXONOMY ITSELF: THE BINARY CUT IS WORSE THAN ASSUMING EVERY LADDER IS SCALE
theta chosen on warm-up..2016 blend gaps only, 2017-2026 read once. OV_HOLD: IS 93.6% (baseline
91.0%) -> **OOS 87.2% against an 89.7% majority-class baseline**. OV_CAP: IS 96.2% -> **OOS 82.1%**.
**Both cuts are BELOW the do-nothing baseline out of sample.** The taxonomy is not merely
insufficient; used as a classifier it destroys information.

## (6) THE CONSTRUCTIVE REPLACEMENT — POST-HOC, LABELLED AS SUCH: THE AXIS IS *EXPOSURE STATE*
OV_HOLD is blind by construction to days when exactly one rung is flat, and `L_S` is the only
ladder whose rungs differ in precisely that way (`flat_one` = **0.3190** vs **0.0000-0.0015**
everywhere else). Adding `flat_one` as a second regressor:
**R^2 0.0154 -> 0.6094**, ladder identity's contribution **+0.3104 -> +0.0053**, worst ladder
residual **t +4.30 -> -0.49**. The same holds for OV_CAP (0.1117 -> 0.6066, dR^2 +0.0079).
**Two numbers make ladder identity redundant; one number does not.** A ladder is not SCALE or
COMPOSITION — it differs in WHAT is held, in HOW MUCH, and in WHETHER the book is invested at all,
and only the third axis moves a blend in this record. Post-hoc, not pre-registered, and R^2 0.61 is
still short of the 0.80 sufficiency bar, so this is a hypothesis for a later run, not a finding.

## (7) METHOD FINDING — THE RECORD'S BLEND CHARGE UNDER-COSTS A REAL BLEND
G8's original premise (netted <= naive, by the triangle inequality) is **false** and the gate was
rewritten to the correct inequality (netted <= naive + split-restoration), which passes at **0 of
234 blends**. A daily constant-mix two-sleeve blend spends **0.57 bp/yr** restoring its capital
split, which the naive lambda-weighted charge omits entirely, so a real blend costs on average
**+0.21 bp/yr MORE** than the naive ruler says: **cross-sleeve netting saves less than restoration
costs.** Small, but it has the opposite sign to the one a blend ruler is usually assumed to have.

## (8) BOTH KEEP PATHS AT ALL 336 CELLS
**4a 0 of 336 full and 0 of 336 OOS** — another consecutive 4a zero (no ordinal claimed; lanes are
landing these concurrently). **4b 76 full / 73 OOS / 70 BOTH of 336**: U56 53 of 112 (all inherited
from the anchor, which passes both windows), B136 17 of 112 (the B136 anchor FAILS at -20.74%
against a -20.23% cap, so these are CREATED by de-gross devices — 10 of 17 on `L_T` alone),
**SMALL 0 of 112**. The binding leg is DRAWDOWN everywhere (U56 65/112, B136 35/112) exactly as the
standing CHANGELOG finding says.

**The one literal candidate, and why it is rejected.** U56 `L_T` = 0.15 (a 15% vol target on the
incumbent): full **15.01% / 1.1806 / -16.61%** (halves 1.2443 / 1.1304), OOS **15.99% / 1.2048 /
-16.61%**, 4b BOTH. It beats the frozen anchor on Sharpe and cuts 2.52 pp of drawdown — but by
**+0.0192 of Sharpe at t +0.39** (paired circular-block bootstrap, 400 reps x 63-row blocks, seed
20260919), i.e. **unresolved**, while giving up **0.79 pp/yr** of CAGR full-sample and **1.33
pp/yr** OOS. It is the twelfth consecutive de-gross-shaped near-miss and it is rejected for the
same reason as the others.

## (9) RULE 8 CAPITAL ARM
argmax-IS-Sharpe over all 112 cells per panel, 2017-2026 read once: U56 picks `L_V` = 0.30 and
**LOSES** (OOS 1.0163 vs the anchor's 1.1857, t -1.91); B136 picks `L_B` = 0.10 and wins (1.1502 vs
1.0180, t +1.31); SMALL picks `L_H` = 252 and wins (0.5935 vs 0.4398, t +0.95). Mean OOS Sharpe
**0.9200 vs 0.8812** for doing nothing — but **the one panel the chooser loses on is the only panel
where the anchor is a 4b passer**, no panel resolves at |t| > 2, and a 2-1 win record over three
panels is not evidence. **Doing nothing remains unbeaten where it matters.**

## Verdict
**KILL** the SCALE/COMPOSITION dichotomy as a taxonomy: it fails all three pre-registered
sufficiency bars on both overlap statistics, its pre-registered labels agree on 33.3% of pairs, and
as a rule-8 binary classifier it lands *below* the majority-class baseline out of sample.
**KILL for capital**: 4a 0 of 336, every 4b pass inherited or de-gross-created, the single literal
candidate unresolved at t +0.39 and CAGR-negative. **The useful residue is (6)** — the record needs
a THIRD axis, exposure state, and with it ladder identity carries no further information.
