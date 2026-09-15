# Idea 912 (cloud, 2026-09-15) — is the record's whole DD-LEG literature a 2020 CONTAINMENT fact?

**ANSWERED = YES for the AGREEMENT literature, NO for the LEG itself, and the ranking INVERTS.
Excise 2020 and every one of 867's and 910's beta-equivalence headlines breaks (4 of 4, at all
four excision windows, 16 of 52 claim-cells survive overall) — while the DD leg's own pass set
barely moves (max flip share 0.161) and the full-sample 4b census holds. The inversion is the
finding: with 2020 in, the CIRCULAR DDWIN beats the ex-ante FULL beta by +0.126 on B136; with
2020 out, the ex-ante FULL beta beats DDWIN by +0.098, and β\* moves from 0.44 onto PROTOCOL's
own 0.60. KILL for the premise as stated — the 2020 artefact is in the beta story, not in the
leg — and one live consequence: the record's only rule-8-reachable 4b pass loses its DD leg at
every excision.**

No RULES change, no book promoted, no PROTOCOL edit applied (rule 6). `RULES.md`, `PROTOCOL.md`,
`scan.py`, `bot.py` and `baseline.py` untouched. No memo written — nothing reached a KEEP path.

**SELECTION.** First eligible Open idea in QUEUE.md (this run's claim rule). Price-only: no EDGAR
/ Form 4 / 8-K / options / spin-off / live-data content, so eligible for the cloud sandbox.

## What was asked, and what "excised" means

Idea 910 measured that **92.9% of U56 and 89.3% of B136 books have their entire peak-to-trough
decline contained inside SPY's own 24-day 2020 window** (median Jaccard 0.854 / 0.708), against
**0.0% on SMALL**. The queue's charge: re-run 867's and 910's agreement tables with 2020 excised
and report which survive.

**Convention, fixed before any number was read.** An excision deletes the episode's days from the
*statistic*, not from the tape. Every book trades, rebalances and pays 10 bps weekly at t+1 on the
full price history, exactly as in 867 and 910; the excised days are then dropped from the daily
net-return vector before CAGR / Sharpe / MaxDD / every beta — for the books, for SPY and for RULES
v2 alike. Re-simulating a world without 2020 would move every rebalance date and stop the two
tables being comparable. Two consequences are stated, not hidden: **MaxDD is read on a spliced
equity curve**, and the 252d rolling / EWMA betas straddle the splice. 2020 lies entirely in the
OOS half, so **the IS half is invariant to every excision (gate G9, exact 0)** — which is what
makes the IS-only rule-8 chooser identical across levels and every OOS move attributable to the
episode.

**TUNED 1** excision window, 5 levels, all reported: `NONE` (control) · `SPYDD` = SPY's own argmin
peak-to-trough, measured at **2020-02-19 .. 2020-03-23, 24 days** on all three panels, i.e. 910's
own window · `CRASH` 2020-02-19..2020-04-30 (51d) · `H1_20` 2020-01-01..2020-06-30 (125d) ·
`CAL20` the whole calendar year (253d). **TUNED 2** panel {U56, B136, SMALL}. Reported axes: 4
families × 3 modes × 3 thetas × 4 gross rungs = **112 real books** + ZEROSIG + RANDGATE×3 = 128
traded books per panel, × 3 windows × 11 proxies × 2 populations. Every grid point is in
`.books.csv` / `.agree.csv` / `.barA.csv` / `.containment.csv` / `.legflips.csv` / `.survival.csv`
/ `.walkforward.csv`.

## GATES 9 of 9 PASS — including exact cross-run reproduction of both tables

| gate | what | result |
|---|---|---|
| G1 | TREND/ROW g=0.75 ≡ `baseline.rules_v2_weights` | max\|Δw\| **0.000e+00** |
| G2 | fast `Book.at` ≡ `engine.backtest` | max\|Δr\| **1.041e-17**, max\|Δturn\| 2.429e-16 |
| G3 | committed U56 triples @ NONE | SPY 15.13%/0.8845/−33.72%, RULES v2 8.62%/1.2013/−12.05% |
| **G4** | **867's committed `.agree.csv`** | **12 of 12 rows reproduce, worst \|Δagree\| 1.11e-16** |
| **G5** | **910's committed `.agree.csv`** | **66 of 66 (panel × popn × proxy) cells reproduce on agree / best_agree / n / n_disagree, worst \|Δ\| 1.11e-16** |
| **G6** | **910's committed `.overlap.csv`** | **9 of 9 cells, \|Δcontained\| 0.000e+00, \|Δ median Jaccard\| 1.39e-17** |
| G7 | determinism (rebuild U56) | 0.000e+00 on Sharpe and β_ROLL |
| G8 | analytic ray, **at every excision**: β of `g × SPY` must read g | max\|β−g\| **1.56e-02** over 5×4×11 |
| G9 | IS-window invariance (no excision touches 2009–2016) | **0.000e+00** over 16 statistics × 4 excisions |

**SMALL panel caveat, declared.** 867 and 910 built SMALL from `load_universe(small=True)` *without*
the `max_1d_move ≥ 1.0` drop. This lane drops those 52 tickers first, so a fourth panel
**SMALLRAW** (undropped, 716 cols) was built for G4/G5/G6 only — the gates are therefore read on
the construction the numbers were published on, and every headline below is on the dropped panel
(664 cols).

## H_STRUCT — containment is a 2020 fact, decisively. NOT a market-episode fact.

With 2020 excised, SPY's worst decline on all three panels becomes **2022-01-03 .. 2022-10-12, 196
days, −24.50%** (from −33.72% over 24 days). Containment does **not** reappear around it:

| panel | NONE | SPYDD | CRASH | H1_20 | CAL20 | bar 0.70 |
|---|---|---|---|---|---|---|
| U56 | **0.929** | 0.143 | 0.143 | 0.143 | 0.143 | 0 of 4 |
| B136 | **0.893** | 0.250 | 0.250 | 0.250 | 0.214 | 0 of 4 |
| SMALL | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | — |

A 24-day crash swallows a book's whole decline; a 196-day grind does not. Note the two statistics
come apart: on U56 median Jaccard stays high (0.854 → **0.757**) while containment collapses
0.929 → 0.143 — the windows still overlap heavily, they are no longer *nested*. On B136 median
Jaccard goes to **0.000**.

## H_AGREE — 4 of 4 committed agreement headlines BREAK; 16 of 52 claim-cells survive

Each claim re-read against **its own committed bar**, at every excision (`.survival.csv`; control
column reproduces 13 of 13, which is G4/G5/G6 restated per claim):

| committed claim | NONE | SPYDD | CRASH | H1_20 | CAL20 |
|---|---|---|---|---|---|
| K1 DDWIN reaches 0.95 on U56 (0.9531) | ✔ | **breaks** | **breaks** | **breaks** | **breaks** |
| K2 DDWIN reaches 0.95 on B136 (0.9833) | ✔ | **breaks** | **breaks** | **breaks** | **breaks** |
| K2b DDWIN B136 has 0 disagreeing pairs | ✔ | **breaks** | **breaks** | **breaks** | **breaks** |
| K3 U56/ROLL clears BAR-A (0.9844) | ✔ | **breaks** | **breaks** | **breaks** | **breaks** |
| K4 B136/SPYDD clears BAR-A (1.0000) | ✔ | **breaks** | **breaks** | **breaks** | **breaks** |
| K5 \|ρ(β_FULL, MaxDD)\| ∈ [0.69,0.97], U56 / B136 | ✔ | ✔ | ✔ | ✔ | ✔ |
| K6 ex-ante agreement still < 1.0 (not a beta cap) | ✔ | ✔ | ✔ | ✔ | ✔ |
| K7 H0 decomposition: POPULATION < 0, ESTIMATOR > 0 (U56, B136) | ✔ | **breaks** | **breaks** | **breaks** | **breaks** |
| K8 containment 0.929 / 0.893 (U56, B136) | ✔ | **breaks** | **breaks** | **breaks** | **breaks** |
| K8 containment 0.000 (SMALL) | ✔ | ✔ | ✔ | ✔ | ✔ |

**BAR-A goes from 2 of 30 to 0 of 30 at every excision level.** 910's positive result — two ex-ante
proxies matching the circular ceiling exactly — exists only with 2020 in the sample.

**The DDSUB population is itself a 2020 artefact, and this is why K7 dies.** DDWIN is undefined
when a book's peak-to-trough is under 20 days, which is what produced 867's n = **64 / 60** against
112. Excise 2020 and DDWIN is defined on **112 of 112 on every panel at every excision** — the
short-window population *was* the 24-day crash. With DDSUB ≡ ALL there is no population gap left
to decompose, so 910's POPULATION/ESTIMATOR split has no referent.

### The inversion (the run's strongest number)

ALL-112 population, FULL window, fixed cap β ≤ 0.60:

| panel | proxy | NONE | SPYDD | CRASH | H1_20 | CAL20 |
|---|---|---|---|---|---|---|
| B136 | **FULL** (ex ante) | 0.8571 | **0.9732** | 0.9554 | 0.9464 | 0.9375 |
| B136 | **SEMI** (ex ante) | 0.8750 | **0.9821** | 0.9554 | 0.9554 | 0.9554 |
| B136 | DDWIN (circular) | **0.9833** (n=60) | 0.8750 | 0.8750 | 0.8750 | 0.8661 |
| U56 | FULL (ex ante) | 0.9018 | 0.8929 | 0.8929 | 0.8929 | 0.8929 |
| U56 | DDWIN (circular) | **0.9531** (n=64) | 0.8482 | 0.8482 | 0.8482 | 0.8482 |

With 2020 in, the circular DDWIN beats the ex-ante FULL by **+0.126** on B136 and **+0.051** on
U56 — 867's entire "only one estimator reaches the bar, and it is the circular one" finding. With
2020 out, **the ex-ante FULL beta beats DDWIN by +0.098 on B136 and +0.045 on U56**. The DD leg is
*more* beta-like once the episode is removed, not less. And the best-fitting cap moves onto the
protocol's: B136 β\* **0.4366 → 0.6104**, against PROTOCOL 4b's declared 0.60.

**K6 survives everywhere and it matters:** the best B136 cell is 0.9732 with **18 of 335 matched
pairs still disagreeing** and up to **7.09 pp** of MaxDD inside a matched pair, so the DD leg is
still not a beta cap even at its most beta-like. K5 strengthens (B136 ρ −0.9502 → **−0.9645**).

## H_LEG / H_4b — the LEG survives. This is the half of the queue's hypothesis that is wrong.

Every real book, nothing selected, FULL window: the DD leg's pass set flips on **16 of 112 (U56),
18 of 112 (B136), 15–16 of 112 (SMALL)** books — max flip share **0.161** against a 0.50 bar,
**0 of 12 cells above it**. The 4b census barely moves: U56 **9 → 7–9**, B136 **10 → 10–13**,
SMALL **0 → 0** of 112. The record's published DD-leg *verdicts* are not one episode read 112
times; its published DD-leg *beta equivalences* are.

## H_WF / RULE 8 — and one live consequence

IS-only choosers on 2009–2016 (identical across excisions by G9), OOS 2017–2026 read once, 10 bps,
t+1, weekly, both KEEP paths, 15 picks per excision (`.walkforward.csv`):

| excision | 4a | 4b | book passing 4b |
|---|---|---|---|
| NONE | 0 of 15 | **1 of 15** | B136 `IS_DDCAP` → TREND/AGG/θ=0.20/g=0.75 |
| SPYDD | 1 of 15 | **0 of 15** | — |
| CRASH | 1 of 15 | **0 of 15** | — |
| H1_20 | 1 of 15 | **0 of 15** | — |
| CAL20 | 1 of 15 | **0 of 15** | — |

That single pass is the record's own standing candidate — idea 910's `b136-trend-agg-th020-g075`,
the 0.70 pp DD margin idea 914 was filed to price. **It fails at every excision on the DD leg
alone** (`leg_H1` and `leg_H2` stay True throughout): SPY's OOS MaxDD shallows −33.72% → −24.50%,
tightening the 0.60 cap from −20.23% to **−14.70%**, while the book's own MaxDD shallows only
−19.53% → **−17.73%**. The de-grossed book sat out a 24-day crash; it participates in a 196-day
grind. The margin is a 2020 margin.

OOS comparands, same window and same excision — SPY **15.33% / 0.877 / −33.72%** (NONE) →
**20.51% / 1.213 / −24.50%** (SPYDD), **17.43% / 1.102** (CRASH), **16.64% / 1.070** (H1_20),
**15.00% / 0.981** (CAL20); RULES v2 (live) on B136 **7.88% / 1.106 / −12.24%** → 9.21% / 1.347 /
−9.28% (SPYDD) → 7.82% / 1.188 (CAL20). Full-window comparands are in the console log. The 4a
column moving the other way (U56 2→6, B136 5→20, SMALL 0→19 OOS) is the mirror image: RULES v2's
own drawdown shallows less than the books' do, so the 4a MaxDD leg loosens.

## Verdict

**KILL for the premise as the queue stated it, with the scope corrected.** "Every DD-leg result on
the large-cap panels may be one episode read 112 times" is **true of the beta-equivalence
literature** — K1–K4, K7, K8 all break at all four excision windows, BAR-A empties, the DDSUB
population turns out to be the crash itself, and the estimator ranking reverses — and **false of
the DD leg's own verdicts**, which move on 16–18 books in 112 and keep their 4b census. Nothing is
promoted; the one rule-8 4b pass in the run is an already-committed book that loses its DD leg
whenever 2020 is removed, which is evidence against promoting it, not for.

Follow-ups filed: 915 (does any committed 4b DD margin survive the 2022-bar), 916 (re-read the
record's beta-equivalence claims against the post-2020 β\* = 0.61), 917 (is the 20-day DDWIN
definition floor a crash-length convention).

## Survivorship

U56 / B136 / SMALL are current-constituent lists (SMALL additionally drops the 52 tickers with
`max_1d_move ≥ 1.0` per `data/small_meta.csv`; SMALLRAW, used for gates only, keeps them), so every
CAGR and drawdown **level** above is optimistic — the books' and the comparands' alike. The
agreement tables, the flip counts, the containment shares and the excised-minus-control contrasts
are same-tape statistics and are unaffected.
