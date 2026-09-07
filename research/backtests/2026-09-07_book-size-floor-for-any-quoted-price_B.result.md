# Idea 124 — book-size-floor-for-any-quoted-price (lane B, 2026-09-07)

**Verdict: SPLIT. The queue's deliverable is a KILL — there is NO book-size number PROTOCOL
can state, because the admissible share is NON-MONOTONE in n, disagrees between panels (40 vs
136) and never reaches the bar on all rows at ANY rung including the whole panel. What
survives is (a) a correction: idea 122's headline statistic is conditioned on a set that
shrinks with n, which is what manufactures the pattern it reads; (b) an unconditional reading
that lands exactly on PROTOCOL's existing informal "~20 names" and cannot be sharpened; and
(c) a relocation — the floor that matters is on the price list's ORDERING (n >= 40), not on
its denominator's sign. No RULES change, no book promoted, no KEEP claimed. RULES.md, scan.py,
bot.py, baseline.py and PROTOCOL.md untouched.**

Script `2026-09-07_book-size-floor-for-any-quoted-price_B.py`; console `…_B.console.txt`;
data `…_B.{grid,draws,d3,signtest,floorcurve,paramgrid,walkforward,walkforward_floor,
reproduction}.csv`. 448 arm-points (7 books x 16 treated arms x 2 published rungs x 2
universes) on the D1/D2 axes, plus **28,560 sub-panel backtests** on D3 (2 universes x 3 drop
fractions x 40 draws x 7 books x 17 arms). Total 5,296 s.

## 0. Reproduction gates — all PASS before any new number was read

| gate | result |
|---|---|
| G1a TOP20 rung == idea 94's `TOP20` targets (all 11 gate/conv combos) | **0.000e+00** |
| G1b TOPall rung == idea 94's `EWall` targets (evaluated slice) | **0.000e+00** |
| G1c V1u == idea 94's `V1u` targets | **0.000e+00** |
| G2 control `run()` == `engine.backtest` | **0.000e+00** |
| G3 idea 94's **committed** `pricelist.csv`, 64 rows (TOP20 + EWall, both unis, both rungs) | max abs diff dCAGR 8.9e-16, dMaxDD 1.8e-15, rate 1.1e-16 |
| LIVE RULES v2 on u56 @10 bps | 8.66% / 1.2056 / −12.05%, halves 1.2259/1.1908 — reference **exact** |

The ladder therefore *nests* two of idea 94's three books exactly, which is what makes the
book axis a single-family ladder rather than idea 122's three-way confound (V1u is 5 names
AND vol-scaled; TOP20 is 20 names, plain composite; EWall is every name, unranked).

## 1. The floor curve — the queue's question, answered directly

Admissible = D1(sign > 0 at 0/5/10/25 bps) AND D2(sign > 0 in BOTH windows) AND D3(sign > 0
in >= tau of 40 draws deleting q of the names). Headline (q, tau) = (0.10, 0.90), inherited
unchanged from ideas 119/122.

| rung n | 3 | 5 | 10 | 20 | 40 | all |
|---|---|---|---|---|---|---|
| **u56** share of PUBLISHED rows admissible | 0.556 | **1.000** | 0.864 | 0.727 | **1.000** | 0.958 |
| **u56** share of ALL 32 arm-rows admissible | 0.313 | 0.375 | 0.594 | 0.563 | 0.750 | 0.719 |
| **broad** share of PUBLISHED rows | 0.421 | 0.714 | 0.389 | 0.333 | 0.786 | **1.000** |
| **broad** share of ALL 32 arm-rows | 0.250 | 0.313 | 0.219 | 0.281 | 0.688 | 0.750 |

(Off-ladder V1u, 5 names + vol scaler: u56 0.333 published / 0.250 all; broad 0.471 / 0.250.)

- **P1 (monotone in n) is REFUTED on both panels.** u56 peaks at n=5, dips at n=20, peaks
  again at n=40. broad reads 0.714 at n=5 and 0.333 at n=20.
- **P2 (floor in [10, 20]) is REFUTED.** n\* = **40** on u56 and **136 (the whole panel)** on
  broad at the 90% bar.
- **P4 (the same n\* on both panels) is REFUTED.** 40 vs 136. The floor is neither an absolute
  count nor a fixed share of the panel (40/56 = 0.71 vs 136/136 = 1.00), so **no number is
  statable** — which is exactly the deliverable the queue asked for.
- On the **unconditional** reading (all 32 arm-rows, not just the priced ones) the bar is
  **NOT REACHED AT ANY RUNG on either panel**, including the full panel. There is no n at
  which 90% of this menu's denominators are sign-stable.

Both tuned parameters are inert. Across all **12 (q, tau) grid points** (`…paramgrid.csv`):
n\*_published = 40 on u56 at **12/12**; on broad = 136 at 10/12 and 40 at 2/12;
n\*_all-rows = NOT REACHED at **24/24** panel-grid-point combinations. The non-monotone shape
(n=5 high, n=10/20 low) is present at every one of the 12 points.

## 2. Why the curve is non-monotone — idea 122's statistic is conditioned

A row is "published" only when it buys > 0.10 pp of MaxDD (idea 94's floor). That set is not
fixed along the ladder: published rows per rung are u56 **[18, 12, 22, 22, 24, 24]** and broad
**[19, 14, 18, 27, 28, 24]**. The 5-name rung has the FEWEST priceable arms — a concentrated
book's instruments mostly cannot move its drawdown measurably at all — so `adm_pub` at n=5 is
computed over 12 survivors that are, by construction, the biggest movers.

The unconditional draw-level statistic reverses the reading completely:

| median `frac_pos_full` over 40 draws (q=0.10) | TOP3 | TOP5 | TOP10 | TOP20 | TOP40 | TOPall | V1u |
|---|---|---|---|---|---|---|---|
| u56 | 0.775 | **0.363** | 1.000 | 1.000 | 1.000 | 1.000 | 0.788 |
| broad | 0.863 | **0.513** | 0.875 | 1.000 | 1.000 | 1.000 | 0.513 |
| u56 mean | 0.630 | 0.563 | 0.739 | 0.788 | 0.805 | 0.772 | 0.650 |
| broad mean | 0.777 | 0.600 | 0.714 | 0.873 | 0.831 | 0.750 | 0.547 |

**TOP5 is the LEAST sign-stable rung on the ladder on both panels and simultaneously the one
that scores 1.000 and 0.714 on idea 122's statistic.** That is the whole explanation of the
non-monotonicity, and it is a defect in the statistic, not in the book.

**P3 (it is the COUNT, not the vol scaler) is CONFIRMED on the metric it was written against**
— TOP5 `adm_pub` 1.000 vs V1u 0.333 (u56) and 0.714 vs 0.471 (broad) — **and REVERSED on the
better metric** on u56: median frac_pos TOP5 **0.363** vs V1u **0.788**. On broad they tie at
0.513. So idea 122's address ("the failures are the 5-name book") is right about V1u, but the
count/scaler decomposition it implies does not survive an unconditional reading. Report both.

The mean unconditional curve is a shallow interior maximum (u56 rises 0.630 -> 0.805 at n=40
then falls to 0.772 at n=56; broad peaks 0.873 at n=20 then falls to 0.750 at n=136), so even
unconditionally the ladder does not have a floor shape — it has a hump.

## 3. Rule 8 / W1 — the floor does not survive its own walk-forward

Screen recomputed on 2009–2016 only (D1 on IS returns + D3 on IS-window draws; D2 has no
IS-only form, per idea 122); 2017–2026 then read once.

| | n\*_IS | n\*_OOS | n\*_full |
|---|---|---|---|
| u56 | **NOT REACHED at any rung** | **5** | 40 |
| broad | 136 | 136 | 136 |

On u56 the in-sample window supports no floor at all while the out-of-sample window supports
the *smallest* rung on the ladder; on broad both windows agree only at the degenerate top rung
("use every name"). This is another in-sample-chooser miss (the record's running count stood
at 14 at idea 357) and it is decisive here: a number chosen on the IS half of this sample
would have been wrong in both directions.

## 4. Rule 8 / W2 — where the real floor is: the ORDERING, not the sign

Idea 94's selector S1 (among arms buying >= 1.0 pp of IS MaxDD, the lowest IS rate) applied
inside each rung, OOS read once. `spearman` is the within-cell rank agreement between the IS
price and the OOS price — a price list whose ordering re-shuffles is not a price list.

| rung n | 3 | 5 | 10 | 20 | 40 | 56 | 136 |
|---|---|---|---|---|---|---|---|
| mean OOS Sharpe of the S1 pick | 0.852 | 0.901 | 0.856 | 0.895 | 1.069 | 1.173 | 1.099 |
| mean OOS Sharpe of the cell CONTROL (no instrument) | 0.834 | 0.933 | 0.890 | 0.994 | 1.057 | 1.130 | 1.097 |
| mean OOS CAGR of the pick | 21.2% | 19.5% | 13.3% | 11.2% | 13.6% | 13.0% | 12.5% |
| mean OOS MaxDD of the pick | −36.7% | −30.5% | −20.5% | −19.8% | −21.9% | −17.8% | −22.7% |
| **mean spearman(IS rate, OOS rate)** | +0.002 | **−0.321** | +0.105 | **−0.529** | **+0.573** | **+0.442** | **+0.752** |

References on the same OOS window: SPY 0.882 (CAGR 15.45%); LIVE RULES v2 **1.285** (u56) /
**1.119** (broad); RULES v1 0.470 (u56). Off-ladder V1u: mean OOS Sharpe **0.372**.

Two things follow. First, **the instrument is worth nothing at any rung** — the S1 pick beats
its own do-nothing control on mean OOS Sharpe at n=3, 40, 56 and 136 and loses at n=5, 10 and
20, and no rung's pick beats the live RULES v2 book. Second, **the price list's ordering is
noise or negative below n=40 and positive at and above it** (+0.573 / +0.442 / +0.752). The
low rungs are also thin: the number of arms priceable in BOTH windows is 4–10 of 16 below
n=40 against 11–13 at and above it, so at n<=20 there is both too little to order and no
agreement in what ordering there is. n=20's −0.529 is carried by a −1.000 on 3 pairs
(broad@10bps) and should be read as "undefined", not "reversed".

## 5. Both KEEP paths (PROTOCOL rule 4) — all 448 arm-points

**4a (vs the LIVE RULES v2 baseline): 0 / 448.** 4a against RULES v1 — idea 94's original
comparand, kept for continuity — is 111/448, which is a statement about v1, not about these
books. **4b: 50 / 448**, and 46 of the 50 have a QUOTABLE price (denominator admissible on all
three axes).

The 4b passes are themselves gated by book size: u56 has 0 at n=3 and 0 for V1u, 3 at n=5,
1 at n=10, 15 at n=20, 11 at n=40, 8 at n=all; broad has **0 below n=40**, 6 at n=40 and 6 at
n=all. So the book-size effect that is real and reproducible is on the 4b bars, not on the
denominator's sign.

**By-product, filed as PARK, NOT promoted.** The best 4b cell is u56 / TOP40 / `band3-rw`
@10 bps: CAGR **11.36%**, Sharpe **1.2112**, MaxDD **−15.66%**, halves 1.2503 / 1.1861, OOS
Sharpe **1.2761**; 4b margins H1 +0.294, H2 +0.352, OOS +0.394, DD +4.57 pp, CAGR +0.70 pp;
it also passes at 25 bps but on a +0.12 pp CAGR margin. It is not a candidate: the live RULES
v2 book on the same panel reads 8.66% / **1.2056** / −12.05% with OOS **1.2851**, i.e. this
cell is a wash on Sharpe, *worse* on drawdown, and adds a top-40 ranking step to a book that
currently has none. And it is not rule-8 clean — idea 94's IS selector picks `ebud-0.10` in
that cell (OOS Sharpe 1.1508), never `band3-rw`.

## 6. What PROTOCOL can and cannot say

Cannot: any sentence of the form "a quoted price needs at least N names". No N exists — the
3-axis admissible share never reaches 90% of all rows at any rung on either panel, the two
panels' published-row answers differ by a factor of three, and the IS half of the sample
supports a different answer again.

Can (report-only, proposed for Sunday review, not written here):

> A published `pp CAGR per pp MaxDD` price must state the mean name count of the book it was
> measured on. Below **20 names** the denominator's sign is not reproducible under name
> resampling (median draw-level positive fraction 0.363–0.863 at n <= 10 against 1.000 at
> n >= 20 on both panels), and below **40 names** the ORDER of the resulting menu does not
> survive out of sample (mean spearman(IS rate, OOS rate) +0.002 / −0.321 / +0.105 / −0.529
> at n = 3/5/10/20 against +0.573 / +0.442 / +0.752 at n = 40/56/136). Neither threshold is a
> pass/fail bar: the admissible share is non-monotone in n and panel-dependent, so the count
> is a caveat to quote, never a screen to apply.

That first number is PROTOCOL's existing informal "~20 names", now measured rather than
asserted. The run's contribution is that it cannot be sharpened, and that the second
threshold — the one that decides whether a menu is usable at all — is higher and had not been
measured.

## 7. Caveats

SURVIVORSHIP: both universes are current-constituent lists, so every absolute CAGR above is
optimistic; the subject here is the SIGN of a difference between two arms sharing a panel and
the same days, which is far less exposed. The draw axis deletes names uniformly and re-forms
each book on the sub-panel, so at q=0.20 the u56 n=40 rung holds 40 of 45 surviving names and
is nearly the whole panel — the high rungs of the ladder compress toward TOPall on small
panels, which is one reason the n=40 and n=all columns move together. `frac_pos` is computed
at the PROTOCOL rung only (10 bps); the cost axis is carried separately as D1.
