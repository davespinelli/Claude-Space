# Idea 189 — does-any-fitted-dial-beat-its-own-modal-pick (cloud, 2026-09-05)

**SPLIT. The queue's literal test does NOT fire — the modal constant beats the fit on 3 of 5
dials on idea 171's corpus, not 5 of 5 — but the decision it was meant to settle comes out
cleanly anyway: "read the mode once and write it down" is WEAKLY DOMINANT (its worst case
anywhere in the grid is −0.0001 OOS Sharpe) and STRICTLY better on both dials where the
selector is actually choosing. No RULES change, no new book, no KEEP candidate.**

Script `2026-09-05_does-any-fitted-dial-beat-its-own-modal-pick_cloud.py`; artefacts
`.console.txt`, `.ladder.csv`, `.modes.csv`, `.paired.csv`, `.walkforward.csv`. 315 s.

## Corpus and reproduction

Idea 171's script imported verbatim (`Book`, `build_corpus`, `fast_backtest`, `rel_margin`,
`keep_4a`, `keep_4b`, the five dials and their ladders). **Corpus A** = idea 171's 53 books;
**corpus B** = 115 books on idea 175's panel definitions rebuilt under idea 171's `Book`
class. 5 dials × 36 ladder points × 168 books = **6048 ladder rows**, 10 bps, t+1,
IS ≤ 2016-12-31, OOS ≥ 2017-01-01 read once.

Asserted before any new number: `fast_backtest` == `engine.backtest` at D/W/M/Q
(max |dret| 6.2e-17), CAND-20 weights == idea 78's `weights_cand` at **0.000e+00** on three
books, and **the rebuilt corpus-A ladder matches idea 171's committed `ladder.csv` on all
1908 rows at 2.2e-16 with 0 4a/4b verdict mismatches.** Its published headline re-derives
exactly: CADENCE **+0.0642 (t +4.54)**, SLEEVE **+0.1801 (t +37.73)**, GROSS −0.0006
(t −4.24), N −0.0215, BAND +0.0085; and its 4b count, 250 of 1908, reproduces.

## Q2 — three of the five "dials" were never choices

| dial | corpus A mode | share | corpus B mode | share | incumbent | same? |
|---|---|---|---|---|---|---|
| GROSS | **1.00** (ladder end) | 94.3% | **1.00** | 84.3% | 0.75 | different |
| N | 20 | **22.6%** | 15 | **23.5%** | 20 | A same, B different |
| BAND | **0.08** (ladder end) | 81.1% | **0.08** | 68.7% | 0.00 | different |
| CADENCE | M | 83.0% | M | 88.7% | W | different |
| SLEEVE | **0.30** (ladder end) | 100.0% | **0.30** | 87.8% | 0.00 | different |

On GROSS, BAND and SLEEVE the IS argmax lands on the **ladder endpoint** in 69–100% of books.
Idea 171 flagged this for SLEEVE (53/53, byte-identical to its ORACLE); it is the same
phenomenon on GROSS (50/53, 97/115) and BAND (43/53, 79/115). On those three dials the "fit"
is a constant wearing a selector's name, its modal arm agrees with it in 69–100% of books, and
the paired difference is bounded by 0.0001 of OOS Sharpe. **They are evidence about the
ladders, not about fitting.** On 4 of 5 dials the selector's own mode is NOT the incumbent
constant, which is idea 183's anchor-position caveat measured directly.

## Q3 — the answer (MODE-LOO minus SEL-SHARPE; positive = the constant wins)

| dial | A, OOS Sharpe | B, OOS Sharpe | A, OOS margin | B, OOS margin | agreement A / B |
|---|---|---|---|---|---|
| GROSS | −0.0001 | −0.0000 | −0.0055 | +0.0061 | 94.3% / 84.3% |
| **N** | **+0.0215** | **+0.0256** | +0.0112 | **+0.0865** | 22.6% / 23.5% |
| BAND | +0.0005 | +0.0078 | +0.0029 | +0.0195 | 81.1% / 68.7% |
| **CADENCE** | **+0.0261** | **+0.0255** | **+0.0343** | +0.0143 | 83.0% / 88.7% |
| SLEEVE | +0.0000 | +0.0030 | +0.0000 | +0.0025 | 100.0% / 87.8% |
| **dials won** | **3/5** | **4/5** | **3/5** | **5/5** | |

MODE-GLOBAL and MODE-XCORPUS give the same counts to within one dial (A: 3/5, 3/5, 2/5, 3/5;
B: 4/5, 5/5, 4/5, 5/5) — the full 3 × 2 × 2 × 5 grid is in `.paired.csv` and the console.

Read as a decision rather than a scoreboard:

* **Fitting's best case anywhere in the grid is +0.0089 OOS Sharpe** (N, corpus A, against the
  cross-corpus mode) and, under the headline MODE-LOO variant, **+0.0001 OOS Sharpe** and
  +0.0055 OOS margin — both on GROSS, the flattest ladder in the set (its whole OOS Sharpe
  spread is 0.002).
* **The constant's best case is +0.0256 OOS Sharpe / +0.0865 OOS margin.**
* On the two dials where the pick distribution is genuinely spread — N (modal share 23%) and
  CADENCE — **the constant wins in 4 of 4 corpus × dial cells**, on both scores in 3 of those 4.

So the queue's "if the constant wins on all five" fails on a technicality: on three dials there
is nothing to win, because the selector already is the constant.

## Q4 — the mechanism: off-modal picks are catastrophic, and it generalises

MODE-LOO minus SEL-SHARPE restricted to the books where the selector leaves its own mode:

| corpus | dial | agree | off-mode n | off-mode mean d | overall | worst single book |
|---|---|---|---|---|---|---|
| A | GROSS | 94.3% | 3 | −0.0010 | −0.0001 | U56 0.8→1.0 +0.0002 |
| A | N | 22.6% | 41 | **+0.0278** | +0.0215 | B136k40d06 10→20 **+0.3176** |
| A | BAND | 81.1% | 10 | +0.0027 | +0.0005 | B136k20d10 0.02→0.08 +0.0590 |
| A | CADENCE | 83.0% | 9 | **+0.1536** | +0.0261 | B136k40d13 Q→M **+0.2761** |
| A | SLEEVE | 100.0% | 0 | — | +0.0000 | — |
| B | GROSS | 84.3% | 18 | −0.0002 | −0.0000 | U56k20d09 0.5→1.0 +0.0022 |
| B | N | 23.5% | 88 | **+0.0334** | +0.0256 | U56k20d15 3→15 **+0.4726** |
| B | BAND | 68.7% | 36 | +0.0249 | +0.0078 | SMALLk40d03 0.0→0.08 +0.1521 |
| B | CADENCE | 88.7% | 13 | **+0.2259** | +0.0255 | U56k20d15 Q→M **+0.4301** |
| B | SLEEVE | 87.8% | 14 | +0.0249 | +0.0030 | SMALLk20d05 0.25→0.3 +0.0631 |

Idea 175's mechanism replicates and is larger on the second corpus: when the CADENCE selector
leaves M it costs **0.15–0.23 of OOS Sharpe**, with single books at −0.28 and −0.43. GROSS is
the one dial where going off-mode is (very slightly) right, by 0.0002–0.0010 — three orders of
magnitude smaller than the CADENCE penalty. **The clause this supports is about tail picks, not
about fitting being uninformative.**

## Q5 — is the mode itself stable? (the mode's own walk-forward)

Each corpus split into two seeded halves; the mode read on one half, scored on the other.

**The mode reproduces across halves in 9 of 10 corpus × dial cells.** The exception is N on
corpus A (10 vs 20) — the dial with the flattest pick distribution — and there the held-out
mode **LOSES −0.0229**, where on corpus B, whose N mode is stable at 15 in both halves, it wins
+0.0256. That is the honest boundary condition: *the modal constant is only as good as the
mode's own concentration, and a dial whose modal share is ~23% on 53 books does not have a
readable mode.*

## Q6 — rule 8 and both KEEP paths

Mean OOS level per arm, pooled over the five dials (every pick made on ≤ 2016-12-31,
2017-2026 read once):

| corpus | arm | OOS Sharpe | OOS CAGR | OOS MaxDD | 4a | 4b |
|---|---|---|---|---|---|---|
| A | ORACLE (not implementable) | 1.0438 | 9.49% | −15.04% | 221 | 42 |
| A | **MODE-LOO / MODE-GLOBAL** | **1.0196** | 10.81% | −17.85% | 194 | 40 |
| A | MODE-XCORPUS | 1.0135 | 10.97% | −18.12% | 187 | 40 |
| A | SEL-SHARPE | 1.0100 | 10.90% | −18.18% | 179 | 40 |
| A | SEL-4B | 0.9806 | 10.57% | −18.16% | 211 | 62 |
| A | CONST-INC (idea 171's incumbent) | 0.9638 | 9.96% | −17.18% | 240 | 50 |
| A | RANDOM | 0.9634 | 9.63% | −16.80% | 210 | 39 |
| B | ORACLE | 0.7716 | 5.54% | −15.74% | 221 | 39 |
| B | **MODE-LOO / MODE-GLOBAL** | **0.7375** | 6.06% | −17.83% | 164 | 62 |
| B | MODE-XCORPUS | 0.7370 | 5.84% | −17.20% | 179 | 54 |
| B | SEL-SHARPE | 0.7251 | 5.80% | −18.14% | 179 | 54 |
| B | SEL-4B | 0.7044 | 5.95% | −18.35% | 131 | 82 |
| B | RANDOM | 0.6866 | 5.19% | −17.33% | 165 | 39 |
| B | CONST-INC | 0.6793 | 5.25% | −17.03% | 155 | 55 |

Benchmarks: **SPY OOS 15.45% / 0.8820 / −33.72%**; RULES v1 @10 bps 7.73% / 0.7471 / −13.83%
(u56), 5.94% / 0.5763 / −21.19% (B136), 7.88% / 0.6617 / −32.37% (small).

Measured as capture of the ORACLE's gap over the inherited constant: **the modal constant banks
69.8% (A) and 63.1% (B); the fit banks 57.8% and 49.6%.**

**This is NOT another do-nothing win, and the difference matters.** In eleven previous runs the
inherited constant beat the fit. Here the inherited constant is the worst or second-worst arm on
both corpora, because it sits at a poor ladder position on four of the five dials. What loses is
not "choosing" — it is *choosing per book*. Choosing once, across books, and writing the answer
down beats both.

Both KEEP paths over all 6048 ladder rows: **4a 2721, 4b 506** (corpus A's 250 reproduce idea
171 exactly). By parent: B136 1486/230 of 1800, U56 (A) 21/20 of 72, U56 (B) 1211/256 of 2376,
**SMALL 3/0 of 1800 — zero 4b passes on the small panel, the thirteenth reproduction of idea
136.** Per idea 144 a re-dialled book is the same book, so **nothing here is proposed**; the
passes are the known CAND-20 family on survivorship-exposed large-cap panels. The best
fixed-panel rows are U56 CADENCE=M (14.8% / 1.2081 / −19.58%, OOS 1.2866) and U56 SLEEVE=0.25
(10.9% / 1.2212 / −13.57%, OOS 1.2856) — both already in the record via ideas 101/134/175.

## Predictions

3 of 6 hit. **P1** (reproduction) HIT. **P2** (CADENCE: mode beats fit on corpus A) HIT at
+0.0261. **P4** (agreement > 50% on ≥ 3 dials) HIT at 4/5.
**P3 MISS**: 3 of 5 dials, not 5 — for the reason set out in Q2, that GROSS/BAND/SLEEVE are
endpoint-degenerate, which was visible in idea 171's SLEEVE finding and should have been
anticipated in the prediction.
**P5 MISS**: 3 of 5 — GROSS's off-mode difference is negative (−0.0010/−0.0002) and corpus A's
SLEEVE has no off-mode books at all, so the prediction could not have been satisfied there.
**P6 MISS, and this one is a defect in the prediction, not a finding**: it asserted no 4b passes,
which idea 171's own committed `keep.csv` already contradicted (250 of 1908, its own P7 miss)
before this run started. It should not have been written and its miss carries no information.

## Caveats carried

Current-constituent survivorship on B136, U56 and the small panel (idea 54): all arms inherit it
equally so the paired comparison is unaffected, and every level is biased upward and is not a
tradable estimate. The books within a corpus are **not independent** — 48 of corpus A's 53 and
112 of corpus B's 115 are sub-panels of a shared parent — so every paired t is over correlated
units and its nominal size is optimistic; the exact sign test is printed beside it and neither is
a p-value on a fresh sample. MODE-GLOBAL uses a book's own vote in the constant applied to it,
which is why MODE-LOO carries the headline and MODE-XCORPUS is reported beside it. Corpus B is
built on idea 175's panel definitions under idea 171's `Book` class with the sleeve assets
attached as price columns; attaching columns perturbs the composite's cross-sectional pct-ranks,
so corpus B's books are near-copies of idea 175's and **no number here is claimed to reproduce
idea 175** — the reproduction control is against idea 171 only. On k=20 sub-panels the N ladder
saturates (n ≥ 20 admits every eligible name), inherited from idea 171. Idea 144, idea 38's
calendar-day index and idea 126's t+1-only execution carry over.

## Follow-ups queued

217 (does the modal-constant result survive at 25 bps and on a cost ladder), 218 (extend the
GROSS/BAND/SLEEVE ladders past their endpoints so the three degenerate dials become real
choices), 219 (a modal-share floor: at what concentration does a mode become writable, given N
on corpus A fails at 22.6% and CADENCE succeeds at 83%).
