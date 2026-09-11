# Idea 670 — is-the-GROSS-dial-s-4b-FOOTPRINT-the-CAGR-FLOOR-alone (lane C, 2026-09-11)

**ANSWERED: the queue's hypothesis is CONFIRMED, and 657's question is answered YES — PROTOCOL 4b
needs a matched-gross leg. KILL for capital: no new book, no RULES change, nothing promoted.
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py untouched.**

Grid: 10 arms × 8 gross rungs × 2 panels = **160 points, every one reported** (`.grid.csv`).
Two tuned parameters and no more: GROSS rung and PANEL. Every arm definition is a committed
book of the record's own (RULES v2 band book; idea 664's band 0.08 pick; 668's CADENCE, N and
VOLCAP dial books; the 2026-09-04 KEEP 4b book CAND20 = top-20 equal weight, no vol scaler;
the 2026-09-03 memo's Finding-2 EWELIG book; and **SPYBH = g × SPY, a zero-signal control**).

**GATES: ALL PASS.** G1 `fast_backtest` vs `engine.backtest` @10 bps **6.939e-18**. G2
`band_book(0.03,0.75)` == `baseline.rules_v2_weights` **0.000e+00** (exact). G3 idea 668's
committed GROSS-dial rows reproduce on TODAY's tape at **4.607e-07 (U56) / 4.885e-07 (B136)**
over 5 rungs × 6 metrics + SPY, bar 5e-4 — a cleaner reproduction than 668's own vintage note
led me to expect; the U56 deviation grows to 7.99e-03 / 1.10e-02 / 1.90e-02 on truncations to
09-09 / 09-08 / 09-04, and B136's cache still ends 2026-09-04 (bears on open idea 517). G4 the
ladder contains the live 0.75 and 1.00. **G5 CORRECTION, stated not hidden: I mis-set this bar.**
`weights(g) == g·weights(1.00)` reads **2.776e-17**, which FAILS the exact-0.0 bar I pre-registered;
the two sides divide by the name count in a different order (`g/k` vs `g·(1/k)`) so they can never
be bit-identical. Re-read at the 1e-12 float bar G1 uses for the same reason: **PASS**. G6 SPYBH at
g=1.00 tracks SPY buy-and-hold **0.000e+00** in Sharpe.

## 1. The footprint is the CAGR floor, and the DD cap is what it trades against

4b decomposed into its five legs, pass share pooled over 10 arms × 2 panels (n=20 per rung):

| g | L1 H1>SPY | L2 H2>SPY | L3 OOS>SPY | L4 DD cap | L5 CAGR floor | 4a | 4b |
|---|---|---|---|---|---|---|---|
| 0.20 | 0.800 | 0.700 | 0.700 | 1.000 | **0.000** | 0.000 | 0.000 |
| 0.50 | 0.800 | 0.700 | 0.700 | 1.000 | **0.100** | 0.000 | 0.000 |
| 0.75 | 0.800 | 0.700 | 0.750 | 0.650 | **0.550** | 0.000 | 0.100 |
| 0.95 | 0.800 | 0.700 | 0.750 | 0.350 | **0.950** | 0.000 | 0.300 |
| 1.00 | 0.800 | 0.700 | 0.750 | 0.250 | **1.000** | 0.000 | 0.250 |

**L1 and L2 are CONSTANT across the entire ladder (spread 0.000 — the Sharpe legs do not know
that gross moved at all); L3 moves by one cell in twenty (spread 0.050).** L5 sweeps the full
0.000 → 1.000 (Spearman **+0.994**) and L4 sweeps 1.000 → 0.250 the other way (**−0.976**). The
levels move mechanically and monotonically: rho(CAGR, g) = **+1.000 on 20/20** arms and
rho(|MaxDD|, g) = **+1.000 on 20/20**, while median max|ΔSharpe| across the whole ladder is
**0.0032** (max 0.0148, B136/CAND05). Nuance the record should carry: Sharpe is monotone in g on
most arms (|rho| ≥ 0.9 on 15/20) but **the movement is economically nil and not even signed the
same way** — U56/BAND08 reads rho −1.000, B136/CAND05 +1.000. 668 quoted 0.0052 on the band book
alone; on ranked books the flatness is **~3× looser (0.0148)**, so 657's "0.0052" is a band-book
number, not a ladder-wide one.

## 2. The queue's count: how many committed 4b passes survive matched gross

**12 of 20 (panel, arm) cells pass 4b somewhere on the ladder. At the matched live gross 0.75,
2 of those 12 survive. At every rung, 0 of 12.** Across all 160 points: **4b 18/160, 4a 0/160,
BOTH 0/160.** 657's "0 pass at all three grosses" **replicates** on a denser 8-rung ladder over
ten arms.

The 10 casualties are exactly the band-book family and its cadence/vol-cap cousins, whose passes
sit at g ≥ 0.95 (U56 and B136 BAND03/BAND03_M/BAND08) or at a single off-live rung (CAND20_NOCAP
at 0.60, U56/CAND20_VS at 0.85). The 2 survivors are **U56/CAND20 — the record's own 2026-09-04
KEEP 4b book — and B136/EWELIG**.

**This is the one place the queue's framing needs correcting, and it matters.** U56/CAND20 passes
at **exactly g = 0.75 and nowhere else**: its CAGR floor breaks below 0.75 and its DD cap breaks
above it. That pass is therefore *not* bought by exposure — raising g destroys it. The band-book
family's passes are the opposite and are pure exposure. So "the GROSS dial's 4b footprint is the
CAGR floor alone" is true of the dial, but **"every 4b pass on the record is a gross artefact" is
false**: on this census 2 of 12 are not. (U56/CAND20 also fails on B136, where its H2 Sharpe is
0.8025 against SPY's 0.8340.)

## 3. The zero-signal control names the mechanism

SPYBH carries no signal whatever, yet **g alone clears the CAGR floor at g ≥ 0.75 on both panels**
— i.e. at exactly the live gross, the 4b floor is not an edge test. It clears the DD cap only at
**g ≤ 0.50**. The two legs therefore define a **gross window**, and for a book with no edge the
window is **CLOSED (width −0.25 on both panels)**. The window is open on 17/20 cells and closed on
3 (both SPYBH cells and B136/CAND20_VS at −0.20). **The width of that window is the edge test**;
it is necessary and not sufficient — 5 cells with an open window still take 0 4b passes because
they fail a Sharpe leg. Window widths are quantised to the 8-rung ladder and should be read as
rung counts, not as continuous quantities.

## 4. Rule 8 (PROTOCOL 8): g chosen on 2009–2016, evaluated 2017–2026 untouched

Two pre-registered choosers, both reported at all 20 cells (`.walkforward.csv`). SPY OOS:
CAGR 15.45% / Sharpe 0.882 / MaxDD −33.72%. Live book OOS: 7.98% / 1.119 / −12.24% (B136 ref).

| chooser | picks g=1.00 | OOS CAGR | OOS Sharpe | OOS MaxDD | beat SPY | beat LIVE | 4b | 4a |
|---|---|---|---|---|---|---|---|---|
| CH_SHARPE (argmax IS Sharpe) | 18/20 | 15.32% | 1.010 | −23.96% | 15/20 | **0/20** | 5/20 | 0/20 |
| CH_MEMO (2026-09-03 live rule) | 3/20 | 12.09% | 1.009 | −19.15% | 15/20 | **0/20** | 9/20 | 0/20 |

The two rules **agree on the pick in only 15% of cells** yet differ by a median **0.0007** of OOS
Sharpe — the choice of gross rule is a coin flip in risk-adjusted terms while moving OOS CAGR by
3.2 pp and OOS MaxDD by 4.8 pp. A flat IS-Sharpe ladder sends an argmax chooser to the top rung
18 times out of 20; the memo's own "smallest G that clears the cap and the floor" rule is the one
that keeps gross at or below 0.75 in 13/20 cells. **Neither chooser beats the live book OOS in a
single cell (0/40).**

## 5. Honest caveat the result depends on — the cash leg

The engine pays **0% on the de-grossed sleeve**, so at g < 1 the CAGR floor is mechanically harder
and part of "exposure buys the floor" is really "cash earns nothing". 90/160 points fail L5; the
flat cash rate that would flip each one is published in `.grid.csv` (`cash_rate_to_flip_L5`).
**27 of the 90 would flip at ≤ 5%/yr**, and at the live g=0.75 the median failing point needs only
**4.22%**. This is a diagnostic, not a claim: open idea **642** PARKs the real T-bill path for lack
of a cached series, and that path (≈10 bps to 2015, ≈500 after 2022) is backloaded onto exactly the
OOS window rule 8 reads. **Any matched-gross leg added to PROTOCOL 4b should be decided only after
642 has its data.**

## 6. PROPOSAL for the Sunday review (not applied here — PROTOCOL rule 6)

Nothing is promoted and no RULES wording is offered, because no book on this grid clears 4a or
beats the live book OOS. The proposal is to PROTOCOL, for the Sunday review to accept or reject:

> **4b (matched-gross leg, proposed):** a 4b pass must state the gross at which it was taken, and
> must be re-reported at the panel's matched gross 0.75. A pass that exists only at g ≥ 0.95, or
> only above the gross at which `g × SPY` itself clears the CAGR floor on the same panel and
> sample, is reported as EXPOSURE, not as a 4b pass.

On this census that leg would reclassify **10 of the 12** cells and leave U56/CAND20 and
B136/EWELIG standing.

**SURVIVORSHIP (PROTOCOL 9):** B136 is today's constituents, so every B136 level above is biased
upward. The load-bearing claims here are within-panel, within-ladder leg shares, which
survivorship biases far less than it biases a level; no B136 level is a tradeable estimate.

Artefacts: `.grid.csv` (160), `.legs.csv` (8), `.flatness.csv` (20), `.survival.csv` (20),
`.window.csv` (20), `.walkforward.csv` (40), `.gate3.csv` (10), `.console.txt`.
