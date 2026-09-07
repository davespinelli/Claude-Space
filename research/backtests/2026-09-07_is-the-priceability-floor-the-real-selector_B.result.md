# idea 379 — is-the-priceability-floor-the-real-selector (lane B, 2026-09-07)

**Verdict: KILL as a selector, one REPORT-ONLY PROTOCOL finding.** The 0.10 pp publication
floor does not choose books, does not choose instruments and does not hide a single capital
decision — but it is not neutral on the record's *orderings*, and it moves idea 124's own
published floor number on the broad panel.

Script: `2026-09-07_is-the-priceability-floor-the-real-selector_B.py` (161 s, deterministic).

## Design

The entire price grid is held fixed — idea 124's TOP-n ladder (TOP3/5/10/20/40/all) plus the
off-ladder V1u, on `universe.json`(56) and `universe_broad.json`(136), with idea 94's 16
instruments at the two published cost rungs: **448 arm-rows**. Only the publication rule
moves: `published(row) <=> dMaxDD > phi`, `phi` in {0.00, 0.05, 0.10, 0.25, 0.50} pp.
`admissible` (D1 cost-axis AND D2 window-axis AND D3 panel-draw axis at q=0.10, tau=0.90) is a
function of the returns and is therefore **constant across the sweep**; D3 is inherited
verbatim from idea 124's committed `d3.csv`. Two tuned parameters: `phi` (the subject axis,
all five points reported everywhere) and `cost` in {10, 25} bps (both reported everywhere).

Reproduction gates, all PASS: **G1** grid vs idea 124's committed `grid.csv`, 448 rows x 20
cols, max|diff| **1.776e-15**; **G2** published-row counts at phi=0.10 reproduce the queue's
own u56 ladder **[18, 12, 22, 22, 24, 24]** at **0.000e+00**; **G3** `adm_pub` curve
**5.551e-17** (`adm_all` 0.000e+00); **G4** idea 124's own gates carry through (ladder nests
idea 94's TOP20/EWall/V1u at 0.000e+00, `run()` == `engine.backtest` at 0.000e+00), and RULES
v2 on u56 reproduces its reference 8.66% / 1.2056 / -12.05%, halves 1.2259/1.1908.

## The answer to the queue's question

**4 of 12 book-level rankings are invariant to the floor. 12 of 12 keep the same argmin.**

| ranking | scope | INVARIANT | min spearman | max inversions | argmin stable | argmax stable |
|---|---|---|---|---|---|---|
| K0 `adm_all` (control) | u56 | **True** | 1.0000 | 0 | True | True |
| K0 `adm_all` (control) | broad | **True** | 1.0000 | 0 | True | True |
| K1 `adm_pub` (idea 124's floor curve) | u56 | False | 0.7207 | 3 | True | True |
| K1 `adm_pub` (idea 124's floor curve) | broad | False | 0.9643 | 1 | True | True |
| K3 median rate by book @10bps | u56 | **True** | 1.0000 | 0 | True | True |
| K3 median rate by book @25bps | u56 | **True** | 1.0000 | 0 | True | True |
| K3 median rate by book @10bps | broad | False | 0.9643 | 1 | True | **False** |
| K3 median rate by book @25bps | broad | False | 0.9643 | 1 | True | True |
| K4 arm menu (idea 94's 3 books) @10bps | pooled | False | 0.9648 | 4 | True | **False** |
| K4 arm menu (idea 94's 3 books) @25bps | pooled | False | **0.8637** | **9** | True | **False** |
| K4 arm menu (7-book ladder) @10bps | pooled | False | 0.9118 | **10** | True | True |
| K4 arm menu (7-book ladder) @25bps | pooled | False | 0.9912 | 2 | True | True |

The two invariant non-control rankings are both on u56 and both are the *book price* ordering
K3; on the broad panel even K3 moves. **P1 CONFIRMED** (the control is invariant, so the
harness is measuring the conditioning and nothing else). **P2 CONFIRMED** (K1 is invariant on
neither panel). **P3 REFUTED** — the prediction that idea 94's headline instrument menu could
not care about a 0.50 pp floor is wrong in 4 of 4 (cell-set, rung) combinations.

The row census behind it: total published rows fall **313 -> 296 -> 293 -> 281 -> 276 of 448**
as phi goes 0.00 -> 0.50. The floor is not a small perturbation on the narrow books (u56 TOP3
21 -> 17, TOP5 18 -> 12 between phi=0.00 and phi=0.05 alone) and near-inert on the wide ones
(u56 TOP40 and TOPall are 24 at every floor).

## What actually moves, by name

39 of 116 entry-slots move at all. The largest single move is **`abs12-dg` on idea 94's own
3-book menu at 25 bps: rank 13 (last, the most expensive instrument) at phi=0.10, rank 6 at
phi=0.25** — a 7-place move that changes which instrument the record calls dearest. Also
`ebud-0.20` 5 places on the 7-book ladder at 10 bps, `abs12-rw` 4, `TOP5` 3 places on idea
124's own u56 floor curve. The argmin — the *cheapest* instrument and the cheapest book — is
stable in every one of the 12 rankings at every floor: `band3-rw`/`ebud-0.10`/`ebud-0.20` at
the arm level, `V1u`/`TOP40` at the book level.

## The floor moves idea 124's own published number

K2, idea 124's `n*` (smallest ladder rung with `adm_pub` >= 90%):

| phi | n\*[u56] | n\*[broad] |
|---|---|---|
| 0.00 | 40 | 136 |
| 0.05 | 40 | 136 |
| 0.10 | 40 | 136 |
| **0.25** | 40 | **40** |
| **0.50** | 40 | **40** |

**P4 CONFIRMED.** u56's floor number is invariant at 40; the broad panel's is not. Idea 124
published "P4 REFUTED — n\* differs between panels, {u56: 40, broad: 136}, so PROTOCOL cannot
state a number." At phi >= 0.25 both panels read **40** and that refutation reverses. Idea
124's headline is therefore conditional on a publication constant nobody chose on evidence.

## Rule 8 walk-forward

**W1 (the curve itself).** Parameters on 2009-2016 only, 2017-2026 read untouched. Published
rows on u56 fall 162 -> 117 in-sample as phi rises while the OOS count is nearly flat 159 ->
145, i.e. the floor bites much harder in-sample. `n*_IS` is **never reached** on u56 at any
floor against `n*_OOS` of 10 (phi=0.00) then 5 (phi>=0.05); on broad `n*_IS` is 136 at every
floor while `n*_OOS` drops 136 -> **5** at phi >= 0.25. The floor number does not walk forward
at any setting, which is the same conclusion idea 124 reached, now shown to be floor-robust.

**W2 (the floor as a selector).** In each of the 28 (uni, book, cost) cells, `S1` = idea 94's
selector (IS reach >= 1.0 pp, then lowest IS rate — its filter sits above every floor tested,
so S1 is the phi-invariant control) and `S2` = the floor-only selector (published at phi on
IS, then lowest IS rate). Both picks read untouched on 2017-2026:

| phi | S2 picks changed vs incumbent | mean OOS Sharpe S1 | S2 | control (do nothing) | S2 - S1 | S2 - control | mean spearman(IS rate, OOS rate) |
|---|---|---|---|---|---|---|---|
| 0.00 | 5 / 28 | 0.8686 | 0.8743 | 0.8957 | +0.0057 | **-0.0214** | 0.1486 |
| 0.05 | 0 / 28 | 0.8686 | 0.8724 | 0.8957 | +0.0039 | **-0.0233** | 0.1421 |
| 0.10 | — | 0.8686 | 0.8724 | 0.8957 | +0.0039 | **-0.0233** | 0.1470 |
| 0.25 | 1 / 28 | 0.8686 | 0.8732 | 0.8957 | +0.0046 | **-0.0225** | 0.1637 |
| 0.50 | 3 / 28 | 0.8686 | 0.8705 | 0.8957 | +0.0019 | **-0.0253** | 0.1850 |

The floor moves 0 to 5 of 28 picks and the whole span of mean OOS Sharpe it commands is
**0.0038** (0.8705 to 0.8743). Head-to-heads are flat too: S2 beats its own control book in
14-15 of 28 cells, beats SPY in 16-17, and beats live RULES v2 in **1 of 28** at every floor.
Both selectors lose to doing nothing out of sample at every floor. **The floor is not the real
selector** — it selects rows, not returns. (The one direction that is monotone is
spearman(IS rate, OOS rate): 0.1486 -> 0.1850 as phi rises, i.e. a stiffer floor does buy a
slightly better-behaved ordering, but from 0.15 to 0.19 the price list is unusable either way.)

## KEEP paths

**4a: 0 of 448** arm-points beat live RULES v2 in both halves at no worse drawdown (111 of 448
beat the superseded RULES v1). **4b: 50 of 448.** No promotion.

The floor hides nothing that matters: at every phi in {0, 0.05, 0.10, 0.25, 0.50}, **50 of 50
4b passes and 0 of 0 4a-v2 passes are published**. Every 4b-clearing arm buys whole percentage
points of drawdown (range 2.26 to 13.03 pp), at least 4.5x the stiffest floor tested, so no
capital decision in this grid is ever made by the publication rule. That is the honest defence
of idea 94's floor and it is worth stating explicitly.

Best 4b-passing arm-points by OOS Sharpe (informational, nothing promoted): u56 TOP40 +
`band3-rw` @10bps 11.36% / 1.2112 / -15.66%, halves 1.2503/1.1861, OOS 1.2761 — this is the
by-product idea 124 already PARKed (`2026-09-07_top40-band3rw-u56_PARK_MEMO.md`) and it
reproduces here to 1.8e-15; it is a reproduction, not a new candidate. Then TOP40 `g200-dg`
(1.1763, OOS 1.2666), TOP40 `band3-dg` (1.1969, OOS 1.2609).

Reference bars: SPY 15.23% / 0.889 / -33.72%, halves 0.957/0.834, OOS 0.882. Live RULES v2 at
10 bps: u56 8.66% / 1.2056 / -12.05% (halves 1.2259/1.1908), broad 8.03% / 1.1058 / -12.24%
(halves 1.2291/0.9844).

## What PROTOCOL should carry (REPORT-ONLY, no rules change)

A published price ORDERING is a function of the publication floor as well as of the returns.
The floor is safe where the record uses it to name the *cheapest* instrument or book (argmin
stable in 12/12 rankings at every floor tested) and unsafe everywhere else: the *dearest*
instrument moves in 3 of 4 menus, `abs12-dg` by 7 places, and idea 124's `n*` on the broad
panel flips from 136 to 40 at phi = 0.25. Any row quoting a rank other than the minimum should
carry the floor it was read at. No new tuned parameter, no rules change, no KEEP.

SURVIVORSHIP: `universe.json` and `universe_broad.json` are current-constituent lists, so
every absolute CAGR here is optimistic. The subject of this run — which rows a publication
rule admits, and how a fixed ordering moves under it — is far less exposed than a level.
