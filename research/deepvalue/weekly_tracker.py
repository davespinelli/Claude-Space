"""Weekly stock-tracker email for David: every reviewed stock ranked by return vs the S&P 500.

Two steps, so the numbers come from code and only the "why" lines come from the model:

  python research/deepvalue/weekly_tracker.py prepare [--quarterly] [--out DIR]
      Writes DIR/data.json: group summary, the 5 picks, this week's top 10 vs the S&P 500
      with the context needed to explain each one, and (quarterly) the full ranked list.
  python research/deepvalue/weekly_tracker.py render [--quarterly] [--out DIR] [--log]
      Reads DIR/data.json plus DIR/why.json ({"TICKER": "one line", "_pattern": "2-4 sentences"})
      and writes DIR/email.html, DIR/email.txt and DIR/subject.txt. --log appends the week's
      top 10 and pattern to research/deepvalue/TOP10_LOG.md.

Inputs: TRACK.md (refreshed every weekday by GitHub Actions), its git history (for the 1-week
move), PICKS.md, COVERAGE.md, universe_v2.csv and filings/MANIFEST.json. "vs S&P" is the stock's
price return since the review date minus SPY's over the same dates, in percentage points.
Quarterly mode switches on automatically in the first 7 days of January, April, July and October.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import html
import json
import re
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
TRACK = HERE / "TRACK.md"
REL_TRACK = "research/deepvalue/TRACK.md"
CHECKLIST_URL = "https://claude.ai/artifact/Dp9uP51Hb8GSEZ3GChctcp"
SITE_URL = "https://davespinelli.github.io/Claude-Space/"
CALL = {"IDEA": "Pick", "WATCH": "Watch", "PASS": "Passed"}
REPORT_FORMS = ("10-Q", "10-K")


# ---------- parsing ----------

def pct(s: str) -> float | None:
    s = s.strip().replace("%", "").replace("+", "")
    try:
        return float(s) / 100
    except ValueError:
        return None


def parse_track(text: str) -> list[dict]:
    rows, group = [], None
    for line in text.splitlines():
        m = re.match(r"## (IDEA|WATCH|PASS)\b", line)
        if m:
            group = m.group(1)
            continue
        if not group or not line.startswith("| 20"):
            continue
        c = [x.strip() for x in line.strip("|").split("|")]
        if len(c) < 10:
            continue
        ret, spy, iwm = pct(c[5]), pct(c[7]), pct(c[6])
        if ret is None or spy is None:
            continue
        rows.append(dict(group=group, date=c[0], ticker=c[1], conv=c[2], p0=float(c[3]), now=float(c[4]),
                         ret=ret, iwm=iwm, spy=spy, alpha=ret - spy, days=int(c[9])))
    return rows


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True).stdout


def week_ago_rows() -> tuple[list[dict], str | None]:
    sha = git("log", "-1", "--before=6 days ago", "--format=%H", "--", REL_TRACK).strip()
    if not sha:
        return [], None
    text = git("show", f"{sha}:{REL_TRACK}")
    m = re.search(r"updated (\d{4}-\d{2}-\d{2})", text)
    return parse_track(text), (m.group(1) if m else None)


def table_rows(path: Path) -> list[list[str]]:
    out = []
    if path.exists():
        for line in path.read_text().splitlines():
            if line.startswith("| 20"):
                out.append([x.strip() for x in line.strip("|").split("|")])
    return out


def load_context() -> tuple[dict, dict, dict, dict]:
    kill = {r[1]: r[6] for r in table_rows(HERE / "PICKS.md") if len(r) > 6}
    oneline = {}
    for r in table_rows(HERE / "COVERAGE.md"):
        if len(r) > 5:
            oneline[r[1]] = re.sub(r"^(IDEA|WATCH|PASS), conviction \d\.\s*", "", r[5]).rstrip("…").strip()
    industry = {}
    uv = HERE / "universe_v2.csv"
    if uv.exists():
        with uv.open() as f:
            for r in csv.DictReader(f):
                industry[r.get("ticker", "")] = dict(industry=r.get("sic_desc", ""), lane=r.get("lane", ""),
                                                      artifact=r.get("artifact_flag", ""))
    manifest = {}
    mf = HERE / "filings" / "MANIFEST.json"
    if mf.exists():
        manifest = json.loads(mf.read_text()).get("tickers", {})
    return kill, oneline, industry, manifest


def filings_after(manifest: dict, ticker: str, since: str) -> list[str]:
    """Filing files dated on or after `since`, e.g. '8-K 2026-09-10 2-02-results'."""
    out = []
    for f in manifest.get(ticker, {}).get("files", []):
        m = re.match(r"(10-K|10-Q|8-K|DEF14A)_(\d{4}-\d{2}-\d{2})_?(.*)\.md$", f)
        if m and m.group(2) >= since:
            out.append(f"{m.group(1)} {m.group(2)} {m.group(3)}".strip())
    return sorted(set(out), key=lambda s: s.split()[1])


def new_report(manifest: dict, ticker: str, since: str) -> str | None:
    latest = manifest.get(ticker, {}).get("latest", {})
    hits = [(v.get("filingDate", ""), k) for k, v in latest.items()
            if k in REPORT_FORMS and v.get("filingDate", "") > since]
    for f in filings_after(manifest, ticker, since):
        if "2-02" in f:
            hits.append((f.split()[1], "earnings release"))
    return " / ".join(f"{k} {d}" for d, k in sorted(hits)) or None


def note_path(ticker: str) -> str | None:
    notes = sorted((HERE / "notes").glob(f"*_{ticker}.md"))
    return str(notes[-1].relative_to(ROOT)) if notes else None


# ---------- prepare ----------

def summarize(rows: list[dict]) -> dict:
    n = len(rows)
    if not n:
        return dict(n=0)
    return dict(n=n, avg_ret=sum(r["ret"] for r in rows) / n, avg_alpha=sum(r["alpha"] for r in rows) / n,
                beat=sum(r["alpha"] > 0 for r in rows), oldest_days=max(r["days"] for r in rows))


def prepare(quarterly: bool) -> dict:
    today = dt.date.today()
    rows = parse_track(TRACK.read_text())
    m = re.search(r"updated (\d{4}-\d{2}-\d{2})", TRACK.read_text())
    prev, prev_date = week_ago_rows()
    prev_by = {r["ticker"]: r for r in prev}
    for r in rows:
        p = prev_by.get(r["ticker"])
        if p and p["date"] == r["date"] and p["now"]:
            wk = r["now"] / p["now"] - 1
            spy_wk = (1 + r["spy"]) / (1 + p["spy"]) - 1
            r["week"], r["week_alpha"] = wk, wk - spy_wk
    kill, oneline, industry, manifest = load_context()
    ranked = sorted(rows, key=lambda r: r["alpha"], reverse=True)
    for i, r in enumerate(ranked, 1):
        r["rank"] = i

    def ctx(r: dict) -> dict:
        info = industry.get(r["ticker"], {})
        return dict(r, call=CALL[r["group"]], industry=info.get("industry", ""), lane=info.get("lane", ""),
                    artifact_flag=info.get("artifact", ""), thesis=oneline.get(r["ticker"], "")[:400],
                    note=note_path(r["ticker"]), filings_since_review=filings_after(manifest, r["ticker"], r["date"]))

    top10 = [ctx(r) for r in ranked[:10]]
    bottom10 = [ctx(r) for r in ranked[-10:]]
    mix_all = {g: sum(r["group"] == g for r in rows) for g in CALL}
    mix_top = {g: sum(r["group"] == g for r in top10) for g in CALL}
    picks = []
    for r in rows:
        if r["group"] == "IDEA":
            picks.append(dict(r, kill=kill.get(r["ticker"], ""), new_report=new_report(manifest, r["ticker"], r["date"])))
    auto_q = today.month in (1, 4, 7, 10) and today.day <= 7
    data = dict(
        generated=today.isoformat(), track_updated=m.group(1) if m else None, week_ago_track=prev_date,
        quarterly=quarterly or auto_q,
        summary={CALL[g]: summarize([r for r in rows if r["group"] == g]) for g in CALL},
        picks=picks, top10=top10, bottom10=bottom10,
        top10_mix=mix_top, all_mix=mix_all,
        top10_industries=sorted({t["industry"] for t in top10 if t["industry"]}),
        full=ranked if (quarterly or auto_q) else [],
    )
    if data["quarterly"]:
        by_conv = {}
        for r in rows:
            by_conv.setdefault(f'{CALL[r["group"]]} {r["conv"]}', []).append(r)
        data["by_call_conv"] = {k: summarize(v) for k, v in sorted(by_conv.items())}
    return data


# ---------- render ----------

GREEN, RED, GREY, INK, LINE, HEAD = "#1D6A46", "#B03A2E", "#5C6871", "#18212B", "#E3E7E2", "#F2F4F1"
FONT = "font-family:Arial,Helvetica,sans-serif;"


def fp(x: float | None, digits: int = 1) -> str:
    return "–" if x is None else f"{x * 100:+.{digits}f}%"


def colored(x: float | None) -> str:
    if x is None:
        return f'<span style="color:{GREY}">–</span>'
    return f'<span style="color:{GREEN if x >= 0 else RED};font-weight:bold">{fp(x)}</span>'


def th(label: str, right: bool = False) -> str:
    return (f'<th style="{FONT}font-size:12px;color:{GREY};text-align:{"right" if right else "left"};'
            f'padding:6px 8px;border-bottom:1px solid {LINE};background:{HEAD};font-weight:normal">{label}</th>')


def td(val: str, right: bool = False, bold: bool = False) -> str:
    return (f'<td style="{FONT}font-size:14px;color:{INK};text-align:{"right" if right else "left"};'
            f'padding:7px 8px;border-bottom:1px solid {LINE};{"font-weight:bold;" if bold else ""}white-space:nowrap">{val}</td>')


def table(head: list[tuple[str, bool]], body: list[str]) -> str:
    return ('<table role="presentation" cellspacing="0" cellpadding="0" '
            f'style="border-collapse:collapse;width:100%;max-width:640px;margin:6px 0 18px">'
            f'<tr>{"".join(th(h, r) for h, r in head)}</tr>{"".join(body)}</table>')


def compact_table(rows: list[dict]) -> str:
    """The quarterly all-stocks table, kept small: Gmail clips messages over ~102 KB, so cells carry
    no inline styles and rows are striped instead of ruled."""
    def num(x: float) -> str:
        return f'<font color="{GREEN if x >= 0 else RED}">{fp(x)}</font>'
    head = "".join(f'<th align="{a}"><font size="2" color="{GREY}">{h}</font></th>'
                   for h, a in (("#", "right"), ("Stock", "left"), ("Our call", "left"), ("Return", "right"),
                                ("vs S&P", "right"), ("Held", "right")))
    body = []
    for i, r in enumerate(rows):
        bg = f' bgcolor="{HEAD}"' if i % 2 else ""
        body.append(f'<tr{bg}><td align="right">{r["rank"]}</td><td><b>{html.escape(r["ticker"])}</b></td>'
                    f'<td>{CALL[r["group"]]} {html.escape(r["conv"])}</td><td align="right">{num(r["ret"])}</td>'
                    f'<td align="right"><b>{num(r["alpha"])}</b></td><td align="right">{r["days"]}d</td></tr>')
    return (f'<table cellspacing="0" cellpadding="5" width="100%" style="{FONT}font-size:13px;color:{INK};'
            f'max-width:640px;border-collapse:collapse;margin:6px 0 18px"><tr>{head}</tr>{"".join(body)}</table>')


def h2(text: str, sub: str = "") -> str:
    s = f'<p style="{FONT}font-size:13px;color:{GREY};margin:2px 0 4px">{html.escape(sub)}</p>' if sub else ""
    return f'<h2 style="{FONT}font-size:17px;color:{INK};margin:22px 0 2px">{html.escape(text)}</h2>{s}'


def render(data: dict, why: dict) -> tuple[str, str, str]:
    e = html.escape
    s = data["summary"]
    picks_alpha = s["Pick"].get("avg_alpha")
    watch_alpha = s["Watch"].get("avg_alpha")
    day = dt.date.fromisoformat(data["generated"])
    subject = (f"Stock tracker{' + quarterly review' if data['quarterly'] else ''}, {day:%b %-d}: "
               f"picks {fp(picks_alpha)} vs S&P, watch list {fp(watch_alpha)}, "
               f"leader {data['top10'][0]['ticker']} {fp(data['top10'][0]['alpha'])}")
    parts = [f'<div style="{FONT}color:{INK};max-width:640px">']
    parts.append(f'<p style="{FONT}font-size:14px;color:{GREY};margin:0 0 4px">Every stock the desk reviewed, '
                 f'ranked by return versus the S&amp;P 500 since the day we reviewed it. Prices as of '
                 f'{e(data["track_updated"] or "")}.</p>')

    # 1. scoreboard
    body = []
    for label in ("Pick", "Watch", "Passed"):
        g = s[label]
        if not g.get("n"):
            continue
        body.append("<tr>" + td(f"{label}s" if label != "Passed" else "Passed on", bold=True) + td(str(g["n"]), True)
                    + td(colored(g["avg_ret"]), True) + td(colored(g["avg_alpha"]), True)
                    + td(f'{g["beat"]} of {g["n"]}', True) + "</tr>")
    parts.append(h2("Scoreboard", f"Oldest review is {max(g.get('oldest_days', 0) for g in s.values())} days old; "
                                  "a few weeks of prices say little yet."))
    parts.append(table([("Group", False), ("Stocks", True), ("Avg return", True), ("Avg vs S&P", True), ("Beating S&P", True)], body))

    # 2. top 10
    parts.append(h2("This week's top 10 vs the S&P 500", "Ranked by return minus the S&P 500 since review. "
                                                         "The line under each says why it's up, from its filings and our notes."))
    body = []
    for t in data["top10"]:
        body.append("<tr>" + td(str(t["rank"]), True) + td(e(t["ticker"]), bold=True) + td(f'{t["call"]} {e(t["conv"])}')
                    + td(colored(t["alpha"]), True) + td(colored(t.get("week_alpha")), True) + td(f'{t["days"]}d', True) + "</tr>")
        line = why.get(t["ticker"])
        if line:
            body.append(f'<tr><td></td><td colspan="5" style="{FONT}font-size:13px;color:{GREY};padding:0 8px 9px;'
                        f'border-bottom:1px solid {LINE};white-space:normal">{e(line)}</td></tr>')
    parts.append(table([("#", True), ("Stock", False), ("Our call", False), ("vs S&P", True), ("This week", True), ("Held", True)], body))
    if why.get("_pattern"):
        parts.append(f'<p style="{FONT}font-size:14px;line-height:1.5;margin:0 0 6px"><b>What we\'re learning.</b> {e(why["_pattern"])}</p>')
    mix = data["top10_mix"]
    parts.append(f'<p style="{FONT}font-size:13px;color:{GREY};margin:0 0 16px">Top 10 by our call: {mix["IDEA"]} picks, '
                 f'{mix["WATCH"]} watch, {mix["PASS"]} passed (of {data["all_mix"]["IDEA"]}, {data["all_mix"]["WATCH"]} '
                 f'and {data["all_mix"]["PASS"]} reviewed).</p>')

    # 3. picks
    parts.append(h2("Our 5 picks", "Each has a written warning sign; a new quarterly report means it's time to check it."))
    body = []
    for p in sorted(data["picks"], key=lambda r: r["alpha"], reverse=True):
        status = f'<span style="color:{RED}">New {e(p["new_report"])}: check due</span>' if p["new_report"] else "No new report yet"
        body.append("<tr>" + td(e(p["ticker"]), bold=True) + td(f'${p["p0"]:.2f} → ${p["now"]:.2f}', True)
                    + td(colored(p["alpha"]), True) + td(colored(p.get("week_alpha")), True) + "</tr>")
        body.append(f'<tr><td colspan="4" style="{FONT}font-size:13px;color:{GREY};padding:0 8px 9px;border-bottom:1px solid {LINE};'
                    f'white-space:normal">Warning sign: {e(p["kill"])}<br>{status}</td></tr>')
    parts.append(table([("Stock", False), ("Price then → now", True), ("vs S&P", True), ("This week", True)], body))

    # 4. quarterly full review
    if data["quarterly"]:
        parts.append(h2("Quarterly review: does our call predict anything?", "Average return vs the S&P 500 by verdict and conviction (1-5)."))
        body = ["<tr>" + td(e(k), bold=True) + td(str(v["n"]), True) + td(colored(v["avg_alpha"]), True)
                + td(f'{v["beat"]} of {v["n"]}', True) + "</tr>" for k, v in data["by_call_conv"].items()]
        parts.append(table([("Call and conviction", False), ("Stocks", True), ("Avg vs S&P", True), ("Beating S&P", True)], body))
        parts.append(h2("Quarterly review: every stock", "All reviewed stocks, best to worst vs the S&P 500."))
        parts.append(compact_table(data["full"]))

    parts.append(f'<p style="{FONT}font-size:12px;color:{GREY};margin-top:24px">Research for discussion, not personalised '
                 f'investment advice. Returns are price-only, before costs. '
                 f'<a href="{CHECKLIST_URL}" style="color:{GREEN}">Your checklist</a> · '
                 f'<a href="{SITE_URL}" style="color:{GREEN}">Full tracker</a></p></div>')

    text = [subject, "", "SCOREBOARD (avg vs S&P 500 since review)"]
    for label in ("Pick", "Watch", "Passed"):
        g = s[label]
        if g.get("n"):
            text.append(f'{label}: {g["n"]} stocks, avg {fp(g["avg_ret"])}, vs S&P {fp(g["avg_alpha"])}, {g["beat"]} beating')
    text += ["", "TOP 10 VS S&P 500"]
    for t in data["top10"]:
        text.append(f'{t["rank"]}. {t["ticker"]} ({t["call"]} {t["conv"]}) {fp(t["alpha"])} vs S&P, {t["days"]}d')
        if why.get(t["ticker"]):
            text.append(f'   {why[t["ticker"]]}')
    if why.get("_pattern"):
        text += ["", "WHAT WE'RE LEARNING", why["_pattern"]]
    text += ["", "OUR 5 PICKS"]
    for p in data["picks"]:
        text.append(f'{p["ticker"]} {fp(p["alpha"])} vs S&P. {"New " + p["new_report"] + ": check due" if p["new_report"] else "No new report yet"}')
    text += ["", f"Checklist: {CHECKLIST_URL}", "Research for discussion, not personalised investment advice."]
    return subject, "".join(parts), "\n".join(text)


def append_log(data: dict, why: dict) -> None:
    log = HERE / "TOP10_LOG.md"
    if not log.exists():
        log.write_text("# Top 10 vs S&P 500, week by week\n\nWritten by the weekly tracker email so patterns "
                       "accumulate. vs S&P = return since review minus SPY over the same dates.\n")
    lines = [f"\n## {data['generated']} (prices {data['track_updated']})",
             "| # | Ticker | Call | vs S&P | Days | Why |", "|---|---|---|---|---|---|"]
    for t in data["top10"]:
        lines.append(f'| {t["rank"]} | {t["ticker"]} | {t["call"]} {t["conv"]} | {fp(t["alpha"])} | {t["days"]} | '
                     f'{why.get(t["ticker"], "").replace("|", "/")} |')
    if why.get("_pattern"):
        lines.append(f"\n**Pattern:** {why['_pattern']}")
    with log.open("a") as f:
        f.write("\n".join(lines) + "\n")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("step", choices=["prepare", "render"])
    ap.add_argument("--out", default="/tmp/tracker")
    ap.add_argument("--quarterly", action="store_true")
    ap.add_argument("--log", action="store_true")
    a = ap.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    if a.step == "prepare":
        data = prepare(a.quarterly)
        (out / "data.json").write_text(json.dumps(data, indent=1, default=str))
        print(f"top10: {[t['ticker'] for t in data['top10']]}  quarterly={data['quarterly']}  "
              f"week_ago_track={data['week_ago_track']}  -> {out / 'data.json'}")
    else:
        data = json.loads((out / "data.json").read_text())
        wf = out / "why.json"
        why = json.loads(wf.read_text()) if wf.exists() else {}
        subject, body_html, body_text = render(data, why)
        (out / "subject.txt").write_text(subject)
        (out / "email.html").write_text(body_html)
        (out / "email.txt").write_text(body_text)
        if a.log:
            append_log(data, why)
        print(f"subject: {subject}\n-> {out}/email.html, email.txt, subject.txt")


if __name__ == "__main__":
    main()
