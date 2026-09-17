# Idea 1164 (lane B, 2026-09-17) — what sets PHI once the episode length is only a lower bound on L*

**ANSWERED: phi is set by the EPISODE LENGTH AGAINST THE BLOCK LENGTH and by the NUMBER OF
NEAR-TIED EPISODES — but neither fact is visible in a correlation across observed books, and
the queue's third candidate (recovery speed) is dead.** 18 of 18 gates PASS, 1 of 7
pre-registered hypotheses SUPPORTED. Nothing enacted.

## What was run

Dials (2, PROTOCOL rule 4): `DRIVER` {D_COVER, D_TIES, D_RECOV, D_EPISODE} x `CONTROL`
{X_NONE, X_PANEL, X_GAP, X_ORDER} = 16 cells, all published in `.dialgrid.csv`. Population:
3 panels x N{5,10,20,40} x HOLD{63,126,252} x CADENCE{W,M} = 72 books at frozen gross 0.75,
1,000 draws, block L=63, 3 seeds. 1162's 15 anchor cells replayed bit for bit (G8/G9/G10).

## The answer, in the order the evidence arrives

1. **ON CONTROLLED TAPES THE MECHANISM IS UNAMBIGUOUS.** On a trending tape whose only
   feature is ONE injected drawdown of a known length E, phi falls monotonically from
   **1.000 (E=5 and E=10) through 0.678 at E=63=L to 0.137 at E=1008**, spearman(E, phi)
   **-0.9879**. On a second tape holding the drawdown FIXED at -20% and varying only the
   number of equally deep 63-bar episodes, phi rises from **0.654 at K=1 to 1.601 at K=8**,
   spearman **+1.0000** — the pre-registered sign for D_TIES, and phi EXCEEDS 1 once K >= 6
   because the block null can chain near-tied episodes into one deeper than the observed
   maximum. Coverage and near-ties are both real, and they push phi in opposite directions.

2. **ON OBSERVED BOOKS NONE OF THE THREE CANDIDATES CLEARS ITS BAR.** X_NONE over the 56
   estimable books: D_TIES **-0.533** (perm p 0.0005), D_COVER **+0.336** (p 0.0090),
   D_EPISODE **-0.324** (p 0.0135), D_RECOV **+0.086** (p 0.534). D_TIES is the largest and
   is sign-stable across panels (-0.472 / -0.501 / -0.831) and under X_GAP (-0.513) — and
   its sign is the **OPPOSITE of the controlled experiment's**. The population reading is
   therefore CONFOUNDED, not a mechanism: books with more near-ties are books with different
   episode lengths, and the two drivers fight.

3. **THE QUEUE'S CANDIDATE 3 IS DEAD.** D_RECOV reads +0.086 at the frozen 5% threshold
   (p 0.53), -0.359 at 2% and +0.131 at 10% — a driver whose SIGN is set by its own
   threshold is noise. Published in `.sensitivity.csv`, never selected on.

4. **D_EPISODE's POPULATION RELATION IS BOOTSTRAP MACHINERY, NOT A TAPE FACT.** It is the
   one driver that SURVIVES order destruction almost intact: X_NONE -0.324 -> X_ORDER
   **-0.309**. That is consistent with the synthetic arms, which need no serial structure at
   all: phi is arithmetic — a block of length L meeting an episode of length E. D_TIES by
   contrast REVERSES under X_ORDER (-0.533 -> +0.325), so the population's strongest reading
   is the one with the least claim to being about the tape.

5. **THIS RUN'S OWN FRAMING PREMISE IS REFUTED.** It opened by arguing 1162 refuted the
   episode story on the WRONG FUNCTIONAL (a threshold crossing L* rather than the level
   phi). The data says the functional was never the problem: **spearman(L*, phi) = -0.903**
   over the 56 estimable books — the crossing and the level are two rank-equivalent readings
   of one quantity. Both give the same weak answer on observed tapes for the same reason.

6. **1162's ONE SURVIVING CLAIM WEAKENS ON A WIDER POPULATION.** "L* >= episode length at 12
   of 12" reads **54 of 72 (0.750)**, or 47 of 56 estimable (0.839), here. It is a tendency,
   not a bound, and should be quoted that way.

## Three corrections this run made to itself (all recorded, none patched away)

- **phi is not always estimable.** Its denominator (OBSERVED - N_IID) passes through zero,
  and the first cut read phi from -31.55 to +13.17. A cell counts only when |denominator|
  >= max(3 x the larger cross-seed spread, 0.25 pp): **56 of 72**. Every book is published
  with its denominator, its resolution and its verdict, and **every dial-grid cell carries
  `rho_all` over all 72 beside the headline `rho`** — the rule moves no sign anywhere.
- **The first synthetic tape was mis-specified** (zero drift, so its own natural drawdowns
  of 40-60% dominated the injected one at 10 of 10 rungs). Published as SYN_ADD with
  found=False at every rung; gate G15 pins it dead.
- **The first near-ties tape was mis-specified too** (-35% episodes 500 bars apart cannot
  recover at 0.08%/day, so all K merged into ONE and the arm priced depth, not ties —
  measured tie count 1 at 6 of 6 rungs). Re-cut at -20% and 520 bars; gate G16 pins the
  measured tie count == K at every rung, G17 pins the observed drawdown fixed at 0.37 pp.

## Rule 8 and both KEEP paths — NO KEEP CANDIDATE

117 books (the 72-book population at gross 0.75 + the anchor book's 15-rung gross ladder on
each panel), all published. **4a: 0 of 117 books and 0 of 27 picks.** 4b full 12, 4b full+OOS
11. **No IS-only chooser reaches a 4b book: 0 of 27 picks.** Ten of the eleven 4b passers are
the U56/B136 anchor book's own gross rungs — idea 1162's de-grossing, already memoed there,
so **no new memo is written and 1162's exact RULES wording stands**. The one new object,
U56 N20/H252/M (full 14.68% / 1.0609 / -18.92%, OOS 15.57% / 1.0550 / -18.92%), is dominated
by the incumbent on Sharpe (1.061 vs 1.138), sits at H2 0.998 against SPY's 0.817, and is
unreachable by every chooser — **PARK at best, not KEEP**.

## Caveats

SURVIVORSHIP bites harder here than usual: every object under study IS a drawdown, and a
current-constituent panel's deepest episode is both shallower and shorter than the true one,
which compresses the very axis the headline is measured along. It cancels out of the rank
correlations (one construction against itself on one tape) and does NOT cancel out of the
4a/4b legs. The synthetic arms are free of it and carry the mechanism claim. Nothing in
RULES.md, PROTOCOL.md, scan.py, bot.py or baseline.py was touched.
