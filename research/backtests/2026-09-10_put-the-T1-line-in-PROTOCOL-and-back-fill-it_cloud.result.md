# Idea 426 — put-the-T1-line-in-PROTOCOL-and-back-fill-it (cloud, 2026-09-10)

**ANSWERED / the clause is DRAFTED and the back-fill is DONE, with two corrections to the
wording idea 426 proposed. Report-only: PROTOCOL.md is NOT edited, no RULES change, no book
promoted, no KEEP-candidate, no memo. RULES.md, scan.py, bot.py and baseline.py untouched.**

Script `2026-09-10_put-the-T1-line-in-PROTOCOL-and-back-fill-it_cloud.py`; outputs
`.txt .sites.csv .keys.csv .books.csv .wf.csv`. Two tuned parameters, exactly the queue's:
**FORM** ∈ {RANK, VALUE} and **TOL** ∈ {0, ONE-RANK-STEP}. Panel and the 40-key menu cap are
reported axes.

## Gates (all pass)

| gate | result |
|---|---|
| G1 | `fast_backtest` vs `engine.backtest` **1.041e-17** returns / **2.220e-16** turnover |
| G2 | live RULES v2 on U56 @10 bps reads **8.65% / 1.2092 / −11.90%** — the comparands are the real book |
| G3 | the two poles of the theorem: `px/px.shift(126)−1` moves rank **1.47e-04** / value **0.00e+00**; `px` moves rank **0.9355** / value **1.0000** |
| G0 | idea 433's committed 20-key table, re-run here with an independently written certificate: the PASS/FAIL partition agrees **20/20 at tol 0 and 20/20 at one rank step** (max difference in the moved fraction 0.0229 — it drew its own panel slice, so only the partition is expected exact) |

## 1. Correction one: the clause cannot be written as an equality

Idea 197/426's wording is `ranks(key(px)) == ranks(key(px @ diag(c)))`. **That test rejects keys
that are scale-free by construction.** On this record's own panel, float64 tie swaps move the
ranks of `px / px.shift(126) − 1` on 1.5e-4 of cells and of `px.pct_change()` on 1.2e-3. Read at
zero tolerance the certificate clears 28.8% of the record's reconstructible keys on the rank form
and 48.1% on the value form; read at **one rank step** (1/N of the *panel's* names) it clears
59.6% and 57.7%. The two classes are not close: scale-free keys move ≤ 8e-5 of cells, price-borne
keys ≥ 0.91 — four orders of magnitude, so any threshold between 1e-3 and 0.5 gives the identical
partition. **The clause must name a tolerance, and one rank step is the one the record's own
evidence supports.**

The zero reading is also *inconsistent between forms on the same key*: `px.shift(21)/px.shift(252)
− 1` fails tol-0 on RANK (1.45e-4) and passes it on VALUE (0.0), while
`px.pct_change().rolling(20).std()*√252` does the reverse (rank 0.0, value 7.9e-5). A clause
written at tol 0 would classify the same key differently depending on which form it named.

## 2. Correction two: T1 certifies the price-unit convention, NOT point-in-time honesty

Idea 197's framing calls the certificate "point-in-time honest". It is not: **a forward return is
perfectly scale-free.** Of the 52 reconstructible keys, **3 are non-causal as written** —
`px.shift(-5)/px − 1`, `px.iloc[-1]/px`, `px.iloc[-1]/px − 1.0` — and **all three PASS the value
certificate**. Before this run added a causality check, the top-10 book on `px.shift(-5)/px − 1`
**cleared BOTH KEEP paths on all three panels at both cost rungs**, with OOS Sharpe 10.98 (U56) /
13.43 (B136) / 19.39 (SMALL439) and SMALL439 CAGR 1744%. An oracle passes T1 and passes 4b. The
clause must therefore carry its scope in writing, and any adoption must pair it with the separate
causality test (perturb prices after a cut date; the key before it may not move) — implemented
here as `causal_check` and used to exclude those 3 keys from the consequence book.

## 3. The back-fill (the deliverable the queue asked for)

609 committed `.py` files scanned; 531 contain at least one self-contained price expression;
**2,188 expressions extracted at 731 committed sites → 126 distinct keys** after normalising the
price/volume variable name. Of those, **52 are evaluable as keys** (74 are not: not key-shaped 37,
`TypeError` 20, `KeyError` 16, all-NaN 1). Full pass/fail column in `.keys.csv`, one row per key
with `n_sites`, `n_files`, `ncols`, `single_col`, `causal`, `moved_rank`, `moved_value` and the
four verdicts.

| reading of the clause | keys passing (of 52) | of which single-column (vacuous) |
|---|---|---|
| RANK, tol 0 | 15 (28.8%) | — |
| VALUE, tol 0 | 25 (48.1%) | — |
| RANK, one rank step | 31 (59.6%) | **8** |
| **VALUE, one rank step** (recommended) | **30 (57.7%)** | **7** |

**Weighted by committed sites, the VALUE/1-step certificate clears 610 of 731 (83.4%)** — the
record's actual usage is dominated by scale-free keys. The forms disagree on **1 of 52 keys**
(`px["SPY"] if "SPY" in px.columns else px.mean(axis=1)`, a single-column market aggregate:
rank 0.0, value 1.0), so on this corpus the argument for naming the value form is the **vacuous
single-column class**, not the disagreement rate — a softening of idea 433's 6-of-20, which was
measured on a deliberately adversarial corpus.

What actually fails, by sites: `px.rolling(200).mean()` (68), `px.dropna(how="all").ffill()` (10),
`px.drop(columns=["SPY"])` (9), `px` (8), `px.diff()` (2), `(px*vol).rolling(20).median()` (2).
**Most of those are not selection keys** — they are panel-shaped intermediates and comparands
(`px > ma` is scale-free even though `ma` is not). That is a limit of any expression-level
back-fill and it is why clause (4) attaches the column to the *selection* key, not to every price
expression in a file.

## 4. What the clause costs: zero (PROTOCOL 4 and 8)

A top-10 equal-weight book (gross 0.75, weekly, t+1) on each of the 39 most-used reconstructible,
multi-column, non-degenerate, **causal** keys, three panels, 10 and 25 bps — 114 books, 228 rows,
all committed in `.books.csv`:

* **Rule 8** (key chosen on 2008–2016 by IS Sharpe, 2017–2026 read once): restricting the menu to
  the T1-passing keys **changes the pick in 0 of 3 panels at both rungs**, ΔOOS Sharpe
  **+0.0000**, under either form. The clause deletes nothing anyone would have chosen. Confirms
  idea 433's finding on an entirely different menu (harvested keys, not hand-written screens).
* The **T1-FAIL-only** menu is much worse where it can be read at all: OOS Sharpe 0.69 vs 1.08
  (B136), 0.85 vs 1.04 (U56), **−0.41 vs 0.92** (SMALL439). Mean OOS Sharpe over the whole menu,
  PASS vs FAIL: +0.11 (U56), +0.18 (B136), +1.26 (SMALL439). This is *not* evidence for the
  clause: T1-failing keys are mostly price levels, which are bad rankers for reasons that have
  nothing to do with the price-unit convention.
* **KEEP paths: 4b 0/114 and 4a 0/114 at both rungs, BOTH 0.** The picks OOS @10 bps: U56 18.86%
  / 1.0351 / −24.32%, B136 24.25% / 1.0817 / −28.15%, SMALL439 29.19% / 0.9218 / −51.80%, against
  RULES v2 OOS 1.2876 / 1.1206 / 0.5665 and SPY 15.3–15.5% / 0.876–0.882 / −33.72%. Every pick
  beats SPY's OOS Sharpe and none clears 4b, because all fail the drawdown cap (60% of SPY's
  −33.72% is −20.2%). **No KEEP-candidate, no memo.**

## 5. The clause, in the exact wording it would take

Printed verbatim in the script (constant `CLAUSE`) and in `.txt`. Six sub-clauses: (0) what it is;
(1) it must name a tolerance — moved fraction ≤ 1/N with c ~ lognormal(0, 0.25), 8 draws;
(2) name the VALUE form and report RANK beside it, because RANK clears single-column keys
vacuously; (3) **T1 is not a look-ahead test** and must be paired with a causality check;
(4) the column attaches to the selection key and FAIL is not automatically a KILL; (5) it is a
reporting clause, no verdict may turn on it, and its measured book cost is zero.

**Recommendation for the Sunday review: adopt (0)–(5) as one clause or none.** Adopting (0) alone
— the equality idea 426 drafted — would reject the record's own momentum keys and certify its
oracles.

## Caveats

* **SURVIVORSHIP (PROTOCOL 9).** B136 and SMALL439 are current-constituent lists; SMALL439 drops
  the 44 names with `max_1d_move ≥ 1.0`. No book here is a tradable estimate, and the load-bearing
  quantity is the menu-minus-menu contrast inside one panel.
* **Harvest coverage is a lower bound.** Only self-contained expressions are reconstructible: an
  expression referencing any other local is counted and excluded (2,895 sites). The price-name
  allowlist is `{px, prices, pxs, price, closes, adj}` and the volume allowlist
  `{vol, volume, shares, vols}`; keys written on other variable names (notably `q`, which is
  ambiguous with quantile) are missed. 74 of the 126 distinct expressions do not evaluate to a
  key on this panel and are reported with their reason rather than dropped.
* The certificate panel is one deterministic SMALL439 slice (750 days × 140 names, σ 0.25, 8
  draws, seed 426), share volume from `data/volume_small.csv[.gz]` — the same construction idea
  433 used, so the two tables are comparable. The moved fractions are panel-dependent; the
  PASS/FAIL partition at one rank step was not (20/20 against idea 433's independent slice).
* The 39-key menu is capped by usage frequency, a reported axis. Ranking books on intermediates
  such as `px.rolling(200).mean()` is not what those expressions are for; they are included so
  that the T1-FAIL arm is not empty, and the C2 comparison is explicitly labelled confounded.
