# Idea 294 — is-within-stratum-CORR-a-SECTOR-concentration-proxy (lane C, 2026-09-06)

**Verdict: ANSWERED / KILL of the sector-concentration explanation. `corr` is NOT a
re-labelled concentration statistic — it survives the control essentially untouched
(shrink 0.991–1.000). No new KEEP: 4a 0/500, 4b 21/500.**

## What was asked
Idea 284 held capitalisation fixed (60 seeded k=40 panels, q=0.5 = 20 small + 20 large) and
found mean pairwise correlation is the one characteristic that both survives the control and
walks forward (`S_CORR` OOS 1.0704/1.0130, the only selector to beat the anchor, SPY and
RULES v2 in both books) — but could not say **what** within-stratum corr is. Mean pairwise
correlation of a basket is mechanically lower when it is spread across many sectors, so the
obvious rival is sector concentration. If that were the story, the surviving half of idea
271's vocabulary would be one more proxy and the implementable form would be a sector cap.

## Construction
Idea 284's panels rebuilt from the same crc32 seed strings — **reproduction is exact**:
max |diff| = 0.00000000 on all of `corr_IS`, `breadth_IS`, `disp_IS`, `evol_IS`,
`CAND10/CAND20/EWall_OOS_Sharpe`, `CAND20_Sharpe`, `SPY_OOS_Sharpe` across all 100 panels.

Two independent sector taxonomies, because neither alone is clean:

* **ETFBETA** — each name assigned to whichever of the 9 sector SPDRs priced across the whole
  IS window (XLK XLF XLV XLE XLI XLY XLP XLU XLB) its daily returns correlate with most,
  measured on 2009–2016 only. XLRE (first close 2015-10-08) and XLC (2018-06-19) do not
  exist over the IS window, so this is the pre-2016 GICS sector set by construction.
  Covers a mean of **32.9 of 40** names per stratum panel (min 28; 143 of 539 names have
  <250 IS observations and are dropped as UNK). *Built from correlations, so it is biased
  toward the hypothesis under test.*
* **GICS** — hardcoded current-GICS sector for all 100 BSTK100 names, no return data of any
  kind. Covers exactly the **20 large** names of every panel. Non-circular check.
  Sanity: ETFBETA agrees with hardcoded GICS on **84/92 = 91.3%** of large-cap names whose
  GICS sector has an IS-window SPDR (chance ≈ 11.1%), mean IS correlation with the assigned
  SPDR 0.685 (large) / 0.407 (small). The labeller works.

H = Σ sᵢ² over sector shares (H = 0.1111 at even spread over 9 sectors, 1.0 at total
concentration). Tuned parameters: **n ∈ {10, 20}** and **label scheme ∈ {ETFBETA, GICS}** —
2, per PROTOCOL rule 4; EWall carried as an untuned third book. All grid points reported.

## Result 1 — corr and H are not the same statistic (inside the stratum)
Spearman(corr_IS, H), 60 panels: **−0.0556** (ETFBETA all 40, p 0.6753), **+0.0237**
(ETFBETA large 20, p 0.8604), **+0.0300** (GICS large 20, p 0.8219). If corr were
concentration this would be strongly positive and large. It is zero on all three schemes.

## Result 2 — H has no ordering power, and controlling for it changes nothing
| book | rho(corr, OOS) raw | rho(H, OOS) raw | rho(corr, OOS \| H) | shrink |
|---|---|---|---|---|
| CAND10 | −0.3648 (p 0.0046) | +0.0986 / −0.0043 | **−0.3617 / −0.3649** (p 0.0053/0.0051) | 0.9913 / 1.0001 |
| CAND20 | −0.4815 (p 0.0003) | +0.1301 / −0.0765 | **−0.4791 / −0.4809** (p 0.0003/0.0003) | 0.9950 / 0.9986 |
| EWall  | −0.4708 (p 0.0005) | +0.0735 / −0.1139 | **−0.4687 / −0.4707** (p 0.0004/0.0002) | 0.9955 / 0.9997 |

(second value in each cell = GICS scheme.) H's own p-values are 0.33–0.97 on every book and
scheme. OLS with z-scored regressors: adding H moves corr's coefficient from −0.0666 to
−0.0667 (CAND10) and −0.0694 to −0.0695 (CAND20); t on H is +0.60/+1.05/+0.40 (ETFBETA) and
+0.26/−0.39/−0.87 (GICS); ΔR² = **0.0010–0.0146**. Split-half by seed: the partial rho is
negative in **6/6** book×half cells (−0.221 to −0.608) and slightly *more* negative than the
raw rho in 5 of 6 — the control does not merely fail to explain corr, it marginally sharpens
it.

## Result 3 — rule 8 walk-forward (IS ≤ 2016 chooses one of 60 panels, 2017–2026 read once)
Anchor (do nothing, mean of 60) 0.6991 / 0.7255, seed sd 0.171/0.145; SPY OOS 0.8820,
RULES v2 OOS 0.8654, RULES v1 OOS 0.6303.

| selector | pick | OOS Sharpe | vs anchor | vs SPY | pctile |
|---|---|---|---|---|---|
| S_CORR (idea 284's winner, reproduced) | q0.500~s34 | **1.0704 / 1.0130** | +0.3713 / +0.2875 | +0.1884 / +0.1310 | 98.3 |
| **S_CORR\|H_ETF** (corr after removing H) | **q0.500~s34** | **1.0704 / 1.0130** | +0.3713 / +0.2875 | +0.1884 / +0.1310 | 98.3 |
| **S_CORR\|H_GICS** | **q0.500~s34** | **1.0704 / 1.0130** | +0.3713 / +0.2875 | +0.1884 / +0.1310 | 98.3 |
| S_HERF_ETF (lowest H) | q0.500~s25 | 0.6200 / 0.4758 | −0.0791 / −0.2498 | −0.262 / −0.406 | 33 / 7 |
| S_HERF_GICS | q0.500~s00 | 0.5974 / 0.6156 | −0.1017 / −0.1099 | −0.285 / −0.266 | 25 / 28 |
| S_H\|CORR_ETF | q0.500~s25 | 0.6200 / 0.4758 | −0.0791 / −0.2498 | — | 33 / 7 |
| S_EWALL / S_ISS | s38 / s06,s48 | 0.487–0.767 | −0.212/−0.113, +0.068/−0.123 | — | — |

Residualising corr on H **picks the identical panel under both schemes**. Both concentration
selectors lose to doing nothing, and their reverse extremes do too (S_HERF_ETF^rev −0.100 /
+0.006; S_HERF_GICS^rev +0.096 / +0.152) — sector concentration has no selector value in
either direction, so this is not a sign-flip story either.

## Result 4 — by-product: the POOLED corr↔H relation has the sign backwards, again
Pooled over the 100 panels Spearman(corr, H) = **−0.4883** (p 0.0000; −0.3344 ETFBETA-large,
−0.2730 GICS) — *more* concentrated panels have *lower* correlation. It is the cap line
doing it: small-cap panels are simultaneously more sector-concentrated (H 0.2629 vs 0.1728 at
q=0) and much less correlated (corr 0.1695 vs 0.3818). Any pooled reading of "concentration
raises correlation" across the cap line reads the sign backwards. This is the same Simpson
structure idea 284 found, now on a second pair of statistics.

## KEEP paths (all 500 cells reported)
**4a 0/500** — RULES v2 is beaten nowhere. **4b 21/500**: 16 at q=0.0, **5 of 300 stratum
cells**, **0 at q=1.0**. Stratum means (CAND10/CAND20/EWall) CAGR 9.79/9.36/9.13%, Sharpe
0.706/0.751/0.748, MaxDD −28.2/−27.0/−26.8%; SPY OOS 0.8820. S_CORR's pick still fails 4b on
the **drawdown cap alone** (−24.2% vs the −20.2% bar), exactly as in idea 284. The 5 stratum
passers have lower IS corr (0.244–0.250 vs 0.275) and **essentially the same H** (0.178–0.183
vs 0.176 ETFBETA; 0.198 vs 0.188 GICS) — the passing margin is the correlation, not the
spread.

## Reading
The record's one surviving panel characteristic is not a concentration statistic in disguise.
`corr` measures something the sector taxonomy does not see: it orders OOS Sharpe at fixed
capitalisation *and* at fixed sector spread, on a labeller good enough to recover 91.3% of
true GICS. That strengthens idea 284's PARK rather than converting it — there is still no
rule here, because the one panel `S_CORR` picks fails 4b on drawdown and 4a fails 500/500.

**SURVIVORSHIP:** SMALL439 and BSTK100 are current constituents of their screens; every panel
inherits the bias whole. It moves the level of every panel's return, and is common to the
stratum, so it does not manufacture a within-stratum ordering either way.

**LIMITS.** (1) Small caps have no sector field anywhere in the repo and the sandbox has no
internet, so the non-circular GICS scheme sees only the large half of each panel; the
all-40-name scheme is correlation-derived. Both give the same answer, which is the reason to
believe it. (2) H is a count-share Herfindahl, not weight- or risk-based. (3) One stratum
(q=0.5), one width (k=40) — idea 293 is the corresponding q/k robustness test.

Outputs: `.panels.csv` (100 panels × H under 3 schemes + all books), `.cells.csv` (500 cells),
`.fits.csv` (18 controlled fits), `.walkforward.csv` (34 selector rows), `.console.txt`.
