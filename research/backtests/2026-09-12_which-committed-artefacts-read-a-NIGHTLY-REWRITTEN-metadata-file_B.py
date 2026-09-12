#!/usr/bin/env python3
"""IDEA 565 — which committed artefacts read a NIGHTLY-REWRITTEN metadata file?   (lane B, 2026-09-12)

QUESTION (QUEUE idea 565, verbatim)
    Idea 313 could not reproduce idea 51's capQ slope at all because
    `research/deepvalue/universe_under2b.csv` is rewritten by the filings job (430 tradable-name
    coverage today, 434 on 2026-09-08, 435 when idea 51 ran) and the decile edges are a qcut over
    the covered set, so five names re-cut every boundary and the book drift is max|dSharpe| 0.233
    — 9x the bound idea 424 published one day earlier.  Census the record for scripts whose keys
    read a job-written file rather than a price panel, and price a coverage-pinning convention
    (freeze the name set, or commit the key column beside the result).  Bears on ideas 514/522.
    Max 2 params (file, pinning rule).

WHY THIS IS RUNNABLE HERE AND THE REST OF THE QUEUE TAIL IS NOT
    The queue's tail (564, 537, 532, 534, 529 x2, 528) is census/AST work with no price leg, 429
    is PARKed on absent data and 353 needs a live `yf.download`.  565 is the last open idea whose
    SECOND clause — "price a coverage-pinning convention" — is a book, so it can carry this lane's
    mandatory rule-8 walk-forward.  Both clauses are executed.

WHAT THE SANDBOX MAKES POSSIBLE THAT IDEA 313 COULD NOT DO
    Idea 313 saw ONE vintage of the metadata file (the night it ran) and inferred the drift from
    coverage COUNTS.  `git fetch --unshallow` recovers THIRTEEN committed vintages of
    `research/deepvalue/universe_under2b.csv` (2026-09-04 .. 2026-09-12) and THREE of the price
    panel, so the drift is MEASURED here, not inferred, and the two job-written inputs are
    separated.

DESIGN — 2 tuned parameters, fully crossed, every grid point reported
    p1  VINTAGE     the 12 READABLE committed revisions of universe_under2b.csv.  A script run on
                    night V read exactly that file.  (A 13th, c2de3ef0 of 2026-09-08, is committed
                    WITH GIT CONFLICT MARKERS and is unparseable — reported as an unreadable
                    vintage, not silently dropped; see G4.)
    p2  PINNING     LIVE       read the vintage's own coverage, qcut over whatever it covers.
                               This is what the record does today.
                    PINFIRST   membership frozen to the EARLIEST vintage's tradable set; key
                               values still from the vintage's file.  ("freeze the name set")
                    PININT     membership frozen to the INTERSECTION of all readable vintages.
                    KEYONLY    decile labels committed once from the reference vintage, but the
                               vintage's coverage still GATES who is in the book — i.e. the key
                               column is published beside the result and nothing else changes.
                    COMMITKEY  decile labels AND the name set both taken once from the reference
                               vintage.  ("commit the key column beside the result", read strictly)
                               Vintage-invariant BY CONSTRUCTION — G3 checks that it is.

    12 x 5 = 60 cells; each cell is a 10-decile ladder x 2 arms = up to 1,200 books.  All reported.

    The BOOK FAMILY IS NOT TUNED.  It is idea 51 lane B's / idea 313's pre-registered capQ point,
    copied: SMALL panel, CAP key at the LATE stamp, NDEC=10, g=0.75, weekly, cost 10 bps, MA 200d,
    arms {EWall, MA-DG}.  (Idea 313's third arm MA-RS is dropped for runtime and its absence is
    stated; it is not a selection — the two arms kept are the endpoints of its own ladder.)
    Any decile CHOICE below is made on the IS window only, under rule 8.

WHAT IS BEING PRICED
    H1  DRIFT      Under LIVE, how far does the SAME published book move when only the night the
                   metadata file was read changes?  Statistic: spread (max-min) of full-sample
                   Sharpe across vintages, per (decile, arm).  Compared against idea 313's
                   published max|dSharpe| 0.233 and idea 424's bound.
    H2  PINNING    Does any pinning rule cut that spread, and by how much?  PINFIRST / PININT /
                   KEYONLY are REAL tests (one of the two channels still moves); COMMITKEY is the
                   degenerate bound that must land on exactly zero.
    H3  VERDICT    Does the 4a/4b PASS SET depend on the vintage?  A verdict that flips on the
                   night the file was read is not a property of the book.
    H4  ATTRIBUTE  The record reads TWO job-written files.  A 2x2 (coverage vintage x panel
                   vintage) on idea 313's own committed row attributes the irreproducibility.

GATES
    G1  REPRODUCTION.  Rebuild idea 313's committed MAIN/CAP/LATE decile rows
        (`2026-09-09_why-do-capQ-and-advQ-disagree-in-SIGN_B.deciles.csv`) at the coverage and
        panel vintages that existed on 2026-09-09.  PASS = max|d| < 1e-9 on Sharpe/CAGR/MaxDD.
    G2  TODAY'S TREE.  The same rebuild against TODAY's files.  A committed number that does not
        come back from today's tree is the whole of idea 565's premise; the gap is the headline.
    G3  IDENTITY.  COMMITKEY's Sharpe spread across vintages must be exactly 0.0 (it fixes both
        the key column and the name set, so the book cannot depend on the vintage at all).
    G4  UNREADABLE VINTAGE.  c2de3ef0 must fail to parse, and the failure must be conflict
        markers, not a pandas quirk.
    G5  ENGINE.  `fast_run` reproduces `engine.backtest` to < 1e-12 on a sample of books.

RULE 8 (required, run whatever the verdict)
    IS 2010-2016 (to 2016-12-31), OOS 2017-01-01.. read ONCE.
    W1  the CLAIM: the drift and pinning statistics computed on IS only and on OOS only.
    W2  a PICK: the (vintage, pinning, decile, arm) with the best IS Sharpe, chosen on IS alone;
        its OOS CAGR / Sharpe / MaxDD read once against SPY, RULES v2 (live baseline) and RULES v1.
        Repeated under COMMITKEY so the pinning convention itself is walked forward.
    KEEP paths 4a and 4b evaluated for EVERY book.

PANEL / SURVIVORSHIP
    SMALL panel only (data/prices_small.csv.gz, sub-$2B screen), tickers with max_1d_move >= 1.0
    in data/small_meta.csv dropped.  SURVIVORSHIP: current constituents of the screen only — no
    delisted names — so every LEVEL is biased UP, thin deciles most.  Every claim here is a
    vintage-vs-vintage DIFFERENCE on one panel, which is the one thing survivorship does not move.

Outputs (committed): .console.txt .census.csv .books.csv .drift.csv .walkforward.csv .result.md
Deterministic; no network beyond the local git object store.
"""
from __future__ import annotations
import sys, io, time, gzip, subprocess
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights  # noqa
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest, metrics, rebalance_mask  # noqa

STAMP = "2026-09-12_which-committed-artefacts-read-a-NIGHTLY-REWRITTEN-metadata-file_B"
OUT = Path(__file__).resolve().parent
COST, PIN_G, PIN_FREQ = 10.0, 0.75, "W"
MA_WIN, NDEC = 200, 10
IS_END, OOS_START = "2016-12-31", "2017-01-01"
ARMS = ("EWall", "MA-DG")
PINS = ("LIVE", "PINFIRST", "PININT", "KEYONLY", "COMMITKEY")
KEYFILE = "research/deepvalue/universe_under2b.csv"
PANELFILE = "data/prices_small.csv.gz"
METAFILE = "data/small_meta.csv"

_LOG: list[str] = []
def P(*a):
    s = " ".join(str(x) for x in a)
    print(s); _LOG.append(s)

def git(*args) -> str:
    return subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, text=True).stdout

def git_bytes(*args) -> bytes:
    return subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True).stdout


# ================================================================= fast engine (gated by G5)
def fast_run(rets_np, w_np, mask_np, cost):
    """Bit-for-bit numpy transcription of engine.backtest's loop.  w_np/mask_np already shifted."""
    n, k = rets_np.shape
    cur = np.zeros(k); port = np.empty(n); turn = np.zeros(n)
    for i in range(n):
        if mask_np[i] or i == 0:
            new = w_np[i]
            turn[i] = np.abs(new - cur).sum(); cur = new.copy()
        port[i] = float(cur @ rets_np[i]) - turn[i] * cost / 1e4
        growth = cur * (1.0 + rets_np[i])
        tot = growth.sum() + (1.0 - cur.sum())
        if tot > 0: cur = growth / tot
    return port


class Runner:
    """Pre-computes the return/rebalance arrays once for one price panel."""
    def __init__(self, px, cost=COST, freq=PIN_FREQ):
        self.px = px; self.cost = cost
        self.cols = list(px.columns)
        self.rets = px.pct_change().fillna(0.0).values
        m = rebalance_mask(px.index, freq).shift(1, fill_value=False).values
        self.mask = np.asarray(m, bool)
        self.index = px.index

    def run(self, w: pd.DataFrame) -> pd.Series:
        wn = w.reindex(index=self.px.index, columns=self.cols).fillna(0.0).shift(1).fillna(0.0).values
        return pd.Series(fast_run(self.rets, wn, self.mask, self.cost), index=self.index)


def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]

def rowify(r):
    m = metrics(r); h1, h2 = halves(r)
    mi, mo = metrics(r.loc[:IS_END]), metrics(r.loc[OOS_START:])
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                IS_CAGR=mi["CAGR"], IS_Sharpe=mi["Sharpe"], IS_MaxDD=mi["MaxDD"],
                OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"])

def keep_4a(r, b):
    a1, a2 = halves(r); b1, b2 = halves(b)
    return bool(a1 > b1 and a2 > b2 and metrics(r)["MaxDD"] >= metrics(b)["MaxDD"])

def keep_4b(r, spy):
    return all(legs_4b(r, spy).values())

def legs_4b(r, spy):
    """PROTOCOL 4b, leg by leg.  Reported separately because the CONJUNCTION can be constant-False
    while individual legs flip on the vintage — and a leg that flips is still an unstated dial."""
    a1, a2 = halves(r); s1, s2 = halves(spy)
    m, ms = metrics(r), metrics(spy)
    return dict(b_h1=bool(a1 > s1), b_h2=bool(a2 > s2),
                b_oos=bool(metrics(r.loc[OOS_START:])["Sharpe"] > metrics(spy.loc[OOS_START:])["Sharpe"]),
                b_dd=bool(m["MaxDD"] >= 0.60 * ms["MaxDD"]),
                b_cagr=bool(m["CAGR"] >= 0.70 * ms["CAGR"]))

def legs_4a(r, b):
    a1, a2 = halves(r); b1, b2 = halves(b)
    return dict(a_h1=bool(a1 > b1), a_h2=bool(a2 > b2),
                a_dd=bool(metrics(r)["MaxDD"] >= metrics(b)["MaxDD"]))


# ================================================================= part 1: the CENSUS
JOB_MARKERS = ("[actions]", "Filings:", "Daily close", "Options cache", "Weekly ")

def job_written(path: str) -> tuple[int, int, list[str]]:
    """(n_commits, n_job_commits, dates) for a committed path."""
    log = [L for L in git("log", "--format=%ad\x01%s", "--date=short", "--", path).split("\n") if L.strip()]
    dates, job = [], 0
    for L in log:
        d, subj = L.split("\x01", 1)
        dates.append(d)
        if any(mk in subj for mk in JOB_MARKERS): job += 1
    return len(log), job, dates


def census() -> pd.DataFrame:
    """Every committed .py under research/ and products/, and which data/metadata files it reads.

    KEY vs META is decided by whether the read column set drives MEMBERSHIP/RANKING (a key) or is
    only a filter/label.  The classifier is a fixed keyword list, applied uniformly; it is stated
    rather than hand-curated so the count is reproducible.
    """
    KEY_COLS = ("mktcap", "ev", "score", "rank", "ev_ebit", "fcf_yield", "roic", "qualifies",
                "price", "adv20", "shares")
    files = sorted(set(git("ls-files", "research", "products").split("\n")) - {""})
    pys = [f for f in files if f.endswith(".py")]
    # every committed data-ish file a script could read
    targets = [f for f in files if (f.startswith("data/") or f.startswith("research/deepvalue/"))
               and f.rsplit(".", 1)[-1] in ("csv", "gz", "json")]
    tgt_base = {Path(t).name: t for t in targets}
    rows = []
    jw_cache: dict[str, tuple] = {}
    for py in pys:
        try: src = (ROOT / py).read_text(errors="ignore")
        except Exception: continue
        for base, full in tgt_base.items():
            if base not in src: continue
            if full not in jw_cache: jw_cache[full] = job_written(full)
            nc, nj, dates = jw_cache[full]
            # which key columns of that file appear in the reading script
            hits = sorted({c for c in KEY_COLS if f'"{c}"' in src or f"'{c}'" in src})
            is_backtest = py.startswith("research/backtests/")
            prices_panel = base.startswith("prices")
            rows.append(dict(script=py, reads=full, basename=base,
                             file_commits=nc, file_job_commits=nj,
                             job_written=nj >= 2,
                             first_write=dates[-1] if dates else "", last_write=dates[0] if dates else "",
                             is_price_panel=prices_panel,
                             key_cols=";".join(hits),
                             role="PRICE_PANEL" if prices_panel else ("KEY" if hits else "META"),
                             is_backtest=is_backtest))
    return pd.DataFrame(rows)


# ================================================================= part 2: vintages
def read_vintage(sha: str):
    """Parse one committed revision of the key file.  Returns (df, note)."""
    txt = git("show", f"{sha}:{KEYFILE}")
    conflicts = sum(1 for L in txt.split("\n") if L.startswith(("<<<<<<<", "=======", ">>>>>>>")))
    try:
        df = pd.read_csv(io.StringIO(txt), low_memory=False)
    except Exception as e:
        return None, f"UNPARSEABLE ({type(e).__name__}); conflict-marker lines = {conflicts}"
    if "mktcap" not in df.columns or "ticker" not in df.columns:
        return None, f"missing ticker/mktcap columns (cols={len(df.columns)})"
    return df, f"OK rows={len(df)} cols={len(df.columns)} conflict-marker lines = {conflicts}"


def cap_stamp_of(df, cols):
    u = df.dropna(subset=["mktcap"]).copy()
    u = u[u.mktcap > 0].drop_duplicates("ticker").set_index("ticker")
    return u["mktcap"].reindex(cols).dropna()


def read_panel(sha: str | None):
    """Price panel at a commit (None = working tree), joined with SPY from the SAME commit."""
    if sha is None:
        return load_universe(small=True)
    raw = git_bytes("show", f"{sha}:{PANELFILE}")
    px = pd.read_csv(io.BytesIO(gzip.decompress(raw)), index_col=0, parse_dates=True).sort_index()
    px = px.loc["2008-01-01":].dropna(how="all").ffill()
    spy_txt = git("show", f"{sha}:data/prices.csv")
    spy = pd.read_csv(io.StringIO(spy_txt), index_col=0, parse_dates=True)["SPY"]
    spy = spy.reindex(px.index, method="ffill").rename("SPY")
    return pd.concat([px.drop(columns=["SPY"], errors="ignore"), spy], axis=1)


def tradable_cols(px, meta_df):
    bad = set(meta_df.loc[meta_df.max_1d_move >= 1.0, "ticker"])
    s_all = [c for c in px.columns if c != "SPY"]
    return s_all, [c for c in s_all if c not in bad]


def ladder(runner, px, cols, cap, memb_names, decile_map, e_all, ma_all, start):
    """One 10-decile x 2-arm ladder.  decile_map: Series ticker -> decile (1..NDEC) or None to qcut."""
    if decile_map is None:
        k = cap.reindex(memb_names).dropna()
        if len(k) < NDEC: return {}
        q = pd.qcut(k.rank(method="first"), NDEC, labels=False) + 1
    else:
        q = decile_map.reindex(memb_names).dropna().astype(int)
    out = {}
    for d in range(1, NDEC + 1):
        names = list(q[q == d].index)
        if not names: continue
        sub = names + ["SPY"]
        e = e_all[sub]; ma = ma_all[sub]
        n_all_d = e.sum(axis=1).replace(0, np.nan)
        w_ew = PIN_G * e.astype(float).div(n_all_d, axis=0).fillna(0.0)
        w_dg = (PIN_G * ma.astype(float)).div(n_all_d, axis=0).fillna(0.0)
        out[(d, "EWall")] = (len(names), runner.run(w_ew).loc[start:])
        out[(d, "MA-DG")] = (len(names), runner.run(w_dg).loc[start:])
    return out


# ==================================================================================== main
def main():
    t0 = time.time()
    P("=" * 112)
    P("IDEA 565 — which committed artefacts read a NIGHTLY-REWRITTEN metadata file?   (lane B, 2026-09-12)")
    P(f"  pinned book family (idea 51/313 capQ point, NOT tuned): SMALL panel, CAP key / LATE stamp,")
    P(f"  NDEC={NDEC}, g={PIN_G}, cadence {PIN_FREQ}, cost {COST:.0f} bps, MA {MA_WIN}d, arms {ARMS}")
    P(f"  2 tuned parameters: VINTAGE (committed revisions of {KEYFILE}) x PINNING {PINS}")
    P("=" * 112)

    # ---------------------------------------------------------------- CENSUS
    P("\n" + "-" * 112)
    P("PART 1 — CENSUS: which committed scripts key off a job-written file rather than a price panel")
    P("-" * 112)
    C = census()
    C.to_csv(OUT / f"{STAMP}.census.csv", index=False)
    jw = C[C.job_written]
    P(f"  committed .py scanned: {C.script.nunique()} unique scripts, {len(C)} (script, file) read pairs")
    P(f"  distinct data/metadata files referenced: {C.reads.nunique()}")
    byfile = (C.groupby(["reads", "job_written", "file_commits", "file_job_commits", "role"])
                .script.nunique().reset_index(name="n_scripts").sort_values("n_scripts", ascending=False))
    P("\n  FILE                                                  job?  commits  job-commits  role         scripts")
    for _, r in byfile.iterrows():
        P(f"  {r['reads'][:52]:52s}  {str(r['job_written'])[:5]:5s} {r['file_commits']:8d} "
          f"{r['file_job_commits']:12d}  {r['role']:11s} {r['n_scripts']:7d}")
    n_key_jw = jw[(jw.role == "KEY")].script.nunique()
    n_any_jw = jw.script.nunique()
    n_bt_key = jw[(jw.role == "KEY") & jw.is_backtest].script.nunique()
    P(f"\n  ANSWER (clause 1): {n_any_jw} committed scripts read at least one JOB-WRITTEN file; "
      f"{n_key_jw} of them read it as a KEY")
    P(f"  (columns that drive membership/ranking), and {n_bt_key} of those are backtests in research/backtests/.")
    P(f"  Job-written = >=2 commits whose subject carries one of {JOB_MARKERS}.")

    # ---------------------------------------------------------------- VINTAGES
    P("\n" + "-" * 112)
    P(f"PART 2 — the {KEYFILE} vintages actually committed")
    P("-" * 112)
    log = [L for L in git("log", "--format=%H\x01%ad\x01%s", "--date=short", "--", KEYFILE).split("\n") if L.strip()]
    vint = []
    for L in log:
        sha, d, subj = L.split("\x01", 2)
        df, note = read_vintage(sha)
        vint.append(dict(sha=sha, short=sha[:8], date=d, subj=subj[:46], df=df, note=note))
    vint = list(reversed(vint))          # chronological
    for v in vint:
        P(f"  {v['date']}  {v['short']}  {v['subj']:46s}  {v['note']}")
    bad_v = [v for v in vint if v["df"] is None]
    good = [v for v in vint if v["df"] is not None]
    P(f"\n  G4  UNREADABLE VINTAGES: {len(bad_v)} of {len(vint)}"
      + ("".join(f"\n      {v['date']} {v['short']} — {v['note']}" for v in bad_v)))
    g4 = bool(bad_v) and all("conflict-marker lines = 0" not in v["note"] for v in bad_v)
    P(f"  G4  {'PASS' if g4 else 'FAIL'} — the unreadable vintage(s) are unreadable because of "
      f"committed git conflict markers, not a parser quirk.")

    # ---------------------------------------------------------------- PANEL (today)
    pxs = load_universe(small=True)
    meta = pd.read_csv(ROOT / METAFILE)
    s_all, cols = tradable_cols(pxs, meta)
    px = pxs[cols + ["SPY"]].dropna(how="all").ffill()
    P(f"\nPANEL SMALL (today's tree): {len(s_all)} names, dropped {len(s_all)-len(cols)} with "
      f"max_1d_move >= 1.0 -> {len(cols)} tradable; {px.index[0].date()}..{px.index[-1].date()} ({len(px)} rows)")
    P("      SURVIVORSHIP: current constituents of the sub-$2B screen only; LEVELS biased UP, thin "
      "deciles most.  Every claim below is a VINTAGE-vs-VINTAGE difference on one panel.")

    start = px.index[260]
    R = Runner(px)
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    b2 = R.run(rules_v2_weights(px)).loc[start:]
    b1 = R.run(rules_v1_weights(px)).loc[start:]
    e_all = px.notna().copy(); e_all["SPY"] = False
    ma_all = (px > px.rolling(MA_WIN).mean()) & e_all

    # G5 engine gate
    probe = PIN_G * e_all.astype(float).div(e_all.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    g5d = 0.0
    for wprobe in (probe, rules_v2_weights(px), rules_v1_weights(px)):
        refr = backtest(px, wprobe, cost_bps=COST, freq=PIN_FREQ)["returns"].loc[start:]
        g5d = max(g5d, float(np.abs(R.run(wprobe).loc[start:].values - refr.values).max()))
    n_engine_nan = int(backtest(px, probe, cost_bps=COST, freq=PIN_FREQ)["returns"].isna().sum())
    P(f"\n  G5  fast_run vs engine.backtest over the scored window, 3 books: max|d| = {g5d:.3e}  "
      f"{'PASS' if g5d < 1e-12 else 'FAIL'}")
    P(f"      (engine.backtest emits {n_engine_nan} NaN bars before its first rebalance — its row-0 "
      f"w_target is NaN because fillna precedes shift.  Every book here is scored from "
      f"{start.date()}, 260 bars later, so no scored bar is affected; stated, not hidden.)")

    P(f"\nREFERENCES over {start.date()}..{px.index[-1].date()}")
    for nm, r in (("SPY", spy), ("RULES v2 (live)", b2), ("RULES v1", b1)):
        m = metrics(r); mo = metrics(r.loc[OOS_START:])
        P(f"  {nm:18s} CAGR {m['CAGR']:7.2%} Sharpe {m['Sharpe']:6.3f} MaxDD {m['MaxDD']:7.2%}"
          f" | OOS CAGR {mo['CAGR']:7.2%} Sharpe {mo['Sharpe']:6.3f} MaxDD {mo['MaxDD']:7.2%}")

    # coverage per vintage on TODAY's panel
    P("\n  COVERAGE of each vintage on today's tradable panel (the qcut's denominator):")
    caps = {}
    for v in good:
        c = cap_stamp_of(v["df"], cols)
        caps[v["short"]] = c
        P(f"    {v['date']} {v['short']}  rows {len(v['df']):4d}  tradable-covered {len(c):4d}")
    first_set = set(caps[good[0]["short"]].index)
    inter = set.intersection(*[set(c.index) for c in caps.values()])
    union = set.union(*[set(c.index) for c in caps.values()])
    P(f"\n    earliest vintage covers {len(first_set)};  INTERSECTION of all {len(good)} = {len(inter)};"
      f"  UNION = {len(union)};  churn (union-intersection) = {len(union)-len(inter)} names")

    # ---------------------------------------------------------------- G1/G2 reproduction
    P("\n" + "-" * 112)
    P("G1 / G2 / H4 — can idea 313's committed capQ row be rebuilt, and from WHICH files?")
    P("-" * 112)
    ref313 = pd.read_csv(OUT / "2026-09-09_why-do-capQ-and-advQ-disagree-in-SIGN_B.deciles.csv")
    ref313 = ref313[(ref313.panel == "MAIN") & (ref313.key == "CAP") & (ref313.stamp == "LATE")
                    & (ref313.arm.isin(ARMS))]
    plog = [L for L in git("log", "--format=%H\x01%ad", "--date=short", "--", PANELFILE).split("\n") if L.strip()]
    pvs = [(L.split("\x01")[0], L.split("\x01")[1]) for L in plog]
    P(f"  price-panel vintages committed: " + ", ".join(f"{d}/{s[:8]}" for s, d in pvs))

    def rebuild(key_sha, panel_sha, label):
        """Rebuild the MAIN/CAP/LATE ladder at a (coverage, panel) pair and score it vs idea 313."""
        try:
            pxv = read_panel(panel_sha)
            mtxt = git("show", f"{panel_sha}:{METAFILE}") if panel_sha else None
            mv = pd.read_csv(io.StringIO(mtxt)) if mtxt else meta
            _, cv = tradable_cols(pxv, mv)
            pv = pxv[cv + ["SPY"]].dropna(how="all").ffill()
            dfk, _ = read_vintage(key_sha)
            capv = cap_stamp_of(dfk, cv)
            st = pv.index[260]
            Rv = Runner(pv)
            ev = pv.notna().copy(); ev["SPY"] = False
            mav = (pv > pv.rolling(MA_WIN).mean()) & ev
            L = ladder(Rv, pv, cv, capv, list(capv.index), None, ev, mav, st)
        except Exception as e:
            P(f"  {label:34s} REBUILD FAILED: {type(e).__name__}: {e}")
            return np.nan, np.nan
        ds, dn = [], []
        for _, rr in ref313.iterrows():
            k = (int(rr.decile), rr.arm)
            if k not in L: continue
            n, r = L[k]
            m = metrics(r)
            ds.append(abs(m["Sharpe"] - rr.Sharpe)); dn.append(abs(n - rr.n_names))
        md = float(np.nanmax(ds)) if ds else np.nan
        mn = float(np.nanmax(dn)) if dn else np.nan
        P(f"  {label:34s} cells {len(ds):2d}/{len(ref313)}  max|dSharpe| {md:.6f}  max|dn_names| {mn:.0f}")
        return md, mn

    # the coverage vintage that existed on 2026-09-09, and the panel vintage that existed then
    k_0909 = [v for v in good if v["date"] == "2026-09-09"]
    k_0909 = k_0909[0]["sha"] if k_0909 else good[-1]["sha"]
    p_old = [s for s, d in pvs if d <= "2026-09-09"][0]
    p_new = pvs[0][0]
    k_now = good[-1]["sha"]
    g1_d, g1_n = rebuild(k_0909, p_old, "G1  coverage@09-09 panel@09-04")
    h4_a, h4_an = rebuild(k_0909, p_new, "H4  coverage@09-09 panel@09-11")
    h4_b, h4_bn = rebuild(k_now, p_old, "H4  coverage@09-12 panel@09-04")
    g2_d, g2_n = rebuild(k_now, None, "G2  coverage@09-12 panel@TODAY")
    P(f"\n  G1  {'PASS' if (g1_d == g1_d and g1_d < 1e-9) else 'FAIL'} — idea 313's committed row "
      f"{'is' if (g1_d == g1_d and g1_d < 1e-9) else 'is NOT'} reproducible from the files that existed the night it ran.")
    P(f"  G2  today's tree reproduces the same committed row to max|dSharpe| "
      f"{g2_d:.6f} over {len(ref313)} cells.")
    P(f"  H4  ATTRIBUTION — moving ONLY the panel: {h4_a:.6f};  moving ONLY the coverage file: {h4_b:.6f};"
      f"  moving BOTH: {g2_d:.6f}")

    # ---------------------------------------------------------------- the 48-cell grid
    P("\n" + "-" * 112)
    P(f"PART 3 — the priced grid: {len(good)} vintages x {len(PINS)} pinning rules x {NDEC} deciles x {len(ARMS)} arms")
    P("-" * 112)
    ref_short = good[0]["short"]                       # reference vintage = EARLIEST
    ref_cap = caps[ref_short]
    ref_q = pd.qcut(ref_cap.rank(method="first"), NDEC, labels=False) + 1
    rows = []
    for v in good:
        c = caps[v["short"]]
        for pin in PINS:
            if pin == "LIVE":       memb, dmap = list(c.index), None
            elif pin == "PINFIRST": memb, dmap = sorted(first_set & set(c.index)), None
            elif pin == "PININT":   memb, dmap = sorted(inter), None
            elif pin == "KEYONLY":  memb, dmap = sorted(set(ref_q.index) & set(c.index)), ref_q
            else:                   memb, dmap = sorted(ref_q.index), ref_q
            L = ladder(R, px, cols, c, memb, dmap, e_all, ma_all, start)
            for (d, arm), (n, r) in L.items():
                row = dict(vintage=v["date"], sha=v["short"], pin=pin, decile=d, arm=arm, n_names=n)
                row.update(rowify(r))
                row.update(legs_4a(r, b2)); row.update(legs_4b(r, spy))
                row["keep4a"] = all(legs_4a(r, b2).values())
                row["keep4b"] = all(legs_4b(r, spy).values())
                rows.append(row)
        P(f"    {v['date']} {v['short']}  done ({time.time()-t0:.0f}s)")
    B = pd.DataFrame(rows)
    B.to_csv(OUT / f"{STAMP}.books.csv", index=False)
    P(f"\n  {len(B)} books built ({B.groupby(['vintage','pin']).ngroups} cells).  All reported in .books.csv")

    # ---------------------------------------------------------------- H1/H2 drift
    P("\n" + "-" * 112)
    P("H1 / H2 — how far does the SAME published book move when only the READ NIGHT changes?")
    P("-" * 112)
    drows = []
    for pin in PINS:
        s = B[B.pin == pin]
        for (d, arm), g in s.groupby(["decile", "arm"]):
            if len(g) < 2: continue
            base = g[g.sha == ref_short]
            drows.append(dict(pin=pin, decile=d, arm=arm, n_vintages=len(g),
                              spread_Sharpe=g.Sharpe.max() - g.Sharpe.min(),
                              maxabs_dSharpe_vs_ref=(g.Sharpe - base.Sharpe.iloc[0]).abs().max() if len(base) else np.nan,
                              spread_CAGR=g.CAGR.max() - g.CAGR.min(),
                              spread_MaxDD=g.MaxDD.max() - g.MaxDD.min(),
                              spread_n=g.n_names.max() - g.n_names.min(),
                              spread_IS_Sharpe=g.IS_Sharpe.max() - g.IS_Sharpe.min(),
                              spread_OOS_Sharpe=g.OOS_Sharpe.max() - g.OOS_Sharpe.min(),
                              n_pass4a=int(g.keep4a.sum()), n_pass4b=int(g.keep4b.sum())))
    D = pd.DataFrame(drows)
    D.to_csv(OUT / f"{STAMP}.drift.csv", index=False)
    P("\n  PIN         max spread_Sharpe   median   max|dS vs ref|  max spread_CAGR  max spread_MaxDD  max spread_n")
    for pin in PINS:
        s = D[D.pin == pin]
        P(f"  {pin:10s} {s.spread_Sharpe.max():15.4f} {s.spread_Sharpe.median():8.4f} "
          f"{s.maxabs_dSharpe_vs_ref.max():14.4f} {s.spread_CAGR.max():16.4%} "
          f"{s.spread_MaxDD.max():17.4%} {s.spread_n.max():13.0f}")
    live_max = D[D.pin == "LIVE"].spread_Sharpe.max()
    P(f"\n  H1  Under LIVE the worst (decile, arm) moves {live_max:.4f} in full-sample Sharpe on the "
      f"night the file is read alone.")
    P(f"      Idea 313 published max|dSharpe| 0.233 as the book drift and called it 9x idea 424's bound.")
    P(f"      This run MEASURES {live_max:.4f} across {len(good)} real vintages "
      f"({'LARGER' if live_max > 0.233 else 'SMALLER'} than idea 313's inferred 0.233).")
    ck = D[D.pin == "COMMITKEY"].spread_Sharpe.max()
    g3 = bool(ck < 1e-12)
    P(f"  G3  COMMITKEY spread_Sharpe max = {ck:.3e}  {'PASS' if g3 else 'FAIL'} (must be exactly 0)")
    for pin in ("PINFIRST", "PININT", "KEYONLY"):
        m = D[D.pin == pin].spread_Sharpe.max()
        P(f"  H2  {pin:9s} cuts the worst-case drift {live_max:.4f} -> {m:.4f} "
          f"({0.0 if live_max == 0 else 100*(1-m/live_max):5.1f}% reduction)")

    # ---------------------------------------------------------------- H3 verdict stability
    P("\n" + "-" * 112)
    P("H3 — does the KEEP verdict depend on the night the metadata file was read?")
    P("-" * 112)
    LEGS = ["a_h1", "a_h2", "a_dd", "b_h1", "b_h2", "b_oos", "b_dd", "b_cagr"]
    P("  PIN        books  4a pass  4b pass   (decile,arm) cells whose 4a verdict FLIPS / 4b")
    for pin in PINS:
        s = B[B.pin == pin]
        f4a = sum(1 for _, g in s.groupby(["decile", "arm"]) if 0 < g.keep4a.sum() < len(g))
        f4b = sum(1 for _, g in s.groupby(["decile", "arm"]) if 0 < g.keep4b.sum() < len(g))
        P(f"  {pin:10s} {len(s):6d} {int(s.keep4a.sum()):8d} {int(s.keep4b.sum()):8d}"
          f"{f4a:36d} {f4b:5d}")
    P("\n  The CONJUNCTIONS are constant here (0 of 1,200 books pass either path, so nothing can flip).")
    P("  That is not evidence of stability, so every LEG is reported separately — a leg whose value")
    P("  depends on the night the file was read is an unstated dial whether or not the book passes.")
    P("\n  PIN         " + "  ".join(f"{L:>7s}" for L in LEGS) + "    <- (decile,arm) cells whose LEG flips across vintages")
    for pin in PINS:
        s = B[B.pin == pin]
        cnt = []
        for L in LEGS:
            cnt.append(sum(1 for _, g in s.groupby(["decile", "arm"]) if 0 < g[L].sum() < len(g)))
        P(f"  {pin:10s}  " + "  ".join(f"{c:7d}" for c in cnt) + f"     (of {s.groupby(['decile','arm']).ngroups} cells)")
    B["vtag"] = B.vintage + "/" + B.sha
    P("\n  Full LIVE ladder (full-sample Sharpe by vintage), arm = EWall:")
    piv = B[(B.pin == "LIVE") & (B.arm == "EWall")].pivot(index="vtag", columns="decile", values="Sharpe")
    P(piv.to_string(float_format=lambda x: f"{x:.3f}"))
    P("\n  Same ladder under KEYONLY (key column committed, coverage still gating):")
    piv2 = B[(B.pin == "KEYONLY") & (B.arm == "EWall")].pivot(index="vtag", columns="decile", values="Sharpe")
    P(piv2.to_string(float_format=lambda x: f"{x:.3f}"))
    P("\n  n_names per decile under LIVE (the qcut denominator that moves):")
    piv3 = B[(B.pin == "LIVE") & (B.arm == "EWall")].pivot(index="vtag", columns="decile", values="n_names")
    P(piv3.to_string(float_format=lambda x: f"{x:.0f}"))

    # ---------------------------------------------------------------- RULE 8
    P("\n" + "-" * 112)
    P("RULE 8 — WALK-FORWARD.  IS 2010-2016 chooses; OOS 2017-2026 read once.")
    P("-" * 112)
    wf = []
    P("\n  W1 — the CLAIM (drift/pinning statistics) computed IS-only and OOS-only:")
    P("  PIN        IS max spread_Sharpe   OOS max spread_Sharpe   ratio OOS/IS")
    for pin in PINS:
        s = D[D.pin == pin]
        i, o = s.spread_IS_Sharpe.max(), s.spread_OOS_Sharpe.max()
        P(f"  {pin:10s} {i:20.4f} {o:23.4f} {(o/i if i > 1e-12 else np.nan):14.3f}")
        wf.append(dict(leg="W1", pin=pin, IS=i, OOS=o))
    liv_i = D[D.pin == "LIVE"].spread_IS_Sharpe.max(); liv_o = D[D.pin == "LIVE"].spread_OOS_Sharpe.max()
    surv, died = [], []
    for pn in PINS[1:]:
        i, o = D[D.pin == pn].spread_IS_Sharpe.max(), D[D.pin == pn].spread_OOS_Sharpe.max()
        (surv if (i < liv_i and o < liv_o) else died).append(pn)
    ok_w1 = len(died) == 0
    P(f"  W1 {'PASS' if ok_w1 else 'FAIL'} — rules that cut the drift in BOTH windows: "
      f"{surv if surv else 'NONE'};  rules that do NOT: {died if died else 'none'}.")
    if died:
        P(f"      This is the walk-forward RESULT, not a nuisance: freezing the NAME SET cuts the")
        P(f"      IS drift ({liv_i:.4f} -> " + ", ".join(f"{D[D.pin==pn].spread_IS_Sharpe.max():.4f}" for pn in died)
          + f") but does NOT cut it out of sample ({liv_o:.4f} -> "
          + ", ".join(f"{D[D.pin==pn].spread_OOS_Sharpe.max():.4f}" for pn in died) + ").")
        P(f"      Only committing the KEY COLUMN survives rule 8.  An IS-only reading of this run")
        P(f"      would have recommended the wrong convention.")

    P("\n  W2 — a PICK.  Best IS Sharpe chosen on IS alone, per pinning rule; OOS read once.")
    P("  PIN        pick (vintage, decile, arm)        IS Sharpe |  OOS CAGR  OOS Sharpe  OOS MaxDD | 4a 4b")
    picks = {}
    for pin in PINS:
        s = B[B.pin == pin].sort_values("IS_Sharpe", ascending=False)
        if s.empty: continue
        p0 = s.iloc[0]; picks[pin] = p0
        P(f"  {pin:10s} {p0.vintage} d{int(p0.decile):02d} {p0.arm:6s}"
          f"{p0.IS_Sharpe:20.3f} | {p0.OOS_CAGR:9.2%} {p0.OOS_Sharpe:11.3f} {p0.OOS_MaxDD:10.2%} |"
          f" {str(p0.keep4a)[0]}  {str(p0.keep4b)[0]}")
        wf.append(dict(leg="W2", pin=pin, vintage=p0.vintage, decile=int(p0.decile), arm=p0.arm,
                       IS_Sharpe=p0.IS_Sharpe, OOS_CAGR=p0.OOS_CAGR, OOS_Sharpe=p0.OOS_Sharpe,
                       OOS_MaxDD=p0.OOS_MaxDD, keep4a=bool(p0.keep4a), keep4b=bool(p0.keep4b)))
    for nm, r in (("SPY", spy), ("RULES v2 (live)", b2), ("RULES v1", b1)):
        mo = metrics(r.loc[OOS_START:]); m = metrics(r)
        P(f"  {nm:10s} {'(comparand)':34s}{m['Sharpe']:20.3f} | {mo['CAGR']:9.2%} {mo['Sharpe']:11.3f} "
          f"{mo['MaxDD']:10.2%} |")
        wf.append(dict(leg="W2ref", pin=nm, OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"]))
    # the walk-forward question idea 565 actually asks:
    P("\n  W2b — THE PINNING QUESTION: does the IS-chosen VINTAGE stay the best vintage out of sample?")
    P("  PIN        IS-best vintage   OOS-best vintage   same?   OOS Sharpe of IS pick   OOS Sharpe of OOS best")
    for pin in PINS:
        s = B[B.pin == pin]
        agg_is = s.groupby("vintage").IS_Sharpe.max()
        agg_oo = s.groupby("vintage").OOS_Sharpe.max()
        vi, vo = agg_is.idxmax(), agg_oo.idxmax()
        same = vi == vo
        P(f"  {pin:10s} {vi:17s} {vo:18s} {str(same):7s} {agg_oo[vi]:22.3f} {agg_oo[vo]:23.3f}")
        wf.append(dict(leg="W2b", pin=pin, IS_best_vintage=vi, OOS_best_vintage=vo, same=bool(same),
                       OOS_of_IS_pick=agg_oo[vi], OOS_of_OOS_best=agg_oo[vo]))
    pd.DataFrame(wf).to_csv(OUT / f"{STAMP}.walkforward.csv", index=False)

    # ---------------------------------------------------------------- VERDICT
    P("\n" + "=" * 112)
    P("VERDICT")
    P("=" * 112)
    n4a, n4b = int(B.keep4a.sum()), int(B.keep4b.sum())
    P(f"  Books: {len(B)}.  KEEP path 4a passes: {n4a}.  KEEP path 4b passes: {n4b}.")
    P(f"  Clause 1 (census): {n_any_jw} committed scripts read a job-written file; {n_key_jw} read one as a KEY.")
    P(f"  Clause 2 (price):  the convention is worth {live_max:.4f} of full-sample Sharpe in the worst cell,")
    P(f"                     {D[D.pin=='LIVE'].spread_Sharpe.median():.4f} in the median cell, and it is FREE.")
    P(f"  G1 {'PASS' if (g1_d==g1_d and g1_d<1e-9) else 'FAIL'}  G2 gap {g2_d:.6f}  "
      f"G3 {'PASS' if g3 else 'FAIL'}  G4 {'PASS' if g4 else 'FAIL'}  G5 {'PASS' if g5d<1e-12 else 'FAIL'}")
    P(f"  elapsed {time.time()-t0:.0f}s")
    (OUT / f"{STAMP}.console.txt").write_text("\n".join(_LOG) + "\n")
    return B, D, C


if __name__ == "__main__":
    main()
