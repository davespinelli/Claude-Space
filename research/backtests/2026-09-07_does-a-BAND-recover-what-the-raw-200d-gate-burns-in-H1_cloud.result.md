# Idea 370 — does a BAND recover what the raw 200d gate burns in H1?

**Verdict: SPLIT. The queue's H1 question answers YES and its MECHANISM is FALSIFIED. A
hysteresis band removes 91% of the gate's flips and recovers, at best, 10% of the gate's
full-sample cost — because what looks like H1 recovery is the band RELOCATING cash days out of
H1 into H2, not repairing whipsaw. KILL as a rule (4a 0/480; rule 8 picks the widest band in
4/4 cells and loses +0.494 of OOS Sharpe for it). No RULES change, no book promoted, no KEEP
claimed; RULES.md, scan.py, bot.py and baseline.py untouched. One PARK by-product below.**

Script: `2026-09-07_does-a-BAND-recover-what-the-raw-200d-gate-burns-in-H1_cloud.py`
Artefacts: `.grid.csv` (480 books), `.core.csv` (24 core-leg rows), `.walkforward.csv`,
`.console.txt`. Every point of every axis is printed and written; nothing is filtered out.

## 0. Reproduction gates (all PASS, printed before any new number was read)

| gate | result |
|---|---|
| derived rung `r(c) = r(0) - turnover*c/1e4` vs `engine.backtest(cost_bps=25)` | max\|diff\| **0.000e+00** |
| `baseline.band_state(px, 0.00)` NESTS idea 30's raw `px > ma` gate | **0 disagreeing days of 4699** on QQQ and on SPY (0 of 4439 post-warm-up) |
| idea 24 variant B's published decimals, on idea 30's own truncated tape (2026-09-02) | 10.8% / 0.95 / -18.9% / 0.84 / 1.04 — **hard assert PASS** |
| idea 30's published gate-cost table (core leg, 60% QQQ, gated vs always-on) | H1 **-0.0611 / -0.3673**, H2 **-0.0128 / +0.1343**, full **-0.0371 / -0.0801** — all PASS |
| idea 30's published cash-day shares | **16.0% / 15.2% / 16.7%** — PASS |
| idea 30's committed `grid.csv`, GATE=ON rows rebuilt here as the band=0.00 slice | **96/96 matched**; max\|d\| CAGR 9.7e-17, Sharpe 1.1e-16, MaxDD 8.3e-17, H1 **0.0e+00**, H2 2.2e-16, OOS Sharpe 2.2e-16, turnover 8.9e-16; **4b verdicts identical 96/96** (parent 0, rebuild 0) |

## 1. Design

Idea 30's grid, verbatim, with the core's raw 200d gate replaced by `baseline.band_state(band)`.
**Two tuned parameters:** `c ∈ {0.50, 0.60, 0.70, 0.80}` (equity core fraction, sleeve = 1-c) and
`band ∈ {0.00, 0.03, 0.06, 0.12}`. **Reported, not tuned:** `q ∈ {0.00, 0.25, 0.50, 0.75, 0.8333,
1.00}` (QQQ share of the core, rest SPY; q=1.00 is idea 24's variant B anchor, q=0.8333 idea 30's
literal proposal), panel ∈ {U56, B136}, rung ∈ {10, 25} bps, plus a GATE=OFF always-on control.
**384 gated books + 96 controls = 480, all reported.** band=0.00 IS idea 30's GATE=ON slice and is
used only as the reproduction gate above.

## 2. The headline: the band recovers H1 and destroys H2, at unchanged total cash days

Core leg alone (c=0.60 in QQQ, no sleeve), gated vs always-on, @10 bps, U56 (B136 identical to
1e-5 — see §5):

| band | flips/yr | H1 dCAGR | H1 dSharpe | H2 dCAGR | H2 dSharpe | full dCAGR | cash% H1 / H2 / full |
|---|---|---|---|---|---|---|---|
| 0.00 (raw) | **5.85** | -6.11 pp | -0.367 | -1.28 pp | +0.134 | -3.71 pp | 13.8 / 18.2 / 16.0 |
| 0.03 | 1.53 | -5.95 pp | -0.353 | -2.46 pp | +0.037 | -4.21 pp | 15.4 / 19.4 / 17.4 |
| 0.06 | 0.85 | -4.03 pp | -0.163 | -2.64 pp | -0.004 | -3.33 pp | 17.4 / 17.5 / 17.5 |
| 0.12 | **0.51** | **-1.75 pp** | **-0.062** | **-7.10 pp** | **-0.384** | -4.47 pp | **4.4 / 30.3 / 17.4** |

Recovery against the raw gate (`d(band) - d(0.00)`):

| band | H1 recovered | H1 Sharpe recovered | H2 recovered | H2 Sharpe recovered | **full recovered** |
|---|---|---|---|---|---|
| 0.03 | +0.16 pp | +0.014 | -1.17 pp | -0.097 | **-0.50 pp** |
| 0.06 | +2.08 pp | +0.204 | -1.36 pp | -0.138 | **+0.38 pp** |
| 0.12 | **+4.36 pp (71% of 6.11)** | **+0.306** | **-5.82 pp** | -0.518 | **-0.75 pp** |

**The queue's question answers yes; its premise does not survive the answer.** A band of 0.12
does give back 4.36 of the 6.11 pp and +0.306 of H1 Sharpe — comfortably more than the +0.113 the
H1 bar needed. But it is not a whipsaw repair:

* **The whipsaw is removed and almost nothing follows.** Gate flips fall **5.85 → 0.51 per year, an
  11.5x reduction (91% of the flips gone)**, and the FULL-SAMPLE gate cost moves from -3.71 pp to
  -4.47 pp — *worse*. The best full-sample recovery over the whole ladder is **+0.38 pp at
  band=0.06, i.e. 10% of the 3.71 pp cost**, and two of the three bands recover a negative amount.
  If the 6.11 pp were a whipsaw tax, deleting 91% of the whipsaws would not cost money.
* **The mechanism is cash-day RELOCATION, and the total premium is unchanged.** Full-sample cash
  days are **16.0 / 17.4 / 17.5 / 17.4%** across the ladder — flat to within 1.5 pp — while the
  H1/H2 split swings from 13.8/18.2 to **4.4/30.3**. Band 0.12 recovers H1 by being invested
  through the best large-cap decade in the sample and pays for it by sitting in cash 30% of H2.
  At matched total insurance, the band moves *when* the premium is paid, not how much it costs.
* Turnover confirms the flip count and not the P&L: mean gated turnover falls **3.49 → 2.56 → 2.22
  → 2.04 x/yr** while mean gross barely moves (0.770 → 0.747).

## 3. The H1 bar (idea 30: GATE=ON 0/24 clear it, GATE=OFF 24/24 do)

Points clearing `H1 > SPY H1 (0.9566)`, of 24 per cell:

| panel @ rung | GATE=OFF | band 0.00 | band 0.03 | band 0.06 | band 0.12 |
|---|---|---|---|---|---|
| U56 @10 bps | 24/24 | **0/24** | **0/24** | **19/24** | **20/24** |
| U56 @25 bps | 20/24 | 0/24 | 0/24 | 11/24 | 18/24 |
| B136 @10 / @25 bps | 24/24, 20/24 | 0/24, 0/24 | 0/24, 0/24 | 19/24, 11/24 | 20/24, 18/24 |

Best H1 margin per band, U56 @10 bps: GATE=OFF **+0.2327** (c=0.80, q=1.00); band 0.00 **-0.1035**;
band 0.03 -0.0482; band 0.06 **+0.0708** (c=0.80, q=0.8333); band 0.12 **+0.1679** (c=0.80, q=1.00).
So on the bar idea 30 could not clear at any (c, q), a band of 0.06 or wider clears it in most of
the grid — and the widest band still does not reach the ungated control's margin.

## 4. KEEP paths (all 480 points) and rule 8

| cell | 4a | 4b |
|---|---|---|
| all 480 | **0/480** | **18/480** |
| GATE=OFF | 0/96 | 14/96 (idea 30's own ungated passes, reproduced) |
| band 0.00 | 0/96 | 0/96 |
| band 0.03 | 0/96 | 0/96 |
| band 0.06 | 0/96 | **4/96** |
| band 0.12 | 0/96 | 0/96 |

First failing bar over the 462 4b failures: `H1+CAGR` 116, `DD` 94, `H2+OOS+DD+CAGR` 72,
`H1+DD` 42, `H1+H2+OOS+DD+CAGR` 40, then a long tail. 4a is **0/480**: nothing in this family
gets near the live book's drawdown.

**Rule 8** — the two tuned dials (c, band), 16 cells, chosen on 2009-2016 by IS Sharpe, 2017-2026
read once:

| panel / q | IS pick | OOS | idea 30's anchor OOS | regret vs anchor | OOS-best | regret vs best |
|---|---|---|---|---|---|---|
| U56 q=1.0000 | c=0.80, **band=0.12** (IS 1.0082) | 9.52% / **0.6684** / -31.46% | 1.1530 | **+0.4847** | c=0.50 band=0.00 (1.1634) | +0.4951 |
| U56 q=0.8333 | c=0.80, band=0.12 (IS 0.9950) | 8.73% / 0.6506 / -30.60% | 1.1533 | +0.5027 | c=0.50 band=0.00 (1.1627) | +0.5121 |
| B136 q=1.0000 | c=0.80, band=0.12 | 9.52% / 0.6685 / -31.46% | 1.1532 | +0.4847 | c=0.50 band=0.00 | +0.4952 |
| B136 q=0.8333 | c=0.80, band=0.12 | 8.73% / 0.6507 / -30.60% | 1.1535 | +0.5027 | c=0.50 band=0.00 | +0.5122 |

The IS chooser picks a **non-zero band in 4/4 cells — always the widest one — and loses a mean
+0.4937 of OOS Sharpe against idea 30's own anchor** (and +0.5036 against the OOS-best cell,
which is the *raw* gate at c=0.50). This is the sharpest instance of the record's standing
IS-chooser result in this file: the dial the band opens is exactly the one the in-sample window
over-rewards, because 2009-2016 IS the decade band=0.12 keeps you invested through.

Reference rows: SPY 15.23% / 0.8890 / -33.72% (H1 0.9566, H2 0.8340, OOS 0.8820); RULES v2 (live)
OOS Sharpe 1.2851 on U56 and 1.1185 on B136.

**PARK by-product (not a KEEP).** `band=0.06, c=0.60, q=1.00` — 60% QQQ inside a ±6% band + 40%
sleeve — is the **first gated 4b pass this family has ever produced** (idea 30's GATE=ON slice was
0/96, reproduced above), and it survives the cost rung:

| rung | CAGR | Sharpe | MaxDD | H1 / H2 | OOS Sharpe |
|---|---|---|---|---|---|
| 10 bps | 11.24% | 0.9622 | -18.86% | 1.012 / 0.931 | 1.035 |
| 25 bps | 10.84% | 0.9314 | -18.89% | 0.977 / 0.903 | 1.007 |

It clears all five 4b bars on both panels at both rungs. **PARK, not KEEP**, for three stated
reasons: rule 8 does not select it (the IS chooser takes c=0.80/band=0.12 and is 0.29 of OOS
Sharpe worse than this cell); it is beaten on Sharpe, drawdown and OOS by idea 30's own **ungated**
c=0.50 books (13.04% / 1.0405 / -20.08%, OOS 1.038), which pass 4b without any gate at all; and
it fails 4a on every bar against the live book.

## 5. Panel and caveats

The panel axis is confirmed **degenerate** for this ETF-only book, as idea 30 found: over 240
matched (rung, gate, band, c, q) cells, **max \|U56 − B136\| Sharpe = 1.094e-04** and max \|d CAGR\|
= 1.082e-05. The B136 column is reported for continuity, not as independent evidence.

(1) **Survivorship**: both universes are current-constituent lists, so levels are flattered; the
band DIFFERENCES this run turns on are far less affected. (2) The tape is the corrected
trading-day index (ideas 38/39) while idea 24's published row predates that fix, so gate 2 is a
match to published decimals *across* the correction, exactly as idea 30 labelled it. (3) **QQQ's
2009-2017 run is the single best large-cap equity decade in the sample**, and band=0.12's entire
H1 gain is "stay invested in it" — this is the strongest reason to treat the H1 recovery as a
window artefact rather than a repair, and rule 8 agrees. (4) The band is applied to the CORE only;
the sleeve's internal momentum votes are untouched, as idea 30 left them.

## 6. What should change

Nothing in RULES. The band is a genuine **turnover** instrument on this book (flips 5.85 → 0.51/yr,
turnover 3.49 → 2.04 x/yr) and should keep being described as one. It is not a repair for the
core-plus-sleeve family's H1 failure: idea 30's whipsaw diagnosis is falsified here, and the
correct statement to carry forward is that **the 200d gate's H1 cost is the premium itself, paid in
the decade where the insurance was worthless — a band can move that premium between halves but not
reduce it.**
