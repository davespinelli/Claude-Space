# Idea 651 — which MATCHED-GROSS claims in the record are SHARPE claims? — **KILL** (2026-09-10, cloud)

Script: `research/backtests/2026-09-10_which-MATCHED-GROSS-claims-in-the-record-are-SHARPE-claims_cloud.py`
Outputs: `.sites.csv` (every claim site), `.census.csv`, `.grid.csv` (216 points), `.ladder.csv`
(504 points), `.walkforward.csv` (18 picks), `.console.txt`.
Two tuned parameters and no more: CLAIMSET (COMMITTED / ALL) and MATCHTYPE (NATIVE / SCALAR /
RESPREAD). Cost rung (10, 25 bps), panel, book, metric and the k-ladder are reported at every
point, never chosen. Costs 10/25 bps per unit turnover, next-day execution (PROTOCOL 2).

## 1. Answer

**88.0% of the record's Sharpe-bar matched-gross claims rest on a match measured to be
Sharpe-inert.** The phrase is doing real work on the CAGR and MaxDD bars and almost none on the
Sharpe bar, and the record does not distinguish the two.

## 2. Census (PART A)

| CLAIMSET | sites | files | mentions | SHARPE-bar sites | of those SCALAR or UNSTATED |
|---|---|---|---|---|---|
| COMMITTED (LEADERBOARD/QUEUE/CHANGELOG/PROTOCOL + every `*.result.md`) | 508 | 100 | 635 | 184 | **162 (88.0%)** |
| ALL (+ `.py` docstrings, `.console.txt`) | 1233 | 275 | 1380 | 245 | **222 (90.6%)** |

COMMITTED breakdown (bar x match type named in the claim's own text):

```
type    SCALAR  RESPREAD  BOTH  UNSTATED
DD           6         0     1        20
NOBAR       19         4     0       229
RETURN      16         0     0        29
SHARPE      63        10    12        99
```

Only **22 of 184** committed Sharpe-bar sites (12.0%) name a re-spread construction — the only
match type measured below to be able to move Sharpe. **99 of 184 (53.8%) name no construction at
all**: a reader cannot tell from the claim which match was run. The Sharpe sites concentrate in
the three top-level files (LEADERBOARD 65, QUEUE 50, CHANGELOG 47) — i.e. in exactly the prose a
future run reads as settled.

## 3. Measurement (PART B) — what each match type can do

12 books x 3 panels (U56, B136, SMALL439) x 2 rungs. Gates: `fast_backtest` reproduces
`engine.backtest` to 1.4e-17; `dg_weights(BAND3,0.75)` is bit-identical to
`baseline.rules_v2_weights`; RESPREAD == NATIVE exactly for EW_ALL and all 7 ranked books
(no gated weight to re-spread) and differs for the gate books (max |dw| 0.360).

| match | n | max &#124;dSharpe&#124; | median | mean dCAGR | mean dMaxDD |
|---|---|---|---|---|---|
| SCALAR (IS-fitted k, gross 0.75 -> ~0.52) | 72 | **0.0039** | 0.0004 | **-2.12 pp/yr** | +5.46 pp |
| SCALAR, k-ladder 0.25..0.875, all books | 432 | **0.0113** | 0.0006 | -3.83 pp/yr | — |
| RESPREAD, gate books only | 24 | **0.1215** | 0.0365 | +1.14 pp/yr | -3.99 pp |

The fitted-k arm reproduces idea 462's 0.0036 bound (0.0039 here on a wider arm set). The ladder
shows the neutrality is not k-specific: |dSharpe| falls monotonically with k, 0.0113 at k=0.25
down to 0.0017 at k=0.875, while |dCAGR| runs to 12.9 pp. **A scalar exposure match is a
first-order move in return and drawdown and a third-decimal move in Sharpe.**

Within-panel book ORDERING on Sharpe (66 pairs x 6 cells): SCALAR flips **2/396 (0.5%)** and
keeps the full 12-book ordering identical in 4/6 cells; RESPREAD flips **24/396 (6.1%)** and
keeps it in **0/6**. On U56 at 10 bps the re-spread changes the top book (RULESV2 -> TOP40); the
scalar never changes a top book anywhere.

## 4. KEEP paths and rule 8

**4a: 0/216** — no arm, in any match type, beats the live RULES v2 on both halves at no worse
MaxDD. **4b: NATIVE 7/72, SCALAR 3/72, RESPREAD 16/72.** This is the sting in the census: the
match is Sharpe-inert but *not verdict-inert* — because 4b also carries a CAGR floor and a DD
cap, a scalar "control" more than halves the 4b count and a re-spread more than doubles it,
entirely through the two bars the match does move.

Rule 8 (choose on IS <= 2016-12-31 by IS Sharpe, read 2017-01-01.. once), 18 picks:

* The rule-8 **pick is unchanged by a SCALAR match in 6/6 (panel, rung) cells** and by a
  RESPREAD match in 5/6 — the one exception is U56/10bps (TOP20 -> ABSdg).
* Picks beating native RULES v2 on OOS Sharpe: **6/18**; beating SPY on OOS Sharpe: **9/18**.
* Best OOS cell (U56, 10 bps, NATIVE, pick TOP20): OOS CAGR 15.7% / Sharpe 1.169 / MaxDD -19.4%
  vs RULES v2 9.5% / 1.279 / -12.1% and SPY 15.3% / 0.876 / -33.7%. Its SCALAR twin has the
  identical OOS Sharpe (1.169) on 11.3% CAGR and -14.3% MaxDD — the match moved 4.4 pp of CAGR
  and 5.1 pp of drawdown and 0.000 of Sharpe.
* SMALL439 picks are the weakest everywhere (OOS Sharpe 0.31-0.62, below both comparands).

No arm clears 4a; every 4b passer is an already-recorded exposure/concentration variant, not a
new instrument. **No KEEP, no memo, no RULES change.**

## 5. What this says about the record

A "matched on gross" control is only a control for the bar it can move. On Sharpe it is a
**no-op**: 162 of the record's 184 committed Sharpe-bar matched-gross claims are the *unmatched*
conclusion wearing a control's name, with a measured ceiling of 0.0113 Sharpe on what the match
could have contributed. On CAGR and MaxDD the same match is worth 2-4 pp/yr and 4-5 pp — which
is why it flips 4b counts while leaving Sharpe orderings alone. A candidate PROTOCOL line, for
Sunday review, not adopted here: *any claim that quotes a matched-gross control must name the
construction (scalar or re-spread) and the bar it is quoted on; a scalar match may not be
offered as the control for a Sharpe conclusion.*

SURVIVORSHIP (idea 54, carried): B136 and SMALL439 are current-constituent lists, so their
levels are biased upward and unequally so; only the within-panel, within-window
book-minus-its-own-twin contrasts here are load-bearing. SMALL439 drops the 44 sub-$2B names
with `max_1d_move >= 1.0` first. U56 is a fixed ETF/mega-cap list and is least biased.
