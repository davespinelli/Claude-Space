# MEMO — PROTOCOL rule 5 CENSUS STAMP clause (proposed, not applied; rule 6)

Evidence: `2026-09-16_should-every-RECORD-CENSUS-carry-its-FILE-LIST-SHA_C.result.md` (idea
1019, lane C). 2 of 214 committed censuses carry a file list, 0 carry a hash; 0 of 80
corpus-size claims reproduce at HEAD; the FAIL-row denominator has grown a median +0.9055
since the median census; cost 0.60 s and 67 KB.

**Exact wording proposed for PROTOCOL rule 5 (an addition; nothing existing is struck):**

> **5b. Census stamp.** A run that publishes any statistic whose denominator is the committed
> corpus writes `research/backtests/<stem>.stamp.txt` carrying, for **every file READ — not
> every file that hit** — its path, byte length and sha256, plus the aggregate row count, the
> HEAD commit, and a `file_list_sha` (sha256 over that sorted manifest). The published prose
> quotes the manifest's own totals verbatim. A corpus-wide claim published without a stamp is
> read as **unverifiable**: it may be repeated as history but may not be cited as a
> denominator, a base rate, or a comparand by a later run.

**Why the file list, not the commit date:** every census lands in a commit that adds files it
could not have scanned (self-inclusion 1.0000, median 6 files), so no tree is the right one a
priori; `DATE_PARENT` misses idea 1010 by 6.682e-03 while its own list reproduces it per file
at |d| = 0.

**Why the sha, not just the list:** 2 of 456 census-eligible files were edited in place inside
13 days. Those edits moved 0 rows, so nothing is wrong today — a list cannot detect the next
one at any price, and a hash costs 0.60 s.

**Why "every file read":** idea 1014's manifest lists 441 of the 454 eligible files in its own
tree; the 13 absentees are exactly those with zero FAIL rows. It pins the numerator and leaves
the denominator loose.

**What it would have caught already:** idea 1010's published "995,062 rows read" is 48 rows
off its own committed manifest and its own console (995,110). The manifest is the only artifact
in the record that makes that visible.

**Effect if adopted:** re-labels 212 of 214 committed censuses unverifiable; changes no price
verdict (this run's 4a is 0 of 60 and 4b 14 of 60 either way); adds ~67 KB and under a second
per census run. Contradicts no committed result — 1010's and 1014's numbers are reproduced
here exactly on their own lists.
