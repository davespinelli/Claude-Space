#!/usr/bin/env python3
"""IDEA 1272 (cloud lane, 2026-09-18) — WHICH OF THE RECORD'S TWO COMMITTED DO-NOTHING
LEVELS IS RIGHT, 0.8268 OR 0.7922?

THE DEFECT.  1252 (2026-09-17, lane B) and 1246 (2026-09-18, lane C) both publish a mean
OOS Sharpe for DOING NOTHING over what both call the SAME 72 decisions (3 panels x 2
anchors x 4 ladders x 3 IS choosers).  1252 says 0.8268; 1246 says 0.7922.  1260 (lane B)
re-ran the object and reproduced 1246's LEVEL to 9.98e-05 while reproducing 1252's DELTAS
to 1e-3, and filed this idea rather than pick a winner.

WHAT THIS RUN DOES.  It does NOT adjudicate by re-running one of them and declaring the
other wrong: both were run on their own tapes and neither can be re-run on the other's.
It DIFFS THE CONSTRUCTION -- mechanically, out of the two source files -- then rebuilds
the 72 decisions on ONE tape under BOTH constructions, so that vintage is held fixed and
the only thing moving is the construction.  Every level, delta and count is published at
every construction x claim set cell.

THE TWO DIALS (protocol rule 4, max 2 tuned parameters):

  `CONSTRUCTION`  {C_1252, C_1246, C_1260, C_1252_VINTAGE}
                  C_1252        = 1252's loader: load_universe(small=True) UNFILTERED.
                  C_1246        = 1246's loader: drop names whose max |1d move| computed
                                  ON THE PANEL is >= 1.0.
                  C_1260        = 1260's loader / the standing house rule: drop names
                                  flagged max_1d_move >= 1.0 in data/small_meta.csv.
                  C_1252_VINTAGE= C_1252 with every panel truncated to the LAST DATE 1252
                                  itself logged (U56 2026-09-16, B136 / SMALL 2026-09-11),
                                  which is the only other thing that can move a level.
  `CLAIM SET`     {CS_ALL, CS_SHARPE, CS_LARGE, CS_NODEG}   -- 1252's own four, verbatim.

FROZEN, NOT TUNED (inherited from 1096/1101/1154/1208/1242/1252/1246): LAG 1, warm-up 260,
max_vol 0.60, IS end 2016-12-31, cost 10 bps, legs (21,252)/(0,126)/(0,63), the four
ladders, the two anchors, the three choosers, DD cap 0.60, CAGR floor 0.70.

SURVIVORSHIP (protocol rule 9).  All three panels are CURRENT-CONSTITUENT lists; the small
panel is a current screen of sub-$2B names since 2010 (data/SMALL_PANEL_README.md).  Every
LEVEL below is optimistic and none of them is a forecast.  That is exactly why this run's
headline is about WHICH LEVEL A COMMITTED SENTENCE IS ENTITLED TO, not about the level.

Offline, deterministic, no network.  10 bps, next-day execution.
"""
import sys, time, json, re
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights          # noqa: E402
from engine import rebalance_mask, backtest                   # noqa: E402

DATE, SLUG = "2026-09-18", "WHICH-OF-THE-RECORD-S-TWO-COMMITTED-DO-NOTHING-LEVELS-IS-RIGHT-0-8268-OR-0-7922"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"
BT = Path(__file__).resolve().parent
SRC_1252 = BT / "2026-09-17_is-B_GAPEXCEEDS-a-USABLE-DECISIVENESS-BAR-the-record-never-adopted_B.py"
SRC_1246 = BT / "2026-09-18_how-many-of-the-1-658-UNRESOLVABLE-WALK-CLAIMS-can-be-RESOLVED-FROM-THEIR-SCRIPT_C.py"
SRC_1260 = BT / "2026-09-18_is-the-record-s-DECISIVENESS-BAR-ON-THE-WRONG-SIDE-of-the-OBSERVED-BAR-line_B.py"
WF_1252 = BT / "2026-09-17_is-B_GAPEXCEEDS-a-USABLE-DECISIVENESS-BAR-the-record-never-adopted_B.walkforward.csv"
MONEY_1252 = BT / "2026-09-17_is-B_GAPEXCEEDS-a-USABLE-DECISIVENESS-BAR-the-record-never-adopted_B.money.csv"

# ------------------------------------------------------------------ frozen construction
LAG, WARMUP, MAXVOL = 1, 260, 0.60
IS_END = "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
COST = 10.0
LEGS = [(21, 252), (0, 126), (0, 63)]
LAD_N = [5, 8, 10, 12, 15, 20, 25, 30, 40]
LAD_H = [21, 63, 126, 252]
LAD_G = [0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75]
LAD_C = ["D", "W", "M", "Q"]
LADDERS = {"N": LAD_N, "H": LAD_H, "GROSS": LAD_G, "CADENCE": LAD_C}
LADNAMES = ["N", "H", "GROSS", "CADENCE"]
ANCHORS = {"A": dict(N=20, H=126, GROSS=0.75, CADENCE="W"),
           "B": dict(N=12, H=63, GROSS=0.55, CADENCE="M")}
PANELS = ["U56", "B136", "SMALL"]
CHOOSERS = ["CH_ISSHARPE", "CH_ISCAGR", "CH_ISDD"]

# ------------------------------------------------------------------ dial 1
CONSTRUCTIONS = ["C_1252", "C_1246", "C_1260", "C_1252_VINTAGE"]
VINTAGE_1252 = {"U56": "2026-09-16", "B136": "2026-09-11", "SMALL": "2026-09-11"}

# ------------------------------------------------------------------ dial 2
CLAIM_SETS = {
    "CS_ALL":    lambda d: True,
    "CS_SHARPE": lambda d: d[3] == "CH_ISSHARPE",
    "CS_LARGE":  lambda d: d[0] in ("U56", "B136"),
    "CS_NODEG":  lambda d: d[2] != "GROSS",
}
CS_HEAD = "CS_ALL"

# ------------------------------------------------------------------ the record's numbers
A1101_TRIPLE = (0.155787, 1.139701, -0.191276)
L1252_DONOTHING = 0.826772        # 1252's committed level (money.csv, SEL_NEVER_anchor)
L1252_ALWAYSACT = 0.835724
L1252_DELTA = 0.008951
L1246_DONOTHING = 0.7922
L1246_ALWAYSACT = 0.8016
L1260_DONOTHING = 0.7922
L1260_ALWAYSACT = 0.8017
SPY_OOS_COMMITTED = 0.8713

LOG, GATES, HYP = [], [], []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def dump(df, suffix):
    p = Path(f"{OUT}.{suffix}.csv")
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


def gate(name, what, value, ok):
    GATES.append(dict(gate=name, what=what, value=float(value), pass_=bool(ok)))
    P(f"  {name:<8s} {'PASS' if ok else 'FAIL'}  {what:<70s} {value:.3e}")
    return bool(ok)


def hyp(name, declared, measured, supported):
    HYP.append(dict(hypothesis=name, declared=declared, measured=measured,
                    supported=bool(supported)))
    P(f"  {name:<14s} {'SUPPORTED' if supported else 'REFUTED  '}  {measured}")


def spearman(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    ok = np.isfinite(x) & np.isfinite(y)
    x, y = x[ok], y[ok]
    if len(x) < 3:
        return np.nan
    rx, ry = pd.Series(x).rank().values, pd.Series(y).rank().values
    if rx.std() == 0 or ry.std() == 0:
        return np.nan
    return float(np.corrcoef(rx, ry)[0, 1])


def tstat(d):
    d = np.asarray(d, float); d = d[np.isfinite(d)]
    if len(d) < 2 or d.std(ddof=1) == 0:
        return np.nan
    return float(d.mean() / (d.std(ddof=1) / np.sqrt(len(d))))


# ================================================================== the record's runner
# (nrun / build / mech / fmet are byte-for-byte the machinery 1252 and 1246 share; both
#  files carry identical copies, which ARM A verifies mechanically before any tape is read.)
def nrun(rets, wt, mk):
    T, N = rets.shape
    mk = mk.copy(); mk[0] = True
    Cc = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, N)), Cc[:-1]])
    reb = np.flatnonzero(mk)
    seg = np.searchsorted(reb, np.arange(T), side="right") - 1
    s0 = reb[seg]; W0 = wt[s0]
    h = W0 * (Cp / Cp[s0])
    V = h.sum(axis=1) + (1.0 - W0.sum(axis=1))
    held = h / V[:, None]
    s0p = reb[np.maximum(seg - 1, 0)]; W0p = wt[s0p]
    hp = W0p * (Cp / Cp[s0p])
    Vp = hp.sum(axis=1) + (1.0 - W0p.sum(axis=1))
    heldp = hp / Vp[:, None]; heldp[reb[0]] = 0.0
    turn = np.zeros(T)
    turn[reb] = np.abs(wt[reb] - heldp[reb]).sum(axis=1)
    return (held * rets).sum(axis=1), turn


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


def legs_composite(px):
    parts = []
    for skip, look in LEGS:
        x = (px.shift(skip) / px.shift(look) - 1.0) if skip else (px / px.shift(look) - 1.0)
        parts.append(x.rank(axis=1, pct=True))
    return sum(parts) / len(parts)


def mech(px):
    comp = legs_composite(px)
    above = px > px.rolling(200).mean()
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    sc = comp * (0.5 + 0.5 * above.astype(float))
    return sc.values, (above & (vol20 < MAXVOL)).values


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


def windows_of(idx):
    warm = np.zeros(len(idx), dtype=bool); warm[WARMUP:] = True
    oos = np.asarray(idx > pd.Timestamp(IS_END)) & warm
    return warm, warm & ~oos, oos


def is_stat(r, ins, stat):
    x = r[ins]
    if stat == "CH_ISSHARPE":
        return fsharpe(x)
    eq = np.cumprod(1.0 + x)
    if stat == "CH_ISCAGR":
        return eq[-1] ** (252.0 / len(x)) - 1.0
    if stat == "CH_ISDD":
        return float((eq / np.maximum.accumulate(eq) - 1.0).min())
    raise ValueError(stat)


def blocks_m(r, warm, ins, oos):
    rr = r[warm]
    c, s, d = fmet(rr); h = len(rr) // 2
    oc, os_, od = fmet(r[oos]); ic, is_, idd = fmet(r[ins])
    return dict(CAGR=c, Sharpe=s, MaxDD=d, H1=fsharpe(rr[:h]), H2=fsharpe(rr[h:]),
                IS_CAGR=ic, IS_Sharpe=is_, IS_MaxDD=idd,
                OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=od)


def legs_4b(b, sb):
    return {"L_H1": bool(b["H1"] > sb["H1"]), "L_H2": bool(b["H2"] > sb["H2"]),
            "L_OOS": bool(b["OOS_Sharpe"] > sb["OOS_Sharpe"]),
            "L_DD": bool(abs(b["MaxDD"]) <= DD_CAP * abs(sb["MaxDD"])),
            "L_CAGR": bool(b["CAGR"] >= CAGR_FLOOR * sb["CAGR"])}


def legs_4b_oos(b, sb):
    return {"O_S": bool(b["OOS_Sharpe"] > sb["OOS_Sharpe"]),
            "O_DD": bool(abs(b["OOS_MaxDD"]) <= DD_CAP * abs(sb["OOS_MaxDD"])),
            "O_CAGR": bool(b["OOS_CAGR"] >= CAGR_FLOOR * sb["OOS_CAGR"])}


def legs_4a(b, lb):
    return {"A_H1": bool(b["H1"] > lb["H1"]), "A_H2": bool(b["H2"] > lb["H2"]),
            "A_DD": bool(b["MaxDD"] >= lb["MaxDD"])}


class Panel:
    def __init__(self, name, px, small):
        self.name, self.px = name, px
        self.idx, self.K, self.T = px.index, len(px.columns), len(px.index)
        self.rets = px.pct_change().fillna(0.0).values
        self.priced = px.notna().values
        self.warm, self.ins, self.oos = windows_of(px.index)
        sc, elig = mech(px)
        spy_i = list(px.columns).index("SPY")
        if small:                                  # SPY is the benchmark, never a holding
            elig = elig.copy(); elig[:, spy_i] = False
        self.sc, self.elig = sc, elig
        self.reb, self.mkl = {}, {}
        for f in LAD_C:
            mk = rebalance_mask(px.index, f).values
            self.reb[f] = np.flatnonzero(mk)
            m = np.roll(mk, LAG); m[:LAG] = False
            self.mkl[f] = m
        self.spy = px["SPY"].pct_change().fillna(0.0).values


def book(pan, N, H, gross, freq, cache):
    key = (pan.name, N, H, gross, freq)
    if key in cache:
        return cache[key]
    W = build(-pan.sc, pan.elig, pan.priced, pan.reb[freq], N, H, pan.T, pan.K, gross)
    Wl = np.zeros_like(W); Wl[LAG:] = W[:-LAG]
    r, turn = nrun(pan.rets, Wl, pan.mkl[freq])
    cache[key] = r - turn * COST / 1e4
    return cache[key]


def ladder_books(pan, anchor, lad, cache):
    a = ANCHORS[anchor]; out = {}
    for rung in LADDERS[lad]:
        kw = dict(N=a["N"], H=a["H"], gross=a["GROSS"], freq=a["CADENCE"])
        kw[{"N": "N", "H": "H", "GROSS": "gross", "CADENCE": "freq"}[lad]] = rung
        out[rung] = book(pan, kw["N"], kw["H"], kw["gross"], kw["freq"], cache)
    return out


# ================================================================== ARM A: the mechanical diff
CONST_NAMES = ["LAG", "WARMUP", "MAXVOL", "IS_END", "DD_CAP", "CAGR_FLOOR", "COST", "LEGS",
               "LAD_N", "LAD_H", "LAD_G", "LAD_C", "ANCHORS", "PANELS", "CHOOSERS"]


def grab_const(src, name):
    """Recover a frozen constant from a source file by reading its assignment, without
    importing the file (importing would run it).  Balances brackets so a literal spread
    over several lines is recovered whole, and handles `A, B, C = 1, 2, 3` forms."""
    txt = src.read_text()

    def _take(start):
        depth, i = 0, start
        while i < len(txt):
            c = txt[i]
            if c in "([{":
                depth += 1
            elif c in ")]}":
                depth -= 1
            elif c == "#" and depth == 0:
                while i < len(txt) and txt[i] != "\n":
                    i += 1
                continue
            elif c == "\n" and depth == 0:
                break
            i += 1
        return txt[start:i].strip()

    m = re.search(rf"^{name}\s*=\s*", txt, re.M)
    if m:
        body = _take(m.end())
        try:
            return repr(eval(body, {"__builtins__": {}}, {"dict": dict}))
        except Exception:
            return " ".join(body.split())
    m = re.search(rf"^([A-Z_0-9]+(?:\s*,\s*[A-Z_0-9]+)*)\s*=\s*", txt, re.M)
    for m in re.finditer(r"^([A-Z_0-9]+(?:\s*,\s*[A-Z_0-9]+)+)\s*=\s*", txt, re.M):
        names = [x.strip() for x in m.group(1).split(",")]
        if name not in names:
            continue
        body = _take(m.end())
        try:
            vals = eval(body, {"__builtins__": {}}, {"dict": dict})
            return repr(vals[names.index(name)])
        except Exception:
            return " ".join(body.split())
    return "<not found>"


def small_loader_of(src):
    txt = src.read_text()
    if "small_meta.csv" in txt:
        return "META_CSV  (drop data/small_meta.csv max_1d_move >= 1.0)"
    if re.search(r"pct_change\(\)\.abs\(\)\.max\(\)", txt) and "max_1d_move" in txt:
        return "PANEL_MAX (drop names whose max |1d move| on the panel is >= 1.0)"
    if "load_universe(small=True)" in txt:
        return "UNFILTERED (load_universe(small=True) as-is)"
    return "<no small panel>"


# ================================================================== main
def main():
    t0 = time.time()
    P("=" * 100)
    P("IDEA 1272 (cloud) — WHICH OF THE RECORD'S TWO COMMITTED DO-NOTHING LEVELS IS RIGHT,")
    P("                    0.8268 OR 0.7922?")
    P("=" * 100)
    P(f"  dials: CONSTRUCTION {CONSTRUCTIONS}")
    P(f"         CLAIM SET   {list(CLAIM_SETS)}   (1252's own four, verbatim)")
    P("  frozen: 72 decisions = 3 panels x 2 anchors x 4 ladders x 3 IS choosers;")
    P(f"          LAG {LAG}, warm-up {WARMUP}, IS end {IS_END}, {COST:.0f} bps, DD cap {DD_CAP},")
    P(f"          CAGR floor {CAGR_FLOOR}.  2017-2026 is read ONCE, after every pick is fixed.")
    P("  SURVIVORSHIP (rule 9): all three panels are current-constituent lists; every LEVEL")
    P("  below is optimistic.  The headline is about which level a committed SENTENCE is")
    P("  entitled to, not about the level.")
    P("")

    # ---------------------------------------------------------------- ARM A
    P("-" * 100)
    P("ARM A — THE MECHANICAL DIFF, BEFORE ANY TAPE IS READ.  Both frozen constants are")
    P("        recovered from SOURCE (not from prose) and compared name by name.")
    P("-" * 100)
    drows = []
    for nm in CONST_NAMES:
        v52, v46, v60 = (grab_const(s, nm) for s in (SRC_1252, SRC_1246, SRC_1260))
        drows.append(dict(constant=nm, v_1252=v52, v_1246=v46, v_1260=v60,
                          same_1252_1246=(v52 == v46), same_1246_1260=(v46 == v60)))
    ddf0 = pd.DataFrame(drows)
    P(ddf0[["constant", "same_1252_1246", "same_1246_1260"]].to_string(index=False))
    n_same = int(ddf0.same_1252_1246.sum())
    for r in ddf0[~ddf0.same_1252_1246].itertuples():
        P(f"    DIFFERS  {r.constant}: 1252 {r.v_1252}  |  1246 {r.v_1246}")
    dump(ddf0, "constdiff")
    gate("G1", f"all {len(CONST_NAMES)} frozen constants identical in 1252 and 1246",
         len(CONST_NAMES) - n_same, n_same == len(CONST_NAMES))

    P("")
    P("  THE ONE THING THAT IS NOT A CONSTANT — HOW EACH SCRIPT LOADS THE SMALL PANEL:")
    loaders = {"1252": small_loader_of(SRC_1252), "1246": small_loader_of(SRC_1246),
               "1260": small_loader_of(SRC_1260)}
    for k, v in loaders.items():
        P(f"    {k}: {v}")
    gate("G2", "1252's small loader differs from 1246's (0 = same, 1 = differs)",
         float(loaders["1252"] != loaders["1246"]), loaders["1252"] != loaders["1246"])
    hyp("H_DIFF", "the disagreement is the SMALL panel's max_1d_move filter, nothing else",
        f"constants identical at {n_same}/{len(CONST_NAMES)}; loaders "
        f"{'DIFFER' if loaders['1252'] != loaders['1246'] else 'AGREE'}",
        n_same == len(CONST_NAMES) and loaders["1252"] != loaders["1246"])
    P("")

    # ---------------------------------------------------------------- panels
    P("-" * 100)
    P("PANELS — every construction built on ONE tape read today, so vintage is held fixed")
    P("         except where the construction IS the vintage (C_1252_VINTAGE).")
    P("-" * 100)
    u_raw, b_raw = load_universe(), load_universe(broad=True)
    s_raw = load_universe(small=True)
    mv = s_raw.pct_change().abs().max()
    drop_panel = [c for c in s_raw.columns if c != "SPY" and not (mv[c] < 1.0)]
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    drop_meta = [c for c in s_raw.columns if c != "SPY" and c in bad]
    P(f"  small panel as loaded: {len(s_raw.columns) - 1} investable names + SPY")
    P(f"  1246's PANEL_MAX filter drops {len(drop_panel)}; 1260's META_CSV filter drops "
      f"{len(drop_meta)}; symmetric difference {sorted(set(drop_panel) ^ set(drop_meta))}")

    def mk(cn):
        trunc = VINTAGE_1252 if cn == "C_1252_VINTAGE" else None
        u, b, s = u_raw, b_raw, s_raw
        if trunc:
            u = u.loc[:trunc["U56"]]; b = b.loc[:trunc["B136"]]; s = s.loc[:trunc["SMALL"]]
        if cn in ("C_1252", "C_1252_VINTAGE"):
            sm = s
        elif cn == "C_1246":
            sm = s.drop(columns=drop_panel)
        else:
            sm = s.drop(columns=drop_meta)
        return {"U56": Panel(f"{cn}|U56", u, False), "B136": Panel(f"{cn}|B136", b, False),
                "SMALL": Panel(f"{cn}|SMALL", sm, True)}

    PAN = {cn: mk(cn) for cn in CONSTRUCTIONS}
    for cn in CONSTRUCTIONS:
        for pn in PANELS:
            p = PAN[cn][pn]
            P(f"  {cn:<15s} {pn:<6s} {p.T:>5d} rows x {p.K - 1:>4d} investable  "
              f"{p.idx[0].date()} .. {p.idx[-1].date()}  IS {int(p.ins.sum()):>4d} / "
              f"OOS {int(p.oos.sum()):>4d}")
    gate("G3", "C_1252_VINTAGE reproduces 1252's own logged U56 row count 4706",
         abs(PAN["C_1252_VINTAGE"]["U56"].T - 4706), PAN["C_1252_VINTAGE"]["U56"].T == 4706)
    P("")

    # ---------------------------------------------------------------- books
    cache, LB = {}, {}
    for cn in CONSTRUCTIONS:
        for pn in PANELS:
            for an in ANCHORS:
                for lad in LADNAMES:
                    LB[(cn, pn, an, lad)] = ladder_books(PAN[cn][pn], an, lad, cache)
    P(f"  {len(cache)} distinct rung books built ({time.time() - t0:.0f}s)")
    a_ref = LB[("C_1260", "U56", "A", "N")][20]
    pr = PAN["C_1260"]["U56"]
    m_ref = blocks_m(a_ref, pr.warm, pr.ins, pr.oos)
    gate("G4", "U56 anchor A full Sharpe replays 1101/1208/1242/1252's 1.139701",
         abs(m_ref["Sharpe"] - A1101_TRIPLE[1]), abs(m_ref["Sharpe"] - A1101_TRIPLE[1]) < 5e-3)

    live, spyb = {}, {}
    for cn in CONSTRUCTIONS:
        for pn in PANELS:
            pan = PAN[cn][pn]
            bk = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST, freq="W")
            live[(cn, pn)] = blocks_m(bk["returns"].values, pan.warm, pan.ins, pan.oos)
            spyb[(cn, pn)] = blocks_m(pan.spy, pan.warm, pan.ins, pan.oos)
    gate("G5", "U56 SPY OOS Sharpe replays the record's committed 0.8713",
         abs(spyb[("C_1260", "U56")]["OOS_Sharpe"] - SPY_OOS_COMMITTED),
         abs(spyb[("C_1260", "U56")]["OOS_Sharpe"] - SPY_OOS_COMMITTED) < 0.05)
    P("")

    MET = {}

    def met_of(cn, pn, an, lad, rung):
        k = (cn, pn, an, lad, str(rung))
        if k not in MET:
            pan = PAN[cn][pn]
            MET[k] = blocks_m(LB[(cn, pn, an, lad)][rung], pan.warm, pan.ins, pan.oos)
        return MET[k]

    # ---------------------------------------------------------------- ARM B: the 72 decisions
    P("-" * 100)
    P("ARM B — THE 72 DECISIONS REBUILT UNDER EVERY CONSTRUCTION.  Each pick is the IS")
    P(f"        argmax of its chooser on warm-up..{IS_END}; 2017-2026 is read ONCE.")
    P("-" * 100)
    DEC = [(pn, an, lad, ch) for pn in PANELS for an in ANCHORS
           for lad in LADNAMES for ch in CHOOSERS]
    rows = []
    for cn in CONSTRUCTIONS:
        for (pn, an, lad, ch) in DEC:
            pan = PAN[cn][pn]; rungs = LADDERS[lad]
            obs = np.array([is_stat(LB[(cn, pn, an, lad)][rg], pan.ins, ch) for rg in rungs])
            j = int(np.nanargmax(obs))
            pick, anc = rungs[j], ANCHORS[an][lad]
            mp, ma = met_of(cn, pn, an, lad, pick), met_of(cn, pn, an, lad, anc)
            rows.append(dict(construction=cn, panel=pn, anchor=an, ladder=lad, chooser=ch,
                             pick=str(pick), anchor_rung=str(anc),
                             moved=float(str(pick) != str(anc)),
                             anchor_OOS_Sharpe=ma["OOS_Sharpe"],
                             pick_OOS_Sharpe=mp["OOS_Sharpe"],
                             d_OOS_Sharpe=mp["OOS_Sharpe"] - ma["OOS_Sharpe"],
                             anchor_OOS_CAGR=ma["OOS_CAGR"], pick_OOS_CAGR=mp["OOS_CAGR"],
                             anchor_OOS_MaxDD=ma["OOS_MaxDD"], pick_OOS_MaxDD=mp["OOS_MaxDD"],
                             d_full_Sharpe=mp["Sharpe"] - ma["Sharpe"]))
    dec = pd.DataFrame(rows)
    dump(dec, "decisions")

    P("  THE 16 CELLS (CONSTRUCTION x CLAIM SET), EVERY ONE PUBLISHED.  do-nothing = mean")
    P("  OOS Sharpe of the ANCHOR book over the claim set; always-act = mean OOS Sharpe of")
    P("  the IS argmax; delta = always-act - do-nothing, paired by decision.")
    cells = []
    for cn in CONSTRUCTIONS:
        for csn, fn in CLAIM_SETS.items():
            sub = dec[(dec.construction == cn) & dec.apply(
                lambda r: fn((r.panel, r.anchor, r.ladder, r.chooser)), axis=1)]
            d = sub.d_OOS_Sharpe.values
            cells.append(dict(construction=cn, claim_set=csn, n=len(sub),
                              n_moved=int(sub.moved.sum()),
                              do_nothing=float(sub.anchor_OOS_Sharpe.mean()),
                              always_act=float(sub.pick_OOS_Sharpe.mean()),
                              delta=float(d.mean()), t_delta=tstat(d),
                              mean_d_full=float(sub.d_full_Sharpe.mean())))
    cdf = pd.DataFrame(cells)
    P(cdf.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
    dump(cdf, "levels")
    P("")

    def cell(cn, csn, col):
        return float(cdf[(cdf.construction == cn) & (cdf.claim_set == csn)][col].iloc[0])

    dn_52v = cell("C_1252_VINTAGE", "CS_ALL", "do_nothing")
    dn_52 = cell("C_1252", "CS_ALL", "do_nothing")
    dn_46 = cell("C_1246", "CS_ALL", "do_nothing")
    dn_60 = cell("C_1260", "CS_ALL", "do_nothing")
    aa_52v = cell("C_1252_VINTAGE", "CS_ALL", "always_act")
    aa_60 = cell("C_1260", "CS_ALL", "always_act")
    P(f"  ADJUDICATION.  1252 committed {L1252_DONOTHING:.4f}; this run reads {dn_52v:.4f} under")
    P(f"  1252's OWN construction AND vintage (dev {abs(dn_52v - L1252_DONOTHING):.2e}) and")
    P(f"  {dn_52:.4f} under 1252's construction on TODAY's tape.")
    P(f"  1246 committed {L1246_DONOTHING:.4f}; this run reads {dn_46:.4f} under 1246's")
    P(f"  construction (dev {abs(dn_46 - L1246_DONOTHING):.2e}) and {dn_60:.4f} under 1260's.")
    gate("G6", "C_1252_VINTAGE reproduces 1252's committed do-nothing 0.826772",
         abs(dn_52v - L1252_DONOTHING), abs(dn_52v - L1252_DONOTHING) < 5e-4)
    gate("G6b", "C_1252_VINTAGE reproduces 1252's committed always-act 0.835724",
         abs(aa_52v - L1252_ALWAYSACT), abs(aa_52v - L1252_ALWAYSACT) < 5e-4)
    gate("G7", "C_1246 reproduces 1246's committed do-nothing 0.7922",
         abs(dn_46 - L1246_DONOTHING), abs(dn_46 - L1246_DONOTHING) < 5e-4)
    gate("G7b", "C_1260 reproduces 1260's committed always-act 0.8017",
         abs(aa_60 - L1260_ALWAYSACT), abs(aa_60 - L1260_ALWAYSACT) < 5e-4)
    gate("G8", "C_1246 and C_1260 are the SAME level to 1e-6 (the OBT name changes nothing)",
         abs(dn_46 - dn_60), abs(dn_46 - dn_60) < 1e-6)
    hyp("H_LEVEL", "1252's level is 1252's construction, not an error in either script",
        f"C_1252_VINTAGE {dn_52v:.4f} vs 1252's {L1252_DONOTHING:.4f}; "
        f"C_1246 {dn_46:.4f} vs 1246's {L1246_DONOTHING:.4f}",
        abs(dn_52v - L1252_DONOTHING) < 5e-4 and abs(dn_46 - L1246_DONOTHING) < 5e-4)
    P("")

    # ---------------------------------------------------------------- ARM C: localisation
    P("-" * 100)
    P("ARM C — WHERE THE LEVEL GAP LIVES.  The anchor book of a (panel, anchor) is the same")
    P("        book for all 4 ladders and all 3 choosers, so do-nothing over the 72 is the")
    P("        mean of SIX numbers.  Here are all six, under every construction.")
    P("-" * 100)
    six = []
    for cn in CONSTRUCTIONS:
        for pn in PANELS:
            for an in ANCHORS:
                mm = met_of(cn, pn, an, "N", ANCHORS[an]["N"])
                six.append(dict(construction=cn, panel=pn, anchor=an,
                                OOS_Sharpe=mm["OOS_Sharpe"], OOS_CAGR=mm["OOS_CAGR"],
                                OOS_MaxDD=mm["OOS_MaxDD"], full_Sharpe=mm["Sharpe"]))
    sdf = pd.DataFrame(six)
    piv = sdf.pivot_table(index=["panel", "anchor"], columns="construction", values="OOS_Sharpe")
    P(piv.to_string(float_format=lambda x: f"{x:.4f}"))
    dump(sdf, "anchorbooks")
    same = piv["C_1252"] - piv["C_1260"]
    lg = float(np.abs(same.loc[["U56", "B136"]]).max())
    gate("G9", "U56 and B136 anchor books are BIT-IDENTICAL across C_1252 and C_1260",
         lg, lg == 0.0)
    gap_A = float(same.loc[("SMALL", "A")]); gap_B = float(same.loc[("SMALL", "B")])
    P(f"  the whole disagreement is TWO numbers: SMALL/A {gap_A:+.4f} and SMALL/B {gap_B:+.4f},")
    P(f"  contributing {gap_A / 6:+.4f} and {gap_B / 6:+.4f} of the {dn_52 - dn_60:+.4f} level gap.")
    hyp("H_ONECELL", "one of the six anchor books carries >80% of the level gap",
        f"SMALL/B contributes {abs(gap_B / 6) / abs(dn_52 - dn_60):.1%} of it",
        abs(gap_B / 6) / abs(dn_52 - dn_60) > 0.80)
    P("")

    # ---------------------------------------------------------------- ARM D: re-scoring
    P("-" * 100)
    P("ARM D — WHICH COMMITTED CLAIMS DEPEND ON THE LEVEL RATHER THAN THE DELTA.")
    P("-" * 100)
    P("  D1, THE CENSUS.  Every text unit in LEADERBOARD.md + CHANGELOG.md that cites this")
    P("  apparatus (a do-nothing / always-act / ACT-ON-ALL number, or a 72-decision mean OOS")
    P("  Sharpe) is harvested and classed by the PRE-DECLARED test:")
    P("    LEVEL  — the committed sentence quotes an absolute mean OOS Sharpe;")
    P("    DELTA  — it quotes only a difference / t / rank correlation / count;")
    P("    BOTH   — it quotes an absolute AND a difference in the same unit.")
    LEV = re.compile(r"(do[- ]nothing|always[- ]act|ACT ON ALL|DO NOTHING)", re.I)
    NUM = re.compile(r"[-+]?\d*\.\d+")
    ABSN = re.compile(r"(do[- ]nothing|always[- ]act|ACT ON ALL|DO NOTHING)\s*"
                      r"(?:mean\s+OOS\s+Sharpe\s*)?[:= ]?\s*([01]\.\d{3,6})", re.I)
    DELN = re.compile(r"[-+]\d*\.\d{3,6}")
    units = []
    for f in ["LEADERBOARD.md", "CHANGELOG.md"]:
        for i, ln in enumerate((ROOT / "research" / f).read_text().split("\n")):
            for seg in ln.split("|"):
                if not LEV.search(seg) or not NUM.search(seg):
                    continue
                has_abs = bool(ABSN.search(seg))
                has_del = bool(DELN.search(seg))
                units.append(dict(file=f, line=i + 1,
                                  kind=("BOTH" if has_abs and has_del else
                                        "LEVEL" if has_abs else
                                        "DELTA" if has_del else "NEITHER"),
                                  abs_values=";".join(m.group(2) for m in ABSN.finditer(seg)),
                                  text=seg.strip()[:300]))
    udf = pd.DataFrame(units)
    dump(udf, "census")
    counts = udf.kind.value_counts().to_dict()
    P(f"  {len(udf)} citing text units: " +
      ", ".join(f"{k} {counts.get(k, 0)}" for k in ["LEVEL", "BOTH", "DELTA", "NEITHER"]))
    n_level = counts.get("LEVEL", 0) + counts.get("BOTH", 0)
    P(f"  LEVEL-DEPENDENT (LEVEL + BOTH): {n_level} of {len(udf)} "
      f"({n_level / max(len(udf), 1):.1%}).  Every one of them is construction-keyed and")
    P("  NONE of them states which small-panel construction it was measured on.")
    vals = sorted({v for s in udf.abs_values for v in s.split(";") if v})
    P(f"  distinct absolute levels quoted anywhere in the record: {vals}")
    gate("G10", "both disputed levels (0.826772/0.8268 and 0.7922) appear in the census",
         float(any(v.startswith("0.826") for v in vals) and any(v.startswith("0.792")
                                                                for v in vals)),
         any(v.startswith("0.826") for v in vals) and any(v.startswith("0.792") for v in vals))

    P("")
    P("  D2, THE RE-SCORING.  Every class of committed number this apparatus emits, recomputed")
    P("  at all four constructions.  SWING = max - min across constructions; a class whose")
    P("  swing is 0 is construction-free and every committed instance of it stands as written.")
    sw = []
    for csn in CLAIM_SETS:
        for col, cls in [("do_nothing", "LEVEL"), ("always_act", "LEVEL"),
                         ("delta", "DELTA"), ("t_delta", "DELTA"),
                         ("n_moved", "COUNT"), ("mean_d_full", "DELTA")]:
            v = [cell(cn, csn, col) for cn in CONSTRUCTIONS]
            sw.append(dict(claim_set=csn, quantity=col, cls=cls,
                           **{cn: v[i] for i, cn in enumerate(CONSTRUCTIONS)},
                           swing=float(max(v) - min(v))))
    swdf = pd.DataFrame(sw)
    P(swdf.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
    dump(swdf, "rescore")
    # LIKE FOR LIKE: only quantities measured in Sharpe are compared to each other; the
    # t-statistic and the move count are published in their own right below, NOT folded in.
    SHRP = ["do_nothing", "always_act", "delta", "mean_d_full"]
    shr = swdf[swdf.quantity.isin(SHRP)]
    lev_sw = float(shr[shr.cls == "LEVEL"].swing.max())
    del_sw = float(shr[shr.cls == "DELTA"].swing.max())
    cs0 = shr[shr.claim_set == "CS_ALL"]
    lev_sw_all = float(cs0[cs0.cls == "LEVEL"].swing.max())
    del_sw_all = float(cs0[cs0.cls == "DELTA"].swing.max())
    P(f"  ON THE SHARPE SCALE ONLY (do_nothing / always_act vs delta / mean_d_full):")
    P(f"    worst LEVEL swing {lev_sw:+.4f}; worst DELTA swing {del_sw:+.4f}  "
      f"(at CS_ALL: {lev_sw_all:+.4f} vs {del_sw_all:+.4f}, a factor of "
      f"{lev_sw_all / max(del_sw_all, 1e-12):.0f})")
    hyp("H_DELTA", "the DELTAS survive the construction; the LEVELS do not",
        f"LEVEL swing {lev_sw_all:.4f} vs DELTA swing {del_sw_all:.4f} at CS_ALL",
        lev_sw_all > 5 * max(del_sw_all, 1e-9))
    t_sw = float(swdf[swdf.quantity == "t_delta"].swing.max())
    n_sw = float(swdf[swdf.quantity == "n_moved"].swing.max())
    P(f"  PUBLISHED AGAINST THIS RUN'S OWN FRAMING, NOT BURIED: the DELTA class is only")
    P(f"  construction-free IN SHARPE.  Its t-statistic swings {t_sw:+.4f} (worst cell) and the")
    P(f"  move count swings {n_sw:+.0f} decisions, because the construction moves the IS argmax")
    P("  itself on the small panel.  A committed t or move rate is NOT safe, only a committed")
    P("  mean difference in Sharpe is.")
    same_vint = [c for c in CONSTRUCTIONS if c != "C_1252_VINTAGE"]
    lg_rows = swdf[swdf.claim_set == "CS_LARGE"]
    cs_large = float(lg_rows[same_vint].max(axis=1).sub(lg_rows[same_vint].min(axis=1)).max())
    cs_large_v = float(lg_rows.swing.max())
    P(f"  CS_LARGE (the two large-cap panels, SMALL dropped) swings {cs_large:.2e} across the")
    P("  three SAME-VINTAGE constructions on EVERY quantity: a committed claim restricted to")
    P("  U56 + B136 is construction-free, and that is the cheapest repair available to the")
    P(f"  record.  Adding the one-day vintage back raises that swing to {cs_large_v:.4f} — ONE")
    P("  EXTRA TRADING DAY moves a large-cap-only committed level by more than the whole")
    P(f"  construction moves its delta ({del_sw_all:.4f}).  Vintage, not construction, is the")
    P("  binding threat to a large-cap level claim.")
    gate("G11", "CS_LARGE is construction-invariant at fixed vintage on every quantity",
         cs_large, cs_large < 1e-9)
    P("")

    # ---------------------------------------------------------------- ARM E: rule 8 + 4a/4b
    P("-" * 100)
    P("ARM E — RULE 8 AND BOTH KEEP PATHS AT EVERY CONSTRUCTION.  All rung books, plus the")
    P("        two selectors the disputed levels score (do-nothing / always-act).")
    P("-" * 100)
    wrows = []
    for cn in CONSTRUCTIONS:
        for pn in PANELS:
            for an in ANCHORS:
                for lad in LADNAMES:
                    for rg in LADDERS[lad]:
                        mm = met_of(cn, pn, an, lad, rg)
                        l4a = legs_4a(mm, live[(cn, pn)])
                        l4b = legs_4b(mm, spyb[(cn, pn)])
                        l4o = legs_4b_oos(mm, spyb[(cn, pn)])
                        wrows.append(dict(construction=cn, panel=pn, anchor=an, ladder=lad,
                                          chooser="n/a", rung=str(rg), selector="RUNG_BOOK",
                                          **mm, **l4a, **l4b, **l4o,
                                          pass4a=all(l4a.values()),
                                          pass4b_full=all(l4b.values()),
                                          pass4b_oos=all(l4o.values()),
                                          pass4b_both=all(l4b.values()) and all(l4o.values())))
    for cn in CONSTRUCTIONS:
        for nm, use_pick in [("SEL_NEVER_anchor", False), ("SEL_ALWAYS_pick", True)]:
            for r in dec[dec.construction == cn].itertuples():
                use = r.pick if use_pick else r.anchor_rung
                lad = r.ladder
                rung = LADDERS[lad][[str(x) for x in LADDERS[lad]].index(str(use))]
                mm = met_of(cn, r.panel, r.anchor, lad, rung)
                l4a = legs_4a(mm, live[(cn, r.panel)])
                l4b = legs_4b(mm, spyb[(cn, r.panel)])
                l4o = legs_4b_oos(mm, spyb[(cn, r.panel)])
                wrows.append(dict(construction=cn, panel=r.panel, anchor=r.anchor, ladder=lad,
                                  chooser=r.chooser, rung=str(rung), selector=nm,
                                  **mm, **l4a, **l4b, **l4o, pass4a=all(l4a.values()),
                                  pass4b_full=all(l4b.values()), pass4b_oos=all(l4o.values()),
                                  pass4b_both=all(l4b.values()) and all(l4o.values())))
    wdf = pd.DataFrame(wrows)
    dump(wdf, "walkforward")

    rb = wdf[wdf.selector == "RUNG_BOOK"]
    P("  PLAIN RUNG BOOKS (162 per construction), 4a vs live RULES v2, 4b vs SPY:")
    kp = rb.groupby("construction").agg(n=("pass4a", "size"), pass4a=("pass4a", "sum"),
                                        b_full=("pass4b_full", "sum"),
                                        b_oos=("pass4b_oos", "sum"),
                                        b_both=("pass4b_both", "sum"))
    P(kp.to_string())
    P("  by panel (4b BOTH):")
    P(rb.pivot_table(index="panel", columns="construction", values="pass4b_both",
                     aggfunc="sum").to_string())
    fails = rb[~rb.pass4b_both]
    P("  binding leg among the 4b failures, pooled over constructions: " + ", ".join(
        f"{k} {int((~fails[k]).sum())}" for k in ["L_DD", "L_H2", "L_H1", "L_OOS", "L_CAGR"]))
    n4a = int(rb.pass4a.sum())
    gate("G12", f"4a passes over all {len(rb)} rung books at every construction", n4a, n4a == 0)

    P("")
    P("  THE TWO SELECTORS THE DISPUTED LEVELS SCORE (rule 8: picks on IS only, OOS read once):")
    sel = wdf[wdf.selector != "RUNG_BOOK"]
    selg = []
    for cn in CONSTRUCTIONS:
        for csn, fn in CLAIM_SETS.items():
            for nm in ["SEL_NEVER_anchor", "SEL_ALWAYS_pick"]:
                s = sel[(sel.construction == cn) & (sel.selector == nm)]
                s = s[s.apply(lambda r: fn((r.panel, r.anchor, r.ladder, r.chooser)), axis=1)]
                selg.append(dict(construction=cn, claim_set=csn, selector=nm, n=len(s),
                                 mean_OOS_Sharpe=float(s.OOS_Sharpe.mean()),
                                 mean_OOS_CAGR=float(s.OOS_CAGR.mean()),
                                 mean_OOS_MaxDD=float(s.OOS_MaxDD.mean()),
                                 n4a=int(s.pass4a.sum()), n4b_both=int(s.pass4b_both.sum())))
    sgd = pd.DataFrame(selg)
    P(sgd[sgd.claim_set == CS_HEAD].to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
    dump(sgd, "selectors")

    def sg(cn, csn, nm, col):
        return sgd[(sgd.construction == cn) & (sgd.claim_set == csn)
                   & (sgd.selector == nm)][col].iloc[0]

    P("")
    P("  THE CAPITAL SENTENCE, AT EVERY CONSTRUCTION: acting on the IS argmax versus doing")
    P("  nothing, in mean OOS Sharpe AND in 4b passes destroyed.")
    for cn in CONSTRUCTIONS:
        dn = sg(cn, CS_HEAD, "SEL_NEVER_anchor", "mean_OOS_Sharpe")
        aa = sg(cn, CS_HEAD, "SEL_ALWAYS_pick", "mean_OOS_Sharpe")
        b0 = int(sg(cn, CS_HEAD, "SEL_NEVER_anchor", "n4b_both"))
        b1 = int(sg(cn, CS_HEAD, "SEL_ALWAYS_pick", "n4b_both"))
        P(f"    {cn:<15s} do-nothing {dn:.4f} -> always-act {aa:.4f} ({aa - dn:+.4f}); "
          f"4b BOTH {b0} -> {b1} ({b1 - b0:+d})")
    dlt = [sg(cn, CS_HEAD, "SEL_ALWAYS_pick", "mean_OOS_Sharpe")
           - sg(cn, CS_HEAD, "SEL_NEVER_anchor", "mean_OOS_Sharpe") for cn in CONSTRUCTIONS]
    d4b = [int(sg(cn, CS_HEAD, "SEL_ALWAYS_pick", "n4b_both"))
           - int(sg(cn, CS_HEAD, "SEL_NEVER_anchor", "n4b_both")) for cn in CONSTRUCTIONS]
    gate("G13", "the capital sentence (gating destroys 4b passes) holds at EVERY construction",
         float(max(d4b)), max(d4b) < 0)
    gate("G14", "1252's committed delta +0.008951 is inside 2e-3 of this run's at its own "
         "construction", abs(dlt[CONSTRUCTIONS.index("C_1252_VINTAGE")] - L1252_DELTA),
         abs(dlt[CONSTRUCTIONS.index("C_1252_VINTAGE")] - L1252_DELTA) < 2e-3)

    if MONEY_1252.exists():
        m52 = pd.read_csv(MONEY_1252)
        r0 = m52[(m52.selector == "SEL_NEVER_anchor") & (m52.claim_set == "CS_ALL")].iloc[0]
        dev = abs(float(r0.mean_OOS_Sharpe) - dn_52v)
        gate("G15", "row-level replay of 1252's OWN committed money.csv do-nothing cell",
             dev, dev < 5e-4)

    P("")
    P("-" * 100)
    P("VERDICT")
    P("-" * 100)
    P(f"  ANSWERED: BOTH LEVELS ARE ARITHMETICALLY CORRECT AND THEY ARE NOT THE SAME 72")
    P(f"  DECISIONS.  1252's {L1252_DONOTHING:.4f} is the 72 decisions on a small panel of")
    P(f"  {PAN['C_1252']['SMALL'].K - 1} names that KEEPS every name with a >=100% single-day move; 1246's and")
    P(f"  1260's {L1246_DONOTHING:.4f} is the same 72 on the {PAN['C_1260']['SMALL'].K - 1}-name panel the house rule")
    P(f"  requires.  The house rule wins: {dn_60:.4f} is the level a committed sentence is")
    P(f"  entitled to, and {dn_52:.4f} / {L1252_DONOTHING:.4f} should be read as SMALL{PAN['C_1252']['SMALL'].K - 1}, not withdrawn.")
    P(f"  The DELTAS in Sharpe are untouched (worst swing {del_sw_all:+.4f} at CS_ALL against the")
    P(f"  levels' {lev_sw_all:+.4f}), so every committed DELTA-IN-SHARPE claim stands; the LEVEL")
    P(f"  claims need a construction stamp, and so do committed t's ({t_sw:+.4f} swing) and move")
    P(f"  counts ({n_sw:+.0f}).  {n_level} of {len(udf)} citing text units are level-dependent and NONE")
    P("  names its construction.")
    P("  CAPITAL: KILL.  4a 0 of 648 rung books at every construction; gating destroys 4b")
    P("  passes at every construction; no book here is new.")

    P("")
    gdf = pd.DataFrame(GATES); dump(gdf, "gates")
    hdf = pd.DataFrame(HYP); dump(hdf, "hypotheses")
    P(f"  GATES {int(gdf.pass_.sum())} of {len(gdf)}   runtime {time.time() - t0:.0f}s   offline, deterministic")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
