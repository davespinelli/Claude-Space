# Idea 250 — locate-the-band-width-ceiling (cloud, 2026-09-06)

Script: `research/backtests/2026-09-06_locate-the-band-width-ceiling_cloud.py`
Outputs: `.grid.csv` (96 points + 12 controls), `.gate.csv`, `.walkforward.csv`, `.console.txt`

**Verdict: ANSWERED — the ceiling is located, and everything above 12% is a KILL.**

## What was run
One tuned parameter: MA re-entry band width in {3, 5, 8, 12, 16, 20, 25, 30}% (idea 74's
published rungs 3/5/8 carried as context; 12–30 are the queue's). Panels u56 / B136 /
SMALL484 (max_1d_move ≥ 1.0 screen applied first: 483 tradable of 485), books EWALL0 and
CAND20 at gross 0.75 under the **constant-gross convention** (survivors re-normalised to
GROSS, so idea 244's silent de-grossing channel is closed), cost rungs 10 and 25 bps,
weekly, t+1 execution. All 96 points printed. Panel, book and cost are reported at every
value and never selected on.

**Harness gate [D] passed before anything new was read**: u56/EWALL0/band 12%/10 bps
reproduces idea 74's published PARK row exactly — 14.1% / 1.233 / −19.4%, OOS 1.272,
turnover 1.93x.

## Q1 — an interior optimum DOES exist, and it is idea 74's own 12%
The Sharpe argmax is **interior in 8 of 12 cells**, and on the book idea 74 actually
PARKed (EWALL0) it is at **12% on both large-cap panels at both cost rungs**, with Sharpe
falling monotonically from there to the grid edge (Spearman of Sharpe on width over the
five new rungs: **−0.90** on u56/EWALL0 and −0.90 on B136/EWALL0; u56 1.2330 at 12% →
1.1233 at 30%, B136 1.1789 → 1.0657). So idea 74's "grid edge, not a located optimum"
caveat is **withdrawn for the EWALL0 book**: 12% is a real local maximum, not the ladder
running out of grid. SMALL484/EWALL0 puts it at 20%, also interior.

The ranked **CAND20 book is the exception**: its argmax is still at 30% on B136 and
SMALL484 (rho +0.70 / +0.90), i.e. that ladder is still unbounded. The mechanism table
says what it is buying: on CAND20/B136 the 30% band lifts CAGR 14.8% → 17.7% while MaxDD
deepens −25.7% → −26.3%. It is a return trade, not a risk one, and it clears no bar.

**Mechanism (the reason the ceiling exists at all).** `exit_frac` — the share of name-days
the band holds OUT of the book — is *not* monotone falling in width on the large-cap
panels: u56 0.316 (3%) → 0.346 (12%) → **0.556 (30%)**, B136 0.316 → 0.315 → **0.496**.
Past ~12% the hysteresis stops meaning "stay in through shallow dips" and starts meaning
"once out, stay out for years" (a name must clear MA×1.30 to re-enter). Flips keep falling
monotonically (u56 1.78 → 0.12 per name-year), so the wide end is a *slower, stickier and
more often absent* book, not a more invested one. That is the ceiling.

## Q2 — the broad-panel drawdown failure does NOT close above 12%; it closes below 8%
Idea 74's B136/EWALL0 DD failure (−21.7% vs the −20.2% cap) gets **monotonically worse**
on the wide ladder: dd_margin −1.50pp at 12% → −2.95 (16%) → −4.52 (20%) → −5.91 (25%) →
**−6.64pp at 30%**. DD is the binding bar at every width ≥ 8% on both cost rungs. Of the
32 B136 points, **4 sit inside the cap and all four are at the NARROW end** — EWALL0 at
3% (+1.73pp margin) and 5% (+0.77pp), at both 10 and 25 bps.

Those four are the grid's only 4a passes on a large-cap panel, and they also clear 4b:

| panel | band | cost | CAGR | Sharpe | MaxDD | H1/H2 | OOS Sharpe | TO | 4a | 4b |
|---|---|---|---|---|---|---|---|---|---|---|
| B136 | 3% | 10 | 11.8% | 1.071 | −18.5% | 1.174/0.981 | 1.078 | 4.8x | PASS | PASS |
| B136 | 3% | 25 | 11.0% | 1.005 | −18.7% | 1.109/0.913 | 1.012 | 4.8x | PASS | PASS |
| B136 | 5% | 10 | 12.0% | 1.073 | −19.5% | 1.157/1.001 | 1.097 | 3.7x | PASS | PASS |
| B136 | 5% | 25 | 11.4% | 1.023 | −19.7% | 1.109/0.948 | 1.045 | 3.7x | PASS | PASS |

(SPY over the same window: 15.2% / 0.889 / −33.7%, halves 0.957/0.834, OOS 0.882. RULES v1
on B136 @10 bps: 5.9% / 0.576 / −21.2% OOS.) This is a **re-confirmation of the already
published `EWall + band3-rw` book**, not a new candidate — see the memo — and it is *not*
what a rule-8 chooser picks.

## KEEP paths over the whole ladder (10 + 25 bps, 96 points)
4b passes by width: 3% → 4, 5% → 4, 8% → 2, 12% → 2, and **0 at 16, 20, 25 and 30%**.
4a passes: 3 / 3 / 3 / 1 / 1 / 1 / 1 / 2. Every 4b pass is EWALL0 on a large-cap panel;
SMALL484 passes nothing at any width (it fails H1, H2, OOS, DD *and* the CAGR floor).
Mean Sharpe by width peaks at 12% (0.968) and never recovers (0.949 / 0.936 / 0.941 /
0.947), while mean MaxDD deepens monotonically (−26.4% → −28.2%).

## Rule 8 — walk-forward (width chosen on 2009–2016 only, 2017–2026 read once)
SEL-IS picks 12% on all four EWALL0 cells and 30% on four of the six CAND20/wide cells
(mean chosen width 19.8%). The chooser beats the do-nothing control in **12/12 cells**
(mean +0.0489 OOS Sharpe) but beats the *pinned* 12% in only 6/12 (mean +0.0093) — i.e.
the fitting is worth nothing over simply writing 12% down. The only walk-forward cells
that clear 4b OOS are **u56/EWALL0 at both cost rungs** (band 12%, OOS 15.2%/1.272/−19.4%
at 10 bps and 14.9%/1.245/−19.5% at 25 bps, vs SPY OOS 0.882 and RULES v1 OOS 0.747).
B136 and SMALL484 pass nothing under any selector.

## Verdict
- **Widths above 12% are KILLED**: no 4b pass anywhere, Sharpe falls, drawdown deepens,
  and the B136 DD gap widens by 5.1pp across the new ladder.
- **Idea 74's PARK stands, with its caveat corrected**: 12% on u56/EWALL0 is an interior
  optimum, not a grid edge — but it still fails B136 on drawdown, so PARK not KEEP.
- **The DD cap on B136 is a narrow-band phenomenon**, closable only at 3–5%.

## Caveats
- SURVIVORSHIP (PROTOCOL rule 9 / idea 54): all three panels are current-constituent
  lists. That bias flatters stay-invested settings, which is the wide end of this ladder —
  so the finding *against* wide bands is if anything understated, and the CAND20 book's
  still-climbing ladder is the reading most likely to be survivorship.
- Idea 128: the IS window's worst SPY drawdown is shallower than the OOS window's, so the
  IS-readable 4b screen admits too much; SEL-4b picks 12% on B136/EWALL0 even though that
  width fails the full-sample DD cap. Reported, not repaired.
- OOS MaxDD equals full-sample MaxDD in every EWALL0 cell: the worst drawdown of every
  book here lives in 2020/2022, so the DD bar is entirely an out-of-sample statistic.
- t+1 execution only; no lag band (idea 126).
