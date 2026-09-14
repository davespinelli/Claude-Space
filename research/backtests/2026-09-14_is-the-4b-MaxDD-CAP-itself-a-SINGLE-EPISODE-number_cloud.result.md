# Idea 851 (cloud, 2026-09-14) — is the 4b MaxDD CAP itself a SINGLE-EPISODE number?

**ANSWERED: YES, literally — the cap is a 35-trading-day number, and re-pricing it on a 2020-free leg costs the standing shelf 3 of its 8 candidates and the mechanical grid 13 of its 19 passes. But the three shelf deaths miss by 6, 9 and 37 basis points, so what the run establishes is a BRITTLE BAR, not a 2020-made shelf.** No RULES change, nothing promoted; RULES.md, scan.py, bot.py, baseline.py and PROTOCOL.md untouched.

Script `2026-09-14_is-the-4b-MaxDD-CAP-itself-a-SINGLE-EPISODE-number_cloud.py`; 2,464 rows (44 books × 7 episodes × 2 bar conventions × 2 legs × 2 rungs), all in `.books.csv` / `.spy.csv` / `.shelf.csv` / `.walkforward.csv` / `.console.txt`.

## What is new against idea 835
835 deleted `2020-02-19..2020-04-07` from a 216-arm **mechanical** QROLL corpus and read 4b 141 → 16. It never touched **the shelf** — the books the record has written 4b KEEP-candidate memos for, which is what a Sunday review actually chooses from. This run rebuilds every such memo from its own committed RULES wording, gates it against its published headline, and asks 851's question of those books; and it separates the two things 835's design confounds — **FIXED** bars (the committed cap −20.23% and floor 10.61%: *is the BOOK 2020-made?*) versus **REPRICED** bars (60% / 70% of SPY on the same spliced leg: *is the BAR 2020-made?*).

## Gates (all pass)
Empty splice == unspliced, **max|d| 0.000e+00**. **8 of 8** committed 4b memos rebuild inside the stated tolerance (Sharpe 0.030, MaxDD 1.5 pp): `b136-r620-gross065-W` and `b136-qroll-q012-w1008-d050-g100` reproduce to **0.0000**, K8 to 0.0003, the two band books to 0.005/0.002, `u56-quantile50-respread-M` to 0.009, `u56-marsrespread-gross075` to 0.004, `u56-top20-band-m20` loosest at dSharpe 0.0202 / dMaxDD 1.09 pp (its memo ends 2026-09-04). **One committed 4b memo could NOT be rebuilt and is named, not re-specified:** `2026-09-12_b136-corr-hi-q017-w252-d050-D-g100` — neither natural reading of its tail convention reproduces its headline (best attempt 13.31% / 1.0951 / −17.69% against 14.02% / 1.1538 / −15.11%), so it is excluded from the shelf here. SPY reproduces 15.1631% / 0.8861 / −33.7172%, and **the cap's provenance is now on the page: SPY's committed MaxDD runs 2020-02-19 → 2020-03-23.**

## (a) The bar is one episode, and nothing else touches it
| deleted episode | days cut | SPY CAGR | SPY Sharpe | SPY MaxDD | re-priced cap | re-priced floor |
|---|---|---|---|---|---|---|
| NONE | 0 | 15.16% | 0.8861 | **−33.72%** | −20.23% | 10.61% |
| **COVID_TIGHT (the queue's)** | **35** | 16.84% | 1.0282 | **−24.50%** | **−14.70%** | 11.79% |
| COVID_DD (2020-02-19→08-10, from SPY) | 121 | 15.57% | 0.9701 | −24.50% | −14.70% | 10.90% |
| COVID_WIDE | 104 | 15.77% | 0.9812 | −24.50% | −14.70% | 11.04% |
| DD_2015 | 36 | 15.92% | 0.9268 | **−33.72%** | −20.23% | 11.15% |
| BEAR2022 | 196 | 17.82% | 1.0328 | **−33.72%** | −20.23% | 12.48% |
| PLACEBO_2017 | 34 | 15.26% | 0.8884 | **−33.72%** | −20.23% | 10.68% |

**Deleting 0.79% of the sample moves the cap by 5.53 pp; deleting a bigger, real drawdown (2015, 2022) or a same-shaped placebo block moves it by exactly zero.** That is the literal sense in which PROTOCOL 4b's drawdown cap is a single-episode number. The CAGR floor is a single-episode number too — a *different* episode: cutting BEAR2022 lifts it 10.61% → 12.48% full-sample and 10.73% → **14.32%** OOS.

## (b) What it costs the shelf and the grid (full sample, 10 bps)
| candidate set | NONE | ex-COVID, **FIXED** bars | ex-COVID, **REPRICED** bars |
|---|---|---|---|
| SHELF (8 memo'd books) | 8 / 8 | **8 / 8** | **5 / 8** |
| GRID (36 mechanical books) | 19 / 36 | **24 / 36** | **6 / 36** |

4a is **0 / 8** on the shelf at every episode and convention. The FIXED column is the circularity made visible: deleting the crash *raises* the mechanical grid's pass count 19 → 24, because the committed cap keeps the depth the crash gave SPY while the candidates lose the depth it gave them. Only when the bar is re-priced on the same leg does the count collapse — to 6 of 36 on the grid (consistent with 835's 141 → 16) and 5 of 8 on the shelf. **The shelf is far more robust than the mechanical corpus: 62.5% survive against 835's 11%.** The placebo leaves the shelf at 8 / 8 and the grid at 18 / 19, so none of this is day-count. At 25 bps the shelf reads 7 (NONE) → 3 (ex-COVID, REPRICED).

Book by book at COVID_TIGHT, REPRICED cap −14.70%, floor 11.79%:

| book | MaxDD (no deletion) | MaxDD ex-2020 | CAGR ex | Sharpe ex | 4b FIXED | 4b REPRICED | margin vs cap |
|---|---|---|---|---|---|---|---|
| b136-qroll-q012-w1008-d050-g100 | −17.31% | −15.07% | 15.58% | 1.214 | PASS | **FAIL DDCAP** | **−0.37 pp** |
| u56-k8-qroll-q017-w1008-d100-g100 | −14.79% | −14.79% | 14.96% | 1.287 | PASS | **FAIL DDCAP** | **−0.09 pp** |
| u56-marsrespread-gross075 | −18.65% | −14.76% | 12.32% | 1.211 | PASS | **FAIL DDCAP** | **−0.06 pp** |
| b136-r620-gross065-W | −19.43% | −14.42% | 16.06% | 1.242 | PASS | PASS | +0.28 pp |
| u56-quantile50-respread-M | −19.75% | −14.33% | 16.36% | 1.346 | PASS | PASS | +0.37 pp |
| u56-top20-band-m20 | −18.31% | −13.01% | 13.75% | 1.201 | PASS | PASS | +1.69 pp |
| u56-band008-gross100 | −19.05% | −11.76% | 12.48% | 1.303 | PASS | PASS | +2.93 pp |
| u56-v2band-gross100 | −15.91% | −10.45% | 12.49% | 1.326 | PASS | PASS | +4.25 pp |

**5 of 8 books sit within 1.00 pp of the re-priced cap and 5 within 0.50 pp** — the bar lands in the middle of the shelf's drawdown distribution, and every one of the three failures is decided by basis points. Note K8: its MaxDD is **unchanged** at −14.79% (its worst decline is not the crash), so it fails only because the bar moved under it.

## (c) Rule 8 — the deletion never reaches the chooser, only the bar
The GRID dial is chosen on 2009–2016 IS Sharpe alone (an IS window that contains no 2020) and the OOS window read once per (episode, convention). The pick is **`band0.08-g1.00` on both panels at all 7 episodes** — 1 distinct pick per panel, so nothing here is selection drift. The OOS 4b verdict flips between FIXED and REPRICED in **2 of 14** (episode, panel) cells, and both flips are **BEAR2022 → FAIL CAGRFLOOR** (OOS 14.21% / 13.29% against a floor lifted to 14.32%), not drawdown. Ex-COVID the pick reads OOS 14.07% / 1.4548 / −11.76% (U56) and 13.17% / 1.4055 / −11.17% (B136) and passes 4b under **both** conventions.

## What this argues for (PROPOSAL ONLY — rule 6, Sunday review)
Not a looser cap and not a tighter one: a **second leg**. A 4b verdict should state its drawdown margin and repeat itself on a leg that excludes the benchmark's single deepest episode, because on this evidence the cap's *level* is set by 35 days and half the shelf sits inside 1 pp of it. A candidate that clears on both legs (here: `u56-v2band-gross100`, `u56-band008-gross100`, `u56-top20-band-m20`, `u56-quantile50-respread-M`, `b136-r620-gross065-W`) is carrying a materially stronger claim than one that clears on only the committed leg.

## Survivorship and limits
U56 and B136 are **current-constituent** lists — every CAGR and drawdown LEVEL above is optimistic; the episode-to-episode difference is the durable part. SMALL is not priced here (the shelf's memo'd books do not live on it), which bounds the generality of the shelf count. The splice convention deletes days from every series identically, so Sharpe, CAGR and MaxDD share one shortened calendar; a spliced MaxDD cannot be compared with an unspliced one, which is exactly why the FIXED column is reported as a diagnostic and not as a verdict. Nothing here is a capital claim on its own and nothing was promoted.
