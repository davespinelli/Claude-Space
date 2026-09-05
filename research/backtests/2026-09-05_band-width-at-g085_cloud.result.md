# Idea 91 — band-width-at-g085 · ANSWERED (KILL of the gross-shortfall hypothesis; 3% survives)

**Question (pre-registered).** Idea 84 fixed the gross dial at g = 0.85 on idea 57's 3% re-entry
band but never re-opened the band, which had been chosen at g = 0.75. Sweep band in
{0, 2, 3, 5, 8}% at g = 0.85 on both large-cap universes at 10 and 25 bps: is 3% still right, or
was the band absorbing a gross shortfall?

**Run.** 5 bands × 5 gross levels {0.55, 0.65, 0.75, 0.85, 1.00} × 2 universes (u56, broad) ×
2 books (equal-weight-all, ranked top-20) × 2 cost rungs = **200 points, every one printed**.
Weekly, t+1, eligibility = 200d MA (banded) AND vol20 < 0.60. Idea 84's script is imported, not
re-implemented. Two tuned parameters, both swept exhaustively: band width and gross.

**Reproduction before anything new was read.** The band-parameterised weight builder equals idea
84's three fixed books at 0 differing cells (band 3% → C57/ew-band3; band 0 → C72/EWall and
C2/CAND20); `run` vs `engine.backtest` max|diff| = 0.0; and idea 84's published rows come back
exactly — u56 12.8% / 1.135 / −17.1% (halves 1.11/1.16), broad 12.6% / 1.062 / −18.9% (1.16/0.97).

## Answer

1. **The two dials are orthogonal on Sharpe.** Holding the band fixed, full-sample Sharpe moves at
   most **0.0048** (median 0.0012) across the entire 0.55–1.00 gross ladder; OOS Sharpe likewise
   (max 0.0047). The Sharpe-optimal band is **identical at every g in 8 of 8 cells** (8% in six,
   3% in one, 0% in one). The band-optimal width does not move when the exposure dial moves, so
   the premise "the band was chosen at the wrong g" has no room to be true.
2. **The substitution mechanism is refuted, with its sign reversed.** A wider band very slightly
   *lowers* mean realised gross (0.8375 → 0.8353 at g = 0.85 going 0% → 8%), it does not raise it.
   What the band buys is turnover: 9.3 → 3.7 turns/yr on u56/ew-all @10 bps.
3. **But the band is a real instrument, not noise.** Against a matched-gross control — the
   unbanded book of the same cell interpolated along its own g ladder to the banded point's own
   realised gross — the band wins full-sample Sharpe in **116/144** matchable points and OOS
   Sharpe in **136/144**. At band 3: +0.052 Sharpe, +0.075 OOS Sharpe, +0.59 pp CAGR, 0.59 pp
   shallower drawdown, −1.97 turns/yr.
4. **3% is not the Sharpe argmax, and should still be pinned.** 8% wins Sharpe in 6 of 8 cells but
   pays for it in drawdown. Pooled over 40 points each, 4b passes run 0% → 5, 2% → 9, **3% → 11**,
   5% → 10, 8% → 9; at g = 0.85, 2/4/4/4/2. Under PROTOCOL rule 8 (band chosen on 2009–2016 alone,
   2017–2026 read once) over all 40 cells: **PIN3 12.3% / 1.054 / −17.7%** beats **SEL-IS
   12.3% / 1.025 / −18.9%** and the unbanded **CTL0 11.5% / 0.983 / −18.3%**, and passes 4b 11/40
   against 9/40 and 5/40. The IS window picks 8% in 30 of 40 cells and it does not hold up.

**Verdict: ANSWERED. KILL of the gross-shortfall hypothesis. 3% survives the move to g = 0.85 and
is better pinned than re-chosen.** No new book, no KEEP candidate, no RULES change proposed. The
only place the two dials interact at all is the 4b *level* bars (CAGR floor, DD cap) — never
through Sharpe, which is why the interaction shows up in pass counts and nowhere else.

**Caveats.** Survivorship (both panels are current-constituent lists), which flatters
stay-invested settings — i.e. the wide-band end this run argues against, so the finding is if
anything understated. Idea 38 (calendar-day index), idea 126 (t+1 only), idea 128 (the IS window's
crash is shallower than the OOS window's, which is why the IS-4b selector abstains in 29 of 40
cells). The matched-gross control matches mean realised gross, not the path of it.
