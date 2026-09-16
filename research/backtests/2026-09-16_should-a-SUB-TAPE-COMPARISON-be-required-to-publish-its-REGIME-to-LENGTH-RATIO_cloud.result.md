# Idea 1148 (cloud, 2026-09-16) — should a SUB-TAPE COMPARISON be required to publish its REGIME-to-LENGTH RATIO?

**ANSWER = YES, AND IT IS NEARLY FREE — BUT ONLY IF THE CLAUSE IS WORDED OVER CS_STRICT.**
The census is as stark as it can be: of **2,587,354 committed rows across 2,274 committed CSVs**
that make a sub-tape, split-half or tape-length comparison, **6 rows in 1 file publish a
regime-to-length ratio** — 1140's own `regime.csv`, the run that coined it. Share of rows
**0.000002**. The prose arm finds **1 of 337** committed sentences naming the ratio, and that one
sentence is the CHANGELOG line *filing this very idea*: **zero** committed prose claims publish
it. H_NOBODY SUPPORTED.

**THE PREMISE HOLDS ON A SECOND CONSTRUCTION, AND UNDER EVERY DEFINITION.** 1140 measured the
ratio on its own resolution ratio |gap|/SD. This run measures it on the **statistic VALUE** —
27 CORE-ladder books per panel at the standing anchor, three panels, six statistics, 1/1 + 1/2 +
1/3 = 6 sub-tapes (486 sub-tape readings, all dumped). Pooled regime/length at the headline
definition: **CAGR 8.73x, VOL 8.00x, SHARPE 4.39x, MAXDD 2.00x, ULCER 17.51x, CALMAR 8.40x** —
**6 of 6 above 1**, and 6 of 6 above 1 under all three definitions (R_SD min 2.69x, R_MATCHED min
1.74x). H_RATIO1 and H_DEFN SUPPORTED. The regime noise is not a 1140 artefact.

**THE CORRECTION THIS RUN ADDS.** `max − min` over k points grows with k, and 1140 pools a k=2
range (halves) with a k=3 range (thirds). The count-matched definition (mean range of a **random
pair** at every length) is smaller in **5 of 6** statistics, median **1.137x** — so 1140's
committed 1.7x-to-61x band is inflated by roughly **14%** and survives the correction in every
sign and in every verdict. The clause should nevertheless require the count-matched form, since
the inflation grows with the number of stretches a run happens to cut.

**THE ONLY SUB-1 CELL IN THE WHOLE TABLE** is SMALL / MAXDD under R_MATCHED (**0.79x**) — the one
place where the length effect exceeds the regime noise, and it is on the panel whose levels are
least trustworthy. Named, not swept.

**PRICING THE CLAUSE — IT COSTS A COLUMN, NOT A RE-RUN.** A committed file is *checkable* iff its
own tape-extent column takes ≥2 distinct values (a between-length move exists) and some value
repeats (a within-length spread exists). **485 of 569 CS_STRICT files (0.8524), carrying 573,668
of 593,172 rows (0.9671)**, already publish enough: the ratio can be computed from what is
committed. Only **3.29%** of CS_STRICT rows would need a re-run. H_CHECKABLE SUPPORTED.

**BUT THE WORDING IS THE WHOLE COST, AND MY OWN SCOPE ESTIMATE WAS WRONG.** H_SCOPE declared
CS_HALVES > 100x CS_STRICT and is **REFUTED**: 2,140,569 vs 593,172 rows = **3.6x**. The cost is
not in the multiple, it is in the *satisfiability*: a split-half row can price REGIME (two
stretches) but **never LENGTH** (a half is one length), so **0 of 2,140,569 CS_HALVES rows are
checkable from what they publish** and a clause worded over "sub-tape comparisons" would demand a
third tape from every one of them — **77.83% of CS_ALL rows needing a re-run against 3.29% of
CS_STRICT rows.** That is the finding a Sunday review needs.

**THE CLAUSE, DRAFTED (proposed, NOT enacted — rule 6).** *PROTOCOL rule 10: a published claim
whose value depends on the LENGTH or the STRETCH of tape it was computed on — a sub-tape, a
tape-length exponent, a window-length ladder — must state beside it its REGIME-to-LENGTH RATIO:
the median spread of the same quantity across DISJOINT stretches of EQUAL length, divided by its
move between the longest and the shortest length. A claim whose ratio exceeds 1 is an UPPER BOUND
ON PRECISION and may not be quoted as a measurement. The within spread must be COUNT-MATCHED (a
random pair at every length). Scope: claims indexed by tape extent (CS_STRICT). A split-half
claim is explicitly OUT of scope, because a half is one length and the clause is unsatisfiable
for it without a third tape.*

**RULE 8 AND BOTH KEEP PATHS — NOTHING PROPOSED AS A BOOK.** The 81 rung books are byte-identical
across both dials; only which committed rows get counted and how the ratio is defined changes.
Scored because rule 4 says so. Rung chosen on IS 2009-2016 alone, 3 choosers, OOS read ONCE:
**4 of 36 picks clear 4b full, 4 of 36 clear 4b OOS, 0 of 36 clear 4a.** Whole grid, 81 rungs:
4b full **16**, 4b OOS **17**, 4a **0** (U56 10/27, B136 6/27, **SMALL 0/27**), independently
reproducing 1110/1131's counts on the same construction. Every passing pick is the standing
anchor U56 / W / H=126 / N=20 / gross 0.75 — full **15.58% / 1.1397 / −19.13%**, halves 1.2037 /
1.0971, OOS **16.97% / 1.1643 / −19.13%** against SPY OOS 15.21% / 0.8711 / −33.72% and live
RULES v2 OOS 9.45% / 1.2762 / −12.05%. Binding leg among the 65 failures: L_DD sole at 26,
L_CAGR sole at 9.

**GATES 6 of 6.** G1 fast runner == `engine.backtest` 1.39e-17; G2 CROSS-RUN the committed U56
W/H126/N=20 triple 3.18e-07; G3 SPY OOS 1.70e-04; G4 live RULES v2 MaxDD == −12.05% 4.95e-05;
G5 determinism 0.00e+00; G6 1140's committed `regime.csv` present with all six statistics, its
numbers quoted verbatim from the file and never re-derived from memory.

**THE DECLARED APPROXIMATION.** The census reads COMMITTED artifacts only, so a ratio published
in a console log or a script comment is not counted — an omission that can only make H_NOBODY
EASIER to support. The CS_STRICT test is a HEADER-NAME test: a file indexing rows by tape extent
under an idiosyncratic name is missed, and a file whose `rows` column means something else is
over-counted. Both directions are live; all 148 accepted header names are dumped.

**SURVIVORSHIP (rule 9).** U56 and B136 are current-constituent lists; SMALL is the current
constituents of a sub-$2B screen (663 names after dropping 52 with `max_1d_move >= 1.0`, tape
2010-01-04 → 2026-09-11). A within-length spread and a between-length move contrast the same
books over stretches of the same inflated tape, so the bias very largely cancels out of the
ratio. It does not cancel out of the 4b legs, so the 16 passes are an UPPER bound.
