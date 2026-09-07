# Idea 384 — price the no-trade BAND's DRAWDOWN TAX across the record

**Lane B, 2026-09-07. Verdict: KILL — the premise is falsified. There is no drawdown tax:
across 3,360 committed observations the no-trade band `m` IMPROVES drawdown 57.7% of the
time and worsens it 32.4%, median +15.0 bp. And the queue's two candidate shapes are both
wrong: dMaxDD(m) is neither a constant of m nor proportional to the book's own DD — the two
models are separated by 0.2% of pooled MAE while each leaves residuals ~1.5× its own fitted
coefficient. The band is a SIGNED COST instrument (dSharpe > 0 at 36/36 fresh cells) with an
UNSIGNED drawdown effect (dMaxDD > 0 at 19/36, 16/33 non-degenerate). No rules change.
By-product: a 4b pass that survives rule 8 and, unlike its filed anchor, survives 25 bps.**

Script `2026-09-07_price-the-no-trade-BANDs-DRAWDOWN-TAX-across-the-record_B.py`; console
`.console.txt`; the 12,400-observation archive census in `.census.csv`; the per-m fit in
`.archive_shape.csv`; all 45 cells × 3 cost rungs in `.grid.csv`; the fresh-grid tax ladder
in `.tax.csv`; rule 8 in `.walkforward.csv`.

## Four gates, all exact, run before any new number was read

| gate | result |
|---|---|
| G1/G2 `fast_backtest` vs `engine.backtest`, returns and turnover, at 0 and 25 bps | **0.000e+00** on all four |
| G3 `sel_band(m=0)` vs `sel_hard(n)` on every rebalance day | **0** disagreements |
| G4 (B136, n=20, g=0.75, m=0, W) vs idea 333's committed grid row, 6 statistics | max \|d\| **0.000e+00** |

So idea 333's own cell is reproduced to the last bit, and everything below is measured on
the identical construction.

## [A] The archive census — what the record actually wrote

1,340 committed CSVs. 68 carry a column named exactly `m` alongside a MaxDD column, but
**the record overloads `m`**: only 15 of the 68 write it integrally (the no-trade band);
53 write it fractionally (idea 103's share dial). That is the same lexical defect idea 359
found in the band vocabulary, now visible in a column name, and it is why a naive census of
"files with a band dial" would have pooled two unrelated instruments.

Restricted to the integral `m`: **3,360 dMaxDD observations, 370 ladders, 10 scripts.**

| | worsens DD | improves DD | exactly 0 | median dMaxDD |
|---|---|---|---|---|
| pooled observations (n=3,360) | 32.4% | **57.7%** | 9.9% | **+15.0 bp** |
| one vote per ladder, at its largest m (n=1,089) | 29.9% | **64.0%** | 6.1% | **+66.6 bp** |

**The premise is backwards.** No single script drives it: per-script medians run +87.9,
+38.6, +17.5, +11.5, +8.1, +5.0, +3.0, 0.0, −20.9, −20.9 bp — 8 of 11 files positive.

### Neither shape fits

| m | n | H_const `a(m)` | H_scale `b(m)` | MAE const | MAE scale | rel. disp. const | rel. disp. scale | corr(dDD, DD0) |
|---|---|---|---|---|---|---|---|---|
| 2 | 236 | 0.0000 | 0.0000 | 0.0005 | 0.0005 | — | — | −0.053 |
| 5 | 463 | 0.0000 | 0.0000 | 0.0024 | 0.0024 | — | — | −0.116 |
| 10 | 561 | 0.0000 | 0.0002 | 0.0045 | 0.0045 | 97.11 | 86.44 | −0.092 |
| 15 | 216 | 0.0035 | 0.0171 | 0.0050 | 0.0054 | 1.46 | 1.70 | −0.244 |
| 20 | 793 | 0.0012 | 0.0049 | 0.0066 | 0.0069 | 5.63 | 6.88 | −0.266 |
| 30 | 228 | 0.0150 | 0.0775 | 0.0195 | 0.0203 | 1.30 | 1.42 | +0.583 |
| 40 | 303 | 0.0050 | 0.0204 | 0.0075 | 0.0079 | 1.51 | 1.44 | −0.101 |
| 50 | 292 | 0.0147 | 0.0606 | 0.0166 | 0.0155 | 1.13 | 1.26 | +0.316 |
| 999 | 268 | 0.0347 | 0.1505 | 0.0171 | 0.0163 | 0.49 | 0.63 | −0.195 |

Pooled MAE **H_const 0.07973 vs H_scale 0.07958** — H_scale "wins" by **0.2%**, which is a
tie, and the scale coefficient is the tighter of the two at only **2 of 7** m-levels. The
decisive column is `rel. disp.`: the residual is **0.49× to 97× the fitted coefficient
itself** (median ≈1.5×), so *whichever* model you pick, the noise around it is larger than
the effect it claims to describe. And `corr(dMaxDD, DD0)` pooled is **+0.008** — H_scale's
whole content is that a deeper book pays a deeper tax, and that correlation is zero.

**Answer to the queue's question as filed: neither. It is noise with a small positive mean.**

## [A2] Contrast — the OTHER "band" has the opposite signature

The 200d MA band WIDTH (column `band`, fractional; 4,792 observations, a *different*
instrument, never pooled here) behaves the way the queue expected the no-trade band to:

- worsens DD **55.5%** / improves 35.9%, median **−5.0 bp**; ladder-level **64.7%** worsen,
  median **−73.5 bp**
- `a(m)` is monotone in width: +0.0001 at 0.02 → −0.0076 at 0.12 → **−0.0282 at 0.30**
- corr(dMaxDD, DD0) **−0.258**, and H_const beats H_scale by 17.5%

So the record's two instruments sharing the word "band" have **opposite drawdown
signatures**: widening the MA band costs drawdown roughly linearly; widening the no-trade
band does not cost drawdown at all. Idea 359 flagged the shared lexicon as a naming defect;
this is the measurement showing it is a *substantive* one.

## [B] Direct re-measurement — 45 cells, all reported

Family pre-registered (idea 331/333's convention): top-n of the v1 composite with the vol
scaler OFF among RULES v1 eligible names, NORM weights g/k_t, gross 0.75, weekly, t+1. The
only two tuned parameters: **n ∈ {10, 20, 40} × m ∈ {0, 5, 10, 20, 40}**. Panel {U56, B136,
SMALL439} and cost rung {0, 10, 25} bps are reported axes.

Holdings are invariant in m to the last decimal at every cell (U56 n=20: mean names
**19.1075** at all five m), reproducing idea 359 independently.

**Degeneracy, and why it matters.** U56's eligible-name ceiling is 55, B136's 128,
SMALL439's 280. Three of the 36 band cells have n + m past their panel's ceiling and are
therefore not bands at all but the **hold-until-ineligible limit** (m = ∞ — idea 273/280's
m=999 arm). They are flagged `degenerate` in `.grid.csv` and every headline is quoted both
ways.

| | dMaxDD > 0 | median dMaxDD | dSharpe > 0 | dCAGR > 0 |
|---|---|---|---|---|
| all 36 band cells | 19/36 | +7.1 bp | **36/36** | 32/36 |
| 33 non-degenerate | 16/33 | −2.3 bp | **33/33** | — |

**A coin flip on drawdown; unanimous on Sharpe.** Median +0.0474 Sharpe (min +0.0009) for a
median **6.66×/yr** of turnover removed. The "exchange rate" the premise implies does not
exist: median **+2.13 bp** of MaxDD per 1.0×/yr of turnover removed, IQR **[−7.40, +8.84]**
— it straddles zero. Fresh-grid fits agree with the archive: H_const vs H_scale separated by
7.5%, corr(dMaxDD, DD0) **−0.125**.

### Idea 333's own cell, in context

Its −37.8 bp is real (reproduced at 0.000e+00) and it is an outlier draw. The DD-cap margin
along m on exactly its book (B136, n=20, @10 bps) is **not monotone**:

| m | 0 | 5 | 10 | 20 | 40 |
|---|---|---|---|---|---|
| MaxDD | −0.2005 | −0.2008 | **−0.1995** | −0.2043 | −0.2106 |
| 4b DD-cap margin | +0.0018 | +0.0015 | **+0.0028** | −0.0020 | −0.0083 |
| turnover ×/yr | 14.31 | 9.52 | 7.61 | 6.20 | 5.09 |

At **m = 10** the band clears the cap by *more* than the m = 0 anchor while removing 6.7×/yr
of turnover. Had idea 329 pre-registered m = 10 instead of m = 20, the same family would
have read "the band buys turnover for free". The B136 DD failure is a **one-cell draw**, not
a property of the instrument.

## [B3/B4] KEEP paths and rule 8

**4a: 0/45 at every cost rung.** 4b: **22/45 @0 bps, 17/45 @10, 5/45 @25.**

Rule 8, (n, m) chosen on 2008–2016 IS Sharpe @10 bps, 2017–2026 read once:

| panel | pick | OOS Sharpe | OOS CAGR | OOS MaxDD | regret | 4b |
|---|---|---|---|---|---|---|
| U56 | n=20, m=40 *(degenerate)* | **1.1892** | 14.34% | −15.27% | +0.008 | **PASS** |
| U56, non-degenerate only | n=20, m=20 | **1.1867** | 14.67% | −17.22% | — | **PASS** |
| B136 | n=10, m=20 | 0.9217 | 15.63% | −22.24% | +0.081 | FAIL (H2, DD) |
| SMALL439 | n=10, m=40 | 0.4797 | 8.05% | −30.74% | +0.160 | FAIL (all five) |

SPY OOS 0.8820 / 15.45% / −33.72%. Live RULES v2 OOS 1.2851 (U56) / 1.1185 (B136) / 0.5680
(SMALL439) — **every pick loses to the live book out of sample**, which is why none of this
is a rules proposal.

The U56 chooser's unrestricted pick is the degenerate hold-until-ineligible arm that **idea
280 already KILLED** as a candidate (at matched turnover the plain parent on a 6W cadence
beat it by +0.093 Sharpe). Restricting to genuine bands moves the pick to n=20, m=20 and
costs 0.0025 of OOS Sharpe — so the finding does not depend on the degenerate cell.

## By-product: a 4b candidate that fixes its anchor's cost fragility

(U56, n=20, gross 0.75, **band m=20**, weekly) clears all five 4b bars, is what rule 8's
non-degenerate chooser selects, and is a strict improvement on the record's already-filed
U56 top-20 anchor (idea 333's memo) on every axis:

| @10 bps | CAGR | Sharpe | MaxDD | H1 / H2 | OOS Sharpe | turn/yr | 4b @25 bps |
|---|---|---|---|---|---|---|---|
| anchor m=0 (filed) | 12.79% | 1.064 | −18.31% | 1.068 / 1.066 | 1.131 | 11.00 | **FAIL (H1)** |
| **m=20** | 12.87% | **1.112** | **−17.22%** | 1.144 / 1.093 | **1.187** | **5.26** | **PASS** |

The anchor's memo named cost fragility (breakeven 21.5 bps, fails 4b at 25) as its main
weakness. The band closes exactly that: every m ≥ 5 at U56 n=20 passes 4b at 25 bps. This is
the same family, not a new one — memo in
`2026-09-07_u56-top20-band-m20_4b_B_MEMO.md`, and it is **not** proposed for adoption.

## Caveats

All three panels are current-constituent lists (SURVIVORSHIP), so CAGR levels are optimistic
and 4b's CAGR floor is tested in the book's favour. The archive census is a census of what
the record *wrote*: a script that swept m but committed no CSV cannot enter it, and 53 of the
68 `m`-carrying files were excluded as the overloaded fractional dial. The 4a comparand
RULES v2 runs at its own live cadence and gross. SMALL439 starts 2010-01-04 and drops the 44
tickers with max_1d_move ≥ 1.0.

## Proposed consequences (no rules change)

1. **Retire "the band buys turnover with drawdown" from the record's working vocabulary.**
   It is true of one cell and false of the corpus.
2. **Split the band lexicon in the leaderboard.** `m` (no-trade / rank buffer) and `band`
   (MA width) have opposite drawdown signatures and must never share a column or a claim.
3. **Stop writing the no-trade band as `m`.** 53 of 68 files use `m` for a share dial; a
   distinct name (`nt` or `buffer`) would have made this census exact instead of heuristic.
