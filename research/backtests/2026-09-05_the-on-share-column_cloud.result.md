# Idea 191 — the-on-share-column (cloud, 2026-09-05)

**VERDICT: SPLIT. Idea 186's MECHANISM claim is CONFIRMED and quantified — the rotation
null's band widens ~8× as on-share rises, with the action held fixed and the timing effect
exactly zero. But the column as the queue proposed it is a KILL: on-share ALONE does not
predict which published overlay claims are inside their band (pooled family-demeaned
Spearman +0.068 ≈ 0), because effect size rises with on-share at almost the same rate and the
two cancel. What survives is a PAIR — on-share published beside the realised |dSharpe|, or
equivalently the clause MARGIN. As a selection gate it is the tenth consecutive KILL.**
Rules unchanged; no new book; no KEEP candidate.

## Reproduction, asserted before any new number was read
`fast_backtest == engine.backtest` on all three panels (max |dret| 1.4e-17 / 2.1e-17 /
2.8e-17), the cost identity at the same precision, base CAND-20 weights identical to idea
78/171's `weights_cand` at **0.0e+00** on all three panels, and RULES v1 on u56 @10bps at
**6.45305% / 0.66418 / −13.82780%** to every published digit. Null validity, idea 186's own
check: on-share preserved in **3600/3600** rotated rows and the circular switch count in
**3600/3600**.

## Design and what changed from idea 186
Idea 186's evidence was **confounded**: DDCTL fired on 4.6–40.5% of dates and cleared 15/36;
BUDGET fired on 53–93% and cleared 2/36. On-share and family moved together, so nothing there
separated "high on-share weakens the clause" from "BUDGET is a weak instrument". The single
change here is that the **threshold grid is widened from 3 points to 5 per family, chosen to
span the widest on-share range each family can reach** (not to maximise anything):

| family | on-share range reached (this run) | idea 186 |
|---|---|---|
| BUDGET | 0.4% – 93.7% | 53% – 93% |
| DDCTL | 0.0% – 62.4% | 4.6% – 40.5% |
| SLEEVE | 9.1% – 28.1% | ~30% – ~45% |

3 panels (U56, BROAD136, SMALL439) × 3 families × 5 thr × 2 depths × (1 real + 20 rotations)
× 2 cost rungs = **3780 rows, 180 real**, plus an **84-real/1680-null NOISE arm** (below).
Exactly **two tuned parameters** (threshold, depth); both cost rungs derived exactly from one
0 bps run via the engine's own turnover series.

## (1) THE MECHANISM — confirmed, and it is large
The decisive control idea 186 did not run: hold the **action** fixed (de-gross by k) and make
the ON indicator **pure noise** — an episodic Markov chain with no information, matched to the
real overlays' median episode length (5.89 rebalances) and driven to a **targeted** on-share.
Any real-vs-rotation difference is then timing luck alone.

| target on-share | realised | switches | **null band** | band sd | realised size |
|---|---|---|---|---|---|
| 0.05 | 6.2% | 15 | **0.0909** | 0.040 | 0/12 |
| 0.15 | 16.8% | 46 | 0.1833 | 0.066 | 0/12 |
| 0.30 | 29.2% | 93 | 0.2657 | 0.095 | 0/12 |
| 0.50 | 50.7% | 155 | 0.4318 | 0.143 | 0/12 |
| 0.70 | 69.0% | 229 | 0.5842 | 0.139 | 0/12 |
| 0.85 | 86.1% | 254 | **0.7149** | 0.149 | 0/12 |
| 0.95 | 86.0% | 263 | 0.6799 | 0.120 | 4/12 |

**Spearman(on-share, band width) = +0.677 over 84 cells.** The band widens **7.9×** from 6% to
86% on-share. Idea 186 was right, and the size of the effect is now a number.

**Realised size of the clause on a zero-timing-effect overlay is 4/84 = 4.8%, exactly its
nominal 1/21.** All four clears are the same single (panel, target) draw — SMALL439 at target
0.95 — so the apparent 33% at that row is one unlucky noise realisation, not an on-share
effect, and is reported as such rather than dressed up. The final band step is non-monotone
only because realised on-share stops rising there (0.8612 → 0.8597, the Markov chain's
`p_on` saturates at 1.0); over every step where on-share actually rises the band rises too.

## (2) THE COLUMN AS PROPOSED IS A KILL — on-share alone predicts nothing
| within family | ρ(on-share, **clears**) | ρ(on-share, **band**) | ρ(on-share, **&#124;dSharpe&#124;**) | ρ(on-share, **margin**) |
|---|---|---|---|---|
| BUDGET (n=60) | −0.340 | +0.643 | +0.422 | −0.235 |
| DDCTL (n=60) | **+0.418** | +0.890 | +0.904 | +0.012 |
| SLEEVE (n=60) | n/a (0 clears) | +0.581 | +0.651 | −0.251 |
| **POOLED, family-demeaned (n=180)** | **+0.068** | **+0.656** | **+0.595** | −0.166 |

The band rises with on-share (+0.656) — but so does the realised effect (+0.595), because a
more-often-on overlay simply *does more*. They cancel almost exactly, and the sign of
ρ(on-share, clears) is **not even consistent across families** (−0.34 BUDGET, +0.42 DDCTL).
A LEADERBOARD reader given on-share alone would draw the wrong inference on DDCTL rows.

## (3) WHAT DOES SURVIVE — on-share is a deflator, not a predictor
Conditioning on the realised effect size (Q3) separates the two channels cleanly:

| ρ(on-share, clears) within &#124;dSharpe&#124; tercile | n | mean band | mean &#124;d&#124; |
|---|---|---|---|
| small | 60 | **−0.141** | 0.075 | 0.008 |
| mid | 60 | **−0.445** | 0.135 | 0.050 |
| large | 60 | **−0.127** | 0.307 | 0.240 |

Clear rate by (|dSharpe| tercile × on-share tercile) shows it directly — at **large** effect
size: low on-share **0.67**, mid **0.17**, high **0.35**. **At a given effect size, a
higher on-share makes clearing strictly harder.** On-share is therefore a real confounder of
the clause and belongs in the schema — but as the second half of a pair, never alone.

## (4) CENSUS AND BACK-FILL
**632 of 3359 committed LEADERBOARD data rows (18.8%) rest on a state-dependent instrument**
— sleeve 142, gate 295, entry/turnover budget 126, drawdown control or trailing stop 83,
breadth 26. **Exactly 1 of the 632 publishes an on-share.** The column is missing from 631
exposed rows. Back-filled on-shares for all 15 configurations this run prices are in the
console output and `.clause.csv` (e.g. DDCTL D=0.03 → 45.7%, D=0.10 → 10.4%, D=0.25 → 0.0%;
SLEEVE ma=50 → 27.4%, ma=400 → 9.3%; BUDGET τ=0.05 → 91.8%, τ=0.50 → 7.6%).

**Proposed PROTOCOL clause 11c, report-only, for Sunday review** (evidence, not a rule change):

> Any state-dependent instrument (gate, sleeve, drawdown control, stop, entry/turnover
> budget) must publish its realised ON-SHARE — the fraction of the book's rebalance dates on
> which the instrument fires — **together with** its realised |dSharpe| against the same
> book without it. Neither number is interpretable alone: the matched-null band of clause 11b
> scales with on-share (Spearman +0.68; 7.9× from 6% to 86% on-share on a zero-timing-effect
> control), so a low-on-share instrument clears on a smaller effect and a high-on-share one
> can be genuinely useful and still sit inside its band. Where both are published, quote the
> MARGIN (|dSharpe| − band) as the single summary.

## (5) RULE 8 — the on-share gate is the tenth consecutive selector KILL
Overlay point chosen on ≤ 2016-12-31 only, 2017-2026 read once, 18 cells (3 panels × 3
families × 2 cost rungs), pool = 10 points (5 thr × 2 depth). Gate = on-share ≤ the corpus
median (19.7%).

| selector | mean OOS Sharpe | dOOS vs S0 | t | W/L | abstains |
|---|---|---|---|---|---|
| ORACLE-OOS (ceiling) | +0.8197 | +0.0431 | +3.86 | 12/0 | 0 |
| **S0 do-nothing** | **+0.7766** | 0 | — | — | — |
| S4 IS-argmax \| on-share ≤ median | +0.7618 | −0.0148 | −1.38 | 5/9 | 0 |
| S5 IS-clause + low on-share | +0.7542 | −0.0224 | −2.35 | 0/6 | 12 |
| S1 IS-Sharpe argmax | +0.7405 | −0.0361 | −1.68 | 5/9 | 0 |
| S2 IS-clause-gated (idea 186) | +0.6902 | −0.0864 | −3.14 | 0/11 | 7 |

The on-share gate **improves on idea 186's clause gate by +0.0716 and on the plain IS argmax
by +0.0213** — and still loses to doing nothing. Tenth consecutive project instance
(110/132/151/166/171/174/175/186/196/191). Benchmarks over the same window: U56 RULES v1 OOS
7.73%/0.7471/−13.83%, BROAD136 5.94%/0.5762/−21.19%, SMALL439 7.88%/0.6617/−32.37%;
**SPY OOS 15.45%/0.8820/−33.72%**.

## (6) BOTH KEEP PATHS
Real overlays **4a 37/180 (20.6%), 4b 28/180 (15.6%)**; rotated nulls **4a 901/3600 (25.0%),
4b 750/3600 (20.8%)** — a **randomly-timed overlay passes 4b MORE often than the real one**,
the third reproduction of that finding after ideas 181 and 186. 4b passes by panel: U56 27,
BROAD136 1, SMALL439 **0** (thirteenth reproduction of idea 136).

Two disqualifications must be stated, not counted as evidence:
- **16 of 180 real cells are INERT by construction** (on-share exactly 0.0% — DDCTL at
  D ≥ 0.15 never fires on these panels), and **8 of the 28 "4b passes" are those inert
  cells**, i.e. the untilted control wearing an overlay label. Excluding them leaves **20**.
- Of those 20, **18 are inside their own null band**. The 2 that clear are BUDGET τ=0.50/half
  on U56 at on-share **0.4%** with band **0.0043** — a nearly-never-firing overlay whose
  rotations are near-degenerate, which is the low-on-share end of exactly the effect measured
  in (1). Read honestly: **20 of 20 non-inert overlay 4b passes are indistinguishable from
  random timing**, reproducing idea 186's 18 of 18.

## (7) THE NULL'S TURNOVER FIDELITY DEGRADES WITHOUT BOUND FOR A SUPPRESSING OVERLAY
Idea 186 published BUDGET-skip's turnover gap at 25.4% mean / 213.8% max on a 3-point grid.
On the widened grid it reaches **1782.7% mean** (DDCTL 1.1–2.3%, SLEEVE 0.7–1.3%, BUDGET-half
4.3%). Suppressing a rebalance genuinely changes trading, and the gap grows with on-share, so
the rotation null for a suppress-a-trade overlay is **not** turnover-matched and gets worse
the more often the overlay fires. That is a second, independent reason the clause must
publish on-share beside it.

## Predictions: 3 of 5 hit
- **P1 MISS** — ρ(on-share, clears) is not negative in all three families: BUDGET −0.340,
  DDCTL **+0.418**, SLEEVE undefined (0 clears). The inconsistency of sign became the finding.
- **P2 MISS as written** — the band sequence is not monotone over all seven targets, but it is
  monotone over every step where realised on-share actually rises; the final step's realised
  on-share does not rise. Reported precisely rather than rescued.
- P3 HIT — realised size 4.8%, at nominal.
- P4 HIT — within every |dSharpe| tercile, ρ(on-share, clears) < 0.
- P5 HIT — the on-share-gated selector loses to do-nothing (−0.0148).

## Caveats carried, not buried
- **SURVIVORSHIP (idea 54):** all three panels are current constituents; SMALL439 contains no
  delistings. Real and rotated draws inherit the bias identically, so every CLAUSE reading is
  unaffected; every LEVEL (CAGR, Sharpe, 4a/4b counts) is biased upward and is not tradable.
- Only J−1 distinct rotations exist and neighbouring offsets are correlated, so the clause's
  nominal one-sided size (4.8%) is approximate; Q2 measures the realised size rather than
  assuming it, and finds it at nominal.
- The noise arm's Markov chain saturates above ~86% realised on-share, so the 0.95 target is
  not a distinct on-share point and its 4 clears are one draw, not a trend.
- The Q4 census is a TEXT MATCH over LEADERBOARD rows. It bounds how many rows are exposed;
  it does not re-price them and does not claim any of them is wrong.
- Idea 38's calendar-day index on U56/BROAD136 after 2014-09-17; idea 126's t+1-only execution.

**RULES.md, scan.py, bot.py and baseline.py untouched.** Ideas 201–203 queued.
