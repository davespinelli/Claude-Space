# Idea 391 — back-fill the 153 UNATTRIB band rows (lane C, 2026-09-07)

**Verdict: INFRASTRUCTURE DELIVERED, and the filed premise needs one correction.**
Not a KEEP candidate: nothing new was proposed for capital, and leg [D] is a gated
reproduction of idea 387's matched grid (`max |d| 2.2e-16` over 42 statistics).

## What the record now says

Every band-speaking row of `research/LEADERBOARD.md` (294 today) carries a leading tag
naming the instrument it measured:

| tag | rows | meaning |
|---|---|---|
| `[MAB]` | 138 | 200d moving-average band WIDTH — the fractional collar half-width (`baseline.band_state`) |
| `[NT]` | 83 | no-trade / exit RANK buffer — integer rank slack (`sel_band` `m`, RANKX `x`, RANKE `e`) |
| `[INTERVAL]` | 46 | not an instrument at all: a null band, a weak-dominance band, an admissible gross band, a drawdown range |
| `[POOLED]` | 13 | the claim genuinely speaks of both instruments |
| `[UNRESOLVED]` | 14 | listed by name in the console log rather than guessed at |

The tagger is idempotent and byte-verified: removing one tag from each changed line
reproduces the original line exactly. `[SHARE]` (idea 103's per-name multiplier) is
reserved by the same taxonomy but no LEADERBOARD row resolved to it.

## The three findings

1. **The denominator was wrong.** 44 of idea 387's 284 band-speaking rows (15.5%), and
   34 of its 153 UNATTRIB rows (22.2%), use "band" for a STATISTICAL INTERVAL. The
   record's band lexicon has three senses, not two. Unreadable *instrument* prose is
   **119 of 240 (49.6%)**, not 153 of 284 (53.9%).
2. **90.8% of the unreadable rows are recoverable** (139 of 153) from the parent
   construction plus the row's own dial value — so the defect is a writing convention,
   not lost information. The irreducible residue is 14 rows, all with a parent that
   constructs no band at all.
3. **Pooling survives, and it is not harmless.** 10 of 284 rows still pool NT and MAB
   (13 of 294 in the current file); nine are census rows whose parent both mentions and
   constructs the two instruments, one is idea 384's own contrast row (legitimately
   plural). On the matched grid the two instruments move **MaxDD in opposite directions
   on 3 of 3 panels**, and on SMALL439 they disagree in sign on Sharpe and CAGR too —
   same sign in only 7 of 12 (panel x statistic) cells. A pooled band claim about
   drawdown is unsound wherever it is quoted, which is exactly the bar 4b turns on.

## Gates

`G_REPRO` reproduces idea 387's published 284/153/68/48/11/4 at its own commit (`019145c^`;
the publishing commit itself reads 291/157/70/48/12/4, its own rows included).
`G_CLS` 5/5. `G1/G2` 0.000e+00 on returns and turnover. `G3a` 0 disagreements, `G3b` 0 of
242,015 cells. `G4` 0.000e+00 vs idea 333/384's committed row. `G4b` 2.2e-16 vs idea 387's
committed `matched.csv`.

`G_BF` is the resolver's measured error rate, not an assertion: it abstains on 13 of the
116 rows idea 387's prose classifier attributed, and agrees on **92.2%** of the 103 where
it commits. All 8 committing disagreements were read by hand and **8 of 8 favour the
resolver** — `b=0.12` and `3% band` are MAB, not NT; `null band` / `Passing band` /
`band edge` / `clause-11b band` / a 20-draw band are intervals, not the MA collar. Idea
387's prose classifier therefore mis-attributes about 6.9% of what it did attribute, on
its loose `width` and `buffer` tokens.

## KEEP paths and rule 8 (the reproduction leg)

4a **0/27** at 0, 10 and 25 bps. 4b **14/27 @0, 9/27 @10, 5/27 @25**, every passer on U56
or B136 and every one a filed object; nothing proposed. Best 4b cell U56/MAB b=0.12
13.88% / 1.130 / -18.72% (halves 1.077/1.180, OOS 1.238) against SPY 15.23% / 0.889 /
-33.72% (0.957/0.834, OOS 0.882) and RULES v2 8.66% / 1.206. Rule 8: the IS chooser beats
its own anchor 5/6, SPY 4/6, RULES v2 **0/6**, mean regret +0.0071 — idea 387's number
reproduced. Both arms pick the grid edge on every panel (NT m=40, MAB b=0.12), which is
idea 240/256's flag and the open idea 390.

## Amendment proposed (extends idea 387's)

Idea 387 asked for `nt` / `mab` / `share` as reserved dial COLUMN names. Add the prose
half: a LEADERBOARD row that uses band language names its instrument in the idea cell —
`[NT]`, `[MAB]`, `[SHARE]`, `[INTERVAL]` or `[POOLED]` — and `INTERVAL` is a first-class
class, because one row in six that says "band" is talking about a confidence interval.

**Caveats.** The resolver reads text; its rule set was refined by reading G_BF's
disagreement list, so G_BF is an in-sample agreement rate, and the hand adjudication of
the 8 disagreements is mine. The protocol's two-parameter budget is spent in [D] on
(m, b). All three panels are current-constituent lists — survivorship — so the 4b CAGR
floor is tested in the books' favour.
