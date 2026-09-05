# Memo to the Sunday review — idea 78, proposed PROTOCOL reporting clause (no RULES change)

1. Idea 78 is **not a KEEP**: no new book, nothing upgraded, the only full-panel 4b passer is idea 10's
   pre-existing `B136/EWall`. This memo proposes one reporting clause and nothing else.
2. The finding: a panel's ranking payoff is governed by **q = n / n_elig**, the quantile the book takes, not
   by the candidate count and not by dispersion (Spearman(q, spread) **-0.975** over 9 cells; at matched q the
   spread is flat while the count varies 4×, ranges +0.0012…+0.0073 against cell SEs of 0.012–0.044).
3. Consequence for every cross-panel comparison the project has published: comparing `CAND-n` at a fixed n
   across panels of different size is comparing **different quantiles**, so the "bigger panel is better"
   readings (idea 73's +0.964 among them) measure selectivity, not the panel.
4. **Proposed PROTOCOL rule 4 addendum, exact wording:**
   *"Any comparison of a ranked book ACROSS panels must be quoted at matched selectivity q = n / n_elig, not
   at matched n. A claim that a panel property (count, dispersion, breadth) pays must survive that matching."*
5. **Proposed PROTOCOL rule 5 addendum, exact wording:**
   *"A leaderboard row for a ranked book states the mean eligible count of its panel beside n, so that q is
   readable from the row."*
6. Neither clause changes a live weight, a gate, or a book. RULES.md, scan.py, bot.py and baseline.py are
   untouched by this run.
7. Supporting evidence for 4: idea 73's two Spearman triples reproduce EXACTLY from scratch here
   (+0.5714/+0.8571/+0.9643 and +0.4286/+0.6786/+0.3571), so the clause is being proposed against a
   reproduced number, not a re-derived one.
8. Supporting evidence for the dispersion half: at exactly matched count, dispersion's pooled standardised
   beta is +24 / -31 / +2 bp/yr with |t| ≤ 1.98 against log-count's +146…+210 bp/yr at t +7.8…+23.2.
9. Cost caveat worth minuting: the gross selectivity payoff **reverses after 10 bps** — Spearman(k, net
   Sharpe premium) = -0.358 (n=5) / -0.601 (n=20). A deeper quantile buys gross spread and sells net Sharpe.
10. Survivorship: `universe_broad.json` is current constituents; the count selector is the one survivorship
    flatters most, and it still fails rule 8 (Spearman(IS n_elig, OOS Sharpe) = **-0.262**).
