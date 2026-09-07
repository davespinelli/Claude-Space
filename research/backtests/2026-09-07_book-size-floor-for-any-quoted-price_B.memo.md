# Memo — idea 124: there is no book-size number, and here is the sentence that replaces it

1. **NOT a KEEP.** 4a 0/448 against the live RULES v2 book; 4b 50/448, none promoted. This
   memo proposes a PROTOCOL reporting clause only. RULES.md is untouched and unchanged.
2. The queue asked for "a number PROTOCOL can state instead of '~20 names'". There isn't one:
   the 3-axis admissible share is **non-monotone in n** (u56 0.556 / 1.000 / 0.864 / 0.727 /
   1.000 / 0.958 at n = 3/5/10/20/40/all), and n\* is **40 on u56 but 136 on broad**.
3. Unconditionally — over all 32 arm-rows per rung rather than the priced ones — the 90% bar
   is **NOT REACHED AT ANY RUNG on either panel**, at all 12 (q, tau) grid points.
4. Idea 122's statistic is conditioned on a set that shrinks with n (published rows per rung
   u56 [18, 12, 22, 22, 24, 24]). TOP5 scores 1.000 on it while being the **least** stable
   rung on the ladder unconditionally (median draw-level positive fraction **0.363**).
5. Rule 8: n\*_IS is NOT REACHED on u56 while n\*_OOS = 5 there; on broad both are 136. A
   floor chosen in-sample is wrong in both directions.
6. The threshold that does matter is on the menu's **ordering**: mean spearman(IS rate, OOS
   rate) is +0.002 / −0.321 / +0.105 / −0.529 at n = 3/5/10/20 and +0.573 / +0.442 / +0.752 at
   n = 40/56/136, on 4–10 vs 11–13 priceable pairs.
7. **Proposed PROTOCOL clause (report-only, for Sunday review — NOT written by this run),
   exact wording:** *"Any published `pp CAGR per pp MaxDD` price must state the mean name
   count of the book it was measured on. Below 20 names its denominator's sign is not
   reproducible under name resampling; below 40 names the ORDER of the resulting menu does not
   survive out of sample. Both are caveats to quote, never screens to apply: the admissible
   share is non-monotone in book size and differs between panels."*
8. Nothing in RULES changes. The live book (RULES v2: every name inside the 200d ±3% band,
   equal weight, 75% gross, weekly) holds no quoted price and is unaffected.
9. By-product PARK, not promoted: u56 / TOP40 / band3-rw @10 bps, 11.36% / 1.2112 / −15.66%,
   OOS 1.2761 — a wash against live RULES v2 (8.66% / 1.2056 / −12.05%, OOS 1.2851) with a
   worse drawdown and an added ranking step, and not the arm idea 94's IS selector picks.
10. Gates: ladder nests idea 94's TOP20/EWall/V1u at 0.000e+00, `run()` == `engine.backtest`
    at 0.000e+00, idea 94's committed price list reproduces on 64 rows at <= 1.8e-15, and the
    live RULES v2 u56 row reads 8.66% / 1.2056 / −12.05% exactly.
