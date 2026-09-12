# Idea 566 — is every DECILE-LADDER claim in the record a DECILE-1 claim?

**Run:** cloud, 2026-09-12.
**Script:** `2026-09-12_is-every-DECILE-LADDER-claim-in-the-record-a-DECILE-1-claim_cloud.py`
**Verdict: ANSWERED = the premise is INVERTED. Dropping decile 1 flips the sign of only 2 of 16
rebuilt ladders and *strengthens* the median ordering (|rho| ratio 1.231x). The bin that carries
these orderings is decile **10**, not decile 1: trimming the HIGH end cuts median |rho| to 0.780
(FULL) / 0.842 (OOS) and costs 6 of 16 sign survivals at TRIM=2 OOS. KILL for capital — the single
book that passes both KEEP paths dies at 25 bps and holds names trading $55k/day.**

## The headline table — trim survival over 16 rebuilt ladders

| window | trim | end | sign survives | median \|rho\| ratio | median rho (full) |
|---|---|---|---|---|---|
| FULL | 1 | **LOW (D1 dropped)** | **14/16** | **1.231** | +0.592 (+0.442) |
| FULL | 1 | HIGH (D10 dropped) | 15/16 | **0.780** | +0.233 (+0.442) |
| FULL | 2 | LOW | 14/16 | 1.296 | +0.667 |
| FULL | 2 | HIGH | 14/16 | 0.779 | −0.024 |
| OOS | 1 | LOW | **16/16** | 1.063 | +0.500 (+0.394) |
| OOS | 1 | HIGH | 13/16 | 0.842 | +0.167 |
| OOS | 2 | LOW | 14/16 | 1.117 | +0.679 |
| OOS | 2 | HIGH | **10/16** | 0.821 | −0.119 |

Read the LOW rows against the HIGH rows: the queue's worry was that the thin bottom corner carries
the ordering. It does not. **Decile 1 fights the ordering** — remove it and rho gets stronger in
median — while decile 10 is what holds it up.

## The ladders (Sharpe by decile, gross 0.75, weekly, 10 bps)

16 ladders = 3 panels × {advQ, volQ, momQ, capQ where available} × {MA-RS, MA-DG}, 160 books.
A representative row per family (MA-DG):

| panel / family | D1 … D10 | rho full | rho trim1 | D1 share of D10−D1 gap |
|---|---|---|---|---|
| SMALL663 advQ | 1.808 0.932 0.818 0.635 0.397 0.328 0.149 0.193 0.009 −0.217 | −0.988 | −0.983 | **+43.3%** |
| SMALL663 capQ | 0.535 0.752 0.725 0.430 0.605 0.561 0.462 0.424 0.539 0.479 | −0.455 | −0.583 | −385% |
| SMALL663 momQ | 0.620 0.211 0.180 0.092 0.081 0.114 0.301 0.174 0.405 0.722 | +0.212 | **+0.517** | −403% |
| B136 momQ | 0.598 0.515 0.105 0.467 0.659 0.502 0.669 0.722 0.683 1.057 | +0.758 | +0.850 | −18.1% |
| U56 momQ | 0.458 0.311 0.446 0.258 0.487 0.589 0.479 0.660 0.701 1.189 | +0.855 | +0.900 | −20.0% |

A **negative** D1 share means removing decile 1 makes the ladder's end-to-end gap *larger*: D1 sits
on the wrong side of its own ordering. That is the general shape here — median share **−25.3%**,
and only **2 of 8** small-panel cells put ≥50% of the gap in D1, so **H_CORNER FAILS**.

**On idea 313 specifically.** Its statistic is different (the capQ-vs-advQ *per-decile sign gap*,
not the D10−D1 Sharpe gap), so this is not a reproduction and is not reported as one. Measured in
its general form on today's **663**-name panel — idea 313 ran on the **430**-name vintage (idea 796
documented that growth) — D1 carries **22.8%** (MA-RS) and **32.1%** (MA-DG) of Σ\|capQ−advQ\|
against its published 81% / 77%. The D1 gap is still the single largest term (−0.82 / −1.27 against
a D2–D10 mean of +0.14 / +0.19); what has changed is that the other nine deciles now carry two
thirds of the mass.

## The census

**109** distinct decile/quantile *ordering* claims over **36** committed files (803 memos +
LEADERBOARD + CHANGELOG; QUEUE excluded — proposals are not claims).

- **57 (52.3%)** name an extreme bin explicitly (D1/D10/top/bottom decile).
- **1 (0.9%)** mentions a trimmed ladder at all → **H_CENSUS PASS** (bar < 5%).

So the record's ladder claims are overwhelmingly written *about* a corner and essentially never
show what the ladder looks like without one. The queue's proposed remedy is right; its direction
is not. **The bin that needs publishing beside the full ladder is the TOP one.**

## Rule 8 walk-forward

Decile picked by IS (≤2016) Sharpe on the FULL ladder and again on the TRIMMED (D1 dropped) ladder;
OOS (≥2017) read once.

- The trim **changes the pick in 4 of 16** cells.
- The IS-best decile is an **extreme bin in 12 of 16** cells → **H_PICK PASS**. Rule 8's own
  selector is a corner selector, which is the operational version of the queue's worry and the one
  that survives.
- OOS Sharpe effect of the trim: median **+0.0000**, mean **−0.0893**, range **−1.2597 … +0.2656**.
  The whole cost sits in the two SMALL cells where the IS pick *was* D1 (advQ MA-DG OOS Sharpe
  2.108 → 0.848, OOS CAGR 12.66% → 6.41%).

| panel / family / form | pick FULL | pick TRIM1 | OOS Sharpe F → T | OOS CAGR F → T | RULES v2 OOS Sharpe | SPY OOS Sharpe |
|---|---|---|---|---|---|---|
| SMALL663 advQ MA-DG | **1** | 2 | 2.108 → 0.848 | 12.66% → 6.41% | 0.560 | 0.877 |
| SMALL663 volQ MA-DG | 1 | 2 | 0.499 → 0.173 | 2.78% → 1.02% | 0.560 | 0.877 |
| B136 volQ MA-DG | 1 | 9 | 0.548 → 0.814 | 2.10% → 8.39% | 1.106 | 0.877 |
| B136 / U56 momQ (4 cells) | 10 | 10 | unchanged (0.98–1.17) | 17.6–27.8% | 1.106 / 1.278 | 0.877 |

## KEEP paths — and why the one passer is not capital

Of 160 books: **4a 2, 4b 1, BOTH 1** — all on `SMALL663 / advQ / MA-DG / decile 1`. Binding 4b legs
across the 160: H1 141, H2 142, OOS 143, DD 103, CAGR 142.

That single passer is the **least-liquid decile of a survivorship-biased sub-$2B panel**, and it
does not survive contact with its own trading costs:

| cost | CAGR | Sharpe | MaxDD | OOS CAGR / Sharpe / MaxDD | 4a | 4b |
|---|---|---|---|---|---|---|
| **10 bps** (PROTOCOL) | 10.11% | 1.808 | −9.94% | 12.66% / 2.108 / −6.65% | True | **True** |
| 25 bps | 9.00% | 1.617 | −10.81% | 11.62% / 1.943 / −7.90% | True | **False (CAGR)** |
| 50 bps | 7.17% | 1.299 | −13.28% | 9.89% / 1.667 / −9.96% | False | False (H1, CAGR) |
| 100 bps | 3.59% | 0.667 | −19.31% | 6.53% / 1.116 / −14.21% | False | False (H1, CAGR) |

**Median 20-day dollar volume of the names actually held: $55,280/day.** A $1m position is **18.1x
the median holding's entire daily volume**. At that size 10 bps is not a cost assumption, it is a
fiction; the book fails 4b at the first realistic rung. **No KEEP is claimed. H_NOFREE PASS.**

## Gates

| gate | reading | bar | verdict |
|---|---|---|---|
| G1 identity (fast vs `engine.backtest`) | 1.388e-17 | 1e-12 | PASS |
| G2 partition (10 masks disjoint, covering, balanced) | overlap 0, coverage 1.000000, count spread 1 | 0 / 1.0 / 1 | PASS |
| G3 static (capQ constant in time) | max daily rank change 3.344e-03 — non-zero only where a name enters/leaves the panel | — | PASS |
| G4 census (idempotent harvest) | 109 distinct claims | — | PASS |

## Hypotheses

H_CORNER **FAIL** (D1 carries ≥50% of the gap in 2 of 8 cells; median share −25.3%) ·
H_FLIP **FAIL** (2 of 16 sign flips) · H_MAG **FAIL**, in the informative direction (median |rho|
ratio **1.231**, i.e. the trim *strengthens* the ordering) · H_CENSUS **PASS** · H_PICK **PASS** ·
H_NOFREE **PASS**.

Three of six pre-registered hypotheses fail, and the two that fail hardest fail *against* the
queue's premise. That is the result.

## Caveats, stated plainly

- **capQ is look-ahead by construction**: a single present-day market cap broadcast over 2010–2026,
  from `research/deepvalue/universe_under2b.csv`, which the filings job rewrites nightly (idea 565
  measured 430/434/435 coverage on three consecutive days). Today: 720 rows, 663 of 663 panel names
  covered. It is included only because it is idea 51's and idea 313's own characteristic. advQ,
  volQ and momQ are point-in-time and carry no such defect.
- **Survivorship:** the small panel is today's sub-$2B screen (52 tickers with max_1d_move ≥ 1.0
  dropped first, per PROTOCOL); B136 and U56 are current constituents. Dead names are absent, so
  every return is biased upward — and decile 1 of advQ, the thinnest and most distressed bin, is
  biased most of all. The 4b passer above is exactly the book this bias most flatters.
- The idle fraction earns zero (the record's convention; idea 576/799 priced what that is worth).
  Gross is fixed at 0.75 for all 160 books, so the convention cannot drive the *ordering*, but
  MA-DG holds more cash than MA-RS and the two forms are compared only within themselves.
- 16 ladders is a small denominator for "a majority of ladders". The sign result (14–16 of 16) is
  comfortable; the magnitude result (1.231x median) rests on 16 paired readings and is reported
  with its window splits rather than as a single number.

## What the record should do

PROTOCOL should require a **top-bin-trimmed** ladder beside every published decile/quantile
ordering — not the bottom-bin trim the queue proposed. 52.3% of the record's 109 committed ordering
claims name an extreme bin and 0.9% ever show the ladder without one; on these 16 rebuilt ladders
the ordering survives losing D1 and does not reliably survive losing D10 (10 of 16 at TRIM=2 OOS).
Separately, rule 8's IS selector lands in a corner in 12 of 16 cells, so **every rule-8 decile pick
should state which bin it picked and what the next-best bin returned out of sample.** Proposal for
Sunday review only — no rules change and no KEEP from this run.
