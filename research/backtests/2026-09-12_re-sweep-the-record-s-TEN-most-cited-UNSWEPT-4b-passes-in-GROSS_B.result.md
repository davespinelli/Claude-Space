# Idea 574 — re-sweep the record's most-cited UNSWEPT 4b passes in GROSS (lane B, 2026-09-12)

**Verdict: ANSWERED — PREMISE SPLIT. No KEEP, no new candidate, no RULES change.**
Every published point survives; what does not survive is the *reading* of it.

## What was run

The record's reconstructible **memo corpus** — every committed KEEP-candidate that has a memo and
can be rebuilt from prices alone (K1–K8, the list fixed and gate-verified by idea 641 on
2026-09-10) — plus the two mandated comparands (live RULES v2, retired RULES v1). Ten books ×
17 gross rungs (0.20 → 1.00, step 0.05) × 3 cost rungs = **510 rows, every one reported** in
`.cells.csv`. Two tuned parameters only: the **book** and the **gross**. 10 bps headline, t+1
fill, no shorting, no leverage. Panels U56 and B136, vintage pinned to 2026-09-04.

**Denominator note, published because the queue asked for ten:** the reconstructible memo corpus
is **eight** candidates, not ten; idea 641 reached "10 books" by counting the two comparands.
This run sweeps all eight and both comparands and does **not** invent two further books to hit
the number. PART A publishes citation counts so "most cited" is measured, not asserted.

**Gates: 4 of 4 PASS.** G1 RULES v2 U56 @10bps 8.66%/1.2056/−12.05% vs committed
8.63%/1.202/−12.05%. G2 **8 of 8** gated memo books reproduce their published headline
(|ΔSharpe| 0.0000–0.0177, bar 0.02). G3 the mesh carries every memo point (K7's 0.375 is
off-mesh and is priced at both). G4 derived cost rungs vs `engine.backtest(cost_bps=25)`
**0.000e+00**.

## PART A — the queue's two premises, measured

**Premise 1 (unswept) HOLDS: 6 of 8** candidates were published at one gross and never re-run at
a second inside their own memo. The two exceptions are **K5** (0.50/0.75/1.00) and **K8**, whose
q=0.20 sibling memo already ran exactly this 17-rung ladder and found a 7-rung band — an
independent precedent this run reproduces at 5 rungs for the q=0.17 variant.

**Premise 2 (most cited), ranked by mentions across committed `research/` text:** K6 25, K4 13,
K2 12, K1 12, K7 4, K3 2, K5 2, K8 2. (LIVE 5574 / V1 2546 dominate by construction.) The
record's *most-cited* candidate, K6, is also one of the *unswept* ones.

## PART C — the ladder

**Every one of the eight keeps its own published verdict at its own gross (8/8).** The seven
books published as 4b passes pass 4b there; K7, the corpus' only path-4a book, passes 4a there
and fails 4b on the CAGR floor — exactly as its memo says. Idea 311's "97.6% flip on their own
ladder" is **not** a claim that the published points are wrong; it is a claim about the *other*
rungs, and that part reproduces hard:

| book | memo g | 4b @ memo | 4b cells /17 | band | span | memo point | 4a cells /17 |
|---|---|---|---|---|---|---|---|
| K1 u56 top20 W | 0.750 | PASS | 4 | 4 | 0.65–0.80 | interior | 0 |
| K2 top20 + buffer m=20 W | 0.750 | PASS | 5 | 5 | 0.65–0.85 | interior | 0 |
| K3 top20-200d DAILY m=50 | 0.750 | PASS | 7 | 7 | 0.70–1.00 | interior | 0 |
| K4 EW-all MA gate MONTHLY | 1.000 | PASS | 3 | 3 | 0.90–1.00 | EDGE | 0 |
| K5 RULES v2 gate g1.00 W | 1.000 | PASS | 2 | 2 | 0.95–1.00 | EDGE | 0 |
| K6 wide-band b=0.12 W | 0.750 | PASS | 4 | 4 | 0.60–0.75 | EDGE | 6 |
| K7 b136 EW + SHY residual | 0.375 | FAIL (CAGR) — **4a PASS** | 2 | 2 | 0.75–0.80 | n/a | 5 |
| K8 EW-all breadth-degross | 1.000 | PASS | 5 | 5 | 0.80–1.00 | EDGE | 0 |
| LIVE RULES v2 g0.75 | 0.750 | FAIL (CAGR) | 2 | 2 | 0.95–1.00 | n/a | 0 |
| V1 RULES v1 | 0.750 | FAIL (H1+H2+OOS+CAGR) | 0 | 0 | none | n/a | 0 |

**Admissible band: median 4 of 17 rungs (24% of the ladder), min 2, max 7.** No candidate admits
everywhere and none admits nowhere. **The binding bar at every failing rung of every candidate is
the CAGR floor below the band and the DD cap above it** — never a Sharpe leg. 4 of the 7 4b
holders sit on their band's EDGE, but **3 of those 4 (K4, K5, K8) sit at g = 1.00, where the edge
is the no-leverage constraint, not a cliff**; only **K6's 0.75 is a genuine cliff** (the DD cap
bites at 0.80). Cost rungs: 4b **38 / 32 / 21** of 136 at 0/10/25 bps, 4a **12 / 11 / 8**.
**BOTH paths: 0 of 136** — the 4a/4b disjointness reproduces again, and it is structural here:
K6 and K7's 4a passes sit at low gross, precisely where 4b dies on the CAGR floor.

## The mechanism — and the actual finding

**Gross is not an information dial. For 7 of 8 candidates it moves Sharpe by less than 0.02
across the entire 0.20 → 1.00 ladder (median span 0.0012; K5 0.0002, K2 0.0005, K8 0.0007),
while rho(g, CAGR) = +1.0000 to four decimals in 8 of 8 and rho(g, MaxDD) ≈ −1.000.** Moving g
slides the book along a straight line in (CAGR, MaxDD) at constant Sharpe. The 4b band is
therefore just the segment of that line lying between the CAGR floor and the DD cap — **a
published 4b verdict quoted at one gross is a statement about where two bars happen to cross,
not evidence about the strategy.** That is the honest reconciliation of idea 311's finding.

The single exception is **K7** (span 0.3252), and it is the exception that proves the rule: its
"gross" trades equities against a **SHY** sleeve rather than against cash, so it is a genuine mix
dial — and it is the one book whose Sharpe the ladder actually rewards (1.0190 at g=1.00 rising
to 1.3442 at g=0.20).

## PART D — rule 8 walk-forward (g on 2009–2016 IS Sharpe alone; 2017–2026 read once)

OOS comparands @10bps: **RULES v2** U56 9.53% / 1.2851 / −12.05%, B136 7.98% / 1.1185 / −12.24%;
**SPY** 15.45% / 0.8820 / −33.72%.

The IS-Sharpe selector reproduces the memo's own gross in **3 of 8**. OOS the picks beat **SPY
8/8** on Sharpe and the **live RULES v2 baseline 3/8**; 4b holds OOS-inclusive for 5/8 picks.
Best OOS pick: K8 g=1.00, **16.14% / 1.4004 / −12.72%**; worst OOS Sharpe among picks: K1 1.1308.

On the **5 books where the selector actually moved the gross**, pick minus memo-g:

* OOS **Sharpe** median **+0.0001** (mean +0.0369, range −0.0005 … +0.1849 — and the +0.1849 is
  K7, the one real mix dial)
* OOS **CAGR** median **+0.97%** (range −5.18% … +5.20%)
* OOS **MaxDD** median **−1.15%** (range −5.88% … +5.56%; negative = deeper)

**An IS-Sharpe selector run over a flat dial is choosing a gross at random.** It reports an OOS
Sharpe that is unchanged to four decimals and hands the owner up to 5.9 pp more drawdown for it.
This is the same shape rule 8 keeps finding, now with a named cause.

## KEEP paths

4a 11/136, 4b 32/136, **BOTH 0/136** at 10 bps. Best 4b cell by full-sample Sharpe is **K6
g=0.75, 14.02% / 1.2264 / −19.42%** (halves 1.2610 / 1.2048, OOS 1.2662) — which is K6's own memo
point, reproduced. **No new KEEP-candidate is claimed and no memo is filed**: every 4b-passing
cell here is a gross re-pricing of a book the record has already memo'd. The deliverable is the
band, not a candidate.

## Proposal (NOT adopted here — RULES/PROTOCOL change only via Sunday review)

Add to PROTOCOL 4: *every published 4b or 4a pass must state (i) the admissible gross band on a
17-rung 0.20–1.00 ladder and (ii) max|ΔSharpe| over that band.* Where (ii) is below ~0.02 the
pass is an **exposure window** and must be reported as such; where the band's upper edge is
g = 1.00 the pass must say so, because that edge is the no-leverage constraint and not evidence.
Cost: one 17-point ladder per candidate — under a minute per book on this panel.

## Caveats

Current-constituent survivorship in both `universe.json` and `universe_broad.json`, so every
LEVEL here is optimistic; the object of this run is a within-book contrast in g, which that bias
does not move. `data/prices.csv` is re-downloaded daily, so U56 rows reproduce to ~3e-3 and not
bit-exact (idea 406). K3's and K8's memo files are their m=30 and q=0.20 siblings' — stated in
PART A rather than smoothed over.
