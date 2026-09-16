# QUEUE idea 1098 (lane C, 2026-09-16) — do the record's COMMITTED COST CLAIMS price the SHARPE LEGS, or only the CAGR FLOOR?

**ANSWERED = NEITHER, AND THE SECOND HALF OF THE QUEUE'S ASK IS UNRESOLVABLE FROM THE RECORD'S
OWN PROSE. The record's committed cost claims price the DRAWDOWN CAP most often (0.4880 of the
125 that name a leg), the SHARPE legs next (0.4720) and the CAGR FLOOR least (0.3920) — so "only
the CAGR floor" is REFUTED as a reading of the record. But the far larger fact is that 1,876 of
2,088 committed cost-and-verdict sentences — 0.8985 — NAME NO LEG AT ALL, and NOT ONE of the 28
CAGR-assuming claims states enough of its own cell to be re-scored: the re-score the queue asks
for has a population of ZERO under an honest resolution rule. On the tape side 1094's correction
GENERALISES but only as a 10-of-17 majority: the killer leg is a Sharpe leg at 0.588 of the books
a rising rung can kill, the CAGR floor at 0.235 — and every CAGR killer is on the GROSS ladder.
No RULES change, no book promoted, no PROTOCOL edit (rule 6); RULES.md, PROTOCOL.md, scan.py,
bot.py and baseline.py untouched.** SELECTION: lane C takes the SECOND open idea; 1098 was the
second line under '## Open' and names no EDGAR / Form 4 / 8-K / options / live-data source.

**NUMBERING COLLISION, DECLARED.** An earlier idea also carries the number 1098 (cited by
1102/1108/1110 as "1098's bootstrap") — idea 932's filing defect again. This run is the QUEUE
line filed as 1098 under '## Open' on 2026-09-16 and re-runs nothing of the older one.

## THE TWO TUNED DIALS AND NO MORE (PROTOCOL rule 4)
`CLAIM SET` {NARROW, PROX, WIDE} x `COST RUNG` {0, 10, 25, 50} bps = **12 points, all published**
(`.census.csv`). NOT dials, all reported: PANEL {U56, B136} x LADDER {N, H, GROSS, CADENCE} at
1082/1086/1094/1097/1110's rung lists = **54 books** (`.books.csv`, `.grid.csv`, `.ladder.csv`);
the eight 4b legs; the three rule-8 choosers. Frozen at 936/1064/1071/1082/1086/1094/1097's
construction: CAND20 legs, cap INF, max_vol 0.60, gross 0.75, W, min hold 126, N = 20, LAG 1,
warm-up 260, IS end 2016-12-31, 4b constants 0.60/0.70. **The 1-bp ladder 0..200 bps is a
MEASUREMENT AXIS, not a dial** — no book is selected on it.

## WHAT "BINDING" MEANS HERE, PRE-REGISTERED
A cost claim is a claim about an axis measured in bps, so **the cost axis is the ruler and no
unit conversion is needed**: `c*_L` is the last 1-bp rung at which leg L still passes counting
only the run that starts at 0 (1094/1097's convention), `KILLER = argmin_L c*_L` over the five
full-sample legs, and `HEADROOM(L, c) = c*_L - c`. A book failing a leg at 0 bps is DEAD0 and is
excluded from the killer population, which is declared in advance to be the books the queue's
question is about: those that have a 4b pass for a rising rung to kill.

## THE TAPE SIDE — 1094's CORRECTION GENERALISES, AS A 59% MAJORITY, NOT A LAW
17 of 54 books clear all five full 4b legs at 0 bps; **all 17 die by 200 bps** (median c\* **68**
bps, min 8, max 172). Killer kind: **SHARPE 10 (0.588) — L_H1 5, L_H2 5 — CAGR 4 (0.235), DD 3
(0.176)**. `H_SHARPE_FIRST` **PASS**. The binding leg (smallest headroom) at 0 / 10 / 25 / 50 bps
is a halves-Sharpe leg at **45 / 46 / 45 / 34 of 54** books, and at 50 bps `L_OOS` takes 14 —
**cost reaches the Sharpe legs first because SPY pays no turnover and the book's vol barely
moves**, exactly 1094's mechanism, now measured on 54 books instead of one.

**THE ONE STRUCTURAL FINDING: EVERY CAGR KILLER IS A DE-GROSSED BOOK.** All four cells whose 4b
pass dies on `L_CAGR` sit on the **GROSS** ladder — U56 g = 0.55 / 0.60 / 0.65 (c\* 44 / 81 /
112 bps) and B136 g = 0.50 (c\* 12) — and none sits on N, H or CADENCE. Cutting gross cuts the
book's CAGR against an uncharged SPY floor while leaving its Sharpe almost untouched (U56 Sharpe
1.1390 / 1.1392 / 1.1394 at g = 0.55 / 0.60 / 0.65 against 1.1397 at 0.75), so **the CAGR floor
is the binding leg of the de-levered book and of nothing else.** `H_CAGR_LAST` **FAILS at 0.2353
in the opposite direction to the queue's framing**: the last leg to die is `L_DD` at 12 of 17,
because `H_DD_INERT` **PASSES at 0.9630** — cost moves drawdown almost not at all.

## THE RECORD SIDE — THE CENSUS (12 dial points, `.census.csv`)
| claim set | n | name a leg | CAGR | SHARPE | DD | CAGR only | SHARPE only |
|---|---|---|---|---|---|---|---|
| NARROW (explicit leg names) | 59 | 59 | 0.3390 | 0.3051 | **0.4576** | 0.2881 | 0.2203 |
| **PROX (headline)** | 125 | 125 | 0.3920 | 0.4720 | **0.4880** | 0.2240 | 0.2160 |
| WIDE (every cost claim) | **2,088** | **212** | 0.3915 | 0.4151 | **0.4717** | 0.2358 | 0.2311 |

**`H_CAGR_ASSUMED` FAILS at 0.3920** — the CAGR floor is the LEAST-named of the three, so the
queue's "only the CAGR floor" is refuted; but the Sharpe legs do not win either, the drawdown cap
does, on all three claim sets. **THE HEADLINE NUMBER IS THE DENOMINATOR: 1,876 of 2,088 committed
cost-and-verdict sentences (0.8985) name NO leg at all.** The record overwhelmingly publishes
*that* a book dies at a rung, not *what* kills it. Read at the rung, the shares move: at 10 bps
PROX claims name SHARPE 0.5490 against CAGR 0.4118; at 50 bps SHARPE 0.5000 against CAGR 0.1667.

## THE RE-SCORE — POPULATION ZERO, AND A DEFECT IN THIS RUN'S OWN FIRST CUT
Of the 28 PROX claims naming the CAGR floor and nothing else, **0 are re-derivable**. The
headline rule `R_STRICT` requires a claim to name its PANEL, at least one CONSTRUCTION dimension
explicitly (N, H, gross or cadence) and no out-of-family token; it resolves **82 of 2,088**
claims overall and **0 of the 28**. **This run's FIRST CUT used `R_LOOSE`** — panel alone, with
unstated dimensions taking the frozen defaults — **and it was wrong**: it resolved 11 of the 28
and would have published **REFUTED 9, CONFIRMED 0, UNDECIDED 2 (0.8182 refuted)**, but reading
its own output showed nine of those eleven are claims about ENSEMBLE, SLEEVE, TRIMMED and BAND
books that merely mention `u56`. Scoring those against the frozen cell's killer leg is a
TRANSFER wearing a re-derivation's clothes. Both rules are published (`.rescore.csv` carries
`basis`, `strict_ok`, `loose_verdict`); `H_RESCORE_FLIPS` is recorded as **UNRESOLVABLE (n = 0)**,
with 0.8182 shown only as R_LOOSE's upper bound and labelled a transfer. The 28 claims are
published as **TRANSFERRED** against the measured base rate (SHARPE 0.588 / CAGR 0.235 / DD
0.176), which is an EXTRAPOLATION and not a re-derivation of any of them (1048/1102/1110's
convention).

## GATES 14 of 14 PASS, printed before any result number (`.gates.csv`)
G1/G1b/G1c the exact cost ladder `r(c) = g − tn*c/1e4` == `engine.backtest` at 0/10/25 bps,
**1.39e-17**; G2 CROSS-RUN 936/1071/1082's committed U56 W/H126 N=20 triple @10 bps 3.18e-07;
G3 SPY OOS triple 1.70e-04; G4 live RULES v2 MaxDD @10 bps == −12.05% at 4.95e-05; **G5 CROSS-RUN
1094's committed n=12/H=21 ladder at all four rungs 4.96e-05; G5b its c\* full/OOS == 63/64
EXACTLY (0.00e+00); G5c its killer leg is L_H1 — the single cell this idea is built on reproduces
bit-for-bit**; **G6 CROSS-RUN 1097's committed `cstar_full` on the 18 shared N/H126 cells,
0.00e+00**; G7 CAGR non-increasing in the rung at all 54 books; G8 determinism 0.00e+00; G9 the
harvest is reproducible across two scans; G10 CORPUS STAMP — **888 files, 12,653,167 bytes,
sha256(file list)[:16] = `dfb0b9e49439fc08`** (LEADERBOARD.md + CHANGELOG.md + 886 committed
`*.result.md`).

## RULE 8 AND BOTH KEEP PATHS — NOTHING PROPOSED (`.walkforward.csv`, `.grid.csv`)
4b full passes **17 / 16 / 15 / 10 of 54** and 4b OOS **19 / 17 / 16 / 14 of 54** at 0 / 10 / 25 /
50 bps; **4a is 0 of 54 at every rung** (the live book's −12.05% MaxDD is unreachable for a
0.75-gross momentum book, as in every run since 2026-09-04). Rule 8 picks the ladder rung on
2009–2016 alone, three IS-only choosers, OOS read once: **96 picks, 4b full 18, 4b OOS 18, 4a 0**.
Every reachable 4b pass is a book the record already holds — the frozen incumbent U56 N=20 /
H=126 / W / g=0.75 (full **15.58% / 1.1397 / −19.13%**, halves 1.2037 / 1.0971, **OOS 16.97% /
1.1643 / −19.13%** at 2.90x/yr turnover, c\* **117** bps on L_H1) and, at 25 and 50 bps only, the
U56 QUARTERLY cell already PARKED by idea 1099. Against **SPY** (full 15.10% / 0.8829 / −33.72%,
halves 0.9588 / 0.8207; OOS 15.21% / 0.8711 / −33.72%) and the **live RULES v2** (full 8.62% /
1.2007 / −12.05%, halves 1.2322 / 1.1760; OOS 9.45% / 1.2762 / −12.05%). **No new book, no memo,
no proposal.**

## SURVIVORSHIP (PROTOCOL rule 9)
U56 and B136 are CURRENT-CONSTITUENT panels. A breakeven rung contrasts a book against SPY, a
real index, so the bias does **not** cancel out of `c*`: every `c*` above is an upper bound and
every 4b pass is optimistic. The census layer is a pure text scan and carries no market bias.

## WHAT THIS RUN CANNOT SAY
The census reads PROSE. A claim whose cell is stated only in its file's header, or only in the
script it cites, is unresolved here (idea 1037's territory); `R_STRICT`'s 82 of 2,088 is a lower
bound on what a script-level resolution could recover. The leg lexicon is a text heuristic —
NARROW and PROX bracket it (59 vs 125 claims) and both are published, but no lexicon recovers a
claim that names no leg, and those are 0.8985 of the corpus.
