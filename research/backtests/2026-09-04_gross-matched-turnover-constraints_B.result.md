# Idea 86 — gross-matched-turnover-constraints — **KILL for `budget-top`; the other three instruments survive**

Lane B, 2026-09-04. Script `2026-09-04_gross-matched-turnover-constraints_B.py`,
console `…_B.console.txt`, grid `…_B.grid.csv`, per-arm effects `…_B.effects.csv`,
survival table `…_B.survival.csv`.
**368 reported points** = 2 universes × 92 arms × 4 costs {0, 5, 10, 25} bps. All printed, none picked on
its own result. Harness reproduces `engine.backtest` to **0.000e+00** (CAND20) and **1.4e-17** (EWall).

## The pre-registered question

Idea 83 closed with an incidental finding that undercut its own headline: `budget-top` — truncate the trade
list at a per-rebalance `Σ|Δw|` cap — is **not self-financing**, so leaving sells unexecuted raises realised
exposure (0.815 gross vs the control's 0.717 on u56/CAND20). The same leak is latent in every other
turnover/holding-period instrument the project owns. So: **re-run them all with realised gross renormalised
to a common target `G* = 0.75` at each rebalance, and mark which published effects survive.**

- `gm=off` — the published form; whatever gross falls out, falls out.
- `gm=on` — identical, then rescale the post-trade vector to sum to exactly 0.75 **before turnover is
  counted**, so the matching trades are paid for at the same 10 bps as every other trade.

Instruments: `budget-top` / `budget-pro` at `B ∈ {0.10, 0.20, 0.40}` (idea 83), `hyst` at `k ∈ {1.25, 1.50,
2.00}` (idea 79, **first run here**), `cadence ∈ {D, M, Q}` vs the weekly control (idea 3). Books: `CAND20`
(idea 2's standing 4b KEEP) and `EWall` (idea 10's `B136/EWall`). Two tuned parameters: the instrument's own
knob, and `gm` — the treatment, always reported on both settings.

## Answer: one of the four instruments was measuring exposure, and it is exactly the one idea 83 flagged

Mean effect vs the same-`gm` control, 10 bps, both universes and books (positive `dMaxDD` = drawdown removed):

| family | dCAGR pp (off → on) | dSharpe (off → on) | t(dSharpe) off → on | dMaxDD pp (off → on) | dTO x/yr | mean dGross off |
|---|---|---|---|---|---|---|
| `budget-top` | **+1.53 → −5.74** | **+0.016 → −0.467** | +1.26 → −2.07 | −5.07 → −6.27 | −2.4 | **+0.043** |
| `budget-pro` | +0.51 → +0.76 | +0.012 → +0.023 | +0.57 → +0.81 | −2.36 → −3.18 | −2.6 | 0.000 |
| `cadence` | +0.36 → +0.54 | −0.012 → +0.002 | −0.18 → −0.09 | −3.43 → −3.82 | +0.0 | −0.001 |
| `hyst` | +0.52 → +0.52 | +0.041 → +0.040 | +0.93 → +0.92 | +0.41 → +0.41 | **−5.66** | 0.000 |

**Survival scoreboard: 27 of 42 instrument-cells survive** (same sign on both dCAGR and dMaxDD, and |gm=on|
≥ 50% of |gm=off| on dCAGR). All 12 non-survivals are concentrated: `budget-top` fails **1 of 12** cells,
`budget-pro0.4` and `cadenceD` account for the rest and are near-null arms (|dCAGR| < 0.2 pp, |dMaxDD| ≈ 0).

### 1. `budget-top` — **KILL. The published effect was exposure, and it has no gross-neutral form.**
`budget-top0.1` and `budget-top0.2` survive **0 of 4** cells each. The sign reverses on every one:
u56/EWall +1.60 → **−8.86** pp CAGR; broad/CAND20 +6.11 → **−1.10** pp with dGross **+0.228**. Idea 83's
"one real positive" — `EWall/budget-pro0.1` and `budget-top0.2` raising the 4b breakeven on u56 — loses its
`top` half here: `EWall/budget-top0.2` passes 4b at 10 bps with `gm=off` and **fails with `gm=on`**, as does
`CAND20/budget-top0.4`. Gross-matching adds no 4b passes anywhere.

The mechanism is worth stating because it is not a fixable implementation detail. Truncating a trade list is
not self-financing in *either* direction. From cash, a `B=0.20` budget fills ~5 of CAND20's 20 target names
and stops, leaving gross at 0.20; renormalising to 0.75 then holds those 5 names at 14% each. So
**`budget-top` has no gross-neutral form: matched on exposure it becomes a concentration lever**, which is
why u56/CAND20's `dMaxDD` goes from −2.80 pp to **−21.58 pp** once gross is matched. Its effect is
inseparable from either exposure or concentration; it is not a turnover instrument and should not be
reported as one. The worst case is not subtle: `u56/EWall/budget-top0.2` goes from **10.4% CAGR / 1.04
Sharpe / −19.2% MaxDD** at `gm=off` to **0.9% / 0.18 / −27.8%** at `gm=on` — the identical turnover cap,
with exposure held constant.

### 2. `budget-pro` — **survives, and idea 83's conclusion strengthens.**
`dGross` is 0.000 to three decimals at every arm, confirming the pro-rata form was correctly gross-preserving
and that idea 83 was right to call it the implementation control. 10 of 12 cells survive; the effect grows
slightly under gm (dCAGR +0.51 → +0.76, dMaxDD −2.36 → −3.18). Idea 83's headline — *a turnover budget sells
drawdown protection to buy return*, at ~0.22 pp CAGR per pp of MaxDD given up — is **confirmed** and, if
anything, the exchange rate is worse than published (0.76/3.18 ≈ 0.24). t(dSharpe) is +0.81; not significant.

### 3. `cadence` — **survives cleanly; idea 3's monthly finding is real turnover, not exposure.**
`dGross` ≤ 0.003 at every arm. The run replicates idea 3 to the decimal at `gm=off` (u56/CAND20 monthly−weekly
**+2.05 pp CAGR / +0.111 Sharpe, t +2.10**; broad/CAND20 **+3.24 / +0.143, t +2.52** — idea 3 published
+2.05/+0.111 and +3.24/+0.143), and under gross-matching it gets *larger*: +2.51/+0.150 (t +2.48) and
+3.63/+0.166 (t +2.83). Daily-is-strictly-worse also survives (t −2.48 to −4.85 in all four cells, both gm).
On `EWall` the two gm columns are bit-identical, as they must be — that book's target already sums to 0.75 —
which is the run's internal control on the treatment.

Monthly still buys its return with drawdown (dMaxDD −1.2 to −6.1 pp), so idea 3's PARK verdict stands
unchanged; what changes is that the effect can no longer be dismissed as an exposure artefact.

### 4. `hyst` (idea 79, first measurement) — **survives, and it is the only instrument that improves both axes.**
Keep a held name while its rank stays inside the top `k·n`; refill freed slots from the best unheld names, to
the same count the base book would have held. Changes no signal, only the exit schedule.

| universe | arm | CAGR | Sharpe | MaxDD | H1 / H2 | OOS Sharpe | TO x/yr | 4b |
|---|---|---|---|---|---|---|---|---|
| u56 | `CAND20/control` (idea 2's KEEP) | 12.7% | 1.093 | −18.3% | 1.088 / 1.103 | 1.170 | 9.63 | PASS |
| u56 | `CAND20/hyst1.25` | 12.9% | 1.119 | −17.5% | 1.106 / 1.136 | 1.211 | 5.86 | PASS |
| u56 | `CAND20/hyst1.5` | 12.9% | 1.124 | −17.5% | 1.128 / 1.127 | 1.208 | 4.76 | PASS |
| u56 | **`CAND20/hyst2`** | **12.7%** | **1.145** | **−17.2%** | **1.169 / 1.133** | **1.231** | **3.91** | **PASS** |
| broad | `CAND20/control` | 13.1% | 0.958 | −20.1% | 1.125 / 0.814 | 0.894 | 13.78 | fail (H2) |
| broad | `CAND20/hyst2` | 14.4% | 1.025 | −20.4% | 1.257 / 0.831 | 0.939 | 5.68 | fail (H2, DD) |

(SPY: u56/broad common sample 15.3% / 0.890 / −33.7%, halves 0.957/0.837, OOS 0.884. RULES v1 at 10 bps:
u56 0.67 (0.64/0.69), broad 0.64 (0.76/0.54).)

All 6 (universe, k) cells show positive dCAGR and 5 of 6 non-negative dMaxDD, with turnover cut **40–60%**.
**But the Sharpe gain is not individually significant** — t(dSharpe) runs 0.00 to +1.70 across the six cells.
The defensible claim is the narrow one: *rank hysteresis removes 40–60% of the ranked book's turnover at no
measured cost, and the point estimates lean positive on every axis in every cell.* It is `gm`-invariant to
three decimals, so this is a genuine holding-period effect. `CAND20/hyst2` at `gm=off` is a **4b
KEEP-candidate on u56** — a strict improvement on the standing candidate (idea 2's control) on Sharpe, MaxDD
and turnover simultaneously — and it fails 4b on broad on the same H2 bar the control fails, by a smaller
margin (0.831 vs SPY's 0.837, against the control's 0.814). Memo: `…_B.memo.md`.

## Walk-forward (rule 8) — gross-matching overturns 3 of 14 selections, and all three are `budget-top`
Selection fixed before any OOS number was read: highest 2009–2016 Sharpe at 10 bps within each
(universe, book, family, gm); ties → the slower arm.

| universe | book | family | gm=off pick (OOS Sh) | gm=on pick (OOS Sh) | changed |
|---|---|---|---|---|---|
| u56 | CAND20 | budget-top | `budget-top0.1` (1.154) | `budget-top0.1` (0.877) | no (OOS collapses anyway) |
| u56 | CAND20 | cadence | `cadenceM` (1.286) | `cadenceM` (1.309) | no |
| u56 | CAND20 | hyst | `hyst2` (1.231) | `hyst2` (1.188) | no |
| u56 | EWall | budget-top | `budget-top0.1` (1.065) | **`control`** (1.114) | **yes** |
| broad | CAND20 | budget-top | `budget-top0.1` (1.059) | **`control`** (0.886) | **yes** |
| broad | EWall | budget-top | `budget-top0.1` (1.076) | **`control`** (1.021) | **yes** |
| (8 others) | | budget-pro, cadence, hyst | — | — | no |

**Picks changed: 3/14, all `budget-top`, and in all three gross-matching demotes it to the do-nothing
control.** OOS references: RULES v1 7.8% / 0.751 / −13.8% (u56), 6.0% / 0.581 / −21.2% (broad); SPY 15.5% /
0.884 / −33.7%. Every rule-8 pick from `hyst` and `cadence` beats both its control and SPY out of sample on
Sharpe under **both** gm settings; every `budget-top` pick beats SPY only at `gm=off`.

## By-product: gross-normalising idea 2's standing KEEP (ideas 73/81)
The literal CAND-20 construction divides `GROSS` by the fixed `n`, so it de-grosses whenever fewer than 20
names are eligible — **11.0% of u56 days** and 2.4% of broad days, plus tie behaviour in `rank <= 20`
(the composite is a mean of three pct-ranks, so ties at the 20th place select 19 names on 414 u56 days).
Together these leave realised gross at **0.717** (u56) and **0.739** (broad) against the nominal 0.750. Fixing it (`gm=on`) costs the standing
candidate **−0.029 Sharpe** on u56 (1.093 → 1.064) and **−0.014** on broad (0.958 → 0.944), and raises
turnover 9.63 → 11.00 x/yr, because matching gross is itself a trade. It does not change any 4b verdict for
`CAND20/control` on either universe. So idea 81's fix is a small, real, *negative* correction to the standing
KEEP — not the artefact-sized one idea 73 found on narrow panels.

## Cross-universe 4b at 10 bps
24 (arm, universe) points pass 4b; **no arm passes on both universes**, including the two controls — u56's
`EWall/control` fails on CAGR, broad's `CAND20/control` on H2. This reproduces idea 83's cross-universe result
and extends it: gross-matching does not create a cross-universe passer, and it removes two of u56's.

## Caveats
Survivorship: current constituents of both lists, one-directional, and **adverse for a turnover study**
(idea 83's caveat restated) — a survivor panel never rotates out of a delisted name, so realised turnover is
an underestimate and every budget here is easier to meet than it would have been live. That bias falls hardest
on `hyst`, whose whole claim is turnover. 2020 and 2022 are the only real stress episodes in the sample. `gm`
is applied at rebalance dates only; intra-period drift in gross is untouched in both arms. No RULES.md,
scan.py, bot.py or baseline.py was modified.
