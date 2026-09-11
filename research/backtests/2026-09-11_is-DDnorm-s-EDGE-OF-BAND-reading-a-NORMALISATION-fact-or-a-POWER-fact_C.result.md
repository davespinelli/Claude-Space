# Idea 717 — is-DDnorm-s-EDGE-OF-BAND-reading-a-NORMALISATION-fact-or-a-POWER-fact

**lane C, 2026-09-11 — ANSWERED / KILL of idea 714's normalisation reading. It is a POWER fact.
No KEEP, no memo.**

Script: `2026-09-11_is-DDnorm-s-EDGE-OF-BAND-reading-a-NORMALISATION-fact-or-a-POWER-fact_C.py`
(58.0s). Outputs: `.cells.csv .permcells.csv .matched.csv .gap.csv .claimleg.csv
.claimleg_matched.csv .walkforward.csv .console.txt`

## The question

Idea 714 (lane C, yesterday) cut idea 540's pooled permutation band by outcome and published,
inside the drawdown family:

| outcome | claims | logx survival | own null band | idea 714's verdict |
|---|---|---|---|---|
| MaxDD | **19** | 10.5% | [23.0%, 66.7%] med 45.5% | **BELOW** |
| DDnorm | **9** | 33.3% | [33.3%, 84.6%] med 62.0% | **INSIDE** (on the exact edge) |

and read it as *"once the drawdown is divided by the book's own vol the separation is gone"* —
a **normalisation** fact. But DDnorm carries **half the claims**, and the null band of a share
over m claims widens roughly as 1/√m. The two readings differ in the normaliser **and** in the
count, and idea 714 never separated them. This run re-reads both at **matched claim count**.

Nothing is re-backtested. The object is a within-stratum slope over idea 533's committed
`.arms.csv` (idea 295's MIX ladder: k=40, 21 q rungs × 8 draws = 168 panels, seed 20260909,
three books per panel, gross 0.75, weekly, 10 bps, next-day execution), and the null is idea
540's **own** permutation (seed 540, 21 strata), re-rolled in the same rng consumption order.

## Gates — five, all pass before a new number is read

| Gate | What | Result |
|---|---|---|
| G0 | idea 533's SPY comparand re-derives from `research/baseline.py` caches (`load_universe(small=True)` + `data/prices.csv`, warm-up 260, OOS 2017-01-01..2026-09-04) | SPY OOS **+15.45% / 0.8820 / −33.72%**, max \|d\| vs the committed column **3.243e-07** |
| G1 | idea 533's committed disp grid re-derives from its own `.arms.csv` | 360/360 rows, max \|db\| **4.649e-16**; KEEP counts **4a 0/504, 4b 41/504** as published |
| G1b | the cached fitter used for 400 draws is the literal one | max \|db\| and \|dt\| **exactly 0.0** on all 180 cells × 4 residualisations |
| G2 | idea 540's committed 180-row claims table re-derives cell for cell | 180/180, max \|d\| **8.882e-16**, `is_claim` **180/180**, `survive_logx` **180/180** |
| G3 | idea 714's two focal rows re-derived, not believed | MaxDD **19 claims, 2/19 = 10.5%**; DDnorm **9 claims, 3/9 = 33.3%** — exact |
| G4 | the first 200 draws reproduce idea 540's committed `permutation.csv` | max \|d\| **0** on all four columns; claim rate **35.9667%**, pooled logx band **[56.8%, 82.3%]** — both as published |

## The two matching devices (the device is not a third tuned dial — both run on both outcomes at every m)

- **SUB** — count-matched **subsample** at the inherited \|t\| ≥ 1.960 bar. Takes MaxDD *down*
  to DDnorm's 9; cannot take DDnorm *up*. The real side is simulated too (2,000 subsets), so
  the verdict's stability under m claims is measured.
- **BAR** — the claim bar is set to the outcome's own **m-th largest \|t_none\|**, so the count
  is exactly m by construction on the real grid and on each of the 400 draws separately. This
  is the only device that takes DDnorm *up* to MaxDD's 19, and it prints the bar it needed.

SUB drops null draws with fewer than m claims (`draws` column: 400 at m=4 down to **10** at
m=19), so its band at large m is conditioned on high-claim draws and reads optimistic for the
null. BAR has no such conditioning — 400 draws at every m. Where the two disagree, BAR is the
honest device; both are published.

## ANSWER — POWER. Idea 714's INSIDE verdict does not survive being given MaxDD's sample size

The four decision cells, pre-registered in the docstring:

| cell | real | own null band | verdict | excess | z | p_left |
|---|---|---|---|---|---|---|
| MaxDD native 19 (SUB) | 10.5% | [41.6%, 68.4%] med 55.3% | **BELOW** | −44.7% | −4.50 | 0.000 |
| MaxDD cut to 9 (SUB) | 10.5% | [22.2%, 74.4%] med 44.4% | BELOW, but **only 79.7%** of its own 9-claim subsamples read BELOW | −33.9% | −2.25 | 0.000 |
| DDnorm native 9 (BAR) | 22.2% | [22.2%, 77.8%] med 55.6% | INSIDE | −33.3% | −2.24 | 0.068 |
| **DDnorm taken up to 19 (BAR)** | **42.1%** | **[57.6%, 89.5%] med 73.7%** | **BELOW** | **−31.6%** | **−3.06** | **0.007** |

Three things follow.

1. **The published INSIDE is a count artefact.** Give DDnorm MaxDD's 19 claims and it reads
   BELOW its own band at p_left 0.007. On the BAR ladder DDnorm reads INSIDE at m = 4, 6, 9, 12
   and **BELOW at 15, 19, 24 and 28** — the verdict flips at the count, not at the normaliser.
2. **MaxDD's BELOW is count-fragile in the same direction.** On BAR at matched m = 9 MaxDD
   reads **INSIDE** (11.1% vs [11.1%, 55.6%], z −1.56, p_left 0.110), and at m = 4 and 6 both
   outcomes read INSIDE with excess exactly +0.0%. Neither edge reading is a property of the
   statistic at 9 claims; **this ladder cannot separate anything from its own null below about
   m = 12–15.**
3. **At matched count the two excesses coincide.** SUB m=9: MaxDD −33.9% vs DDnorm −33.3%,
   gap **−0.6 pp**. BAR m=12: −33.3% vs −33.3%, gap **exactly 0.0**. The native-count gap idea
   714 published is −35.0% vs −28.7% = **−6.3 pp**. What actually differs between the two rows
   is the **null band width**: 0.44–0.56 at m = 9 against 0.22–0.32 at m ≥ 19.

### The part that is NOT power

At m ≥ 15 MaxDD's excess stays more negative than DDnorm's (−0.467 / −0.474 / −0.542 / −0.536
against −0.333 / −0.316 / −0.375 / −0.357), a stable **−13 to −18 pp** residual. So vol-
normalising does shrink the shortfall by roughly a third — but it does **not** remove it. Idea
714's sentence *"once the drawdown is divided by the book's own vol, the separation from its own
band is gone"* is **false at matched count** and should be restated as: *the normaliser moves
the size of the shortfall, not its existence; the published disappearance was the loss of ten
claims.*

All 5 outcomes × 2 devices × 8 counts are in `.matched.csv`; the two focal outcomes are printed
in full in `.console.txt`. The three return outcomes are reported on the same ladder and show
the artefact running the **other** way: `Sharpe` and `CAGRnorm` read INSIDE at every m, while
**`CAGR` reads BELOW at m = 4, 6 and 9** (0/4, 0/6 and 2/9 survive at bars 5.09 / 4.49 / 4.18) and INSIDE
at every m ≥ 12, i.e. at its native 23 claims. A small-m reading is unreliable in both
directions; only the ≥ 12 rungs are worth quoting, and there the drawdown family is still the
only one that separates.

## Rule 8 walk-forward (PROTOCOL 8) — both legs, both at matched count

**CLAIM LEG** (fit on ≤2016-12-31 only, read once on 2017–2026; 12 cells per outcome):

| outcome | resid | IS claims (bar 1.960) | hold OOS | matched m=4 | m=8 | m=12 |
|---|---|---|---|---|---|---|
| MaxDD | none | 9 | 4 (44.4%) | 25.0% | 50.0% | 58.3% |
| MaxDD | logx | 4 | **0 (0.0%)** | 0.0% | 50.0% | 58.3% |
| DDnorm | none | 4 | **0 (0.0%)** | 0.0% | 62.5% | 58.3% |
| DDnorm | logx | 4 | **0 (0.0%)** | 0.0% | 50.0% | 41.7% |

Under the control, **neither** drawdown statistic has a claim that holds out of sample, and once
the count is matched the two are indistinguishable (m=8: 50.0% vs 50.0% logx) — the same power
reading from the out-of-sample side.

**BOOK LEG** (IS-only per-outcome `disp` selectors over the 168 panels, read once on OOS;
comparands on the same calendar RULES v2 OOS **+8.50% / 1.0734 / −12.53%**, SPY OOS
**+15.45% / 0.8820 / −33.72%**, G0-verified):

| selector | arms | OOS CAGR | OOS Sharpe | OOS MaxDD | beat anchor | beat v2 | beat SPY | 4a | 4b | median random-pick pct |
|---|---|---|---|---|---|---|---|---|---|---|
| SEL-S (argmax IS Sharpe) | 3 | 9.09–12.83% | 0.8262–0.9844 | −28.8…−15.8% | 3/3 | 0 | 1 | 0 | **1** | 73.4% |
| SEL-DISP-**MaxDD** (± and \|v) | 6 | −2.18–10.28% | −0.0439–0.6788 | −44.1…−23.4% | 1/6 | 0 | 0 | 0 | 0 | **1.8%** |
| SEL-DISP-**DDnorm** (± and \|v) | 6 | −2.18–11.53% | −0.0439–0.7995 | −44.1…−18.7% | 1/6 | 0 | 0 | 0 | 0 | **6.8%** |

Over all 15 picks: **beat the do-nothing anchor 5, beat RULES v2 0, beat SPY 1, 4a 0/15,
4b 1/15** — and that single 4b pass is `SEL-S` on EWall (OOS +12.13% / 0.9844 / −19.33%), the
record's own Sharpe selector, **not a disp selector**. Corpus reference 4a 0/504, 4b 41/504.
The normaliser changes the panel pick in **3 of 6** (arm × control) cells and buys nothing: both
drawdown-directed selectors sit in the bottom decile of 2,000 random picks. The MaxDD rows
reproduce idea 714's committed book leg exactly, which is a further consistency check on both
runs.

## Verdict

**ANSWERED / KILL of the normalisation reading. No KEEP (4a 0/15, 4b 1/15 and that pass is not a
disp selector), no memo.**

DDnorm's edge-of-band reading is a **power** fact. Matched to MaxDD's 19 claims it reads BELOW
its own band (42.1% vs [57.6%, 89.5%], p_left 0.007); matched to DDnorm's 9 claims MaxDD reads
INSIDE on the unconditioned device. The excesses agree to 0.6 pp at m=9 and exactly at m=12.
The residue that *is* the normaliser is a −13 to −18 pp difference in the size of the shortfall
at m ≥ 15, not its presence. The wider lesson for the record: on this ladder a survival share
over fewer than ~12 claims cannot be distinguished from its own permutation band at all, so
**every INSIDE verdict in the corpus quoted at a small claim count is uninformative, not
negative** — and two outcomes compared at different counts were never comparable.

**SURVIVORSHIP** (idea 54, `data/SMALL_PANEL_README.md`): both ends of the q ladder are current
constituents of their screens, so every level inherited here is optimistic. The object under
test is a within-stratum slope under a control and a selector's OOS ranking, neither of which is
a level claim. No book here is a capital candidate.

## Follow-ups filed

- **721** — publish a MINIMUM CLAIM COUNT beside every permutation-band verdict in the record.
- **722** — how many published INSIDE / "not distinguishable from the null" verdicts are quoted
  at a claim count below their own ladder's separation floor?
- **723** — is the −13 to −18 pp residual excess gap at matched count the vol channel itself?
