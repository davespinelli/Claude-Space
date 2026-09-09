# Idea 549 — is-every-published-CADENCE-verdict-really-a-c_sd-verdict (cloud, 2026-09-09)

**ANSWER: NO. H_CALENDAR_LABEL HOLDS — but not in the direction the queue assumed.**
On the record's own cross-cadence ladders, "c_sd ordered it" and "the calendar ordered it" are
**observationally equivalent** (c_sd is monotone in D<W<M<Q<A in 34/42 of my ladders, and
rho(c_sd,Sharpe) is *numerically identical* to rho(calendar,Sharpe) in the same 34/42), so no
published cadence ladder can distinguish them. Where the two CAN be separated — within a fixed
cadence, across book-forms — c_sd does **not** order dSharpe (consistent sign in only 8/15
panel×cadence cells, mean rho −0.16). And the one thing c_sd does robustly say is **backwards**
for the record: the pooled slope is **negative**, so a pure c_sd rule predicts every ladder peaks
at **D**, while 929/1754 published ladders (53.0%) peak at **M** and **not one** peaks at A.
The c_sd rule reproduces **238/1754 = 13.6%** of published argmaxes — worse than random (29.6%)
and far worse than the modal-cadence null (53.1%). **KILL of the c_sd-relabelling reading.**

## Gates (all printed before any headline number)
| Gate | What | Result |
|---|---|---|
| G0.1 | local cadence-extended runner == `engine.backtest` at D/W/M/Q, 3 panels | **PASS**, worst \|dr\| **0.000e+00**, 0 mask-disagreement bars |
| G0.2 | idea 307's committed `.decomp.csv` c_sd reproduces on SMALL439, 30 cells (2 families × 5 cadences × 3 shared thetas) | **PASS**, worst \|d c_sd\| **5.9e-17** at 1e-9 |
| G0.3 | idea 290 identity `r_dg == c_t · r_rs` at 0 bps, 90 gate books | **PASS**, worst **2.4e-16** at 1e-12 |

## PART A — the census (machine scan, no prose read)
2,364 committed CSVs; 74 carry both a cadence and a Sharpe column; **1,754 clean cadence ladders
over 25 files** (k=3: 989, k=4: 739, k=5: 26; one row per cadence, every other design column held
fixed). Published argmax: **M 929 (53.0%), Q 502 (28.6%), W 171 (9.7%), D 152 (8.7%), A 0 (0.0%)**.
Monotone in calendar order 45.6%; mean Spearman(calendar, Sharpe) +0.321; median per-ladder
Sharpe span 0.083.

## PART B/C — the law, and what identifies it
Grid: 3 panels (U56 55 names, B136 135, SMALL439 439) × 14 book-forms (EWALL, BAND v2-form,
MA/QM at θ ∈ {+0.12, 0.00, −0.12} × DEGROSS/RESPREAD) × 5 cadences = **210 books**, gross 0.75,
10 bps, t+1.

- c_sd rises with cadence on every panel (U56 0.0558 D → 0.0820 A; SMALL439 0.0478 → 0.0762), i.e.
  idea 307's monotone ladder generalises — **which is exactly why it cannot be told apart from the
  calendar label**: `|rho(c_sd,Sharpe) − rho(cal,Sharpe)| = 0` in 34/42 ladders.
- Mean Sharpe by cadence peaks at **M** on all three panels (U56 1.052/1.118/**1.167**/1.094/1.096
  for D/W/M/Q/A), while c_sd's argmax is **A in 39/42** ladders. The two argmaxes coincide in
  **5/42**.
- Within-cadence (the only identifying variation): rho(c_sd, dSharpe) = **+0.10/+0.03/−0.20/−0.59/−0.71**
  on B136 and **+0.13/+0.24/−0.01/−0.67/−0.79** on U56 across D/W/M/Q/A — it **flips sign along the
  dial**, which is a cadence×c_sd interaction, not a law. Clause (1) **FAIL** (8/15, \|mean rho\| 0.16 < 0.30).
- Pooled `dSharpe ~ c_sd`: slope **−0.316 (t −3.36)**, R² 0.051; with cadence+panel FE
  **−0.327 (t −4.15)**, R² 0.369 vs 0.315 for FE alone (c_sd adds +0.054). Clause (2) **PASS** —
  c_sd is not *only* the calendar, but its sign points away from the record's verdicts.

## PART D — scoring the record
c_sd rule (negative slope ⇒ pick the lowest-c_sd cadence available) reproduces the published argmax
in **238/1754 (13.6%)** vs uniform 29.6% and modal-M 53.1% (−39.6 pp, −48 se). Clause (3) **FAIL**.
By width: k=3 12.7%, k=4 15.2%, k=5 0/26.

## Rule-8 walk-forward (IS 2010–2016 chooses, OOS 2017–2026 read once, 42 ladders)
| selector | mean OOS Sharpe | mean OOS CAGR | mean OOS MaxDD | mean regret | beats SPY | beats RULES v2 |
|---|---|---|---|---|---|---|
| IS-Sharpe | **0.9429** | 9.93% | −21.3% | **0.0412** | 66.7% | 0.0% |
| always-W | 0.9261 | 9.53% | −20.4% | 0.0581 | 64.3% | 2.4% |
| **c_sd rule** | **0.9037** | 9.81% | −22.0% | **0.0804** | 66.7% | 2.4% |

Choosing cadence by c_sd is the **worst** of the three selectors out of sample and carries the
highest regret against the ex-post best cadence. WF-C: the within-cadence c_sd ordering keeps its
IS sign OOS in 9/15 cells and reverses at D/W on two panels.

## Both KEEP paths (all 210 books)
**4a 1/210, 4b 12/210, BOTH 0/210** — 4a's single pass is the live BAND/DEGROSS-W book on U56
(which then fails 4b on CAGR); 10 of the 12 4b passes are U56, 2 are B136, **0 on SMALL439**.
Failing-clause counts: DD 133, CAGR 120, H2 79, H1 78, OOS 76. This reproduces the record's known
4b footprint (idea 404: 7/126, 6 of them u56) and adds nothing to it. SPY comparands: U56 CAGR
15.19%, Sharpe 0.887, MaxDD −33.7%, halves 0.959/0.829, OOS 0.879.

Best 4b passer: **U56 QM+0.00/RESPREAD monthly** — CAGR 14.35%, Sharpe 1.220, MaxDD −20.15%,
halves 1.322/1.136, OOS Sharpe 1.221, turnover 2.0×/yr. Its DD margin is **0.08 pp** (bar −20.23%),
i.e. inside the 1.13 pp of MaxDD that idea 299 showed comes from cadence alone → **PARK, not KEEP**
(memo: `.memo.md`).

**SURVIVORSHIP:** B136 and SMALL439 are current constituents only (no delistings); CAGR levels are
inflated and the 4a/4b columns inherit that bias whole. The headline is an arm-minus-arm ordering
statistic on the same names and days, which the bias very largely leaves alone.

Outputs: `.census.csv` (1,754 ladders) `.grid.csv` (210 books) `.within.csv` `.walkforward.csv`
`.leaderboard.txt` `.console.txt`.
