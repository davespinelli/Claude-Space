# Idea 868 — does the record's SHELF beat a GROSS-MATCHED SPY on the CAGR leg? (cloud, 2026-09-15)

**ANSWERED: YES ON THE SHELF (6 of 8, median +2.41 pp/yr) — BUT THE FLOOR NEVER BINDS THERE
(0 of 8), AND WHERE IT DOES BIND THE SWAP ADMITS BOOKS COMPOUNDING AT 5.3–10.6% AGAINST SPY'S
15.1%. KILL the swap; the two floors measure different things and the record needs both, not one
in place of the other.** No PROTOCOL edit applied, no book promoted, no RULES change;
`RULES.md`, `PROTOCOL.md`, `scan.py`, `bot.py`, `baseline.py` untouched.

Script `2026-09-15_does-the-record-s-SHELF-beat-a-GROSS-MATCHED-SPY-on-the-CAGR-LEG_cloud.py`.
**62 books** — the record's **8 memo-backed SHELF** books and a **54-book mechanical GRID**
ladder, both `shelf_books()`/`grid_books()` **imported verbatim** from the lane-C script committed
earlier today rather than re-typed, with the GRID extended to a third (small-cap) panel — × 3
comparand conventions × 6 floor fractions × 2 cost rungs, weekly, t+1, **all 2,232 verdict cells
published**. Two tuned parameters, the queue's own: **gross rung** and **floor fraction φ**.

## The comparand, stated exactly

For a book holding gross `g_t` on day t (its own summed weight, not its nominal parameter):

- **CURRENT** — PROTOCOL's floor: `0.70 × CAGR(SPY)`, SPY 100% invested every day.
- **CONST** — `0.70 × CAGR(ḡ · r_SPY)`, matched to the book's time-averaged exposure.
- **PATH** — `0.70 × CAGR(g_t · r_SPY)`, matched **day by day** to the book's own exposure.

Cash earns **zero** in both matched conventions — the record's own rf=0 convention, and idea 676
is why: crediting cash and then reading an rf=0 Sharpe pays cash-heavy books twice.

## Gates

**G1 8 of 8 SHELF books reproduce their committed memo triples** (max |ΔCAGR| 0.30 pp, max
|ΔSharpe| 0.010; `b136-r620-gross065-W` exact) · G2 the matched SPY at constant g=1.00 ≡ SPY
**0.000e+00** · G3 the PATH comparand's realised mean gross ≡ the book's own **0.000e+00** ·
G4 fast metrics ≡ `engine.metrics()` **0.000e+00**.

## [1] The title question — H_BEAT **PASS**, 6 of 8

| book | ḡ | book CAGR | its g×SPY | gap | SPY at 100% | gap |
|---|---|---|---|---|---|---|
| b136-r620-gross065-W | 0.650 | 14.99% | 10.01% | **+4.98%** | 15.16% | −0.18% |
| u56-quantile50-respread-M | 0.731 | 15.23% | 11.34% | **+3.89%** | 15.13% | +0.10% |
| u56-top20-band-m20 | 0.708 | 12.69% | 10.09% | **+2.61%** | 15.13% | −2.44% |
| u56-band008-gross100 | 0.663 | 11.22% | 8.62% | **+2.60%** | 15.13% | −3.91% |
| u56-v2band-gross100 | 0.695 | 11.35% | 9.14% | **+2.21%** | 15.13% | −3.78% |
| u56-marsrespread-gross075 | 0.735 | 11.34% | 11.28% | +0.06% | 15.13% | −3.79% |
| b136-qroll-q012-w1008-d050-g100 | 0.944 | 14.20% | 14.56% | −0.36% | 15.16% | −0.96% |
| u56-k8-qroll-q017-w1008-d100-g100 | 0.857 | 13.86% | 14.23% | −0.37% | 15.13% | −1.27% |

**6 of 8 beat their own gross-matched SPY (median +2.41 pp/yr) while only 1 of 8 beats SPY at
100%.** So the queue's suspicion is literally correct about the shelf: the floor is charging these
books for exposure they never held. Note the nominal grosses are *not* the realised ones — three
books labelled `gross100` hold 0.66–0.70 on average once their own gate is counted, which is
exactly why the PATH convention is the honest one.

## [2]–[3] And three things that make the swap the wrong fix

**1. THE FLOOR NEVER BINDS ON THE SHELF. H_FLIP FAIL: 0 of 8.** At φ=0.70, every shelf book
clears the *current* 100%-SPY floor — the binding-leg census is `H1 0/8, H2 0/8, OOS 0/8, DDCAP
0/8, **CAGRFLOOR 0/8**`. The defect the queue names is real in principle and **vacuous on the
object it was raised about**: no committed 4b candidate was ever rejected by this floor. The
swap changes **0** shelf verdicts and **9** GRID verdicts, all FAIL→PASS.

**2. IT IS THE MOST-BINDING LEG ON EVERYTHING ELSE, AND THE CONCESSION IS LARGE. H_FREE PASS,
+27.8 pp.** On the GRID the CAGR floor binds **27 of 54** — more than H1 (17), H2 (18), OOS (18)
or the DD cap (19). Swapping it lifts the CAGR-leg pass rate 0.500 → 0.778 and the full 4b count
**18 → 27 of 54** (10 bps; 21 → 31 of 62 at 25 bps). Full φ × convention ladder, all 18 cells per
set, is in `.ladder.csv`; at φ=1.00 the SHELF goes 0.125 → 0.750 and the GRID 0.000 → 0.296.

**3. WHO IT ADMITS.** The 9 flippers run realised gross **0.332–0.703 (mean 0.462, against 0.746
for the GRID and 0.748 for the shelf)** and compound at **5.27%–10.58% against SPY's 15.13%**.
Honesty requires the other half: **9 of 9 of them do beat their own gross-matched SPY** (median
+1.24 pp), so they are not free riders — they add real value *per unit of exposure taken*. But a
4b pass is a **capital** claim, and a book compounding at 5.6% while holding two-thirds cash is
not something to put capital in; the investor holds that cash themself. This is idea 676's
finding in a new place: **normalising a bar by a book's own gross pays it for exposure it
declined to take.**

## The mechanism — the two floors rank the same books in opposite orders

ρ(realised gross, gap vs its own g×SPY) = **−0.619** on the GRID; ρ(realised gross, gap vs SPY at
100%) = **+0.535**. By gross bucket, beats-its-own-g×SPY runs 5/9 (<0.50), 6/8 (0.50–0.70),
3/12 (0.70–0.85), 2/25 (>0.85). **The CAGR floor is doing two different jobs and they disagree by
construction**: *is this book better than passive at its own risk level* (the gross-matched
question) and *is this book worth real capital in absolute terms* (the 100%-SPY question). One
cannot be swapped for the other; the record needs both reported.

## The matched-gross control the title question needs

The SHELF sits at ḡ **0.748** and beats its own g×SPY in **6 of 8**. Unselected GRID books in the
**same 0.70–0.85 gross bucket** beat it in **3 of 12**. Over the whole ladder the GRID beats PATH
in **16 of 54** (median −0.43%) and SPY at 100% in **0 of 54** (median −4.38%); by panel U56 6/18,
B136 10/18, **SMALL 0/18**. So *"beats a gross-matched SPY" is not a property of this book family
— it is a property of the eight books that were already memo-selected for passing 4b.* The
title's YES is a selection result, and any PROTOCOL line built on it would be circular.

## [4] Rule 8 — H_WF **PASS but weak**, 38 of 62

Gap measured on 2009-2016 and read again on 2017+: sign stable in 38 of 62 books overall, but
only **32 of 54** on the GRID, where both medians sit at ≈0 (IS −0.27%, OOS −0.10%). The SHELF's
gap is stable and grows (IS +1.22% → OOS +2.96%, same sign 6 of 8, beats PATH 5/8 IS → 7/8 OOS) —
which is what a selected set does out of sample when the selection window overlaps the IS half.
Rule-8 chooser (best book per panel by IS Sharpe, 2017+ read once): U56
`u56-quantile50-respread-M` **15.90% / 1.230 / −19.46%** (SPY OOS CAGR 15.27%, RULES v2 OOS Sharpe
1.286; its own g×SPY 11.47%); B136 `b136-r620-gross065-W` 14.52% / 1.040 / −19.43% (SPY 15.33%,
v2 1.108; g×SPY 10.13%); SMALL `SMALL-band0.08-g1.00` 5.44% / 0.599 / −18.73% (SPY 15.33%, v2
0.559). **No pick beats SPY's OOS CAGR and none beats RULES v2's OOS Sharpe** — a KEEP path is
reached by none of the three.

## Verdict

**KILL the proposed swap** (and no PROTOCOL edit is applied or proposed for adoption). The
queue's premise is confirmed on the shelf and is inert there; where the floor actually binds, the
gross-matched version admits nine cash-heavy band books on a bar that is supposed to mean
"worth real capital". The durable finding is the decomposition, filed as follow-ups **872, 873,
874**: the CAGR floor conflates a per-unit-exposure question with an absolute-capital one, the two
rank the same 54 books at ρ = −0.619 vs +0.535, and both should be published beside every 4b
claim rather than one replacing the other.

**SURVIVORSHIP:** U56 / B136 / SMALL are current-constituent lists (the small panel additionally
drops the 52 tickers with `max_1d_move` ≥ 1.0 per `data/small_meta.csv`), so every CAGR level here
— the books' *and* the floor's — is optimistic. The book-minus-comparand GAP is a same-tape
difference and is the durable part; SMALL's 0-of-18 result is on a panel whose levels are the most
inflated of the three, which makes it the conservative reading, not the fragile one.
