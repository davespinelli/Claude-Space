# Idea 333 — does the B136 DRAWDOWN CAP admit ANY top-n book at all?

**KILL (premise falsified).** The 4b drawdown cap admits **19 of 20** top-n books on B136 at
10 bps; the joint (DD cap ∩ CAGR floor) gross band is **non-empty at all five n**; and three
cells clear the **full** 4b conjunction. The DD cap is not the binding bar on B136 — the
Sharpe bars are. Idea 329's DD failure was a **band** effect (m=20), not an n or gross effect:
its own m=0 anchor, reproduced here to 0.000e+00, clears the cap by 0.18 pp.

Script `2026-09-07_does-the-B136-drawdown-cap-admit-any-top-n-book_C.py`; console, grid,
Calmar, gross-interval and walk-forward CSVs alongside.

## Design (pre-registered, in the script's docstring before any number was read)

Family = idea 329's **anchor** arm, fixed: top-n of the v1 composite with the vol scaler OFF
among RULES v1 eligible names (200d MA up, vol20 < 0.60), NORM weights `w_i = g / k_t`,
`k_t = |{rank ≤ n}|`, band **m = 0**, **weekly**, next-day execution. Exactly two tuned
parameters — `n ∈ {10, 20, 40, 80, ALL}` × `gross ∈ {0.375, 0.50, 0.625, 0.75}` = 20 cells per
panel, **all 20 reported** at each of the three cost rungs {0, 10, 25} bps (the rung is a
reported axis, not a choice). B136 is the question's panel; U56 and SMALL439 run the identical
grid as context and cannot change the verdict. Decision rules R1 (DD region) → R2 (CAGR floor
inside it) → R3 (full 4b) were fixed in advance.

**Gates, all before any new number was read.** G1 `fast_backtest` vs `engine.backtest`
0.000e+00 on returns and turnover, and the derived 25 bps rung vs a live `cost_bps=25` run
0.000e+00. G2 `n=ALL` at 0.75 nests scored-eligible equal weight exactly (0.000e+00). G2b, a
**stated limitation rather than an assertion**: `n=ALL` is *not* plain eligible-equal-weight on
B136 — 390 name-days after 2009-01-13 are eligible but carry no composite (no 252d history),
max |dw| 2.4e-02; the family is rank-based, so "ALL" means "all *scored* eligible names"
throughout. G3, cross-run: the (B136, n=20, g=0.75) cell reproduces idea 329's committed grid
row (W, m=0) at |d| ≤ 1.1e-16 on CAGR/Sharpe/MaxDD/H1/H2/OOS — the two runs price the same
object.

## (1) The answer: the DD cap is not the B136 constraint

At 10 bps on B136 (cap −20.23%, floor 10.66% CAGR):

| region | count | cells |
|---|---|---|
| R1 DD cap alone | **19/20** | everything except (n=10, g=0.75), which misses by 0.0122 |
| R2 CAGR floor inside R1 | **6/19** | (10, .625), (20, .625), (20, .75), (40, .75), (80, .75), (ALL, .75) |
| R3 full 4b | **3/20** | (40, .75) 12.04%/0.989/−19.11% OOS 0.971; (80, .75) 11.20%/1.025/−18.44% OOS 1.044; (ALL, .75) 10.70%/1.025/−17.69% OOS 1.019 |

The queue's premise came from idea 329's *band* arm. The DD margin at the anchor (n=20,
g=0.75, m=0) is **+0.0018** — a pass — and idea 329's own m=20 cell is −0.0020, so the whole
DD failure it reported is the band's held-name drift, not the book's width or gross. Best
margin per bar over all 20 B136 cells: H1 +0.1867, H2 +0.1102, OOS +0.1641, DD +0.1110, CAGR
+0.0359 — **no bar is unclearable on B136**, and the tightest is the CAGR floor, not the DD cap.

## (2) The admissible (n, g) region, located rather than sampled

MaxDD and CAGR are near-linear in gross (cash earns 0; R² of each per-n fit ≥ 0.9987 on every
panel), so the two bars invert into a gross interval per n. On **B136 the band is non-empty at
5/5 n**: n=10 [0.558, 0.705], n=20 [0.614, 0.756], n=40 [0.664, 0.795], n=80 [0.714, 0.824],
ALL [0.747, 0.860] — width 0.11–0.15 of gross, narrowing and drifting UP as the book widens.
Only n=10's interval sits entirely inside the tested grid; the rest extend above 0.75 and are
flagged as extrapolation, not claimed. On **U56** it is likewise non-empty at 5/5. On
**SMALL439 it is empty at 5/5** (g_lo(CAGR) 0.975…2.188 above g_hi(DD) 0.333…0.461), which
**independently reproduces idea 326** by a different method.

## (3) The Calmar closed form is confirmed, and is what predicts (2)

4b's DD cap and CAGR floor combine into `Calmar ≥ (0.70/0.60) × Calmar_SPY` = 0.5269 (U56,
B136) and 0.4889 (SMALL439 — idea 326's number to four decimals). Empirically the bar is
**near** gross-invariant, not exactly: Calmar moves by at most **0.0198** across the four gross
settings (≤ 3% relative), rising with gross on B136/U56 and falling on SMALL439. The sign
prediction is perfect: every B136 cell tops the bar by +0.078…+0.138 and every U56 cell by
+0.117…+0.219, both with non-empty bands; every SMALL439 cell misses by −0.234…−0.397 with
empty bands — **15/15 agreement between "Calmar ≥ bar" and "some gross admits both bars"**.
Practical consequence: **the two bars are a ranking test, not a sizing test.** Gross moves a
book along a nearly fixed Calmar ray, so de-grossing can trade CAGR for drawdown but cannot
put a book over the joint bar; whether a joint region exists at all is decided before gross.

## (4) KEEP paths and rule 8

Grid-wide (3 panels × 20 cells): **4a 0/60 at every rung** — the live RULES v2 book's −12.05%
MaxDD dominates every cell here. **4b 13/60 at 0 bps, 5/60 at 10 bps, 0/60 at 25 bps.** The
five at 10 bps are B136 (40/80/ALL at g=0.75) and U56 (20 and 40 at g=0.75); breakevens 10.5–
21.5 bps, so the whole set dies before 25 bps.

Rule 8 (params chosen on 2008–2016 IS Sharpe at 10 bps, 2017–2026 read once):

| panel | IS pick | OOS Sharpe | vs SPY 0.882 | vs RULES v2 | regret |
|---|---|---|---|---|---|
| B136 | n=10, g=0.75 | 0.781 | **−0.101** | −0.338 (v2 1.119) | +0.266 |
| U56 | n=20, g=0.75 | **1.131** | +0.249 | −0.154 (v2 1.285) | +0.005 |
| SMALL439 | n=20, g=0.75 | 0.466 | −0.416 | −0.102 (v2 0.568) | +0.085 |

**On B136 the walk-forward chooser does not find the three 4b cells** — it picks the narrowest,
highest-gross book, which fails 4b on H2, OOS and DD and loses to SPY out of sample. So the
B136 4b passes are **PARK, not KEEP**: they exist, but no honest selector reaches them.

On U56 the IS chooser lands on the 4b-passing cell with regret +0.005, so **(U56, n=20,
g=0.75, m=0, weekly)** is a 4b KEEP-candidate under rule 8 — but it is a **re-measurement of a
family the record already holds** (idea 325's anchor / the record's top-20 composite books),
not a new object, and it carries **11.0×/yr turnover** against RULES v2's 1.77×, a DD margin of
only 1.9 pp, and a 21.5 bps breakeven. Memo:
`2026-09-07_u56-top20-g075-4b_C_MEMO.md`. Every rule-8 pick on all three panels still loses OOS
to the live RULES v2 book.

## Caveats

All three panels are current-constituent lists — **survivorship** — so CAGR levels are
optimistic and the CAGR floor is tested in the books' favour; a floor that fails here fails
harder on a survivorship-free panel. The 4a comparand always runs at its live weekly cadence
and gross, so the gross dial moves the idea arm only. SMALL439 starts 2010-01-04 (different
calendar halves) and drops the 44 tickers with `max_1d_move ≥ 1.0`.

## Follow-ups queued

383 (does the Calmar ray hold under a NON-cash de-gross), 384 (the band's DD tax priced across
the record), 385 (why the IS chooser prefers narrow-and-levered on B136 and wide on U56).
