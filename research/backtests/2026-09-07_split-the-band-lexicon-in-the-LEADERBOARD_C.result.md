# Idea 387 — split the band lexicon (lane C, 2026-09-07)

**Verdict: ANSWERED — INFRASTRUCTURE DEFECT CONFIRMED and QUANTIFIED; idea 384's
"opposite drawdown signatures" contrast was fully CONFOUNDED in the archive and is
RE-ESTABLISHED here on a matched grid. No 4a anywhere (0/27 at every rung), no new
4b object.**

## The audit (the queue's question)

Corpus: 319 committed scripts, 1,345 committed CSVs, 3,291 LEADERBOARD lines.
Pre-registered 4-class taxonomy — `NT` (no-trade / exit RANK buffer, integer rank
slack), `MAB` (200d MA band half-width, fractional collar), `SHARE` (idea 103's
per-name share multiplier), `OTHER`. Classifier gated (G_CLS 7/7) against the classes
ideas 359 and 384 established by hand before any count was read.

| corpus | result |
|---|---|
| CSV dial columns | **135 (file, column) instances in 130 CSVs**: SHARE 51 (37.8%), MAB 41 (30.4%), NT 38 (28.1%), OTHER 5 |
| the letter `m` | **72 CSVs — SHARE 51 (71%), NT 21 (29%)**. Two instruments, one name. |
| `band` / `b` | **46 CSVs — MAB 39 (85%), NT 3 (7%), OTHER 4 (9%)**. Three instruments, one name. |
| scripts | 158 of 319 use band language; **37 (23.4%) carry cues for MORE THAN ONE instrument in the same file** (33 MAB+NT, 4 MAB+NT+SHARE) |
| LEADERBOARD prose | 284 band-speaking rows: NT 68, MAB 48, **POOLED 11 (3.9%)**, **UNATTRIB 153 (53.9%)** — over half name a band with no recoverable instrument cue at all |

## The finding the queue did not ask for, and the reason the audit matters

**0 of 46 band-sweeping scripts ever swept BOTH instruments** (28,626 recoverable
dMaxDD observations; every script contributes exactly one class). Idea 384's contrast
is therefore **100% between-script** — confounded with panel, book-form, era and cost
rung. The archive cannot establish it. The re-derived archive split reproduces 384's
signs (NT 56.1% improve, median +9.9 bp; MAB 57.5% worsen, median −29.4 bp) but that
number is not evidence.

## The matched grid (leg C) — the control the archive lacks

One parent book (top-20 of the v1 composite, vol scaler off, RULES v1 eligible),
one anchor, g=0.75, weekly, 3 panels; the **only** thing that moves is which dial is
turned. Two tuned parameters: `m ∈ {0,5,10,20,40}`, `b ∈ {0,.03,.06,.12}` — 27 cells
× 3 rungs, all reported. Gates G1/G2 0.000e+00, G3a 0 disagreements, G3b 0/242,015
cells, G4 max|d| 0.000e+00 vs idea 333/384's committed row.

| arm | cells | improves DD | median dMaxDD | median dSharpe | median dTurnover | median dNames | corr(MaxDD, dMaxDD) |
|---|---|---|---|---|---|---|---|
| **NT** | 12 | **8/12 (66.7%)** | **+75.2 bp** | +0.0410 | **−6.31x/yr** | **+0.0000** | +0.160 |
| **MAB** | 9 | **2/9 (22.2%)** | **−41.6 bp** | +0.0057 | −0.23x/yr | −0.0185 | **+0.781** |

The opposite drawdown signature **replicates under the control** — and the two
instruments differ on every other axis too: NT removes **27x more turnover** per unit
of dial and moves holdings by exactly zero (reproducing idea 359 independently), while
MAB's drawdown damage **scales with the book's own depth** (corr +0.781 vs NT's +0.160
— H_scale for MAB, H_const for NT, the split idea 384 read out of the archive). The
defect is substantive, not cosmetic. MAB monotonicity holds only on U56
(spearman −1.000) against −0.500 on B136 and SMALL439, so 384's monotone a(m) is a
one-panel fact.

## KEEP paths and rule 8

4a **0/27 at 0, 10 and 25 bps** — nothing beats RULES v2. 4b **14/27 @0, 9/27 @10,
5/27 @25**, every passer on U56 and every one a filed object. First-failing 4b bars
@10 bps: H2 18, DD 12, OOS 10, H1 9, CAGR 9.

Rule 8 (dial on IS 2008-2016 Sharpe @10bps, 2017-2026 read once): **4/6 picks above
SPY OOS 0.882, 0/6 above RULES v2 OOS, 5/6 above the shared anchor, mean regret
+0.0071**. U56 NT picks m=40 → OOS 1.1892 (4b pass, but n+m=60 exceeds the 55-name
ceiling — idea 384 already killed this cell as degenerate). U56 MAB picks b=0.12 →
13.88% / 1.1297 / −18.72%, H1/H2 1.0773/1.1800, **OOS 1.2384**, 4b pass at 0/10/25 bps
— and it **reproduces idea 359's committed MAB-TOPN U56 n=20 b=0.12 row to six
decimals**, so it is an independent reproduction, not a discovery. Both U56 picks sit
on the grid EDGE (idea 240/256's flag). Nothing proposed.

## Proposed amendment (INFRASTRUCTURE — no RULES.md change, not a Sunday item)

Retire `m`, `band`, `b`, `x`, `e` and `width` as **dial column names in committed grid
CSVs**. Three reserved names, one instrument each:

- **`nt`** — no-trade / exit RANK buffer, integer rank slack (`nt_in` / `nt_out` where
  one-sided). Absorbs today's `m` (integral), `x` (RANKX), `e` (RANKE).
- **`mab`** — 200d moving-average band HALF-WIDTH, fractional collar. Absorbs today's
  `band`, `b`, `width`.
- **`share`** — idea 103's fractional per-name share multiplier. Absorbs today's `m`
  (fractional).

Companion to idea 359's proposed `names` column: any grid CSV carrying a band dial
writes the reserved name, and any LEADERBOARD row citing a band names the instrument.
That closes the 153 UNATTRIB rows going forward and makes the 11 POOLED rows
unwritable.

## Caveats

(1) All three panels are current-constituent lists — SURVIVORSHIP; 4b's CAGR floor is
tested in the book's favour. (2) The LEADERBOARD prose leg is cue-based and noisiest;
its 53.9% UNATTRIB rate is the honest measure of its own limits and no conclusion rests
on it alone. (3) The census is a census of what the record WROTE — a script that swept
a band but committed no CSV cannot enter it. (4) The matched grid holds n=20 fixed, so
it prices the two instruments at one width, not across widths.
