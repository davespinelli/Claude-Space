# Idea 1226 (lane B, 2026-09-17) — does ANY committed SE in the record state what it DIVIDED BY?

**VERDICT: KILL (capital). ANSWERED = NO — not one committed result sentence names its
denominator, and the choice is worth a factor of 2.69 on the bar and nothing at all on money.**

Script: `2026-09-17_does-any-committed-SE-in-the-record-state-what-it-DIVIDED-BY_B.py`
(offline, deterministic, 76s, **gates 12 of 12**).

## The premise, read from the record

1219 published as declared bycatch that the SAME Newey-West SE of the same daily difference
calibrates at crit95 2.0161–2.4754 when the pooled BOOK volatility puts it on the Sharpe scale
and 0.9219–1.2778 when the SD of the DIFFERENCE does. It stated its own choice in a source
comment and stopped. Both committed bands **reproduce here to 3.3e-05 and 4.7e-05 on 1219's own
null pairs** (gates G7, G8), so this run measures the record's object, not a lookalike.

## The two dials (PROTOCOL rule 4), all 16 cells published

CLAIM SET {C_1219, C_HEAD, C_MEMO, C_ALL} × DENOMINATOR SET {D_PAIR, D_VOL3, D_VOL4, D_ALL5}.
The SE **numerator** is held fixed at one construction (HAC/Bartlett on the mean daily
difference) for the whole run; the L ladder {21,63,126,252,504} is 1212's, reported at every
rung and never chosen. Five denominators measured, not tuned: D_BOOKVOL (1219's choice),
D_DIFFSD (1219's bycatch), D_ANCHOR, D_MAXVOL, D_SPYVOL.

## (1) The census — the answer, and it is NO

| claim set | pop | n | states in text | in script | either | share |
|---|---|---|---|---|---|---|
| C_1219 | SE | 113 | **0** | 3 | 3 | 0.0265 |
| C_HEAD | SE | 115 | **0** | 3 | 3 | 0.0261 |
| C_MEMO | SE | 264 | **0** | 4 | 4 | 0.0152 |
| C_ALL | SE | 316 | 38 | 6 | 43 | 0.1361 |
| C_HEAD | t | 211 | **0** | 7 | 7 | 0.0332 |
| C_ALL | t | 482 | 47 | 40 | 87 | 0.1805 |

**Every one of C_ALL's text-stating hits is in QUEUE.md** (38 of 38 SE, 47 of 47 t) — the queue
entries that *ask* this question, 1219's bycatch note and idea 1226 itself. Zero are in
LEADERBOARD.md or CHANGELOG.md at any claim set. The record's only statement of a denominator
is the question about it. `not-ratio` (38–81 per set) is published separately and folded into
neither pass nor fail: those are claims whose emitting script never puts an SE on a ratio scale
by this rule's markers, which this rule cannot prove either way.

## (2) The bar, re-measured not quoted (90 disjoint gross-matched null pairs, true Δ = 0)

crit95 of |t| on P_1219, **numerator, basis and L identical across the row**:

| denominator | L=21 | L=63 | L=126 | L=252 | L=504 | mean daily scale |
|---|---|---|---|---|---|---|
| D_BOOKVOL | 2.0161 | 2.0427 | 2.1229 | 2.1587 | 2.4754 | ×1.0000 |
| D_DIFFSD | 0.9382 | **0.9219** | 0.9284 | 1.1051 | 1.2778 | ×0.4381 |
| D_ANCHOR | 2.0128 | 2.0575 | 2.1342 | 2.1602 | 2.4630 | ×1.0003 |
| D_MAXVOL | 2.0194 | 2.0575 | 2.1377 | 2.1621 | **2.4877** | ×1.0040 |
| D_SPYVOL | 2.9064 | 3.0321 | 3.1066 | 3.0950 | 4.0721 | ×1.5201 |

Reference, not a rung: the iid-bootstrap SE of the Sharpe **difference** calibrates at 1.9697 —
that is where the quoted 1.96 comes from.

- **D_PAIR band [0.9219, 2.4754] = ×2.69**; D_ALL5 [0.9219, 4.0721] = ×4.42.
- **At a SINGLE L the band is ×2.80–×3.35**, so the L dial cannot be blamed for it.
- **The exposure is one distinction, not five.** D_BOOKVOL, D_ANCHOR and D_MAXVOL agree to
  0.4% — any book-volatility reading gives the same bar. The whole factor of 2.69 is
  difference-SD versus any book vol, because two books correlated at 0.9037 have a difference
  whose SD is 0.438 of theirs. D_SPYVOL (the information-ratio scale) is the one further rung.
- **Seed luck, stated rather than hidden.** An independent replication under this run's own
  seeds (P_OWN) puts the same bands 0.4035 lower at worst, against a per-cell Monte-Carlo SE of
  at most 0.2028 (bootstrapping the 90 pairs, 400 draws). A crit95 read off 90 pairs is a
  measurement with a width of roughly ±0.18, and the record quotes such numbers to four
  decimals without one. The headline uses P_1219 so nothing rests on this run's draw; the
  16 exposure cells move by at most 30 claims on P_OWN's bands and do not reorder.

## (3) The exposure — the 16 cells

| claim set | denom set | n | \|t\|>1.96 | AMBIG | of all | of sig | LOST | GAINED |
|---|---|---|---|---|---|---|---|---|
| C_1219 | D_PAIR | 210 | 126 | 54 | 0.2571 | 0.4286 | 15 | 39 |
| C_1219 | D_ALL5 | 210 | 126 | 95 | 0.4524 | 0.7540 | 56 | 39 |
| C_HEAD | D_PAIR | 211 | 126 | **55** | **0.2607** | **0.4365** | 15 | 40 |
| C_HEAD | D_VOL4 | 211 | 126 | 56 | 0.2654 | 0.4444 | 16 | 40 |
| C_HEAD | D_ALL5 | 211 | 126 | 96 | 0.4550 | 0.7619 | 56 | 40 |
| C_MEMO | D_PAIR | 359 | 191 | 95 | 0.2646 | 0.4974 | 24 | 71 |
| C_MEMO | D_ALL5 | 359 | 191 | 165 | 0.4596 | 0.8639 | 94 | 71 |
| C_ALL | D_PAIR | 482 | 263 | 131 | 0.2718 | 0.4981 | 39 | 92 |
| C_ALL | D_ALL5 | 482 | 263 | 220 | 0.4564 | 0.8365 | 128 | 92 |

(All 32 rows, both pair sets, in `.exposure.csv`.) On the narrowest honest reading — the two
denominators the record has actually exhibited — **55 of 211 committed t's (0.2607), and 0.4365
of the ones published as significant, have a verdict that is a function of a choice nobody
wrote down.** 15 are significant at 1.96 and not at the strictest bar in the pair.

## (4) The capital content — rule 8, and it buys nothing

216 books (9 N × 4 H × 2 cadence × 3 panels), parameters chosen on 2009–2016, 2017–2026 read
ONCE, 10 bps, next-day execution. Then 1,200 publish decisions: 24 contexts × 5 denominators ×
5 L × 2 bars, every one published.

- **Doing nothing** (anchor N=20 at all 24 contexts): mean OOS Sharpe 0.8575.
- **HONEST bar minus QUOTED 1.96** over the 25 (denominator, L) cells: **+0.0014 of mean OOS
  Sharpe (SE 0.0014, t +1.05)**, moves −1.72, 4b +0.00; the two bars make identical decisions
  at 10 of 25 cells. H_WF **REFUTED**.
- **The dial itself at the bar the record quotes**: D_BOOKVOL 7.0 moves / 0.8553, D_ANCHOR 7.2 /
  0.8553, D_MAXVOL 8.2 / 0.8505, D_SPYVOL 10.6 / 0.8532, and **D_DIFFSD 0.0 moves / 0.8575 at
  every single L**. That is the sharpest consequence in the run: had the record's SEs been
  divided by the difference SD, **no publish decision in this entire family would ever have
  been made** — the unstated denominator is the difference between a chooser that moves 7–13
  times and one that never moves at all. Every one of those readings still lands at or below
  doing nothing.
- **Count-matched random bar**: 9 of 50 rules clear the 90th percentile of their own null
  against 5.0 by chance (one-sided binomial p = 0.0579). Not separation. 17 of 50 beat doing
  nothing. H_ANCHOR is scored SUPPORTED against its declared "at least one rule" bar, and that
  bar was too weak — read it as no.
- **BOTH KEEP PATHS: 4a 0 of 216. 4b full AND OOS 12 of 216 over 12 DISTINCT books** (U56 11,
  B136 1, SMALL 0). Best: U56 / W / N=12 / H=126 — full 17.65% / 1.1658 / −20.17% (halves
  1.2741 / 1.0833), OOS 18.78% / 1.1701 / −20.17%. SPY U56 full 15.06% / 0.8814 / −33.72%, OOS
  15.15% / 0.8684 / −33.72%; live RULES v2 full 8.60% / 1.1980 / −12.05%. **That book is
  already in the record (1183, 1212, 1219). CONFIRMATORY, NOT GENERATIVE. NOT PROMOTED, NO
  RULES CHANGE.**

## Survivorship (rule 9)

U56 and B136 are CURRENT-CONSTITUENT lists; SMALL is the current sub-$2B screen less the
documented max_1d_move ≥ 1.0 exclusion (52 of 715 dropped, 663 names, SPY as benchmark only).
Arms A and C scan committed text and source and carry no market bias. Arm B is one construction
measured against itself and the bias largely cancels out of a critical-value **ratio**, which is
the whole headline. It does NOT cancel out of Arm D's OOS levels or the 4b legs, so any pass
there is an upper bound.

## What this is worth

The reporting defect is real, large and cheap to fix: an SE on a ratio scale is a quotient and
the record has never written down the bottom half of it, at a cost of a factor of 2.69 on the
bar and 0.2607 of its own committed t's. The repair is worth **nothing in OOS Sharpe** (+0.0014,
t +1.05), which is the same answer 1210, 1219, 1221 and 1227 have now returned from five
directions: the record's bars are not what is standing between it and capital. Recommended as a
one-line PROTOCOL reporting clause at a Sunday review, not as a rules change — and this run
proposes none.
