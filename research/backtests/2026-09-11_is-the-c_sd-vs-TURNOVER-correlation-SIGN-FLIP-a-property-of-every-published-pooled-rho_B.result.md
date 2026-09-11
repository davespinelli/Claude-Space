# Idea 733-SIGNFLIP - is the c_sd-vs-TURNOVER sign flip a property of every published pooled rho?  (lane B, 2026-09-11)

Corpus: every committed `research/backtests/*.grid.csv` (425 usable blocks of 441 on disk, 441560 quads) plus a FRESH rebuild of idea 538's 162 cells / 324 books (3 panels x 2 families x 9 levels x 3 cadences, gross 0.75, 10 bps, next-day execution).
Tuned (2): CLAIM SET ['QUEUE', 'CANON', 'ALL'] x STRATUM (every categorical column a block carries + controls ['ROWHALF', 'RANDOM2']). All grid points in `.census.csv`.
Fixed, not tuned: EPS_SIGN 0.1, NMIN 8, MAXCOLS 16, seed 733.

## Gates
- **G1 PASS** - idea 538's published premise reproduces off its committed `.cells.csv`: pooled Pearson +0.0444 / Spearman -0.1291, per family +0.5141 (MA-THRESH, n=81) / -0.3879 (QUANTILE, n=81).
- **G2 PASS** - the same four numbers rebuilt from prices: +0.0444 / -0.1291 / +0.5141 / -0.3879; max|d rho| 0.0000, max|d c_sd| 9.97e-17, max|d turn_yr| 8.88e-16.

## Bars
- **B1 FAIL** - CANCEL rate on the CANON claim set over real strata = 0.0362 (bar 0.25).
- **B2 FAIL** - vs the RANDOM2/ROWHALF control 0.0282: 1.28x (bar 2.0x).
- **B3 FAIL** - mean within-block spread between the best and worst stratum's CANCEL rate = 0.0747 over 318 blocks (bar 0.2).
- **B4 (descriptive)** - 1524 published correlation mentions; 9.6% quote an n nearby, 17.6% quote a stratum, 74.5% quote neither. Text scan, not a parse.

## Rule 8
- WF-1(a) idea 538's own pair, IS fit / OOS read once: pooled sign survives 2/2, FAMILY strata 4/4, PANEL strata 6/6.
- WF-1(b) record-wide IS->OOS sign survival on |rho_IS| >= 0.1: POOLED 0.9364 vs PER-STRATUM 0.9021.
- WF-2 the book: 12 arms, (level, cadence) picked on IS Sharpe alone; beat RULES v2 OOS 0/12, SPY 8/12, no-gate EW control 5/12.

## KEEP paths
- 4a 0/324 books; 4b 16/324 books. KEEP candidate: True.

SURVIVORSHIP: all three panels are current constituents; CAGR levels are inflated and the 4a/4b columns inherit that. The headline object is a correlation SIGN across cells of one panel, which is far less exposed than a level, but not immune.

## Addendum (`..._B_addendum.py`) — two corrections to this run's own B2

1. **GROUP-COUNT ARTEFACT.** Real strata carry up to 12 groups; the controls always carry 2, and
   more groups mechanically means more chances for two of them to disagree in sign. The k-ladder
   shows it directly: CANCEL runs 0.0277 at k=2, 0.0459 at k=3, 0.0664 at k=5, 0.0973 at k=12.
   At matched k=2 the headline 1.28x collapses — QUEUE 1.20x / CANON 1.02x on Pearson, and
   **below 1** on Spearman (0.98 / 0.76). B2's raw ratio should not be quoted; the k-matched one
   should.
2. **THE CONTROL WAS NOT ONE CONTROL.** B2 pooled ROWHALF and RANDOM2. Rows inside a `.grid.csv`
   are written in dial order, so ROWHALF is itself a real ordinal stratification. Split, k-matched:
   real strata 0.0261–0.0307, RANDOM2 (the only true null) 0.0039–0.0069, ROWHALF 0.0439–0.0586.
   So real strata do beat the true null by **3.4x–7.4x** — and are beaten by an arbitrary cut of
   the file at **0.43x–0.66x**. Stratification finds real structure; the *named* stratum is not
   the principled place to look for it.

## Answer

**NO — and the queue's proposed reporting fix is KILLED in the general form, PARKED in a narrow one.**
The 538 cancellation reproduces exactly (G1/G2, max|d rho| 0.0000) but it is **rare, not generic**:
3.6% of CANON quads, 4.3% of ALL, 5.3% of the QUEUE family; strict Simpson reversal 1.3%. Within
538's own cells it is a **FAMILY** fact and not a stratification fact — cutting the identical quad
by PANEL gives +0.045 / +0.068 / +0.027, no flip at all. Record-wide, which stratum you pick moves
the rate by only 7.5pp within a block (B3), and per-stratum rho signs survive IS→OOS **less** often
than pooled ones (0.9021 vs 0.9364) because the strata are smaller. Publishing a per-stratum rho
beside every pooled one would therefore add ~4 numbers per claim, ~96% of which say nothing, and
each less reproducible out of sample than the one it annotates.

What the census does establish is the **reporting gap**: of 1,524 published correlation mentions,
**74.5% quote neither an n nor a stratum**, and only 1.7% quote both; even among the 125 that say
"pooled" explicitly, only 11.2% quote an n. The defensible clause is the **n**, not the stratum —
it is one number, always available, never noisier out of sample, and it is the thing 9 in 10 of the
record's correlation claims are missing.
