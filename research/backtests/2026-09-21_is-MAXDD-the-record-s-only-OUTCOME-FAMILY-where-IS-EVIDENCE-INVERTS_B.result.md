# Idea 743 — is MAXDD the record's only outcome family where IS evidence INVERTS out of sample?

**Lane B, 2026-09-21.  ANSWERED / NO ON BOTH READINGS — and the premise is an artefact.**
10 bps, next-day execution, gross 0.75, 324 books, 162 cells x 2 splits, 20 forms, 2,304 ladder
rows.  Tuned: P1 OUTCOME SET (BASE8 / WIDE20 / WIDE20_RANK) x P2 CONSTANT (ZERO / GLOBAL /
FAMILY / PANEL).  All 24 grid points published in `.console.txt`.

## 1. 738's +0.5632 is recovered exactly — and it is a POOLED number over a near-degenerate column

Re-read off idea 738's **own committed `ladder.csv`** (no tape involved): MAXDD rho_POOLED
**+0.5638** against its published +0.5632 (G2 PASS).  Its two halves, never published, are
**+0.0262 (S2016)** and **+0.6867 (S2018)**.  The pooled figure is neither: it is what pooling
two splits whose OOS-MAE LEVELS differ (11.84 vs 8.90) does to a rank correlation.

An OLS prediction has mean equal to the IS mean of the outcome, for *every* form.  So when no
prediction crosses the realised OOS value, OOS MAE collapses to `|mean(y_is) - mean(y_oos)|` —
identical for every form.  On 738's S2016 MAXDD, **18 of 20 forms share ONE OOS MAE to 1e-6**
(tie mass 0.90) over a span of **0.98% of its own level**, against 89% of level for TURN.  The
ratio column the rho is taken over carries essentially no information; the sign is decided by
the two forms that happen to cross, and by the pooling.

## 2. Widened to 20 outcome families, BOUNDEDNESS runs the WRONG WAY

| support | cells | inverters | rate | median rho |
|---|---|---|---|---|
| BOUNDED | 64 | 4 | **6.3%** | -0.9043 |
| SEMI | 40 | 8 | 20.0% | -0.8100 |
| UNBOUNDED | 56 | 12 | **21.4%** | -0.5571 |

Bounded statistics invert **least**.  MAXDD is not the only inverter and is not even the
strongest: **KURT (SEMI) and CALMAR (UNBOUNDED) invert in 8 of 8 cells**, MAXDD in 4 of 8.
Seven of the eight bounded families never invert once.

**The decisive arm.**  A monotone cross-cell RANK transform makes every outcome bounded in
[0,1] while changing no ordering.  Over 160 matched cells it turns **12 non-inverters into
inverters and 12 inverters into non-inverters** — symmetric, i.e. no directional effect —
with Spearman(rho_raw, rho_rank) **+0.8882**.  Boundedness per se does nothing.

## 3. The carrier is whether the MAE column can separate the forms at all

Over the 40 (outcome x split) cells at the FAMILY constant:

| candidate carrier | Spearman with rho |
|---|---|
| −SPAN of the MAE column over its own level | **+0.7080** |
| CROSS EXTREMITY (predictions never crossing y_oos) | **+0.5152** |
| the outcome's own IS→OOS persistence (20 families) | **−0.7669** |
| BOUNDED support (the queue's hypothesis) | −0.2874 (wrong sign) |

The queue offered DRAWDOWN and BOUNDEDNESS.  The measurement says neither: rho goes positive
exactly where the MAE column is too narrow to rank the forms, and where the outcome's own
cross-cell ordering does not survive into the OOS window.

## 4. CAPITAL LEG (rule 8) — the inversion does not price

Every arm's (level, cadence) chosen by IS-ARGBEST on **2009–2016 alone**, 2017–2026 read ONCE.
12 arms x 8 IS choosers = 96 picks, all published.

| block | median OOS Sharpe | median OOS CAGR | median OOS MaxDD | beats SPY | 4b |
|---|---|---|---|---|---|
| BOUNDED choosers (n=48) | **1.0631** | 9.05% | **−22.05%** | 33/48 | 4/48 |
| UNBOUNDED choosers (n=48) | 0.9306 | 8.37% | −24.15% | 28/48 | 2/48 |

`IS_MAXDD` — the chooser 738's finding would condemn — returns the **shallowest** median OOS
drawdown of any chooser (**−17.54%**, SPY −33.72%) and the most 4b passes (2/12).  Picking on IS
MaxDD instead of IS Sharpe moves OOS MaxDD by a median of only −0.0101 (6 of 12 arms deeper).

## 5. KEEP paths

4a **3/324**, 4b **16/324** (both identical to 738's committed counts on its own grid — the
grid reproduces).  Among the 96 IS-only picks: 4a 4/96, **4b 6/96, all six on U56**.  The best,
`U56 / QUANTILE q=0.60 / RESPREAD / monthly`, reached independently by IS_CALMAR and IS_MAXDD,
reads OOS CAGR 15.56% / Sharpe 1.2409 / MaxDD −19.72% against SPY 15.26% / 0.8737 / −33.72%.
**It is NOT proposed as a KEEP:** its DD margin is 19.72 vs the 20.23 cap = **0.51 pp**, inside
the rebalance-offset spread idea 806 measured and idea 914 is open on, so it is a date, not a
property.  **No new KEEP; RULES.md unchanged.**

## Caveats

- **Vintage.** `data/` has been re-cached since 738 ran: the small panel now admits 665 names,
  not 439, and the tape is 10 days longer.  U56 reproduces 738's cells to 2.9e-03 on every IS
  column (G1 PASS); B136 drifts ≤0.61 MaxDD pp; SMALL439 is a different panel and is published
  as such.  Section 1 is tape-independent — it is read off 738's own committed file.
- **Survivorship.** All three panels are current constituent lists (idea 54): every CAGR and
  MaxDD LEVEL is inflated and the 4a/4b columns inherit that in full.  The headline (a sign of
  a within-outcome rank correlation across cells that all share the bias) is largely immune;
  the chooser leg's levels are not.
- The ladder is one corpus of 162 cells and 20 single-term forms.  "Inverts" means rho > 0 at
  the stated constant; no significance bar is claimed on a 16-point rank correlation.
