# Idea 995 (cloud lane, 2026-09-16) — is REFUSAL COST a CADENCE object the way `L4_DD` is?

**ANSWERED = YES IT IS A CADENCE OBJECT, BUT IT IS THE OPPOSITE ONE — IT RUNS EXACTLY BACKWARDS
TO `L4_DD`.**
Three KILLs: (1) for "refusal cost tracks 981's `L4_DD` drift channel"; (2) for reading 993's
`ctrl_4b_in_emptied` 0-vs-4 as a cadence asymmetry in the SCREEN — it is a DENOMINATOR artefact;
(3) for "the refusal cost is this screen's" — a rate-matched null covers the real number at
**12 of 12** points. One KEEP, as a PROTOCOL rule 4 reporting clause (proposed, not applied).

Gates **11 of 11 PASS**, including three cross-run reproductions: idea 993's committed 13,500-row
ladder at max|d| 7.11e-15 (G3a), idea 981's published `L4_DD` gradient at max|d| 3.33e-04 (G3c),
and this run's per-cadence decline table aggregating to 993's committed MQ18/DW18 rows at
max|d n_emptied| 0, max|d ctrl_4b| 0, max|d mean dSharpe| 5.0e-05 (G3b). The resolution below is
a **split of 993's own numbers**, not a different measurement of them.

## The grid

3 panels {U56 56 cols, B136 136 cols, SMALL 664 cols after dropping the 52 tickers with
`max_1d_move >= 1.0`} × 5 books × 2 gross
{CORE 0.75, EXT 1.00} × D/W/M/Q at MATCHED gross × every phase (1/5/21/63) = **2,700 phase-books
× 5 cost rungs = 13,500 rows**; 36 rule-8 slots (3 panels × 3 IS-only choosers × 4 cadences),
9 per cadence. Tuned axes exactly two — fallback {FB_NONE, FB_CASH, FB_SPY, FB_LIVE} × floor
{0.00 … 0.90}, all 28 points reported, none selected. **Cadence is the MEASURED axis, never a
tuned one.** Share basis FIXED at `S_IS4B`.

## 1. The gradient is monotone, and its sign is inverted

`RC_PAIR` = mean over EMPTIED slots of (fallback − the unscreened control's pick in the SAME slot),
OOS Sharpe. Negative = refusing was expensive.

| floor 0.40 | D | W | M | Q | Spearman(cadence rank, COST) |
|---|---|---|---|---|---|
| FB_CASH | −0.8939 | −0.8502 | −0.5665 | −0.3740 | **−1.00** |
| FB_SPY  | −0.0188 | +0.0239 | +0.3104 | +0.5029 | **−1.00** |
| FB_LIVE | +0.0871 | +0.0682 | −0.0064 | +0.1862 | −0.20 |
| *comparand:* 981's `L4_DD` fail rate | 0.633 | 0.647 | 0.832 | 0.927 | **+1.00** |

Refusal is **most expensive at the FAST end and cheapest at the SLOW end** — a perfect monotone
gradient (|rho| = 1.00 at 4 of the 6 floors under both passive fallbacks) pointing the opposite
way to the one leg the record has established as a cadence object. **H_MONO FAIL at −1.0000
against a +0.80 bar; H_TRACK FAIL at −0.8829 against a +0.50 bar** over the 7 non-empty
(panel × cadence) cells. A pre-declared bar missed by a sign, not by a margin.

## 2. …but it is the SAME CHANNEL: drift, not the turnover rebate

981's own diagnostic, re-run here: the cadence range of `RC_PAIR` at the **0 bps** rung retains
**0.9573 / 0.9592 / 1.0885** of its 10 bps magnitude under CASH / SPY / LIVE. **H_ZERO PASS.**
The gradient is a property of what the tape does between resets, not of what the turnover costs —
the same channel 981 localised under `L4_DD`, traversed in the opposite direction.

A second, construction-free rate control agrees: at **floor 0.90 the screen refuses 9 of 9 slots
in every cadence**, so the refusal RATE is identical across the ladder, and the cost gradient is
still there (CASH −0.8939 / −0.9008 / −0.8467 / −0.6578).

## 3. 993's 0-vs-4 is a DENOMINATOR artefact

| floor | D | W | M | Q |
|---|---|---|---|---|
| control OOS 4b passes AVAILABLE to destroy | **2** | **2** | **0** | **0** |
| destroyed (`ctrl_4b_in_emptied`), 0.25 up | 2 | 2 | 0 | 0 |

The screen destroys **4 of the 4 available at D/W and 0 of the 0 available at M/Q**. It is not
gentler on the slow half; the slow half had nothing to lose. **H_4B_FAST PASS** on the literal
count (D+W 4 > M+Q 0) and **KILL for the reading** — 993's "the price of a refusal is 0 on one
half of the ladder and total on the other" is true of the numerator only.

What the screen actually does at its headline floor is a **trade, 4 for 3**: it gives up the D 2
and W 2 and buys **3 at M** (floors 0.40 and 0.50), under every fallback convention alike.

## 4. The cost is the CELL's, not the SCREEN's

Rate-matched null, 2,000 draws, seed 995: a random screen refusing the SAME number of slots in the
SAME (panel, cadence) cell and paying the SAME fallback. The real `RC_PAIR` lands at percentile
**0.13–0.47 at all 12 (fallback × cadence) points; `outside90` is False everywhere. H_RATE FAIL.**
A refusal in a daily cell costs about −0.85 Sharpe whoever refuses it. The gradient is a property
of the cadence rung, not of `S_IS4B`.

## 5. The convention gap, per cadence — and the empty median at D

`RC_CONV` = med OOS Sharpe(FB_NONE) − med(fb), the free-refusal flattery, at floor 0.40:
**W +1.1050 under CASH** (a full Sharpe point), M +0.0697, Q +0.0316. At **D it is UNDEFINED at
every floor above 0.00**: the screen refuses all 9 daily slots, so 980's convention has zero rows
to take a median over. The incumbent accounting does not merely flatter on the fast half — on the
fastest rung it **has no number at all**, and the record would have published silence as absence.

## 6. Rule 8 walk-forward — the capital reading

Every (book, gross) chosen on 2009–2016 alone; OOS 2017–2026 read once. **Both KEEP paths
evaluated at all 28 points × 4 cadences.**

* Unscreened control, 36 rule-8 picks: **OOS 4b 4 of 36** (D 2/9, W 2/9, M 0/9, Q 0/9),
  **OOS 4a 0 of 36**.
* Paid/screened, best point (floors 0.40, 0.50, cadence M): **OOS 4b 3 of 9, OOS 4a 0**, identical
  under all four fallback conventions — no fallback can certify (cash and SPY fail four legs each,
  the live book fails `L5_CAGR` on every panel), so paying for refusals can only remove a pass.
* Best screened pick: **U56 / M / `BAND03` @ gross 1.00 — OOS CAGR 12.81%, Sharpe 1.2245,
  MaxDD −18.81%** vs **SPY OOS 15.21% / 0.8713 / −33.72%** and vs the live RULES v2 baseline
  (full-sample Sharpe 1.2009, MaxDD −12.05%). Best control pick: the same object at D/W
  (OOS 12.45% / 1.2871 / −14.77% and 12.67% / 1.2758 / −15.91%).
* Full sample over the whole ladder: 4b **662 of 13,500** rows, 4a **38 of 13,500**; by cadence
  4b D 16/150, W 97/750, M 231/3,150, Q 318/9,450 and 4a D 3, W 18, M 0, Q 17 (the row counts are
  unequal because a cadence contributes one row per phase: 1 / 5 / 21 / 63).

**Every OOS 4b passer in this run is U56 `BAND03` at gross 1.00 — the live book at full gross,
now on its sixth independent arrival — and not one of them passes 4a.** Sixth arrival, sixth
refusal. Nothing promoted.

## Verdict

**KILL ×3 / PARK the object / KEEP one reporting clause (proposed, not applied, rule 6).**
Refusal cost *is* a cadence object and *is* carried by 981's drift channel, but it is not `L4_DD`
— it runs backwards to it, and it belongs to the cadence rung rather than to the screen. No KEEP
path is bought: 4a is 0 of 36 and every 4b pass is an object the record has already refused five
times. `2026-09-16_refusal-denominator-clause_cloud.memo.md` carries the exact wording.

## Survivorship (rule 9)

U56, B136 and SMALL are CURRENT-CONSTITUENT lists; SMALL additionally drops every ticker with
`max_1d_move >= 1.0` per `data/small_meta.csv`. Every CAGR and drawdown LEVEL above is optimistic
and **every 4b count — control, screened and fallback alike — is an UPPER bound.** The measured
object is a DIFFERENCE between accounting conventions applied to the SAME picks on the SAME tape,
resolved by cadence, and is very nearly immune; `FB_SPY` and `FB_CASH` carry no survivorship
inflation at all, so the fast-end refusal cost they price is if anything understated on honest
data. `RULES.md`, `PROTOCOL.md`, `scan.py`, `bot.py` and `baseline.py` are untouched.
