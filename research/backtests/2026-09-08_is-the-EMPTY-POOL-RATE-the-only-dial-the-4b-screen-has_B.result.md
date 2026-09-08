# Idea 419 — is the EMPTY-POOL RATE the only dial the 4b screen has?  (lane B, 2026-09-08)

**ANSWERED. The queue's premise is FALSIFIED: the rate is NOT the only dial. The screen has a
second, real and monotone dial — its DD bar `delta` — which runs a drawdown/return exchange
INSIDE the live pool, and the record's committed pair (phi 0.70, delta 0.60) sits almost
exactly on that dial's zero crossing. That is why idea 163 measured a live-pool null.
No book promoted. PROTOCOL.md, RULES.md, scan.py, bot.py, baseline.py untouched.**

Corpus: idea 163's census, unchanged — 132 / 142 / 151 / 416, 210 (file,cell) pairs, 150
distinct (panel, book, cost) cells, 3,570 arm-rows, 4 panels, rungs 0/10/25 bps, 4
deterministic selectors. Two tuned parameters (phi, delta), **swept**: 7 x 7 = 49 grid points,
every one reported in `.dial.csv` / `.keeppaths.csv` / `.walkforward.csv`. 41,160 swept rows.

## Gates — this run earns the right to read the record

* **G1 screen identity.** The screen is rebuilt from RAW grid columns, with each panel's SPY IS
  bars backed out of the committed margins (|SPY_IS_MaxDD| = (IS_m_DD + |IS_MaxDD|)/0.60,
  SPY_IS_CAGR = (IS_CAGR − IS_m_CAGR)/0.70) and asserted constant within panel (spread 3.9e-16).
  At (0.70, 0.60) the rebuild equals the committed admission column on **3,570 of 3,570 rows**.
* **G2 pick identity.** Every deterministic committed pick reproduces arm-for-arm:
  **144/144, 384/384, 576/576, 576/576**. K_Random excluded from both gates and every reading.
* **Idea 163 reproduces exactly** at the committed point: live-pool moved d OOS MaxDD
  **−0.690 pp, n 82, t −1.35**, and the empty-pool share of the pooled drawdown effect
  **95.3%** — the two numbers idea 419 was written from.

## 1. The dial calibrates, and it is wide

E (empty-pool rate) spans **32.7% to 100.0%**; mean admitted spans 0.00 to 8.07 of 17 arms.
The most permissive grid point still abstains 32.7% of the time — that residual is the FIXED
core (IS_m_H1 > 0, IS_m_H2 > 0), not the dial, and it is not swept here (2-parameter cap).

## 2. The regression the queue asked for — and why it does not settle anything

Pooled over 49 grid points: `d_OOS_MaxDD = −0.964 pp + (−2.212 pp) x E`, **R2 0.894**, t −19.91;
`d_OOS_CAGR = +0.554 pp + (+1.075 pp) x E`, R2 0.921, t +23.32. The dial law transfers: fitted
on the OLD corpus (132+142) and read on the NEW, non-overlapping one (151+416), the MaxDD slope
is −2.284 -> −2.210, **ratio 0.968** (rule 8 on the law itself).

**Stated before the number was used:** the pooled d is E-weighted by construction
(d = E·d_EMPTY + (1−E)·d_LIVE) and d_EMPTY is near-constant across the grid (−3.03 to −4.17 pp),
so a high R2 here is most of the way to an identity. It is not evidence for the queue's claim.

## 3. The live-pool leg is NOT null, and it is not a function of the rate

| delta (IS DD bar) | 0.20 | 0.40 | 0.60 | 0.80 | 1.00 | 1.25 | 1.50 |
|---|---|---|---|---|---|---|---|
| live-pool d OOS **MaxDD** (pp, mean over phi) | **+4.50** | **+2.95** | **+0.31** | −3.44 | −4.31 | −5.61 | −5.80 |
| live-pool d OOS **CAGR** (pp) | −2.10 | −1.84 | −0.59 | +1.76 | +2.96 | +3.71 | +3.80 |

Monotone, sign-flipping between delta 0.60 and 0.80, and mirrored on CAGR. The leg is
**significant (|t| >= 2) at 33 of 41 grid points (80.5%)** that have >= 2 live moves; the sign
holds in 4 of 4 files (−0.52 / −2.81 / −3.21 / −2.67 pp), including the out-of-corpus file 416.

Regressed across grid points: `live d_OOS_MaxDD ~ E` gives **R2 0.085**; `~ delta` gives
**R2 0.750** (slope −7.90 pp per unit delta) against `live d_OOS_CAGR ~ delta` R2 0.639
(+5.29 pp). **The abstention rate explains 8.5% of the live leg; the DD bar explains 75%.**

## 4. The rate-matched null — the screen is not a coin

A coin abstaining in k of n cells at random IS an exposure switch. Against it (2,000 seeded
draws per point): **z(total) |z| < 2 at only 5 of 41 points (12.2%), mean −4.02**, i.e. the
screen's total effect is reliably WORSE on OOS drawdown than a rate-matched coin. Splitting it,
**z(abst) — where it abstains, live picks held out — is inside |2| at 25 of 41 (61.0%), mean
−1.59**: the *placement* of the abstention is close to uninformative, and the departure from
the coin comes from the live screening. Both columns near zero is what "the rate is the only
dial" would have looked like; only one of them is.

## 5. KEEP paths (PROTOCOL rule 4), all 49 grid points, distinct cells

4a(v2): unscreened 31/600, screened **20 to 32** across the grid (net positive at only 6 of 49
points, max +1). 4b(full): 86/600 vs **46 to 129**. 4b(OOS window): 94/576 vs **50 to 131**.
BOTH PATHS: 6/576 unscreened vs **0 to 9** screened. Net swaps regress on E at −74.5 (4b) and
−16.3 (4a) passes per unit E, R2 0.71 — the KEEP-path effect IS mostly the rate, unlike the
drawdown effect. **Nothing here is a KEEP-candidate: no new book exists, and the screened pick
is a per-cell object, not a policy that can be traded.**

## 6. Levels, freshly computed (rule 8: IS <= 2016-12-31, OOS 2017-01-01.. read once)

SPY OOS **15.45% / 0.8820 / −33.72%** -> 4b OOS bars CAGR >= 10.82%, |MaxDD| <= 20.23%.
RULES v2 (live) OOS @10 bps **9.53% / 1.2851 / −12.05%** (@25 9.24% / 1.2483 / −12.09%).
Census pooled OOS means, screened / unscreened / do-nothing control, at the committed point:
**13.52% / 0.932 / −24.45%**, 12.29% / 0.912 / −22.46%, 13.97% / 0.933 / −25.63%. Along the
whole dial the screened policy's OOS MaxDD level regresses on E at −2.21 pp (R2 0.894) and its
OOS CAGR at +1.08 pp (R2 0.921) — an exchange of **−0.486 pp OOS CAGR per pp of OOS MaxDD**.
Survivorship (idea 54) inflates every level; read the contrasts, not the levels.

## What this changes

Idea 163's "the screen does nothing to drawdown inside a live pool" is correct **at its
setting and nowhere else**. The screen is two instruments wearing one name: an abstention rate
(which, per §4, is placed no better than a coin and should indeed be re-specified as an
explicit exposure switch, as idea 419 proposed) **and** a live-pool drawdown/return exchange
governed by delta, which is a real, monotone, priced dial the record has never sold as one.
Any future use of the IS-4b screen should state BOTH, and should not read the committed
delta = 0.60 as representative: it is the exchange's zero.

Mechanism hypothesis, flagged as untested here: idea 420 measured OOS drawdowns **1.49x deeper
than IS** on 96.2% of arms, so an IS bar of delta = 0.60 admits arms whose OOS drawdown is
roughly 0.9x SPY's — no protection at all. The crossing sitting near 0.60-0.80 is what that
window bias predicts. Idea 421 (re-state IS DD bars as ranks or scale them by 1.5) is the
direct test and is already queued.
