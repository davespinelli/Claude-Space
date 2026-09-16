# Idea 975 (cloud lane, 2026-09-16) — price the QUARTERLY TRANCHE against a GROSS-MATCHED ROTATING NULL

**ANSWERED = THE TRANCHE'S OWN 4b BASE RATE IS 0.000 OF 200 DRAWS, AT Q AND AT M.**
964's only rule-8 4b pass in 54 picks is **not** what a coin flip does at this cadence. But the
whole of its advantage sits on ONE leg, and two KILLs come with the answer: **KILL for "the
tranche is a better book"** — a matched coin flip earns MORE than it (median OOS CAGR 13.53% vs
12.29%, OOS Sharpe percentile **0.06**) — and **KILL for "the tranche gain is a property of the
construction"**, since the same gain is **negative at M** (−0.0445) while the null's is positive.
**Verdict: PARK, not KEEP.** OOS 4a is **0 of 402** (subject 0 of 2, null 0 of 400).

Gates **10 of 11**. G3a fails and is reported, not tuned away — see §0.

## 0. The one failed gate, stated

G3a rebuilds the subject on **964's own last trading day (2026-09-14)** and compares it to 964's
committed `fport.csv` row at a 1e-09 bar. It reads **1.727e-04** and FAILS. Per-column: every
return metric agrees to **≤ 3.03e-05** (OOS Sharpe 3.03e-05, H2 2.58e-05, OOS CAGR 2.36e-06,
MaxDD 3.21e-08) and **`turn_per_yr` alone carries 1.727e-04**. The construction is identical line
for line — same book function, same `Ctx`, same LAG-1 shift, same mean-of-net-returns tranche —
and `pass4b_share` reproduces 964 **exactly** (G3b, 0.000e+00) as does the published DD margin
(G3c, 5.8e-05 pp). The residual is a **restatement of `data/prices.csv` between 964's run and
this one**, not a disagreement about method. On the live panel, which now runs one trading day
longer than 964's, the same residual is 1.28e-03. Nothing below depends on the fourth decimal
place of turnover; the bar stayed at 1e-09 and the gate is scored on it.

## 1. The null, and what it is matched on

`RANDROT_W`: at every decision close of every phase it counts how many names `EWELIG` would hold
(k_t, the eligible count) and holds **k_t names drawn uniformly at random from the tradable set**
at the same gross/k_t, then tranches over all P phases by 964's own rule. Gross, book width,
rebalance schedule, cadence and the phase family are preserved **exactly** (G5, max|d| 1.11e-16);
the only thing destroyed is **which names**. G6 proves the match is tight in the strongest
available way: a `RANDROT` that draws its k_t names from the *eligible* pool instead reproduces
`EWELIG` **bit for bit** (max|d| 1.39e-17).

## 2. The base rate — the queue's literal question

| cadence | draws | tranche OOS 4b rate | 4a | median OOS Sharpe | median OOS CAGR | median OOS MaxDD | median DD margin | DD leg pass rate |
|---|---|---|---|---|---|---|---|---|
| Q | 25 / 50 / 100 / **200** | 0.000 / 0.000 / 0.000 / **0.000** | 0.000 | 1.1321 | 0.1353 | −0.2187 | **−1.6395 pp** | **0.000** |
| M | 25 / 50 / 100 / **200** | 0.000 / 0.000 / 0.000 / **0.000** | 0.000 | 1.0909 | 0.1306 | −0.2202 | −1.7934 pp | 0.000 |
| **SUBJECT Q** | — | **PASS** | False | 1.1201 | 0.1229 | **−0.2014** | **+0.0879 pp** | pass |
| **SUBJECT M** | — | **PASS** | False | 1.1707 | 0.1235 | −0.1763 | +2.5954 pp | pass |

**H_BASE PASS** at 0.000 against a 0.25 bar, converged (**H_CONV** |200 − 100| = 0.000) and the
same at both cadences (**H_CAD PASS**). The null family's per-phase 4b rate is **140 of 12,600 =
0.0111** against the subject family's **26 of 63 = 0.4127** (**H_FAMILY PASS**).

## 3. …but the subject wins on exactly one leg, and loses on the others

`L4_DD` is the **only** failed leg on **200 of 200** draws at Q and at M (`only_DD` = 1.0000);
`L1_H1`, `L2_H2`, `L3_OOS` and `L5_CAGR` fail on **0.0000** of draws. Percentiles of the subject
inside its own null at Q:

| statistic | percentile |
|---|---|
| OOS MaxDD | **1.000** |
| OOS DD margin | **1.000** |
| family 4b share | **1.000** |
| OOS Sharpe | **0.060** |
| full-sample Sharpe | **0.000** |
| OOS CAGR | **0.000** |

**H_DD PASS (1.000). H_SUBJ FAIL (0.060). H_CAGR FAIL (0.000).** A random basket of the same
width, gross and cadence out-earns the eligibility gate and pays for it entirely in drawdown.
The gate is a **drawdown instrument, not a return instrument**, and 4b at this cadence is
decided on the leg it moves — the same conclusion idea 981 reached from the other direction, now
arrived at from the null side.

## 4. The knife edge is real and it is small

The subject's Q DD margin is **+0.0879 pp** inside a cap of 20.2304%. That is **1.73 pp better
than the null's median (−1.6395 pp)** and **0.09 pp from failing**. Both readings are true and
neither should be published without the other. At M the same book clears by **+2.5954 pp** with a
family share of 0.8095 — the monthly tranche is the comfortable pass and the quarterly one, which
964 published, is the marginal one.

## 5. Who owns the tranche gain — nobody, consistently

At Q the subject's (tranched − canonical) OOS Sharpe gain is **+0.0873** against the null's median
**+0.0103** (**H_FREE PASS**, gap 0.077 ≥ 0.05): at Q the tranche buys the subject something the
coin flip does not get, and it is what flips its canonical (which fails on `L4_DD`) into a pass.
At **M the subject's tranche gain is −0.0445** while the null's is **+0.0187** — tranching *hurts*
the subject and *helps* the coin flip. Measured against the family mean rather than the canonical
the two are indistinguishable at both cadences (subject +0.0284 / +0.0224, null +0.0261 / +0.0277).
**The tranche gain is a cadence-specific accident, not a property of the construction or of the
book.**

## 6. Appendix, no selection made: rotation is what kills the null

`RANDFIX` — one **fixed** random list of the median width (40 names), held unconditionally through
no gate, tranched the same way — certifies **0.16 (Q) / 0.12 (M)** of 25 draws, against `RANDROT`'s
**0.000**. Randomising *which names* is survivable; **rotating them at the subject's own turnover
is not**. Reported, never selected on.

## 7. Rule 8 walk-forward — both KEEP paths

The subject is 964's IS-chosen pick (book × gross chosen on 2009–2016 alone); the OOS window
2017–2026 is read once here, and the null inherits the same IS-only construction (G8: the draws
are a function of seed, cadence, draw and phase and the eligibility/tradability masks only).

| who | cadence | CAGR | Sharpe | MaxDD | H1 | H2 | OOS CAGR | OOS Sharpe | OOS MaxDD | 4b | 4a |
|---|---|---|---|---|---|---|---|---|---|---|---|
| SUBJECT tranche | Q | 11.59% | 1.1067 | −20.14% | 1.2030 | 1.0333 | 12.29% | 1.1201 | −20.14% | **True** | False |
| SUBJECT canonical (phase 0) | Q | 11.55% | 1.0751 | −22.21% | 1.2280 | 0.9518 | 11.52% | 1.0328 | −22.21% | False (`L4_DD`) | False |
| NULL tranche (median of 200) | Q | 13.11% | 1.1247 | −21.87% | 1.1989 | 1.0643 | 13.53% | 1.1321 | −21.87% | 0.000 | 0.000 |
| SUBJECT tranche | M | 11.31% | 1.1108 | −17.63% | 1.1434 | 1.0870 | 12.35% | 1.1707 | −17.63% | **True** | False |
| SUBJECT canonical (phase 0) | M | 11.78% | 1.1382 | −17.01% | 1.1464 | 1.1349 | 12.97% | 1.2152 | −17.01% | True | False |
| NULL tranche (median of 200) | M | 12.55% | 1.0782 | −22.02% | 1.1483 | 1.0213 | 13.06% | 1.0909 | −22.02% | 0.000 | 0.000 |
| SPY buy-and-hold | — | 15.10% | 0.8830 | −33.72% | 0.9591 | 0.8208 | 15.21% | 0.8713 | −33.72% | — | — |
| RULES v2 baseline (live) | W | 8.62% | 1.2009 | −12.05% | 1.2325 | 1.1762 | — | — | — | — | — |

* **KEEP path 4b:** subject 2 of 2 cadences; null **0 of 400** draws.
* **KEEP path 4a:** **0 of 402** — subject 0 of 2, null 0 of 400. The live book's Sharpe 1.2009
  and MaxDD −12.05% are out of reach for the tranche on both statistics at both cadences.
  **H_4A FAIL.**

## Verdict

**PARK.** The pass survives the coin flip the queue asked for — decisively, 0 of 200 — and that
is worth recording. It is not promoted: it wins on one leg, by 0.09 pp, while losing to a random
basket on both return statistics; its tranche gain reverses sign between the two cadences; and it
clears no 4a anywhere in 402 books. `2026-09-16_tranched-EWELIG-candidate_cloud.memo.md` carries
the exact RULES wording so the candidate is on file in tradable form, together with this lane's
recommendation **not** to promote it.

## Survivorship (rule 9)

U56 is a CURRENT-CONSTITUENT list, so every CAGR and drawdown LEVEL above is optimistic and both
4b readings — subject and null — are UPPER bounds. The measured object is a **percentile of the
subject inside a null drawn from the SAME panel on the SAME tape**, so the bias is carried by both
sides and very largely cancels. What does not cancel runs against this run's favourable finding:
a uniformly-drawn null on a survivorship-clean panel would be weaker, which makes the 0.000 base
rate a **conservative** reading of how hard 4b is to reach by chance, and the subject's 0.060 OOS
Sharpe percentile a **generous** one. `RULES.md`, `PROTOCOL.md`, `scan.py`, `bot.py` and
`baseline.py` are untouched.
