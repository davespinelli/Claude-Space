# Idea 609 — is the TWIN ORDERING window-invariant on a ROLLING census? (lane B, 2026-09-12)

**ANSWERED = NO, AND THE FAILURE IS ONE NAMED LEG.** Idea 605's published family ordering
**QROLL > QEXP > ABS** is the order a reader would have seen in **5 of 59** rolling 3-year windows
(**0.0847**). The order they *did* see, in 31 of 59 (**0.5254**), is **QROLL > ABS > QEXP**. The top
of the ordering is the most invariant thing in the record — **QROLL > QEXP holds 59 of 59 windows
(1.0000)** — and the rest of it is a full-sample aggregation artefact: **QEXP > ABS holds 0.0847**.
KILL for capital: 4a **0 of 648**, and the 142 arms clearing 4b are idea 605's own committed passes
(141) reproduced, not a new book.

Script `2026-09-12_is-the-TWIN-ORDERING-window-invariant-on-a-ROLLING-census_B.py`.
No RULES change, no KEEP claimed, no PROTOCOL edit applied (rule 6); RULES.md, PROTOCOL.md,
scan.py, bot.py and baseline.py untouched.

## 0. Reproduction gates — and a data-drift finding that forced a second corpus

Idea 605 ran on 2026-09-10. Since then the nightly jobs appended two trading days to
`data/prices.csv` and **rewrote `data/prices_small.csv.gz`: the sub-$2B screen went from 439
tradable names to 663 in two days.** "Re-run idea 605's corpus" is therefore two different corpora
depending on when you run it — exactly the hazard idea 565 filed. So this run built **both**, and
reports the census on both.

| gate | what | result |
|---|---|---|
| G1 | derived ladder `r_gate(c) = m·r0 − (c/1e4)(m·t0 + g·\|dm\|)` vs a live `engine.backtest` through idea 399's `apply_gate`, all 15 rungs | max \|diff\| **3.469e-18** — PASS (bar 1e-12) |
| G2 | fast CAGR/Sharpe/MaxDD vs `engine.metrics`, 200 real series | **0.000e+00** — PASS |
| G3 | idea 84's EWALL U56 g=0.85 @10bps | **11.752% / 1.046 / −17.894%** vs published 11.8% / 1.05 / −17.9% — PASS |
| G4a | **AS-OF replica** (today's caches truncated to idea 605's last dates; SMALL panel restored from the git blob `e02949d` it read) vs its committed `cells.csv.gz`, 135 (panel, rung, family) cells | **U56 0.000e+00, SMALL439 0.000e+00, B136 1.389e-02** — FAILS the 1e-9 bar **on B136 only**, because `data/prices_broad.csv` is also re-downloaded daily |
| G4b | the same join on **TODAY's** caches | **SMALL439 6.667e-01**, B136 2.083e-02, U56 1.389e-02 |
| G5 | the O(1) window-Sharpe recursion (cumsums, twin second moment quadratic in λ) vs direct numpy on 400 random (arm, window) slices | max \|diff\| **2.554e-14** — PASS |

The as-of replica reproduces idea 605's panel shapes exactly (U56 4441 eval days, B136 4439,
SMALL439 440 cols / 3934 days) and its pooled `ordering.csv` to **≤ 0.0046** at every rung. Its
KEEP-path columns land at 4a **0/648** and 4b **142/648** (B136 76 / U56 66 / SMALL439 0) against
idea 605's committed **0** and **141** (B136 75 / U56 66 / SMALL439 0) — one B136 arm apart.
**H1 is scored FAIL because the pre-registered bar was 1e-9; the honest reading is that two of
three panels are bit-exact and the third moves by one arm in 108.**

**G4b is the reportable by-product.** On today's caches the same published per-panel family win
rate moves by up to **0.667** on SMALL439. A published number keyed to that panel is not a
statement about the panel; it is a statement about the day the job last ran (idea 565, 514/522).

## 1. The census

Population, inherited verbatim from ideas 602/605 so the rows join: 3 panels × 18 gate specs
(ABS B∈{0.30,0.40,0.50}; QEXP q∈{0.07,0.12,0.17}; QROLL q × w∈{252,504,1008,2016}) × 3 depths ×
2 cadences × 2 gross = **648 arms** (108 ABS / 108 QEXP / 432 QROLL). Comparand for every arm is
its **matched-mean-gross static twin**; win = ΔSharpe > 1e-12.

Tuned, both named by the queue, **all 9 grid points reported**: window ∈ {504, 756, 1008} trading
days, step ∈ {21, 63, 126}. Headline 756/63 (the queue's "3-year", quarterly). Reported and never
tuned: panel, family, level, w, depth, cadence, gross, rung ∈ {0, 10, 25} bps, corpus ∈
{ASOF, TODAY}, and the twin-matching convention ∈ {WINDOW, FULL}.

### Headline (ASOF corpus, pooled, 756/63, 10 bps, WINDOW-matched twin, 59 windows)

| statistic | value |
|---|---|
| exact **QROLL > QEXP > ABS** | **0.0847** (5 of 59) |
| **QROLL > QEXP** | **1.0000** (59 of 59) |
| QEXP > ABS | **0.0847** |
| QROLL > ABS | 0.7458 |
| QROLL on top | 0.7627 |
| ABS at the bottom | 0.0847 |
| mean ρ vs the published order | **+0.3462** (ρ = +1 in 0.0847 of windows) |
| mean window win rates ABS / QEXP / QROLL | 0.4271 / **0.2385** / 0.5608 |

Every order a reader would have seen: **QROLL>ABS>QEXP 0.5254**, ABS>QROLL>QEXP 0.2373,
QROLL>ABS=QEXP 0.1356, **QROLL>QEXP>ABS 0.0847**, ABS=QROLL>QEXP 0.0169.

The five windows that *do* read the published order are **2016-10→2019-10, 2017-04→2020-04,
2017-07→2020-07, 2017-10→2020-10 and 2022-10→2025-10** — four of the five span the COVID crash.
The 15 windows where even QROLL > ABS fails are the quiet 2010–2016 stretch (QEXP's window win
rate is literally **0.000** in seven of them) plus the four 2019-10→2024-01 windows.

### All 9 grid points (ASOF, pooled, WINDOW, 10 bps)

| window | step | n | exact | QR>QE | QE>AB | QR>AB | mean ρ |
|---|---|---|---|---|---|---|---|
| 504 | 21 | 188 | 0.0585 | 0.9894 | 0.0585 | 0.7713 | 0.3473 |
| 504 | 63 | 63 | 0.0635 | 1.0000 | 0.0635 | 0.7778 | 0.3560 |
| 504 | 126 | 32 | **0.0312** | 1.0000 | 0.0312 | 0.7500 | 0.2999 |
| 756 | 21 | 176 | 0.0909 | 1.0000 | 0.0909 | 0.7386 | 0.3342 |
| **756** | **63** | **59** | **0.0847** | **1.0000** | **0.0847** | **0.7458** | **0.3462** |
| 756 | 126 | 30 | 0.0333 | 1.0000 | 0.0333 | 0.7667 | 0.3443 |
| 1008 | 21 | 164 | **0.1280** | 1.0000 | 0.1280 | 0.8049 | 0.4018 |
| 1008 | 63 | 55 | 0.1091 | 1.0000 | 0.1091 | 0.8000 | 0.3903 |
| 1008 | 126 | 28 | 0.0714 | 1.0000 | 0.0714 | 0.7857 | 0.3345 |

Span **0.0968** (H5 passes) — the dials do not rescue the claim, they only move it between 3% and
13%. `QR > QE` is **1.0000 at eight of nine** grid points and 0.9894 at the ninth.

### The two axes that do move the answer, and neither saves it

| corpus | convention | exact | QR>QE | QE>AB | QR>AB | mean ρ |
|---|---|---|---|---|---|---|
| ASOF | WINDOW | 0.0847 | 1.0000 | 0.0847 | 0.7458 | +0.3462 |
| ASOF | FULL (idea 605's own) | **0.3390** | 0.7288 | 0.6102 | 0.8814 | +0.5655 |
| TODAY | WINDOW | 0.1017 | 1.0000 | 0.1017 | 0.8305 | +0.4479 |
| TODAY | FULL | 0.3220 | 0.6949 | 0.6271 | 0.9492 | +0.6271 |

Matching the twin on the **full sample** rather than inside the window — idea 605's own convention
— raises the exact share to 0.3390 and swaps which leg breaks (QEXP>ABS recovers to 0.6102 while
QROLL>QEXP falls to 0.7288). Under **either** convention the published order is a minority
reading. The 439→663 panel rewrite moves the answer by **+0.017**, so the drift that wrecks G4b
does not touch this verdict.

Per panel (ASOF, WINDOW, 10 bps, 756/63): **B136 0.0000**, U56 0.1186, SMALL439 0.2264.

## 2. Rule 8

**(a) On the claim.** IS windows (ending ≤ 2016-12-31) read first, OOS windows (starting ≥
2017-01-01) read once. On the ASOF corpus at 10 bps the IS exact share is **0.0000 at every one of
the 9 grid points** — the published order was never once the reading available to a pre-2017
reader — against an OOS share of 0.000–0.163. Headline gap **+0.1481**, so **H6 fails**, in the
direction "the claim only starts to appear out of sample". `QROLL > ABS` moves the same way,
0.4500 IS → 0.8519 OOS.

**(b) On a book.** The IS rolling census picks the family, IS Sharpe picks the arm inside it,
2017-2026 is read once. 27 (panel × grid point) picks on the ASOF corpus:

| | pick | own twin | hindsight-family pick | RULES v2 | SPY |
|---|---|---|---|---|---|
| mean OOS Sharpe | 0.8299 | 0.8064 | 0.8982 | **0.9885** | 0.8799 |
| mean OOS CAGR | 9.23% | — | — | 7.10% | **15.41%** |
| mean OOS MaxDD | −22.22% | — | — | **−12.99%** | −33.72% |

The selector names the OOS-leading family in **17 of 27**; the picked book beats RULES v2 on OOS
Sharpe in **9 of 27**, SPY in 18, its own matched-gross twin in 18. **H7 fails.** The failures are
all SMALL439, where the IS census picks ABS (its IS win rate 0.36–0.52 against QROLL's 0.12–0.23)
and OOS reads QROLL — OOS Sharpe **0.1450** against SPY's 0.8820. TODAY's corpus gives the same
17/27 and 9/27 with a slightly better mean (0.8959).

## 3. KEEP paths (all 648 arms, 10 bps)

**4a 0 of 648** on both corpora. **4b 142 of 648** (ASOF; TODAY 141) — B136 76, U56 66, SMALL439
0; failure legs CAGR 185, DD 91, the full set 216. These are idea 605's committed passes
reproduced (its own 141 at the same rung), not a new book, so **no KEEP is claimed and no memo
with RULES wording is written.** 17 of the 27 rule-8 picks sit on an arm that clears 4b full
sample, which is the same statement: the 4b bar cannot separate these arms from each other.

## 4. Pre-registered hypotheses — 2 of 9 pass

| | | |
|---|---|---|
| H1 | G4a reproduces to 1e-9 | **FAIL** — 1.389e-02, B136 only; U56 and SMALL439 are 0.000e+00 |
| H1b | today's caches reproduce (not a bar) | FAIL — 6.667e-01 |
| H2 | published order is the modal reading (≥ 0.50) | **FAIL** — 0.0847 |
| H3 | strong invariance (≥ 0.90) | **FAIL** — 0.0847 |
| H4 | every pairwise leg ≥ 0.50 | **FAIL** — QR>QE 1.0000, QE>AB 0.0847, QR>AB 0.7458 |
| H5 | exact share spans ≤ 0.10 over 9 grid points | **PASS** — 0.0968 |
| H6 | \|OOS − IS\| exact share ≤ 0.10 | **FAIL** — 0.1481 |
| H7 | IS pick beats baseline AND SPY on OOS Sharpe | **FAIL** — 9/27 and 18/27 |
| H8 | some arm clears 4a or 4b | **PASS** — 4a 0, 4b 142 |

## 5. What the record should do with this

1. **Demote the ordering to its one invariant leg.** "QROLL > QEXP > ABS" should be quoted as
   **"QROLL beats QEXP in every 3-year window (59/59, 1.0000 at eight of nine grid points)"**.
   The QEXP-over-ABS half is a full-sample artefact seen in 8.5% of windows and in **zero**
   pre-2017 windows.
2. **A twin claim needs its matching convention stated.** WINDOW vs FULL matching moves the exact
   share 0.0847 → 0.3390 and swaps which leg breaks. Idea 605's numbers are FULL-matched; nothing
   in the record says so.
3. **Idea 565 is now priced.** The nightly rewrite of `data/prices_small.csv.gz` (439 → 663
   tradable names in two days) moves a published per-panel family win rate by **0.667**. Any
   committed claim keyed to that panel needs its coverage pinned or its key column committed.
4. Idea 605's caveat was right and understated: it read two half-windows and got ρ −0.500; 59
   windows give ρ +0.3462 and an 8.5% hit rate.

_Survivorship: all three panels are current-constituent lists, so CAGR and drawdown LEVELS are
optimistic. Every statistic here is a WITHIN-panel contrast between arms that share the panel,
which the bias does not move._

Follow-ups filed: **823** (is QROLL > QEXP at 59/59 a QROLL fact or a breadth fact — rerun the
rolling census on a non-breadth gate state), **824** (re-read every committed ordering claim in the
record under both twin-matching conventions), **825** (pin the SMALL panel's coverage: commit the
name set beside every result that reads it).
