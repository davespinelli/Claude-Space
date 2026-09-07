# Idea 105 — is-it-gold-or-any-real-asset (cloud, 2026-09-07)

**VERDICT: SPLIT — H_METALS and H_REAL are both KILLED; H_GOLD survives only in
re-specified form. One PARK candidate (`GLD+UUP`), with its blocker named.**

The queue's three hypotheses do not survive contact with the substitution test. It is **not**
a precious-metals factor: silver retains 36% of the sleeve's dSharpe, gold miners 6.5%, and
run *alone* both are actively destructive (SLVonly **−0.340**, GDXonly **−0.381**, negative in
8/8 cells). It is **not** any non-dollar real asset: oil retains 4.9%, energy equity 10.0%,
broad commodity 29.6%. But it is not simply "gold" either — **gold alone is worth +0.0102
dSharpe and is positive in only 4 of 8 cells.** The exposure is a **two-leg interaction**:
`GLD+UUP` delivers **+0.1604, positive 8/8, which is 99.1% of the three-asset arm's +0.1630**.
Gold does nothing without the dollar leg; the dollar leg does nothing without gold
(UUPonly **+0.0094**); together they reproduce the whole sleeve and make TLT redundant.

Script: `2026-09-07_is-it-gold-or-any-real-asset_cloud.py` · console `.console.txt` ·
640-point grid `.grid.csv` · `.assets.csv` · `.substitution.csv` · `.mechanism.csv` ·
`.walkforward.csv` · `.keeppaths.csv` · `.costladder.csv` · PARK memo `_PARK_MEMO.md`.

**Tuned parameters: 2** — sleeve composition (16 arms) × f ∈ {0, .25, **.50** (the queue's
pre-registered headline), .75, 1.00}. Books {top20, ewall}, universes {u56, broad},
conventions {natural, g=1.00} and the 0/5/10/15/20/25 bps ladder are reported controls, never
selected on. Cadence W, gross 0.75, 60d vol, (252,126,63) lags, next-day execution, 10 bps
headline — all at incumbent values. All 640 points written to `.grid.csv`.

**DATA DEVIATION:** the queue asked for GLD swapped for **SLV/IAU**. **IAU is in neither
cached panel** and the sandbox has no network, so its arm cannot be run. IAU is a
same-underlying gold ETF, so it would have been a redundancy check; the metals question is
instead carried by **SLV** (a different precious metal) and **GDX** (gold-mining equity),
which is a stronger test. Broad real assets: DBC, USO, XLE, TIP.

**Survivorship:** both panels are current constituents, so equity levels are biased up. Every
sleeve asset is an ETF and is not exposed to it; the bias hits all 16 arms identically.

## Reproduction gates — exact

| gate | result |
|---|---|
| cost linearity vs a direct 10 bps run | max abs err **0.000e+00** PASS |
| idea 100 u56 `top20 + 50% S4` @ g=1.00 | 11.8% / **1.149** / −14.2%, OOS 12.9% / **1.236** — **as published** |
| idea 100 broad, same | 12.2% / 1.063 / −15.6%, OOS 11.8% / 1.020 — **exact** |
| idea 102 u56 `top20 + 50% (TLT,GLD,UUP)` @ g=1.00 | 11.5% / **1.167** / **−13.3%**, OOS 12.3% / **1.215** — **exact** |
| idea 102 broad, same | 12.0% / 1.073 / −14.6%, OOS 11.1% / 0.985 — **exact** |

## (1) The substitution test at f = 0.50 — 8 cells, retention against idea 102's `noDBC`

| group | arm | dSharpe | pos | retention | 4b |
|---|---|---|---|---|---|
| A | `noDBC` = TLT,GLD,UUP (idea 102's best) | **+0.1630** | 8/8 | 100% | 2/8 |
| **B** | **`GLD_UUP` = GLD,UUP** | **+0.1604** | **8/8** | **99.1%** | **3/8** |
| A | `S4` = TLT,GLD,DBC,UUP (idea 100's) | +0.1225 | 8/8 | 76.0% | 2/8 |
| C | `sub_TIP` = TLT,**TIP**,UUP | +0.0920 | 8/8 | 54.9% | 0/8 |
| C | `sub_SLV` = TLT,**SLV**,UUP | +0.0619 | 8/8 | 36.2% | 1/8 |
| A/C | `noGLD` ≡ `sub_DBC` = TLT,**DBC**,UUP | +0.0488 | 8/8 | 29.6% | 2/8 |
| C | `sub_XLE` | +0.0181 | 7/8 | 10.0% | 1/8 |
| C | `sub_GDX` | +0.0149 | 6/8 | 6.5% | 1/8 |
| C | `sub_USO` | +0.0107 | 5/8 | 4.9% | 1/8 |
| B | `GLDonly` | **+0.0102** | **4/8** | 6.4% | 0/8 |
| B | `UUPonly` | +0.0094 | 6/8 | 3.9% | 2/8 |
| B2 | `SLV_UUP` | +0.0199 | 7/8 | 10.0% | 2/8 |
| B2 | `SLVonly` | **−0.3403** | **0/8** | −215% | 0/8 |
| B2 | `GDXonly` | **−0.3805** | **0/8** | −236% | 0/8 |
| B | `TLTonly` (idea 102's passenger) | −0.1177 | 0/8 | −79% | 0/8 |

Three readings follow directly:
1. **H_METALS is dead.** The best metals substitute (`sub_SLV`, 36%) is beaten by an
   **inflation-linked bond** (`sub_TIP`, 55%), and gold *miners* — the closest levered proxy
   to gold itself — retain 6.5%. Standalone, both non-gold metals are the two worst arms in
   the run. Whatever gold is doing, silver and gold equity do not do it.
2. **H_REAL is dead.** The two purest real assets (oil 4.9%, energy equity 10.0%) retain
   almost nothing, and broad commodity retains under a third. Ordering the substitutes by
   "realness" gets the answer backwards: TIP > SLV > DBC > XLE > GDX > USO.
3. **H_GOLD needs re-specifying, and H_DOLLAR is not the answer either.** Neither leg works
   alone (GLD +0.0102 at 4/8; UUP +0.0094 at 6/8) but the pair delivers 99.1% of the
   three-asset sleeve. **The exposure is a gold × dollar interaction, not a single asset.**
   TLT's marginal contribution on top of that pair is **+0.0026 dSharpe (1.6%)** — idea 102
   called TLT a passenger; it is closer to a stowaway.

## (2) Mechanism — it is book-correlation, not the asset's own Sharpe

Regressing each single-asset arm's f=0.50 dSharpe (40 points) on the two candidate drivers:

| driver | slope | R² |
|---|---|---|
| asset's own standalone Sharpe | −0.0712 | **0.0042** |
| asset's correlation to the book | **−0.5801** | **0.4263** |

The asset's own Sharpe explains **nothing** (R² 0.004); correlation to the book explains 43%.
Buy-and-hold corr(asset, book), mean over panels: **TIP 0.014 / −0.025**, TLT −0.187/−0.205,
UUP −0.170/−0.142, **GLD 0.188/0.111**, GDX 0.301/0.239, SLV 0.309/0.238, USO 0.279/0.257,
DBC 0.368/0.329, XLE 0.465/0.472. Gold is simply *the only precious metal with a low book
correlation* — silver and miners carry equity beta that gold does not. This is also why TIP is
the best substitute despite being no kind of real asset: it is the least correlated thing
available. After removing the own-Sharpe term, gold's residual is the largest positive
(**+0.192**, vs UUP +0.164, TLT +0.030, SLV −0.170, GDX −0.216).

*(Read alongside same-day idea 358, which found correlation is NOT the design variable once
the sleeve's own standalone Sharpe is controlled. There is no contradiction: 358 varied sleeve
composition along an axis that moved correlation and own-Sharpe together (corr +0.746), while
this run's single-asset axis has own-Sharpe explaining R²=0.004. The two runs jointly say
correlation matters for **which asset**, not for **how many**.)*

## (3) Rule 8 — the arm that wins out of sample is the one the selector never picks

IS 2009-2016 → OOS 2017-2026 untouched, 8 cells, both choosers (joint over arm×f, and arm at
the pre-registered f=0.50) give identical picks:

| chooser | picks | mean OOS Sharpe | OOS CAGR | OOS MaxDD | beats no-sleeve ctrl | beats SPY | mean regret |
|---|---|---|---|---|---|---|---|
| joint(arm,f) | `sub_TIP` 5/8, `noDBC` 3/8 | 1.1239 | 8.54% | −11.8% | 7/8 | 8/8 | −0.186 |
| arm @ f=0.50 | `sub_TIP` 5/8, `noDBC` 3/8 | 1.1239 | 8.54% | −11.8% | 7/8 | 8/8 | −0.186 |

**The IS selector picks `GLD_UUP` in 0 of 8 cells**, yet `GLD_UUP` has the **highest OOS
Sharpe of all 16 arms at f=0.50 (1.2651)**, ahead of `noDBC` (1.2035) and `S4` (1.1969); its
IS-preferred rival `sub_TIP` lands 9th (1.0651). Mean regret −0.186 is the price of that.
This is the blocker on the candidate below and it is stated first, not last.

## (4) KEEP paths — reported, nothing selected on them

89 of 640 points clear **4b**; **4a vs RULES v2 is 4/640** (all broad/natural). 17 arm ×
f × book × convention combinations clear 4b on **both** panels — including `UUPonly` — so a 4b
pass on this grid is weak evidence on its own: at g=1.00 and f≥0.25, *any* low-correlation
ballast re-grossed to 1.0 clears the bar. Two things do discriminate.

**Best cross-universe book: `top20 + 50% (GLD,UUP)` at g = 1.00** — 10 bps, next-day:

| | CAGR | Sharpe | MaxDD | H1 / H2 | OOS CAGR / Sharpe / MaxDD | Turn/yr | 4a | 4b |
|---|---|---|---|---|---|---|---|---|
| u56 | **12.24%** | **1.170** | −14.65% | 1.109 / **1.229** | 13.09% / **1.259** / −14.65% | 12.4× | ❌ | ✅ |
| broad | **12.67%** | 1.081 | −16.02% | 1.175 / 0.989 | 12.05% / 1.042 / −16.02% | 15.1× | ❌ | ✅ |
| *SPY* | 15.23% | 0.889 | −33.72% | 0.957 / 0.834 | 15.45% / 0.882 / −33.72% | — | | |
| *RULES v2 (live)* | 8.66% u56 / 8.03% broad | 1.206 / 1.106 | −12.05% / −12.24% | 1.226/1.191, 1.229/0.984 | 1.285 / 1.119 | | | |

**Cost reach is the discriminating statistic.** Cross-universe 4b passes by rung
(top20, g=1.00, f=0.50), out of 2 panels:

| arm | 0 | 5 | 10 | 15 | 20 | 25 bps |
|---|---|---|---|---|---|---|
| **`GLD_UUP`** | 2 | 2 | **2** | **2** | **2** | 0 |
| `S4`, `noDBC` | 2 | 2 | 2 | 2 | 0 | 0 |
| `noGLD`/`sub_DBC`, `UUPonly`, `SLV_UUP` | 2 | 2 | 2 | 0 | 0 | 0 |
| `sub_GDX`, `sub_SLV`, `sub_USO`, `sub_XLE` | 2 | 2 | 1 | 0 | 0 | 0 |
| `sub_TIP` | 2 | 2 | 0 | 0 | 0 | 0 |
| `GLDonly`, `SLVonly`, `GDXonly`, `TLTonly` | 0 | 0 | 0 | 0 | 0 | 0 |

`GLD_UUP` is **the only arm in the run holding a cross-universe 4b pass to 20 bps**, and it
dominates `S4` and `noDBC` on OOS Sharpe at every rung on both panels (u56 1.3665→1.0966 vs
S4 1.3510→1.0632 and noDBC 1.3325→1.0382). It reaches this with **one fewer asset than idea
102's arm and two fewer than idea 100's**, which is a real reduction in fitted surface.

## (5) Verdict: PARK, not KEEP — and why

`GLD_UUP` clears 4b on both panels at 10 bps, carries three independent screens (highest
retention, highest OOS Sharpe of 16 arms, longest cost reach), and simplifies the incumbent
candidate. It is **still PARK**, for one reason stated plainly:

> **Rule 8's pre-registered selector picks it in 0 of 8 cells.** It was identified from the
> full-sample and OOS tables, i.e. by looking at the answer. Adopting it now would be
> out-of-sample-informed selection — the mirror image of the in-sample overfit PROTOCOL rule 8
> exists to catch, and not obviously the less dangerous one.

Secondary blockers: (a) it is 4a-negative — 0/640 4a passes for this arm, so it does not beat
the live book on RULES v2's own terms; (b) its edge over the pure-ballast null is real but
bounded (**+0.135 u56 / +0.133 broad** Sharpe over `UUPonly` at the same f and convention),
and `UUPonly` itself clears 4b, so the grid's 4b bar is not what is carrying the claim;
(c) broad H2 is **0.989**, 0.155 above SPY's 0.834 but below 1.0, the same weak-second-half
signature ideas 101/106 flagged; (d) it is written at g=1.00, the convention lane B's idea-106
correction found flips the `noDBC` prune's sign — this arm has not been tested against that
finding. Exact RULES wording, and the conditions that would clear the blocker, are in
`_PARK_MEMO.md`.

## What this settles for the record

1. **Any RULES wording that says "macro sleeve", "multi-asset diversifier" or
   "precious-metals exposure" is now blocked.** The sleeve is two assets with an interaction:
   gold and the dollar. Silver and gold miners do not substitute; oil, energy and broad
   commodity substitute barely; the best single substitute for gold is **TIPS**.
2. **Idea 102's TLT-passenger finding is strengthened and extended.** TLT adds **+0.0026
   dSharpe (1.6%)** on top of `GLD+UUP`. DBC's deletion (idea 106) and TLT's deletion are the
   same kind of result and can be taken together.
3. **The mechanism is book-correlation, not asset quality** (R² 0.426 vs 0.004), which reduces
   "why gold" to "gold is the only low-correlation precious metal" and predicts, correctly,
   that TIP outperforms every commodity as a substitute.
