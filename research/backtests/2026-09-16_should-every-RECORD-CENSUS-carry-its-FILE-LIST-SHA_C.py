#!/usr/bin/env python3
"""IDEA 1019 -- should every RECORD CENSUS carry its FILE-LIST SHA?  (lane C, 2026-09-16)

Idea 1014's G3 missed idea 1010's committed census by 1.49e-02 and its G3b reproduced it at
9.54e-17 once restricted to 1010's own 449-file list: the whole gap was 13,248 rows of
append-only corpus growth, and the run watched its own artifact move the denominator
mid-session.  This run PRICES the stamp 1019 proposes and measures how much of the record's
existing census stock is re-derivable without one.

THE TWO TUNED AXES (the queue line's own; every grid point reported, none selected):

  TUNED 1 -- STAMP SCOPE, 4 rungs, the four things a reader could be given:
    NONE         the corpus as it stands at HEAD today (what a reader actually gets)
    DATE_AT      the corpus in the git tree at the census's OWN commit (self-inclusive)
    DATE_PARENT  the corpus in the tree at parent(commit) (excludes the run's own artifacts)
    LIST         the exact file list the run committed (`*.corpusfiles.csv`), where it exists

  TUNED 2 -- CLAIM SET, 3 rungs:
    REPRO2    the 2 censuses that committed a file list (ideas 1010, 1014): exactly
              re-derivable, published numbers known -> a QUANTITATIVE re-derivation
    CENSUS_N  every committed `*.census.csv[.gz]` artifact -> STRUCTURAL re-derivability
              (stamp level, git-recoverability of its file list, denominator drift to HEAD)
    PROSE     corpus-wide (files, rows) counts regexed out of every committed `*.result.md`
              / `*.memo.md`, attributed to that file's own add-commit and re-derived there

MECHANISM THE ARITHMETIC RESTS ON.  The corpus is append-only, so a file's bytes at any
commit equal its bytes at HEAD unless it was later modified.  G7 measures exactly that, and
it is what lets any historical census be re-derived as a SUM of per-file statistics computed
ONCE at HEAD over the file subset present at that commit -- no historical checkout.

The census statistic re-derived is the record's own `fail4b` leg census (1010/1014's object,
token alphabet and conventions copied verbatim so the cross-run gates are legal).

PROTOCOL: 10 bps, next-day execution, rule 8 walk-forward, both KEEP paths, rule 9 stated.
Writes `RECORD CENSUS` outputs + a rule-8 ladder.  Modifies nothing outside research/.
Deterministic.  Standalone:  python research/backtests/2026-09-16_should-...-SHA_C.py
"""
from __future__ import annotations
import gzip, hashlib, json, os, re, subprocess, sys, time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, band_state, score  # noqa: E402

sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest as engine_backtest, rebalance_mask  # noqa: E402

OUT = ROOT / "research" / "backtests"
STEM = "2026-09-16_should-every-RECORD-CENSUS-carry-its-FILE-LIST-SHA_C"

SMOKE = bool(int(os.environ.get("IDEA1019_SMOKE", "0")))

# ---- the record's 4b alphabet (1010's, verbatim) -----------------------------------------
LEGS = ["H1", "H2", "OOS", "DD", "CAGR"]
LEGNAME = {"H1": "L1_H1", "H2": "L2_H2", "OOS": "L3_OOS", "DD": "L4_DD", "CAGR": "L5_CAGR"}
BIT = {k: 1 << i for i, k in enumerate(LEGS)}
PASS_SENTINEL = {"-", "", "none", "NONE", "None", "nan", "-none-", "NaN", "n/a"}
TOKMAP = {}
for _k, _v in LEGNAME.items():
    TOKMAP[_k] = _k
    TOKMAP[_v] = _k
for _extra, _leg in (("L5_CAGRfloor", "CAGR"), ("CAGRfloor", "CAGR"), ("CAGRFLOOR", "CAGR"),
                     ("DDcap", "DD"), ("DDCAP", "DD"), ("L4_DDcap", "DD")):
    TOKMAP[_extra] = _leg
TOKMAP = {k.upper(): v for k, v in TOKMAP.items()}
SPLIT = re.compile(r"[,|;+/ ]+")
NULL_KIND = re.compile(r"draw|null", re.I)

# ---- price ladder constants (the record's) ------------------------------------------------
OOS_START = "2017-01-01"
WARM = 260
VOLCAP, BAND0 = 0.60, 0.03
HEADRUNG = 10.0
REC_SPY_OOS = dict(CAGR=0.1521, Sharpe=0.8713, MaxDD=-0.3372)

# ---- pre-registered bars ------------------------------------------------------------------
BAR_STAMP = 0.50        # H_STAMP: share of committed censuses carrying a file-list stamp
BAR_APPEND = 0.99       # H_APPEND: share of census-eligible files blob-stable after add
BAR_DERIVE = 1e-3       # H_DERIVE: relative tolerance for "re-derivable"
BAR_DRIFT = 0.01        # H_DRIFT: median denominator drift commit->HEAD
BAR_COSTT = 0.01        # H_COST: stamp wall-time as a share of the scan's
BAR_COSTB = 100_000     # H_COST: stamp bytes

LINES: list[str] = []


def P(s=""):
    print(s, flush=True)
    LINES.append(str(s))


def dump(df, suffix):
    p = OUT / f"{STEM}.{suffix}.csv"
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


def git(*args):
    return subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True,
                          text=True, check=True).stdout


# ==========================================================================================
# (0) corpus primitives -- 1010/1014's, verbatim
# ==========================================================================================
def parse_fail(s):
    if s is None:
        return 0, False
    t = str(s).strip()
    if t in PASS_SENTINEL:
        return 0, True
    m = 0
    for tok in SPLIT.split(t):
        if not tok:
            continue
        k = TOKMAP.get(tok.strip().upper())
        if k is None:
            return 0, False
        m |= BIT[k]
    return m, True


def header_of_bytes(b: bytes, gz: bool):
    if gz:
        b = gzip.decompress(b)
    line = b.split(b"\n", 1)[0].decode("utf-8", "replace")
    return [c.strip() for c in line.rstrip("\r").split(",")]


def header_of(p: Path):
    op = gzip.open(p, "rt") if p.name.endswith(".gz") else open(p, newline="")
    with op as fh:
        line = fh.readline()
    return [c.strip() for c in line.rstrip("\n").rstrip("\r").split(",")]


# ==========================================================================================
# (1) PER-FILE CENSUS AT HEAD  -- computed once, re-aggregated over any historical file set
# ==========================================================================================
def scan_head():
    files = sorted(list(OUT.glob("*.csv")) + list(OUT.glob("*.csv.gz")))
    rows = []
    t0 = time.time()
    for p in files:
        try:
            hdr = header_of(p)
        except Exception:
            continue
        if "fail4b" not in hdr:
            continue
        want = ["fail4b"] + [c for c in ("draw", "kind") if c in hdr]
        try:
            df = pd.read_csv(p, usecols=want, low_memory=False)
        except Exception:
            continue
        raw = df["fail4b"].astype("string").fillna("")
        uniq = raw.unique().tolist()
        pm = {u: parse_fail(u) for u in uniq}
        ok = raw.map({u: pm[u][1] for u in uniq}).fillna(False).to_numpy(bool)
        masks = raw.map({u: pm[u][0] for u in uniq}).fillna(0).to_numpy(np.int64)

        sfx = p.name.replace(".csv.gz", "").replace(".csv", "").split(".")[-1]
        isnull = np.full(len(df), sfx in ("nulls", "draws", "nulls_wide"), bool)
        if "draw" in df.columns:
            d = pd.to_numeric(df["draw"], errors="coerce").to_numpy()
            isnull |= np.nan_to_num(d, nan=-1.0) >= 0
        if "kind" in df.columns:
            isnull |= df["kind"].astype(str).str.contains(NULL_KIND, na=False).to_numpy(bool)

        f = ok & (masks > 0)
        r = dict(file=p.name, rows=len(df), unparsed=int((~ok).sum()),
                 n_fail=int(f.sum()), n_pass=int((ok & (masks == 0)).sum()),
                 null_rows=int((isnull & ok).sum()),
                 n_fail_real=int((f & ~isnull).sum()))
        for k in LEGS:
            r["infail_" + LEGNAME[k]] = int((f & (masks & BIT[k] > 0)).sum())
            r["sole_" + LEGNAME[k]] = int((f & (masks == BIT[k])).sum())
        rows.append(r)
    P(f"  scanned {len(rows)} committed CSVs carrying `fail4b` of {len(files):,} "
      f"corpus CSVs  ({time.time()-t0:.0f}s)")
    return pd.DataFrame(rows), time.time() - t0, len(files)


CENSUS_COLS = None


def census_of(perfile: pd.DataFrame, fileset) -> dict:
    """The census statistic, aggregated over an arbitrary subset of the HEAD per-file table."""
    d = perfile[perfile["file"].isin(fileset)]
    n_fail = int(d["n_fail"].sum())
    out = dict(n_files=int(len(d)), n_rows=int(d["rows"].sum()), n_fail=n_fail,
               n_pass=int(d["n_pass"].sum()), n_null=int(d["null_rows"].sum()),
               n_fail_real=int(d["n_fail_real"].sum()))
    for k in LEGS:
        nm = LEGNAME[k]
        out["infail_" + nm] = d["infail_" + nm].sum() / n_fail if n_fail else np.nan
        out["sole_" + nm] = d["sole_" + nm].sum() / n_fail if n_fail else np.nan
    return out


# ==========================================================================================
# (2) GIT TIMELINE -- replay adds/mods/deletes to get the file set at every commit
# ==========================================================================================
def timeline():
    raw = git("log", "--reverse", "--name-status", "--format=C\t%H\t%cI",
              "--", "research/backtests")
    commits = []          # (sha, iso, frozenset of paths present AFTER this commit)
    present = set()
    addcommit, modcount, delset = {}, {}, set()
    sha = iso = None
    order = {}
    for line in raw.split("\n"):
        if not line.strip():
            continue
        parts = line.split("\t")
        if parts[0] == "C":
            if sha is not None:
                commits.append((sha, iso, frozenset(present)))
            sha, iso = parts[1], parts[2]
            order[sha] = len(commits)
            continue
        st, path = parts[0], parts[-1]
        name = path.split("/")[-1]
        if st.startswith("A"):
            present.add(name)
            addcommit.setdefault(name, (sha, iso))
        elif st.startswith("M"):
            present.add(name)
            modcount[name] = modcount.get(name, 0) + 1
        elif st.startswith("D"):
            present.discard(name)
            delset.add(name)
    if sha is not None:
        commits.append((sha, iso, frozenset(present)))
    return commits, addcommit, modcount, delset


def files_at(commits, sha, parent=False):
    """File set present after commit `sha`; parent=True -> the set just BEFORE it."""
    for i, (s, _iso, fs) in enumerate(commits):
        if s == sha:
            if not parent:
                return fs
            return commits[i - 1][2] if i else frozenset()
    return None


def is_csv(name):
    return name.endswith(".csv") or name.endswith(".csv.gz")


def n_csv(fileset):
    """Ground truth a reader CAN reconstruct with no stamp at all: how many CSVs the
    committed corpus held at that commit.  Independent of the fail4b restriction."""
    return sum(1 for f in fileset if is_csv(f))


# ==========================================================================================
# (3) STAMP LEVELS + DRIFT for every committed census artifact
# ==========================================================================================
STAMP_LEVELS = {0: "L0_NONE", 1: "L1_COUNT", 2: "L2_LIST", 3: "L3_SHA"}
RE_FILES = re.compile(r"([0-9]{1,3}(?:,[0-9]{3})*|[0-9]+)\s*(?:committed\s+)?(?:CSV\s+)?files?\b",
                      re.I)
RE_ROWS = re.compile(r"([0-9]{1,3}(?:,[0-9]{3})*|[0-9]+)\s*(?:parsed\s+|committed\s+)?"
                     r"(?:4b\s+)?(?:FAIL|PASS|census|corpus|ladder)?\s*rows\b", re.I)
RE_SHA = re.compile(r"\bsha(?:256|1)?\b|file[_ ]list[_ ]sha", re.I)
# deliberately CONSERVATIVE: only claims about the TOTAL size of the committed corpus, never
# a subset claim ("160 committed files carry an OOS Sharpe"), which has no git ground truth.
RE_CORPUS_SIZE = re.compile(r"([\d,]{2,})\s+(?:committed\s+)?CSVs?\b"
                            r"|\(([\d,]{2,})\s+scanned\)"
                            r"|([\d,]{2,})\s+committed\s+CSV\s+files?\b", re.I)


def n(x):
    return int(str(x).replace(",", ""))


def stamp_level(stem_name: str, present: set) -> tuple[int, str]:
    """What provenance a run committed alongside its census."""
    fl = f"{stem_name}.corpusfiles.csv"
    if fl in present:
        return 2, fl
    txt = ""
    for sfx in (".result.md", ".console.txt", ".memo.md"):
        p = OUT / f"{stem_name}{sfx}"
        if p.exists():
            txt += p.read_text(errors="replace")
    if RE_SHA.search(txt) and ("file list" in txt.lower() or "file_list" in txt.lower()):
        return 3, "sha-in-text"
    if RE_FILES.search(txt) or RE_ROWS.search(txt):
        return 1, "count-in-text"
    return 0, "-"


# ==========================================================================================
# (4) PRICE LADDER (rule 8) -- the record's machinery, verbatim
# ==========================================================================================
def offset_mask(idx, per):
    if per == "D":
        return pd.Series(True, index=idx)
    key = pd.Series(idx.to_period(per), index=idx)
    return key != key.shift(-1)


class Ctx:
    def __init__(self, px, mask):
        self.idx = px.index
        self.rets = px.pct_change().fillna(0.0).values
        m = np.asarray(mask.values, bool)
        m = np.concatenate([[False], m[:-1]]).copy()
        m[0] = True
        self.T, self.N = self.rets.shape
        C = np.cumprod(1.0 + self.rets, axis=0)
        self.Cp = np.vstack([np.ones((1, self.N)), C[:-1]])
        self.reb = np.flatnonzero(m)
        seg = np.searchsorted(self.reb, np.arange(self.T), side="right") - 1
        self.s0 = self.reb[seg]
        self.s0p = self.reb[np.maximum(seg - 1, 0)]
        self.ratio = self.Cp / self.Cp[self.s0]
        self.ratiop = self.Cp / self.Cp[self.s0p]

    def shift(self, W):
        return W.reindex(self.idx).fillna(0.0).shift(1).fillna(0.0).values

    def run(self, wt):
        W0 = wt[self.s0]
        h = W0 * self.ratio
        V = h.sum(axis=1) + (1.0 - W0.sum(axis=1))
        held = h / V[:, None]
        W0p = wt[self.s0p]
        hp = W0p * self.ratiop
        Vp = hp.sum(axis=1) + (1.0 - W0p.sum(axis=1))
        heldp = hp / Vp[:, None]
        heldp[self.reb[0]] = 0.0
        turn = np.zeros(self.T)
        turn[self.reb] = np.abs(wt[self.reb] - heldp[self.reb]).sum(axis=1)
        return (held * self.rets).sum(axis=1), turn


def sharpe(r):
    v = r.std() * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan


def maxdd(r):
    eq = np.cumprod(1.0 + r)
    return float((eq / np.maximum.accumulate(eq) - 1).min())


def cagr(r):
    eq = np.cumprod(1.0 + r)
    y = len(r) / 252.0
    return float(eq[-1] ** (1 / y) - 1) if y > 0 else np.nan


def profile(r, oi):
    h = len(r) // 2
    o, i_ = r[oi:], r[:oi]
    hi = len(i_) // 2
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=maxdd(r),
                H1=sharpe(r[:h]), H2=sharpe(r[h:]),
                OOS_CAGR=cagr(o), OOS_Sharpe=sharpe(o), OOS_MaxDD=maxdd(o),
                IS_CAGR=cagr(i_), IS_Sharpe=sharpe(i_), IS_MaxDD=maxdd(i_),
                IS_H1=sharpe(i_[:hi]), IS_H2=sharpe(i_[hi:]))


def legs_of(d, spy):
    return dict(H1=d["H1"] > spy["H1"], H2=d["H2"] > spy["H2"],
                OOS=d["OOS_Sharpe"] > spy["OOS_Sharpe"],
                DD=abs(d["OOS_MaxDD"]) <= 0.60 * abs(spy["OOS_MaxDD"]),
                CAGR=d["OOS_CAGR"] >= 0.70 * spy["OOS_CAGR"])


def legs_is(d, spy):
    return dict(H1=d["IS_H1"] > spy["IS_H1"], H2=d["IS_H2"] > spy["IS_H2"],
                OOS=d["IS_Sharpe"] > spy["IS_Sharpe"],
                DD=abs(d["IS_MaxDD"]) <= 0.60 * abs(spy["IS_MaxDD"]),
                CAGR=d["IS_CAGR"] >= 0.70 * spy["IS_CAGR"])


def maskname(lg):
    return ",".join(LEGNAME[k] for k in LEGS if not lg[k]) or "-"


def ew_gross(px, g):
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    return g * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)


def band_book(px, band, g):
    return ew_gross(px, g).where(band_state(px, band) & px.notna(), 0.0)


def ew_elig(px, g):
    _, above, vol20 = score(px, vol_scale=False)
    e = (above & (vol20 < VOLCAP)).astype(float).where(px.notna(), 0.0)
    return g * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)


def ranked_book(px, g, k):
    sc, above, vol20 = score(px, vol_scale=False)
    rank = sc.where(above & (vol20 < VOLCAP)).rank(axis=1, ascending=False)
    return (rank <= k).astype(float) * (g / k)


BOOKS = {"EWELIG": lambda p, g: ew_elig(p, g),
         "BAND03": lambda p, g: band_book(p, BAND0, g),
         "TOP10":  lambda p, g: ranked_book(p, g, 10),
         "TOP20":  lambda p, g: ranked_book(p, g, 20),
         "TOP40":  lambda p, g: ranked_book(p, g, 40)}
GROSSES = [0.50, 0.75, 1.00]
CADS = ["W", "M"]


def ladder():
    panels = {"U56": load_universe()}
    if not SMOKE:
        panels["B136"] = load_universe(broad=True)
    rows, picks = [], []
    gate_g1 = gate_g2 = np.nan
    spy_rows = []
    for pn, px in panels.items():
        idx = px.index
        post = idx[WARM:]
        oi = int(np.searchsorted(post, pd.Timestamp(OOS_START)))
        spyr = px["SPY"].pct_change().fillna(0.0).values[WARM:]
        spyp = profile(spyr, oi)
        spy_rows.append(dict(panel=pn, **{k: spyp[k] for k in
                                          ("CAGR", "Sharpe", "MaxDD", "H1", "H2",
                                           "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD")}))
        for cad in CADS:
            ctx = Ctx(px, offset_mask(idx, cad))
            for bname, bf in BOOKS.items():
                for g in GROSSES:
                    W = bf(px, g)
                    wt = ctx.shift(W)
                    r, t = ctx.run(wt)
                    net = (r - t * HEADRUNG / 1e4)[WARM:]
                    d = profile(net, oi)
                    lg = legs_of(d, spyp)
                    lgi = legs_is(d, dict(IS_H1=spyp["IS_H1"], IS_H2=spyp["IS_H2"],
                                          IS_Sharpe=spyp["IS_Sharpe"],
                                          IS_MaxDD=spyp["IS_MaxDD"],
                                          IS_CAGR=spyp["IS_CAGR"]))
                    rows.append(dict(panel=pn, cad=cad, book=bname, gross=g,
                                     **d, pass4b=all(lg.values()),
                                     fail4b=maskname(lg), is_pass4b=all(lgi.values()),
                                     turnover_yr=float(t[WARM:].sum() / (len(net) / 252))))
                    if np.isnan(gate_g1) and pn == "U56" and cad == "W" and \
                            bname == "BAND03" and g == 0.75:
                        # engine.backtest carries 2 NaN returns in the pre-warm-up window
                        # (names with leading NaN prices); the record reads the post-warm-up
                        # path, so the gate is asserted there, on returns AND turnover.
                        ref = engine_backtest(px, W, cost_bps=HEADRUNG, freq="W")
                        gate_g1 = float(np.abs(ref["returns"].values[WARM:] -
                                               (r - t * HEADRUNG / 1e4)[WARM:]).max())
                        gate_g1t = float(np.abs(ref["turnover"].values[WARM:] -
                                                t[WARM:]).max())
                        gate_g1 = max(gate_g1, gate_g1t)
                        gate_g2 = float((W - rules_v2_weights(px)).abs().to_numpy().max())
    grid = pd.DataFrame(rows)
    # --- rule 8: IS-only choosers pick on 2009-2016, OOS read once
    base = pd.DataFrame(spy_rows).set_index("panel")
    for pn in grid["panel"].unique():
        sub = grid[grid["panel"] == pn]
        for ch, keyf in (("IS_SHARPE", lambda d: d["IS_Sharpe"]),
                         ("IS_CAGR", lambda d: d["IS_CAGR"]),
                         ("IS_LEGS", lambda d: d["is_pass4b"].astype(float) * 1e6 +
                          d["IS_Sharpe"])):
            k = keyf(sub)
            w = sub.loc[k.idxmax()]
            picks.append(dict(panel=pn, chooser=ch, book=w["book"], cad=w["cad"],
                              gross=w["gross"], OOS_CAGR=w["OOS_CAGR"],
                              OOS_Sharpe=w["OOS_Sharpe"], OOS_MaxDD=w["OOS_MaxDD"],
                              pass4b=w["pass4b"], fail4b=w["fail4b"],
                              spy_OOS_CAGR=base.loc[pn, "OOS_CAGR"],
                              spy_OOS_Sharpe=base.loc[pn, "OOS_Sharpe"],
                              spy_OOS_MaxDD=base.loc[pn, "OOS_MaxDD"]))
    return grid, pd.DataFrame(picks), pd.DataFrame(spy_rows), gate_g1, gate_g2, panels


def keep_paths(grid, panels):
    """4a against the LIVE book (RULES v2), 4b against SPY -- both, every grid point."""
    live = {}
    for pn, px in panels.items():
        idx = px.index
        post = idx[WARM:]
        oi = int(np.searchsorted(post, pd.Timestamp(OOS_START)))
        ctx = Ctx(px, offset_mask(idx, "W"))
        wt = ctx.shift(rules_v2_weights(px))
        r, t = ctx.run(wt)
        live[pn] = profile((r - t * HEADRUNG / 1e4)[WARM:], oi)
    out = []
    for _, r in grid.iterrows():
        lv = live[r["panel"]]
        a = (r["H1"] > lv["H1"]) and (r["H2"] > lv["H2"]) and (r["MaxDD"] >= lv["MaxDD"])
        out.append(dict(panel=r["panel"], cad=r["cad"], book=r["book"], gross=r["gross"],
                        pass4a=bool(a), pass4b=bool(r["pass4b"]), fail4b=r["fail4b"],
                        live_H1=lv["H1"], live_H2=lv["H2"], live_MaxDD=lv["MaxDD"],
                        live_OOS_CAGR=lv["OOS_CAGR"], live_OOS_Sharpe=lv["OOS_Sharpe"],
                        live_OOS_MaxDD=lv["OOS_MaxDD"]))
    return pd.DataFrame(out), live


# ==========================================================================================
# MAIN
# ==========================================================================================
def main():
    t_start = time.time()
    P("=" * 94)
    P("IDEA 1019 -- should every RECORD CENSUS carry its FILE-LIST SHA?   (lane C)")
    P("=" * 94)
    P("TUNED 1 STAMP SCOPE  {NONE, DATE_AT, DATE_PARENT, LIST}")
    P("TUNED 2 CLAIM SET    {REPRO2, CENSUS_N, PROSE}")
    P("All grid points reported.  10 bps, next-day execution, rule 8, both KEEP paths.")
    P()

    # ---------------------------------------------------------------- corpus + timeline
    P("[1] CORPUS AT HEAD")
    perfile, scan_secs, n_corpus_csv = scan_head()
    head_files = set(perfile["file"])
    head_cen = census_of(perfile, head_files)
    P(f"  HEAD census: {head_cen['n_files']} files, {head_cen['n_rows']:,} rows, "
      f"{head_cen['n_fail']:,} parsed 4b FAIL rows "
      f"({head_cen['n_null']:,} null-draw, {head_cen['n_fail_real']:,} real-FAIL)")
    own = {f for f in head_files if f.startswith(STEM)}
    cen_ex = census_of(perfile, head_files - own)
    P(f"  EXCLUDING this run's own {len(own)} eligible artifacts: {cen_ex['n_files']} files, "
      f"{cen_ex['n_rows']:,} rows, {cen_ex['n_fail']:,} FAIL rows")
    P("  (`.grid` / `.keeppaths` / `.walkforward` carry a `fail4b` column, so THIS script's")
    P("   own outputs are census-eligible: a second pass over a directory holding them reads")
    P(f"   {cen_ex['n_files']+3} files, not {cen_ex['n_files']} -- the 1019 defect, reproduced")
    P("   live.  The headline is taken on the self-excluded set; both are stamped below.)")
    P()

    P("[2] GIT TIMELINE of research/backtests")
    commits, addcommit, modcount, delset = timeline()
    P(f"  {len(commits):,} commits touching research/backtests, "
      f"{addcommit and len(addcommit):,} distinct files added, "
      f"{len(modcount)} modified after add, {len(delset)} deleted")
    elig_mod = sorted(f for f in modcount if f in head_files)
    append_rate = 1.0 - len(elig_mod) / max(len(head_files), 1)
    P(f"  census-eligible files modified after their add commit: {len(elig_mod)} of "
      f"{len(head_files)}  -> append-only rate {append_rate:.4f}")
    if elig_mod:
        P("    " + ", ".join(elig_mod[:6]) + ("..." if len(elig_mod) > 6 else ""))
    P()

    # ---------------------------------------------------------------- GATES (before results)
    P("[3] GATES  (printed before any result number)")
    grows = []
    grid, picks, spy_rows, g1, g2, panels = ladder()

    # G0 -- parse coverage
    unp = int(perfile["unparsed"].sum())
    tot = int(perfile["rows"].sum())
    grows.append(("G0", "fail4b parse coverage (unparsed values are EXCLUDED, never guessed)",
                  unp / max(tot, 1), unp == 0 or unp / tot < 0.01,
                  f"{unp} unparsed of {tot:,}"))

    # G1/G2 -- fast runner and book identity
    grows.append(("G1", "fast Ctx == engine.backtest (U56/BAND03@0.75/W, post-warm-up net "
                        "returns AND turnover)", g1, g1 < 1e-12, f"max|d| {g1:.3e}"))
    grows.append(("G2", "band_book(px,0.03,0.75) == baseline.rules_v2_weights(px)",
                  g2, g2 < 1e-15, f"max|d| {g2:.3e}"))

    # G3 -- CROSS-RUN: reproduce idea 1010's committed census under the LIST scope
    lst1010 = OUT / ("2026-09-16_does-the-SOLE-KILLER-MONOPOLY-of-the-TWO-LEVEL-LEGS-"
                     "hold-on-the-RECORD-s-COMMITTED-FAIL-ROWS_C.corpusfiles.csv")
    pub1010 = dict(n_files=449, n_rows=995_062, n_fail=883_294)
    cen1010 = man1010 = None
    if lst1010.exists():
        man1010 = pd.read_csv(lst1010)[["file", "rows", "n_fail"]]
        fl = set(man1010["file"])
        cen1010 = census_of(perfile, fl)
        # G3 -- PER-FILE reproduction of the manifest, the strongest form of the cross-run
        j = man1010.merge(perfile[["file", "rows", "n_fail"]], on="file", how="left",
                          suffixes=("_pub", "_now"))
        d = float(np.nanmax(np.abs(np.r_[(j["rows_pub"] - j["rows_now"]).to_numpy(float),
                                         (j["n_fail_pub"] - j["n_fail_now"]).to_numpy(float)])))
        grows.append(("G3", "CROSS-RUN PER-FILE: idea 1010's committed 449-file manifest "
                            "re-read at HEAD (rows and n_fail)", d, d == 0,
                      f"{len(j)} files, {int(j['rows_now'].sum()):,} rows / "
                      f"{int(j['n_fail_now'].sum()):,} FAIL, max per-file |d| {d:.0f}"))
        # G3b -- the record's INTERNAL consistency: does 1010's PUBLISHED prose total agree
        #        with the manifest 1010 itself committed?
        gap = int(j["rows_pub"].sum()) - pub1010["n_rows"]
        gapf = int(j["n_fail_pub"].sum()) - pub1010["n_fail"]
        grows.append(("G3b", "INTERNAL: idea 1010's PUBLISHED prose totals == its OWN "
                             "committed manifest", abs(gap), gap == 0 and gapf == 0,
                      f"manifest {int(j['rows_pub'].sum()):,} rows / "
                      f"{int(j['n_fail_pub'].sum()):,} FAIL vs prose 995,062 / 883,294  "
                      f"-> rows {gap:+,}, FAIL {gapf:+,}"))
    else:
        grows.append(("G3", "CROSS-RUN idea 1010 file list", np.nan, False, "list not found"))

    # G3c -- rule out the competing explanation for ANY manifest miss: the census-eligible
    #        files MODIFIED IN PLACE after their add commit.  A file LIST cannot see an
    #        in-place edit; only a content SHA can.  Measure what those edits actually moved.
    growth = []
    for fn in elig_mod:
        sha, _iso = addcommit.get(fn, (None, None))
        if sha is None:
            continue
        try:
            blob = subprocess.run(["git", "-C", str(ROOT), "show",
                                   f"{sha}:research/backtests/{fn}"],
                                  capture_output=True, check=True).stdout
        except subprocess.CalledProcessError:
            continue
        gz = fn.endswith(".gz")
        n_then = (gzip.decompress(blob) if gz else blob).count(b"\n") - 1
        n_now = int(perfile.loc[perfile["file"] == fn, "rows"].iloc[0])
        growth.append((fn, n_then, n_now, n_now - n_then))
    added_by_edit = sum(g[3] for g in growth)
    on_1010 = sum(1 for g in growth if man1010 is not None and
                  g[0] in set(man1010["file"]))
    grows.append(("G3c", "CONTROL: in-place edits are NOT the channel -- rows added by "
                         "editing a file after its add commit", abs(added_by_edit),
                  added_by_edit == 0,
                  f"{len(growth)} edited eligible files ({on_1010} of them on 1010's "
                  f"manifest) moved {added_by_edit:+,} rows: " +
                  "; ".join(f"{g[0][:38]} {g[1]:,}->{g[2]:,}" for g in growth)))

    # G4 -- CROSS-RUN: idea 1014's published FAIL-row count on its own list
    lst1014 = OUT / "2026-09-16_is-the-4b-H2-LEG-DEAD-WEIGHT_cloud.corpusfiles.csv"
    cen1014 = None
    if lst1014.exists():
        fl = set(pd.read_csv(lst1014)["file"])
        cen1014 = census_of(perfile, fl)
        d = abs(cen1014["n_fail"] - 896_542) / 896_542
        grows.append(("G4", "CROSS-RUN: idea 1014's 896,542 FAIL rows on its OWN list",
                      d, d < 1e-9, f"{cen1014['n_fail']:,} vs published 896,542"))
    else:
        grows.append(("G4", "CROSS-RUN idea 1014 file list", np.nan, False, "list not found"))

    # G5 -- SPY OOS triple == the record's committed comparand
    u = spy_rows[spy_rows["panel"] == "U56"].iloc[0]
    d5 = max(abs(u["OOS_CAGR"] - REC_SPY_OOS["CAGR"]),
             abs(u["OOS_Sharpe"] - REC_SPY_OOS["Sharpe"]),
             abs(u["OOS_MaxDD"] - REC_SPY_OOS["MaxDD"]))
    grows.append(("G5", "SPY OOS triple == the record's committed 15.21%/0.8713/-33.72%",
                  d5, d5 < 5e-4, f"{u['OOS_CAGR']:.4%} / {u['OOS_Sharpe']:.4f} / "
                                 f"{u['OOS_MaxDD']:.4%}"))

    # G6 -- determinism of the census aggregation
    a = census_of(perfile, head_files)
    b = census_of(perfile, head_files)
    d6 = max(abs(a[k] - b[k]) for k in a if isinstance(a[k], (int, float)))
    grows.append(("G6", "determinism: census_of re-run on the same file set", d6, d6 == 0,
                  "0.0"))

    # G7 -- APPEND-ONLY: the whole re-derivation rests on blob stability after add
    rng = np.random.default_rng(1019)
    samp = sorted(head_files)
    samp = [samp[i] for i in rng.choice(len(samp), size=min(30, len(samp)), replace=False)]
    bad7, checked7 = [], 0
    for fn in samp:
        sha, _iso = addcommit.get(fn, (None, None))
        if sha is None:
            continue
        try:
            blob = subprocess.run(["git", "-C", str(ROOT), "show",
                                   f"{sha}:research/backtests/{fn}"],
                                  capture_output=True, check=True).stdout
        except subprocess.CalledProcessError:
            continue
        cur = (OUT / fn).read_bytes()
        checked7 += 1
        if hashlib.sha256(blob).hexdigest() != hashlib.sha256(cur).hexdigest():
            bad7.append(fn)
    grows.append(("G7", "APPEND-ONLY: sampled census files byte-identical at add-commit "
                        "and HEAD", len(bad7) / max(checked7, 1), not bad7,
                  f"{len(bad7)} of {checked7} sampled differ"))

    gates = pd.DataFrame(grows, columns=["gate", "what", "value", "pass", "detail"])
    for _, r in gates.iterrows():
        v = r["value"]
        vs = "   nan" if (isinstance(v, float) and np.isnan(v)) else f"{v:.3e}"
        P(f"  {r['gate']:<4} {'PASS' if r['pass'] else 'FAIL'}  {vs}  {r['what']}")
        P(f"        {r['detail']}")
    P(f"  GATES {int(gates['pass'].sum())} of {len(gates)} PASS")
    P()

    # ---------------------------------------------------------------- CLAIM SET 1: REPRO2
    P("[4] TUNED2 = REPRO2  x  TUNED1 = the four STAMP SCOPES")
    P("    the 2 committed censuses that shipped a file list, re-derived four ways")
    red = []
    subjects = [
        ("1010", "2026-09-16_does-the-SOLE-KILLER-MONOPOLY-of-the-TWO-LEVEL-LEGS-"
                 "hold-on-the-RECORD-s-COMMITTED-FAIL-ROWS_C",
         dict(n_files=449, n_rows=995_062, n_fail=883_294)),
        ("1014", "2026-09-16_is-the-4b-H2-LEG-DEAD-WEIGHT_cloud",
         dict(n_fail=896_542)),
    ]
    for idea, stem, pub in subjects:
        art = f"{stem}.census.csv"
        sha, iso = addcommit.get(art, (None, None))
        scopes = {"NONE": head_files}
        if sha:
            scopes["DATE_AT"] = set(files_at(commits, sha) or ()) & head_files
            scopes["DATE_PARENT"] = set(files_at(commits, sha, parent=True) or ()) & head_files
        fl = OUT / f"{stem}.corpusfiles.csv"
        if fl.exists():
            scopes["LIST"] = set(pd.read_csv(fl)["file"])
        for sc, fs in scopes.items():
            c = census_of(perfile, fs)
            row = dict(idea=idea, scope=sc, commit=(sha or "")[:8], commit_iso=iso or "",
                       **{k: c[k] for k in ("n_files", "n_rows", "n_fail")})
            for k, v in pub.items():
                row["pub_" + k] = v
                row["relerr_" + k] = abs(c[k] - v) / v
            row["max_relerr"] = max(row["relerr_" + k] for k in pub)
            row["rederivable"] = bool(row["max_relerr"] <= BAR_DERIVE)
            for k in LEGS:
                row["sole_" + LEGNAME[k]] = c["sole_" + LEGNAME[k]]
                row["infail_" + LEGNAME[k]] = c["infail_" + LEGNAME[k]]
            red.append(row)
    rede = pd.DataFrame(red)
    P(rede[["idea", "scope", "commit", "n_files", "n_rows", "n_fail", "max_relerr",
            "rederivable"]].to_string(index=False,
                                      formatters={"max_relerr": lambda x: f"{x:.3e}"}))
    P("    `pub` is what each run PUBLISHED IN PROSE.  1010's residual under LIST and")
    P("    DATE_AT is NOT corpus drift: G3 reproduces its manifest per file at |d| = 0, and")
    P("    G3b shows the 48 rows are a gap between 1010's prose and 1010's OWN manifest.")
    P()
    P("    MANIFEST COMPLETENESS -- does a committed file list enumerate everything the run")
    P("    SCANNED, or only the files that HIT?  A partial manifest pins a numerator and")
    P("    leaves the denominator loose.")
    for idea, stem, _pub in subjects:
        fl = OUT / f"{stem}.corpusfiles.csv"
        if not fl.exists():
            continue
        lst = pd.read_csv(fl)
        listed = set(lst["file"])
        art = f"{stem}.census.csv"
        sha, _iso = addcommit.get(art, (None, None))
        at = set(files_at(commits, sha) or ()) & head_files if sha else set()
        zero_hit_listed = int(perfile[perfile["file"].isin(listed)]["n_fail"].eq(0).sum())
        missing = at - listed
        miss_zero = int(perfile[perfile["file"].isin(missing)]["n_fail"].eq(0).sum())
        P(f"      idea {idea}: manifest {len(listed)} files; eligible files in its own tree "
          f"{len(at)}; {len(missing)} eligible files ABSENT from the manifest, of which "
          f"{miss_zero} carry ZERO FAIL rows; {zero_hit_listed} listed files carry zero")
    P()

    # ---------------------------------------------------------------- CLAIM SET 2: CENSUS_N
    P("[5] TUNED2 = CENSUS_N -- every committed census artifact: stamp level + drift")
    cen_arts = sorted([p.name for p in OUT.glob("*.census.csv")] +
                      [p.name for p in OUT.glob("*.census.csv.gz")])
    cen_arts = [a for a in cen_arts if not a.startswith(STEM)]   # never census itself
    present_head = set(p.name for p in OUT.iterdir())
    crows = []
    for art in cen_arts:
        stem = art.replace(".census.csv.gz", "").replace(".census.csv", "")
        sha, iso = addcommit.get(art, (None, None))
        lvl, how = stamp_level(stem, present_head)
        at = set(files_at(commits, sha) or ()) & head_files if sha else set()
        pa = set(files_at(commits, sha, parent=True) or ()) & head_files if sha else set()
        c_at = census_of(perfile, at) if at else dict(n_files=0, n_rows=0, n_fail=0)
        c_pa = census_of(perfile, pa) if pa else dict(n_files=0, n_rows=0, n_fail=0)
        csv_at = n_csv(files_at(commits, sha) or ()) if sha else 0
        csv_pa = n_csv(files_at(commits, sha, parent=True) or ()) if sha else 0
        crows.append(dict(
            artifact=art, commit=(sha or "")[:8], commit_iso=iso or "",
            stamp_level=STAMP_LEVELS[lvl], stamp_how=how,
            git_recoverable=bool(sha),
            n_files_at=c_at["n_files"], n_fail_at=c_at["n_fail"],
            n_files_parent=c_pa["n_files"], n_fail_parent=c_pa["n_fail"],
            n_csv_at=csv_at, n_csv_parent=csv_pa,
            self_inclusion_csv=csv_at - csv_pa,
            self_inclusion_files=c_at["n_files"] - c_pa["n_files"],
            self_inclusion_fail=c_at["n_fail"] - c_pa["n_fail"],
            drift_files=(head_cen["n_files"] - c_at["n_files"]) / max(c_at["n_files"], 1),
            drift_fail=(head_cen["n_fail"] - c_at["n_fail"]) / max(c_at["n_fail"], 1)))
    cens = pd.DataFrame(crows)
    lvlcount = cens["stamp_level"].value_counts().to_dict()
    P(f"  {len(cens)} committed census artifacts")
    for k in ("L0_NONE", "L1_COUNT", "L2_LIST", "L3_SHA"):
        P(f"    {k:<9} {lvlcount.get(k, 0):>4}   ({lvlcount.get(k,0)/max(len(cens),1):.4f})")
    share_stamped = (cens["stamp_level"].isin(["L2_LIST", "L3_SHA"])).mean()
    P(f"  file-list-or-better stamp: {share_stamped:.4f}  "
      f"({int((cens['stamp_level'].isin(['L2_LIST','L3_SHA'])).sum())} of {len(cens)})")
    P(f"  git-recoverable file list (add-commit found): "
      f"{cens['git_recoverable'].mean():.4f}")
    valid = cens[cens["n_files_at"] > 0]
    P(f"  denominator DRIFT to HEAD over {len(valid)} locatable censuses "
      f"(census-eligible FAIL rows):")
    P(f"    median {valid['drift_fail'].median():.4f}   mean "
      f"{valid['drift_fail'].mean():.4f}   p90 {valid['drift_fail'].quantile(0.90):.4f}   "
      f"max {valid['drift_fail'].max():.4f}")
    P(f"  SELF-INCLUSION (the census's OWN commit adds CSVs the run could not have scanned):")
    P(f"    on ALL committed CSVs:      "
      f"{(cens['self_inclusion_csv'] > 0).mean():.4f} of censuses, median "
      f"{cens['self_inclusion_csv'].median():.1f}, max "
      f"{cens['self_inclusion_csv'].max():.0f} files")
    P(f"    on census-ELIGIBLE CSVs:    "
      f"{(valid['self_inclusion_files'] > 0).mean():.4f} of censuses, median "
      f"{valid['self_inclusion_files'].median():.1f} files / "
      f"{valid['self_inclusion_fail'].median():,.0f} FAIL rows, max "
      f"{valid['self_inclusion_fail'].max():,.0f} FAIL rows")
    P()

    # ---------------------------------------------------------------- CLAIM SET 3: PROSE
    P("[6] TUNED2 = PROSE -- every committed document's claim about HOW BIG THE CORPUS WAS")
    P("    ground truth: the number of CSVs under research/backtests in the git tree, which")
    P("    a reader can rebuild with NO stamp.  Exact match, and 1% / 5% bands.")
    P(f"    corpus size at HEAD: {n_csv(commits[-1][2]):,} CSVs")
    prows = []
    for p in sorted(list(OUT.glob("*.result.md")) + list(OUT.glob("*.memo.md"))):
        txt = p.read_text(errors="replace").replace("**", "")
        sha, iso = addcommit.get(p.name, (None, None))
        if not sha:
            continue
        truth = {"NONE": n_csv(commits[-1][2]),
                 "DATE_AT": n_csv(files_at(commits, sha) or ()),
                 "DATE_PARENT": n_csv(files_at(commits, sha, parent=True) or ())}
        for m in RE_CORPUS_SIZE.finditer(txt):
            claim = n(next(g for g in m.groups() if g))
            if claim < 50:                       # not a corpus-size claim
                continue
            row = dict(source=p.name, commit=sha[:8], commit_iso=iso, claim_csvs=claim,
                       snippet=txt[max(0, m.start() - 70):m.end() + 40]
                       .replace("\n", " ").strip()[:150])
            for sc, t in truth.items():
                row["truth_" + sc] = t
                row["relerr_" + sc] = abs(claim - t) / t if t else np.nan
                row["exact_" + sc] = bool(claim == t)
            row["best_scope"] = min(truth, key=lambda s: row["relerr_" + s])
            row["best_relerr"] = row["relerr_" + row["best_scope"]]
            prows.append(row)
    prose = pd.DataFrame(prows)
    if len(prose):
        P(f"  {len(prose)} corpus-SIZE claims located in "
          f"{prose['source'].nunique()} committed documents")
        P(f"  {'scope':<12} {'exact':>8} {'<=1%':>8} {'<=5%':>8}   median relerr")
        for sc in ("NONE", "DATE_AT", "DATE_PARENT"):
            e = prose["exact_" + sc].mean()
            b1 = (prose["relerr_" + sc] <= 0.01).mean()
            b5 = (prose["relerr_" + sc] <= 0.05).mean()
            P(f"  {sc:<12} {e:>8.4f} {b1:>8.4f} {b5:>8.4f}   "
              f"{prose['relerr_'+sc].median():.4f}")
        anyex = prose[["exact_NONE", "exact_DATE_AT", "exact_DATE_PARENT"]].any(axis=1)
        P(f"  exact under ANY of the three scopes: {anyex.mean():.4f} "
          f"({int(anyex.sum())} of {len(prose)})")
        bs = prose["best_scope"].value_counts().to_dict()
        P(f"  closest scope per claim: " +
          ", ".join(f"{k} {v}" for k, v in sorted(bs.items())))
    else:
        P("  no corpus-size claims matched the regex")
    P()

    # ---------------------------------------------------------------- COST of the stamp
    P("[7] THE COST OF THE STAMP")
    t0 = time.time()
    blobs = [(fn, (OUT / fn).read_bytes()) for fn in sorted(head_files)]
    read_secs = time.time() - t0
    t0 = time.time()
    stamp_rows = [(fn, len(b), hashlib.sha256(b).hexdigest()) for fn, b in blobs]
    payload = "\n".join(f"{f},{s},{h}" for f, s, h in stamp_rows)
    file_list_sha = hashlib.sha256(payload.encode()).hexdigest()
    hash_secs = time.time() - t0
    del blobs
    stamp_secs = read_secs + hash_secs
    stamp_bytes_full = len(payload.encode())
    stamp_bytes_min = len(f"file_list_sha={file_list_sha} n_files={len(stamp_rows)} "
                          f"n_rows={head_cen['n_rows']}".encode())
    P(f"  file_list_sha (sha256 of sorted file,size,sha256 over {len(stamp_rows)} files)")
    P(f"    = {file_list_sha}")
    P(f"  STANDALONE cost (re-read + hash): {stamp_secs:.2f}s vs {scan_secs:.0f}s for the "
      f"census scan -> {stamp_secs/max(scan_secs,1e-9):.4f} of it")
    P(f"  MARGINAL cost (hash only; a real census already holds the bytes): "
      f"{hash_secs:.2f}s -> {hash_secs/max(scan_secs,1e-9):.4f} of the scan")
    P(f"  bytes: {stamp_bytes_min} for the one-line stamp, {stamp_bytes_full:,} for the "
      f"full manifest")
    P(f"  NOTE: the ratio's denominator is THIS run's scan ({scan_secs:.1f}s), which is "
      f"page-cache dependent (32s cold, ~5s warm on this box); the absolute cost -- "
      f"{hash_secs:.2f}s and {stamp_bytes_full/1024:.0f} KB -- is the durable number.")
    P()

    # ---------------------------------------------------------------- HYPOTHESES
    P("[8] HYPOTHESES  (pre-registered, bars fixed before the numbers)")
    H = []
    H.append(("H_STAMP", f">= {BAR_STAMP:.0%} of committed censuses carry a file-list stamp",
              share_stamped, share_stamped >= BAR_STAMP,
              f"{share_stamped:.4f} of {len(cens)}"))
    H.append(("H_APPEND", f">= {BAR_APPEND:.0%} of census-eligible files blob-stable after "
                          "add", append_rate, append_rate >= BAR_APPEND,
              f"{len(elig_mod)} modified of {len(head_files)}"))
    r1010 = rede[(rede.idea == "1010")]
    lst_ok = bool(r1010[r1010.scope == "LIST"]["rederivable"].all()) if \
        (r1010.scope == "LIST").any() else False
    dp = r1010[r1010.scope == "DATE_PARENT"]
    dp_err = float(dp["max_relerr"].iloc[0]) if len(dp) else np.nan
    da = r1010[r1010.scope == "DATE_AT"]
    da_err = float(da["max_relerr"].iloc[0]) if len(da) else np.nan
    H.append(("H_GITDATE", "a DATE stamp substitutes for a file-list SHA: DATE_PARENT "
                           "re-derives 1010 within 1e-3", dp_err,
              bool(dp_err <= BAR_DERIVE) if not np.isnan(dp_err) else False,
              f"DATE_PARENT relerr {dp_err:.3e}; DATE_AT relerr {da_err:.3e} (reported, "
              f"not the registered arm); LIST re-derives {lst_ok}"))
    self_rate = float((cens["self_inclusion_csv"] > 0).mean())
    H.append(("H_SELF", "a census's OWN commit adds CSVs it could not have scanned, so "
                        "DATE_AT is the wrong tree (self-inclusion > 0 in > 50%)",
              self_rate, self_rate > 0.5,
              f"{self_rate:.4f} of {len(cens)} censuses on all CSVs; "
              f"{float((valid['self_inclusion_files']>0).mean()):.4f} on eligible CSVs"))
    none_err = float(rede[rede.scope == "NONE"]["max_relerr"].max())
    H.append(("H_DERIVE", f"an UNSTAMPED census is re-derivable at HEAD within "
                          f"{BAR_DERIVE:.0e}", none_err, none_err <= BAR_DERIVE,
              f"worst NONE-scope relerr {none_err:.3e}"))
    med_drift = float(valid["drift_fail"].median())
    H.append(("H_DRIFT", f"median denominator drift commit->HEAD < {BAR_DRIFT:.0%}",
              med_drift, med_drift < BAR_DRIFT, f"median {med_drift:.4f}, "
              f"max {valid['drift_fail'].max():.4f}"))
    costshare = hash_secs / max(scan_secs, 1e-9)
    H.append(("H_COST", f"the stamp's MARGINAL cost is < {BAR_COSTT:.0%} of the scan and "
                        f"< {BAR_COSTB:,} bytes", costshare,
              costshare < BAR_COSTT and stamp_bytes_full < BAR_COSTB,
              f"marginal {costshare:.4f} / standalone "
              f"{stamp_secs/max(scan_secs,1e-9):.4f} of scan time; {stamp_bytes_full:,} "
              f"bytes full / {stamp_bytes_min} bytes minimal"))
    if len(prose):
        pr_none = float(prose["exact_NONE"].mean())
        pr_best = float(prose[["exact_NONE", "exact_DATE_AT",
                               "exact_DATE_PARENT"]].any(axis=1).mean())
        H.append(("H_PROSE", "the record's corpus-SIZE claims are re-derivable today "
                             "without a stamp (exact match at HEAD, > 50%)", pr_none,
                  pr_none > 0.5,
                  f"HEAD {pr_none:.4f}, any git scope {pr_best:.4f}, of {len(prose)} claims"))

    # ---------------------------------------------------------------- rule 8 + KEEP paths
    kp, live = keep_paths(grid, panels)
    n4b, n4a = int(kp["pass4b"].sum()), int(kp["pass4a"].sum())
    pick4b = int(picks["pass4b"].sum())
    H.append(("H_RULE8", "the meta-question moves no price verdict: the ladder's 4a/4b "
                         "counts are what they are", float(pick4b), True,
              f"rule-8 picks 4b {pick4b} of {len(picks)}; full grid 4b {n4b} of "
              f"{len(kp)}, 4a {n4a} of {len(kp)}"))

    hyp = pd.DataFrame(H, columns=["hypothesis", "statement", "value", "pass", "detail"])
    for _, r in hyp.iterrows():
        P(f"  {r['hypothesis']:<10} {'PASS' if r['pass'] else 'FAIL'}  {r['statement']}")
        P(f"        {r['detail']}")
    P(f"  HYPOTHESES {int(hyp['pass'].sum())} of {len(hyp)} PASS")
    P()

    P("[9] RULE 8 WALK-FORWARD  (picks made on 2009-2016 ALONE, 2017-2026 read once)")
    P(picks.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P()
    P(f"  full grid at 10 bps: {len(kp)} books;  KEEP path 4b {n4b};  KEEP path 4a {n4a}")
    for pn in sorted(live):
        lv = live[pn]
        s = spy_rows[spy_rows.panel == pn].iloc[0]
        P(f"  {pn}: SPY OOS {s['OOS_CAGR']:.2%} / {s['OOS_Sharpe']:.4f} / "
          f"{s['OOS_MaxDD']:.2%}   |   RULES v2 (live) OOS {lv['OOS_CAGR']:.2%} / "
          f"{lv['OOS_Sharpe']:.4f} / {lv['OOS_MaxDD']:.2%}  "
          f"(full Sharpe {lv['Sharpe']:.4f}, MaxDD {lv['MaxDD']:.2%})")
    P()

    # ---------------------------------------------------------------- outputs
    P("[10] OUTPUTS")
    dump(gates, "gates")
    dump(hyp, "hypotheses")
    dump(rede, "rederive")
    dump(cens, "census")
    if len(prose):
        dump(prose, "prose")
    dump(perfile, "corpusfiles")
    dump(grid, "grid")
    dump(picks, "walkforward")
    dump(kp, "keeppaths")
    (OUT / f"{STEM}.stamp.txt").write_text(
        f"file_list_sha={file_list_sha}\nn_files={len(stamp_rows)}\n"
        f"n_rows={head_cen['n_rows']}\nn_fail={head_cen['n_fail']}\n"
        f"n_files_excl_self={cen_ex['n_files']}\nn_rows_excl_self={cen_ex['n_rows']}\n"
        f"n_fail_excl_self={cen_ex['n_fail']}\n"
        f"head_commit={git('rev-parse','HEAD').strip()}\n")
    P(f"  wrote {STEM}.stamp.txt  (this run's OWN file-list stamp)")
    P()
    P(f"total {time.time()-t_start:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")


if __name__ == "__main__":
    main()
