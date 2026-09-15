# Idea 872 — publish BOTH CAGR floors beside every committed 4b claim (lane B, 2026-09-15)

**ANSWERED — SPLIT / KILL AS A SELECTOR, KEEP AS A COMPANION NUMBER. The re-score is ONE-WAY on
this corpus: 0 of 26 committed 4b passes are lost under the gross-matched floor and 9 are gained,
so no committed claim in the record NEEDS the matched floor to stand. What the matched floor does
change is the MARGIN: 5 of 26 committed passes (3 distinct books, all memo-backed SHELF) hold the
CAGR leg as their thinnest leg under PROTOCOL's floor at +0.63 to +0.76 pp/yr and hold +3.44 to
+5.19 pp/yr under the matched one — a 4.6×–8.2× re-reading of the same claim, which is exactly
the pair that must be published together. But it buys no capital: at the headline rung both floors
pick the SAME book ex ante, and at the one rung where they differ the matched floor picks WORSE
out of sample by −2.79 pp/yr CAGR and −0.275 Sharpe.** No PROTOCOL edit applied, no book promoted,
no RULES change; `RULES.md`, `PROTOCOL.md`, `scan.py`, `bot.py`, `baseline.py` untouched.

Script `2026-09-15_publish-BOTH-CAGR-FLOORS-beside-every-committed-4b-claim_B.py`.
**62 books** — the record's **8 memo-backed SHELF** books and the **54-book mechanical GRID**
ladder over three panels — `shelf_books()` / `grid_books()` / `small_grid()` **imported verbatim**
from the committed lane-C and idea-868 scripts rather than re-typed, so this run and 868 price the
same objects. × 3 claim sets × 3 floor forms × 2 cost rungs, weekly, t+1, **all 9 grid points and
all 18 walk-forward cells published**. Two tuned parameters, the queue's own: **claim set** and
**floor form**.

## The two floors, stated exactly

For a book holding gross `g_t` on day t (its own summed weight, t+1 aligned, cash at zero):

- **CURRENT** — PROTOCOL's floor: `0.70 × CAGR(SPY)`, SPY 100% invested every day.
- **CONST** — `0.70 × CAGR(ḡ · r_SPY)`, matched to the book's time-averaged exposure.
- **PATH** — `0.70 × CAGR(g_t · r_SPY)`, matched **day by day**. Headline pair: CURRENT vs PATH.

Claim sets: **MEMO8** (the record's literal memo-backed 4b claims), **PASS62** (every book the
CURRENT floor passes on the full sample — the mechanical restatement of "a committed 4b pass";
n = 26; **declared headline**), **ALL62** (all 62, not conditioned on the outcome).

## Gates — 5 of 5 PASS

**G1** 8 of 8 SHELF books reproduce their committed memo triples (worst |ΔCAGR| 0.30 pp,
|ΔSharpe| 0.0102) · **G2** the matched SPY at constant g = 1.00 ≡ SPY **0.000e+00** · **G3** the
PATH comparand's realised mean gross recovered back out of the series ≡ the book's own
**1.11e-16** · **G4** fast metrics ≡ `engine.metrics()` **2.22e-16** · **G5 CROSS-RUN 8 of 8
exact** — 868's published CAGR-leg counts at φ=0.70 rebuilt from this run's own arms (SHELF 8/8
under all three floors; GRID 27/54 CURRENT and 42/54 CONST and PATH) **and** its full-4b count
**18 → 27 of 54**.

## [2] H_ONEWAY **PASS**, 62 of 62 — the re-score cannot cost a claim

`floor_PATH ≤ floor_CURRENT` for every one of the 62 books (max realised ḡ **0.953**; a book
above 1.00 would be the exception and there is none). So for a long-only book that ever holds
cash the matched floor is strictly the **weaker** floor, and the re-score is one-way:

| | committed CURRENT passes LOST under PATH | FAILs GAINED |
|---|---|---|
| ALL62 | **0** | **9** |

**Which claims need which is therefore not a question about lost passes.** It is a question about
the 9 MATCHED-ONLY claims and about the margin the other 26 carry.

## [3] All 9 grid points (claim set × floor form), both rungs

4b pass counts; `cagrleg_binding` = books the CAGR leg alone rejects.

| claim set | floor | 10 bps pass / binding | 25 bps pass / binding | median margin 10 bps |
|---|---|---|---|---|
| MEMO8 (8) | CURRENT | 8 / 0 | 7 / 1 | +2.68 pp |
| MEMO8 | CONST | 8 / 0 | 8 / 0 | +4.44 pp |
| MEMO8 | PATH | 8 / 0 | 8 / 0 | +5.07 pp |
| PASS62 (26) | CURRENT | 26 / 0 | 21 / 3 | +2.47 pp |
| PASS62 | CONST | 26 / 0 | 22 / 0 | +3.97 pp |
| PASS62 | PATH | 26 / 0 | 22 / 0 | +3.90 pp |
| ALL62 (62) | CURRENT | 26 / 27 | 21 / 34 | +0.67 pp |
| ALL62 | CONST | 35 / 12 | 31 / 15 | +3.08 pp |
| ALL62 | PATH | 35 / 12 | 31 / 12 | +3.40 pp |

`pass_4a` is **0 at every one of the 18 cells** — not one of the 62 books clears path 4a against
live RULES v2 on the full sample. The floor question is a 4b question only.

## [4] H_MOVES **FAIL** — 14.5%, bar 20%

4b verdicts differing CURRENT vs PATH: **MEMO8 0 of 8 (0.0%)**, **PASS62 0 of 26 (0.0%)**,
**ALL62 9 of 62 (14.5%)**. The floor form moves nothing the record has actually claimed.

## [5] H_NEEDBOTH **PASS** — ρ +0.728 on ALL62, and **+0.085 on the committed passes**

| claim set | ρ(margin_CURRENT, margin_PATH) | ρ(ḡ, margin_CURRENT) | ρ(ḡ, margin_PATH) |
|---|---|---|---|
| MEMO8 | +0.500 | +0.167 | **−0.690** |
| **PASS62** | **+0.085** | **+0.534** | **−0.572** |
| ALL62 | +0.728 | +0.465 | −0.105 |

868's finding restates and sharpens: on the set the record actually claims, the two floors rank
the claims **almost independently** (ρ +0.085), and the sign of the gross loading **flips**
(+0.534 → −0.572). Under PROTOCOL's floor a book is rewarded for holding more; under the matched
floor it is penalised for it. They are two questions, as the queue said.

## [6] The deliverable — both floors beside every claim

Full table in `.claims.csv` (all 62 books, both floors, both margins, binding legs, class).
Classification, with each 4b leg's slack normalised by that leg's own spread across the 62-book
corpus (CAGR 0.0338, DD 0.0738, H1 0.2417, H2 0.3203 — computed once and stated):

| class | ALL62 | PASS62 |
|---|---|---|
| BOTH-FLOOR-FREE (pass both, CAGR leg not thinnest) | 21 | 21 |
| BOTH-CAGR-BOUND (pass both, CAGR leg thinnest) | 5 | **5** |
| MATCHED-ONLY (fail CURRENT, pass PATH) | 9 | — |
| NEITHER | 27 | — |

**The 5 BOTH-CAGR-BOUND rows are the claims that need both floors printed** — 3 distinct books,
all memo-backed SHELF (two appear twice because the GRID ladder rebuilds them):

| book | ḡ | CAGR | floor CURRENT | margin | floor PATH | margin | ratio |
|---|---|---|---|---|---|---|---|
| `u56-band008-gross100` (= `U56-band0.08-g1.00`) | 0.663 | 11.22% | 10.59% | **+0.63 pp** | 6.03% | **+5.19 pp** | 8.2× |
| `u56-marsrespread-gross075` | 0.735 | 11.34% | 10.59% | **+0.75 pp** | 7.89% | **+3.44 pp** | 4.6× |
| `u56-v2band-gross100` (= `U56-band0.03-g1.00`) | 0.695 | 11.35% | 10.59% | **+0.76 pp** | 6.40% | **+4.95 pp** | 6.5× |

These three memos publish a 4b pass whose thinnest leg is a **0.63–0.76 pp/yr** CAGR margin
against a floor the book was never built to clear — and a **3.44–5.19 pp/yr** margin against the
exposure it actually held. A reader given one number and not the other reads a different claim.
Each of the three fails the CURRENT floor's CAGR leg at 25 bps, so the margin is inside the
record's own cost dial.

**The 9 MATCHED-ONLY claims** — true only under the matched floor, and never quotable without it —
are 868's flippers exactly: `{U56,B136}-band{0.03,0.08}-g{0.50,0.75}` plus `B136-band0.03-g1.00`,
realised ḡ **0.332–0.703**, compounding at **5.27%–10.58% against SPY's 15.13%**. They beat their
own exposure and lose to the index by 5–10 pp/yr.

## [7] Rule 8 walk-forward — does publishing both floors change a CAPITAL decision? **Mostly no**

Selection on **IS ≤ 2016-12-31 only**; evaluation on **OOS > 2016-12-31, untouched**. Ex-ante
selector declared before running: among books clearing 4b **on the IS window** under that floor
form, take the largest IS CAGR margin under that same floor form; ties by name. All 18 cells in
`.walkforward.csv`.

**H_PICK FAIL at the headline cell** — PASS62 / 10 bps: CURRENT and PATH both pick
`b136-r620-gross065-W`. Across the 6 (claim set × rung) cells the two floors pick the **same book
3 times**; the 3 disagreements are all at 25 bps, and there the matched floor picks worse:

| rung | CURRENT pick | OOS CAGR / Sharpe | PATH pick | OOS CAGR / Sharpe | Δ |
|---|---|---|---|---|---|
| 10 bps | `b136-r620-gross065-W` | 14.52% / 1.040 | same | 14.52% / 1.040 | 0.00 pp |
| 25 bps | `u56-quantile50-respread-M` | 15.35% / 1.192 | `b136-r620-gross065-W` | 12.56% / 0.917 | **−2.79 pp** |

The matched floor widens IS eligibility 2.3× (PASS62: 4 → 9 books at 10 bps, 3 → 7 at 25 bps;
ALL62: 5 → 21) and that extra eligibility buys **zero** OOS CAGR at 10 bps and **−2.79 pp/yr**
at 25 bps.

**OOS table for the headline pick, `b136-r620-gross065-W` (identical under all three floors):**

| | CAGR | Sharpe | MaxDD | H1 / H2 |
|---|---|---|---|---|
| **book OOS 2017-2026** | **14.52%** | **1.040** | **−19.43%** | 1.117 / 0.962 |
| SPY OOS | 15.33% | 0.877 | −33.72% | 0.980 / 0.765 |
| RULES v2 (live) OOS | 7.88% | 1.108 | −12.18% | 1.282 / 0.904 |
| book IS 2009-2016 | 15.56% | 1.254 | −10.15% | 0.982 / 1.604 |
| book FULL | 14.99% | 1.126 | −19.43% | 1.343 / 0.956 |

**OOS verdicts: 4b PASS under CURRENT and under PATH (no leg fails); 4a FAIL** — the book loses
both OOS half-Sharpes to live RULES v2 (1.117 vs 1.282, 0.962 vs 0.904 — H1 fails) and runs a
−19.43% drawdown against the baseline's −12.18%. **H_WF over all 18 cells: OOS 4a 0/18, OOS
4b(CURRENT) 18/18, OOS 4b(PATH) 18/18.**

`b136-r620-gross065-W` and `u56-quantile50-respread-M` are both already memo-backed SHELF books
(`2026-09-12_b136-r620-gross065-W_4b_C_MEMO.md`, `2026-09-11_u56-quantile50-respread-M_4b_B_MEMO.md`),
so this run promotes nothing new and writes no memo.

## Verdict

| hypothesis | bar | reading | |
|---|---|---|---|
| H_ONEWAY | 62 of 62 | 62 of 62; 0 passes lost, 9 gained | **PASS** |
| H_MOVES | ≥ 20% of ALL62 | 14.5% (0% on MEMO8 and PASS62) | **FAIL** |
| H_NEEDBOTH | ρ < 0.90 | +0.728 ALL62, **+0.085 PASS62**, gross loading flips sign | **PASS** |
| H_PICK | different books ex ante | identical at the headline; differ at 3 of 6 cells | **FAIL** |
| H_WF | a KEEP path OOS | 4b 18/18 both floors, 4a 0/18 | reported |

**KILL the matched floor as a SELECTOR.** It cannot rescue a committed claim (one-way, 0 lost),
it moves no claim the record has made (0 of 26), it picks the same book ex ante at the headline
rung, and where it does pick differently it picks −2.79 pp/yr worse out of sample. 868 killed the
swap; this run kills the selector too, on the ex-ante evidence 868 did not have.

**KEEP it as a published COMPANION number** — the pair, not the swap. The two floors rank the
record's own committed passes at ρ **+0.085** with **opposite** gross loadings, and 5 of 26
committed passes (3 distinct memo-backed books) sit on a **0.63–0.76 pp/yr** CURRENT margin that
reads **3.44–5.19 pp/yr** matched. Those three memos are unreadable with one number.

**PROTOCOL line PROPOSED, not applied** (rule 6 — Sunday review, one change per week):

> *Every published 4b claim states BOTH CAGR floors: `0.70 × CAGR(SPY)` and
> `0.70 × CAGR(g_t · r_SPY)` on the book's own realised gross path, with the margin in pp/yr
> against each. The **CURRENT** floor remains the binding one — the matched floor is reported,
> never substituted.*

Costs 2 numbers per claim; changes 0 verdicts on the record as it stands; and stops a 0.63 pp/yr
margin being read as the same object as a 5.19 pp/yr one.

**SURVIVORSHIP:** U56 / B136 / SMALL are current-constituent lists; the small panel additionally
drops every ticker with `max_1d_move ≥ 1.0` per `data/small_meta.csv`. Every CAGR **level** above
is optimistic — for the books and for both comparands. The headline quantities are same-tape
margin **differences** and a difference of two ex-ante **selections**; the rule-8 table reads
levels and is exposed in full.
