# Idea 762 (lane cloud, 2026-09-19) — does the SELECTOR's 10 pp EXTRA DRAWDOWN price out as PURE GROSS?

**VERDICT: KILL — YES, IT IS PURE GROSS. Idea 560's rolling threshold selector beats its IS-best
FIXED twin on U56 / MA-DIST by +7.63 pp of full-sample CAGR and +5.89 pp of OOS CAGR, and de-grossing
it to the fixed arm's own drawdown (g\* = 0.4783) leaves +0.45 pp full and −0.67 pp OOS. Solved the
rule-8-legal way, on IS rows only (g\* = 0.4663): +0.13 pp full and −0.96 pp OOS. Pooled over all
nine (panel, family) cells the matched advantage is NEGATIVE on both windows.**

Script `research/backtests/2026-09-19_selector-extra-drawdown-as-pure-gross_cloud.py` (imports idea
560's committed builders, so the arms are literally 560's arms).
288 cells published (9 panel×family pairs × [9 fixed thresholds + 12 selector variants + 14
de-gross rungs + 8 matched cells]). Two tuned parameters: the selector's gross and the matching
target. All 3 gates PASS — **G1 replays 560's committed U56/MA-DIST numbers to 6.0e-04** (selector
OOS 18.01%/1.1251/-30.11% vs committed 18.01%/1.1245/-30.11%; IS-best FIXED th -0.12
12.12%/1.1018/-20.10% vs committed 12.14%/1.1020/-20.10%). 236s, offline, deterministic.

---

## 0. THE TWO ARMS AND THE TWO DIALS

- **SELECTOR** — 560's construction: at every weekly rebalance it holds the gate book of the
  threshold with the highest trailing value of a leg statistic, data ≤ t only. The (statistic,
  window) pair is 560's own rule-8 pick, by IS Sharpe alone over 12 variants, reproduced here
  (U56/MA-DIST SPREAD·TRAIL3Y, U56/MOM12_1 SPREAD·TRAIL1Y, U56/LOWVOL SPREAD·TRAIL3Y,
  B136/MA-DIST EXCESS·FULL_IS, …).
- **FIXED twin** — 560's IS-best fixed threshold on the same family, always at the record's
  standing gross 0.75. Only the selector is de-grossed; no leverage is ever used.
- **DIAL 1** the selector's gross over 14 rungs 0.10…0.75, plus the solved g\*.
- **DIAL 2** the matching target ∈ {MAXDD, MEANGROSS, VOL, CAGR}, each solved on the FULL window
  and, separately, on the IS window only (the rule-8-legal version).

## 1. THE HEADLINE — U56 / MA-DIST, the exact cell 762 was filed on

RAW, both arms at gross 0.75: the selector wins **+7.63 pp of FULL CAGR** and **+5.89 pp of OOS
CAGR**, at **−10.01 pp of MaxDD** and 5.6× the turnover (15.32 vs 2.71 per yr, 153 vs 27 bp/yr
of cost, charged — both figures reproduce 560's exactly).

| matching target | solved on | g\* | sel CAGR | fixed CAGR | **ΔCAGR pp** | sel MaxDD | fixed MaxDD | ΔSharpe | **OOS ΔCAGR pp** | OOS ΔSharpe |
|---|---|---|---|---|---|---|---|---|---|---|
| **MAXDD** | FULL | **0.4783** | 12.55% | 12.10% | **+0.45** | -20.10% | -20.10% | +0.0065 | **-0.67** | +0.0231 |
| **MAXDD** | **IS** | **0.4663** | 12.23% | 12.10% | **+0.13** | -19.64% | -20.10% | +0.0065 | **-0.96** | +0.0231 |
| MEANGROSS | FULL / IS | 0.7500 | 19.73% | 12.10% | +7.63 | -30.11% | -20.10% | +0.0073 | +5.89 | +0.0233 |
| VOL | FULL | 0.4642 | 12.18% | 12.10% | +0.08 | -19.56% | -20.10% | +0.0064 | -1.01 | +0.0231 |
| VOL | IS | 0.4105 | 10.76% | 12.10% | -1.34 | -17.45% | -20.10% | +0.0063 | -2.30 | +0.0230 |
| CAGR | FULL | 0.4612 | 12.10% | 12.10% | -0.00 | -19.44% | -20.10% | +0.0064 | -1.08 | +0.0231 |
| CAGR | IS | 0.4157 | 10.90% | 12.10% | -1.20 | -17.66% | -20.10% | +0.0063 | -2.18 | +0.0230 |

**The answer to 762 in one line: of the +7.63 pp, 7.18 pp (94%) is gross and 0.45 pp is the
selector.** Solved the legal way, on IS rows only, 98% of it is gross; and what is left goes
NEGATIVE out of sample. The MEANGROSS row is the control that makes the point: both arms already
stand at the same NOMINAL gross 0.75, so matching on nominal exposure changes nothing — **nominal
gross matching is not drawdown matching, and the record's "matched exposure" language has been
carrying the weaker of the two meanings.**

## 2. THE SAME ANSWER ON ALL NINE (panel, family) CELLS

Matched on **MAXDD**, ΔCAGR of selector-minus-fixed in pp:

| panel | family | g\* (FULL) | ΔCAGR | ΔCAGR OOS | g\* (IS) | ΔCAGR | ΔCAGR OOS | RAW ΔCAGR | RAW ΔMaxDD |
|---|---|---|---|---|---|---|---|---|---|
| U56 | MA-DIST | 0.478 | +0.45 | -0.67 | 0.466 | +0.13 | -0.96 | +7.63 | -10.01 |
| U56 | MOM12_1 | 0.595 | +0.40 | +1.20 | 0.690 | +2.44 | +3.41 | +3.75 | -5.04 |
| U56 | LOWVOL | 0.750 | -3.87 | -4.72 | 0.750 | -3.87 | -4.72 | -3.87 | +3.15 |
| B136 | MA-DIST | 0.313 | -4.60 | -3.75 | 0.403 | -1.98 | -0.98 | +7.77 | -26.25 |
| B136 | MOM12_1 | 0.702 | +3.33 | +4.49 | 0.461 | -2.24 | -1.52 | +4.46 | -1.56 |
| B136 | LOWVOL | 0.392 | -2.52 | -2.02 | 0.586 | -0.21 | -0.14 | +1.74 | -9.94 |
| SMALL439 | MA-DIST | 0.738 | -1.03 | -0.80 | 0.750 | -0.93 | -0.72 | -0.93 | -0.48 |
| SMALL439 | MOM12_1 | 0.703 | +0.79 | +1.23 | 0.696 | +0.70 | +1.14 | +1.43 | -2.04 |
| SMALL439 | LOWVOL | 0.545 | -0.04 | +0.44 | 0.487 | -0.43 | +0.28 | +1.29 | -7.82 |
| **pooled mean** | | | **-0.79** | **-0.51** | | **-0.71** | **-0.47** | **+2.59** | **-6.67** |
| **cells positive** | | | 4/9 | 4/9 | | 3/9 | 3/9 | 7/9 | |

**The raw +2.59 pp pooled CAGR edge becomes −0.79 pp (FULL-solved) or −0.71 pp (IS-solved) at
matched drawdown, and the OOS edge +2.71 pp becomes −0.51 / −0.47 pp.** The one cell where a real
edge survives the IS-legal match is **U56/MOM12_1 (+2.44 pp full, +3.41 pp OOS)** — and its
sibling **B136/MOM12_1 flips sign between the FULL-solved (+3.33) and IS-solved (−2.24) match on
the same book**, which is the size of the noise on this axis.

## 3. THE METHOD FINDING — de-grossing is SHARPE-NEUTRAL to 3 decimals, so this whole family of contrasts is one number

Across all **9 ladders × 14 gross rungs**, the selector's Sharpe moves by a span of **0.0026 on
average and 0.0067 at worst** (U56/LOWVOL 0.0006; B136/MOM12_1 0.0013; B136/MA-DIST 0.0067).

| panel / family | Sharpe min | Sharpe max | span |
|---|---|---|---|
| U56 LOWVOL | 0.9739 | 0.9745 | **0.0006** |
| U56 MOM12_1 | 1.1220 | 1.1233 | 0.0013 |
| B136 MOM12_1 | 1.0740 | 1.0753 | 0.0013 |
| U56 MA-DIST | 1.1373 | 1.1396 | 0.0023 |
| SMALL439 MA-DIST | 0.5482 | 0.5512 | 0.0031 |
| SMALL439 LOWVOL | 0.5984 | 0.6027 | 0.0043 |
| B136 MA-DIST | 0.9262 | 0.9329 | **0.0067** |

At 10 bps with a 0% cash leg, the de-gross ladder is a **pure (CAGR, MaxDD) slide with no Sharpe
cost at all**. Two consequences the record should carry:

1. **Any comparison of two books at different drawdowns is, to within 0.007 of Sharpe, already
   decided by their Sharpes alone.** Here the selector's pooled ΔSharpe against its fixed twin is
   **−0.0306 full and −0.0302 OOS** — i.e. the selector is slightly WORSE, and the +2.59 pp of raw
   CAGR was never evidence of anything but a bigger position.
2. It also explains why the eight prior 2026-09-19 runs kept finding a plain de-gross beating every
   drawdown-buying device: on this tape the de-gross frontier is a straight line through the
   origin in (CAGR, MaxDD), and a device can only beat it by moving Sharpe.

## 4. WHAT THE CHURN COSTS

RAW = the selector at its own gross 0.75 (560's arm). MATCHED = the same book de-grossed to
g\* on the IS MaxDD target; turnover scales with gross, so the match buys back part of the cost.

| panel | family | RAW turn/yr | fixed turn/yr | ratio | RAW cost bp/yr | fixed cost bp/yr | extra | g\*(IS) | MATCHED turn/yr | MATCHED cost bp/yr |
|---|---|---|---|---|---|---|---|---|---|---|
| U56 | MA-DIST | **15.32** | **2.71** | 5.6× | 153 | 27 | **+126** | 0.4663 | 9.58 | 96 |
| U56 | MOM12_1 | 13.05 | 3.95 | 3.3× | 131 | 39 | +91 | 0.6896 | 12.01 | 120 |
| U56 | LOWVOL | 7.67 | 1.28 | 6.0× | 77 | 13 | +64 | 0.7500 | 7.67 | 77 |
| B136 | MA-DIST | 22.50 | 0.96 | **23.5×** | 225 | 10 | **+215** | 0.4034 | 12.19 | 122 |
| B136 | MOM12_1 | 15.05 | 3.14 | 4.8× | 151 | 31 | +119 | 0.4611 | 9.28 | 93 |
| B136 | LOWVOL | 10.54 | 13.58 | 0.8× | 105 | 136 | -30 | 0.5856 | 8.24 | 82 |
| SMALL439 | MA-DIST | 17.98 | 1.93 | 9.3× | 180 | 19 | **+160** | 0.7500 | 17.98 | 180 |
| SMALL439 | MOM12_1 | 13.66 | 6.48 | 2.1× | 137 | 65 | +72 | 0.6960 | 12.68 | 127 |
| SMALL439 | LOWVOL | 22.28 | 23.36 | 1.0× | 223 | 234 | -11 | 0.4867 | 14.46 | 145 |

The U56/MA-DIST RAW figures (15.32 vs 2.71) reproduce idea 560's committed pair exactly. All costs
are already charged inside every number in this file. **Note the two LOWVOL cells where the FIXED
arm is as churny or churnier** (B136 13.58 vs 10.54, SMALL439 23.36 vs 22.28): "the selector adds
turnover" is a MA-DIST / MOM12_1 fact, not a property of rolling selection.

## 5. CAPITAL ARM — both KEEP paths at all 288 cells, rule-8 walk-forward

- **Path 4a: 3/288**, all three the SMALL439/MOM12_1 selector at gross 0.10-0.20, i.e. books
  running 1.5-3.0% CAGR that clear the live low-return book on halves by being almost flat. None of
  them clears 4b.
- **Path 4b: 23/288.** Binding-leg census over the 288 cells: **DD 169, CAGR 167, H2 148, OOS 124,
  H1 64.**
- **No new KEEP candidate.** The best 4b passers here are U56/MA-DIST `FIXED th=-0.12`
  (12.10%/1.1323/-20.10% full, 12.12%/1.1018/-20.10% OOS) and the MAXDD-matched selector at
  g\* = 0.4783 (12.55%/1.1388/-20.10% full, 11.46%/1.1249/-20.10% OOS). **Both are strictly worse
  than the standing frozen 2026-09-04 incumbent on CAGR, Sharpe AND drawdown**
  (15.80%/1.1537/-19.13% full; 17.32%/1.1857/-19.13% OOS), so nothing here is worth a memo.
- **RULE 8 (protocol rule 8): g\* solved on warm-up..2016-12-31 ONLY, 2017-2026 read once.**

| panel | family | g\* | selector OOS CAGR/Sharpe/MaxDD | fixed OOS CAGR/Sharpe/MaxDD | ΔCAGR pp | ΔSharpe |
|---|---|---|---|---|---|---|
| U56 | MA-DIST | 0.4663 | 11.17% / 1.1249 / -19.64% | 12.12% / 1.1018 / -20.10% | -0.96 | +0.0231 |
| U56 | MOM12_1 | 0.6896 | 15.93% / 1.0840 / -24.59% | 12.51% / 1.0725 / -21.48% | +3.41 | +0.0115 |
| U56 | LOWVOL | 0.7500 | 8.06% / 0.9014 / -17.68% | 12.78% / 1.1156 / -20.83% | -4.72 | -0.2142 |
| B136 | MA-DIST | 0.4034 | 12.57% / 0.9033 / -31.30% | 13.55% / 1.0833 / -25.08% | -0.98 | -0.1799 |
| B136 | MOM12_1 | 0.4611 | 11.46% / 1.0613 / -17.16% | 12.98% / 1.0647 / -25.25% | -1.52 | -0.0034 |
| B136 | LOWVOL | 0.5856 | 5.74% / 0.8134 / -17.33% | 5.88% / 0.8449 / -11.85% | -0.14 | -0.0315 |
| SMALL439 | MA-DIST | 0.7500 | 6.47% / 0.4676 / -34.71% | 7.19% / 0.5080 / -34.24% | -0.72 | -0.0404 |
| SMALL439 | MOM12_1 | 0.6960 | 9.68% / 0.6661 / -36.09% | 8.54% / 0.6082 / -36.41% | +1.14 | +0.0579 |
| SMALL439 | LOWVOL | 0.4867 | 1.50% / 0.2880 / -21.97% | 1.22% / 0.1826 / -24.34% | +0.28 | +0.1054 |
| **mean** | | | | | **-0.47** | **-0.0302** |

Benchmarks on the common sample: SPY 15.12%/0.8843/-33.72% full and 15.26%/0.8737/-33.72% OOS;
RULES v2 live U56 8.64%/1.2081/-11.90% full and 9.49%/1.2854/-11.90% OOS.

## 6. SURVIVORSHIP (rule 9)

U56 and B136 are CURRENT-constituent lists and SMALL439 a CURRENT sub-$2B screen (665 names after
the protocol-mandated `max_1d_move >= 1.0` drop of 54 tickers) carried back to 2008/2010. Every
ABSOLUTE level above is an UPPER BOUND. What this run reads is a CONTRAST between two books over
the same names on the same days, which the bias cannot manufacture. Note also, as idea 706 and 1074
recorded, that the label `SMALL439` now denotes a 665-name pool.

## 7. WHAT THE RECORD GAINS

1. **The mirror of the eight de-gross runs closes.** They showed a plain de-gross beats every
   drawdown-BUYING device at matched exposure; 762 shows the one device in the record that BUYS
   RETURN WITH DRAWDOWN is likewise nothing but a de-gross read backwards. **Gross is the axis;
   the devices are decoration.**
2. **A rule for reading the record: "matched exposure" must name whether it means matched NOMINAL
   gross or matched REALISED drawdown.** On this cell the two differ by g\* = 0.75 vs 0.478 and by
   7.2 pp of CAGR — the whole of the claim.
3. **De-grossing is Sharpe-neutral to 0.0026 on this tape**, so any two books at different
   drawdowns can be adjudicated on Sharpe alone; the selector's Sharpe deficit (−0.0306 pooled)
   was the answer all along.
