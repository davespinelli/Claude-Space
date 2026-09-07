# Idea 139 — sleeve-moves-the-frontier

**Cloud, 2026-09-07.** Script `2026-09-07_sleeve-moves-the-frontier_cloud.py`, console
`…console.txt`, grid `…grid.csv` (432 rows), ladders `…ladders.csv` (684 rows, 3 windows),
cheapest-by-family `…cheapest_by_family.csv` (60 rows), walk-forward `…walkforward.csv`
(120 rows), selectors `…selectors.csv`, memo `…memo.md`.

## Verdict — **SPLIT. The queue's UNIQUENESS claim is KILLED; a 4b KEEP-candidate is filed as the by-product.**
- **KILL of "the first instrument that is not a point on the gross ladder".** On idea 74's own
  axis, at matched starting book and cost, the sleeve beats its own matched-drawdown ladder point
  in **97.9%** of priced arms — but so does the **3% band in 91.3%** and the **200d gate in
  90.9%**, and idea 94's *already committed* price list says the same thing (positive
  `vs_matchedDD` on 44 of its 48 gate rows). Being off the ladder is the normal case, not the
  sleeve's distinction. Worse for the claim: on the price itself the sleeve is **not even the
  cheapest** — over the 12 cells the cheapest family is `g200` **5**, `band3` **4**, sleeve **3**.
- **What IS true, and is new:** the sleeve is the only one of the four that buys its drawdown at
  **unchanged exposure** (mean gross 0.7502 against a control's 0.7502, max |diff| 0.0033 over all
  12 cells), where the gate's honest `-dg` form buys its drawdown by cutting gross to 0.53. And
  under rule 8 it is the only family whose IS-chosen arm clears 4b out of sample.
- **By-product (memo): a 4b KEEP-candidate** — `EWall + 25% S3 sleeve` at 0.75 gross, weekly,
  which clears all five 4b bars on **both panels at 10 and 25 bps** and is the rule-8 pick in
  **7 of 8** cells that admit anything, clearing all three OOS bars in **7 of 8**.

RULES.md, scan.py, bot.py, baseline.py and PROTOCOL.md untouched. No RULES change proposed here;
the candidate goes to Sunday review and is blocked on ideas 105/106 (sleeve RULES wording).

## Reproduction (nothing new was read until these passed)
- `H.run` (idea 94's simulator) equals `engine.backtest` at **0.000e+00** on TOP20@10 bps and
  EWall@25 bps.
- **idea 134's COMMITTED `ladder.csv` rebuilt from source: 100 of 100 rows** (R20, S3-10, S3-25,
  S4-10, S4-25 on both panels and both rungs), max |diff| over CAGR / Sharpe / MaxDD **2.22e-16**.
- **idea 94's COMMITTED `pricelist.csv` rebuilt from source: 48 of 48 rows** for the two
  comparands the queue names, max |diff| dCAGR 8.9e-16, dMaxDD 4.4e-16, **rate 1.0e-16**,
  vs_matchedDD 4.4e-16, gross **0.0e+00**. The axis this run prices the sleeve on is idea 74's,
  to machine precision, on every row idea 94 published.
- LIVE RULES v2 reproduces: u56 @10 bps 8.66% / 1.206 / −12.05%; broad 8.03% / 1.106 / −12.24%.

## Premise audit, in the queue's own words
On broad @10 bps with base book TOP20: **1 of 19** ladder points clears 4b (m = 0.10, a
CAGR-floor artefact of a near-cash book), Sharpe over the ladder **0.968–0.976** against the
queue's quoted 0.973–0.978 on its own coarser 5-point m = 0.60–1.40 grid — the queue's "no gross
level" reading holds on the rungs it quoted. Its second half needs one correction: **at native
gross only f = 0.25 passes 4b** (1 of 6 f-values, both asset sets); the "f ≥ 0.10 passes" rows in
idea 134's own committed grid are at **m = 0.80**, not at m = 1.00. Nothing in this run's answer
depends on which reading is used.

## (1) The price list — idea 74's axis, 432 rows, all committed
`rate` = pp of CAGR surrendered per pp of MaxDD bought vs the SAME base book at the SAME cost;
`lever` = rate / that book's own ladder slope (<1 = cheaper than holding less);
`vs_matchedDD` = the arm's CAGR minus the ladder's CAGR at the arm's OWN drawdown (>0 = not
reachable by de-grossing).

| family | n | priced | median rate | median lever | dominated | median vs_matchedDD | beats its ladder point |
|---|---|---|---|---|---|---|---|
| SLV3 (TLT/GLD/UUP) | 72 | 72 | **0.311** | **0.565** | 1.4% | +0.817 | **98.6%** |
| SLV4 (+DBC) | 72 | 72 | 0.337 | 0.611 | 2.8% | +0.635 | 97.2% |
| band3 | 24 | 23 | 0.344 | 0.627 | 8.7% | **+1.090** | 91.3% |
| g200 | 24 | 22 | 0.437 | 0.658 | 9.1% | +0.779 | 90.9% |
| DEGROSS (the reference) | 228 | 216 | 0.583 | **1.025** | 79.6% | 0.000 | 0.0% |

The DEGROSS row is the sanity check the design demands: the ladder prices at its own slope
(lever 1.025, the excess being its convexity) and beats itself by exactly 0.000 pp.

## (2) Is the sleeve a point on the gross ladder? No — and neither are the comparands
- By f, pooled over 12 cells and both asset sets: beats-its-ladder-point is **87.5% at f = 0.05**
  and **100% at f = 0.10 … 0.50**, with median vs_matchedDD rising monotonically
  **+0.21 → +1.58 pp/yr** and median lever rising 0.566 → 0.686. More sleeve buys more
  off-ladder content and pays more for it — a clean dial, not a corner.
- By panel x cost: 100% / 100% (broad @10, @25), 97.2% / 94.4% (u56) — this is not the broad-panel
  fact idea 134's claim was written about.
- By base book: EWall 100% (median +1.10 pp/yr), V1u 100% (+0.32), TOP20 93.8% (+0.87). The
  effect survives being blended into three different books, so it is a property of the sleeve,
  not of `R20`.

## (3) What the sleeve does that the gate and the band do not
Mean achieved gross, arm against its own control, all 12 cells: **sleeve 0.7501–0.7503 against a
control of 0.7471–0.7502** (max |diff| 0.0033), while the gate/band arms run **0.5320–0.7502** —
on EWall the `-dg` forms sit at 0.532, i.e. they buy their drawdown by holding 29% less. The
sleeve buys drawdown with **mix**, at the exposure the book already had. That, not "off the
ladder", is the property the queue was reaching for, and it is the one that survives.

## (4) Both KEEP paths, all 432 rows
- **4b vs SPY: 59 of 432 (13.7%)** — by family SLV3 **20**, SLV4 **15**, DEGROSS 10, band3 8,
  g200 6. Best rows are sleeve arms: `broad/EWall/SLV3-25 @10 bps` **11.93% / 1.2370 / −18.50%**
  (halves 1.372/1.118, OOS 1.196) and `u56/EWall/SLV3-25 @10 bps` **11.22% / 1.2331 / −16.67%**
  (halves 1.327/1.160, OOS 1.221).
- **4a vs the LIVE book (RULES v2): 9 of 432 (2.1%)**, and 8 of the 9 are DEGROSS rows on
  broad/EWall@25 bps whose halves are identical to each other (a gross-invariance artefact, not
  an instrument). The one real 4a row is `u56/EWall/SLV3-50 @10 bps` 8.91% / **1.3508** / −12.03%
  (halves 1.454/1.269, OOS 1.315) — it fails 4b on the CAGR floor. **0 rows pass both paths.**
- SPY: 15.23% / halves 0.957/0.834 / MaxDD −33.72%; bars CAGR ≥ 10.66%, MaxDD ≥ −20.23%.

## (5) Rule 8 — f, m and the family chosen on 2009–2016 alone, 2017–2026 read once (12 cells)

| selector | cells | mean OOS Sharpe | mean OOS CAGR | mean OOS MaxDD | OOS 4b pass | beats SPY | beats v2 |
|---|---|---|---|---|---|---|---|
| **S_4bIS** (IS-4b-admissible, argmax IS Sharpe) | 8 | **1.106** | 11.8% | −18.0% | **7/8** | 7 | 2 |
| S_4bIS_price (same set, argmin IS price) | 8 | 1.075 | 13.2% | −21.1% | **0/8** | 7 | 2 |
| S_price (cheapest insurance anywhere) | 12 | 0.865 | 10.5% | −21.5% | 0/12 | 7 | 2 |
| S_sharpe (argmax IS Sharpe, no screen) | 12 | 0.956 | 7.1% | −13.0% | 0/12 | 7 | 3 |
| S_fam:SLV3 / SLV4 (cheapest sleeve) | 12 / 12 | 0.863 / 0.865 | 10.4% | −21.7% | 0 / 1 | 7 / 7 | 2 / 2 |
| S_fam:band3 / g200 / DEGROSS | 6 / 8 / 12 | 1.119 / 0.928 / 0.850 | 13.3 / 9.7 / 2.3% | — | 6 / 4 / 0 | 6 / 6 / 7 | 0 / 0 / 1 |

SPY OOS 15.45% / 0.882 / −33.72%; RULES v2 OOS u56 1.267, broad 1.096.

Two findings here, and the second is the sharper one:
1. **S_4bIS picks a sleeve arm in 8 of 8 cells that admit anything** — never a gate, band or
   ladder arm — and picks **SLV3-25 in 7 of 8** (SLV3-20 in the eighth). It clears all three
   OOS 4b bars in **7 of 8**; the one failure is broad/TOP20 @25 bps (OOS Sharpe margin −0.049).
2. **The price axis is the wrong selector for capital.** Choosing from the *same* IS-admitted set
   by cheapest IS price instead of highest IS Sharpe picks the small-f arms and clears the OOS 4b
   bars **0 of 8** times. Idea 74's menu answers "what does insurance cost", not "what should be
   held" — and on this corpus the two answers are never the same arm.

## Caveats carried, not buried
- **The sleeve's edge is partly an asset-class fact about 2009–2026**, and this run measures it
  rather than waving at it: TLT full 1.14%/0.151 (IS 3.77%, **OOS −0.97%**), GLD 9.61%/0.626
  (IS 3.91%, **OOS 14.55%**), DBC 3.54%/0.284 (IS −3.15%, OOS 9.41%), UUP 1.64%/0.251. The
  momentum vote is what carries the blend across that reversal, but the result does not transport
  unconditionally to a sample where all four legs are dead at once.
- **Turnover roughly triples**: EWall control 0.83x/yr against SLV3-25 at 2.29x (u56) and 2.33x
  (broad). This is why the 25 bps rung is reported for every row, and the candidate still clears
  4b there.
- Survivorship (idea 54): current-constituent panels. The sleeve legs are index ETFs, so
  survivorship inflates the **equity** side of the blend — it works against the sleeve's measured
  price, not for it.
- Idea 128: the IS window cannot express deep drawdowns, so every IS price and every IS
  drawdown bar is measured on a short ruler. MaxDD is one number off one path and the price's
  denominator is a difference of two of them; arms buying < 0.10 pp get no price (NaN), as in
  idea 94 — **3 of 48** gate/band prices and 12 of 228 ladder prices are undefined (all 144
  sleeve arms are priced), and each is reported as such, never as a failure.
- SPY sits inside both panels and inside the EWall base book, and is also the benchmark
  (inherited from ideas 94/133); it applies identically to an arm and to its own control.
- The realised sleeve share is not exactly f: after the momentum vote and the rescale to 0.75
  gross it averages **0.248** (u56) / **0.222** (broad) at f = 0.25, with a 10–90 range of
  0.13–0.32 and no day at zero.
