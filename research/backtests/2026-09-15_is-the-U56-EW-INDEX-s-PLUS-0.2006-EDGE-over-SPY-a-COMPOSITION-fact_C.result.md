# Idea 924 (lane C, 2026-09-15) — is the U56 equal-weight index's +0.2006 edge over SPY a COMPOSITION fact?

**ANSWERED = NEITHER OF THE QUEUE'S TWO CANDIDATES. The edge is not the ETF panel and it is not
equal-weighting/size — it is carried, at 159% of its own total, by the 20 HAND-PICKED MEGA-CAP
SINGLE NAMES, and 80% of that sleeve's own edge is NAME SELECTION rather than weighting. Both ETF
sleeves are DRAGS. KILL for the queue's composition premise; KILL for promoting any of the 27
4b-clearing cells this run found (rule 8 reaches 0 of them); PARK, survivorship-bounded, for
SINGLE20/VT. Nothing promoted, no RULES / PROTOCOL change.**

Script `2026-09-15_is-the-U56-EW-INDEX-s-PLUS-0.2006-EDGE-over-SPY-a-COMPOSITION-fact_C.py`.
8 sleeves × 3 weightings × 20 gross rungs × 4 cost rungs × 17 windows = **32,640 scored rows**,
plus an exact 3-player Shapley decomposition on every window, two chain decompositions (both
orders), a 56-name leave-one-out and 10 rule-8 picks. Two tuned parameters, the queue's own:
**sleeve** (8 levels, all reported) and **weighting** (3 levels, all reported). **GATES 8 of 8
PASS**, including an exact cross-run reproduction of idea 922's leg-window numbers.

## The decomposition (leg window ISH1_HALF, 2009-01-13 … 2013-01-07, 1,003 days, g=0.75, 10 bps)

The partition **EQETF24 + SINGLE20 + NONEQ12 = ALL56** is exhaustive and disjoint (G6), so the
Shapley values are exact and order-independent (residual 5.6e-17, G5):

| sleeve | Shapley φ | share of +0.2006 |
|---|---|---|
| **SINGLE20** (20 mega-cap single names) | **+0.3193** | **+159.2%** |
| EQETF24 (SPY, QQQ, IWM, sectors, …) | −0.0423 | −21.1% |
| NONEQ12 (TLT/IEF/SHY/HYG/LQD/TIP/GLD/SLV/USO/UNG/DBC/UUP) | −0.0764 | −38.1% |

The sign holds on every aggregate window: **FULL** +0.2352 = −0.0482 / **+0.4798** / −0.1964;
**IS** +0.2113 = −0.0301 / **+0.5658** / −0.3243; **OOS** +0.2541 = −0.0636 / **+0.4188** / −0.1010.
φ(SINGLE20) > 0 in **13 of 14** sub-windows (H_ROBUST PASS); the one exception is 2011.

**The ETF-only panel has no edge at all.** `EQETF24/EW` reads **+0.0022** of Sharpe against SPY in
the leg window — two thousandths. `ETF36/EW` (every ETF, bonds and gold included) reads +0.0289.
The queue's "U56 carries ETFs alongside mega-caps" is true and is **the part that does not pay**.

## The three candidates

| candidate | verdict | the number |
|---|---|---|
| **PANEL COMPOSITION (the ETF sleeves)** | **KILL** | H_PANEL FAIL: the non-equity sleeve's Shapley share is **−38.1%**, not ≥ +50%. Added last to the 44-name equity book it is worth **+0.0140**; added first to SPY alone it is worth **−0.1603**. On no ordering does it reach 7% of the edge. |
| **EQUAL-WEIGHTING / SIZE** | **FAIL — it is real but small** | H_SIZE FAIL: `RSP` (equal-weight S&P 500, a **traded** instrument in the panel, no survivorship) beats SPY by **+0.0750** in the leg window = **37.4%** of the gap, and it is positive in only **8 of 14** sub-windows. On FULL and OOS it is **negative** (−0.0863, −0.1797). |
| **SINGLE-NAME SELECTION** | **PASS — the carrier** | H_SINGLES PASS: `SINGLE20/EW` beats SPY by **+0.3708**. Split against RSP: weighting/size **+0.0750**, **name selection +0.2958** (80% of the sleeve's edge, 147% of the whole +0.2006). On FULL: weighting −0.0863, **selection +0.5750**. |

**What "name selection" means here, said plainly:** `universe.json`'s `megacap` group is the list of
the 20 largest US companies **as of 2026** (NVDA, TSLA, META, AVGO, PLTR, …) held at equal weight
**from 2009**. It is not a rule, not a signal and not tradeable ex ante — it is the answer key. The
record's U56 "headroom" over SPY is a look-ahead artefact of a universe file.

## Not a cost, gross or weighting artefact

Leg-window edge by cost rung: **+0.2072 / +0.2006 / +0.1908 / +0.1744** at 0 / 10 / 25 / 50 bps.
Sharpe moves ≤ **0.0088** over the whole 20-rung no-leverage gross ladder (G7). The weighting dial
moves the level (IVOL lifts `ALL56` to 1.1852 by cutting vol to 8.00%) but not the attribution:
`SINGLE20` is the top sleeve under all three weightings (EW 1.2085 / IVOL 1.2516 / VT 1.2358).
Mechanically the `ALL56` edge is a **denominator** effect — 13.93% CAGR at 13.43% vol against SPY's
16.36% at 20.63% — while `SINGLE20`'s is a **numerator** effect (21.65% at 17.49%).

## Both KEEP paths, and why nothing is promoted

At 10 bps over 480 (sleeve, weighting, gross) cells: **4b FULL 28, IS 42, OOS 33; 4a FULL 24, IS 40,
OOS 9**. **27 cells clear 4b on FULL and IS and OOS together** (SINGLE20 17, EQ44 4, ALL56 3,
ALL55 3), best `SINGLE20/VT g=0.75` — **FULL 18.84% / 1.391 / −19.13%** (halves 1.493 / 1.303),
**OOS 18.54% / 1.357 / −19.13%** — and `SINGLE20/VT g=0.45` additionally clears **4a** on FULL and
OOS (11.12% / 1.389 / −11.82%).

**Every single one of those 103 window-passes contains the mega-cap sleeve.** The
survivorship-free sleeves — `EQETF24`, `ETF36`, `NONEQ12`, `SPYONLY` — clear 4b **0 times in any
window at any gross**. That is the run's cleanest sentence: on this panel, *every* 4b pass is
bought with the answer key.

**Rule 8 (required) — (sleeve, weighting, gross) chosen on 2009-2016 alone, 2017-2026 read once.**
5 IS-only selectors × 2 pools = 10 picks. **OOS 4b 0 of 10, OOS 4a 0 of 10.** Every unrestricted
chooser takes `SINGLE20/EW` at the top of the gross ladder and fails the DD cap outright:
**31.86% / 1.328 / −31.82%** at g=1.00 (cap −20.23%), 23.58% / 1.326 / −24.46% at g=0.75,
21.95% / 1.325 / −22.94% at g=0.70. The zero-parameter `PICK_LIVE_EWALL` (922's own EWALL at
g=0.75) reads **13.70% / 1.128 / −22.53%**, missing 4b on the DD cap by **2.30 pp**. Against SPY OOS
**15.27% / 0.874 / −33.72%** and RULES v2 OOS **9.46% / 1.277 / −12.05%**. **The 27 three-window
passers are not reachable from in-sample information** — the IS chooser prefers gross the DD cap
then rejects, so `SINGLE20/VT` is PARK, not KEEP, before survivorship is even counted.

## What this does to idea 922's readings

922's deductions (filter −0.1953, concentration −0.1130, interaction +0.0260) are arithmetic on a
base that is itself a look-ahead artefact, so their **signs and sizes stand as same-days contrasts**
— nothing here contradicts them — but the sentence "U56 has +0.2006 of headroom for a rule to give
back" should read "the 2026 mega-cap list has +0.32 of look-ahead, of which a rule gives back some".
Any statement of the form *"book X clears 4b on U56"* is a statement about a panel whose only
4b-bearing sleeve is unrepeatable. Filed as 933/934 below.

## Gates (8 of 8)

**G1** fast runner ≡ `engine.backtest` on returns and turnover, **1.388e-17 / 2.359e-16**
(post-warm-up window; `engine` shifts an already-filled frame so its row 0 is NaN by construction —
same convention as 922's G1). **G1b** the same on a **de-grossed** book (`ALL56/VT`), 1.388e-17.
**G2 CROSS-RUN:** idea 922's committed leg-window triple reproduces to 4 dp — EWALL **1.0384**,
SPY **0.8378**, edge **+0.2006**. **G3** committed U56 FULL triples: SPY 0.1513 / 0.8845 / −0.3372
vs (0.1516, 0.8861, −0.3372), RULES v2 0.0862 / 1.2013 / −0.1205 vs (0.0863, 1.2018, −0.1205).
**G4** the leg window is 922's exactly (2009-01-13 … 2013-01-07, 1,003 days). **G5** Shapley sums to
the total on all 17 windows, max residual 2.776e-16. **G6** partition exhaustive and disjoint.
**G7** Sharpe scale-freeness 0.0088 over the gross ladder.

## Survivorship

U56 is a current-constituent list, so every CAGR and drawdown **level** above is optimistic. This
run's headline is precisely a measurement of that: the decomposition is a same-days, same-panel
contrast (robust), but the **level** of `SINGLE20` is not a level any 2009 investor could have had.
`RSP` and `SPY` are traded instruments and are the only survivorship-free comparands used; the
weighting leg (+0.0750 leg, −0.0863 FULL) is therefore the only part of the +0.2006 that survives
the critique, and it is 37% of it in the leg window and **negative** over the full sample.

## Follow-ups filed

- 933 — re-read every committed U56 4b pass in the record for its **mega-cap Shapley share**: this
  run finds 0 of 480 survivorship-free cells clear 4b, so which committed passes are answer-key passes?
- 934 — does the `SINGLE20` look-ahead survive a **vintage-honest** mega-cap list (top-20 by dollar
  volume as of each rebalance from the panel's own data), i.e. is any of the +0.2958 a momentum rule?
- 935 — `RSP` vs `SPY` is +0.0750 in 2009-2013 and −0.1797 OOS; price the equal-weight premium as a
  **regime** object rather than a constant, since the record quotes it as one.
