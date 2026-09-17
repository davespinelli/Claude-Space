# Idea 1190 (lane B, 2026-09-17) — is a SUB-TAPE FIGURE's JACKKNIFE SE WIDER THAN ITS OWN LADDER SPREAD AT EVERY CELL?

**ANSWER = NO, NOT AT EVERY CELL — AND THE QUESTION HAS NO SINGLE ANSWER, BECAUSE "ITS OWN JACKKNIFE SE" IS AT LEAST FOUR DIFFERENT NUMBERS THAT DISAGREE BY 16.8x.**
**VERDICT: KILL as a capital finding.** No new candidate, no memo. Gates 14 of 14. Runtime 61 s.

Script `2026-09-17_is-a-SUB-TAPE-FIGURE-s-JACKKNIFE-SE-WIDER-THAN-ITS-OWN-LADDER-SPREAD-AT-EVERY-CELL_B.py`.
Two tuned dials, both named by the queue: **RUNG COUNT** K ∈ {2..8} × **SE BASIS** ∈ {J_LADDER, J_INT, J_D2, J_GROUP} = 28 cells, every one in `.grid.csv`.
Reported at every value, not tuned: 3 panels × 6 statistics × 2 partitions × 2 constructions × 3 within terms × 2 between repairs = **432 coordinates**, × 3 endpoints × the K walk × 4 bases = **63,936 SE readings** (`.se.csv.gz`) over **15,984 figure readings** (`.figures.csv.gz`).

## 1. The literal question

Under **J_LADDER — 1188's own basis, verbatim** — the SE is wider than the figure's own ladder spread at **0.2037 to 0.2593 of 432 cells** across the whole rung-count dial (0.2292 at K=3, 0.2500 at the rung count whose rung set IS 1188's L8). Not every cell; about one in four.

Three comparands, all published, none substituted:

| comparand | what it is | J_INT | J_LADDER | J_D2 | J_GROUP |
|---|---|---|---|---|---|
| `S_LAD` (headline) | max−min of v over the whole K ladder | 0.021–0.037 | 0.204–0.259 | 0.220–0.287 | 0.426–0.556 |
| `S_LAD3` | the same dropping the degenerate 2-rung reading | 0.035–0.058 | 0.264–0.375 | 0.271–0.370 | 0.500–0.597 |
| `S_PUB` | **\|v(L8) − v(L3)\|, the move the record actually published** | 0.188–0.338 | **0.308–0.482** | 0.363–0.440 | 0.477–0.593 |

Against the move the record itself reported — 1188's L3-to-L8 step — **the bar is wider than the thing it is measuring at nearly half the cells.** That is the same fact 1188 met from the other side as its 0.2348 "did not move".

## 2. The finding that matters: the SE is not a standard error, and resolution cannot buy one

The queue asked for the SE's own sampling behaviour. Measured directly:

- **It RISES with rung count.** Median log-log slope of SE on K, at fmax=8: **J_LADDER +0.3500, J_INT +0.5325, J_D2 +0.3634**, only J_GROUP −0.2904. A quantity behaving like a standard error falls at ≈ −0.50. It rises at **0.5972 / 0.6690 / 0.6042** of cells. On the longest ladder (fmax 20) J_LADDER reaches only −0.1722 and J_D2 −0.2235 — still nowhere near −0.50.
- **So K\* is not a resolution you walk to.** Where decidability is attainable it is attained at the *smallest* rung count on the dial (median K\* = 3.0 of 2..8; ever-decidable 0.9190 J_LADDER / 1.0000 J_INT / 0.8588 J_D2 / 0.6111 J_GROUP at fmax 8). The **0.0810 of cells that never decide do not decide at any attainable rung count** — adding rungs widens their bar. The mechanical ceiling is f = 1,312 rungs on the shortest tape (3,938 post-warm-up bars, 3 bars per part) and it is irrelevant: the curve is going the wrong way long before it.
- **The bar's own sampling error is as large as the bar.** Jackknife-of-jackknife over the four dial ladders: median `SE_of_SE / SE` = **0.9109 (J_LADDER), 0.7744 (J_INT), 0.9279 (J_D2)**; it is **≥ 1.00 at 0.4815 / 0.4176 / 0.4806** of cells. At roughly half of them the published bar cannot state its own width to within its own width.
- **One added rung is invisible to the figure's own bar at fine resolution.** Share of cells where the K−1→K step exceeds the SE collapses **0.5648 (K=3) → 0.0139 (K=8)** under J_LADDER.

## 3. Why — the mechanism, printed data-free before any tape number (G0)

The delete-1 jackknife of a **median** is degenerate: its n replicates take **at most 3 distinct values for odd n and 2 for even n**, because dropping one point moves a median only through the central order statistics. So the "SE" is one or two order-statistic gaps and is not a function of n at all. Verified on iid draws, n = 27 and 26, 1200 samples each: the delete-1 SE's ratio to the median's true sampling SD is 0.9448 / 1.0410 — near-unbiased — but **its own relative SD is 0.6942 / 0.9478**, and the delete-2 repair does not fix it (0.7001 / 0.5643). *The bar is not biased; it is noise.*

**A DEFECT OF THIS RUN'S OWN, FOUND BY ITS OWN GATE AND NOT HIDDEN:** the first cut declared the bound as "at most TWO distinct values" for every n. G0 **FAILED at max 3 on odd n**. The claim above is the corrected one and is re-gated on both parities.

In the real cells the same degeneracy is visible directly: median distinct replicate values behind a published SE is 4 (J_LADDER) / 3 (J_INT) / 6 (J_D2), and **0.1671 of J_LADDER SEs and 0.3625 of J_INT SEs are built on ≤ 2 distinct values.**

## 4. The dial that moves the answer is the BASIS, not the rung count

Median share SE-wider: **J_INT 0.0278, J_LADDER 0.2326, J_D2 0.2616, J_GROUP 0.4676 — a 16.8x span.** The rung-count dial moves it by 0.06 at most. The record quotes "its own jackknife SE" as though it were one object; it is at least four, and they disagree by more than an order of magnitude on the only question a bar exists to answer. Under J_INT (endpoint held, so 1192's endpoint channel is removed) the record's figures are essentially always decidable; under J_GROUP (1158's own leave-one-dial-ladder-out) it is a coin flip.

By statistic, the lineage's **headline statistic is its best-resolved one**: MAXDD SE-wider 0.1111 with median `se_rel` 0.1420, against SHARPE 0.3056 / VOL 0.3194 / CAGR 0.2778. Panels agree (U56 0.2361 / B136 0.2431 / SMALL 0.2708).

Cross-read of 1188's two committed numbers, over **every** coordinate rather than 1188's harvested claim set — a cross-read, not a replay: median own-SE as a share of the value **0.3604** (1188: 0.5463), share whose SE exceeds the number **0.0810** (1188: 0.3649). 1188's claim set is the more SE-heavy population.

## 5. Gates — 14 of 14

G0/G0b the data-free median-jackknife mechanism (and this run's own corrected overclaim). G1 fast runner ≡ `engine.backtest` post-warm-up, dev 1.39e-17. **G1b reproduces idea 1191's `engine.backtest` defect on ndarray** — 2 non-finite rows, both inside the 260-bar warm-up, so no committed figure moves. G2/G3/G3b cross-run the committed U56 W/H126/N=20 triple (4.12e-05), SPY's OOS triple (1.70e-04) and 1157's three full-tape MaxDD levels (7.17e-06). G4 vectorised all-pairs ≡ the combinations form (4.44e-16). **G5 the K=7 rung set at fmax=8 IS 1188/1158's L8 {1,2,3,4,5,6,8}, dev 0.** **G6 replays 1158's committed 1.173714 (2.59e-08); G7 replays 1148/1157's committed 0.794259 BIT FOR BIT (1.50e-07)** — including its Monte-Carlo draw order, which idea 1191 showed is not recoverable from the artefact. **G8: R_ASIS's between term cannot move with K at a fixed endpoint, dev 0.000e+00** — the rung-count channel is isolated from 1192's endpoint channel by construction. G9 the refinement ladder is nested. G10 the vintage published, not absorbed (pinned ≡ unpinned at the headline cell).

## 6. Rule 8 walk-forward and both KEEP paths — chosen on 2009–2016, 2017–2026 read once

81 rung books, every one in `.walkforward.csv`. **4a: 0 of 81.** 4b full AND OOS: 15 of 81 (U56 10, B136 5, SMALL 0) — but per idea 1189, **at most 8 distinct books** once each panel's GROSS ladder collapses to one (U56's 10 include 5 GROSS rungs and 4 copies of the anchor book; B136's 5 include 4 GROSS rungs). Best: U56/N=12, full 17.71% / 1.1692 / −20.17%, OOS 18.89% / 1.1759 / −20.17% — the incumbent family, confirmatory, not new.

**Resolution buys nothing.** Book-level decidability is rare (3 of 27 U56, 4 of 27 B136, **0 of 27 SMALL** — CH_DEC had to fall back on the whole pool there). Choosing on resolution moves the pick at 3/3 (CH_SE), 3/3 (CH_SPREAD), 2/3 (CH_DEC) panels and never into a pass: **0 of 12 picks clear 4a, 0 of 12 clear 4b.** CH_SE costs U56 OOS Sharpe 1.0985 → 0.9003 and SMALL 0.6676 → 0.3372 against CH_IS.

SURVIVORSHIP (PROTOCOL 9): U56/B136 are current-constituent lists, SMALL is a current screen output; every level is optimistic and every 4a/4b count is an upper bound. The resolution object is a ratio of ratios and far less exposed.

## 7. Proposed, NOT enacted (rule 6 — Sunday review only)

> A published jackknife SE must state its **basis** (which units are dropped) and the number of **distinct replicate values** behind it. An SE built on ≤ 2 distinct replicates is not a resolution statement, and an SE whose value rises with the resolution of the ladder it is read on must not be quoted as a standard error.
