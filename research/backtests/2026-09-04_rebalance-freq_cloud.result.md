# Idea 3 — rebalance-freq (cloud lane, 2026-09-04)

**Verdict: KILL for daily and quarterly, PARK for monthly, and a robustness PASS for idea
57's standing 4b candidate.** Trading *more* often than weekly is decisively and
significantly harmful in every book on both universes; trading *less* often (monthly) is a
large and significant improvement in 3 of the 4 books — but it buys that return with
drawdown, so it fails 4b's MaxDD cap on the broad list, and **both** pre-registered rule-8
walk-forward selections end on arms that fail the OOS 4b bars. No cadence change is
recommended for RULES.

Script: `research/backtests/2026-09-04_rebalance-freq_cloud.py`
Console: `2026-09-04_rebalance-freq_cloud.console.txt`

## Question and design

Every result in this project rebalances **weekly**, a choice never tested. Idea 3 asks
daily vs weekly vs monthly vs quarterly. The prior from ideas 55/57/4 makes it a real test:
those runs found net Sharpe in the gate-only book orders by *flip rate* — the cheapest
(slowest) trend instrument wins, because the incumbent 200d gate flips 7.55x/ticker/yr and
pays the whipsaw. Rebalance frequency is the cruder way to slow a book down. If whipsaw is
the mechanism, monthly should beat weekly at 10 bps and the gap should widen with cost.

- **Universes:** `universe.json` (56) and `universe_broad.json` (136), both fully reported.
- **Books (all pre-chosen, none tuned here):** `v1` = `rules_v1_weights` exactly as live;
  `top20` = idea 2's 4b KEEP; `ew-all` = equal-weight all eligible @75%; `ew-band3` = idea
  57's 4b KEEP-candidate (3% MA band).
- **Tuned dimension: exactly one** — the rebalance calendar, 4 arms {D, W, M, Q}.
- **Costs:** 5/10/25/50 bps; verdicts read at the protocol's 10 bps. Costs applied
  analytically; harness check shows max abs daily diff **0.00e+00** vs a real `cost_bps=10`
  engine run, and the harness reproduces idea 2 (12.7%/1.093/-18.3%), idea 57
  (11.3%/1.136/-15.1%) and the ew-all control (10.4%/1.050/-15.9%) to the decimal.
- **128 grid points** (2 universes x 4 books x 4 cadences x 4 costs), all printed.

## Result 1 — daily is strictly worse, everywhere (the one unambiguous finding)

Paired daily differences vs the weekly incumbent, same book, same days, at 10 bps:

| book | universe.json dSharpe (t) | broad dSharpe (t) | dTurnover |
|---|---|---|---|
| v1 | -0.268 (**t -3.21**) | -0.398 (**t -3.99**) | +34x / +36x |
| top20 | -0.116 (**t -2.93**) | -0.196 (**t -4.63**) | +13x / +18x |
| ew-all | -0.082 (**t -2.48**) | -0.066 (**t -2.59**) | +11x / +10x |
| ew-band3 | -0.032 (t -1.61) | -0.000 (t -0.59) | +2x |

At 25 bps daily v1 is -7.8pp/yr CAGR (t -8.68) on universe.json and -9.4pp (t -8.72) on
broad, with MaxDD blowing out to -60%/-75%. Turnover, not signal, is doing this.

## Result 2 — monthly beats weekly, but not on the bar that matters

At 10 bps, monthly minus weekly (paired): v1 **+3.72pp CAGR / +0.295 Sharpe (t +2.64)** on
universe.json and +2.02pp/+0.138 (t +1.26) on broad; top20 +2.05pp/+0.111 (t +2.10) and
+3.24pp/+0.143 (t +2.52); ew-all +1.44pp/+0.094 (t +1.72) and +1.00pp/+0.043 (t +1.25);
ew-band3 **+0.09pp/-0.031 (t +0.15)** and +0.45pp/-0.006 (t +0.57). Monthly is the best
cadence by net Sharpe in 6 of the 8 (universe, book) cells at 10 bps, and the advantage
widens with cost exactly as the whipsaw story predicts (top20 monthly-minus-weekly goes
from +0.111 at 10 bps to +0.183 at 25).

Headline arms at 10 bps (SPY 15.3%/0.890/-33.7%, halves 0.957/0.837, OOS 0.884; 4b bars
H1>0.957, H2>0.837, OOS>0.884, MaxDD>=-20.2%, CAGR>=10.7%):

| arm | universe.json | broad |
|---|---|---|
| top20 W (idea 2 KEEP) | 12.7%/1.093/-18.3%, halves 1.088/1.103, OOS 1.170 | 13.1%/0.958/-20.1%, halves 1.125/0.814, OOS 0.894 |
| **top20 M** | 14.7%/1.204/-19.5%, halves 1.211/1.206, OOS 1.286 | 16.4%/1.101/**-26.1%**, halves 1.328/0.923, OOS 1.009 |
| ew-all M | 11.9%/1.144/-17.0%, halves 1.141/1.151, OOS 1.226 | 11.7%/1.071/**-21.7%** |
| ew-band3 W (idea 57) | 11.3%/1.136/-15.1%, halves 1.113/1.160, OOS 1.234 | 11.1%/1.064/-16.8%, halves 1.163/0.971, OOS 1.074 |
| ew-band3 M | 11.4%/1.105/-18.6% | 11.6%/1.058/**-22.4%** |

`top20 M` is the best-looking book this project has produced on `universe.json` — it passes
4b at **every** cost from 5 to 50 bps, the first arm ever to do so. It dies on the broad
list on drawdown alone: -26.1% against a -20.2% cap, a 5.9pp miss, not a rounding one.
Every monthly and quarterly arm on the broad list fails 4b on MaxDD; quarterly fails it on
both lists in 6 of 8 cells. The mechanism is visible in 2020: quarterly top20 returns +8.1%
(universe.json) and +1.0% (broad) against monthly's +22.9%/+14.0% — a quarterly book cannot
re-enter after a crash it slept through.

**Cross-universe 4b at 10 bps: 2 of 16 arms pass on both lists — `ew-band3` at D and at W.**
Monthly passes on neither pair. Idea 57's candidate is the only book whose 4b pass survives
a cadence change at all, and it is also the book least sensitive to cadence (dSharpe
-0.03..+0.00 across D/W/M): evidence its edge is not an artefact of the weekly calendar.

## Result 3 — rule 8: cadence is not selectable in-sample

Parameters chosen on 2009-2016, evaluated untouched on 2017-2026, at 10 bps:

- `universe.json`: **both** rules pick `ew-all/Q` (IS Sharpe 1.134) -> OOS
  11.7%/1.044/-22.2% vs SPY 15.5%/0.884/-33.7% — **FAILS** the OOS 4b bars (drawdown and
  CAGR). The monthly arms that look best full-sample are not what IS picks.
- `universe_broad.json`: both rules pick `top20/M` (IS 1.239) -> OOS 15.7%/1.009/-26.1% —
  also **FAILS** OOS 4b (drawdown).
- Within-book: the IS-chosen cadence matches the OOS-best cadence in only **2 of 8** cells
  (top20 both times; ew-all, ew-band3 and v1 disagree). Reference: RULES v1 weekly OOS
  7.8%/0.751/-13.8% (universe.json), 6.0%/0.581/-21.2% (broad).

## What this means for RULES

Nothing changes. The live weekly cadence is not optimal on any full-sample measure, but the
alternative that beats it (monthly) fails the capital test on drawdown on the second
universe and is not endorsed by either walk-forward. The defensible reading is narrower and
useful: **do not trade more often than weekly** (t -2.5 to -4.6 against it, and the sign is
identical in 8 of 8 cells), and treat any future candidate's weekly cadence as a parameter
it must survive, as `ew-band3` does and `top20` does not.

## Honest limits

- **Survivorship:** both lists are current constituents; absolute CAGR/Sharpe are
  optimistic. The cadence-vs-cadence comparisons hold the names and days fixed and are far
  less exposed.
- Monthly's win is partly a 2020 artefact (v1 monthly +25.5% vs weekly +8.4% on
  universe.json): a monthly book held through the March crash and was still invested for
  the rebound. That is one episode, and it is the same episode that makes quarterly's
  drawdown unacceptable.
- Month-end and quarter-end rebalancing is a real, crowded calendar effect; nothing here
  separates it from the whipsaw story.
- `top20/M`'s 50-bps 4b pass on `universe.json` is the strongest single cell in the project
  and should be treated with suspicion precisely for that reason — it does not replicate one
  universe over.
