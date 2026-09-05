# Memo — idea 121, an ADV floor for the small panel (PROTOCOL clause, no RULES change)

1. **Finding.** The sub-$2B panel's narrow books are untradeable as published: at $10M of
   capital the ranked n=20 book trades **17.6%** of its p25 held name's daily dollar volume per
   rebalance, n=10 **46%**, n=5 **137%**. A $1M ADV floor is the smallest ladder value that
   brings n=20 under 10%; that criterion used ADV only, no return.
2. **Cost of the floor:** equal-weight-everything goes 10.18% -> 5.92% -> 1.64% -> -4.92% CAGR
   at none / $1M / $5M / $20M (Sharpe 0.678 / 0.413 / 0.181 / -0.163, reproducing idea 120's
   control). The panel's return lives in names it cannot buy.
3. **Verdicts it moves: 7 of 48.** All seven 4a passes the small panel has ever produced are at
   floor $0 and none survives $1M (4a by floor 7 / 0 / 0 / 0); six are the ungated/unscaled
   ranked family. **4b: 0 of 192 points at any floor**, so nothing capital-worthy is lost.
4. **What it does NOT overturn.** The gate's -5.4 pp/yr small-cap cost (ideas 49/51/39) keeps
   its sign in 12/12 cells and only attenuates 25% (-6.52 -> -4.87 pp at the proposed floor);
   the four-way gate ordering holds exactly at $1M. Idea 120's scaler premium stays the only
   published small-panel finding a floor reverses.
5. **Separate exposure found in passing:** the four-way gate spread is **0.080** here versus
   **0.356** as published, under gross-matched weights (idea 81). The ordering is stable, the
   magnitude is a weighting convention. That is a queue item, not a liquidity result.
6. **Do not change `load_universe`.** The floor is point-in-time and book-dependent; baking it
   into the loader would silently re-scope every historical row and hide the very comparison
   this run is for. It belongs in PROTOCOL as a reporting requirement plus a default.
7. **Exact PROTOCOL wording proposed to the Sunday review** (new clause 10; nothing else edited):

> **10. Small-panel liquidity (added Sep 5).** Any result computed on
> `baseline.load_universe(small=True)` must report, for the names its book actually HOLDS, the
> p25 and median 20-day median dollar volume, and the share of the p25 name's dollar volume the
> book trades in one rebalance at $10M of capital. A small-panel row may not be quoted as a 4a
> or 4b pass, or cited as a signed comparison against another book, unless that share is **<=
> 10%**; rows that fail it are reported as diagnostics only. The default screen when one is
> applied is a **$1M point-in-time 20-day median dollar-volume floor on the selectable set,
> applied before any ranking or gate**, with every result also reported at $0 so the effect of
> the screen is visible. The floor does not correct the panel's survivorship bias and is
> positively correlated with it (the missing delisted cohort is the thin cohort); that caveat
> must be restated wherever the floor is used.

8. **Retro-action if adopted:** mark the seven 4a rows above as failing clause 10, and annotate
   ideas 31/38/49/50/51/97/119's leaderboard rows with the floor-$0 caveat rather than deleting
   them — their signed comparisons mostly survive (point 4), their levels do not.
9. **No RULES change, no new candidate.** Rule-8 picks lose to SPY at every floor
   (OOS Sharpe 0.286 / 0.163 / -0.026 / -0.608 vs SPY 0.882) and get worse as the floor rises.
10. **Cost note for whoever writes clause 10:** flat 10 bps across floors flatters thin names.
    If the Sunday review wants the clause to bite harder, slope cost with ADV; that makes
    section 2's decay shallower and the gate's cost larger, and changes no verdict here.
