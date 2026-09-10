# Idea 645 — does the DOLLAR floor's EJECT-AFTER-A-FALL channel exist off SMALL439?

**Lane B, 2026-09-10.** Script `2026-09-10_does-the-DOLLAR-floor-s-EJECT-AFTER-A-FALL-channel-exist-off-SMALL439_B.py`.
**Verdict: ANSWERED — the channel is REAL and TRANSPORTS, but it is NOT the mechanism the queue named,
and it is NOT capital-worthy. 4a 0/360, 4b 0/360 for the channel; no KEEP.**
No RULES/scan/bot/baseline file touched.

## The data problem, and why the idea is runnable anyway

645 asks for the split re-measured on a panel with a delisted cohort or on U56/broad136 "once idea 429
caches volume". Neither exists: `data/` has no delisted cohort and volume is cached for SMALL439 only
(the script enumerates this). The literal idea is PARK. It is not PARKed, because of an identity idea
427 reported as a "post-hoc mechanism" but which is actually algebra:

    DV := median20(px*vol), SV := median20(vol), IP := DV/SV
    DV-only(F,s)    <=> DV>=F and SV<s  <=> SV*IP>=F and SV<s  ==> IP > F/s
    VOLSH-only(F,s) <=> SV>=s and DV<F  <=> SV>=s and SV*IP<F  ==> IP < F/s

**Measured on SMALL439: 1.000000 of the 83,624 DV-only ticker-days have IP > F/s\*, and 1.000000 of the
83,592 VOLSH-only ticker-days have IP < F/s\*.** The swapped sets are an exact one-sided cut on an
implied price at F/s\* = $14.36, with no return input and no fitted parameter. Transport gate:
corr(log IP, log px) = 0.9960, IP/px median 0.9984, and the *traded close* cut at $14.36 agrees with the
IP cut on **97.78%** of live ticker-days — so the split can be run on any panel with prices alone.

## Gates (pre-registered, all PASS)

- **G1** `fast_bt` == `engine.backtest` over the evaluation window on 3 (panel, book) pairs:
  max|Δret| ≤ 2.1e-17, max|Δturn| ≤ 3.0e-16. (Incidental: `engine.backtest` emits 2 NaN rows on every
  panel — `weights.shift(1)` leaves row 0 undefined — both inside the dropped 260-day warm-up.)
- **G2** idea 427's published split reproduces to **0.011 pp**: DV-only +11.01% / +0.30%, VOLSH-only
  +2.53% / +28.92%. Published forward gap **+28.62%**, the object of 645.

## Q2 — "eject after a fall" names the WRONG object

Same trailing/forward-126d statistic, four splits on SMALL439:

| split | forward-126d gap | share of the published +28.62% |
|---|---|---|
| VOLUME split (idea 427) | +28.62% | 100% |
| IP LEVEL cut at F/s\* | +13.72% | 48% |
| PRICE LEVEL cut at F/s\* (no volume) | +13.73% | 48% |
| **literal EJECT vs RE-ADMIT (crossed the DV floor in the last 126d)** | **+1.61%** | **6%** |

The crossing *event* — the thing 427 and 645 both name — carries 6% of the gap. A static price-level
cut carries 48%; the remaining 52% is that the swapped sets are the narrow tails straddling the
threshold, not the two halves. **The channel is a price-LEVEL effect wearing a price-PATH name.**

## Q3 — the answer to 645: yes, off-panel, at about half size

Price-only restatement, 3 panels × (1 absolute + 5 relative q) × 3 horizons = **54 cells, all reported**
(`.gaps.csv`). Forward-minus-forward, LOW price side minus HIGH:

| panel | mean fwd gap | median | positive | at h=126 |
|---|---|---|---|---|
| SMALL439 | +19.44% | +14.25% | 18/18 | +16.23% |
| U56 | +11.73% | +7.50% | 18/18 | +8.99% |
| broad136 | +8.06% | +5.86% | 18/18 | +6.35% |

**SMALL439 +19.44% vs off-panel +9.90% — 1.96x, and positive in 54 of 54 cells.** The channel is not a
SMALL439 artefact; roughly half of SMALL439's version is panel-specific excess.

## Q4 — survivorship signatures: one fires, one fires the wrong way

- **(a) TAIL TEST — fires, everywhere.** At REL q=0.20 the SMALL439 mean gap is +18.43% but the median
  gap is +5.71% (median carries 31%); P(forward 126d > +100%) is 8.02% on the LOW side vs 1.68% on the
  HIGH. U56 33% / 2.84% vs 0.34%; broad136 42% / 1.56% vs 0.27%. The low-price forward return is a
  lottery-ticket tail on every panel — exactly the shape a missing delisted cohort inflates, and
  exactly the shape that does not survive equal-weighted holding of the whole side.
- **(b) ERA TEST — fires backwards on SMALL439.** `SMALL_PANEL_README.md` says the bias grows with
  lookback, so the gap should decay IS→OOS. It decays on U56 (+12.69% → +4.00%, 0.32x) and broad136
  (+7.79% → +4.64%, 0.60x) and **grows** on SMALL439 (+10.35% → +22.14%, 2.14x). The SMALL439 excess is
  therefore not the era shape survivorship predicts; it sits in the 2020-21 small-cap window.

Net: the +28.9% forward return **cannot** be attributed to survivorship on the era evidence, and
**should not** be traded on the tail evidence. Both panels used off SMALL439 are current-constituent
lists too (PROTOCOL 9), so no panel here is survivorship-free.

## Q5/Q6 — priced as a book: KILL on both paths

Equal-weight the selected side at gross 0.75, remainder cash; 3 panels × 2 sides × 5 q × 3 cadences ×
4 cost rungs = **360 points, all reported** (`.grid.csv`). Tuned dials: **q and cadence** (2).

- **4a 0/360, 4b 0/360 for the channel, BOTH 0/360.** Binding bars 4b: DD 340, CAGR 85, H1 81, H2 60,
  OOS 60. Binding bars 4a: DD 360, H2 200, H1 168.
- **All 45 LOW cells at 10 bps fail 4b on the DD leg and nothing else** — they clear H1, H2, OOS Sharpe
  and the CAGR floor against SPY on all three panels at every q and every cadence, and miss the
  −20.2% cap (0.60 × SPY's −33.7%) by 3 to 18 pp. Range of LOW MaxDD: −23.0% to −37.9%.
- The **only** 4b passes in the entire grid are 8 rows of the HIGH-price **mirror control** (U56, q=0.30,
  M and Q, all four costs): CAGR 10.8% vs SPY 15.2%, Sharpe 0.98 vs 0.89, MaxDD −19.7/−20.2%. It passes
  by not falling, not by earning.
- LOW − HIGH at matched (panel, q, cadence), 10 bps: **SMALL439 +23.62 pp CAGR / +1.0720 Sharpe (15/15),
  U56 +11.34 pp / +0.3878 (15/15), broad136 +8.48 pp / +0.3737 (15/15).**

**Rule 8** — (q, cadence) chosen on 2010-2016 IS Sharpe, 2017-2026 read once:

| panel | side | pick | OOS CAGR | OOS Sharpe | OOS MaxDD | RULES v2 OOS Sh | SPY OOS CAGR / Sh / DD | 4b-OOS |
|---|---|---|---|---|---|---|---|---|
| SMALL439 | LOW | q0.10/W | 48.85% | 1.852 | −35.2% | 0.568 | 15.45% / 0.882 / −33.7% | FAIL(DD) |
| U56 | LOW | q0.10/M | 28.00% | 1.532 | −24.2% | 1.279 | 15.32% / 0.876 / −33.7% | FAIL(DD) |
| broad136 | LOW | q0.10/Q | 22.17% | 1.498 | −23.0% | 1.119 | 15.45% / 0.882 / −33.7% | FAIL(DD) |
| SMALL439 | HIGH | q0.10/Q | 5.62% | 0.408 | −36.7% | 0.568 | " | FAIL(Sharpe,DD,CAGR) |
| U56 | HIGH | q0.10/Q | 12.78% | 1.069 | −21.8% | 1.279 | " | FAIL(DD) |
| broad136 | HIGH | q0.10/W | 12.97% | 1.035 | −25.5% | 1.119 | " | FAIL(DD) |

**rule-8 OOS 4b passes 0/6.** LOW beats its own HIGH control on OOS Sharpe 3/3 panels, and beats both
SPY and RULES v2 on OOS Sharpe 3/3 — and still fails, on drawdown alone, every time. That is the same
DD-leg story ideas 527/530/531 measured record-wide, reached here by a fourth route.

## What the record should carry forward

1. **Idea 427's "post-hoc mechanism" is an identity, not a mechanism.** The DV-vs-VOLSH swap is
   `IP > F/s` vs `IP < F/s`, exactly, on 167,216 of 167,216 ticker-days. Any future dollar-vs-share
   floor claim should be stated as a price-level cut at F/s from the start.
2. **"Eject after a fall" is the wrong name** and should not be repeated: the crossing event carries 6%.
3. **The forward-return gap transports** (1.96x SMALL439 vs off-panel, 54/54 positive) but is
   **tail-driven on every panel** (median carries 31-42%) and **unbankable**: 0/360 on both KEEP paths,
   0/6 on rule 8, DD the sole binding leg on all 45 LOW cells at the PROTOCOL cost rung.
