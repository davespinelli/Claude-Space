# Idea 2264 (2026-09-22, lane B) — DOES A DRAWDOWN-BUDGETED IS-ONLY GROSS CHOOSER MAKE THE RECORD'S ONLY RELIABLE 4b PASSER RULE-8 REACHABLE?

**ANSWERED = YES, and the reason the record kept reading NO is that it only ever tried one
chooser.** Three runs (2233 cloud, 2237 C, 953 cloud) established that the only cells clearing
PROTOCOL path 4b anywhere on this corpus are plain GROSS rungs of the live RULES v2 band book,
and all three PARKed them as "not rule-8 reachable" because the habitual IS-Sharpe chooser takes
the ladder end g = 1.50 and blows the OOS DD cap. Sharpe is the one statistic gross is *invariant*
to (u56 1.2010 → 1.2000 over g = 0.25..1.50): the chooser was measuring the axis the dial does not
move. Matched to the leg that actually binds — **the largest gross whose IN-SAMPLE MaxDD stays
inside κ × (IS SPY MaxDD), the 4b drawdown cap computed on 2009-2016 alone** — the cell is reached.

## Gates: 10 of 10 PASS
G1 `g = 0.75` reproduces `baseline.rules_v2_weights` at max|dw| **0.0** and its 10 bps return line
at **0.0**, both panels. G2 the dial is pure sizing, `w(g) = (g/0.75)·w(0.75)` at **3.5e-18**.
G3 the committed cells reproduce to **5.0e-05** (live v2 u56 @10 bps 8.62%/1.2010/-12.05%, halves
1.2276/1.1806, OOS 9.46%/1.2767/-12.05%; g=1.00 11.53%/1.2009/-15.91%, OOS 12.67%/1.2760/-15.91%;
SPY OOS 15.29%/0.8751/-33.72%). G4 IS MaxDD monotone non-increasing in gross, both panels.
G5 110 book cells + 170 chooser cells published. G6 the derived cost ladder equals a full
re-simulation at 25 bps to **0.0** (`engine.backtest` never feeds cost back into positions).

## The grid — 110 book cells, every one published
GROSS {0.250 … 1.500 step 0.125} × COST {0,5,10,25,50} bps × PANEL {u56, b136}. Two tuned dials
and no more: **κ and GROSS**. Cost, panel, band (3%) and cadence (W) are reported, never selected.

- **4a: 0 of 110.** Gross is Sharpe-neutral, so the book can never beat the live one in both
  halves, and it is strictly deeper in drawdown. Path 4a is a KILL for this dial, unconditionally.
- **4b FULL 27 of 110; 4b OOS 29 of 110.** Unlevered sub-ladder (g ≤ 1.00, 70 cells): 7 and 10.
- Binding leg over the 83 4b-FULL fails: **CAGR floor 63, DD cap 20** — the CAGR floor still
  dominates, exactly as 2227 / 2233 / 2237 / 2241 / 2254 found, but gross is the one dial that
  climbs it before the DD cap bites.

## Rule 8 — 2009-2016 chooses, 2017-2026 read once. Chooser scoreboard (10 panel × cost cells each)

| chooser | picks | 4b OOS | 4b FULL | 4a |
|---|---|---|---|---|
| `C_LIVE` (shipped g = 0.75, no-information control) | 0.75 | **0/10** | 0/10 | 0/10 |
| `C_SHARPE` (the record's habitual chooser) | 1.25 / 1.375 / 1.50 | **1/10** | 1/10 | 0/10 |
| `C_CALMAR` | 1.50 | **0/10** | 0/10 | 0/10 |
| `C_DDB` κ=0.40 | 0.75 | 0/10 | 0/10 | 0/10 |
| `C_DDB` κ=0.50 | 0.875 / 1.00 | 5/10 | 7/10 | 0/10 |
| **`C_DDB` κ=0.60** (= PROTOCOL 4b's own δ) | 1.125 / 1.25 | **9/10** | **10/10** | 0/10 |
| `C_DDB` κ=0.70 | 1.25 / 1.375 / 1.50 | 1/10 | 1/10 | 0/10 |
| `C_DDB` κ≥0.80 | 1.50 | 0/10 | 0/10 | 0/10 |
| **`U_DDB` κ≥0.60** (same rule, PROTOCOL rule 2's no-leverage cap g ≤ 1.00) | **1.00** | **6/10** | 8/10 | 0/10 |

The κ ladder is sharply peaked (0/5/9/1/0/0/0 out of 10), which would be damning if κ were free.
It is not free at the pick that matters: **under the no-leverage cap the budget is slack for every
κ ≥ 0.60, so `U_DDB` degenerates to "take the largest legal gross" — a zero-parameter rule that
returns g = 1.00 on both panels at every cost rung.** And κ = 0.60 is PROTOCOL 4b's own δ,
pre-registered 2026-09-04, not chosen here.

## The candidate: the live book at gross 1.00 (u56)
@10 bps FULL **11.53% / 1.2009 / -15.91%** (halves 1.2282 / 1.1799), **OOS 12.67% / 1.2760 /
-15.91%**, turnover **2.35x/yr** — against live RULES v2 8.62% / 1.2010 / -12.05% (OOS 9.46% /
1.2767 / -12.05%, 1.77x/yr) and SPY 15.14% / 0.8851 / -33.72% (OOS 15.29% / 0.8751 / -33.72%).
**4b passes in FULL and OOS at 0 / 5 / 10 / 25 bps**; at 50 bps OOS still passes and FULL misses
the CAGR floor by 0.11 pp. OOS margins at 10 bps: DD **+4.32 pp**, CAGR **+1.97 pp**.
The cost-fragility that disqualified every previous candidate is absent here — 2.35x/yr, not 8.18x.

## Arm F — leverage is not free and is not needed
Re-read every levered rung with a flat financing charge of (g−1) × rate, rate ∈ {0, 2%, 4%}/yr:
**4 of 8 levered rungs clear 4b OOS at every rate**, and the two that fail (1.375, 1.50) fail on
the DD cap, not on financing. So κ = 0.60's levered picks survive financing — but the unlevered
candidate above is the one filed, because PROTOCOL rule 2 forbids leverage unless the idea says so.

## Arm R — falsification: reversed walk-forward (2017-2026 chooses, 2009-2016 read)
The forward test is flattered by tape order: the choosing window's SPY MaxDD (-22.06%, 2011) is
*shallower* than the read window's (-33.72%, 2020), so an IS budget is automatically conservative.
Reversing the windows removes that: choosing SPY MaxDD -33.72%, read -22.06%, cap -13.24%.
**κ = 0.60 still clears 4b at 7 of 10 cells** (picks g = 1.25); κ = 0.50 reads 3 of 10, κ = 0.40
and κ ≥ 0.70 read 0 of 10 — the same peak, in the harder direction. The reversed binding leg flips
as expected (DD cap 43 of 70 fails, CAGR floor 27). The device is not a tape-order artefact.

## Honest limits
- **Panel-dependent.** On b136 the same g = 1.00 pick clears 4b FULL at 0/5/10 bps but misses 4b
  OOS from 5 bps on, failing the CAGR floor by 0.05-0.21 pp. 1 of 2 panels at the headline rung.
- **It buys CAGR with drawdown and no Sharpe:** +2.91 pp CAGR for +3.86 pp MaxDD, Sharpe
  unchanged to 4 decimals. It is a sizing decision, and PROTOCOL rule 6 gives that to the Sunday
  review, not to a run. Filed as a candidate, explicitly not recommended.
- **Survivorship (rule 9):** u56/b136 are 2026 constituents held from 2008, so every CAGR level is
  optimistic and both 4b level legs are easier than on a point-in-time panel.
- Flat costs, no spread/impact/borrow. One cadence (W), one delay (t+1), one band (3%).

**VERDICT: KEEP-candidate (4b, FULL and OOS, 0-25 bps, u56, unlevered, rule-8 reachable) —
recorded, not recommended. KILL on 4a (0 of 110). Method finding: the record's "not rule-8
reachable" verdict on the gross cell was a property of the CHOOSER, not of the cell.**
