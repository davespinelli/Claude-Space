# Idea 144 — is-the-ladder-even-a-candidate (lane C, 2026-09-05)

**Verdict: ANSWERED — KILL of the hypothesis.** Idea 144 pre-registered "if the answer is
'none', 4b loses a bar rather than gaining one." **The answer is not none.** With the static-gross
ladder dropped from the corpus and every book judged over its own gross family, **both** the CAGR
floor and the MaxDD cap keep exclusive exclusions: at the published coefficients the floor
uniquely excludes **51 of 306** books (m ≤ 1.00) / **37** (m ≤ 1.30) and the cap **18** / **22**.
No bar is deleted. Across the whole φ×δ grid the floor is load-bearing at **36 of 42** points
under *both* conventions.

**What the fix does buy, and it is not nothing.** (1) The ladder ceases to exist as a corpus, so
idea 131's decisive control — "does this bar keep the lever out?" — has nothing left to
adjudicate. (2) The floor and the cap stop being two independent constraints: they act only
through one binding point, m\* = the largest admissible gross. **The m\* rule reproduces the
exhaustive family verdict in 306 of 306 books at both ceilings (agreement 1.000).** Two bars, one
degree of freedom. (3) The cap's bite falls by **62%** at the published coefficients (47 → 18
unique exclusions) and to **1 of 306** at δ = 0.70.

## Harness and reproduction

Idea 94's script is **imported**; idea 131's corpus is reproduced **exactly** before any new
number is read. Corpus = 3 panels (u56, broad, small) × 3 books (V1u, TOP20, EWall) × 17 arms ×
2 cost rungs = **306 books**; gross family = 25 static multipliers m ∈ [0.10, 1.30] step 0.05 =
**7,650 backtests**. Weekly, t+1, 75% target gross at m = 1.00, IS ≤ 2016-12-31, OOS ≥ 2017-01-01.
No leverage: m = 1.30 is 97.5% target gross and `run()` caps any row at 1.00 gross.

| check | result |
|---|---|
| (a) `H.run` vs `engine.backtest`, ungated EWall u56 | max abs diff **0.00e+00** — PASS |
| (b) idea 94's published `EWall+vol60-dg` u56 @10bps (11.6% / 1.133 / −16.9%) | **11.587% / 1.133 / −16.884%** — PASS |
| (c) idea 131/129's census: 306 rows / 82 Pareto / 29 pass 4b / 27 floor-only / 342 ladder rows / 97 ladder floor-only, all at m ≤ 0.80 | **all seven exact** — PASS |
| (d) idea 131's IS-screen groups A / B / C | **45 / 9 / 252** — PASS |

Two tuned parameters, both bar coefficients: φ ∈ {0.00 … 1.00} (7 values), δ ∈ {0.40 … 1.00}
(6 values) — **all 42 points reported under both conventions.** m is the construction dial, swept
exhaustively; the ceiling m_max ∈ {1.00, 1.30} is run as an **arm**, both values reported everywhere.

## Q1 — the convention is coherent, but only for scale-free instruments

A rescale must leave Sharpe alone and move CAGR and |MaxDD| monotonically. Split
**pre-registered from the instruments' units, not from the results**: PURE = `ctl`/`gate`/`stop`
(every parameter scale-free); SCALE-DEP = `dd`/`bud` (the drawdown trigger D and the turnover
budget `ebud` are absolute quantities).

| family | n | CAGR monotone | \|MaxDD\| monotone | max Sharpe range over m |
|---|---|---|---|---|
| **PURE** (ctl/gate/stop) | 234 | **228 / 234** | **234 / 234** | **0.0130** |
| **SCALE-DEP** (dd/bud) | 72 | 27 / 72 | 35 / 72 | **0.2924** |

Cross-book Sharpe sd is 0.319, so 0.013 is noise and 0.292 is not. **"A static rescaling is the
same book" is true for scale-free instruments and false for instruments carrying an
absolute-unit parameter** — a `ddctl-8%` book at half gross is a *different* rule, because the
8% trigger now fires on a book that can no longer fall 8%. Every headline count above is
therefore also reported PURE-only (floor 33 / cap 14 unique exclusions at m ≤ 1.00; floor 26 /
cap 16 at m ≤ 1.30): the conclusion does not depend on the impure arms.

## Q2 / Q3 — load-bearing, before and after the fix

Unique exclusions = rows admitted when that bar is deleted that are not admitted with all five.

| bar | POINT, arms only (306) | POINT, arms+ladder (648) | POINT, ladder only (342) | **FAMILY m≤1.00** | **FAMILY m≤1.30** |
|---|---|---|---|---|---|
| H1 | 1 | 1 | 0 | 1 | 3 |
| H2 | 2 | 2 | 0 | 3 | 3 |
| OOS | **0** | **0** | **0** | **0** | **0** |
| DD | 47 | 73 | 26 | **18** | **22** |
| CAGR | 27 | 124 | **97** | **51** | **37** |
| *admitted* | *29* | *39* | *10* | *58* | *72* |

The ladder-only column is idea 131's finding restated: on the lever the CAGR floor is the only
bar that excludes anything meaningful (97 of 342). After the fix that column does not exist.
**The OOS Sharpe bar excludes nothing anywhere, under either convention, in this corpus** — the
one bar that is genuinely idle here.

## Q4 — two bars, one binding point

Along a family CAGR rises and |MaxDD| rises with m, so the DD cap and the CAGR floor can only
ever bind at m\* = the largest m clearing the cap.

| m_max | family admits | m\*-rule admits | **agreement** | closed-form Calmar bar admits | agreement | ceiling binds | no admissible m |
|---|---|---|---|---|---|---|---|
| 1.00 | 58 | 58 | **1.0000** | 91 | 0.8922 | 127 | 0 |
| 1.30 | 72 | 72 | **1.0000** | 91 | 0.9314 | 54 | 0 |

So the pair reduces exactly to **one** test — `CAGR(m*) ≥ φ·CAGR_SPY` — and 4b's five bars carry
**four** degrees of freedom, not five. The single closed-form ratio bar
`CAGR/|MaxDD| ≥ (φ·CAGR_SPY)/(δ·|MaxDD_SPY|)` is a *good* approximation (89–93%) but **not** a
substitute: compounding is not linear in m and the no-leverage ceiling binds in 54 of 306 books.

**Which bar each rescale rescues** (m ≤ 1.30, 72 admits): **29 pass only BELOW** published gross
(they were failing the DD cap; de-grossing fixes it), **14 only ABOVE** (they were failing the
CAGR floor; up-grossing fixes it — and these are 14 of idea 129/131's 27 floor-only victims),
**29 include m = 1.00** and are exactly the POINT admits, for which the convention changes
nothing. At m ≤ 1.00 the fix saves **0 of the 27 victims**: de-grossing cannot cure a CAGR floor.

## Q5 — the price of the loosening

Admissions 29 → 58 (m ≤ 1.00) → 72 (m ≤ 1.30); both-KEEP-paths 6 → 72. Admitted-set OOS quality
(read on 2017–2026, at m\*): POINT n=29 Sharpe **1.114** / MaxDD **−18.5%** / CAGR **13.2%**;
FAMILY m≤1.00 n=58 **1.087 / −19.1% / 12.9%**; FAMILY m≤1.30 n=72 **1.098 / −19.6% / 13.2%**.
2.5× the admissions for −0.016 to −0.027 of mean OOS Sharpe. The ungated `control` book — the
ladder's own parent — is admitted in **5 of 18** cells under the fix and 0 under POINT-4b; that
is the substantive concession, stated plainly.

## Rule 8 walk-forward (screens read 2009–2016 only; picks read once on 2017–2026)

S0 no screen · S1 IS POINT-4b · S2 IS POINT-4b − floor · S3 IS FAMILY-4b (screen picks m too) ·
S4 FAMILY − floor · S5 FAMILY − cap · S6 IS Calmar bar.

| selector | cells | OOS CAGR | OOS Sharpe | OOS MaxDD | beat SPY | beat v1 | picks moved vs S0 |
|---|---|---|---|---|---|---|---|
| S0 (all 18) | 18 | 9.1% | 0.695 | −23.1% | 6/18 | 12/18 | — |
| S1 (POINT, published) | 7 | 12.7% | 1.022 | −21.1% | 5/7 | 7/7 | **0** |
| S2 (POINT − floor) | 7 | 12.7% | 1.022 | −21.1% | 5/7 | 7/7 | **0** |
| **S3 (FAMILY)** | 7 | **13.8%** | 1.019 | −22.8% | 5/7 | 7/7 | **7** |
| S4 (FAMILY − floor) | 7 | 12.4% | 1.020 | −21.2% | 5/7 | 7/7 | **7** |
| S5 (FAMILY − cap) | 7 | 10.8% | **1.029** | **−18.1%** | 6/7 | 7/7 | **7** |
| S6 (Calmar bar) | 7 | 13.8% | 1.019 | −22.8% | 5/7 | 7/7 | **7** |

Reference OOS, mean over the 18 cells: **SPY 15.45% / 0.882 / −33.7%**; **RULES v1 4.86% / 0.451
/ −25.3%**. The paired table on the 7 cells all selectors enter is identical to the above.

Two readings, both honest. (1) **The family screen is the first screen in this project that is
not inert**: S1/S2 move 0 of 18 picks (reproducing ideas 131 and 132 on a third and fourth bar),
while every FAMILY selector moves **7 of 18**. (2) It moves them **without buying Sharpe**:
S3 vs S1 is **+1.1pp OOS CAGR, −1.7pp of extra drawdown, −0.003 Sharpe**, and S5 is the mirror
image (−1.9pp CAGR, +3.0pp shallower, +0.007 Sharpe). That is exactly the signature of a pure
exposure lever — a clean out-of-sample confirmation of idea 66 (gross is an exact, Sharpe-neutral
dial) on ground idea 66 never touched. Letting a screen choose m is therefore **safe but not
valuable**: it re-points the book on the CAGR/MaxDD line without moving it off the line.

## Both KEEP paths, all 306 books

4a: POINT **97/306**; FAMILY (some m of the book's own family passes 4a) **184/306**.
4b: POINT **29/306**; FAMILY m≤1.00 **58/306**; FAMILY m≤1.30 **72/306**. Both paths: 6 → 72.
POINT admits are a strict subset of FAMILY admits at both ceilings (verified).
**No new book is proposed** — this run re-scores an existing corpus under an alternative
*construction convention*, which is the thing being adjudicated. Nothing is promoted.

## Caveats, stated not buried

- **Survivorship** (idea 54): all three panels are current-constituent lists. De-grossing rescues
  books on the drawdown cap, and absent delistings understate drawdown, so the 29 cap-rescued
  admits are the ones this bias flatters most.
- **Idea 128**: the IS window's SPY MaxDD (−22.1% u56/broad, −18.6% small) is shallower than the
  full sample's −33.7%, so every IS drawdown cap admits too much. This biases S1–S6 identically
  and cannot explain a 0-vs-7 difference in moved picks.
- **The SCALE-DEP result is a real limit, not a footnote**: 72 of 306 books are not closed under
  rescaling at all, and 3 of the 7 moved walk-forward picks land on `ddctl`/`ebud` arms.
- **n is small where it matters**: 7 paired walk-forward cells, 18 total; 11 of 18 cells admit
  nothing under any 4b screen (all 6 small-panel cells among them).
- **Idea 38** (u56/broad calendar-day index) and **idea 126** (t+1 only, no lag band) carry over.
- The no-leverage ceiling is a *choice* (PROTOCOL rule 2), and it is load-bearing: it binds in 54
  of 306 books and changes the floor's unique exclusions from 51 to 37.

## What this leaves for PROTOCOL

The memo proposes the convention as a **reporting rule with a stated restriction** — a static
rescaling of a book is the same book *when every parameter of its instrument is scale-free* —
plus the accompanying clause that 4b's DD cap and CAGR floor be **stated as one bar evaluated at
m\***, since that is what they provably are (306/306). It does **not** propose deleting a bar,
because the run says you cannot. Idea 129's `4b-defensive` reporting class remains the live
proposal for the 27 floor-only victims; this run halves that problem (14 of 27 are admitted once
up-grossing to 97.5% is allowed) rather than solving it.

**Determinism:** the script is deterministic (no RNG, fixed grids); the reduced-configuration
smoke run and the full run agree on every shared number.

Script: `research/backtests/2026-09-05_is-the-ladder-even-a-candidate_C.py`
Console: `.console.txt` · Corpus: `.corpus.csv` · Full family: `.family.csv.gz` ·
Family shape: `.family_shape.csv` · Load-bearing: `.loadbearing_point.csv`,
`.loadbearing_family.csv` · Collapse: `.collapse.csv`, `.mstar.csv` · Grid: `.grid.csv` ·
Walk-forward: `.walkforward.csv` · Picks: `.picks.csv` · Memo: `.memo.md`
