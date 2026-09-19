# Idea 1562 — does the 1538 TWO-STATE GROSS survive a CAGR-MATCHED DE-GROSS TWIN and a SPY-LAG SWEEP?

**2026-09-19, lane cloud (idea 1 of 2).  VERDICT: KILL FOR CAPITAL — but the PREMISE IS REFUTED.**
Script `2026-09-19_two-state-gross-vs-cagr-matched-degross-twin_cloud.py`; 9/9 gates PASS, 44 s.

## What was asked

Idea 1538 left an incidental KEEP-4b candidate: the frozen incumbent book (U56, N = 20, H = 126,
band 0.00, MAXVOL 0.60, weekly) at gross **0.75 above SPY's own 200d MA and 0.5625 below**.  Eight
consecutive 2026-09-19 runs had found every drawdown-buying device beaten **at matched exposure**
by a plain constant de-gross, so the idea asked for this one to be priced the same way: against a
CAGR-matched constant twin, on a 0/10/25/50 bps cost ladder, over MA {100, 150, 200, 250} x
low-state gross {0.375, 0.5625, 0.675}, plus the SPY-lag sweep of its title.

**Pre-registered before the run:** `H_SCALAR` (twin wins, pooled mean dSharpe <= 0 on U56 at
10 bps) => dead on arrival, KILL.  `H_DEVICE` (pooled dSharpe > 0 AND every rule-8 cell beats its
own twin OOS) => the first macro gate in the record that is not a de-gross in costume.

## H_SCALAR DOES NOT HOLD — the nine-run streak breaks, and it breaks cleanly

At 10 bps the two-state gross beats its **own CAGR-matched constant de-gross twin** on Sharpe at
**12 of 12 U56 cells (mean +0.0238)** and **12 of 12 B136 cells (mean +0.0143)**, and is
**shallower** on MaxDD at 9 of 12 (U56) and **12 of 12** (B136).  This is the first device in the
record's de-gross races that is not strictly dominated by the scalar.  The mechanism is legible:
the twin has to spend a *lower constant* gross (g\* 0.696 against the candidate's realised mean
0.712 at the headline cell) to reach the same CAGR, so it pays the de-gross everywhere instead of
only where the tape is below its own trend.

## And it is worth almost nothing — four independent reasons, all published

1. **NOT ONE CELL IS RESOLVED.**  `|t| > 2` at **0 of 36** cells on the paired circular-block
   bootstrap (L = 63, 400 reps).  Best U56 t is +1.52, best OOS t +0.94.  The entire finding sits
   inside one SE of itself, which is exactly idea 1511's 2.93 pp complaint in Sharpe units.
2. **IT DIES ON THE COST LADDER.**  Pooled U56 dSharpe runs **+0.0295 / +0.0238 / +0.0152 /
   +0.0009** over 0/10/25/50 bps, and on B136 and SMALL the sign **flips negative at 50 bps**
   (-0.0051, -0.0173).  A device whose whole margin is smaller than one cost rung is a cost
   artefact until proven otherwise.
3. **IT DIES ON THE LAG.**  The signal read 5 trading days late instead of 1 collapses the U56
   pooled margin from +0.0238 to **+0.0001** (cand wins 8 of 12).  A macro gate whose value
   evaporates over four days is a timing coincidence, not a state variable.
4. **IT IS ALREADY GONE ON SMALL.**  Pooled +0.0006, cand wins **7 of 12** — a coin flip.

## Rule 8 (params on warm-up..2016-12-31 only; 2017-01-01..2026-09-18 read ONCE)

Both legal IS-only choosers (argmax IS Sharpe; argmax IS Sharpe margin over the twin) agree on
every panel: U56 -> MA 100 / gL 0.5625, B136 -> MA 200 / gL 0.375, SMALL -> MA 200 / gL 0.375.

| panel | OOS cand | OOS twin | OOS anchor (g = 0.75) | OOS LIVE RULES v2 | OOS SPY |
|---|---|---|---|---|---|
| U56 | 16.15% / **1.2247** / -16.54% | 16.05% / 1.1855 / -17.83% | 17.32% / 1.1857 / -19.13% | 9.46% / 1.2769 / -12.05% | 15.26% / 0.8738 / -33.72% |
| B136 | 14.29% / 1.0254 / -16.69% | 14.36% / 1.0171 / -18.54% | 16.19% / 1.0180 / -20.74% | 7.85% / 1.1019 / -12.24% | 15.26% / 0.8739 / -33.72% |
| SMALL | 5.33% / 0.4057 / -31.21% | 5.95% / **0.4393** / -31.96% | 6.70% / 0.4398 / -36.51% | 4.41% / 0.6473 / -12.48% | 15.26% / 0.8738 / -33.72% |

Pooled over the 6 (panel, chooser) cells: **cand 0.8853 vs twin 0.8806 vs anchor 0.8812 vs SPY
0.8738 vs LIVE 1.0087.**  The chosen cell beats its own twin out of sample at **4 of 6**, so
**H_DEVICE FAILS** on its second conjunct.  Against *doing nothing at all* the whole device is
worth **+0.0041 of pooled OOS Sharpe**.

## KEEP paths

**4a: 0 of 144 cells, full and OOS, on every panel and every cost rung.**  The live RULES v2 book
is a lower-return, much shallower object (U56 8.62% / 1.2011 / -12.05%) and nothing here goes near
its drawdown.

**4b: 48 of 144 full = 48 OOS = 48 BOTH at the three lower cost rungs — every one on U56 or B136,
0 of 48 on SMALL.**  But 4b does not discriminate here: at 10 bps the candidate passes 12 of 12,
**the twin passes 12 of 12 on U56 as well**, and so does the plain g = 0.75 anchor.  At 50 bps the
B136 column dies entirely (0 of 12 full) while U56 survives 12 of 12.  The rule-8-chosen U56 cell
(MA 100 / gL 0.5625) is a genuine, *reachable* 4b passer on FULL and OOS — memo written — but its
margin over a constant de-gross at the same CAGR is +0.0393 of OOS Sharpe at t +0.94.

## Gates

G0 sample 16.7 y.  **G1 cross-script replay of the committed 2026-09-04 U56 frozen anchor
(15.80% / 1.1537 / -19.13%; OOS 1.1857) to 3.7e-05.**  **G2 cross-script replay of idea 1538's own
candidate cell (14.92% / 1.1788 / -18.05% full, 16.48% / 1.2250 / -18.05% OOS) to 3.3e-04** — 1538's
number reproduces from an independently written engine.  G3 exactly two tuned parameters.
**G4 every CAGR-matched twin lands within 6.7e-07 of its target CAGR** (fine ladder + exact engine
run at g\*).  G5 no chooser reads a row on or after 2017-01-01.  G6 max gross 0.7769 <= 1.
G7 the cost ladder is an identity on one turnover path (0.00e+00).  G8 all 144 cells published.

## Survivorship (rule 9)

U56 and B136 are CURRENT-constituent lists and SMALL a CURRENT sub-$2B screen (665 names after the
protocol-mandated `max_1d_move >= 1.0` drop of 54 tickers) carried back to 2010, so every absolute
level is an **upper bound**.  The headline is a contrast between two books over the same names on
the same days differing only in the gross PATH, which the bias cannot manufacture; the 4a / 4b
pass counts are not immune.

## What the record should say instead

*A two-state gross keyed to SPY's own trend is the FIRST drawdown-buying device in the record that
is not beaten at matched CAGR by a plain constant de-gross — it wins 24 of 24 large-cap cells on
Sharpe and 21 of 24 on drawdown.  It is also the cheapest possible refutation of that streak: not
one of the 36 contrasts reaches |t| > 2, the margin is smaller than the 10-to-25 bps cost step, it
vanishes when the signal is read four days later, and it is worth +0.0041 of pooled OOS Sharpe
against doing nothing.  "The scalar always wins" should be restated as "no device yet measured has
beaten the scalar by more than its own SE" — a weaker claim the record can actually defend.*

No RULES change (rule 6).  RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py untouched.
