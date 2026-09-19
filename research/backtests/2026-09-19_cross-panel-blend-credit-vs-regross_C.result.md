# Idea 1649 (lane C, 2026-09-19) — is any CROSS-PANEL BLEND CREDIT a RE-GROSS in disguise?

**VERDICT: KILL for the cross-panel NAV split, and a documented caution for ideas 1645 / 1653.**
Their premise — that a NAV split between the U56 book and the SMALL book at CONSTANT TOTAL TARGET
gross "only moves capital" and so can raise CAGR without buying drawdown — is **false**. The split
moves REALISED exposure, and the blend's entire drawdown gain is that exposure move.

Dials: **w (NAV share to U56) {0.00, 0.25, 0.50, 0.75, 1.00} x G (total target gross) {0.50, 0.75,
1.00}** — 15 cells, two tuned parameters, no more. Not dials, all published: SLICE {FULL, IS, OOS}
x COST {0, 10, 25, 50} bps = 180 rows. Book: live RULES v2 band 0.03 on each panel, weekly, t+1,
gated-out weight to 0%-yielding cash. Tape: 4203 rows, 2010-01-04..2026-09-18 (16.7y), the days both
panels price. **20 of 20 gates pass**, including a bit-for-bit replay of `baseline.rules_v2_weights`
by the (w = 1.00, G = 0.75) cell.

## Q0 — the premise of the idea HOLDS, and it is the whole story

In-band share of priced names: **U56 0.7051, SMALL 0.5482**. Realised mean gross at the same target
0.75: **U56 0.5293, SMALL 0.4113** (gap 0.1180). So routing NAV to SMALL at constant TARGET gross
**lowers realised exposure** — exactly the confound 1649 was filed to catch.

## G11 — which axes a re-gross can even touch (measured, not assumed)

Scaling a corner to 90% / 75% / 50% of its own realised gross moves CAGR (−0.4 to −4.1 pp/yr) and
MaxDD (+1.2 to +6.9 pp) and leaves **Sharpe fixed to |dSharpe| <= 0.0004** over all six cells (cash
yields 0%, so a constant scaler is Sharpe-neutral by construction). **Sharpe contrasts are therefore
re-gross-immune; the re-gross component can only live on CAGR and MaxDD.** Any future blend claim
quoting a drawdown number must be matched on realised gross before it is believed.

## Q1 vs Q2 — the drawdown credit is MORE than 100% re-gross

Nine blend cells (w interior), against the U56 corner, at the binding 10 bps:

| slice | raw dMaxDD (vs corner at matched TARGET gross) | matched dMaxDD (vs corner at the blend's OWN realised gross) | re-gross share |
|---|---|---|---|
| FULL | **+1.02 pp shallower** | **−0.28 pp DEEPER** | +127.6% |
| OOS  | **+1.02 pp shallower** | **−0.60 pp DEEPER** | +158.5% |

The headline a NAV-split proponent would quote (+1.02 pp of drawdown) **reverses sign** once the
corner is de-grossed to the blend's own exposure. On CAGR the blend loses either way: raw −1.93 pp/yr
FULL / −2.92 pp OOS, matched −1.02 / −1.59, i.e. **~47% of the CAGR loss is the de-gross and the rest
is the real cost of holding SMALL names**. On Sharpe the blend beats the U56 corner in **0 of 9 cells
at every cost rung on FULL and OOS** (mean −0.193 FULL, −0.292 OOS), matched and raw alike.

## The mixture is convex — against the wrong benchmark

Blend Sharpe exceeds the NAV-weighted average of its two corner Sharpes in **27 of 27 cells** (mean
**+0.0535**): real diversification. But against the **better** corner it is positive in only **3 of
27**, all three IS-only at w = 0.75 (+0.0049), and all three flip to **−0.1067 OOS**. A credit that
exists only against the worse corner is not a reason to move capital.

## Q3 + rule 8

**4a: 0 of 15 cells on both windows. 4b: 1 of 15** — and it is **w = 1.00, G = 1.00**, the pure U56
corner at full gross, i.e. no blend at all (its "matched twin" is itself, so that row is a tautology
and is not evidence). **0 of 9 blend cells clear either path.** Choosers fit on 2010-2016 only:
**C_SHARPE picks w = 0.75, G = 1.00** (IS Sharpe 0.9642) → OOS **10.68% / 1.1678 / −14.72%** against
LIVE RULES v2 **9.44% / 1.2752 / −12.07%** and SPY **15.26% / 0.8738 / −33.72%**: neither path, and
**−0.1068 Sharpe OOS against its own IS-fitted de-gross twin**. C_MEMO and C_LIVE both stay at the
live corner. **Reaching for a blend on IS rows is negative-value OOS.**

## The sharpest cell

At w = 0.75, G = 1.00 (the chooser's pick), the matched de-gross twin — the U56 book alone at target
0.944, realised gross 0.6663, the blend's own — **clears 4b on FULL and OOS where the blend fails the
CAGR floor**: twin Sharpe 1.1620 / MaxDD −15.08% FULL and 1.2747 / −14.88% OOS, against the blend's
1.0938 / −14.72% and 1.1678 / −14.72%. The blend buys **+0.36 pp** of drawdown FULL (+0.15 pp OOS)
for **−0.69 pp/yr** of CAGR (−1.09 pp OOS) and **−0.068** Sharpe (−0.107 OOS). De-grossing the live
book dominates the split on every axis that matters.

## Incidental, labelled as such

(w = 1.00, G = 1.00) — the live RULES v2 book at gross 1.00 rather than 0.75 — clears 4b on FULL
(10.87% / 1.1620 / −15.94%) and OOS (12.65% / 1.2745 / −15.94%), fixing the CAGR floor the live book
fails at G = 0.75 (8.13% against a 9.81% floor). This is a GROSS claim on the existing book, already
swept by idea 1498, not a product of this idea's blend dial, and **no legal IS-only chooser here
reaches it** (C_SHARPE takes w = 0.75, C_MEMO the live corner). It is reported, not proposed.

## Survivorship (rule 9)

U56 is a current-constituent list and SMALL a current sub-$2B screen carried back to 2010, so every
ABSOLUTE level above is an upper bound. The headline is a blend-minus-twin contrast inside one tape,
same names, same days, same realised exposure, so it is first-order immune; the 4b pass counts are not.
