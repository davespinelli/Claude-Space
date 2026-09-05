# Idea 100 — sleeve-with-a-real-diversifier (cloud, 2026-09-05) — **PARK (strong)**

**Script:** `research/backtests/2026-09-05_sleeve-with-a-real-diversifier_cloud.py`
**Artefacts:** `.console.txt`, `.grid.csv`, `.correlation.csv`, `.convexity.csv`, `.walkforward.csv`,
`.loyo.csv`, `.ex2022.csv`, `.grossladder.csv`, `.costladder.csv`, memo `.memo.md`

## What was run

120 grid points, all reported: 5 sleeve fractions f ∈ {0, 0.25, 0.50, 0.75, 1.00} × 2 sleeves ×
3 books (live `v1`, idea 2's `top20` 4b KEEP, idea 10's `EWall`) × 2 universes × 2 gross
conventions (natural / gross-matched). Tuned parameters: exactly 2 (f and the sleeve). Books,
universes and conventions are reported controls, never selected on.

- **S9** — idea 26's sleeve verbatim (SPY QQQ IWM EFA EEM TLT GLD DBC UUP, 3-signal trend vote ×
  inverse-60d-vol risk parity). **Control: this run reproduces idea 26 exactly** — dSharpe vs the
  linear blend +0.052 mean, positive in 36/36; `top20 + 25% S9` at 10.8%/1.085/−16.0%, halves
  1.061/1.110, OOS 1.184; sleeve-to-book correlation 0.626–0.820.
- **S4** — the same construction on TLT GLD DBC UUP only.

## Results

**(1) The premise is confirmed, and by more than the queue supposed.** S4's daily-return
correlation to the three books is **−0.011 … +0.212** (against S9's 0.626 … 0.820), and to SPY
itself **−0.141**. The 5 equity ETFs were carrying essentially all of S9's correlation: removing
them moves the correlation by −0.50 to −0.78 in every cell.

**(2) The convexity is 5.1× larger, and 2.9× cheaper per unit of CAGR.** dSharpe against the
linear blend of the parts is positive in **36/36** interior cells for both sleeves, but averages
**+0.265 (range +0.070 … +0.479) for S4** against **+0.052 (+0.008 … +0.085) for S9**. Per
percentage point of CAGR surrendered, S4 buys a median **0.090** of Sharpe against S9's **0.031**.
The queue's question — *does a genuinely lower correlation buy the same Sharpe convexity at less
CAGR?* — answers **yes on the exchange rate, no in absolute CAGR**: S4 costs *more* total CAGR
(−3.19% vs −2.15% mean) because the sleeve itself earns only 2.6% standalone against S9's 5.0%.

**(3) Both objections that killed idea 26's by-product are repaired.**
- *Rule 8.* Idea 26's sleeve was **unselectable**: IS Sharpe was monotone decreasing in f, so the
  walk-forward picked f = 0 in every top20/EWall cell. With S4 the IS surface is no longer
  monotone — rule 8 picks **f = 0.50 in 8 of 8 S4 cells**, and the pick beats its own no-sleeve
  anchor out of sample in **8 of 8** (u56 top20 natural OOS 1.308 vs 1.168; broad EWall 1.232 vs
  1.019), with regret 0.000 … −0.104 (four cells at exactly 0.000, i.e. rule 8 lands on the grid's
  best OOS arm). This is a direct counter-example to idea 99's conjecture: defensive overlays are
  not rule-8-invisible *in general* — S9's invisibility was a property of an equity-correlated
  sleeve.
- *One-year dependence.* Idea 26's by-product had a sleeve contribution negative in 17/18 years.
  S4's year table looks the same (positive in 2/18: 2011 and 2022) — **but the Sharpe advantage
  does not depend on it**: with 2022 deleted, dSharpe(blend − anchor) stays positive in **8 of 8**
  S4 cells (mean shrink only −0.015), while S9's is negative in 4 of 8 both with and without 2022.
  Leave-one-year-out is also *kinder* to the S4 blend than to the bare book (worst-year deletion
  costs the anchor −0.077/−0.083 Sharpe and the S4 blend −0.065/−0.074).

**(4) And yet the literal 4b footprint is SMALLER than S9's.** Interior 4b passes: **S4 2/36, S9
4/36**; the only (sleeve, book, f) passing all four (universe × convention) combinations is still
**S9/top20/f=0.25** (idea 26's by-product). Every single S4 failure is on **one bar, the CAGR
floor** (70% of SPY = 10.66%): e.g. u56 `top20 + 25% S4` natural runs 10.2%/**1.144**/−14.2%,
halves 1.114/1.175, OOS 1.231 — clear of the Sharpe bars by 0.16–0.34 and of the drawdown cap by
6pp, and short of the CAGR floor by 0.5pp.

**(5) The CAGR shortfall is a gross artefact, not a return artefact.** The natural blend
de-grosses (0.648–0.700 average exposure against the book's 0.750) because the sleeve's trend vote
is often partial. Rescaling the rule-8-picked arm (`top20 + 50% S4`) to a fixed exposure moves
Sharpe by ≤ 0.001 across g ∈ {0.75, 0.85, 1.00, 1.25} — the exact-lever result of ideas 66/84
reproduced — and at **g = 1.00 (fully invested, no leverage) it clears 4b on BOTH universes**:
u56 **11.8% / 1.149 / −14.2%**, halves 1.099/1.197, OOS 1.236; broad **12.2% / 1.063 / −15.6%**,
halves 1.173/0.961, OOS 1.020. Both have materially better drawdowns than the incumbent
candidate's −18.3%/−20.1%.

**(6) Cost is where it is fragile.** At the natural gross the cross-universe 4b pass for
`top20 + 25% S4` holds at 5 bps and is lost by 10 (CAGR floor again). Sharpe itself degrades
−0.048/10 bps (u56) and −0.055/10 bps (broad) — comparable to the incumbent's, at 9.2–12.5x/yr
turnover. The g = 1.00 arm was **not** run across the cost ladder; that gap is the first thing the
follow-up must close.

## Verdict

**PARK**, not KEEP. The idea as worded is confirmed on its own mechanism and repairs both defects
that made idea 26's by-product unadoptable, but the 4b-passing version requires a **third dial**
(the exposure target g) that this run did not pre-register, and gross-tuning to clear a floor is
exactly the move PROTOCOL rule 7 warns about — even when idea 84 has already established that the
dial is exact and Sharpe-neutral. The honest reading is that `top20 + 50% S4 at 100% gross` is the
strongest 4b-passing book the project has produced on drawdown terms, and it deserves a clean,
pre-registered run rather than adoption off the back of a diagnostic ladder.

Recommended RULES wording: **none this week.** Proposed wording for the follow-up run is in
`.memo.md`, explicitly marked not-yet-adoptable. Rules unchanged.

Follow-ups queued: **101** (pre-registered fixed-g run of `top20 + 50% S4` with the full cost
ladder and the cadence-insensitivity bar), **102** (which of the four assets carries S4 — is this
TLT in a falling-rate sample?).

## Caveats

- SURVIVORSHIP: both equity panels are current constituents; every level is biased upward. The
  sleeve's four assets are ETFs and are not exposed to this.
- **The sample flatters TLT.** 2009–2021 is a falling-rate regime; a bond-heavy diversifier's
  standalone 2.6% CAGR and −8.7% MaxDD are not regime-neutral, and 2022 — the one year the sleeve
  earns its keep — is also the year the trend vote was *short* duration. Idea 102 exists to
  decompose this before anyone sizes the sleeve.
- Queue idea 38 (calendar-day index) applies: post-2014 weekends are zero-return rows, hitting
  every arm, baseline and SPY identically. Cross-arm comparisons are apples-to-apples; absolute
  Sharpe levels wait on idea 38.
- The gross ladder's g = 1.25 point is leverage, which PROTOCOL rule 2 forbids; it is reported
  only to locate the CAGR floor and is not an admissible book.
