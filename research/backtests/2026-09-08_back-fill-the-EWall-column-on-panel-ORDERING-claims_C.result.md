# Idea 460 — back-fill the EW_ALL column on the record's PANEL ORDERING claims (lane C, 2026-09-08)

**Verdict: ANSWERED — SPLIT. No KEEP, no RULES change.** Two-panel orderings survive the
restatement (95.7%); the record's headline three-panel ordering **U56 > B136 > SMALL439 does
not** (70.8% of cells, **50.9% file-clustered** — about half the files that publish it lose
it). Worst of all in exactly QUEUE 460's target subset: three-panel cells from files that
publish **no** un-ranked control survive only **46.6%**.

## What was done
Every committed CSV (2,002 scanned) was read; 313 files publish a Sharpe for **≥2 mapped
panels at a MATCHED CELL** (all non-outcome columns held fixed), giving **119,451 ordering
cells** over 213 stems. Each cell's published values induce a RAW panel ordering; the
restatement re-quotes each panel as `published Sharpe − Sharpe(EW_ALL on that panel)`,
window-matched (FULL/IS/OOS/H1/H2), and asks whether the induced permutation is unchanged.
Two tuned parameters only — control **gross** {0.50, 0.75, 1.00} × **cadence** {W, M} — all
6 points reported at both 10 and 25 bps. 928 unmapped panel labels (21,826 rows) are listed
in `.unmapped.csv` and never guessed.

The back-filled column replicates idea 239-cloud exactly (g0.75/W/10bps FULL Sharpe: u56
**1.1240**, broad136 **1.1220**, small439 **0.6781**), independently constructed.

## The mechanism, stated before the numbers
An ordering is a *difference* of levels, so it is invariant to anything that shifts all
panels equally. The restatement subtracts a **different constant per panel**, so an ordering
flips exactly when the control's own panel gap rivals the published gap. The control gaps are
**u56 − broad136 = +0.0021** but **broad136 − small439 = +0.4438**. That predicts, and the
data confirm, that u56-vs-broad136 claims are essentially untouched while every claim
involving small439 is at risk.

## Numbers (g = 0.75, W, 10 bps; file-clustered beside pooled because one file can carry thousands of cells)

| subset | cells | files | pooled | file-clustered | file-blocked 95% CI (pooled) |
|---|---|---|---|---|---|
| ALL | 119,284 | 313 | **0.8800** | 0.7273 | [0.7532, 0.9337] |
| k = 2 panels | 81,990 | — | **0.9567** | — | — |
| k = 3 panels | 37,415 | 140 | **0.7122** | 0.4891 | — |
| headline `u56>broad136>small439` | 27,559 | 139 | **0.7078** | **0.5087** | — |
| files with no own control | 78,522 | 167 | 0.9123 | 0.7417 | [0.7118, 0.9608] |
| files with an own control | 40,762 | 146 | 0.8178 | 0.7110 | [0.6650, 0.8916] |

The no-control column reads *better* pooled and the same file-clustered (0.7417 vs 0.7110) —
that gap is file weighting, not a real difference. The real difference is at **k = 3**:
no-control **0.4662** (8,619 cells) vs has-control **0.7857** (28,842). The files QUEUE 460
names are the ones whose three-panel orderings do not survive.

Pairwise sign concordance (a weaker bar than the full permutation):

| pair | n | raw favours first | excess favours first | sign kept | control gap |
|---|---|---|---|---|---|
| u56 vs broad136 | 113,757 | 0.796 | 0.792 | **0.9564** | +0.0021 |
| broad136 vs small439 | 38,873 | **0.985** | **0.775** | 0.7902 | +0.4438 |
| u56 vs small439 | 41,743 | 0.994 | 0.873 | 0.8788 | +0.4459 |

**21 pp of the record's "broad beats small" statements reverse** once each panel is quoted
against its own un-ranked control. By window, survival is FULL 0.9294 / IS 0.8888 /
**OOS 0.8237** — the restatement bites hardest exactly where the record makes its OOS claims.
Two published orderings survive **0/460** and **0/125**: `u56>small439>broad136` and
`broad136>small439>u56`.

What the headline becomes when it breaks: `u56>small439>broad136` (3,962 cells),
`small439>u56>broad136` (2,684), `broad136>u56>small439` (1,239). **small439 moves up** —
its low control is doing the work in the raw ordering.

## Robustness, rule 8 and the KEEP paths
- **Convention (2 params, all 12 points):** pooled ALL spans **0.8565–0.8831** across
  gross × cadence × rung; headline spans 0.6387–0.7153. The answer is not a dial.
- **Rule 8 on the convention** (files < 2026-09-06 in sample, ≥ read once): IS picks
  g0.50/W (0.8641) → held-out **0.8856**; the six conventions span 0.8598–0.8856 out of
  sample. **The headline moves 2.2 pp out of sample and 2.6 pp across the whole grid.**
- **Rule 8, live** (arm chosen on 2009–2016 IS Sharpe per panel, 2017–2026 read once): the
  chooser picks **EW_ALL in 6/6** panel × rung cells. OOS vs do-nothing 0/6, vs RULES v2 3/6,
  vs SPY 4/6. u56 OOS 1.136 / 13.8% / −22.5%; broad136 1.102 / 13.9% / −25.4%; small439
  0.637 / 10.1% / −36.2%; SPY OOS **0.882 / 15.5% / −33.7%**; RULES v2 OOS 1.285 / 9.5% /
  −12.1%.
- **KEEP paths over the 36 live grid points: 4a 0/36, 4b 2/36** — u56 RANKED20 (12.7% /
  1.092 / −18.3%, OOS 1.168) and broad136 RANKED40 (11.9% / 1.003 / −19.1%, OOS 0.979).
  **Neither is rule-8 selectable** (IS Sharpe 0.993 and 1.034 vs EW_ALL's 1.110 and 1.146),
  and **both carry negative excess over their own control** (−0.032 and −0.119 full sample)
  — the exact pattern QUEUE 459 is about. **PARK, not KEEP.**
- **Live orderings** (the question asked directly, not archivally): 8/12 arm × window
  orderings are unchanged; the four that flip are all RANKED arms, and all flip by moving
  small439 up.
- **Gate:** the fast simulator reproduces `engine.backtest` on RULES v1 to max|Δ| ≤ 1.4e-17
  on all three panels.

## Honest limits
The back-fill prices the control at one pre-registered convention regardless of the published
row's own gross, cadence or cost rung; that is inherent to a back-fill and is why the
convention is swept and rule-8'd rather than asserted. Cells are concentrated by file, so
every headline is quoted file-clustered with a file-blocked bootstrap. Ties (≤178 cells at
any convention) are excluded from the denominator, not counted as survivals.
**SURVIVORSHIP:** small439 is current constituents of the sub-$2B screen
(`data/SMALL_PANEL_README.md`); broad136 is current constituents of `universe_broad.json`
(PROTOCOL 9). Every panel-level number here is relative, never achievable.
