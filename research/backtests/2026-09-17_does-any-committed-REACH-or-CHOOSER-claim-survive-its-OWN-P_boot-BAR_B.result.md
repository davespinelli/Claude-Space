# Idea 1154 (lane B, 2026-09-17) — does ANY committed REACH or CHOOSER claim survive its OWN P_boot BAR?

**ANSWERED = ALMOST NONE, AND THE FEW THAT DO ARE CERTIFIED BY AN IDENTITY RATHER THAN BY
EVIDENCE.** At the headline rung (`C_STRICT` × `L63`, 1101's own basis) **1 of 12** committed
pick decisions clears the record's own 0.90 / 0.10 bootstrap bar. Over all 72 decisions,
**17 of 72 (0.2361)**. **15 of those 17 are GROSS-ladder decisions, and the GROSS ladder is
EXACTLY monotone in IS Sharpe at 6 of 6 (panel, anchor) cells (Spearman ρ = 1.000000, gate
G10) over an IS-Sharpe spread of only 0.001395 to 0.009050.** Outside GROSS, **2 of 54**
decisions resolve.

**VERDICT: KILL (capital). ANSWERED = NO (the bar does not certify the record's picks, and
cannot).** Gates **10 of 10**.

## The two dials, and no more (protocol rule 4)

| dial | rungs | headline |
|---|---|---|
| CLAIM SET | `C_STRICT` ⊂ `C_PROX` ⊂ `C_ALL` (1197/1199/1155's nesting, gate G5) | `C_STRICT` |
| BLOCK LENGTH | 21, 63, 126, 252 | 63 (1101's own) |

All **12 dial cells published**. PANEL (3), ANCHOR (2, 1101's A and B), LADDER (4) and
CHOOSER (3) are **not** dials — all 72 decisions are scored at every dial cell (288 rows).
Nothing is selected on.

## Arm 0 — data-free, before any tape is read

A 0.90 bar demands **9.00×** the uniform null on the 10-rung GROSS ladder and only **3.60×**
on the 4-rung H and CADENCE ladders. *"Resolved" is not comparable across ladders unless the
rung count travels with it* — idea 1155's count-inflation defect, arriving on PICKS instead
of on SPREADS.

## Arm A — census of 32,979 committed text units

| claim set | units | states a resolution | states a margin | states a rung count |
|---|---|---|---|---|
| `C_STRICT` | 1,455 | 229 (**0.1574**) | 166 (0.1141) | 930 (0.6392) |
| `C_PROX` | 1,661 | 250 (0.1505) | 174 (0.1048) | 1,041 (0.6267) |
| `C_ALL` | 6,414 | 696 (0.1085) | 449 (0.0700) | 3,327 (0.5187) |

**1,455 committed sentences name a pick and adjudicate on it; five in six state no resolution
for that pick at all.**

## Arm B — the 72 decisions

```
claim_set   L   n  resolved   frac  supported  P_pick mean   min   max
 C_STRICT  21  12         0  0.0000         0       0.5037 0.231 0.877
 C_STRICT  63  12         1  0.0833         1       0.5381 0.199 0.941
 C_STRICT 126  12         1  0.0833         1       0.5378 0.198 0.959
 C_STRICT 252  12         3  0.2500         3       0.5730 0.199 0.991
   C_PROX  21  36         5  0.1389         5       0.5651 0.165 1.000
   C_PROX  63  36         8  0.2222         8       0.6000 0.199 1.000
   C_PROX 126  36         8  0.2222         8       0.6268 0.191 1.000
   C_PROX 252  36        11  0.3056        11       0.6606 0.188 1.000
    C_ALL  21  72        14  0.1944        14       0.5814 0.165 1.000
    C_ALL  63  72        17  0.2361        17       0.6126 0.199 1.000
    C_ALL 126  72        18  0.2500        18       0.6400 0.191 1.000
    C_ALL 252  72        22  0.3056        22       0.6703 0.188 1.000
```

**THE UNSTATED DIAL MOVES THE HEADLINE BY 57%.** Resolution rate runs 0.1944 → 0.2361 →
0.2500 → **0.3056** as L goes 21 → 252, monotonically, on the same 72 decisions. 1101
published "11 of 24" and named L = 63 but not why; a run free to pick L is free to pick its
own resolution count.

Per ladder at L = 63 (all 72): **GROSS 15/18 resolved** (P̄ = 0.9597, null 0.1000) ·
**N 2/18** (0.5692, null 0.1111) · **H 0/18** (0.5052, null 0.2500) · **CADENCE 0/18**
(0.4162, null 0.2500).

**CROSS-READ of 1101 (G9 passes: its committed U56 anchor-A reach set {GROSS, CADENCE}
reproduces exactly).** Its own headline 24 reads **4 of 24** resolved here against its
committed **11 of 24** — the difference is the panel construction, not the arithmetic: this
run uses 1161's decision-at-t / apply-at-t+1 frame, which reproduces the record's committed
U56 anchor triple to **1.622e-03** (G2), where 1155's build-on-the-shifted-row convention
misses it by 3.69e-02. 1101's two committed values reproduce closely: U56/A GROSS
**0.7670** vs committed 0.716, U56/A CADENCE **0.2740** vs committed 0.278.

## Arm C — WHY the bar cannot do the job it was asked to do

**P_boot MEASURES ORDER STABILITY, NOT EFFECT SIZE.** argmax of a monotone ladder is an
identity, so the joint bootstrap re-picks the same endpoint on nearly every draw *no matter
how small the difference is*:

- smallest-margin **RESOLVED**: B136/A/GROSS/CH_ISSHARPE, IS margin **3.33e-04** → P_pick
  0.9410 → **CERTIFIED**
- largest-margin **UNRESOLVED**: SMALL/B/H/CH_ISSHARPE, IS margin **2.28e-01** (**685×
  larger**) → P_pick 0.8120 → **REJECTED**

Stated at its true strength, which is *not* "inverted": median IS margin is **9.739e-03**
among the resolved against **9.369e-03** among the unresolved (ratio 1.0395), Spearman
**0.1551** over all 72. The two are **near-orthogonal** — which is worse for the bar than an
inversion would be, because it means the bar carries **no effect-size information at all**.
The hypothesis this arm was written to test — that idea 1120's cheap MARGIN column is a free
substitute for the bootstrap — is **REFUTED, and so is its converse**.

## Arm D — rule 8 walk-forward (the capital arm)

Picks chosen on 2009–2016 **alone**; 2017–2026 read **once**. `R_RAW` = publish the IS argmax
always (the record's habit) · `R_BAR` = publish only if P_pick ≥ 0.90, else stay at the anchor ·
`R_ANCHOR` = never move (1155's do-nothing control).

| claim set | rule | n moved | mean OOS Sharpe | mean OOS MaxDD | 4b full |
|---|---|---|---|---|---|
| `C_STRICT` L63 | R_RAW | 7/12 | 0.8496 | −0.2709 | **2** |
| `C_STRICT` L63 | R_BAR | 0/12 | **0.8750** | −0.2523 | **4** |
| `C_STRICT` L63 | R_ANCHOR | 0/12 | **0.8750** | −0.2523 | **4** |
| `C_ALL` L63 | R_RAW | 59/72 | **0.7996** | −0.2455 | **6** |
| `C_ALL` L63 | R_BAR | 13/72 | 0.7887 | −0.2317 | **19** |
| `C_ALL` L63 | R_ANCHOR | 0/72 | 0.7901 | −0.2363 | **24** |

**THE CAPITAL FINDING IS NOT IN MEAN OOS SHARPE — IT IS IN THE 4b COUNT.** The three rules
sit inside 0.011 of mean OOS Sharpe on `C_ALL`, a distinction worth nothing. But the record's
habit of publishing the IS argmax **destroys three quarters of the capital-worthy books it
walks off: 6 of 72 against the do-nothing control's 24 of 72**, and the resolution bar
recovers most of them (19) purely by refusing to move 59 of 72 times. On `C_STRICT` the
anchor wins outright on every axis. **A bar whose only demonstrated value is that it stops
you moving is not a bar, it is an expensive way to do nothing — and doing nothing is
available for free.** This is idea 1155's "the widest-dial habit loses to doing nothing"
arriving from a second direction, on a different statistic and a different population.

## Arm E — both KEEP paths, all 144 distinct rung books

**4a 0 of 144 · 4b full 20 · 4b OOS 24 · BOTH 19** (U56 14/48, B136 6/48, **SMALL 0 of 48 on
every path**). SMALL leg rates: L_H1 0.021, L_H2 0.000, L_OOS 0.000, L_DD 0.104, L_CAGR 0.021.

**NO NEW CANDIDATE, AND THE PASSER LIST IS THE RECORD'S OWN PRIOR ART.** Five of the U56
passers are one book read at a different gross rung: N=20 / H=126 / W at g = 0.55 → 0.75
spans Sharpe **1.137390 → 1.138079**, a spread of **6.89e-04 over a 1.36× change in gross**;
B136 g = 0.55 → 0.70 spans 1.27e-03. That is idea 1189's degenerate gross ladder arriving
from a fifth direction — and here it is not a side observation but **the mechanism of the
headline result**, since it is exactly that degeneracy which lets the bootstrap certify the
GROSS picks. U56 N=12/H=126/g0.75/W reads full 17.65% / 1.1658 / −20.17%, OOS 18.78% /
1.1701 / −20.17%, ahead of the standing incumbent — **and this run's own machinery says the
U56 N-ladder pick is UNRESOLVED (P_pick 0.4290); preferring it would be selecting on the OOS
window, which rule 8 exists to forbid. RECORDED AND NOT PROMOTED. No memo.**

Benchmarks (this vintage): U56 SPY 15.06% / 0.8814 / −33.72%, OOS 15.15% / 0.8684; U56 live
RULES v2 8.60% / 1.1980 / −12.05%, OOS 9.42% / 1.2714. B136 SPY 15.16% / 0.8861, OOS 0.8767;
B136 live 7.98% / 1.0993. SMALL SPY 14.06% / 0.8581; SMALL live 4.30% / 0.6637.

## PROTOCOL clause PROPOSED NOT ENACTED (rule 6)

> *"no resolution claim without its ladder shape"* — any committed sentence calling a pick,
> reach or argmax RESOLVED, STABLE or SIGNIFICANT under a resampling bar SHALL state (i) the
> rung count k, since the bar's own uniform null is 1/k, (ii) the block length the bar was
> computed at, since the resolution rate on this record's own ladders moves 0.1944 → 0.3056
> across L ∈ {21, 252} with no other change, and (iii) the pick's IS MARGIN beside the
> probability, since the two are near-orthogonal (Spearman 0.1551). **A pick on a ladder
> that is monotone in the chooser's own statistic SHALL NOT be reported as resolved at all:
> there the bar certifies an identity and is silent on the effect.**

## Gates — 10 of 10

G1 fast runner ≡ `engine.backtest` **1.388e-17** · G2 cross-run 1101's committed U56 anchor-A
triple **1.622e-03** (1161's 5e-3 bar; 1163's price-vintage defect carried, not absorbed) ·
G3 live RULES v2 U56 MaxDD −12.0549% vs committed −12.05% **4.949e-05** · G4 SPY OOS triple
**2.894e-03** · G5 claim sets nest **0** · G6 exchangeable ladders' position-mean P_boot ≡
uniform null 1/5 **1.848e-02** against a **derived** 3-SE bar of 0.0849 · G7 degenerate ladder
puts all mass on the first rung **0** (1199's first-wins, re-gated) · G8 bootstrap determinism
**0** · G9 cross-run 1101's U56 anchor-A reach set {GROSS, CADENCE} **0** · G10 GROSS ladder
exactly monotone at 6 of 6 cells **0**.

**THE GATE THAT FAILED FIRST, PRINTED RATHER THAN PATCHED OVER.** G6's first cut read
**5.975e-02** against a hand-set 0.05. That was a **mis-specified bar, not a broken
machinery**: draws inside one exchangeable ladder share that ladder's realisation, so the
effective sample is the LADDER count M, and at M = 40 the position-mean's own SE is 0.063 —
the "failure" sat at 0.95 SE. The bar is now **derived** (3 × √(p(1−p)/M) at p = 1/k) and M
raised to 200 until the gate can discriminate. A gate that cannot reject is not a gate.
**A second defect was caught by G2 before any result was read:** the first cut built
selections on the ALREADY-SHIFTED rebalance rows (1155's convention) and missed the record's
committed anchor triple by 3.69e-02 — decision and application on the same row. Corrected to
1161's decide-at-t / apply-at-t+1 frame, which is what protocol rule 2 requires.

## Survivorship (rule 9)

U56 and B136 are CURRENT-CONSTITUENT lists; SMALL is the current output of a sub-$2B screen
less the documented `max_1d_move >= 1.0` exclusion (52 of 715 dropped; 663 names + SPY as
benchmark only, excluded from SMALL's eligible set). Every LEVEL is optimistic and every
4a/4b count is an UPPER bound. P_boot is a ratio of resampled argmax counts on one panel's
own ladder and is far less exposed, but the levels are published beside it.

## Declared approximation, and its direction (1101's, restated)

P_boot resamples ONE tape, so it measures sampling error around THIS regime and not regime
uncertainty. Every P_boot is therefore **closer to 0 or 1 than the truth**, and "resolved" is
scored in the direction that **favours the record**. A decision this run calls unresolved is
unresolved *a fortiori*.

## Artefacts

Script `2026-09-17_does-any-committed-REACH-or-CHOOSER-claim-survive-its-OWN-P_boot-BAR_B.py`
(87s, standalone, offline, deterministic), 9 CSVs (`datafree`, `census`, `census_units`,
`decisions`, `dialgrid`, `monotonicity`, `blocksens`, `walkforward`, `rule8`, `books`,
`gates`), console log, 4 LEADERBOARD rows.
