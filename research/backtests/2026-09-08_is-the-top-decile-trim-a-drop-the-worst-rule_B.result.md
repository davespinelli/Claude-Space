# Idea 227 — is-the-top-decile-trim-a-drop-the-worst-rule (lane B, 2026-09-08)

**Verdict: KILL.** Idea 155's q = 0.90–0.95 trim is **not the composite ranking**. It is a
"delete ~10% of the eligible set" operation that a *persistent random key* reproduces at the
same trim depth, the same held count and a **lower** turnover. 4a **0 of 3297** grid points
against the live RULES v2; 4b passes at a **higher** rate for the random-key arms (17.3%) than
for the composite (13.9%). No RULES change, no book, no KEEP.

Script: `research/backtests/2026-09-08_is-the-top-decile-trim-a-drop-the-worst-rule_B.py`
Artefacts: `.console.txt`, `.grid.csv.gz` (3,297 rows), `.deepnull.csv`, `.walkforward.csv`

---

## Reproduction gates (all passed BEFORE any new number was read)

| gate | requirement | result |
|---|---|---|
| [a] harness | idea 2's U56/CAND20 (12.7% / 1.093 / −18.3%) and live RULES v1 (6.5% / 0.666 / −13.8%) | 12.7% / **1.092** / −18.3%; 6.5% / **0.665** / −13.8% |
| [b] premise | idea 155's own headline premia at 10 bps: U56 q=0.90 **+0.0316**, B136 q=0.95 **+0.0171** | **+0.0316** and **+0.0171**, \|d\| = **0.0000** both |
| [c] cost identity | `net(c) = gross − turnover·c/1e4` vs a direct 10 bps backtest | max\|d\| = **0.000e+00** |
| [d] shared control | q = 1.00 must be the identical book across all 26 arms | max\|d\| returns = **0.000e+00** |

Idea 155's number reproduces exactly, so this is a test of that number, not of a different one.

## Design

Idea 155's CANDq verbatim — eligible set (200d MA + vol20 < 0.60, tradable, composite defined),
hold the top `n_t = clip(round(q·n_elig), 1, n_elig)` equally weighted at **75% gross at every q
and every key**, weekly, t+1, so idea 157's cash channel is closed by construction and the number
of names held is **identical across arms to 4 dp** (29.29 on U56, 71.55 on B136, 115.32 on
SMALL484). Only *which* names are dropped changes.

Arms: 5 keys × 2 directions + 2 nulls × 8 seeds = **26**, on 3 panels × 6 q × 7 cost rungs.
Tuned parameters: **q** and the **cost rung c** — idea 155's own two. Key, direction, seed and
panel are the treatment axes of the question and are reported at every point, never chosen.

* **KEYS** `COMP` (155's composite, no vol tilt) · `MOM` (12−1) · `R6` · `R3` · `LOWVOL` (−vol20)
* **DIRECTIONS** `KEEPTOP` (drop the worst — 155's reading) · `KEEPBOT` (drop the *best* — the sign control)
* **NULLS** `SHUFW` fresh permutation every rebalance week (the queue's wording) · `SHUFF` one
  uniform draw per name held forever

## The null the question needs is SHUFF, not SHUFW

`SHUFW` destroys the information **and** the persistence: it triples turnover (412.7 vs the
control's 144.7 on U56). Beating it says only that the composite is *persistent*, which was never
in doubt. `SHUFF` destroys the information alone and holds the trim depth, the held count and the
turnover profile fixed, so it isolates the claim. Against SHUFW the composite looks overwhelming
(z +2.6 to +7.1). Against SHUFF it does not.

### Deep null — 60 persistent random keys per cell, 10 bps

| panel | q | COMP premium | null mean | null sd | null max | COMP percentile | exact p (one-sided) | COMP turnover vs null |
|---|---|---|---|---|---|---|---|---|
| U56 | 0.85 | +0.0263 | −0.0163 | 0.0410 | +0.0843 | 88.3 | **0.131** | 175.8 vs 156.3 |
| U56 | **0.90** | **+0.0316** | −0.0092 | 0.0364 | +0.0602 | 86.7 | **0.148** | 164.9 vs 153.3 |
| U56 | 0.95 | +0.0031 | −0.0047 | 0.0177 | +0.0333 | 65.0 | 0.361 | 158.7 vs 149.7 |
| B136 | 0.85 | −0.0079 | −0.0053 | 0.0232 | +0.0483 | 46.7 | 0.541 | 169.7 vs 153.3 |
| B136 | 0.90 | +0.0072 | −0.0041 | 0.0206 | +0.0555 | 75.0 | 0.262 | 163.2 vs 151.8 |
| B136 | **0.95** | **+0.0171** | −0.0043 | 0.0118 | +0.0186 | 98.3 | **0.033** | 154.4 vs 149.5 |

**1 of 6 cells clears 5%**, which is what six tests produce by chance, and the one that clears
(B136 q=0.95) is contradicted by the *same construction on the other panel* (U56 q=0.95, 65th
percentile, p 0.36). Idea 155's own headline cell, U56 q=0.90, sits at the **86.7th percentile**
of random keys — inside the null, and paying **7.6% more turnover** than the average random key to
get there. The composite is not buying the premium; it is buying a slightly worse cost profile and
landing where a coin lands.

## The key that "wins" is a different key on every panel

Mean premium at 10 bps, KEEPTOP arms only (the `.grid.csv.gz` carries all 3,297 points):

| panel | COMP | MOM | R3 | R6 | LOWVOL | SHUFF | SHUFW |
|---|---|---|---|---|---|---|---|
| U56 | **+0.0030** | −0.0389 | −0.0367 | −0.0273 | −0.1308 | −0.0341 | −0.1711 |
| B136 | −0.0167 | −0.0411 | −0.0519 | **−0.0048** | −0.1096 | −0.0263 | −0.1535 |
| SMALL484 | −0.0059 | −0.0287 | −0.0172 | +0.0104 | **+0.0351** | −0.0036 | −0.1067 |

The argmax key is **COMP on U56, R6 on B136, LOWVOL on SMALL484** — three panels, three answers,
and on two of the three the composite is beaten by a single leg or by a screen that contains no
return information at all. `LOWVOL` even flips sign between the large-cap panels (−0.13, −0.11)
and the small panel (+0.035), because the vol gate has already removed the tail it screens.
Before costs (0 bps) the picture is the same: **every** key family's mean premium is negative on
B136 and U56 except COMP/KEEPTOP on U56 (+0.0157) and R6/KEEPTOP on B136 (+0.0110). There is no
gross edge for the trim to defend.

## What the ranking *does* carry: direction, not level

`KEEPTOP > KEEPBOT` in **77 of 90** (panel × key × q) cells, mean gap **+0.0746**. So the keys are
not noise — inverting one costs real money (COMP/KEEPBOT is −0.178 on U56, −0.081 on B136). The
reconciliation is the whole finding:

> **A composite ranking carries enough information to LOSE money if you invert it, and not enough
> to BEAT a random trim of the same depth.** Dropping the best 10% is much worse than random;
> dropping the worst 10% is indistinguishable from random.

`LOWVOL` is the exception that confirms it — its direction gap is **negative** on both large-cap
panels (−0.06 to −0.20), i.e. keeping the *high*-vol half of an already vol-gated set beats keeping
the low-vol half.

## Mechanism: the premium is a turnover statistic

Spearman(premium, turnover) = **−0.739 / −0.809 / −0.741** across the three panels;
Spearman(premium, n_held) = +0.458 / +0.487 / +0.335. The cost ladder makes it explicit — mean
premium falls monotonically with the rung for **every** key on **every** panel (e.g. U56 COMP
−0.0514 → −0.1595 from 0 to 30 bps), and falls fastest for the arm with the most churn
(SHUFW: −0.0231 → −0.4663). Nothing in this family pays *more* as costs rise, so the trim is not
a cost-avoidance rule either; it is a book that is slightly smaller and slightly more expensive.

## Rule 8 walk-forward (params on 2009–2016, 2017–2026 read once)

| panel | selector | arm | OOS CAGR | OOS Sharpe | OOS MaxDD | vs do-nothing |
|---|---|---|---|---|---|---|
| U56 | S0 do-nothing | q=1.00 | 11.34% | 1.1133 | −15.87% | — |
| U56 | S1 IS-argmax (all keys) | **SHUFF6**/KEEPTOP/q=0.50 | 11.36% | 1.0356 | −21.73% | **−0.0777** |
| U56 | S2 IS-argmax (COMP only) | COMP/KEEPTOP/q=0.90 | 12.14% | 1.1263 | −16.79% | +0.0130 |
| U56 | S3 random arm | SHUFW6/KEEPTOP/q=0.90 | 10.22% | 1.0060 | −16.10% | −0.1073 |
| B136 | S0 do-nothing | q=1.00 | 10.59% | 1.0191 | −17.69% | — |
| B136 | S1 IS-argmax (all keys) | **SHUFF1**/KEEPTOP/q=0.90 | 10.43% | 1.0030 | −18.73% | **−0.0160** |
| B136 | S2 IS-argmax (COMP only) | COMP/KEEPTOP/q=0.95 | 10.85% | 1.0236 | −17.76% | +0.0045 |
| B136 | S3 random arm | SHUFF6/KEEPTOP/q=0.70 | 10.23% | 0.9868 | −17.38% | −0.0323 |
| SMALL484 | S0 do-nothing | q=1.00 | 5.00% | 0.4086 | −34.63% | — |
| SMALL484 | S1 IS-argmax (all keys) | **LOWVOL**/KEEPTOP/q=0.70 | 5.53% | 0.4458 | −36.72% | +0.0372 |
| SMALL484 | S2 IS-argmax (COMP only) | COMP/KEEPTOP/q=0.85 | 3.82% | 0.3322 | −39.73% | **−0.0764** |
| SMALL484 | S3 random arm | SHUFF7/KEEPTOP/q=0.95 | 5.02% | 0.4073 | −34.87% | −0.0013 |
| all | **SPY** | buy & hold | 15.45% | 0.8820 | −33.72% | — |
| all | **RULES v2 (live)** | baseline | 9.53% / 7.98% / 4.55% | 1.2851 / 1.1185 / 0.6629 | −12.05% / −12.24% / −12.09% | — |

The chooser that is honestly allowed to see all the keys (**S1**) picks a **shuffled key on both
large-cap panels** — the strongest possible statement that the in-sample surface is noise — and
loses to doing nothing on both (−0.078, −0.016). The believer's chooser (S2), restricted to
idea 155's own family, wins by **+0.0130 / +0.0045** on the large-cap panels and loses **−0.0764**
on the small panel; the mean over the three is **−0.0196**. On the OOS premium the trim band is
+0.0250 / +0.0130 / +0.0065 (U56) and −0.0041 / +0.0077 / +0.0045 (B136) — all well inside the
0.018–0.041 sd of the persistent-random null.

Per **idea 229** the quotable number for a selection result is the **REGRET** (the IS chooser's OOS
loss against the unselected arm of its own ladder), not the margin against a baseline book. The
regret here is **best-OOS-arm − S1** on each panel, at 10 bps over the 156-arm ladder:
U56 1.1867 (SHUFF7/KEEPTOP/q=0.70) − 1.0356 = **0.151**; B136 1.0699 (SHUFF2/KEEPTOP/q=0.70)
− 1.0030 = **0.067**; SMALL484 0.5291 (SHUFF5/KEEPTOP/q=0.50) − 0.4458 = **0.083**.
Mean **0.100**, above idea 229's pooled 0.0387 [0.021, 0.058] — and the OOS-best arm is a
**shuffled key on all three panels**, which is what a surface with no signal in it looks like.

## KEEP paths (both, all 3,297 points)

* **4a vs RULES v2 (live): 0 of 3297.** Every point fails on drawdown, and 3,139 fail on both
  halves as well. The live book's −12.1% MaxDD is out of reach for a 75%-gross equity book.
* **4a vs RULES v1 (continuity only): 928 of 3297** — carried for comparability with idea 155's
  table; RULES v1 has not been the live book since 2026-09-06.
* **4b vs SPY: 451 of 3297**, and the pass rate is **highest for the random keys**:

  | key family | SHUFF | R6 | COMP | LOWVOL | MOM | SHUFW | R3 |
  |---|---|---|---|---|---|---|---|
  | 4b pass rate | **17.3%** | 15.9% | 13.9% | 12.7% | 11.5% | 11.0% | 9.9% |

  SMALL484 is **0 of 1099** on 4b — the 16th reproduction of idea 136. A 4b pass here is a
  property of the EWall-shaped book that all 26 arms share, not of any key, which is idea 144's
  point restated: a re-keyed book is the same book.

The two headline cells, priced in full at 10 bps:

| arm | CAGR | Sharpe | MaxDD | halves | OOS | 4a | 4b |
|---|---|---|---|---|---|---|---|
| U56 COMP/KEEPTOP q=0.90 | 11.30% | 1.0808 | −16.79% | 1.114 / 1.054 | 1.1263 / 12.14% / −16.79% | H1,H2,DD | pass |
| B136 COMP/KEEPTOP q=0.95 | 11.09% | 1.0424 | −17.76% | 1.176 / 0.918 | 1.0236 / 10.85% / −17.76% | H1,H2,DD | pass |
| *control* q=1.00 U56 | 10.40% | 1.0492 | −15.87% | 1.067 / 1.036 | 1.1133 | — | pass |
| *control* q=1.00 B136 | 10.70% | 1.0253 | −17.69% | 1.143 / 0.915 | 1.0191 | — | pass |

Both headline arms clear 4b — and so do their own do-nothing controls, and so do 174 random-key
arms. Per idea 144 that is not a new book, and per the deep null it is not a new edge.

## What the record should now say about idea 155

Idea 155's surviving line — *"a pre-registered q=0.90 trim clears 4b on both large-cap panels and
is PARKed, not proposed"* — should be closed as **KILLED**, not PARKed, and for a reason stronger
than the one 155 gave itself. 155 parked it because the +0.0072 B136 margin was smaller than a
construction sign flip. The real objection is that **the operation has no content**: the same
premium arrives from a key drawn from a uniform distribution, so "trim the bottom decile by the
composite" and "trim a fixed random tenth" are the same rule at 10 bps.

The direction result is worth keeping as a positive: a composite ranking is a **veto**, not a
**selector** — reliable about which names to refuse, uninformative about which to prefer. That is
consistent with idea 82's "drop the ranking" and with the live RULES v2 having no ranking at all.

## Limits

* Survivorship: `universe_broad.json` and the small panel are **current constituents**,
  one-directional; nothing here corrects it, and the 4b pass rates above inherit it in full.
* The deep null is 60 seeds at 3 q on 2 panels; the 8-seed null covers the rest of the grid, which
  resolves the sign but not a 5% threshold at those points.
* One construction only — CANDq at 75% gross with a time-varying count. Idea 155 showed the
  argmax moves under a constant count; this run does not re-test the key swap under that
  construction. Queued as idea 447.
