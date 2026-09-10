# Idea 426 — put-the-T1-line-in-PROTOCOL-and-back-fill-it (lane B, 2026-09-10)

**ANSWERED, no KEEP. The clause is drafted and the back-fill column is published — and the
back-fill's own harvest produces the counterexample that decides how the clause must be worded:
the key rule 8 picks in every cell of this run is FORWARD-DATED and T1-PASS.**

Script `2026-09-10_put-the-T1-line-in-PROTOCOL-and-back-fill-it_B.py`.
Outputs `.console.txt .keys.csv .backfill.csv .coverage.csv .census.csv .book.csv .walkforward.csv`.
Deterministic: two independent processes produce byte-identical `.backfill.csv` and
`.walkforward.csv`.

## Gates

| gate | result |
|---|---|
| idea 428's detector imported verbatim | 307 lines, sha256[:16] **8dbb98aa47fd80cb** = 433's published value |
| idea 433's 20-key instrument table | reproduced **EXACTLY on all five counts** (DET clears 12/20, false clearances PXDIFF/LOGPX/PXRANK/DVRANK, false rejection REBASED; CERT-VALUE@1step 0/0; CERT-RANK@1step false-clears MKTLVL) |
| `fast_bt` == `engine.backtest` | 6.939e-18 at 0 and at 10 bps |

## (A) The clause — drafted, report-only

PROTOCOL.md is **not** edited (rule 6, Sunday review). Full text in `.console.txt` PART 5. It
names the ordered pair idea 433 recommended, and adds two things 433 did not have:

* **(b) reproducibility first.** The certificate presupposes the key is a *function* of the panel.
  Two harvested expressions in this record inline an `np.empty_like` allocation filled by a later
  loop, so they read uninitialised memory. Un-gated they moved the published PASS/FAIL split
  **74/39 → 72/41 between two runs of a seeded certificate**. They are now rejected as
  `NOT_REPRODUCIBLE`, at source — a double evaluation agrees by luck within one process, because
  the same freed buffer is handed back.
* **(c) necessary, not sufficient.** See the counterexample below.

## (B) The back-fill column — the deliverable

Harvest: 601 committed `.py`, **142,028 assignment sites**, of which **30,092 are key-bearing**.
Inlining single-assignment locals and defaulted parameters (depth ≤ 7) reconstructs **5,845
(19.4%)**; the other **80.6% is the free-variable wall** and needs a hand-written harness. That
collapses to **485 distinct normalised expressions**, admitted as:

| class | n |
|---|---|
| **KEY (certified)** | **111** |
| UNREACHABLE (raises) | 254 |
| NOT_PANEL | 72 |
| NOT_PRICE_BORNE | 45 |
| NOT_REPRODUCIBLE | 2 |
| NOT_NUMERIC | 1 |

**T1 PASS 72 / FAIL 39 over 111.** Eighteen of the 39 failures are *identity* re-expressions of
the panel (`px.copy()`, `.ffill()`, `drop(columns=['SPY'])`, a slice) — arithmetically degree 1 and
correctly failed, but panel handles, not keys. Split out, the real back-fill is **93 keys: 72 PASS,
21 FAIL**. Biggest failure by reach: `px.rolling(200).mean()`, **72 scripts**. CERT cost 86 ms/key.

**DET/CERT disagree on 13 of 111 of the record's own keys**, every one a DET false clearance
(`px.diff()` and its Wilder/RSI descendants, `pd.DataFrame(px)`, `drop(columns=['SPY'])`,
`(px*vol).rank(...)`) — the same failure modes 433 found on synthetic keys, now on real ones.

Census: 39 T1-FAIL expressions are carried by **111 committed scripts**, touching **1,157 of 4,518
LEADERBOARD rows (25.6%)**. This is a count of **sites, not of verdicts**: a 200d mean is a degree-1
object sitting inside a degree-0 ratio in nearly all of them, which is exactly why clause 10(b)
adjudicates *the key as the book uses it* and not every sub-expression.

## (C) The price of the clause — book, PROTOCOL 2/3/4/8

Two tuned parameters, KEY × m; 2 panels × 2 books × 16 keys × 7 tilts × 4 rungs = **420 rows at
each rung, all in `.book.csv`**. Gross is held equal across every tilt by construction: mean
realised gross over the whole 10-bps grid runs **0.7499 to 0.7504** (spread **4.45e-04**, all of it
intra-week drift between rebalances), so m moves the cross-section and never the exposure.

| rung | 4a | 4b | 4b deduped (m=0 counted once) |
|---|---|---|---|
| 0 bps | 0/420 | 68/420 | 55/364 |
| 5 bps | 0/420 | 57/420 | 44/364 |
| **10 bps** | **0/420** | **48/420** | **35/364** |
| 25 bps | 0/420 | 12/420 | 12/364 |

**4a is 0/420 at every rung.** The 4b passes are the *underlying book* clearing, not the key: the
shared m=0 control passes 4b on its own in the U56/MA200 cell (11.51% / 1.088 / −18.65%, halves
1.171/1.027), and it loses to RULES v2 OOS (1.106 vs **1.279**).

## Rule 8 — the counterexample, and the finding

(KEY, m) chosen on 2010–2016 IS Sharpe, 2017–2026 read once.

| chooser | picks | mean ΔOOS Sharpe vs m=0 | beats SPY | beats RULES v2 |
|---|---|---|---|---|
| S_ALL (no gate) | K10 / +1.00 in **4/4** | **+0.5431** | 4/4 | 4/4 |
| S_T1 (T1-PASS only) | K10 / +1.00 in **4/4** | **+0.5431** | 4/4 | 4/4 |
| S_T1F (T1-PASS + not forward-dated) | mixed | +0.0923 | 2/4 | 2/4 |
| S_FAIL (T1-FAIL only) | K02/K08 / −1.00 | +0.2139 | 3/4 | 2/4 |

**K10 is `px.iloc[-1] / px - 1.0` — the terminal-dated key — and it is T1-PASS.** It is homogeneous
of degree 0 in the price scale, so the certificate clears it; it is dated at T, so rule 8's date
split cannot see it. Best cell U56/MA200 at 10 bps: **OOS 21.58% / 1.527 / −22.25%** against SPY
15.32%/0.876/−33.72%, RULES v2 9.48%/1.279/−12.05%, the m=0 control 12.35%/1.106/−18.65%. It is
pure look-ahead and it wins everything.

* **Price of the T1 gate in front of rule 8: exactly +0.0000 over 4 cells** — identical pick in all
  four. T1 alone buys nothing here, because the leak it is aimed at is not the leak that is paying.
* With 10(c) enforced the pick moves and **costs −0.4508** OOS Sharpe — i.e. the dating exclusion,
  not T1, is what removes the winner, and what it removes is the fake return.
* **Rule 8 passed over 10 arms** that pass 4b at 10 bps, are T1-PASS, are not forward-dated, and
  beat their own m=0 control OOS (U56/MA200 K00,K01,K03,K04,K06,K07,K15; U56/EWALL K07). Its
  IS-Sharpe chooser preferred the oracle in every cell. That is the cost of running T1 — or
  nothing — *after* rule 8 instead of before it, and it is idea 195's finding reproduced through
  the back-fill's own harvest rather than by hand.
* No rule-8 pick passes 4b: every one fails the drawdown leg (the U56/MA200 m=0 control is the
  single exception and it loses 4a).

## Pre-registered predictions

| | prediction | result |
|---|---|---|
| P1 | back-fill reaches <40% of key-bearing sites | **HIT** — 19.4% |
| P2 | a T1-FAIL key carried by ≥5 scripts | **HIT** — max 72 |
| P3 | a key PASSES T1 and is still look-ahead | **HIT** — 8 found |
| P4 | T1 gate does not improve OOS **and** no tilt arm clears 4b | **MISS** — gate +0.0000 (hit), but 34 tilt arms clear 4b at 10 bps (miss); both readings reported |

## Verdict

**ANSWERED / no KEEP.** 4a 0/420, 4b 48/420 at the protocol rung and every 4b pass is the control
book, not the key. The deliverable is the clause plus the 111-row PASS/FAIL column. Two amendments
the queue's draft did not anticipate: the **rank** certificate it names must be the **value** one
(433), and a **reproducibility gate** must come first or the column is not stable run to run.
The clause is worth adopting as a *necessary* condition and is **not** worth quoting as protection:
on this record's own keys it removes 21 keys and changes rule 8's pick in 0 of 4 cells.

**SURVIVORSHIP:** U56 and SMALL439 are both current constituents, SMALL doubly so. No book is
proposed on either.

RULES.md, PROTOCOL.md, scan.py, bot.py, baseline.py untouched.

## Follow-ups filed

* the free-variable wall is 80.6% of key-bearing sites — a back-fill that matters needs the
  record's scripts to expose their keys as `fn(px)`, which is a convention change, not an idea;
* the forward-dating clause (T2) is the one that would have caught the winner here, and nothing in
  PROTOCOL states it.
