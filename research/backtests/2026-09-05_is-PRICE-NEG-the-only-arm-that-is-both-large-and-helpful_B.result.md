# Idea 193 — is-PRICE/NEG-the-only-arm-that-is-both-large-and-helpful (lane B, 2026-09-05)

**ANSWERED, and the answer is bigger than the question: NO — and the reason is that the PRICE key
is not a signal at all.  On auto-adjusted closes a cross-sectional PRICE-LEVEL key is, by an exact
identity, `terminal price minus realised future total return`.  KILL of PRICE/NEG.  KILL of the
dollar-volume rescue that first looked like a genuine find.  PARK of the market-cap leg (no data).
No new book, no KEEP-candidate, RULES untouched.**

Script `research/backtests/2026-09-05_is-PRICE-NEG-the-only-arm-that-is-both-large-and-helpful_B.py`
— 204 real arms + 240 matched-null arms + 4 controls = 448 backtests, 76 s, deterministic, no
network.  Outputs: `.arms.csv` (every grid point), `.decomp.csv`, `.walkforward.csv`,
`.reproduction.csv`, `.console.txt`.

**Tuned parameters: exactly two** — the tilt strength `m ∈ {0.20, 0.50, 1.00}` and the direction
`{POS, NEG}`, both inherited verbatim from idea 181.  The KEY is a reported axis, never selected on
outside the pre-registered rule-8 selectors.  All grid points are printed.

## Reproduction — 6 of 6, before any new number was read

| check | result |
|---|---|
| R0 RULES v1 on u56 @10bps | **6.45305% / 0.66418 / −13.82780%** — the published anchor to every printed digit |
| R1 adjusted-price identity `px[T]/px[t] == cumulative TR(t→T)` | max abs err **3.18e-12** (broad), **4.26e-13** (small) |
| R2 `fast_backtest == engine.backtest` | **2.08e-17** / **2.78e-17** |
| R3 cost identity `r_c == r_0 − turnover·c/1e4` | **2.08e-17** / **2.78e-17** |
| R4 idea 181's published grid, 72 (panel,key,dir,m,cost) cells rebuilt from scratch | max \|dSharpe − published\| = **4.16e-16** |
| R5 idea 181's 24 matched-null bands rebuilt from the parent's own seed | max \|band − published\| = **3.19e-16** |
| R6 clause verdicts on those 72 cells | **0 mismatches** |

The 17 positive clearers live on exactly two panels — `broad` (9) and `small` (8); none on u56 —
so this run rebuilds idea 181's corpus-T machinery on those two and substitutes the key.

## (1) The published PRICE key is not implementable — this is an identity, not a finding about data

`load_universe()` serves **auto-adjusted** closes, so the price series *is* a total-return index and
`px[T]/px[t]` **is** the cumulative total return from t to T (R1: 3.2e-12).  Therefore, exactly:

```
log PRICE_t  =  log px[T]  −  log TR(t → T)
```

The cross-sectional rank of the price level at date t is the rank of the **terminal price** minus
the rank of the **realised future total return to the end of the sample**.  Neither term is
knowable at t.  A price-LEVEL key on this data cannot be traded at any cost, at any gross, on any
panel.  By contrast a *ratio* key — MOM, R3, REBASED — cancels the factor
(`px[t]/px[t−k]` on adjusted closes **is** the raw total return over `[t−k, t]`) and is clean.

## (2) The whole of PRICE/NEG's dSharpe is the look-ahead term

Running the two halves of the identity as their own arms (labelled `oracle` everywhere; excluded
from every selector), means over the 12 grid points:

| arm | mean dSharpe_F | share of PRICE/NEG |
|---|---|---|
| **PRICE/NEG** (published) | **+0.3532** | 1.00 |
| **FWDRET/POS** (the future-return term alone) | **+0.6921** | **+1.879** |
| **PXTERM/NEG** (the terminal-level term alone) | **−0.1514** | **−0.373** |

The future-return term delivers *nearly twice* the published effect on its own; the level term works
*against* it.  Mean cross-sectional Spearman(PRICE, FWDRET) = **−0.296** (broad), **−0.424** (small).
FWDRET/POS is also the **only clearing-and-positive arm in the entire run that passes 4b**
(broad, m=1.0 @10bps: 23.67% / 1.5414 / −20.21%, OOS Sharpe 1.7411) — the ceiling is an oracle.

## (3) The queue's three substitutions

| substitution | mean dSharpe (NEG) | clearing-AND-positive | 4b |
|---|---|---|---|
| **FROZEN** — price rank frozen at each name's entry date | +0.1621 broad / +0.1633 small | 6/12 broad, **0/12 small** | 0/24 |
| **DVOL** — 20d mean dollar volume (small panel only) | **+0.5777** | **6/12** | 0/12 |
| **MCAP** — market capitalisation | **PARK: needs local/Actions data** | — | — |

MCAP is **parked, not run**: no shares-outstanding series is cached in `data/` and this sandbox has
no internet.  That leg of the queue item is unanswered here and is re-queued as idea 195.

FROZEN does not replicate the published effect (it roughly halves it on broad and is inside the
null band at every point on small) — **P2 MISS**.  DVOL/NEG, on the other hand, is *larger* than
PRICE/NEG on the same panel (+0.578 vs +0.466), clears at every m and both rungs, passes **4a** at
3 of 12 points, and won its rule-8 cells 6/6 — **P4 MISS**, and for one reading it looked like the
first genuine, causal, capital-relevant find of the project.

## (4) It is not.  The liquidity tilt is the same leak.  *(post-hoc control, declared as such)*

`DVOL = adjusted close × share volume`, so it carries the R1 factor too.  Two controls, added
**after** P4's miss was read and labelled post-hoc everywhere:

* **DVOLT** = each name's **terminal** price × volume — same liquidity cross-section, R1 factor removed.
* **VOLSH** = share volume alone — no price term (yfinance still split-adjusts volume, so a weaker leak remains).

| key | Spearman with FWDRET | mean dSharpe (NEG) | clearing-AND-positive |
|---|---|---|---|
| DVOL | **−0.596** | **+0.578** | **6/12** |
| VOLSH | **−0.417** | **+0.323** | 5/12 |
| **DVOLT** | **−0.096** | **+0.142** | **0/12** |

The effect size and the clear rate track the leak monotonically, and DVOL rank-correlates with
DVOLT at **+0.817** and with VOLSH at **+0.813** — the three measure nearly the same liquidity
cross-section, and only the leaky ones work.  **Remove the future information and the illiquidity
tilt dies inside the null band at every one of 12 grid points.**

## (5) The queue's question, answered

Of **204 real arms**, 50 are clearing-and-positive.  43 of them are a price-LEVEL key (PRICE 12/24,
FROZEN 6/24), a liquidity key whose price term carries the leak (DVOL 6/12, VOLSH 5/12), or an
outright oracle (FWDRET 12/24, PXTERM 2/24).  The **7 leak-free** ones — MOM/NEG ×1, R3/NEG ×4,
REBASED/NEG ×2, *all* at the smallest tilt m = 0.20 — clear their band by **0.0091 to 0.0375**, i.e.
they sit on the lip of a one-sided 1/21 test, and **none passes 4b**.
**Zero leak-free arms are both clearing-and-positive and 4b-passing**
(**P6 HIT**).  4b passes across the whole run: **4 of 204** — broad MOM/NEG/0.5@10 (12.93% / 1.0138 /
−18.80%), broad R3/POS/0.2@10, broad R3/POS/1.0@10, and the FWDRET oracle; none of the three real
ones clears the null.  Both KEEP paths by class: 4a broad causal 28/36, small causal 11/60,
**DVOLT 0/12**; 4b broad causal 3/36 and **0 everywhere else**.

**No KEEP-candidate.  RULES untouched.**

## (6) Rule 8 walk-forward — key chosen on ≤ 2016-12-31 only, 2017–2026 read once

12 cells = 2 panels × 3 m × 2 cost rungs.  Oracle keys are excluded from every selector.

| selector | mean OOS Sharpe | ΔOOS vs S0 | t (naive) | t (cost-collapsed, n=6) | W/L | n |
|---|---|---|---|---|---|---|
| C-DVOL/NEG (small only) | +1.2032 | **+0.8088** | +7.94 | +5.02 | 6/0 | 6 |
| ORACLE-OOS (ceiling) | +1.1527 | +0.5466 | +5.58 | +3.77 | 12/0 | 12 |
| C-VOLSH/NEG (small only) | +0.8986 | +0.5042 | +12.12 | +7.67 | 6/0 | 6 |
| C-PRICE/NEG | +1.0560 | +0.4500 | +7.28 | +4.91 | 12/0 | 12 |
| S1 IS-argmax (all keys) | +1.0091 | +0.4030 | +5.98 | +4.04 | 12/0 | 12 |
| S2 IS-argmax (causal as pre-registered) | +0.9781 | +0.3720 | +2.90 | +1.96 | 11/1 | 12 |
| C-REBASED/NEG | +0.7722 | +0.1661 | +3.79 | +2.56 | 12/0 | 12 |
| **S2LF IS-argmax (leak-free) [post-hoc]** | +0.7431 | **+0.1370** | +3.22 | **+2.19** | 11/1 | 12 |
| S3 clause+positive | +0.6198 | +0.0137 | +1.39 | +1.00 | 2/0 (abstains 10 of 12) | 12 |
| **S0 do-nothing** | **+0.6061** | 0 | — | — | — | 12 |

Benchmarks over the same OOS window: broad RULES v1 @10bps **5.94% / 0.5763 / −21.19%**, small
RULES v1 **6.35% / 0.4923 / −36.12%**, SPY **15.45% / 0.8820 / −33.72%**.

**P7 MISS — the eight-run streak of do-nothing wins ends, but not cleanly.**  Every large selector
win is carried by a key that knows the future: strip the leak and the causal selector's edge falls
from **+0.372 to +0.137**, on 6 effectively-independent cells (the two cost rungs are the *same*
book, so the naive n=12 t-stats are overstated and the cost-collapsed column is the honest one).
A +0.137 mean OOS Sharpe edge from a 3-key × 2-direction pool, on two current-constituent panels,
is not a result to spend capital on; it is a candidate for a bigger corpus (queued as idea 196).

## Pre-registered predictions: 4 of 7 HIT

| | prediction | result |
|---|---|---|
| **P1** | the adjusted-price identity holds < 1e-10 | **HIT** (3.18e-12) |
| P2 | FROZEN/NEG is large and clears on both panels | **MISS** (6/12 clear, 0/12 on small) |
| **P3** | FWDRET/POS carries most of PRICE/NEG, PXTERM/NEG little | **HIT** (share +1.879 / −0.373) |
| P4 | DVOL/NEG at m=0.2 is not clearing-and-positive | **MISS** (2 of 2) |
| **P5** | REBASED/NEG much smaller than PRICE/NEG | **HIT** (0.1205 vs 0.3532) |
| **P6** | zero causal clearing-and-positive arms pass 4b | **HIT** (0) |
| P7 | the causal selector does not beat do-nothing | **MISS** (+0.372; +0.137 once leak-free) |

## What this run proposes (report-only; no PROTOCOL edit made here — rule 6)

> **Proposed PROTOCOL clause 12 (for Sunday review).**  Every price series in `data/` is
> auto-adjusted, so `px[T]/px[t]` *is* the realised total return from t to T.  Any key that reads
> the **level** of such a series cross-sectionally — a raw price rank, a price-level tilt, a
> frozen-at-entry rank, or any product with a price (dollar volume, notional, price × anything) —
> is contaminated with future information by construction and is **not a candidate for any book**.
> Only **ratio** keys (returns, momentum, volatility, price relative to its own past) are safe: the
> adjustment factor cancels.  A backtest whose key is a price level must report the mean
> cross-sectional Spearman of that key against `px[T]/px[t] − 1` alongside its dSharpe.

Blast radius in the record: the LEADERBOARD carries **6 rows naming PRICE/NEG**, all from ideas
181/192; idea 181's `PRICE` is one of five keys across 36 published cells per panel, and idea 192's
headline "12 of the 17 positive clearers are PRICE/NEG" is now explained rather than replicated.
Nothing that has ever been a KEEP-candidate used a price-level key, so no live rule is affected.

## Caveats

* **Survivorship.** Both panels are CURRENT constituents (idea 54); the small panel additionally
  drops the 44 tickers with `max_1d_move ≥ 1.0`.  Every number above inherits that bias in one
  direction, and an illiquidity tilt on a survivorship-screened small-cap panel is exactly where it
  bites hardest — a second reason, independent of the leak, not to trust §(3)'s DVOL result.
* **DVOL exists only on the small panel** (`data/volume_small.csv.gz`).  SPY carries no volume and
  is given the neutral rank 0.5 in the volume keys only; the control book's mean SPY weight share on
  the small panel is **0.0000%**, so the concession changes nothing.
* **DVOLT and PXTERM are not implementable either** — they use the terminal price.  They are
  controls that isolate the *path* leak, not candidate signals.
* The two cost rungs are derived from ONE 0 bps run via the engine's own identity (R3 exact); they
  are the same book, so paired t-statistics over 12 cells are overstated (see the cost-collapsed
  column).
* All rows are weekly, t+1, top-20 equal weight at 75% gross — idea 2's base book throughout.

## Queued from this run

* **195. market-cap-as-the-third-substitution** — the parked leg: cache shares outstanding (Actions
  or local) and re-run idea 193's substitution with a true market-cap key, the one size proxy that
  is neither a price level nor a volume product.
* **196. does-the-leak-free-selector-edge-survive-a-third-corpus** — S2LF's +0.137 (t +2.19 on 6
  cost-collapsed cells) is the first non-zero do-nothing loss in nine runs; re-run the same three
  leak-free keys on idea 175's 115-book corpus and report whether it replicates or is a two-panel
  accident.
* **197. audit-every-published-key-for-the-adjustment-leak** — apply §(4)'s Spearman-vs-FWDRET test
  to every key in the LEADERBOARD's published books and report which are levels and which are ratios.
