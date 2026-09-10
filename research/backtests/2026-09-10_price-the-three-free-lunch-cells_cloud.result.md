# Idea 495 — price the three "free lunch" cells

**ANSWER: THREE DRAWS OUT OF TWELVE. KILL.** The free lunch reproduces exactly on all three parent
cells, and then **survives on 2 of 80 resamples of the two large-cap panels' own names (2.5%)**,
where the mean effect is not a free lunch at all but the ordinary CAGR-for-Sharpe trade with a
**large** Sharpe cost (mean ΔOOS Sharpe **−0.174** on B136, **−0.159** on BSTK100 for +2.16 / +1.25
pp of CAGR). The queue's framing is backwards: shallow n is what `S_CAGR` **always picks**, not what
makes it win. No RULES change, nothing promoted; RULES.md, scan.py, bot.py, baseline.py, PROTOCOL.md
untouched.

3 panels × 40 seeded resamples × 3 n-floors = **360 selector cells** plus the 3 parent cells,
**all 369 reported**; 861 priced arms committed. 10 bps, weekly, t+1, gross 0.75.
Two tuned parameters: `seeds` (40, the queue's number) and `nfloor` ∈ {5, 10, 20}.

## Gates (pre-registered, printed before any hypothesis number) — ALL PASS
- **G1** `fast_bt` vs `engine.backtest` on B136/FWD20 = **1.388e-17** over 4,697 finite rows
  (2 engine-NaN warm-up rows, 0 inside the scored window).
- **G2** every resample is a strict subset of its parent's tradable set at the stated coverage:
  102/136 = **0.750**.
- **G3** the n menu is nested (FWD5's holdings inside FWD10's, every day): **0 violations**.

## Part A — the three parent cells reproduce idea 270 exactly (nfloor = 5)

| cell | S_SHARPE picks | S_CAGR picks | ΔOOS Sharpe | ΔOOS CAGR | |
|---|---|---|---|---|---|
| B136 / n | FWD10 (OOS 0.781 / 12.77%) | **FWD5** (0.824 / 16.39%) | **+0.0437** | **+3.63 pp** | FREE LUNCH |
| BSTK100 / n | FWD10 (0.749 / 12.34%) | **FWD5** (0.779 / 15.35%) | **+0.0306** | **+3.01 pp** | FREE LUNCH |
| S5_M120 / n | EWall (0.135 / 0.87%) | **FWD5** (0.253 / 3.19%) | **+0.1175** | **+2.33 pp** | FREE LUNCH |

It is already fragile in its own second parameter: at **nfloor = 10** the two selectors agree on all
three panels (Δ = 0 by construction), and at **nfloor = 20** the sign flips to **−0.1349** (B136)
and **−0.1185** (BSTK100). The free lunch exists only when FWD5 is on the menu.

## Part B/C — 40 seeded resamples per panel at 75% coverage (seeds 2000–2039)

| panel | nfloor | disagree | FREE LUNCH | reverse | p(FL \| disagree, coin) | mean ΔOOS Sharpe | mean ΔOOS CAGR |
|---|---|---|---|---|---|---|---|
| B136 | 5 | 34/40 | **1/40** | 3 | 0.0000 | **−0.1743** | +2.16 pp |
| B136 | 10 | 33/40 | 0/40 | 6 | 0.0000 | −0.1520 | +1.05 pp |
| B136 | 20 | 27/40 | 0/40 | 1 | 0.0000 | −0.0835 | +0.75 pp |
| BSTK100 | 5 | 34/40 | **1/40** | 7 | 0.0000 | **−0.1594** | +1.25 pp |
| BSTK100 | 10 | 29/40 | 0/40 | 13 | 0.0000 | −0.1553 | +0.03 pp |
| BSTK100 | 20 | 32/40 | 0/40 | 8 | 0.0000 | −0.0910 | +0.18 pp |
| S5_M120 | 5 | 15/40 | **10/40** | 5 | **0.3018** | **+0.0256** | +0.41 pp |
| S5_M120 | 10 | 13/40 | 9/40 | 2 | 0.2668 | +0.0328 | +0.58 pp |
| S5_M120 | 20 | 11/40 | 6/40 | 3 | 1.0000 | +0.0035 | +0.05 pp |

Pooled at nfloor = 5: disagree **83/120 (69.2%)**, free lunch **12/120 (10.0%)**, reverse
15/120 (12.5%), mean ΔOOS Sharpe **−0.1027** for **+1.27 pp** of CAGR.

**The one asymmetry worth naming, and it points the opposite way from the queue's hypothesis:**
the only panel with a *positive* mean is **S5_M120, the SMALL-CAP one** — not the large-cap panels
the queue proposed. And even there the rate is **10/40** with **p = 0.30** against a coin flip on
the disagreeing cells, i.e. indistinguishable from chance, on books whose OOS Sharpe is 0.14–0.17
with a −50% drawdown.

## Why it looked like shallow n was the cause

`S_CAGR` picks **FWD5 or FWD10 in 40/40 seeds** on B136 and on BSTK100 — and still loses **39/40
times** on each. Shallow n is what maximising IS CAGR *always* selects (the shallowest book has the
highest IS CAGR almost by construction), so "all three picked FWD5/FWD10" carries no information
about why they won. On S5_M120, where `S_CAGR` picks shallow in only 22/40 seeds, the free lunch
splits **9/22 shallow vs 1/18 otherwise** — the one place the shallow-n story has any content, and
it is on the panel the queue excluded.

## Neither selector beats do-nothing (nfloor = 5, resamples)

| panel | S_SHARPE > EWall (OOS Sharpe) | S_CAGR > EWall | mean OOS Sharpe: S_SHARPE / S_CAGR / EWall |
|---|---|---|---|
| B136 | **0/40** | **0/40** | 0.9360 / 0.7617 / **1.0118** |
| BSTK100 | 9/40 | **0/40** | 0.9184 / 0.7590 / **0.9841** |
| S5_M120 | 14/40 | 22/40 | 0.1411 / **0.1667** / 0.1121 |

## Both KEEP paths, all 369 selected books (rule 8 is intrinsic: IS 2009–2016 chooses, OOS read once)

**4a: 0/369 for both selectors.** **4b: S_SHARPE 35/369, S_CAGR 3/369** — choosing the dial on CAGR
destroys 32 of the 35 4b passes the Sharpe selector finds. Fail-bar census over 700 failing books:
`H1;H2;OOS;DD;CAGR` 242, `H2;OOS;DD` 194, `DD` alone 87, `H2;DD` 58, `CAGR` alone 36.

## Verdict

**KILL.** The free lunch is three draws out of twelve. It survives 2/80 on the large-cap panels it
was attributed to; the mean there is a −0.16 Sharpe loss for +1–2 pp of CAGR, which is the record's
own selection-loses result with a bigger price tag than the −0.014 idea 270 published. Nothing here
is capital-worthy: on both large-cap panels the best selector loses to holding the whole eligible
list equal-weighted.

## Caveats
- **Survivorship:** B136/BSTK100 are current constituents of a current screen and S5_M120 is drawn
  from a current sub-$2B screen (483 names after dropping `max_1d_move ≥ 1.0` per `small_meta.csv`),
  so every LEVEL is biased up. The free-lunch RATE compares two selectors on the same books within
  a panel and is not.
- Resamples are 75% of each parent's own names, so they are correlated with the parent and with
  each other; the 40 seeds are not 40 independent panels, which makes the 1/40 rates if anything
  *generous* to the hypothesis.
- `S5_M120` is itself one seeded draw (idea 270's seed 5); its resamples inherit that draw.
