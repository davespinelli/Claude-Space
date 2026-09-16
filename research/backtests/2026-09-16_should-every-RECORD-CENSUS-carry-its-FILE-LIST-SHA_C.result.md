# idea 1019 — should every RECORD CENSUS carry its FILE-LIST SHA? (lane C, 2026-09-16)

**ANSWERED = YES, AND THE STAMP IS NEARLY FREE — BUT THE CHEAP SUBSTITUTE EVERYONE ASSUMES
IS ALREADY THERE (THE GIT HISTORY) DOES NOT WORK. KILL the "the corpus is in git, so any
census is re-derivable" framing; KEEP a PROTOCOL rule-5 CENSUS STAMP clause (proposed, not
applied — rule 6). Gates 9 of 10, hypotheses 3 of 9, and every failure is the answer.
Nothing promoted, no KEEP claimed on either price path; `RULES.md`, `PROTOCOL.md`,
`scan.py`, `bot.py` and `baseline.py` untouched.**

## THE OBJECT

Idea 1014's G3 missed idea 1010's committed census by 1.49e-02 and reproduced it at 9.54e-17
once restricted to 1010's own 449-file list. 1019 asks what that costs corpus-wide. To
answer it at all the shallow clone was deepened to the **full 1,427-commit history**
(2026-09-03 → 2026-09-16), so the corpus can be rebuilt at any commit.

**TUNED 1 — STAMP SCOPE** (4 rungs): `NONE` (the corpus at HEAD, what a reader gets today),
`DATE_AT` (the git tree at the census's own commit), `DATE_PARENT` (the tree just before it),
`LIST` (the file list the run committed). **TUNED 2 — CLAIM SET** (3 rungs): `REPRO2` (the 2
censuses that shipped a file list — quantitative re-derivation), `CENSUS_N` (all **214**
committed `*.census.csv` artifacts — structural), `PROSE` (**80** corpus-SIZE claims regexed
out of 72 committed documents, against a git ground truth). Every grid point reported, none
selected. 31 s.

**THE ARITHMETIC RESTS ON APPEND-ONLY-NESS, AND IT IS MEASURED, NOT ASSUMED.** Of 456
census-eligible CSVs, **2 were modified in place after their add commit** (append-only rate
**0.9956**), and G3c shows those two edits moved **+0 rows**. That is what licenses rebuilding
any historical census as a sum of per-file statistics computed once at HEAD.

## THE HEADLINE IS AN INTEGER AND IT IS TWO

**2 of 214** committed census artifacts ship a file list (`L2_LIST` 0.0093); **0** ship a
content hash (`L3_SHA` 0.0000); **175** state a count in prose only (`L1_COUNT`); **37** state
nothing (`L0_NONE`). **H_STAMP FAIL 0.0093 against a 0.50 bar.** Both stamped censuses are
from the last 24 hours, both filed after the defect was noticed.

**WHAT THE UNSTAMPED STOCK IS WORTH TODAY. H_PROSE FAIL, and it is a zero.** Of the **80**
corpus-SIZE claims in the record, **0 reproduce exactly at HEAD** — median relative error
**0.6526**, i.e. the corpus the median claim describes is two thirds smaller than the one a
reader rebuilds today. Pinning the commit date recovers almost nothing exact (**0.0125**
`DATE_AT`, **0.0625** `DATE_PARENT`, **0.0750** under any of the three), though **66.25%**
land within 5% under either date scope. The exact-match failure conflates two causes and the
run says so: **definition drift** (claims count different things — with/without `.csv.gz`,
scanned vs admitted) and **corpus drift**. The 5% band isolates the second; the exact column
is the honest measure of what a reader can *verify*, and it is zero.

**THE DENOMINATOR HAS DOUBLED UNDER THE MEDIAN CENSUS. H_DRIFT FAIL.** Across the 214
locatable censuses, census-eligible FAIL rows grew **median +0.9055**, mean **+6.4049**, p90
**+2.7778**, max **+553.46** between a census's own commit and HEAD. **Every corpus-wide
share in this record was computed on a denominator that no longer exists**, and 1019's
question is whether the record can tell *which* one.

## THE MECHANISM: A CENSUS CANNOT SEE THE COMMIT IT IS IN. H_SELF PASS 1.0000

**Every one of the 214 censuses lands in a commit that adds CSVs the run could not have
scanned** — median **6**, max **16** files. On the census-eligible subset it bites in
**31.31%** of censuses, up to **41,338 FAIL rows** in one commit. So `DATE_AT` is not a
well-defined reconstruction *a priori* — and yet it is the arm that works (below), because
runs scan their own outputs. A date stamp therefore requires knowing something a date cannot
express: whether the run read the corpus before or after writing into it.

**This run reproduced the defect on itself.** Its own `.grid` / `.keeppaths` / `.walkforward`
outputs carry a `fail4b` column, so a second pass over a directory holding them reads **459**
files, not **456**. The headline census is taken on the self-excluded set and both totals are
stamped in `.stamp.txt`.

## REPRO2 — THE FOUR SCOPES ON THE TWO STAMPED CENSUSES

| idea | scope | n_files | n_rows | n_fail | max relerr vs PUBLISHED | re-derivable @1e-3 |
|---|---|---|---|---|---|---|
| 1010 | NONE | 456 | 1,011,630 | 896,559 | **1.665e-02** | **False** |
| 1010 | DATE_AT | 449 | 995,110 | 883,294 | 4.824e-05 | True |
| 1010 | DATE_PARENT | 446 | 995,014 | 883,221 | **6.682e-03** | **False** |
| 1010 | LIST | 449 | 995,110 | 883,294 | 4.824e-05 | True |
| 1014 | NONE | 456 | 1,011,630 | 896,559 | 1.896e-05 | True |
| 1014 | DATE_AT | 454 | 1,011,432 | **896,542** | **0.000e+00** | True |
| 1014 | DATE_PARENT | 452 | 1,011,294 | 896,431 | 1.238e-04 | True |
| 1014 | LIST | 441 | 1,011,059 | **896,542** | **0.000e+00** | True |

**H_DERIVE FAIL** — the worst `NONE`-scope error is **1.665e-02**, sixteen times the 1e-3 bar.
**H_GITDATE FAIL as registered**: `DATE_PARENT` misses 1010 by **6.682e-03**. Reported, not
the registered arm: `DATE_AT` lands at **4.824e-05** and `LIST` at the same — and the two are
identical because 1010's list *is* its own commit's eligible set. Note how loose the 1e-3 bar
is on a ~900k denominator: it tolerates ~900 rows, which is why 1014 reads "re-derivable"
even at `NONE`. It is generous and 1010 still fails it.

**A LIST IS ENOUGH ON THIS CORPUS; A SHA IS WHAT WOULD DETECT THAT IT ISN'T.** G3 reproduces
1010's manifest **per file** at max |d| = **0** over all 449 files; G4 reproduces 1014's
published 896,542 at **0.000e+00**. The two in-place edits (G3c) moved 0 rows, so nothing was
lost here — but a file list cannot *detect* an in-place edit at any price, and 2 of 456 files
got one inside 13 days. The SHA buys detection, not accuracy.

**THE STAMP ALREADY CAUGHT A PUBLISHED ERROR — G3b FAIL, AND IT IS THE BEST ARGUMENT IN THE
RUN.** Idea 1010's committed manifest sums to **995,110 rows / 883,294 FAIL**, and its own
console prints `rows read : 995,110` and `235 unparsed of 995,110`. Its **result.md publishes
995,062** ("995,062 rows read, ~247 MB", and "235 of 995,062"). **The published headline is 48
rows off the run's own artifacts**, FAIL rows agreeing exactly. This is not corpus drift and
not a reproduction failure by this run: it is a transcription gap inside one publication that
**only the manifest makes visible**. 1014's earlier 1.49e-02 miss of 1010 was a different
object (leg shares on a grown corpus); this is a new, smaller, sharper defect.

**MANIFEST COMPLETENESS — a list can be lossy, and one of the two is.** 1010's manifest
enumerates **449 of 449** eligible files in its own tree, 13 of them carrying zero FAIL rows.
**1014's enumerates 441 of 454**: the 13 absentees are exactly the files with **zero** FAIL
rows, because its per-file table only appended rows where `n_fail > 0`. That manifest pins the
numerator and leaves the denominator loose — which is why its `LIST` row above reads 441 files
and 1,011,059 rows while still reproducing its FAIL count exactly. **A stamp clause has to say
"every file READ", not "every file that HIT".**

## THE COST — H_COST FAIL ON THE RATIO, AND THE RATIO IS THE WRONG NUMBER

sha256 over the sorted (file, size, sha256) manifest of 456 files: **0.60 s** marginal
(hash-only; a census already holds the bytes), **0.78 s** standalone, **68,744 bytes** for the
full manifest and **105 bytes** for the one-line stamp. Against this run's scan that is
**0.1175**, which fails the pre-registered 1% bar — but the denominator is page-cache
dependent (**32 s cold, 5.1 s warm** on this box), so the bar was measuring the cache, not the
stamp. **The durable numbers are 0.60 s and 67 KB**, and both are reported as the answer to
"cost a `file_list_sha` stamp". Against the 5 s–32 s this run spent scanning and the minutes
its price ladder took, the stamp is free at any cache temperature. **H_APPEND PASS 0.9956**
(2 of 456 modified); **G7 PASS**, 30 sampled eligible files byte-identical at add-commit and
HEAD.

## RULE 8 (PROTOCOL rule 8) AND BOTH KEEP PATHS — OOS 4b **0 of 6**, 4a **0 of 60**

60-book grid at 10 bps, next-day execution: 2 panels × 2 cadences (W, M) × 5 books
(`EWELIG`, `BAND03`, `TOP10`, `TOP20`, `TOP40`) × 3 gross rungs. Picks made on **2009–2016
alone** by three IS-only choosers × 2 panels, 2017–2026 read once:

| panel | chooser | pick | OOS CAGR | OOS Sharpe | OOS MaxDD | 4b |
|---|---|---|---|---|---|---|
| U56 | IS_SHARPE / IS_CAGR | `TOP10`/M @1.00 | 23.17% | 1.1045 | −29.79% | FAIL `L4_DD` |
| U56 | IS_LEGS | `TOP10`/M @0.75 | 17.31% | 1.1009 | −23.22% | FAIL `L4_DD` |
| B136 | IS_SHARPE | `TOP20`/M @1.00 | 20.81% | 1.0051 | −33.68% | FAIL `L4_DD` |
| B136 | IS_CAGR | `TOP10`/M @1.00 | 24.16% | 0.9992 | −35.79% | FAIL `L4_DD` |
| B136 | IS_LEGS | `TOP20`/M @0.75 | 15.55% | 1.0004 | −26.11% | FAIL `L4_DD` |

**Every rule-8 pick binds `L4_DD` and nothing else** — the IS window buys gross, and gross
buys drawdown. Comparands: **SPY OOS 15.21% / 0.8713 / −33.72%** (U56) and
**15.33% / 0.8769 / −33.72%** (B136); **RULES v2 (live) OOS 9.45% / 1.2765 / −12.05%** (U56,
full Sharpe 1.2009 / MaxDD −12.05%) and **7.88% / 1.1061 / −12.24%** (B136, full 1.0994 /
−12.24%). Full-sample **KEEP path 4b 14 of 60** (12 U56, 2 B136) and **KEEP path 4a 0 of
60** — gross against the live book's −12.05% is not close on any cell. **Nothing is
promoted**: no rule-8 chooser picks a 4b passer, none of these is a new book, and every 4b
count is an upper bound under the standing base-rate, per-leg-percentile, declined-slot and
split-point-band clauses (926/942, 975-B, 993, 1013-B). An unplanned cross-run reproduction:
U56/M/`TOP20`@0.75 reads **16.68% / 1.2833 / −19.51%** against idea 980's committed headline
**16.68% / 1.283 / −19.51%**.

## GATES — 9 of 10 PASS, printed before any result number

G0 PASS (235 unparsed of 1,011,630, all **excluded**, none guessed) · G1 PASS fast `Ctx` ==
`engine.backtest` on post-warm-up net returns **and** turnover **1.665e-16** · G2 PASS band
book == `baseline.rules_v2_weights` **0.000e+00** · **G3 PASS** 1010's 449-file manifest
re-read per file at max |d| **0** · **G3b FAIL 48 rows — the finding above** · G3c PASS
in-place edits moved **+0** rows · **G4 PASS** 1014's 896,542 at **0.000e+00** · G5 PASS SPY
OOS **15.2102% / 0.8713 / −33.7173%** vs the record's committed 15.21% / 0.8713 / −33.72% ·
G6 PASS determinism **0.0** · G7 PASS append-only, 0 of 30 sampled differ.

## LIMITS, STATED

The quantitative re-derivation covers **one** census family — the `fail4b` leg census, 1010's
and 1014's object — because it is the only one this run can recompute from a committed
definition. The other 212 censuses are scored **structurally** (stamp level, git
recoverability, denominator drift), not re-run; their claims are not asserted to be wrong,
only **unverifiable**. The `PROSE` arm's regex is deliberately conservative — only claims
about the TOTAL corpus size, never a subset claim like "160 committed files carry an OOS
Sharpe", which has no git ground truth — so **80 is a lower bound** on the record's
corpus-wide count claims and the 0-of-80 exact rate is measured on the subset most favourable
to re-derivation. The whole history-based reconstruction assumes the repository is the only
route by which files enter the corpus; an uncommitted file read at run time would be invisible
to every scope here, which is one more thing a scan-time stamp catches and git cannot.

## SURVIVORSHIP (PROTOCOL rule 9)

The census arms are a census of committed text and inherit their sources' bias. The price
ladder runs on **U56** and **B136**, current-constituent lists, so every CAGR and drawdown
LEVEL is optimistic and the 14 full-sample 4b passes are an **upper** bound. The ladder is a
control here, not the finding: it exists to satisfy rule 8 and to show the meta-question moves
no price verdict (**H_RULE8 PASS**). SPY is a real index series and is not inflated.

## PROPOSED, NOT APPLIED (rule 6)

`2026-09-16_census-stamp-clause_C.memo.md` proposes a PROTOCOL rule 5 addition: *a run that
publishes a statistic over the committed corpus commits a `<stem>.stamp.txt` naming every file
READ (not every file that hit), its byte length and its sha256, plus the aggregate row count
and a `file_list_sha` over that manifest; a corpus-wide claim published without one is read as
unverifiable and may not be cited as a denominator by a later run.* Applying it to the record
re-labels **212 of 214** committed censuses as unverifiable and leaves the two stamped ones
standing. It contradicts nothing: 1010's and 1014's numbers are reproduced here exactly on
their own lists.

Follow-ups filed: 1024 (back-fill stamps for the 37 `L0_NONE` censuses by rebuilding their
file lists from git and report how many published shares move), 1025 (the `L1_COUNT` majority
state a count — test whether a row COUNT alone is as good as a file list, since it is what 175
censuses already have), 1026 (a census reads the corpus while other lanes are committing into
it: measure the concurrent-write window from commit timestamps and price what it costs a
scan-time stamp to close).
