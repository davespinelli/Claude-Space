# Idea 523 — restate idea 276's 26-file UPPER BOUND on the headline block (lane B, 2026-09-11)

**VERDICT: ANSWERED / KILL of the 136 as an independent bound, and the 26 restates to 4.**
No RULES change, no book promoted, no PROTOCOL edit. `RULES.md`, `PROTOCOL.md`, `scan.py`,
`bot.py`, `baseline.py` untouched.

Script `2026-09-11_restate-idea-276-s-26-file-UPPER-BOUND-on-the-headline-block_B.py`.
Artefacts: `.console.txt`, `.grid.csv` (50 cells), `.survivors.csv`, `.panels.csv`,
`.arms.csv` (84 rows), `.bars.csv`, `.walkforward.csv` (100 cells).

## Selection note
Taken as the LAST eligible open idea in QUEUE.md. 353 is marked LOCAL ONLY (verifying it
needs a live `yf.download`); 429 is already PARKed for needing a volume cache the sandbox has
no network to build. The 2026-09-11 cloud run skipped 520/521/522/523 on the grounds that they
are "prose/gate censuses with no price leg and so cannot carry this run's mandatory rule-8
walk-forward and KEEP-path report". **That objection is answered here by construction**: the
census outcome is wired into the rule-8 CHOICE SET (the panels the surviving files name), so
the documentation decision is priced in OOS Sharpe/CAGR/MaxDD rather than asserted to be
irrelevant. The answer happens to be zero, which is a measurement, not an excuse.

## Parameters (2, as the queue allows) — all 25 points reported, twice
1. **WINDOW WIDTH** W ∈ {40, 70, 100, 140, 200} chars either side of the occurrence (70 = idea 286's).
2. **BLOCK RULE** B ∈ {TITLE, PRE-H2, FIRST-H2, CHARS1500, WHOLE} (PRE-H2 = idea 286's; WHOLE = idea 276's).

The **EXCLUSION reading** (LITERAL = the queue's own `breadth\d+` / 'breadth gate' wording;
GENERAL = the same instrument shapes over idea 276's whole vocabulary) is a pre-registered
*pair of readings* of every cell, not a third tuned parameter: both are reported at all 25
cells and neither is selected on. It barely matters — mean restated_26 7.32 (LITERAL) vs 7.12
(GENERAL) over the same 25 cells.

## GATE 0 — reproduction before any new number was read
| Gate | Result |
|---|---|
| G1 idea 276's three counts recomputed from source on its **frozen 292-file list**: cross **136** (published 136), cross&prop **26** (26), cross&breadth **14** (14), 0 missing files | **PASS, exact** |
| G2 idea 286's role audit on the 12 headline files, **row-for-row** against its committed `audit.csv` (file/pos/role/in_headline): **28** occurrences (published 28); HEADLINE-BREADTH files **1 of 12** (published 1), and the same file | **PASS, exact** |
| G2b idea 286's *concentration* statistic is a **VINTAGE** number, not an invariant: published **218/246 = 88.6%**, today **560/588 = 95.2%** (+342 `breadth` occurrences in the two append-only ledgers in 2 days) | **DRIFT, documented** — it drifts in the direction that strengthens idea 286 |
| G3 cost-rung identity r(10) = r(0) − turnover·10/1e4 on U56: max abs diff **0.000e+00** | **PASS** |
| G3b live RULES v2 on U56 @10bps reads **8.61% / 1.1998 / −12.05%** against idea 415 G2's committed **8.66% / 1.2056 / −12.05%** | **DRIFTED** (−0.0058 Sharpe, −5 bp CAGR; **MaxDD exact**). Not the start-date effect idea 518 logged — this run uses baseline's own `start=2008-01-01` as 415 did. It is the `prices.csv` vintage: the panel now ends **2026-09-10**, six sessions past 415's. Bears on ideas 514/517/519. |

## LEG A — what the two bounds become
- Panel-property **vocabulary** occurrences over the 136 files: **1,364** in **26** files (i.e. in
  exactly the 26 — see D1). Token mix: breadth 588, corr 236, dispersion 192, n_elig 149,
  disp 103, evol 86, pairwise correlation 7, eligible-set vol 3.
- **1,228 of 1,364 (90.0%)** sit in the two ledgers. Idea 286's concentration finding is not a
  breadth-only fact; it is **vocabulary-wide**.

| setting | restated 26 | of 26 | restated 136 | of 136 |
|---|---|---|---|---|
| **idea 286's own (W=70, PRE-H2, LITERAL)** | **4** | 15.4% | **4** | 2.9% |
| idea 276's own (block = WHOLE, W=70) | 20 | 76.9% | 20 | 14.7% |
| full 50-cell range | **2 → 20** (median 5.0) | 7.7–76.9% | **2 → 20** | 1.5–14.7% |

**The block rule is the whole story; the window is nearly inert.** Range of restated_26 over W
*within* each block rule: TITLE 2–2, PRE-H2 4–4, FIRST-H2 6–7, CHARS1500 4–5, WHOLE 17–20.
So a ±5× change in context width moves the bound by at most 3 files, while moving from the
record's headline convention to no-restriction-at-all moves it by 16.

The 4 survivors at idea 286's setting: `2026-09-04_asset-class-dispersion_B`,
`2026-09-06_dispersion-as-a-survivorship-detector_cloud`,
`2026-09-06_is-the-reversal-share-a-function-of-n-over-n_elig_C`,
`2026-09-06_where-selectivity-and-cost-cross_B`.

## LEG D — two structural findings
- **D1 (the KILL).** `restated_26 == restated_136` in **50 of 50** cells, and this is a theorem,
  not a coincidence: a file with no vocabulary hit has none to put in its headline, so the
  survivor set is a subset of the 26 by construction. **The 136-file cross-cap count carries no
  independent information as a bound on panel-property reach** — it counts capitalisation
  tokens, not claims. The 26 was always the binding column; the 136 should never again be
  quoted as a reach bound.
- **D2.** Of the 4 survivors, **2 are inside idea 286's frozen 14 and 2 are not** (both
  dispersion-sense). Idea 286's breadth-only audit **undercounts headline panel-property claims
  by 2 of 4**; the 26's wider vocabulary sees claims the 14 cannot.

## LEG C + rule 8 — the price leg
60 candidate arms (top-n n∈{5,10,20,30,50} and gated equal-weight band∈{0.00,0.03,0.05,0.08,0.12},
gross 0.75, weekly, t+1) × 3 panels × 2 cost rungs, plus RULES v2 / RULES v1 / SPY / EWALL
controls per cell.

- **PROTOCOL 4a: 2 / 60. PROTOCOL 4b: 1 / 60. BOTH: 0 / 60.**
- 4b sole-cut attribution at 10 bps: the **CAGR floor is the only failing bar for 14 of 30 arms**
  (fail-sets: CAGR 14, H1+H2+OOS+CAGR 7, H1+H2+OOS+DD+CAGR 6, H2+OOS+CAGR 2, NONE 1).
- The single 4b pass, **U56/topn30 @10bps**: CAGR 11.31% (floor 10.58%), Sharpe 1.1348,
  MaxDD −17.02% (cap −20.23%), H1/H2 1.1368/1.1400, **OOS 12.90% / 1.2228 / −17.02%**.
  It is **RUNG-FRAGILE** — at 25 bps the same book reads CAGR 10.27% against a 10.58% floor and
  fails — and **PROTOCOL 8 never reaches it**: the IS-Sharpe argmax on U56 is band0.08, and over
  all 100 rule-8 cells the pick is **B136/band0.08** every time. **Not a KEEP-candidate.**
- **Rule 8 (params on 2010–2016 only, 2017–2026 read once), 100 cells:**
  pick **B136/band0.08**, OOS CAGR **8.36%**, OOS Sharpe **1.1095**, OOS MaxDD **−14.81%**
  (25 bps rung: 8.15% / 1.0831 / −14.84%), against RULES v2 OOS **7.98% / 1.1185 / −12.24%**
  and SPY OOS **15.45% / 0.8820 / −33.72%**. Beats SPY OOS Sharpe **100/100**; beats RULES v2
  OOS Sharpe **50/100** (the 25 bps rung only, where the live book decays faster); beats the
  EWALL do-nothing control 50/100. It never beats SPY on CAGR.
- **D5 — book consequence of the restatement: ZERO.** All 100 cells draw the identical choice set
  (B136, SMALL439, U56) because even the 2-file TITLE survivor set names all three runnable
  panels, so the same arm is picked and the same OOS numbers read at every grid point. OOS
  Sharpe spread across cells 1.0831→1.1095 is the **cost rung**, not the census.

## Caveats
SURVIVORSHIP: U56 = `universe.json`, B136 = `universe_broad.json` (current constituents only),
SMALL439 = the sub-$2B screen with the 44 `max_1d_move ≥ 1.0` tickers dropped. Every small-cap
number is biased upward by an unknown amount and no cross-panel ordering here is
survivorship-clean. The census legs are frozen to idea 276's 292-file list; today's corpus is
larger and the two ledgers grow daily, so every occurrence count in this file is a
**2026-09-11 vintage** reading of a frozen file list, exactly as G2b documents. The price leg
reads 2010/2011–2026 only; 2020 and 2022 are the only real stress episodes in it.
Research, not investment advice.

## Reconciliation with the parallel cloud run of the same idea (added at push time)
A cloud run answered idea 523 independently the same day and published **26 → 1 and 14 → 1**
against this run's **26 → 4**. The two agree and are not in conflict; they restate different
things.
- **The 136.** The cloud run scores it on **cap-token SITE** (is the capitalisation token in the
  headline?) and gets a site-varying ladder **136 / 76 / 50 / 10**. This run scores it on
  **panel-property VOCABULARY** (is a property word in the headline?) and gets **4 in every one
  of 50 cells**, identical to its restated 26 by construction (LEG D1). Both readings reach the
  same conclusion: **the 26 and the 136 are not the same kind of number, and the 136 is not a
  claim count.** D1 is the stronger form of it — under a vocabulary reading the 136 *cannot*
  exceed the 26, so it carries no independent information at all.
- **The residual 1 vs 4.** It is the **block rule**, exactly the parameter this run found
  dominates: the cloud run's TITLE+VERDICT block is the tightest rung, and this run's TITLE block
  gives **2**, against 4 at PRE-H2 and 20 at WHOLE. Neither number is wrong; each is the bound at
  a stated block rule, which is precisely why idea 690 is queued.
- The cloud run's gate finding — idea 276's columns re-derive exactly **only once its own
  result.md is self-excluded**, because a globbing census counts itself — does not bear on G1
  here: this run scores the **frozen 292-file list as committed**, which already contains idea
  276's own output, so the self-inclusion is reproduced as published rather than corrected.
- Both runs report no KEEP (cloud 4a 0/3, 4b 0/3; this run 4a 2/60, 4b 1/60, BOTH 0/60).
