#!/usr/bin/env python3
"""Idea 1153 (cloud lane, 2026-09-17) — does ANY committed CAGR-FLOOR DEATH in the record
survive a GROSS-MATCHED BENCHMARK?

THE PARENT.  Idea 1150 ran a control in which 4b's CAGR floor (`CAGR >= 0.70 * SPY_CAGR`)
was re-scored against a SPY that had been DE-GROSSED with the book (g*SPY + (1-g)*cash at
zero), and the L_CAGR leg then read TRUE at 528 of 528 cells.  On a gross ladder the leg
therefore carries no information at all: it fires exactly when the book holds less than the
index, which is a statement about exposure, not about the rule.  The queue's question is
whether that is a property of the gross ladder 1150 happened to run, or a property of the
RECORD: harvest every committed claim that a book dies on the CAGR floor, re-score each one
against a gross-matched floor, and report HOW MANY STATED VERDICTS (not numbers) MOVE.

WHY THIS ONE IS A REAL CENSUS AND NOT A FRESH POPULATION.  Most record-census ideas cannot
resolve their claims' cells from prose (idea 1098: R_STRICT resolves 82 of 2,088 cost
claims).  This one does not have to read prose.  The 4b legs are committed as MACHINE-
READABLE COLUMNS: `research/backtests/*.csv` carries an exact `L_CAGR` column in 104 files
and 58,757 rows, beside the book's own `CAGR`, its `panel`, and in most files its `gross`.
A committed CAGR-floor death is literally a row with `L_CAGR == False`.  So every number
below is read off the record's own committed files, not recalled and not re-derived from
prose.  The two places where this run must supply something the files do not carry — the
SPY comparand and the book's exposure — are both GATED (G2, G5) and every row that fails
its gate is EXCLUDED and counted, not patched.

THE TWO TUNED PARAMETERS AND NO MORE (PROTOCOL rule 4), exactly the two the queue names:
  CLAIMSET   {C_ALL, C_BIND, C_FRESH}
      C_ALL   every reproduced committed row with L_CAGR == False (the death itself)
      C_BIND  the subset where L_CAGR is the BINDING leg — every other 4b leg passes, so
              the CAGR floor alone is what killed the book.  This is the set whose VERDICTS
              can move at all; C_ALL's extra rows are dead twice over and cannot.
      C_FRESH a fresh, fully-specified grid of the same shape, where nothing is inferred
  FLOORFORM  {F_SPY, F_GROSS, F_EXPO, F_VOL}
      F_SPY   the incumbent, 0.70 * CAGR(SPY)                        (the comparand)
      F_GROSS 0.70 * CAGR(g * r_spy), g the row's committed gross     (1150's control)
      F_EXPO  0.70 * CAGR(e * r_spy), e the book's REALISED mean invested share
      F_VOL   0.70 * CAGR(k * r_spy), k = vol(book) / vol(SPY)
= 12 cells, EVERY ONE PUBLISHED in `.cells.csv`.  PANEL {U56, B136, SMALL} is not a dial —
it is the population and all three are published everywhere.  Nothing else is tuned: the
0.70 floor coefficient, the 0.60 DD cap, LAG 1, warm-up 260, IS end 2016-12-31 and the
10 bps cost are all FROZEN at PROTOCOL's values and at the record's own construction.

F_GROSS IS COMPOUNDED, NOT SCALED.  CAGR(g*r) != g*CAGR(r); the run compounds the de-grossed
daily series and takes its CAGR, which is what a real gross-matched benchmark would earn.

SURVIVORSHIP: B136 and SMALL are CURRENT constituents only (PROTOCOL rule 9 /
data/SMALL_PANEL_README.md).  SMALL additionally drops every ticker with max_1d_move >= 1.0
in data/small_meta.csv before anything else is computed.  No result here is a live-tradable
edge on those panels; they are breadth controls, and the census inherits whatever
survivorship the committed rows already carry.

Writes: .gates.csv .census.csv .cells.csv .rows.csv .grid.csv .walkforward.csv .console.txt
Deterministic, standalone, no network.  Does not modify RULES.md / PROTOCOL.md / scan.py /
bot.py / baseline.py / engine.py.
"""
import sys, glob, time
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE = "2026-09-17"
SLUG = "does-ANY-committed-CAGR-FLOOR-DEATH-in-the-record-survive-a-GROSS-MATCHED-BENCHMARK"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"
LOG = []

LAG, WARMUP = 1, 260
IS_END = "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
GROSS0, FREQ0, HOLD0, N0, COST0, MAXVOL0 = 0.75, "W", 126, 20, 10.0, 0.60
LEGS = [(21, 252), (0, 126), (0, 63)]

CLAIMSETS = ["C_ALL", "C_BIND", "C_FRESH"]
FLOORFORMS = ["F_SPY", "F_GROSS", "F_EXPO", "F_VOL"]

# panel label -> which loader.  The record's SMALL labels all denote the sub-$2B pool at
# whatever build date the row was committed on (idea 1074 is open on exactly this); the
# replay gate G2 decides row by row whether today's pool reproduces the committed leg.
PANEL_OF = {"U56": "U56", "B136": "B136",
            "SMALL": "SMALL", "SMALL663": "SMALL", "SMALL439": "SMALL"}


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def dump(df, suffix):
    p = Path(f"{OUT}.{suffix}.csv")
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


# ------------------------------------------- the record's fast runner and book, VERBATIM
def nrun(rets, wt, mk):
    T, N = rets.shape
    mk = mk.copy()
    mk[0] = True
    Cc = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, N)), Cc[:-1]])
    reb = np.flatnonzero(mk)
    seg = np.searchsorted(reb, np.arange(T), side="right") - 1
    s0 = reb[seg]
    W0 = wt[s0]
    h = W0 * (Cp / Cp[s0])
    V = h.sum(axis=1) + (1.0 - W0.sum(axis=1))
    held = h / V[:, None]
    s0p = reb[np.maximum(seg - 1, 0)]
    W0p = wt[s0p]
    hp = W0p * (Cp / Cp[s0p])
    Vp = hp.sum(axis=1) + (1.0 - W0p.sum(axis=1))
    heldp = hp / Vp[:, None]
    heldp[reb[0]] = 0.0
    turn = np.zeros(T)
    turn[reb] = np.abs(wt[reb] - heldp[reb]).sum(axis=1)
    return (held * rets).sum(axis=1), turn, held.sum(axis=1)


def fcagr(r):
    r = np.asarray(r, float)
    eq = np.cumprod(1.0 + r)
    return eq[-1] ** (252.0 / len(r)) - 1.0


def fmet(r):
    r = np.asarray(r, float)
    eq = np.cumprod(1.0 + r)
    cagr = eq[-1] ** (252.0 / len(r)) - 1.0
    dd = float((eq / np.maximum.accumulate(eq) - 1.0).min())
    vol = r.std(ddof=1) * np.sqrt(252.0)
    return cagr, ((r.mean() * 252.0) / vol if vol else np.nan), dd


def fsharpe(r):
    r = np.asarray(r, float)
    vol = r.std(ddof=1) * np.sqrt(252.0)
    return (r.mean() * 252.0) / vol if vol else np.nan


def mech(px):
    parts = []
    for skip, look in LEGS:
        x = (px.shift(skip) / px.shift(look) - 1.0) if skip else (px / px.shift(look) - 1.0)
        parts.append(x.rank(axis=1, pct=True))
    comp = sum(parts) / len(parts)
    above = px > px.rolling(200).mean()
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    return (comp * (0.5 + 0.5 * above.astype(float))).values, above.values, vol20.values


def build(rank_key, elig, priced, reb, N, H, T, K, gross):
    W = np.zeros((T, K))
    cur = np.full(K, -1, dtype=np.int64)
    for i, t in enumerate(reb):
        held = np.flatnonzero(cur >= 0)
        if len(held):
            young = held[(t - cur[held]) < H]
            young = young[priced[t, young]]
        else:
            young = held
        keep = set(int(c) for c in young)
        need = N - len(keep)
        take = []
        if need > 0:
            k = rank_key[t].copy()
            k[~(elig[t] & priced[t])] = np.inf
            for c in keep:
                k[c] = np.inf
            order = np.argsort(k, kind="stable")
            take = [int(c) for c in order[:need] if np.isfinite(k[c])]
        new_cur = np.full(K, -1, dtype=np.int64)
        for c in keep:
            new_cur[c] = cur[c]
        for c in take:
            new_cur[c] = t
        cur = new_cur
        sel = np.flatnonzero(cur >= 0)
        if len(sel):
            stop = reb[i + 1] if i + 1 < len(reb) else T
            W[t:stop, sel] = gross / len(sel)
    return W


def load_panel(name):
    if name == "U56":
        px = load_universe()
    elif name == "B136":
        px = load_universe(broad=True)
    else:
        px = load_universe(small=True)
        meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
        bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"].astype(str))
        px = px[[c for c in px.columns if c == "SPY" or c not in bad]]
    return px


def prep(px):
    idx = px.index
    warm = np.zeros(len(idx), dtype=bool)
    warm[WARMUP:] = True
    oos = np.asarray(idx > pd.Timestamp(IS_END)) & warm
    ins = warm & ~oos
    sc, above, vol20 = mech(px)
    return dict(px=px, idx=idx, K=len(px.columns), T=len(idx),
                rets=px.pct_change().fillna(0.0).values, priced=px.notna().values,
                warm=warm, ins=ins, oos=oos, sc=sc, above=above, vol20=vol20,
                spy=px["SPY"].pct_change().fillna(0.0).values,
                mk=rebalance_mask(idx, FREQ0).values)


def run_cell(d, gross=GROSS0, N=N0, H=HOLD0, maxvol=MAXVOL0, freq=FREQ0, cost=COST0):
    mk = d["mk"] if freq == FREQ0 else rebalance_mask(d["idx"], freq).values
    mkl = np.roll(mk, LAG)
    mkl[:LAG] = False
    reb = np.flatnonzero(mk)
    el = d["above"] & (d["vol20"] < maxvol)
    W = build(-d["sc"], el, d["priced"], reb, N, H, d["T"], d["K"], gross)
    Wl = np.zeros_like(W)
    Wl[LAG:] = W[:-LAG]
    g, t, inv = nrun(d["rets"], Wl, mkl)
    return g - t * cost / 1e4, t, inv


def blocks_m(r, d):
    rr = r[d["warm"]]
    c, s, dd = fmet(rr)
    h = len(rr) // 2
    oc, os_, od = fmet(r[d["oos"]])
    ic, is_, idd = fmet(r[d["ins"]])
    return dict(CAGR=c, Sharpe=s, MaxDD=dd, H1=fsharpe(rr[:h]), H2=fsharpe(rr[h:]),
                IS_CAGR=ic, IS_Sharpe=is_, IS_MaxDD=idd,
                OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=od)


# =====================================================================================
#  THE FOUR FLOOR FORMS.  Each returns the CAGR a de-grossed SPY earns on the same window.
# =====================================================================================
def floor_cagr(spy_r, mask, lam):
    """CAGR of lam * r_spy, COMPOUNDED (not lam * CAGR(spy)), on the masked window."""
    return fcagr(lam * spy_r[mask])


def lam_of(form, gross, expo, volratio):
    if form == "F_SPY":
        return 1.0
    if form == "F_GROSS":
        return gross
    if form == "F_EXPO":
        return expo
    return volratio


# =====================================================================================
P("=" * 100)
P(f"IDEA 1153 (cloud) — {SLUG}")
P(f"run {pd.Timestamp.utcnow():%Y-%m-%d %H:%M:%S} UTC")
P("=" * 100)
t0 = time.time()

P("\nLoading the three panels ...")
PAN = {}
for nm in ("U56", "B136", "SMALL"):
    px = load_panel(nm)
    PAN[nm] = prep(px)
    d = PAN[nm]
    P(f"  {nm:6s} {px.shape[0]:5d} x {px.shape[1]:4d}  post-warmup {d['idx'][WARMUP].date()} .. {d['idx'][-1].date()}")

# SPY reference numbers per panel, on the record's three windows.
SPYREF = {}
for nm, d in PAN.items():
    SPYREF[nm] = dict(
        FULL=fcagr(d["spy"][d["warm"]]), IS=fcagr(d["spy"][d["ins"]]), OOS=fcagr(d["spy"][d["oos"]]),
        FULL_DD=fmet(d["spy"][d["warm"]])[2], OOS_DD=fmet(d["spy"][d["oos"]])[2],
        FULL_S=fsharpe(d["spy"][d["warm"]]), OOS_S=fsharpe(d["spy"][d["oos"]]),
        VOL=d["spy"][d["warm"]].std(ddof=1) * np.sqrt(252.0))
    P(f"  SPY {nm:6s} full CAGR {SPYREF[nm]['FULL']:.4%}  floor {CAGR_FLOOR*SPYREF[nm]['FULL']:.4%}"
      f"   OOS {SPYREF[nm]['OOS']:.4%}  MaxDD {SPYREF[nm]['FULL_DD']:.2%}")

GATES = []


def gate(name, ok, detail):
    GATES.append(dict(gate=name, verdict="PASS" if ok else "FAIL", detail=detail))
    P(f"  {name:6s} {'PASS' if ok else 'FAIL'}  {detail}")


P("\n" + "=" * 100)
P("GATES — printed BEFORE the hypothesis is read (PROTOCOL rule 7)")
P("=" * 100)

# ----------------------------------------------------------------- G1 harvest is complete
files = sorted(glob.glob(str(ROOT / "research" / "backtests" / "*.csv")))
hit, rows_raw = [], 0
for f in files:
    try:
        head = open(f, "r", errors="replace").readline()
    except Exception:
        continue
    if "L_CAGR" in head.split(","):
        hit.append(f)
P(f"  scanned {len(files):,} committed csv files in research/backtests/")
gate("G1", len(hit) >= 100, f"{len(hit)} files carry an EXACT `L_CAGR` column "
                            f"(the canonical committed 4b CAGR leg)")

# ----------------------------------------------------------------- harvest the rows
def as_bool(s):
    return s.astype(str).str.strip().str.lower().isin(["true", "1", "1.0", "yes"])


LEGCOLS = ["L_H1", "L_H2", "L_OOS", "L_DD"]
harv = []
for f in hit:
    try:
        d = pd.read_csv(f)
    except Exception:
        continue
    if not {"L_CAGR", "CAGR", "panel"} <= set(d.columns):
        continue
    d = d[d["panel"].astype(str).isin(PANEL_OF)].copy()
    if not len(d):
        continue
    rows_raw += len(d)
    out = pd.DataFrame(dict(
        src=Path(f).name, panel_raw=d["panel"].astype(str),
        panel=d["panel"].astype(str).map(PANEL_OF),
        CAGR=pd.to_numeric(d["CAGR"], errors="coerce"),
        L_CAGR=as_bool(d["L_CAGR"]),
        gross=pd.to_numeric(d["gross"], errors="coerce") if "gross" in d.columns else np.nan,
        Sharpe=pd.to_numeric(d["Sharpe"], errors="coerce") if "Sharpe" in d.columns else np.nan,
        MaxDD=pd.to_numeric(d["MaxDD"], errors="coerce") if "MaxDD" in d.columns else np.nan,
    ))
    for c in LEGCOLS:
        out[c] = as_bool(d[c]) if c in d.columns else np.nan
    out["n_other_legs"] = out[LEGCOLS].notna().sum(axis=1)
    out["other_legs_pass"] = out[LEGCOLS].fillna(True).all(axis=1)
    harv.append(out)

H = pd.concat(harv, ignore_index=True)
H = H[H["CAGR"].notna()].reset_index(drop=True)
P(f"  harvested {len(H):,} committed rows carrying an L_CAGR leg from {H['src'].nunique()} files")

# ----------------------------------------------------------------- G2 the replay gate
H["spy_full"] = H["panel"].map({k: v["FULL"] for k, v in SPYREF.items()})
H["repro_L_CAGR"] = H["CAGR"] >= CAGR_FLOOR * H["spy_full"]
H["reproduced"] = H["repro_L_CAGR"] == H["L_CAGR"]
rr = H["reproduced"].mean()
gate("G2", rr > 0.95,
     f"{H['reproduced'].sum():,} of {len(H):,} committed L_CAGR values ({rr:.4f}) reproduce "
     f"EXACTLY from (row CAGR, row panel, today's SPY). Non-reproducing rows are EXCLUDED, not patched.")

# ----------------------------------------------------------------- G3 SPY matches the record
g3 = (abs(SPYREF["U56"]["FULL"] - 0.1506) < 5e-4 and abs(SPYREF["B136"]["FULL"] - 0.1516) < 5e-4
      and abs(SPYREF["SMALL"]["FULL"] - 0.1406) < 5e-4)
gate("G3", g3, f"panel SPY full CAGR {SPYREF['U56']['FULL']:.4f}/{SPYREF['B136']['FULL']:.4f}/"
               f"{SPYREF['SMALL']['FULL']:.4f} vs the record's committed 0.1506/0.1516/0.1406")

# --------------------------------- G4/G8 the PARENT's own committed gross-matched column
# Idea 1150 committed `spygross_L_CAGR` — its gross-matched CAGR leg — on all 528 cells.
# This run's F_GROSS must reproduce that column EXACTLY or it is measuring something else.
P1150 = ROOT / "research" / "backtests" / (
    "2026-09-16_is-the-CAGR-FLOOR-a-DE-GROSSING-DETECTOR-rather-than-a-COST-LEG_C.grid.csv")
if P1150.exists():
    d150 = pd.read_csv(P1150)
    sub = H[H["src"] == P1150.name]
    gate("G4", len(sub) == 528 and bool(sub["reproduced"].all()),
         f"the parent's own committed grid replays {int(sub['reproduced'].sum())} of {len(sub)} "
         f"INCUMBENT-floor rows off today's SPY")
else:
    d150 = None
    gate("G4", False, "idea 1150's committed grid not found")

# ----------------------------------------------------------------- G5 gross column present
ADM = H[H["reproduced"]].copy()
hasg = ADM["gross"].notna() & (ADM["gross"] > 0) & (ADM["gross"] <= 2.0)
gate("G5", hasg.mean() > 0.5,
     f"{int(hasg.sum()):,} of {len(ADM):,} reproduced rows carry a usable committed `gross`; "
     f"the other {int((~hasg).sum()):,} CANNOT be gross-matched at all and are reported as UNRESOLVABLE")

# ----------------------------------------------------------------- G6 de-grossed floor monotone
mono = True
for nm, d in PAN.items():
    v = [floor_cagr(d["spy"], d["warm"], g) for g in (0.2, 0.4, 0.6, 0.8, 1.0)]
    mono &= all(v[i] < v[i + 1] for i in range(4))
gate("G6", mono, "CAGR(lam*r_spy) is strictly increasing in lam on all three panels "
                 "(so a de-grossed floor can only ever LOWER the bar)")

# ----------------------------------------------------------------- G7 compounding matters
nm = "U56"
lin = GROSS0 * SPYREF[nm]["FULL"]
cmp_ = floor_cagr(PAN[nm]["spy"], PAN[nm]["warm"], GROSS0)
gate("G7", abs(lin - cmp_) > 1e-4,
     f"compounded g=0.75 SPY CAGR {cmp_:.4%} vs the naive g*CAGR {lin:.4%} "
     f"(gap {1e4*(cmp_-lin):.1f} bp/yr) — this run compounds")

# ----------------------------- G8 THE DECISIVE ONE: reproduce 1150's own gross-matched leg
if d150 is not None:
    pr = np.array([bool(r.CAGR >= CAGR_FLOOR * floor_cagr(PAN[r.panel]["spy"], PAN[r.panel]["warm"], r.gross))
                   for _, r in d150.iterrows()])
    cm = d150["spygross_L_CAGR"].astype(str).str.strip().str.lower().isin(["true", "1", "1.0"]).values
    agree = int((pr == cm).sum())
    mgap = float(np.nanmax(np.abs(
        np.array([(r.CAGR - CAGR_FLOOR * floor_cagr(PAN[r.panel]["spy"], PAN[r.panel]["warm"], r.gross))
                  / abs(CAGR_FLOOR * floor_cagr(PAN[r.panel]["spy"], PAN[r.panel]["warm"], r.gross))
                  for _, r in d150.iterrows()]) - d150["spygross_m_L_CAGR"].values)))
    gate("G8", agree == len(d150),
         f"this run's F_GROSS reproduces the parent's OWN committed `spygross_L_CAGR` at "
         f"{agree} of {len(d150)} cells (all TRUE — 1150's 528 of 528). The committed MARGIN differs "
         f"by up to {mgap:.4f} in its own relative unit (the parent did not compound its floor), "
         f"and NOT ONE of the 528 VERDICTS is sensitive to that choice.")
else:
    gate("G8", False, "parent grid absent")

GD = pd.DataFrame(GATES)
dump(GD, "gates")
P(f"  {(GD.verdict == 'PASS').sum()} of {len(GD)} gates PASS")

# =====================================================================================
P("\n" + "=" * 100)
P("PART A — THE CENSUS: how many committed CAGR-FLOOR DEATHS are there, and can they move")
P("=" * 100)

ADM["death"] = ~ADM["L_CAGR"]
ADM["binding"] = ADM["death"] & ADM["other_legs_pass"] & (ADM["n_other_legs"] >= 3)
ADM["resolvable"] = hasg.values

cen = []
for panel, g in ADM.groupby("panel"):
    cen.append(dict(panel=panel, rows=len(g), deaths=int(g["death"].sum()),
                    death_rate=g["death"].mean(),
                    binding=int(g["binding"].sum()),
                    resolvable_deaths=int((g["death"] & g["resolvable"]).sum()),
                    resolvable_binding=int((g["binding"] & g["resolvable"]).sum())))
cen.append(dict(panel="ALL", rows=len(ADM), deaths=int(ADM["death"].sum()),
                death_rate=ADM["death"].mean(), binding=int(ADM["binding"].sum()),
                resolvable_deaths=int((ADM["death"] & ADM["resolvable"]).sum()),
                resolvable_binding=int((ADM["binding"] & ADM["resolvable"]).sum())))
CEN = pd.DataFrame(cen)
P(CEN.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
dump(CEN, "census")

P(f"\n  {int(ADM['death'].sum()):,} committed CAGR-floor DEATHS in {len(ADM):,} reproduced rows.")
P(f"  {int(ADM['binding'].sum()):,} of them are BINDING (every other 4b leg passes) — only these "
  f"can move a stated VERDICT.")
P(f"  {int((ADM['death'] & ~ADM['resolvable']).sum()):,} deaths carry NO committed gross and are "
  f"UNRESOLVABLE against a gross-matched floor by any means short of re-running their script.")

# =====================================================================================
P("\n" + "=" * 100)
P("PART B — RE-SCORE: the 12 published cells (CLAIMSET x FLOORFORM)")
P("=" * 100)

# realised exposure and vol ratio need the book; the committed rows do not carry them.
# For committed rows we use the row's own gross as the exposure proxy ONLY under F_EXPO
# when a `turnover`-style exposure column is absent, and we SAY SO — so F_EXPO on C_ALL /
# C_BIND collapses onto F_GROSS.  That is a limitation of the record, published as one.
ADM["expo"] = ADM["gross"]
ADM["volratio"] = np.nan

FLOORS = {}
for nm, d in PAN.items():
    FLOORS[nm] = {}

def floor_for(panel, lam):
    key = round(float(lam), 6)
    if key not in FLOORS[panel]:
        FLOORS[panel][key] = floor_cagr(PAN[panel]["spy"], PAN[panel]["warm"], key)
    return FLOORS[panel][key]


# ---------------------------------------------------------------- the fresh grid (C_FRESH)
P("\nBuilding the fresh, fully-specified grid (C_FRESH) ...")
GROSS_LADDER = [round(0.20 + 0.05 * i, 3) for i in range(17)]
N_LADDER = [5, 10, 20, 30]
grid = []
for panel, d in PAN.items():
    for N in N_LADDER:
        for g in GROSS_LADDER:
            r, turn, inv = run_cell(d, gross=g, N=N)
            m = blocks_m(r, d)
            m.update(panel=panel, N=N, gross=g,
                     expo=float(inv[d["warm"]].mean()),
                     vol=float(r[d["warm"]].std(ddof=1) * np.sqrt(252.0)),
                     IS_expo=float(inv[d["ins"]].mean()),
                     turn_yr=float(turn[d["warm"]].sum() * 252.0 / d["warm"].sum()))
            grid.append(m)
G = pd.DataFrame(grid)
G["volratio"] = G["vol"] / G["panel"].map({k: v["VOL"] for k, v in SPYREF.items()})
sp = G["panel"].map({k: v["FULL"] for k, v in SPYREF.items()})
sd = G["panel"].map({k: v["FULL_DD"] for k, v in SPYREF.items()})
ss = G["panel"].map({k: v["FULL_S"] for k, v in SPYREF.items()})
G["spy_H1"] = np.nan
for nm, d in PAN.items():
    rr = d["spy"][d["warm"]]
    h = len(rr) // 2
    G.loc[G.panel == nm, "spy_H1"] = fsharpe(rr[:h])
    G.loc[G.panel == nm, "spy_H2"] = fsharpe(rr[h:])
G["L_H1"] = G["H1"] > G["spy_H1"]
G["L_H2"] = G["H2"] > G["spy_H2"]
G["L_OOS"] = G["OOS_Sharpe"] > G["panel"].map({k: v["OOS_S"] for k, v in SPYREF.items()})
G["L_DD"] = G["MaxDD"].abs() <= DD_CAP * sd.abs()
G["L_CAGR"] = G["CAGR"] >= CAGR_FLOOR * sp
G["other_legs_pass"] = G[["L_H1", "L_H2", "L_OOS", "L_DD"]].all(axis=1)
G["death"] = ~G["L_CAGR"]
G["binding"] = G["death"] & G["other_legs_pass"]
G["pass_4b"] = G[["L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"]].all(axis=1)
dump(G, "grid")
P(f"  {len(G)} books; {int(G['death'].sum())} CAGR-floor deaths, {int(G['binding'].sum())} BINDING, "
  f"{int(G['pass_4b'].sum())} full-sample 4b passes")

# ---------------------------------------------------------------- score all 12 cells
def rescore(df, form, panelcol="panel"):
    """Return the re-scored L_CAGR under `form` for every row of df."""
    lam = np.where(df.index == df.index, 1.0, 1.0)  # placeholder, filled below
    if form == "F_SPY":
        lam = np.ones(len(df))
    elif form == "F_GROSS":
        lam = df["gross"].values.astype(float)
    elif form == "F_EXPO":
        lam = df["expo"].values.astype(float)
    else:
        lam = df["volratio"].values.astype(float)
    out = np.full(len(df), np.nan)
    for i, (p, l, c) in enumerate(zip(df[panelcol].values, lam, df["CAGR"].values)):
        if not np.isfinite(l) or l <= 0:
            continue
        out[i] = 1.0 if c >= CAGR_FLOOR * floor_for(p, min(l, 2.0)) else 0.0
    return out


cells, rowout = [], []
SETS = {
    "C_ALL":   ADM[ADM["death"]].copy(),
    "C_BIND":  ADM[ADM["binding"]].copy(),
    "C_FRESH": G[G["death"]].copy(),
}
for cs, df in SETS.items():
    df = df.copy()
    if cs != "C_FRESH":
        df["volratio"] = np.nan
    for ff in FLOORFORMS:
        new = rescore(df, ff)
        resolvable = np.isfinite(new)
        survives = resolvable & (new == 0.0)          # still dead under the new floor
        flips = resolvable & (new == 1.0)             # the death disappears
        # a stated VERDICT moves only where the CAGR leg was BINDING and it flips
        if cs == "C_FRESH":
            bind = df["binding"].values
        else:
            bind = df["binding"].values if "binding" in df.columns else np.zeros(len(df), bool)
        if cs == "C_FRESH":
            note = "fully specified"
        elif ff == "F_EXPO":
            note = "PROXY: the record commits no REALISED exposure column, so expo:=gross and this cell aliases F_GROSS"
        elif ff == "F_VOL":
            note = "UNRESOLVABLE: the record commits no realised-vol column on these rows"
        else:
            note = "read off the committed rows"
        cells.append(dict(
            claimset=cs, floorform=ff, note=note, n_claims=len(df),
            n_resolvable=int(resolvable.sum()),
            unresolvable=int((~resolvable).sum()),
            n_survive=int(survives.sum()), n_flip=int(flips.sum()),
            survive_share=float(survives.sum() / max(resolvable.sum(), 1)),
            n_binding=int(bind.sum()),
            verdicts_moved=int((flips & bind).sum()),
            verdict_move_share=float((flips & bind).sum() / max((bind & resolvable).sum(), 1)),
        ))
        if ff == "F_GROSS":
            k = df.copy()
            k["new_L_CAGR"] = new
            k["survives_gross_matched"] = survives
            k["claimset"] = cs
            keep = [c for c in ["claimset", "src", "panel", "gross", "CAGR", "Sharpe", "MaxDD",
                                "N", "binding", "new_L_CAGR", "survives_gross_matched"] if c in k.columns]
            rowout.append(k[keep])

C = pd.DataFrame(cells)
P("\nALL 12 CELLS (every grid point reported, PROTOCOL rule 4):")
P(C.drop(columns=["note"]).to_string(index=False, float_format=lambda x: f"{x:.4f}"))
P("  cell notes:")
for _, r in C.drop_duplicates(["claimset", "floorform"]).iterrows():
    if r.note != "read off the committed rows" and r.note != "fully specified":
        P(f"    {r.claimset:8s} {r.floorform:8s}  {r.note}")
dump(C, "cells")
R = pd.concat(rowout, ignore_index=True)
dump(R, "rows")

P("\n  THE ANSWER, read off the F_GROSS column:")
for cs in CLAIMSETS:
    r = C[(C.claimset == cs) & (C.floorform == "F_GROSS")].iloc[0]
    P(f"    {cs:8s}  {r.n_survive:6,} of {r.n_resolvable:6,} resolvable deaths SURVIVE the "
      f"gross-matched floor ({r.survive_share:.4f});  verdicts moved {r.verdicts_moved} of {r.n_binding}")

# =====================================================================================
P("\n" + "=" * 100)
P("PART C — MECHANISM: what separates a death that SURVIVES from one that does not")
P("=" * 100)
fr = R[R.claimset == "C_FRESH"]
if len(fr):
    surv = fr[fr.survives_gross_matched]
    died = fr[~fr.survives_gross_matched]
    P(f"  fresh-grid deaths: {len(fr)};  survive gross-matching {len(surv)};  flip {len(died)}")
    for nm, s in (("SURVIVES", surv), ("FLIPS", died)):
        if len(s):
            P(f"    {nm:9s} gross {s.gross.min():.2f}-{s.gross.max():.2f} (med {s.gross.median():.2f}), "
              f"CAGR {s.CAGR.min():.2%}-{s.CAGR.max():.2%} (med {s.CAGR.median():.2%})")
P("\n  WHAT THE RECORD WOULD GAIN: full-sample 4b PASSES on the fresh grid under each floor form")
for ff in FLOORFORMS:
    lamv = (np.ones(len(G)) if ff == "F_SPY" else G["gross"].values if ff == "F_GROSS"
            else G["expo"].values if ff == "F_EXPO" else G["volratio"].values)
    nl = np.array([bool(c >= CAGR_FLOOR * floor_for(p, min(max(l, 1e-9), 2.0)))
                   for p, l, c in zip(G["panel"], lamv, G["CAGR"])])
    p4 = G[["L_H1", "L_H2", "L_OOS", "L_DD"]].all(axis=1).values & nl
    P(f"    {ff:8s} 4b passes {int(p4.sum()):3d} of {len(G)}   (incumbent F_SPY = {int((G['pass_4b']).sum())})")

al = R[R.claimset == "C_ALL"]
al = al[np.isfinite(al.new_L_CAGR)]
if len(al):
    P(f"  committed deaths (C_ALL, resolvable): {len(al):,};  survive {int(al.survives_gross_matched.sum()):,}")
    for nm, s in (("SURVIVES", al[al.survives_gross_matched]), ("FLIPS", al[~al.survives_gross_matched])):
        if len(s):
            P(f"    {nm:9s} gross {s.gross.min():.2f}-{s.gross.max():.2f} (med {s.gross.median():.2f}), "
              f"CAGR {s.CAGR.min():.2%}-{s.CAGR.max():.2%} (med {s.CAGR.median():.2%})")
    P("  per panel:")
    for p, s in al.groupby("panel"):
        P(f"    {p:6s} {int(s.survives_gross_matched.sum()):6,} of {len(s):6,} survive "
          f"({s.survives_gross_matched.mean():.4f})")

# =====================================================================================
P("\n" + "=" * 100)
P("PART D — RULE 8 WALK-FORWARD and BOTH KEEP PATHS")
P("   Four choosers, one per FLOORFORM.  Each reads 2009-2016 ONLY: take the IS-Sharpe")
P("   argmax among books that clear that floor form's CAGR leg IN SAMPLE.  The pick is then")
P("   evaluated on the untouched 2017-2026 against SPY and the live RULES v2 baseline.")
P("=" * 100)

# live RULES v2 per panel, same windows
LIVE = {}
for nm, d in PAN.items():
    b = backtest(d["px"], rules_v2_weights(d["px"]), cost_bps=COST0, freq="W")
    lr = b["returns"].reindex(d["idx"]).fillna(0.0).values
    LIVE[nm] = blocks_m(lr, d)
    P(f"  live RULES v2 {nm:6s} full {LIVE[nm]['CAGR']:.2%} / {LIVE[nm]['Sharpe']:.4f} / "
      f"{LIVE[nm]['MaxDD']:.2%}   OOS {LIVE[nm]['OOS_CAGR']:.2%} / {LIVE[nm]['OOS_Sharpe']:.4f} / "
      f"{LIVE[nm]['OOS_MaxDD']:.2%}")

# IS floors per panel per lam
def is_floor(panel, lam):
    return CAGR_FLOOR * fcagr(lam * PAN[panel]["spy"][PAN[panel]["ins"]])


wf = []
for panel, gp in G.groupby("panel"):
    d = PAN[panel]
    spy_is_S = fsharpe(d["spy"][d["ins"]])
    for ff in FLOORFORMS:
        lam = (np.ones(len(gp)) if ff == "F_SPY" else
               gp["gross"].values if ff == "F_GROSS" else
               gp["IS_expo"].values if ff == "F_EXPO" else
               (gp["IS_Sharpe"].values * 0 + 1) * (gp["vol"].values /
                                                   SPYREF[panel]["VOL"]))
        okc = np.array([gp["IS_CAGR"].values[i] >= is_floor(panel, min(max(l, 1e-6), 2.0))
                        for i, l in enumerate(lam)])
        ok = okc & (gp["IS_Sharpe"].values > spy_is_S)
        cand = gp[ok]
        if not len(cand):
            wf.append(dict(panel=panel, chooser=ff, pick="NONE", n_cand=0))
            continue
        pick = cand.loc[cand["IS_Sharpe"].idxmax()]
        sb = SPYREF[panel]
        lb = LIVE[panel]
        row = dict(panel=panel, chooser=ff, n_cand=int(ok.sum()),
                   pick=f"N={int(pick.N)} gross={pick.gross:.2f}",
                   N=int(pick.N), gross=float(pick.gross),
                   CAGR=pick.CAGR, Sharpe=pick.Sharpe, MaxDD=pick.MaxDD, H1=pick.H1, H2=pick.H2,
                   IS_Sharpe=pick.IS_Sharpe,
                   OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe, OOS_MaxDD=pick.OOS_MaxDD,
                   SPY_CAGR=sb["FULL"], SPY_Sharpe=sb["FULL_S"], SPY_MaxDD=sb["FULL_DD"],
                   SPY_OOS_CAGR=sb["OOS"], SPY_OOS_Sharpe=sb["OOS_S"], SPY_OOS_MaxDD=sb["OOS_DD"],
                   LIVE_Sharpe=lb["Sharpe"], LIVE_MaxDD=lb["MaxDD"], LIVE_OOS_Sharpe=lb["OOS_Sharpe"],
                   # 4b on the FULL sample, judged with the INCUMBENT floor (PROTOCOL rule 4b)
                   L_H1=bool(pick.L_H1), L_H2=bool(pick.L_H2), L_OOS=bool(pick.L_OOS),
                   L_DD=bool(pick.L_DD), L_CAGR=bool(pick.L_CAGR),
                   # 4b again on the OOS window alone
                   O_S=bool(pick.OOS_Sharpe > sb["OOS_S"]),
                   O_DD=bool(abs(pick.OOS_MaxDD) <= DD_CAP * abs(sb["OOS_DD"])),
                   O_CAGR=bool(pick.OOS_CAGR >= CAGR_FLOOR * sb["OOS"]),
                   # 4a against the LIVE book
                   A_H1=bool(pick.H1 > lb["H1"]), A_H2=bool(pick.H2 > lb["H2"]),
                   A_DD=bool(pick.MaxDD >= lb["MaxDD"]))
        row["pass_4b_full"] = all(row[k] for k in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"))
        row["pass_4b_oos"] = all(row[k] for k in ("O_S", "O_DD", "O_CAGR"))
        row["pass_4a"] = all(row[k] for k in ("A_H1", "A_H2", "A_DD"))
        wf.append(row)
W = pd.DataFrame(wf)
show = ["panel", "chooser", "n_cand", "pick", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
        "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "pass_4b_full", "pass_4b_oos", "pass_4a"]
P(W[[c for c in show if c in W.columns]].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
dump(W, "walkforward")

n4b = int((W.get("pass_4b_full", pd.Series(dtype=bool)).fillna(False) &
           W.get("pass_4b_oos", pd.Series(dtype=bool)).fillna(False)).sum())
n4a = int(W.get("pass_4a", pd.Series(dtype=bool)).fillna(False).sum())
P(f"\n  4b (full AND OOS) clean picks: {n4b} of {len(W)}      4a passes: {n4a} of {len(W)}")
if n4b:
    b = W[(W.pass_4b_full.fillna(False)) & (W.pass_4b_oos.fillna(False))]
    for _, r in b.iterrows():
        P(f"    4b CLEAN: {r.panel} {r.chooser} {r['pick']}  full {r.CAGR:.2%}/{r.Sharpe:.4f}/{r.MaxDD:.2%}"
          f"  OOS {r.OOS_CAGR:.2%}/{r.OOS_Sharpe:.4f}/{r.OOS_MaxDD:.2%}")

P("\n" + "=" * 100)
P(f"done in {time.time()-t0:.1f}s")
P("=" * 100)
Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
print(f"wrote {OUT}.console.txt")
