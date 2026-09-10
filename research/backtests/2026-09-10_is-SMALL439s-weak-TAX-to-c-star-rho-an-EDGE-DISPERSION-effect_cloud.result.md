# Idea 610 — is SMALL439's weak TAX-to-c* rho an EDGE-DISPERSION effect? (cloud, 2026-09-10)

**CONFIRMED, on a pre-registered bar and against a permutation floor — and confirmed by the
mechanism the queue named, not merely by the statistic it asked for.** Nothing promoted, no RULES
change; RULES.md, PROTOCOL.md, scan.py, bot.py, baseline.py untouched.

Corpus: idea 605/608's own 648 twin-pair arms (3 panels × 18 level-arms × 3 depths × 2 cadences ×
2 gross), 10 bps, weekly, t+1. Tuned exactly two as the queue allows — PANEL (4) × BIN COUNT K
∈ {2,3,4,5,6,8,10} — **all 28 grid points reported**, IS and OOS, on two censoring rules.

**GATES, all PASS.** G1 derived ladder vs live `engine.backtest` through idea 399's `apply_gate`
at 7 rungs **3.47e-18**; G2 fast metrics vs `engine.metrics` on 200 series **2.22e-16**; G3 idea
608's committed `.arms.csv.gz`, **648/648** arms joined on 12 columns at **5.68e-14** with the
+inf set identical; G5 `DRAG == SWITCH_TAX + TIMING` **2.17e-17**; G6 the closed form
rho(dSharpe_0/SLOPE, c*) = **+0.999861**, median level error 0.55%, so `log c* = E − S` is the
same object as the measured c*.

**G4 CORRECTION for the record.** Idea 608's per-panel triple −0.755 / −0.724 / −0.297 is a
**g = 0.75 slice**, not a per-panel reading; its own `.rho.csv` gives whole-panel
**−0.7436 / −0.7123 / −0.2741**. Its pooled −0.5131 and its pooled mean-within-quintile −0.8413
both reproduce to 4dp. The gap is ≤ 0.023 and moves no verdict; the bars below were pre-registered
on the quoted 0.297 / 0.458 and are **not** restated after the fact.

**Q1 — the queue's test: CLOSES.** SMALL439's mean within-edge-bin |rho(tax, c*)| runs
0.5592 / 0.6851 / 0.7584 / 0.7705 / 0.7755 / 0.7928 / **0.8194** over K = 2…10, i.e. **0.2741 →
0.8194, a gain of +0.5453** against a pre-registered CLOSES bar of 0.60. The three-panel spread
falls **0.4695 → 0.1223** (K=8; 0.1466 at K=10) against a bar of 0.229. Conditioning also lifts
U56 (+0.008…+0.121) and B136 (+0.149…+0.213), but **SMALL439 gains 2.5–4× more than either**,
which is the queue's claim exactly. Uncensored (idea 612's worry, +inf ranked top, 0 kept) the
levels drop across the board — raw 0.0909, best 0.6535 — and the same ordering and the same
closing hold.

**Q2 — the floor.** The same statistic on bins of identical sizes drawn at random, 200 draws per
panel per K: SMALL439's excess over the null mean is **+0.286 to +0.559 with p = 0.000 at all
seven K**, against U56's +0.036…+0.128 and B136's +0.153…+0.229. The lift is not what binning does
to a Spearman.

**Q3 — the fork, which is the real answer.** With `log c* = E − S` (E = log dSharpe_0,
S = log SLOPE), rho(tax, c*) has exactly two legs, and only one of them moves:

| leg | U56 | B136 | SMALL439 | span |
|---|---|---|---|---|
| PROXY  rho(tax, SLOPE) | +0.9592 | +0.9694 | +0.9472 | **0.022** |
| CONTAMINATION  rho(SLOPE, c*) | −0.7667 | −0.6957 | **−0.2910** | **0.476** |
| sd(log dSharpe_0) | 0.6324 | 0.8604 | **0.9668** | — |
| EDGE SHARE of Var(log c*) | 0.8835 | 0.7665 | **1.2351** | — |

The tax is an equally good stand-in for SLOPE on all three panels. **SLOPE is the exact
denominator of c* — no proxy error at all — and it still orders SMALL439's c* at only −0.291.**
So the weakness is entirely in the numerator: SMALL439 carries the widest zero-cost edges
(sd(log E) 0.967, edge IQR ratio 3.54) over the narrowest slopes (sd(log S) 0.764), and its edge
share of Var(log c*) exceeds 1 (E and S co-move the wrong way). Note the proxy leg is nominally
weakest on SMALL439 too, but by 0.022 — a distinction with no content.

**Q4 — rule 8.** Every quantity rebuilt inside 2009/2011–2016 only, K picked there per panel, OOS
(2017+) read once. SMALL439: IS pick **K=5** (|rho_IS| 0.8316) → **OOS |rho| 0.7845** against an
OOS raw of **0.1401**, a gain of **+0.6444**, with OOS regret vs the hindsight-best K of only
−0.0438. The fork's own legs walk forward with the same signature: OOS rho(SLOPE, c*) is
−0.7778 / −0.6638 / **−0.1423**, OOS rho(tax, SLOPE) flat at +0.957 / +0.955 / +0.962.

**Q5 — PROTOCOL, both KEEP paths, no candidate.** All 648 arms at 0/10/25 bps: **4a 3 / 0 / 0**
(zero at PROTOCOL's own rung), **4b 306 / 141 / 45**, **BOTH 0 at 10 bps**. By panel at 10 bps,
4b is U56 66/216, B136 75/216, **SMALL439 0/216**. Rule-8 book chooser (IS Sharpe pick, OOS read
once, 18 cells at 10 bps): 4a 0/18, 4b 2/18, beats RULES v2 OOS **1/18**, beats SPY OOS 12/18;
picked-arm OOS means U56 10.87% / 1.1538 / −15.38%, B136 10.28% / 1.0705 / −15.82%, SMALL439
2.28% / 0.2427 / −28.08%, against RULES v2 OOS (9.48% / 1.2788 / −12.05%; 7.98% / 1.1185;
3.85% / 0.5680) and SPY OOS (15.32% / 0.8758 / −33.72%). **Nothing is promoted.**

**Prescription (a proposal for Sunday review, not adopted here).** A published rho between a
COST statistic and a crossing cost c* is a statement about the denominator only. Because
c* = dSharpe_0 / SLOPE identically, any such rho is contaminated by the panel's edge dispersion,
and the contamination is panel-specific and large: it is the whole of the −0.75 / −0.27 gap the
record has been reading as a panel difference. Any future rho(cost-statistic, c*) should be
published **conditioned on dSharpe_0**, or beside rho(SLOPE, c*) so the reader can see which leg
is moving.

**SURVIVORSHIP.** All three panels are current-constituent screens, so every CAGR and drawdown
level above is optimistic; SMALL439 is 439 sub-$2B names that exist today (44 dropped for
max_1d_move ≥ 1.0 per `data/small_meta.csv`), starting 2010-01-04. Every claim in this run is a
rank statistic comparing arms **within** a fixed panel, which a common level shift does not move;
the cross-panel comparison at the heart of Q1/Q3 does inherit whatever differential the three
screens' survivorship carries, and the walk-forward in Q4 is the only control offered against it.

Script `research/backtests/2026-09-10_is-SMALL439s-weak-TAX-to-c-star-rho-an-EDGE-DISPERSION-effect_cloud.py`;
outputs `.arms.csv.gz`, `.cells.csv.gz`, `.q1.csv`, `.q2_floor.csv`, `.q3_fork.csv`,
`.walkforward.csv`, `.picks.csv`, `.refs.csv`, `.console.txt`.
