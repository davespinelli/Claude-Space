# Idea 1224 (lane C, 2026-09-17) — what does the RECORD's TUNING COST once every UNRESOLVABLE DIAL CALL is replaced by the ANCHOR?

**VERDICT: KILL (capital). ANSWERED = +0.0204 of OOS Sharpe (SE 0.0105, t +1.94) on the
record's own committed rule-8 picks, and the word UNRESOLVABLE is VACUOUS — 0 of 620
committed pick-cells resolve against the anchor under ANY honest bar.** 14 of 14 gates pass.
Runtime 19s, offline, deterministic. No new book.

Script: `2026-09-17_what-does-the-RECORD-s-TUNING-COST-once-every-UNRESOLVABLE-DIAL-CALL-is-replaced-by-the-ANCHOR_C.py`
Dials (2, PROTOCOL rule 4): **PICK SET** {P_1214, P_AXIS, P_TEXT} x **SUBSTITUTION RULE**
{S_NONE, S_ALL, S_SE1, S_SE2, S_ANC95}. 15 cells, every one published in `.grid.csv`.
Nothing selected on. `DELTA = OOS Sharpe(substituted book) − OOS Sharpe(the book the record
picked)`, so POSITIVE = the record's tuning cost it that much.

---

## 1. The harvest — what the record actually committed

33,861 committed units (LEADERBOARD.md rows, CHANGELOG.md paragraphs, 1,160 `research/backtests/*.md`).
10,398 (0.3071) sit in a rule-8 / walk-forward / OOS context; 4,532 (0.1338) also carry a pick
verb; 1,778 also name a panel; **576 (0.0170) are CHECKABLE** — they name a panel AND a ladder
rung this tree can rebuild. Those resolve to **62 DISTINCT (panel, ladder, rung) picks over
1,992 unit-mentions**; the distinct triple is priced and the mention count is reported, not
weighted on (1194's duplicate warning). **50 of the 62 sit OFF the anchor rung.**

## 2. The price — all 15 cells

| pick set | rule | picks | move rate | mean OOS Sharpe | DELTA | SE | t |
|---|---|---|---|---|---|---|---|
| P_1214 | S_NONE | 42 | 0.0000 | 0.9677 | +0.0000 | — | — |
| P_1214 | S_ALL | 42 | 1.0000 | 1.0362 | **+0.0685** | 0.0514 | +1.33 |
| P_1214 | S_SE1 | 42 | 0.9762 | 1.0386 | +0.0709 | 0.0514 | +1.38 |
| P_1214 | S_SE2 | 42 | 1.0000 | 1.0362 | +0.0685 | 0.0514 | +1.33 |
| P_1214 | S_ANC95 | 42 | 1.0000 | 1.0362 | +0.0685 | 0.0514 | +1.33 |
| P_AXIS | S_NONE | 168 | 0.0000 | 1.0151 | +0.0000 | — | — |
| P_AXIS | S_ALL | 168 | 0.5833 | 1.0362 | **+0.0211** | 0.0283 | +0.75 |
| P_AXIS | S_SE1 | 168 | 0.5357 | 1.0436 | +0.0285 | 0.0273 | +1.04 |
| P_AXIS | S_SE2 | 168 | 0.5833 | 1.0362 | +0.0211 | 0.0283 | +0.75 |
| P_AXIS | S_ANC95 | 168 | 0.5595 | 1.0322 | +0.0171 | 0.0276 | +0.62 |
| P_TEXT | S_NONE | 620 | 0.0000 | 1.0158 | +0.0000 | — | — |
| P_TEXT | S_ALL | 620 | 0.8065 | 1.0361 | **+0.0204** | 0.0105 | +1.94 |
| P_TEXT | S_SE1 | 620 | 0.8065 | 1.0361 | +0.0204 | 0.0105 | +1.94 |
| P_TEXT | S_SE2 | 620 | 0.8065 | 1.0361 | +0.0204 | 0.0105 | +1.94 |
| P_TEXT | S_ANC95 | 620 | 0.8065 | 1.0361 | +0.0204 | 0.0105 | +1.94 |

Gate G11 replays 1214's committed leg to **4.38e-05**: CH_RAW 0.9677, CH_ANCHOR 1.0362,
delta +0.0685, SE 0.0514, t +1.33. Off-anchor picks only: P_AXIS +0.0362 (t +0.73),
P_TEXT +0.0253 (t +1.94).

**1214's +0.0685 is the TAIL, not the level.** Its chooser lands on whichever ladder is
raw-widest, and that ladder is the one whose argmax travels furthest from the anchor. Pooled
over every axis the same substitution is worth **+0.0211 (t +0.75)**, less than a third of it.
Nothing was wrong with 1214's number; it is a statement about ONE chooser, and the queue was
right that it does not price the record.

## 3. The word "unresolvable" does no work

S_SE1, S_SE2 and S_ANC95 are decision-identical to S_ALL at **0 of 620 differing P_TEXT
cells** — not one of the record's 62 committed picks beats its own ladder's runner-up by 1 SE,
or beats the anchor at 95%, on the IS window it was chosen on. On the rebuilt grid the bars
move 8 of 168 (S_SE1) and 4 of 168 (S_ANC95) cells. **"Replace every UNRESOLVABLE dial call
with the anchor" and "replace every dial call with the anchor" are the same operation on this
record**, and the honest bar is again the anchor (1206/1209/1211/1214/1221/1226/1227/1230/1231,
now an eighth time, and for the first time on the record's OWN committed picks rather than one
run's grid).

## 4. Where the delta comes from (S_ALL; `.bycut.csv`)

| cut | value | picks | DELTA | SE | t |
|---|---|---|---|---|---|
| P_AXIS ladder | **N** | 42 | **+0.1067** | 0.0348 | **+3.07** |
| P_AXIS ladder | CADENCE | 42 | +0.0361 | 0.0302 | +1.20 |
| P_AXIS ladder | GROSS | 42 | +0.0010 | 0.0004 | +2.45 |
| P_AXIS ladder | H | 42 | **−0.0594** | 0.0743 | −0.80 |
| P_AXIS panel | B136 / U56 / SMALL | 56 each | +0.0639 / +0.0330 / −0.0336 | 0.0367 / 0.0355 / 0.0704 | +1.74 / +0.93 / −0.48 |

**The tuning cost is an N-ladder fact.** Anchoring N is worth +0.1067 at t +3.07; anchoring H
runs the other way at −0.0594; GROSS's +0.0010 is the degenerate gross ladder again (1189/1214
— a t of +2.45 on a tenth of a basis point of Sharpe, which is why the record should never read
GROSS t-statistics as economic). The pooled headline is a small positive left after those
cancel, and the cancellation is the finding: **the record does not have one tuning cost, it has
one expensive axis and one that pays.**

## 5. Rule 8 and both KEEP paths — nothing promoted

Every rung chosen on warm-up..2016-12-31 ONLY; 2017-2026 read once. 60 rule-8 rows
(`.walkforward.csv`), 45 stitched rolling curves, 66 rung books.

| panel | ladder | IS argmax | held (S_ALL) | full CAGR / Sharpe / MaxDD | halves | OOS CAGR / Sharpe / MaxDD | 4a | 4b | 4b OOS |
|---|---|---|---|---|---|---|---|---|---|
| U56 | N | 40 | 20 | 15.71% / 1.1480 / −19.13% | 1.2127/1.1050 | **17.16% / 1.1759 / −19.13%** | F | **T** | **T** |
| U56 | H | 252 | 126 | 15.71% / 1.1480 / −19.13% | 1.2127/1.1050 | **17.16% / 1.1759 / −19.13%** | F | **T** | **T** |
| U56 | N | 40 | 40 (S_NONE) | 13.40% / 1.1311 / −22.46% | — | 14.08% / 1.1150 / −22.46% | F | F | F |
| U56 | H | 252 | 252 (S_NONE) | 15.90% / 1.1630 / −21.84% | — | 17.33% / 1.1900 / −21.84% | F | F | F |
| B136 | all four | 5 / 63 / 0.75 / W | anchor (S_ALL) | 16.18% / 1.0715 / −20.74% | 1.2902/0.8995 | 16.29% / 1.0240 / −20.74% | F | F | F |
| B136 | N | 5 | 5 (S_NONE) | 18.73% / 0.9690 / −28.12% | 1.3074/0.7109 | 14.71% / 0.7546 / −28.12% | F | F | F |
| SMALL | all four | 40 / 252 / 0.75 / M | anchor (S_ALL) | 7.84% / 0.5055 / −35.81% | 0.6594/0.3942 | 7.09% / 0.4534 / −35.81% | F | F | F |
| SMALL | H | 252 | 252 (S_NONE) | 13.36% / 0.7845 / −37.41% | 0.9555/0.6419 | 11.16% / 0.6677 / −37.41% | F | F | F |

Benchmarks: U56 SPY 15.06% / 0.8815 / −33.72% (halves 0.9600/0.8171), OOS 15.15% / 0.8686;
U56 LIVE (RULES v2) 8.60% / 1.1982 / −12.05%, OOS 9.42% / 1.2717. B136 SPY 15.16% / 0.8862,
OOS 15.33% / 0.8769; B136 LIVE 7.98% / 1.0994, OOS 7.88% / 1.1061. SMALL SPY 14.06% / 0.8582,
OOS 15.33% / 0.8769; SMALL LIVE 4.64% / 0.7130, OOS 4.47% / 0.6518.

**BOTH KEEP PATHS.** Rule-8 rows: **4a 0 of 60**; 4b full 18, 4b OOS 18, BOTH 18 — 2 per
rule under S_NONE, **4 per rule under every substitution rule**, and all 18 collapse to **ONE
distinct book on 1211's realised-return key**: the frozen U56 anchor N=20 / H=126 / gross 0.75 /
weekly, the book the record committed on 2026-09-04 and confirmed on 2026-09-15. Stitched
curves: 4a 0 of 45, 4b both 14. Rung books: 4a 0 of 66, 4b full 17, 4b OOS 16, BOTH 15 over 12
distinct realised-return keys. **CONFIRMATORY, NOT GENERATIVE — NOT PROMOTED, NO MEMO, NO RULES
CHANGE.** The substitution's whole effect on the 4b count is to route the U56 N and H rows onto
the book the GROSS and CADENCE rows were already holding.

## 6. Survivorship (rule 9)

U56 (55 names) and B136 (135) are CURRENT constituents; SMALL is the sub-$2B screen, 664
investable of 715 after dropping every ticker with max_1d_move >= 1.0, and starts 2010. SPY is
excluded from every eligible set and used as benchmark only. The bias does not cancel out of
the OOS levels or the 4b legs, so any pass above is an upper bound.

## 7. Gates (14 of 14)

G1 fast runner == engine.backtest 2.78e-17 · G2 GROSS ladder is the anchor frame scaled 0.0 ·
G3 live RULES v2 U56 MaxDD −12.0549% == committed −12.05% · G4 the anchor rung of all four
ladders is ONE book bit for bit 0.0 · G5 block-sum bootstrap == direct Sharpe on the identity
tiling 4.44e-15 · G6 bootstrap deterministic across independent constructions 0.0 · G7 folds
tile all three panels with no overlap and no gap · G8 every harvested rung is a committed
ladder rung (0 bad) · G9 S_NONE delta == 0 at every cell · G10 a pick already AT the anchor has
delta 0 under every rule · G11 P_1214 x S_ALL replays 1214's committed CH_RAW / CH_ANCHOR /
delta / SE to 4.38e-05 · G12 stitched lengths == the sum of their folds.

## 8. What this leaves for the queue

The record's tuning cost is **small, positive and still not resolved**: +0.0204 of OOS Sharpe at
t +1.94 on its own committed picks, +0.0211 at t +0.75 on the rebuilt grid. It is ONE axis (N,
+0.1067 at t +3.07) net of one that pays the other way (H, −0.0594). Two sentences are worth a
future header: **(i) the resolution qualifier is inert — 0 of 620 committed picks resolve, so
any "replace the unresolvable ones" clause is just "replace them all"**; **(ii) a pooled tuning
cost is an average over axes that disagree in SIGN, so the record should price N and H
separately or not at all.** Three follow-ups filed, all price-only.
