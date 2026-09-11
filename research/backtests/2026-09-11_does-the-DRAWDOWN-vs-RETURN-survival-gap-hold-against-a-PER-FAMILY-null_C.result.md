# Idea 714 — does-the-DRAWDOWN-vs-RETURN-survival-gap-hold-against-a-PER-FAMILY-null

**lane C, 2026-09-11 — ANSWERED / SPLIT. No KEEP, no memo.**

Script: `2026-09-11_does-the-DRAWDOWN-vs-RETURN-survival-gap-hold-against-a-PER-FAMILY-null_C.py`
(712.6s). Outputs: `.claims.csv .permfamily.csv .bands.csv .claimleg.csv .walkforward.csv .console.txt`

## The question

Idea 540 measured `disp`'s logx survival at **5/28 = 17.9%** on the drawdown claims and
**47/63 = 74.6%** on the return claims, and read both against **one pooled** permutation band
`[56.8%, 82.3%]`. The per-family null was never measured, so the gap was directional only.
This run re-runs **idea 540's own permutation** — same seed (540), same within-stratum
construction at 21 strata, same rng consumption order — **partitioned by outcome family**, and
asks whether the drawdown shortfall clears its **own** band.

Nothing is re-backtested. The object is a within-stratum slope over idea 533's committed
`.arms.csv` (idea 295's MIX ladder: k=40, 21 q rungs × 8 draws = 168 panels, seed 20260909,
three books per panel, gross 0.75, weekly, 10 bps, next-day execution).

## Gates — all pass before a new number is read

| Gate | What | Result |
|---|---|---|
| G1 | idea 533's committed disp grid re-derives from its own `.arms.csv` | 360/360 rows, max \|db\| **4.649e-16** (bar 1e-9); KEEP counts **4a 0/504, 4b 41/504** as published |
| G2 | idea 540's committed 180-row claims table re-derives cell for cell | 180/180, max \|d\| **8.882e-16**, `is_claim` agree **180/180**, `survive_logx` agree **180/180** |
| G3 | idea 540's published DD/RET numbers re-derived, not believed | **DD 5/28 = 17.9%**, **RET 47/63 = 74.6%** — exact |
| G4 | the first 200 draws reproduce idea 540's committed `permutation.csv` | max \|d\| **0** on all four columns; pooled claim rate **35.9667%** (pub 35.97%), pooled logx band **[56.8%, 82.3%]** (pub identical) |

G4 is the point of the design: the per-family bands below are a **partition of exactly those
draws**, not a fresh roll of the dice.

## Tuned parameters (2, as the queue specifies) — all grid points in `.bands.csv`

1. **family scheme** ∈ {FAM2 (= idea 540's own DD/RET split), FAM3, FAM5 (per outcome)}
2. **draws** ∈ {50, 100, 200, 400} — 200 is idea 540's committed count and the reproduction gate; 400 is a strict superset at the same seed.

Residualisation, arm, stratum resolution, window and the |t| ≥ 1.96 bar are **inherited** from
ideas 295/533/540 and are reported axes, never tuned. All 3 schemes × 10 families × 3
residualisations × 4 draw rungs are published.

## ANSWER — the drawdown shortfall clears its own band; the return "survival" does not

At 400 draws, FAM2, logx (log(book vol) held, native outcome):

| family | cells | real claims | null claim rate | real survival | **own** null band | verdict |
|---|---|---|---|---|---|---|
| **DD** (MaxDD, DDnorm) | 72 | 28 (38.9%) | **29.2%** [19.4, 44.4] | **17.9%** | **[30.4%, 71.9%]** med 52.2% | **BELOW** |
| **RET** (Sharpe, CAGR, CAGRnorm) | 108 | 63 (58.3%) | **39.8%** [31.5, 50.0] | **74.6%** | **[63.2%, 92.3%]** med 78.6% | **INSIDE** |

Three things follow, and only the first is what the queue expected:

1. **YES — the drawdown shortfall is real.** 17.9% sits below its own band at **every** draw
   rung (50 / 100 / 200 / 400: bands `[30.7,75.2] [29.1,72.0] [29.1,72.5] [30.4,71.9]`), so it
   is not a resolution artefact of the null.
2. **NO — the return side is not a finding at all.** 74.6% sits **INSIDE** its own band. Idea
   540's 47/63 is precisely what a no-information `disp` produces in that family. The published
   gap is one real number and one null draw, not two real numbers.
3. **The null itself has a family effect, so the nominal counts were never comparable.** A
   permuted `disp` throws "claims" **1.37× more often** in the return family (39.8%) than the
   drawdown family (29.2%), and its surviving share is **26.4 pp higher** (78.6% vs 52.2%).

### Decomposing the published gap

```
RAW    gap   RET 74.6% − DD 17.9% = +56.7%    (idea 540's headline)
NULL   gap   RET 78.6% − DD 52.2% = +26.4%    (what a ZERO-SIGNAL disp produces)
EXCESS gap   RET −4.0% − DD −34.3% = +30.3%   (the part that is not the null)
```

**46.5% of the published gap is already in the null.** A draw-level null on the gap statistic
itself gives median **+26.3%**, band **[+1.9%, +50.1%]**, and a two-sided
**p(|null gap| ≥ 56.7%) = 0.0200** — significant at 5%, not at 1%, on a statistic the record
quotes without any band at all.

### FAM5 — the drawdown result is a RAW-MaxDD result, and vol-normalising kills it

| outcome | real claims | real logx survival | own null band | verdict |
|---|---|---|---|---|
| **MaxDD** | 19/36 | **10.5%** | [23.0%, 66.7%] med 45.5% | **BELOW** |
| **DDnorm** | 9/36 | 33.3% | [33.3%, 84.6%] med 62.0% | **INSIDE** (on the edge) |
| Sharpe | 20/36 | 70.0% | [61.5%, 92.9%] | INSIDE |
| CAGR | 23/36 | 82.6% | [61.5%, 93.3%] | INSIDE |
| CAGRnorm | 20/36 | 70.0% | [62.5%, 92.9%] | INSIDE |

The whole FAM2 drawdown result is carried by **raw MaxDD**; once the drawdown is divided by the
book's own vol (`DDnorm`), the separation from its own band is gone. That is the same direction
as idea 533's original claim — the drawdown channel *is* largely the vol channel — but it means
the surviving statistic is a level-of-vol statistic, not a shape statistic.

`loglog` reads **0.0% real and 0.0% null in every family** (bands `[0.0, 6.7]` or `[0.0, 0.0]`).
Idea 540's 0/28 is confirmed as **no power**, now per family rather than pooled.

### Record correction

Idea 540's "**14 of 28 REVERSING SIGN**" restates as: 14/28 flip sign at **any** |t|, but only
**2/28** flip sign **and stay significant**. The reversal headline is a sign count taken over
mostly insignificant coefficients.

## Rule 8 walk-forward (PROTOCOL 8) — both legs, both split by family

**CLAIM LEG** (fit on ≤2016-12-31 only, read once on 2017–2026):

| family | resid | IS claims | hold OOS |
|---|---|---|---|
| DD | none | 13 | **4 (30.8%)** |
| DD | logx | 8 | **0 (0.0%)** |
| RET | none | 11 | 11 (100.0%) |
| RET | logx | 22 | 18 (81.8%) |

The drawdown claims that survive the control in-sample hold out of sample **zero times**.

**BOOK LEG** (IS-only per-family `disp` selectors over the 168 panels, read once on OOS;
comparands on the same calendar RULES v2 OOS **+8.50%/1.0734/−12.53%**, SPY OOS
**+15.45%/0.8820/−33.72%**):

| selector | arms | OOS Sharpe range | beat anchor | beat v2 | beat SPY | 4a | 4b | median random-pick pct |
|---|---|---|---|---|---|---|---|---|
| SEL-S (argmax IS Sharpe) | 3 | 0.8262–0.9844 | 3/3 | 0 | 1 | 0 | **1** | 73.4% |
| SEL-DISP-**DD** (± and \|v) | 6 | **−0.0439–0.6788** | 1/6 | 0 | 0 | 0 | 0 | **1.8%** |
| SEL-DISP-**RET** (± and \|v) | 6 | 0.2852–0.8960 | 4/6 | 0 | 1 | 0 | 0 | 55.1% |

Over all 15 picks: **beat the do-nothing anchor 8, beat RULES v2 0, beat SPY 2, 4a 0/15,
4b 1/15** — and that single 4b pass is `SEL-S` on EWall (OOS +12.13%/0.9844/−19.33%), the
record's own Sharpe selector, **not a disp selector**. Corpus reference 4a 0/504, 4b 41/504.

The book leg agrees with the claim leg and sharpens it: selecting panels on `disp` in the
direction its own IS drawdown slope prescribes lands at the **1.8th percentile of random picks**
— worse than a coin flip, the same pathology idea 540 filed as SEL-DISP|v (and idea 715 is
open on). Selecting on the return slope lands at **55.1%**, i.e. random.

## Verdict

**ANSWERED / SPLIT. No KEEP (4a 0/15, 4b 1/15 and that pass is not a disp selector), no memo.**

The queue asked whether the drawdown shortfall clears its own band: **it does**, at every draw
rung. But re-running the null per family costs the record the other half of the sentence — the
**return family's 74.6% is inside its own band and is not evidence of anything**, and **46.5% of
the published +56.7 pp gap is a property of the null rather than of `disp`**. What is left is a
narrow, one-outcome statement: raw `MaxDD` direction claims on `disp` die under
log(book vol) held at a rate a permuted `disp` does not reach — and those same claims hold out
of sample 0 of 8 times and select books at the 1.8th percentile of random.

**SURVIVORSHIP** (idea 54, `data/SMALL_PANEL_README.md`): both ends of the q ladder are current
constituents of their screens, so every level inherited here is optimistic. The object under
test is a within-stratum slope under a control and a selector's OOS ranking, neither of which is
a level claim. No book here is a capital candidate.

## Follow-ups filed

- **716** — do the record's other pooled permutation bands hide a family effect of the same size?
- **717** — is `DDnorm`'s edge-of-band reading a normalisation artefact or a power loss (9 claims vs MaxDD's 19)?
- **718** — is "worse than random as a selector" a general property of controlled characteristics on this ladder (joins 715 from the drawdown side)?
