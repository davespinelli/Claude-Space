# Idea 227 — is-the-top-decile-trim-a-drop-the-worst-rule (cloud lane, 2026-09-08)

**Verdict: SPLIT. The question is ANSWERED — the trim is the COMPOSITE, no single leg and no
vol20 screen reproduces it, and it is directionally a drop-the-worst rule. The trim is KILLED as
a 4b candidate: 4 of 8 turnover-matched RANDOM keys clear 4b at the same trim depth, nothing
clears at 25 bps, and 4a is 0 of 216. Idea 155's PARK does not survive its own null.**

Script: `2026-09-08_is-the-top-decile-trim-a-drop-the-worst-rule_cloud.py` (deterministic,
seed 227000, no network, 506 s, 396 books). Idea 155's construction: eligible = above the 200d
MA AND vol20 < 0.60; rank the eligible names by a key; hold the top `round(q·n_elig)` equally
weighted at 75% gross; weekly, t+1, 260-bar warm-up skip. **q = 1.00 is the ladder's own exact
EWall endpoint and is the do-nothing arm — at q = 1.00 every key holds the identical book.**

**Two tuned parameters, every grid point reported:** P1 trim depth q ∈ {0.75, 0.80, 0.85, 0.90,
0.95, 1.00}; P2 cost rung ∈ {0, 10, 25} bps (0 is a diagnostic, 10 is the protocol rung and the
only rung KEEP is read at). Eight keys are pre-registered treatment arms, not tuned; the 8
shuffle seeds are a null distribution reported as mean ± sd, never as a best draw.

**Reproduction:** the cost identity `net(c) = gross − turnover·c/1e4` holds at **0.000e+00**, and
idea 155's two published cells reproduce **exactly**: U56 q=0.90 @10 bps COMP premium **+0.0316**
(published +0.0316) and B136 q=0.95 **+0.0171** (published +0.0171).

---

## 1. Is it the composite ranking at all?  Yes — and only the composite.

Premium = Sharpe(q) − Sharpe(q=1.00), protocol rung 10 bps:

| panel | key | 0.75 | 0.80 | 0.85 | **0.90** | **0.95** |
|---|---|---|---|---|---|---|
| U56 | **COMP** | −0.0248 | +0.0078 | +0.0263 | **+0.0316** | +0.0031 |
| U56 | MOM | −0.0374 | −0.0553 | −0.0417 | −0.0376 | −0.0317 |
| U56 | R6 | −0.0074 | −0.0268 | −0.0339 | −0.0416 | −0.0306 |
| U56 | R3 | −0.0452 | −0.0286 | −0.0186 | −0.0250 | −0.0325 |
| U56 | VOL20 | −0.1386 | −0.1104 | −0.1151 | −0.0841 | −0.0342 |
| U56 | COMP-REV | −0.1724 | −0.1707 | −0.1488 | −0.0990 | −0.0516 |
| B136 | **COMP** | −0.0221 | −0.0154 | −0.0079 | +0.0072 | **+0.0171** |
| B136 | MOM | −0.0433 | −0.0337 | −0.0349 | −0.0461 | −0.0057 |
| B136 | R6 | −0.0125 | −0.0094 | −0.0106 | −0.0074 | −0.0145 |
| B136 | R3 | −0.0520 | −0.0551 | −0.0530 | −0.0181 | −0.0134 |
| B136 | VOL20 | −0.1333 | −0.1138 | −0.1021 | −0.0549 | −0.0256 |
| B136 | COMP-REV | −0.0739 | −0.0642 | −0.0638 | −0.0654 | −0.0418 |

**On both large-cap panels COMP is the ONLY key with a positive trim premium at the argmax q;
every one of its three legs is negative there.** The composite is not decomposable — the edge
lives in the combination, not in 12-1 momentum, the 6-month return or the 3-month return
separately. (R2 REFUTED: I predicted a leg would match or beat COMP.)

**VOL20 is the worst deterministic key on both large-cap panels** (−0.0841 U56, −0.0549 B136),
so the trim is not a hidden volatility screen. (R3 REFUTED — idea 330's "wins on vol" shape does
not appear in this instrument.)

SMALL439 is the exception and behaves nothing like the large-cap panels: at 10 bps COMP +0.0325,
R6 +0.0300, VOL20 +0.0288, MOM +0.0217 at q=0.90 — **nearly every key earns a trim premium
there**, which is what a thin, survivorship-selected panel looks like, and it clears 4b 0 of 72.

## 2. Is it a drop-the-worst rule?  Directionally yes — but the ranking's content is in the TOP.

`COMP-REV` (keep the names COMP would delete) is **negative on every panel, every q, every
rung**. The composite ordering is therefore monotone-informative. But the two sides are not
symmetric: at U56 q=0.90 @10 bps, **dropping the worst 10% earns +0.0316 while dropping the best
10% costs −0.0990 — a 3.1× asymmetry.** So idea 155's q=0.90 argmax *is* a drop-the-worst rule,
and that is exactly why it earns so little: the key's information is concentrated in the top
decile, which a q=0.90 book keeps by default. (R4 REFUTED — I predicted the reverse would be
*smaller*.)

## 3. Does the trim survive the key being DESTROYED?

Two nulls, 8 seeds each. **SHUF-S** draws one uniform key per *name*, constant over time, so its
turnover matches the real book (1.80× vs COMP's 1.93×) — this is the control that matters.
**SHUF-W** redraws every rebalance (3.16× turnover) and shows what the trim costs when a
meaningless key also churns.

| cell (10 bps) | COMP | SHUF-S null | excess | z | random keys beating COMP | SHUF-W null |
|---|---|---|---|---|---|---|
| U56 q=0.90 | +0.0316 | −0.0201 ± 0.0374 | **+0.0518** | +1.38 | **0 of 8** | −0.0799 (excess +0.1115) |
| B136 q=0.95 | +0.0171 | +0.0030 ± 0.0154 | **+0.0141** | +0.92 | **2 of 8** | −0.0307 (excess +0.0479) |

**The point estimate survives; the noise does not.** The turnover-matched null's own premium is
≈ 0 to slightly negative at every q on the large-cap panels (R1 REFUTED — trimming per se buys
nothing, so the premium is not a concentration effect), and COMP's excess over it is inside one
null sd on U56 and inside two seeds on B136. Mean z over the whole q ladder: COMP **+0.54**
(U56) and **+0.27** (B136); the only key with a large-magnitude z anywhere is COMP-REV at −2.79
/ −2.35, i.e. the record's cleanest signal here is the *reverse* trim being reliably bad.

## 4. The number that kills it: a MEANINGLESS key clears 4b about half the time

4b passes out of 8 seeds, same trim, same panel, same rung:

| panel | rung | null | 0.75 | 0.80 | 0.85 | 0.90 | 0.95 | 1.00 | COMP |
|---|---|---|---|---|---|---|---|---|---|
| U56 | 10 | SHUF-S | **5/8** | **5/8** | **4/8** | **4/8** | 1/8 | 0/8 | P P P P P · |
| U56 | 10 | SHUF-W | 0/8 | 0/8 | 0/8 | 0/8 | 0/8 | 0/8 | P P P P P · |
| U56 | 25 | both | 0/8 | 0/8 | 0/8 | 0/8 | 0/8 | 0/8 | · · · · · · |
| B136 | 10 | SHUF-S | 3/8 | 3/8 | 4/8 | 4/8 | 5/8 | 8/8 | · P P P P P |
| B136 | 25 | both | 0/8 | 0/8 | 0/8 | 0/8 | 0/8 | 0/8 | · · · · · · |
| SMALL439 | 10/25 | both | 0/8 | 0/8 | 0/8 | 0/8 | 0/8 | 0/8 | · · · · · · |

(B136's 8/8 at q=1.00 is by construction — at q=1.00 every key holds the same book.)

**At the protocol rung on U56 the 4b bar admits a turnover-matched random key in 4 of 8 draws at
exactly the trim depths where COMP passes.** A 4b pass at this trim depth is therefore not
evidence about the key.

Why the pass exists at all: **U56 q=1.00 fails 4b on the CAGR floor alone** (10.395% vs the
10.66% bar, a 0.27pp miss); the trim adds +0.9pp of CAGR and crosses it. Across all 216
deterministic cells the CAGR floor binds on 187 of them — the fourth independent reproduction of
idea 330's premise that the CAGR floor is the bar doing the work.

## 5. Rule 8 walk-forward, and both KEEP paths

(key, q) chosen on IS ≤ 2016-12-31 by IS Sharpe, 2017–2026 read once. Published as ROOM and
REGRET beside the margin, per the clause idea 445 drafted earlier today.

| panel | cost | IS pick | OOS pick | OOS S0 | MARGIN | OOS best | REGRET | ROOM | OOS argmax |
|---|---|---|---|---|---|---|---|---|---|
| U56 | 10 | COMP@0.90 | 1.126 | 1.113 | +0.0130 | 1.138 | 0.0121 | +0.0250 | COMP@0.85 |
| U56 | 25 | COMP@0.90 | 0.993 | 0.989 | +0.0044 | 0.999 | 0.0062 | +0.0106 | COMP@0.85 |
| B136 | 10 | COMP@0.95 | 1.024 | 1.019 | +0.0045 | 1.033 | 0.0098 | +0.0144 | R3@0.90 |
| B136 | 25 | COMP@0.95 | 0.896 | 0.896 | −0.0000 | 0.896 | 0.0000 | +0.0000 | COMP@1.00 |
| SMALL439 | 10 | VOL20@0.80 | 0.271 | 0.288 | −0.0173 | 0.349 | 0.0781 | +0.0608 | R6@0.75 |
| SMALL439 | 25 | VOL20@0.80 | 0.085 | 0.133 | −0.0482 | 0.183 | 0.0985 | +0.0502 | COMP@0.80 |

Pooled over 6 cells: **MARGIN −0.00727, REGRET 0.03410, ROOM +0.02683**; the chooser beats
do-nothing in 3 of 6. The IS chooser does land on COMP@0.90 / COMP@0.95 — the full-sample
argmaxes — on the large-cap panels, so the trim is at least IS-stable there.

OOS CAGR / Sharpe / MaxDD, chooser vs do-nothing vs SPY:

| cell | pick | do-nothing (q=1.00) | SPY |
|---|---|---|---|
| U56 @10 | 12.14% / 1.126 / −16.79% | 11.34% / 1.113 / −15.87% | 15.45% / 0.882 / −33.72% |
| U56 @25 | 10.56% / 0.993 / −16.95% | 9.95% / 0.989 / −16.11% | 15.45% / 0.882 / −33.72% |
| B136 @10 | 10.85% / 1.024 / −17.76% | 10.59% / 1.019 / −17.69% | 15.45% / 0.882 / −33.72% |
| SMALL439 @10 | 2.80% / 0.271 / −42.63% | 3.11% / 0.288 / −40.22% | 15.45% / 0.882 / −33.72% |
| SMALL439 @25 | 0.22% / 0.085 / −44.84% | 0.88% / 0.133 / −42.21% | 15.45% / 0.882 / −33.72% |

**KEEP paths over the 216 deterministic cells: 4a (vs live RULES v2) 0 of 216. 4b (vs SPY) 27 of
216 — U56 10/72, B136 17/72, SMALL439 0/72. Both paths: 0.** Every 4b pass is at 10 bps; nothing
survives 25 bps. On B136 the untrimmed q=1.00 control passes 4b too, so the trim adds nothing
there; on U56 the pass rests entirely on the CAGR floor, at a trim depth where half the random
keys also pass. **No KEEP candidate, and no memo.**

Full-sample numbers for the best cell, for the record: U56 COMP q=0.90 @10 bps
**11.30% / 1.081 / −16.79%, halves 1.114 / 1.054, OOS 12.14% / 1.126 / −16.79%**, against SPY
15.23% / 0.889 / −33.72% (halves 0.959 / 0.834, OOS 15.45% / 0.882) and RULES v2 @10 bps
8.66% / 1.206 / −12.05%.

## Predictions vs outcomes

| | prediction | outcome |
|---|---|---|
| R1 | the turnover-matched null earns a positive trim premium (concentration effect) | **REFUTED** — SHUF-S premium ≈ 0 / slightly negative at every q on large caps |
| R2 | a leg (R3 or R6) matches or beats COMP | **REFUTED** — COMP is the only positive key at the argmax q on both large-cap panels |
| R3 | VOL20 beats every return key on Sharpe | **REFUTED** — VOL20 is the worst deterministic key on both large-cap panels |
| R4 | COMP-REV negative but smaller than COMP is positive | **REFUTED** — COMP-REV is 3.1× larger in magnitude |
| R5 | no 4b KEEP survives rule 8 | **CONFIRMED in substance** — 27/216 cells pass 4b at 10 bps, but 4 of 8 random keys pass the same cells, and 0 pass at 25 bps; 4a 0 of 216 |

Four of five pre-registered predictions were wrong, which is worth stating plainly: the priors
this record has built up about vol terms and leg-decomposability did not transfer to this
instrument.

## Caveats

* q < 1 changes the *number* of names held as well as which ones (33.5 vs 37.4 at U56 q=0.90 vs
  1.00), so every trim is partly a concentration effect; SHUF-S is the control for exactly that
  and is reported beside every key.
* Premiums are differences of Sharpe ratios on overlapping samples and are not independent
  across q; no significance is claimed from the ladder's shape, only against the null.
* 8 seeds is a coarse null: a "0 of 8" is an upper bound of roughly 1-in-3 at 95% confidence,
  not a p-value. The verdict rests on the 4-of-8 4b base rate, which needs no fine resolution.
* VOL20 trims inside an already vol-capped eligible set (vol20 < 0.60), so it is not an
  independent volatility book.
* SMALL439 is a **current-constituents** panel (`data/SMALL_PANEL_README.md`) with
  `max_1d_move >= 1.0` tickers dropped: **survivorship bias**, a shape check only, never a
  tradable return.
* 10 bps is the protocol rung and the only rung KEEP is read at; 0 bps is a diagnostic.
