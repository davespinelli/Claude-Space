# Idea 521 — do the record's HAND-COPIED-CONSTANT gates fail more than its ARTEFACT gates?

**lane B, 2026-09-11.** Script: `2026-09-11_do-the-record-s-HAND-COPIED-CONSTANT-gates-fail-more-than-its-ARTEFACT-gates_B.py`.
Nothing re-executed: `observed` / `bar` / `passed` are idea 515's committed `.gates.csv`, so every
failure rate below is the record's **native** one. Two tuned params (REFERENCE-KIND CLASSIFIER x
BAR), all grid points reported. PROTOCOL rules 1–9; 10 bps, t+1. RULES.md / scan.py / bot.py /
baseline.py / PROTOCOL.md untouched.

## Verdict — ANSWERED (yes), and the queue's proposed fix is the wrong one. KILL for capital.

**A. Yes, and by 2.1–3.0x.** Native failure rate on idea 515's 171 reached gates:

| classifier | CONST | ARTEFACT | SELF | STRUCTURAL |
|---|---|---|---|---|
| NARROW | **0.7143** (n=7) | 0.2353 (n=17) | 0.0815 (n=135) | 0.2500 (n=12) |
| MID | **0.6250** (n=8) | 0.3030 (n=33) | 0.0424 (n=118) | 0.2500 (n=12) |
| WIDE | **0.5556** (n=9) | 0.2683 (n=41) | 0.0367 (n=109) | 0.2500 (n=12) |

The direction holds at every classifier. It is the **opposite sign** to idea 681's
`SELF 0.9403 > CONST 0.9074 > ARTEFACT 0.7200`, and both are right about their own populations:
681's CONST class is n=54 (any committed constant, self-consistency being the object), this run's
is n=7–9 (a decimal literal standing in the compared expression as the *reference value*). The
CONST-vs-ARTEFACT ordering is therefore **classifier-dependent and must be quoted with its
classifier**; only the SELF-is-cleanest leg reproduces across both.

**B. But the two populations fail in completely different size classes**, and that is the real
finding. Overrun = observed / declared bar on the 23 native failures:

* CONST failures (n=5): median **1.57x**, max **2.50x** — a *transcription-sized* miss.
* ARTEFACT failures (n=10): median **8.8e+06x**, max **1.0e+10x**.
* SELF failures (n=5): median **2.2e+06x**, max **5.5e+09x**.

A hand-copied 3-decimal constant carries a rounding half-width q = 5e-4, and the record's own bar
on those gates is *also* 5e-4 — i.e. the gate demands the re-run land in the **same rounding cell**
as the typed number, leaving zero slack for anything else. `abs(m['Sharpe'] - 1.133) < 5e-4` reads
7.848148e-4 in all **3** scripts that restate it (queue claim reproduced exactly, gate G3).

**C1 — "re-gate on the artefact" cannot be executed.** The typed number does not identify its own
source: scanning the record's **3,732** committed CSV artefacts, each constant's rounding cell
contains thousands of candidate cells (1.133 -> 17,245 cells over 537 scripts; 0.2185 -> 1,855 over
248; 0.95 -> 195,123). **0 of 6** constants are identifiable from their value alone. Re-gating on
the artefact needs a *pointer* field (file + column + row), not a better bar.

**C2 — the quantization correction is identifiable, and it works.** `bar' = bar + 0.5*10^-d` for a
d-decimal transcription (q = 0 for a full-precision artefact) recovers **4 of the 5** CONST
failures — CONST native passes 3/8 -> 7/8 at MID — and gate **G4 proves it changes nothing
anywhere else**: on all 30 non-CONST grid rows the bar+q outcome reproduces the native outcome
exactly. The one CONST failure it does not recover (`abs(m['CAGR'] - 0.2185) < 5e-4`, overrun
2.50x) is a genuine reproduction gap, correctly left failing.

**D. Rule 8 (2009–2016 chosen, 2017-01-01+ read once) — the gate is worthless for capital.**
27 books (3 panels x gross {0.50, 0.75, 1.00} x cadence {W, M, Q}), 5 policies x 6 bars x 3 panels
= 90 cells, all reported. Re-run perturbation: the record's own 260-vs-252 warm-up convention.

* Control, proven not assumed: a **+/-2 trading-day cache vintage step moves a fixed-window
  statistic by EXACTLY 0** (max TRAIL and max LEAD drift both 0.000e+00 over all 27 books), because
  every window date already has its 200 observations. The record's CONST failures cannot be vintage.
* The convention step moves IS Sharpe by 2.61e-3 to 3.53e-2 — **5x to 70x the 5e-4 bar**.
* Consequence: `ARTEFACT`, `CONST3`, `CONST4` and `CONST3+q` admit **identically** at every bar
  (0 / 0 / 0 / 0 / 18 / 27 books at bar 1e-6 / 1e-4 / 5e-4 / 1e-3 / 1e-2 / 1e-1). Of 72 gated cells,
  **52 are a total stand-down and 0 ever pick a different book** from ungated.
* OOS: ungated picks are U56 g1.00-M (OOS CAGR 12.86%, Sharpe 1.2325, MaxDD -18.6%), B136 g1.00-W
  (10.66%, 1.1195, -16.1%), SMALL439 g1.00-M (5.75%, 0.6209, -21.9%) against RULES v2 OOS Sharpe
  1.2834 / 1.1206 / 0.5665 and SPY 0.8721 / 0.8820 / 0.8820 (SPY OOS CAGR 15.24% / 15.45% / 15.45%).
  **4a 0/90, 4b 28/90** (NOGATE alone 4a 0/18, 4b 12/18) — the gated cells' extra 4b passes are the
  same three books re-counted at the loose bars, never a new one.

**No KEEP on either path.** 4a fails everywhere (no book beats RULES v2 in both halves). The 4b
passes belong to the ungated books, not to the gate: the reference kind is a **no-op on capital**,
and the binding dial is the bar's scale versus the record's own convention noise.

## Proposed as a reporting habit (not adopted; PROTOCOL untouched — Sunday's call)

> A reproduction gate comparing against a constant typed with d decimals must be written
> `bar' = bar + 0.5*10^-d`, or carry an explicit pointer (file, column, row) to the full-precision
> artefact it reproduces. A bar tighter than the transcription's own rounding half-width is
> unsatisfiable by construction.

Cost of the habit: 4 of the record's 23 native failures clear; provably 0 other gates move (G4).

## Gates (all pre-registered, non-raising) — 4/4 PASS

* **G1** idea 515 census shape 520/345/87/46/40/151 — PASS, exact.
* **G2** 171 reached gates with 23 native failures — PASS.
* **G3** queue's 1.133 claim: restated in >=3 scripts, observed 7.85e-4 in all — PASS (3 scripts,
  3 clauses, single observed value 7.848148e-4).
* **G4** bar+q reproduces the native outcome on every non-CONST kind — PASS, 30/30 rows.

Scope: the classification covers all 520 committed clauses; the failure rates cover the 171 idea 515
reached (43 of 151 scripts), so they are the record's reached sample, not its whole gating surface.
Part C's counterfactuals are scored on the 155 tol/exact/count gates with a numeric observation —
the 15 structural clauses carry no bar and the single `floor` clause inverts the sense, both excluded.
SMALL439 carries the panel's documented survivorship bias (current constituents).
