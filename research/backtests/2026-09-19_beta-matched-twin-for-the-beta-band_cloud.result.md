# Idea 1436 — is the BETA BAND's 4b DD GAIN anything more than a BETA-MATCHED EXPOSURE DIAL?

**2026-09-19, lane cloud. VERDICT: ANSWERED NO — KILL (capital). No new book, no RULES change.**

Idea 1429 shut the DOLLAR exposure channel to <1e-12 and still widened U56's binding 4b
drawdown margin from the frozen incumbent's +1.1028 pp to +1.83..+4.40 pp — but its realised
book beta fell and its own PARK memo named the repair it did not run: *"a BETA-MATCHED twin."*
This is that twin. 1429's committed script is **imported, not re-typed**, so drift between the
two runs is impossible; G1a replays the committed U56 anchor to 3.7e-05 of Sharpe and G1b
replays its +1.1028 pp DD margin exactly.

## The two controls

Both hold the identical names on the identical rows as the cell and are solved segment by
segment against the cell's own realised NAV beta `b* = sum_i w_i beta_i`:

| | ranking bits read | gross | beta |
|---|---|---|---|
| **CELL** (1429's band) | all n ranks | pinned 0.75 | free (falls with c) |
| **TWIN-G** beta-matched de-gross | **zero** | free, clipped to [0, 0.75] | matched to the cell |
| **TWIN-B** beta-matched barbell | **one** (side of the median) | pinned 0.75 | matched to the cell |

At c = 0 both twins are bit-identical to the frozen incumbent to 4.5e-17 — by algebra, asserted
not assumed (G3). Beta match exact to 8.9e-16 (G2). TWIN-B's gross pinned to 3.3e-16 (G7a) and
clips at 0 of 56,520 segments; TWIN-G never levers (G7b) and clips at 2,895 of 56,520 (5.12%).

## Result 1 — the pure exposure dial wins the drawdown leg 48 of 48

Handed the cell's own beta and nothing else, a plain de-gross of the anchor draws down **less
than the beta band at every one of the 48 biting cells on all three panels.** On U56:

| | 4b DD margin (pp) | mean gross | turnover/yr | drag (bp/yr) | CAGR |
|---|---|---|---|---|---|
| frozen anchor (c=0) | +1.1028 | 0.7500 | 2.87 | 28.7 | 15.80% |
| **CELL** (band) | +1.8329 .. +4.4039 | 0.7500 | 3.02 .. 9.89 | 30.2 .. 98.9 | 12.01 .. 14.97% |
| **TWIN-G** (de-gross) | **+2.0664 .. +7.0996** | 0.4538 .. 0.6981 | 2.24 .. 3.61 | 22.4 .. 36.1 | 9.10 .. 14.61% |
| **TWIN-B** (barbell) | +1.7022 .. +4.6408 | 0.7500 | 3.23 .. 11.15 | 32.3 .. 111.5 | 12.29 .. 15.09% |

The band recovers at most 62% of the drawdown its own beta reduction is worth, and pays more
capital and more turnover for it. It is the same object as the trailing stop (1405), the breadth
throttle (1413) and the convention blend (1423) — an exposure dial in costume — except more
expensive: it pins DOLLAR gross and spends the exposure cut in BETA instead, which PROTOCOL's
4b DD cap cannot tell apart. Anchor NAV beta 0.7621 (= 0.75 x 1429's stock-side 1.0162); cell
0.4887..0.6997; both twins reproduce it to machine precision.

## Result 2 — one bit of beta reproduces all n bits

On U56 the median-split barbell beats the CELL on Sharpe at **16 of 16** cells (1.0784–1.1666 vs
1.0585–1.1568) and on OOS Sharpe at **16 of 16** (1.1690–1.2303 vs 1.1222–1.2040), matches it on
drawdown (cell ahead at 10 of 16, **|t| on MaxDD 0 of 16**), and clears 4b full and OOS at 16 of
16. On B136 |t| on MaxDD is likewise **0 of 16**. The fine n-way ranking 1429's rule reads is
worth nothing over knowing which half of the book a name sits in.

## The pre-registered bar (stated in the script header before any number was read)

Name-level only if on U56 (i) the cell's DD margin beats BOTH twins at a majority of the 16
biting cells — **0 of 16**; (ii) |t| > 2 on MaxDD vs TWIN-B at >= 1 cell — **0 of 16**;
(iii) 4b passes full and OOS there — 16/16. **(i) and (ii) fail: KILL.**

## Rule 8 (walk-forward, chooser-matched across all three arms)

(c, B) chosen by argmax IS Sharpe on warm-up..2016-12-31; 2017–2026 read ONCE.

| panel | arm | IS pick | OOS CAGR | OOS Sharpe | OOS MaxDD | 4b OOS |
|---|---|---|---|---|---|---|
| U56 | CELL / TWIN-G / TWIN-B | c=0 (the anchor), all three | 17.32% | 1.1857 | -19.13% | yes |
| B136 | CELL / TWIN-G / TWIN-B | c=0, all three | 16.19% | 1.0180 | -20.74% | no |
| SMALL | CELL | c=1.00, B=126 | 10.21% | 0.6385 | -31.38% | no |
| SMALL | TWIN-G | c=0 | 6.70% | 0.4398 | -36.51% | no |
| SMALL | TWIN-B | c=1.00, B=126 | 9.86% | 0.6148 | -36.07% | no |

SPY OOS 15.26% / 0.8738 / -33.72%. **4a: 0 of 180 books.**

## The one thing that survives, and where

The band's only non-beta content is on SMALL, on RETURN and not on drawdown: at matched beta the
cell beats TWIN-G on Sharpe by +0.0517..+0.2340 with **|t| > 2 at 12 of 16** — on the one panel
whose 4b DD leg fails by 16.28 pp at the anchor and at every cell. Beta information resolves only
where it cannot carry capital, exactly as 1433's vol information did. **The beta family is closed
on the drawdown leg.**

## Survivorship (rule 9)

U56 and B136 are current-constituent lists; SMALL is a current sub-$2B screen carried back to
2010 (483 names after the protocol-mandated `max_1d_move >= 1.0` drop from `data/small_meta.csv`).
Every absolute level is an upper bound and every 4b pass an optimistic one. What this run reads is
a contrast between three weightings of the same names on the same days at the same NAV beta, which
the bias cannot manufacture — but cannot cure either.

Artifacts: `.grid.csv` (60 cells x 3 arms), `.walkforward.csv` (9 rows), `.gates.csv`, `.log.txt`.
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py untouched.
