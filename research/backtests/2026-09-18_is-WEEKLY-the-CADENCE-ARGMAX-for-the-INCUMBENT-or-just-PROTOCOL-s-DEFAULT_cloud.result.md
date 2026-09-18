# Idea 1335 (lane cloud, 2026-09-18) — is WEEKLY the CADENCE ARGMAX for the INCUMBENT, or just PROTOCOL's DEFAULT?

**ANSWERED: WEEKLY IS THE ARGMAX, NOT A LUCKY DEFAULT, ON THE PANEL THAT CARRIES EVERY
COMMITTED 4b PASS — AND THE QUEUE'S OWN RATIONALE IS FALSIFIED: THE CADENCE ARGMAX DOES NOT
MOVE WITH THE COST RUNG ON ANY OF THE THREE PANELS (0 of 3). KILL as a dial, no new book.**

Script: `research/backtests/2026-09-18_is-WEEKLY-the-CADENCE-ARGMAX-for-the-INCUMBENT-or-just-PROTOCOL-s-DEFAULT_cloud.py`
(offline, deterministic, 35s). All 60 cells in `.grid.csv`, rule 8 in `.walkforward.csv`,
argmax-by-rung in `.argmax_by_cost.csv`, gates in `.gates.csv`, full console in `.console.txt`.
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py untouched (rule 6).

## The instrument

Two dials and no more (rule 4): **CADENCE {D, W, 2W, M, Q} x COST {0, 10, 25, 50} bps**, 20
cells per panel, 60 in all, every one published. The book is the record's frozen incumbent —
3-leg rank composite ((21,252), (0,126), (0,63)) x the `0.5+0.5*above-200d` tilt, eligibility
above-200d AND vol20 < 0.60, N=15 equal weight, min hold H=126, **gross 0.60**, decisions
lagged one row and applied at t+1 (rule 2). Only *when it re-picks* and *what the tape charges*
vary. Gross returns and turnover are cadence properties, so each (panel, cadence) is run once
and all four rungs are read off the same pair — the grid is exact, not interpolated, and no
cell is a re-tune. 2W is the engine's own W array subsampled every second entry.

## 1. The queue's rationale, tested and falsified

> *"if the cadence argmax moves with the cost rung, every committed number in this family is a
> 10-bps artifact"*

Full-sample Sharpe argmax over the 5 cadences, at each rung:

| panel | 0 bps | 10 bps | 25 bps | 50 bps | stable? |
|---|---|---|---|---|---|
| U56 | **W** 1.1931 | **W** 1.1717 | **W** 1.1394 | **W** 1.0855 | STABLE |
| B136 | **M** 1.1100 (W 1.0840) | **M** 1.0950 (W 1.0630) | **M** 1.0722 (W 1.0314) | **M** 1.0337 (W 0.9783) | STABLE |
| SMALL | **W** 0.5797 | **W** 0.5570 | **W** 0.5227 | **W** 0.4656 | STABLE |

**The argmax moves with the cost rung on 0 of 3 panels.** The committed numbers in this family
are therefore NOT a 10-bps artifact — the cost rung changes every *level* (U56 W Sharpe 1.1931
-> 1.0855 from 0 to 50 bps) and no *ranking*. W is the argmax in 8 of 12 (panel, rung) cells.
What the rung does move is the *size* of B136's M-over-W gap, monotonically and in M's favour:
+0.0261 / +0.0320 / +0.0408 / +0.0554. A slower cadence is worth more the more the tape charges
— which is the rebate reading, priced, and it is still not enough to change an argmax anywhere.

## 2. Weekly is earned on U56 and second-best elsewhere

OOS Sharpe order at 10 bps (2017-2026):

- **U56**: W 1.1965 > 2W 1.1251 > M 1.0902 > D 1.0769 > Q 1.0110 — **W ranks 1 of 5.**
- **B136**: M 1.1196 > W 1.0387 > 2W 1.0230 > Q 0.9328 > D 0.8679 — W ranks 2 of 5.
- **SMALL**: 2W 0.5750 > W 0.4728 > Q 0.3891 > M 0.2525 > D 0.1997 — W ranks 2 of 5.

So on U56, the only panel on which this family has ever cleared 4b, PROTOCOL's inherited default
is simultaneously the full-sample argmax at every cost rung and the out-of-sample argmax. It was
never chosen and it did not need to be. **Idea 1305's W->M sign is reproduced on all three
panels** (this run -0.1061 / +0.0320 / -0.1427 against 1305's -0.1053 / +0.0283 / -0.0796;
gate G2), and turnover is monotone non-increasing across D >= W >= 2W >= M >= Q on all three
(G3): U56 3.39 / 2.46 / 2.12 / 1.86 / 1.41 per year, W->M refunding +6.0 bp/yr at 10 bps and
+30.2 at 50.

## 3. B136's better cadence is unbuyable, and that is the run's one substantive new fact

M beats W on B136 at every rung full-sample (+0.0261..+0.0554) and out of sample (+0.0809), and
it is the ex-post best OOS cadence on that panel. **It fails 4b on the drawdown leg at every
rung** — MaxDD -22.76% against the cap of 0.60 x SPY's -33.72% = -20.23%, a 2.53 pp miss — while
W on B136 passes all four legs at -15.97%. D and 2W on B136 fail the same leg (-22.98%, -21.85%).
The cadence that earns more Sharpe on B136 buys it with drawdown the protocol will not pay for,
so there is nothing to claim: **4a 0 of 60; 4b 23 of 60 full-sample and 23 of 60 full AND OOS
(U56 19/20, B136 4/20, SMALL 0/20)**, and every one of the 19 U56 passes is the incumbent or a
slower version of it that no cell dominates on Sharpe.

## 4. Rule 8 (cadence chosen on warm-up..2016-12-31 by argmax IS Sharpe at each rung; 2017-2026 read ONCE)

| panel | rung | IS pick | OOS CAGR / Sharpe / MaxDD | PROTOCOL W OOS | d Sharpe | 4b OOS |
|---|---|---|---|---|---|---|
| U56 | 10 bps | **W** | 15.15% / **1.1965** / -16.38% | 15.15% / 1.1965 / -16.38% | +0.0000 | PASS |
| B136 | 10 bps | 2W | 15.17% / 1.0230 / -21.85% | 14.03% / 1.0387 / -15.97% | **-0.0157** | FAIL (DD) |
| SMALL | 10 bps | M | 2.85% / 0.2525 / -32.36% | 6.38% / 0.4728 / -32.63% | **-0.2202** | FAIL (Sharpe, DD, CAGR) |

Comparands at 10 bps OOS: SPY 15.26% / 0.8738 / -33.72%; RULES v2 live 9.46% / 1.2769 (U56 run),
7.85% / 1.1019 (B136), 4.41% / 0.6473 (SMALL).

The IS chooser picks PROTOCOL's W in only **4 of 12** (panel, rung) cells; choosing the cadence
costs a mean **-0.0746 of OOS Sharpe** (min -0.2268, max +0.0010) and **-0.75 pp of OOS CAGR**,
and beats W in **1 of 12** (B136 @50 bps, +0.0010). **4b on every OOS leg after rule 8: 4 of 12
— all four are the U56 rungs where the pick IS W**, i.e. every surviving pass comes from not
choosing. H_HINDSIGHT fires again: the ex-post best OOS cadence differs from the IS pick in
**8 of 12** cells.

## 5. The tape-vintage caveat this run had to measure (gate G1b FAILS and is reported, not loosened)

The W/10 bps cell on U56 is idea 1305's committed flat control and idea 1339's PROTOCOL_DEFAULT
cell. This run reproduces its **MaxDD to 1e-8 and its IS-window Sharpe to 6.6e-7** (G1a), which
proves the construction is identical, but the tape-sensitive statistics land off the committed
values: CAGR +0.000129, Sharpe +0.001096, **H1 -0.006378, H2 +0.006984**, OOS Sharpe +0.001826.
The cause is not construction. Commit **4e19a80 "Daily close 2026-09-18" rewrote
data/prices.csv, prices_broad.csv and prices_small.csv.gz wholesale (9410 lines replaced, +6 net
rows) after 1305 was committed**: 1305 ran on a tape ending 2026-09-17 / 09-11 / 09-11
(4707 / 4703 / 4198 rows), this one on 2026-09-18 (4708 / 4708 / 4203) with the whole history
re-adjusted (G1c). The declared 3e-3 replay tolerance therefore **fails at 6.98e-3 and is
reported as a failure rather than widened**: cross-run replay of a *half-sample* Sharpe in this
repo is resolution-limited to ~7e-3 by daily re-adjustment of `data/prices*.csv`, and no
committed number in this family carries a tape stamp. The committed cell's **verdict** is
unaffected (G1d: 4b PASS on all four legs, Sharpe 1.1717 vs SPY 0.8844, MaxDD -16.38% inside
the -20.23% cap). Gates: **11 of 12 pass**, the twelfth diagnosed above.

## Verdict

**KILL as a dial / ANSWERED. No new book, no RULES change.** Weekly is not an unpriced tuned
coordinate that happens to flatter the record: it is the Sharpe argmax at every cost rung and
the OOS argmax on U56, it is second of five on the other two panels, and an IS chooser allowed
to move it loses 0.0746 of OOS Sharpe on average. B136 prefers monthly by a gap that widens with
cost, but monthly breaches the 4b drawdown cap by 2.53 pp at every rung, so the preference is
unbuyable. There is nothing here to promote and nothing to retract.

## Survivorship (rule 9)

U56 / B136 / SMALL are CURRENT-constituent lists. SMALL is a sub-$2B screen carried back to 2010
with the protocol-mandated 52 tickers of `max_1d_move >= 1.0` dropped (663 of 715 priced names
kept), so its **levels are an upper bound** and only its cadence CONTRASTS are read here — its
best cell (2W, 0.5750 OOS Sharpe) still fails all four 4b legs.
