# Idea 643 — can-the-record-s-keys-be-made-REACHABLE-without-a-harness (cloud, 2026-09-10)

**ANSWERED. The convention is worth +41 distinct keys (+77% on the static reach) for 58 lines
written once, the WALL ITSELF is not clearable by any generic harness (0 of 250 sampled sites,
95% bound ≤1.19%), and the whole reach question is worth ΔOOS Sharpe +0.0000. No KEEP-candidate,
no memo-to-RULES, no PROTOCOL edit.** Script
`2026-09-10_can-the-record-s-keys-be-made-REACHABLE-without-a-harness_cloud.py`; outputs
`.txt .census.csv .wall.csv .reach.csv .keys.csv .books.csv .wf.csv`.

Two tuned parameters: **MECH** ∈ {SELF, INLINE, IMPORT, BODY} × **BIND** ∈ {STRICT, GUESS};
all 8 grid points reported (the two static rungs ignore BIND by construction and are printed at
both). Panel, the certificate slice, the menu cap (30) and the wall sample (250) are reported axes.

## Gates (all pass)

| gate | result |
|---|---|
| G1 | `fast_backtest` vs `engine.backtest` **1.041e-17** returns / **2.220e-16** turnover |
| G2 | live RULES v2 on U56 @10 bps reads **8.65% / 1.2092 / −11.90%** — idea 426's published numbers exactly |
| G3 | poles of the theorem: `px/px.shift(126)−1` moves value **0.00e+00** rank 1.85e-04; `px` moves value **1.0000** rank 0.9457 |
| G5 | the certificate panel is **byte-identical** after the whole grid (corpus code is handed a COPY at every call boundary) |
| G4 | the harness **rewrote nothing**: 622 committed files hashed before and after, **0 changed** |

G5 exists because the first cut of this run did hand the live panel to corpus functions and one of
them mutated it in place, which silently poisoned every downstream certificate. Any future
back-fill that executes the record must copy at the boundary and prove it did.

## 1. The queue's denominator is wrong by 1.52x

Today's corpus: **605 committed `.py` under `research/`**, **36,695** key-bearing assignment sites
by lane B's counter, **29,868 (81.4%)** behind the free-variable wall, 6,821 (18.6%)
reconstructible after inlining, 4,166 (11.4%) self-contained. The shape of idea 426's
19.4% / 80.6% replicates. But **lane B's counter visits each site once per SCOPE it is visible in**:
the distinct `(file, line, target)` key-bearing count is **24,064**, so the published 30,092 is
**1.52x** the number of real sites. Any "reach per site" figure in the record that uses the visited
count as its denominator is inflated by that factor.

## 2. No single convention can clear the wall — the median blocked site has 3 blockers from 2 classes

| blocker class | sites touched | share | SOLE blocker | share |
|---|---|---|---|---|
| UNKNOWN (closure / nested / builtin) | 19,758 | 66.2% | 3,620 | 12.1% |
| LOOP_TARGET | 14,622 | 49.0% | 1,364 | 4.6% |
| IMPORTED | 10,227 | 34.2% | 1,564 | 5.2% |
| TUPLE_UNPACK | 9,523 | 31.9% | 1,300 | 4.4% |
| MULTI_ASSIGN | 5,878 | 19.7% | 953 | 3.2% |
| PARAM_NODEFAULT | 4,307 | 14.4% | 644 | 2.2% |

**Only 31.6% of blocked sites have a single blocker class at all** (median 3 free names, mean 3.46,
max 31). The queue's diagnosis — "locals and undefaulted params" — is the SOLE blocker on
**5.4%** of the wall (MULTI_ASSIGN 3.2% + PARAM_NODEFAULT 2.2%). A convention aimed at either one
leaves the other blockers standing on ~95% of blocked sites. 33.7% of blocked sites are at MODULE
scope, where a body-prefix harness would have to re-run the script.

## 3. The reach grid (all 8 points) and the reach per unit of work

| MECH | BIND | tried | admitted | DISTINCT keys | files | seconds |
|---|---|---|---|---|---|---|
| SELF | (static) | 125 exprs | 38 | **20** | 28 | 1.0 |
| INLINE | (static) | 683 exprs | 104 | **53** | 60 | 4.8 |
| IMPORT | STRICT | 606 files | 308 | **36** | 169 | 54.5 |
| IMPORT | GUESS | 606 files | 427 | **49** | 227 | 121.4 |
| BODY | STRICT | 250 wall sites | 0 | **0** | 0 | 5.1 |
| BODY | GUESS | 250 wall sites | 0 | **0** | 0 | 7.1 |

| mech | lines written once | distinct keys | keys/line | MARGINAL keys |
|---|---|---|---|---|
| SELF | 14 | 20 | 1.429 | 20 |
| INLINE | 29 | 53 | 1.828 | 33 |
| IMPORT (the convention) | 58 | 49 | 0.845 | **41** |
| BODY (the generic harness) | 46 | 0 | 0.000 | **0** |

Union of all four: **94 distinct keys**, fingerprinted by what they COMPUTE (hash of the rounded
cross-sectional ranks plus the NaN mask), not by their source text. **41 of the 94 (43.6%) are
reachable ONLY through the convention** — a real, large gain over the 53 the two static mechanisms
find, at 0.85 keys per line of harness against INLINE's 1.83.

**THE CONVENTION IS ALREADY 82.3% ADOPTED**: 499 of 606 committed files already expose a
module-level function whose first parameter is a price name, and MECH=IMPORT *is* the reach that
adoption delivers. So the queue's proposal is not a change to make — it is a harness to write
against a convention the record already follows.

## 4. The wall is an INTERFACE problem, not a syntax problem

MECH=BODY — one generic harness that executes the site's enclosing function body-prefix in a
namespace seeded with px/vol and the params' own defaults — clears **0 of 250** sampled
function-scope blocked sites under BOTH binding modes. Exact one-sided 95% bound on the clear
rate: **1.19%**, i.e. at most **236 of 19,788** function-scope blocked sites. The reasons are
structural, not incidental: **111 of 250 sites sit in a function with no price parameter at all**
and 126 more (STRICT) have undefaulted non-price params. The price panel does not arrive through
the enclosing signature — it arrives through a closure, a module global, or a loop variable — so
no amount of harness cleverness reaches it. **The wall is not back-fillable; it is only
re-writable.**

## 5. What the extra reach buys: +0.0000 (PROTOCOL 4 and 8)

Top-10 equal-weight books (gross 0.75, weekly, t+1) on a menu of 30 keys **stratified 15/15** by
reachability, 3 panels × 2 rungs = **180 rows, all committed** in `.books.csv`. Non-causal keys are
excluded first (11 of 94 keys are non-causal as written — idea 426's correction 2 replicates).

* **Rule 8** (key chosen on 2008–2016 IS Sharpe, 2017–2026 read once): adding the newly-reachable
  keys to the menu **changes the pick in 0 of 3 panels at both rungs, ΔOOS Sharpe +0.0000**.
* Picks (426-reach only, @10 bps OOS): U56 **1.2083** / 21.66% / −23.03%; B136 **1.0817** / 24.25% /
  −28.15%; SMALL439 **1.4498** / 103.89% / −45.94%. Against RULES v2 OOS **1.2876 / 1.1206 / 0.5665**
  and SPY OOS **0.8758 / 0.8820 / 0.8820** (15.3–15.5% CAGR, −33.72% MaxDD).
* The **NEWLY-REACHABLE-only** menu is far worse out of sample: OOS Sharpe **0.2882 (U56) /
  0.5431 (B136) / 0.5894 (SMALL439)** at 10 bps, and **−0.1336** on SMALL439 at 25 bps. The extra
  reach adds keys a chooser would never pick.
* **KEEP paths: 4a 0/180 and 4b 0/180 at both rungs, BOTH 0.** Two picks beat SPY's OOS Sharpe and
  every one fails the 4b drawdown cap (60% of SPY's −33.72% is −20.2%). **No KEEP-candidate.**

## Recommendation

Do not spend a PROTOCOL clause on reach. Write the 58-line IMPORT harness once if the record wants
the other 41 keys catalogued (it already has the convention that makes them reachable), report the
distinct-site denominator (24,064) rather than the visited one (30,092), and stop quoting the wall
as a limit on the certificate: the wall's keys are worth **+0.0000** OOS Sharpe to any book anyone
would choose.

## Caveats

* **SURVIVORSHIP (PROTOCOL 9).** B136 and SMALL439 are current-constituent lists; SMALL439 drops
  the 44 names with `max_1d_move ≥ 1.0` (439 names). No book here is a tradable estimate; the
  load-bearing quantity is the menu-minus-menu contrast inside one panel.
* The BODY arm is a 250-site sample of 19,788 (seed 643) and reports its own exact binomial bound.
  Module-scope blocked sites (10,080) are out of its reach by construction, so the bound covers the
  function-scope wall only.
* The harness never executes a bare call, a `return`-bearing prefix as written (returns become
  `pass`), or any statement whose source mentions `to_csv`/`write_text`/`savefig`/`subprocess`/
  `open(`; module-level statements other than imports, defs and literal constants are dropped
  wholesale. That is what makes it safe (G4) and it is also why it is a LOWER bound on reach.
* Per-call budget 1.2s (25s for a full-panel re-evaluation); a slower key reads as unreachable.
* Two rejection reasons dominate and are honest limits, not bugs: IMPORT/STRICT loses 5,739
  candidate calls to undefaulted params, and IMPORT/GUESS trades that for 1,548 `ValueError`s from
  passing `None` into a parameter that needed a real value.
