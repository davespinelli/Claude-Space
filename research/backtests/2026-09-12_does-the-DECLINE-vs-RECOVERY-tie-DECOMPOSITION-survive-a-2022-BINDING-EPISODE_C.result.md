# Idea 811 — does the DECLINE vs RECOVERY tie DECOMPOSITION survive a 2022 BINDING EPISODE?

**lane C, 2026-09-12.** Script `2026-09-12_does-the-DECLINE-vs-RECOVERY-tie-DECOMPOSITION-survive-a-2022-BINDING-EPISODE_C.py`.
Outputs `.console.txt` / `.cells.csv` (720 rows = 144 arms × 5 windows) / `.bear22cells.csv` /
`.predicates.csv` (200 points) / `.episodes.csv` / `.walkforward.csv` / this file.

## ANSWER = NO. THE PREDICATE SURVIVES; THE **CLAIM ABOUT THE LEG SPLIT** DOES NOT.

Idea 596's headline was not "DECLINE is exact" but "**the LEG SPLIT is the whole gap**" —
necessity moving +0.8667 from the whole-episode window to the decline leg. On a corpus whose
binding episode is the 2022-era bear instead of 2020, that gap **is +0.0000**: the whole-episode
predicate is exact too. The leg split carries nothing, because on a long decline there is
nothing left for it to carry.

| corpus | binding episode | ties | nec(EPISODE) | nec(DECLINE) | **LEG-SPLIT delta** | suff(DECLINE) |
|---|---|---|---|---|---|---|
| FULL (596's) | 2020, 17d↓ / 170d↑ | 45 / 141 | 0.1333 | 1.0000 | **+0.8667** | 1.0000 |
| POST20 | mixed (1 of 3 panels BEAR22) | 12 / 126 | 0.5833 | 1.0000 | **+0.4167** | **0.8000** |
| BEAR22-binding cells | 2021-11 → 2023-03, 302d↓ / 195d↑ | **3 / 276** | **1.0000** | 1.0000 | **+0.0000** | 1.0000 |
| BEAR22a / b / c (pure) | same | **0 / 117** | — | — | — | — |

Read left to right: as the binding episode's decline lengthens, the episode-average column climbs
to meet the decline column and the decomposition flattens out. **0.8667 is a property of a 17-day
decline, not of the predicate.** The queue's guess was that the two columns' roles would *invert*;
they do not invert, they **converge** — and then the table empties.

## The vacancy is the mechanism, and it is the sharper half of the result

The three pure BEAR22 windows carry **zero MaxDD ties in 117 scored arms on all three panels**,
against 45 of 141 (31.9%) on FULL. Not a marginal drop — nothing. The reason is in the same
files: at **every** cover bar up to 1e-3, `#pred(DECLINE) = 0 of 117`, i.e. every single arm
de-grosses *somewhere* inside the control's peak→trough leg. A market gate can sit out a 17-day
crash; across 302–336 trading days of grinding decline, **every gate in every family fires at
some point**, so no arm reproduces the control's decline, so no arm ties its MaxDD. Idea 596's
exact predicate needs a tie population, and a long decline does not produce one.

This also dates 596's scope limit precisely. 596 named sufficiency as its empirical half ("the
arm's MaxDD could be set on a *different* episode — 0 instances here"). **POST20 finds the
instances: sufficiency 1.0000 → 0.8000, 3 false positives**, all U56 SPYDD at dial 0.20, each an
arm whose own MaxDD is set on the 2025 episode instead. With the **SPYDD confound family dropped
the break disappears** (12/12 both directions) — so the honest statement is that sufficiency
broke *only inside the family this corpus names as its confound*, which is weaker than a clean
break but is more than the 0 instances 596 could show.

## What had to be measured rather than assumed

A post-2020 **start date alone does not give a 2022-binding corpus**. On the live band book a
2020-07-01 → today window binds on **April 2025** (U56, −7.22%, 35d↓/104d↑), not on the 2022 bear;
the end date had to join the window dial. And the "2022" label is the **episode**, not a calendar
year: the band book's 2021-11-08 peak grinds to a **2023-03-10** trough (U56) / 2023-03-13 (B136).
Trough years are printed for every window so the label hides nothing. **SMALL never binds on that
bear at any rung** — its book grinds to a 2023-10-27 trough after a 492-day decline — which is why
the pooled ≥80% pre-registration bar (H_BEAR22p) fails and the corpus had to be read the way the
queue words it, per (panel, window) cell.

## Power, stated with the result and not after it

**The restricted corpus carries 3 ties.** Every rate in its row of the table above rests on three
cells and none of them deserves a decimal place. What this run establishes at strength is the
**negative and the vacancy** — the leg-split delta does not reproduce away from 2020, and a
long-decline corpus has no ties at all (0 of 117, at every cover bar) — not a new exactness claim.
H_BEAR22c (≥10 ties) **FAILS**, and that failure is the honest headline for the positive direction.

**6 of 8 evaluable pre-registered hypotheses pass**; the two that fail are both the corpus-existence
bars. H_SHAPE, H_DECLINE, H_SUFF, H_EPUP, H_COST, H_RECOV pass.

## Gates and the reproduction of 596 (unplanned, and the strongest check here)

G1 never-firing arm ≡ CONTROL-U **0.000e+00**; G2 runner ≡ `engine.backtest` **1.388e-17**;
G3 every (panel, gross, window) binding episode reproduces its window's MaxDD **0.000e+00**;
G4 CONTROL-M's mean gross ≡ the arm's, max **1.562e-04**. All pass.

The FULL window is a fresh rebuild of 596's corpus and lands on it **field for field**: 141 scored
arms, **45 ties (31.9%)**, by family SPYTR 0 / BREADTH 12 / VOL 18 / SPYDD 15; EPISODE 0.1333,
DECLINE 1.0000/1.0000, RECOVERY 0.1333, DECLINE+COST 1.0000; 39 of 45 ties missed by the episode
predicate, all with decline cover 0.000e+00, all 39 recovered by the decline leg; DECLINE vs
DECLINE+COST disagree on **0 of 141**; rule 8 **4 of 36** picks pass 4b OOS and **2 of 36** pass 4a
OOS; over all arms 4a 2 / 4b 7 full sample, 4a 12 / 4b 12 OOS, BOTH 0. 596 reproduces exactly.

H_COST holds in **every** window (0 disagreements at all 5 rungs): the switch-cost term stays
redundant, now across four episode shapes rather than one.

## Rule 8 and both KEEP paths: KILL

Dial chosen on IS by IS Sharpe alone, OOS read once — (a) the standing 2016/2017 split on FULL,
(b) a window-local half split on the short windows, a **stated departure** reported beside (a).

| window | scored | 4a | 4b | 4a OOS | 4b OOS | BOTH | 4b & 4b-OOS | **…& beats its own CONTROL-M** |
|---|---|---|---|---|---|---|---|---|
| FULL | 141 | 2 | 7 | 12 | 12 | 0 | 6 | **0** |
| POST20 | 126 | 2 | 12 | 0 | 3 | 0 | 3 | **0** |
| BEAR22a | 117 | 2 | 16 | 13 | 9 | 0 | 4 | 1 |
| BEAR22b | 117 | 15 | 0 | 9 | 0 | 0 | 0 | **0** |
| BEAR22c | 117 | 12 | 8 | 0 | 0 | 0 | 0 | **0** |

FULL-window comparands (OOS): SPY 15.33% / 0.877 / −33.72%; RULES v2 9.47% / 1.278 / −12.05%
(U56), 7.88% / 1.106 / −12.24% (B136), 3.75% / 0.560 / −13.89% (SMALL). Dominant binding 4b leg on
FULL: CAGR (74 cells), then H1+H2+OOS+CAGR (53).

**KILL.** On the protocol-standard window, 0 of 141 arms clear 4b on both windows *and* beat their
own gross-matched control — 6 of the 7 full-sample 4b passers are matched by a CONTROL-M that
passes 4b too (the pass is exposure, not the clause), reproducing ideas 502/504/674/767 and 596
itself. The single row anywhere that beats its matched control is **U56 BREADTH 0.35 g=0.75 in
BEAR22a** (10.64% / 1.446 / −6.77% vs ctlM 10.28% / 1.419 / −6.65%, 2.12x/yr turnover) — an 881-day
window, judged on a window-local half split, margin 0.027 Sharpe and 0.12pp MaxDD, selected after
looking at a 720-row grid. That is a rounding error inside a cherry-picked window, not a candidate.
**No KEEP, no memo, no RULES change.**

## Caveats

- **SURVIVORSHIP.** All three panels are current-constituent lists; every level is optimistic, the
  SMALL panel worst (`data/SMALL_PANEL_README.md`); the 52 tickers with `max_1d_move >= 1.0` in
  `data/small_meta.csv` were dropped first, leaving 663. Predicate rates are within-panel agreement
  rates, which survivorship moves far less than levels; the walk-forward levels carry the full bias.
- The BEAR22 windows are **short (775–1005 trading days) and post-crash**, i.e. bull-heavy, and
  their walk-forward uses a half split rather than the record's 2016/2017 convention. No level from
  them is a capital claim, and none is used as one.
- **3 ties.** Restated because it governs everything positive above.
- `data/prices.csv` is re-downloaded daily, so U56 rows reproduce to ~3e-3, not bit-exact (idea 406).
- The tie label, the confound family, the book and the gate families are 596's, unchanged, so this
  is a re-measurement of that construction and inherits its choices — including that the result
  holds only for **de-gross** clauses (an arm that can hold *more* than the control is untested).

## Filed for the queue

- **812** — the vacancy generalised: census every committed tie-population claim on the record for
  the DECLINE LENGTH of its binding episode, and report which claims live only on short declines.
- **813** — does sufficiency break outside the SPYDD confound on any corpus with ≥ 30 ties and a
  decline leg longer than 60 trading days?
