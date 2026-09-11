# Idea 524 — does any published panel-property claim have an INTERIOR cap mix?

**Lane B, 2026-09-11. ANSWERED / NO — 0 of 147, and the queue's literal bar is met only by
degenerate pairs. No KEEP (4a 0/450, 4b 7/450), so no memo and no RULES change.**
`RULES.md`, `PROTOCOL.md`, `scan.py`, `bot.py`, `baseline.py` untouched.
The run does, however, return a **priced recommendation**: a standing interior comparand
costs **0.73 s / 5 book cells / 1 draw** and buys a leg the endpoints provably cannot show.

## The question

Idea 286 found every *named* panel in the record sits at cap mix `q ∈ {0, 1}`. The queue
asked for a census of claims whose compared panels differ in `q` by **less than 1.0**, and —
if none exists — for the **price** of adding one interior panel (`q = 0.5`, `k` matched) as a
standing comparand.

## Gates

* **G1 — the premise re-derived, not quoted.** `q` of every named panel computed from the
  source lists: U56 **0.0000** (k 55), B136 **0.0000** (135), BSTK100 **0.0000** (100),
  ETF36 **0.0000** (35), SMALL439 **1.0000** (439). **0 of 5 interior. Premise holds.**
* **G0 — engine twin.** `fast_backtest` vs `engine.backtest` on a real interior panel
  (q=0.5, k=40, CAND-10): `|ΔSharpe| 0.000e+00`, `|ΔCAGR| 0.000e+00`. 8× faster.
* **Determinism:** all five committed CSVs are md5-identical across two full runs.

## Design (2 tuned params, PROTOCOL rule 4; every grid point reported)

`q ∈ {0, .25, .50, .75, 1}` × `k ∈ {40, 56, 100}` × **6 seeded draws = 90 panels**
(5 exact repeats at q=0/k=100, where BSTK100 is exhausted — kept and flagged `dup=1`).
Books CAND-5/10/20 + EWall + RULES v2 → **450 book cells**. 10 bps, weekly, t+1, 75 %
gross, seed 524. `k=40` is the record's own ladder width (ideas 276/285/525), **`k=56`
matches U56** — the "k matched" comparand the queue names — and `k=100` is the widest width
at which `q=0` is constructible at all.

## PART A — the census (589 committed `*.result.md`; claim regexes imported verbatim from idea 525 cloud leg C)

533 files name ≥ 2 panels and a panel-property word; **402 LOOSE** claims (verb anywhere),
**147 TIGHT** (verb within 200 chars of both a panel token and a property word).

| | TIGHT (147) | LOOSE (402) |
|---|---|---|
| Δq < 1.0 — **the queue's literal bar** | 29 (0.197) | 104 (0.259) |
| …of which **Δq == 0 exactly** (both panels in the SAME stratum) | **29 — all of them** | **104 — all of them** |
| Δq == 1.0 (endpoint to endpoint) | 118 | 298 |
| **claims with an INTERIOR compared panel (0 < q < 1)** | **0** | **0** |

**The literal bar passes 29 claims and every one of them is degenerate.** A Δq = 0 pair
(U56 vs B136, 24 of the 29) has *zero* cap variation, so it carries no more within-stratum
content than a Δq = 1 pair does — it is the *other* degenerate corner of the same axis. The
record's cross-panel property claims are therefore **118 endpoint-to-endpoint + 29
no-variation, 0 interior**. Most common compared set: `U56;B136;SMALL439` (83 of 147).
27 TIGHT files *construct* an interior-q panel somewhere in their text (the 276/285/525
ladders), but those interior points are **rungs of a sweep, not standing comparands**: no
panel any published claim compares against is interior.

## PART B — the price of one standing interior comparand

**B1 COMPUTE — cheap.** One panel = 5 book cells = **0.73 s** on the vectorised twin (≈5 s
on `engine.backtest`). MIX50 at all three widths: **2.20 s**. Retrofitting one interior
comparand to all 147 TIGHT claim files: **1.8 min** of twin compute (0.2 h on the engine).

**B2 INFORMATION — the interior panel is NOT on the chord.** Mean position on the
q=0 → q=1 chord is **0.3401** against 0.5 for a straight cap axis; below the midpoint in
**301 of 450** cells (0.669); mean |midpoint residual| **0.860 draw-sd = 0.300 of the
endpoint gap**. On the (k, book, stat) means (6 draws each), **24 of 75 triples reject the
straight-axis null at |t| > 2, and all 24 are BELOW the midpoint** — a 50/50 cap mix
behaves *more like the large-cap endpoint* than linear interpolation predicts.

| stat | mean chord pos | median t vs 0.5 | triples with t < −2 |
|---|---|---|---|
| **MaxDD** | **−0.0076** | **−3.4888** | **11 of 15** |
| Sharpe | 0.3947 | −1.0775 | 5 |
| CAGR | 0.4209 | −0.2502 | 4 |
| OOS Sharpe | 0.4104 | −1.0492 | 4 |
| Ebar | 0.4821 | −0.5118 | 0 |

**The DD leg is where it pays, and it is not curvature but non-monotonicity.** Tested
directly: the q=0.5 panel's MaxDD is **shallower than BOTH endpoints in 31 of 90 (k, book,
draw) cells (0.344)** — on **RULES v2, the live book, 0.833 at k=56 and 0.833 at k=100**.
A mixed panel diversifies the live rules' drawdown below either pure panel's, and **no
endpoint-only comparison can represent that at all** — it is not a point on the chord, it is
off the chord on the favourable side. Both KEEP paths use the DD leg.

Only **10 of 450** cells land outside the endpoint interval by more than one draw sd
(0.0222) — so the *interval* claim is nearly always safe; it is the *position inside it*,
and the DD leg's sign, that endpoint-only comparison gets wrong.

**B3 RESOLUTION — one panel is enough.** Interior single-draw sd against half the endpoint
gap: median **0.359–0.414** (Ebar 0.119). On **0 of 75 (k, book, stat) triples** does the
single-draw sd exceed half the endpoint gap; **median draws needed 1**, worst case 4. So the
queue's "a single interior panel" is the right unit — it resolves its own position at
half-gap resolution from one draw.

## PART C — PROTOCOL rule 8 (walk-forward) and both KEEP paths

`(q, k)` chosen on **IS 2010–2016 only** by argmax mean IS Sharpe; **OOS 2017–2026 read
once**. SPY on the sample: CAGR 14.13 %, Sharpe 0.8615 (H1 0.8907 / H2 0.8577),
MaxDD −33.72 %, OOS Sharpe 0.8820.

| book | pick (q,k) | CAGR | Sharpe | MaxDD | H1 / H2 | OOS CAGR | OOS Sharpe | OOS MaxDD | v2 same panel OOS Sharpe |
|---|---|---|---|---|---|---|---|---|---|
| EWall | **(0.0, 100)** | 15.19 % | 1.1538 | −26.49 % | 1.2717 / 1.0791 | 15.89 % | **1.1487** | −26.49 % | 1.1404 |
| CAND-20 | (0.0, 100) | 13.25 % | 0.9774 | −20.40 % | 1.1242 / 0.8525 | 13.20 % | 0.9407 | −20.40 % | 1.1404 |
| CAND-10 | (0.0, 100) | 13.59 % | 0.8732 | −22.43 % | 1.0757 / 0.7109 | 12.38 % | 0.7725 | −22.43 % | 1.1404 |
| CAND-5 | (0.0, 56) | 14.22 % | 0.8382 | −25.57 % | 1.0171 / 0.7011 | 13.12 % | 0.7502 | −25.57 % | 1.1340 |

**Interior q picked in 0 of 4 books** — rule 8 sends every book to the large-cap endpoint.
OOS Sharpe beats SPY in **2 of 4**, beats RULES v2 on the same panel in **1 of 4**.
**4a: 0 of 450. 4b: 7 of 450**, and — a fourth independent construction reproducing ideas
276/285/286 — **every 4b pass sits at q ≤ 0.25** (0.0694 at q=0, 0.0278 at q=0.25, **0.0000
at q = 0.50, 0.75, 1.00**). By width: 0.0417 at k=56, 0.0167 at k=40, 0.0000 at k=100.

## Verdict

**ANSWERED / NO.** No published panel-property claim has an interior cap mix (0 of 147
TIGHT, 0 of 402 LOOSE); the 29 that meet the queue's literal Δq < 1.0 bar all sit at Δq = 0
and carry no cap variation at all. **No KEEP** on either path — the interior of the cap axis
is where the 4b footprint *dies*, not where it lives.

**Recommendation, priced (for Sunday review — NOT a RULES change):** adopt **MIX50 at
k = 56, 1 draw, seed 524** as a standing comparand beside U56/B136/SMALL439. It costs
**0.73 s and 5 book cells per run**; it buys the only statistic in this run that the two
endpoints cannot bracket — the **DD leg, non-monotone in cap mix on 83 % of RULES v2 draws
at k ≥ 56**. It should **not** be used to argue a book's return: on CAGR, Sharpe and OOS
Sharpe the interior panel is inside the endpoint interval in 97.8 % of cells, and a claim
about those is adequately served by the endpoints the record already runs.

## Survivorship (PROTOCOL rule 9)

SMALL439 and B136 are **current constituents** of their screens, so every small-cap level is
optimistic by an unknown amount. The census is a property of the record's text and is
survivorship-free. The interpolation, DD-leg and resolution results are **contrasts between
panels drawn from the same screens**, not levels; survivorship moves the q=1 endpoint's
level and would, if anything, make the measured non-monotonicity of the DD leg *larger*, not
smaller.
