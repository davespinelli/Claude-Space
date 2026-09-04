# Idea 15 — crypto-sleeve — **PARK** (2026-09-04, lane C)

`research/backtests/2026-09-04_crypto-sleeve_C.py` · console `…_C.console.txt` · grid `…_C.grid.csv`
78 points (2 universes × 3 books × [1 control + 2 funding × 2 gates × 3 caps]), all reported.
Harness reproduces idea 2's KEEP row (12.7% / 1.093 / −18.3%, halves 1.088/1.103) and the live
v1 row (6.5% / 0.666 / −13.8%) to the decimal; c=0 equivalence vs the crypto-free panel is
1.4e-17.

## Verdict in one line
The sleeve is the largest and most consistent improvement any idea has produced on this
repo — **36 of 36 arms beat their own control on both lists** — and **PROTOCOL rule 8
rejects it 4 times out of 4**, because every pre-registered selection rule buys the cap and
gate that fail the out-of-sample drawdown bar. **PARK, not KEEP.**

## What was run
Books (structural, all reported): `v1` (live RULES v1), `CAND20` (idea 2's standing 4b KEEP —
top-20 eligible EQW at 75%/n, no vol scaler), `EWall` (equal-weight all eligible at 75%).
The equity signal, gate and ranking are computed on the crypto-free panel in every arm, so
the equity leg is bit-identical to the published books and the sleeve is the only change.

Funding (structural, both reported): `matched` — the sleeve is funded by scaling the equity
leg down, total gross unchanged (pre-registered primary, because ideas 66/73/81 showed an
un-matched gross change is an exact return lever); `add` — crypto added on top, gross rises.

Tuned parameters (rule 4 limit = 2):
1. cap `c ∈ {0, 5, 10, 15}%` per crypto name (0 = control, 10 = the queued value).
2. gate `g ∈ {same, trend}` — `same` applies RULES v1's own test to crypto (above 200d MA
   **and** vol20 < 0.60); `trend` waives only the vol cap.

`universe_broad.json` carries no crypto columns, so BTC/ETH are joined onto it from
`data/prices.csv` (index verified identical) for the standard cross-universe test.

## The gate is the whole design question, and it is a real one
BTC's median vol20 is **0.532** and ETH's **0.714**, so RULES v1's 0.60 vol cap — written for
equities and never examined on an asset whose distribution sits on top of it — is close to
binding. It cuts BTC's eligible days from **43.3% → 24.9%** and ETH's from **24.2% → 7.8%**.
Standalone gated-only returns over the eval window:

| | buy&hold | gate `same` | gate `trend` |
|---|---|---|---|
| BTC-USD | 33.8% / 0.810 / −83.0% | 21.0% / 0.855 / −52.4% | 38.8% / 0.966 / −63.6% |
| ETH-USD | 12.1% / 0.492 / −93.5% | 5.3% / 0.374 / −52.5% | 11.5% / 0.470 / −65.5% |

`trend` earns more Sharpe standalone; `same` is the one that survives 4b in the book, because
4b is a drawdown bar and `same` is where the drawdown control lives (mean dMaxDD −2.9%/−4.2%
vs `trend`'s −7.0%/−6.7%).

## The positive result (and it is the project's first of its kind)
* **36 of 36 sleeve arms beat their own crypto-free control on full-sample Sharpe on BOTH
  lists.** Paired daily t vs control: `matched` +1.71…+2.81, `add` +2.70…+3.21.
* **5 of 39 points pass cross-universe 4b at 10 bps** — `CAND20/matched/same/c5`,
  `EWall/matched/same/c5`, `EWall/matched/same/c10`, `EWall/matched/trend/c5`,
  `EWall/add/same/c5`. Both crypto-free controls fail that test — CAND20 on broad H2 (0.814
  vs SPY's 0.837), EWall on u56 CAGR (10.4% vs the 10.68% floor), the two near-misses ideas
  28/44 have been circling — and **the sleeve fixes exactly the bar each one was missing**,
  at 10 bps, where idea 11 showed neither control survives. It is not the project's first
  cross-universe pass (ideas 57, 63 and 66 have them) but it is the first to repair those
  two specific books.
* On universe.json, `CAND20/matched/same/c10` (the literal queued 10% cap, gross-matched,
  v1's own gate) goes 12.7% → **14.3% CAGR, 1.093 → 1.178 Sharpe**, MaxDD −18.3% → −19.1%,
  halves 1.254/1.127, OOS 1.237, turnover 9.6 → 10.3x/yr. It fails cross-universe on broad
  drawdown (−24.2% vs the −20.2% cap) by 4pp.
* Cost is not what kills it: at 25 / 50 / 100 bps the best arm's advantage over its control
  *widens* (+0.154 → +0.175 → +0.209 → +0.276 dSharpe), because the sleeve adds return
  without adding much turnover.

## Why it is a PARK — the four negatives, in order of weight
**1. Rule 8 rejects it 4 times out of 4, and the mechanism is systematic, not noisy.**

| walk-forward | S1 (plain Sharpe) | S2 (4b-aware) | OOS result | clears OOS 4b? |
|---|---|---|---|---|
| u56, IS ≤2016 | `CAND20/add/trend/c15` | same | 28.4% / 1.315 / **−31.1%** | **No** (cap −20.2%) |
| broad, IS ≤2016 | `EWall/add/trend/c15` | same | 24.3% / 1.226 / **−30.4%** | **No** |
| u56, crypto era IS ≤2021 | `EWall/add/trend/c10` | `EWall/add/same/c15` | 10.5% / 0.810 / **−19.4%** | **No** (cap −14.7%) |
| broad, crypto era IS ≤2021 | `EWall/add/trend/c15` | `EWall/add/same/c15` | 9.7% / 0.670 / −24.1% | **No** |

This is idea 66's failure shape exactly — its `ew-band3 g=0.90` also passes cross-universe 4b
at 5–25 bps and is also unselectable by rule 8 — and the two together are now a pattern worth
naming: **on this repo, a cross-universe 4b pass that sits at an interior parameter value has
twice turned out to be unreachable by any rule that maximises in-sample Sharpe.**

In-sample Sharpe is **monotone increasing in `c`** and higher for `trend` than `same` in
essentially every cell, so any Sharpe-maximising rule buys the largest cap and the loosest
gate — and that is precisely the corner that blows the OOS drawdown bar. Within-book audits
pick c=15 in **11 of 12** cells. **Not one of the 5 cross-universe-passing arms is selected
by any rule in this run.** They are the arms you would only choose knowing the answer.
Spearman(IS, OOS Sharpe) is +0.771/+0.855 on the rule-8 windows but falls to **+0.362/+0.252**
on the crypto-era windows — the ordering that looks stable is the equity book's, not the
sleeve's.

**2. Rule 8 cannot honestly select this parameter anyway, and that is a data fact.**
BTC's cache starts 2014-09-17 (tradeable 2015-07-02); ETH's starts 2017-11-09 (tradeable
2018-08-27). The rule-8 in-sample window (≤2016-12-31) therefore holds ~1.5 years of BTC and
**zero** ETH. The crypto-era walk-forward (IS 2018-09→2021, OOS 2022→2026) was added for that
reason and rejects the idea too, but it is only 3.3 years of in-sample. **This idea cannot be
walk-forward validated on the data the project has**, and no amount of care changes that.

**3. Most of the full-sample t-statistic is one calendar year.** 2017: BTC **+1425%**,
ETH +135%. It sits inside H1 (H1 ends 2017-11-02), which is why sleeve H1 Sharpes look
spectacular (CAND20 1.088 → 1.408 at trend/c10) — but only **13.1%** (`same`) / **24.0%**
(`trend`) of H1 days hold any crypto at all, and the first divergence from the control is
2015-07-27. An "H1 Sharpe" for a sleeve arm is not the same object as an H1 Sharpe for an
equity book. Restricted to the crypto era (2018-09+, where both names exist and 2017 is
excluded), the effect shrinks by a third and loses significance: t_cry **+0.66…+2.06**, and
dSharpe turns **negative in 4 of 18** gross-matched arms on universe.json (`same/c15`,
`trend/c15`, and the EWall c15 pair). 2018 is the counter-year the full sample hides:
BTC −74%, ETH −82%, and `CAND20/matched/trend/c10` returns **−0.4% vs the control's +5.9%**.

**4. Survivorship is worse here than anywhere else in the repo.** BTC and ETH are the two
survivors of the crypto field; LUNA, FTT and the entire 2014–18 altcoin cohort are absent,
and unlike an equity panel the dead names went to zero rather than being acquired. Every
number above is an upper bound on a sleeve chosen with ten years of hindsight about which two
tickers to hold. Secondary: crypto trades 24/7 but the price index is equity trading days, so
weekend moves land in the Monday bar and a Friday-close rebalance cannot react to them —
this *understates* realised crypto drawdown; and 10 bps is an equity cost assumption while
retail crypto spreads are larger (the cost column above is a partial answer, not a full one).

## What this does and does not license
It does **not** license adding crypto to RULES. It does establish two things the project
did not have:
* **The 0.60 vol20 cap is doing real work as a drawdown instrument, not just as an equity
  hygiene filter.** Every 4b failure among the sleeve arms is `DD`, and `same` vs `trend` is
  the only lever in this run that changes which side of the cap a book lands on. That is a
  cleaner demonstration of the vol gate's function than idea 56 (which tested it on
  equities, where it destroys value on small caps) — the gate's value is conditional on the
  asset's own vol distribution relative to the cap.
* **The 4b drawdown cap is what stops any high-vol satellite**, and the cap at which it stops
  binding is between 5% and 10% per name — a number RULES could state directly if a
  satellite clause is ever wanted.

## RULES wording — **not recommended for adoption**, recorded so the Sunday review can see
what would be required:
> Non-equity instruments may be held only under the same eligibility test as equities (above
> the 200-day average AND vol20 < 0.60), capped at 5% of book per instrument and funded by
> scaling the equity leg down so total gross is unchanged.

Adopting it would rest on two ex-post-selected tickers, an unvalidatable parameter, and a
2017 that will not repeat. **Recommend: do not adopt. Revisit only when (a) a delisting-aware
crypto panel exists (cf. idea 54 for equities) and (b) there are ≥8 further years of ETH.**

Ideas 87–89 queued.
