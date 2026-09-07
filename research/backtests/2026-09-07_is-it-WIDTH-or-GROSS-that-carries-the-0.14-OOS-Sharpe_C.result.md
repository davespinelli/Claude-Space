# Idea 355 — is-it-WIDTH-or-CADENCE-that-carries-the-0.14-OOS-Sharpe (lane C, 2026-09-07)

**Verdict: SPLIT — the decomposition is ANSWERED and clean; the width dial it isolates is KILLED as a general instrument. No new KEEP (4a 0/36, and the rule-8 pick fails 4b on both panels).**

Note on the title: the queue *title* says WIDTH-or-CADENCE, but the queue *body* pins cadence at
MONTHLY and names the two dials as **n and gross**. The body is the operative spec, so the tuned
parameters are exactly two — n and g — and cadence is carried only as a pre-registered robustness
check (Part E), never as a third dial.

## The answer to the question asked

The +0.1409 of OOS Sharpe between idea 352's PARK by-product **D = (n=40, g=0.75)** and the
pre-registered chooser's pick **A = (n=20, g=1.00)** on U56, monthly, 10 bps, splits as:

| panel | total D−A | n main effect | gross main effect | interaction |
|---|---|---|---|---|
| U56  | **+0.1409** | **+0.1409 (100.0%)** | **−0.0000 (−0.0%)** | −0.0004 |
| B136 | **−0.0009** | +0.0009 | −0.0018 | +0.0032 |

The two edge readings of each dial agree to 4 decimals (n dial: +0.1411 at g=1.00, +0.1407 at
g=0.75; gross dial: +0.0002 at n=20, −0.0002 at n=40), so the 2×2 is additive and the attribution
is not path-dependent. **Width carries all of it; gross carries none of it.**

## Why gross carries none of it — and what it does carry

Part C measures the gross dial's Sharpe span at fixed n over the whole grid: the maximum
|OOS Sharpe span across g| is **0.0112** (U56: ≤ 0.0023), against **0.0817** of CAGR span and
**0.1398** of MaxDD span. This replicates idea 51's invariance on a second grid: an unlevered
gross scalar is a *scale* dial, so it **cannot mechanically move Sharpe** and could never have
explained a Sharpe gap. The comparand — span across n at fixed g — is **0.2834–0.5286** of OOS
Sharpe, one to two orders of magnitude larger.

But gross is what decides the **4b verdict**, because it moves exactly the two bars Sharpe does not:
6 of the grid's 8 4b passes sit at g=0.75, and the corner pair is decided entirely by it —
A and B (g=1.00) fail on **DD** (−23.6%, −23.4% against the −20.23% cap) while C and D (g=0.75)
clear it (−18.2%, −18.0%). At g=0.50 the same books then fail on **CAGR**. The two dials are
therefore not substitutes at all: **n prices the Sharpe, g prices admissibility**, and the
"(40, 0.75) beats (20, 1.00)" headline is two unrelated facts stapled together.

## Why the width dial is nonetheless killed

1. **It does not replicate.** At the queue's own fixed monthly cadence the gap on B136 is
   **−0.0009** — nothing. The +0.14 is a U56 fact.
2. **n=40 is not an argmax, it is a plateau edge.** On U56 the OOS Sharpe runs
   0.941 / 1.073 / 1.078 / **1.219** / **1.226** / **1.224** for n = 5/10/20/40/80/ALL: n=40 is the
   first point of a plateau that n=80 and n=ALL match or beat. The finding is not "width 40", it is
   "stop concentrating at 20" — and the un-ranked EWALL control gets there too. Idea 240/256's
   grid-edge flag applies.
3. **The IS chooser is anti-informative about this dial.** spearman(IS Sharpe, OOS Sharpe) is
   **+0.162** (U56) and **+0.131** (B136) over the 18 points, **+0.143 / +0.314** over the six
   n-levels with g averaged out. The IS argmax is n=20 (U56) and n=40 (B136); the OOS argmax is
   **n=80 on both**. Rule-8 chooser regret: **−0.1479** (U56), **−0.1282** (B136).
4. **Rule 8 does not deliver D.** The chooser trained on 2009-2016 picks **(20, 1.00)** on U56 and
   **(40, 1.00)** on B136 — both g=1.00, both **failing 4b on the DD cap**. The gross setting that
   makes D admissible is exactly the one an IS-Sharpe chooser is blind to, because Sharpe is
   invariant in it. D is reachable only by choosing g after seeing the 4b verdict.

## Rule 8 walk-forward (params chosen on 2009-2016, read once on 2017-2026)

| panel | IS pick | OOS CAGR | OOS Sharpe | OOS MaxDD | 4b at the pick |
|---|---|---|---|---|---|
| U56  | n=20, g=1.00 | 16.38% | 1.0778 | −23.64% | **fail (DD)** |
| B136 | n=40, g=1.00 | 14.97% | 0.9714 | −29.50% | **fail (DD)** |
| U56  | *OOS argmax* n=80, g=0.75 | 13.11% | 1.2257 | −17.01% | pass |
| B136 | *OOS argmax* n=80, g=0.50 | 8.39% | 1.0997 | −15.13% | fail (CAGR) |
| — | RULES v2 (live) | 9.53% / 7.98% | **1.2851 / 1.1185** | −12.05% / −12.24% | fails CAGR floor |
| — | SPY | 15.45% | 0.8820 | −33.72% | — |

RULES v2's OOS Sharpe (1.285 on U56) beats **every one of the 36 grid points** (max 1.226), which is
why 4a is 0/36 and no width setting is a candidate to replace the live book.

## Cadence robustness (Part E — not a tuned dial)

The D−A gap and its split at W / M / Q:

| panel | W | M | Q |
|---|---|---|---|
| U56  | +0.1224 (n +0.1218, g +0.0006) | +0.1409 (n +0.1409, g −0.0000) | +0.2018 (n +0.1970, g +0.0047) |
| B136 | +0.1278 (n +0.1271, g +0.0007) | −0.0009 (n +0.0009, g −0.0018) | +0.0067 (n +0.0056, g +0.0011) |

The *attribution* is completely stable — the gross dial reads between −0.0018 and +0.0047 in all six
cells, i.e. zero everywhere. The *effect* is not: B136 shows the width gap weekly (+0.128) and
nothing monthly or quarterly, so the width dial's size is a (panel × cadence) accident even where its
sign is not.

## Grid census (monthly, 10 bps, all 36 points reported in `.grid.csv`)

- **4a: 0/36.** **4b: 8/36** — U56 (5,1.00), (10,0.75), (10,1.00), (20,0.75), (40,0.75), (80,0.75),
  (ALL,0.75); B136 (20,0.75).
- 4b first-failing bar: CAGR 11, DD 11, H2 6, pass 8. The DD/CAGR split is the gross dial; the H2
  block is B136 at n ≤ 10.
- Turnover falls monotonically in n (U56: 14.0 → 3.6 ×/yr from n=5 to n=ALL at g=0.75), so the width
  dial buys its Sharpe *and* cuts cost — consistent with idea 352's c* = 43.5 bps on D.

## Caveats

U56 and B136 are current-constituent panels (survivorship). Both share the same SPY series, so the
4b bars are identical across panels; only the books differ. The n=ALL arm is un-ranked EWALL over the
eligible set, included as the width dial's own limit point, not as a separate family.

Files: `.grid.csv` (36), `.corners.csv` (8), `.decomposition.csv` (18), `.invariance.csv` (12),
`.walkforward.csv` (40), `.cadence.csv` (24), `.informativeness.csv` (2), `.ctx.csv`,
`.console.txt` (full run).
