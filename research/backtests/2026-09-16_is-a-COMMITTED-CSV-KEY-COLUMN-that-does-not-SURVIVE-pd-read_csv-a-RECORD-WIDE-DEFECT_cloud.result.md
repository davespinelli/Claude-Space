# 1105 — is a COMMITTED CSV KEY COLUMN that does not SURVIVE pd.read_csv a RECORD-WIDE DEFECT?

**ANSWERED = NO as a SEED defect, YES as a TEXT defect, and the two must not be confused.
CONFIRM of 1097's incident and of its mechanism; KILL of "record-wide" as a description of the
seed exposure; CORRECTION to the implied scope — the far bigger round-trip failure is in the
record's MEASUREMENT columns, where nothing is keyed and nothing is at risk.** No RULES change,
no book promoted, no PROTOCOL edit (rule 6). RULES.md, PROTOCOL.md, scan.py, bot.py,
baseline.py untouched.

**THE TWO DIALS AND NO MORE (rule 4).** `COLUMN CLASS` {SEED_KEY, ANY_KEY} x `ROUND-TRIP TEST`
{LITERAL, SEMANTIC}. All 4 grid points published. SEED_KEY = a column whose name is a token in
one of the record's own **44 committed `mdseed(...)` call sites**, restricted to tokens of >= 3
characters — the short ones (`s`, `t`, `k`, `n`, `p`, `c`, `f`, `r`, `l`) are loop variables,
and leaving them in matched t-stats, p-values and counts, inflating the class with columns no
reader ever keys on. That restriction is part of the D1 definition, declared before the answer.
LITERAL = `str(pd.read_csv(f)[col])` differs from the committed text; SEMANTIC = the raw ->
re-read map is not injective, so the damage cannot be undone by any format rule. Panels, the
`n` ladder and 1071's cap ladder are COORDINATE SETS, not dials.

**THE CENSUS. 5,302 committed CSVs, 87,836 columns (this run's own outputs self-excluded).**

| class | test | cols | fail | share | files | file share |
|---|---|---|---|---|---|---|
| SEED_KEY | LITERAL | 3,541 | 98 | 2.77% | 97 | 1.83% |
| SEED_KEY | SEMANTIC | 3,541 | 60 | 1.69% | 59 | 1.11% |
| ANY_KEY | LITERAL | 87,836 | 45,644 | **51.97%** | 4,701 | **88.66%** |
| ANY_KEY | SEMANTIC | 87,836 | 7,281 | 8.29% | 1,777 | 33.52% |

**H_WIDE FAILS at 1.83% of files against its 5% bar, and H_SEED FAILS by a factor of 19** —
seed-key columns round-trip *better* than columns at large, not worse. **1097's incident is
real and reproduced, but it is not a record-wide seed defect.**

**THE MODE BREAKDOWN IS THE PART WORTH KEEPING.** Of the 98 SEED_KEY literal failures:
**KEY 22 columns / 22,357 cells** (1071's kind — a literal whose FORMAT carries the key),
**EMPTY_NAN 42 / 40,599** (a committed `''` returning as the string `'nan'`), **FLOAT_REPR 34 /
6,195** (17-significant-digit text vs pandas' 16-digit repr). Across ALL columns the ordering
inverts completely: **FLOAT_REPR 39,430 columns / 18.2M cells** and **EMPTY_NAN 6,137 / 2.88M**
against **KEY 99 / 76,467**. The record's CSVs are massively lossy in their *printed digits* —
`CAGR` alone fails in 1,206 files and 1.39M cells — and that is harmless, because nobody hashes
a CAGR. **The defect is not "CSV columns do not round-trip". It is "a key must never be
recovered from a float-inferred column", and only about 100 columns in the record are keys.**

**H_CAPONLY FAILS, and that is the finding with teeth.** `cap` is not alone. Ten seed-key column
names fail LITERAL — `cap`, `kind`, `panel`, `gate`, `seed`, `null`, `elig`, `native`, `u56`,
`U56` — and **`kind` (23 files, 38,656 cells, SEMANTICALLY lossy in 23 of 23) and `panel` (26
files, 23,532 cells, lossy in 25 of 26) are worse than `cap` (24 files, 5,880 cells, lossy in 1
of 24)**. `seed` itself fails in 4 files, all four semantically. **60 SEED_KEY columns are
semantically lossy: for those, no re-reading convention recovers the committed key at all.**

**THE PRICE. 24 cells (2 panels x n {5,10,20} x 1071's caps {INF, 2.00, 1.50, 1.00}), all
published.** Every one of the four committed cap literals fails to survive — pandas returns
`inf`, `2.0`, `1.5`, `1.0`, and all four give a different md5 seed, shown from pandas itself
rather than asserted. Re-seeding the null families from the re-read literal moves the committed
EDGE by **median 0.4013 pp, max 2.0898 pp**, against a median seed SE of 0.3221 pp. **0 of 24
cells reproduce the committed EDGE exactly; only 8 of 24 (33.3%) land inside one seed SE.**
That is 1097's "8 of 40" reproduced on an independent grid and an independent construction.

**GATES 11 of 11 PASS, printed before any result number.** Fast runner NET returns and turnover
== `engine.backtest` post-warm-up at 1.39e-17 / 3.75e-16; the cap binds (G2b 0.0375 = 1.00 x
0.75/20) and de-grosses (G2c -1.11e-16); the defect reproduced from pandas (G3, G3b).
**G6 is the control the priced grid could not supply** — because all four committed literals
fail, there is no naturally-surviving cell, so the same key drawn twice is shown to give a
**bit-identical** null family (0.0) while `'INF'` vs `'inf'` gives a different one (9.95e-03).
Only with G6 passing is a non-zero delta attributable to the key rather than to the machinery.

**RULE 8 AND BOTH KEEP PATHS — nothing proposed.** IS 2009-2016 chooses, OOS 2017-2026 read
once. **4a 0 of 24, 4b full 0 of 24, 4b OOS 7 of 24.** Binding leg `L_CAGR` **0 of 24**: the
capped composite tops out at 10.41% full-sample CAGR against the 10.57% floor (70% of SPY's
15.10%) — it misses by 0.16 pp, well inside idea 1083's measured 4.1-7.2 pp resolution for
exactly that quantity, so the miss is not resolvable either. `L_DD` 24/24, `L_H1` 20/24,
`L_OOS` 19/24, `L_H2` 7/24. Of the four declared choosers only `C_CAGR` on U56 (N=20, cap=INF
-> OOS 11.16% / 1.0145 / -16.74%) clears 4b out-of-sample, and it fails the same CAGR leg
full-sample, so it is **not a candidate**. SPY U56 full 15.10% / 0.8829 / -33.72%, OOS 15.21% /
0.8711 / -33.72%; B136 full 15.16% / 0.8861 / -33.72%, OOS 15.33% / 0.8767 / -33.72%. Live
RULES v2 8.62% / 1.2007 / -12.05%.

**SURVIVORSHIP (rule 9).** U56 and B136 are CURRENT-CONSTITUENT panels: every CAGR/Sharpe level
is optimistic and the 4a/4b counts are UPPER bounds. The RAW-vs-REREAD contrasts are within-tape
and the bias very largely cancels out of them.

**WHAT SHOULD CHANGE (not a RULES edit).** Idea 979's `unit`/`cell_key` proposal is the wrong
shape for this: the problem is not that columns lack a declared unit, it is that ~100 columns
are KEYS and are being recovered from a float-inferred read. The one-line fix is at the read,
not at the write — **any script re-reading a committed CSV for a key must pass
`dtype=str, keep_default_na=False`**, which makes all three modes (KEY, EMPTY_NAN, FLOAT_REPR)
vanish at once. The 60 semantically-lossy seed-key columns are past saving and should be
re-derived from their scripts, never from their CSVs.

Script `research/backtests/2026-09-16_is-a-COMMITTED-CSV-KEY-COLUMN-that-does-not-SURVIVE-pd-read_csv-a-RECORD-WIDE-DEFECT_cloud.py`;
5 CSVs (census 87,836 rows, grid 4, reprice 24, hypotheses 5, walkforward 24) + console log.
**HYPOTHESES 2 of 5** — H_SEMANTIC and H_PRICE pass; H_WIDE, H_SEED and H_CAPONLY fail, and
those three failures are the answer.
