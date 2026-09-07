# Idea 106 — is-DBC-a-drag-or-a-contango-artefact (cloud, 2026-09-07)

**SPLIT.** The queue's *premise* is **falsified** — 2009-2013 is not DBC's dead era, it is
DBC's **best** era. The queue's *mechanism* is **confirmed** — the deletion gain is heavily
era-concentrated, and the chooser's DBC decision flips in **24 of 24** cells when the era is
withheld. On the queue's *conclusion* this run was **corrected by an independent lane-B run of
the same idea on the same day**: the prune survives out of sample only under the `natural`
convention, and **loses 0/16 at g=1.00, which is the convention idea 104's arm is written in**
— so **idea 104's arm IS mis-specified**, as the queue suspected. See §5. One 4a candidate is
**PARKED with a memo recommending against adoption** (`_MEMO.md`).

Script: `2026-09-07_is-DBC-a-drag-or-a-contango-artefact_cloud.py`
(+ `.console.txt`, `.grid.csv` 720 rows, `.attribution.csv`, `.deletion_by_era.csv`,
`.keeppaths.csv`, `.walkforward.csv`)

---

## 0. Gates — both pass before any new claim

| gate | result |
|---|---|
| cost linearity (derive every rung from one 0-bps run) | max abs err **0.000e+00** vs a direct 10-bps run |
| idea 102's committed `.deletion.csv`, 40 matched rows at f=0.50 / 10 bps | max abs err **CAGR 9.7e-17, Sharpe 2.2e-16, MaxDD 9.7e-17** |

Idea 102's published levels are confirmed: mean `dSharpe` across the 8 cells is **+0.163**
for `noDBC` against **+0.122** for `S4`. The *deletion gain* is their difference,
**+0.0405** — the number this run is about.

## 1. THE PREMISE IS WRONG — 2009-2013 is DBC's *best* era, not its dead one

DBC's contribution to the S4 sleeve's return, `sum_t w_DBC,t * r_DBC,t`, by calendar year
(u56; broad is identical to 0.01 pp):

| era | DBC contribution | raw DBC buy-and-hold CAGR |
|---|---|---|
| 2009-2013 (the queue's "severe contango era") | **+1.66 pp** | **+4.69%/yr** |
| 2014-2020 | **+0.27 pp** | **-7.27%/yr** |
| 2021-2026 | **+8.45 pp** | +17.54%/yr |
| **full sample** | **+10.38 pp** | +3.54% |

The **+10.4 pp total and its 2021/2022/2026 concentration reproduce exactly** (+4.47 / +2.28
/ +4.63). The "dead years are 2009-2013" half of the premise does not: those five years are
net **positive**, on both the contribution and the raw price. The genuinely dead stretch is
**2014-2020** — after the contango era the queue names.

Mechanism note: **DBC's mean weight inside the sleeve is 0.0903, against the 0.2500 an equal
share would give.** The trend vote already holds DBC out roughly two-thirds of the time,
which is why deleting it moves so little.

## 2. THE MECHANISM IS RIGHT — the gain *is* era-concentrated

Deletion gain = Sharpe(arm) − Sharpe(S4), at f=0.50 / 10 bps, over the 8 (universe × book ×
convention) cells:

| era | mean gain | cells helped |
|---|---|---|
| FULL sample | **+0.0405** | **8/8** |
| CONTANGO (→2013) | **+0.0935** | **8/8** |
| POST (2014→) | +0.0192 | 6/8 |
| **EXCISED (2009-2013 days deleted)** | **+0.0192** | **6/8** |
| 2014-2020 | +0.0494 | 8/8 |
| **2021-2026** | **-0.0147** | **3/8** |

Excising the contango era cuts the mean gain by **53%** and the count from 8/8 to 6/8; the
gain in the contango era is **4.9x** the gain after it. And in 2021-2026 the sign **reverses**
— DBC does earn its keep in the commodity boom, exactly as the queue suspected.

Sibling controls show this is not a universal era effect, but it is not unique to DBC either:

| arm | FULL | CONTANGO | POST | 2021-2026 |
|---|---|---|---|---|
| **noDBC** | +0.0405 (8/8) | **+0.0935 (8/8)** | +0.0192 (6/8) | **-0.0147 (3/8)** |
| noTLT | -0.0132 (1/8) | -0.0672 (0/8) | +0.0110 (8/8) | **+0.1391 (8/8)** |
| noGLD | -0.0737 (0/8) | -0.1146 (0/8) | -0.0580 (0/8) | -0.0938 (0/8) |
| noUUP | -0.0662 (0/8) | -0.0050 (3/8) | -0.0907 (0/8) | -0.1758 (0/8) |
| DBConly | -0.2733 (0/8) | -0.3946 (0/8) | -0.2228 (0/8) | -0.1123 (1/8) |

**Open flag for the record:** `noTLT` has a *stronger* era reversal than `noDBC`, in the
opposite direction — TLT's deletion gain is negative in the contango era and **+0.1391 (8/8 cells)** in
2021-2026. Idea 104's arm S3 = (TLT, GLD, UUP) therefore **keeps the asset whose deletion is
becoming more attractive and drops the one whose deletion is becoming less so.** On the most
recent era alone the arm is backwards. That is a queue item, not a conclusion of this run.

## 3. THE CHOOSER'S DECISION IS ERA-SELECTED — 24/24 flip

Rule 8 run twice: `IS_full` = PROTOCOL's 2009-2016; `IS_post` = 2014-2016, contango withheld.
OOS 2017-2026 read once.

| IS window | bps | picks holding DBC | OOS Sharpe | Δ vs S4 | beats S4 | beats ctrl | beats v2 | beats SPY | 4b |
|---|---|---|---|---|---|---|---|---|---|
| IS_full | 10 | **0/8** (picks `noDBC@f=0.50` 8/8) | **1.2035** | +0.0066 | 4/8 | **8/8** | 4/8 | **8/8** | 2/8 |
| IS_post | 10 | **8/8** (picks `noGLD@f=0.75` 8/8) | 0.9742 | -0.2407 | 0/8 | 1/8 | 0/8 | 8/8 | 0/8 |
| IS_full | 25 | 0/8 | 1.0252 | +0.0243 | 5/8 | 7/8 | 0/8 | 7/8 | 0/8 |
| IS_post | 25 | 8/8 | 0.7554 | -0.2714 | 0/8 | 0/8 | 0/8 | 0/8 | 0/8 |

**The DBC decision flips in 24 of 24 cells** (all 8 books × 3 cost rungs). The prune is an
era-selected decision, and the queue was right to suspect it.

**The era-selected decision looks like the winner on the pooled figure — and that figure is
misleading.** The `IS_full` chooser beats the no-sleeve control 8/8 and SPY 8/8 at 10 bps and
appears a wash against S4 (+0.0066, 4/8) at lower turnover (-0.0966x/yr). But **the 4/8 is not
noise, it is a clean convention split** (§5): 4/4 positive under `natural`, 4/4 negative under
`g1.00`.

**Honest confound, stated:** `IS_post` is a **3-year** IS window against `IS_full`'s 8. Some
of its degradation is window length, not era content — it does not merely re-add DBC, it
switches arm entirely (to `noGLD`). This run therefore establishes that the DBC decision is
era-dependent; it does **not** establish that the contango era is the *reason* the `IS_full`
pick wins.

**Conclusion on the queue's question — see §5, which corrects an earlier reading of this run.**
The prune is what rule 8 picks under PROTOCOL's own window in 8/8 cells, and it does reduce
turnover, but its out-of-sample value is entirely convention-dependent and is **negative in the
convention idea 104 uses**. The `noTLT` flag in §2 is a further, separate problem with that arm.

## 4. KEEP paths (all 720 points reported, none selected on)

**4b: 113/720 raw, 83/600 distinct** — by rung 69 / 40 / 4 at 0 / 10 / 25 bps.
**4a vs RULES v2: 17/720**, of which **2 at PROTOCOL's 10-bps rung — both `noDBC`.**

Best 4b at 10 bps: `u56 noDBC top20 g1.00 f=0.50` — 11.55% / 1.1673 / −13.29%, H1 1.1694 /
H2 1.1669, OOS 1.2150, 12.42x/yr. Its S4 sibling also passes (1.1491), so 4b does not
discriminate the prune.

**The 4a passes do.** See `_MEMO.md`. Both are `noDBC` at f=0.50 natural on the **broad**
panel, and both are what rule 8's `IS_full` chooser selects.

## 5. CROSS-VALIDATION AND CORRECTION — independent lane-B run, same day

Lane B (`2026-09-07_is-DBC-a-drag-or-a-contango-artefact_B.py`) ran this idea concurrently
from a separately written script. The two runs agree on every shared number, several to four
decimals:

| quantity | this run | lane B |
|---|---|---|
| DBC's 2009-2013 contribution | +1.66 pp | +1.66 pp |
| rule-8 pick, PROTOCOL window | `noDBC@f=0.50`, 8/8 | `noDBC@f=0.50`, 8/8 |
| OOS gap noDBC−S4 at each arm's IS-best f | +0.0066, 4/8 | +0.0066, 4/8 |
| 4a vs RULES v2 at 10 bps | 2, both noDBC, broad+natural | 2, both noDBC, broad+natural |
| OOS gap by convention, all (panel × book × f) at 10 bps | **+0.0135 (12/16) natural, -0.1052 (0/16) g1.00** | **+0.0135 (12/16), -0.1052 (0/16)** |

**Lane B split the OOS gap by gross convention and this run did not — and that split reverses
the conclusion.** The pooled +0.0066 (4/8) is not a wash around zero; it is 4/4 positive under
`natural` and 4/4 negative under `g1.00`. Idea 101/104's candidate is written **at g=1.00**, and
in that convention the prune is behind on OOS Sharpe in **16 of 16** matched cells
(mean -0.1052) and in **4 of 4** of the rule-8 picks. Idea 102's turnover claim survives
(-0.0966x/yr here, -0.196x/yr on lane B's wider cell set), worth roughly 0.02 of Sharpe and
swamped by the -0.105 OOS cost.

**Withdrawn: the statement, in an earlier reading of this run, that "idea 104's arm needs no
re-specification."** The verified position is lane B's: **at the convention it is written in,
idea 104's arm is mis-specified.** What this run adds beyond lane B is the 24/24 era-flip of
the chooser's decision (§3), DBC's 0.0903 realised weight inside the sleeve (§1), and the
`noTLT` flag (§2).

## Caveats

* **Survivorship**: both panels are current constituents (equity levels biased up). The four
  sleeve ETFs are alive throughout, so arm-vs-arm differences are unaffected; the *book* they
  blend into is not, and every headline here is a difference between arms sharing that book.
* **We cannot measure roll yield offline.** "Contango" here is the queue's pre-registered
  calendar era (→2013), not a measured futures-curve state. What is tested is the sub-period
  claim, which is what the queue asked for.
* The excision splices daily net returns and is exact for the Sharpe and CAGR of the spliced
  series. It is not a tradable path and is used only as a sub-period statistic.
