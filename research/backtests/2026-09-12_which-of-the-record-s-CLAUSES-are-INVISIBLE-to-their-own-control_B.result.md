# Idea 582 — which of the record's CLAUSES are INVISIBLE to their own control?

**Lane B, 2026-09-12. Verdict: ANSWERED = 3 of 8. KILL for capital — no new KEEP, no rules change.**

> **A cloud lane ran idea 582 concurrently and pushed first** (`Research cloud: ... ANSWERED, and the
> queue's own prescription is REFUTED`). This run is an independent replication on a different
> control ladder and is logged as **582B**. Neither result is withdrawn — and on inspection the two
> headline claims are **not in contradiction**, because the two runs read "constant-exposure control"
> differently. See "Reconciliation with the cloud run" at the foot of this file.

Script: `2026-09-12_which-of-the-record-s-CLAUSES-are-INVISIBLE-to-their-own-control_B.py`
Outputs: `.txt` `.cells.csv` (1344 rows) `.degen.csv` (112) `.census.csv` (16) `.boot.csv` (16) `.wf.csv` (16)
`RULES.md`, `PROTOCOL.md`, `scan.py`, `bot.py`, `baseline.py` untouched.

## What was run

Idea 317's gate G3 found the GROSS pair collapses to **one** book at matched gross
(`max |A_Sharpe − B_Sharpe| = 4.4e-16`), so 48 of its 288 cells were never a two-parent test.
This run generalises the limit to every clause family the record actually trades, by pricing
each clause against a **ladder of controls**:

| level | control | strips |
|---|---|---|
| **L0** NAIVE | the book with the clause removed, same nominal gross | nothing (what the record does today) |
| **L1** MEAN-GROSS | L0 rescaled by ONE constant so mean target gross matches | the static exposure level |
| **L2** PATH-GROSS | L0 rescaled day by day to the treated book's gross on every date | the entire exposure channel |

L2 is the **constant-exposure control** the queue asks for. Both rescalings are causal and
neither levers (the treated book's gross is ≤ 1, so the rescaled control's is too).

**Verdict taxonomy, pre-registered.** `max |W_treat − W_ctrl(L)| < 1e-10` means the two books
are *the same book* and no amount of data can separate them.
**STATIC-GROSS** = degenerate at L1 (a constant exposure dial). **TIMING-ONLY** = survives L1,
degenerate at L2 (zero selection content; all content is the exposure *path*).
**SELECTION** = survives L2 (it changes *what* you hold at matched exposure).

**Two tuned parameters, as the queue allows: the CLAUSE (8 levels) and the base GROSS g
(7 levels, 0.40…1.00).** All 8 × 7 × 2 panels = **112 cells** reported, each with four arms
= **448 books**; 1,344 rows once the 0/10/25 bps rungs are added (rungs come off one cost-free
simulation per book, exact). 10 bps is the headline everywhere. Panels U56 / B136, vintage
pinned to 2026-09-04. Block-bootstrap settings (400 draws, block 21d, seed 582) are reporting
machinery, not a third dial.

**Gates 4/4 PASS.** G1 RULES v2 U56 @10bps 8.66%/1.2056/−12.05% vs committed 8.63%/1.202/−12.05%.
G2 the GROSS clause *must* be degenerate at L2 — `max|dW| = 0.000e+00`, reproducing idea 317's G3.
G3 the matcher must *not* wash out a real cross-sectional clause — TOPN `max|dW| = 0.0500`.
G4 the L2 control's gross path equals the treated book's on every date — worst `max_t|dG| = 3.9e-15`.

## Result 1 — three of eight clause families are structurally invisible

Identical on both panels, at every one of the 7 g points:

| clause | verdict | dSharpe vs L0 | vs L1 (exposure *level* stripped) | vs L2 (whole exposure channel stripped) |
|---|---|---|---|---|
| **GROSS** g vs 0.375 | **STATIC-GROSS** | +0.0012 / +0.0007 | **0.000000** | **0.000000** |
| **RESPREAD** cash vs re-spread | **TIMING-ONLY** | +0.0447 / +0.0369 | +0.0448 / +0.0374 | **0.000000 / −4.4e-16** |
| **BREADTH** de-gross on q0.17 | **TIMING-ONLY** | +0.1769 / +0.0451 | +0.1769 / +0.0452 | **0.000000** |
| MAGATE above-200d | SELECTION | +0.0472 / −0.0284 | +0.0479 / −0.0280 | −0.0156 / −0.0586 |
| BAND 3% hysteresis | SELECTION | +0.0344 / +0.0125 | +0.0344 / +0.0125 | +0.0619 / +0.0253 |
| VOLCAP vol20<0.60 | SELECTION | −0.0419 / −0.0303 | −0.0419 / −0.0303 | −0.0419 / −0.0303 |
| TOPN top-20 | SELECTION | +0.0147 / −0.0772 | +0.0148 / −0.0772 | +0.0147 / −0.0772 |
| VOLSCALE /√vol20 | SELECTION | −0.0943 / −0.1190 | −0.0943 / −0.1190 | −0.0943 / −0.1190 |

(U56 / B136, headline g = 0.75, 10 bps.)

**GROSS, RESPREAD and BREADTH have no second parent at matched exposure — the control *is* the
book.** That is not an empirical near-miss; it is algebra. RESPREAD: the de-grossed book holds
`g/N` in each of K in-band names (N = names priced), the re-spread control holds `g/K`, and
scaling the control to the treated gross path multiplies it by `K/N` — recovering `g/N` exactly.
BREADTH is the same with a 0/1 multiplier. Idea 317's 48-cell hole is therefore **not specific to
GROSS**: it is the generic fate of any clause whose only action is to move the exposure path.

## Result 2 — the clauses that *do* survive carry no measurable content

Paired stationary block bootstrap of dSharpe vs the L2 control, g = 0.75, 10 bps:

| panel | clause | dSharpe | 95% interval | |
|---|---|---|---|---|
| U56 | **BAND** | **+0.0619** | **[+0.0188, +0.0956]** | CONTENT+ |
| U56 | MAGATE | −0.0156 | [−0.1154, +0.0958] | EMPTY |
| U56 | VOLCAP | −0.0419 | [−0.1380, +0.0528] | EMPTY |
| U56 | TOPN | +0.0147 | [−0.1085, +0.1610] | EMPTY |
| U56 | VOLSCALE | −0.0943 | [−0.1955, +0.0297] | EMPTY |
| B136 | BAND | +0.0253 | [−0.0014, +0.0521] | EMPTY |
| B136 | MAGATE | −0.0586 | [−0.1583, +0.0309] | EMPTY |
| B136 | VOLCAP | −0.0303 | [−0.1006, +0.0336] | EMPTY |
| B136 | TOPN | −0.0772 | [−0.2719, +0.1204] | EMPTY |
| B136 | VOLSCALE | −0.1190 | [−0.3088, +0.0784] | EMPTY |

**1 of 10 excludes zero at a 95% bar over 10 tests — exactly what chance delivers**, and it does
not replicate on the second panel (B136 BAND's interval contains zero). Four of the ten point
estimates are *negative on both panels*: VOLCAP, VOLSCALE — and MAGATE. Three of the five
surviving clauses cost Sharpe once you stop paying them for their exposure.

## Result 3 — what this says about the live book

RULES v2 is **MAGATE + BAND + RESPREAD**. RESPREAD has zero selection content by construction;
MAGATE's selection leg is −0.0156 / −0.0586 (negative on both panels); only BAND is positive, on
one panel, at a bar 10 tests will clear by luck. Decomposed at g = 0.75 on U56, the MA gate's
+0.0479 over a mean-gross-matched control is **+0.0635 of exposure timing and −0.0156 of
selection**. The live book's measured edge is an exposure path, not a stock-picking rule — which
is a real thing to own, but it means the book must be benchmarked against a constant-exposure
control, never against "hold everything at 75%".

## Result 4 — the 4b verdicts the record quotes are mostly not the clause's

Over the 70 SELECTION cells (the only ones where treated and control are two different books):
treated passes 4b in **9**, and **3 of those 9 (33.3%) are also passed by its own
constant-exposure control** — a book without the clause. 4a: treated **0/70**, L2 control 3/70.
Across all 112 cells, 4b pass counts by arm are as much a property of the exposure the arm
happens to run as of the clause, which is idea 317's Result 4 ("more than half the 4b flags are
earned by books with no conditioning at all") reproduced on a different corpus.

## Rule 8 (walk-forward) and the KEEP paths

g chosen on **IS 2009-2016 Sharpe of the treated book alone**; OOS 2017-01-01..2026-09-04 read once.

| panel | clause | g* | OOS CAGR | OOS Sharpe | OOS MaxDD | L2 ctrl OOS Sh | 4b | 4a |
|---|---|---|---|---|---|---|---|---|
| U56 | GROSS | 1.00 | 18.47% | 1.1353 | −29.18% | 1.1353 | — (DD) | — |
| U56 | MAGATE | 1.00 | 12.20% | 1.2623 | −15.84% | 1.2774 | **4b** | — |
| U56 | BAND | 1.00 | 12.78% | 1.2844 | −15.91% | 1.2125 | **4b** | — |
| U56 | VOLCAP | 1.00 | 15.14% | 1.1119 | −20.88% | 1.1116 | — (DD) | — |
| U56 | TOPN | 0.85 | 16.40% | 1.1309 | −20.60% | 1.1119 | — (DD) | — |
| U56 | VOLSCALE | 1.00 | 14.33% | 0.9919 | −22.79% | 1.1312 | — (DD) | — |
| U56 | BREADTH | 1.00 | 16.14% | 1.4004 | −12.72% | 1.4004 | **4b** | — |
| U56 | RESPREAD | 1.00 | 12.78% | 1.2844 | −15.91% | 1.2844 | **4b** | — |
| B136 | GROSS | 1.00 | 18.59% | 1.1007 | −32.72% | 1.1007 | — (DD) | — |
| B136 | MAGATE | 1.00 | 10.51% | 1.1251 | −16.63% | 1.1626 | — (CAGR) | — |
| B136 | BAND | 1.00 | 10.66% | 1.1174 | −16.16% | 1.1009 | **4b** | — |
| B136 | VOLCAP | 1.00 | 14.11% | 1.0189 | −23.09% | 1.0645 | — (DD) | — |
| B136 | TOPN | 1.00 | 16.50% | 0.8876 | −26.20% | 1.0189 | — (H2+DD) | — |
| B136 | VOLSCALE | 1.00 | 10.08% | 0.7359 | −23.61% | 0.8876 | — (H2+OOS+DD) | — |
| B136 | BREADTH | 1.00 | 13.31% | 1.1852 | −16.14% | 1.1852 | **4b** | — |
| B136 | RESPREAD | 1.00 | 10.66% | 1.1174 | −16.16% | 1.1174 | **4b** | — |

OOS comparands, same window: **SPY** CAGR 15.45% / Sharpe 0.8820 / MaxDD −33.72%;
**RULES v2 (live)** 9.53% / 1.2851 / −12.05% on U56 and 7.98% / 1.1185 / −12.24% on B136.
Full-sample bars: SPY CAGR 15.23% / Sharpe 0.8890 (H1 0.9566 / H2 0.8340) / MaxDD −33.72%;
RULES v2 8.66% / 1.2056 (1.2259 / 1.1909) / −12.05%.

**KEEP paths: 4a 0/16, 4b 7/16 — and every one of the seven 4b picks is a book the record
already owns**, re-labelled. Four of the seven (BREADTH ×2, RESPREAD ×2) are *identical* to their
own L2 control, so the 4b flag says nothing about the clause. Only **4 of 16** picks beat their
own constant-exposure control OOS by more than 1e-6; **6 lose to it**; the other 6 are exact ties
by construction. No pick beats the live book OOS on Sharpe on U56 (1.2851) except BREADTH
(1.4004) — which is idea 641's already-committed K8, not a new book, and which is degenerate
against its own control here.

**KILL for capital. No KEEP claimed, no new book promoted, no RULES change proposed.**

## What the record should change (reporting, not a gate)

Idea 317 recommended reporting two parents at matched *mean* gross. This run shows that is the
wrong control for half the record's clause families: at matched mean gross a pure exposure-path
clause still looks like it has content (+0.1769 for BREADTH, +0.0448 for RESPREAD on U56), and
all of it vanishes at matched exposure *path*. Proposed PROTOCOL reporting line, for the Sunday
review — no pass/fail attaches to it:

> Any book whose clause moves its exposure must report the clause's **structural class**
> (STATIC-GROSS / TIMING-ONLY / SELECTION), measured as `max|W_treat − W_ctrl|` against a
> control rescaled day-by-day to the treated book's gross path. A clause classed STATIC-GROSS or
> TIMING-ONLY has no second parent and must be priced against a constant-exposure control; a
> two-parent comparison of it is not a test.

## Caveats

Current-constituent survivorship in both panels, so all *levels* are optimistic; the object here
is a within-cell contrast on the same panel and window, which survivorship moves far less. Only
2020 and 2022 are real stress tests. The bootstrap is stationary-block on a single realised path
and does not price panel-selection or clause-selection. The eight clause families are the ones
reconstructible from `baseline.py` primitives; conditional/state clauses (idea 317's corpus) are
not re-run here.

## Reconciliation with the cloud run (582 cloud, same day)

The cloud run's H_CONST is **refuted for its own object, and does not bear on this one**: its CONST
control is *"EWall scaled to that arm's own **mean** gross"* (`...cloud.py:293`) — a **third book**
substituted for both arms at matched *average* exposure. This run's L2 is the clause's **own**
control rescaled **day by day to the treated book's exposure path**. Those are different controls,
and the queue's phrase "constant-exposure control" admits both readings.

Where they can be compared, they agree and they disagree in traceable places:

| | cloud (582) | this run (582B) |
|---|---|---|
| GROSS collapses at matched gross | **MECH_DEGEN**, L1max 1.6e-16 on 3 panels | **STATIC-GROSS**, `max|dW| = 0.000e+00` on 2 panels, all 7 g — **agree** |
| DEGROSS vs RESPREAD (their SPREAD / my RESPREAD) | visible under CONST on all three panels | **structurally degenerate at L2** (`max|dW| < 1e-10`) — **disagree, and the disagreement is the control, not the data**: at a matched mean gross the two books differ; at a matched gross *path* they are the same matrix |
| VOLCAP | invisible under **every** control on U56 and B136 | survives L2 structurally (`max|dW|` 0.10–0.25) but its ΔSharpe interval contains zero on both panels — **agree on the substance**, differ on the word |
| is the label window-stable | 39/120 flip IS→OOS (32.5%) | not measured here; the structural class *is* window-stable by construction (it is an algebraic property of the weights), the bootstrap verdict is not |
| capital | KILL, 4a 0/264 | KILL, 4a 0/16 picks, 0/70 SELECTION cells — **agree** |

The cloud run's **gate G5** — idea 317's `MA-DG` is bit-identical to a re-spread book because `_ew`
divides by the count of TRUE entries in the mask it is handed — does **not** affect this file: the
de-gross arm here is `baseline.rules_v2_weights` itself (g/N of NAV, N = names priced), and the
re-spread arm divides by the survivor count, so the RESPREAD pair is a genuine de-gross/re-spread
contrast (mean gross 0.5038 vs 0.7182 at g=0.75 on U56).

**Both recommendations should go to the Sunday review together.** They are compatible: a clause can
be invisible to the clause's own path-matched control (no selection content, this run) and still be
visible against an external equal-weight comparand at matched mean gross (it runs a different
exposure path, the cloud run). What neither run supports is calling either object "the" constant-
exposure control without saying which.
