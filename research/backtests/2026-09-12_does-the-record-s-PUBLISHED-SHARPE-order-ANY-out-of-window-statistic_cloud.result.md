# Idea 833 — does the record's PUBLISHED SHARPE order ANY out-of-window statistic?
cloud lane, 2026-09-12, idea 2 of 2 · script
`2026-09-12_does-the-record-s-PUBLISHED-SHARPE-order-ANY-out-of-window-statistic_cloud.py`

**ANSWER: NO. Under the only honest reading (predictor measured on ≤2016, target on 2017+), the
published Sharpe's six Spearmans are −0.2797, −0.0699, −0.4825, −0.1399, +0.0582, −0.0381 — five of
six NEGATIVE, all six inside the n=12 null band (|ρ| ≤ 0.5804). The +0.5385 idea 831 measured, and
the +0.6084 against OOS Sharpe, are artefacts of a predictor computed on a window that CONTAINS its
own target.** KILL for the ordering claim; no KEEP claimed, no book promoted, no memo. `RULES.md`,
`PROTOCOL.md`, `research/scan.py`, `products/bot/bot.py`, `research/baseline.py` untouched.

## The headline (predictor = full-sample Sharpe, ordering set = MEMO12, n = 12)

| target | (a) FULL→OOS ρ | Pearson | perm p | (b) IS→OOS ρ | perm p |
|---|---|---|---|---|---|
| OOS_Sharpe | **+0.6084** | +0.7007 | 0.0388 | **−0.2797** | 0.3800 |
| OOS_CAGR | +0.3357 | +0.1200 | 0.2884 | −0.0699 | 0.8318 |
| OOS_MaxDD | −0.0140 | +0.2301 | 0.9724 | −0.4825 | 0.1132 |
| share_3y (831's) | **+0.5385** | +0.6384 | 0.0730 | −0.1399 | 0.6693 |
| cost_surv | **+0.6479** | +0.5665 | 0.0246 | +0.0582 | 0.8612 |
| gross_band | +0.1222 | +0.0443 | 0.7120 | −0.0381 | 0.9056 |

Two-sided 95% null band at n = 12 is |ρ| ≤ 0.5804 (20,000 fixed-seed permutations), so under (a)
only cost_surv and OOS_Sharpe clear it at all, and neither reaches the pre-registered +0.70.
Under (b) nothing does, in either direction.

**2 of 10 pre-registered hypotheses PASS** (H_REPRO, H_SIG). FAIL: H_ANY, H_OOS, H_COST, H_GROSS,
H_SIGN (OOS_MaxDD is negative), H_SETFREE (OOS_CAGR spread 0.3714 and gross_band 0.3357 across the
four ordering sets), H_STATBEST, H_R8CLAIM.

## What reading (a) is actually measuring

The two biggest correlations in the whole 240-cell grid are identities, not forecasts:

* **MAXDD → OOS_MaxDD, ρ = +1.0000** (MEMO12, MEMO8 and U56ONLY alike) — because **11 of the 12
  books' full-sample MaxDD IS their OOS MaxDD to 1e-9**: every one of these books took its deepest
  drawdown after 2017-01-01, so the "predictor" and the "target" are the same number.
* **H2 → OOS_Sharpe, ρ = +0.9510** (MEMO14) — the second half of the sample is mostly the OOS
  window.

That is the mechanism behind the whole of reading (a). Mean |ρ| over the 120 (a) cells is 0.4682
against 0.3036 over the 120 (b) cells, 22 of 120 (a) cells clear +0.70 against **1 of 120** under
(b) — and that one is `CAGR → OOS_CAGR` on **MEMO14**, the set that adds the two known-weak
comparands LIVE and V1, i.e. the correlation is bought by putting two books in the corpus everyone
already knows are worse.

## Rule 8 on the claim, read once

The (statistic, ordering set) pair chosen under (a) by highest ρ against OOS_Sharpe is
**(H2, MEMO14) at +0.9516**; read once under (b) it is **+0.0901** — a gap of **0.8615** against a
pre-registered bar of 0.30. **H_R8CLAIM FAILS by a factor of three.**

The concrete version of the same fact: the best book by **published full-sample Sharpe** is **R3**;
the best by **OOS Sharpe** is **K8**; and the best by the number a reader actually had in
2016, **IS Sharpe, is R4 — which has the WORST OOS Sharpe of the twelve (1.0400)**. Three different
books, and the reader's own pick is last.

## What a reader would have gotten

Top 6 by published Sharpe `[R3, K6, K8, K4, K5, K7]` against bottom 6 `[K3, R1, K2, R4, R2, K1]`:

| target | top mean | bottom mean | delta |
|---|---|---|---|
| OOS_Sharpe | 1.2673 | 1.1605 | +0.1068 |
| OOS_CAGR | 0.1314 | 0.1372 | **−0.0058** |
| OOS_MaxDD | −0.1577 | −0.1751 | +0.0174 |
| share_3y | 0.3059 | 0.2036 | +0.1023 |
| cost_surv | 49.0 bps | 30.0 bps | +19.0 |
| gross_band | 0.1875 | 0.2083 | **−0.0208** |

Top half wins 4 of 6; a coin wins 3.

## Gate H_REPRO — PASS, exactly

Rebuilt from idea 831's own constructors: full Sharpe max|d| **2.2e-16**, full CAGR 8.3e-17, OOS
Sharpe 2.2e-16 against `..ENTRY-DATE-CENSUS_B.books.csv`; share_3y max|d| **8.2e-17** against its
`.deliverable.csv`; and 831's headline Spearman(published Sharpe, share_3y) = **+0.5385** and
Pearson **+0.6384** reproduce to 4 decimals. The corpus is 831's, not a re-definition.

## PROTOCOL rule 8 on the books, and both KEEP paths

All 12 books at 10 bps, next-day fill, own memo cadence and gross; OOS = 2017-01-01..

| | K1 | K2 | K3 | K4 | K5 | K6 | K7 | K8 | R1 | R2 | R3 | R4 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| full Sharpe | 1.063 | 1.117 | 1.158 | 1.210 | 1.202 | 1.223 | 1.169 | 1.223 | 1.146 | 1.088 | 1.226 | 1.126 |
| OOS CAGR | 14.4% | 15.2% | 13.8% | 12.7% | 12.7% | 15.1% | 6.4% | 16.0% | 12.0% | 12.4% | 16.0% | 14.5% |
| OOS Sharpe | 1.130 | 1.235 | 1.286 | 1.269 | 1.278 | 1.261 | 1.187 | **1.394** | 1.165 | 1.106 | 1.215 | 1.040 |
| OOS MaxDD | −18.3% | −17.2% | −12.4% | −15.5% | −15.9% | −19.4% | −11.1% | −12.7% | −19.1% | −18.7% | −20.0% | −19.4% |
| cost_surv (bps) | 20 | 40 | 25 | 50 | 40 | 100 | −1 | 30 | 50 | 20 | 75 | 25 |
| gross_band | 0.250 | 0.250 | 0.125 | 0.125 | 0.125 | 0.250 | 0.000 | 0.250 | 0.125 | 0.125 | 0.375 | 0.375 |

Comparands on the same windows: **RULES v2 LIVE** full 8.63% / 1.202 / −12.05%, OOS 9.47% / 1.278 /
−12.05%. **SPY** full 15.16% / 0.886 / −33.72%, OOS 15.33% / 0.877 / −33.72%.
**Fixed-window 4b: 11 of 12 PASS** (only K7 fails, on the CAGR floor). **4a: 0 of 12 PASS** — not
one committed 4b book beats the live RULES v2 book on both halves at no worse drawdown.
OOS-local 4b: 11 of 12 PASS. Every book's OOS CAGR is below SPY's 15.33% except K8 (16.04%) and R3
(16.00%); the whole corpus buys its Sharpe with drawdown, not with return.

## Caveats

n is 8–14. Nothing here can distinguish a ρ of 0.5 from noise, which is the point: the record has
been quoting exactly such numbers without a null band. Permutation p-values use 20,000 fixed-seed
shuffles (seed 833), so every number reproduces. SURVIVORSHIP: U56 and B136 are current-constituent
lists, so every level is optimistic; this run reads orderings across books on one panel, which
survivorship moves far less than a level, but no CAGR or Sharpe printed here is a capital claim.
`cost_surv` = −1 means the book fails 4b already at 0 bps. No gross rung exceeds 1.000, so
PROTOCOL rule 2's no-leverage clause is never bent to widen a band.

## Follow-ups filed
836 (re-read every committed memo headline as an IS-only number and report which memos change),
837 (does ANY cheap-to-compute book statistic order OOS Sharpe out of window at n ≥ 30).
