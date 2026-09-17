# Idea 1219 — should every committed t carry its SE BASIS and its L?

**VERDICT: KILL (capital) / ANSWERED = YES for the reporting clause, NO for the money.**
Reading the **emitting script** instead of the text raises the share of committed t's whose SE
basis is recoverable from **18 of 210 (0.086) to 86 of 210 (0.410)** — but only **4 of 210
(0.019)** sit in a script that pins a **unique L as well**, which is what "carries its basis and
its L" actually means. **27 of 210 committed t's (0.129), and 27 of the 126 that clear 1.96
(0.214), lie inside the band [1.6375, 2.5605] that the unstated dials span**, so their
significance verdict is a function of something nobody wrote down. And **using the honest bar
instead of 1.96 is worth +0.0010 of OOS Sharpe (t +0.71) across 20 (basis, L) cells** — the two
bars make **identical decisions at 13 of 20 cells**. The clause is worth writing down; it is not
worth anything in capital.

Script: `2026-09-17_should-every-committed-t-carry-its-SE-BASIS-and-its-L_B.py`
Artefacts: `.claims.csv` (1,258), `.census_grid.csv` (16), `.calibration.csv` (25),
`.verdicts.csv` (16), `.walkforward.csv` (216), `.decisions.csv` (984), `.rules.csv` (40),
`.randombar.csv` (40), `.gates.csv`, `.hypotheses.csv`, `.console.txt`.
**Gates 11 of 11 PASS**, including the fast runner against `engine.backtest` at 1.4e-17,
**1212's census reproducing at exactly 210 hits at its own commit 0743d51** and its fold count at
exactly 10, `S_BLOCK at L=1 == S_IID` to 1.3%, `S_FOLD` refusing to report with fewer than two
usable folds, and the null pairs verified exchangeable at mean ΔSharpe −0.0025 before anything
was read off them.

## THE TWO DIALS AND NO MORE (rule 4, and the queue names both)
`CLAIM SET` {C_1212, C_HEAD, C_MEMO, C_ALL} × `RECOVERY RULE` {R_TEXT200, R_TEXTWIDE, R_SCRIPT,
R_SCRIPT_STRICT} = **16 cells, every one published**. NOT dials: the SE basis ladder {S_IID,
S_BLOCK, S_FOLD} and the L ladder {21, 63, 126, 252, 504} are **1212's, inherited whole** (S_NW
added as a rung only so the census can classify a Newey–West script); PANEL {U56, B136, SMALL};
the 216-book rule-8 population; the count-matched random bar. Book frozen at 1212's construction,
10 bps, next-day execution, warm-up 260, IS ends 2016-12-31, anchor N 20 / H 126 / g 0.75 /
weekly, SEED_BASE 12191219.

## (A) THE CENSUS — ALL 16 CELLS (share of committed t's whose SE BASIS is recoverable)

| claim set | R_TEXT200 | R_TEXTWIDE | **R_SCRIPT** | R_SCRIPT_STRICT |
|---|---|---|---|---|
| C_1212 (n=210) | 18 / 0.086 | 30 / 0.143 | **86 / 0.410** | 4 / 0.019 |
| C_HEAD (n=210) | 18 / 0.086 | 30 / 0.143 | **86 / 0.410** | 4 / 0.019 |
| C_MEMO (n=358) | 30 / 0.084 | 50 / 0.140 | **109 / 0.304** | 5 / 0.014 |
| C_ALL (n=480) | 43 / 0.090 | 52 / 0.108 | **138 / 0.287** | 5 / 0.010 |

**All 210 of 1212's committed t's map to an emitting script and all 210 of those scripts are on
disk**, so the mapping is not the bottleneck. What R_SCRIPT recovers is **S_IID 82, S_BLOCK 4,
AMBIGUOUS 6, and NO NAMED BASIS AT ALL 118**. **Of those 210, 9 sit in a script that pins a
unique L and 201 in a script that declares none.**

**1212's text rule and the emitting scripts DISAGREE COMPLETELY, and the scripts win.** 1212
classified 10 of 210 as fold-clustered because "fold", "cluster" or "year" sits within 200
characters. **0 of those 10 have an emitting script containing any fold-SE machinery** (they are
NO_SE and S_IID), and **R_SCRIPT finds 0 fold-SE t's in the whole 210**. 1212's own limitation
note was right to distrust the rule; it was *more* wrong than it said, because the 10 it did
classify appear to be keyword collisions — chiefly on the word "year" — rather than a small
honest sample.

**NO_SE IS A FLOOR, NOT A PROOF, and is reported as one:** 53 distinct scripts carry a committed
t this rule cannot trace to any of the four constructions, and **47 of those 53 contain "SE",
"std(", ".sem(" or "np.sqrt(" somewhere**. R_SCRIPT's 0.410 is a **lower bound** on what a richer
recovery rule could reach and an upper bound on nothing.

## (B) THE HONEST BARS, RE-MEASURED RATHER THAN QUOTED
90 disjoint gross-matched null pairs (30 per panel), true Sharpe difference zero by construction,
mean ΔSharpe −0.0025, mean pair correlation 0.9037. Empirical 95th percentile of |t| — the honest
bar against the 1.96 the record writes:

| basis | L=21 | L=63 | L=126 | L=252 | L=504 | max/min |
|---|---|---|---|---|---|---|
| S_IID | 1.9820 | 1.9835 | 1.9759 | 1.9416 | 1.9319 | ×1.03 |
| S_BLOCK | 1.9530 | 1.9943 | 2.1074 | 2.1027 | 2.3266 | ×1.19 |
| S_FOLD | 1.6375 | 1.7690 | 1.9085 | 1.9127 | 2.5605 | **×1.56** |
| S_NW | 2.0161 | 2.0427 | 2.1229 | 2.1587 | 2.4754 | ×1.23 |

**1212's committed 15-cell table reproduces to a worst deviation of 0.1636** on independently
drawn seeds, and its central claim survives verbatim: **L, not the basis, is the dial** — S_FOLD
moves ×1.56 (1212 measured ×1.54) and S_BLOCK ×1.19 (1212: ×1.24). The **ambiguity band is
[1.6375, 2.5605]**; the NW rung calibrates inside it and widens it by nothing.

**DECLARED BYCATCH, REPORTED BECAUSE IT WAS MEASURED FIRST AND NOT REPAIRED QUIETLY.** A
Sharpe-scale HAC SE has a *denominator* that is itself an unstated dial. Dividing the HAC SE of
the mean daily difference by `sd(ra − rb)` — this run's first scaling — instead of the pooled
**book** volatility **under-rejects by about a factor of two: crit95 0.9219–1.2778 against a
nominal 1.96**, because two books correlated at 0.90 have a difference whose SD is far below
either book's. Published as `S_NW_DIFFSD` in `.calibration.csv`; it is not a rung and enters
nothing downstream.

## (C) HOW MANY COMMITTED CLAIMS ARE VERDICT-AMBIGUOUS
Of C_1212's 210 t's, **126 clear 1.96** and **27 (0.1286 of all, 0.2143 of the significant) lie
inside [1.64, 2.56]** — significant under some (basis, L) the record leaves open and not under
others. The same shares hold on the larger claim sets: C_MEMO 44 of 358 (0.2304 of its
significant), C_ALL 64 of 480 (0.2433). Re-read against the bar their own recovered cell implies,
**0 of the 86 R_SCRIPT-resolved t's are lost** — the resolvable ones are overwhelmingly S_IID,
whose honest bar is 1.93–1.98, i.e. *already* 1.96. **The exposure is entirely in the 124 that
cannot be resolved**, not in the ones that can.

## (D) RULE 8 AND BOTH KEEP PATHS — THE HONEST BAR BUYS NOTHING
216 books (3 panels × 9 N × 4 H × 2 cadences), chosen on 2009-2016, 2017-2026 read ONCE, every
one published. Benchmarks: **U56 SPY 15.06% / 0.8814 / −33.72%, OOS 15.15% / 0.8684 / −33.72%;
U56 RULES v2 (live) 8.60% / 1.1980 / −12.05%, OOS 9.42% / 1.2714. B136 SPY 15.16% / 0.8861 /
−33.72%, OOS 15.33% / 0.8767; B136 LIVE 7.98% / 1.0993 / −12.24%. SMALL SPY 14.06% / 0.8581 /
−33.72%; SMALL LIVE 4.30% / 0.6637 / −13.89%, OOS 3.75% / 0.5600.**

**4a 0 of 216. 4b full 12, 4b OOS 13, BOTH 12 — over 12 distinct books, U56 11 and B136 1, SMALL
0.** Best is **U56 / W / N=12 / H=126: full 17.65% / 1.1658 / −20.17% (halves 1.2741 / 1.0833),
OOS 18.78% / 1.1701 / −20.17%** — the same book 1183 and 1212 already committed.
**CONFIRMATORY, NOT GENERATIVE. NO NEW CANDIDATE, NOTHING ENACTED.**

Each (basis, L) is a publish rule over the 9-rung N ladder in each of 24 (panel, H, cadence)
contexts: move to the largest-|t| rung only if that t clears the bar. **BAR_QUOTED = 1.96;
BAR_HONEST = this run's own crit95.** 960 decisions, every one published.

- **HONEST minus QUOTED over the 20 (basis, L) cells: +0.0010 of mean OOS Sharpe, SE 0.0014,
  t +0.71; moves −0.10; 4b (full+OOS) +0.00.** The two bars make **identical decisions at 13 of
  20 cells** — for S_IID at all five L, because its honest bar *is* 1.96 to two decimals.
  **H_WF REFUTED.**
- **Doing nothing beats almost everything again.** The anchor rung at all 24 contexts returns
  mean OOS Sharpe **0.8575**; 10 of 40 rules beat it, the best being S_FOLD / L504 / BAR_HONEST
  at 0.8660 (16 → 14 moves).
- **And the 5 that clear their own count-matched random bar are what chance predicts.** 40 rules
  at a 0.90 bar clear it **4.0 times by chance**; observed **5**. Nothing in this family separates
  itself from its own move count. This is 1210's and 1221's finding arriving a third time.

## WHAT THIS IS WORTH
A reporting clause and a correction, not a book. **The correction:** 1212's "10 of 210 committed
t's are fold-clustered" should be read as **0** — no committed t in this record traces to fold-SE
machinery, and the 10 were keyword collisions. **The clause:** a committed t is uninterpretable
without its SE basis *and* its L, because the two together move the honest bar from 1.64 to 2.56,
and the record supplies both for **4 of 210** of its own t's. Quoting them is free. What is *not*
worth doing is acting on the difference: the honest bar and 1.96 pick the same book 13 times in
20, and neither picks a better one than doing nothing.

## SURVIVORSHIP (rule 9)
U56 and B136 are CURRENT-CONSTITUENT lists; SMALL is the current output of a sub-$2B screen
(`data/SMALL_PANEL_README.md`) less the documented `max_1d_move >= 1.0` exclusion — 52 of 715
dropped, 663 investable names plus SPY as benchmark only. Arms A and C are scans of committed
text and source and carry no market bias at all; Arm B is one construction measured against
itself and the bias very largely cancels out of a critical-value ratio. It does **not** cancel out
of Arm D's OOS levels or the 4b legs, so the 12 passes are an upper bound.

## FOLLOW-UPS FILED
1225 (the record's t's are S_IID at 82 of 86 resolvable — is a paired IID bootstrap SE the right
basis for a difference between two books correlated at 0.90?), 1226 (a Sharpe-scale HAC SE's
DENOMINATOR moves its honest bar by ×2 — census every committed SE for whether it states what it
divided by), 1227 (three runs now find the count-matched random bar decisive — should PROTOCOL
require one beside every chooser claim?).
