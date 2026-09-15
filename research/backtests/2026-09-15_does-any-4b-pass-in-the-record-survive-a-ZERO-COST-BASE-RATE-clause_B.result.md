# Idea 680 — does any 4b pass in the record survive a ZERO-COST BASE-RATE clause? (lane B)

**ANSWERED = ALMOST NONE AT 0 bps, ALL OF THEM AT 10 bps.** The queue's premise is
**CONFIRMED at zero cost and REFUTED at PROTOCOL's own cost rung**: at 0 bps only **1 of 7**
committed-key 4b passes sits outside its own gross-matched coin-flip null, but at 10 bps
**4 of 4** do and at 25 bps **2 of 2**. PROTOCOL rule 2's 10 bps already does the entire job a
base-rate clause would do, so the clause is **KILL as a new bar** — it changes no verdict the
protocol reaches, and as a rule-8 *chooser* it actively costs money. No book promoted, no
RULES change, no PROTOCOL edit applied (rule 6). `RULES.md`, `PROTOCOL.md`, `scan.py`,
`bot.py`, `baseline.py` untouched.

SELECTION: the LAST Open idea carrying a price leg. Everything below it in the queue (894–904,
869–877 and the 5xx/6xx census block) carries standing SKIP notes as prose/number censuses with
no book to price, so none can carry this lane's mandatory rule-8 walk-forward.

Script: `2026-09-15_does-any-4b-pass-in-the-record-survive-a-ZERO-COST-BASE-RATE-clause_B.py`
(1,259 s, seed base 680). Artifacts: `.census.csv` (1,118 rows), `.books.csv` (90),
`.nulls.csv` (270), `.draws.csv` (30,000), `.walkforward.csv` (27), `.console.txt`.

---

## PART A — the census: what "every committed 4b passer" actually is

4,433 committed `research/backtests/*.csv` scanned. **1,118 carry a 4b pass-flag column**
(`pass4b` / `p4b` / `keep4b` / `pass_4b` / `4b` / `oos4b` / `v4b` / `path4b` / `is4b`),
holding **1,215,158 rows of which 153,020 are committed 4b PASSES**. Classified by the
construction of the book each row names:

| class | pass rows | share |
|---|---|---|
| REAL-rule books | 68,559 | 44.8% |
| NULL-construction (`SHUFF`, `RAND*`, `PERM`, `PLACEBO`, `BLOCK`, …) | 6,608 | 4.3% |
| UNLABELLED — no book column, construction not recoverable from the CSV | 77,853 | 50.9% |

**Stated, not worked around: a full re-scoring of all 153,020 rows is not possible in this
sandbox and this run does not claim one.** Over half the ledger does not name its own book, and
the rows that do are CELLS (a book re-published in two files counts twice), not distinct books.
What PART B re-scores is the record's **modal REAL 4b-pass book keys** — `TOP20`/`top20`/
`CAND20` (16,483 pass rows), `EWALL`/`EWall`/`ewall` (12,655), plus `TOP10`, `TOP5` and
`BAND03` (RULES v2 itself) — rebuilt on their own panels at their own conventions, with G3/G3b
reproducing two of them against published triples. That is 30 (panel × claim set × book) cells,
not 153,020, and every headline below says so.

The 4.3% is a finding in its own right: **6,608 of the record's committed 4b PASS rows already
belong to books whose own key names them as nulls.** The ledger is not a list of rules that
cleared the bar.

## PART B — the price leg

Each book's null replaces its SELECTION with a coin flip and changes nothing else: on every
rebalance row the null holds the **same number of names at the same per-name weight**, drawn
uniformly from that family's pool (TOPk → the book's own candidate set; EWELIG/BAND03 → every
priced name). Gross, cash drag and de-grossing path are identical row by row —
**G5 gross match = 0.0000 on all 30 cells**, exact rather than approximate.

### The answer, by cost rung (1,000 draws, both claim sets pooled — 30 cells)

| cost | committed-key 4b passes | outside their null (base rate ≤ 0.05) | survive rate |
|---|---|---|---|
| **0 bps** (the queue's object) | 7 of 30 | **1** | **14.3%** |
| 10 bps (PROTOCOL rule 2) | 4 of 30 | **4** | **100%** |
| 25 bps (stress) | 2 of 30 | **2** | **100%** |

The seven zero-cost passers' own null base rates: **0.2%, 9.3%, 53.4%, 74.8%, 81.4%, 98.0%,
100.0%**. The single survivor is `B136/CORE/EWELIG` at 0.2%.

### The inversion — at zero cost, passing 4b PREDICTS a higher null base rate

Over the 30 cells at 0 bps, mean null base rate is **0.5959 for the 4b passers against 0.0733
for the failers**, Spearman ρ(pass, base rate) = **+0.6387**. The two books with the *highest*
base rates in the whole run — `U56/EXT/BAND03` at **98.0%** and `B136/EXT/BAND03` at **100.0%**
— are both 4b **passers**. At 10 bps the sign flips to **−0.1048** and the association is gone.
That is the queue's suspicion in its strongest form: **at zero cost the 4b bar ranks books by
how easy their family is, not by whether their rule works.**

### The whole effect is a zero-cost artefact

Null base rate across the same 30 cells, 0 → 10 bps: mean **0.1953 → 0.0004**, max
**1.0000 → 0.0100**, cells above 0.05 **12 → 0**, cells above 0.50 **6 → 0**. Ten basis points
of turnover cost removes every coin flip from the pass set. The standing 2026-09-04 KEEP
candidate, `U56/CORE/TOP20`, is the clean case: base rate **74.8% at 0 bps → 0.0% at 10 bps**,
and it passes 4b at both rungs. Its 74.8% independently reproduces **idea 502's 78.1%** on a
different, exactly gross-matched null construction, so 502's number is not an artefact of its
own null — but 502's *implication* for the live book does not survive the cost rung.

### It is a LARGE-CAP problem only

Cells with a zero-cost base rate above 0.05: **U56 8 of 10** (max 0.980), **B136 4 of 10**
(max 1.000), **SMALL439 0 of 10** (max **0.000**). On the small panel no coin flip clears 4b at
any cost, because the bar is against SPY and the panel does not reach it.

### The null's ROTATION convention moves the number more than the cost rung does

`U56/TOP20/CORE` at 0 bps: **RANDROT 74.8%** vs **RANDFIX 0.2%** — a fixed random 20-name list
held through the same gate essentially never clears 4b, while a list re-drawn weekly usually
does. At gross 1.00 the same pair reads 28.7% vs 28.0%. **A "coin-flip base rate" is therefore
not one number**; it is a function of how much the null is allowed to rotate, and any clause
written around one would have to name its null. Reported here rather than buried, and RANDFIX
is never mixed into a headline.

## RULE 8 — walk-forward, parameters chosen on 2009–2016 only, 2017–2026 read once

Three IS-only choosers over the 10 books on each panel × 3 cost rungs = 27 cells, **21 live
picks (6 IS sets EMPTY)**. Totals: **4b 7 of 21, 4a 0 of 21.**

| chooser | OOS 4b | mean OOS Sharpe | mean OOS CAGR |
|---|---|---|---|
| CH_SHARPE (best IS Sharpe, no clause) | 3 / 9 | 0.948 | 10.27% |
| CH_4bIS (best IS Sharpe among IS 4b-level passers) | 2 / 3 | 1.160 | 12.23% |
| **CH_BASE (the clause: IS base rate ≤ 0.05, then best IS Sharpe)** | **2 / 9** | **0.948** | **9.77%** |

**CH_BASE is inert where it matters and harmful where it bites.** At 10 and 25 bps it picks
*identically* to CH_SHARPE on all three panels — the clause buys nothing, because the cost rung
has already emptied the null. It differs only at 0 bps, and there it makes things worse: on U56
it steers from `EXT/BAND03` (OOS **12.95% / 1.301 / −15.88%**, 4b PASS) to `CORE/BAND03`
(OOS **9.66% / 1.302 / −12.03%**, 4b **fail**) — **−3.29 pp of OOS CAGR and a lost 4b pass**,
bought with a clause whose only job was to be conservative. CH_BASE's IS base rate is computed
on the 2009–2016 window's own 4b level legs; the full-sample base rate reads the OOS window and
is never used to choose.

Best OOS cells, both already-known books and neither newly promoted:

| pick | rung | OOS CAGR / Sharpe / MaxDD | 4b | 4a |
|---|---|---|---|---|
| U56 `CORE/TOP20` (CH_4bIS) | 0 bps | **15.34% / 1.240 / −18.22%** | PASS | fail |
| U56 `EXT/BAND03` (CH_SHARPE ≡ CH_BASE) | **10 bps** | **12.68% / 1.277 / −15.91%** | PASS | fail |

Same OOS window, comparands: **SPY 15.27% / 0.874 / −33.72%** (U56 tape; 15.33% / 0.877 /
−33.72% on B136/SMALL), **RULES v2 (live) 9.46% / 1.277 / −12.05%** (U56), 7.88% / 1.106 /
−12.24% (B136), 3.75% / 0.560 / −13.89% (SMALL439). `EXT/BAND03` is the live band book at gross
1.00 — a known book at a known gross, consistent with idea 919's `U56/BAND03_M` g = 1.000
reading of 12.8% / 1.23 / −18.8%. **4a is 0 of 21**: nothing here beats the live book's
drawdown, which is exactly why PROTOCOL 4b exists.

## GATES — 9 of 9 PASS

`G1` ctx.run ≡ `engine.backtest` @10 bps **8.674e-18** · `G2` band_book(0.03, 0.75) ≡
`rules_v2_weights` **0.000e+00** · `G3` the 2026-09-04 KEEP-4b incumbent re-derived on U56:
got **12.60% / 1.0881 / −18.31%** vs published 12.66% / 1.0921 / −18.31%, max|Δ| **3.958e-03**
(under the 5e-3 vintage bar) · `G3b` RECOMMENDATION Finding 2's EWELIG: got **10.36% / 1.045 /
halves 1.07/1.02** vs published 10.4% / 1.05 / 1.07/1.03, max|Δ| **7.581e-03** · `G4` panel
triples printed · `G5` gross match **0.0000** worst over all 30 cells · `G6` determinism
**0.000e+00** · `G7` SMALL439 screen: 52 tickers with `max_1d_move ≥ 1.0` dropped · `G8` census
self-check on 60 files by an independent pandas path: **0 disagreements** · `G9` nesting: the
250/500 base rates are exact prefixes of the same 1,000 draw streams.

**A naming correction the record should carry:** the panel the record calls `SMALL439` is
**663 names + SPY** on today's cache after the `max_1d_move` screen, not 439. The label is
vintage; the count is printed by G7 in every run.

## SURVIVORSHIP (PROTOCOL 9)

`universe.json`, `universe_broad.json` and the SMALL screen are current-constituent lists, so
every CAGR and drawdown LEVEL above is optimistic. The direction here is specific and works
against the incumbents, not for them: a coin flip drawn from a survivor panel is a **better**
book than one drawn in real time, so **every null base rate above is an UPPER bound** and every
book's percentile inside its null a **lower** bound. The 4b bar is against SPY, which is not
survivorship-inflated, so the 4b LEVELS are not protected by the usual same-tape argument; the
base rates, the 0 → 10 bps collapse and the RANDROT/RANDFIX contrast are same-tape comparisons
and are unaffected.

## WHAT THIS MEANS FOR CAPITAL

Nothing changes in the live book. The one operational consequence is a reporting line, proposed
in the memo and **not applied** (rule 6): a 4b pass quoted at 0 bps is not evidence about a
rule, and the record should stop quoting one without its null beside it. At 10 bps — the only
rung PROTOCOL actually sanctions — the record's 4b passes are already rare under their own
nulls, and the standing candidate is one of them.

Follow-ups filed: 924 (re-score the 77,853 UNLABELLED committed 4b pass rows by recovering each
book's construction from its own SCRIPT, as idea 876 did for placebo files), 925 (is the
RANDROT/RANDFIX base-rate gap a TURNOVER fact — the rotating null's edge at 0 bps is exactly
what 10 bps removes), 926 (does the zero-cost pass↔base-rate inversion hold on the record's
MONTHLY-cadence 4b passes, where turnover is a third of the weekly books').
