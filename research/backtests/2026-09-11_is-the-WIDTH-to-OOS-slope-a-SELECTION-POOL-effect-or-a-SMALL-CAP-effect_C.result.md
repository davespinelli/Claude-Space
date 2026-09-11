# Idea 694 — is-the-WIDTH-to-OOS-slope-a-SELECTION-POOL-effect-or-a-SMALL-CAP-effect
lane C, 2026-09-11 · `2026-09-11_is-the-WIDTH-to-OOS-slope-a-SELECTION-POOL-effect-or-a-SMALL-CAP-effect_C.py`

**SPLIT ANSWER: MOSTLY NEITHER AS POSED — the published width→OOS slope is ~3/4 SELECTION RATIO,
and the cap-mix channel the queue offered as the alternative is REAL and ~6x bigger than the part
of width that survives. Plus one PARK. No RULES change, no book promoted, no KEEP claimed;
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py untouched.**

## Gates (all asserted before any new number was read)
* **GATE 0 — reproduction.** 240 book rows against idea 688's committed `.books.csv` and 50 against
  idea 525's, on nine quantities each (CAGR/Sharpe/MaxDD/H1/H2/OOS_CAGR/OOS_Sharpe/OOS_MaxDD/
  IS_Sharpe): worst |Δ| **2.220e-16**, 0 of 2,610 comparisons above 1e-9.
* **GATE 0c — the headline this run decomposes.** Spearman(k, OOS Sharpe) over the 288 fixed-n rows
  re-measured from scratch = **+0.5269** (published +0.5269) and the six means
  **0.2516 → 0.2729 → 0.3232 → 0.3725 → 0.4257 → 0.4849**, identical to idea 688's to 4 dp.
* **GATE 1 — envelope:** all 58 panels exact width, exact cap mix, no duplicate columns, inside the
  pool bounds. **GATE 2 — ratio identity:** worst |n/k − r| over the 24 ARM-B cells = **0.0000**.

## The design (2 tuned params, every cell reported)
One panel set, two paths through the (k, n) plane, plus a cap leg.
`r = n/k ∈ {0.05, 0.10, 0.25, 0.50}` × `k ∈ {40, 60, 80, 100, 200, 400}`, q = 1.00 (pure SMALL439,
8 draws, idea 688's own ladder rebuilt by importing its `build_ladder`), against the record's
**ARM A** (fixed `n ∈ {5,10,15,20,30}`). Cap leg: **k = 100 fixed**, `q ∈ {0, 0.25, 0.5, 0.75, 1.0}`
(lane B's own cells replayed from seed 2026; q=0.00 dedupes to 1 panel because k=100 at q=0 **is**
the whole BSTK100 pool). 58 panels, 480 book rows, 10 bps, weekly, next-day, GROSS 0.75.

## 1. The width slope does not survive at a fixed selection ratio

| | ρ(k, OOS Sharpe) per level | mean | positive |
|---|---|---|---|
| **ARM A** fixed n = 5/10/15/20/30 | +0.4015 / +0.5988 / +0.6525 / +0.6727 / +0.6842 | **+0.6020** | 5/5 |
| **ARM B** fixed r = .05/.10/.25/.50 | +0.3329 / +0.4244 / +0.2342 / **−0.0343** | **+0.2393** | 3/4 |
| EWall (r = breadth, not fixed) | — | +0.1920 | — |

**SURVIVAL = B/A = +0.3975 → MIXED** on the pre-registered bar (POOL-DEPTH needed ≥0.60 and
B ≥ +0.30; SELECTIVITY ARTEFACT needed ≤0.25 or |B| ≤ 0.15). In **Sharpe units** the collapse is
sharper than the rank statistic: the k = 40 → 400 lift is **+0.108 / +0.317 / +0.301 / +0.325 /
+0.305** across ARM A (mean **+0.271**) and **+0.130 / +0.078 / +0.063 / +0.028** across ARM B
(mean **+0.074**) — **27.5% of the level effect survives; 72.5% of it is the selection ratio.**

The other axis carries it, and increasingly so with width: within-k ρ(r, OOS Sharpe) =
**−0.3693 / −0.1393 / −0.3724 / −0.4632 / −0.8325 / −0.9415** at k = 40…400. A standardised rank
regression over all 352 q=1.00 CAND rows with both coordinates free gives
**β(log k) +0.2501 vs β(log r) −0.4462** (R² 0.3338) — the ratio loads **1.78×** the width.
ρ(k, breadth) is **−0.1356** over the 48 panels (breadth 0.2717…0.3657), so on this ladder n/k and
n/n_elig are the same dial up to that spread; the finding is not an n_elig artefact.

**So idea 688's stated mechanism is 3/4 wrong as stated.** "A CAND-n book at fixed n selects from a
bigger pool" is true, but what pays is the *selectivity* that buys, not the pool. Hold n/k fixed and
a 10× panel is worth ~+0.07 of OOS Sharpe; at r = 0.50 it is worth **nothing** (−0.0343).

## 2. The cap-mix channel is real, and it is the bigger one

At **matched width (k=100) and matched ratio**, within-r ρ(q, OOS Sharpe) =
**−0.5980 / −0.6458 / −0.9144 / −0.9253** (r = .05/.10/.25/.50); **CAP = −0.7709**
(fixed-n version −0.7606) → **REAL CAP CHANNEL** on the pre-registered bar (|CAP| ≥ 0.30).
Mean OOS Sharpe from q = 0 → 1: **0.8067→0.4345** (r=.05), **0.7725→0.4201** (r=.10),
**0.9424→0.3062** (r=.25), **1.0778→0.2248** (r=.50). The largest cap move, **−0.853**, is
**6.6× the largest surviving width move (+0.130)** measured on the same books and the same tape.

That reconciles ideas 688 and 685 without either being wrong: 685's wide end loses because its wide
panels are *forced* small-cap-heavy (only q ≥ 0.75 reaches k = 400); 688's wide end wins because at
q = 1.00 cap mix cannot move and the fixed-n book gets more selective as k grows. Neither ladder was
measuring width.

**Caveats, stated not buried.** The cap leg has 1/3/3/3/8 panels at q = 0/0.25/0.5/0.75/1.00 — the
q = 0.00 cell is one deterministic panel, not a draw. The q slope is a *level* statement about
2010–2026 (US large caps beat this small-cap screen over the OOS window); it is not a portable rule.
**SURVIVORSHIP** (idea 54, `data/SMALL_PANEL_README.md`): SMALL439 and BSTK100 are current
constituents, so every level is optimistic — most of all at the small end, which makes the measured
small-cap penalty the **conservative** reading of the cap channel.

## 3. Rule 8 (PROTOCOL 8) — dials fitted on ..2016-12-31 only, read once on 2017-01-01..
14 selectors × 8 draws. **SPY OOS: CAGR 15.45%, Sharpe 0.8820, MaxDD −33.72%. RULES v2 on the same
panels: CAGR 3.77%, Sharpe 0.5310, MaxDD −15.44%.**

| selector | OOS CAGR | OOS Sharpe | OOS MaxDD | anchor | beats anchor | beats v2 | beats SPY |
|---|---|---|---|---|---|---|---|
| PICK-n @k=400 (best) | 9.88% | **0.5758** | −28.07% | 0.5234 | 8/8 | 4/8 | **0/8** |
| PICK-n @k=200 | 6.77% | 0.4613 | −28.37% | 0.4504 | 6/8 | 1/8 | 0/8 |
| PICK-(k,n) joint | 4.22% | 0.3166 | −38.54% | 0.3702 | 5/8 | 0/8 | 0/8 |
| PICK-(k,r) joint | 3.34% | 0.2821 | −34.10% | 0.3385 | 4/8 | 0/8 | 0/8 |
| PICK-r @k=400 (worst) | 1.63% | 0.2266 | −19.08% | 0.3842 | 0/8 | 0/8 | 0/8 |

**Every one of the 14 selectors loses to SPY on 8 of 8 draws.** Choosing the *ratio* on IS is worse
than not choosing: PICK-r beats its own choice-set anchor at 1 of 6 widths (k=60, +0.0239) and costs
−0.1576 at k = 400. With r free, the joint selector no longer pins to the widest panel (k picked:
40×1, 80×1, 100×4, 200×1, 400×1) — idea 688's width-pin is a fixed-n artefact too — but it still
loses to the do-nothing anchor (−0.0564).

## 4. KEEP paths (4a vs RULES v2, 4b vs SPY, every book row)
**4a: 0 of 480.** **4b: 7 of 480**, and the concentration is the point: **all 7 sit at k = 100 with
q ≤ 0.25; 0 of 352 q = 1.00 rows pass at any width** — the record's q-dependence (ideas 276/285/525)
reproduced on a third construction. By width: 0/64, 0/64, 0/72, 0/64, 0/64, 0/72 — width buys no
4b pass anywhere. 2 of the 7 are already committed rows in idea 525; the other 5 are CAND25/CAND50,
book sizes this run's ratio ladder added.

Best row: **CAND50 on the q=0.00 panel (= the whole BSTK100 large-cap pool)** — CAGR 11.66%,
Sharpe 1.0634, MaxDD −18.71%, halves 1.1481/0.9856, OOS 12.10% / 1.0778 / −18.71%, against SPY
14.13% / 0.8616 / −33.72% (halves 0.8907/0.8577, OOS 0.8820). **This is a PARK, not a KEEP.** The
post-hoc rule-8 read (appendix of `.console.txt`, `.capwf.csv`, computed from this run's own
`.books.csv` — no new backtest) picks n on IS alone at k=100: it beats SPY OOS on **4 of 18**
panel-draws (all q ≤ 0.25) and lands on a 4b passer on **2 of 18** (both q=0.25, n=50, OOS Sharpe
1.0199 and 1.0018). On the deterministic BSTK100 panel the IS pick is **n=15** (OOS Sharpe 0.9318,
above SPY, *not* a 4b pass) — the 4b passer there is not what an IS-honest selector takes. It is
also a de-grossing book (n = 50 against mean eligibility ~31), which the record already knows is
where its 4a/4b passes live (ideas 503/679). Queued as idea 702 for a dedicated walk-forward.

## Verdict
**SPLIT.** The queue's first candidate (**selection pool**) survives only in part — 27.5% of the
published level effect, ρ 0.2393 vs 0.6020, **MIXED** on the pre-registered bar, and **zero** at
r = 0.50. The queue's second candidate (**small cap**) is confirmed and is the larger channel:
**CAP = −0.7709** at matched width and matched ratio, up to **−0.853** of OOS Sharpe. The correct
restatement of idea 688's claim, which this run supports and idea 688's own wording does not:
*a width ladder run at fixed book size is a selectivity ladder wearing width's clothes, and any
width ladder run at mixed q is a cap ladder.* Neither ladder licenses a capital decision: 4a 0/480,
4b 7/480 with none at q = 1.00, and every rule-8 selector loses to SPY 8/8.

## Independent agreement (noted after the fact, on merge)
A cloud lane ran idea 694 in parallel, launched before either result landed on main, on its own
construction (its own ladder, its own draws, a fixed-n arm read at three cap mixes). Cross-checked
only after both finished, the two runs agree on the two headline numbers: fixed-ratio
ρ(k, OOS Sharpe) **+0.2393 (this run) vs +0.2387 (cloud)** and the cap channel
**−0.7709 (this run) vs ρ(q, OOS S | k) −0.7627 (cloud)**. Its 4b count (77/1,130) differs because
its grid is larger, but it also reports **0 of 480 at q = 1.00**, as here (0 of 352).

Artefacts: `.py .books.csv .panels.csv .grid.csv .slopes.csv .walkforward.csv .keeppaths.csv
.capwf.csv .console.txt .result.md` · runtime 1255.3s.
