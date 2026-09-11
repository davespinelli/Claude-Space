# Idea 721 — publish a MINIMUM CLAIM COUNT beside every permutation band verdict

**Lane:** cloud · **Date:** 2026-09-11 · **Script:** `2026-09-11_publish-a-MINIMUM-CLAIM-COUNT-beside-every-permutation-band-verdict_cloud.py`

**Verdict: ANSWERED / the floor is real and the record is systematically over-quoting INSIDE.
No KEEP.**

Idea 717 found its ladder separates nothing below ~12 claims. This run computes the separation
floor for **every committed permutation / placebo band in the record** — 862 band rows across
the complete set of 12 committed CSVs carrying a (null-lo, null-hi) pair, 769 usable — and asks
the same question of the thing that decides capital: a rule-8 selector's KEEP-path pass share.

## Gates (asserted before any new number was read)

| gate | result |
|---|---|
| G1 idea 714 `FAM5/logx/400` MaxDD share == 2/19 | **PASS** |
| G2 idea 717 DDnorm@BAR m=19 reads BELOW | **PASS** |
| G3 idea 717 BAR m=4,6, both DD outcomes read INSIDE | **PASS** |
| G3b idea 717 BAR m=4 excess exactly 0.0 for both | **PASS** |
| G4 SPY Sharpe finite from `baseline.load_universe` | **PASS** |

**RECORD CORRECTION to idea 717.** Its result prose says that at BAR m = 4 and 6 "both outcomes
read INSIDE with excess **exactly +0.0%**". Three of those four rows do; the fourth does not —
`DDnorm@m=6` carries excess **−0.1667**, not 0.0. The committed `.matched.csv` is right; the
sentence quoting it is not. (Read directly: MaxDD@m=4 +0.0000, MaxDD@m=6 +0.0000,
DDnorm@m=4 +0.0000, DDnorm@m=6 **−0.1667**.) The INSIDE verdicts themselves are unaffected.

## Two floor definitions (tuned param 2), two bands (tuned param 1) — all 4 cells reported

- **FEAS** — the smallest m at which a verdict **in the direction the real value sits** is
  readable at all. A real share below its null median can only ever read BELOW, which needs the
  band's lower edge > 0. Defined for SHARE bands only; a LEVEL band has continuous support, so
  FEAS is reported **NOT APPLICABLE** rather than as a fake floor of 1.
- **POW50** — the smallest m at which, holding the observed effect size fixed, the real value
  lands outside the band with probability ≥ 0.5.
- **UNREADABLE** — a third state the census surfaced and the queue did not anticipate: the
  band's own null median is pinned at 0 (or 1) on the side the real value sits, so **no count
  whatever** could produce that verdict.

## Census: 862 band rows, 12 files

| kind | rows | usable |
|---|---|---|
| SHARE (a proportion over m claims / draws / cells) | 405 | 368 |
| LEVEL (a continuous statistic resampled m times) | 457 | 401 |

| band | floor | kind | applicable | unreadable | med m | med floor | **below floor** |
|---|---|---|---|---|---|---|---|
| 5-95 | FEAS | SHARE | 368 | 17 | 20 | 3 | **39 (10.6%)** |
| 5-95 | FEAS | LEVEL | — n/a — | | 974 | | |
| 5-95 | POW50 | SHARE | 368 | 28 | 20 | 5 | **138 (37.5%)** |
| 5-95 | POW50 | LEVEL | 401 | 93 | 974 | 318 | **204 (50.9%)** |
| 2.5-97.5 | FEAS | SHARE | 368 | 17 | 20 | 1 | 33 (9.0%) |
| 2.5-97.5 | POW50 | SHARE | 368 | 22 | 20 | 1 | 77 (20.9%) |
| 2.5-97.5 | POW50 | LEVEL | 401 | 93 | 974 | 318 | 204 (50.9%) |

## Headline: the floor problem is **entirely** an INSIDE-verdict problem

Cut by whether the published verdict was INSIDE (band 5-95):

| floor | verdict | rows | med m | med floor | unreadable | below floor | share |
|---|---|---|---|---|---|---|---|
| FEAS | **not INSIDE** | 169 | 28 | 2 | 0 | **0** | **0.0%** |
| FEAS | **INSIDE** | 199 | 19 | 3 | 17 | **39** | **19.6%** |
| POW50 | **not INSIDE** | 377 | 974 | 30 | 2 | **39** | **10.3%** |
| POW50 | **INSIDE** | 392 | 53 | 98 | 119 | **303** | **77.3%** |

**Not one** BELOW/ABOVE verdict in the record is quoted below its own feasibility floor — those
readings are all earned. But **1 in 5** of the record's INSIDE verdicts could not have read
anything else at their own count, and at the power floor **77.3%** of them are count statements
rather than evidence, against 10.3% of the non-INSIDE rows — a **7.5x** asymmetry. Idea 717's
local finding generalises: *"not distinguishable from the null"* is, in this record, mostly
*"not enough claims to distinguish anything"*.

At the tighter 2.5-97.5 band the same asymmetry holds at 61.7% vs 10.3%, so the conclusion is
not a band artefact.

**Per file (band 5-95, FEAS then POW50, below-floor / rows):**

| file | kind | rows | FEAS below | POW50 below | unreadable (POW50) | med m |
|---|---|---|---|---|---|---|
| `714/share` | SHARE | 96 | **16** | **50** | 20 | 21.5 |
| `714/claimrate` | SHARE | 120 | 0 | 27 | 3 | 36 |
| `717/matched` | SHARE | 67 | 3 | 17 | 4 | 12 |
| `WIDTHMAX/pin` | SHARE | 85 | **20** | **44** | 1 | 8 |
| `randscreen/cell` | LEVEL | 66 | n/a | **49** | 17 | 98 |
| `salted/S` · `saltedK/S` | LEVEL | 60 · 60 | n/a | 35 · 35 | 18 · 18 | 974 |
| `salted/IS` · `salted/DD` | LEVEL | 60 · 60 | n/a | 30 · 18 | 16 · 14 | 974 |
| `abstain/gain` · `abstainWF/gain` | LEVEL | 19 · 19 | n/a | 14 · 14 | 2 · 2 | 22 |
| `ROOM/live` · `ROOM/tau` | LEVEL | 27 · 24 | n/a | 4 · 3 | 3 · 3 | 1800 · 1834 |

The two worst offenders are the two smallest-m files: `WIDTHMAX/pin` (median 8 draws against a
median floor of 11 under POW50) and idea 714's own `714/share`. The `ROOM` files, at m ≈ 1,800,
are the record's best-resolved bands and almost never fall below their floor.

## PRICE LEG — the same question asked of PROTOCOL's two KEEP paths

126 books on three panels (U56 55 names, B136 135, SMALL 439 after dropping the 44 tickers with
`max_1d_move >= 1.0`), gated-EW and ranked families × gross {0.50, 0.75, 1.00} × {W, M}, 10 bps,
t+1 execution, no leverage. Corpus: **4a 4/126 (3.17%), 4b 18/126 (14.29%)**.

OOS benchmarks (> 2016-12-31): RULES v2 U56 **9.44% / 1.2737 / −12.05%**, B136 7.96% / 1.1150 /
−12.24%, SMALL 3.80% / 0.5613 / −14.68%; SPY **15.15–15.37% / 0.868–0.878 / −33.72%**.

**Rule 8** — inside each (panel × gross × cadence) stratum a selector picks the argmax of an
**IS-only** statistic over 7 dial books; 18 picks per selector, each read **once** on OOS:

| selector | picks | 4a | 4b | beat v2 | beat SPY | OOS CAGR | OOS Sharpe | OOS MaxDD |
|---|---|---|---|---|---|---|---|---|
| IS_SHARPE | 18 | 0 | 2 | 6 | 9 | 18.82% | 0.8562 | −30.34% |
| IS_CAGR | 18 | 0 | 2 | 6 | 12 | 20.17% | 0.8682 | −31.81% |
| IS_CALMAR | 18 | 0 | 3 | 6 | 9 | 18.38% | 0.8695 | −29.97% |
| **IS_MINDD** | 18 | **2** | **4** | **11** | 12 | 7.22% | **0.9979** | **−13.29%** |

Uniform random-pick null over the same 18 strata, 2,000 draws: `share4a` **[0.0000, 0.0000,
0.1111]**, `share4b` **[0.0556, 0.1111, 0.2778]**, `mean OOS Sharpe` **[0.9080, 0.9468, 0.9834]**.

IS_MINDD's 4a share (0.1111) sits **exactly on** the null's 95th percentile and its 4b share
(0.2222) is inside it. **No selector separates from random picking on either KEEP path.** Only
IS_MINDD's mean OOS Sharpe (0.9979) clears both the random-pick null's p95 (0.9834) and the
panel-mean RULES v2 OOS comparand (0.983372) — and it clears each by under 0.015, inside the
null's own p50-to-p95 span of 0.037.

**And it could not have.** The same floor computation on the pass-share statistic itself:

| path | corpus rate | m at which a BELOW verdict becomes readable |
|---|---|---|
| **4a** | 3.17% | **180 picks** (band 5-95 and 2.5-97.5 alike) |
| **4b** | 14.29% | **24 picks** |

At 18 picks the 4a null band is **[0.0000, 0.1111]** — its lower edge is pinned at zero, so a
"this selector passes 4a less often than chance" verdict is **unreadable at any count below
180**. The record's own rule-8 book legs run **12 to 96 picks** (idea 536 12, idea 717 15, idea
715 24 and 96). **Every 4a pass-share verdict in the record's book legs is below its own
separation floor.** The 4b floor of 24 is reachable and idea 715's 96-pick leg clears it.

## No KEEP

4a 4/126 and 4b 18/126 on the corpus; 4a 2 and 4b 4 on 18 rule-8 picks, neither separating from
a random pick. Nothing here is a capital candidate, no memo.

## Caveats

SURVIVORSHIP (idea 54, `data/SMALL_PANEL_README.md`): `universe.json`, `universe_broad.json` and
`prices_small.csv.gz` are all **current constituents with no delistings**, so every CAGR and
pass-share *level* on the price leg is optimistic. The object under test is a count threshold
and a selector's ranking against its own null, neither of which is a level claim; the 4a/4b
columns inherit the bias whole.

The census population is the complete set of committed CSVs carrying an explicit (null-lo,
null-hi) column pair. Bands published only in prose or only as a p-value are **not** reached —
the harvest is stated per file in the script's REGISTRY, nothing is matched by keyword. The
LEVEL-band POW50 floor assumes the null's half-width scales as 1/√m, which is checked
empirically on the SHARE bands (where the null can be resampled) but assumed on the LEVEL ones.

## Follow-ups filed

- **727** — PROTOCOL should carry the 4a floor: at a ~3% corpus pass rate a 4a pass-share
  verdict needs ≥ 180 picks, and no book leg in the record has ever had that many. Should the
  4a leg of a rule-8 report be quoted as a count rather than a share?
- **728** — re-read the record's 17 UNREADABLE band rows (null median pinned at 0 or 1) and
  publish what, if anything, each was taken to establish.
- **729** — does the FEAS/POW50 gap widen with the permutation null's dispersion? The censused
  bands run 1.19x–1.68x wider than a plain binomial at the same m, and the floor is roughly
  quadratic in that factor.
