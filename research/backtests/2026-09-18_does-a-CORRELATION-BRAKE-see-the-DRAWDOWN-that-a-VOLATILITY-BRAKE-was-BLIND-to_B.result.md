# Idea 1266 — does a CORRELATION BRAKE see the DRAWDOWN that a VOLATILITY BRAKE was BLIND to?

**Run 2026-09-18 by lane cloud from lane B's committed script, UNCHANGED** (lane B wrote it complete on
2026-09-18 04:40Z but could not install pandas — PyPI egress 503 — and asked the next lane to run it as
committed). `pip install pandas` succeeded this run (3.0.6); the block was transient egress, not the idea.

## Verdict: ANSWERED **NO** / **KILL (capital)** — no new book, no RULES change, no memo.

- **The literal answer.** In the only drawdown that binds 4b's DD leg (U56/COMPOSITE3, 2020-02-19 -> 2020-03-16,
  -19.13%), mean brake intensity INSIDE the episode is **CORR 0.129 / 0.000 / 0.000 / 0.000** at LOOK 20 / 60 /
  126 / 252 against **VOL 0.739 / 0.473 / 0.245 / 0.164**. CORR never reaches u >= 0.5 at any lookback; VOL first
  arms 2020-03-02. Before the peak both are 0.000 — neither is early.
- **Head to head, 96 matched pairs.** CORR minus VOL: MaxDD **-1.83pp** (CORR better at 20/96), CAGR +1.61pp,
  Sharpe +0.0222, OOS +0.0042. Correlation keeps CAGR because it arms less (on% 46.0 vs 64.1), not because it
  is better timed. Intensity rank correlation between the two: mean +0.495 (+0.147..+0.726).
- **Capital.** 240 cells. 4a **0 of 240**. 4b 83 of 240. Rule 8 (LOOK, SLOPE chosen on IS Sharpe to 2016-12-31,
  2017-2026 read once, 12 choosers): chooser-minus-do-nothing OOS Sharpe **mean -0.1655, positive at 0 of 12**;
  CORR mean -0.1951 with IS/OOS rank corr **-0.351**.
- **The control that kills it.** Against a flat schedule at the same realised mean gross: CORR d_CAGR -0.75pp,
  d_Sharpe -0.0449 (>0 at 19/96), d_MaxDD -0.05pp, **d_OOS -0.0992 (>0 at 3 of 96)**. All 49 4b conversions are
  reproduced by that cell's own flat control.
- **The one real channel.** Against the permuted-intensity placebo both brakes are positive (CORR +0.0215 Sharpe,
  +0.91pp MaxDD). The timing channel exists and is simply smaller than the CAGR a gross cut costs.
- **Anchors.** U56/COMPOSITE3 SLOPE 0 = 15.78% / 1.1522 / -19.13%, OOS 1.1832. SPY 15.13% / 0.8849 / -33.72%,
  halves 0.9600 / 0.8236, OOS 0.8747. Live RULES v2 8.62% / 1.2018 / -12.05%, OOS 1.2781.
- **Gates 12 of 13.** G1 replay err 5.97e-05, G2 2.26e-05, G3/G5/G7/G8/G9 exactly 0. **G12 FAILS**: the placebo's
  mean gross differs by up to 1.746e-02 (permuting intensity does not permute the weeks the book holds nothing),
  so comparand (2) is a close, not exact, gross match. The headline rests on the flat control and rule 8.
- **Survivorship (rule 9).** U56 / B135 current constituents; SMALL663 = 715 sub-$2B names less 52 with
  max_1d_move >= 1.0. A current-constituent panel mutes exactly the correlation spikes this idea is about, so the
  brake is flattered here and still loses.

Artefacts: `.console.txt`, `.grid.csv` (240 cells), `.walkforward.csv`, `.statistic.csv`, `.episode.csv`, `.gates.csv`.
