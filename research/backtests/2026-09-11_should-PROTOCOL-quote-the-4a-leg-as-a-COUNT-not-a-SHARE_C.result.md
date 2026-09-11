# Idea 727 — should PROTOCOL quote the 4a leg as a COUNT, not a SHARE?

**Lane:** C · **Date:** 2026-09-11 · **Script:**
`2026-09-11_should-PROTOCOL-quote-the-4a-leg-as-a-COUNT-not-a-SHARE_C.py`

**Verdict: ANSWERED / KILL OF THE PROPOSED FIX, AND THE PROBLEM IT WAS MEANT TO FIX IS WORSE
THAN IDEA 721 MEASURED. No RULES change, no book promoted, no KEEP claimed, no memo, no
PROTOCOL edit applied; RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py untouched.**

Idea 721 filed the question: at a ~3% corpus 4a pass rate a pass-SHARE "BELOW" verdict is
unreadable below 180 picks, and no rule-8 book leg in the record exceeds 96 — so should the 4a
leg be quoted as a COUNT instead? This run builds a fresh corpus, prices the two forms head to
head at matched alpha, and answers: **no — the count form buys exactly zero. Not one
feasibility cell moves and not one power point moves, to six decimals. The units were never the
problem; the atom at zero is.** What a count form does buy is a *graded* number in place of a
trichotomy, and that is worth having for a different reason.

## Gates (pre-registered, printed before any new number was read)

| gate | result |
|---|---|
| G1 `fast_backtest` == `engine.backtest` @ 10 bps, 2 probe books | **PASS**, max dev **0.000e+00** (bar 1e-12) |
| G2 `EWALL(g=0.75)` == `baseline.rules_v2_weights` on U56 | **PASS**, max dev **0.000e+00** |
| G3 idea 721's corpus re-read from its own `.bookgrid.csv` | **PASS** — 4a **4/126** (3.17%), 4b **18/126** (14.29%) |
| G3b idea 721's floors re-read from its own `.pricefloor.csv` | **PASS** — 4a BELOW readable at m ≥ **180**, 4b at m ≥ **24** |
| G4 SPY OOS from `baseline.load_universe` | **PASS** — 15.24% / 0.8721 / −33.72% |

G2 was **mis-specified on the first run and is reported, not dropped**: a re-spreading
equal-weight book was compared against `rules_v2_weights`, which de-grosses to cash. Max dev
**3.597e-01**. The EWALL family was corrected to the live de-grossing form (`gross/N` over every
instrument *priced* that day, gated weight to cash) before any number below was read.

## Design

**Two tuned parameters, both swept, all grid points reported.** (1) CORPUS ∈ {NARROW = U56 +
B136, WIDE = U56 + B136 + SMALL}. (2) FORM ∈ {SHARE, COUNT}. Everything else pre-registered and
fixed: families {CAND *n*, IVOL *n*, EWALL}, *n* ∈ {10,20,30,40}, gross ∈ {0.50,0.75,1.00},
cadence ∈ {W,M}, band 0.03, 10 bps, t+1, IS ≤ 2016-12-31 / OOS ≥ 2017-01-01, α = 0.05.
**162 books, 54 per panel.** Freshness: idea 721's corpus was {RANK n∈5/10/20/50, GATE}; this is
a different family set (IVOL is new) on a different *n* ladder.

The two forms, at **matched alpha**:

- **SHARE** (the record's practice) — verdict from the realised share's position against the
  null share band [q05, q95], read as BELOW / INSIDE / ABOVE.
- **COUNT** (the proposal) — verdict from the exact null count distribution's one-sided
  achieved significance: BELOW if P(K ≤ k) ≤ 0.05, ABOVE if P(K ≥ k) ≤ 0.05, else INSIDE; the
  report quotes "k of m" and that ASL.

Null: a uniform random pick inside each (panel × gross × cadence) stratum; per-stratum
p_s = passers/9. A leg of m picks is the Poisson-binomial of the cyclically-extended p_s (exact
at m = S, preserves the strata's heterogeneity). Exact convolution vs 20k Monte Carlo agrees to
max **0.0023**.

## Corpus (all grid points in `.corpus.csv`; the panel × family × gross × cadence table is in the console)

| corpus | books | 4a | 4b |
|---|---|---|---|
| NARROW | 108 | **0 (0.00%)** | 16 (14.81%) |
| WIDE | 162 | **1 (0.62%)** | 16 (9.88%) |

## THE ANSWER — the two forms are the same test

**FORM AGREEMENT: 120/120 feasibility cells identical; max |power difference| over 360 matched
(corpus, path, m, θ) points = 0.000000, mean 0.000000.**

Exact integer floors (not ladder rungs), α = 0.05:

| corpus | path | p̄ | FEAS_below SHARE | FEAS_below COUNT | closed form ⌈ln α / ln(1−p̄)⌉ | FEAS_above (both) |
|---|---|---|---|---|---|---|
| NARROW | 4a | 0.0000 | **inf** | **inf** | inf | 1 |
| NARROW | 4b | 0.1481 | **21** | **21** | 19 | 1 |
| WIDE | 4a | 0.0062 | **457** | **457** | 484 | 1 |
| WIDE | 4b | 0.0988 | **33** | **33** | 29 | 1 |

The reason is algebraic and holds for any α: under both forms a BELOW verdict is readable iff
P(K=0) = ∏(1−p_j) ≤ α, and an ABOVE verdict iff P(K=m) = ∏ p_j ≤ α. The 5-95 quantile band and
the one-sided 5% ASL put the same tail mass in the same place. **Re-denominating a share as a
count cannot move a floor, because the floor is a property of the null's atom at zero, not of
the units the statistic is printed in.**

(FEAS_above = 1 is degenerate and is reported as such: once any stratum has no passers, "all m
pass" has probability 0, so the ABOVE direction is trivially readable. The direction idea 721
flagged — BELOW — is the one that costs.)

## The problem is worse than 721 measured

On this fresher corpus the 4a floor is **457 picks** (WIDE, p̄ = 0.62%) against 721's 180, and on
NARROW it is **infinite**: with 0 of 108 books passing 4a, no leg of any length could ever read
"this selector passes 4a less often than chance". The record's rule-8 book legs run **12 to 96**
picks. This run's own legs are 12 and 18.

Power at the record's own leg lengths, 4a, both forms identical (θ = alternative / base rate):

| corpus | m | θ=0 | θ=0.5 | θ=2 | θ=3 | θ=5 |
|---|---|---|---|---|---|---|
| WIDE 4a | 12 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| WIDE 4a | 18 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| WIDE 4a | 96 | 0.000 | 0.000 | 0.076 | 0.210 | 0.603 |
| WIDE 4a | 180 | 0.000 | 0.000 | 0.163 | 0.441 | 0.904 |

At the longest book leg the record has ever run (96), a selector passing 4a at **five times** the
corpus rate is detected 60% of the time and one passing at **half** the corpus rate is detected
**never**.

## Census — 457 committed tables carrying a `pass4a` column

Files enumerated by extension, nothing matched by keyword; each table read as a claim
population of size m = its row count, against the floor implied by its **own** observed rate.

| scale | tables | med m | med 4a rate | zero-rate tables (floor = inf) | below own floor |
|---|---|---|---|---|---|
| **LEG (m ≤ 100)** | 171 | 30 | 0.0000 | **87** | **110 (64.3%)** |
| MID (101–1000) | 228 | 306 | 0.0185 | 88 | 102 (44.7%) |
| GRID (m > 1000) | 58 | 1792 | 0.0162 | 14 | 18 (31.0%) |
| all | 457 | 180 | 0.0148 | 189 | 230 (50.3%) |

Only the LEG bucket is rule-8-leg scale; GRID rows are whole design grids, not selector legs.
At leg scale **87 of 171 tables have a zero 4a rate outright**, so their floor is not large — it
does not exist.

## What the count form DOES buy

The trichotomy discards a graded number. Across the 16 selector legs here, **1 leg** reads
INSIDE under SHARE while carrying a one-sided ASL ≤ 0.20: WIDE / IS_MINDD / 4a, **k = 1 of 18**,
null band [0, 1], **ASL_above = 0.1111**. A reader of the share sees "0.0556, inside [0.0000,
0.0556]" and learns nothing; a reader of "1 of 18, P(K ≥ 1) = 0.111 under a random pick" learns
the size of the evidence. That is a **legibility** gain, not a power gain, and it is worth
having on its own terms — but it is not the fix 727 was filed to test.

## Rule 8 (walk-forward) — selectors fit on IS only, each pick read ONCE on OOS

| corpus | selector | m | 4a | 4b | OOS CAGR | OOS Sharpe | OOS MaxDD | beat v2 | beat SPY |
|---|---|---|---|---|---|---|---|---|---|
| NARROW | IS_SHARPE | 12 | 0 | 3 | 10.43% | **1.1457** | −15.60% | 2 | 12 |
| NARROW | IS_CAGR | 12 | 0 | 2 | 12.52% | 1.0729 | −20.24% | 0 | 12 |
| NARROW | IS_CALMAR | 12 | 0 | 2 | 11.61% | 0.9997 | −18.62% | 0 | 7 |
| NARROW | IS_MINDD | 12 | 0 | 1 | 8.27% | 0.9975 | −15.15% | 0 | 9 |
| WIDE | IS_SHARPE | 18 | 0 | 3 | 8.48% | 0.8980 | −21.44% | 2 | 12 |
| WIDE | IS_CAGR | 18 | 0 | 2 | 10.07% | 0.8576 | −24.80% | 0 | 12 |
| WIDE | IS_CALMAR | 18 | 0 | 2 | 9.22% | 0.8007 | −22.89% | 0 | 7 |
| WIDE | IS_MINDD | 18 | **1** | 1 | 6.88% | 0.8627 | −15.32% | 4 | 9 |

OOS comparands (panel means): NARROW RULES v2 **1.2020** / 8.73% / −12.04%, SPY 0.8771 / 15.34% /
−33.72%. WIDE RULES v2 **0.9902** / 7.10% / −12.93%, SPY 0.8787 / 15.38% / −33.72%.
Full-sample: U56 SPY 15.11% / 0.8835 / −33.72%, RULES v2 8.63% / 1.2069 / −11.90%.

**No selector's mean OOS Sharpe beats the live book on either corpus.** The two closest single
picks lose by a hair and are reported as losses: `U56|EWALL|g1.00|W` OOS Sharpe **1.2827** vs
RULES v2's **1.2834** (−0.0007) and `B136|EWALL|g1.00|W` **1.1195** vs **1.1206** (−0.0011).

## Both KEEP paths — no KEEP

Corpus: 4a **0/108** (NARROW) and **1/162** (WIDE); 4b **16/108** and **16/162**. On the rule-8
legs, 4b passes 1–3 of 12 and 1–3 of 18 — every one of them **INSIDE** its own random-pick null
(best ASL_above **0.2407**, NARROW / IS_SHARPE / 4b, 3 of 12). The 4b-passing picks are the live
RULES v2 family at gross 1.00 and the ranked CAND books at gross 0.75 — a gross dial already
priced by ideas 670 / 675 / 677 — and none of them beats the live book out of sample. **Nothing
here is a capital candidate. No memo.**

## Proposed PROTOCOL wording (a PROPOSAL — not applied; rule 6, Sunday review only)

Add to rule 8, as a required field rather than a new bar:

> A KEEP-path pass reported over a selector leg must be quoted as a **count with its leg
> length and its null's achieved significance** — "k of m picks, P(K ≥ k) = p under a
> uniform random pick inside each stratum" — never as a bare share. A leg must also state
> its corpus base rate p̄ and, when the reported direction is BELOW, the feasibility floor
> **m\* = ⌈ln α / ln(1 − p̄)⌉**; a BELOW verdict quoted at m < m\* is **UNREADABLE** and must
> be reported as such rather than as a negative result. Changing the units from a share to
> a count does not move m\* — only more picks, or a higher-base-rate corpus, does.

The clause the queue proposed (count instead of share) is in there, but demoted: it earns its
place for legibility, not for power, and the sentence that actually protects a reader is the
floor.

## Caveats

SURVIVORSHIP (idea 54, `data/SMALL_PANEL_README.md`): `universe.json`, `universe_broad.json` and
`prices_small.csv.gz` are current constituents with no delistings, so every CAGR and pass-rate
*level* here is optimistic. The object under test is a reporting form and a floor, neither of
which is a level claim — but the corpus base rates p̄ that drive the floors inherit the bias
whole, and a survivorship-free corpus would have *lower* 4a rates and therefore *higher* floors.
The direction of the bias runs against the record, not for it.

The floor computation is exact for the pre-registered cyclic extension of a fixed stratum set.
A leg drawn i.i.d. from a stratum *pool* would be Binomial(m, p̄), whose floor is the closed form
in the table — the two differ by 2 picks at 4b and 27 at 4a, and both are quoted.

The census reads each committed table's row count as a claim count. That is right for the LEG
bucket and a loose upper bound for the GRID bucket, which is why the buckets are cut and
reported separately rather than pooled into one headline.

## Follow-ups filed

- **731** — the record's 4a corpus rate is falling (721: 3.17% on 126 books; this run: 0.62% on
  162, 0.00% on 108). Is 4a's drawdown leg reachable at all on a post-2020 corpus, or has the
  live book's own MaxDD improved past what any growth book can match?
- **732** — the ABOVE direction is free (floor 1) and the BELOW direction can be infinite. Should
  rule 8's KEEP-path leg be declared a one-sided ABOVE test outright, and every BELOW reading in
  the record retired?
- **733** — two rule-8 picks lose to the live book's OOS Sharpe by 0.0007 and 0.0011. Price the
  gross-1.00 de-grossing EWALL book against RULES v2 on a resolution fine enough to say whether
  that tie is a real dead heat or a cost-rung artefact.
