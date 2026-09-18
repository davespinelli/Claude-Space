#!/usr/bin/env python3
"""IDEA 1115 (lane B, 2026-09-18) — does the PER-CELL CALIBRATION BAR change any committed
DECISIVENESS claim?

THE QUESTION.  1110's D2 found that the AGGREGATE error-share test the record declares is WEAKER
than a per-cell one: a family (ANNOTATED) passed the aggregate bar at q=0.80 while 24 of its 32
cells failed their own.  Most of the record's decisiveness language ("the ladder is decisively
ordered", "4-7 of 8 steps are decisively down") is written in the AGGREGATE voice but READ as if it
were per cell.  This run prices the gap directly and then asks whether it is worth anything to an
allocator.

WHY THIS IS MEASURED ON FRESH BOOKS AND NOT HARVESTED FROM THE TEXT.  The committed decisiveness
rows in LEADERBOARD.md do not carry their return series (the same limit 1257's run documented), so
they cannot be re-bootstrapped from the record.  Re-scoring them per cell is therefore impossible
from text alone, and this run does NOT claim to re-adjudicate any committed row.  What it does is
rebuild the record's OWN decisiveness objects — the four CORE ladders on three panels at both 1101
anchors, 24 families — and measure, on those, how often the aggregate and the per-cell reading of
the SAME bar disagree.  That is the quantity a schema clause would be written against.

TWO DIALS (rule 4), 24 cells, EVERY ONE PUBLISHED:
  dial 1 = CLAIM SET  {CS_STEPS, CS_ENDS, CS_VSANCHOR, CS_VSBEST}
           which cells the bar is applied to inside a family:
             CS_STEPS    every adjacent rung pair (the record's "step" language)
             CS_ENDS     the end-to-end pair only (top rung vs bottom rung)
             CS_VSANCHOR every rung against the 1101 anchor rung
             CS_VSBEST   every rung against the family's IS-best-Sharpe rung
  dial 2 = BAR q  {0.50, 0.60, 0.70, 0.80, 0.90, 0.95}
           the sign-agreement share at/above which a cell (or a pooled family) is DECISIVE.
           0.90 is the record's incumbent bar and is flagged as such, not treated as special.

WHAT IS NOT A DIAL.  PANEL {U56, B136, SMALL} (rule 9 wants all three), ANCHOR {A, B} (1101's pair,
inherited whole), LADDER {N, H, GROSS, CADENCE} (the record's four CORE ladders), BLOCK LENGTH
(frozen at the record's L=63; L=21/252 reported as a CONTROL, never selected on), DRAWS (1000),
COST (10 bps), LAG (1).

THE TWO READINGS OF ONE BAR.
  AGGREGATE (what the record declares): pool the claim set's cells and ask whether the POOLED
      sign-agreement share over (cell, draw) clears q.  One number per family.
  PER CELL (what the record's language implies): EVERY cell in the claim set must clear q on its
      own.  A family is decisive only if its weakest cell is.
  A FLIP is a family where the two readings disagree at the same (claim set, q).

CAPITAL ARM (rule 8, real money question).  A decisiveness bar is only worth anything if it changes
what an allocator BUYS.  For each family the chooser proposes moving off the anchor rung to the
IS-best-Sharpe rung, and the gate LICENSES that move only if the family is decisive under the
reading being tested.  Everything — the ladder's IS Sharpes, the bootstrap, the licensing — is
computed on warm-up..2016-12-31 ONLY; 2017-2026 is read ONCE at the end.  Controls: DO-NOTHING
(always the anchor) and ALWAYS-ACT (always the IS-best rung).  Both KEEP paths (4a vs RULES v2,
4b vs SPY) are evaluated for every chosen book, full sample and OOS.

EXECUTION (binding, rule 2): weights decided at the rebalance close t, applied at t+1; 10 bps per
unit turnover; no shorting, no leverage.

Offline, deterministic, standalone.  Writes .cells.csv .families.csv .grid.csv .capital.csv
.books.csv .control.csv .gates.csv .console.txt
"""
import sys
import time
import zlib
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE = "2026-09-18"
SLUG = "does-the-PER-CELL-CALIBRATION-BAR-change-any-committed-DECISIVENESS-claim"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_B"

# ----- 1101's construction, inherited whole -----------------------------------------------------
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

CLAIMSETS = ["CS_STEPS", "CS_ENDS", "CS_VSANCHOR", "CS_VSBEST"]        # dial 1
QUANTS = [0.50, 0.60, 0.70, 0.80, 0.90, 0.95]                          # dial 2
INCUMBENT_Q = 0.90                                                     # the record's bar, flagged
L_FROZEN = 63
L_CONTROL = [21, 252]
BDRAWS = 1000
SEED_BASE = 11151115

# ----- committed numbers QUOTED and GATED, never re-derived ------------------------------------
C1110_D2 = (24, 32, 0.80)          # 24 of 32 cells fail their own bar while the family passes at q=0.80
C1101_TRIPLE = (0.155787, 1.139701, -0.191276)   # U56 W/H126/N=20/g0.75 full-sample CAGR/Sharpe/MaxDD
LIVE_MAXDD_COMMITTED = -0.1205                   # RULES v2 OOS MaxDD
SPY_OOS_COMMITTED = (0.1528, 0.8747, -0.3372)    # SPY OOS CAGR/Sharpe/MaxDD as last committed
RULESV2_OOS_COMMITTED = (0.0947, 1.2781, -0.1205)

LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def dump(df, suffix):
    p = Path(f"{OUT}.{suffix}.csv")
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


def seed_of(*parts):
    return SEED_BASE + int(zlib.crc32("|".join(str(p) for p in parts).encode())) % 10_000_000


GATES: list[dict] = []


def gate(name, what, value, ok):
    GATES.append(dict(gate=name, check=what, value=float(value), pass_=bool(ok)))
    P(f"  [{'PASS' if ok else 'FAIL'}] {name:<5s} {what}  ->  {value:.4e}")
    return bool(ok)


# ================================================================================================
# 1101's runner and metrics, verbatim
# ================================================================================================
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
    warm = np.zeros(len(idx), dtype=bool)
    warm[WARMUP:] = True
    oos = np.asarray(idx > pd.Timestamp(IS_END)) & warm
    ins = warm & ~oos
    return warm, ins, oos


def load_small():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    return px[keep].dropna(how="all").ffill(), len(bad), len(meta)


class Panel:
    def __init__(self, name, px):
        self.name, self.px = name, px
        self.idx, self.K, self.T = px.index, len(px.columns), len(px.index)
        self.rets = px.pct_change().fillna(0.0).values
        self.priced = px.notna().values
        self.warm, self.ins, self.oos = windows_of(px.index)
        sc, elig = mech(px)
        spy_i = list(px.columns).index("SPY")
        if name == "SMALL":
            elig = elig.copy()
            elig[:, spy_i] = False
        self.sc, self.elig = sc, elig
        self.reb, self.mkl = {}, {}
        for f in LAD_C:
            mk = rebalance_mask(px.index, f).values
            self.reb[f] = np.flatnonzero(mk)
            m = np.roll(mk, LAG)
            m[:LAG] = False
            self.mkl[f] = m
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        self.cache: dict = {}

    def book(self, N, H, gross, freq):
        key = (N, H, gross, freq)
        if key in self.cache:
            return self.cache[key]
        W = build(-self.sc, self.elig, self.priced, self.reb[freq], N, H, self.T, self.K, gross)
        Wl = np.zeros_like(W)
        Wl[LAG:] = W[:-LAG]
        r, turn = nrun(self.rets, Wl, self.mkl[freq])
        out = r - turn * COST / 1e4
        self.cache[key] = out
        return out


def rungs_of(anchor, lad):
    a = ANCHORS[anchor]
    kmap = {"N": "N", "H": "H", "GROSS": "gross", "CADENCE": "freq"}
    out = []
    for rung in LADDERS[lad]:
        kw = dict(N=a["N"], H=a["H"], gross=a["GROSS"], freq=a["CADENCE"])
        kw[kmap[lad]] = rung
        out.append((rung, kw))
    return out


def blocks_idx(T, L, rng, B=BDRAWS):
    """Circular block bootstrap index matrix (B, T), block length L."""
    nb = int(np.ceil(T / L))
    starts = rng.integers(0, T, size=(B, nb))
    off = np.arange(L)
    idx = (starts[:, :, None] + off[None, None, :]).reshape(B, nb * L)[:, :T]
    return idx % T


def sharpe_draws(r, idx):
    """Per-draw annualised Sharpe of r under the paired draw index matrix idx."""
    x = r[idx]
    m = x.mean(axis=1) * 252.0
    s = x.std(axis=1, ddof=1) * np.sqrt(252.0)
    return np.where(s > 0, m / np.maximum(s, 1e-300), np.nan)


def agree_share(sd_a, sd_b, obs):
    """Share of draws whose (a - b) Sharpe gap agrees in SIGN with the observed gap."""
    d = sd_a - sd_b
    if obs == 0 or not np.isfinite(obs):
        return 0.5, float(np.nanstd(d, ddof=1))
    ok = np.isfinite(d)
    if not ok.any():
        return np.nan, np.nan
    return float((np.sign(d[ok]) == np.sign(obs)).mean()), float(np.nanstd(d, ddof=1))


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


def block_metrics(r, warm, ins, oos):
    rr = r[warm]
    c, s, d = fmet(rr)
    h = len(rr) // 2
    oc, os_, od = fmet(r[oos])
    ic, is_, idd = fmet(r[ins])
    return dict(CAGR=c, Sharpe=s, MaxDD=d, H1=fsharpe(rr[:h]), H2=fsharpe(rr[h:]),
                IS_CAGR=ic, IS_Sharpe=is_, IS_MaxDD=idd,
                OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=od)


# ================================================================================================
T0 = time.time()
P("=" * 100)
P(f"IDEA 1115 (lane B, {DATE}) — does the PER-CELL CALIBRATION BAR change any committed")
P("DECISIVENESS claim?   Dials: CLAIM SET x BAR q (24 cells, all published).")
P("=" * 100)
P(f"Committed and quoted, not re-derived: 1110 D2 = {C1110_D2[0]} of {C1110_D2[1]} cells fail their")
P(f"  own bar at q={C1110_D2[2]} while the family passes;  1101 U56 anchor triple = {C1101_TRIPLE};")
P(f"  RULES v2 OOS = {RULESV2_OOS_COMMITTED};  SPY OOS = {SPY_OOS_COMMITTED}.")
P("NOT CLAIMED: that any specific committed decisiveness ROW flips.  Committed rows carry no return")
P("  series in this repo, so they cannot be re-bootstrapped; this run measures the aggregate-vs-")
P("  per-cell gap on the record's own 24 ladder families, rebuilt here.")
P("")

# ---- panels -----------------------------------------------------------------------------------
P("LOADING PANELS")
pans = {}
pans["U56"] = Panel("U56", load_universe())
pans["B136"] = Panel("B136", load_universe(broad=True))
spx, nbad, nmeta = load_small()
pans["SMALL"] = Panel("SMALL", spx)
for k, p in pans.items():
    P(f"  {k:<6s} {p.K:>4d} cols  {p.T:>5d} days  {p.idx[0].date()}..{p.idx[-1].date()}  "
      f"IS {int(p.ins.sum())}d  OOS {int(p.oos.sum())}d")
P(f"  SMALL survivorship note (rule 9): current sub-$2B screen, {nmeta - nbad} of {nmeta} names kept "
  f"on max_1d_move < 1.0 (label SMALL663 is stale — idea 1074's object).")
P("")

# ---- baselines ---------------------------------------------------------------------------------
P("BASELINES (RULES v2 live book and SPY, per panel, 10 bps, weekly)")
BASE, SPYM = {}, {}
for k, p in pans.items():
    bt = backtest(p.px, rules_v2_weights(p.px), cost_bps=COST, freq="W")
    BASE[k] = block_metrics(bt["returns"].values, p.warm, p.ins, p.oos)
    SPYM[k] = block_metrics(p.spy, p.warm, p.ins, p.oos)
    b, s = BASE[k], SPYM[k]
    P(f"  {k:<6s} RULES v2  full {b['CAGR']:>7.2%} / {b['Sharpe']:.4f} / {b['MaxDD']:>7.2%}   "
      f"OOS {b['OOS_CAGR']:>7.2%} / {b['OOS_Sharpe']:.4f} / {b['OOS_MaxDD']:>7.2%}")
    P(f"  {'':<6s} SPY       full {s['CAGR']:>7.2%} / {s['Sharpe']:.4f} / {s['MaxDD']:>7.2%}   "
      f"OOS {s['OOS_CAGR']:>7.2%} / {s['OOS_Sharpe']:.4f} / {s['OOS_MaxDD']:>7.2%}")
P("")

# ---- G1: fast runner vs engine.backtest --------------------------------------------------------
P("GATES")
p = pans["U56"]
a = ANCHORS["A"]
Wc = build(-p.sc, p.elig, p.priced, p.reb["W"], a["N"], a["H"], p.T, p.K, a["GROSS"])
eng = backtest(p.px, pd.DataFrame(Wc, index=p.idx, columns=p.px.columns), cost_bps=COST, freq="W")
fast = p.book(a["N"], a["H"], a["GROSS"], "W")
er = eng["returns"].values
fin = np.isfinite(er)
# 1198's finding, honoured explicitly rather than hidden behind a skipna .max(): engine.backtest
# leaves `returns` NaN wherever weights.shift(1) is unfilled (row 0 and the first rebalance-
# application row).  Both sit inside the 260-day warm-up and are excluded from every metric here.
g1 = float(np.abs(er[fin] - fast[fin]).max())
gate("G1a", "max |fast runner - engine.backtest| over FINITE engine rows (U56 anchor A)", g1, g1 < 1e-12)
nnan = int((~fin).sum())
gate("G1b", "non-finite engine.backtest rows (1198's NaN pair), all inside warm-up",
     nnan, nnan == 2 and bool(np.flatnonzero(~fin).max() < WARMUP))

# ================================================================================================
# ARM 0 — the committed text: do the record's DECISIVENESS claims say WHICH READING they are?
# This counts STRINGS.  It does not re-adjudicate any verdict (the rows carry no return series).
# ================================================================================================
P("")
P("ARM 0 — CENSUS OF COMMITTED DECISIVENESS STRINGS (LEADERBOARD.md + CHANGELOG.md).")
P("  Counts strings only; re-adjudicates nothing.")
import re  # noqa: E402

PERCELL_RX = re.compile(r"per[- ]cell|each cell|every cell|its own bar|their own bar|own cell", re.I)
AGG_RX = re.compile(r"aggregate|pooled|pooling|family[- ]level|overall share|error[- ]share", re.I)
COUNT_RX = re.compile(r"\b\d+\s+of\s+\d+\b")
BAR_RX = re.compile(r"0\.(?:50|55|60|65|70|75|80|85|90|95)\b")
DEC_RX = re.compile(r"decisiv", re.I)

cens_rows = []
for fn in ("LEADERBOARD.md", "CHANGELOG.md"):
    txt = (ROOT / "research" / fn).read_text(errors="replace")
    units = [u for u in re.split(r"\n(?=\|)|\n\n+|\n(?=- )", txt) if DEC_RX.search(u)]
    for u in units:
        cens_rows.append(dict(file=fn, n_chars=len(u),
                              says_percell=bool(PERCELL_RX.search(u)),
                              says_aggregate=bool(AGG_RX.search(u)),
                              states_k_of_m=bool(COUNT_RX.search(u)),
                              states_a_bar=bool(BAR_RX.search(u))))
dfcen = pd.DataFrame(cens_rows)
dump(dfcen, "census")
for fn, g in dfcen.groupby("file"):
    P(f"  {fn:<16s} {len(g):>5d} decisiveness-mentioning units:  names a READING "
      f"{int((g.says_percell | g.says_aggregate).sum()):>4d} ({(g.says_percell | g.says_aggregate).mean():.4f})"
      f"   per-cell {int(g.says_percell.sum()):>3d} ({g.says_percell.mean():.4f})"
      f"   aggregate {int(g.says_aggregate.sum()):>3d} ({g.says_aggregate.mean():.4f})")
    P(f"  {'':<16s} {'':>5s} states a k-of-m cell count {int(g.states_k_of_m.sum()):>4d} "
      f"({g.states_k_of_m.mean():.4f});  states a bar {int(g.states_a_bar.sum()):>4d} "
      f"({g.states_a_bar.mean():.4f})")
NAMES_READING = float((dfcen.says_percell | dfcen.says_aggregate).mean())
P(f"  POOLED over both files ({len(dfcen)} units): a reading is NAMED in {NAMES_READING:.4f}; "
  f"NEITHER named in {1 - NAMES_READING:.4f}.")
P("  This is the schema gap the rest of the run prices: the record's decisiveness language mostly")
P("  does not say whether the bar was cleared in AGGREGATE or CELL BY CELL.")

# ---- build every ladder book -------------------------------------------------------------------
P("")
P("BUILDING LADDER BOOKS (3 panels x 2 anchors x 4 ladders)")
BOOKS: dict = {}          # (panel, anchor, ladder) -> list[(rung, returns)]
rows_books = []
for pk, pan in pans.items():
    for anc in ANCHORS:
        for lad in LADNAMES:
            seq = []
            for rung, kw in rungs_of(anc, lad):
                r = pan.book(**kw)
                seq.append((rung, r))
                m = block_metrics(r, pan.warm, pan.ins, pan.oos)
                rows_books.append(dict(panel=pk, anchor=anc, ladder=lad, rung=str(rung),
                                       **{k: v for k, v in m.items()}))
            BOOKS[(pk, anc, lad)] = seq
    P(f"  {pk:<6s} done  ({len(pan.cache)} distinct books cached)  t={time.time() - T0:.0f}s")
dfb = pd.DataFrame(rows_books)
dump(dfb, "books")
P("")

# G2/G3 on the anchor book: the 1101 triple, and no degenerate ladder
u = dfb[(dfb.panel == "U56") & (dfb.anchor == "A") & (dfb.ladder == "N") & (dfb.rung == "20")].iloc[0]
d1101 = max(abs(u.CAGR - C1101_TRIPLE[0]), abs(u.Sharpe - C1101_TRIPLE[1]), abs(u.MaxDD - C1101_TRIPLE[2]))
gate("G2", "U56 anchor-A book vs 1101's committed triple (max abs dev)", d1101, d1101 < 5e-3)

# ================================================================================================
# ARM 1 — the CELL level: every pair in every claim set, bootstrapped, both windows
# ================================================================================================
P("ARM 1 — CELL-LEVEL SIGN AGREEMENT (circular block bootstrap, L=63, 1000 draws)")
P("  A CELL is a pair of rungs inside one family.  Its score is the share of draws whose Sharpe")
P("  gap agrees in SIGN with the observed gap.  Computed on the FULL warm-up sample (for the")
P("  census arm) and on the IS window ONLY (for the rule-8 capital arm).")

cell_rows = []
# per (panel, anchor, ladder, window) -> {claimset: [(i,j,agree)]}, plus per-draw sharpes
AGREE: dict = {}
DRAWSD: dict = {}
nzero = 0
for (pk, anc, lad), seq in BOOKS.items():
    pan = pans[pk]
    rungs = [str(r) for r, _ in seq]
    R = len(seq)
    for win, mask in (("FULL", pan.warm), ("IS", pan.ins)):
        rng = np.random.default_rng(seed_of(pk, anc, lad, win, L_FROZEN))
        rs = [r[mask] for _, r in seq]
        Tw = len(rs[0])
        idx = blocks_idx(Tw, L_FROZEN, rng)
        sd = np.vstack([sharpe_draws(x, idx) for x in rs])          # (R, B)
        obs = np.array([fsharpe(x) for x in rs])
        DRAWSD[(pk, anc, lad, win)] = (sd, obs, rungs)
        best = int(np.nanargmax(obs))
        anchor_i = rungs.index(str(ANCHORS[anc][lad]))
        sets = {
            "CS_STEPS": [(i, i + 1) for i in range(R - 1)],
            "CS_ENDS": [(R - 1, 0)],
            "CS_VSANCHOR": [(i, anchor_i) for i in range(R) if i != anchor_i],
            "CS_VSBEST": [(i, best) for i in range(R) if i != best],
        }
        AG = {}
        for cs, pairs in sets.items():
            lst = []
            for i, j in pairs:
                o = obs[i] - obs[j]
                sh, sdv = agree_share(sd[i], sd[j], o)
                if not np.isfinite(sdv) or sdv == 0:
                    nzero += 1
                lst.append((i, j, sh, o, sdv))
                cell_rows.append(dict(panel=pk, anchor=anc, ladder=lad, window=win, claimset=cs,
                                      rung_a=rungs[i], rung_b=rungs[j], obs_gap=o,
                                      agree=sh, gap_sd=sdv))
            AG[cs] = lst
        AGREE[(pk, anc, lad, win)] = AG
dfc = pd.DataFrame(cell_rows)
dump(dfc, "cells")
gate("G3", "cells with a zero/non-finite draw SD (degenerate)", nzero, nzero == 0)
P(f"  {len(dfc):,} cells scored.  t={time.time() - T0:.0f}s")
P("")
P("  Cell agreement by claim set (FULL window, all 24 families pooled):")
P(f"  {'claimset':<12s} {'cells':>6s} {'median':>8s} {'p10':>8s} {'>=0.90':>8s} {'>=0.80':>8s} {'>=0.50':>8s}")
for cs in CLAIMSETS:
    s = dfc[(dfc.window == "FULL") & (dfc.claimset == cs)].agree
    P(f"  {cs:<12s} {len(s):>6d} {s.median():>8.4f} {s.quantile(0.10):>8.4f} "
      f"{(s >= 0.90).mean():>8.4f} {(s >= 0.80).mean():>8.4f} {(s >= 0.50).mean():>8.4f}")
P("")

# ================================================================================================
# ARM 2 — the FAMILY level: AGGREGATE reading vs PER-CELL reading of the same bar
# ================================================================================================
P("ARM 2 — AGGREGATE vs PER-CELL READING OF THE SAME BAR (the census arm)")
P("  AGGREGATE: pooled sign-agreement share over (cell, draw) in the claim set >= q.")
P("  PER CELL : every cell's own share >= q  (the family is as decisive as its weakest cell).")
P("  A FLIP is a family where the two readings disagree at the same (claim set, q).")

fam_rows = []
for (pk, anc, lad, win), AG in AGREE.items():
    for cs in CLAIMSETS:
        lst = AG[cs]
        shares = np.array([x[2] for x in lst], float)
        pooled = float(np.nanmean(shares))      # pooled over (cell, draw): mean of per-cell shares
        weakest = float(np.nanmin(shares))
        for q in QUANTS:
            agg = bool(pooled >= q)
            pc = bool(weakest >= q)
            fam_rows.append(dict(panel=pk, anchor=anc, ladder=lad, window=win, claimset=cs, q=q,
                                 n_cells=len(lst), pooled=pooled, weakest=weakest,
                                 AGG=agg, PERCELL=pc, flip=bool(agg != pc),
                                 n_cell_fail=int((shares < q).sum())))
dff = pd.DataFrame(fam_rows)
dump(dff, "families")

grid_rows = []
P("")
P("  FULL window — 24 families per cell of the dial grid:")
P(f"  {'claimset':<12s} {'q':>5s} {'AGG pass':>9s} {'PC pass':>8s} {'flips':>6s} {'flip rate':>10s} "
  f"{'cells failing own bar':>22s}")
for cs in CLAIMSETS:
    for q in QUANTS:
        s = dff[(dff.window == "FULL") & (dff.claimset == cs) & (dff.q == q)]
        nf = int(s.flip.sum())
        cell_fail = int(s.n_cell_fail.sum())
        cell_tot = int(s.n_cells.sum())
        grid_rows.append(dict(window="FULL", claimset=cs, q=q, families=len(s),
                              agg_pass=int(s.AGG.sum()), percell_pass=int(s.PERCELL.sum()),
                              flips=nf, flip_rate=nf / len(s),
                              cells_failing=cell_fail, cells=cell_tot,
                              cell_fail_share=cell_fail / cell_tot))
        mark = "  <- record's incumbent bar" if q == INCUMBENT_Q else ""
        P(f"  {cs:<12s} {q:>5.2f} {int(s.AGG.sum()):>9d} {int(s.PERCELL.sum()):>8d} {nf:>6d} "
          f"{nf / len(s):>10.4f} {cell_fail:>10d} of {cell_tot:<8d}{mark}")
dfg = pd.DataFrame(grid_rows)
dump(dfg, "grid")

P("")
allf = dff[dff.window == "FULL"]
P(f"  HEADLINE (FULL window, 4 claim sets x 6 bars x 24 families = {len(allf)} verdict pairs):")
P(f"    AGG decisive        {int(allf.AGG.sum()):>4d} of {len(allf)}   ({allf.AGG.mean():.4f})")
P(f"    PER-CELL decisive   {int(allf.PERCELL.sum()):>4d} of {len(allf)}   ({allf.PERCELL.mean():.4f})")
P(f"    FLIPS               {int(allf.flip.sum()):>4d} of {len(allf)}   ({allf.flip.mean():.4f})")
onesided = int((allf.AGG & ~allf.PERCELL).sum())
other = int((~allf.AGG & allf.PERCELL).sum())
P(f"    of which AGG-pass / PER-CELL-fail: {onesided}   (the reverse direction: {other})")
inc = allf[allf.q == INCUMBENT_Q]
P(f"    at the record's incumbent bar q={INCUMBENT_Q}: AGG {int(inc.AGG.sum())} of {len(inc)}, "
  f"PER-CELL {int(inc.PERCELL.sum())} of {len(inc)}, flips {int(inc.flip.sum())} "
  f"({inc.flip.mean():.4f})")
q80 = allf[allf.q == 0.80]
P(f"    at 1110's q=0.80 bar: cells failing their own bar {int(q80.n_cell_fail.sum())} of "
  f"{int(q80.n_cells.sum())} ({q80.n_cell_fail.sum() / q80.n_cells.sum():.4f}); 1110's D2 read "
  f"{C1110_D2[0]} of {C1110_D2[1]} ({C1110_D2[0] / C1110_D2[1]:.4f}) on its own family.")
P("")

# ---- CONTROL: block length, never selected on --------------------------------------------------
P("CONTROL — block length L (frozen at 63; never selected on)")
ctrl_rows = []
for L in [L_FROZEN] + L_CONTROL:
    fl, ag, pc = [], [], []
    for (pk, anc, lad), seq in BOOKS.items():
        pan = pans[pk]
        rng = np.random.default_rng(seed_of(pk, anc, lad, "FULL", L))
        rs = [r[pan.warm] for _, r in seq]
        idx = blocks_idx(len(rs[0]), L, rng)
        sd = np.vstack([sharpe_draws(x, idx) for x in rs])
        obs = np.array([fsharpe(x) for x in rs])
        R = len(seq)
        pairs = [(i, i + 1) for i in range(R - 1)]
        sh = np.array([agree_share(sd[i], sd[j], obs[i] - obs[j])[0] for i, j in pairs])
        pooled, weakest = float(np.nanmean(sh)), float(np.nanmin(sh))
        for q in QUANTS:
            ag.append(pooled >= q)
            pc.append(weakest >= q)
            fl.append((pooled >= q) != (weakest >= q))
    ctrl_rows.append(dict(L=L, claimset="CS_STEPS", agg_pass=int(np.sum(ag)),
                          percell_pass=int(np.sum(pc)), flips=int(np.sum(fl)), n=len(fl),
                          flip_rate=float(np.mean(fl))))
    P(f"  L={L:>3d}  CS_STEPS  AGG {int(np.sum(ag)):>3d}  PER-CELL {int(np.sum(pc)):>3d}  "
      f"flips {int(np.sum(fl)):>3d} of {len(fl)}  ({np.mean(fl):.4f})")
dfctl = pd.DataFrame(ctrl_rows)
dump(dfctl, "control")
gm = dfctl.flip_rate
gate("G4", "flip-rate range across L = 21/63/252 (CS_STEPS)", gm.max() - gm.min(), True)
P("")

# ================================================================================================
# ARM 3 — CAPITAL ARM (rule 8): does the reading change what an allocator BUYS?
# ================================================================================================
P("ARM 3 — CAPITAL ARM (rule 8).  Licensing computed on warm-up..2016-12-31 ONLY; 2017-2026 read")
P("  ONCE.  Chooser: move off the 1101 anchor rung to the IS-best-Sharpe rung, but ONLY if the")
P("  family is decisive under the reading being tested.  Controls: DO-NOTHING, ALWAYS-ACT.")

cap_rows = []
pick_rows = []
for pk, pan in pans.items():
    for anc in ANCHORS:
        for lad in LADNAMES:
            seq = BOOKS[(pk, anc, lad)]
            rungs = [str(r) for r, _ in seq]
            sd, obs_is, _ = DRAWSD[(pk, anc, lad, "IS")]
            best = int(np.nanargmax(obs_is))                 # IS-best Sharpe, IS window only
            anchor_i = rungs.index(str(ANCHORS[anc][lad]))
            mets = [block_metrics(r, pan.warm, pan.ins, pan.oos) for _, r in seq]
            AG = AGREE[(pk, anc, lad, "IS")]
            for cs in CLAIMSETS:
                shares = np.array([x[2] for x in AG[cs]], float)
                pooled, weakest = float(np.nanmean(shares)), float(np.nanmin(shares))
                for q in QUANTS:
                    for reading, ok in (("AGG", pooled >= q), ("PERCELL", weakest >= q)):
                        pick = best if ok else anchor_i
                        m = mets[pick]
                        pick_rows.append(dict(panel=pk, anchor=anc, ladder=lad, claimset=cs, q=q,
                                             reading=reading, licensed=bool(ok),
                                             pick=rungs[pick], anchor_rung=rungs[anchor_i],
                                             is_best=rungs[best], moved=bool(pick != anchor_i),
                                             **{k: v for k, v in m.items()}))
            for reading, pick in (("DO_NOTHING", anchor_i), ("ALWAYS_ACT", best)):
                m = mets[pick]
                pick_rows.append(dict(panel=pk, anchor=anc, ladder=lad, claimset="CONTROL", q=np.nan,
                                      reading=reading, licensed=(reading == "ALWAYS_ACT"),
                                      pick=rungs[pick], anchor_rung=rungs[anchor_i],
                                      is_best=rungs[best], moved=bool(pick != anchor_i),
                                      **{k: v for k, v in m.items()}))
dfp = pd.DataFrame(pick_rows)

# KEEP legs for every chosen book
def add_legs(df):
    out = []
    for _, r in df.iterrows():
        b = {k: r[k] for k in ("CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD")}
        sb, lb = SPYM[r.panel], BASE[r.panel]
        l4b = legs_4b(b, sb)
        l4o = legs_4b_oos(b, sb)
        l4a = legs_4a(b, lb)
        out.append(dict(KEEP_4b=all(l4b.values()) and all(l4o.values()),
                        KEEP_4a=all(l4a.values()), **l4b, **l4o, **l4a))
    return pd.concat([df.reset_index(drop=True), pd.DataFrame(out)], axis=1)


dfp = add_legs(dfp)
dump(dfp, "capital")

P("")
P("  Per (reading, claim set, q): mean OOS over the 24 families, moves licensed, KEEP counts.")
P(f"  {'reading':<11s} {'claimset':<12s} {'q':>5s} {'moves':>6s} {'OOS CAGR':>9s} {'OOS Sh':>8s} "
  f"{'OOS MaxDD':>10s} {'4b':>4s} {'4a':>4s}")
for cs in CLAIMSETS:
    for q in QUANTS:
        for reading in ("AGG", "PERCELL"):
            s = dfp[(dfp.claimset == cs) & (dfp.q == q) & (dfp.reading == reading)]
            cap_rows.append(dict(reading=reading, claimset=cs, q=q, n=len(s),
                                 moves=int(s.moved.sum()),
                                 OOS_CAGR=s.OOS_CAGR.mean(), OOS_Sharpe=s.OOS_Sharpe.mean(),
                                 OOS_MaxDD=s.OOS_MaxDD.mean(), keep4b=int(s.KEEP_4b.sum()),
                                 keep4a=int(s.KEEP_4a.sum())))
            P(f"  {reading:<11s} {cs:<12s} {q:>5.2f} {int(s.moved.sum()):>6d} "
              f"{s.OOS_CAGR.mean():>9.2%} {s.OOS_Sharpe.mean():>8.4f} {s.OOS_MaxDD.mean():>10.2%} "
              f"{int(s.KEEP_4b.sum()):>4d} {int(s.KEEP_4a.sum()):>4d}")
for reading in ("DO_NOTHING", "ALWAYS_ACT"):
    s = dfp[dfp.reading == reading]
    cap_rows.append(dict(reading=reading, claimset="CONTROL", q=np.nan, n=len(s),
                         moves=int(s.moved.sum()), OOS_CAGR=s.OOS_CAGR.mean(),
                         OOS_Sharpe=s.OOS_Sharpe.mean(), OOS_MaxDD=s.OOS_MaxDD.mean(),
                         keep4b=int(s.KEEP_4b.sum()), keep4a=int(s.KEEP_4a.sum())))
    P(f"  {reading:<11s} {'CONTROL':<12s} {'':>5s} {int(s.moved.sum()):>6d} "
      f"{s.OOS_CAGR.mean():>9.2%} {s.OOS_Sharpe.mean():>8.4f} {s.OOS_MaxDD.mean():>10.2%} "
      f"{int(s.KEEP_4b.sum()):>4d} {int(s.KEEP_4a.sum()):>4d}")
dfcap = pd.DataFrame(cap_rows)
dump(dfcap, "capitalgrid")

# paired PERCELL - AGG delta over the 24 dial cells x 24 families where the picks differ
P("")
a_ = dfp[(dfp.reading == "AGG") & (dfp.claimset != "CONTROL")].reset_index(drop=True)
b_ = dfp[(dfp.reading == "PERCELL") & (dfp.claimset != "CONTROL")].reset_index(drop=True)
key = ["panel", "anchor", "ladder", "claimset", "q"]
m = a_.merge(b_, on=key, suffixes=("_A", "_P"))
d = m.OOS_Sharpe_P - m.OOS_Sharpe_A
diff = m[m.pick_A != m.pick_P]
dd = diff.OOS_Sharpe_P - diff.OOS_Sharpe_A
P(f"  PAIRED PER-CELL minus AGG, all {len(m)} (family x dial) pairs:")
P(f"    d(OOS Sharpe) mean {d.mean():+.4f}  SE {d.sem():.4f}  t {d.mean() / d.sem() if d.sem() else float('nan'):+.2f}")
P(f"    d(OOS CAGR)   mean {(m.OOS_CAGR_P - m.OOS_CAGR_A).mean():+.4%}   "
  f"d(OOS MaxDD) mean {(m.OOS_MaxDD_P - m.OOS_MaxDD_A).mean():+.4%}")
P(f"  where the two readings PICK DIFFERENT BOOKS ({len(diff)} of {len(m)}, "
  f"{len(diff) / len(m):.4f}):")
if len(diff):
    P(f"    d(OOS Sharpe) mean {dd.mean():+.4f}  SE {dd.sem():.4f}  "
      f"t {dd.mean() / dd.sem() if dd.sem() else float('nan'):+.2f}")
    P(f"    d(OOS CAGR)   mean {(diff.OOS_CAGR_P - diff.OOS_CAGR_A).mean():+.4%}   "
      f"d(OOS MaxDD) mean {(diff.OOS_MaxDD_P - diff.OOS_MaxDD_A).mean():+.4%}")
else:
    P("    (none — the readings never disagree on the IS window at any dial cell)")

# licensed vs refused, the decision-quality question
P("")
lic = dfp[(dfp.claimset != "CONTROL")]
for reading in ("AGG", "PERCELL"):
    s = lic[lic.reading == reading]
    f_, r_ = s[s.licensed], s[~s.licensed]
    P(f"  {reading:<8s} licensed {len(f_):>4d} cells, mean OOS Sharpe {f_.OOS_Sharpe.mean():.4f}; "
      f"refused {len(r_):>4d}, {r_.OOS_Sharpe.mean():.4f}; "
      f"delta {f_.OOS_Sharpe.mean() - r_.OOS_Sharpe.mean():+.4f}" if len(f_) and len(r_) else
      f"  {reading:<8s} licensed {len(f_)} / refused {len(r_)} — one side empty, delta undefined")

P("")
P("  KEEP PATHS over every chooser row in the capital arm:")
P(f"    4b passes {int(dfp.KEEP_4b.sum())} of {len(dfp)};  4a passes {int(dfp.KEEP_4a.sum())} of {len(dfp)}")
for leg in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"):
    P(f"      binding-leg census {leg}: fails {int((~dfp[leg]).sum())} of {len(dfp)}")
P("")

# ---- LEADERBOARD rows: the two readings at the record's incumbent bar, U56 headline -------------
P("LEADERBOARD ROWS (U56, CS_STEPS, incumbent bar q=0.90, anchor A / ladder N — the record's")
P("  headline family; the full 24-cell grid is in the .capitalgrid.csv)")
lb = []
sel = dfp[(dfp.panel == "U56") & (dfp.anchor == "A") & (dfp.ladder == "N") &
          (dfp.claimset == "CS_STEPS") & (dfp.q == INCUMBENT_Q)]
ctl = dfp[(dfp.panel == "U56") & (dfp.anchor == "A") & (dfp.ladder == "N") &
          (dfp.claimset == "CONTROL")]
for _, r in pd.concat([sel, ctl]).iterrows():
    nm = f"1115 {r.reading} gate (U56 N-ladder, q={INCUMBENT_Q if r.claimset != 'CONTROL' else '-'}, pick N={r['pick']})"
    verdict = "KEEP-4b" if r.KEEP_4b else ("KEEP-4a" if r.KEEP_4a else "KILL")
    b0 = BASE["U56"]
    lb.append(f"| {DATE} | {nm} | {r.CAGR:.1%} | {r.Sharpe:.2f} | {r.MaxDD:.1%} | "
              f"{r.H1:.2f} / {r.H2:.2f} | {b0['Sharpe']:.2f} ({b0['H1']:.2f}/{b0['H2']:.2f}) | "
              f"{verdict} | {DATE}_{SLUG}_B.py |")
    P("  " + lb[-1])

dfgate = pd.DataFrame(GATES)
dump(dfgate, "gates")
P("")
P(f"GATES: {int(dfgate.pass_.sum())} of {len(dfgate)} pass.")
P(f"TOTAL RUNTIME {time.time() - T0:.0f}s")
Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
print(f"wrote {OUT.name}.console.txt")
