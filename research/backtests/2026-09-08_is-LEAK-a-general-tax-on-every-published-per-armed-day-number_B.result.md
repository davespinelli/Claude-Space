# idea 248 — is LEAK a general tax on every published per-armed-day number? (lane B, 2026-09-08)

**VERDICT: SPLIT. The tax is REAL and systematic (LEAK < 0 in 515/563 live cells, p 7.9e-100)
but NOT dominant (median per-cell |LEAK| share 26.9%; verdicts flip in 21.3%). The queue's
"52% LEAK vs 13% CONC" is reproduced EXACTLY (53.9% / 14.2% live, 52.2% / 13.4% on the record's
own 432 rows) and shown to be a RATIO OF MEDIANS: per cell the median shares are CONC 50.7% /
ACT 17.2% / LEAK 26.9%, so the statistic's named mechanism is the LARGEST term, not the
smallest. And the census answers "every published claim" with a number: the record contains
1,026 explicit per-armed rows in 2 files, both outputs of ONE parent script. No KEEP.**

## PART A — the census (2,044 committed CSVs, 1,684,512 published rows)
* **EXPLICIT per-armed normalisation: 2 files, 1,026 rows** — idea 246's `.decomp.csv` (432)
  and `.grid.csv` (594). Both are outputs of the same parent script. `.decomp.csv` carries all
  five split ingredients on its own; `.grid.csv` does not (no `d_on`/`d_off`) but its sibling
  `.mechanism.csv` does, so **1,026 of 1,026 explicit rows are restatable from the commit**.
* **LATENT exposure: 25 files, 26,928 rows** publish an armed/active fraction beside a delta
  but none of the split. That is an **upper bound**, not a count: not every such file quotes a
  per-armed number. No verdict is asserted over it.
* **Prose: 7 lines** (3 in idea 246's memo, 2 LEADERBOARD rows, 2 QUEUE lines) — all trace to
  idea 246. **The per-armed-day statistic is one script's habit, not a record-wide practice**,
  which is the single most useful thing this census establishes.

## PART B — the restatement (record 432 rows + a fresh 891-run corpus, 648 decomposed cells)
Identity `total = CONC + ACT + LEAK` exact on both (max residual 6.8e-14 record, 1.4e-14 live).

| statistic | record (432) | live (648) |
|---|---|---|
| LEAK median, pp/yr | **-1.4251** (neg 344/376, p 3.6e-67) | **-1.3791** (neg 515/563, p 7.9e-100) |
| median &#124;LEAK&#124; vs median (&#124;CONC&#124;+&#124;ACT&#124;) | 1.43 vs 3.17 | 1.38 vs 3.05 |
| ratio-of-medians LEAK / CONC share | 52.2% / 13.4% | 53.9% / 14.2% |
| **median per-cell share** CONC / ACT / LEAK | **50.7% / 16.7% / 27.2%** | **50.7% / 17.2% / 26.9%** |
| verdicts flipping when LEAK removed | 93/432 (21.5%) | 138/648 (21.3%) |
| verdicts flipping UNNORMALISED | 334/432 (77.3%) | 502/648 (77.5%) |
| LEAK-dominated (&#124;total-LEAK&#124; < 0.5&#124;total&#124;) | 124/432 (28.7%) | 180/648 (27.8%) |

* **H1 PARTIAL.** (a) systematic sign MET — 91.5% negative, p 7.9e-100. (b) dominance NOT MET —
  median |LEAK| 1.379 < median (|CONC|+|ACT|) 3.047.
* **H2.** Pooled median total **-2.5604 -> -0.7684** pp/yr on LEAK removal: the **pooled sign
  SURVIVES** (unlike idea 471's gross restatement) and the sign test stays decisive (425/612,
  p 2.9e-22). Unnormalised it becomes **+0.8338** — the sign inverts, as idea 246 reported.
* **The tax is regime-specific, and (1-f)/f is why.** flips: hivol80 8/216, spy200 50/216,
  **breadth20 80/216 (37%)**; median (1-f)/f = 4.86 / 8.21 / **10.56**. The rarer the regime,
  the more the divisor magnifies the disarmed-day residue.
* **H4 — the named mechanism survives.** sign(CONC) == sign(total) in 452/648 (69.8%), and CONC
  is the median-largest term. Idea 246's "13%" understated it by construction.
* **B4 — LEAK is a HOLDINGS artefact, not a switching bill.** median |LEAK| 1.2713 @0bps ->
  1.3642 @10 -> 1.5286 @25: only **6.8% / 16.8%** of it is cost. It is position carry-over from
  the last armed rebalance, which no cost assumption removes.

## KEEP paths (all 891 rows) and RULE 8
* **4a vs the LIVE RULES v2 book: 0/891.** (vs the older v1 book: 169/648 conditional, 68/216
  always, 5/27 control — the v1/v2 gap alone flips 4a for 237 rows, so quote which book.)
* **4b: 139/648 conditional, 18/216 always, 0/27 control**; 87 conditional passes whose own
  always-on sibling AND control both fail. Best @10bps u56/TOP20/band3-dg/hivol80 **15.08% /
  1.179 / -19.76%**, halves 1.285/1.099, OOS 1.166 — but its realised gross is 0.731 vs the
  control's 0.750, exactly the confound idea 471 restated away, and its MaxDD sits 0.5 pp
  inside the cap. **No new KEEP candidate; nothing here is proposed for RULES.md.**
* **RULE 8** (params picked on 2009-2016 IS, read once on 2017-2026), median over 27 cells:
  published pick OOS **CAGR 11.20% / Sharpe 0.8135 / MaxDD -18.85%**, regret vs do-nothing
  **-0.0034** (beats it in only **9/27**); LEAK-purged pick 10.54% / 0.8287 / -19.29%, regret
  -0.0057 (13/27); IS-Sharpe 11.12% / 0.7957 / -21.44%, regret 0.0000 (12/27). Live RULES v2
  OOS **Sharpe 1.1185, CAGR 7.98%, MaxDD -12.24%**; SPY OOS **0.8820, 15.45%, -33.72%**.
  **Purging LEAK changes the chosen arm in 22 of 27 cells and buys nothing** — both selectors
  lose to doing nothing more often than they beat it.

## What this changes
1. Quote the per-armed-day statistic only with its split, as idea 246 already recommended — but
   quote **per-cell shares**, not a ratio of medians: the ratio form inflated LEAK 2x and
   deflated CONC 3.6x, and both distortions are reproduced here from the record's own file.
2. The record's exposure is bounded and small (1,026 rows, one script). No published verdict
   outside idea 246 needs restating on this account.
3. Survivorship: all three panels are current-constituent lists; the paired splits are robust
   to it, the KEEP-path and rule-8 LEVELS are upper bounds.
