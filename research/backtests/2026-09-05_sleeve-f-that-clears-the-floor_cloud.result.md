# idea 134 — sleeve-f-that-clears-the-floor (cloud, 2026-09-05)

**Verdict: ANSWERED — YES, but it is not a KEEP. PARK.**
The floor *is* one dial away: lowering the sleeve fraction `f` from 0.50 to 0.10–0.25 turns idea
133's `4b-defensive` sleeve books into outright 4b passes — **250 of the 680 swept `f<=0.25`
sleeve rows pass 4b** (272 of all 884 rows). It stops one cell short of being capital-worthy:
**broad @ 25 bps admits 0 of 442 rows at any f, at any overlay, at any gross.**

Script: `2026-09-05_sleeve-f-that-clears-the-floor_cloud.py` ·
console `…console.txt` · grid `…grid.csv` (884 rows) · ladder `…ladder.csv` (260 rows) ·
walk-forward `…walkforward.csv` · memo `…memo.md`

## Harness checks, run before any new number was read
* **(a) engine-equivalence** on all 13 ungated books, both panels: `max|diff| = 0.000e+00` (EXACT).
* **(b) premise audit.** The queue's label `SLV50` is not a book name in idea 133's file; the
  f=0.50 sleeve books there are `S3-50` (TLT/GLD/UUP) and `S4-50` (TLT/GLD/DBC/UUP). The
  8.7%/1.292/-13.6% headline is closest to `u56/S3-50/ebud-0.10 @10bps` (9.94%/1.291/-11.1%,
  OOS 1.277). The queue's "2.0–3.0 pp/yr" shortfall is the **tail, not the median**: over idea
  133's 101 sleeve rows in the class the CAGR-floor shortfall runs **-4.10 / -1.29 / -0.06 pp/yr**
  (min/median/max).
* **(c) reproduction.** This run's 136 f=0.50 rows equal idea 133's arm-for-arm,
  `max|diff| <= 2.2e-16` on CAGR/Sharpe/MaxDD/OOS Sharpe/gross — EXACT.

## The answer, as a table (4b passes; 17 arms per book, 2 sleeves per f)

| f | broad 10bps | broad 25bps | u56 10bps | u56 25bps |
|---|---|---|---|---|
| 0.00 (R20, no sleeve) | **0** | 0 | 9 | 6 |
| 0.05 | **0** | 0 | 16 | 10 |
| 0.10 | 5 | 0 | 23 | 12 |
| 0.15 | 9 | 0 | 27 | 20 |
| 0.20 | 16 | 0 | 29 | 19 |
| 0.25 | **22** | 0 | 28 | 14 |
| 0.50 (idea 133's anchor) | 4 | 0 | 3 | 0 |

**What f actually buys** (means over all arms, panels and cost rungs): the CAGR-floor margin falls
monotonically **+1.89 → +1.53 → +1.16 → +0.79 → +0.45 → +0.08 → -1.88 pp/yr** as f goes
0.00→0.50, while the drawdown-cap margin rises monotonically **-1.11 → -0.37 → +0.64 → +1.64 →
+2.62 → +3.52 → +7.84 pp**. The exchange rate over 0.00→0.25 is about **1 pp of CAGR margin per
2.5 pp of drawdown margin**, and the pass count peaks at **f = 0.15–0.20**, where both margins are
positive at once. Below f=0.10 the drawdown cap binds; above f=0.25 the CAGR floor binds
(fail_CAGR 11 → 129 rows across the sweep).

## The finding that is not about f: on `broad` the sleeve does something gross cannot
The 260-row static-gross ladder is the control for "is f just an exposure dial in disguise".
* On **u56** it is: `R20` alone passes 4b at m=0.80 (both cost rungs), so de-grossing reaches the
  same place.
* On **broad @ 10 bps the ladder cannot get there at all**: `R20` fails the **CAGR floor** at
  m=0.60 and the **drawdown cap** at every m from 0.80 to 1.40 (Sharpe is flat at 0.973–0.978
  across the whole ladder — idea 66's result again). Adding the sleeve at f>=0.10 passes.
  The sleeve **moves the (CAGR, MaxDD) frontier**; gross only slides along it.
* At f=0.50 the ladder needs m=1.2–1.4 to pass; at f<=0.25 it passes at m=1.00. That is the same
  statement from the other side: low f already sits where high f has to be levered to.

## The wall: broad @ 25 bps
**0 of 442 rows pass, and 0 of 130 ladder points.** Exactly **one** row clears the halves, the OOS
Sharpe bar and the drawdown cap and fails only the floor (`S4-50/band3-rw`, by **0.99 pp/yr**);
every other row fails a Sharpe bar as well. No f rescues it. This is idea 82's breakeven result
(~7.5–10.5 bps for the standing candidates) reappearing as a hard edge, not a margin.

## Best member and its numbers (reported, not selected on)
35 (book, arm) pairs pass in 3 of the 4 cells; none passes in 4. Ranked by mean OOS Sharpe the top
is **`S4-25 / band3-rw`** = 75% gross in (0.75 × ranked-top-20 + 0.25 × momentum-vote × risk-parity
over TLT/GLD/DBC/UUP), with a 3% band around the 200d MA in the matched-gross convention:

| cell | CAGR | Sharpe | MaxDD | H1 / H2 | OOS CAGR / Sharpe / MaxDD | TO | 4a | 4b |
|---|---|---|---|---|---|---|---|---|
| u56 @10 | 13.0% | 1.192 | -16.9% | 1.214 / 1.181 | 14.4% / 1.235 / -16.9% | 8.8x | no | **yes** |
| u56 @25 | 11.6% | 1.070 | -17.1% | 1.077 / 1.070 | 12.9% / 1.123 / -17.1% | 8.8x | no | **yes** |
| broad @10 | 13.3% | 1.055 | -17.1% | 1.208 / 0.929 | 13.1% / 1.001 / -17.1% | 12.2x | yes | **yes** |
| broad @25 | 11.2% | 0.909 | -17.3% | 1.052 / 0.791 | 11.1% / 0.861 / -17.3% | 12.2x | yes | no (H2, OOS) |

SPY over the same sample: 15.23% / 0.889 / -33.7%, halves 0.957/0.834, OOS 0.882/15.5%/-33.7%.
RULES v1 OOS Sharpe 0.747 (u56 @10) down to 0.155 (broad @25).

## Rule 8 walk-forward (PROTOCOL rule 8; selectors written down before any OOS number was read)
Parameters chosen on 2009–2016 only, read once on 2017–2026. S0 = argmax IS Sharpe; S1 = same
among arms whose IS window clears 4b's halves, DD cap and CAGR floor; S2 = floor deleted.

| cell | S1 pick | OOS CAGR | OOS Sharpe | OOS MaxDD | vs control | vs SPY | vs v1 |
|---|---|---|---|---|---|---|---|
| broad @10 | S3-50/band3-rw | 10.8% | 1.047 | -11.8% | 0.930 | 0.882 | 0.576 |
| broad @25 | S3-50/band3-rw | 9.0% | 0.891 | -12.0% | 0.807 | 0.882 | 0.155 |
| u56 @10 | S3-25/control | 13.6% | 1.202 | -17.1% | 1.168 | 0.882 | 0.747 |
| u56 @25 | S3-25/control | 12.1% | 1.086 | -17.2% | 1.072 | 0.882 | 0.399 |

S1 beats the ungated control, SPY and RULES v1 in **4 of 4** cells, and its pick passes full-sample
4b in 3 of 4. Mean OOS Sharpe S0 1.065 / S1 1.057 / S2 1.065 — **the screen is worth -0.008 of OOS
Sharpe**, and S1 differs from S2 in 4 of 4 cells here (contrast idea 129's 0 of 18: with a corpus
this wide the floor finally moves the pick, and moving it does not help). Every full-sample 4b
pass also passes 4b re-measured on the OOS window alone.

## Pre-registered predictions, scored
* **P1** (a sleeve arm with f<=0.25 passes 4b) — **HELD**, 250.
* **P2** (the passing f's are the low end, <=0.15) — **FAILED**: passes run to f=0.50; the count
  peaks at 0.15–0.20, not at the bottom. The floor is bought by *some* de-sleeving, not by all of it.
* **P3** (u56 first) — **HELD**, u56 216 / broad 56.
* **P4** (the ladder also reaches 4b) — **HELD** on u56, 44 ladder rows, m 0.8–1.4; but see above —
  **not** on broad, where the ladder never passes and the sleeve does.
* **P5** (25 bps kills more) — **HELD**, 191 at 10 bps vs 81 at 25.

## Why PARK and not KEEP
Under PROTOCOL 4b as literally written, `S4-25/band3-rw` is a KEEP-candidate on 3 of 4 cells. It is
parked, not promoted, for three reasons, all pre-registered rather than discovered:
1. **Cost fragility.** The broad panel gives up entirely at 25 bps (0 of 442). Ideas 11 and 82
   already set the project's cross-universe/cost practice; this candidate fails it at the same
   place every previous one has.
2. **Blocked upstream.** Ideas 105 (is the sleeve gold, precious metals, or any real asset?) and
   106 (is DBC a drag or a contango artefact?) are open, and both bear on whether "macro sleeve"
   is even the right description of the thing doing the work. No RULES wording can be proposed
   for a sleeve book until they close. The memo states the wording it *would* take.
3. **Survivorship.** Both panels are current constituents (idea 54). Absent delistings inflate the
   equity leg more than the ETF sleeve, so every CAGR-floor margin quoted here is biased **in
   favour of low f** — the direction that manufactures this run's answer.

Additional caveats carried: idea 128 (the IS window is too shallow to express a deep drawdown, so
the S1/S2 screens admit too much), idea 126 (t+1 execution only), idea 127 (mean realised gross is
reported on every row; the dg/rw split is never collapsed). The small panel has no
TLT/GLD/DBC/UUP, so a sleeve book cannot exist there — idea 136 remains the open item for it, and
this run does not speak to it.

## Follow-ups proposed
1. `broad-25bps-is-the-wall` — the same 442-row grid says broad @25 fails on **Sharpe bars**, not
   the floor. Decompose whether that is turnover (12.2x vs u56's 8.8x) or the panel's H2.
2. `f-as-a-pre-registered-constant` — the pass count peaks at f=0.15–0.20 on both panels and both
   cost rungs. Idea 128's plateau test belongs on this dial before any f is written into RULES.
3. `sleeve-moves-the-frontier` — the broad ladder result (gross cannot reach 4b, the sleeve can) is
   the first instrument the project has found that is not a point on the gross ladder. Price it on
   idea 74's one axis (pp of CAGR per pp of MaxDD) against the gate, the band and de-grossing.
