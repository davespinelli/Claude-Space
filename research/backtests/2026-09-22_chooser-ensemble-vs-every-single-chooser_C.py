#!/usr/bin/env python3
"""Idea 2105 (lane C, 2026-09-22) — DOES A CHOOSER ENSEMBLE BEAT EVERY SINGLE CHOOSER
OUT OF SAMPLE?

THE DEFECT THIS PRICES.  Idea 2087 (lane C, 2026-09-22) ran SEVEN legal IS-only choosers over
one 30-cell grid (the 1795 turnover-budget family) on two panels and found

  * 97.75% of admission-haircut draws contain at least one cell clearing 4b FULL+OOS, and a
    mean of 3.27 of the 7 choosers find one, BUT
  * no single chooser finds one more than 78.5% of the time (IS_LEGS 0.785, CELL_ALPHA 0.005 —
    a 157x spread), and
  * the top two INVERT between panels (IS_LEGS 0.785 -> 0.300, IS_SHARPE 0.680 -> 0.983),
    Spearman rho +0.5357 over the seven ranks.

Every rule-8 verdict in this record is stated as if "reached by a legal IS-only chooser" were
neutral machinery.  2087 showed the machinery has a 157x selection width and no panel-stable
best member.  That is exactly the signature of a case where an ENSEMBLE over the members should
dominate any single member out of sample.  This run prices that.

WHAT IS PRICED.
  Three BOOK FAMILIES x THREE PANELS (U56, B136, SMALL), each family a 2-dial grid, each
  re-priced on the SAME seeded admission-haircut
  draws (2087's device: at depth d the panel drops round(d * (N-1)) of its single names, SPY
  retained; everything -- equal weight, sigma20, the momentum ranks, the 200d band -- is rebuilt
  on the survivors, as an investor holding a smaller list would):

    TURNBUDGET  2087's OWN grid: equal weight, g = clip(t/sigma20, 0, 1), MONTHLY trade,
                turnover budget B turns/yr.  target t x budget B = 5 x 6 = 30 cells.
    BANDGROSS   RULES v2's family: equal weight at gross/N, 200d MA band with hysteresis,
                gated weight de-grossed to cash, WEEKLY.  band x gross = 5 x 5 = 25 cells.
    TOPN        the 2026-09-04 KEEP-4b family: top-n momentum composite (no vol scaler),
                equal weight at gross/n, WEEKLY.  n x gross = 5 x 5 = 25 cells.

  On EVERY (family, panel, draw) all cells are scored at 10 bps and the SEVEN legal IS-only
  choosers of 2087 each pick one cell from 2009-2016 columns only.  Then FIVE ENSEMBLES over the
  six INFORMATIVE members (CELL_ALPHA is the no-information control, not a voter) pick as well.

  TUNED PARAMETERS (exactly 2, both reported at every grid point):
      DIAL 1  aggregation rule  in {MEANRANK, MEDRANK, VOTE}
      DIAL 2  vote threshold k  in {2, 3, 4}   (VOTE only; below k it falls back to MEANRANK)
  Reported, not tuned: the haircut depths, the draw counts, a 7-voter VOTE variant, the cost
  ladder on the headline pick, and every cell of every grid.

  BENCHMARKS for each chooser: the ORACLE (the grid's best OOS-Sharpe cell, an unreachable
  upper bound), the COIN (a uniform draw from the same grid, scored EXACTLY as the grid mean /
  the grid's own 4b share -- no sampling noise), and SPY.

RULE 8.  Every chooser here is IS-only by construction (2009-2016); the entire evaluation is the
untouched 2017-2026 window.  The headline ensemble pick on the clean panel is additionally
reported as a book against the LIVE RULES v2 baseline and SPY on FULL, both halves and OOS.

PROTOCOL: 10 bps, decided close t applied t+1, no shorting, both KEEP paths.
SURVIVORSHIP: U56, B136 and SMALL are CURRENT-constituent lists (protocol rule 9 and
data/SMALL_PANEL_README.md); the haircut draws perturb the name set but cannot restore
delisted names, so every level here is survivorship-inflated.  The CONTRASTS this run reports
(chooser vs chooser on the SAME draw) are paired and therefore far less exposed than levels.
"""
import sys, json, itertools, time
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights, band_state            # noqa: E402
from engine import backtest as engine_backtest, rebalance_mask              # noqa: E402

DATE, SLUG = "2026-09-22", "chooser-ensemble-vs-every-single-chooser"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_C"

WARMUP = 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"
COST0 = 10
COSTS_LADDER = [0, 10, 25, 50]
DD_CAP, CAGR_FLOOR = 0.60, 0.70
SIG_L, WIN = 20, 252
SEED0 = 2105
DEPTHS = [0.10, 0.20, 0.30]          # reported, not tuned (2087's device)
NDRAW = {"U56": 20, "B136": 20, "SMALL": 6}     # draws per depth per panel
PANELS = ["U56", "B136", "SMALL"]
# U56 and B136 hold SPY as a constituent (that is how the record's 1795 / 2087 books are built,
# and the gates below reproduce their published numbers); the SMALL panel carries SPY only as
# the benchmark column, so it is never held there.
HOLD_SPY = {"U56": True, "B136": True, "SMALL": False}

# --- family grids (all dials from the record's own committed ladders, reported not tuned) -----
TARGETS = [0.08, 0.10, 0.12, 0.16, 0.20]
BUDGETS = [0.5, 1.0, 1.5, 2.0, 3.0, 5.0]
BANDS   = [0.00, 0.01, 0.03, 0.05, 0.08]
GROSSES = [0.50, 0.75, 1.00, 1.25, 1.50]
NTOP    = [5, 10, 20, 30, 40]

MEMBERS = ["IS_SHARPE", "IS_LEGS", "IS_CALMAR", "IS_MINMARG", "IS_CAGRSLACK", "IS_DD"]
CHOOSERS = MEMBERS + ["CELL_ALPHA"]
ENSEMBLES = ["ENS_MEANRANK", "ENS_MEDRANK", "ENS_VOTE2", "ENS_VOTE3", "ENS_VOTE4"]
ENS_SENS = ["ENS7_VOTE2", "ENS7_VOTE3", "ENS7_VOTE4"]       # 7-voter variant, reported not tuned

_log, _gates = [], []


def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    _log.append(s)


def gate(name, value, target, ok):
    _gates.append(dict(gate=name, value=str(value), target=target, pass_=bool(ok)))
    log(f"  GATE {'PASS' if ok else 'FAIL'}  {name}: {value}   (target {target})")
    return bool(ok)


# ----------------------------------------------------------------------------- fast engines
def bt_sched(R, W, mask):
    """engine.backtest's semantics in numpy: hold target weights, rebalance only on `mask`,
    drift in between.  Returns COST-FREE returns and the turnover series so any cost rung can be
    applied afterwards.  W and mask are ALREADY shifted (decided t, applied t+1)."""
    n, k = R.shape
    cur = np.zeros(k)
    held = np.empty_like(R)
    turn = np.zeros(n)
    for i in range(n):
        if mask[i] or i == 0:
            new = W[i]
            turn[i] = np.abs(new - cur).sum()
            cur = new
        held[i] = cur
        gr = cur * (1.0 + R[i])
        tot = gr.sum() + (1.0 - cur.sum())
        if tot > 0:
            cur = gr / tot
    return (held * R).sum(axis=1), turn, held.sum(axis=1)


def bt_budget(R, W0, g0, mT, B):
    """1795's TURNOVER-BUDGETED refresh, copied unchanged from idea 2087's script.  The refresh
    trigger is R = D but a refresh executes only while trailing-252d realised turnover plus the
    refresh's own cost stays inside the annual budget B; mandatory trade-cadence re-spreads
    always execute and are charged against the same budget."""
    n = len(R)
    cur = np.zeros(R.shape[1])
    held = np.empty_like(R)
    turn = np.zeros(n)
    g_eff = g0[0]
    spent = 0.0
    for i in range(n):
        if i >= WIN:
            spent -= turn[i - WIN]
        if i == 0:
            g_eff = g0[i]
            new = W0[i] * g_eff
            turn[i] = np.abs(new - cur).sum()
            spent += turn[i]
            cur = new
        else:
            if mT[i]:
                new = W0[i] * g0[i]
                c_ref = np.abs(new - cur).sum()
                if spent + c_ref <= B:
                    g_eff = g0[i]
                else:
                    new = W0[i] * g_eff
                    c_ref = np.abs(new - cur).sum()
                turn[i] = c_ref
                spent += c_ref
                cur = new
            elif abs(g0[i] - cur.sum()) > 0.0:
                s = cur.sum()
                if s > 0:
                    new = cur * (g0[i] / s)
                    c_ref = np.abs(new - cur).sum()
                    if spent + c_ref <= B:
                        g_eff = g0[i]
                        turn[i] = c_ref
                        spent += c_ref
                        cur = new
        held[i] = cur
        gr = cur * (1.0 + R[i])
        tot = gr.sum() + (1.0 - cur.sum())
        if tot > 0:
            cur = gr / tot
    return (held * R).sum(axis=1), turn, held.sum(axis=1)


# ----------------------------------------------------------------------------- metrics
def net(r0, t0, c):
    return r0 - t0 * c / 1e4


def mets(r):
    r = r.dropna()
    eq = (1 + r).cumprod()
    yrs = len(r) / 252.0
    vol = r.std() * np.sqrt(252.0)
    return dict(CAGR=eq.iloc[-1] ** (1 / yrs) - 1 if yrs else np.nan,
                Sharpe=(r.mean() * 252.0) / vol if vol else np.nan,
                MaxDD=float((eq / eq.cummax() - 1).min()))


def halves(r):
    h = len(r) // 2
    return mets(r.iloc[:h])["Sharpe"], mets(r.iloc[h:])["Sharpe"]


def spy_bars(px, st):
    spy = px["SPY"].pct_change().fillna(0.0).loc[st:]
    h1, h2 = halves(spy)
    ih1, ih2 = halves(spy.loc[:IS_END])
    return dict(full=mets(spy), oos=mets(spy.loc[OOS_START:]), is_=mets(spy.loc[:IS_END]),
                h1=h1, h2=h2, ish1=ih1, ish2=ih2, ret=spy)


def score_row(r0, t0, st, S, LV, c=COST0):
    """Every 4b / 4a leg and every legal IS-only statistic for ONE book on ONE draw."""
    r0, t0 = r0.loc[st:], t0.loc[st:]
    yrs = len(r0) / 252.0
    r = net(r0, t0, c)
    mf, mo, mi = mets(r), mets(r.loc[OOS_START:]), mets(r.loc[:IS_END])
    h1, h2 = halves(r)
    ih1, ih2 = halves(r.loc[:IS_END])
    k4bf = (h1 > S["h1"] and h2 > S["h2"]
            and mf["MaxDD"] >= DD_CAP * S["full"]["MaxDD"]
            and mf["CAGR"] >= CAGR_FLOOR * S["full"]["CAGR"])
    k4bo = (mo["Sharpe"] > S["oos"]["Sharpe"]
            and mo["MaxDD"] >= DD_CAP * S["oos"]["MaxDD"]
            and mo["CAGR"] >= CAGR_FLOOR * S["oos"]["CAGR"])
    k4a = (h1 > LV["h1"] and h2 > LV["h2"] and mf["MaxDD"] >= LV["full"]["MaxDD"])
    k4ao = (mo["Sharpe"] > LV["oos"]["Sharpe"] and mo["MaxDD"] >= LV["oos"]["MaxDD"])
    is_legs = (int(ih1 > S["ish1"]) + int(ih2 > S["ish2"])
               + int(mi["MaxDD"] >= DD_CAP * S["is_"]["MaxDD"])
               + int(mi["CAGR"] >= CAGR_FLOOR * S["is_"]["CAGR"]))
    is_minmarg = min(ih1 - S["ish1"], ih2 - S["ish2"],
                     mi["MaxDD"] - DD_CAP * S["is_"]["MaxDD"],
                     mi["CAGR"] - CAGR_FLOOR * S["is_"]["CAGR"])
    return dict(turn_py=float(t0.sum() / yrs),
                CAGR=mf["CAGR"], Sharpe=mf["Sharpe"], MaxDD=mf["MaxDD"], H1=h1, H2=h2,
                is_Sharpe=mi["Sharpe"], is_MaxDD=mi["MaxDD"], is_CAGR=mi["CAGR"],
                is_legs=is_legs, is_minmarg=float(is_minmarg),
                is_calmar=float(mi["CAGR"] / abs(mi["MaxDD"])) if mi["MaxDD"] < 0 else np.nan,
                is_cagrslack=float(mi["CAGR"] - CAGR_FLOOR * S["is_"]["CAGR"]),
                oos_CAGR=mo["CAGR"], oos_Sharpe=mo["Sharpe"], oos_MaxDD=mo["MaxDD"],
                keep4b_full=k4bf, keep4b_oos=k4bo, keep4b=(k4bf and k4bo),
                keep4a=k4a, keep4a_oos=k4ao)


# ----------------------------------------------------------------------------- book families
class Panel:
    """One panel + one surviving name set.  Everything a book needs, rebuilt on the survivors."""

    def __init__(self, px, cols, delay=1, hold_spy=True):
        hold = list(cols) if hold_spy else [c for c in cols if c != "SPY"]
        self.px, self.cols, self.delay = px, hold, delay
        self.index = px.index
        self.R = np.nan_to_num(px.pct_change().values, nan=0.0)
        sub = px[hold]
        e = pd.DataFrame(1.0, index=sub.index, columns=sub.columns).where(sub.notna(), 0.0)
        ew = e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
        self.EWs = ew                                            # on survivor columns
        ewf = ew.reindex(columns=px.columns).fillna(0.0)
        self.EW = np.nan_to_num(ewf.values, nan=0.0)
        pr = (ew.shift(1) * sub.pct_change()).sum(axis=1)
        self.SIG = pr.rolling(SIG_L).std() * np.sqrt(252.0)
        mM = np.asarray(rebalance_mask(px.index, "M").values, bool)
        mW = np.asarray(rebalance_mask(px.index, "W").values, bool)
        self.mM = np.concatenate([[False], mM[:-1]])
        self.mW = np.concatenate([[False], mW[:-1]])
        self.band = {b: band_state(sub, b) if b > 0 else (sub > sub.rolling(200).mean())
                     for b in BANDS}
        # momentum composite of the 2026-09-04 KEEP-4b: NO vol scaler, no 200d gate
        mom = sub.shift(21) / sub.shift(252) - 1
        r6 = sub / sub.shift(126) - 1
        r3 = sub / sub.shift(63) - 1
        self.comp = (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True)
                     + r3.rank(axis=1, pct=True)) / 3
        self.rank = self.comp.rank(axis=1, ascending=False)

    def _lag(self, Wdf):
        W = np.nan_to_num(Wdf.reindex(columns=self.px.columns).fillna(0.0).values, nan=0.0)
        return np.vstack([np.zeros((self.delay, W.shape[1])), W[:-self.delay]])

    def _ser(self, r, t, g):
        return (pd.Series(r, index=self.index), pd.Series(t, index=self.index),
                pd.Series(g, index=self.index))

    def turnbudget(self, tgt, B):
        g = (tgt / self.SIG.replace(0, np.nan)).clip(upper=1.0).fillna(0.0).values
        g = np.concatenate([np.zeros(self.delay), g[:-self.delay]])
        W = np.vstack([np.zeros((self.delay, self.EW.shape[1])), self.EW[:-self.delay]])
        return self._ser(*bt_budget(self.R, W, g, self.mM, B))

    def bandgross(self, band, gross):
        W = (gross * self.EWs).where(self.band[band], 0.0)
        return self._ser(*bt_sched(self.R, self._lag(W), self.mW))

    def topn(self, n, gross):
        W = (self.rank <= n).astype(float) * (gross / n)
        return self._ser(*bt_sched(self.R, self._lag(W), self.mW))

    def live_v2(self, st):
        """LIVE RULES v2 on the SAME survivors — the matched 4a comparand for this draw."""
        W = rules_v2_weights(self.px[self.cols], 0.03, 0.75)
        r0, t0, _ = bt_sched(self.R, self._lag(W), self.mW)
        r0, t0 = pd.Series(r0, index=self.index).loc[st:], pd.Series(t0, index=self.index).loc[st:]
        r = net(r0, t0, COST0)
        h1, h2 = halves(r)
        return dict(full=mets(r), oos=mets(r.loc[OOS_START:]), h1=h1, h2=h2, ret=r)


FAMILIES = {
    "TURNBUDGET": [("t=%.2f|B=%.1f" % (t, b), ("turnbudget", t, b))
                   for t, b in itertools.product(TARGETS, BUDGETS)],
    "BANDGROSS":  [("band=%.2f|g=%.2f" % (b, g), ("bandgross", b, g))
                   for b, g in itertools.product(BANDS, GROSSES)],
    "TOPN":       [("n=%d|g=%.2f" % (n, g), ("topn", n, g))
                   for n, g in itertools.product(NTOP, GROSSES)],
}


# ----------------------------------------------------------------------------- choosers
KEYS = {"IS_SHARPE": lambda s: s.is_Sharpe.values,
        "IS_LEGS": lambda s: s.is_legs.values * 1e6 + s.is_Sharpe.values,
        "IS_CALMAR": lambda s: np.nan_to_num(s.is_calmar.values, nan=-1e9),
        "IS_MINMARG": lambda s: s.is_minmarg.values,
        "IS_CAGRSLACK": lambda s: s.is_cagrslack.values,
        "IS_DD": lambda s: s.is_MaxDD.values}


def picks_for_draw(sub):
    """sub = one (family, panel, draw) grid, one row per cell.  Returns {chooser: cell_index}.
    Deterministic tie-break: cells are pre-sorted in grid order and argmax takes the first."""
    s = sub.reset_index(drop=True)
    out, keyranks, votes = {}, {}, {}
    for m in MEMBERS:
        k = KEYS[m](s)
        i = int(np.argmax(k))
        out[m] = i
        votes[i] = votes.get(i, 0) + 1
        keyranks[m] = pd.Series(k).rank(pct=True).values      # higher = better
    out["CELL_ALPHA"] = int(s.cell.astype(str).sort_values().index[0])
    RK = np.vstack([keyranks[m] for m in MEMBERS])
    mean_rank, med_rank = RK.mean(axis=0), np.median(RK, axis=0)
    i_mean, i_med = int(np.argmax(mean_rank)), int(np.argmax(med_rank))
    out["ENS_MEANRANK"], out["ENS_MEDRANK"] = i_mean, i_med
    v6 = np.zeros(len(s))
    for i, c in votes.items():
        v6[i] = c
    for k in (2, 3, 4):
        best = v6.max()
        if best >= k:
            cands = np.flatnonzero(v6 == best)
            out[f"ENS_VOTE{k}"] = int(cands[np.argmax(mean_rank[cands])])
        else:
            out[f"ENS_VOTE{k}"] = i_mean
    v7 = v6.copy()
    v7[out["CELL_ALPHA"]] += 1
    for k in (2, 3, 4):
        best = v7.max()
        if best >= k:
            cands = np.flatnonzero(v7 == best)
            out[f"ENS7_VOTE{k}"] = int(cands[np.argmax(mean_rank[cands])])
        else:
            out[f"ENS7_VOTE{k}"] = i_mean
    return out, v6


# ----------------------------------------------------------------------------- draws
def draws_for(px, panel):
    """(tag, depth, draw_id, surviving cols).  SPY retained in every draw (it is the benchmark;
    dropping it would confound the 4b contrast)."""
    names = [c for c in px.columns if c != "SPY"]
    out = [("d=0.00", 0.0, 0, list(px.columns))]
    poff = {"U56": 0, "B136": 500, "SMALL": 900}[panel]
    for d in DEPTHS:
        k = int(round(d * len(names)))
        for j in range(NDRAW[panel]):
            rs = np.random.RandomState(SEED0 + int(d * 100) * 1000 + j + poff)
            keep = sorted(rs.choice(names, size=len(names) - k, replace=False).tolist())
            out.append((f"d={d:.2f}", d, j, keep + ["SPY"]))
    return out


# ----------------------------------------------------------------------------- run
def main():
    t_start = time.time()
    log(f"# Idea 2105 (lane C, {DATE}) — does a CHOOSER ENSEMBLE beat EVERY SINGLE CHOOSER "
        f"out of sample?")
    log(f"  families {list(FAMILIES)}  cells {[len(v) for v in FAMILIES.values()]}  "
        f"panels {PANELS}  depths {DEPTHS} x {NDRAW} draws per panel + clean")
    log(f"  members {MEMBERS} + CELL_ALPHA;  ensembles {ENSEMBLES} (+ sensitivity {ENS_SENS})")
    log(f"  10 bps, t+1 execution, IS {IS_END} / OOS {OOS_START}, 4b caps DD {DD_CAP} "
        f"CAGR {CAGR_FLOOR}\n")

    PX = {"U56": load_universe(), "B136": load_universe(broad=True),
          "SMALL": load_universe(small=True)}
    rows = []
    for panel in PANELS:
        px = PX[panel]
        st = px.index[WARMUP]
        S = spy_bars(px, st)
        log(f"## {panel}: {px.shape[1]} columns, {px.index[0].date()}..{px.index[-1].date()}, "
            f"scored from {st.date()}")
        log(f"   SPY: FULL {S['full']['CAGR']:.2%} / {S['full']['Sharpe']:.3f} / "
            f"{S['full']['MaxDD']:.2%}   OOS {S['oos']['CAGR']:.2%} / "
            f"{S['oos']['Sharpe']:.3f} / {S['oos']['MaxDD']:.2%}")
        dr = draws_for(px, panel)
        for (tag, depth, j, cols) in dr:
            P = Panel(px, cols, hold_spy=HOLD_SPY[panel])
            LV = P.live_v2(st)
            for fam, cells in FAMILIES.items():
                for cell, (meth, a, b) in cells:
                    r0, t0, gs = getattr(P, meth)(a, b)
                    rec = score_row(r0, t0, st, S, LV)
                    rows.append(dict(panel=panel, family=fam, depth=depth, draw=j,
                                     tag=tag, n_names=len(P.cols), cell=cell,
                                     d1=a, d2=b, gross_mean=float(gs.loc[st:].mean()), **rec))
            if j == 0:
                log(f"   {tag} draw {j}: {len(P.cols)} held names, live v2 FULL S "
                    f"{LV['full']['Sharpe']:.3f}  ({time.time()-t_start:.0f}s)")
        log(f"   {panel} done at {time.time()-t_start:.0f}s")
    G = pd.DataFrame(rows)
    G.to_csv(f"{OUT}.grid.csv.gz", index=False, compression="gzip")
    log(f"\n   grid: {len(G)} (panel, family, draw, cell) rows -> {Path(OUT).name}.grid.csv.gz\n")

    # -------------------------------------------------------------- GATE: reproduce 1795/2087
    c0 = G[(G.panel == "U56") & (G.family == "TURNBUDGET") & (G.depth == 0)
           & (G.cell == "t=0.12|B=5.0")]
    pub = dict(CAGR=0.1407, Sharpe=1.251, MaxDD=-0.1590, oCAGR=0.1540, oSharpe=1.357)
    log("## GATES — machinery reproduces the committed record")
    if len(c0) == 1:
        r = c0.iloc[0]
        gate("G1 1795 cell CAGR", f"{r.CAGR:.4f}", f"{pub['CAGR']:.4f} +/- 0.002",
             abs(r.CAGR - pub["CAGR"]) < 0.002)
        gate("G2 1795 cell Sharpe", f"{r.Sharpe:.3f}", f"{pub['Sharpe']:.3f} +/- 0.01",
             abs(r.Sharpe - pub["Sharpe"]) < 0.01)
        gate("G3 1795 cell MaxDD", f"{r.MaxDD:.4f}", f"{pub['MaxDD']:.4f} +/- 0.002",
             abs(r.MaxDD - pub["MaxDD"]) < 0.002)
        gate("G4 1795 cell OOS Sharpe", f"{r.oos_Sharpe:.3f}", f"{pub['oSharpe']:.3f} +/- 0.01",
             abs(r.oos_Sharpe - pub["oSharpe"]) < 0.01)
    # bt_sched must equal engine.backtest exactly
    pxu = PX["U56"]
    Pu = Panel(pxu, list(pxu.columns), hold_spy=True)
    W = rules_v2_weights(pxu, 0.03, 0.75)
    r0, t0, _ = bt_sched(Pu.R, Pu._lag(W), Pu.mW)
    eb = engine_backtest(pxu, W, cost_bps=COST0, freq="W")
    mine = pd.Series(net(r0, t0, COST0), index=pxu.index)
    gate("G5 bt_sched == engine.backtest", f"{float((mine - eb['returns']).abs().max()):.2e}",
         "< 1e-12", float((mine - eb["returns"]).abs().max()) < 1e-12)

    # -------------------------------------------------------------- chooser / ensemble scoring
    log("\n## PER-DRAW PICKS")
    prec, vrec = [], []
    for (panel, fam), sub in G.groupby(["panel", "family"], sort=False):
        for (depth, j), s in sub.groupby(["depth", "draw"], sort=False):
            s = s.sort_values("cell").reset_index(drop=True)
            picks, v6 = picks_for_draw(s)
            orc = int(np.argmax(s.oos_Sharpe.values))
            rk = s.oos_Sharpe.rank(pct=True).values
            base = dict(panel=panel, family=fam, depth=depth, draw=j)
            for ch, i in picks.items():
                r = s.iloc[i]
                # NOTE the flags are stored as FLOATS here: a chooser row carries a 0/1
                # indicator and the COIN row carries a share, and mixing bool with float in one
                # column silently makes it object-dtype, which corrupts every later .mean().
                prec.append(dict(**base, chooser=ch, cell=r.cell, oos_Sharpe=r.oos_Sharpe,
                                 oos_CAGR=r.oos_CAGR, oos_MaxDD=r.oos_MaxDD, CAGR=r.CAGR,
                                 Sharpe=r.Sharpe, MaxDD=r.MaxDD, keep4b=float(r.keep4b),
                                 keep4b_full=float(r.keep4b_full),
                                 keep4b_oos=float(r.keep4b_oos),
                                 keep4a=float(r.keep4a), oos_pct=rk[i], votes=float(v6[i])))
            # exact COIN (uniform draw over the same grid) and ORACLE
            prec.append(dict(**base, chooser="COIN_EXACT", cell="(grid mean)",
                             oos_Sharpe=s.oos_Sharpe.mean(), oos_CAGR=s.oos_CAGR.mean(),
                             oos_MaxDD=s.oos_MaxDD.mean(), CAGR=s.CAGR.mean(),
                             Sharpe=s.Sharpe.mean(), MaxDD=s.MaxDD.mean(),
                             keep4b=s.keep4b.mean(), keep4b_full=s.keep4b_full.mean(),
                             keep4b_oos=s.keep4b_oos.mean(), keep4a=s.keep4a.mean(),
                             oos_pct=float(np.mean(rk)), votes=np.nan))
            r = s.iloc[orc]
            prec.append(dict(**base, chooser="ORACLE_OOS", cell=r.cell,
                             oos_Sharpe=r.oos_Sharpe, oos_CAGR=r.oos_CAGR,
                             oos_MaxDD=r.oos_MaxDD, CAGR=r.CAGR, Sharpe=r.Sharpe,
                             MaxDD=r.MaxDD, keep4b=float(r.keep4b),
                             keep4b_full=float(r.keep4b_full),
                             keep4b_oos=float(r.keep4b_oos), keep4a=float(r.keep4a),
                             oos_pct=rk[orc], votes=float(v6[orc])))
            vrec.append(dict(**base, max_votes=float(v6.max()),
                             n_cells_voted=int((v6 > 0).sum()),
                             grid_4b_share=float(s.keep4b.mean()),
                             any_4b=bool(s.keep4b.any())))
    P = pd.DataFrame(prec)
    V = pd.DataFrame(vrec)
    gate("G6 pick flags are numeric (object dtype would corrupt every reach)",
         str({c: str(P[c].dtype) for c in ["keep4b", "keep4b_full", "keep4a", "oos_pct"]}),
         "all float", all(P[c].dtype.kind == "f"
                          for c in ["keep4b", "keep4b_full", "keep4a", "oos_pct"]))
    P.to_csv(f"{OUT}.picks.csv", index=False)
    V.to_csv(f"{OUT}.votes.csv", index=False)

    agg = (P.groupby(["panel", "family", "chooser"])
             .agg(n=("oos_Sharpe", "size"), oosS=("oos_Sharpe", "mean"),
                  oosPct=("oos_pct", "mean"), reach4b=("keep4b", "mean"),
                  reach4bF=("keep4b_full", "mean"), reach4a=("keep4a", "mean"),
                  oosCAGR=("oos_CAGR", "mean"), oosDD=("oos_MaxDD", "mean"))
             .reset_index())
    agg.to_csv(f"{OUT}.choosers.csv", index=False)

    ORDER = CHOOSERS + ENSEMBLES + ENS_SENS + ["COIN_EXACT", "ORACLE_OOS"]
    for (panel, fam), s in agg.groupby(["panel", "family"], sort=False):
        s = s.set_index("chooser").reindex(ORDER)
        log(f"\n### {panel} / {fam}   ({int(s.n.iloc[0])} draws, "
            f"{len(FAMILIES[fam])} cells)")
        log("   chooser          mean OOS S   OOS pctile   4b FULL+OOS   4b FULL    4a")
        for ch in ORDER:
            r = s.loc[ch]
            mark = "  <-- ENS" if ch.startswith("ENS") else ""
            log(f"   {ch:<15} {r.oosS:>10.4f} {r.oosPct:>12.4f} {r.reach4b:>13.4f} "
                f"{r.reach4bF:>10.4f} {r.reach4a:>6.3f}{mark}")

    # -------------------------------------------------------------- V1..V4
    log("\n## V1 — DOES THE BEST ENSEMBLE BEAT THE BEST SINGLE MEMBER, PANEL BY PANEL?")
    v1_rows = []
    for (panel, fam), s in agg.groupby(["panel", "family"], sort=False):
        s = s.set_index("chooser")
        bm = s.loc[MEMBERS].oosPct.idxmax()
        be = s.loc[ENSEMBLES].oosPct.idxmax()
        for metric in ["oosPct", "reach4b"]:
            bm_m = s.loc[MEMBERS, metric].max()
            bm_n = s.loc[MEMBERS, metric].idxmax()
            mean_m = s.loc[MEMBERS, metric].mean()
            for e in ENSEMBLES:
                v1_rows.append(dict(panel=panel, family=fam, metric=metric, ens=e,
                                    ens_v=s.loc[e, metric], best_member=bm_n,
                                    best_member_v=bm_m, mean_member_v=mean_m,
                                    beats_best=bool(s.loc[e, metric] > bm_m),
                                    beats_mean=bool(s.loc[e, metric] > mean_m),
                                    beats_coin=bool(s.loc[e, metric] > s.loc["COIN_EXACT", metric])))
        log(f"   {panel}/{fam}: best member by OOS pctile = {bm} ({s.loc[bm,'oosPct']:.4f}), "
            f"best ensemble = {be} ({s.loc[be,'oosPct']:.4f}), "
            f"member mean {s.loc[MEMBERS,'oosPct'].mean():.4f}, "
            f"COIN {s.loc['COIN_EXACT','oosPct']:.4f}, ORACLE {s.loc['ORACLE_OOS','oosPct']:.4f}")
    V1 = pd.DataFrame(v1_rows)
    V1.to_csv(f"{OUT}.v1.csv", index=False)
    for metric in ["oosPct", "reach4b"]:
        sub = V1[V1.metric == metric]
        log(f"\n   [{metric}] ensemble vs BEST single member, over "
            f"{sub.panel.nunique()*sub.family.nunique()} (panel, family) cells:")
        for e in ENSEMBLES:
            t = sub[sub.ens == e]
            log(f"     {e:<14} beats best member {int(t.beats_best.sum())}/{len(t)}   "
                f"beats member mean {int(t.beats_mean.sum())}/{len(t)}   "
                f"beats COIN {int(t.beats_coin.sum())}/{len(t)}")
    log("\n   HOW MANY OF THE 6 MEMBERS EACH ENSEMBLE BEATS (the ex-ante question):")
    beat_rows = []
    for (panel, fam), s in agg.groupby(["panel", "family"], sort=False):
        s = s.set_index("chooser")
        for metric in ["oosPct", "reach4b"]:
            for e in ENSEMBLES:
                nb = int((s.loc[e, metric] > s.loc[MEMBERS, metric]).sum())
                beat_rows.append(dict(panel=panel, family=fam, metric=metric, ens=e,
                                      n_members_beaten=nb))
    BT = pd.DataFrame(beat_rows)
    BT.to_csv(f"{OUT}.members_beaten.csv", index=False)
    for metric in ["oosPct", "reach4b"]:
        t_ = BT[BT.metric == metric]
        log(f"     [{metric}] mean members beaten (of 6), over 9 (panel, family) cells:")
        for e in ENSEMBLES:
            u = t_[t_.ens == e]
            log(f"       {e:<14} mean {u.n_members_beaten.mean():.2f}   "
                f"min {u.n_members_beaten.min()}   max {u.n_members_beaten.max()}   "
                f"cells where it beats >= 4 of 6: {int((u.n_members_beaten>=4).sum())}/{len(u)}")
    best_e = V1[V1.metric == "oosPct"].groupby("ens").beats_best.sum().idxmax()
    n_cells = V1[(V1.metric == "oosPct") & (V1.ens == best_e)].shape[0]
    n_best = int(V1[(V1.metric == "oosPct") & (V1.ens == best_e)].beats_best.sum())
    V1_ok = gate("V1 some ensemble beats the best single member on EVERY (panel, family)",
                 f"{best_e} {n_best}/{n_cells}", f"{n_cells}/{n_cells}", n_best == n_cells)
    V2_ok = gate("V2 every ensemble beats the MEMBER MEAN on every (panel, family)",
                 f"{int(V1[V1.metric=='oosPct'].beats_mean.sum())}/"
                 f"{len(V1[V1.metric=='oosPct'])}",
                 "all", bool(V1[V1.metric == "oosPct"].beats_mean.all()))
    V4_ok = gate("V4 every ensemble beats the COIN on every (panel, family)",
                 f"{int(V1[V1.metric=='oosPct'].beats_coin.sum())}/"
                 f"{len(V1[V1.metric=='oosPct'])}",
                 "all", bool(V1[V1.metric == "oosPct"].beats_coin.all()))

    log("\n## V3 — PANEL STABILITY: spread of 4b reach ACROSS PANELS, within each family")
    sp_rows = []
    for fam in FAMILIES:
        s = agg[agg.family == fam].pivot(index="chooser", columns="panel", values="reach4b")
        for ch in ORDER:
            if ch in s.index:
                sp_rows.append(dict(family=fam, chooser=ch,
                                    **{p: float(s.loc[ch, p]) for p in PANELS},
                                    spread=float(s.loc[ch].max() - s.loc[ch].min())))
    SP = pd.DataFrame(sp_rows)
    SP.to_csv(f"{OUT}.stability.csv", index=False)
    for fam in FAMILIES:
        t = SP[SP.family == fam].set_index("chooser")
        log(f"\n   {fam}:  " + "  ".join(f"{p}" for p in PANELS) + "   |spread|")
        for ch in ORDER:
            if ch in t.index:
                log(f"     {ch:<15} " + "  ".join(f"{t.loc[ch,p]:.3f}" for p in PANELS)
                    + f"   {t.loc[ch,'spread']:.3f}")
    mem_sp = SP[SP.chooser.isin(MEMBERS)].groupby("family").spread.mean()
    ens_sp = SP[SP.chooser.isin(ENSEMBLES)].groupby("family").spread.mean()
    log(f"\n   mean member spread by family: {dict(mem_sp.round(4))}")
    log(f"   mean ensemble spread by family: {dict(ens_sp.round(4))}")
    V3_ok = gate("V3 ensembles are MORE panel-stable than members in every family",
                 f"ens {dict(ens_sp.round(4))} vs mem {dict(mem_sp.round(4))}",
                 "ens < mem in all", bool((ens_sp < mem_sp).all()))

    # -------------------------------------------------------------- V5 rule-8 headline books
    log("\n## V5 — RULE 8 WALK-FORWARD: the ensembles' CLEAN-PANEL picks as BOOKS "
        "(params from 2009-2016 only, 2017-2026 untouched)")
    clean = P[(P.depth == 0)]
    head = []
    for (panel, fam), s in clean.groupby(["panel", "family"], sort=False):
        s = s.set_index("chooser")
        for ch in ENSEMBLES + MEMBERS + ["CELL_ALPHA", "ORACLE_OOS"]:
            r = s.loc[ch]
            head.append(dict(panel=panel, family=fam, chooser=ch, cell=r.cell,
                             CAGR=r.CAGR, Sharpe=r.Sharpe, MaxDD=r.MaxDD,
                             oos_CAGR=r.oos_CAGR, oos_Sharpe=r.oos_Sharpe,
                             oos_MaxDD=r.oos_MaxDD, keep4b=r.keep4b, keep4a=r.keep4a))
    H = pd.DataFrame(head)
    H.to_csv(f"{OUT}.clean_picks.csv", index=False)
    for (panel, fam), s in H.groupby(["panel", "family"], sort=False):
        log(f"\n   {panel}/{fam} (clean panel, d=0):")
        for _, r in s.iterrows():
            log(f"     {r.chooser:<15} {r.cell:<16} FULL {r.CAGR:>7.2%}/{r.Sharpe:>6.3f}/"
                f"{r.MaxDD:>8.2%}   OOS {r.oos_CAGR:>7.2%}/{r.oos_Sharpe:>6.3f}/"
                f"{r.oos_MaxDD:>8.2%}   4b {str(bool(r.keep4b)):<5} 4a {bool(r.keep4a)}")

    # headline book: the ENS_MEANRANK pick on U56/TURNBUDGET, full protocol comparison
    log("\n## HEADLINE BOOK vs LIVE BASELINE and SPY (U56, clean panel)")
    px = PX["U56"]
    st = px.index[WARMUP]
    S = spy_bars(px, st)
    Pu = Panel(px, list(px.columns), hold_spy=True)
    LV = Pu.live_v2(st)
    hl_rows = []
    for fam in FAMILIES:
        row = H[(H.panel == "U56") & (H.family == fam) & (H.chooser == "ENS_MEANRANK")].iloc[0]
        cell = row.cell
        meth, a, b = dict(FAMILIES[fam])[cell]
        r0, t0, gs = getattr(Pu, meth)(a, b)
        for c in COSTS_LADDER:
            rr = net(r0.loc[st:], t0.loc[st:], c)
            h1, h2 = halves(rr)
            m, mo = mets(rr), mets(rr.loc[OOS_START:])
            hl_rows.append(dict(family=fam, cell=cell, cost=c, CAGR=m["CAGR"],
                                Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                                oos_CAGR=mo["CAGR"], oos_Sharpe=mo["Sharpe"],
                                oos_MaxDD=mo["MaxDD"]))
    HL = pd.DataFrame(hl_rows)
    HL.to_csv(f"{OUT}.costladder.csv", index=False)
    lv, sp = LV, S
    lh1, lh2 = lv["h1"], lv["h2"]
    log(f"   LIVE RULES v2 : FULL {lv['full']['CAGR']:>7.2%}/{lv['full']['Sharpe']:>6.3f}/"
        f"{lv['full']['MaxDD']:>8.2%}  halves {lh1:.3f}/{lh2:.3f}  "
        f"OOS {lv['oos']['CAGR']:>7.2%}/{lv['oos']['Sharpe']:>6.3f}/{lv['oos']['MaxDD']:>8.2%}")
    log(f"   SPY           : FULL {sp['full']['CAGR']:>7.2%}/{sp['full']['Sharpe']:>6.3f}/"
        f"{sp['full']['MaxDD']:>8.2%}  halves {sp['h1']:.3f}/{sp['h2']:.3f}  "
        f"OOS {sp['oos']['CAGR']:>7.2%}/{sp['oos']['Sharpe']:>6.3f}/{sp['oos']['MaxDD']:>8.2%}")
    for fam in FAMILIES:
        r = HL[(HL.family == fam) & (HL.cost == COST0)].iloc[0]
        log(f"   ENS_MEANRANK {fam:<11}({r.cell}): FULL {r.CAGR:>7.2%}/{r.Sharpe:>6.3f}/"
            f"{r.MaxDD:>8.2%}  halves {r.H1:.3f}/{r.H2:.3f}  "
            f"OOS {r.oos_CAGR:>7.2%}/{r.oos_Sharpe:>6.3f}/{r.oos_MaxDD:>8.2%}")
    log("\n   cost ladder (reported, not tuned):")
    for _, r in HL.iterrows():
        log(f"     {r.family:<11} {r.cell:<16} {int(r.cost):>3} bps  FULL {r.CAGR:>7.2%}/"
            f"{r.Sharpe:>6.3f}/{r.MaxDD:>8.2%}   OOS S {r.oos_Sharpe:>6.3f}")

    # -------------------------------------------------------------- vote structure
    log("\n## VOTE STRUCTURE (why the threshold dial does what it does)")
    for (panel, fam), s in V.groupby(["panel", "family"], sort=False):
        log(f"   {panel}/{fam}: mean max-votes {s.max_votes.mean():.2f} of 6, "
            f"mean distinct cells voted {s.n_cells_voted.mean():.2f}, "
            f"draws with >=3 agreeing {float((s.max_votes>=3).mean()):.3f}, "
            f">=4 {float((s.max_votes>=4).mean()):.3f}; "
            f"grid 4b share {s.grid_4b_share.mean():.3f}, "
            f"draws with ANY 4b cell {float(s.any_4b.mean()):.3f}")

    log("\n## VERDICTS")
    log(f"   V1 an ensemble beats the BEST single member everywhere ... "
        f"{'YES' if V1_ok else 'NO'}")
    log(f"   V2 every ensemble beats the MEMBER MEAN everywhere ....... "
        f"{'YES' if V2_ok else 'NO'}")
    log(f"   V3 ensembles are MORE panel-stable than members .......... "
        f"{'YES' if V3_ok else 'NO'}")
    log(f"   V4 every ensemble beats the COIN everywhere .............. "
        f"{'YES' if V4_ok else 'NO'}")
    n4b = int(H[H.chooser.isin(ENSEMBLES)].keep4b.sum())
    log(f"   clean-panel ensemble picks clearing 4b FULL+OOS: {n4b}/"
        f"{len(H[H.chooser.isin(ENSEMBLES)])}")
    log(f"   total runtime {time.time()-t_start:.0f}s")

    pd.DataFrame(_gates).to_csv(f"{OUT}.gates.csv", index=False)
    Path(f"{OUT}.log.txt").write_text("\n".join(_log) + "\n")


if __name__ == "__main__":
    main()
