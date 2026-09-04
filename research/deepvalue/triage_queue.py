#!/usr/bin/env python3
"""Work queue for the triage stage.

Maintains research/deepvalue/TRIAGE_QUEUE.md with three sections: Open,
In progress, Done. Source of tickers is universe_under2b.csv when present,
otherwise candidates.csv.

    python research/deepvalue/triage_queue.py sync
    python research/deepvalue/triage_queue.py status
    python research/deepvalue/triage_queue.py next 5 --lane a
    python research/deepvalue/triage_queue.py done STRT [TICKER ...]
    python research/deepvalue/triage_queue.py reset-stale 6

Concurrency: the whole file is re-read, mutated and rewritten atomically under
an exclusive lock on TRIAGE_QUEUE.md.lock, so parallel lanes can claim work
without stepping on each other, and routines that commit between runs converge.
"""

from __future__ import annotations

import argparse
import fcntl
import math
import os
import re
import sys
import tempfile
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
QUEUE = HERE / "TRIAGE_QUEUE.md"
LOCK = HERE / ".TRIAGE_QUEUE.lock"
UNIVERSE = HERE / "universe_under2b.csv"
CANDIDATES = HERE / "candidates.csv"

OPEN, PROG, DONE = "Open", "In progress", "Done"
SECTIONS = (OPEN, PROG, DONE)
LOCK_TIMEOUT = 30.0


def now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_ts(s: str) -> datetime | None:
    try:
        return datetime.strptime(s.strip(), "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    except (ValueError, AttributeError):
        return None


def money(v) -> str:
    if v is None or v == "" or (isinstance(v, float) and math.isnan(v)):
        return "n/a"
    try:
        a = float(v)
    except (TypeError, ValueError):
        return str(v)
    if a >= 1e9:
        return f"${a/1e9:,.2f}B"
    if a >= 1e6:
        return f"${a/1e6:,.1f}M"
    return f"${a:,.0f}"


# ------------------------------------------------------------------- locking


class FileLock:
    def __init__(self, path: Path, timeout: float = LOCK_TIMEOUT):
        self.path, self.timeout, self.fh = path, timeout, None

    def __enter__(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.fh = open(self.path, "w")
        deadline = time.time() + self.timeout
        while True:
            try:
                fcntl.flock(self.fh, fcntl.LOCK_EX | fcntl.LOCK_NB)
                return self
            except OSError:
                if time.time() > deadline:
                    self.fh.close()
                    raise SystemExit(
                        f"triage_queue: could not lock {self.path} within {self.timeout:.0f}s; "
                        "another lane is mid-write. Retry."
                    )
                time.sleep(0.15)

    def __exit__(self, *exc):
        if self.fh:
            fcntl.flock(self.fh, fcntl.LOCK_UN)
            self.fh.close()


def atomic_write(path: Path, text: str) -> None:
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=".tq-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(text)
        # mkstemp creates 0600; keep the queue readable like any other repo file
        mode = path.stat().st_mode & 0o777 if path.exists() else 0o644
        os.chmod(tmp, mode)
        os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


# ------------------------------------------------------------------ file i/o

ROW = re.compile(r"^\|(?!\s*-)(.+)\|\s*$")


def read_queue() -> dict[str, list[dict]]:
    state = {s: [] for s in SECTIONS}
    if not QUEUE.exists():
        return state
    section = None
    for line in QUEUE.read_text(encoding="utf-8").split("\n"):
        h = re.match(r"^##\s+(.+?)\s*(?:\(|$)", line)
        if h:
            name = h.group(1).strip()
            section = name if name in SECTIONS else None
            continue
        if section is None:
            continue
        m = ROW.match(line.rstrip())
        if not m:
            continue
        cells = [c.strip() for c in m.group(1).split("|")]
        if not cells or cells[0].lower() in ("ticker", "") or set(cells[0]) <= {"-", ":"}:
            continue
        rec = {
            "ticker": cells[0].upper(),
            "name": cells[1] if len(cells) > 1 else "",
            "mktcap": cells[2] if len(cells) > 2 else "",
            "lane": cells[3] if len(cells) > 3 else "",
            "ts": cells[4] if len(cells) > 4 else "",
        }
        state[section].append(rec)
    return state


HEADERS = {
    OPEN: ("| Ticker | Name | Mkt cap |", "|---|---|---|"),
    PROG: (
        "| Ticker | Name | Mkt cap | Lane | Claimed (UTC) |",
        "|---|---|---|---|---|",
    ),
    DONE: ("| Ticker | Name | Mkt cap | Lane | Done (UTC) |", "|---|---|---|---|---|"),
}


def render(state: dict[str, list[dict]], source: str) -> str:
    counts = " · ".join(f"{s.lower()} {len(state[s])}" for s in SECTIONS)
    out = [
        "# Triage queue",
        "",
        f"_Source: {source} · updated {now()} · {counts}_",
        "",
        "Managed by `research/deepvalue/triage_queue.py`. Claim work with "
        "`next N --lane X`, release it with `done TICKER`, recover abandoned claims with "
        "`reset-stale HOURS`. Edit by hand only if no lane is running.",
        "",
    ]
    for s in SECTIONS:
        rows = state[s]
        out.append(f"## {s} ({len(rows)})")
        out.append("")
        head, sep = HEADERS[s]
        out += [head, sep]
        for r in rows:
            if s == OPEN:
                out.append(f"| {r['ticker']} | {r['name']} | {r['mktcap']} |")
            else:
                out.append(
                    f"| {r['ticker']} | {r['name']} | {r['mktcap']} | "
                    f"{r.get('lane') or '-'} | {r.get('ts') or '-'} |"
                )
        out.append("")
    return "\n".join(out).rstrip() + "\n"


# -------------------------------------------------------------------- source


def load_source() -> tuple[list[dict], str]:
    src = UNIVERSE if UNIVERSE.exists() else CANDIDATES
    if not src.exists():
        raise SystemExit(
            f"triage_queue: neither {UNIVERSE.name} nor {CANDIDATES.name} exists. "
            "Run screen.py first."
        )
    try:
        import pandas as pd
    except ImportError:
        raise SystemExit("triage_queue: pandas is required to read the ticker source.")
    df = pd.read_csv(src)
    if "ticker" not in df.columns:
        raise SystemExit(f"triage_queue: {src.name} has no 'ticker' column.")
    if "rank" in df.columns:
        df = df.sort_values("rank")
    elif "score" in df.columns:
        df = df.sort_values("score", ascending=False)
    elif "mktcap" in df.columns:
        df = df.sort_values("mktcap", ascending=False)
    rows, seen = [], set()
    for _, r in df.iterrows():
        t = str(r["ticker"]).strip().upper()
        if not t or t in seen or t == "NAN":
            continue
        seen.add(t)
        rows.append(
            {
                "ticker": t,
                "name": str(r.get("name", "")).strip(),
                "mktcap": money(r.get("mktcap")),
                "lane": "",
                "ts": "",
            }
        )
    return rows, src.name


def sync(state: dict[str, list[dict]], source_rows: list[dict]) -> int:
    known = {r["ticker"] for s in SECTIONS for r in state[s]}
    added = 0
    for r in source_rows:
        if r["ticker"] in known:
            continue
        state[OPEN].append(dict(r))
        known.add(r["ticker"])
        added += 1
    # refresh name/mktcap for rows that were created empty
    by_t = {r["ticker"]: r for r in source_rows}
    for s in SECTIONS:
        for r in state[s]:
            src = by_t.get(r["ticker"])
            if src:
                r["name"] = r["name"] or src["name"]
                r["mktcap"] = r["mktcap"] or src["mktcap"]
    reorder_open(state, source_rows)
    return added


def reorder_open(state: dict[str, list[dict]], source_rows: list[dict]) -> None:
    """Keep Open in source (screen rank) order so every lane sees the same next-up."""
    order = {r["ticker"]: i for i, r in enumerate(source_rows)}
    state[OPEN].sort(key=lambda r: order.get(r["ticker"], len(order)))


def move(state: dict[str, list[dict]], ticker: str, to: str, **fields) -> dict | None:
    rec = None
    for s in SECTIONS:
        for r in list(state[s]):
            if r["ticker"] == ticker:
                state[s].remove(r)
                rec = r if rec is None else rec
    if rec is None:
        return None
    rec.update(fields)
    state[to].append(rec)
    return rec


# ------------------------------------------------------------------ commands


def cmd_sync(args) -> int:
    with FileLock(LOCK):
        state = read_queue()
        rows, src = load_source()
        added = sync(state, rows)
        reorder_open(state, rows)
        atomic_write(QUEUE, render(state, src))
    print(f"synced from {src}: {added} new ticker(s) added to Open; {len(state[OPEN])} open")
    return 0


def cmd_status(args) -> int:
    with FileLock(LOCK):
        state = read_queue()
        rows, src = load_source()
        sync(state, rows)
        reorder_open(state, rows)
        atomic_write(QUEUE, render(state, src))
    print(f"source {src} · open {len(state[OPEN])} · in progress {len(state[PROG])} · "
          f"done {len(state[DONE])}")
    for r in state[PROG]:
        print(f"  in progress: {r['ticker']} lane={r.get('lane') or '-'} since {r.get('ts') or '-'}")
    return 0


def cmd_next(args) -> int:
    n = max(1, int(args.n))
    lane = str(args.lane).strip()
    if not lane:
        print("triage_queue: --lane is required for `next`", file=sys.stderr)
        return 2
    with FileLock(LOCK):
        state = read_queue()
        rows, src = load_source()
        sync(state, rows)
        claimed = []
        stamp = now()
        for r in list(state[OPEN])[:n]:
            state[OPEN].remove(r)
            r = dict(r, lane=lane, ts=stamp)
            state[PROG].append(r)
            claimed.append(r)
        reorder_open(state, rows)
        atomic_write(QUEUE, render(state, src))
    if not claimed:
        print(f"lane {lane}: queue is empty, nothing claimed", file=sys.stderr)
        return 3
    for r in claimed:
        print(r["ticker"])
    print(
        f"lane {lane}: claimed {len(claimed)} of {n} requested · {len(state[OPEN])} still open",
        file=sys.stderr,
    )
    return 0


def cmd_done(args) -> int:
    tickers = [t.strip().upper() for t in args.tickers if t.strip()]
    with FileLock(LOCK):
        state = read_queue()
        rows, src = load_source()
        sync(state, rows)
        ok, unknown = [], []
        stamp = now()
        for t in tickers:
            rec = move(state, t, DONE, ts=stamp)
            (ok if rec else unknown).append(t)
        reorder_open(state, rows)
        atomic_write(QUEUE, render(state, src))
    if ok:
        print(f"done: {', '.join(ok)} · {len(state[OPEN])} open, {len(state[PROG])} in progress")
    for t in unknown:
        print(f"triage_queue: {t} is not in the queue; ignored", file=sys.stderr)
    return 0 if ok else 1


def cmd_reset_stale(args) -> int:
    hours = float(args.hours)
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
    with FileLock(LOCK):
        state = read_queue()
        rows, src = load_source()
        sync(state, rows)
        freed = []
        for r in list(state[PROG]):
            ts = parse_ts(r.get("ts", ""))
            if ts is None or ts < cutoff:
                state[PROG].remove(r)
                state[OPEN].append(dict(r, lane="", ts=""))
                freed.append(f"{r['ticker']}(lane {r.get('lane') or '-'})")
        reorder_open(state, rows)
        atomic_write(QUEUE, render(state, src))
    print(
        f"reset-stale {hours:g}h: released {len(freed)} claim(s)"
        + (f" — {', '.join(freed)}" if freed else "")
        + f" · {len(state[OPEN])} open"
    )
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Triage work queue.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("sync", help="add any new tickers from the source file to Open")
    sub.add_parser("status", help="print counts and current claims")

    p = sub.add_parser("next", help="claim the next N open tickers for a lane")
    p.add_argument("n", type=int)
    p.add_argument("--lane", required=True, help="lane id, e.g. a, b, routine-1")

    p = sub.add_parser("done", help="mark tickers finished")
    p.add_argument("tickers", nargs="+")

    p = sub.add_parser("reset-stale", help="return claims older than HOURS to Open")
    p.add_argument("hours", type=float)

    args = ap.parse_args(argv)
    return {
        "sync": cmd_sync,
        "status": cmd_status,
        "next": cmd_next,
        "done": cmd_done,
        "reset-stale": cmd_reset_stale,
    }[args.cmd](args)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
