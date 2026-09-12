# Idea 813 — does TIE SUFFICIENCY break outside the SPYDD CONFOUND on any corpus with 30+ ties?
lane C, 2026-09-12 · script `2026-09-12_does-TIE-SUFFICIENCY-break-outside-the-SPYDD-CONFOUND-on-any-corpus-with-30-PLUS-TIES_C.py`

## ANSWER = YES. SUFFICIENCY BREAKS, AND IT BREAKS OUTSIDE THE CONFOUND.

Idea 596 published the DECLINE-leg tie predicate as **exact in both directions** (necessity and
sufficiency = 1.0000, 0 counterexamples). Idea 811 found its first 3 counterexamples and reported
them as confounded — every one SPYDD, the family that gates on the drawdown itself. This run built
the corpus the queue asked for and the confound story does **not** survive it.

**The corpus the queue specified exists.** Pooled (panel, window) cells whose CONTROL-U binding
decline runs longer than 60 trading days: **14 of 21 cells, 897 scored arms (299 distinct gate
configurations × 3 gross), 111 MaxDD ties (37 distinct), 114 arms satisfying the DECLINE predicate
(38 distinct)**, median decline **273 trading days** against the FULL window's 17. Both existence
bars pass — ≥ 30 ties with all families (111) and with SPYDD dropped (90). This is the first time
596's sufficiency leg has been read on a powered long-decline corpus; 811 could only report a
vacancy (0 predicate arms in 117).

**Sufficiency is not exact there: P(tie | DECLINE) = 0.9737 (114 predicate arms, 3 false
positives), and with SPYDD dropped 0.9677 (93 arms, the same 3 false positives).** All three
long-decline false positives are **CORR 0.30 on SMALL**, i.e. outside the confound. **H_BREAK
PASSES.**

**The confound story fails as a general claim.** Over all 1,404 scored arm-windows there are 15
false positives (5 distinct configurations): **CORR 9, VOL 3, SPYDD 3** — SPYDD's share of false
positives is **0.200** against its share of the predicate population **0.2043**. It is not where
the breaks concentrate; it is simply where 811's 4-family corpus could see them. **H_CONFSHR
FAILS**, and that failure is the finding.

**596's exactness is a property of its corpus, not of the predicate.** On the FULL window — the
very window 596 published — sufficiency reads **0.9677** once the corpus carries 6 families × 5
dials instead of 4 × 4. The reproduction gate G5 confirms this is not a data disagreement: the
596/811 sub-corpus on FULL still returns **141 scored arms / 45 ties / necessity 1.0000 /
sufficiency 1.0000 / ties SPYTR 0, BREADTH 12, VOL 18, SPYDD 15**, field for field.

**The mechanism, measured not asserted:** in all 15 false positives the arm is **deeper** than its
control (dMaxDD_U −0.18% to −3.34%) and in 12 of 15 its own trough sits on a **different date**.
The shape is a whipsaw — the gate sits out the control's decline, fires *after* the trough, and is
back on for a later decline it then rides deeper. A gate that never touches the control's decline
leg is therefore **not** sufficient for a MaxDD tie, and the counterexample does not need the
drawdown-gated family to exist.

**Necessity survives, as it must.** P(DECLINE | tie) = **1.0000** on every corpus and at every
cover rung: an arm holding the control's weights through peak → trough reproduces that decline
exactly. This leg is near-identity by construction and is reported as a sanity check, not evidence.

## The tuned grid (2 params, 14 points, all reported)

Leg = DECLINE, headline cover bar eps = 0. Cover ladder {0, 1e-12, 1e-6, 1e-4, 1e-3} flat at every
rung (`.predicates.csv`).

| window | dec_d (med) | scored | #pred | #tie | P(pred\|tie) | P(tie\|pred) ALL | P(tie\|pred) NO-SPYDD | FP |
|---|---|---|---|---|---|---|---|---|
| FULL | 17 | 246 | 93 | 90 | 1.0000 | **0.9677** | 0.9583 | 3 |
| PRE20 | 147 | 219 | 48 | 48 | 1.0000 | 1.0000 | 1.0000 | 0 |
| E2011 | 147 | 213 | 42 | 42 | 1.0000 | 1.0000 | 1.0000 | 0 |
| E2015 | 132 | 168 | 39 | 33 | 1.0000 | **0.8462** | 0.8333 | 6 |
| E2018 | 77 | 168 | 12 | 9 | 1.0000 | **0.7500** | 0.7500 | 3 |
| POST20 | 302 | 204 | 36 | 33 | 1.0000 | 0.9167 | 1.0000 | 3 |
| BEAR22 | 336 | 186 | 9 | 9 | 1.0000 | 1.0000 | 1.0000 | 0 |
| **QUALIFY** (pooled long-decline) | **273** | **897** | **114** | **111** | **1.0000** | **0.9737** | **0.9677** | **3** |

POST20 reproduces 811 exactly: 3 false positives, all SPYDD, and the break vanishes when the
family is dropped (1.0000). It is the *only* window where that is true.

## Pre-registered hypotheses — 7 of 9 pass

| | |
|---|---|
| H_CORPUS ≥ 30 ties on a > 60-day-decline corpus exists | **PASS** (111) |
| H_CORPUSX same with SPYDD dropped | **PASS** (90) |
| H_PRED ≥ 30 predicate arms there | **PASS** (114) |
| H_NEC necessity = 1.0000 | **PASS** |
| H_SUFF sufficiency = 1.0000, all families (596's claim) | **FAIL** (0.9737) |
| H_BREAK sufficiency breaks OUTSIDE SPYDD [load-bearing] | **PASS** (3 of 3 non-confound) |
| H_CONFSHR SPYDD over-represented among false positives | **FAIL** (0.200 vs 0.2043) |
| H_LONG tie rate lower on long declines | **PASS** (12.4% vs 36.6%) |
| H_COST DECLINE ≡ DECLINE+COST | **PASS** (0 disagreements, all 7 windows) |

## Gates — all pass

G1 never-firing arm ≡ CONTROL-U **0.000e+00** · G2 `fast_run` ≡ `engine.backtest` **1.388e-17** ·
G3 every (panel, gross, window) binding episode reproduces its window MaxDD **0.000e+00** ·
G4 CONTROL-M mean gross ≡ arm's **1.778e-04** · G5 reproduction of 811's committed FULL cell
**exact on all five fields**.

## PROTOCOL rule 8 and both KEEP paths — KILL for capital, no candidate

Dial chosen on IS by IS Sharpe alone, OOS read once. (a) standing 2016/2017 split on FULL;
(b) window-local half split on the six short windows, a stated departure reported beside (a).

FULL-window OOS comparands: **SPY 15.33% / 0.877 / −33.72%**; RULES v2 **9.47% / 1.278 / −12.05%**
(U56), 7.88% / 1.106 / −12.24% (B136), 3.75% / 0.560 / −13.89% (SMALL). Rule-8 picks passing 4b OOS
**6 of 54**, 4a OOS **2 of 54**.

Best full-sample 4b cell, U56 VOL ≤ 0.25 at g = 1.00: **11.08% / 1.210 / −9.57%** (halves
1.305 / 1.125), OOS **11.58% / 1.239 / −9.57%** — and its own gross-matched CONTROL-M passes 4b
too, so the pass is exposure, not the clause. This is idea 810's arm, already killed for capital on
the record, and it re-reads here field for field.

| window | scored | 4a | 4b | 4a OOS | 4b OOS | BOTH | 4b & 4b-OOS | … & beats CONTROL-M |
|---|---|---|---|---|---|---|---|---|
| FULL | 246 | 6 | 16 | 15 | 17 | 0 | 11 | **0** |
| PRE20 | 219 | 8 | 9 | 1 | 24 | 0 | 8 | 1 |
| E2011 | 213 | 6 | 0 | 3 | 0 | 0 | 0 | **0** |
| E2015 | 168 | 0 | 19 | 3 | 4 | 0 | 4 | **0** |
| E2018 | 168 | 5 | 2 | 8 | 0 | 0 | 0 | **0** |
| POST20 | 204 | 2 | 15 | 1 | 5 | 0 | 5 | **0** |
| BEAR22 | 186 | 20 | 0 | 13 | 0 | 0 | 0 | **0** |

The single row anywhere that clears both windows and beats its matched control is B136 DISP ≤ 0.15
at g = 1.00 in **PRE20** (10.95% / 1.173 / −10.46% vs CONTROL-M 9.56% / 1.142 / −9.12%) — a window
that ends in 2019 and is entirely in-sample under the record's own 2016/2017 convention, read off a
270-arm grid at 3.44×/yr turnover. It is a grid artefact, not a candidate, and nothing here is
proposed for RULES.

## Power and limits, stated with the result

- Arms come in **gross triples** and the three gross levels of one gate are near-duplicates. The
  15 false positives are **5 distinct configurations**; the 3 on the qualifying corpus are **one**
  (SMALL / CORR 0.30). The *existence* of a non-confound counterexample is therefore established;
  its *rate* is not, and no decimal place on 0.9737 should be relied on.
- The pooled long-decline corpus re-uses arms across **overlapping** windows (PRE20 ⊃ E2011,
  POST20 ⊃ BEAR22). Stated, not netted; the per-window table above is the un-pooled read.
- The corpus was widened, as pre-registered, by one loose dial per family and two extra families
  (CORR, DISP — idea 606's). This is exactly why 596 could see no counterexample: its 16 dials
  contained none. The widening is declared, every arm is reported, and G5 shows it leaves 596's own
  cell untouched.
- 33 of 1,404 scored rows are **all-cash** in their window (gate never turns on). They never tie,
  never satisfy the predicate, and fail both KEEP paths by construction. Count disclosed, not
  netted, because the 596/811 corpus is defined on fire_rate == 0 alone.
- 486 of 1,890 rows are **degenerate** (gate never fires in that window; the arm *is* the control)
  and are excluded from every rate.
- SURVIVORSHIP: all three panels are current-constituent lists, SMALL worst
  (`data/SMALL_PANEL_README.md`). Rates are within-panel agreement rates and are far less exposed
  than levels, but every Sharpe/CAGR here carries the full bias. Several windows are 3–5 years and
  bull-heavy; no level from them is a capital claim.

## What the record should now say

596's tie predicate is **necessary by construction and not sufficient**. The sufficiency figure it
published (1.0000) is a reading of a 4-family × 4-dial corpus, not a property of the predicate, and
811's attribution of the break to the SPYDD confound holds only in the one window it measured.
Any claim in the record that relies on the DECLINE cover being *equivalent* to a MaxDD tie should
be restated as one-directional.

No RULES change, no KEEP claimed, no memo, no PROTOCOL edit (rule 6). `RULES.md`, `PROTOCOL.md`,
`research/scan.py`, `products/bot/bot.py` and `research/baseline.py` are untouched.
