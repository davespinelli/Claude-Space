# Idea 81 — vol20-as-the-hidden-ranking-key (cloud, 2026-09-05)

**KILL of the inversion, third independent CONFIRM of the deletion. RULES v1's `/sqrt(vol20)`
is signed against its own panel and should go — but the fix is to STOP dividing, not to start
multiplying. 0 of 36 books is a cross-universe KEEP. One documented near-miss (broad, POS,
n=20: fails 4b on the drawdown cap ALONE, by 1.2pp).**

Script `2026-09-05_vol20-as-the-hidden-ranking-key_cloud.py`; outputs `.console.txt`,
`.grid.csv`, `.fm.csv`, `.diag.csv`, `.walkforward.csv`.

## Reproduction, before any new number was read

| check | target | this run |
|---|---|---|
| [a] `INV / n=5 / w=0.15` vs `baseline.rules_v1_weights`, all 3 panels | 0 | **0.000e+00 (EXACT)** — the INV arm IS the live book |
| [b] `NONE / n=20` vs idea 80's committed `CAND/COMP/n=20` code path, u56@10bps | identical | **12.65974% / 1.09214 / -18.30835%, halves 1.08828 / 1.10155 — IDENTICAL** |
| [c] idea 80's `fama_macbeth`, imported and called verbatim | u56 +0.0045 (t +3.90), broad +0.0029 (t +3.19) | **+0.00450 (t +3.90) / +0.00294 (t +3.19)**; low-vol rank IC **-0.0428 / -0.0332** vs published -0.0426 / -0.0329 |

**NOT FULLY REPRODUCED, and reported as such:** idea 2's published KEEP row reads Sharpe
**1.093** and halves **1.088 / 1.103**. Both this run and idea 80's own committed code give
**1.09214 / 1.08828 / 1.10155**. CAGR (12.7%) and MaxDD (-18.3%) match exactly; Sharpe and H2
differ by 0.001 in the last published digit, and that digit is not re-derivable from any
committed script. The gap is far below anything that matters here and is recorded, not hidden.

## Corpus and grid

3 panels (u56 / broad / small) x 2 cost rungs x **exactly two tuned parameters** — the vol
scaler in {INV = `/sqrt(v)`, NONE = `x1`, POS = `x sqrt(v)`} and n in {5, 20} — = 6 grid points,
**every one reported**, 36 books, weekly, t+1, equal-weight at 0.75/n so position count and
gross are not one dial (idea 2's correction).

## (1) The premise reproduces on the large caps and REVERSES on the small panel (P1 half-failed)

| panel | vol20 slope (bivariate w/ PROX) | univariate | low-vol rank IC |
|---|---|---|---|
| u56 | **+0.00450 (t +3.90)** | +0.00499 (t +4.63) | -0.0428 (t -3.96) |
| broad | **+0.00294 (t +3.19)** | +0.00369 (t +3.90) | -0.0332 (t -3.78) |
| **small (new — idea 80 never ran it)** | **-0.00084 (t -0.95)** | -0.00093 (t -1.03) | **+0.0195 (t +3.84)** |

Inside the gate, the large-cap panels pay HIGH vol next week and the sub-$2B panel pays LOW vol,
significantly so in IC space. Any wording that puts a vol tilt into RULES therefore needs the
same universe clause ideas 39/49 already demanded of the trend gate.

## (2) THE ANSWER: the first dose is the whole effect (P2 FAILED, 4 of 12 cells)

Paired daily t-tests, same panel / cost / n, annualised mean difference:

| step | mean over 12 cells | u56 (4 cells) | broad (4 cells) | small (4 cells) |
|---|---|---|---|---|
| **NONE - INV** (delete the scaler) | **+5.08%/yr, mean t +2.37** | +2.7 to +11.0 pp, **t +3.33..+3.79 (4/4 significant)** | +4.4 to +11.8 pp, **t +2.82..+3.48 (4/4)** | -1.1 to +2.5 pp, t -0.20..+1.12 |
| **POS - NONE** (invert it) | **-0.05%/yr, mean t +0.64** | +0.5 to +1.6 pp, t **+0.74..+1.14 (0/4)** | +2.5 to +5.2 pp, **t +2.02..+3.15 (4/4)** | -1.6 to -8.6 pp, t -1.04..-1.97 |

Sharpe peak by cell: **NONE on all four u56 cells, POS on all four broad cells, INV on three of
four small cells**. Mean dSharpe: NONE - INV **+0.145**, POS - NONE **-0.034**. A monotone
premium needs those two to be similar and both positive; they are not.

**The winning tilt's sign matches its panel's own vol premium sign in 3 of 3 panels** (u56 and
broad positive -> NONE/POS beat INV; small negative -> INV beats both), so the *sign* of idea
80's finding is real and tradeable-in-direction. What does not follow is the *dose*.

**Mechanism, and it is not the slope's t.** u56 has the LARGER slope (+0.0045) and gets nothing
from the second dose; broad has the smaller slope (+0.0029) and gets +2.5..+5.2 pp/yr. What
separates them is how much of the panel the book holds: at n=20 the INV and NONE books overlap
**69.4%** of their union on u56 (20 names out of ~37.5 eligible from a 56-name list) against
**42.5%** on broad (20 out of a 136-name list). On u56 there is barely a different book to tilt
into. A cross-sectional slope only pays where the book is a small slice of the cross-section.

## (3) What POS costs, and which bar it breaks (P3a HELD, P3b FAILED)

POS's MaxDD is deeper than NONE's in **12 of 12** cells. Held-name mean vol20 runs
INV **0.175** -> NONE **0.321** -> POS **0.383**; turnover 23.2 -> 18.8 -> 22.7 x/yr (INV is the
*most* expensive arm as well as the worst).

Of POS's 11 4b failures, **10 include the drawdown cap** — P3b's "every" failed on one book
(broad@25 / n=5 fails on H1 alone). Two POS books fail on the **DD cap and nothing else**:

* **broad @ 10 bps, POS, n=20: 16.0% / 1.052 / -21.4%, halves 1.197 / 0.927, OOS Sharpe 1.005 —
  clears H1, H2, OOS and the CAGR floor, and misses the -20.2% cap by 1.2pp.**
* broad @ 10 bps, POS, n=5: 22.4% / 1.053 / -29.7%, halves 1.161 / 0.964, OOS 1.009 — same
  failure, 9.5pp out.

That is worth stating precisely because the incumbent NONE/n=20 book on broad fails 4b on **H2
alone** (0.811 vs SPY's 0.834). **The POS tilt fixes broad's H2 failure (0.811 -> 0.927) and
breaks its drawdown instead.** It is a swap of one binding bar for another, not an improvement.

## (4) Both KEEP paths, all 36 books

| | 4a | 4b (full sample) | 4b (OOS window alone) |
|---|---|---|---|
| INV n=5 / n=20 | 0 / 2 | 0 / 0 | 0 / 0 |
| NONE n=5 / n=20 | 1 / 2 | 0 / **1** | 0 / 2 |
| POS n=5 / n=20 | 0 / 1 | 0 / **1** | 0 / 2 |
| **total (36 books)** | **6** | **2** | 4 |

Both full-sample 4b passes are on u56 @ 10 bps at n=20 — NONE (12.7% / 1.092 / -18.3%, the
standing idea-2 candidate, recovered independently) and POS (13.2% / 1.082 / -19.0%). **Neither
passes on a second panel and neither survives 25 bps** (both fail H1 there). **0 of 36 points is
a cross-universe KEEP (P5 HELD).** The whole INV arm — the live book's own tilt — passes 4b
**0 times in 12** and fails the CAGR floor in 12 of 12.

## (5) Rule 8 walk-forward (both selection rules fixed before any OOS number was read)

| panel@cost | S1 pick (IS Sharpe) | OOS CAGR / Sharpe / MaxDD | 4b on OOS? | RULES v1 OOS | SPY OOS |
|---|---|---|---|---|---|
| u56@10 | **NONE n=20** | **14.36% / 1.168 / -18.3%** | **yes** | 7.73% / 0.747 / -13.8% | 15.45% / 0.882 / -33.7% |
| u56@25 | NONE n=20 | 12.73% / 1.050 / -18.4% | **yes** | 3.78% / 0.399 / -14.2% | as above |
| broad@10 | **POS n=5** | 22.35% / 1.009 / -29.7% | no (DD) | 5.94% / 0.576 / -21.2% | as above |
| broad@25 | POS n=20 | 13.02% / 0.856 / -22.8% | no | 1.11% / 0.155 / -26.7% | as above |
| small@10 | INV n=20 | 3.30% / 0.313 / -29.3% | no | 7.92% / 0.581 / -32.8% | as above |
| small@25 | INV n=20 | -0.56% / 0.023 / -37.6% | no | 2.67% / 0.250 / -43.0% | as above |

**P4 FAILED**: the plain-Sharpe rule picks POS in 2 of 6 cells (both broad). Pick counts are
NONE 2 / POS 2 / INV 2 — the walk-forward picks a *different* scaler on every panel, which is the
same universe-fragility ideas 49 and 55 found, now measured on the scaler axis.

**The 4b-aware rule picks NOTHING in 6 of 6 cells** — no in-sample point met the in-sample
drawdown cap. That is the fifth independent reproduction of the structural result in ideas 38,
39, 46 and 49.

## Verdict

**KILL for the inversion; the deletion is confirmed for the third time independently** (idea 1
at n=5, idea 2 at n=20, this run across 3 panels x 2 costs x 2 n with paired t-tests). For the
Sunday review: (a) RULES v1's `/sqrt(vol20)` is signed against its own panel and costs **+5.1
pp/yr** at t +2.8..+3.8 on the large-cap lists — the evidence to drop it is now overwhelming;
(b) do **not** replace it with the opposite tilt — the second dose is worth **-0.05 pp/yr**
overall, is significant on exactly one of three panels, and buys deeper drawdown in 12 of 12
cells; (c) any vol wording needs the large-cap universe clause, because the premium's sign
reverses on the sub-$2B panel.

New queue ideas: **152** (price the broad POS/n=20 near-miss on its own gross ladder — it fails
4b on the DD cap alone by 1.2pp and idea 66 says gross is an exact lever), **153** (does the
overlap fraction predict the tilt's realised gain, across n and panel?).

## Caveats carried

* **Survivorship**: all three panels are current-constituent lists (idea 54); the small panel
  drops the 44 tickers with `max_1d_move >= 1.0` and its SPY is a held-out benchmark, not a
  constituent. It runs **against** POS being real — the high-vol cohort is exactly where the
  missing delisted names would sit, so POS is flattered here and still loses on 2 of 3 panels.
* **Idea 128**: the IS window's SPY drawdown is shallower than the OOS window's; the IS
  drawdown bar admits too much for every arm equally.
* **Ideas 39/49**: the eligibility gate is inverted on the small panel, so every small-panel
  number here describes a gate that does not work there. Reported, not traded.
* **Idea 38** (calendar-day price index) and **idea 126** (t+1 execution only) carry over.
* No IWM in the cache, so the small panel is judged against SPY — stated, not adjusted.
