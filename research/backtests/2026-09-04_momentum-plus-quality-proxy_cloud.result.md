# Idea 21 — momentum-plus-quality-proxy — **KILL** (cloud, 2026-09-04)

Script `2026-09-04_momentum-plus-quality-proxy_cloud.py`, console
`…_cloud.console.txt`, all 312 grid points in `…_cloud.grid.csv`.

## The question, and the honest control

Queue wording: *"among top-10 momentum in broad universe, drop the 3 highest-vol names
(vol as quality proxy)."* Book = RULES v1's gate (200d MA + `vol20 < 0.60`), rank by 12-1
momentum, take top `K`, drop `D = round(d·K)` names by `vol20`, equal weight, 0.75 gross,
weekly, next-day execution.

Two tuned parameters and no more: `K ∈ {10,20,30}`, `d ∈ {0,0.1,0.2,0.3,0.5}`. Three arms,
of which only the first is the idea:

| arm | what it does | role |
|---|---|---|
| **HI** | drop the `D` **highest**-vol20 names of the top K | the idea under test |
| **LO** | drop the `D` **lowest**-vol20 names | SIGN CHECK |
| **CTRL** | no vol screen; rank-cap at `K−D` names | **the control the idea needs** |

CTRL matters because a vol screen that removes 3 of 10 names also *shrinks the book*, and
holding fewer names is a separate (already-studied) lever. HI must beat CTRL, not merely beat
`K`, or the only content is position count. Both gross conventions are reported (`g/count`
MATCHED and `g/K` LITERAL) because idea 73 showed the naive `g/K` denominator turns a drop
into a hidden de-grossing.

Universes: `universe_broad.json` (136, PRIMARY — the queue item says "broad") and
`universe.json` (56, portability). Costs 10 and 25 bps.

## Result: the screen loses on every axis, and the walk-forward refuses to buy it

**HI beats CTRL on Sharpe in 1 of 24 cells across the two universes** (broad 1/12, mean
−0.127; u56 0/12, mean −0.156). **HI beats the reversed screen LO in 2 of 24** (means −0.096
/ −0.103). The loss is monotone in `d` on both universes and both rankers.

The queue's literal proposal, broad, MATCHED gross, 10 bps:

| book | CAGR | Sharpe | MaxDD | H1 / H2 | OOS Sh | 4b |
|---|---|---|---|---|---|---|
| K=10, no drop (anchor) | 18.7% | 1.077 | −21.4% | 1.284 / 0.919 | 0.996 | fail (DD) |
| **K=10, drop 3 highest-vol (the idea)** | **14.8%** | **0.926** | −19.2% | 1.133 / 0.768 | 0.865 | fail (H2, OOS) |
| K=10, drop 3 **lowest**-vol (sign check) | 21.1% | 1.070 | −25.5% | 1.385 / 0.822 | 0.911 | fail (H2, DD) |
| K=7 momentum, no screen (CTRL) | 18.6% | 0.994 | −23.2% | 1.258 / 0.794 | 0.859 | fail (H2,OOS,DD) |
| SPY | 15.3% | 0.890 | −33.7% | 0.957 / 0.837 | 0.884 | — |

Priced on idea 74's axis the screen buys drawdown expensively: **1.77 pp of CAGR per pp of
MaxDD** against the no-drop K=10 anchor (−3.9pp CAGR for +2.2pp MaxDD) and **0.95 pp/pp**
against the matched-size CTRL (−3.8pp for +4.0pp). Both are worse than the static gross lever
(0.57, idea 22) and the second is at best level with the book-level DD control (1.02) that
idea 22 already KILLed — and unlike gross it also costs 0.07–0.15 of Sharpe.

**Walk-forward (rule 8) picks `d = 0` — no screen at all — on BOTH universes.** IS Sharpe is
monotone decreasing in `d` at every `K`: broad K=10 reads 1.204 / 1.161 / 1.092 / 1.024 /
0.863 for d = 0 / 0.1 / 0.2 / 0.3 / 0.5; u56 K=20 reads 1.049 / 0.948 / 0.874 / 0.847 / 0.725.
The IS Sharpe spread is 0.546 (broad) and 0.400 (u56), so the grid is amply selectable under
idea 88's 8a pre-test and the selection is not a coin flip. At the selected d=0 the three arms
are identical by construction; OOS 2017-26 reads broad 18.3% / 0.996 / −21.4% and u56 12.9% /
1.016 / −18.8%, against RULES v1 6.0% / 0.581 and 7.8% / 0.751 and SPY 15.5% / 0.884 / −33.7%.

**Zero 4b passes among the HI arms with `d > 0` at 10 bps on the primary universe** (1/39 on
the whole broad MATCHED grid, and that one is the `d = 0` no-screen anchor). Nothing survives
25 bps anywhere.

**Robustness (composite ranker instead of raw 12-1):** identical conclusion. Broad, K=10:
HI Sharpe 0.895 → 0.890 → 0.798 → 0.718 → 0.537 as d rises; CTRL stays 0.88–0.93; LO stays
0.88–0.92. Ranker choice is not what is driving the loss.

## The sign check says the tilt is backwards, not merely useless

LO — dropping the *lowest*-vol names — **raises CAGR against CTRL in 9 of 12 u56 cells and 7
of 12 broad cells** (u56 mean +0.12pp, positive in all four K=30 cells) while HI lowers it in
23 of 24 (+0.12pp in one cell, −1.4pp to −10.3pp in the other 23). That reproduces idea 80/81's Fama-MacBeth result — the
short-horizon vol premium *inside* the eligibility gate is positive-signed (slope +0.0045,
t +3.90 on u56; +0.0029, t +3.19 on broad) — with a completely different instrument. RULES v1's
`/sqrt(vol20)` scaler, already killed by idea 1, and idea 21's hard drop are the same wrong-way
tilt in smooth and blunt form. LO does not itself pass 4b (it fails on drawdown almost
everywhere: −22% to −33% MaxDD), so this is a KILL of idea 21, not a KEEP of its mirror.

## By-product: the `g/K` denominator manufactures 4a passes

The LITERAL convention (`w = g/K`, keeping the dropped names' weight in cash) reproduces idea
73's artefact exactly. At broad K=10 d=0.3 realised gross falls 0.750 → 0.522, MaxDD improves
−23.2% → −13.6%, and **4a passes on the broad grid go from 18/39 (MATCHED) to 30/39 (LITERAL)**
while Sharpe is unchanged to 3 decimals (0.926 vs 0.924). Every one of those extra "passes" is
the drawdown of a 52%-invested book being compared to a 75%-invested baseline. Any future
screen-style idea must be reported at matched gross or its 4a column is meaningless.

## Verdict

**KILL.** Loses to its own matched-size control in 23 of 24 cells, loses to the reversed
screen in 22 of 24, is monotone-decreasing in the screen's own strength on two universes and
two rankers, and rule 8 sets the parameter to zero on both universes. Recommended RULES
wording: **none** — and this is the third independent refutation (ideas 1, 80/81, 21) of a
low-vol tilt inside this gate. Suggest PROTOCOL stop re-queuing vol-as-quality variants
without a new mechanism.

## Caveats

- **Survivorship.** Both panels are current-constituent lists, so all CAGR levels are
  optimistic. The bias is *signed against the conclusion here*: a survivor panel is missing the
  high-vol names that did not survive, which flatters LO and understates HI. HI still loses by
  a wide margin, so the KILL is if anything conservative.
- One-lever caveat: only a `vol20` screen was tested. "Quality" in the accounting sense
  (accruals, profitability, leverage) is not price-only and is out of scope for the sandbox.
