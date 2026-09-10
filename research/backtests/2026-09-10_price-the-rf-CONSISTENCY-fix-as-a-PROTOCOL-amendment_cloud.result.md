# Idea 641 — price the rf-CONSISTENCY fix as a PROTOCOL amendment (cloud, 2026-09-10)

**ANSWERED. The amendment is drafted and priced. The 4b column of the record CARRIES ACROSS;
the 4a column and every rule-8 SELECTION do not. No KEEP, no RULES change, no PROTOCOL edit —
`RULES.md`, `PROTOCOL.md`, `scan.py`, `bot.py`, `baseline.py` untouched by this run.**

Script: `research/backtests/2026-09-10_price-the-rf-CONSISTENCY-fix-as-a-PROTOCOL-amendment_cloud.py`
Artefacts: `.txt` (full log), `.corpus.csv` (100 rows, PART B), `.census.csv` (2,905 files, PART C),
`.wf.csv` (160 rule-8 grid points, PART D).

Two tuned parameters as the queue allows: **RATE** ∈ {0, 150, 300} bps × **CORPUS** ∈ {MEMO, RECORD}.
Every grid point reported. 10 bps headline, 25 bps also reported; next-day execution; no shorting,
no leverage.

Three treatments — the object under test, not dials:

| | cash leg | rf in `metrics` | what it is |
|---|---|---|---|
| **C0** | 0 | 0 | the record's standing convention: every published verdict used this |
| **C1@c** | c | 0 | idea 641's literal ask, the "credit rate" line alone |
| **C2@c** | c | c | the internally consistent amendment, both lines |

---

## GATES — five, pre-registered, all pass

* **G1** `run_cash(c=0)` vs `engine.backtest` on RULES v2 U56: returns **2.572e-16**, turnover
  **0.000e+00** (bar 1e-12). 2 head rows excluded — `engine.backtest`'s own `w_target.shift(1)`
  NaN, present in every run in the record.
* **G2** RULES v2 U56 @10 bps **8.66% / 1.2056 / −12.05%** vs committed 8.63% / 1.202 / −12.05%.
  `data/prices.csv` is re-downloaded daily with auto-adjusted closes, so u56 rows in this record
  reproduce to **~3e-3, not bit-exact** (idea 406's finding, re-confirmed).
* **G3** memo-headline reproduction, **8 of 8 gated books pass** (bar |ΔSharpe| ≤ 0.02):
  K1 −0.0005, K3 +0.0177, **K4 +0.0000**, **K5 −0.0001**, **K6 −0.0000**, K7 −0.0011, K8 +0.0057.
  Two memo wordings had to be read literally to reproduce at all, and that is itself a finding:
  K4's "EW-all at 100% gross" is `band=0` **de-grossed**, not respread (respreading gives
  16.90%/1.1595, 4.9 pp of CAGR too much); K6's "0.75/k over IN names" **is** respread
  (de-grossing gives 8.72%/1.1515, 5.3 pp too little). K3 needs the fixed 3.75%-per-name wording
  (gross/k gives −16.69% MaxDD against the published −12.37%).
* **G4** vol recovered from (Sharpe, CAGR) via `vol = S − sqrt(S² − 2·CAGR)` vs true vol on the
  corpus: max |err| **0.0083**, median 0.0060. A declared TOLERANCE, not an assert — PART C is
  explicitly first-order.
* **G5** first-order credit `(1−ḡ)·c` vs exact re-simulation at 300 bps: the first-order form
  **understates** the credit by 0.0–13.1 bps of CAGR (compounding), so PART C is conservative in
  the C1 direction.

---

## PART A — the amendment (DRAFT; rule 6 says PROTOCOL changes at Sunday review, not in a run)

> **10. Cash and the risk-free rate (one convention, three lines).**
> (a) Un-invested NAV earns the credit rate **c** inside the drift renormalisation, so a book at
> gross g earns (1−g)·c per year on its cash leg;
> (b) every Sharpe and Sortino **in the same comparison** is computed at **rf = c**, including
> SPY's and the live book's — `engine.metrics(r, rf=c)`, never rf=0 beside a credited book;
> (c) **c is one number fixed for the whole record** and stated in every memo; a run may not
> choose it. Changing c re-prices EVERY committed verdict and is a PROTOCOL amendment, not a
> run-level dial.

Lines (a) and (b) are **inseparable**: (a) without (b) pays a risk-free return and then measures
it as excess return. That is what PART B and PART D price.

---

## PART B — the MEMO corpus, re-simulated exactly (10 books × 2 rungs × 5 treatments = 100 rows)

The corpus is **every KEEP-candidate the record filed a memo for that is reconstructible from
prices alone**, plus the two live books as comparands: K1 u56 top20 g0.75 W; K2 the same + rank
buffer m=20; K3 u56 top20 DAILY + buffer m=50; K4 u56 EW-all MA-gate g1.00 monthly; K5 RULES v2
gate at g1.00 weekly; K6 idea 360's b=0.12 respread band; K7 b136 ewall g0.375 with the residual
in SHY (the record's only 4a candidate here); K8 the 2026-09-10 breadth-gate candidate;
LIVE = RULES v2; V1 = RULES v1.

**(1) The 4b column carries across.** At the PROTOCOL rung (10 bps) **4b passes 7 of 10 books
under ALL FIVE treatments — the same seven every time.** Over both rungs the 4b verdict is
identical under all five treatments in **16 of 20 (book × rung) cells**. The three that move are
all at 25 bps and all at the edge: K1 (fails C0, passes under C1 at both rates, fails again under
C2), K8 (passes C0/C1/C2@150, fails C2@300), K7 (immaterial, 4b-failing throughout).

**(2) The 4a column does NOT carry across, and it is destroyed rather than moved.** The corpus'
single 4a pass — K7 at 10 bps, the SHY-residual book — **fails under all four amended treatments**,
so 4a goes **1/10 → 0/10** at the protocol rung. K7 holds **zero cash** (the residual is in SHY),
so C1 does nothing to its own returns and everything to the RULES v2 book it is judged against:
RULES v2 holds **46.7% cash** and its Sharpe rises 1.2056 → **1.4032** at C1@300, more than any
candidate's. This is idea 406's 45→56/59 (C1) and 45→23/18 (C2) result reproduced on the memo
corpus with a sample size of one: **4a is a comparison against the cashiest book in the record,
so any convention that pays cash re-prices the bar harder than the candidate.**

**(3) The two lines move Sharpe in opposite directions, and the gap is large.** Median over the
20 cells: **C1@300 − C0 = +0.0702 of Sharpe; C2@300 − C0 = −0.2199.** The queue's literal fix
flatters every de-grossed book; the consistent fix docks every book with any exposure by
`g·c/vol`. The **binding 4b bar** shifts with it — CAGR-floor 14 / DD 3 / H1 3 / H2 0 at C0,
against CAGR 10 / DD 4 / H1 4 / **H2 2** at C2@300: under the consistent amendment the Sharpe legs
start binding, which is exactly the failure mode idea 406 flagged.

**(4) The live book is unchanged in verdict.** RULES v2's 4b CAGR-floor deficit closes from
**−200 bps (C0) to −47 bps (C1@300)** and **still fails**, on both rungs and all five treatments —
idea 406's −198 → −44 bps, independently reproduced on a different corpus.

---

## PART C — the RECORD corpus, first-order (327,971 rows across 461 committed files)

2,905 committed CSVs scanned in 24 s; **461 publish (Sharpe, CAGR, MaxDD, gross) in one row**
(2,435 lack one of the four columns — that alone is a limit on how much of the record can be
re-priced at all). 352,131 book-rows, mean gross 0.661 (mean cash 0.339), 87.9% de-grossed,
1.3% levered; 327,971 survive the vol-recovery domain check, median recovered vol 0.110.

| rate | median ΔS (C1) | median ΔS (C2) | \|ΔS\|>0.05 (C1) | \|ΔS\|>0.05 (C2) | Sharpe-bar flips C1 | Sharpe-bar flips C2 | CAGR-floor flips |
|---|---|---|---|---|---|---|---|
| 150 bps | **+0.0361** | **−0.0913** | 36.2% | **97.2%** | 5.63% | **11.28%** | 3.35% |
| 300 bps | **+0.0722** | **−0.1827** | 73.5% | **99.9%** | 10.27% | **30.91%** | 7.15% |

**The consistent amendment is 2.5× the size of the queue's fix and points the other way** — the
credit is worth `(1−g)·c` and the rf charge is worth `c`, so the net is `−g·c`, and the record is
87.9% de-grossed but only 33.9% cash. At 300 bps the consistent amendment moves **99.9%** of the
record's published Sharpe column by more than 0.05.

*Limits:* first-order (conservative on the C1 leg per G5); `vol_hat` carries a ~0.006–0.008
tolerance (G4); the full-sample Sharpe-vs-SPY comparison used here is **not** a 4b leg (4b reads
halves + OOS), so these are **size** statistics for the record's Sharpe column, not verdict counts
— PART B counts verdicts exactly. Panel is inferred from the filename, default U56.

---

## PART D — rule 8: the dial chosen on ≤2016 under each treatment, 2017– read exactly once

Three dial families on U56 @10 bps, all 160 grid points in `.wf.csv`.

| family | C0 pick | C1@150 | C1@300 | C2@150 | C2@300 |
|---|---|---|---|---|---|
| BAND3 (gross × cadence) | (1.00, M) | **(0.50, W)** | **(0.50, W)** | (1.00, M) | (1.00, M) |
| MAGATE (gross × cadence) | (1.00, M) | **(0.50, M)** | **(0.50, M)** | (1.00, M) | (1.00, M) |
| TOPN (n × gross) | (20, 0.75) | **(50, 0.50)** | **(50, 0.50)** | (20, 0.75) | **(20, 1.00)** |

**THE SELECTION IS WHERE THE QUEUE'S FIX BREAKS.** Under **C1 the IS pick changes in 6 of 6
(family × rate) cells and every single move is toward LESS exposure** — gross 1.00 → 0.50, n 20 →
50 — because paying cash while measuring excess return at rf = 0 makes **holding cash look like
alpha**, and an IS-Sharpe selector buys as much of it as the grid allows. Under **C2 the pick
changes in 1 of 6** and that one move is toward *more* gross. 7 of 12 cells overall.

Out of sample the picks beat **SPY 15 of 15** and **RULES v2 2 of 15** — and the two wins are both
C1 cells, i.e. they are the artefact, not a result: BAND3 C1@150/@300 pick (0.50, W), OOS Sharpe
1.4839/1.6821 on **7.35%/8.39% OOS CAGR** against RULES v2's own credited 1.3804/1.4756. A book
that earns 3% on half its NAV and is then graded against a zero risk-free rate is not a strategy.

---

## The answer to the queue's question

**Is ANY published verdict safe to carry across? Yes — but only the 4b ones, and only as
verdicts, never as selections.**

1. **4b KEEP/KILL verdicts carry.** 7/10 books pass 4b identically under all five treatments at
   10 bps; 16/20 cells over both rungs. The record's published 4b passes are **not near their
   bars** (idea 406 found the same: 0 flips in both committed `keeppaths.csv`), so a change of
   cash convention does not reach them. The exceptions are the 25-bps edge cases (K1, K8), which
   were already the corpus' thinnest margins.
2. **4a verdicts do not carry.** 1/10 → 0/10. 4a is a comparison against RULES v2, which holds
   46.7% cash — more than every candidate in the corpus — so any credit convention re-prices the
   **bar** harder than the book. **No published 4a verdict should be carried across an adopted
   credit rate without being re-run.**
3. **No rule-8 pick carries under line (a) alone.** 6/6 cells change, always toward cash. This is
   the concrete, quantified reason the amendment must be adopted as **(a) AND (b) together or not
   at all** — which is what PART A's draft says and what idea 406 suspected without pricing it.
4. **A third of the record cannot be re-priced at all**: 2,435 of 2,905 committed CSVs do not
   publish a gross column beside their Sharpe, so their rows have no recoverable cash leg. Line
   (c) of the draft (one fixed c, stated in every memo) is worth less than a fourth line the
   record actually needs: **publish realised gross beside every published Sharpe.**

**Recommendation: do not adopt this week.** The amendment as drafted is correct but its cost is
that every 4a verdict and every rule-8 pick in the record becomes unreadable, and idea 642's
objection stands unpriced — a **flat** c over 2009–2026 is wrong in both directions (T-bills ~10 bps
to 2015, ~500 after 2022), so the credit is backloaded onto exactly the OOS window rule 8 reads.
Idea 642 (a real T-bill path) must land before any c is fixed.

**SURVIVORSHIP:** U56 and B136 are current-constituent lists, so every level here is optimistic;
only the *differences between treatments* are this run's object, and those are within-panel.
