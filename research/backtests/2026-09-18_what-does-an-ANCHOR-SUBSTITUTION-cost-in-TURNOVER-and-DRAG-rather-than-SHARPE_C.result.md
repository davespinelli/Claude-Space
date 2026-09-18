# Idea 1236 (lane C, 2026-09-18) — what does an ANCHOR SUBSTITUTION cost in TURNOVER and DRAG rather than SHARPE?

**VERDICT: KILL (capital), NO NEW BOOK. ANSWERED NO — THE QUEUE'S PREMISE IS REFUTED. Only
1.9% of 1224's committed +0.0211 is the turnover rebate; 98.1% survives with costs switched
OFF, and NO cost rung makes the gain entirely the rebate because the ANCHOR IS NOT A SLOW
BOOK.** Outcome (C) MOSTLY GROSS at all three pick sets. 15 of 16 gates; the one failure is
reported below and is a tape-drift fact, not a machinery fact. Runtime 22s, offline,
deterministic.

Script: `2026-09-18_what-does-an-ANCHOR-SUBSTITUTION-cost-in-TURNOVER-and-DRAG-rather-than-SHARPE_C.py`
Dials (2, PROTOCOL rule 4): **COST RUNG** {0, 10, 25, 50} bps x **PICK SET** {P_1214, P_AXIS,
P_TEXT}. 12 cells, every one published in `.grid.csv`. The substitution rule is FROZEN at
S_ALL (1224 proved S_ALL / S_SE1 / S_SE2 / S_ANC95 decision-identical on 0 of 620 differing
cells, so it is not a live dial). The PICKS are frozen at the record's own 10 bps rung —
the queue says "re-price the SAME 168 picks".

    DELTA(c) = OOS Sharpe(anchor book @ c) - OOS Sharpe(the book the record picked @ c)
    GROSS PART = DELTA(0);  REBATE(c) = DELTA(c) - DELTA(0);  SHARE(c) = REBATE(c)/DELTA(c)
    ENTIRELY THE REBATE at rung c  <=>  SHARE(c) >= 1.0  <=>  DELTA(0) <= 0 < DELTA(c)

---

## 1. The answer — all 12 cells

| pick set | cost | picks | move | mean ann turnover pick / anchor | DELTA | SE | t | **SHARE** |
|---|---|---|---|---|---|---|---|---|
| P_1214 | 0 | 42 | 1.000 | 3.662 / 3.469 | +0.0681 | 0.0516 | +1.32 | **0.000** |
| P_1214 | 10 | 42 | 1.000 | 3.662 / 3.469 | +0.0690 | 0.0513 | +1.35 | **+0.014** |
| P_1214 | 25 | 42 | 1.000 | 3.662 / 3.469 | +0.0705 | 0.0510 | +1.38 | +0.035 |
| P_1214 | 50 | 42 | 1.000 | 3.662 / 3.469 | +0.0731 | 0.0504 | +1.45 | +0.068 |
| P_AXIS | 0 | 168 | 0.583 | 3.426 / 3.469 | +0.0209 | 0.0282 | +0.74 | **0.000** |
| **P_AXIS** | **10** | **168** | **0.583** | **3.426 / 3.469** | **+0.0213** | **0.0282** | **+0.75** | **+0.019** |
| P_AXIS | 25 | 168 | 0.583 | 3.426 / 3.469 | +0.0219 | 0.0283 | +0.77 | +0.048 |
| P_AXIS | 50 | 168 | 0.583 | 3.426 / 3.469 | +0.0230 | 0.0285 | +0.81 | +0.092 |
| P_TEXT | 0 | 620 | 0.806 | 3.336 / 3.517 | +0.0191 | 0.0104 | +1.83 | **0.000** |
| P_TEXT | 10 | 620 | 0.806 | 3.336 / 3.517 | +0.0205 | 0.0105 | +1.95 | +0.068 |
| P_TEXT | 25 | 620 | 0.806 | 3.336 / 3.517 | +0.0226 | 0.0106 | +2.13 | +0.154 |
| P_TEXT | 50 | 620 | 0.806 | 3.336 / 3.517 | +0.0260 | 0.0108 | +2.42 | +0.266 |

**The rung at which the Sharpe gain is entirely the rebate: THERE IS NONE, and there cannot
be one.** SHARE reaches 1.0 only if DELTA(0) <= 0, and DELTA(0) is +0.0209 (P_AXIS) /
+0.0191 (P_TEXT) / +0.0681 (P_1214) — 98.1% / 93.2% / 98.6% of each committed figure is
already there with costs switched off. Even at **50 bps, five times PROTOCOL rule 2's rung**,
the rebate is 9.2% (P_AXIS) and 26.6% (P_TEXT) of the total. 931's mechanism is real and it
is **an order of magnitude too small to be this number**.

## 2. Why — the anchor is not a slow book (`.anchorrank.csv`, `.turnover.csv`)

The queue's premise needs the anchor to be the SLOW rung that collects 931's rebate. It is
not. Annualised one-way turnover, anchor rank inside its own ladder, 1 = slowest:

| panel | N | H | GROSS | CADENCE | anchor turnover |
|---|---|---|---|---|---|
| U56 | 3 of 6 | 2 of 4 | **10 of 10** | **2 of 2** | 2.872 |
| B136 | 3 of 6 | 2 of 4 | **10 of 10** | **2 of 2** | 3.247 |
| SMALL | 3 of 6 | 2 of 4 | **10 of 10** | **2 of 2** | 4.149 |

**The anchor is the FASTEST rung of its own GROSS ladder and of its own CADENCE ladder on all
three panels, and mid-ladder on N.** Pooled over the queue's 168 picks it turns over 3.469
times a year against the picks' 3.426 and pays **MORE** drag, not less: 0.394 pp/yr against
0.388 at 10 bps, 0.984 against 0.968 at 25, 1.960 against 1.928 at 50. The anchor is the
faster book at only 0.333 of the 168 picks; median turnover difference 0.000.

So the small positive rebate that does exist is not the anchor being slow — it is a handful
of very fast picks being punished. The H ladder's fast rung turns over 6.078 (U56), 7.755
(B136) and **10.951 (SMALL)** times a year against the anchor's 2.872 / 3.247 / 4.149; at 50
bps that rung alone loses 3-5 pp/yr of CAGR. Pooled, that tail moves DELTA by +0.0004 between
0 and 10 bps. **It is a tail effect on four cells, not a rebate every book collects.**

## 3. Where the sign lives, at every rung (`.bycut.csv`, P_AXIS)

| cut | value | turn pick / anchor | @0 | @10 | @25 | @50 |
|---|---|---|---|---|---|---|
| ladder | **N** | 3.539 / 3.469 | **+0.1074** (t +3.12) | +0.1073 (+3.10) | +0.1071 (+3.07) | +0.1068 (+3.03) |
| ladder | H | 3.709 / 3.469 | **-0.0617** (-0.83) | -0.0592 (-0.80) | -0.0553 (-0.74) | -0.0489 (-0.64) |
| ladder | CADENCE | 3.328 / 3.469 | +0.0369 (+1.22) | +0.0361 (+1.20) | +0.0348 (+1.16) | +0.0327 (+1.11) |
| ladder | GROSS | 3.126 / 3.469 | +0.0009 (+2.30) | +0.0010 (+2.45) | +0.0012 (+2.65) | +0.0014 (+2.89) |
| panel | U56 | 2.847 / 2.841 | +0.0335 | +0.0336 | +0.0337 | +0.0339 |
| panel | B136 | 3.589 / 3.313 | +0.0620 | +0.0639 | +0.0668 | +0.0717 |
| panel | SMALL | 3.841 / 4.253 | -0.0329 | -0.0336 | -0.0347 | -0.0366 |

**1224's headline cut is COST-INVARIANT.** The N axis (+0.1074 at t +3.12 with costs OFF)
and the H axis that pays the other way (-0.0617) are both there at 0 bps and move by less
than 0.006 of Sharpe over the whole 0-50 bps range. 1224's finding that the record has one
expensive axis and one that pays **is not a cost artefact**; the sign disagreement is
economic. The one exception is GROSS, whose t rises from +2.30 to +2.89 on a delta of a
tenth of a basis point of Sharpe — the degenerate ladder again (1189/1214/1224), and one more
reason never to read a GROSS t-statistic as economic.

## 4. ARM D — the re-booking cost the sliced accounting omitted runs the OTHER WAY (`.stitched.csv`)

The queue's second charge is the sharper one: 1224 read every fold's OOS Sharpe off a book
run CONTINUOUSLY over the whole tape, so a pick that CHANGED between folds was never charged
for the switch. The REALISED STITCHED book — fold f's IS argmax held through fold f, true
turnover paid on the switch day — **43 switches across 12 (panel, ladder) books**:

| cost | mean d_Sharpe (anchor - stitched) | anchor wins | ann turnover stitched / anchor |
|---|---|---|---|
| 0 | +0.0331 | 10 of 12 | 3.670 / 3.472 |
| 10 | +0.0348 | 10 of 12 | 3.670 / 3.472 |
| 25 | +0.0374 | 10 of 12 | 3.670 / 3.472 |
| 50 | +0.0417 | 10 of 12 | 3.670 / 3.472 |

**Charging the omitted cost makes the anchor look BETTER, not worse.** The realised moving
book turns over 3.670 a year against the anchor's 3.472 and the anchor's edge WIDENS from
+0.0331 to +0.0417 across the cost ladder. 1224's accounting, which the queue suspected of
flattering the anchor, in fact **understated** it: the substitution's realised advantage on
the stitched books is larger than the +0.0213 read off the slices. 4a 0 of 12 stitched books;
4b 1 of 12 stitched against 4 of 12 anchor at 10 bps.

## 5. Robustness (reported, not a dial) — a chooser that pays its own costs (`.robust.csv`)

If the chooser ALSO sees rung c it does pick slower rungs (move rate 0.6131 -> 0.5833 ->
0.5417 -> 0.5595) and the delta falls: **+0.0157 / +0.0213 / +0.0159 / +0.0052** at 0 / 10 /
25 / 50. A cost-aware chooser at 50 bps closes three quarters of the gap — but it closes it
by becoming the anchor, not by beating it, which is the eighth arrival at the same sentence.

## 6. Rule 8 and both KEEP paths (`.walkforward.csv`) — nothing promoted

Every rung chosen on warm-up..2016-12-31 ONLY, at its own cost rung; 2017-2026 read once.
**96 rule-8 rows** (3 panels x 4 ladders x 4 cost rungs x {IS_ARGMAX, ANCHOR}).

**4a 0 of 96 full and 0 of 96 OOS** — live RULES v2's -12.05% MaxDD is shallower than every
growth book, as it has been at every previous attempt. **4b full 25, 4b OOS 24, BOTH 24.**
By arm: ANCHOR **4 of 12 at every one of the four cost rungs**; IS_ARGMAX 3 / 2 / 2 / 1 as
cost rises. Every 4b pass is on U56 and every one of them is the SAME realised book — the
committed 2026-09-04 anchor (N=20 / H=126 / gross 0.75 / weekly) reached down four ladders.

The one capital-relevant fact worth keeping, and it is about the INCUMBENT rather than this
idea: **the standing 4b pass survives a 5x cost shock.**

| cost | OOS CAGR | OOS Sharpe | OOS MaxDD | 4b |
|---|---|---|---|---|
| 0 bps | 17.63% | 1.2039 | -19.08% | T |
| **10 bps (live)** | **17.28%** | **1.1832** | **-19.13%** | **T** |
| 25 bps | 16.77% | 1.1522 | -19.20% | T |
| 50 bps | 15.91% | 1.1003 | -19.35% | T |

against U56 OOS SPY 15.28% / 0.8747 / -33.72% (H 0.9915/0.7488) — DD cap -20.23%, CAGR floor
10.70%. At 50 bps the book still clears the CAGR floor by 5.2 pp and the DD cap by 0.88 pp.
Its whole-book drag is 0.333 / 0.831 / 1.656 pp/yr of CAGR at 10 / 25 / 50 bps on 2.872
turns a year. **CONFIRMATORY, NOT GENERATIVE — NOT PROMOTED, NO RULES CHANGE (rule 6).**
Chooser-minus-anchor on the rule-8 split: +0.0233 / +0.0294 / +0.0274 / +0.0328 at 0/10/25/50.

Benchmarks (OOS 2017-2026): U56 SPY 15.28% / 0.8747 / -33.72%, LIVE v2 9.47% / 1.2781 /
-12.05%; B136 SPY 15.33% / 0.8769, LIVE 7.88% / 1.1061; SMALL SPY 15.33% / 0.8769, LIVE
4.47% / 0.6518.

## 7. Survivorship (rule 9)

U56 (55 names) and B136 (135) are CURRENT constituents; SMALL is the sub-$2B screen, 664
investable of 715 after dropping every ticker with max_1d_move >= 1.0, and starts 2010. SPY
is excluded from every eligible set and used as benchmark only. The bias does not cancel out
of the OOS levels or the 4b legs, so every pass above is an upper bound.

## 8. Gates — 15 of 16, and the failure is the tape, not the machinery

G1 fast runner @10bps == engine.backtest 2.08e-17 · G2 r(c) = gross - turn*c/1e4 ==
engine.backtest at EVERY cost rung 2.08e-17 · G3 live RULES v2 U56 MaxDD -12.0549% ==
committed -12.05% · G4 the anchor rung of all four ladders is ONE book, returns AND turnover,
0.0 · G5 the 0 bps rung is the gross book exactly 0.0 · G6 folds tile all three panels ·
G7 every harvested rung is a committed ladder rung (0 bad) · G8 P_AXIS is 1224's 168 cells ·
G9 a pick already AT the anchor has delta 0 at every cost rung 0.0 ·
**G10 P_AXIS delta/SE replays 1224 on the LIVE tape 2.01e-04 (bar 5e-4) — PASS;
G10 P_1214 5.45e-04 — FAIL** · G11 both legs replay 1224's LEVELS on 1224's own tape
(truncated to 2026-09-16) to **3.36e-05 / 4.38e-05 — PASS** · G12 the stitched books switch
43 times.

**The G10 failure is a REPRODUCIBILITY fact and is reported as one, not tolerated.**
`data/prices.csv` is rewritten by the nightly close: this tree's U56 tape ends 2026-09-17,
1224's ended 2026-09-16. **ONE EXTRA TRADING DAY moves the committed LEVELS by 2.61e-03 and
the P_1214 delta by 5.45e-04.** The 5e-4 bar was set from the P_AXIS drift before P_1214 was
read; P_1214 exceeds it, and the bar was NOT widened afterwards to make it pass. G11 is the
correct replay and it is exact: re-run on the tape 1224 actually read, both legs come back to
4e-05. **A committed number on this record is reproducible to ~4e-05 against its own tape and
to ~3e-03 against tomorrow's**, which is the operational size of the question idea
`is-the-RECORD-REPRODUCIBLE-AT-ALL-while-prices-csv-is-REWRITTEN-NIGHTLY` raised and is worth
a schema line: **a committed replay tolerance must name the tape it was measured against.**

## 9. What this leaves for the queue

1224's +0.0204 / +0.0211 stands, and it stands for the reason 1224 gave. Three sentences are
worth a header: **(i) the anchor is a MID-TO-FAST book, not a slow one — it is the fastest
rung of its own GROSS and CADENCE ladders on all three panels, so the substitution has no
rebate to collect and 931's mechanism does not reach it**; **(ii) the re-booking cost the
sliced accounting omits runs in the anchor's FAVOUR (+0.0331 -> +0.0417 across 0-50 bps on
the realised stitched books), so 1224's figure is a floor rather than a ceiling**; **(iii)
the N-vs-H sign disagreement is cost-invariant to within 0.006 of Sharpe over a 5x cost
range, so it is economic and the record should keep pricing those axes separately.** Three
follow-ups filed, all price-only.
