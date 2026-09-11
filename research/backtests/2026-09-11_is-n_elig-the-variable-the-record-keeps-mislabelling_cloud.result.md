# Idea 525 (cloud) — is n_elig the variable the record keeps mislabelling?

**Verdict: ANSWERED / SPLIT — YES at matched width, NO across it, and NOT for the panel ordering
itself.** At matched k, `breadth = Ebar/k` is a *linear rescaling* of n_elig, so **9 of 9 matched
cells give the two variables an identical rank-correlation with every outcome — a "breadth" claim
and an "n_elig" claim are the same statement there.** They separate only ACROSS k, and there the
answer splits by statistic: CAGR is a breadth statistic, MaxDD is an n_elig statistic, Sharpe is
both. **The panel ordering is neither**: U56 > B136 > SMALL439 on Sharpe survives at all three
matched widths while disagreeing with the Ebar ordering at 2 of 3. No KEEP, no book promoted, no
rule change. `RULES.md`, `PROTOCOL.md`, `scan.py`, `bot.py`, `baseline.py` untouched.

Script: `2026-09-11_is-n_elig-the-variable-the-record-keeps-mislabelling_cloud.py`
Artefacts: `.books.csv` (195 books), `.cells.csv` (27 cells), `.grid.csv`, `.within.csv`,
`.panelorder.csv`, `.strata.csv`, `.walkforward.csv`, `.census.csv` (530 files), `.console.txt`.

## Parameters (two, as the queue allows; every grid point reported)

* **P1 k**, the matched panel width, 3 levels **{20, 36, 55}**: 55 is U56's own tradable width (the
  record's narrowest named panel), 36 is idea 286's published U56 `Ebar`, 20 is the record's
  standard book size.
* **P2 band**, the eligibility dial, 3 levels **{0.00, 0.03, 0.08}** of the live 200d ±band gate.
  It moves `Ebar` at FIXED k — the contrast the record never runs.

Draws are fixed at 8 per (panel, k), seeded; gross fixed at the live 0.75; 10 bps, weekly, t+1.
Nothing tuned on an outcome. 195 books (U56 at k=55 is the whole panel, so 1 draw not 8).

## Reproduction gates (recorded, non-raising) — idea 286's own definitions, re-implemented

All PASS. 200d MA ∧ 20d ann. vol < 0.60, counted on weekly rebalance days, first 40 dropped:
**Ebar U56 36.14** (published 36.1), **SMALL439 141.53** (141.5), **breadth 0.6571 / 0.6619 /
0.3224** (published 0.6571 / 0.6619 / 0.3224 — exact to 4 dp), **k 55 / 135 / 439**, and **44**
names dropped from the 483-name small panel by `max_1d_move ≥ 1.0`.

**The identity restated on today's panels:** the record's SMALL panel is its **widest in n_elig**
(141.5) and its **narrowest in breadth** (0.3224); U56 is the exact reverse (36.1, 0.6571).

## [A] The answer, with n_elig and k published beside the property

**Inside every matched (k, band) cell** — k held, so only Ebar can move:

| k | band | n | ρ(Ebar, Sharpe) | ρ(breadth, Sharpe) | Ebar range | Sharpe range |
|---|---|---|---|---|---|---|
| 20 | 0.00 | 24 | +0.5870 | **+0.5870** | 5.29–14.01 | 0.273–1.238 |
| 20 | 0.03 | 24 | +0.6009 | **+0.6009** | 5.29–14.01 | 0.317–1.297 |
| 20 | 0.08 | 24 | +0.6026 | **+0.6026** | 5.29–14.01 | 0.407–1.340 |
| 36 | 0.00 | 24 | +0.4643 | **+0.4643** | 10.45–24.79 | 0.232–1.244 |
| 36 | 0.03 | 24 | +0.4417 | **+0.4417** | 10.45–24.79 | 0.300–1.273 |
| 36 | 0.08 | 24 | +0.5383 | **+0.5383** | 10.45–24.79 | 0.323–1.209 |
| 55 | 0.00 | 17 | +0.7941 | **+0.7941** | 16.71–37.38 | 0.190–1.196 |
| 55 | 0.03 | 17 | +0.7770 | **+0.7770** | 16.71–37.38 | 0.222–1.207 |
| 55 | 0.08 | 17 | +0.8088 | **+0.8088** | 16.71–37.38 | 0.325–1.207 |

**This is the queue's answer in its cleanest form.** The equality is not an empirical coincidence —
at fixed k, `breadth = Ebar/k` is Ebar times a constant, and Spearman is invariant to that. So
**any published claim that compares panels at one width and attributes the result to "breadth" is
an n_elig claim with a different name on it.** The two are only distinguishable across k.

**Pooled across k**, where they do separate (195 books):

| statistic | ρ(breadth,·) | ρ(Ebar,·) | partial (breadth \| Ebar) | partial (Ebar \| breadth) | reads as |
|---|---|---|---|---|---|
| CAGR | +0.6748 | +0.4460 | **+0.5774** | +0.1401 | a **breadth** statistic |
| MaxDD | +0.5195 | +0.5855 | +0.3035 | **+0.4276** | an **n_elig** statistic |
| Sharpe | +0.6137 | +0.5463 | +0.4560 | +0.3293 | **both**, breadth ahead |
| OOS Sharpe | +0.5754 | +0.5699 | +0.3917 | +0.3813 | **both**, a dead heat |

So "how many are n_elig statistics" has no single count: **the drawdown leg is, the return leg is
not, and the risk-adjusted legs are both.** A record that labels all four "breadth" is wrong about
one of them and unfalsifiable about two.

**The panel ordering is a third thing again.** Mean Sharpe by panel at each matched k:

| k | U56 | B136 | SMALL439 | Sharpe order | Ebar order | agree? |
|---|---|---|---|---|---|---|
| 20 | 1.1015 (Ebar 13.07) | 1.0217 (13.41) | 0.4975 (6.77) | U56 > B136 > SMALL439 | B136 > U56 > SMALL439 | **no** |
| 36 | 1.1569 (23.16) | 1.0845 (23.78) | 0.5296 (11.28) | U56 > B136 > SMALL439 | B136 > U56 > SMALL439 | **no** |
| 55 | 1.1771 (36.14) | 1.0793 (35.99) | 0.5069 (17.78) | U56 > B136 > SMALL439 | U56 > B136 > SMALL439 | yes |

The ordering **survives matching at every width** and **contradicts the Ebar ordering at two of
three**. Within Ebar terciles it survives too: in the Ebar-lo stratum (Ebar ≈ 9–13) U56 **1.1493**
> B136 **0.9002** > SMALL439 **0.5135**. **Whatever separates the record's panels, it is not
n_elig** — a negative that idea 153's reversal does not licence anyone to forget.

KEEP paths over all 195 books: **4a 6, 4b 1**. This is not a KEEP candidate.

## [B] Rule 8 — band chosen on 2009-2016 only, 2017-2026 read once

Band **0.08** is the IS pick at all 9 (panel, k). OOS against SPY (0.8721 U56 sample / 0.8820 on
the B136/SMALL439 samples) and RULES v2 (Sharpe 1.1998 / 1.2056 / 1.1672 on the three samples):

| panel | k | OOS CAGR | OOS Sharpe | OOS MaxDD | Ebar | beats SPY OOS | 4a | 4b |
|---|---|---|---|---|---|---|---|---|
| U56 | 20 | 9.09% | 1.0907 | −15.03% | 13.07 | yes | 1 | 0 |
| U56 | 36 | 9.25% | 1.1684 | −14.25% | 23.16 | yes | 0 | 0 |
| U56 | 55 | 9.04% | **1.1749** | −14.35% | 36.14 | yes | 0 | 0 |
| B136 | 20 | 8.22% | 1.0103 | −15.56% | 13.41 | yes | 0 | **1** |
| B136 | 36 | 8.43% | 1.0881 | −14.19% | 23.78 | yes | 0 | 0 |
| B136 | 55 | 8.47% | 1.1343 | −13.92% | 35.99 | yes | 0 | 0 |
| SMALL439 | 20 | 4.04% | 0.4702 | −21.05% | 6.77 | no | 0 | 0 |
| SMALL439 | 36 | 5.46% | 0.6444 | −17.96% | 11.28 | no | 0 | 0 |
| SMALL439 | 55 | 4.52% | 0.5782 | −17.30% | 17.78 | no | 0 | 0 |

**OOS Sharpe beats SPY in 6 of 9 picks — every U56 and B136 pick, no SMALL439 pick.** Every pick
loses OOS CAGR to SPY (15.24% / 14.13%), which is why 4b passes once in 65 picked books. Over the
9 picks **Spearman(Ebar, OOS Sharpe) +0.7667 > Spearman(breadth, ·) +0.4667 > Spearman(k, ·)
+0.3689** — at the level a rule-8 pick is actually made, **n_elig is the better-ordered variable of
the three**, which is the one place this run supports the queue's suspicion outright.

## [C] The census the queue asked for

586 committed `*.result.md`; **530** name ≥ 2 of the record's panels together with a panel-property
word. Of those, **399 carry an "explains / orders / drives" verb anywhere (LOOSE — this counts the
WORD, so it is an UPPER bound, exactly idea 286/523's own critique)** and **145 carry it within 200
characters of both a panel token and a property word (TIGHT)**. Both are published; neither is a
tuned dial.

| | LOOSE (399) | TIGHT (145) |
|---|---|---|
| publish n_elig / Ebar | **34 (8.5%)** | **23 (15.9%)** |
| publish k / width | 194 | 72 |
| publish **neither** | 187 | 62 |

**Separability.** This run's own within-(panel, k) draw spread in Ebar gives a yardstick of
**2.03 eligible names** (2 sd, largest cell). **144 of 144** tight claim files whose compared panels
this run measures compare panels whose Ebar differs by **more** than that — median gap **105.4
eligible names**, fifty times the noise. **Zero published cross-panel property claims in the record
are separable from an n_elig difference**, and 84% of the tight set never print n_elig at all.

## What should change (Sunday review; nothing taken here)

1. A cross-panel property claim must print **(k, Ebar)** beside the property. At one width the two
   readings are the same statement; a reader cannot tell which was meant without both numbers.
2. `breadth` and `n_elig` should not be used interchangeably **across** widths: CAGR follows
   breadth, MaxDD follows n_elig, and the two disagree by a factor of 4 in partial rank.
3. The panel ordering itself should stop being explained by either — it survives matched k and
   matched Ebar, so the explanation is still missing.

## Caveats

The census counts words in a proximity window, not parsed claims: 399 is an upper bound and 145 a
tighter one, neither is the number of distinct claims. `Ebar` is idea 286's definition (200d MA ∧
vol < 0.60 on weekly rebalance days); a different eligibility rule gives different levels, though
the matched-k identity holds for any rule. Draw counts are unbalanced across Ebar strata (B136 has
3 books in Ebar-lo, U56 none in Ebar-hi), so the within-stratum panel gaps are indicative, not
estimated. The three panels do not share a sample (SMALL439 starts 2011-01-13 after warm-up), so
cross-panel *levels* are not strictly comparable — the within-k contrasts are.
**SURVIVORSHIP (idea 54): all three panels are current constituents only; the sub-$2B panel is the
survivors of a screen run today, so its levels are optimistic — its being LAST on every statistic
here is if anything understated.**
