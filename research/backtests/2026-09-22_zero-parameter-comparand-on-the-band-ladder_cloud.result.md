# Idea 2211 (lane cloud, 2026-09-22) — does ANY IS-only chooser on the band ladder beat the zero-parameter rule "take max gross"?

**ANSWERED = NO. It is a coin flip (6 of 12 instances), and on the two panels the record
actually uses, fitting is worth ZERO or LESS than reading no in-sample data at all.**
Script `..._cloud.py`; 300 grid rows (`.grid.csv`), 168 picks (`.picks.csv`), 12 EWALL rows.
**6 of 6 gates PASS** (G3 max|d| 0.000e+00 — the ladder's centre cell IS `rules_v2_weights`;
G1 max|d| 0.000e+00 against `engine.backtest`; G5 54 tickers with `max_1d_move >= 1.0` dropped
from SMALL before pricing, 665 names surviving). **No RULES change; RULES.md / PROTOCOL.md /
scan.py / bot.py / baseline.py untouched.**

## What is new here against idea 2121 (run earlier in this same lane)
2121 priced ONE zero-parameter comparand (MAXGROSS pinned at the live band 0.03) on TWO panels,
as a by-product. This run makes it the question: (1) the comparand is a **family** — all five
bands at g=1.00 are separate zero-parameter rules, so a fitted chooser must beat the *best* of
them, not a lucky one; (2) a **no-band control**, EWALL (equal-weight every priced name at
gross 1.00, weekly — no band, no signal, no parameter), asks whether the band device earns
anything; (3) a **third panel, SMALL** (sub-$2B), which the record has never put this question
to.

## V1 — the answer: a coin flip, decided in the fourth decimal
Best fitted chooser vs best zero-parameter rule on OOS Sharpe: **6 of 12 panel × cost
instances** (beats the *worst* zero-param rule in 12 of 12, which is no achievement — the worst
member is itself a fitted pick's cell). The winning margins are **+0.0012 (U56 @10), +0.0005
(SMALL @10), +0.0016 (U56 @0)** — smaller than the record's own 0.0145 seed-noise floor
(idea 871).

## V2 — the fitting premium is negative where it matters
Mean over cost rungs of (fitted-chooser mean − MAXGROSS-family mean):

| panel | OOS Sharpe premium | OOS CAGR premium | mean OOS rank of a fitted pick (coin = 13.0 of 25) | 4b FULL+OOS fitted / zero-param |
|---|---|---|---|---|
| **U56**  | **−0.0288** | **−1.81 pp** | **18.1 — worse than a coin** | 20 / 15 |
| **B136** | +0.0056 | −1.12 pp | 12.9 — a coin | 14 / 6 |
| SMALL | +0.0334 | −0.22 pp | 6.5 | **0 / 0** |

On U56 at 10 bps, **five of the seven choosers (IS_SHARPE, IS_MINMARG, IS_CAGRSLACK, IS_LEGS,
and the same four on B136) pick `b0.08_g1.00`, which is OOS rank 25 of 25 — the single worst
cell on the ladder.** The zero-parameter `MAXGROSS_b0.02` is rank 5 and `MAXGROSS_b0.03` rank
10. Eight years of in-sample fitting steers *away* from the good cells. SMALL is the only panel
where fitting beats a coin, and it is also the panel where **nothing passes 4b at all**.

## Rule 8, 10 bps, 2017–2026 read once
OOS benchmarks: U56 RULES v2 9.46% / 1.2767 / −12.05%, SPY 15.29% / 0.8751 / −33.72%;
B136 RULES v2 7.85% / 1.1017 / −12.24%; SMALL RULES v2 3.64% / 0.5458 / −14.16%.

| panel | rule | cell | OOS CAGR | OOS Sharpe | OOS MaxDD | rank | 4b FULL | 4b OOS |
|---|---|---|---|---|---|---|---|---|
| U56 | IS_SHARPE / MINMARG / CAGRSLACK / LEGS (fitted) | b0.08_g1.00 | 12.00% | 1.1625 | −19.05% | **25/25** | ✓ | ✓ |
| U56 | IS_CALMAR (fitted) | b0.02_g1.00 | 12.53% | 1.2784 | −15.65% | 5 | ✓ | ✓ |
| U56 | IS_DD (fitted) | b0.02_g0.50 | 6.20% | **1.2796** | −7.99% | **1** | ✗ | ✗ |
| U56 | **MAXGROSS_b0.02 (0 params)** | b0.02_g1.00 | 12.53% | **1.2784** | −15.65% | 5 | ✓ | ✓ |
| U56 | EWALL (no band at all) | — | **18.28%** | 1.1263 | **−29.18%** | — | ✗ | ✗ |
| U56 | RANDCELL (25-cell mean) | — | 9.06% | 1.2366 | −12.41% | 13 | ✗ | ✗ |
| B136 | four gross-blind choosers | b0.08_g1.00 | 10.98% | 1.0921 | −19.50% | 20 | ✓ | ✓ |
| B136 | MAXGROSS_b0.02 (0 params) | b0.02_g1.00 | 10.59% | **1.1211** | −16.18% | 5 | ✓ | ✗ |
| SMALL | five choosers | b0.08_g1.00 | 5.28% | 0.5861 | −19.09% | 5 | ✗ | ✗ |
| SMALL | MAXGROSS_b0.08 (0 params) | b0.08_g1.00 | 5.28% | 0.5861 | −19.09% | 5 | ✗ | ✗ |

**PATH 4a: 1 of 21 fitted picks at 10 bps** (IS_DD on SMALL, `b0.08_g0.50`), and that pick
fails 4b on every leg — it is the de-grossed corner, not a book.

## V3 — the no-band control: the band buys drawdown and nothing else
EWALL — zero parameters, zero signal — earns **OOS CAGR 18.28% (U56) / 18.27% (B136) / 11.48%
(SMALL)** against the band books' 10.5–12.7% / 10.3–11.0% / 4.5–5.3%. It pays for it in
drawdown: **every one of the 60 (panel × cost × band) cells at g=1.00 is shallower than EWALL,
60 of 60**, by 11–25 pp. EWALL therefore **fails 4b on every panel at every cost rung** (its
−29.2%/−32.7%/−44.4% OOS MaxDD blows the −20.2% cap). So the band device is real, and it is a
**drawdown instrument, not a return instrument** — consistent with idea 1534's pooled dMaxDD
readings. But on OOS *Sharpe* it is fragile to cost: band cells beat EWALL 5/5 on U56 at 0–25
bps, **4/5 then 0/5 on B136 at 10 then 25 bps, and 2/5 then 0/5 on SMALL at 0 then 10 bps.**

## The SMALL panel result, which is new to the record
**Zero of 25 ladder cells, zero of 7 choosers and zero of 7 zero-parameter rules clear 4b on
SMALL, at any of the four cost rungs, in any window.** The best OOS Sharpe anywhere on that
panel is 0.5866 against SPY's 0.8751; the CAGR floor is missed by 5–8 pp everywhere. The band ×
gross family — the live rules' own form — **does not port to sub-$2B names at all**, and that
verdict holds even though the SMALL panel's survivorship bias inflates its returns (see below).

## Verdict: KILL. No new KEEP, no RULES change
The zero-parameter rule is not beaten. The question as filed — "how much OOS performance does
the in-sample fitting actually buy?" — is answered: **−0.0288 of OOS Sharpe and −1.81 pp of
OOS CAGR on U56, ≈0 on B136, and on SMALL a positive Sharpe premium in a region where no book
clears the bar.** The record's rule-8 machinery on this family is selecting the worst cell on
the ladder more often than the best, and the honest statement of the family's one real finding
is not "a chooser found a book" but "the band is a drawdown device and gross is an exposure
dial", both of which a rule with no parameters delivers.

## Survivorship (PROTOCOL rule 9)
All three panels are **current-constituent** lists. U56 and B136 are optimistic. **SMALL is the
worst of the three**: it screens names that are sub-$2B *and still listed today*, so every
sub-$2B company delisted, acquired or taken to zero between 2010 and 2026 is absent, and 54
further tickers with a `max_1d_move >= 1.0` data artefact were dropped before pricing (665
names survive). Its absolute CAGR is severely overstated and its drawdown severely understated
— which makes the SMALL 4b failure *stronger*, not weaker: the family fails on a tape that is
already tilted in its favour. No absolute number in this run is an achievable return.
