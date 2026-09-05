# idea 218 — extend-the-three-degenerate-ladders-past-their-endpoints (lane C, 2026-09-05)

**VERDICT: ANSWERED — all three verdicts ARE truncation artefacts, and the extension is a KILL
for capital.** The IS argmax moves past idea 171's endpoint in **69.8% / 88.7% / 92.5%** of the 53
books (BAND / SLEEVE / GROSS, SEL-SHARPE), so on every one of the three dials idea 189's
"the argmax is the last ladder point" was a fact about **where idea 171 stopped the ladder**, not
about the dial. But the three fail apart once the wall is moved, and nothing tradable comes out.

## Reproduction, asserted before any new number was read
* `[a]` fast_backtest ≡ `engine.backtest` at all four cadences (idea 189's own check, called).
* `[b]` CAND-20 weights ≡ idea 78's `weights_cand` on three books.
* `[c]` the **1166 rows at the 22 ORIGINAL ladder points reproduce idea 189's committed
  `.ladder.csv` at 3.553e-15** over 12 numeric columns, with `fail4a` and `fail4b` identical in
  **100.0%**.
* `[c2]` its published truncated pick counts reproduce **exactly**: GROSS 1.00 in 50/53, BAND 0.08
  in 43/53, SLEEVE 0.30 in 53/53.

## The answer, dial by dial (SEL-SHARPE, 53 books, IS ≤ 2016 only)

| dial | old end | share@old | new end | share@new | moved past old | ext. mode (share) | reading |
|---|---|---|---|---|---|---|---|
| GROSS | 1.00 | 94.3% | 1.50 | **81.1%** | **92.5%** | 1.50 (81.1%) | runs to the NEW wall |
| BAND | 0.08 | 81.1% | 0.15 | 26.4% | 69.8% | **0.12** (30.2%) | **interior optimum** |
| SLEEVE | 0.30 | 100.0% | 0.50 | 22.6% | 88.7% | **0.45** (39.6%) | **interior optimum** |

**GROSS is not a dial.** Its full-sample Sharpe on U56 is **1.106–1.108 across the entire 0.2→1.5
range** and the corpus-mean IS Sharpe moves 0.952→0.958 (spread 0.006) while mean **OOS** Sharpe
*declines* 0.964→0.961. Gross is a scaling knob whose Sharpe is flat by construction; the argmax
is decided in the fourth decimal by cost drift, so it runs to whatever endpoint exists. What it
does move is CAGR (2.7%→19.6% OOS) and drawdown (−4.7%→−32.7% OOS) one-for-one, which is why 4b's
DD cap kills every levered point on U56 (fail4b = DD from g ≥ 0.90 upward).

**BAND and SLEEVE resolve.** The corpus-mean IS ladder now turns over inside the extension —
BAND argmax **0.12** (OOS argmax also 0.12), SLEEVE argmax **0.40** with IS falling at 0.50 — so
idea 171's endpoint concentration on these two was truncation and the real optimum is one to two
steps beyond it.

**The degeneracy is a SEL-SHARPE property, not a dial property.** Under the 4b-margin selector the
endpoint was never crowded on two of the three: GROSS 37.7% at the old endpoint (24.5% move),
SLEEVE 1.9% (1.9% move). Only BAND is degenerate under both selectors (69.8% at old, 60.4% move).

## The leverage control — the sharpest number in the run
The engine finances the residual at 0%, so the GROSS extension is borrowing for free. Charging a
flat rate daily on (gross − 1), nominal gross (a **lower bound** on the true charge):

| financing | IS pick distribution | share levered | share @1.50 | mean OOS Sharpe of the pick |
|---|---|---|---|---|
| 0%/yr | 1.5:43, 1.4:2, 1.3:1, 1.2:2, 1.1:1, ≤1.0:4 | **92.5%** | **81.1%** | 0.9617 |
| 2%/yr | 1.0:50, 0.9:1, 0.8:1, 0.6:1 | **0.0%** | 0.0% | 0.9633 |
| 5%/yr | 1.0:50, 0.9:1, 0.8:1, 0.6:1 | **0.0%** | 0.0% | 0.9633 |

**A 2%/yr borrow charge — below any real broker rate in either window — erases the entire GROSS
extension**, and the un-levered pick is *better* out of sample (0.9633 vs 0.9617).

## What the extension costs out of sample (paired, 53 books)

| contrast | GROSS | BAND | SLEEVE |
|---|---|---|---|
| SEL-EXT − SEL-TRUNC, OOS Sharpe | **−0.0016** (t −6.13, 8W/41L, p 0.0000) | −0.0005 (n.s., p 0.74) | **+0.0603** (t +12.56, 47W/0L) |
| SEL-EXT − SEL-TRUNC, OOS 4b margin | **−0.3579** (t −9.72) | −0.0070 (n.s.) | **−0.0541** (t −7.26, 1W/46L) |
| MODE-EXT-LOO − SEL-EXT, OOS Sharpe | −0.0005 (p 0.02) | **+0.0120** (t +2.64, p 0.0076) | +0.0004 (n.s.) |

SLEEVE is the only dial where the extension buys Sharpe, and it buys it with the 4b CAGR floor:
OOS CAGR falls 8.82% → 8.19% against SPY's 15.45%, and books whose OOS 4b margin is positive drop
**7/53 → 1/53**. Per family (the honest n is 3 families, not 53 books): SLEEVE +0.0320 U56 /
+0.0600 B136 / +0.1315 SMALL; GROSS −0.0007 / −0.0017 / +0.0016.

Idea 189's modal-constant result **reproduces on the widened ladder**: MODE-EXT-LOO beats SEL-EXT
on the one dial whose pick distribution is genuinely spread (BAND, +0.0120, p 0.0076) and ties it
where the selector barely deviates.

## Rule 8 walk-forward (all picks on ≤2016-12-31; 2017–2026 read once)
Pooled OOS Sharpe over 3 dials × 53 books: **ORACLE-EXT 1.0649 > MODE-EXT-LOO 1.0499 > SEL-EXT
1.0460 > MODE-TRUNC-LOO 1.0267 ≈ SEL-TRUNC 1.0265 > RANDOM-EXT 1.0140 > CONST 0.9638.**
OOS CAGR 12.79% / 12.36% / 10.79% / 10.70% / 10.00% / 9.96%; OOS MaxDD −20.75% / −20.18% /
−17.69% / −17.51% / −16.41% / −17.18%. **SPY OOS 15.45% / 0.8820 / −33.72%; RULES v1 OOS
7.73% / 0.7471 / −13.83% (U56), 5.94% / 0.5763 / −21.19% (broad), 19.31% / 0.6046 / −35.01%
(small).** The extension's +0.0195 of pooled Sharpe over SEL-TRUNC is bought with 2.67pp more
drawdown, and it is negative on the OOS 4b margin on two of the three dials.

## Both KEEP paths (all 1802 ladder rows, 0% financing)
* **4a 1406/1802, 4b 226/1802** (197 on sub-panels = corpus device, not tradable).
* On the **636 ADDED points only: 4a 393/636, 4b 64/636**; binding bars there CAGR 302, DD 268,
  H2 158, OOS 66, H1 56.
* **SMALL484: 0/34 pass 4b** — the fourteenth reproduction of idea 136.
* 29 fixed-panel 4b passes, **4 of them on added points**: U56 BAND 0.10 / 0.12 / 0.15 and
  BSTK100 SLEEVE 0.35. All are re-parameterisations of an existing book (idea 144). **None is
  proposed.** The best of them (U56 BAND=0.12: 13.8% / 1.149 / −18.2%, halves 1.138/1.162, OOS
  1.223 / 15.5% / −18.2%, turnover 7.7×/yr) passes 4a **and** 4b but is single-universe — B136 and
  BSTK100 BAND rows pass neither — which is idea 53's failure mode exactly. Memo'd, not proposed.
* Arm-level on fixed panels: CONST 3/15, SEL-TRUNC 4/15, **SEL-EXT 2/15**, MODE-TRUNC-LOO 3/15,
  **MODE-EXT-LOO 1/15**, RANDOM-EXT 2/15, ORACLE-EXT 1/15 — **extending the ladder REDUCES the
  number of 4b passes an arm lands on.**

## Predictions (all written before any number was read): 5 of 7 hit
P1 reproduction **HIT**. P2 SLEEVE moves past 0.30 in ≥90% **MISS (88.7% = 47/53** — a threshold
miss, no directional content). P3a GROSS@0% levered in ≥90% **HIT (92.5%)**. P3b GROSS@5% picks
≤1.00 in >50% **HIT (100.0%)**. P4 BAND new-endpoint share <80% **HIT (26.4%)**. P5 ≥2 of 3 dials
run to the new wall **MISS — only GROSS does (81.1%); BAND 26.4% and SLEEVE 22.6% resolve to
interior optima.** That miss is the informative one: I predicted monotonicity would simply
persist, and it persists only where Sharpe is flat by construction. P6 the extension fails to pay
OOS on ≥1 dial **HIT (GROSS −0.0016, BAND −0.0005)**. P7 no new fixed-panel 4b KEEP beyond
re-parameterisations — 29 rows, 4 on added points, all re-parameterisations, none proposed.

## Caveats carried
Leverage priced at 0% in the engine (hence the financing control, and no gross > 1.00 number at
the 0% rung is tradable). Survivorship on B136/U56/SMALL484 (idea 54) — paired comparisons
unaffected, levels not. Idea 144: a re-grossed/re-banded/re-sleeved book is the same book. Idea 38
(calendar-day index) and idea 126 (t+1) carry over. **The new endpoints are themselves walls**: on
GROSS the argmax sits on 1.50, so this run moved the truncation rather than removing it — stated,
not hidden. Idea 190 already killed the static sleeve as an asset choice; nothing here revives it.
Sub-panels of B136 are correlated draws, so the pooled t overstates: 3 families, not 53 books.

RULES.md, scan.py, bot.py and baseline.py untouched.
