# Idea 447 — does-the-key-swap-survive-a-CONSTANT-count (cloud lane, 2026-09-08)

**Verdict: SPLIT — question answered, no book.** The VETO/SELECTOR split is a property of the
**RANKING**, not of the count rule. Swapping idea 227's time-varying count (CANDq) for a
constant count at equal cash (CONSTn-dg) moves the veto by **0.002 Sharpe** (mean direction gap
+0.1070 → +0.1047 over 630 cells each) and moves the selector result not at all (COMP/KEEPTOP
clears the 60-seed persistent-random null at p < 0.05 in **10 of 75** cells under CANDq and
**9 of 75** under CONSTn-dg). The one *new* fact is a retraction: idea 227's single significant
cell, **B136 q = 0.95 (p = 0.033)**, does **not** survive the count swap — at the matched
constant count it sits at the **31.7th percentile, p = 0.683**. 4a **0 of 26,460**. No KEEP.

Script: `research/backtests/2026-09-08_does-the-key-swap-survive-a-CONSTANT-count_cloud.py`
Artefacts: `.console.txt`, `.grid.csv.gz` (26,460 rows), `.curve.csv`, `.veto.csv`, `.null.csv`,
`.walkforward.csv`, `.keep.csv`

---

## Reproduction gates (run BEFORE any new number was read)

| gate | requirement | result |
|---|---|---|
| [a] harness | the fast backtester must replicate `engine.backtest` on 6 books | max \|d returns\| **5.6e-17**, \|d turnover\| **6.9e-16** |
| [b] cost identity | `net(c) = gross − turnover·c/1e4` vs a direct 10 bps backtest | max \|d\| = **5.6e-17** |
| [c] shared control | CANDq @ S = 1.00 identical across all 70 arms | **FAILED as stated: 1.70e-03** — see below |
| [d] premise | idea 227's CANDq COMP/KEEPTOP cells at 10 bps: U56 q=0.90 **1.0808**, B136 q=0.95 **1.0424** | **1.0798** (\|d\| 0.0010) and **1.0425** (\|d\| 0.0001) |

**Gate [c] and the 0.0010 in gate [d] are the same declared construction difference, and it is
reported rather than patched.** This run sets the count target from the **gate-only** eligible
count `E_t` (200d MA + vol20 < 0.60), because CONSTn's `n` must also be key-independent for the
two constructions to be matched. Idea 227 set it from the **key-masked** count. A name that
passes the gate but has an undefined key is therefore dropped from the book here without lowering
the target, so keys with different warm-ups hold marginally different books at S = 1.00: COMP and
MOM (252 days) hold 37.44 names on U56 against R3/R6/LOWVOL's (63/126/20 days) 37.50. The whole
effect is a Sharpe sd of **2.8e-05 (U56) / 2.0e-04 (B136) / 4.0e-04 (SMALL439)** and it is two
orders of magnitude below every difference this run reads. It does mean the S = 1.00 arm is a
*near*-shared control, not an exact one, and every premium below is quoted against COMP's
S = 1.00 book.

## Design

Idea 227's arms on three constructions at **matched mean book size**, so the count rule is the
treatment and the gate, the 75% gross level, the weekly cadence, t+1 execution and the cost
identity are all held fixed:

| construction | count | weight | what it is |
|---|---|---|---|
| `CANDq` | `n_t = clip(round(S·E_t), 1, E_t)` | `0.75 / count_held` | idea 227's; count tracks breadth, gross always 75% |
| `CONSTn-dg` | `n = round(S · mean_IS E_t)`, fixed | **`0.75 / n` per name** | idea 155's *constant count at equal cash*; de-grosses when `E_t < n`. **The queue's target.** |
| `CONSTn-rw` | the same fixed `n` | `0.75 / count_held` | not asked for; the decomposition control, because CANDq and CONSTn-dg differ in two ways at once |

`n` is pinned on **2009–2016 only** (idea 160's matching convention), so the constant-count arms
never read the evaluation window to set their own size: U56 n = 15/20/25/31/34/36, B136
36/50/63/77/86/90, SMALL439 54/74/94/114/127/134 at S = 0.40/0.55/0.70/0.85/0.95/1.00.

Arms: 5 keys × 2 directions + a **60-seed persistent-random null** (`SHUFF`, one uniform draw per
name held forever — the turnover-matched null; idea 227 lane B established that the weekly-redraw
null answers a different question, so it is not re-run). **Tuned parameters (2):** P1 the depth S,
P2 the cost rung ∈ {0, 5, 10, 15, 20, 25, 30} bps. Panel, construction, key, direction and seed
are reported at every point and never chosen on. 26,460 grid points, all committed.

## (a) THE VETO survives the count rule intact

Direction gap = Sharpe(KEEPTOP) − Sharpe(KEEPBOT), same panel, key, depth and rung.

| construction | cells | gap > 0 | mean gap | median | min | max |
|---|---|---|---|---|---|---|
| CANDq | 630 | 450/630 | **+0.1070** | +0.0665 | −0.5262 | +0.7425 |
| CONSTn-dg | 630 | 509/630 | **+0.1047** | +0.0851 | −0.3336 | +0.6332 |
| CONSTn-rw | 630 | 518/630 | **+0.1018** | +0.0830 | −0.3481 | +0.6317 |

Per key, protocol rung, pooled over panels and depths — the same ordering under all three count
rules, including `LOWVOL`'s sign inversion, which lane B flagged as the exception that proves the
rule (keeping the *high*-vol half of an already vol-gated set beats keeping the low-vol half):

| construction | COMP | MOM | R6 | R3 | LOWVOL |
|---|---|---|---|---|---|
| CANDq | +0.1413 | +0.1097 | +0.1588 | +0.0800 | **−0.0213** |
| CONSTn-dg | +0.1427 | +0.1131 | +0.1194 | +0.0621 | **−0.0081** |
| CONSTn-rw | +0.1449 | +0.1155 | +0.1225 | +0.0671 | **−0.0283** |

At the protocol rung with S < 1.00 the gap is positive in **20 of 25** cells on U56 and B136 under
every construction. Inverting a ranking costs real money whatever the count rule is: **R1
confirmed.**

## (b) THE SELECTOR result also survives — and idea 227's one significant cell does not

COMP/KEEPTOP against the 60-seed persistent-random null, exact one-sided p = share of null draws
≥ COMP, protocol rung:

| construction | COMP/TOP cells p < 0.05 (S < 1.00) | mean percentile | all 5 keys × TOP |
|---|---|---|---|
| CANDq | 5 of 15 | 71.3 | **10 of 75 (13.3%)** |
| CONSTn-dg | 1 of 15 | 64.0 | **9 of 75 (12.0%)** |
| CONSTn-rw | 2 of 15 | 70.2 | **10 of 75 (13.3%)** |

**R2 confirmed.** The composite is no more of a selector under a constant count than under a
floating one. On U56 — the panel idea 155's headline lived on — *every* cell is inside the null
under every construction: p runs 0.133–0.383 (CANDq), 0.267–0.383 (CONSTn-dg), 0.233–0.283
(CONSTn-rw). The count rule changes the *level* of the book (U56 COMP at S = 0.85 is 1.0739 under
CANDq and 1.1219 under CONSTn-dg) but it hands the same +0.05 to a random key: the null mean moves
from 1.0362 to 1.0992 alongside it.

**The retraction.** Lane B's one cell below 5%, B136 q = 0.95, reproduces here under CANDq
(**96.7th percentile, p = 0.033**, matching lane B's 0.033 to 3 dp). Under the matched constant
count the same cell is **31.7th percentile, p = 0.683**, and under CONSTn-rw **53.3rd, p = 0.467**.
Lane B already called it "contradicted by the same construction on the other panel"; it is now
also contradicted by the same panel under a different count rule, so nothing in the composite's
trim clears a null anywhere on a large-cap panel.

The cells that *do* clear are all on **SMALL439** and they clear under all three constructions
(CANDq p = 0.017/0.033/0.033/0.033 at S = 0.40–0.85; CONSTn-dg p = 0.050/0.000/0.083/0.067;
CONSTn-rw 0.033/0.000/0.083/0.067). That is a genuine construction-invariant signal — on a
**current-constituents, survivorship-biased** panel, where the composite's job is largely to avoid
the names that fell out of favour and stayed there. It is a shape result, not a tradable one, and
it delivers **0 of 8,820** 4b passes.

## Where the argmax goes under a constant count

Idea 155's claim was that the selectivity argmax moves to **0.55 (U56) / 1.00 (B136)** under a
constant count. Half of it reproduces:

| panel | CANDq argmax | CONSTn-dg argmax | idea 155 |
|---|---|---|---|
| U56 | S = 0.85 (+0.0247) | **S = 0.85** (+0.0728) | 0.55 — **not reproduced** |
| B136 | S = 0.95 (+0.0172) | **S = 1.00** (+0.0448) | 1.00 — **reproduced** |
| SMALL439 | S = 0.40 (+0.1074) | S = 0.55 (+0.0797) | — |

And the whole CONSTn-dg premium is available to a random key: at U56 S = 1.00 the null earns
**+0.0661** against COMP's **+0.0669**. The constant count's apparent lift over the floating one
is the de-grossing, not the ranking — `CONSTn-rw`, which matches exposure, gives COMP/TOP
**+0.0061** at the same point, and the null **−0.0065**.

## Rule 8 (PROTOCOL 8): parameters on 2009–2016, 2017–2026 read once

| construction | cells | margin > 0 | mean MARGIN | mean REGRET | picks a *shuffled* key |
|---|---|---|---|---|---|
| CANDq | 18 | 12/18 | +0.0105 | 0.0839 | **6/18** |
| CONSTn-dg | 18 | 12/18 | +0.0181 | 0.1377 | **6/18** |
| CONSTn-rw | 18 | 5/18 | −0.0009 | 0.1084 | **6/18** |

The honest chooser — the one allowed to see all 70 arms — picks a **shuffled key on all 6 of 6
panel × rung cells under every construction**, exactly as lane B found on CANDq. Under CONSTn-dg
it picks `SHUFF#40@S0.40` on U56 and beats do-nothing by **+0.175**, which is the clearest possible
statement that this surface is noise: the biggest walk-forward win in the whole run belongs to a
key drawn from a uniform distribution. Mean REGRET is **0.084–0.138**, against idea 229's pooled
0.0387 [0.021, 0.058].

OOS at 10 bps, honest chooser vs do-nothing vs SPY:

| panel | construction | pick | do-nothing (S0) | SPY |
|---|---|---|---|---|
| U56 | CONSTn-dg | 13.03% / **1.288** / −15.85% | 11.34% / 1.113 / −15.87% | 15.45% / 0.882 / −33.72% |
| B136 | CONSTn-dg | 11.30% / 1.091 / −16.97% | 10.59% / 1.019 / −17.69% | 15.45% / 0.882 / −33.72% |
| SMALL439 | CONSTn-dg | 2.44% / 0.244 / −38.17% | 3.11% / 0.288 / −40.22% | 15.45% / 0.882 / −33.72% |

(Live references at 10 bps, full sample: RULES v2 8.66% / 1.206 / −12.05% on U56, 8.03% / 1.106 /
−12.24% on B136, 3.81% / 0.572 / −14.68% on SMALL439.)

## KEEP paths (both, all 26,460 points)

* **4a vs the live RULES v2: 0 of 26,460.** Every point fails on drawdown — the live book's
  −12% MaxDD is out of reach for a 75%-gross equity book. **R4 confirmed.**
* **4b vs SPY: 4,133 of 26,460**, and **0 of 8,820 on SMALL439** (**R5 confirmed** — idea 136's
  17th reproduction). The binding bar is CAGR (21,977 failing points), then H2, H1, OOS, MaxDD.
* The pass is not the key. 4b pass rate at the protocol rung:

| construction | COMP | MOM | R6 | R3 | LOWVOL | **SHUFF** |
|---|---|---|---|---|---|---|
| CANDq | 38.9% | 27.8% | 44.4% | 5.6% | 5.6% | **24.8%** |
| CONSTn-dg | 38.9% | 33.3% | 33.3% | 22.2% | 0.0% | **8.7%** |
| CONSTn-rw | 66.7% | 61.1% | 55.6% | 33.3% | 0.0% | **26.0%** |

A key drawn from a uniform distribution clears 4b between 8.7% and 26.0% of the time, and `R6`
or `R3` clears it less often than the null does under CANDq. Per idea 144 that is a property of
the EWall-shaped book all 70 arms share, not of any ranking. The best deterministic cell,
U56 CONSTn-dg COMP/TOP S = 0.85, is 11.11% / 1.122 / −16.27% (halves 1.067/1.175, OOS 12.93% /
1.250 / −16.27%) — a 4b pass whose own do-nothing control also passes and whose IS chooser prefers
a shuffled key. **Not proposable.**

## What the record should now say

* Idea 227's finding **generalises**: *a composite ranking is a veto, not a selector* is a
  property of the ranking and holds under a floating count, a constant count at equal cash, and a
  constant count at rebuilt gross. Idea 155's "the argmax moves under a constant count" is true of
  the **level** and irrelevant to the **content** — the move is de-grossing, and it is fully
  available to a random key.
* **Idea 227 lane B's B136 q = 0.95 cell should be withdrawn as evidence.** It was the record's
  only sub-5% trim cell on a large-cap panel; it does not survive the count rule. The KILL of
  idea 155's trim now rests on 6 cells of which 0, not 1, clear 5% on a large-cap panel.
* The composite-clears-the-null result on SMALL439 is construction-invariant and is the one thing
  in this family worth a follow-up — under a survivorship caveat that currently makes it
  unusable.

## Limits

* Survivorship: `universe_broad.json` and the small panel are **current constituents**,
  one-directional. Every SMALL439 number above, including the only null-clearing cells, inherits
  it in full.
* The near-shared control (gate [c]): the S = 1.00 arm differs across keys by ≤ 4.0e-04 Sharpe.
  Declared, quantified, and two orders of magnitude below every read.
* One gate (200d MA + vol20 < 0.60), one gross level (75%), one cadence (weekly). The count rule
  is the only construction axis varied.
* Sharpe differences on overlapping samples; significance is claimed only from the 60-seed null,
  and only cell by cell — no multiplicity correction is applied across the 75 cells per
  construction, which is why the 12–13% sub-5% rate is quoted against the 5% a null surface
  would give rather than treated as a discovery.
