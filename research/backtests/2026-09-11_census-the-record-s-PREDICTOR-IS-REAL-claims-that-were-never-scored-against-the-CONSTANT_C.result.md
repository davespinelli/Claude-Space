# Idea 738 — census the record's "PREDICTOR IS REAL" claims that were never scored against the CONSTANT

**Lane C, 2026-09-11.** Script `2026-09-11_census-the-record-s-PREDICTOR-IS-REAL-claims-that-were-never-scored-against-the-CONSTANT_C.py`.
Artefacts: `.console.txt`, `.census.csv` (5,436 sites), `.cells.csv`, `.grid.csv`, `.ladder.csv` (384 form-cells), `.walkforward.csv`, `.summary.json`.

**ANSWERED / THE CENSUS CONFIRMS THE HABIT AND THE RE-SCORE KILLS THE ALARM. Both of idea 735's
headline lessons are RESID-SPECIFIC, and "its own family constant" — the object this idea was
told to score against — is not a well-defined comparand.**
No RULES change, no book promoted, no KEEP claimed, no memo, no PROTOCOL edit applied (rule 6);
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py untouched.

SELECTION: taken as the SECOND open idea per this lane's rule; 738 mentions no EDGAR / Form 4 /
8-K / options / live data.

## Gates (printed before any new fit was read)

**G1 PASS** — idea 538's exact 162 cells / 324 books rebuilt from source: max |d| **9.975e-17**
(c_sd_is), **1.110e-16** (c_bar_is), **4.449e-14 / 6.665e-14** (resid_is / resid_oos),
**8.882e-16 / 3.553e-15** (to_is / tors_is), **6.661e-16** (oSharpe_dg).
**G1b PASS** — idea 735's committed RESID ladder at S2016 reproduces to **1.3e-07 … 4.6e-07**
on all nine checked forms (CSD 0.177296, CT_RANGE 0.176908, FAMILY 0.193700, ZERO 0.264220,
GLOBAL 0.246024, DSH 0.249912, RESID_IS 0.208734, TORS 0.242709, DTO 0.240438) — residual is
the 6-dp rounding of the reference, not a rebuild difference. Idea 301's 1e-2 pp vintage
allowance was not needed.

## LEG A — the census (P1 CLAIM SET, all 5 values, all 3 window widths published)

Corpora: CHANGELOG 1,715,978 chars; LEADERBOARD 3,052,882; RESULTS 636 `.result.md`, 5,493,042;
MEMOS 22 files, 69,487. An **IS-EVIDENCE SITE** is a quoted t-statistic, R2, OLS slope/beta,
Spearman/rho or p-value. **5,436 sites; 2,974 (54.7%) QUANTIFIED** — a decimal sits beside the
token and it is not part of an artefact filename. The quantified set is the census population;
the raw set is published beside it so the filter can be checked.

| window | SCORED_vs_CONSTANT | OOS_ONLY | CONST_ONLY | IS_ONLY | IS_ONLY share | SCORED share |
|---|---|---|---|---|---|---|
| SENTENCE | **32** | 426 | 167 | **2,349** | 79.0% | **1.08%** |
| ±300 | 427 | 800 | 441 | 1,306 | 43.9% | 14.4% |
| ±600 | 857 | 913 | 485 | 719 | 24.2% | 28.8% |

Per corpus at the sentence window, IS_ONLY share: RESULTS **88.8%**, CHANGELOG 73.7%,
LEADERBOARD 71.4%. Per evidence kind: R2 **85.7%**, SLOPE 82.0%, T_STAT 77.8%, CORR 76.0%,
PVALUE 65.3%. **719 sites (24.2%) are IS_ONLY at EVERY window width.**

**The count 738 asked for, narrowed honestly.** An IS_ONLY site is only a *"predictor is real"*
claim when the statistic it quotes clears the bar; the record quotes plenty of nulls. Of 822
quantified t-sites with a recoverable value, **551 are affirmative (|t| ≥ 2) and 271 are nulls
(|t| < 2)**. The affirmative-and-IS_ONLY count is **415 (sentence) / 219 (±300) / 120 (±600)**.
That is the defensible answer to "count the committed claims resting on an IS t alone": on the
order of **10²**, not the 2,349 the raw IS_ONLY column suggests.

The 12-site audit sample in `.console.txt` shows the two residual failure modes directly: a
site can be a *null* reading (`t -1.24, win 0.490`; `Spearman(modal share, mean d) = -0.046`),
and a site is a text match, not an adjudicated claim.

## LEG B — the re-score (P2 CONSTANT, all 4 values; 8 outcome families × 20 forms × 2 splits)

Every form fitted on IS-window cell values ONLY and scored ONCE on the OOS truth. 320
non-constant form-cells; **227 (70.9%) are IS-significant at |t| ≥ 2**.

**Survival of the IS-significant, by constant (ALL 32 grid points in `.ladder.csv`):**

| P2 CONSTANT | OOS-beats-const | survival of IS-live | median ratio |
|---|---|---|---|
| ZERO | 293/320 | **98.7%** | 0.5089 |
| GLOBAL | 219/320 | **74.5%** | 0.9913 |
| FAMILY | 177/320 | **64.3%** | 0.9996 |
| PANEL | 203/320 | **63.9%** | 0.9961 |

**FINDING 1 — "its own family constant" is not a well-defined comparand.** The choice of
constant moves survival by **34.8 pp pooled** (98.7% ZERO → 63.9% PANEL) and by up to
**96.9 pp inside a single outcome**:
CAGR survives **100.0%** against ZERO and **3.1%** against PANEL; CSD survives **25.0%**
against FAMILY and **100.0%** against PANEL; RESID **13.3%** (FAMILY) vs **86.7%** (PANEL).
Which constant a verdict is quoted against decides it more often than which predictor is used.
This is the same mechanism ideas 731/737 measured on the 4a comparand, on a third corpus.

**FINDING 2 — idea 735's 87% OOS-death rate is a RESID fact, not a general one.** Pooled over
8 outcome families at the FAMILY constant: **81 of 227 IS-significant forms are OOS-dead
(35.7%); survival 64.3%** (63.3% excluding the 6 degenerate own-value forms). Per family:

| outcome | IS-sig | OOS-DEAD | survival |
|---|---|---|---|
| RESID | 30/40 | 26 (**87%**) | 13.3% |
| CSD | 16/40 | 12 (75%) | 25.0% |
| SHARPE | 24/40 | 10 (42%) | 58.3% |
| MAXDD | 29/40 | 11 (38%) | 62.1% |
| GAP | 29/40 | 7 (24%) | 75.9% |
| CAGR | 32/40 | 7 (22%) | 78.1% |
| PRED | 29/40 | 6 (21%) | 79.3% |
| TURN | 38/40 | 2 (**5%**) | 94.7% |

735 measured the single most hostile family in the set and generalised from it. RESID's 87%
reproduces exactly; nothing else comes near it.

**FINDING 3 — IS R2 DOES predict OOS survival, contradicting 735's stated lesson.** 735 read
Spearman(IS R2, OOS ratio) = −0.1483 / −0.3088 on RESID and called it "weak, and explicitly NOT
an inverse law". Across the 8 families the relation is strong and consistently signed
(negative = more IS evidence, better OOS score): pooled **−0.6001** (R2) / **−0.5999** (|t|);
**within-outcome median −0.4872 / −0.4871, negative in 7 of 8 families**.

| outcome | rho(R2, ratio) | rho(&#124;t&#124;, ratio) |
|---|---|---|
| TURN | **−0.9469** | −0.9466 |
| PRED | −0.7611 | −0.7610 |
| GAP | −0.7453 | −0.7453 |
| CSD | −0.6810 | −0.6809 |
| RESID | −0.2933 | −0.2934 |
| CAGR | −0.2875 | −0.2876 |
| SHARPE | −0.0524 | −0.0525 |
| MAXDD | **+0.5632** | +0.5621 |

RESID sits second-weakest; **MAXDD is the one family where the record's habit genuinely
inverts** (+0.56 — more in-sample evidence, *worse* out-of-sample), and it is a family the
record quotes constantly. That is the transportable warning, not "IS R2 is uninformative".

**The two legs multiplied.** 2,349 quantified IS_ONLY sites (sentence) × the measured 35.7%
death rate = **≈838 sites** whose evidence would not survive a constant-scoring at this study's
base rate; 466 at ±300, 257 at ±600. On the narrow affirmative-t reading it is ≈148 / 78 / 43.
This is an EXPECTED COUNT under one corpus's base rate, **not** an adjudication of those sites.

## RULE 8 (required) — WF-A, 2017+ read ONCE

12 arms, each (level, cadence) chosen on **IS Sharpe alone**. OOS CAGR **1.04%–24.02%**, OOS
Sharpe **0.5655–1.2168**, OOS MaxDD **−3.38% to −35.07%**, against RULES v2 OOS Sharpe
**1.2747 (U56) / 1.1185 (B136) / 0.5680 (SMALL439)** and SPY OOS **0.8721 / 0.8820** at
15.24% / 15.45% CAGR and −33.72%.
**Beats RULES v2 OOS Sharpe 7/12; beats SPY 8/12; 4a 0/12; 4b 1/12** — identical to idea 735.
The single 4b pass (`U56 QUANTILE x=0.50 M RESPREAD`, CAGR 15.47%, Sharpe 1.2359, MaxDD
−19.80%, halves 1.3518/1.1454, OOS Sharpe 1.2164) is **one of the 16 books idea 538 already
published**, reproduced exactly — not a new result, and it LOSES to RULES v2 on OOS Sharpe.

## BOTH KEEP PATHS on all 324 books

**4a 9/324** (same-panel RULES v2 comparand per PROTOCOL rule 3; all 9 on SMALL439 DEGROSS,
CAGRs 1.9%–3.8% against SPY's 14.13%) — **4b 16/324** (U56 8 RESPREAD + 5 DEGROSS, B136 1 + 2,
SMALL439 0). Every passer is a reproduction of 538/735. **No KEEP.** Promoting an
already-published book is a rule-6 Sunday-review decision, so none is claimed here.

## Caveats

- **Survivorship (idea 54):** three current-constituent panels, no delistings, so every CAGR
  LEVEL is inflated and the 4a/4b columns inherit it whole. Leg B's RESID/GAP/PRED outcomes are
  arm-minus-arm contrasts on one gate mask (same names, days, gross) so the bias very largely
  cancels there; it does **not** cancel out of CAGR, SHARPE, MAXDD, which are read as levels.
  SMALL439 drops the 44 tickers with max_1d_move ≥ 1.0 first.
- **The census classifies TEXT, not claims.** A site is a regex match; the OOS/constant markers
  are keyword sets; a sentence boundary is a heuristic split. The three window widths are the
  sensitivity analysis and all three are published, but no width makes the label an
  adjudication. The 12-site audit sample is the honest check and it shows the failure modes.
- The two splits share the same 162 cells and are **not** independent evidence.
- |t| ≥ 2 and MAE ≤ constant are conventional cut-points; the full ratio against all four
  constants is published for every form-cell in `.ladder.csv`, so any other cut can be read off.
- Leg B is ONE corpus (162 cells, 20 single-term forms). The base rate it measures is this
  corpus's; the record's other corpora are not sampled by it.

## Filed

- **743** — is MAXDD the record's only OUTCOME FAMILY where IS evidence INVERTS out of sample?
- **744** — restate every committed "beats the constant" verdict against all four constants.
- **745** — does the affirmative/null split (551 vs 271 t-sites) change any committed census count?
