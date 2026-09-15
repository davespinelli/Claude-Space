# Idea 926 — does the ZERO-COST pass↔BASE-RATE inversion hold on MONTHLY 4b passes? (lane B)

**ANSWERED = YES ON MONTHLY, AND 680's HEADLINE IS A WEEKLY-ONLY RESULT.** Idea 680 concluded
that PROTOCOL rule 2's 10 bps "already does the entire job a base-rate clause would do"
(4 of 4 committed-key 4b passes outside their own null at 10 bps). Re-run across a cadence
ladder that conclusion **does not transfer**: at the same 10 bps a **monthly** book's 4b pass
is outside its null **1 time in 3**, Spearman ρ(4b pass, null base rate) is **+0.4470** where
the weekly ρ is **−0.0728**, and the monthly version of the record's standing candidate passes
4b while **38.4%** of its own gross-matched coin flips pass the same bar. **KILL for 680's
claim as a general statement** (it stands, exactly, for weekly books); the base-rate clause it
killed is **needed again for any book slower than about 100 bp/yr of cost drag**. Nothing
promoted: 4a **0 of 125** IS-only picks, OOS 4b on monthly **1 of 35**, and that one passer is
an already-known book. No RULES change, no PROTOCOL edit applied (rule 6). `RULES.md`,
`PROTOCOL.md`, `scan.py`, `bot.py`, `baseline.py` untouched.

SELECTION: the LAST Open idea carrying a price leg. Idea 904 sits below it and carries a
standing SKIP note (a census of committed placebo *numbers* against a seed floor — no book to
price, so it cannot carry this lane's mandatory rule-8 walk-forward); its note is extended
rather than removed.

Script: `2026-09-15_is-the-ZERO-COST-pass-to-BASE-RATE-inversion-a-CADENCE-fact_B.py`
(1,563 s, seed base 680 — 680's own, which is what makes G3 exact). Artifacts: `.books.csv`
(480 rows), `.nulls.csv` (960), `.rho.csv` (16), `.drag.csv` (480), `.draws.csv` (60,000),
`.walkforward.csv` (144), `.console.txt`. The whole grid was run **twice end to end** and the
ρ table is byte-identical between the runs.

---

## THE GRID

4 cadences × 3 panels × 2 claim sets × 5 books × 4 cost rungs = **480 scored books**, each
against its own 500-draw gross-matched null (**240,000 null book-scorings**). Two tuned axes
and only two — **CADENCE** {W, 2W, M, Q} and **COST RUNG** {0, 5, 10, 25 bps} — every grid
point reported, none selected. Everything else (panels, books, claim sets, gate, warm-up, null
construction, seeds) is copied from idea 680 unchanged, which is why its W column reproduces.

## THE ANSWER — ρ(4b pass, null base rate), SPEARMAN, n = 30 cells per point

| cadence | turn/yr | ρ @0 bps | ρ @5 | ρ @10 | ρ @25 | mean base @0 → @10 | 4b passes OUTSIDE their null @10 |
|---|---|---|---|---|---|---|---|
| **W** (680's) | 16.08 | **+0.6569** | +0.4639 | **−0.0728** | nan (2 passes, no variance) | 19.43% → **0.03%** | **4 of 4** |
| **2W** | 11.11 | +0.4418 | +0.4915 | **+0.4533** | −0.0714 | 22.45% → 3.95% | 4 of 7 |
| **M** (the question) | 7.27 | +0.4045 | +0.4116 | **+0.4470** | **+0.4597** | 9.03% → 3.45% | **1 of 3** |
| **Q** | 3.55 | nan | nan | nan | nan | 1.71% → 1.24% | 0 of 0 (no 4b pass at any rung) |

ρ is nan, never 0, where the pass flag is constant. Pearson is printed beside every ρ in the
console; at the monthly 10 bps point it is +0.5215, i.e. the sign does not depend on the
statistic. 680's own weekly numbers (+0.6387 at 0 bps, −0.1048 at 10 bps, on 1,000 draws)
reproduce here in sign and size on the 500-draw prefix.

**The inversion is not a zero-cost artefact. It is a FAST-BOOK artefact.** On monthly books it
is present at every rung tested, including the only rung PROTOCOL sanctions, and it is
*stronger* at 25 bps (+0.4597) than at 0 bps (+0.4045).

## THE BINDING CELL — what this costs the record's standing candidate

Same rule, same panel, same 10 bps, only the cadence changed:

| cadence | U56 `CORE/TOP20` | halves | OOS | turnover | 4b | its null's 4b base rate |
|---|---|---|---|---|---|---|
| W | 12.60% / 1.0881 / −18.31% | 1.094 / 1.090 | 14.24% / 1.160 / −18.31% | 9.64x | PASS | **0.0%** |
| **M** | **14.69% / 1.2025 / −19.51%** | 1.216 / 1.198 | **16.67% / 1.283 / −19.51%** | 4.33x | PASS | **38.4%** |

Slowing the 2026-09-04 KEEP-4b incumbent from weekly to monthly improves every headline it has
— +2.09 pp of CAGR, +0.114 of Sharpe, +2.43 pp of OOS CAGR — and moves its coin-flip base rate
from 0.0% to 38.4%. **The cadence gain is inside its own null**, and a reader who quotes the
monthly triple as evidence about the RULE is quoting the family. (SPY, same tape: 15.13% /
0.8846 / −33.72% full, 15.27% / 0.8741 / −33.72% OOS.)

## THE MECHANISM — it is ANNUAL COST DRAG, not the cost rung (section E2, POST-HOC)

Labelled post-hoc in the console because it was written after the grid was read; it selects
nothing. Over the 480 cells, base rate vs the cost **rung** ρ = −0.3026, vs **turnover** alone
−0.0099, vs **cost × turnover** −0.2745; restricted to the 152 cells where the statistic can
move (base rate > 0) the ordering is decisive: rung −0.4103, turnover −0.1182, **drag −0.5012**.

| annual drag (bp/yr of NAV) | cells | mean null base rate | max | cells > 5% |
|---|---|---|---|---|
| 0 | 120 | 13.15% | 100.0% | 36 |
| < 25 | 72 | 5.88% | 96.0% | 13 |
| 25–50 | 65 | 5.04% | 81.2% | 17 |
| 50–100 | 81 | 2.25% | 44.4% | 11 |
| **100–200** | 72 | **0.17%** | 2.8% | **0** |
| **> 200** | 70 | **0.00%** | 0.0% | **0** |

Matched-drag pairs make the point without a model: `W @5 bps` (80 bp/yr) reads 2.09% and
`M @10 bps` (73 bp/yr) reads 3.45% — the same place on the drag axis, two different rungs;
`W @10 bps` (161 bp/yr) reads 0.03% and `M @25 bps` (182 bp/yr) reads 0.21%. **PROTOCOL's fixed
10 bps buys 161 bp/yr of disinfectant on a weekly book and 73 bp/yr on a monthly one** — less
than half — which is the whole of 680's result and the whole of its failure to generalise.

**The queue's own premise is wrong in size and right in direction, and it is MEASURED here
(G8):** the M/W turnover ratio across the 30 cells is **median 0.448** (min 0.421, max 0.698),
not "a third". The band book is the outlier at ~0.70: `BAND03` barely trades less when slowed,
because its turnover is gate-driven, not schedule-driven.

## RULE 8 — walk-forward, parameters chosen on 2009–2016 only, 2017–2026 read once

4 cadences × 3 panels × 4 rungs × 3 IS-only choosers = 144 cells, **125 live picks (19 IS sets
EMPTY)**. Totals: **OOS 4b 19 of 125, 4a 0 of 125.**

| cadence | OOS 4b | best OOS pick (its chooser's own IS-only pick) |
|---|---|---|
| W | 9 / 28 | U56 `EXT/BAND03` @0 bps — 12.95% / 1.301 / −15.88%, 4b PASS |
| 2W | 9 / 30 | U56 `EXT/BAND03` @0 bps (CH_4bIS) — **13.34% / 1.331 / −15.97%, 4b PASS** |
| **M** | **1 / 35** | U56 `EXT/BAND03` @25 bps (CH_4bIS) — 12.54% / 1.201 / −18.84%, 4b PASS |
| Q | 0 / 32 | U56 `CORE/EWELIG` @0 bps — 11.76% / 1.052 / −22.21%, 4b fail |

Comparands on the same OOS window: **SPY 15.27% / 0.8741 / −33.72%** (15.33% / 0.8769 /
−33.72% on B136/SMALL); **RULES v2 (live) 9.46% / 1.277 / −12.05%** weekly on U56, 9.56% /
1.224 / −14.38% monthly. Every OOS 4b passer in the grid is `BAND03` — the live band book at
gross 1.00 — or `EWELIG`; **no new book, and 4a is 0 of 125**, so nothing here is promotable
and nothing is proposed for promotion.

**The clause as a CHOOSER still does not pay, even where it now bites.** CH_BASE differs from
CH_SHARPE in **6 of 48 cells** (680, weekly only, saw 1 of 21) — the clause is no longer inert
once books are slow — and the picks it buys are worse: OOS 4b **5 vs 6**, mean OOS Sharpe
0.810 vs 0.814, mean OOS CAGR **12.90% vs 12.94%**. Its largest single move is still 680's:
U56 weekly at 0 bps, −3.29 pp of OOS CAGR for nothing. **Report the null; do not choose with
it.**

## GATES — 9 of 10, and the failure is reported as a failure

`G0` local cadence mask ≡ `engine.rebalance_mask` on W/M/Q, **0 differing rows** · `G1`
ctx.run ≡ `engine.backtest` @10 bps, worst of W/M/Q **2.082e-17** · `G2` band_book(0.03,0.75)
≡ `rules_v2_weights` **0.000e+00** · `G3b` the 2026-09-04 KEEP-4b incumbent **12.60% / 1.0881 /
−18.31%** vs published 12.66% / 1.0921 / −18.31%, max|Δ| 3.958e-03 · `G5` gross match
**0.0000** worst over all 120 families · `G6` determinism **0.000e+00** · `G7` SMALL screen
drops 52 tickers (663 names + SPY) · `G8` turnover monotone in cadence **30 of 30 cells** ·
`G9` the 250-draw base rates are exact prefixes of the 500-draw streams.

**`G3` FAILS AS WRITTEN, and the bar is not moved after the fact.** The gate required an exact
reproduction of idea 680's committed `.nulls.csv` on its W column at 500 draws — **bar 0.0 on
both legs**. All 90 cells matched and the leg the gate exists for, the **null base rate, is
0.000e+00 exact**; the book-Sharpe leg differs by **2.220e-16**, one ULP of double precision
from the CSV round-trip. The gate is recorded FAIL because that is what it says; the
reproduction it was written to establish succeeded. Filed as a follow-up so the next run states
a float bar rather than 0.0 for a round-tripped level.

## SURVIVORSHIP (PROTOCOL 9)

`universe.json`, `universe_broad.json` and the SMALL screen are current-constituent lists, so
every CAGR and drawdown LEVEL above is optimistic — the books' and the nulls' alike. Direction,
as in 680: a coin flip drawn from a survivor panel is a **better** book than one drawn in real
time, so **every base rate is an UPPER bound** and every percentile a **LOWER** bound. That
cuts against this run's headline, not for it: the true monthly base rates are *at most* the
38.4% reported, which is why the result is stated as "a coin flip clears the bar often enough
to matter", not as a point estimate. The cadence contrast, the drag law and the matched-drag
pairs are same-tape, same-names comparisons and are unaffected; the 4b LEVELS are read against
SPY, which is not survivorship-inflated, so they are not protected by the same-tape argument.

## WHAT THIS MEANS FOR CAPITAL

Nothing changes in the live book. The operational consequence is a reporting line, proposed for
the Sunday review in `2026-09-15_cadence-base-rate-clause_B.memo.md` and **not applied**
(rule 6): 680's "a 4b pass quoted at 0 bps is not evidence" should read **"a 4b pass quoted at
an annual cost drag below ~100 bp/yr is not evidence without its null beside it"** — which
catches every monthly book in this record at PROTOCOL's own 10 bps rung, including the slowed
version of the standing candidate.

## AN INDEPENDENT REPLICATION THAT IS ALSO A DEFECT REPORT

**The cloud lane claimed and ran this same idea in the same hour** (commit `cb0fab5`, pushed
while this run was scoring its last panel; neither lane saw the other's commit, because a claim
in `QUEUE.md` is only visible after a push). Its grid is narrower — W and M only, 3 rungs, 250
draws — and its pre-registration is its own, so the agreement is worth recording:

| | cloud lane (250 draws, W/M, 3 rungs) | this run (500 draws, 4 cadences, 4 rungs) |
|---|---|---|
| monthly ρ @0 / 10 / 25 bps | +0.4131 / +0.4349 / +0.4245 | +0.4045 / +0.4470 / +0.4597 |
| weekly ρ @0 → 10 bps | +0.6569 → −0.0728 | +0.6569 → −0.0728 |
| U56 `CORE/TOP20` monthly base rate @10 bps | 40.8% | 38.4% |
| M/W turnover, median | 0.4483 | 0.448 |

The base-rate gap is the draw budget and nothing else: both lanes draw nested prefixes of idea
680's seed streams, so 250 is a prefix of this run's 500. **Same verdict, reached twice, from
two pre-registrations.** The two runs propose *different wordings for the same reporting line* —
turnover below ~10x/yr (cloud) versus **annual drag below ~100 bp/yr** (here) — and they should
be reconciled at the Sunday review rather than both landing; the drag wording is the one this
run's E2 can defend, because turnover alone correlates −0.1182 with the base rate while drag
correlates −0.5012.

**TWO RECORD DEFECTS, stated because each has now cost a duplicated run:** (a) `QUEUE.md`
carries **two different ideas numbered 924, two numbered 925 and two numbered 926** — one set
filed by idea 922, one by idea 680; this run claimed 680's 926. (b) A claim is only visible
after a push, so two lanes ran the same idea, and their follow-ups then collided again — the
cloud lane took 927–929 within the hour, so this run's follow-ups were renumbered. Both filed
as idea 932.

Follow-ups filed: 930 (re-score the record's committed 4b passes by their own book's annual
cost DRAG and flag every pass below the ~100 bp/yr line), 931 (is the W→M Sharpe gain on the
standing candidate itself inside its null — a cadence-ladder percentile test on the book, not
the bar), 932 (both defects above: the duplicate numbering, and a claim protocol that survives
concurrent lanes).
