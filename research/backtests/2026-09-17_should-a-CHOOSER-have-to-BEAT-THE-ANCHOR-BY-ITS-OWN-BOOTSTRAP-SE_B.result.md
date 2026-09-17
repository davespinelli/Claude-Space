# Idea 1210 (lane B, 2026-09-17) — should a CHOOSER have to BEAT THE ANCHOR BY ITS OWN BOOTSTRAP SE rather than merely OUTRANK IT?

**VERDICT: KILL (capital). ANSWERED = NO — the SE bar is a DIMMER SWITCH BETWEEN TWO CONTROLS THE RECORD ALREADY HAS, and the "18 capital-worthy books" it was asked to recover are ONE book.**

Script `2026-09-17_should-a-CHOOSER-have-to-BEAT-THE-ANCHOR-BY-ITS-OWN-BOOTSTRAP-SE_B.py`, 51s,
offline, **gates 12 of 12**. Dials, both named by the queue and both fully published: `k`
{0, 0.25, 0.5, 1.0, 1.5, 2.0} x `SE basis` {SE_BLOCK, SE_IID, SE_FOLD} = **18 cells, every one
reported**. Headline `k = 1.0 x SE_BLOCK`, declared before any number. Everything else — 3
panels x 2 anchors x 4 ladders x 3 choosers = 1154's SAME 72 decisions, CAND20 legs, max_vol
0.60, min hold 126, 10 bps (rule 2), LAG 1, warm-up 260, IS end 2016-12-31, 1000 draws — is
1101/1154's, inherited whole and not re-tuned. The BLOCK basis uses **1154's own seeds**, so
`P_pick` and therefore R_BAR are its rows to the bit.

## 1. The rule was an interpolation between the two controls before any tape was read

Declared in Arm 0, gated after:

- `k = 0` → `d = stat(argmax) − stat(anchor) ≥ 0` at **all 72** decisions by the definition of
  argmax (**G9**, 0.000e+00), so **R_SE(0) ≡ R_RAW** — selections identical at 72 x 3 bases
  (**G5**, 0.000e+00).
- `k = ∞` → **R_SE(∞) ≡ R_ANCHOR**, 1155's do-nothing — identical at 72 x 3 bases (**G6**).
- Move count is **non-increasing in k at every basis** (**G11**): 72 → 60 → 54 → 41 → 32 → 22
  (SE_BLOCK); effective moves (excluding the no-op where the argmax IS the anchor) 59 → 9.

So the falsifier was fixed in advance and is not a post-hoc reading: **only an INTERIOR k
beating BOTH endpoints** would make the SE bar a rule rather than a re-labelling.

## 2. It does not. 0 of 3 bases, 18 of 18 cells inside the endpoints

Mean OOS Sharpe over the 72 walk-forward selections (pick on 2009–2016 alone, 2017–2026 read
once):

| basis | k=0 (≡R_RAW) | 0.25 | 0.5 | 1.0 | 1.5 | 2.0 | ∞ (≡R_ANCHOR) | interior > both? |
|---|---|---|---|---|---|---|---|---|
| SE_BLOCK | 0.7996 | 0.7895 | 0.7829 | **0.7870** | 0.7942 | 0.7899 | 0.7901 | **False** |
| SE_IID | 0.7996 | 0.7895 | 0.7819 | 0.7891 | 0.7911 | 0.7894 | 0.7901 | **False** |
| SE_FOLD | 0.7996 | 0.7971 | 0.7916 | 0.7889 | 0.7895 | 0.7803 | 0.7901 | **False** |

Every interior cell in the whole grid lies in **[0.7803, 0.7971]**, i.e. strictly inside the two
endpoints (0.7901 / 0.7996). The **argmax over all 18 cells is k = 0**, which is R_RAW itself.
Comparands (1154's, reproduced): R_RAW 0.7996 / R_BAR 0.7887 / R_ANCHOR 0.7901, 4b-full 6 / 19 /
24 — **cross-run gate G8 at 4.542e-07**.

Paired against the do-nothing control on the SAME 72 decisions, SE clustered on the **6**
(panel, anchor) clusters — which is the honest cluster count and is small:

- best R_SE cell in the grid: **k = 0 (= R_RAW), +0.0095, clustered SE 0.0198, t +0.48** — and
  that is a maximum over 18 cells, so even its own t is optimistic.
- every interior cell: **−0.0098 to +0.0041**, all |t| ≤ 2.06.
- the **only** reading in the entire grid that reaches 2 SE is `R_SE[SE_BLOCK, k=2.0]` at
  **−0.0002, t −2.06** — i.e. the one resolved statement the SE bar produces says the bar
  **costs** rather than buys. It is a −2e-04 effect and is reported at that size.

Headline `R_SE[SE_BLOCK, k=1.0]`: moves 28 of 72, mean OOS Sharpe **0.7870** / CAGR **0.1075** /
MaxDD **−0.2360**, paired **−0.0031, SE 0.0103, t −0.30**. It is behind doing nothing.

## 3. The queue's "18 capital-worthy books" are ONE book — the count was of DECISION ROWS

1154's 4b-full counts (6 / 19 / 24 of 72) are counts of **decision rows**, and R_ANCHOR selects
the same anchor rung at all 12 (ladder, chooser) decisions of a (panel, anchor). In **distinct
books** (**G12**: R_ANCHOR's 72 selections are exactly 6 books):

| rule | 4b-full ROWS | 4b-full DISTINCT BOOKS | distinct books selected |
|---|---|---|---|
| R_RAW | 6 | **3** | 48 |
| R_BAR | 19 | **2** | 17 |
| R_ANCHOR | 24 | **2** | 6 |
| R_SE, all 18 cells | 6–21 | **2–3** | 14–48 |

- R_ANCHOR's 24 rows are **2 books**: `U56|20|126|0.75|W`, `U56|12|63|0.55|M`.
- R_RAW's 6 rows are **3 books**: `U56|20|126|0.75|W`, `U56|12|126|0.55|M`, `U56|12|252|0.55|M`.
- **The gap is ONE book**, `U56|12|63|0.55|M` — not 18. And the framing was one-sided: R_RAW
  finds **two** 4b books R_ANCHOR never reaches, which the "the habit loses 18" reading hides.
- Every R_SE cell at k ≥ 0.25 on every basis recovers that one book — **by not moving off it**,
  which R_BAR and R_ANCHOR already do for free.
- **0 of 18 cells** produce a single 4b book that neither control found.

## 4. Declared, then refuted by the tape: the SE ordering is not what it should be

Arm 0 predicted SE_IID < SE_BLOCK < SE_FOLD (iid understates serial dependence; folds add
between-year variance). Realised, over the 59 decisions where the argmax is not the anchor:

- `SE_IID ≤ SE_BLOCK` at only **0.3750** of decisions — the naive basis reads **larger**, not
  smaller, because a joint iid redraw destroys the cross-rung path co-movement that keeps the
  DIFFERENCE tight.
- **SE_FOLD has the SMALLEST median (0.013200** vs SE_BLOCK 0.020937, SE_IID 0.029165**)** and
  the largest t's (median 1.1898, max 15.2242, 0.4068 of decisions at t ≥ 2), because a
  difference that is consistent year to year has a tiny SE of its fold mean. The basis added to
  be conservative is the **loosest** one. The prediction is published as made and as refuted.

And the third reading is not orthogonal to the two the record has: Spearman(t_SE_BLOCK, P_pick)
**+0.4633**, Spearman(t_SE_BLOCK, IS margin) **+0.3666**, against Spearman(margin, P_pick)
**0.1551** (1154's, reproduced exactly). The SE t-statistic is a **blend** of the rank bar and
the margin column, more correlated with each than they are with each other — not a new
dimension of evidence.

## 5. KEEP paths (protocol rule 4), nothing selected on

144 distinct rung books, both paths on every one:

- **4a: 0 of 144.** At every cell. The live RULES v2 book's MaxDD (−12.05% U56) is not matched
  by any rung book here.
- **4b full 20 of 144; 4b OOS 24; BOTH 19** — U56 14/17, B136 6/7, **SMALL 0/0**.
- The 19 both-readings books are **set-identical to 1154's 19** (verified book-for-book):
  **prior art, recorded and not promoted. No memo, no candidate from this run.**

Per-panel comparands (rule 3): SPY 0.1506/0.8814/−0.3372 (U56, OOS 0.1515/0.8684/−0.3372);
RULES v2 live 0.0860/1.1980/−0.1205 (U56, OOS 0.0942/1.2714/−0.1205).

## 6. Gates (12 of 12)

G1 fast runner ≡ `engine.backtest` 1.388e-17 · G2 1101's committed U56 anchor-A triple 1.622e-03
· G3 live RULES v2 U56 MaxDD ≡ −12.05% 4.949e-05 · G4 SPY OOS triple 2.894e-03 · **G5** R_SE(0) ≡
R_RAW at 72x3 · **G6** R_SE(∞) ≡ R_ANCHOR at 72x3 · **G7** degenerate pair (pick book = anchor
book) → d and SE(d) **exactly 0 on all three bases**, which is the gate that would have caught an
independent draw leaking into the joint index · G8d bootstrap determinism 0 · **G8** cross-run
1154's three rules' mean OOS Sharpe AND 4b counts 4.542e-07 · G9 d ≥ 0 at all 72 · **G11** move
count non-increasing in k at every basis · **G12** R_ANCHOR's 72 selections = exactly 6 books.

## 7. Survivorship and declared approximations

Rule 9: U56 and B136 are **current-constituent** lists; SMALL is the current output of a sub-$2B
screen less 52 of 715 names on `max_1d_move ≥ 1.0`. Every LEVEL is optimistic and every 4a/4b
count is an **upper bound**; the rule comparison is a DIFFERENCE between selections on the same
panel and is far less exposed.

1. SE_BLOCK and SE_IID resample ONE tape, so they price sampling error around THIS regime, not
   regime uncertainty. Both **understate** SE(d), which makes R_SE move MORE than it should —
   the direction that **favours** the record's habit. A cell this run calls no better than doing
   nothing is no better a fortiori.
2. The 72 decisions are not 72 independent draws; they share panels, anchors and books. **6
   clusters is a small number of clusters** and a t near 2 on 6 clusters is not a 95% statement.
3. The best R_SE cell is a maximum over 18 and is published as a ceiling, never as a pick.

## 8. What this leaves for the queue

The finding that generalises is not about the SE bar: it is that **a publishing rule's score in
DECISION ROWS is not its score in BOOKS**, and the two diverge by an order of magnitude exactly
where the rule declines to move (R_ANCHOR: 24 rows, 2 books; R_BAR: 19 rows, 2 books). Any of the
record's committed "rule A finds N more capital-worthy books than rule B" sentences that counts
rows rather than distinct books is inflated by the (ladder x chooser) multiplicity of the anchor.
