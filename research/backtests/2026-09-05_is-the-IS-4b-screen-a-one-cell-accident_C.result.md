# Idea 178 — is-the-IS-4b-screen-a-one-cell-accident (lane C, 2026-09-05)

**VERDICT: ANSWERED — NO, it is not an accident, but it is not a Sharpe selector either.**
The IS-window 4b screen is a **drawdown / de-concentration instrument that abstains in 7 of 11
cells and never fires at 25 bps at all**. Where it fires it has never yet cost anything under
idea 165's own convention (3 wins / 0 losses / 8 ties, +0.0287 mean OOS Sharpe, t +1.92 — *not*
significant). One KEEP-candidate is memo'd, not proposed. **No RULES change.**

Script: `2026-09-05_is-the-IS-4b-screen-a-one-cell-accident_C.py` (3661 s, 11 cells, 4 workers).
Outputs: `.console.txt`, `.corpus.csv` (1003 book-rows), `.walkforward.csv` (66 arm-rows),
`.repro.csv`, `.audit.csv`.

---

## 0. Reproduction gates — 4 of 4 pass, all before any new number was read

| gate | what | result |
|---|---|---|
| [a] | idea 159's committed `grid.csv`, **row by row, all 294 rows** | max abs diff **2.22e-16** on CAGR / Sharpe / MaxDD / H1 / H2 / OOS-Sharpe / IS-Sharpe |
| [b] | idea 168's committed `grid.csv`, **row by row, all 352 rows** | max abs diff **2.22e-16** on the same seven quantities |
| [c] | idea 165's `W_4bIS` u56 @ 10 bps walk-forward cell | **pick identical** (R6 @ m=0.15, n=6, g=0.750); max abs diff on OOS CAGR/Sharpe/MaxDD **2.78e-17** |
| [d] | AST audit of every `margins_at` call site in the corpus | 53 PUBLISHED, 5 three-bar variant, **3 SWAPPED** |

Both corpora were rebuilt from *their own committed construction code* (imported, never re-typed),
so [a] and [b] are total reproductions, not samples.

## 1. AUDIT [d] — the corpus has a real coefficient-order defect, and it does **not** change the verdict

`C.margins_at(r, b, phi, delta, which)` takes the CAGR floor first and the drawdown cap second.
Three committed call sites pass them the other way round:

```
2026-09-05_required-gross-as-a-leaderboard-column_cloud.py:626   C.margins_at(..., 0.60, 0.70, ...)   # idea 165's IS screen
2026-09-05_required-gross-as-a-leaderboard-column_cloud.py:641   C.margins_at(..., 0.60, 0.70, ...)   # idea 165's OOS read
2026-09-05_the-sign-is-the-parameter-not-the-share_cloud.py:515  C.margins_at(..., 0.60, 0.70, ...)   # idea 168's OOS read
```

A swapped call runs a **looser** CAGR floor (60% of SPY instead of 70%) and a **looser** drawdown
cap (70% of SPY's instead of 60%). So idea 165's screen was not the published 4b. Both readings are
carried here as tuned parameter 2 and reported at every grid point.

**The defect does not flatter idea 165 — it costs it.** Under the PUBLISHED coefficients the screen
admits *fewer* books (85 vs 126 across 11 cells) but changes the pick in **4 of 11 cells vs 3**, and
its changed picks clear the OOS window **3 times vs 2**. Idea 165's headline cell survives the
correction with a *different book*: the published-coefficient screen picks **MOM @ m=0.53 (n=20)**,
which also clears every OOS-window 4b bar (13.18% / 1.0355 / −18.88%). Idea 165's own
`R6 @ m=0.15` result is reproduced exactly and is correct as printed.

## 2. THE ANSWER — the screen fires in 4 of 11 cells and is inert in 7

Counts over the **10 new cells** (C159 6 + C168 4) and over **all 11** (adding idea 165's own):

| arm | cells | changed the pick | pick clears OOS 4b | changed **and** clears | mean OOS Sharpe | vs control |
|---|---|---|---|---|---|---|
| `W_STATIC` (do-nothing / incumbent) | 10 / 11 | 0 / 0 | **0 / 0** | 0 / 0 | 0.7298 / 0.7515 | — |
| `W_4bIS[STATIC][AS165]` | 10 / 11 | 2 / 3 | 1 / 2 | 1 / 2 | 0.7500 / 0.7802 | **+0.0202 / +0.0287** |
| `W_4bIS[STATIC][PUB]` | 10 / 11 | 3 / 4 | 2 / 3 | 2 / 3 | 0.7420 / 0.7687 | +0.0122 / +0.0172 |
| `W_4bIS[CFIS][AS165]` — *idea 165's own arm* | 10 / 11 | 2 / 3 | 1 / 2 | 1 / 2 | 0.7500 / 0.7802 | **+0.0202 / +0.0287** |
| `W_4bIS[CFIS][PUB]` | 10 / 11 | 3 / 4 | 2 / 3 | 2 / 3 | 0.7420 / 0.7687 | +0.0122 / +0.0171 |
| `ORACLE_OOS` (ceiling, not implementable) | 10 / 11 | 10 / 11 | 3 / 4 | 3 / 4 | 0.9999 / 1.0184 | +0.2701 / +0.2669 |

Paired by cell, `W_4bIS[CFIS][AS165]` − `W_STATIC` = **+0.0287, t +1.92, 3 wins / 0 losses / 8 ties**
(ALL 11); under PUB, **+0.0172, t +1.18, 3 wins / 1 loss / 7 ties**. Eight of eleven cells are exact
ties because the screen empties and falls back. **Not significant, and the sample is 11 cells that
share two panels — this is an estimate, not a result.**

**Gross convention is inert.** `[STATIC]` and `[CFIS]` differ in exactly one arm-cell of 22
(C168 broad @ 10 bps PUB, where CF_IS re-grosses the pick 0.75 → 0.80). Idea 165's CF_IS ladder buys
nothing the screen does not already do — a sixth confirmation that gross is not a choice variable.

## 3. The screen has one hard boundary: **it never fires at 25 bps**

| cost rung | arm-cells | screen fired | changed the pick | changed & clears |
|---|---|---|---|---|
| 10 bps | 24 | **16** | 14 | **10** |
| 25 bps | 20 | **0** | 0 | 0 |

It is also empty on the whole small panel at both rungs, and the small panel has **0 of 98** books
that clear the OOS window at any point — so there is nothing there to find, in agreement with
ideas 164/170. The screen's scope is *large-cap panels at 10 bps*, and nowhere else.

## 4. MECHANISM — this answers idea 163: the screen pays through **drawdown**, by de-concentrating

All 14 changed arm-cells move the pick to a **larger book**: n 4→6, 4→20, 14→25, 9→18, 9→25.

* **OOS |MaxDD| falls in 14 of 14** (−1.22 to −4.36 pp).
* OOS Sharpe rises in 10 of 14 (+0.066 to +0.117) and falls in 4 (all the C168 broad PUB pick, which
  the screen pushes to the live k = −0.50 exponent, −0.061).
* OOS CAGR falls in 10 of 14 (−7.25 to +0.24 pp).

The IS drawdown cap is what does the work: it excludes the concentrated top-of-the-IS-Sharpe books
and leaves the wider ones. **Idea 163's hypothesis is confirmed on this corpus** — the screen should
be sold as drawdown control, not as a selector.

## 5. Both KEEP paths over all 1003 corpus book-rows (full sample, published bars)

4a **302 of 1003**; 4b **162 of 1003** — and **every single 4b pass is at 10 bps** (u56 93, broad 69,
small 0). All of them are rows idea 159 or idea 168 already published: reproduction [a]/[b] matched
them to 2.2e-16, so **no new book is discovered here** (P5 HIT).

## 6. Pre-registered predictions: 2 HIT, 3 MISS

| | prediction | outcome |
|---|---|---|
| P1 | screen changes the pick in a minority of the new cells | **HIT** — 2 of 10 (idea 165's arm), 3 of 10 under PUB |
| P2 | changed picks clear the OOS window at most 1 in 3 | **MISS** — 6 of 10 changed arm-cells in the new corpora clear; 10 of 14 over all 11 |
| P3 | no arm beats the control by more than +0.02 OOS Sharpe | **MISS** (marginally) — best paired mean **+0.0202** on the new 10, +0.0287 on all 11 |
| P4 | published coefficients admit no more and win no more | **MISS** — PUB admits fewer (85 vs 126) but wins *more* (3 vs 2 changed-and-clears) |
| P5 | no new KEEP | **HIT** — all 162 4b passers are already-published rows |

P2 and P3 missing in the same direction is the substantive finding: **when this screen fires it has
so far always been in the right direction.** P4 missing is the audit result.

## 7. What this does NOT establish

* **No random-selector control was run.** Idea 151 found a RANDOM selector inside the same band as
  every real one; without that arm here, "+0.0287 with 0 losses" cannot be separated from a
  de-concentration prior that any screen with a drawdown cap would inherit. **This is the single
  most important missing arm** and is queued (idea 198).
* 11 cells, 8 of them ties, two shared panels. t +1.92 is not a result.
* SURVIVORSHIP: u56 and broad are current-constituent lists; every OOS number is an upper bound.
* Idea 165's CF_IS gate reads a FULL-sample failing-bar string before choosing the ladder, a mild
  look-ahead inside a rule-8 arm. Carried verbatim so [c] is exact; it changes one arm-cell of 22.
* Ideas 38 (calendar-day index) and 126 (t+1) carry over unchanged.
