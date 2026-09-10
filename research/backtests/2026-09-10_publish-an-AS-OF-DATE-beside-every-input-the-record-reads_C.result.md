# Idea 629 — publish an AS-OF DATE beside every input the record reads (lane C, 2026-09-10)

**Verdict: ANSWERED/SPLIT. The census answers YES and decisively; the consequence leg is a
measured NULL on the recommended gate. No KEEP, no PARK, no book promoted, no RULES change.
PROTOCOL.md, RULES.md, scan.py, bot.py and baseline.py untouched — the PROTOCOL clause below is
proposed for Sunday review, not applied.**

Script `2026-09-10_publish-an-AS-OF-DATE-beside-every-input-the-record-reads_C.py`;
`.census.csv .certs.csv .confusion.csv .arms.csv .gates.csv .walkforward.csv .console.txt`
alongside. Costs 10 bps with 0 and 25 reported; weights at close t applied t+1.

## Gates (five, pre-registered — all pass)

| gate | statistic | value | tol |
|---|---|---|---|
| G1 | `fast_backtest` == `engine.backtest` on the control book (returns / turnover) | **1.388e-17 / 3.331e-16** | 1e-12 |
| G2 | cost-rung identity `r(c) = r(0) − turnover·c/1e4` @25 bps | **1.388e-17** | 1e-12 |
| G3 | idea 623's committed `.certs.csv` `T2_med` reproduced under ASOF_TRUE, 20/20 keys | **0.000e+00** exact; `T1_flag` agreement 20/20 | 0 |
| G4 | a causal scale-free control key clears T1 and T2 under **all three** dating rules | **0.000e+00** | 0 |
| G5 | idea 623's `absIC_fwd` leak column reproduced, 20/20 keys | **< 5e-3** | 5e-3 |

G3's split matters: T2's median is deterministic (fixed probe dates) and matches idea 623 **bit
for bit**; T1's median is a Monte-Carlo statistic over 8 rescale draws, so only its flag is
seed-comparable — and it agrees 20/20.

## PART A — the census (tuned dial 1: FILE CLASS)

24 input files under `data/`, `research/*.json`, `research/deepvalue/`, `research/tenders/` and
the pinned artefacts. 16 are read by ≥1 committed script; **12 by a rule-8-running one**.

| FILE CLASS | all 24 files | read by a rule-8 script (12) |
|---|---|---|
| STRICT (only `as_of`/`asof`/`scan_date`/`pinned_utc`/`filing_date`… counts) | INDEX_DATE 10, UNDATED 8, ROW_KNOWLEDGE 6 | UNDATED **5**, INDEX_DATE 4, ROW_KNOWLEDGE 3 |
| LOOSE (any date-parsing column counts) | INDEX_DATE 10, UNDATED 7, ROW_KNOWLEDGE 6, ROW_EVENT_ONLY 1 | INDEX_DATE 4, UNDATED **4**, ROW_KNOWLEDGE 3, ROW_EVENT_ONLY 1 |

**Four files read by a rule-8-running committed script have NO recoverable dating under EITHER
reading**, and they are not obscure ones:

| file | readers | of which run rule 8 | only external dating |
|---|---|---|---|
| `research/universe.json` | 258 | **253** | git 2026-09-09 |
| `research/universe_broad.json` | 232 | **229** | git 2026-09-09 |
| `research/deepvalue/universe_under2b.csv` | 11 | 9 | git 2026-09-09 (rewritten nightly — idea 565) |
| `research/deepvalue/data/company_tickers.json` | 4 | 2 | git 2026-09-09 |

The record's **most-read input is its own universe list, and it carries no as-of date at all**.
253 rule-8-running scripts read a current-constituent name set whose knowledge date exists
nowhere in the file; the only dating available is a git timestamp that moves whenever the file is
re-committed. `data/small_meta.csv` (304 readers, **301 rule-8**) is UNDATED under STRICT and only
ROW_EVENT_ONLY under LOOSE: its `first_date`/`last_date` are the panel's own event dates and do
not date the `max_1d_move` payload that idea 623 flagged and idea 627 priced. By contrast
`research/tenders/history.csv` already publishes `scan_date` and the form-4 and earnings files
publish `filing_date` — the convention exists in the repo; it is simply not required.

## PART B — the instrument (tuned dial 2: DATING RULE)

Idea 623's 20-key corpus, T1 (scale) and T2 (dating) re-run under three rules for the one
exogenous input (the shares snapshot). Detection is against the dating ground truth, tol = idea
433's one rank step.

| rule | T1 | T2 | T1&T2 | exog-only slice, T1&T2 |
|---|---|---|---|---|
| **NONE** (no column — what an UNDATED file forces) | 3/10 | **6/10** | **8/10** | **2/4** |
| **ASOF_TRUE** (idea 623's courtesy) | 3/10 | **10/10** | **10/10** | **4/4** |
| **ASOF_EARLY** (the value really was knowable in 2010) | 1/6 | 6/6 | 6/6 | n/a (0 terminal) |

Two structural findings, both exact rather than statistical:

1. **T1 is invariant to the dating rule.** `max|T1_med(rule) − T1_med(NONE)| = 0.000e+00` across
   all 20 keys and all three rules. The scale certificate perturbs the price panel and never
   touches an exogenous input, so no as-of column can change what it sees. Idea 629's premise —
   that SHARES and MCAPREB are invisible to **both** certificates without a date — is confirmed
   directly: they carry `T1_med = 0.0` and `T2_med = 0.0` under NONE.
2. **T2(NONE) is bit-identical to T2(ASOF_EARLY) on every one of the 20 keys, while the ground
   truths differ on 4** (MCAP, MCAPFRZ, MCAPREB, SHARES). This is an **identification** failure,
   not a power failure: the certificate's output is the same in a world where the snapshot is a
   terminal read and in a world where the identical value was knowable from the panel's first
   day. No tolerance, no extra probe date and no larger draw count can separate them. Only the
   column can. That is the tightest statement of what the field buys.

Idea 623's headline (T2 perfect, 10/10, FP 0) is therefore **a statement about idea 195's
courtesy, not about the record**. Re-read on the dating the files actually publish, T2 detects
6 of 10 and T1&T2 8 of 10.

## PART C — the consequence, and PROTOCOL 8

Book: `score = composite + dir·m·(key − 0.5)`, above own 200d MA, `vol20 < 0.60`, top n=20,
gross 0.75, weekly, SMALL430. **20 keys × 2 dirs × 3 m × 3 cost rungs = 360 arms, every one in
`.arms.csv`.** Comparands over the common window: SPY 14.13 % / 0.862 / −33.72 % (OOS 15.45 % /
0.882 / −33.72 %); RULES v2 live 3.77 % / 0.565 / −14.58 % (OOS 0.558); RULES v1 7.41 % / 0.554 /
−34.92 %; no-tilt control 6.12 % / 0.438 / −25.90 %.

**PROTOCOL 4a 0/360 and 4b 0/360.** Failing legs: DD **357**, H1 332, H2 286, OOS 285, CAGR 267 —
idea 195's drawdown-cap result on the same panel, for the fourteenth time.

Rule 8: (KEY, dir, m) chosen on 2010–2016 IS Sharpe alone among the admitted keys; 2017–2026 read
exactly once, at 10 bps.

| gate | rule | keys admitted | pick | IS Sh | OOS CAGR / Sharpe / MaxDD |
|---|---|---|---|---|---|
| T2 only | NONE | 14/20 | **MCAP/NEG/1.00 — terminal-dated** | 0.963 | 26.31 % / **1.584** / −24.87 % |
| T2 only | ASOF_TRUE | 10/20 | PXDVOL/NEG/1.00 (causal) | 0.838 | 24.41 % / **1.588** / −24.38 % |
| T2 only | ASOF_EARLY | 14/20 | MCAP/NEG/1.00 | 0.963 | 26.31 % / 1.584 / −24.87 % |
| **T1&T2** (623's recommendation) | NONE | 8/20 | VOL20/NEG/0.50 (causal) | 0.796 | 5.79 % / **0.467** / −26.88 % |
| **T1&T2** | ASOF_TRUE | 6/20 | VOL20/NEG/0.50 (causal) | 0.796 | 5.79 % / **0.467** / −26.88 % |
| **T1&T2** | ASOF_EARLY | 8/20 | VOL20/NEG/0.50 | 0.796 | 5.79 % / 0.467 / −26.88 % |

**The honest half of the answer is the null.** On idea 623's recommended T1&T2 gate the missing
column changes the admitted set (8 keys → 6) and **does not move the pick at all**: VOL20/NEG/0.50
under all three rules, OOS Sharpe 0.467, losing to SPY 0.882 and to RULES v2 0.558. dSharpe_OOS
from adding the column: **+0.0000**. P5 MISS.

But the protection is thin and measurable, not structural. Under NONE the T1&T2 gate **admits 2
terminal-dated keys it cannot see** (MCAPREB, SHARES); the best of their arms, MCAPREB/NEG, sits
only **+0.113 of IS Sharpe** below the pick and would have delivered **OOS 0.962** — beating SPY.
The selector missed the blind spot by a tenth of a Sharpe point, not by design.

On the T2-only gate the column does move the pick, MCAP/NEG → PXDVOL/NEG, and it buys **nothing**:
dSharpe_OOS **+0.0035**, and *both* picks beat SPY out of sample by ≈ +0.70. That is idea 628's
open question landing exactly where it predicted — PXDVOL is a price-LEVEL key (|IC| 0.5996) and
dating is not the only leak channel — so T2-only is dishonest with the column and without it.

Leak content (idea 623's `absIC_fwd`, reproduced at G5) ranks the four exog keys MCAP 0.7092 >
FULLSHRP 0.6104 > PXDVOL 0.5996 > … > MCAPREB 0.4405 > SHARES 0.3462: the keys the as-of column
decides are among the leakiest in the corpus.

## Predictions

P1 **HIT** · P2 **HIT** · P3 **HIT** · P4 **HIT** · P5 **MISS** (both gate forms — see above) ·
P6 **HIT**. Five of six.

## Proposed PROTOCOL wording (report-only; NOT applied)

> **10.** Every non-price input a script reads must publish an **as-of date** — a column in the
> file, or a stated constant in the script beside the read. An input with no as-of date is
> UNDATED, and any key built on it is treated as TERMINAL-DATED until it is dated: both the T1
> (scale) and T2 (dating) certificates are structurally blind to it, so no certificate result may
> be quoted for that key.

Cheapest first repair, by readership: `research/universe.json` (253 rule-8 readers) and
`research/universe_broad.json` (229) are two constants. `data/small_meta.csv` needs its
`max_1d_move` payload dated, not just its rows.

## Survivorship (PROTOCOL 9)

PART C runs on idea 195's SMALL430: current constituents of a sub-$2B screen
(`data/SMALL_PANEL_README.md`) intersected with the names that still file today, carrying idea
623's terminal-dated `max_1d_move` screen (kept to match the published convention; idea 627 priced
it at a median +0.0496 Sharpe in the other direction). A survivor of a survivor — every PART C
number is biased in the tilt's favour, so no level above is achievable. PARTS A, B and D do not
depend on the panel. The census counts readers by basename occurrence in committed `.py` sources
and will over-count a file whose name appears in a comment; the 12 rule-8 rows were read by eye.
