# Idea 470 — does the matched-gross control belong on every published DIAL, not just count?

Lane C, 2026-09-08. Script `2026-09-08_does-the-matched-gross-control-belong-on-every-published-DIAL-not-just-count_C.py`,
console `..._C.console.txt`, artefacts `.census.csv` `.census_rejects.csv` `.grid.csv` `.matched.csv` `.walkforward.csv`.
10 bps headline (+25 bps rung), weekly unless the cadence dial says otherwise, next-day execution, cash credited at 0.

**Verdict: ANSWERED / SPLIT. The queue's premise is half right and its consequence does not transfer.
No KEEP, no memo, no RULES change.**

---

## 0. What was asked and what was found, in one paragraph

Idea 244 showed that a COUNT dial run under `GROSS/n` is an exposure ladder wearing an `n` label, and
that matching mean realised gross killed 7 of its 10 4b passes. QUEUE 470 asks whether the same control
belongs on band, vol-cap, cadence and threshold dials. **It does — on the GATING dials, and as a
reported column rather than as a verdict filter.** Vol-cap moves 6 of 6 (panel × gross) cells by ≥ 5 pp
of NAV, MA-length 4 of 6, band 2 of 6, and cadence — carried deliberately as the negative control —
**0 of 6**, so this is a property of dials that change *what is held*, not of dials in general. But the
consequence idea 244 found does NOT transfer: **all 9 of this grid's matched-pair 4b passes survive the
control, and the control itself passes 0 of 252.** The bigger finding is auditability: **455 of 710
published non-count dial cells (64.1%) publish no gross column of any kind**, so most of the record's
dial results cannot be adjudicated from their own artefacts at all.

## 1. Q1 — the census (2,000 committed CSVs, 191 files admitted, every rejection logged)

| status | cells | ladder (span ≥ 5 pp) | median span | max span |
|---|---|---|---|---|
| QUOTED-REAL (an unambiguous realised-gross column) | 48 | 17 (35.4%) | 0.0129 | 0.4361 |
| QUOTED-AMBIG (only a bare `gross` column) | 207 | 59 (28.5%) | 0.0017 | 1.1924 |
| UNQUOTED (no gross column at all) | 455 | **not adjudicable** | — | — |
| **total** | **710** | | | |

Rejections: 162 dial columns with no Sharpe beside them, 80 with < 3 distinct values, 1 empty file.

Two labelling corrections were made **during** this run and are recorded because they change the headline:

* `m_GROSS` is a **margin against a bar**, not a gross level (verified: `2026-09-05_gross-as-the-missing-third-bar_B`
  publishes `m_GROSS` −0.425…+0.250 beside `gross` 0.075…0.750). A first pass read it as a level and
  inflated the QUOTED-REAL ladder count from 17 to 23.
* The column `m` names **at least two different objects** in the record — a gross multiplier in that same
  file, a no-trade band in QUEUE 328. Two pre-registered source regexes were tried and **both mislabel the
  verified instance**, so `m` is carried as its own `M?` family, counted in every denominator, and the
  headline is quoted as a bound. This is idea 469's undecidability problem in a second column.

**Headline Q1:** on label-decidable cells the published ladder rate is **2 of 33 = 6.1%**; including the
284 undecidable `m` cells the record-wide rate is **bounded at 4.2%–35.4%** (2–17 of 48 adjudicable).
The AMBIG column is genuinely ambiguous, not merely noisy: its max span of **1.1924 exceeds 1.0 of NAV**,
which is only possible if that `gross` column is a design *level* (a leverage dial), not a realised
measurement. **The operative census result is the UNQUOTED count: 64.1% of published non-count dial
cells cannot be checked at all**, which is why Q2 measures the span directly rather than reading it off.

## 2. Q2 — the span measured directly (3 panels × 2 gross × 4 families, all 24 cells printed)

Realised-gross span across each dial's own grid, 10 bps, full sample:

| family | ladder cells (span ≥ 0.05) | max span | where |
|---|---|---|---|
| VOLCAP `max_vol ∈ {0.25,0.40,0.60,0.90,1.50,∞}` | **6 / 6** | **0.3827** | SMALL439 @ gross 1.00 |
| MA `len ∈ {50,100,150,200,300}` | **4 / 6** | 0.1057 | B136 @ gross 1.00 |
| BAND `∈ {0.00,0.01,0.03,0.06,0.10,0.15}` | **2 / 6** | 0.0682 | U56 @ gross 1.00 (B136 0.0149, SMALL439 0.0270) |
| CADENCE `∈ {D,W,M,Q}` (negative control) | **0 / 6** | 0.0139 | — |

**12 of 24 cells are gross ladders.** The negative control behaves exactly as pre-registered: cadence
changes only the rebalance schedule, so its gross moves through drift alone and never reaches 1.4 pp.
The confound is a property of dials that change **which names are held**, and its size is panel-dependent
— vol-cap spans 99.2% of its own mean gross on SMALL439 (0.090 → 0.377 at gross 0.75) versus 27.1% on U56.

## 3. Q3 — the matched control (leverage-safe anchor, max realised match error 1.17e-04)

For each point the higher-gross member of {dial point, adopted book} is scaled **down** to the other's mean
realised gross; neither is ever scaled up, so no control is levered and no point is dropped as unmatchable.
Off-adopted points (the ones a sweep is read from), both rungs, both gross levels, 102 points:

| family | n | dSharpe mean / median | dSharpe > 0 | dOOS_Sharpe mean | dOOS > 0 | dCAGR mean |
|---|---|---|---|---|---|---|
| BAND | 30 | −0.0022 / −0.0149 | 8/30 | −0.0057 | 12/30 | +0.0021 |
| CADENCE | 18 | −0.0265 / −0.0046 | 8/18 | −0.0396 | 10/18 | +0.0017 |
| MA | 24 | **−0.0938 / −0.0645** | **2/24** | **−0.1083** | **2/24** | −0.0060 |
| VOLCAP | 30 | +0.0020 / +0.0272 | 20/30 | −0.0201 | 18/30 | +0.0008 |

**The control has real bite on MA and none on VOLCAP.** Every off-adopted MA-length point loses to a
constant de-gross of the adopted book, on Sharpe (22 of 24) and OOS Sharpe (22 of 24): moving the trend
gate's length buys nothing that holding less of the 200d book does not already buy. Loosening the vol cap
is the opposite — it beats its own matched control on Sharpe in 20 of 30 points, so it is a selection
change, not an exposure change. Band and cadence are coin flips.

**KEEP paths on all 252 live points, both rungs:**

| arm | 4a | 4b @ gross 0.75 | 4b @ gross 1.00 |
|---|---|---|---|
| RAW (as a sweep publishes it) | **0 / 252** | 0 / 126 | 12 / 126 (9 @10 bps, 3 @25 bps) |
| PAIR-DIAL (dial, gross-matched) | 0 / 252 | 0 / 126 | 9 / 126 |
| PAIR-CTRL (adopted book, gross-matched) | 0 / 252 | 0 / 126 | **0 / 126** |

**Headline Q3: 9 of 9 gross-matched 4b passes survive the control, and the control passes nothing.**
This is the opposite of idea 244's count-dial result (7 of 10 died). Binding 4b bars on the 240 RAW
failures: CAGR 240, H2 106, OOS 96, H1 92, DD 11 — the CAGR floor binds everywhere at gross 0.75, which
is why the gross axis was added (declared in the script docstring as a change of mind, not as the
original design).

**The 9 passers are NOT a new object and no memo is written.** They are U56/B136 EW-all + 200d-gate at
gross 1.00 with a dial nudge — the already-committed family of `2026-09-08_u56-ewall-magate-fullgross_KEEP_MEMO.md`
(11.96% / 1.2126 / −15.49%) and of ideas 441/444's 54 gross-1.00 passes. The best point here, U56
VOLCAP=∞ at gross 1.00, reproduces `rules_v2_weights(gross=1.00)` **exactly** (CAGR 11.59%, Sharpe 1.2055,
halves 1.2265/1.1901, MaxDD −15.91%, OOS 1.2844), i.e. it is the live book un-de-grossed, not a discovery.
All 12 RAW passers fail 4a against the live RULES v2 (0 of 252 pass 4a anywhere).

## 4. Q4 — rule 8 (dial chosen on IS ≤ 2016-12-31, 2017-2026 read once, 48 cells)

| arm | OOS CAGR | OOS Sharpe | OOS MaxDD | OOS gross |
|---|---|---|---|---|
| ISARGMAX-RAW | 6.72% | 0.8417 | −14.83% | 0.510 |
| ISARGMAX-PAIRDIAL (pick, gross-matched) | 6.64% | 0.8417 | −14.60% | 0.503 |
| ISARGMAX-MATCHED (adopted, gross-matched) | 6.43% | 0.8381 | −13.39% | 0.508 |
| ADOPTED (do-nothing within the family) | 6.47% | 0.8380 | −13.57% | 0.513 |
| NOTHING (RULES v2) | 8.10% | **0.9665** | −15.16% | 0.553 |
| EWALL | 14.51% | 0.9514 | −32.05% | 0.875 |
| SPY | 15.45% | 0.8820 | −33.72% | 1.000 |

ISARGMAX-RAW minus: PAIRDIAL **−0.0000** (8/48) · MATCHED **+0.0036, median −0.0081** (24/48) ·
ADOPTED +0.0037 (24/48) · **RULES v2 −0.1248 (0 / 48)** · EWALL −0.1097 (16/48) · SPY −0.0403 (32/48).
IS pick == OOS oracle in **16 of 48**. Picks are stable across rungs and gross: band 0.10–0.15,
cadence M, MA 150, vol-cap 1.5/∞ (0.40 on SMALL439 @10 bps).

**Choosing a non-count dial value on IS Sharpe is a coin flip against its own matched-gross control
(24/48, median negative) and loses to doing nothing in 48 of 48 cells.** That is the 18th entry in the
record's selection-loses census, and it is why the Q3 survivals are not a rules change.

## 5. What this says about PROTOCOL (a recommendation, nothing was modified)

The queue asked whether the control "belongs on every published DIAL". The answer this run supports is
narrower than the question and is worth writing down in that narrower form:

> Any sweep whose dial changes the **eligibility set** (band, gate length, vol cap, liquidity floor,
> breadth threshold) must publish **mean realised gross per grid point** beside its Sharpe column.
> Sweeps of pure **scheduling** dials (cadence, partial-rebalance λ) need not: measured span ≤ 1.4 pp.

That clause is cheap (one column), it is the column 64.1% of the record's dial cells are missing, and it
is *reporting*, not adjudication — because on this grid the matched control changed **zero** 4b verdicts
in the direction idea 244 found for counts. Proposing it as a required LEADERBOARD/artefact column pairs
with QUEUE 408's `step_delta` proposal.

## 6. Harness checks (run before any result was read)

* `[c1]` `base_weights(band=.03, ma=200, volcap=off)` == `baseline.rules_v2_weights`: max|dW| **0.000e+00**
* `[c2]` `_gate(0.03, 200)` == `baseline.band_state`: **0** disagreements
* `[c3]` cost applied post-hoc == `engine.backtest(cost_bps=10)`: max|dr| **0.000e+00**
* `[c4]` scaling target weights by c scales held gross by c exactly at rebalance and approximately under
  drift (max|dg(t)| 9.6e-03); the operative quantity, the realised **mean**-gross match error, is
  **1.17e-04** over all 252 pairs and is carried per row in `.grid.csv`.

## 7. Limits, stated plainly

* **Survivorship:** all three panels are current constituents, one-directional, hardest on SMALL439. The
  census additionally inherits the bias of every parent script it reads.
* The census is **mechanical and column-name based**. It cannot see a dial that was swept without a
  column, and its family labels are pre-registered column lists, not semantics — `m` is the proof that
  those two can come apart, and it is reported as undecidable rather than assigned.
* `M?` (284 cells) and the AMBIG `gross` column (207 cells) are the two places a future run can tighten
  this bound; QUEUE 469's AST approach is the right instrument for both.
* Cash is credited at 0 throughout (QUEUE 406 is still open). Every comparison here is between books at
  the **same** mean gross, which is the one comparison that convention cannot bias.
