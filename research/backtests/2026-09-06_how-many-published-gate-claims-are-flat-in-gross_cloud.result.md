# Idea 277 — how-many-published-gate-claims-are-flat-in-gross (cloud, 2026-09-06)

**ANSWERED: the flatness is an IDENTITY, not a finding — so no published *Sharpe* verdict can
be a gross artefact through this channel. The exposure channel lands on CAGR and MaxDD, where
it carries a median 35–40% of a published difference and the whole of it in ~19% of cases.
The record's real exposure is not the comparisons it can audit — it is the 90.7% it cannot.
Rules unchanged. No new book. 4a 0/144; every 4b pass is a gross-ladder point or worse.**

## Gates (before any new number was read)
- `fast_backtest_g` vs `engine.backtest`: max |diff| **6.9e-18**; vs idea 171's `fast_backtest`: **0.0**.
- LIVE RULES v2 on U56 @10bps reproduces the CHANGELOG row **exactly**: 8.66% / 1.2056 / −12.05%,
  halves 1.2259 / 1.1908.
- `weights_gate(band3, 0.75, dg)` is asserted **identical** to `baseline.rules_v2_weights`
  (max |diff| < 1e-12), so the gate family contains the live book as a point, not as an analogue.

## Q1 the structural claim idea 274 did not make
A constant-gross un-gated book scales **both** its returns and its turnover linearly in `g`:
|r(g=0.50) − 0.5·r(g=1.00)| max = **2.6e-03**, same for turnover **1.6e-02**. Sharpe is therefore
invariant *by construction* up to the cash-drift renormalisation. **Idea 274's 0.0023 is that
renormalisation.** It is not evidence that gross carries no information; it is arithmetic.

## Q2 the ladder as an exchange rate (17 points × 3 panels × 2 rungs, all reported)
| panel | rung | Sharpe span | CAGR span | MaxDD span |
|---|---|---|---|---|
| U56 | 10 | **0.0023** | 14.24 pp | 22.78 pp |
| U56 | 25 | 0.0039 | 14.08 pp | 22.80 pp |
| B136 | 10 | 0.0013 | 15.19 pp | 25.45 pp |
| B136 | 25 | 0.0030 | 15.02 pp | 25.46 pp |
| SMALL439 | 10 | 0.0029 | 10.24 pp | 35.34 pp |
| SMALL439 | 25 | 0.0017 | 9.92 pp | 35.61 pp |

P1 **TRUE** (span < 0.01 in 6/6, max 0.0039 — idea 274's 0.0023 is exactly U56@10, not a
one-panel accident). P2 **TRUE**. The ladder is a pure scale dial in every cell.

## Q3 the gated arms priced twice (4 instruments × 2 conventions × 3 gross × 3 panels × 2 rungs = 144)
- P3 half-holds: `rw` realised gross is within **0.0003** of nominal everywhere; `dg` runs
  **−0.17** (large caps) and **−0.34** (small) below nominal on average — but only −0.018 at the
  bottom of the ladder, so the pre-registered "at least 0.10 below" fails at g = 0.50.
- **P4's sign half FAILS and its magnitude half holds.** Re-matching a `dg` arm to the ladder at
  its own realised gross moves dSharpe by at most **0.0023** and flips **0/144** signs — because a
  de-grossing gate and the gross channel push CAGR and drawdown the *same* way, so the sign
  survives while the size does not.
- The reportable statistic is the **share**: on `dg` arms the gross channel alone accounts for a
  mean **59.4%** of the published dCAGR and **54.0%** of the published dMaxDD, and a *majority* of
  the difference in **54/72** cells on each. On `rw` arms the share is **0.000** — the convention,
  not the instrument, is what creates the exposure.

## Q4 the census (this run's own outputs excluded)
| | count |
|---|---|
| committed grid CSVs in `research/backtests/` | 853 |
| … carrying a Sharpe-like column | 541 |
| … **and** gate/overlay vocabulary — the census population | **323** |
| … **gross-auditable** (a realised-gross column is committed) | **30 (9.3%)** |
| … nominal-gross-only | 90 |
| … no gross column at all | 203 |

Two files (`gross-as-the-missing-third-bar`, `gross-dispersion-not-gross-level`) carry an
`m_GROSS` column that ranges to **−0.22** — it is not a gross level, and they are excluded and
flagged rather than scored.

**5033 within-group comparisons** (no comparison crosses a panel or a cost rung) over 25 files
and 278 homogeneous groups:

- across a gross gap > the ladder's own Sharpe span (0.0023): **3851/5033 (76.5%)** ← the queue's
  literal count
- across a gross gap > 0.05 of realised gross: 2879/5033 (57.2%)
- published **dSharpe** inside what the ladder buys: **299/5033 (5.9%)**
- published **dCAGR** inside what the ladder buys: **947/4849 (19.5%)**
- published **dMaxDD** inside what the ladder buys: **935/4849 (19.3%)**
- gross-channel share of a published dCAGR (|dCAGR| > 1pp, n = 4038): median **+0.353**
- gross-channel share of a published dMaxDD (|dMaxDD| > 1pp, n = 4275): median **+0.401**
- majority-exposure (share > 0.50): dCAGR **40.1%**, dMaxDD **43.7%**

P5 **TRUE**. The queue's premise ("comparing CAGR/MaxDD scale, not information") is confirmed on
the CAGR/MaxDD axes and **refuted on the Sharpe axis** — the flatness that motivated the worry is
exactly what makes a Sharpe verdict immune to it.

## Q5 rule 8 (IS ≤ 2016-12-31 chooses, OOS ≥ 2017-01-01 read once)
The IS-Sharpe chooser beats do-nothing (the live book) in **2 of 6** cells, mean OOS Sharpe
**0.876 vs 0.967** — P6 holds, the **12th** "selection loses to doing nothing" instance in the
record. Against its own **gross-matched ungated ladder point** it wins 4/6 (mean 0.951), i.e. the
gates do carry OOS information the ladder does not — but less than doing nothing carries.
Spearman(IS, OOS) +0.14 … +0.95.

## Q6 both KEEP paths
**4a: 0/144.** **4b: 17/144** (U56 10, B136 7, SMALL439 0). **9 of the 17 are beaten by their own
gross-matched ungated ladder point** — including 7 of the 9 `rw` passes. No candidate; no memo.

## Caveats
SURVIVORSHIP: U56/B136/SMALL439 are current-constituent lists and it runs *against* the un-gated
arm, so a delisting-aware panel would make the gates look better, not worse — stated, not
adjusted. The small panel is secondary (ideas 39/49/136: the gate is inverted there). Costs are
flat linear bps. The census reads what the record **committed**; a parent that computed realised
gross and did not write it to CSV is counted un-auditable, which is a schema statement, not a
judgement of that parent.

## What PROTOCOL should carry
A realised-mean-gross column beside every published arm — the 9.3% auditability rate, not the
19.5%, is the finding.
