#!/usr/bin/env python3
"""2026-09-18 lane B, QUEUE idea 1268 — is the binding 4b DRAWDOWN leg buyable by WHAT THE
IDLE SLEEVE HOLDS rather than by HOW MUCH IS HELD?

WHY THIS IDEA.  Six dials running (1253 phase, 1254 years, 1255 names, 1257 signal, 1264
sizing, 1265's N x H frame) say the committed 2026-09-04 4b pass is a statement about the
DRAWDOWN leg and nothing else, and all three mechanisms priced for BUYING that leg have now
failed: the explicit depth brake (1262) cannot arm at the only trough that matters, portfolio
vol targeting (1263) is a short-lookback artefact half of whose conversions are flat
de-grossing, and inverse-vol slot sizing (1264) is refused by rule 8 at 4 of 4 large-cap
cells.  Every one of those three REDUCES EQUITY EXPOSURE, so every one of them confounds "the
risk clause worked" with "less equity was held".  This run removes that confound: the
committed book holds GROSS = 0.75, i.e. it parks a CONSTANT 25% of NAV in ZERO-RETURN CASH.
Route that idle sleeve into duration and the EQUITY BOOK IS BIT-IDENTICAL at every cell —
same names, same slots, same dates — so d_CAGR and d_MaxDD are attributable to the sleeve
alone.  If the diagnosis "every risk clause costs more return than it saves" is a fact about
risk clauses rather than about de-grossing, this mechanism should break it.

THE BOOK (frozen, not a dial).  The committed 2026-09-04 4b book: RAW three-leg composite of
percentile ranks (21/252, 0/126, 0/63), NO vol scaler, gate = above 200d MA AND vol20 < 0.60,
N = 20, H = 126 minimum hold, GROSS = 0.75 of NAV, weekly decide-Friday / trade-Monday, 10
bps on traded notional, weights decided at t applied at t+1, warm-up 260 days.

DIAL 1  SLEEVE = {SHY, IEF, TLT, LQD, TIP, SPY} — what the idle sleeve holds.  SPY is the
        EQUITY-FILL COMPARAND, carried so the run can say whether any gain is about DURATION
        or merely about BEING INVESTED; it is reported as a rung, not recommended.
DIAL 2  FILL  = {0.00, 0.25, 0.50, 0.75, 1.00} — the fraction of the idle sleeve routed into
        SLEEVE.  FILL = 0.00 IS THE COMMITTED CASH ANCHOR at every SLEEVE, which makes the
        six FILL-0 rows a bit-identity control (gate G2) rather than six data points.
NOT DIALS, reported at every value: PANEL {U56, B135, SMALL} (rule 9) x SIGNAL {COMPOSITE3,
M12_1 = 1257's single 21/252 leg}.  The sleeve asset is NEVER selectable — it is joined as an
overlay column where the panel lacks it and is excluded from the selection set everywhere
except where it already was one (the U56/B135 bond ETFs, whose selection is left frozen).

NO LEVERAGE (protocol rule 2): the sleeve can only ever be filled out of cash the book is
already holding, so total gross <= 1.00 by construction and gate G3 checks it.

PRE-REGISTERED HYPOTHESES, declared before the grid was read, scored as they fell:
  H_DD    at least one non-SPY sleeve cell converts the committed U56 4b DD FAIL into a PASS.
  H_FREE  the cheapest such conversion costs NO full-sample CAGR against the anchor (d >= 0) —
          this is the hypothesis the standing diagnosis says must fail.
  H_R8    rule 8 (choose SLEEVE/FILL on warm-up..2016-12-31 IS Sharpe, read 2017-2026 once)
          reaches a NON-CASH sleeve and beats do-nothing on OOS Sharpe.
  H_DUR   at matched FILL, the best duration sleeve beats the SPY fill on MaxDD — i.e. the
          mechanism is about duration and not about being invested.
THE CONTROL THAT DECIDES THE RUN (added after the first full grid was read, and said so).
The engine pays ZERO on cash, so a CASH anchor is not the right comparand for a T-BILL
sleeve: SHY at FILL 1.00 is approximately the non-zero cash rate the book should have been
earning all along (queue idea 1193's question), not a strategy.  Every sleeve is therefore
ALSO scored against SHY AT THE SAME FILL on the SAME equity book — the DURATION EXCESS over
bills.  That is this run's equivalent of the gross-matched control that killed 1263: if the
mechanism is only "cash should not be modelled at 0%", the excess over SHY is where it dies.

PRE-DECLARED VERDICT RULE: KEEP (path 4b) only if a cell clears every 4b leg AND rule 8
reaches it AND its OOS Sharpe is above the anchor's.  A cell that clears 4b but is not reached
is PARK at best; a grid where rule 8 picks FILL 0 is a KILL of the mechanism.
"""
import sys, time
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE = "2026-09-18"
SLUG = "is-the-BINDING-4b-DD-LEG-buyable-by-WHAT-THE-IDLE-SLEEVE-HOLDS"
OUT = ROOT / "research" / "backtests"
STEM = OUT / f"{DATE}_{SLUG}_B"

COST, WARMUP, MAXVOL = 10.0, 260, 0.60
OOS_START = pd.Timestamp("2017-01-01")
DD_CAP, CAGR_FLOOR = 0.60, 0.70
A_N, A_H, A_G = 20, 126, 0.75                       # the frozen 2026-09-04 book
SIGNALS = {"COMPOSITE3": [(21, 252), (0, 126), (0, 63)], "M12_1": [(21, 252)]}
SLEEVES = ["SHY", "IEF", "TLT", "LQD", "TIP", "SPY"]   # DIAL 1 (SPY = equity-fill comparand)
FILLS = [0.00, 0.25, 0.50, 0.75, 1.00]                 # DIAL 2 (0.00 == committed CASH anchor)
COMMITTED_U56 = (0.157147, 1.14804, -0.191276)         # 1264 gate G1 (composite3 anchor)
COMMITTED_M12 = (0.167116, 1.18933, -0.205813)         # 1257's single-leg book
VINTAGE = pd.Timestamp("2026-09-16")                   # cache end date those numbers ran on
GATES: list[dict] = []


def say(*a):
    print(" ".join(str(x) for x in a), flush=True)


def gate(name, value, target, ok):
    GATES.append(dict(gate=name, value=str(value), target=str(target), pass_=bool(ok)))
    say(f"   GATE {name}: {value} vs {target} -> {'PASS' if ok else 'FAIL'}")
    return bool(ok)


# ------------------------------------------------------------------ metrics
def sharpe(r):
    r = np.asarray(r, float)
    if len(r) < 20:
        return np.nan
    v = r.std(ddof=0) * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan


def cagr(r):
    r = np.asarray(r, float)
    if len(r) < 20:
        return np.nan
    return float(np.prod(1.0 + r)) ** (252.0 / len(r)) - 1.0


def mdd(r):
    e = np.cumprod(1.0 + np.asarray(r, float))
    return float((e / np.maximum.accumulate(e) - 1.0).min())


def rankcorr(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    ok = np.isfinite(a) & np.isfinite(b)
    a, b = a[ok], b[ok]
    if len(a) < 3:
        return float("nan")
    ra, rb = pd.Series(a).rank().values, pd.Series(b).rank().values
    sa, sb = ra.std(ddof=0), rb.std(ddof=0)
    if sa == 0 or sb == 0:
        return float("nan")
    return float(((ra - ra.mean()) * (rb - rb.mean())).mean() / (sa * sb))


def stats(r):
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=mdd(r))


def windows(idx, r):
    n = len(r)
    h = n // 2
    o = int(np.searchsorted(idx.values, OOS_START.to_datetime64()))
    return dict(full=stats(r), h1=stats(r[:h]), h2=stats(r[h:]), oos=stats(r[o:]), is_=stats(r[:o]))


def flat(w):
    return {f"{k}_{m}": x for k, v in w.items() for m, x in v.items()}


def year_ret(idx, r, y):
    m = np.asarray(idx.year) == y
    return float(np.prod(1.0 + np.asarray(r, float)[m]) - 1.0) if m.sum() else float("nan")


# ------------------------------------------------------------------ panel
class Panel:
    """Everything independent of the two dials, built once per panel."""

    def __init__(self, name, px, invest):
        need = [s for s in SLEEVES if s not in px.columns]
        if need:                                  # overlay-only columns (never selectable)
            src = pd.read_csv(ROOT / "data" / "prices.csv", index_col=0, parse_dates=True)
            add = src[need].reindex(px.index, method="ffill")
            px = pd.concat([px, add], axis=1)
        self.name = name
        self.px = px
        self.invest = invest
        cols = list(px.columns)
        self.iinv = np.array([cols.index(c) for c in invest])
        self.isleeve = {s: cols.index(s) for s in SLEEVES}
        self.cover = {s: float(px[s].notna().mean()) for s in SLEEVES}
        self.rets = px.pct_change().fillna(0.0).values
        self.priced = px.notna().values
        self.idx = px.index
        q = px[invest]
        self.keys = {}
        for sig, legs in SIGNALS.items():
            parts = []
            for skip, look in legs:
                x = (q.shift(skip) / q.shift(look) - 1.0) if skip else (q / q.shift(look) - 1.0)
                parts.append(x.rank(axis=1, pct=True))
            comp = (sum(parts) / len(parts)).values
            self.keys[sig] = np.where(np.isfinite(comp), -comp, np.inf)
        self.above = (q > q.rolling(200).mean()).values
        qr = q.pct_change()
        vol20 = (qr.rolling(20).std() * np.sqrt(252)).values
        self.volok = np.nan_to_num(vol20, nan=1e9) < MAXVOL
        self.elig = self.above & self.volok
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        m = rebalance_mask(px.index, "W").shift(1, fill_value=False).values.copy()
        m[0] = True
        self.reb = np.flatnonzero(m)


# ------------------------------------------------------------------ the book (dial-free)
def build(pan, sig, N=A_N, H=A_H, lag=1):
    """The committed selection frame at GROSS = 1.0, equal weight across held names.
    IDENTICAL AT EVERY CELL — neither dial touches selection or slot weights."""
    T, M = pan.rets.shape
    K = len(pan.iinv)
    W = np.zeros((T, M))
    cur = np.full(K, -1, dtype=np.int64)
    pr = pan.priced[:, pan.iinv]
    key = pan.keys[sig]
    nreb = len(pan.reb)
    nheld = np.zeros(nreb)
    sumdev = 0.0
    for i, t in enumerate(pan.reb):
        ts = max(t - lag, 0)
        held = np.flatnonzero(cur >= 0)
        young = held[(t - cur[held]) < H] if len(held) else held
        if len(young):
            young = young[pr[t, young]]
        keep = [int(c) for c in young]
        need = N - len(keep)
        take = []
        if need > 0:
            k = key[ts].copy()
            k[~(pan.elig[ts] & pr[ts])] = np.inf
            for c in keep:
                k[c] = np.inf
            order = np.argsort(k, kind="stable")
            for c in order:
                if need == 0 or not np.isfinite(k[c]):
                    break
                take.append(int(c))
                need -= 1
        new = np.full(K, -1, dtype=np.int64)
        for c in keep:
            new[c] = cur[c]
        for c in take:
            new[c] = t
        cur = new
        sel = np.flatnonzero(cur >= 0)
        if not len(sel):
            continue
        w = np.full(len(sel), 1.0 / len(sel))
        sumdev = max(sumdev, abs(float(w.sum()) - 1.0))
        nheld[i] = len(sel)
        stop = pan.reb[i + 1] if i + 1 < nreb else T
        W[t:stop, pan.iinv[sel]] = w
    w0 = int(np.searchsorted(pan.reb, WARMUP))
    return W, dict(n_held=float(nheld[w0:].mean()), sum_dev=float(sumdev))


def run(pan, Wt, sleeve=None, fill=0.0, gross=A_G):
    """Hold gross*Wt plus fill*(idle cash) in `sleeve`, rebalanced weekly, drifting between.
    fill = 0 (or sleeve = None) is the committed CASH book, bit for bit."""
    rets = pan.rets
    T, M = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, M)), C[:-1]])
    held = np.zeros((T, M))
    turn = np.zeros(T)
    curw = np.zeros(M)
    ends = np.append(pan.reb[1:], T)
    j = pan.isleeve[sleeve] if (sleeve is not None and fill > 0.0) else -1
    sw = np.zeros(len(pan.reb))
    maxgross = 0.0
    mincash = 1.0
    for n, (i0, i1) in enumerate(zip(pan.reb, ends)):
        w0 = gross * Wt[i0].copy()
        if j >= 0 and pan.priced[i0, j]:
            idle = 1.0 - w0.sum()
            if idle > 0:
                w0[j] += fill * idle
        sw[n] = w0[j] if j >= 0 else 0.0
        turn[i0] = np.abs(w0 - curw).sum()
        maxgross = max(maxgross, float(w0.sum()))
        mincash = min(mincash, 1.0 - float(w0.sum()))
        base = Cp[i0]
        A = w0[None, :] * (Cp[i0:i1] / base[None, :])
        c0 = 1.0 - w0.sum()
        V = A.sum(axis=1) + c0
        held[i0:i1] = A / V[:, None]
        Ae = w0 * (C[i1 - 1] / base)
        curw = Ae / (Ae.sum() + c0)
    r = (held * rets).sum(axis=1) - turn * COST / 1e4
    w0i = int(np.searchsorted(pan.reb, WARMUP))
    return r, dict(turnover=float(turn.sum() / (T / 252.0)),
                   exposure=float(held[WARMUP:].sum(axis=1).mean()),
                   sleeve_w=float(sw[w0i:].mean()), max_gross=maxgross, min_cash=mincash)


# ------------------------------------------------------------------ KEEP paths
def legs_4a(book, live):
    return dict(H1=book["h1"]["Sharpe"] > live["h1"]["Sharpe"],
                H2=book["h2"]["Sharpe"] > live["h2"]["Sharpe"],
                DD=book["full"]["MaxDD"] >= live["full"]["MaxDD"])


def legs_4b(book, spy):
    return dict(H1=book["h1"]["Sharpe"] > spy["h1"]["Sharpe"],
                H2=book["h2"]["Sharpe"] > spy["h2"]["Sharpe"],
                OOS=book["oos"]["Sharpe"] > spy["oos"]["Sharpe"],
                DD=book["full"]["MaxDD"] >= DD_CAP * spy["full"]["MaxDD"],
                CAGR=book["full"]["CAGR"] >= CAGR_FLOOR * spy["full"]["CAGR"])


def failed(d):
    return ",".join(k for k, v in d.items() if not v) or "-"


# ------------------------------------------------------------------ main
def main():
    t0 = time.time()
    say(f"# {DATE} idea 1268 lane B — {SLUG}")
    say(f"# frozen book: RAW composite, above-200d AND vol20 < {MAXVOL}, N={A_N}, H={A_H}, "
        f"GROSS={A_G}, weekly, {COST:.0f} bps, t+1, warm-up {WARMUP}")
    say(f"# DIAL 1 SLEEVE = {SLEEVES}   (SPY = equity-fill comparand, reported not recommended)")
    say(f"# DIAL 2 FILL   = {FILLS}   (0.00 == the COMMITTED CASH ANCHOR at every sleeve)")
    say("# THE EQUITY BOOK IS BIT-IDENTICAL AT EVERY CELL — only the idle sleeve moves")
    say(f"# reported-not-dials: panel x signal {list(SIGNALS)}")

    panels = []
    px = load_universe()
    panels.append(("U56", px, [c for c in px.columns if c != "SPY"]))
    pb = load_universe(broad=True)
    panels.append((f"B{pb.shape[1]-1}", pb, [c for c in pb.columns if c != "SPY"]))
    psm = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    inv_s = [c for c in psm.columns if c != "SPY" and c not in bad]
    say(f"# SMALL panel: {psm.shape[1]-1} names, {len(bad & set(psm.columns))} dropped for "
        f"max_1d_move >= 1.0 -> {len(inv_s)} investable; sleeve ETFs joined as OVERLAY columns")
    panels.append((f"SMALL{len(inv_s)}", psm, inv_s))

    rows, r8rows, dur_rows, fillrows = [], [], [], []
    for pname, p_px, inv in panels:
        pan = Panel(pname, p_px, inv)
        idx = pan.idx[WARMUP:]
        spy = windows(idx, pan.spy[WARMUP:])
        live_r = backtest(p_px, rules_v2_weights(p_px), cost_bps=COST, freq="W")["returns"].values[WARMUP:]
        live = windows(idx, live_r)
        say(f"\n## {pname}  n_days={len(pan.idx)}  n_names={len(inv)}  window {idx[0].date()}..{idx[-1].date()}")
        say("   sleeve coverage " + "  ".join(f"{s} {pan.cover[s]:.3f}" for s in SLEEVES))
        say(f"   SPY     full {spy['full']['CAGR']:7.2%} / {spy['full']['Sharpe']:.4f} / {spy['full']['MaxDD']:7.2%}"
            f"   halves {spy['h1']['Sharpe']:.4f}/{spy['h2']['Sharpe']:.4f}   OOS {spy['oos']['Sharpe']:.4f}")
        say(f"   LIVE v2 full {live['full']['CAGR']:7.2%} / {live['full']['Sharpe']:.4f} / {live['full']['MaxDD']:7.2%}"
            f"   halves {live['h1']['Sharpe']:.4f}/{live['h2']['Sharpe']:.4f}   OOS {live['oos']['Sharpe']:.4f}")
        say(f"   4b bars: DD cap {DD_CAP*spy['full']['MaxDD']:7.2%}   CAGR floor {CAGR_FLOOR*spy['full']['CAGR']:7.2%}"
            f"   Sharpe H1 {spy['h1']['Sharpe']:.4f} H2 {spy['h2']['Sharpe']:.4f} OOS {spy['oos']['Sharpe']:.4f}")

        for sig in SIGNALS:
            W, bdiag = build(pan, sig)
            say(f"\n   --- signal {sig}  (mean names held {bdiag['n_held']:.2f}) ---")
            say("   sleeve fill |    CAGR   Sharpe    MaxDD |  H1/H2 Sharpe |  OOS Sh |  turn  slv_w | 4a 4b | fail4b")
            cells = {}
            for sl in SLEEVES:
                for fl in FILLS:
                    r, d = run(pan, W, sl, fl)
                    r = r[WARMUP:]
                    w = windows(idx, r)
                    a4, b4 = legs_4a(w, live), legs_4b(w, spy)
                    rec = dict(panel=pname, signal=sig, sleeve=sl, fill=fl, **flat(w), **d,
                               n_held=bdiag["n_held"], y2022=year_ret(idx, r, 2022),
                               y2008=year_ret(idx, r, 2008), y2020=year_ret(idx, r, 2020),
                               keep4a=all(a4.values()), keep4b=all(b4.values()),
                               fail4a=failed(a4), fail4b=failed(b4))
                    rows.append(rec)
                    cells[(sl, fl)] = rec
                    say(f"   {sl:6s} {fl:4.2f} | {w['full']['CAGR']:7.2%} {w['full']['Sharpe']:8.4f} "
                        f"{w['full']['MaxDD']:8.2%} | {w['h1']['Sharpe']:.4f}/{w['h2']['Sharpe']:.4f} | "
                        f"{w['oos']['Sharpe']:7.4f} | {d['turnover']:5.2f} {d['sleeve_w']:5.3f} | "
                        f"{'Y' if all(a4.values()) else 'n'}  {'Y' if all(b4.values()) else 'n'} | {failed(b4)}")

            anc = cells[("SHY", 0.00)]
            # ---- G2: every sleeve at FILL 0 is the CASH anchor, bit for bit
            dev = max(abs(cells[(s, 0.00)]["full_Sharpe"] - anc["full_Sharpe"]) for s in SLEEVES)
            gate(f"G2 {pname}/{sig} FILL-0 rows are one book", f"{dev:.3e}", "== 0.0", dev == 0.0)
            # ---- G3: no leverage anywhere in this arm
            mg = max(c["max_gross"] for c in cells.values())
            mc = min(c["min_cash"] for c in cells.values())
            gate(f"G3 {pname}/{sig} no leverage", f"max gross {mg:.6f}, min cash {mc:.6f}",
                 "<= 1.0 / >= 0.0", mg <= 1.0 + 1e-12 and mc >= -1e-12)
            # ---- G5: turnover non-decreasing in FILL (mechanical)
            worst = min(cells[(s, FILLS[i + 1])]["turnover"] - cells[(s, FILLS[i])]["turnover"]
                        for s in SLEEVES for i in range(len(FILLS) - 1))
            gate(f"G5 {pname}/{sig} turnover non-decreasing in FILL", f"worst step {worst:+.4f}",
                 ">= 0", worst >= -1e-9)

            # ---- H_DUR: duration vs the SPY equity fill at matched FILL
            for fl in FILLS[1:]:
                bestdur = min((cells[(s, fl)] for s in SLEEVES if s != "SPY"),
                              key=lambda c: -c["full_MaxDD"])
                spyc = cells[("SPY", fl)]
                dur_rows.append(dict(panel=pname, signal=sig, fill=fl, best_dur=bestdur["sleeve"],
                                     dur_MaxDD=bestdur["full_MaxDD"], spy_MaxDD=spyc["full_MaxDD"],
                                     dur_CAGR=bestdur["full_CAGR"], spy_CAGR=spyc["full_CAGR"],
                                     dur_Sharpe=bestdur["full_Sharpe"], spy_Sharpe=spyc["full_Sharpe"],
                                     dur_beats_spy_DD=bestdur["full_MaxDD"] > spyc["full_MaxDD"]))

            # ---- rule 8: choose (SLEEVE, FILL) on IS only, read OOS once
            ks = list(cells)
            is_s = np.array([cells[k]["is__Sharpe"] for k in ks])
            oos_s = np.array([cells[k]["oos_Sharpe"] for k in ks])
            pick = ks[int(np.nanargmax(is_s))]
            r8 = dict(panel=pname, signal=sig, pick_sleeve=pick[0], pick_fill=pick[1],
                      pick_IS=cells[pick]["is__Sharpe"], pick_OOS=cells[pick]["oos_Sharpe"],
                      donothing_OOS=anc["oos_Sharpe"],
                      delta=cells[pick]["oos_Sharpe"] - anc["oos_Sharpe"],
                      pick_OOS_CAGR=cells[pick]["oos_CAGR"], nothing_OOS_CAGR=anc["oos_CAGR"],
                      pick_OOS_MaxDD=cells[pick]["oos_MaxDD"], nothing_OOS_MaxDD=anc["oos_MaxDD"],
                      cellmean_OOS=float(np.nanmean(oos_s)), worst_OOS=float(np.nanmin(oos_s)),
                      best_OOS=float(np.nanmax(oos_s)), rank_IS_OOS=rankcorr(is_s, oos_s),
                      spy_OOS=spy["oos"]["Sharpe"], live_OOS=live["oos"]["Sharpe"],
                      pick_keep4b=cells[pick]["keep4b"], nothing_keep4b=anc["keep4b"])
            r8rows.append(r8)
            # ---- POST-HOC DIAL REDUCTION, DECLARED AS SUCH.  Not pre-registered: it was
            # written after the grid was read, because the grid showed rule 8's loss is
            # entirely the SLEEVE ASSET choice (TLT at 6 of 6) and not the FILL choice.  With
            # the sleeve FROZEN a priori this is a ONE-dial idea; every sleeve is reported so
            # no asset is cherry-picked, and the run does NOT claim IEF was chosen in advance.
            for sl in SLEEVES:
                kk = [(sl, f) for f in FILLS]
                iss = np.array([cells[k]["is__Sharpe"] for k in kk])
                pk = kk[int(np.nanargmax(iss))]
                fillrows.append(dict(panel=pname, signal=sig, sleeve=sl, pick_fill=pk[1],
                                     pick_IS=cells[pk]["is__Sharpe"], pick_OOS=cells[pk]["oos_Sharpe"],
                                     donothing_OOS=anc["oos_Sharpe"],
                                     delta=cells[pk]["oos_Sharpe"] - anc["oos_Sharpe"],
                                     pick_full_CAGR=cells[pk]["full_CAGR"],
                                     pick_full_Sharpe=cells[pk]["full_Sharpe"],
                                     pick_full_MaxDD=cells[pk]["full_MaxDD"],
                                     pick_keep4b=cells[pk]["keep4b"], nothing_keep4b=anc["keep4b"],
                                     rank_IS_OOS=rankcorr(iss, [cells[k]["oos_Sharpe"] for k in kk])))
            say(f"   RULE 8  IS-argmax = {pick[0]} / FILL {pick[1]:.2f} (IS Sh {r8['pick_IS']:.4f}) -> "
                f"OOS {r8['pick_OOS']:.4f} vs do-nothing {r8['donothing_OOS']:.4f}  delta {r8['delta']:+.4f}"
                f"   cellmean {r8['cellmean_OOS']:.4f}  worst {r8['worst_OOS']:.4f}  "
                f"rank corr IS/OOS {r8['rank_IS_OOS']:+.2f}")

            # ---- G1/G4: vintage-pinned replay of the committed anchor
            if pname == "U56":
                q = p_px.loc[:VINTAGE]
                vpan = Panel("U56v", q, [c for c in q.columns if c != "SPY"])
                Wv, _ = build(vpan, sig)
                rv, _ = run(vpan, Wv, None, 0.0)
                mv = stats(rv[WARMUP:])
                tgt = COMMITTED_U56 if sig == "COMPOSITE3" else COMMITTED_M12
                dv = max(abs(mv["CAGR"] - tgt[0]), abs(mv["Sharpe"] - tgt[1]), abs(mv["MaxDD"] - tgt[2]))
                gate(f"{'G1' if sig == 'COMPOSITE3' else 'G4'} vintage-pinned anchor replay ({sig})",
                     f"({mv['CAGR']:.6f}, {mv['Sharpe']:.5f}, {mv['MaxDD']:.6f}) dev {dv:.2e}",
                     f"{tgt} to 1e-4", dv < 1e-4)

    grid = pd.DataFrame(rows)
    wf = pd.DataFrame(r8rows)
    dur = pd.DataFrame(dur_rows)
    fr = pd.DataFrame(fillrows)
    grid.to_csv(f"{STEM}.grid.csv", index=False)
    wf.to_csv(f"{STEM}.walkforward.csv", index=False)
    dur.to_csv(f"{STEM}.duration_vs_equityfill.csv", index=False)
    fr.to_csv(f"{STEM}.rule8_fill_only.csv", index=False)

    # ---- G6 determinism
    pan = Panel("U56", panels[0][1], panels[0][2])
    W, _ = build(pan, "COMPOSITE3")
    chk = [sharpe(run(pan, W, s, f)[0][WARMUP:]) for s in SLEEVES for f in FILLS]
    ref = grid[(grid.panel == "U56") & (grid.signal == "COMPOSITE3")].full_Sharpe.values
    dd = float(np.max(np.abs(np.array(chk) - ref)))
    gate("G6 determinism (U56 composite3 grid re-run)", f"{dd:.3e}", "== 0.0", dd == 0.0)
    pd.DataFrame(GATES).to_csv(f"{STEM}.gates.csv", index=False)

    # ---- hypotheses
    say("\n## HYPOTHESES")
    anch = grid[grid.fill == 0.00]
    nonspy = grid[(grid.sleeve != "SPY") & (grid.fill > 0)]
    conv = []
    for (p, s), g in nonspy.groupby(["panel", "signal"]):
        a = anch[(anch.panel == p) & (anch.signal == s)].iloc[0]
        for _, c in g.iterrows():
            if c.keep4b and not a.keep4b:
                conv.append(dict(panel=p, signal=s, sleeve=c.sleeve, fill=c.fill,
                                 CAGR=c.full_CAGR, anchor_CAGR=a.full_CAGR,
                                 dCAGR=c.full_CAGR - a.full_CAGR,
                                 MaxDD=c.full_MaxDD, anchor_MaxDD=a.full_MaxDD,
                                 dMaxDD=c.full_MaxDD - a.full_MaxDD,
                                 dSharpe=c.full_Sharpe - a.full_Sharpe,
                                 dOOS=c.oos_Sharpe - a.oos_Sharpe, dturn=c.turnover - a.turnover))
    cv = pd.DataFrame(conv)
    cv.to_csv(f"{STEM}.conversions.csv", index=False)
    h_dd = len(cv) > 0
    say(f"   H_DD   non-SPY cells converting a committed 4b FAIL -> PASS: {len(cv)}  -> "
        f"{'HELD' if h_dd else 'FAILED'}")
    if h_dd:
        ch = cv.sort_values("dCAGR", ascending=False).iloc[0]
        h_free = ch.dCAGR >= 0
        say(f"   H_FREE cheapest conversion {ch.panel}/{ch.signal} {ch.sleeve}/FILL {ch.fill:.2f}: "
            f"d_CAGR {ch.dCAGR:+.2%}  d_MaxDD {ch.dMaxDD:+.2%}  d_Sharpe {ch.dSharpe:+.4f}  "
            f"d_OOS {ch.dOOS:+.4f}  d_turn {ch.dturn:+.2f}/yr -> {'HELD' if h_free else 'FAILED'}")
    else:
        h_free = False
        say("   H_FREE not evaluable (no conversions) -> FAILED")
    h_r8 = bool(((wf.pick_fill > 0) & (wf.delta > 0)).any())
    say(f"   H_R8   rule 8 picks a NON-CASH sleeve at {int((wf.pick_fill > 0).sum())} of {len(wf)} arms; "
        f"beats do-nothing OOS at {int((wf.delta > 0).sum())} of {len(wf)}; mean delta {wf.delta.mean():+.4f}"
        f" -> {'HELD' if h_r8 else 'FAILED'}")
    h_dur = bool(dur.dur_beats_spy_DD.mean() > 0.5)
    say(f"   H_DUR  best duration sleeve beats the SPY fill on MaxDD at "
        f"{int(dur.dur_beats_spy_DD.sum())} of {len(dur)} (panel,signal,FILL) -> "
        f"{'HELD' if h_dur else 'FAILED'}")

    say("\n## SUMMARY")
    say(f"   cells {len(grid)}   4a passes {int(grid.keep4a.sum())}   4b passes {int(grid.keep4b.sum())}")
    for p in grid.panel.unique():
        for s in SIGNALS:
            g = grid[(grid.panel == p) & (grid.signal == s)]
            say(f"   {p:10s} {s:11s} 4b {int(g.keep4b.sum()):2d}/{len(g)}   "
                f"MaxDD {g.full_MaxDD.min():7.2%}..{g.full_MaxDD.max():7.2%}   "
                f"CAGR {g.full_CAGR.min():6.2%}..{g.full_CAGR.max():6.2%}   "
                f"turn {g.turnover.min():.2f}..{g.turnover.max():.2f}")
    say("   4b FAIL legs over all failing cells: " +
        "  ".join(f"{k} {v}" for k, v in
                  pd.Series([x for f in grid.loc[~grid.keep4b, "fail4b"] for x in f.split(",")]
                            ).value_counts().items()))
    say("   POOLED non-SPY sleeve vs its own FILL-0 anchor (same equity book):")
    for fl in FILLS[1:]:
        g = grid[(grid.sleeve != "SPY") & (grid.fill == fl)]
        d = []
        for _, c in g.iterrows():
            a = anch[(anch.panel == c.panel) & (anch.signal == c.signal)].iloc[0]
            d.append((c.full_CAGR - a.full_CAGR, c.full_Sharpe - a.full_Sharpe,
                      c.full_MaxDD - a.full_MaxDD, c.oos_Sharpe - a.oos_Sharpe))
        d = np.array(d)
        say(f"     FILL {fl:.2f}  d_CAGR {d[:,0].mean():+.2%}  d_Sharpe {d[:,1].mean():+.4f} "
            f"(positive {int((d[:,1]>0).sum())}/{len(d)})  d_MaxDD {d[:,2].mean():+.2%} "
            f"(positive {int((d[:,2]>0).sum())}/{len(d)})  d_OOS {d[:,3].mean():+.4f}")
    say("   CALENDAR STRESS (the duration bear): 2022 return by sleeve at FILL 1.00, U56/COMPOSITE3")
    g = grid[(grid.panel == "U56") & (grid.signal == "COMPOSITE3")]
    say("     " + "  ".join(f"{r.sleeve} {r.y2022:+.2%}" for _, r in g[g.fill == 1.00].iterrows())
        + f"   | anchor(CASH) {g[g.fill==0].iloc[0].y2022:+.2%}")
    say(f"   rule 8 picks: " + ", ".join(f"{r.panel}/{r.signal}={r.pick_sleeve}@{r.pick_fill:.2f}"
                                        f"({r.delta:+.4f})" for _, r in wf.iterrows()))
    say("   PER-SLEEVE d_MaxDD vs the SAME equity book's CASH anchor (mean over 6 arms, by FILL):")
    for sl in SLEEVES:
        line = []
        for fl in FILLS[1:]:
            g = grid[(grid.sleeve == sl) & (grid.fill == fl)]
            d = [c.full_MaxDD - anch[(anch.panel == c.panel) & (anch.signal == c.signal)].iloc[0].full_MaxDD
                 for _, c in g.iterrows()]
            line.append(f"{fl:.2f} {np.mean(d):+.2%}({int(np.sum(np.array(d)>0))}/{len(d)})")
        say(f"     {sl:4s}  " + "  ".join(line))
    say("\n## POST-HOC (NOT PRE-REGISTERED): RULE 8 WITH THE SLEEVE FROZEN, FILL THE ONLY DIAL")
    say("   sleeve | picks FILL | beats do-nothing OOS | mean delta | mean IS/OOS rank corr | 4b at pick")
    for sl in SLEEVES:
        g = fr[fr.sleeve == sl]
        say(f"   {sl:6s} | {sorted(set(g.pick_fill.round(2)))} | {int((g.delta>0).sum())} of {len(g)} | "
            f"{g.delta.mean():+.4f} | {g.rank_IS_OOS.mean():+.2f} | {int(g.pick_keep4b.sum())} of {len(g)}")
    best = grid[(grid.sleeve != "SPY") & grid.keep4b & (grid.fill > 0)]
    if len(best):
        say("\n   NON-SPY 4b PASSES THAT STRICTLY DOMINATE THEIR OWN CASH ANCHOR (CAGR, Sharpe, MaxDD, OOS all better):")
        for _, c in best.iterrows():
            a = anch[(anch.panel == c.panel) & (anch.signal == c.signal)].iloc[0]
            if (c.full_CAGR > a.full_CAGR and c.full_Sharpe > a.full_Sharpe
                    and c.full_MaxDD > a.full_MaxDD and c.oos_Sharpe > a.oos_Sharpe):
                say(f"     {c.panel}/{c.signal} {c.sleeve}@{c.fill:.2f}: {c.full_CAGR:.2%} / {c.full_Sharpe:.4f} / "
                    f"{c.full_MaxDD:.2%}  halves {c.h1_Sharpe:.4f}/{c.h2_Sharpe:.4f}  OOS {c.oos_Sharpe:.4f}  "
                    f"turn {c.turnover:.2f}  vs anchor {a.full_CAGR:.2%} / {a.full_Sharpe:.4f} / {a.full_MaxDD:.2%} "
                    f"OOS {a.oos_Sharpe:.4f} turn {a.turnover:.2f}")
                r2 = wf[(wf.panel == c.panel) & (wf.signal == c.signal)].iloc[0]
                rf1 = fr[(fr.panel == c.panel) & (fr.signal == c.signal) & (fr.sleeve == c.sleeve)].iloc[0]
                say(f"        reached by 2-dial rule 8: "
                    f"{'YES' if (r2.pick_sleeve == c.sleeve and abs(r2.pick_fill - c.fill) < 1e-9) else f'NO (it picks {r2.pick_sleeve}@{r2.pick_fill:.2f})'}"
                    f"   |  by FILL-only rule 8 with this sleeve frozen: "
                    f"{'YES' if abs(rf1.pick_fill - c.fill) < 1e-9 else f'NO (it picks FILL {rf1.pick_fill:.2f})'}")
    say("\n## THE SHY CONTROL: DURATION EXCESS OVER BILLS ON THE SAME EQUITY BOOK AT THE SAME FILL")
    say("   (the engine pays 0% on cash, so SHY@FILL ~= the non-zero cash rate, NOT a strategy)")
    ctl = []
    for _, c in grid[(grid.sleeve != "SHY") & (grid.fill > 0)].iterrows():
        b = grid[(grid.panel == c.panel) & (grid.signal == c.signal)
                 & (grid.sleeve == "SHY") & (abs(grid.fill - c.fill) < 1e-9)].iloc[0]
        ctl.append(dict(panel=c.panel, signal=c.signal, sleeve=c.sleeve, fill=c.fill,
                        dCAGR=c.full_CAGR - b.full_CAGR, dSharpe=c.full_Sharpe - b.full_Sharpe,
                        dMaxDD=c.full_MaxDD - b.full_MaxDD, dOOS=c.oos_Sharpe - b.oos_Sharpe,
                        dH1=c.h1_Sharpe - b.h1_Sharpe, dH2=c.h2_Sharpe - b.h2_Sharpe,
                        keep4b=c.keep4b, shy_keep4b=b.keep4b))
    ctl = pd.DataFrame(ctl)
    ctl.to_csv(f"{STEM}.shy_control.csv", index=False)
    say("   sleeve | d_CAGR  d_Sharpe  d_MaxDD  d_OOS_Sharpe (mean over 6 arms x 4 fills; positive count)")
    for sl in [x for x in SLEEVES if x != "SHY"]:
        g = ctl[ctl.sleeve == sl]
        say(f"   {sl:6s} | {g.dCAGR.mean():+.2%} ({int((g.dCAGR>0).sum())}/{len(g)})  "
            f"{g.dSharpe.mean():+.4f} ({int((g.dSharpe>0).sum())}/{len(g)})  "
            f"{g.dMaxDD.mean():+.2%} ({int((g.dMaxDD>0).sum())}/{len(g)})  "
            f"{g.dOOS.mean():+.4f} ({int((g.dOOS>0).sum())}/{len(g)})")
    say("   OOS-SHARPE EXCESS OVER SHY BY FILL (is the duration excess there out of sample?):")
    for sl in [x for x in SLEEVES if x != "SHY"]:
        say(f"     {sl:4s}  " + "  ".join(
            f"{fl:.2f} {ctl[(ctl.sleeve==sl)&(abs(ctl.fill-fl)<1e-9)].dOOS.mean():+.4f}"
            f"({int((ctl[(ctl.sleeve==sl)&(abs(ctl.fill-fl)<1e-9)].dOOS>0).sum())}/6)" for fl in FILLS[1:]))
    say("   FILL-ONLY RULE 8 PICK vs THE SHY CONTROL AT THE SAME FILL (OOS Sharpe):")
    for sl in [x for x in SLEEVES if x != "SHY"]:
        d = []
        for _, r_ in fr[fr.sleeve == sl].iterrows():
            b = grid[(grid.panel == r_.panel) & (grid.signal == r_.signal) & (grid.sleeve == "SHY")
                     & (abs(grid.fill - r_.pick_fill) < 1e-9)].iloc[0]
            d.append(r_.pick_OOS - b.oos_Sharpe)
        say(f"     {sl:4s}  mean {np.mean(d):+.4f}  positive {int(np.sum(np.array(d)>0))} of {len(d)}")
    say(f"   GATES {sum(g['pass_'] for g in GATES)} of {len(GATES)} pass   {time.time()-t0:.0f}s")


if __name__ == "__main__":
    main()
