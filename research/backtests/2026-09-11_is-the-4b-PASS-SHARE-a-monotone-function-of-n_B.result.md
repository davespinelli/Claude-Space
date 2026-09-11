# Idea 503 — is the 4b PASS SHARE a monotone function of n? (lane B, 2026-09-11)

**VERDICT: ANSWERED / SPLIT. KILL for capital.** The queue's conditional — *"if the share is
monotone in n, the record's 4b counts are not comparable across books of different size"* — has
its conclusion right and its antecedent wrong. In the record's **own** book form the share is
**not** monotone in n: it peaks and then collapses (B136 pooled 2.03% → 25.17% at n=30 → 16.67%
at n=40; at k=20 it runs 4.8% → 24.7% → 9.3% → **0.1% → 0.0% → 0.0%**). Once gross is held at
0.75 it **is** strictly monotone, **1.60% → 32.40%, a 20.25× span, Spearman exactly +1.0000**.
Either way the comparability conclusion stands, and harder than the queue asked: a published 4b
count without its n is uninterpretable, and the governing variable is **min(n, n_elig)**, not n.
No RULES change, no book promoted, no memo. `RULES.md`, `scan.py`, `bot.py`, `baseline.py`
untouched. Scripts `2026-09-11_is-the-4b-PASS-SHARE-a-monotone-function-of-n_B.py` (+`_addendum.py`).

Tuned parameters (PROTOCOL rule 4, max 2): **n** ∈ {5,10,15,20,30,40} and **panel** ∈ {B136,
SMALL484}. All 12 points printed and written to `.grid_summary.csv`. The sub-panel width k ∈
{20,40,80} and the book form are **reporting** axes — every point published. 10 bps, weekly,
next-day execution, no shorting, no leverage.

## Gates

- **[a]** `fast_backtest` vs `engine.backtest`, 6 books: max |Δret| **2.776e-17**. PASS.
- **[b] DIGIT GATE** — all **6,000 of 6,000** draw-rows merge against idea 486's committed grid,
  and this run's NOM n=5 / n=20 CAGR, Sharpe, MaxDD, H1, H2, OOS Sharpe, OOS CAGR, OOS MaxDD
  match it to **worst 2.220e-16**. The draws under test **are** idea 486's own. PASS.
- **[c] COUNT GATE** — idea 486's two published B136 counts reproduce **exactly**: n=5 **61/3000**
  (published 61), n=20 **747/3000** (published 747). PASS.
- Panel anchors: B136 SPY **15.2283% / 0.8890 / −33.7160%**, halves 0.9566/0.8340, OOS 0.8820
  (idea 83's published line, to the digit); 4b bars CAGR ≥ 10.66%, |MaxDD| ≤ 20.23% — idea 486's.
  SMALL484 bars 9.89% / 20.23%, also idea 486's.

## The two book forms (why the run has to publish both)

Idea 78/83/486's CAND-n book is `w = GROSS/n`. When fewer than n names are eligible it holds
`n_elig·GROSS/n < GROSS`: **the n dial is also a gross dial.** Realised gross, measured:

| panel | k | mean n_elig | n=5 | n=10 | n=15 | n=20 | n=30 | n=40 |
|---|---|---|---|---|---|---|---|---|
| B136 | 20 | 13.46 | 0.716 | 0.690 | 0.628 | 0.504 | 0.336 | **0.252** |
| B136 | 80 | 53.82 | 0.740 | 0.738 | 0.735 | 0.731 | 0.717 | 0.700 |
| SMALL484 | 20 | 6.13 | 0.642 | 0.447 | 0.304 | 0.228 | 0.152 | **0.114** |

So every number is published twice: **NOM** `w = GROSS/n` (idea 486's, verbatim — the form the
gates reproduce) and **MATCH** `w = GROSS/min(n, n_elig_t)` (same names, same ranks, gross held).

## PART A — the 12-point grid (3,000 draws per point)

**NOM — the record's own form**

| panel | n | 4b pass | share | med Sharpe | med MaxDD | med CAGR | med gross | 4a vs live v2 |
|---|---|---|---|---|---|---|---|---|
| B136 | 5 | 61 | 2.03% | 0.834 | −23.07% | 12.70% | 0.732 | 0 |
| B136 | 10 | 433 | 14.43% | 0.913 | −20.05% | 11.81% | 0.726 | 0 |
| B136 | 15 | 628 | 20.93% | 0.953 | −18.77% | 10.97% | 0.714 | 2 |
| B136 | 20 | **747** | **24.90%** | 0.973 | −17.91% | 10.40% | 0.697 | 21 |
| B136 | 30 | 755 | **25.17%** | 1.001 | −14.80% | 9.04% | 0.636 | 40 |
| B136 | 40 | 500 | **16.67%** | 1.013 | −11.93% | 6.94% | 0.505 | 72 |
| SMALL484 | all six | **0** | **0.00%** | 0.272–0.293 | −44.1%…−13.9% | 1.2%–3.5% | 0.229–0.719 | 0–3 |

**MATCH — gross held at 0.75**

| panel | n | 4b pass | share | med Sharpe | med MaxDD | med CAGR | 4a vs live v2 |
|---|---|---|---|---|---|---|---|
| B136 | 5 | 48 | 1.60% | 0.824 | −23.92% | 12.72% | **0** |
| B136 | 10 | 260 | 8.67% | 0.894 | −21.63% | 12.08% | **0** |
| B136 | 15 | 497 | 16.57% | 0.926 | −20.93% | 11.62% | **0** |
| B136 | 20 | 680 | 22.67% | 0.944 | −20.51% | 11.33% | **0** |
| B136 | 30 | 941 | 31.37% | 0.966 | −19.94% | 11.07% | **0** |
| B136 | 40 | 972 | **32.40%** | 0.974 | −19.75% | 10.90% | **0** |
| SMALL484 | all six | **0** | **0.00%** | 0.275–0.299 | −48.0%…−43.2% | 3.3%–3.8% | **0** |

**Monotonicity, pooled over the three k cells:**

| panel | form | Spearman(n, share) | strictly increasing | min → max | span |
|---|---|---|---|---|---|
| B136 | NOM | **+0.6571** | **NO** | 2.03% → 25.17% (argmax n=30) | 12.38× |
| B136 | MATCH | **+1.0000** | **YES** | 1.60% → 32.40% | **20.25×** |
| SMALL484 | both | n/a | n/a | 0.00% → 0.00% | — |

## PART A′ — per k cell, and what the share actually tracks (addendum)

4b pass share per 1,000-draw cell:

| panel | k | n_elig | NOM 5/10/15/20/30/40 | MATCH 5/10/15/20/30/40 |
|---|---|---|---|---|
| B136 | 20 | 13.46 | .048 .247 .093 **.001 .000 .000** | .038 .131 .170 **.173 .173 .173** |
| B136 | 40 | 26.93 | .009 .155 .399 .402 .039 **.000** | .008 .107 .233 .278 .274 .264 |
| B136 | 80 | 53.82 | .004 .031 .136 .344 .716 .500 | .002 .022 .094 .229 .494 **.535** |
| SMALL484 | all | 6.1–24.6 | **0 everywhere** | **0 everywhere** |

Spearman over the 18 (k, n) cell-points of a panel/form:

| panel | form | ρ vs **n** | ρ vs **min(n, n_elig)** | ρ vs realised gross |
|---|---|---|---|---|
| B136 | NOM | **−0.0283** | +0.4172 | +0.3382 |
| B136 | MATCH | +0.8325 | **+0.9201** | n/a (constant 0.75) |

**At the cell level the raw n dial carries no rank information at all (ρ = −0.028).** Only 1 of
12 cells is strictly increasing in n — B136 MATCH k=80, the single cell where n never reaches
n_elig. Where n does reach it, the dial stops: MATCH k=20 moves **0.0030** across all rungs at or
above n_elig (.173 at n=15, 20, 30, 40), k=40 moves 0.0100. That is the law: **the pass share is
monotone in min(n, n_elig), and n is only a dial while n < n_elig.**

## PART B — which 4b leg binds, by n

NOM B136, share of draws whose nearest bar is each leg (raw units): the binding bar **migrates
with n** — at n=5 it is H2 (51.4%) with CAGR at 0.1%; by n=40 it is CAGR at **86.2%** (z-units
97.4%) and DD has fallen to 0.4%. Under MATCH the migration is far weaker (CAGR 0.0% → 32.2%,
DD holds 16.9% → 31.2%). On SMALL484 the OOS Sharpe leg binds for 17–38% of draws at every n and
the **fail share is 1.000 everywhere** — no rung of any dial brings that panel near the bars.
So "which bar binds 4b" is not a property of 4b: it is a function of the book size **and** of
how much the book form de-grosses, which is idea 486's unit-dependence finding in a second guise.

## PART C — RULE 8 walk-forward (n chosen on 2009–2016 IS pass share only; 2017–2026 read once)

| panel | form | IS shares by n | pick | IS share | **OOS share** | med OOS CAGR/Sharpe/MaxDD | beat SPY | beat live v2 |
|---|---|---|---|---|---|---|---|---|
| B136 | NOM | .015 .086 .127 **.163** .120 .085 | **20** | 16.27% | **29.83%** | 10.49% / 0.970 / −17.91% | 83.5% | **10.4%** |
| B136 | MATCH | .010 .068 .120 .191 .230 **.248** | **40** | 24.83% | **31.03%** | 10.95% / 0.980 / −19.61% | 78.9% | **6.5%** |
| SMALL484 | NOM | .000 .001 .000 .000 .000 .000 | 10 | 0.07% | **0.00%** | 3.30% / 0.293 / −32.73% | 0.1% | 4.0% |
| SMALL484 | MATCH | all .000 | 5 | 0.00% | **0.00%** | 4.00% / 0.290 / −45.44% | 0.6% | 4.9% |

The chooser picks the **largest** n it is offered under MATCH (n=40) and n=20 under NOM — i.e.
in sample it buys exactly the confound. The base rate **rises** out of sample on B136 (16.3% →
29.8%, 24.8% → 31.0%), the opposite direction to idea 486's B136 halving, so the non-transfer it
reported is not signed. OOS comparands: SPY 0.8820, live RULES v2 **1.1185** (B136) / 0.6629
(SMALL484). **Books beating the live book out of sample: 10.4% and 6.5% on B136, ~4–5% on
SMALL484** — the live book is still above ~90% of every random draw at every n.
*Honest note:* the SMALL484 picks are degenerate — the IS share is 0.000 at every rung, so the
argmax is a tie broken by position, and those two rows carry no selection content.

## PART D — both KEEP paths on the rule-8 picked books, full sample, 10 bps

| panel | book | k | draw | CAGR | Sharpe | MaxDD | H1/H2 | OOS Sharpe | 4a | 4b |
|---|---|---|---|---|---|---|---|---|---|---|
| B136 | CAND-20 NOM | 20 | 253 | 9.99% | 1.4177 | −13.86% | 1.727/1.164 | 1.3063 | no | **no** (CAGR −0.67 pp) |
| B136 | CAND-40 MATCH | 20 | 253 | 16.28% | 1.3819 | −16.55% | 1.727/1.082 | 1.1941 | no | **pass** (DD +3.68 pp, CAGR +5.62 pp) |
| SMALL484 | CAND-10 NOM | 40 | 905 | 8.12% | 0.6048 | −42.95% | 1.073/0.222 | 0.3273 | no | no (all legs) |
| SMALL484 | CAND-5 MATCH | 20 | 922 | 5.92% | 0.3790 | −67.78% | 0.791/0.025 | −0.1369 | no | no (all legs) |

**4a 0/4, 4b 1/4, BOTH 0/4.** Over all 24 grid points × their draws (**72,000 book-rows**):
**4a 145/72,000, 4b 6,522/72,000, BOTH 3/72,000** — and the split by form is the finding:

| form | 4a vs live v2 | 4b | BOTH | rows |
|---|---|---|---|---|
| NOM (de-grossing) | **145** | 3,124 | **3** | 36,000 |
| MATCH (gross 0.75) | **0** | 3,398 | **0** | 36,000 |

**Every 4a pass in this run is in the de-grossing form; holding gross at 0.75 removes all 145.**
The live book's MaxDD leg is only ever cleared by books that stopped being invested.

**The one 4b passer is not promotable and gets no memo.** At k=20 with mean n_elig 13.46, the
`CAND-40 MATCH` book is `w = 0.75/min(40, n_elig)` on every eligible name — i.e. it *is*
equal-weight-all-eligible at gross 0.75 on a random 20-name slice, not a new book form. Its own
cell passes 4b at **17.3%** (one draw in six), it is one name list out of 3,000 selected by an
IS-Sharpe argmax on top of an IS-share argmax, and it fails 4a. It is the exact object idea 486
declined to promote, reproduced at a different n.

## What this establishes

1. **The queue's 12× gap is real and reproduces to the count** (61 and 747 of 3,000), but it is
   not a book-size effect alone: in the record's own form the share **peaks and collapses**
   (k=20: 24.7% at n=10 → 0.0% at n≥30) because `w = GROSS/n` de-grosses to 0.25 gross.
2. **At matched gross the share is strictly monotone and spans 20.25×** (1.60% → 32.40%).
   The queue's conclusion therefore holds: **every published 4b count needs its n**, and this
   run says it needs its **k / n_elig** too — the governing variable is min(n, n_elig).
3. **n is only a dial while n < n_elig.** Above that the pass share moves 0.003–0.010 across
   three rungs. Comparing a "CAND-40" count on a 20-name sub-panel to one on an 80-name
   sub-panel is comparing two different books with the same label.
4. **All 145 of this run's 4a passes are the gross loophole** (ideas 311/657): 0 survive at
   matched gross. 4a's MaxDD leg against the live book is an exposure test.
5. **SMALL484 is untouched by the n dial**: 0 of 36,000 book-rows clear 4b at any n, either
   form. Idea 486's zero was not an artefact of its two book sizes.
6. **The base rate does not transfer, and its direction is not signed**: it halved on B136 in
   idea 486 and roughly doubles here (16.3% → 29.8%). No in-sample base-rate correction is
   reusable.

## Caveats

- **Survivorship** (PROTOCOL rule 9): B136 and SMALL484 are current constituents; the random
  sub-panel draws inherit that bias in full. The B136 4b shares above are upper bounds.
- The MATCH form is **this run's construction**, not something the record has traded; it exists
  to strip the exposure confound out of the n dial and is reported beside NOM, never instead.
- `n_elig` is a **mean** over post-warm-up rebalance days; the saturation statement uses it as a
  scalar, while the actual eligible count varies day to day. The per-cell table is given so the
  reader can judge the saturation claim without that scalar.
- The 4b OOS leg is evaluated on 2017–2026 in PART A/D and re-based to the OOS window's own SPY
  bars in PART C; the two are not the same bar and are labelled separately.
- Only k ∈ {20,40,80} is swept — idea 486's ladder. A cell with n_elig far above 40 would extend
  the monotone region and is not measured here.
