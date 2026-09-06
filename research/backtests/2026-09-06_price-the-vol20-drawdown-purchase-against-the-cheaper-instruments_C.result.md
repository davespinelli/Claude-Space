# Idea 288 — price the vol20 drawdown purchase against the cheaper instruments

**Verdict: ANSWERED / KILL for vol20 as an instrument worth owning.** Idea 56's reading survives —
`vol20 < 0.60` is a drawdown instrument, not a return edge — but once it is put beside the rest of
the record's drawdown menu at matched purchase depth it is the **most expensive** thing on the
shelf: it is the only instrument that charges Sharpe for the drawdown it buys, and a pure exposure
cut that contains no information at all buys the same 3.12pp with **+0.057 more Sharpe**.

Script `2026-09-06_price-the-vol20-drawdown-purchase-against-the-cheaper-instruments_C.py`,
40 grid points x 2 panels = 80 book cells, all reported. 10 bps, weekly, t+1, PROTOCOL rules 1-9.

## Reproduction gate (asserted before any new number)

`VOL20(0.60)` against the un-gated base book B0 on U56: **dCAGR +1.94pp, dSharpe -0.0647,
dMaxDD +3.12pp** — idea 56's published digits exactly. B136 gives +2.07pp / -0.0641 / +3.31pp.

## The menu (all four applied to the SAME base book B0 = composite top-20 EW @75% gross, no gate)

| instrument | dial | what it is |
|---|---|---|
| `VOL20(v)` | `vol20 < v`, de-gross | idea 56's instrument |
| `BAND(b)` | 200d +/- b band with hysteresis, de-gross | RULES v2 clause 2 |
| `DEGROSS(m)` | every weight x m, remainder cash | the **null** — a pure exposure cut, zero information |
| `SLEEVE(f)` | `(1-f) B0 + f x S4` (idea 18 variant B on TLT/GLD/DBC/UUP) | idea 100/129's sleeve |

## 1. On the CAGR axis the menu is flat, and vol20's apparent win is noise

Idea 74's own axis (pp of CAGR surrendered per pp of MaxDD bought) does not separate the
instruments: **0.52-0.87 pp/pp on U56, 0.01-0.94 on B136**, i.e. every one of them costs roughly
two-thirds of a point of CAGR per point of drawdown. At its own published depth of 3.12pp vol20
ranks 1 of 3 on U56 (0.662 < SLEEVE 0.710 < DEGROSS 0.786) — but the ranking is **not stable in
depth**: vol20 is rank 2 at 1, 2, 4 and 5pp on U56 and rank 1/3/1/1/3/3 across the six reachable
B136 depths, on a curve that moves 0.20 pp/pp between adjacent grid depths against a 0.048 pp/pp
margin. **The CAGR-price ordering of this menu is not a reportable quantity.**

## 2. On the Sharpe axis the menu separates completely, and vol20 is last

Sharpe surrendered per pp of MaxDD bought (negative = the instrument *raises* Sharpe while cutting
drawdown), interpolated onto the common depth grid:

| depth (pp) | BAND | DEGROSS | SLEEVE | VOL20 |
|---|---|---|---|---|
| U56 1.00 | -0.0109 | +0.0001 | -0.0098 | **+0.0174** |
| U56 2.00 | +0.0039 | +0.0001 | -0.0098 | **+0.0233** |
| U56 3.00 | — | +0.0001 | -0.0097 | **+0.0171** |
| U56 **3.12** | — | +0.0001 | -0.0097 | **+0.0183** |
| U56 4.00 | — | +0.0001 | -0.0096 | **+0.0111** |
| U56 5.00 | — | +0.0001 | -0.0094 | **+0.0121** |
| U56 6.00 / 8.00 | — | +0.0001 | -0.0088 / -0.0069 | unreachable |
| B136 2.00-6.00 | — | +0.0004 | -0.0082 .. -0.0088 | +0.0077 .. +0.0297 |

**`DEGROSS` is Sharpe-neutral by construction (+0.0001/pp): scaling a book does not change its
Sharpe.** That makes it the honest null, and it is the bar vol20 has to clear. It does not:
vol20's Sharpe price is **positive in 10 of the 11 reachable matched depths across both panels**,
and it ranks **last or next-to-last at every depth on both panels**. The sleeve is the only
instrument with a negative Sharpe price, at **16 of 16** reachable depths on both panels.

Head to head at idea 56's own 3.12pp on U56 (matched-gross control, ideas 135/244):

| at 3.12pp of MaxDD bought | CAGR | Sharpe | realised gross |
|---|---|---|---|
| VOL20 | 13.34% | 1.1197 | 0.7446 |
| DEGROSS (the null) | 12.95% | **1.1764** | 0.6297 |
| SLEEVE | 13.19% | **1.2071** | 0.7470 |

vol20 buys 0.39pp more CAGR than doing nothing but scaling down, and pays **0.057 of Sharpe** for
it. The sleeve is 0.15pp of CAGR behind vol20 and **0.087 of Sharpe ahead**.

## 3. The two conditional instruments buy almost nothing in-sample

Maximum MaxDD reduction each ladder can reach, IS (2009-2016) vs full sample:

| instrument | U56 IS | U56 full | B136 IS | B136 full |
|---|---|---|---|---|
| DEGROSS | 7.59pp | 14.53pp | 9.08pp | 16.32pp |
| SLEEVE | 5.30pp | 10.48pp | 5.63pp | 12.38pp |
| VOL20 | **0.48pp** | 5.73pp | **2.53pp** | 7.63pp |
| BAND | **0.05pp** | 2.18pp | **0.03pp** | 1.85pp |

Full-sample dDD equals OOS dDD to the digit for **every** instrument on **both** panels: this
book's max drawdown is set entirely by 2020 and 2022, both inside the OOS window. The
unconditional instruments (`DEGROSS`, `SLEEVE`) cut drawdown in every window because they always
hold less risk; the conditional ones (`VOL20`, `BAND`) only pay in the crashes that happen to sit
in the window you measure. This is idea 257's warning arriving from a new direction, and it is
mechanical, not statistical: **a conditional drawdown instrument cannot be priced on a window
whose crashes it did not have to survive.**

Consequence: `BAND` has a **reachability ceiling** (idea 237's construction) — no band setting on
this book buys more than **2.18pp** (U56) / **1.85pp** (B136). Beyond that depth the band is not
an available instrument at all, which is why it is blank in most of the table above rather than
expensive.

## 4. Rule 8 walk-forward

(instrument, level) chosen on <= 2016 by cheapest IS price among points with IS dDD >= 3.0pp
(pre-registered); 2017-2026 read once.

The IS-eligible pool is **9 of 39 points on U56 and 11 of 39 on B136, and contains zero `VOL20`
and zero `BAND` points on either panel** — a direct consequence of section 3, not a screen choice.

| panel | IS pick | OOS CAGR | OOS Sharpe | OOS MaxDD |
|---|---|---|---|---|
| U56 | `SLEEVE(0.30)` | 12.71% | **1.2398** | -15.96% |
| U56 | anchor `VOL20(0.60)` | 14.56% | 1.1446 | -18.15% |
| U56 | do-nothing B0 | 16.50% | 1.1700 | -21.27% |
| U56 | best OOS point `SLEEVE(0.60)` | 8.86% | 1.2938 | -10.80% |
| U56 | RULES v2 (live) | 9.56% | 1.2937 | -11.90% |
| U56 | SPY | 15.45% | 0.8820 | -33.72% |
| B136 | `SLEEVE(0.40)` | 10.50% | **1.0400** | -15.46% |
| B136 | anchor `VOL20(0.60)` | 12.25% | 0.8695 | -20.70% |
| B136 | do-nothing B0 | 14.78% | 0.9354 | -24.00% |
| B136 | best OOS point `SLEEVE(0.60)` | 8.27% | 1.1075 | -11.62% |
| B136 | RULES v2 (live) | 7.98% | 1.1206 | -12.18% |

Edge over do-nothing **+0.0699 / +0.1046 of OOS Sharpe**, over the anchor **+0.0952 / +0.1705**,
regret against the best OOS point **-0.054 / -0.068**. This is one of the rare instances in the
record where an IS chooser beats doing nothing — and the reason is legible: it is choosing on a
**drawdown price**, not on IS Sharpe, which is exactly what idea 163 asked for. It costs 3.79pp
(U56) / 4.28pp (B136) of OOS CAGR to buy 5.31pp / 8.54pp of OOS drawdown. IS->OOS price drift
0.951 -> 0.501 pp/pp on B136 and 1.035 -> 0.714 on U56: the purchase is *cheaper* out of sample,
for the same window reason.

## 5. Both KEEP paths

**4a: 0 of 80.** The live RULES v2 (U56 1.2127 Sharpe / -11.90% DD; B136 1.1206 / -12.18%) is
unbeaten by every point of every ladder — the familiar 4a pathology on a low-drawdown live book.

**4b: 30 of 80** (U56 24/40, B136 6/40). First-failing bar over the 50 failures: DD 27, CAGR 16,
H2 7. Six arms pass 4b on **both** panels:

| arm | U56 CAGR / Sharpe / MaxDD / OOS Sh | B136 CAGR / Sharpe / MaxDD / OOS Sh |
|---|---|---|
| `SLEEVE(0.30)` | 11.64% / **1.2259** / -15.96% / **1.2398** | 11.36% / **1.0526** / -17.62% / **1.0080** |
| `SLEEVE(0.25)` | 12.27% / 1.2188 / -16.85% / 1.2271 | 11.96% / 1.0424 / -18.71% / 0.9935 |
| `SLEEVE(0.20)` | 12.90% / 1.2109 / -17.75% / 1.2147 | 12.55% / 1.0323 / -19.78% / 0.9800 |
| `VOL20(0.70)` | 14.10% / 1.1319 / -18.98% / 1.1588 | 14.04% / 0.9875 / -20.05% / 0.9523 |
| `DEGROSS(0.80)` | 12.29% / 1.1763 / -17.29% / 1.1694 | 11.94% / 0.9945 / -19.56% / 0.9337 |
| `DEGROSS(0.75)` | 11.51% / 1.1762 / -16.27% / 1.1693 | 11.19% / 0.9941 / -18.43% / 0.9333 |

Two readings, both worth recording:

1. **`DEGROSS` passes 4b on both panels.** A book with no information in it beyond "hold the
   top-20 composite, scaled down 20-25%" clears every 4b bar on two large-cap panels. That is a
   fact about the bar, not about the book, and it belongs beside idea 253's finding that random
   k=80 sub-panels clear 4b at a 46% base rate.
2. **`SLEEVE(0.20-0.30)` is a three-wide plateau that passes 4b on both panels and is the rule-8
   pick on both** (f=0.30 on U56, f=0.40 on B136 — adjacent rungs). It dominates the standing
   MA200-only 4b candidate (U56 14.4% / 1.158 / -19.1%, OOS 1.181, which **fails** 4b on B136 on
   the DD cap) on Sharpe (+0.068), MaxDD (+3.1pp), OOS Sharpe (+0.059) and on passing the second
   panel at all — at the cost of 2.8pp of CAGR.

   **This is not new.** Idea 100 already published the S4 sleeve re-grossed to g=1.00 clearing 4b
   on both universes (u56 11.8% / 1.149 / -14.2%; broad 12.2% / 1.063 / -15.6%) and it was PARKed
   on the ground that 2009-2021 is a falling-rate regime and TLT carries the sleeve (idea 102).
   This run reproduces that result on a different equity book and does **not** re-test the rate
   caveat. **PARK, not KEEP** — the memo beside this file is evidence for Sunday review, not a
   proposal.

## Caveats

- B136 is `universe_broad.json`, current constituents: survivorship-biased (PROTOCOL rule 9).
- The S4 sleeve assets stay inside B0's own selectable set (they are members of both panels), so a
  small part of the sleeve's benefit is double-counted exposure; the effect is bounded by the
  four names' share of a 20-name book and is not isolated here.
- The sleeve's whole record rests on a falling-rate sample. Idea 102's deletion test is the
  binding open question and this run does not answer it.
- Depth interpolation is linear along each ladder sorted by realised dDD. `VOL20` on B136 is
  non-monotone in its own dial, so its interpolated curve is multivalued there and its per-depth
  rank should not be read as a measurement — which is itself the point of section 1.
