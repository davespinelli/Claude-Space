# Idea 88 — vol-cap-as-a-satellite-clause — **KILL (percentile wording); satellite stays PARK**

Script `2026-09-04_vol-cap-as-a-satellite-clause_B.py` · lane B · 2026-09-04 · 10 bps, weekly,
next-day execution · 48 points (2 universes × 3 books × [1 control + 7 gate specs]), all
reported · cap **fixed** at 5%/name, funding **fixed** at `matched` · harness reproduces idea 2's
KEEP row to the decimal (12.7%/1.093/-18.3%, halves 1.088/1.103), control equivalence 1.4e-17,
percentile-clause look-ahead check 0.000e+00.

---

## The question, answered before any backtest

RULES v1 gates on `vol20 < 0.60`. Where does 0.60 sit in each instrument's **own** vol20
distribution over the eval window?

| instrument | median vol20 | share of its own days below 0.60 | own p50 / p70 / p90 |
|---|---|---|---|
| median equity name (u56, n=55) | 0.185 | **98.9%** | 0.185 / 0.223 / 0.331 |
| median equity name (broad, n=134) | 0.212 | **98.3%** | 0.212 / 0.265 / 0.372 |
| SPY | 0.129 | **99.5%** | 0.129 / 0.167 / 0.263 |
| BTC-USD | 0.532 | **58.8%** | 0.532 / 0.699 / 0.956 |
| ETH-USD | 0.714 | **30.2%** | 0.714 / 0.872 / 1.201 |

If `vol20 < 0.60` were a percentile statement that column would be flat. It is not: 0.60 is a
**p99 tail exclusion on equities** (8 of 55 / 8 of 134 names never touch it at all) and a
**p59 / p30 median exclusion on the satellite**. The same six characters are two different
rules depending on what they are pointed at, which is the whole reason idea 15 (cap protects a
satellite) and idea 56 (cap destroys small caps) could both be true. Confirmed.

## Result 1 — on Sharpe the satellite vol clause is pure cost, monotonically

Mean dSharpe vs each book's own crypto-free control, averaged over the 3 books:

| spec | either-on | u56 dSharpe | u56 dMaxDD | broad dSharpe | broad dMaxDD |
|---|---|---|---|---|---|
| abs0.45 | 14.9% | +0.070 | +0.1% | +0.068 | +0.2% |
| abs0.60 (**RULES v1's own**) | 25.7% | +0.072 | -0.1% | +0.074 | -0.7% |
| abs0.80 | 35.6% | +0.096 | -0.9% | +0.099 | -1.7% |
| p50 | 28.3% | +0.035 | -2.0% | +0.042 | -1.6% |
| p70 | 35.6% | +0.074 | -2.0% | +0.080 | -1.8% |
| p90 | 41.3% | +0.119 | -2.0% | +0.123 | -1.7% |
| none (200d only) | 45.2% | **+0.147** | -2.0% | **+0.152** | -1.7% |

`none` is the highest-Sharpe arm in **6 of 6** (book, universe) cells; the spec ordering is
near-identical across universes (Spearman +1.000 / +0.893 / +1.000 for v1 / CAND20 / EWall).
Every arm beats its own control on Sharpe (21/21 on each list) with paired t +0.96..+3.04.

## Result 2 — but 4b is a drawdown bar, and there the ordering reverses

Cross-universe 4b: **9 of 24 points pass**, and on the ranked book only the two **tightest
absolute** specs survive.

| book | passing specs (both lists) | failing specs and why |
|---|---|---|
| v1 | none | H1, H2, OOS, CAGR everywhere |
| CAND20 | **abs0.45, abs0.60** | abs0.80, p50, p70, p90, none — all `DD` on broad |
| EWall | all 7 | — (this book has DD headroom to spare) |

Every CAND20 failure is `DD` and nothing else. Idea 15's finding replicates exactly: **the vol
clause is a drawdown instrument on a satellite, not a return one**, and it is the only lever
that moves a satellite book across 4b's drawdown cap.

## Result 3 — absolute beats percentile, at matched exposure, on both asset classes

The comparison is clean because two pairs sit at matched satellite exposure:

- **abs0.80 vs p70** — identical either-on (35.6% both): abs0.80 gives dSharpe +0.096/+0.099
  vs p70's +0.074/+0.080, and better MaxDD on u56 (-0.9% vs -2.0%).
- **abs0.60 (25.7% on) vs p50 (28.3% on)** — abs0.60 wins at *lower* exposure: +0.072/+0.074
  vs +0.035/+0.042, dMaxDD -0.1%/-0.7% vs -2.0%/-1.6%.

Mechanism: the expanding percentile **ratchets**. After each vol regime shift the instrument's
own p70 rises, so a percentile clause keeps re-admitting the satellite at ever-higher absolute
volatility — it is a rule that gets looser exactly as the asset gets more dangerous. That is
why every percentile spec carries ~2pp more drawdown than the absolute spec at the same
exposure.

**The equity-side diagnostic says the same thing, harder.** Rewriting the *equity* gate as a
percentile (EWall, no verdict depends on this):

| spec | pass rate | u56 Sharpe / 4b-fail | broad Sharpe / 4b-fail |
|---|---|---|---|
| abs0.60 (live) | 97.5 / 98.1% | 1.050 / `CAGR` | 1.027 / `-` |
| abs0.80 | 99.2 / 99.4% | 1.057 / `-` | 1.061 / `-` |
| p90 | 96.5 / 96.5% | 1.070 / **`DD`** | 1.044 / **`DD`** |
| p70 | 84.3 / 84.0% | 1.036 / **`DD`,CAGR** | 1.002 / **`DD`,CAGR** |
| p50 | 67.5 / 66.8% | 0.884 / H1,**`DD`**,CAGR | 0.763 / H2,OOS,CAGR |

Every percentile spec introduces a drawdown failure that **no absolute spec has**, on both
lists. Adopting the percentile wording into RULES would break the equity book to fix a
satellite clause that is unreachable anyway (Result 4).

## Result 4 — rule 8: the passing specs are unselectable (idea 15's failure shape, again)

- **PROTOCOL rule 8** (IS ≤2016, OOS 2017+): S1 and S2 both pick `CAND20/p90` on u56
  (OOS 16.7% / 1.270 / -19.7%; SPY OOS 15.5%/0.884/-33.7%, v1 baseline 7.8%/0.751/-13.8%) and
  `EWall/p90` on broad (OOS 13.2% / 1.144 / -20.1%; v1 baseline 6.0%/0.581/-21.2%). Both clear
  their OOS 4b bars — but `CAND20/p90` **fails full-sample cross-universe 4b on broad's DD**,
  i.e. the rule buys an arm the protocol then rejects. Spearman(IS, OOS) +0.932 / +0.879 is the
  **equity book's** ordering: BTC's 200d gate starts 2015-07-02 and ETH's 2018-08-27, so the IS
  window holds ~1.5 yr of BTC and **zero ETH** and cannot see the clause at all.
- **Crypto-era walk-forward** (IS 2018-09→2021-12, OOS 2022+): S1 picks `none` in **6 of 6**
  cells and **not one clears the OOS 4b bars** (u56 `EWall/none` 9.1%/0.858/-16.6% vs the
  -14.7% cap; broad `EWall/none` 8.0%/0.791/-18.4%). Spearman collapses to +0.541 / +0.475.

IS Sharpe is monotone in looseness while the 4b drawdown cap is not — so every in-sample rule
overshoots to `none`/`p90`, and the arms that actually pass (`abs0.45`, `abs0.60`) are never
selected. This is idea 87's interior-pass problem verbatim, on a third idea.

## Result 5 — cost

The satellite's dSharpe **widens** with cost on every arm (u56 EWall `none` +0.133 @10 bps →
+0.178 @100) because crypto weight displaces high-turnover equity weight. But absolute
drawdown blows out (-18.8% → -31.4% over the same range), so **no arm passes 4b at
crypto-realistic cost**. 10 bps is an equity assumption; retail crypto spreads are larger.

## Verdict and recommended RULES wording

**KILL the percentile expression. Keep the absolute number, and say what it is for.**

Proposed clause, for the Sunday review, replacing nothing in the equity book:

> **Volatility gate.** An instrument is eligible only while `vol20 < 0.60`. This is an
> **absolute** threshold and is deliberately not a percentile of the instrument's own history:
> on the large-cap lists 0.60 sits at ≈p99 of a typical name's own vol (it is a tail
> exclusion that costs nothing), while on a high-volatility satellite it sits at p59 (BTC) /
> p30 (ETH), where it functions as a **drawdown cap, not a return filter**. Any instrument
> whose own median vol20 exceeds 0.35 is a satellite: it may be held only under a per-name
> weight cap, and the 0.60 gate is what keeps it inside the book's drawdown budget. Do not
> re-express this gate as a percentile — a percentile ratchets looser as the instrument gets
> more volatile, which costs ≈2pp of MaxDD at matched exposure on the satellite and
> introduces a 4b drawdown failure on the equity book that the absolute form does not have.

**The satellite itself remains PARK, unchanged from idea 15** — `CAND20/abs0.45`,
`CAND20/abs0.60` and all seven `EWall` specs pass cross-universe 4b at 10 bps, but no
in-sample rule can reach them, and the survivorship problem below is not fixable with the data
that exists. **Recommended AGAINST adoption.**

## Caveats (none removable in this sandbox)

Current-constituent survivorship on both equity lists, one-directional. BTC and ETH are the
two crypto **survivors**; LUNA, FTT and the 2014-18 altcoin field are absent, and a loose vol
clause is exactly what would have held the dead names — so Result 1's "looser is better" is
biased in precisely the direction it points. Crypto trades 24/7 on an equity-trading-day
index: weekend moves land in the Monday bar, understating realised drawdown and overstating
the gate's tradeability. 2017 (BTC +1425%) sits inside H1 and is a large share of every
satellite arm's H1 advantage. The 0.35 median-vol threshold in the proposed wording is a
description of this panel, not an estimated parameter.
