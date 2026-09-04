#!/usr/bin/env python3
"""Research-verdict long/short tracker (idea D1).

The cleanest test of whether the Deep Value Desk's *reading* has information:
go long every IDEA, short every PASS, hedge the net with IWM, and see whether
the spread is positive. WATCH is carried as a third, long-only basket for
information only -- it is not part of the traded book.

Writes research/deepvalue/LS_TRACK.md and research/deepvalue/ls_daily.csv.
Run daily, right after track_picks.py.
"""
import re, datetime as dt
from pathlib import Path
import numpy as np, pandas as pd, yfinance as yf

ROOT = Path(__file__).resolve().parents[2]
DV = ROOT / "research" / "deepvalue"
MD_OUT = DV / "LS_TRACK.md"
CSV_OUT = DV / "ls_daily.csv"

CAP = 0.20            # max weight per name
HOLD_DAYS = 365       # 12 months
COST_BPS = 10.0       # bps per unit of turnover, estimate only (not deducted)
HEDGE = "IWM"
BENCH = ["IWM", "SPY"]

RULES = (
    "**Portfolio rules.** Every IDEA enters the LONG book at the first close on or after its publication date; "
    "every PASS enters the SHORT book the same way. Within each book names are weighted 1/N, where N is the number "
    "of open positions in that book recomputed daily, capped at 20% per name; when N is below 5 the cap binds and the "
    "book is deliberately left partly in cash rather than levered up, so a two-name book runs 40% gross. "
    "A position stays open for 12 months or until a later note changes the verdict on that ticker (detected as a newer "
    "COVERAGE.md row for the same ticker), whichever comes first. The net exposure of the traded book "
    "(long weight minus short weight) is offset with IWM so the combined book is dollar-neutral; the raw long-minus-short "
    "spread is also reported unhedged. WATCH names are excluded from the traded book and carried as a separate long-only "
    "basket, for information only. Returns are price-only on adjusted closes with no costs deducted; an estimate at "
    f"{COST_BPS:.0f} bps per unit of turnover is printed separately. Cash earns 0%."
)


def rows(path, cols):
    out = []
    if not path.exists():
        return out
    for line in path.read_text().splitlines():
        if not line.startswith("| 20"):
            continue
        parts = [p.strip() for p in line.strip("|").split("|")]
        if len(parts) >= len(cols):
            out.append(dict(zip(cols, parts)))
    return out


def bail(msg):
    MD_OUT.write_text(f"# Research-verdict long/short\n\n{RULES}\n\n_{msg}_\n")
    print(msg)
    raise SystemExit(0)


picks = rows(DV / "PICKS.md", ["date", "ticker", "verdict", "conviction", "price", "thesis", "kill", "note"])
cov = rows(DV / "COVERAGE.md", ["date", "ticker", "verdict", "conviction", "price", "line"])
seen = {(r["date"], r["ticker"]) for r in picks}
allrows = picks + [r for r in cov if (r["date"], r["ticker"]) not in seen]
for r in allrows:
    r["verdict"] = r["verdict"].strip().upper()
    r["ts"] = pd.Timestamp(r["date"])
allrows = [r for r in allrows if r["verdict"] in ("IDEA", "PASS", "WATCH")]
if not allrows:
    bail("No published verdicts yet.")

# a newer row for the same ticker supersedes the older one
by_ticker = {}
for r in sorted(allrows, key=lambda x: (x["ticker"], x["ts"])):
    by_ticker.setdefault(r["ticker"], []).append(r)
for tk, rs in by_ticker.items():
    for i, r in enumerate(rs):
        nxt = rs[i + 1]["ts"] if i + 1 < len(rs) else None
        cap_ts = r["ts"] + pd.Timedelta(days=HOLD_DAYS)
        r["exit_target"] = min(nxt, cap_ts) if nxt is not None else cap_ts
        r["superseded"] = nxt is not None and nxt <= cap_ts

tickers = sorted({r["ticker"] for r in allrows} | set(BENCH) | {HEDGE})
start = (min(r["ts"] for r in allrows) - pd.Timedelta(days=5)).strftime("%Y-%m-%d")
raw = yf.download(tickers, start=start, auto_adjust=True, progress=False)
px = raw["Close"] if isinstance(raw.columns, pd.MultiIndex) else raw[["Close"]].rename(columns={"Close": tickers[0]})
px = px.ffill().dropna(how="all")
if px.empty:
    bail("Published verdicts exist but no price data is available yet.")
for b in set(BENCH) | {HEDGE}:
    if b not in px.columns:
        bail(f"Benchmark {b} unavailable from the price source.")

# ---- build positions -------------------------------------------------------
positions = []
for r in allrows:
    t = r["ticker"]
    if t not in px.columns:
        continue
    s = px[t].dropna()
    if s.empty:
        continue
    fwd = s.loc[r["ts"]:]
    if fwd.empty:                       # published after the last available close
        entry = s.index[-1]             # mark at the last close; 0 days of history
        stale = True
    else:
        entry = fwd.index[0]
        stale = False
    ex = s.loc[r["exit_target"]:]
    exit_d = ex.index[0] if len(ex) else pd.Timestamp.max
    if exit_d <= entry:
        continue
    positions.append(dict(ticker=t, verdict=r["verdict"], pub=r["date"], entry=entry,
                          exit=exit_d, stale=stale, superseded=r["superseded"],
                          p0=float(s.loc[entry])))
if not positions:
    bail("Published verdicts exist but none has a tradable entry price yet.")

dates = px.loc[min(p["entry"] for p in positions):].index
LONG = [p for p in positions if p["verdict"] == "IDEA"]
SHORT = [p for p in positions if p["verdict"] == "PASS"]
WATCH = [p for p in positions if p["verdict"] == "WATCH"]


def weights_on(book, day):
    """Target weights held at the close of `day`."""
    open_ = [p for p in book if p["entry"] <= day < p["exit"]]
    if not open_:
        return {}
    w = min(1.0 / len(open_), CAP)
    return {p["ticker"]: w for p in open_}


def book_path(book):
    """Daily returns, gross exposure and turnover for one book."""
    rets, gross, turn = [], [], []
    prev_held = {}
    for i, d in enumerate(dates):
        if i == 0:
            rets.append(0.0)
        else:
            p = dates[i - 1]
            r = sum(w * (px[t].loc[d] / px[t].loc[p] - 1) for t, w in prev_held.items())
            rets.append(float(r))
            # drift previous weights to today's close before rebalancing
            prev_held = {t: w * float(px[t].loc[d] / px[t].loc[p]) for t, w in prev_held.items()}
        tgt = weights_on(book, d)
        turn.append(sum(abs(tgt.get(t, 0.0) - prev_held.get(t, 0.0)) for t in set(tgt) | set(prev_held)))
        gross.append(sum(tgt.values()))
        prev_held = tgt
    return (pd.Series(rets, index=dates), pd.Series(gross, index=dates), pd.Series(turn, index=dates))


lr, lg, lt = book_path(LONG)
sr, sg, st = book_path(SHORT)
wr, wg, wt = book_path(WATCH)
net = (lg - sg)                                   # net exposure held at each close
_ih = (px[HEDGE] / px[HEDGE].shift(1) - 1).reindex(dates).fillna(0.0)
_ih.iloc[0] = 0.0
hedge_leg = -net.shift(1).fillna(0.0) * _ih
spread = lr - sr
hedged = spread + hedge_leg
hedge_turn = net.diff().abs().fillna(net.abs())
turnover = lt + st + hedge_turn

bench_r = {}
for b in BENCH:                       # benchmarks start from the same inception close as the books
    v = (px[b] / px[b].shift(1) - 1).reindex(dates).fillna(0.0)
    v.iloc[0] = 0.0
    bench_r[b] = v
series = {"long": lr, "short": sr, "spread": spread, "hedged": hedged, "watch": wr,
          **{b.lower(): bench_r[b] for b in BENCH}}
cum = {k: (1 + v).cumprod() - 1 for k, v in series.items()}
ndays = len(dates)
enough = ndays >= 20


def stats(k):
    v = series[k]
    tot = float(cum[k].iloc[-1])
    if not enough or v.std() == 0 or len(v) < 2:
        return tot, None, None
    vol = float(v.std(ddof=1) * np.sqrt(252))
    shp = float(v.mean() / v.std(ddof=1) * np.sqrt(252))
    return tot, vol, shp


# ---- per-name ---------------------------------------------------------------
last = dates[-1]
name_rows = []
for p in sorted(positions, key=lambda x: (x["verdict"], x["ticker"])):
    end = min(p["exit"], last) if p["exit"] <= last else last
    end = px.index[px.index.get_indexer([end], method="ffill")[0]]
    p1 = float(px[p["ticker"]].loc[end])
    r = p1 / p["p0"] - 1
    ib = float(px[HEDGE].loc[end] / px[HEDGE].loc[p["entry"]] - 1)
    name_rows.append(dict(ticker=p["ticker"], verdict=p["verdict"], pub=p["pub"],
                          entry=p["entry"].date(), p0=p["p0"], p1=p1, ret=r,
                          iwm=ib, vs=r - ib, stale=p["stale"],
                          closed=p["exit"] <= last, sup=p["superseded"]))
nm = pd.DataFrame(name_rows)
lname, sname = nm[nm.verdict == "IDEA"], nm[nm.verdict == "PASS"]
# a hit rate needs at least one day of post-entry price movement to mean anything
hit_long = float((lname.vs > 0).mean()) if (len(lname) and ndays > 1) else None
hit_short = float((sname.vs < 0).mean()) if (len(sname) and ndays > 1) else None

cost = float(turnover.sum() * COST_BPS / 1e4)
rebals = int((turnover > 1e-9).sum())

# ---- write ------------------------------------------------------------------
def pc(x):
    return "—" if x is None else f"{x:+.2%}"


def n2(x):
    return "—" if x is None else f"{x:.2f}"


sumrows = [("Long book (IDEA)", "long"), ("Short book (PASS)", "short"),
           ("Spread (long − short, unhedged)", "spread"),
           (f"Hedged book (dollar-neutral vs {HEDGE})", "hedged"),
           ("WATCH basket (excluded, long-only)", "watch"),
           ("IWM", "iwm"), ("SPY", "spy")]
tbl = ["| Book | Since-inception return | Ann. vol | Sharpe |", "|---|---|---|---|"]
for label, k in sumrows:
    t, v, s = stats(k)
    tbl.append(f"| {label} | {t:+.2%} | {'—' if v is None else f'{v:.1%}'} | {n2(s)} |")

interp_bits = []
sp = float(cum["spread"].iloc[-1]); hd = float(cum["hedged"].iloc[-1])
if not enough:
    interp = (f"Too early to say: {ndays} trading day{'s' if ndays != 1 else ''} of history and "
              f"{len(LONG)} long / {len(SHORT)} short position{'s' if len(SHORT) != 1 else ''} — "
              f"the spread reads {sp:+.2%} and the hedged book {hd:+.2%}, but neither is statistically meaningful yet.")
else:
    _, _, shp = stats("hedged")
    interp = (f"Over {ndays} trading days the hedged verdict book returned {hd:+.2%} "
              f"(Sharpe {n2(shp)}); longs beat IWM {hit_long:.0%} of the time"
              + (f" and shorts underperformed IWM {hit_short:.0%} of the time." if hit_short is not None
                 else ", with no PASS verdicts published yet to short."))

md = [f"# Research-verdict long/short — updated {dt.date.today()}", "",
      RULES, "",
      "<!--LS_SUMMARY-->",
      f"### Summary — {len(LONG)} long, {len(SHORT)} short, {len(WATCH)} watch · {ndays} trading day"
      + ("s" if ndays != 1 else "") + f" since {dates[0].date()}", ""]
md += tbl
md += ["",
       (f"Hit rate: longs beating IWM since entry {hit_long:.0%} ({int((lname.vs>0).sum())}/{len(lname)}) · "
        f"PASS names underperforming IWM since entry "
        + (f"{hit_short:.0%} ({int((sname.vs<0).sum())}/{len(sname)})." if hit_short is not None else "— (no PASS verdicts yet).")
        if hit_long is not None else
        f"Hit rate: not yet defined — {len(lname)} long and {len(sname)} short name(s), "
        f"{ndays} trading day{'s' if ndays != 1 else ''} of history."), "",
       f"*{interp}*", "", "<!--/LS_SUMMARY-->", ""]
if not enough:
    md += [f"> Annualised vol and Sharpe are suppressed until at least 20 trading days of history exist "
           f"(currently {ndays}). Every number above should be read as a placeholder, not a result.", ""]
md += [f"Estimated trading cost, not deducted above: {turnover.sum():.2f} units of cumulative turnover across "
       f"{rebals} rebalance day{'s' if rebals != 1 else ''} at {COST_BPS:.0f} bps = **{cost:.2%}** of capital.", ""]

md += ["## Positions", "",
       "| Ticker | Verdict | Published | Entry date | Entry | Current | Return | IWM | vs IWM | Status |",
       "|---|---|---|---|---|---|---|---|---|---|"]
for r in nm.itertuples():
    status = "closed (new verdict)" if r.sup and r.closed else ("closed (12m)" if r.closed else
              ("open (marked at last close, no post-publication close yet)" if r.stale else "open"))
    md.append(f"| {r.ticker} | {r.verdict} | {r.pub} | {r.entry} | {r.p0:.2f} | {r.p1:.2f} | "
              f"{r.ret:+.2%} | {r.iwm:+.2%} | {r.vs:+.2%} | {status} |")
md += ["", f"Daily series: [ls_daily.csv](ls_daily.csv) (cumulative since-inception returns, one row per trading day).", ""]
MD_OUT.write_text("\n".join(md))

out = pd.DataFrame({"date": [d.date() for d in dates],
                    "long_ret": cum["long"].values, "short_ret": cum["short"].values,
                    "spread": cum["spread"].values, "hedged": cum["hedged"].values,
                    "iwm": cum["iwm"].values, "spy": cum["spy"].values})
out.to_csv(CSV_OUT, index=False, float_format="%.6f")

print("\n".join(tbl))
print()
print(f"cost estimate @ {COST_BPS:.0f}bps: {cost:.2%} ({rebals} rebalance days, turnover {turnover.sum():.2f})")
print(interp)
print(f"wrote {MD_OUT.name} and {CSV_OUT.name}")
