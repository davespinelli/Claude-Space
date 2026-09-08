# Idea 452 — does-a-pre-registered-arm-beat-its-own-IS-chooser-generally (lane C, 2026-09-08)

**Verdict: SPLIT.** The queue's *mechanism* is **confirmed on its own instance and only there**;
the *generalisation* is **KILLED**; and the parent claim needs one **correction**.

* On idea 232's own 84 cells, the chooser's whole hit-rate deficit is a corner: it picks
  `n <= 10` in **33.3%** of cells and loses **100%** of those (mean **−0.0778**, hit **0.0%**);
  on the other 66.7% it beats the pre-registered arm on **both** axes (**+0.1856**, hit
  **100.0%**). "A chooser paying for a corner it reaches too often" is exactly right — there.
* **CORRECTION.** That divergence exists only because the chooser and the pre-registered arm do
  not choose over the same ladder: lane B's `A1` is pinned at n = 20 and varies the gate, while
  `S1` is an IS-argmax over gate × n — six arms `A1` cannot reach. Restricted to `A1`'s own
  ladder the chooser does **not** diverge, it simply **LOSES on both axes** (+0.0510 / 57.1% vs
  the pre-registered +0.0621 / 88.1%). And `A1` is not the ladder's best arm: `GATE_OFF/n40`
  dominates everything at **+0.1583 / 100.0%**.
* **The general claim fails.** Over **201 committed instances** re-read from the record, the
  mean-up/hit-down quadrant holds in **10.9%** (vs the MEDIAN position rule) and **13.9%** vs
  each ladder's best-hit arm; the modal quadrant is the chooser **DOMINATING** at **69.7%**.
  On a 189-cell live corpus built here it is **10.6%** (matched) / **10.1%** (wide).
* **The mechanism does not generalise either.** corr(DIVERGE, ladder-endpoint pick share) is
  **+0.006** (matched) and **−0.129** (wide); the tercile table is non-monotone
  (4.5% / 26.9% / 1.5%). Widening a chooser's pool does not manufacture divergence — it makes
  the chooser worse on **both** axes (paired hit **−5.2 pp**, t **−5.02**, n = 189).
* **What survives** is a weaker, real statement: the asymmetry. DIVERGE outnumbers its mirror
  REVERSE **22–5** in the census (sign p **0.0015**) and **33–11** live (p **0.0013**). Choosers
  do tilt mean-up/hit-down — in about one instance in ten, not as a signature.

Script: `research/backtests/2026-09-08_does-a-pre-registered-arm-beat-its-own-IS-chooser-generally_C.py`
Artefacts: `.console.txt`, `.flagship.csv`, `.census.csv` (445 rows incl. sensitivity),
`.arms.csv` (369), `.cells.csv` (378), `.walkforward.csv` (63), `.keeppaths.csv` (378)

---

## Reproduction gates (passed BEFORE any new number was read)

| gate | requirement | result |
|---|---|---|
| [G1] harness | `fast_backtest` == `engine.backtest` on all three panels | max \|d returns\| **1.0e-17**, \|d turnover\| **1.8e-16** |
| [G2] cost identity | `net(c) = gross − turnover·c/1e4` vs a direct 25 bps backtest | **0.000e+00** on all three panels |
| [G3] premise | idea 232's published `A1−A0` +0.0621 / 88.1% and `S1−A0` +0.0978 / 66.7% | **+0.0621 / 88.1%** and **+0.0978 / 66.7%**, exact |
| [G4] reconstruction | this run's chooser rebuilt from lane B's 840-row arm grid vs lane B's own walk-forward file | \|d A0\| \|d A1\| \|d S1\| all **0.000e+00**, S1 pick identical **84 of 84** |

G4 is the gate that licenses Part B: the same reconstruction code that re-reads 201 committed
files reproduces the flagship's published picks and margins exactly.

## The statistic

An INSTANCE is a pool of cells sharing one arm ladder A (|A| ≥ 3, ≥ 8 cells). For a cell c and
an object x (a fixed arm, or a chooser):
`margin_x(c) = OOS_Sharpe_x(c) − base(c)`, `mean_x = mean_c margin_x`, `hit_x = share_c[margin_x > 0]`,
with `base` = the pool mean over A (every object priced against the same number) or the ladder's
own control arm. **DIVERGENCE(a) := mean_chooser > mean_a AND hit_chooser < hit_a** — the queue's
shape. Its three alternatives (DOMINATE / LOSE / REVERSE) are counted at every point.

**Tuned parameters (2):** `p` — the pre-registered position rule naming the fixed arm the chooser
is compared to, `p ∈ {CONTROL, MEDIAN, LADDER-MIN, LADDER-MAX}`; and `h` — the fold horizon,
`h ∈ {1, 2, 3}` years. All 4 × 3 grid points are reported everywhere. Panels, families, cost
rungs, comparand convention and the matched-vs-wide contrast are reported axes, never selected on.

## Part A — the flagship, every arm on the (mean, hit) plane (comparand = CONTROL, 84 cells)

| object | mean | hit | sd | skew |
|---|---|---|---|---|
| ARM GATE_OFF/n40 | **+0.1583** | **100.0%** | 0.0616 | +0.18 |
| ARM GATE_OFF/n30 | +0.1062 | 100.0% | 0.0550 | +0.57 |
| ARM GATE_ON/n40 | +0.1191 | 83.3% | 0.0939 | −0.32 |
| **ARM GATE_OFF/n20 — the queue's pre-registered arm** | **+0.0621** | **88.1%** | 0.0924 | +1.84 |
| ARM GATE_ON/n30 | +0.0621 | 83.3% | 0.0639 | −0.02 |
| ARM GATE_ON/n20 (the control) | 0.0000 | 0.0% | 0.0000 | — |
| ARM GATE_OFF/n10 | −0.0299 | 33.3% | 0.1549 | +0.66 |
| ARM GATE_OFF/n5 | −0.0421 | 48.8% | 0.2086 | −0.30 |
| ARM GATE_ON/n10 | −0.1076 | 16.7% | 0.1076 | +0.40 |
| ARM GATE_ON/n5 | −0.1445 | 16.7% | 0.1639 | +0.05 |
| **CHOOSER-WIDE (gate × n) — lane B's S1** | **+0.0978** | **66.7%** | 0.1461 | −0.14 |
| **CHOOSER-MATCHED (the n = 20 ladder)** | +0.0510 | 57.1% | 0.0965 | +1.90 |

Two readings the parent did not make. (i) The pre-registered arm is **fourth** on mean and
**third** on hit: two arms of its own ladder dominate it, so "pre-registration beat the chooser"
is a statement about one nominated arm, not about pre-registration. (ii) The chooser restricted
to the pre-registered arm's ladder is **LOSE**, not DIVERGE — it is beaten on both axes.

### A2 — the queue's mechanism, decomposed on its own instance

Both statistics are linear in the pick mixture, so each pick contributes `freq × (its conditional)`:

| picked arm | freq | mean given pick | hit given pick | share of the chooser's mean | share of its hit |
|---|---|---|---|---|---|
| GATE_OFF/n40 | 34.5% | +0.2069 | 100.0% | 73.0% | 51.8% |
| GATE_OFF/n20 | 16.7% | +0.2567 | 100.0% | 43.7% | 25.0% |
| GATE_ON/n30 | 11.9% | +0.0393 | 100.0% | 4.8% | 17.9% |
| GATE_OFF/n30 | 2.4% | +0.0861 | 100.0% | 2.1% | 3.6% |
| GATE_ON/n40 | 1.2% | +0.2349 | 100.0% | 2.9% | 1.8% |
| **GATE_OFF/n10** | **16.7%** | **−0.0419** | **0.0%** | **−7.1%** | **0.0%** |
| **GATE_OFF/n5** | **16.7%** | **−0.1137** | **0.0%** | **−19.4%** | **0.0%** |
| TOTAL | | +0.0978 | 66.7% | | |

The thin corner is **one third of the cells and every one of the chooser's losses**. Delete those
picks and the same chooser reads **+0.1856 / 100.0%** against the pre-registered arm's
+0.0621 / 88.1% — it dominates. The queue's sentence is therefore right about *this* chooser:
it pays for a corner it reaches too often. The corner is the **WIDTH** dial's thin end, which is
not on the pre-registered arm's ladder at all.

## Part B — the record, re-read (201 instances from 1,876 committed CSVs)

Tiers: **201** instances, 1,405 files carry no per-row IS *and* OOS Sharpe, 168 admit no
arm/cell split, 102 have too few balanced cells. 164 instance files admit more than one split;
238 sensitivity rows under the alternative splits are carried in `.census.csv`.

Comparand = pool mean, median instance 90 cells / 3 arms:

| position rule | n | DIVERGE | REVERSE | DOMINATE | LOSE | IDENT | Δmean | Δhit | DIVERGE vs REVERSE |
|---|---|---|---|---|---|---|---|---|---|
| MEDIAN | 201 | **10.9%** | 2.5% | **69.7%** | 13.4% | 3.5% | +0.1099 | +17.2% | 22–5, sign p **0.0015** |
| LADDER-MIN | 201 | 2.5% | 2.0% | 41.3% | 32.3% | 21.9% | +0.0122 | +9.6% | 5–4, p 1 |
| LADDER-MAX | 201 | 3.5% | 3.0% | 67.7% | 22.9% | 3.0% | +0.1802 | +47.9% | 7–6, p 1 |
| CONTROL (only 6 instances name a control arm) | 6 | 66.7% | 0.0% | 0.0% | 33.3% | 0.0% | +0.0092 | −6.3% | 4–0, p 0.125 |

Against each ladder's **best-hit** arm — the strongest form of the queue's claim — DIVERGE is
**13.9%**, LOSE **53.7%**, DOMINATE 9.0%.

Corner mechanism, by ladder-endpoint pick share: **4.5% / 26.9% / 1.5%** across terciles —
non-monotone; corr(conc, DIVERGE) **−0.190**. Endpoint-reaching does not predict divergence in
the record.

## Part C — the live corpus (3 panels × 7 families × 3 rungs, ladders built here)

189 cells per comparand (panel × family × rung × h). Chooser MATCHED (the family's own ladder)
vs WIDE (family ∪ the WIDTH ladder, lane B's shape):

| comparand | rule | MATCHED DIVERGE / DOMIN / LOSE / REV | WIDE DIVERGE / DOMIN / LOSE / REV |
|---|---|---|---|
| pool mean | MEDIAN | **10.6%** / 43.4% / 36.0% / 5.3% | **10.1%** / 28.0% / 55.0% / 6.9% |
| pool mean | CONTROL | 5.3% / 37.6% / 51.9% / 3.7% | 4.8% / 31.7% / 58.2% / 5.3% |
| control | MEDIAN | **17.5%** / 36.5% / 35.4% / 5.8% (p 0.0013) | 10.6% / 27.5% / 38.1% / 23.8% |
| control | LADDER-MIN | 19.6% / 43.9% / 32.8% / 2.1% (p 1.0e-07) | 8.5% / 47.6% / 37.0% / 6.9% |

Every h × rung point is reported in the console: DIVERGE ranges 4.8%–23.8% (matched) and
4.8%–14.3% (wide) with no trend in h and no trend in the rung. By panel: broad 14.3%, u56 11.1%,
small 6.3% (matched). By family: CADENCE 25.9% and GROSS 22.2% at the top, WIDTH and GATE 0.0%.

**The pool-width test (paired, same cells, same fixed arms).** Discordant pairs **17 wide-only vs
18 matched-only, McNemar p 1.0** — widening the pool does *not* create divergence. What it does
do is make the chooser worse on both axes: hit **63.1% → 57.9%** (paired d −5.2 pp, t **−5.02**),
mean +0.0472 → +0.0303 (t −1.63). The WIDE chooser leaves its own family in **65.2%** of folds
and its corner-pick share is *lower* (10.8% vs 43.5%), which is why the flagship's corner story
does not travel: on the live corpus the wide pool's extra arms are not corners.

## Part D — PROTOCOL rule 8 (parameters on 2009–2016, 2017–2026 read ONCE, 63 cells)

| object | mean margin | hit | OOS Sharpe | OOS CAGR | OOS MaxDD | > SPY | > RULES v2 |
|---|---|---|---|---|---|---|---|
| CHOOSER-MATCHED | +0.0244 | 63.5% | 0.9410 | 10.63% | −19.37% | 63.5% | 23.8% |
| CHOOSER-WIDE | **−0.0445** | **36.5%** | 0.8721 | 17.67% | −28.53% | 50.8% | 34.9% |
| CONTROL arm | **+0.0450** | **73.0%** | 0.9616 | 8.04% | −14.30% | 65.1% | 14.3% |
| MEDIAN arm | +0.0174 | **76.2%** | 0.9340 | 8.48% | −15.98% | 66.7% | 27.0% |
| LADDER-MIN | −0.0633 | 41.3% | 0.8533 | 8.71% | −17.71% | 55.6% | 39.7% |
| LADDER-MAX | +0.0198 | 55.6% | 0.9364 | 8.33% | −16.00% | 63.5% | 17.5% |

References, same window: **SPY 0.8820 / 15.45% / −33.72%**, **RULES v2 0.9848 / 7.08% / −13.02%**,
RULES v1 0.5938, pool mean 0.9166, OOS oracle 1.0140. At the PROTOCOL rung (10 bps):

| panel | CHOOSER-MATCHED | CHOOSER-WIDE | MEDIAN arm | SPY | RULES v2 |
|---|---|---|---|---|---|
| u56 | 1.191 / 13.2% / −17.6% | 1.039 / 23.0% / −28.5% | 1.215 / 10.2% / −13.7% | 0.882 / 15.5% / −33.7% | 1.285 |
| broad | 1.062 / 11.2% / −16.5% | 0.881 / 16.2% / −23.6% | 1.073 / 9.8% / −15.3% | 0.882 / 15.5% / −33.7% | 1.119 |
| small | 0.585 / 8.1% / −24.4% | 0.684 / 13.9% / −32.7% | 0.536 / 5.8% / −18.8% | 0.882 / 15.5% / −33.7% | 0.566 |

On the one non-overlapping window the record actually uses, **a do-nothing control arm beats both
choosers on both axes** — the pre-registered arm wins here by DOMINATION, not by the queue's
divergence. That is the fifth independent reproduction of the record's selector result and it
does not need the mean-vs-hit-rate story to say it.

## Part E — both KEEP paths (PROTOCOL 4a and 4b)

* **4a: 3 of 324** honest arm rows. 45 arm rows *are* the live RULES v2 book re-expressed (EW
  band3, gross 0.75, weekly is a member of 5 of the 7 ladders) and 10 of those "pass" 4a against
  themselves on a float tie (`fast_backtest` vs `engine.backtest` differ at ~1e-17) — they are
  excluded and named. The 3 survivors are all `u56 WIDTH n=80`, i.e. gross **0.525** (top-80 of a
  56-name panel), a **de-grossed** variant of the live book: idea 311's gross-scalar flag, not a
  signal. Chooser/position books: 4a 14 of 378, **0** once the live book's own rows are removed.
* **4b: 38 of 369** arm rows (u56 26, broad 12, small 0 — idea 136 again), concentrated in
  LOOKBACK (20) and at gross 1.00; binding bar over all arms: CAGR 171, H2 76, H1 70, DD 52.
  Every passer is a known ranked/EW u56 or broad book at full gross, none produced by a chooser.
* **No KEEP, no PARK, no RULES change.** RULES.md, scan.py, bot.py, baseline.py and PROTOCOL.md
  untouched.

## Predictions, scored

| | prediction | outcome |
|---|---|---|
| P1 | divergence is not the general signature (< half of instance × rule pairs) | **CONFIRMED** — 10.9% census, 10.6% live |
| P2 | the WIDE chooser diverges strictly more often than the MATCHED one | **FALSIFIED** — 17 vs 18 discordant, McNemar p 1.0; widening lowers both statistics instead |
| P3 | divergence rises with corner-reach | **FALSIFIED** — corr +0.006 / −0.129, terciles non-monotone |
| P4 | no book promoted; any 4a is the live book, any 4b the known carve-out | **CONFIRMED** |

P2 and P3 were this run's own mechanism story and both are dead. What replaced them is narrower
and better evidenced: the flagship's divergence is a **thin-n corner inside one wider pool**
(A2), and pool width in general buys nothing (C3).

## What the record should now say

1. Idea 232's headline pair — pre-registered **+0.0621 / 88.1%** vs chooser **+0.0978 / 66.7%** —
   is **not a like-for-like comparison**: the chooser ranges over gate × n, the pre-registered arm
   over the gate at n = 20 only. Quote it with its ladder, or quote the matched pair
   (**+0.0510 / 57.1%** vs +0.0621 / 88.1%), which says the same thing more strongly and without
   the divergence.
2. **Mean-vs-hit-rate divergence is not a chooser signature.** It holds in ~1 instance in 10
   (10.9% census, 10.6% live), while the chooser dominates a mid-ladder arm ~70% of the time in
   the record's own committed files. It is, however, **directionally real** (22–5 and 33–11
   against its mirror), so the useful version of the queue's instinct is: *publish mean and hit
   rate together* — they disagree often enough (one in ten) that quoting one alone can invert a
   selector verdict.
3. A **corner** explains the flagship and nothing else measured here. "Chooser reaches a corner
   too often" should be quoted as a property of a named pool, never as a general diagnosis.

## Limits

* Survivorship (idea 54): u56, broad and small are current constituents; every CAGR is flattered.
  All statistics here are within-pool contrasts, which a level bias does not move.
* The census infers each file's arm/cell split heuristically (idea 436's committed vocabulary).
  It is gated by G4 on the flagship and carries 238 alternative-split sensitivity rows, but a
  reconstructed pool is not always a selector's real choice set; where a file pools over a
  reported axis the ladder is too wide, which *inflates* the wide-pool effect this run reports as
  null.
* Only files carrying a per-row IS **and** OOS Sharpe can be re-read at all: 201 of 1,876. The
  other 1,675 are silent, not supportive.
* Instances overlap heavily (the same books recur across files); folds overlap by construction
  (expanding IS windows, overlapping OOS at h > 1). No instance-level or fold-level t here is an
  independent-sample t; the canonical rule-8 split in Part D is the only non-overlapping read.
* One book shape per family, weekly, t+1, gross 0.75 unless the family is GROSS. PROTOCOL rung
  10 bps; 0 and 25 bps reported throughout.
