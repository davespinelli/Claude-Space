# Idea 525 — is `n_elig` the variable the record keeps mislabelling?

**Lane B, 2026-09-11. ANSWERED / NO — the premise is FALSIFIED. 1 of 5, and that one is not
an `n_elig` statistic either. No KEEP, no book promoted, no memo, no RULES change.**
`RULES.md`, `PROTOCOL.md`, `scan.py`, `bot.py`, `baseline.py` untouched.

## The question and why it could not be answered before

Idea 286 established the **k-identity**: `breadth == mean(n_elig) / k`. Its ladder held
`k = 40`, so on it breadth and `n_elig` were literally the same number (Spearman +0.99999).
It also noticed the two run **opposite** ways in the record — SMALL439 is the record's
*widest* panel (Ebar 141.5) and its *lowest*-breadth one (0.322), while U56 is its
*narrowest* (Ebar 36.1) at breadth 0.657. So the queue asked: when the record says a result
is explained by `breadth`, is it really `n_elig` wearing the wrong name?

## Design — the decoupling grid (2 tuned params, all 58 panels reported)

`q` (cap mix) × `k` (panel width), `q ∈ {0, .25, .50, .75, 1}` × `k ∈ {40, 60, 80, 100}`,
3 seeded draws (2 deduped as exact repeats at q=0/k=100, where BSTK100 is exhausted).
Books `NS_LAD = {5,10,15,20,30}` + EWall + ADAPT, 10 bps, weekly, t+1, 75% gross, seed 2026.

The grid works because **breadth is flat in k and steep in q, while `Ebar = breadth·k` is
steep in both**: within-q sd of breadth **0.0186** against an across-q sd of **0.1406**.
So the within-q slice moves `Ebar` with breadth held (identifies `n_elig`), and the
within-Ebar-bin slice moves breadth with `Ebar` held (identifies breadth). Neither slice
exists at fixed k. **Unconditional Spearman(breadth, Ebar) falls from +0.99999 on idea 286's
ladder to +0.5166 here**; breadth spans 2.61×, `Ebar` spans 6.30×.

The five statistics are idea 286's, **imported and never re-typed**: S1 ρ(n, OOS Sharpe)
[209/199], S2 INV-vs-NONE top-20 overlap [153], S3 Sharpe-vs-CAGR reversal [271/269C],
S4 argmax-n premium over EWall [155], S5 fixed n=20 − adaptive [157].

**Pre-registered bar** (fixed in the docstring before any statistic was read; idea 286's
own 0.30 / 8-of-11 rescaled to this grid): *n_elig* iff |mean within-q ρ(S, Ebar)| ≥ 0.30
in ≥ 4 of 5 q-levels; *breadth* iff |mean within-Ebar-bin ρ(S, breadth)| ≥ 0.30 in ≥ 4 of 5
bins; both → JOINT; neither → NULL.

## Gates

* **G0** — idea 286's committed `.stats.csv` named rows re-derived by its own code on its own
  ladder: **machine precision on 44 of 50 quantities**, and the **only** panel that moves is
  **U56**; all four panels drawn from `prices_broad`/`prices_small` are exact, S4 (a count) and
  S2 (a share) reproduce **exactly 5/5**. This is a *structural* gate, not a tolerance.
* **Reported, not absorbed:** U56's residual is **3.443e-03 in Sharpe units / 1.068e-03 of a
  name-count** — it **exceeds idea 515's proposed 1e-3 Sharpe bar**, two days after idea 286
  committed the rows. A second independent sighting of idea 516's drift, and evidence for
  ideas 520/522 that a flat 1e-3 bar cannot gate U56. It moves no verdict here.
* **G1** — the k-identity on this run's own construction: `max |k·breadth − Ebar| = 1.421e-14`
  over all 63 panels.
* **Truncation cost reported:** dropping n=40 (forced, since CAND-40 on a k=40 panel *is* the
  equal-weight book) moves S1 by ≤ 0.171 and S3 by ≤ 0.067 on the named panels; every
  ladder-vs-named comparison uses NS_LAD on both sides.

## The answer

| statistic | within-q ρ(S,Ebar) | within-Ebar ρ(S,breadth) | β_log breadth | β_log k | verdict |
|---|---|---|---|---|---|
| S1 ρ(n, OOS Sharpe) [209/199] | −0.167 (4/5) | **+0.539 (5/5)** | +0.725 | −0.036 | **breadth** |
| S2 INV-vs-NONE overlap [153] | **−0.966 (5/5)** | +0.349 (4/5) | −0.421 | **−0.919** | JOINT |
| S3 reversal share [271/269C] | −0.046 (3/5) | **+0.653 (5/5)** | +0.692 | −0.053 | **breadth** |
| S4 argmax-n premium [155] | +0.150 (2/4) | **+0.493 (5/5)** | +0.619 | +0.134 | **breadth** |
| S5 fixed − adaptive [157] | −0.145 (4/5) | +0.276 (4/5) | +0.287 | −0.135 | **NULL** |

**THE COUNT: 1 of 5.** `n_elig` only **0**, breadth only **3**, JOINT **1**, NULL **1**.

**And the one exception is not an `n_elig` statistic either.** Since
`log Ebar ≡ log breadth + log k` exactly, a genuine `Ebar` statistic must load **equally** on
both coordinates. S2 loads **−0.919 on log k against −0.421 on log breadth** (R² 0.945): it is
closer to a *raw panel-width* statistic than to an eligible-count one. Idea 153's overlap
ordering is a **k** claim. The asymmetry the queue did not anticipate: a statistic can clear
the `n_elig` slice and still not be a function of `n_elig`, because `n_elig` has two factors
and the within-q slice moves only one of them. The regression is what says which.

The regression is also what disambiguates slice 2: inside an `Ebar` bin breadth and k move
together (ρ **−0.776**), so a slice-2 loading alone cannot separate a breadth statistic from a
low-k one. **β_log k ≈ 0 beside a large β_log breadth** is what makes S1/S3/S4 breadth.

**So idea 286 was right and the queue's suspicion was wrong.** Three of the five published
claims are genuinely functions of the eligible **share**, i.e. of the cap mix, exactly as idea
286 restated them. The record is not systematically mislabelling `n_elig` as breadth.

## Rule 8 (PROTOCOL 8) — the same question, forward-looking

Properties measured on **2010–2016 only**; 2017-01-01.. read once.

| selector | OOS CAGR | OOS Sharpe | OOS MaxDD | > anchor | > RULES v2 | > SPY |
|---|---|---|---|---|---|---|
| EBAR-MAX | 13.56% | **0.8871** | −21.09% | 5/5 | **0/5** | 3/5 |
| BREADTH-MAX | 11.98% | **0.8824** | −20.67% | 5/5 | **0/5** | 3/5 |
| EBAR-MIN | 6.44% | 0.4945 | −25.10% | 1/5 | 0/5 | 0/5 |
| BREADTH-MIN | 6.44% | 0.4945 | −25.10% | 1/5 | 0/5 | 0/5 |
| IS-SHARPE-MAX | 10.07% | 0.7950 | −19.74% | 5/5 | 0/5 | 0/5 |

SPY OOS Sharpe **0.8820**; RULES v2 OOS Sharpe (mean over ladder panels) **0.8462**;
do-nothing anchor 0.5576 (n=5) → 0.6971 (n=30).

**The head-to-head settles it.** EBAR-MAX and BREADTH-MAX pick a different **panel** on 5 of
5 book sizes (they disagree about k: 100 vs 60) yet land in the same **cap stratum** on
**10 of 10** picks counting the MIN pair (every MAX pick q=0.00, every MIN pick q=1.00;
EBAR-MIN and BREADTH-MIN are the same panel 5/5). Disagreeing about k and agreeing about q
costs **0.0047 of OOS Sharpe**. Choosing the panel on `n_elig` and choosing it on breadth are,
out of sample, the same selector — both are the cap line under two names.

Unconditionally breadth is the **better** OOS predictor, against the queue's premise:
within book size ρ(breadth_IS, OOS Sharpe) **+0.806** vs ρ(Ebar_IS, OOS Sharpe) **+0.460**.
Within q both collapse — at n=20, **−0.081 (3/5)** and **−0.061 (2/5)**. Neither panel
property predicts OOS once the cap mix is held.

## KEEP paths (10 bps, every arm row)

**4a 0 / 348. 4b 21 / 348 (6.03%)**, every pass at **q ≤ 0.25** (highest q carrying any 4b
pass: 0.25), by arm CAND30 12 / CAND20 4 / CAND15 2 / CAND10 2 / EWall 1. Passers vs the rest:
Ebar 42.7 vs 33.5, breadth 0.6479 vs 0.4874 — **4b eligibility is again a monotone function of
the cap mix**, reproducing ideas 276/285/286 on a third construction. Named panels 4a 0/35,
4b 7/35 (U56 CAND15/20/30, B136 CAND40 + EWall, BSTK100 CAND30/40).

**No KEEP and no candidate.** No arm here is a new book: CAND-n and EWall are the record's
existing books re-run on re-drawn panels, so a pass is a statement about the panel, not a rule.

## Limits, stated

3 draws per cell is thin — the within-q slice rests on 12 points per level and the sign counts
should be read as such. `k ≤ 100` because BSTK100 has exactly 100 names, so the k arm spans
2.5× where the record itself spans 12.5× (35 → 439); the extrapolation to SMALL439's width is
**not** claimed. NS had to be truncated to keep max(n) < min(k), which moves S1/S3/S4 by the
amounts tabulated above. S4 is undefined within q=0.00 (constant there), so its within-q count
is 2 of 4, not 2 of 5. **SURVIVORSHIP** (idea 54): SMALL439 and BSTK100 are current
constituents, so every level is optimistic at the small-cap end — the bias runs against the
small/wide end and therefore *against* an `n_elig` reading, making this the conservative call.

## For the Sunday review — one reporting clause proposed, nothing taken

Publish **`k` and `mean(n_elig)` beside every breadth reading**, as the queue asked. It costs
nothing, and it is the only way a reader can tell which of the three coordinates a claim is
about — this run found the record's own five claims split 3 breadth / 1 k / 1 null, and none
of that is visible from the breadth column alone. Follow-ups filed as 684–686.

## Collision
**COLLISION:** idea 525 was claimed and run CONCURRENTLY by the cloud lane (pushed first) and this one (pushed second); neither saw the other and BOTH ARE KEPT, as with idea 286. They ask different questions under one title. The cloud lane HOLDS k and shows that at matched k `rho(Ebar, .) == rho(breadth, .)` at all nine (k, band) cells — a one-width breadth claim IS an n_elig claim, by rescaling — then splits across k (CAGR breadth, MaxDD n_elig, Sharpe both) and censuses 144 tight cross-panel claims, none separable, only 23 of 145 printing n_elig. This lane BREAKS the confound with a q x k ladder and asks which coordinate each of idea 286's five published statistics loads on. **They agree on the mechanical core** — at fixed k the two are the same variable (cloud's 9-of-9 identity is this run's GATE 1 stated the other way round), there is no single answer across statistics, and neither finds a KEEP. Their book families differ (cloud's 195 band books vs this run's 348 CAND/EWall arm rows), so **their 4a/4b counts are NOT comparable** and neither is offered as a check on the other. The one place they touch the same object is idea 153's U56 > B136 > SMALL439 ordering: cloud finds it survives matched k while disagreeing with the Ebar order at 2 of 3, and this run finds its statistic loads -0.919 on log k against -0.421 on log breadth — both readings say the ordering is not an eligible-share fact, arrived at independently.
