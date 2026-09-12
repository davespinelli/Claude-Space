# Idea 565 — which committed artefacts read a NIGHTLY-REWRITTEN metadata file? (lane B, 2026-09-12)

**ANSWERED on both clauses. KILL for capital (0 of 1,200 books clear 4a or 4b). One convention
survives rule 8 and two do not.** No RULES change, no KEEP claimed, no memo, no book promoted, no
PROTOCOL edit applied (rule 6); `RULES.md`, `PROTOCOL.md`, `scan.py`, `bot.py` and `baseline.py`
untouched.

Script: `2026-09-12_which-committed-artefacts-read-a-NIGHTLY-REWRITTEN-metadata-file_B.py`
Outputs: `.console.txt` `.census.csv` `.books.csv` `.drift.csv` `.walkforward.csv`

## Selection
Taken as the LAST open idea in `QUEUE.md` that has a price leg. The tail below it — 564, 537, 532,
534, 529 (x2), 528 — is census/AST work with no book, 429 is PARKed on data the sandbox does not
carry, and 353 needs a live `yf.download`. Each was marked SKIP again rather than silently passed
over. 565's second clause ("price a coverage-pinning convention") IS a book, so it can carry this
lane's mandatory rule-8 walk-forward.

## What this run could do that idea 313 could not
Idea 313 saw ONE vintage of `research/deepvalue/universe_under2b.csv` and INFERRED the book drift
from coverage counts (max|dSharpe| 0.233). `git fetch --unshallow` recovers **13 committed vintages**
of that file (2026-09-04 .. 2026-09-12) and **3 of the price panel**, so the drift is **measured**
here across real revisions, and the two job-written inputs are separated.

## Clause 1 — the census (`.census.csv`)
27 committed `.py` files under `research/` and `products/` were scanned against every committed file
under `data/` and `research/deepvalue/`; 32 (script, file) read pairs, 6 distinct files.

| file | commits | job commits | scripts reading it |
|---|---|---|---|
| `research/deepvalue/universe_under2b.csv` | 13 | 8 | 14 as KEY, 3 as META |
| `research/deepvalue/candidates.csv` | 12 | 9 | 4 as KEY |
| `research/deepvalue/filings/MANIFEST.json` | 10 | 8 | 1 as KEY |
| `research/deepvalue/ls_daily.csv` | 6 | 4 | 1 as KEY |
| `research/deepvalue/universe_v2.csv` | 6 | 4 | 1 as KEY |
| `research/deepvalue/data/company_tickers.json` | 1 | 0 | (not job-written) |

**20 committed scripts read at least one job-written file; 17 of them read it as a KEY** (a column
that drives membership or ranking), and **10 of those 17 are backtests in `research/backtests/`**.
"Job-written" = ≥2 commits whose subject carries `[actions]` / `Filings:` / `Daily close` /
`Options cache` / `Weekly`.

**G4 — one vintage of the key file is not readable at all.** Commit `c2de3ef0` (2026-09-08, "Deep
Value: quality-growth screen v2") shipped `universe_under2b.csv` **with 3 git conflict-marker lines
in the tree**; it is unparseable and was fixed by `a1b46677` the same day. Any script that read the
file at that commit got a `ParserError` or, with `on_bad_lines='skip'`, a silently truncated
universe. Reported, not dropped.

## Clause 2 — pricing the pinning convention

Book family **pinned, not tuned** — idea 51 lane B's / idea 313's capQ point copied verbatim: SMALL
panel (663 tradable after dropping 52 names with `max_1d_move ≥ 1.0`), CAP key at the LATE stamp,
NDEC=10, g=0.75, weekly, cost 10 bps, MA 200d, arms {EWall, MA-DG}. Idea 313's third arm MA-RS was
dropped for runtime; that is stated, not a selection.

**2 tuned parameters, fully crossed, every point reported:** VINTAGE (the 12 readable revisions) ×
PINNING (5 rules) × 10 deciles × 2 arms = **1,200 books, 60 cells**.

Coverage of each vintage on today's tradable panel: 431 (09-04) → 434 (09-05..09-08) → **652**
(09-08, after the screen-v2 rewrite) → 660 → 663 → 657 (09-12). Intersection of all 12 = **424**,
union = **663**, churn = **239 names**. The queue described a five-name wobble; the file actually
carries a **+218-name regime break** inside one week.

### G1 / G2 / H4 — is a committed number reproducible, and from which file?

| rebuild of idea 313's committed `MAIN/CAP/LATE` rows | cells | max\|dSharpe\| | max\|dn_names\| |
|---|---|---|---|
| **G1** coverage@2026-09-09, panel@2026-09-04 (the files that existed that night) | 20/20 | **0.000000** | 0 |
| **H4** coverage@2026-09-09, panel@2026-09-11 (move only the PANEL) | 20/20 | **0.222229** | 23 |
| **H4** coverage@2026-09-12, panel@2026-09-04 (move only the COVERAGE file) | 20/20 | **0.172596** | 1 |
| **G2** coverage@2026-09-12, panel@TODAY (what a reader gets now) | 20/20 | **0.259806** | 23 |

**G1 PASS.** Idea 313's published row is exactly reproducible — *from the vintages it read*. **G2:
today's tree returns a different number for the same committed claim, by 0.2598 of Sharpe.**

**H4 corrects the queue's diagnosis.** Idea 565 blames the metadata file. The larger single channel
is the **price panel** (0.2222 alone) — `data/prices_small.csv.gz` is job-written too, and it moves
23 names in a decile against the coverage file's 1. The metadata file is the *second* channel
(0.1726), not the only one. Any pinning convention that names only `universe_under2b.csv` fixes less
than half the problem.

### H1 / H2 — the drift, and what each convention buys (`.drift.csv`)

Spread (max − min) across the 12 vintages, worst and median over the 20 (decile, arm) cells:

| PIN | max spread Sharpe | median | max\|dS vs ref\| | max spread CAGR | max spread MaxDD | max spread n | reduction |
|---|---|---|---|---|---|---|---|
| **LIVE** (what the record does) | **0.2833** | 0.1266 | 0.2580 | 3.02% | 12.93% | 24 | — |
| **PINFIRST** (freeze the name set) | 0.2298 | 0.0776 | 0.1525 | 1.84% | 10.24% | 1 | 18.9% |
| **PININT** (freeze to the intersection) | 0.1777 | 0.0747 | 0.1777 | 1.68% | 5.83% | 0 | 37.3% |
| **KEYONLY** (commit the key column) | 0.0253 | 0.0000 | 0.0212 | 0.31% | 0.91% | 3 | 91.1% |
| **COMMITKEY** (key column + name set) | **0.0000** | 0.0000 | 0.0000 | 0.00% | 0.00% | 0 | 100% |

**H1: the measured drift is 0.2833, LARGER than idea 313's inferred 0.233.** The idea's premise is
confirmed and understated.

**H2, and this is the substantive result: freezing the NAME SET is the wrong fix.** PININT holds
membership literally constant (max spread in n = 0) and still leaves **0.1777** of Sharpe on the
table, because the drift is not coverage — it is the **qcut edges moving when the mktcap VALUES are
re-stated**, which happens to names that never leave the file. Committing the key column removes
91.1% of it on its own; only committing the key column *and* the name set is exact (**G3 PASS**,
spread 0.000e+00).

### H3 — verdict stability
0 of 1,200 books pass 4a or 4b, so no conjunction can flip and "no flips" would be a vacuous claim.
Every PROTOCOL leg is therefore scored separately. Cells (of 20) whose leg value depends on the night
the file was read:

| PIN | a_h1 | a_h2 | a_dd | b_h1 | b_h2 | b_oos | b_dd | b_cagr |
|---|---|---|---|---|---|---|---|---|
| LIVE | 9 | 10 | 3 | 7 | 0 | 0 | 3 | 4 |
| PINFIRST | 3 | 8 | 1 | 2 | 0 | 0 | 5 | 3 |
| PININT | 2 | 8 | 0 | 2 | 0 | 0 | 4 | 4 |
| KEYONLY | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| COMMITKEY | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

Under LIVE, **10 of 20 cells** change their 4a second-half verdict on the read night alone. Over all
1,200 books the legs pass: a_h1 245, a_h2 472, a_dd 39, b_h1 87, **b_h2 0**, **b_oos 0**, b_dd 464,
b_cagr 301 — 4b dies on its second-half and OOS Sharpe legs everywhere, which is why the conjunction
is constant.

## RULE 8 — walk-forward (IS 2010-2016 chooses, OOS 2017-2026 read once)

**W1 — the CLAIM. FAIL, and the failure is the finding.**

| PIN | IS max spread Sharpe | OOS max spread Sharpe | OOS/IS |
|---|---|---|---|
| LIVE | 0.5726 | 0.2038 | 0.356 |
| PINFIRST | 0.3506 | **0.2229** | 0.636 |
| PININT | 0.3044 | **0.2463** | 0.809 |
| KEYONLY | 0.0399 | 0.0412 | 1.033 |
| COMMITKEY | 0.0000 | 0.0000 | — |

Freezing the name set cuts the IS drift (0.5726 → 0.3506 / 0.3044) and **does not cut it out of
sample** (0.2038 → 0.2229 / 0.2463 — both *worse* than doing nothing). Only KEYONLY and COMMITKEY cut
it in both windows. **An in-sample-only reading of this run would have recommended the wrong
convention**, which is exactly what rule 8 exists to catch.

**W2 — a PICK (best IS Sharpe chosen on IS alone; OOS read once).**

| PIN | pick | IS Sharpe | OOS CAGR | OOS Sharpe | OOS MaxDD | 4a | 4b |
|---|---|---|---|---|---|---|---|
| LIVE | 2026-09-10, d02, EWall | 1.262 | 6.44% | 0.449 | −37.06% | F | F |
| PINFIRST | 2026-09-04, d02, EWall | 0.968 | 6.56% | 0.432 | −42.69% | F | F |
| PININT | 2026-09-12, d02, EWall | 0.981 | 5.86% | 0.392 | −45.65% | F | F |
| KEYONLY | 2026-09-04, d02, EWall | 0.968 | 6.56% | 0.432 | −42.69% | F | F |
| COMMITKEY | 2026-09-04, d02, EWall | 0.968 | 6.56% | 0.432 | −42.69% | F | F |
| **SPY** | comparand | 0.858 (full) | **15.33%** | **0.877** | −33.72% | | |
| **RULES v2 (live)** | comparand | 0.664 (full) | 3.75% | 0.560 | −13.89% | | |
| **RULES v1** | comparand | 0.882 (full) | 7.83% | 0.706 | −29.12% | | |

Every IS-chosen pick loses to SPY on OOS CAGR and OOS Sharpe and has a worse drawdown; LIVE's pick
carries the highest IS Sharpe (1.262) and the *second-worst* OOS Sharpe of the five — the reward for
picking the luckiest night.

**W2b — does the IS-best VINTAGE stay best out of sample?** Under LIVE it does not (IS-best 09-10,
OOS-best 09-04; 0.681 vs 0.756 OOS Sharpe), and under PININT it does not (09-12 vs 09-05; 0.699 vs
0.741). Under PINFIRST / KEYONLY / COMMITKEY it does, trivially. **The read night is itself a tuned
parameter that does not survive rule 8.**

## Book statistics (all 1,200 in `.books.csv`)
LIVE: CAGR 2.21%–12.10% (median 6.78%), Sharpe 0.320–0.852 (median 0.597), MaxDD −47.77%…−11.85%;
OOS CAGR 0.69%–13.88% (median 5.34%), OOS Sharpe 0.131–0.756 (median 0.552), OOS MaxDD −47.77%…−10.71%.
COMMITKEY: CAGR 2.21%–12.02% (median 6.34%), Sharpe 0.320–0.702 (median 0.549), MaxDD −45.79%…−13.22%;
OOS CAGR 1.17%–13.88% (median 5.67%), OOS Sharpe 0.190–0.756, OOS MaxDD −45.79%…−12.28%.
SPY full CAGR 14.06% / Sharpe 0.858 / MaxDD −33.72%; RULES v2 4.30% / 0.664 / −13.89%; RULES v1
9.95% / 0.882 / −29.12%. **No book beats SPY on both halves; 4b's b_h2 and b_oos legs are 0 of 1,200.**

## Gates
G1 PASS (0.000000) · G2 gap 0.259806 (the premise) · G3 PASS (0.000e+00) · G4 PASS (1 of 13 vintages
unreadable, 3 conflict-marker lines) · G5 PASS (`fast_run` vs `engine.backtest`, 3 books, max|d| <
1e-12 over the scored window). `engine.backtest` emits 2 NaN bars before its first rebalance (its
row-0 `w_target` is NaN because `fillna` precedes `shift`); every book here is scored from 2011-01-13,
260 bars later, so no scored bar is affected. Stated, not hidden.

## Survivorship
SMALL panel = current constituents of the sub-$2B screen only, no delisted names, so every LEVEL is
biased up and the thin deciles most. Every claim above is a vintage-vs-vintage DIFFERENCE on one
panel, which is the one quantity that bias does not move.

## Proposed PROTOCOL line — NOT applied (rule 6: Sunday review only)
> **10. As-of pinning.** A script whose membership or ranking key comes from a job-written file
> (`research/deepvalue/*.csv`, `data/prices*`, `data/small_meta.csv`, any `[actions]`-committed
> artefact) MUST commit the resolved KEY COLUMN — ticker → key value or decile label — beside its
> result, and quote the reading commit SHA of every such file it read. Freezing the NAME SET is not
> a substitute: it removes 18.9%–37.3% of the drift in sample and none of it out of sample
> (idea 565).

## Verdict
**KILL for capital** — 0 of 1,200 books clear 4a or 4b; the capQ decile ladder is not a book.
**ANSWERED for the record** — 17 of 20 committed scripts that read a job-written file read it as a
KEY, one committed vintage of that file is unreadable, the measured drift (0.2833) exceeds the
inferred one (0.233), the larger channel is the PRICE PANEL rather than the metadata file, and of the
three conventions the queue suggested only "commit the key column" survives rule 8.
