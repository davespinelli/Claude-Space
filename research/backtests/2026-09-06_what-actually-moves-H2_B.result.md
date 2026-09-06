# Idea 70 — what-actually-moves-H2 (lane B, 2026-09-06)

**Verdict: ANSWERED / KILL of both candidate explanations. The broad ranked book's H2
shortfall is neither a handful of names nor a sector hole. It is a BILL and an EPISODE:
the book's stock selection beats SPY by +0.114 vol-matched Sharpe in H2 and hands all of
it back to a −0.098 turnover bill and a −0.040 vol-matched underinvestment residual; what
is left of the −0.023 gap lives entirely in one 21-day window, 2020-03-24 → 2020-04-22.
No KEEP-candidate, no memo, no RULES change. RULES.md, scan.py, bot.py and baseline.py
untouched.**

**Race note.** A cloud lane answered idea 70 concurrently (commit `0a9fdf6`) from a
different construction — whole-sample eligibility bans over the 128 *held* names, a PIT
top-10 mega-cap **cap dial**, and a SPY-state regime split. It reached the **same verdict
on both queued mechanisms** (not names: 0 of 128 deletions clear SPY; not mega-cap weight:
capping moves H2 monotonically the wrong way, 0 of 5 levels) and the same "it is a regime"
conclusion. This run is an independent second answer that agrees, and adds two things the
cloud run does not have: the **exact vol-matched Sharpe identity** (so the gap is priced
into selection / cost / underinvestment rather than described) and the **localisation of
the whole residual to 21 days**. Both are kept; neither is a KEEP-candidate.

Script: `research/backtests/2026-09-06_what-actually-moves-H2_B.py`
Console: `…_B.console.txt` · CSVs: `…_B.{sectors,names,loo,years,grid}.csv`

## Reproduction gate — 6/6 EXACT before any new number was read

Idea 66's published broad `top20-200d`, g=0.75, core=0, weekly, 10 bps, prices truncated
at its last eval day 2026-09-03 so the halves split on the same date:

| | CAGR | Sharpe | MaxDD | H1 | H2 | SPY H2 |
|---|---|---|---|---|---|---|
| published (idea 66) | 13.1% | 0.958 | −20.1% | 1.125 | **0.814** | **0.837** |
| reproduced here | 13.11% | 0.9581 | −20.05% | 1.1246 | 0.8135 | 0.8366 |

Eval 2009-01-13 → 2026-09-03; H2 = 2017-11-03 → 2026-09-03, 2219 days.

## Why the question had to be re-framed before it could be answered

The failing bar is a **Sharpe** bar, and Sharpe is scale-free, so decomposing raw excess
return cannot address it: in H2 the book runs 11.46%/14.67% vol against SPY's
15.05%/18.90%, with 26% in cash. Raw excess is dominated by that cash, which idea 66
already proved Sharpe-neutral. So this run decomposes the **vol-matched** active return
`a_t = k·r_book,t − r_spy,t` with `k = σ_SPY/σ_book = 1.2888` a constant, for which
`S_book − S_SPY = 252·mean(a)/σ_SPY` holds exactly. Per name that gives
`Σ_i A_i + COST + BENCH = ΔS`, **verified to 1.1e-16**, not assumed.

## Result 1 — the gap is an accounting identity, and selection is the winning term

    Σ_i A_i  +0.9115   +   COST  −0.0979   +   BENCH (−S_SPY)  −0.8366   =   ΔS  −0.0231

Regrouped into the three things a book operator can act on:

| term | value | what it is |
|---|---|---|
| **selection (active)** | **+0.1145** | Σ_s (A_s − k·w̄_s·S_SPY): what picking these 20 names is worth |
| **turnover bill** | **−0.0979** | 14.37× annual turnover in H2 (13.78× full sample) at the 10 bps rung |
| **vol-matched underinvestment** | **−0.0395** | (k·gross − 1)·S_SPY, i.e. −0.0472 × 0.8366 |
| = ΔS | **−0.0231** | the 0.814-vs-0.837 gap |

**The stock picking is not the problem — the bill is.** Selection is +0.114 and cost alone
eats 85% of it. This is a different disease from either idea 63's cash drag (worth only
−0.040 once vol is matched, exactly as idea 66's flat-Sharpe result implied) or the
mega-cap concentration story.

**No sector is a hole.** All 15 classes, mean weight and Sharpe contribution:

| sector | mean wt | A_s | active |
|---|---|---|---|
| InfoTech | 0.2328 | **+0.4874** | **+0.2364** |
| ETF-Sector | 0.0504 | +0.0710 | +0.0167 |
| CommSvcs | 0.0351 | +0.0673 | +0.0295 |
| Financials | 0.0842 | +0.0623 | −0.0284 |
| ConsDisc | 0.0567 | +0.0590 | −0.0021 |
| HealthCare | 0.1058 | +0.0590 | −0.0550 |
| Industrials | 0.0646 | +0.0543 | −0.0153 |
| ETF-Cmdty | 0.0232 | +0.0308 | +0.0058 |
| Energy | 0.0205 | +0.0284 | +0.0063 |
| ConsStap | 0.0358 | +0.0070 | −0.0315 |
| RealEstate | 0.0037 | +0.0019 | −0.0021 |
| ETF-Bond | 0.0038 | +0.0001 | −0.0040 |
| Materials | 0.0065 | −0.0002 | −0.0071 |
| ETF-Index | 0.0047 | −0.0047 | −0.0097 |
| Utilities | 0.0117 | −0.0123 | −0.0250 |

Only three sectors have a negative gross contribution and together they are worth −0.017 —
less than a fifth of the cost term. The largest negative *active* cell, HealthCare −0.055,
is a weight effect (10.6% of gross earning less than SPY per unit of weight), not a
selection failure: its gross contribution is positive. Taxonomy is a fixed 15-class map
written before any result was read, constant over the sample (no point-in-time GICS, so
the 2023 V/MA/ADP reclassifications are deliberately not applied).

## Result 2 — "a handful of names" is false as a diagnosis and worthless as a rule

136 **real re-runs**, each removing one name from the eligible panel so the rank is
recomputed and the book still holds 20:

- **3 of 136** single-name removals lift H2 Sharpe above SPY's 0.8366; the best is WFC at
  0.8436 (+0.0070 over SPY, i.e. +0.030 over the parent).
- LOO H2 Sharpe spans 0.7804 (drop MU) … 0.8436 (drop WFC), sd 0.0105. The book is not
  hostage to any one name in either direction.
- Spearman(LOO gain, −A_i) = **+0.526** — the cheap attribution ranks removals only
  moderately, which is why every claim above rests on the re-runs.

Hindsight drop-k ladder (exclusion chosen **on H2** — this is a ceiling, not a rule):
k = 0/1/2/3/5/10 → H2 Sharpe **0.8135 / 0.8163 / 0.8452 / 0.8594 / 0.8666 / 0.9201**.
Against 2000 random k-subsets the hindsight-best k sits at the 99.4th–100th percentile at
every k, which is exactly what a maximum over 136 candidates is supposed to do. It takes
dropping the 10 worst names *chosen with full knowledge of H2* to buy +0.084.

## Result 3 — it is a regime, and the regime is one month of 2020

Time-concentration of `a_t` (nothing is selected on L; all three values reported):

| L | worst L-day Σa | share of \|ΔS\| | ΔS with that window deleted | permutation pctile | window |
|---|---|---|---|---|---|
| 21 | −0.2368 | 617% | **+0.1203** | **1.0%** | 2020-03-24 → 2020-04-22 |
| 63 | −0.2705 | 705% | +0.1435 | 5.0% | 2020-03-24 → 2020-06-22 |
| 126 | −0.2769 | 722% | +0.1519 | 31.5% | 2020-03-24 → 2020-09-21 |

**One 21-day window is worth 6.2× the entire H2 Sharpe gap**, and deleting it flips the
book from −0.023 behind SPY to +0.120 ahead. Only 1% of 200 permutations of the same daily
returns produce a window that bad, so this is genuine time-concentration, not the tail you
get for free from re-ordering. The window is the COVID *rebound*, not the crash: the 200d
gate had taken the book out and the book was still climbing back in while SPY went
vertical — the whipsaw mechanism ideas 52/57 priced on the gate, showing up here as the
whole of the 4b failure. Note the L=126 percentile of 31.5%: the concentration is sharp at
one month and dissolves at six, which is the signature of a single episode rather than a
multi-year regime.

H2 raw excess by calendar year (book − SPY): −2.8 / +6.4 / −14.9 / −6.1 / −13.2 / +7.3 /
−13.5 / −4.3 / +2.2 / +1.1 pp for 2017…2026; the book beat SPY in 4 of 10. That series is
*raw*, so it is dominated by the 26% cash in up years and says nothing about the Sharpe
bar — it is reported for completeness, not as evidence.

## Result 4 — the mega-caps are the book's best asset, not its hole

MEGA10 = AAPL, MSFT, NVDA, AMZN, GOOGL, META, AVGO, TSLA, BRK-B, LLY — a **hindsight**
list (2026's top 10), which makes the concentration hypothesis *easier* to confirm, so the
null result below is the robust direction.

- Book's mean MEGA10 weight in H2: 0.0996 of 0.7393 gross = **13.5% of the book**, range 0.000–0.267.
- Regression of `a_t` on MEGA10 weight: β +0.0055, t **+1.66**, R² **0.0012** (same-day);
  β +0.0070, t +2.10, R² 0.0020 (lag-1). Both signs are **positive** — more mega-cap
  weight goes with *less* shortfall — and R² is under a quarter of one percent either way.
- MEGA10 supplies **+0.2242 of the book's +0.9115** Sharpe (24.6%) from 13.5% of the weight.
- Counterfactual re-run with all ten banned: H2 **9.59% / 0.730 / −20.73%**, i.e. **−0.084
  Sharpe**. Underweighting mega-caps costs the book almost four times the gap it is
  accused of causing.

## Rule 8 — the exclusion fitted on 2009-2016, 2017-2026 untouched

H2 begins 2017-11-03 and the OOS window begins 2017-01-03: **H2 is the OOS window**
(100% overlap), so any exclusion fitted on H2 is hindsight by construction. The honest
test is whether names/sectors that hurt in-sample keep hurting out-of-sample. All 12 grid
points (2 tuned parameters: k ∈ {0,1,2,3,5,10}, granularity ∈ {name, sector}):

| gran | k | excluded | OOS CAGR | OOS Sh | OOS DD | full CAGR | Sh | DD | H1/H2 | verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| name | 0 | (none) | 12.52% | 0.894 | −20.05% | 13.11% | 0.958 | −20.05% | 1.125/0.814 | KILL 4a(H1,H2,DD) / KILL 4b(H2) [v1: KEEP 4a] |
| name | 1 | ACN | 12.41% | 0.887 | −20.05% | 13.12% | 0.961 | −20.05% | 1.139/0.806 | KILL 4a(H1,H2,DD) / KILL 4b(H2) [v1: KEEP 4a] |
| name | 2 | ACN,AMD | 12.64% | 0.912 | −19.79% | 13.27% | 0.979 | −19.79% | 1.163/0.819 | KILL 4a(H1,H2,DD) / KILL 4b(H2) [v1: KEEP 4a] |
| name | 3 | ACN,AMD,ICE | 12.61% | 0.911 | −19.79% | 13.32% | 0.983 | −19.79% | 1.174/0.818 | KILL 4a(H1,H2,DD) / KILL 4b(H2) [v1: KEEP 4a] |
| name | 5 | ACN,AMD,ICE,SPGI,VRTX | 12.46% | 0.902 | −20.30% | 13.45% | 0.994 | −20.30% | 1.202/0.815 | KILL 4a(H1,H2,DD) / KILL 4b(H2,DD) [v1: KEEP 4a] |
| name | 10 | +ABBV,CB,SCHW,GE,MRK | 12.45% | 0.902 | −19.71% | 13.78% | 1.017 | −19.71% | 1.250/0.816 | KILL 4a(H2,DD) / KILL 4b(H2) [v1: KEEP 4a] |
| sector | 0 | (none) | 12.52% | 0.894 | −20.05% | 13.11% | 0.958 | −20.05% | 1.125/0.814 | KILL 4a(H1,H2,DD) / KILL 4b(H2) [v1: KEEP 4a] |
| sector | 1 | ETF-Bond | 12.39% | 0.880 | −21.32% | 13.26% | 0.961 | −21.32% | 1.147/0.799 | KILL 4a(H1,H2,DD) / KILL 4b(H2,OOS,DD) [v1: KILL 4a(DD)] |
| sector | 2 | +ETF-Index | 12.37% | 0.880 | −20.96% | 13.28% | 0.964 | −20.96% | 1.152/0.800 | KILL 4a(H1,H2,DD) / KILL 4b(H2,OOS,DD) [v1: KEEP 4a] |
| sector | 3 | +Energy | 12.41% | 0.883 | −20.96% | 13.30% | 0.964 | −20.96% | 1.156/0.797 | KILL 4a(H1,H2,DD) / KILL 4b(H2,OOS,DD) [v1: KEEP 4a] |
| sector | 5 | +RealEstate,Utilities | 12.13% | 0.862 | −22.34% | 13.38% | 0.965 | −22.34% | 1.186/0.772 | KILL 4a(H1,H2,DD) / KILL 4b(H2,OOS,DD) [v1: KILL 4a(DD)] |
| sector | 10 | +Materials,ETF-Cmdty,Financials,ConsStap,ETF-Sector | **14.51%** | **1.005** | −22.16% | 14.66% | 1.043 | −22.16% | 1.209/0.899 | KILL 4a(H1,H2,DD) / **KILL 4b(DD)** [v1: KILL 4a(DD)] |

Comparands over the same windows:

| | OOS CAGR | OOS Sharpe | OOS MaxDD | full CAGR | Sharpe | MaxDD | H1/H2 |
|---|---|---|---|---|---|---|---|
| **RULES v2 (live book)** | 8.01% | **1.122** | −12.24% | 8.04% | 1.107 | −12.24% | 1.229/0.988 |
| RULES v1 (retired 2026-09-06) | 5.99% | 0.581 | −21.19% | 6.41% | 0.638 | −21.19% | 0.756/0.537 |
| SPY | 15.50% | 0.884 | −33.72% | 15.26% | 0.890 | −33.72% | 0.957/0.837 |

The 4a comparand is the LIVE book, which became **RULES v2** at the 2026-09-06 Sunday
review (`9ed1f2b`) while this run was executing; the run was re-executed against it. v2 is
defined on universe.json and is run here on the broad panel so that comparand and arms see
the same days and instruments — the only way the halves line up. The v1 verdict is carried
in brackets for continuity with the pre-v2 record.

**4a passes 0 of 12 against the live book and 4b passes 0 of 12.** (Against the retired
RULES v1 it was 9 of 12, which was never informative: v1's OOS Sharpe is 0.581 and almost
anything clears it. v2 at 1.122 OOS / 1.229/0.988 halves and −12.24% MaxDD is a real bar,
and none of these arms comes close on either half or on drawdown.) The IS-fitted name
exclusions move OOS Sharpe over the whole ladder by 0.887…0.912, i.e. ±0.013 around the
parent's 0.894 — nothing.

**The persistence test is the direct KILL:** Spearman(IS per-name contribution, OOS
per-name contribution) = **+0.285**, and the overlap of the IS-worst-10 names with the
OOS-worst-10 is **0 of 10**; the IS-worst-3 sectors overlap the OOS-worst-3 by 1 of 3. The
names that hurt in 2009-2016 are simply not the names that hurt in 2017-2026, which is
what "a handful of names" would have had to mean to be tradable.

The one grid point that beats SPY OOS on Sharpe, `sector k=10` (1.005 vs 0.884), is not a
candidate and is not reported as one: it bans 10 of 15 classes and keeps only InfoTech,
CommSvcs, ConsDisc, HealthCare and Industrials — a structural growth bet whose OOS drawdown
of −22.16% breaks the 4b bar (0.60 × 33.72% = 20.23%), and whose own ladder is
non-monotone (0.894 / 0.880 / 0.880 / 0.883 / 0.862 / **1.005**), i.e. it is one outlier
point, not a trend. Reported because the protocol requires every grid point, flagged
because a single non-monotone winner at the end of a ladder is the shape of noise.

## What this hands the queue

1. The 4b-binding number on the broad ranked book is **a turnover bill (−0.098 Sharpe at
   10 bps, 14.37× annual turnover in H2), not an alpha hole** — selection is +0.114 in the same
   window. Every past attempt to fix H2 by changing *what the book owns* (idea 63's core,
   idea 66's gross) was aimed at the wrong term. The lever is turnover.
2. The residual after cost is **one 21-day episode** (2020-03-24 → 2020-04-22, the gate's
   post-crash re-entry lag), permutation percentile 1.0%. That is the whipsaw ideas 52/57
   priced, and it is the entire remaining gap.
3. Mega-cap underweight and sector composition are both ruled out, the second with a
   hindsight-favourable test that still came back null.

Proposed follow-ups (queued below): turnover-budgeted rebalancing on this exact book, and
a re-entry rule aimed specifically at the post-crash lag.
