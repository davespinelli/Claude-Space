# Idea 251 — does-reach-belong-beside-every-instrument-price (lane C, 2026-09-06)

**Verdict: ANSWERED — YES, and the back-fill changes published claims.** `max_bought`
(REACH) is delivered for all six instruments on two ladders, two panels, two
instrument-free books and two cost rungs; **136 of the 240 published menu prices (56.7%)
were quoted at a budget the instrument could not reach on the ladder they were priced on**,
and **4 of the 40 published menu picks change** once reach is back-filled. But the column
is not free of the grid it is measured on, and it is not stable across windows: extending
each family's ladder to its admissible extreme rescues 19 of the 136, and reach measured
on 2009–2016 under-states 2017–2026 reach in **47 of 48 cells**. No RULES change, no new
KEEP; nothing in RULES.md, scan.py, bot.py or baseline.py touched.

Script `research/backtests/2026-09-06_does-reach-belong-beside-every-instrument-price_C.py`,
importing idea 245's module (base books, simulator, instruments) and through it idea 94's
`run_stop` — nothing re-implemented. **504 arms + 8 controls = 512 backtests, all reported**,
exactly two tuned dimensions (family, level); panel, book, cost and ladder are reporting
axes printed at every value.

## 0. Harness

| gate | result |
|---|---|
| [A] `run(no instrument)` vs `engine.backtest` | max\|dret\| **0.000e+00**, max\|dturn\| **0.000e+00** |
| [C] `run(stop=S)` vs idea 94's published `run_stop` | **0.000e+00** at every depth |
| [B] every shared point vs idea 74's **committed** grid CSV (288 points) | bought_pp **1.8e-15**, paid_pp **1.8e-15**, MaxDD **8.3e-17**, CAGR **9.7e-17** |
| [B2] idea 74's committed per-cell `max_bought` recomputed here | **1.8e-15** |
| [C-census] every extracted claim written to `.claims.csv` with file:line provenance | audit sample printed in the console |

Idea 74's window convention (drop the first 260 bars, the instruments' warm-up, from BOTH
arm and control) is kept exactly, which is what makes [B] a bit-for-bit check.

## 1. The column the queue asked for

`max_bought`, pp of MaxDD the family's **whole** ladder can buy, 10 bps, per cell:

| family | ladder | u56/EWALL0 | u56/CAND20 | broad/EWALL0 | broad/CAND20 | best cell |
|---|---|---|---|---|---|---|
| 200d gate | PUB | 4.20 | 1.21 | 7.02 | 4.07 | **7.02** |
| | EXT | 4.20 | 1.21 | 7.02 | 5.95 | **7.02** |
| MA band | PUB | 4.82 | 0.02 | 6.87 | 1.10 | **6.87** |
| | EXT | 4.82 | 0.15 | 6.87 | 1.10 | **6.87** |
| abs momentum | PUB | 3.41 | −0.11 | 5.05 | 2.60 | **5.05** |
| | EXT | 3.97 | 1.56 | 6.56 | 5.12 | **6.56** |
| de-gross (ref) | PUB | 13.04 | 12.74 | 14.65 | 14.86 | **14.86** |
| | EXT | 22.46 | 21.92 | 25.36 | 25.68 | **25.68** |
| ddctl (idea 40) | PUB | 7.49 | 8.12 | 8.57 | 9.42 | **9.42** |
| | EXT | 9.25 | 9.54 | 10.61 | 10.93 | **10.93** |
| trailing stop | PUB | 2.51 | 2.59 | 2.73 | 1.85 | **2.73** |
| | EXT | **5.44** | **6.45** | **6.91** | **6.13** | **6.91** |

PUB = idea 74's published 6-level ladder. EXT = the same family pushed to its admissible
extreme (`stop` down to 2%, `band` out to 30%, `200d` 20–500d, `abs` 10–756d, `ddctl`
2–40%, `dg` down to g=0, which is cash and is why de-gross is unbounded by construction).

**The stop's published reach was a grid edge.** Idea 74 reported "the stop cannot buy 4pp
at any depth"; its reach maximum sat at the *shallowest* level it swept (0.08). At stop=0.02
the stop buys **5.44–6.91 pp** in all four cells. The same happens to abs momentum
(5.05 → 6.56) and to ddctl (9.42 → 10.93). The gates and the band are NOT grid edges: their
reach is unchanged by extension, so ~7pp is a real ceiling for them.

## 2. How many published prices were quoted beyond reach

**Stratum 1 — the record's only price list that quotes AT budgets** (idea 74's committed
`menu.csv`: 2 panels x 2 books x 2 costs x 6 families x 5 budgets = 240 entries):

| | count | share |
|---|---|---|
| quoted beyond the **published** ladder's reach | **136** | 56.7% |
| still beyond reach on the **extended** ladder | **117** | 48.8% |
| rescued by extending the ladder | 19 | 14% of the 136 |

Per family (of 40 each, PUB / EXT): 200d **28 / 28**, band **30 / 30**, abs **33 / 31**,
de-gross **0 / 0**, ddctl **11 / 5**, stop **34 / 23**. So the exposure is overwhelmingly a
real instrument limit, not a grid artefact — with the stop (11 rescued) and ddctl (6) the
two exceptions.

**Stratum 2 — the record's prose prices.** 110 price-claim lines in 34 files → **238
(claim, named-instrument) pairs** (a comparative sentence naming several families is
exposed on each). Only **48 (20.2%) state the depth they were quoted at**; of those, 3 were
beyond the published reach and **0 beyond the extended reach** (all three are stop mentions
at 3.1–4.5pp against the stop's published 2.73pp ceiling — i.e. they are the very claim
section 1 refutes; one of the three is a false flag, a sleeve's own 4.5pp in a sentence
that merely cites idea 94's menu). Depths are read from the claim's own line: a ±3-line
window leaks numbers between adjacent claims (it attributed an unrelated 28.1pp figure from
a neighbouring CHANGELOG entry), and is reported only as an upper bound (3 of 92).

**The prose finding is the absence, not the count.** Four-fifths of the record's published
prices state no depth at all and none states a reach, so a reader cannot tell whether the
price applies at their budget. Over PROTOCOL's own budget grid {2,4,6,8,10}pp the share of
budgets on which each family's price is undefined is: stop 40% (80% on the published
ladder), 200d 40%, band 40%, abs 40% (60% published), ddctl 0% (20% published), de-gross 0%.
Across the 238 pairs, a budget drawn uniformly from that grid lands outside the named
instrument's reach **22.4%** of the time.

## 3. The back-fill changes 4 of 40 published menu picks

Median rate over the 4 cells at 10 bps, PUB → EXT (`unreach` = no level buys T):

| family | T=2 | T=4 | T=6 | T=8 | T=10 |
|---|---|---|---|---|---|
| 200d | 0.44 → 0.44 | 0.42 → 0.42 | 0.46 → 0.46 | unreach | unreach |
| band | −0.06 → −0.03 | 0.23 → 0.23 | 0.36 → 0.36 | unreach | unreach |
| abs | 0.41 → 0.32 | 0.53 → 0.65 | **unreach → 0.84** | unreach | unreach |
| **dg (ref)** | 0.63 | 0.62 | 0.62 | 0.61 | 0.61 |
| ddctl | 0.29 | 0.40 | 0.53 | 0.56 → 0.52 | **unreach → 0.59** |
| stop | 0.89 → 0.93 | **unreach → 0.68** | **unreach → 0.96** | unreach | unreach |

The cheapest entry a reader takes off the menu changes in **4 of 40** (panel, book, cost,
budget) cells, all at the deep budgets and all in the same direction — idea 40's book DD
control displaces de-gross, the reference lever idea 74 said was the only instrument
available there:

    broad/EWALL0 @10bps T=10pp : dg 0.58 -> ddctl 0.43
    broad/EWALL0 @25bps T=10pp : dg 0.58 -> ddctl 0.49
    u56/EWALL0   @10bps T= 8pp : dg 0.61 -> ddctl 0.45
    u56/EWALL0   @25bps T= 8pp : dg 0.61 -> ddctl 0.51

What does **not** change is the ordering idea 74 published at the shallow budgets, and the
stop's verdict: reachable at T=4 after all, but at 0.68 vs de-gross's 0.62 it is still
dominated by simply holding less. **Idea 74's reach LABELS were wrong for the stop; its
price CONCLUSION about the stop survives.**

## 4. Rule 8 — is `max_bought` an ex-ante column?

Level chosen to maximise reach on 2009–2016 only, 2017–2026 read once, 48 cells
(2 panels x 2 books x 2 costs x 6 families):

* IS reach-argmax == OOS reach-argmax in **22/48** (PUB) and **18/48** (EXT); median OOS
  reach regret **0.04 pp** (PUB) and **0.33 pp** (EXT), mean 0.93 / 1.10, max 5.07 / 6.66.
* Spearman(IS reach, OOS reach) across the six families = **0.743** (PUB) / **0.700** (EXT)
  — the column ORDERS the instruments the same way out of sample.
* Its LEVEL does not transfer: mean IS → OOS reach is 200d 1.26 → 3.94, band 1.79 → 3.19,
  abs 2.04 → 3.51, dg 13.16 → 23.90, ddctl 4.05 → 9.89, stop 0.80 → 5.14 pp. **OOS reach
  exceeds IS reach in 47 of 48 cells** (idea 117's mechanism again: the IS window's crashes
  are shallow, so there is less drawdown to buy).

So reach is publishable as a **ranked, window-stamped** column, not as a number. A
`max_bought` read off 2009–2016 would have called the stop unable to buy 1pp.

## 5. KEEP paths (PROTOCOL rule 4, every arm)

4a passes 209/504, 4b passes 57/504. Nothing new: the best 4b arm is idea 74's own PARK
by-product, re-derived — u56/EWALL0 + 12% band, **14.09% / 1.233 / −19.4%**, halves
1.268/1.211, **OOS 15.22% / 1.272 / −19.4%**, 1.9x turnover — which idea 250 is already
sweeping for the grid edge it sits on. References on the same window: no-instrument
EWALL0 control 13.30% / 1.128 / −22.5% (fails 4b on DD), **RULES v1 6.45% / 0.664 / −13.8%**
(halves 0.641/0.688, OOS 7.73% / 0.747 / −13.8%), **SPY 15.23% / 0.889 / −33.7%** (halves
0.957/0.834, OOS 15.45% / 0.882 / −33.7%). This idea is a measurement of the record, not a
candidate book.

## 6. Recommendation (proposed, not applied — PROTOCOL rule 6)

Any published drawdown-instrument price should carry, beside it, `max_bought` **with the
ladder and the window it was measured on**, and a price quoted at a budget above that
number should be printed `unreachable` rather than as a rate. Reach earns the column: it
decided 136 of 240 published quotes and it changes 4 of 40 published picks. But two
qualifiers are mandatory — the number moves when the ladder is extended (the stop:
2.73 → 6.91 pp) and it moves when the window changes (47/48 cells), so a bare
`max_bought` is as misleading as no column at all.

## 7. Limits

* **Survivorship.** Both panels are current constituents, so crashes here are shallower
  than they were; reach is an absolute (not within-cell) quantity, so this bias is NOT
  cancelled and every `max_bought` above is, if anything, an under-statement.
* **Reach is book-dependent.** It is quoted on two instrument-free books at gross 0.75;
  a price published on a different book has a different reach. Stratum 2 uses the most
  generous of the four cells, which under-counts the exposure rather than inflating it.
* **The prose census is a keyword census.** Family attribution is "the claim names this
  instrument", not "the claim prices this instrument"; the 20 unclassified lines and the
  full 258-pair table are committed in `.claims.csv` for audit.
* `dg`'s EXT reach includes g=0 (hold cash), the degenerate limit; its unboundedness is a
  construction fact, not a measurement.
* **The census reads the record, so the record's own growth changes it.** The committed
  `.claims.csv` and every stratum-2 count above were produced against the record as it
  stood *before* this idea's CHANGELOG / QUEUE / result entries were written; re-running
  the script after this commit will find those entries too and return slightly larger
  counts. The stratum-1 numbers (136 / 117 / 4 of 40) are computed from committed CSVs and
  are stable.
