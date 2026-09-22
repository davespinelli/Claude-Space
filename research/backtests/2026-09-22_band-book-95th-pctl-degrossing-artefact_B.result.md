# Idea 950 — is the BAND book's only 95th-percentile cell a DE-GROSSING artefact?

**Lane B, 2026-09-22.  VERDICT: KILL of the premise (ANSWERED = NO, decisively).  No KEEP, no memo.**
Script `2026-09-22_band-book-95th-pctl-degrossing-artefact_B.py`; console `.console.txt`; log `.log.txt`;
artifacts `.gates.csv` `.grossprofile.csv` `.books.csv` `.gain.csv` `.nulls.csv.gz` `.walkforward.csv`.

Two tuned parameters, both fully reported: **P1** gross-match rule ∈ {TARGET (945's), REALISED (this
run's daily exposure overlay)}; **P2** band ladder b ∈ {0.00, 0.02, 0.03, 0.04, 0.06, 0.08}, every rung
priced against b = 0.00 as side A.  Priced at **0 / 10 / 25 / 50 bps** on **SMALL** (945's cell) and
**U56** (robustness).  250 draws per (panel, band), 945's seed stream `(20260915, panel_i, setting_i, s)`
reused verbatim for the two bands 945 itself priced.  **Gates:** G1 (book == `rules_v2_weights`) PASS,
G2 (TARGET null's gross/count/weight == book's) PASS, G3 (REALISED null's drifted gross == book's,
max|dG| 1.11e-16) PASS, G4 (determinism) PASS, G5a (945's direction + percentile) PASS, G5b (945's
levels) FAIL by 0.0048 of book gain — tape vintage, stated below, not repaired.

---

## (A) THE ANSWER IS NO, AND THE PREMISE IS WRONG AT ITS ROOT

Swapping 945's TARGET-gross null for a null carrying the book's **DRIFTED** gross on every row moves
**nothing**. Across all 40 (panel, dial, cost) cells: median null gain shifts by at most **0.00159** of
Sharpe, the book's percentile inside its null by at most **2.40 pp**, and the ≥95th-percentile verdict
flips in **2 of 40** cells — once down (SMALL b0.03 @10 bps, 95.2 → 94.8) and once up (SMALL b0.08
@0 bps, 94.4 → 95.6), so the count is **14 of 40 under both rules**. On 945's own cell, SMALL /
0.00→0.06 @10 bps: percentile **100.0 → 99.6**, excess **+0.1086 → +0.1080**.

The reason is that **945's null was already realised-gross matched.** Because the BAND book holds k(t)
names at 1/N(t) and the null holds k(t) *random* names at the same 1/N(t), the two share their
exposure path to within the drift of the held names: the median realised-gross mismatch |null − book|
is **≤ 0.00031** on every one of the 12 (panel, band) cells. There was no exposure gap for the overlay
to close.

**The de-grossing hypothesis mis-identifies the axis.** Widening the band 0.00 → 0.08 moves median
realised gross by **0.0160** on SMALL (0.4233 → 0.4393) and **0.0228** on U56, i.e. under 4% of the
level — while it cuts annual turnover **2.07×** on SMALL (3.67 → 1.77) and **2.78×** on U56
(3.13 → 1.13). The band dial is a **turnover** dial, not a gross dial, and 945's G6 failure was a
mis-set bar (`median realised gross > 0.50` on a book whose design puts gated weight in cash), not a
mismatched null.

## (B) REPRODUCTION OF 945's CELL — DIRECTION AND PERCENTILE EXACT, LEVEL OFF BY THE TAPE

SMALL / D5_BAND (0.00→0.06) @10 bps, TARGET null, 250 draws: book gain **+0.0958** (945: +0.1006,
d 0.0048), null gain median **−0.0128** (945: −0.0115, d 0.0013), percentile **100.0** (945: 100.0),
median realised gross **0.4235** (945: 0.4286). The book leg carries **no** draw noise, so its 0.0048
gap is tape: 945 ran on a 2026-09-15 tape; the SMALL cache was rebuilt 2026-09-22 and ends 2026-09-18.
G5b is recorded FAIL rather than tuned to pass.

## (C) BY-PRODUCT — "THE ONLY 95th-PERCENTILE CELL" IS A (PANEL × COST) CORNER, AND IT INVERTS

945 read one band pair at one cost rung on three panels and found 1 of 15 cells clearing the bar. On
the ladder that pair sits in, **14 of 40** cells clear it, and the two panels run in **opposite
directions across the cost axis**:

| panel | 0.00→0.06 percentile @ 0 / 10 / 25 / 50 bps | book gain @ same rungs |
|---|---|---|
| SMALL | 95.2 / **100.0** / 97.6 / 80.4 | +0.0699 / +0.0958 / +0.1346 / +0.1993 |
| U56   | 61.6 / 87.2 / **99.2** / **100.0** | −0.0566 / −0.0294 / +0.0115 / +0.0798 |

At 945's own 10-bps rung the band dial clears the bar on **4 of 5** SMALL rungs (b 0.03 / 0.04 / 0.06 /
0.08) and **0 of 5** U56 rungs; at 50 bps SMALL clears **0 of 5** and U56 **4 of 5**. The book's raw
gain rises monotonically with cost on both panels — it is a turnover rebate — but so does the null's,
and which side wins the race is a panel fact. 945's "single 95th-percentile cell" is a statement about
the grid 945 read, not about the band dial.

## (D) CAPITAL (PROTOCOL 3 / 4) — 4a 0 of 12, 4b 0 of 12, AND THE BINDING LEG IS CAGR

Every rung scored with `baseline.compare()` at 10 bps weekly against RULES v2 (live), RULES v1 and SPY.
**4a: 0 of 12.** **4b: 0 of 12.** On U56 legs L1/L2/L3/L4 pass at **every** band and only the CAGR
floor fails (book CAGR 8.2–8.6% against SPY's 15.1%, floor 10.6%); on SMALL four legs fail. The band
axis buys Sharpe on SMALL (0.66 → 0.76 over the ladder) and loses it on U56 past b=0.03
(1.20 → 1.14) while MaxDD worsens monotonically on both (SMALL −12.3% → −14.5%, U56 −12.0% → −14.5%).

## (E) RULE 8, 2017–2026 READ ONCE — THE IS CHOOSER PICKS THE WIDEST RUNG AND LOSES

Band chosen on 2009–2016 IS Sharpe alone; IS argmax is **b = 0.08 on both panels** (SMALL IS ranking
0.722 / 0.818 / 0.863 / 0.882 / 0.935 / 0.965; U56 1.055 / 1.085 / 1.104 / 1.061 / 1.055 / 1.122 — a
non-monotone ladder whose argmax is 0.018 above its runner-up).

| panel | series | OOS CAGR | OOS Sharpe | OOS MaxDD |
|---|---|---|---|---|
| SMALL | 950 pick b=0.08 | 4.61% | 0.6603 | −14.51% |
| SMALL | RULES v2 (live) | 4.41% | 0.6472 | −12.48% |
| U56 | 950 pick b=0.08 | 8.97% | 1.1635 | −14.47% |
| U56 | RULES v2 (live) | 9.46% | 1.2767 | −12.05% |
| both | SPY | 15.29% | 0.8751 | −33.72% |

**OOS 4b FAIL on both panels** (CAGR floor: 4.61% and 8.97% against SPY's 10.70% bar; the DD cap passes
with room, −14.5% against a −20.23% cap). **OOS 4a FAIL on both**: SMALL gains +0.013 of Sharpe but
gives up 2.03 pp of MaxDD, U56 gives up both (−0.113 Sharpe, −2.42 pp DD). The live book is not beaten
by any band rung the IS window would have chosen.

---

**WHAT THIS RUN CANNOT DO (stated, not repaired).** One book FORM (the live BAND book at gross 0.75),
one cadence (weekly), one offset (the canonical weekly phase) — the rebalance-offset spread idea 914
and the 2026-09-22 cloud run price is not read here, so every margin above is a single-phase margin.
The null is uniform-without-replacement over the priced pool, 945's convention; a turnover-matched or
momentum-matched null is a different object. 250 draws bound a percentile to ±~2 pp, which is why the
two verdict flips in (A) are reported as flips and not as a change.

**SURVIVORSHIP (rule 9).** SMALL is a current-constituent sub-$2B screen (`data/SMALL_PANEL_README.md`)
and U56 is a current-constituent list, so every absolute level above is optimistic. The book-vs-null
contrast is within-tape — same names, same dates, same exposure path, only WHICH names moves — and
does not repair the level.

**RESIDUE, not a rules change (rule 6; RULES.md, PROTOCOL.md, scan.py, bot.py, baseline.py untouched).**
(1) 945's G6 bar (`median realised gross > 0.50`) is wrong for any book that parks gated weight in cash;
the correct invested-ness gate for such a book is the null-vs-book gross *mismatch*, which is what (A)
reports. (2) A percentile published against a gross-matched null should name its **cost rung and its
panel**: on this family the same dial reads 100.0 and 61.6 at two rungs of the same ladder.
