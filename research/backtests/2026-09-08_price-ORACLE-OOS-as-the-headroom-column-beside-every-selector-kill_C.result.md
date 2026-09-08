# Idea 436 — ORACLE-OOS as the headroom column beside every selector kill (lane C, 2026-09-08)

**Verdict: ANSWERED / SPLIT. The column is ADOPTED report-only in its NET form and KILLED as a
screen; the queue's count question is answered, and its premise needs one correction.**

Script `2026-09-08_price-ORACLE-OOS-as-the-headroom-column-beside-every-selector-kill_C.py`;
console, `.census.csv`, `.kills.csv`, `.cells.csv`, `.arms.csv`, `.walkforward.csv`,
`.keeppaths.csv` alongside. Rules unchanged, PROTOCOL untouched, no memo (no KEEP candidate).

## The statistic, and the two things the queue did not notice

For a pool `P` of arms with OOS metric `M(a)` and do-nothing control `c`:

    H_ctl  := max_P M(a) - M(c)        H_mean := max_P M(a) - mean_P M

Any selector obeys `M(R) - M(c) <= H_ctl`, so `H = 0` **proves** a kill was unfalsifiable. The
queue's instinct is right. But:

1. **H is a MAXIMUM, so it is upward-biased.** Even when every arm has the same true Sharpe,
   max-minus-mean is strictly positive in finite samples. "ORACLE-OOS +0.0286" reports that a
   max was taken, not that anything was there. The certificate is **net** headroom: H minus the
   H that noise alone produces in the same pool.
2. **H is not available at decision time.** It is computed on the window the rule may not see.

## [e] Reproduction — the queue's premise, off the record's own files

| claim | ORACLE-OOS | S0 | gap | published | \|d\| |
|---|---|---|---|---|---|
| idea 216 (flip-rate, cloud) | 0.805157 | 0.776605 | **+0.028552** | +0.0286 | 4.75e-05 |
| idea 203 (turnover-matched null, lane B) | 0.810226 | 0.776605 | **+0.033622** | +0.0336 | 2.17e-05 |

Both quoted numbers reproduce exactly. Gates G1 (fast vs `engine.backtest`) ≤ 1.04e-17 and G5
(cost-rung turnover identity) 0.000e+00 on all three panels.

## C1 — the back-fill (1,664 committed CSVs, this run's own output excluded)

Tiers: **910** carry no OOS Sharpe column at all, **27** publish an oracle column (T1), **567**
are pool-reconstructable (T2), **160** carry an OOS Sharpe that cannot be pooled (T3).
**50,404 pools** across 594 files.

**The reconstruction gate does NOT pass, and its direction is the finding.** Against the 27
files that publish an oracle column: exact in 26.2% of 321 cells, median |d| 3.69e-02, max 1.55.
Signed, per file: recon **below** published in 17, equal in 5, **above** in 5. A committed
walk-forward file usually holds only the PICKS, not the arm ladder, so a row-max under-states
the true oracle; where it over-states, the reconstruction pooled over a reported axis. **Net
bias is downward — the census finds LESS headroom than the record really had, which cuts
AGAINST the "no headroom" reading, not for it.** T2 numbers are therefore reported as bounds.

| threshold | recon `H_mean` | recon `H_ctl` (n 3,428) | published-exact `H_ctl` (n 1,362) |
|---|---|---|---|
| ≤ 0.00 | 4.2% | 2.8% | **33.3%** |
| ≤ 0.02 | 21.2% | 3.5% | 44.4% |
| ≤ 0.05 | 34.7% | 4.3% | 54.1% |
| ≤ 0.10 | 50.3% | 4.8% | 63.3% |
| ≤ 0.20 | 72.3% | 5.6% | 76.4% |

Read the last column: on the 1,362 rows where a script published BOTH an oracle and a control,
**one third have the control already at or above the ladder's OOS best** — those selector
verdicts were bounded at zero before any selector ran.

## C2 — the count the queue asks for

**"12 selector kills" is an ORDINAL, not a set (P5 confirmed).** The LEADERBOARD carries **60
kill-claim rows over 56 distinct scripts**, and **166 ordinal-streak mentions over 146 rows**
("third" x62, "second" x53, "thirteenth" x6, "twelfth" x5, "fourteenth" x4 …): the record runs
several parallel counters (gate kills, do-nothing wins, 4b reproductions) and no single "12th"
enumerates a corpus.

Of the 60 kill rows:

* **53** have pool-mean-convention headroom recoverable; **7 cannot be re-read at all**.
* **only 22** have a control-convention headroom — the quantity a kill is actually bounded by —
  and only **4** of those come from the script's own published oracle column.
* **10 of 22 (45%) sit at a ladder-median `H_ctl` ≤ 0**: in the typical cell of those ladders
  the do-nothing control was already the OOS best, so no selector could have won. **1 of 22 has
  `max H_ctl ≤ 0` — unfalsifiable outright.** 14 of 22 (64%) are ≤ 0.05.
* On the weaker pool-mean bound: 23 of 53 (43%) are ≤ 0.10, 12 of 53 (23%) ≤ 0.05 — **P2 was
  predicted at "over half" and MISSED at this level.**

The lowest kill ladders: `is-the-priceability-floor-the-real-selector_B` (median −0.2883),
`price-the-post-crash-re-entry-lag_cloud` (−0.0103, max −0.0027, unfalsifiable),
`shallow-window-prices-are-not-prices_C` (−0.0071), then five ladders at exactly 0.0000.

## L1 — the live ladders, where headroom can be given a null (63 pools, 369 arm-rows)

3 panels × 7 dial families × 3 cost rungs. Noise floor = paired circular-block bootstrap
(500 draws) after shifting every arm to the pool's mean Sharpe, preserving each arm's vol,
higher moments and the pool's cross-arm correlation.

| convention | H_OOS mean | noise floor H0 | NET | pools net>0 | clear p<0.05 |
|---|---|---|---|---|---|
| pool-mean | 0.0974 | 0.0931 | **+0.0043 (t +0.52)** | 25/63 | **3/63** |
| control | 0.0524 | 0.0943 | **−0.0419 (t −4.48)** | 14/63 | **0/63** |

**P1 confirmed:** raw headroom is positive nearly everywhere and vanishes against its own noise
floor. Block length is immaterial (H0 0.0957 / 0.0931 / 0.0912 at L = 5 / 21 / 63; 3 pools clear
at every L).

**The floor is not a constant — it spans 0.0011 to 0.1842 (a 168x range) at the same pool size
and window**, driven by how *different* the arms are: GROSS (seven near-identical gross scalars)
has H0 0.0014, GATE/WIDTH 0.11–0.13. Per family at 10 bps:

| family | H_IS | H_OOS | H0 | net | p | selector gain |
|---|---|---|---|---|---|---|
| GROSS | 0.0015 | 0.0011 | 0.0014 | −0.0003 | 0.547 | −0.0009 |
| CADENCE | 0.0604 | 0.0748 | 0.0792 | −0.0044 | 0.438 | +0.0002 |
| VOLCAP | 0.0661 | 0.1767 | 0.0960 | **+0.0807** | 0.252 | +0.0605 |
| GATE | 0.1008 | 0.0885 | 0.1100 | −0.0215 | 0.613 | −0.0251 |
| WIDTH | 0.1159 | 0.1220 | 0.1338 | −0.0118 | 0.467 | −0.1217 |
| MALEN | 0.1234 | 0.1036 | 0.1066 | −0.0030 | 0.437 | −0.0629 |
| LOOKBACK | 0.1900 | 0.0809 | 0.1258 | −0.0449 | 0.722 | −0.0095 |

## L2 — is the column available at decision time?

`corr(H_IS, H_OOS)` **+0.2574** (Spearman **+0.4842**) on the pool-mean convention, +0.3214 /
+0.5092 on the control convention. **P3 (|corr| < 0.3) is MISSED in rank terms**: the IS twin
does carry real *ordering* information about which ladders will be wide, even though the level
does not transfer. What it does not carry is the thing a selector needs: `corr(H_IS, selector
gain)` is **−0.0072**, and selector gain is negative in every IS-headroom tercile
(low −0.0094, mid −0.0330, high −0.0193). Over all 63 pools the IS-argmax gains **−0.0206
(t −1.43), 22W/37L, sign p 0.0674**.

## L3 — rule 8 (τ on the inner IS split, 2017-2026 read once)

`R(τ, s)`: take the IS-argmax where IS headroom under statistic `s` exceeds τ, else the control.
Chosen on IS only: **s\* = mean, τ\* = 0.0416** (inner-IS gain +0.0404, 50 of 63 pools gated on).

| arm | OOS Sharpe | vs do-nothing |
|---|---|---|
| S0 do-nothing (always the control) | **0.9616** | — |
| S1 always the IS-argmax | 0.9410 | −0.0206 (t −1.43, 22W/37L) |
| **R(τ\*, s\*) headroom-gated** | **0.9424** | **−0.0192 (t −1.37, 20W/24L)** |
| ORACLE-OOS (perfect hindsight) | 1.0140 | +0.0524 |
| best single τ on the OOS grid (not selectable) | — | +0.0035 |

All 21 τ grid points are printed in `.walkforward.csv`; the best of them buys +0.0035, and the
honestly-chosen one loses. Comparands: RULES v2 OOS 0.9848, RULES v1 OOS 0.5938, **SPY OOS
0.8820 (CAGR 15.45%, MaxDD −33.72%)**. Pick book OOS 10.63% CAGR / −19.37% MaxDD vs do-nothing
8.04% / −14.30%. **P4 confirmed — gating a selector by headroom does not rescue it.**

## L4 — both KEEP paths

* Arms (369 rows): **4a 13, 4b full 38, 4b OOS 41, BOTH 0.** 4b binding bars CAGR 154, H2 76,
  H1 70, DD 31. 4a by family WIDTH 5 / GROSS 2 / CADENCE 2 / GATE 2 / VOLCAP 2; 4b by panel
  u56 26 / broad 12 / small **0** (idea 136's shape again; no ordinal is quoted, for the reason C2 gives).
* Rule-selected books (126 rows): 4a 10, 4b 16, 4b OOS 15, **BOTH 0** (CTL 8/3/3, PICK_IS 2/13/12).

No promotion, no memo.

## Predictions: 3 hit, 1 partial, 1 missed

P1 hit · P2 **missed** (43%, not "over half") · P3 **missed in rank terms** (Spearman +0.48;
hit on the level) · P4 hit · P5 hit.

## Recommendation (report-only; PROTOCOL, RULES.md, scan.py, bot.py, baseline.py untouched)

1. **Publish ORACLE-OOS, never raw.** Wording: `ORACLE-OOS +X (noise floor +Y, net +Z, p=P over
   B draws)`, with the floor computed on **the ladder's own arms** — never borrowed from another
   run, because the floor spans 168x within this one corpus.
2. **Do not adopt headroom as a screen.** It is not knowable at decision time in the way a
   selector needs, and R(τ\*) is priced above at −0.0192.
3. **Idea 216's "unlike idea 434's family there IS headroom" is UNSUPPORTED rather than wrong**,
   and it is unsupportable from what the record kept: +0.0286 is uninterpretable without a floor,
   and the arm return series needed to compute one were not committed. This run does not
   re-price their ladder and does not claim to.
4. **The enabling change:** a run publishing a selector verdict should commit its arm-level OOS
   rows (arm × metric at minimum). 160 committed files carry an OOS Sharpe that cannot be
   pooled, only 27 publish an oracle column, and 38 of 60 kill rows have no control-convention
   headroom recoverable at all.

## Caveats carried

Survivorship — u56/broad/small are current constituents; every CAGR is flattered and every
statistic here is a within-pool contrast. The census reconstruction is a heuristic (347 files
have an ambiguous arm column; the min/median/max across every admissible split is in
`.census.csv`), and its gate fails downward as described. 63 live pools are not 63 independent
observations. `data/prices.csv` was rewritten 2026-09-07, so older reproductions are quoted per
number. Determinism: seeded RNG, `zlib.crc32` (never Python's salted `hash()`); a full re-run
reproduces every number.
