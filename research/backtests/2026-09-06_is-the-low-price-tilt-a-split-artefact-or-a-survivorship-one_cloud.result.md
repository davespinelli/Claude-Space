# Idea 185 — is-the-low-price-tilt-a-split-artefact-or-a-survivorship-one (cloud, 2026-09-06)

**Verdict: KILL, and both horns of the queue's dichotomy are wrong. The low-price tilt is
neither a split artefact nor a survivorship one — it is priced by its look-ahead content and
nothing else, and it is *weaker*, not stronger, in exactly the cohort a current-constituent
panel over-represents.** No KEEP, no book, no RULES change.

Script `research/backtests/2026-09-06_is-the-low-price-tilt-a-split-artefact-or-a-survivorship-one_cloud.py`.
Artefacts: `.console.txt`, `.arms.csv` (748 arms), `.cohorts.csv`, `.keyic.csv`,
`.walkforward.csv`, `.reproduction.csv`.

## What was open, and what this run owed

Idea 193 (2026-09-05) already ran legs (a) FROZEN and (b) DVOL and settled a third horn the
queue text did not anticipate: on auto-adjusted closes `px[T]/px[t]` **is** the cumulative total
return t→T, so a cross-sectional price-*level* rank is terminal price minus realised future total
return. That subsumes the **SPLIT** horn analytically — a split-adjusted and a dividend-adjusted
level are the same object. The identity is re-asserted here: max err **4.263e-13** (small),
**2.4e-13** (broad).

Leg **(c) MCAP is NOT RUN**: a market-cap proxy needs a shares-outstanding series, none is cached
in `data/` and this sandbox has no internet. Unchanged from idea 193; it stays queued as idea 195.
Declared, not dropped.

What idea 185 asks that idea 193 did not answer is the **SURVIVORSHIP** horn. This run tests it,
and adds the leak-free analogue of the tilt.

**Two tuned parameters** (PROTOCOL rule 4): KEY (all reported) × TILT STRENGTH m ∈ {0.20, 0.50,
1.00} (all reported). Panel, direction and cost rung are inherited reported axes. Book unchanged
from idea 181: top 20 by `composite + dir·m·key` among names above the 200d MA with vol20 < 0.60,
equal weight at gross 0.75, weekly, t+1, 10 and 25 bps.

**Reproduction**: RULES v1 u56 @10bps 6.45305% / 0.66418 / −13.82780%, exact to the published
digits; `fast_backtest == engine.backtest` at 2.8e-17; **idea 181's published grid reproduces on
604/604 broad+small rows, max |dSharpe_F| 4.441e-16, max |ddSharpe_F| 4.996e-16.**

## Q2 — the substitution table (mean dSharpe_F, NEG direction)

| key | class | broad | small | null q95 \|d\| broad / small |
|---|---|---|---|---|
| **PRICE** (published) | price level | **+0.2402** | **+0.4663** | 0.1045 / 0.2606 |
| FROZEN — leg (a) | price level | +0.1621 | +0.1633 | |
| DVOL — leg (b) | level×volume | — | **+0.5777** | |
| VOLSH | level-free volume | — | +0.3229 | |
| **DDTR** — leak-free "beaten down" | leak-free | **+0.0519** | **−0.0653** | |
| REBASED | leak-free | −0.0021 | +0.2289 | |
| MOM / R6 / R3 / VOL | leak-free | −0.0041 / −0.2010 / −0.0475 / −0.1743 | −0.2462 / −0.2326 / +0.0310 / +0.0187 | |
| PXTERM / FWDRET | oracle | −0.0546 / −0.5253 | −0.2481 / −0.7914 | |

Clearing-and-positive counts against the parent's own 20-draw null band (12 cells per key):
PRICE **4/12 broad, 6/12 small**; DVOL **6/12 small**; FROZEN 4/12 broad, **0/12 small**;
**DDTR 0/12 on both panels**; REBASED 0/12 broad, 2/12 small.

## Q4 — the tilt is priced by its leak

Mean Spearman between each key's rank at *t* and the realised forward total return *t→T*, on an
annual date grid, against the key's own mean NEG-direction dSharpe:

| panel | Spearman( \|leak IC\|, mean NEG dSharpe ) | n keys |
|---|---|---|
| broad | **+0.806** | 10 |
| small | **+0.881** | 12 |

Small panel ordering: DVOL −0.596 → PRICE −0.407 → VOLSH −0.421 → FROZEN −0.214 → DDTR −0.075,
and mean dSharpe orders the same way (+0.578, +0.466, +0.323, +0.163, −0.065). The keys that pay
are the keys that read the future, in rank order, on both panels.

## Q3 — the SURVIVORSHIP horn, refuted

The small panel split into terciles by each name's **own full-sample max drawdown** (an
oracle-conditioned cohort, declared as such — a diagnostic of the panel, never a book):
deepDD 147 names (mean MaxDD −95.88%), midDD 146 (−85.60%), shallowDD 146 (−64.80%).

If the low-price tilt were the survivorship effect the queue proposed, it would live in the
deep-drawdown cohort — the cohort a current-constituent list over-represents. It does the opposite:

| key | mean deep-minus-shallow dSharpe over 6 (m, cost) cells | cells positive |
|---|---|---|
| PRICE | **−0.1203** | **0/6** |
| DDTR | −0.1674 | 0/6 |
| DVOL | −0.2411 | 0/6 |
| FROZEN | −0.0440 | 2/6 |

At m=1.00 / 10 bps, PRICE/NEG adds **+0.1525** in the deep cohort and **+0.3643** in the shallow
one. The tilt is *strongest where survivorship exposure is weakest*. Pre-registered prediction P6
predicted the opposite and **MISSED** — which is the finding.

And the causal analogue settles it directly: **DDTR/NEG** — tilt toward names in a deep trailing
252d drawdown, knowable at *t*, the implementable version of "buy the beaten-down" — carries
**+0.0519 (broad) and −0.0653 (small)** against PRICE/NEG's +0.2402 and +0.4663, and clears the
null band positively in **0 of 24** cells. There is no beaten-down effect here to be a
survivorship artefact *of*.

## PROTOCOL rule 8 walk-forward (chose ≤ 2016-12-31; 2017-2026 read once)

| selector | mean OOS Sharpe | mean d vs S0 | t | 4b |
|---|---|---|---|---|
| S0 do nothing | 0.6061 | — | — | 0/4 |
| S1 best IS Sharpe over **all** keys | **1.7805** | **+1.1744** | +3.89 | 0/4 |
| S2 best IS Sharpe over **leak-free** keys | 0.5947 | **−0.0114** | −0.31 | 1/4 |

S1's picks are FWDRET/POS in 3 of 4 cells and PRICE/NEG in the fourth — i.e. the only selector
that beats doing nothing does so by picking a key that reads the future. **S2, the only
implementable selector, loses to doing nothing**, continuing the project's do-nothing streak.
References over the same window: SPY 15.45% / 0.8820 / −33.72%; RULES v1 (broad) 5.94% / 0.5763 /
−21.19% at 10 bps and (small) 6.35% / 0.4923 / −36.12%.

S2's one 4b pass is broad @10 bps, **DDTR/NEG/m0.50: OOS 14.69% / 0.9599 / −19.87%**. It is not a
candidate: DDTR's dSharpe there (+0.0519 mean) sits inside the null band and clears positively
0/12, and see the KEEP rate below.

## Both KEEP paths (all 748 arms)

| class | arms | 4a | 4b |
|---|---|---|---|
| control | 4 | 3 | 0 |
| leak-free | 144 | 68 | **6 (4.2%)** |
| level×volume | 24 | 4 | 0 |
| price level | 48 | 23 | **0** |
| oracle | 48 | 23 | 1 |
| **null keys** | 480 | 242 | **28 (5.8%)** |

The leak-free 4b rate (4.2%) is **below** the random-key rate (5.8%), and the 4a rate likewise
(47.2% vs 50.4%). Pre-registered prediction P7 ("no 4b pass among leak-free arms") is scored a
MISS, but the miss is not a find: a 4b pass at that frequency is what a random walk key delivers
on this panel. **No 4b pass at all among the price-level arms** — the family on trial.

## Predictions

P1 HIT (reproduction 4.4e-16) · P2 HIT (PRICE/NEG +0.2402 / +0.4663) · P3 HIT (DDTR carries far
under half) · P4 as stated (FROZEN +0.1633 small — 0/12 clearing-and-positive; DVOL +0.5777) ·
P5 HIT on the mechanism, order slightly off (DVOL leaks more than PRICE) · **P6 MISS — and that
is the run's finding** · P7 MISS, below the null rate.

## Reading

Idea 185 asked which of two artefacts explains the first selector in this project ever to beat
doing nothing. The answer is **neither**. The split horn was already closed analytically by idea
193's identity; the survivorship horn is closed here by measurement, in the wrong direction and
in 6 of 6 cells; and the leak-free version of the same economic idea is worth nothing. The
published +0.4086 OOS Sharpe of idea 181's PRICE/NEG selector is future information, full stop.
Nothing here changes RULES.md, and leg (c) remains open as idea 195 for a local run with a
shares-outstanding series.

### Caveats
* **SURVIVORSHIP is the subject, not a footnote.** Both panels are current-constituent lists
  (`data/SMALL_PANEL_README.md`, idea 54). Q3's cohorts are formed on full-sample drawdown and are
  therefore oracle-conditioned by construction: a diagnostic of the panel, never a book, and no
  level in Q3 is an attainable return. The panel contains no delisted names at all, so this test
  bounds the *within-survivor* gradient; it cannot price the names that left.
* Q4's forward-return IC uses the terminal date and is look-ahead by construction. That is the
  measurement; it is labelled, and no arm is selected on it.
* SPY is a benchmark column on the small panel, never a constituent; it carries no volume, so
  DVOL/VOLSH give it a neutral 0.5 rank (idea 193's convention, kept for comparability).
* Idea 38: `data/prices*.csv` are calendar-day indexed after 2014-09-17; it hits every arm and the
  control identically.
* Leg (c) MCAP is NOT RUN — no shares-outstanding series offline.
