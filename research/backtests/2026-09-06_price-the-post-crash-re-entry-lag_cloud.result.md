# idea 274 — price-the-post-crash-re-entry-lag (cloud, 2026-09-06)

**Verdict: PARK, not KEEP. The overlay does pay for itself outside 2020 — that part of the QUEUE
question is a clean YES — and its full-sample form clears 4a on both large-cap panels at both cost
rungs. But the pre-registered rule-8 selector does not pick that form: it picks (D=0.15, L=20),
whose OOS dSharpe on the LIVE panel is −0.0027 at 10 bps and −0.0178 at 25 bps. A candidate that
only wins when the parameters are read off the full sample is PARK (PROTOCOL rule 8).**

Script: `2026-09-06_price-the-post-crash-re-entry-lag_cloud.py`
Artefacts: `.grid.csv` (96 cells), `.episodes.csv`, `.walkforward.csv`, `.console.txt`.

## What was run

Base book = the live book, RULES v2 (EWall inside the 200d ±3% band, 0.75/N, gated-out weight to
cash, weekly, t+1). The overlay changes one thing: when SPY's drawdown from its running high
reaches −D, the per-name gate is replaced by `px > 20d MA` for the L trading days following the
latest trough; the episode disarms when SPY recovers to within 5% of its high. Two tuned
parameters, D and L. The fast MA (20d), the disarm level (5%) and the base book are fixed.

Grid: D ∈ {0.15, 0.20, 0.25} × L ∈ {10, 20, 30, 60, 90} × {U56, B136, SMALL439} × {10, 25} bps.
**The L grid was extended from the pre-registered {30, 60, 90} after 30 came out the argmax on its
edge; 30 is now interior and still the argmax on both large-cap panels.** All 90 overlay cells and
6 controls are reported.

## Does it pay outside 2020? Yes.

dSharpe vs the un-overlaid v2 control, calendar 2020 **deleted from both books**, 10 bps:

| panel | D | L=10 | L=20 | L=30 | L=60 | L=90 |
|---|---|---|---|---|---|---|
| U56 | 0.15 | −0.0052 | +0.0330 | **+0.0423** | −0.0262 | −0.0030 |
| U56 | 0.20 | +0.0200 | +0.0401 | **+0.0521** | −0.0231 | +0.0006 |
| U56 | 0.25 | +0.0151 | +0.0289 | +0.0296 | −0.0148 | −0.0191 |
| B136 | 0.20 | +0.0188 | +0.0409 | **+0.0592** | +0.0014 | +0.0164 |
| SMALL439 | 0.20 | +0.0164 | +0.0214 | +0.0314 | +0.0437 | **+0.0526** |

Sign counts over all 90 overlay cells: dCAGR > 0 in **90/90**, dCAGR ex-2020 in **80/90**,
dSharpe in 75/90, dSharpe ex-2020 in **57/90**, dMaxDD > 0 in only 34/90. The return leg is
robust and one-directional; the risk leg is not — on U56 and B136 the overlay leaves MaxDD
**exactly unchanged** (−12.05% / −12.18%, the drawdown is set outside every fast window), and on
SMALL439 at L=30 it makes it 1.1 pp *worse*.

At D=0.25 on SMALL439 the ex-2020 dSharpe is **exactly 0.0000** at every L — the single D=0.25
episode in the whole sample is March 2020, so deleting 2020 deletes the treatment. That is the
sanity check the ex-2020 column needed.

## The shape: it is a SHORT-window effect, not a long one

On both large-cap panels the curve peaks at L=30 and turns negative by L=60 (U56 D=0.20:
+0.0545 → −0.0094). Re-entering fast is worth something; *staying* on a 20-day gate for a quarter
gives it all back in whipsaw. SMALL439 is the exception — it rises monotonically to L=90, the grid
edge, which is a different (and unresolved) mechanism.

## Full-sample 4a, and why it is not a KEEP

`fast20-D20-L30` on U56 @10bps: **9.57% / 1.2601 / −12.05%**, halves 1.2805/1.2431, OOS
**10.27% / 1.3296 / −12.05%**, turnover 2.14×/yr — against the v2 control's 8.66% / 1.2056 /
−12.05% (halves 1.2259/1.1908, OOS 9.53% / 1.2851). Better CAGR, better Sharpe, both halves, OOS,
identical MaxDD. 25 of 96 cells clear 4a; 0 of 96 clear 4b (the CAGR floor fails in 90/90 overlay
cells — the 0.75-gross book is too low-return against SPY's 15.23%).

**The rule-8 selector picks something else.** Choosing (D, L) by IS Sharpe on 2009–2016 gives
(0.15, 20) in all six panel × cost cells, because D=0.15 arms 3 times in-sample while D=0.20 arms
once. Evaluated untouched on 2017–2026 that pick returns:

| panel | bps | IS Sharpe (ctl) | OOS Sharpe (ctl) | dOOS Sharpe |
|---|---|---|---|---|
| U56 | 10 | 1.1842 (1.1043) | 1.2823 (1.2851) | **−0.0027** |
| U56 | 25 | 1.1398 (1.0657) | 1.2305 (1.2482) | **−0.0178** |
| B136 | 10 | 1.1666 (1.0931) | 1.1414 (1.1206) | +0.0208 |
| B136 | 25 | 1.1229 (1.0543) | 1.0834 (1.0759) | +0.0076 |
| SMALL439 | 10 | 0.6438 (0.5790) | 0.6045 (0.5665) | +0.0380 |
| SMALL439 | 25 | 0.5810 (0.5194) | 0.5319 (0.5056) | +0.0263 |

Mean +0.0120, positive in 4 of 6, **negative on the live panel at both cost rungs**. Under the
narrower pre-registered {30, 60, 90} grid the selector had picked (0.20, 30) and scored +0.0644 in
6/6 — i.e. **extending the grid by two rungs flipped the walk-forward verdict.** That fragility is
itself the finding, and it is why this is PARK: the arm that wins is not the arm an honest
in-sample chooser reaches for. This is the record's "selection loses to doing nothing" pattern
(ideas 141/151/155/229) appearing for the twelfth time.

## Event count — the real limit

The whole result rests on very few independent events. Over 2009–2026: D=0.15 arms 7 times on
U56/B136 (2009-02, 2010-07, 2011-08, 2018-12, 2020-03, 2022-05, 2025-04) and 5 on SMALL439;
D=0.20 arms **3** times; D=0.25 arms **once**. Only 1 D=0.20 episode and 0 D=0.25 episodes fall in
the IS window, so D=0.25 is literally **unchoosable in sample**. No Sharpe delta computed off 3
events should be treated as an estimate with a usable standard error.

## Caveats

Weekly cadence caps how fast "fast" can be: the 20d gate acts at the next weekly rebalance, not
intra-week, so this prices the honest form of the live book rather than the best case. All three
panels are current-constituent lists; SMALL439 has no delistings, so its levels — and the
beaten-down cohort a fast re-entry buys — are optimistic by an unknown one-directional margin.
