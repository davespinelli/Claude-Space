# Idea 1551 (lane C, 2026-09-19) — is the SLEEVE CREDIT a CLOSED-FORM CORRECTION?

**ANSWERED, BOTH WAYS. YES the axis is closed form — exactly, and not approximately. NO the
committed form is not that closed form: `sbar x CAGR_sleeve` under-predicts the credit at 45 of
45 cells, missing 6.5% of it on SHY, 17.1% on IEF and 43.7% (up to 60.2%) on TLT, because it
omits the term a fixed-weight mix must carry. KILL for the dial (idea 1358's rule-8 verdict
reproduces on a wider gross ladder). METHOD KEEP for the identity.**

Script `research/backtests/2026-09-19_is-the-SLEEVE-CREDIT-a-CLOSED-FORM-CORRECTION_C.py`.
60 cells (SLEEVE {CASH, SHY, IEF, TLT} x GROSS {0.40, 0.50, 0.60, 0.75, 0.90} x PANEL {U56,
B136, SMALL}), all published in `.grid.csv`; 45 closed-form comparisons in `.closedform.csv`;
60 reconstruction residuals in `.recon.csv`; 12 rule-8 rows in `.walkforward.csv`; 23 gates in
`.gates.csv`; full console in `.log.txt`. Book frozen at idea 1358's incumbent (N=15, H=126,
MAXVOL 0.60, MA gate, weekly, t+1, 10 bps on every leg including the sleeve). No fitted
parameter anywhere in the run.

## 1. The five forms, scored on the measured credit (sleeve cell minus CASH cell, same gross)

| form | what it is | MAE pp/yr | MAX pp/yr | MEAN pp/yr | sign |
|---|---|---|---|---|---|
| F_A | `(1-g) * CAGR_s` — the memo's "scales with (1-gross)" | 0.1674 | 0.4317 | −0.1674 | under-predicts 45/45 |
| F_B | `sbar * CAGR_s` — **the queue's literal wording** | 0.1678 | 0.4322 | −0.1678 | under-predicts 45/45 |
| F_C | `(1+CAGR_cash) * sbar * CAGR_s − d(drag)` | 0.1356 | 0.4079 | −0.1356 | under-predicts 45/45 |
| F_E | F_C in log space **+ `g(1-g)(var_s/2 − cov(core,sleeve))`** | **0.0306** | 0.0923 | +0.0306 | over-predicts |
| F_D | the two-asset **MIX IDENTITY** | **0.0000** | **0.0000** | +0.0000 | exact |

OOS (2017–2026) is the same story: F_A 0.0808, F_B 0.0810, F_C 0.0896 pp/yr MAE, all one-signed.

**F_A and F_B are the same form.** `sbar`, the realised mean residual weight, equals the nominal
`(1-g)` to within **0.00054** across all 45 sleeve cells (gate G5). The queue's refinement of the
memo's wording buys 0.0004 pp/yr. Whatever is wrong with one is wrong with the other.

## 2. What the scalar forms omit, identified not guessed

A book held at fixed weights `(g, 1-g)` does not earn the weighted average of its legs' CAGRs; it
earns the weighted average of their **log growth rates**, which against a cash book whose residual
has zero variance adds `g(1-g)(var_s/2 − cov(core, sleeve))`. Regressing F_C's shortfall on that
term over the 45 cells gives **corr² = 0.9980**. Adding it (F_E) collapses the error from 0.1356
to 0.0306 pp/yr. The shortfall tracks sleeve volatility exactly as that term says it must:

| sleeve | sleeve vol | F_B shortfall pp/yr | share of the credit missed |
|---|---|---|---|
| SHY | 1.36% | 0.0302 | 6.5% (max 12.1%) |
| IEF | 6.67% | 0.1315 | 17.1% (max 25.9%) |
| TLT | 15.02% | 0.3418 | 43.7% (max 60.2%) |

So the memo's form is *accidentally* adequate for the sleeve the memo actually recommends (SHY,
0.030 pp/yr of error) and materially wrong for any sleeve with duration. It is not a closed form;
it is a low-volatility limit of one.

## 3. The exact closed form: the (SLEEVE, GROSS) book IS a two-asset mix

F_D reconstructs each cell as the weekly-rebalanced mix of (i) the CORE book at gross 1.00 and
(ii) the sleeve, at weights `(g, 1-g)`, charging 10 bps on the mix's own turnover vector. The
reconstruction runner sees no price matrix, no score, no eligibility and no min-hold state — only
a per-window target vector, a per-window drifted proportion vector and the sleeve's return series.

- **G3: max |daily net return, F_D − direct| over ALL 60 cells = 1.110e-16.** CAGR, Sharpe and
  MaxDD all reproduce to the same precision.
- **G4: the CASH cells reproduce identically (1.110e-16)** — the degenerate sleeve-is-a-0%-asset case.
- One asymmetry had to be carried or the identity fails, and it is the incumbent's convention, not
  a free choice: a 0% cash line is not traded and pays no turnover, a bond-ETF sleeve is and does.
  Omitting it broke the identity by exactly 6.0e-04 of daily return on the opening rebalance.

**Consequence: the axis is retired.** Any (sleeve, gross) cell is obtainable from one core book
plus the sleeve's price series, by arithmetic. Pricing the 20-cell ladder on a panel costs one
book, not twenty.

## 4. Capital arm — both KEEP paths at every one of the 60 cells

Comparands: SPY (U56/B136 full 15.12%/0.884/−33.72%; 4b bars DD −20.23%, CAGR floor 10.59%),
live RULES v2 (U56 8.62%/1.2011/−12.05%), frozen (CASH, 0.60) incumbent.

- **G1 cross-script replay**: the (CASH, 0.60) cell reproduces ideas 1296/1346/1358's committed
  anchor to **4.4e-16 / 1.1e-16 / 8.3e-17** on U56 / B136 / SMALL. U56 SHY@0.60 also reproduces
  idea 1358's memo cell exactly (14.24% / 1.2182 / −16.00% full; 15.91% / 1.2500 / −16.00% OOS).
- **4b: 21 of 60 cells FULL, 18 FULL and OOS** (SHY 6, IEF 6, TLT 3, CASH 3). Every one is an
  already-known book re-priced, not a new one. Both tails of the gross ladder fail: g = 0.40 fails
  the CAGR floor at 12 of 12, g = 0.90 fails the DD cap at 12 of 12.
- **4a: 2 of 60 FULL, 0 FULL and OOS.** Both are SHY at g = 0.40 (U56 9.90%/1.2735/−10.56%,
  halves 1.335/1.243 vs live 1.228/1.181; B136 9.77%/1.1572/−10.26%). They re-confirm idea 1498's
  standing 4a SHY finding on a second frame, and **both fail the OOS re-read** — PARK under rule 8,
  not KEEP. Nothing here is a KEEP candidate and nothing is proposed for enactment.
- Turnover cost of the sleeve is real and netted throughout: U56 g=0.60 turnover 2.46 → 2.71 (SHY)
  / 2.74 (IEF) / 2.83 (TLT) per year, drag 24.6 → 27.1 / 27.4 / 28.3 bp/yr.

## 5. Rule 8 — three choosers, 2017–2026 read once, against doing nothing

| chooser | what it needs | U56 pick | B136 pick | SMALL pick | mean OOS dSharpe |
|---|---|---|---|---|---|
| C_GRID | all 60 direct books | IEF 0.40 | IEF 0.40 | TLT 0.40 | **−0.0439** |
| C_RECON | 3 core books + 3 sleeve series (F_D) | IEF 0.40 | IEF 0.40 | TLT 0.40 | **−0.0439** |
| C_CHEAP | CASH ladder + F_B only | TLT 0.40 | TLT 0.40 | TLT 0.40 | **−0.2514** |

- **C_RECON reproduces C_GRID's pick on 3 of 3 panels** at 1/20th the compute. That is the
  retirement claim, tested operationally rather than asserted.
- **As a tuned dial the axis is a KILL, reproducing idea 1358 on a wider ladder**: the IS chooser
  never finds SHY, and SHY is the ex-post best OOS cell on **3 of 3** panels (U56 SHY@0.40 OOS
  11.14%/1.3128/−10.56%, the only ex-post cell clearing 4b OOS).
- **C_CHEAP is the coda.** The term F_B omits is precisely a *penalty* on volatile sleeves, so a
  chooser built on F_B rates duration as free return and picks TLT on all three panels, for
  −0.2514 of OOS Sharpe. The committed form's error is not neutral; it points the wrong way.

## 6. How much does the error matter to the record?

Every scalar form's error is inside the cell's own paired circular-block bootstrap SE of dCAGR
(400 reps x 63-row blocks, seed 20260919) at **45 of 45** cells — mean SE 0.7492 pp/yr. Re-reading
the 4b CAGR leg with F_B's predicted CAGR instead of the measured one flips the leg at **1 of 45**
cells. So no committed verdict in the record moves because of this: the correct reading is that
the record cannot *resolve* the difference, not that the difference is zero. It is one-signed at
45 of 45 cells, which a sampling error would not be.

## 7. Caveats

(a) Survivorship (rule 9): U56/B136/SMALL are current-constituent lists; this run reads contrasts
(sleeve minus cash at the same gross) and residuals (measured minus predicted), both of which
difference the level bias away. SHY/IEF/TLT are survivorship-free.
(b) 2009–2026 contains the largest bond bull market on record plus 2022; that is why the sleeves'
own CAGRs (SHY 1.31%, IEF 1.94%, TLT 1.08%) are small and why F_A/F_B's absolute error looks
small — a higher-carry sleeve scales every error in section 1 linearly.
(c) The mix identity is a property of the *incumbent's runner*, including its convention that the
0% cash line pays no turnover. A runner that charged the cash line would need the other branch.
(d) F_C and F_E are handed the sleeve leg's realised drag for free; even so, F_C misses. F_D
needs nothing.
(e) B136's own SHY/IEF/TLT columns differ from `data/prices.csv`'s at 1e-4 daily (idea 353's
standing finding); the sleeve always comes from `data/prices.csv`, published and bounded as G7b.

**GATES 23/23** (G1 cross-script replay x3, G2 no leverage, G3/G4 the identity, G5 sbar vs
nominal, G6 rule 1, G7a/b/c the sleeve join, plus 14 published stamps).
