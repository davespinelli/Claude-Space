# Idea 786 — is the U56 CAGR-FLOOR GAP a DELISTING artefact?

**lane B, 2026-09-11.** Script `2026-09-11_is-the-U56-CAGR-FLOOR-GAP-a-DELISTING-artefact_B.py`.
Two tuned parameters, **every grid point reported**: **(drag model, panel)**. Drag magnitude `d`,
book share `phi`, hazard `h`, decline window `W`, terminal delisting return `L` and seed are
published ladders, not selected dials — 2,240 FLAT points + 308 HAZARD points + 30 rule-8 rows, all
in the CSVs. 10 bps, next-day execution, no shorting, gross ≤ 1.00, 260-row warm-up, SPY-free frame,
rule 8 throughout.

## ANSWER — **NO, not on the full sample.** The gap is the right SIZE for delisting and the wrong SHAPE.

Idea 787 killed the record's standing shelf against an equal-weight basket of the book's own panel
and named the binding leg: the U56 RULES v2 band book at gross 1.00 misses the 4b CAGR floor by
**−0.83 pp/yr** (−0.14 pp OOS). Its caveat 1 said the bar is the most survivorship-exposed object in
the record, so a delisting-complete panel might revive the shelf. This run bounds that, and the
bound has two halves that point opposite ways:

| window | required **bar-only** drag (phi = 0) | (h, L) pairs delivering it | verdict |
|---|---|---|---|
| full sample | **1.184 pp/yr** | h = **2.48%** at L = −30%, **1.63%** at −55%, **1.01%** at −100% | **not defensible on 55 US large caps + ETFs** |
| OOS 2017–26 | **0.205 pp/yr** | h = **0.43%** / **0.28%** / **0.17%** | **entirely inside the plausible band** |
| B136, full | **3.624 pp/yr** | h = **7.40%** / **4.90%** / **3.05%** | **not defensible at any reading** |

And the drag only helps if it is **bar-heavy**. The book trades the *same* survivorship-biased panel,
so with `phi` = the share of the bar's drag the book also eats, the closing condition is exactly
`(0.70 − phi) · d ≥ 0.83 pp`:

```
Required BAR drag d* (pp/yr) to close the floor, U56 BAND-DG g1.00 vs B_EWW10
 phi    0.0    0.2    0.4    0.5    0.6   0.7+
 full  1.184  1.657  2.762  4.143  8.285   inf
 oos   0.205  0.287  0.478  0.718  1.435   inf
```

**At phi ≥ 0.70 no delisting drag of any size closes the floor** — a drag shared evenly between bar
and book *widens* the miss (U56 d = 5 pp at phi = 1.0 takes the slack from −0.83 to **−2.25 pp**).
So the whole question reduces to one measurable number, and DRAG MODEL 2 measures it.

## The two drag models, and why only one of them is empirical

* **FLAT** charges an assumed constant drag `d` to the bar and `phi·d` to the book. Gate **G9**
  (added post-hoc, stated as such) shows `slack = slack(0) + 0.70·bar_drag − book_drag` holds to
  **1.78e-15** across all 308 HAZARD cells: the FLAT inversion is an **identity given phi**, i.e.
  DRAG MODEL 1 contributes arithmetic only.
* **HAZARD** injects synthetic delistings into the price panel and rebuilds **both** the book and the
  bar on it, so `phi` is **measured**. A current-constituent panel of N survivors over T years
  implies `N0 = N/(1−h)^T` names at the start, so `D = N0 − N` died inside the window: U56 gets
  **+11 / +24 / +41 / +85** phantoms at h = 1 / 2 / 3 / 5%, B136 **+28 / +60 / +99 / +209**. Each
  phantom clones a real donor's path, slides geometrically to `(1+L)` over its last `W` days, then
  goes NaN. The bar holds it all the way down; the 200-day band gate can exit first — that gate is
  the entire reason `phi` could be below 0.70.

## The measurement: phi is well below 0.70 — until the delisting return gets severe

Measured `phi` at g1.00 over the 116 well-conditioned cells (bar drag > 0.5 pp; at h ≤ 2% on U56 the
donor-composition noise is the size of the drag and the ratio is meaningless — two such cells show a
*negative* bar drag, which is why the denominator is screened and the seed control is published):

| panel | L = −30% | L = −55% | L = −100% | cells with phi ≥ 0.70 |
|---|---|---|---|---|
| U56 | median **0.347** | median **0.175** | median **0.645** | **7 of 20** (all at L = −100%) |
| B136 | median **0.315** | median **0.181** | median **0.652** | **2 of 20** (all at L = −100%) |

The mechanism is visible in the ordering: the gate exits on the *breach*, not on the eventual depth,
so the book's drag **saturates** while the bar's keeps growing (phi falls from 0.35 to 0.18 going
from −30% to −55%). At a **total loss** that breaks: the final collapse is large enough that even one
week inside the gate is expensive, phi jumps to **0.65** and crosses 0.70 in 7 of 20 U56 cells.

**So the delisting channel is self-limiting, and that is the finding.** You cannot make the bar
arbitrarily worse to rescue the book, because the assumption that lowers the bar most is the one the
book cannot dodge:

| panel | L = −30% | L = −55% | L = −100% |
|---|---|---|---|
| U56 CAGR floor closes at | **h = 3%** (W = 504 only), h = 5% (W ≥ 126) | **h = 2%** (all W) | **never — 0 of 20 cells, max slack −0.20 pp at bar drag 3.70 pp** |
| B136 CAGR floor closes at | **never** (best −1.08 pp at h = 5%) | h = 5% (W ≥ 63) | **never** |

U56 full-sample CAGR-floor slack (pp/yr, + = clears), L = −30%, g1.00, seed 0, **all 20 cells**:

```
 h      0.01   0.02   0.03   0.05        B136:  0.01   0.02   0.03   0.05
W=21   -0.79  -0.55  -0.30  -0.22              -2.40  -2.22  -2.12  -1.62
W=63   -0.73  -0.48  -0.12  -0.14              -2.38  -2.16  -2.00  -1.44
W=126  -0.71  -0.44  -0.06  +0.05              -2.38  -2.10  -1.89  -1.38
W=252  -0.69  -0.31  -0.00  +0.06              -2.30  -2.05  -1.77  -1.24
W=504  -0.62  -0.30  +0.03  +0.34              -2.29  -1.95  -1.67  -1.08
```

**4b passes: 23 of 308 HAZARD cells, 19 of them U56 at gross 1.00, 15 of those requiring L = −55%.
4a: 0 of 308 — the live book is not beaten on its own path under any delisting assumption.**

## Rule 8 — gross picked on IS ≤ 2016 alone, 2017–2026 read ONCE (30 rows, all reported)

The IS selector picks **gross 1.00 in 30 of 30** variants, undragged and dragged alike, so the
walk-forward adds no dial risk here.

| panel | variant | OOS CAGR | OOS Sharpe | OOS MaxDD | OOS floor slack | 4b |
|---|---|---|---|---|---|---|
| U56 | UNDRAGGED | 12.70% | 1.2827 | −15.70% | **−0.14 pp** | fail CAGR |
| U56 | HAZARD h=2% W=252 L=−30% | 12.33% | 1.2439 | −16.26% | **+0.32 pp** | fail CAGR* |
| U56 | HAZARD h=5% W=252 L=−30% | 11.18% | 1.1917 | −15.45% | **+0.81 pp** | **PASS** |
| B136 | UNDRAGGED | 10.66% | 1.1195 | −16.08% | −2.37 pp | fail H1,H2,CAGR |
| B136 | HAZARD h=5% W=252 L=−30% | 9.14% | 1.0377 | −15.13% | −0.91 pp | fail CAGR |

\* the OOS slack turns positive at h = 2% but the **full-sample** CAGR leg still binds, which is the
run's whole point: the OOS miss dies under delisting, the full-sample miss does not.

**OOS comparands:** RULES v2 live U56 **9.48% / 1.2834 / −11.90%**; SPY **15.24% / 0.8721 / −33.72%**.
The rule-8 pick **beats SPY's OOS Sharpe in 29 of 30** rows and **beats RULES v2's in 0 of 30** (the
undragged U56 pick loses by 0.0007 of Sharpe and gives up 3.8 pp of drawdown to do it). 4b 10 of 30,
4a 0 of 30.

## OOS is where the artefact reading survives

The OOS leg needs only **0.205 pp/yr** of bar-only drag — h ≈ 0.2–0.4% at any literature anchor — and
it **flips sign at every hazard rung ≥ 2%** and at h = 1% with W = 504 (−0.144 → +0.10 … +1.17 pp).
The record should treat idea 787's OOS CAGR-floor miss on U56 as **inside the survivorship
uncertainty and not a finding**. The full-sample miss is 5.8× larger and survives.

## Verdict — **ANSWERED / KILL for capital.** No KEEP, no memo, no book promoted.

The gap is not *ruled out* by magnitude: 1.18 pp/yr is squarely inside the 0.4–3.7 pp/yr of bar drag
the simulation produces at L = −30% (and up to 7.0 pp at total loss). It fails on **shape**. Closing it needs (i) a hazard of **2.5–5.8%/yr**
on a 55-name panel of US large caps and ETFs, which is a small-cap number, not a large-cap one, and
(ii) a delisting return mild enough to keep phi < 0.70 — and the two requirements fight each other,
because severity is what pushes phi up. At total loss the floor never closes on either panel at any
hazard to 5%/yr. Promoting this book would mean asserting an unobservable hazard in the direction
that happens to pay, which is the opposite of what 4b is for; PROTOCOL rule 4b names SPY, and against
SPY this book already passes (idea 787, 26 of 82). RULES.md, PROTOCOL.md, scan.py, bot.py and
baseline.py are untouched (rule 6).

## Gates (pre-registered except G9, all PASS)

| gate | value | bar |
|---|---|---|
| G1 `fast_backtest` vs `engine.backtest`, returns AND turnover, 2 books | max **2.08e-17** | 1e-12 |
| G2 `b_band_dg(0.75)` == `baseline.rules_v2_weights` (full frame) | **0.000e+00** | exact |
| G3 cost-rung identity `r(25) = r(0) − turnover·25/1e4` | **0.000e+00** | 1e-12 |
| G4 U56 `B_EWW10` == idea 787 (17.69% / 1.1237 / −29.09%) | 2.892e-05 | 5e-4 |
| G5 U56 `B_EW742` == idea 742/787 (17.94 / 1.1357 / −28.87 / OOS 18.64 / 1.1448) | 4.536e-05 | 5e-4 |
| G6 U56 BAND-DG g1.00 == standing memo line 3 (11.55 / 1.2067 / −15.70 / 1.2405 / 1.1798) | 4.954e-05 | 5e-4 |
| **G7 the object under test: the floor miss re-read as −0.829 pp full / −0.144 pp OOS vs idea 787's −0.83 / −0.14** | 3.512e-03 | 5e-2 |
| G8a `flat_drag(d=0)` is a no-op / G8b bar CAGR strictly decreasing in d | 0.000e+00 / −2.26e-02 | exact / < 0 |
| G9 (**added post-hoc**) `slack = slack(0)+0.70·bar_drag−book_drag` over all 308 HAZARD cells | **1.776e-15** | 1e-9 |

## Caveats

1. **NO INTERNET in this sandbox: no delisting figure was fetched.** The `L` rungs are labelled with
   the commonly cited Shumway-1997-style NYSE/AMEX (−30%) and Shumway-Warther-1999-style Nasdaq
   (−55%) anchors **from recollection, UNVERIFIED**, plus an arithmetic total-loss rung that needs no
   citation. Every rung is reported in full, so the published deliverable is the **required (h, L)
   curve** — `inversion_hl.csv` — not a claim about the true delisting return. The hazard comparison
   ("2.5–5.8%/yr is a small-cap number") is a judgement on the U56 constituent list, not a citation;
   a reader who believes large-cap performance-delisting hazard reaches 3%/yr should read the L = −30%
   h = 3% row as a pass. **Verifying the anchors is the obvious local/Actions follow-up.**
2. **The caches cannot supply an internal hazard estimate.** U56, B136 and SMALL439 are
   current-constituent panels; names delisted before 2026-09-10 are in none of them, so h cannot be
   measured from committed data at all. That is the same stated limit as idea 782.
3. **The phantoms clone survivors, so their pre-death paths are too good.** A real delistee
   underperforms for years before the event; this construction gives it the donor's return until the
   slide begins, which **understates** both drags. The `W` ladder (21–504 days) is the sensitivity
   that brackets it, and the direction is favourable to the artefact hypothesis — the KILL is stated
   against the construction that flatters it.
4. **Donor-composition noise is the size of the drag at low h.** At U56 h = 1–2% (11–24 phantoms
   from 55 donors) the bar drag is **negative** in 2 cells, so `phi` is screened on bar drag > 0.5 pp
   and a 3-seed control is published: at h = 2%, W = 252, L = −30% the conclusion-bearing slack is
   seed-stable (−0.31 / −0.31 / −0.44 pp U56; −2.05 / −2.16 / −2.22 pp B136) while `phi` itself is
   not (−0.54 / +0.28 / +0.24). Read `phi` only at h ≥ 3%.
5. **One bar form in the headline.** `B_EWW10` (weekly, 10 bps) is idea 787's *weaker* equal-weight
   bar, so the required drags above are the smaller ones; `B_EW742` is in `grid.csv` and needs more.
6. **SURVIVORSHIP, the irony of this run:** it prices a survivorship correction on panels that are
   themselves survivorship-selected, so the *book's* own returns are inflated by the same unmeasured
   amount. Caveat 3's direction applies to the book too, and `phi` is exactly the quantity that
   decides whether that matters. This run measures phi; it does not restore the missing names.
