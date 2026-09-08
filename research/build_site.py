#!/usr/bin/env python3
"""Build docs/index.html (GitHub Pages) from the newest scan report + paper NAV. Zero JS deps."""
import datetime as dt, re
from collections import Counter
from pathlib import Path
import pandas as pd, markdown
ROOT = Path(__file__).resolve().parents[1]
reports = sorted((ROOT / "reports").glob("????-??-??.md")); latest = reports[-1]
nav = pd.read_csv(ROOT / "paper" / "nav.csv", parse_dates=["date"]).drop_duplicates("date", keep="last")
nav_ret = nav.nav.iloc[-1] / nav.nav.iloc[0] - 1; spy_ret = nav.spy.iloc[-1] / nav.spy.iloc[0] - 1
def spark(vals, w=600, h=120):
    if len(vals) < 2: return "<p><em>Track record starts accumulating daily.</em></p>"
    lo, hi = min(vals), max(vals); rng = (hi - lo) or 1
    pts = " ".join(f"{i*w/(len(vals)-1):.1f},{h-(v-lo)/rng*(h-10)-5:.1f}" for i, v in enumerate(vals))
    return f'<svg viewBox="0 0 {w} {h}" width="100%" height="{h}"><polyline fill="none" stroke="#2563eb" stroke-width="2" points="{pts}"/></svg>'
body = markdown.markdown(latest.read_text(), extensions=["tables"])
dv = ROOT / "research" / "deepvalue"
picks_md = (dv / "PICKS.md").read_text() if (dv / "PICKS.md").exists() else ""
track_md = (dv / "TRACK.md").read_text() if (dv / "TRACK.md").exists() else ""
ls_md = (dv / "LS_TRACK.md").read_text() if (dv / "LS_TRACK.md").exists() else ""
def ls_section(md):
    """Pull the marked summary block out of LS_TRACK.md; stay silent if it is missing or malformed."""
    if "<!--LS_SUMMARY-->" not in md or "<!--/LS_SUMMARY-->" not in md: return ""
    block = md.split("<!--LS_SUMMARY-->", 1)[1].split("<!--/LS_SUMMARY-->", 1)[0].strip()
    if not block: return ""
    return f"""<h2>Does the reading have information?</h2>
<p><small>A market-neutral test of the verdicts themselves: long every IDEA, short every PASS, hedge the net with IWM. WATCH names are excluded and shown separately. <a href="https://github.com/davespinelli/Claude-Space/blob/main/research/deepvalue/LS_TRACK.md">Full rules, positions and daily series</a>.</small></p>
{markdown.markdown(block, extensions=["tables"])}"""
ls_html = ls_section(ls_md)
notes = sorted((dv / "notes").glob("*.md"), reverse=True) if (dv / "notes").exists() else []
note_links = "".join(f'<li><a href="https://github.com/davespinelli/Claude-Space/blob/main/research/deepvalue/notes/{n.name}">{n.stem.replace("_", " · ")}</a></li>' for n in notes[:20])
SITE = "https://davespinelli.github.io/Claude-Space"
REPO = "https://github.com/davespinelli/Claude-Space"
DISCLAIMER = ("Research and education only. Nothing here is investment advice or a recommendation to buy or sell "
              "any security. No price targets are recommendations; positions and sizing are the reader's decision. "
              "Past performance does not predict future results.")
NOTE_CSS = """body{font:16px/1.65 system-ui,sans-serif;max-width:820px;margin:0 auto;padding:0 1rem 3rem;color:#111}
.topbar{background:#111;margin:0 -1rem 1.5rem;padding:.7rem 1rem;font-size:14px}
.topbar a{color:#7dd3fc;text-decoration:none;margin-right:.35rem}.topbar a:hover{text-decoration:underline}
.topbar span{color:#888;margin-right:.35rem}
h1{font-size:1.6rem;line-height:1.25;margin:.4rem 0}h2{font-size:1.15rem;margin-top:2rem;border-top:1px solid #eee;padding-top:1rem}
table{border-collapse:collapse;width:100%;font-size:14px;display:block;overflow-x:auto}
th,td{border:1px solid #ddd;padding:4px 8px;text-align:right}th:first-child,td:first-child{text-align:left}th{background:#f4f4f5}
small,.meta{color:#555}.badge{display:inline-block;background:#f4f4f5;border-radius:6px;padding:.15rem .5rem;font-size:13px;margin-right:.4rem}
.disc{border-top:1px solid #eee;margin-top:2.5rem;padding-top:1rem;font-size:13px;color:#555}
a{color:#1d4ed8}"""

def esc(t):
    return (t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;").replace("'", "&#39;"))

NOTE_HDR = re.compile(r"^#\s+(?P<t>[A-Z0-9.\-]+)\s+—\s+(?P<c>.+?)\s+·\s+(?P<d>\d{4}-\d{2}-\d{2})\s+·\s+Verdict:\s*(?P<v>\w+)\s+·\s+Conviction\s+(?P<k>\d+)", re.M)

def parse_note(path):
    """Header line + section-9 summary. Returns None if the header is not the expected shape."""
    md = path.read_text()
    m = NOTE_HDR.match(md.splitlines()[0] if md.splitlines() else "")
    if not m: return None
    summary = ""
    if "## 9." in md:
        sec9 = md.split("## 9.", 1)[1].split("\n", 1)[-1]
        sec9 = sec9.split("\n## ", 1)[0]
        for para in sec9.split("\n\n"):
            para = " ".join(para.split()).strip()
            if para and not para.startswith("_"):
                summary = para; break
    return dict(ticker=m["t"], company=m["c"], date=m["d"], verdict=m["v"].upper(),
                conviction=m["k"], summary=summary, md=md, src=path.name)

# Latest note per ticker (notes are sorted newest-first, so the first one wins).
parsed, seen = [], set()
for n in notes:
    rec = parse_note(n)
    if not rec or rec["ticker"] in seen: continue
    seen.add(rec["ticker"]); parsed.append(rec)
parsed.sort(key=lambda r: (r["date"], r["ticker"]), reverse=True)

def note_page(r):
    desc = esc(r["summary"][:155])
    title = f'{r["ticker"]} stock research: {r["company"]} ({r["verdict"].title()}, {r["date"]})'
    body = markdown.markdown(r["md"], extensions=["tables"])
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{SITE}/notes/{r['ticker']}.html">
<link rel="sitemap" type="application/xml" href="{SITE}/sitemap.xml">
<style>{NOTE_CSS}</style></head><body>
<nav class="topbar"><a href="../index.html">&#8592; Daily Systematic Market Scan</a><span>·</span><a href="index.html">All research notes</a><span>·</span><a href="../index.html#storefront">Get your idea backtested</a></nav>
<p class="meta"><span class="badge">{esc(r['verdict'])}</span><span class="badge">conviction {esc(r['conviction'])}</span><span class="badge">published {r['date']}</span></p>
<article>{body}</article>
<p class="meta"><small>Source markdown: <a href="{REPO}/blob/main/research/deepvalue/notes/{r['src']}">{esc(r['src'])}</a> · <a href="{REPO}/blob/main/research/deepvalue/README.md">how these notes are built</a> · <a href="{REPO}/blob/main/research/deepvalue/TRACK.md">every verdict tracked since publication</a>.</small></p>
<p class="disc">{DISCLAIMER}</p>
</body></html>"""

def notes_index_page(rows):
    tr = "".join(
        f'<tr><td><a href="{r["ticker"]}.html">{esc(r["ticker"])}</a></td><td>{esc(r["company"])}</td>'
        f'<td>{esc(r["verdict"])}</td><td>{esc(r["conviction"])}</td><td>{r["date"]}</td>'
        f'<td>{esc(r["summary"][:180])}{"…" if len(r["summary"]) > 180 else ""}</td></tr>' for r in rows)
    counts = Counter(r["verdict"] for r in rows)
    tally = " · ".join(f"{counts[v]} {v}" for v in ("IDEA", "WATCH", "PASS") if counts.get(v))
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Deep Value research notes — {len(rows)} small and mid-cap stocks, every verdict tracked</title>
<meta name="description" content="{len(rows)} full research notes on US small and mid-cap stocks, built from SEC filings with citations, valuation and pre-registered kill criteria. {esc(tally)}. Every verdict tracked from publication.">
<link rel="canonical" href="{SITE}/notes/">
<link rel="sitemap" type="application/xml" href="{SITE}/sitemap.xml">
<style>{NOTE_CSS}
td:nth-child(2),td:nth-child(6){{text-align:left}}</style></head><body>
<nav class="topbar"><a href="../index.html">&#8592; Daily Systematic Market Scan</a><span>·</span><a href="../index.html#storefront">Get your idea backtested</a></nav>
<h1>Deep Value Desk — research notes</h1>
<p><small>{len(rows)} notes, newest first ({tally}). Each one is built from the 10-K, 10-Q, proxy, 8-Ks, insider filings and the earnings call or press release, with citations, base/bear/bull valuation and pre-registered kill criteria. Every verdict, including the rejections, is tracked from publication. <a href="{REPO}/blob/main/research/deepvalue/README.md">Methodology</a> · <a href="{REPO}/blob/main/research/deepvalue/TRACK.md">track record</a> · <a href="{REPO}/blob/main/research/deepvalue/COVERAGE.md">coverage log</a>.</small></p>
<table><thead><tr><th>Ticker</th><th>Company</th><th>Verdict</th><th>Conv</th><th>Date</th><th>Summary</th></tr></thead><tbody>{tr}</tbody></table>
<p class="disc">{DISCLAIMER}</p>
</body></html>"""

notes_index_html = f'<p><strong><a href="notes/index.html">Browse all {len(parsed)} research notes &#8594;</a></strong> — one page per company, with the full note, the valuation and the kill criteria.</p>'

deepvalue_html = f"""<h2>Deep Value Desk — researched ideas, tracked forever</h2>
<p><small>Small and mid-cap edge cases. Every note is built from the 10-K, 10-Q, proxy, 8-Ks, insider filings and the earnings call or press release, with citations, base/bear/bull valuation and pre-registered kill criteria. Every verdict, including rejections, is tracked from publication. <a href="https://github.com/davespinelli/Claude-Space/blob/main/research/deepvalue/README.md">Methodology</a>.</small></p>
{markdown.markdown(track_md.split("\n", 1)[1] if track_md else "_Track record starts with the first published verdict._", extensions=["tables"])}
{ls_html}
<h3>Latest research notes</h3>
{notes_index_html}
<ul>{note_links or "<li><em>First notes publishing shortly.</em></li>"}</ul>"""
# Idea B2 — odd-lot tender offers. Show only the live-share-tender table from
# TENDERS.md (the first markdown table) plus a link to the full file.
tenders_path = ROOT / "research" / "tenders" / "TENDERS.md"
tenders_html = ""
if tenders_path.exists():
    tmd = tenders_path.read_text()
    sub = tmd.split("## Live share tenders", 1)[-1].split("\n## ", 1)[0]
    table = "\n".join(l for l in sub.splitlines() if l.startswith("|"))
    stamp = next((l.strip().strip("_") for l in tmd.splitlines() if l.startswith("_Generated")), "")
    tenders_html = f"""<h2>Tender offers with odd-lot priority</h2>
<p><small>Issuer self-tenders (SEC Schedule TO-I) that buy back stock at a premium. Most give <strong>odd-lot priority</strong>: a holder of fewer than 100 shares who tenders all of them is bought in full, ahead of the proration that hits everyone else. Profit shown is for a 99-share position. {stamp}</small></p>
{markdown.markdown(table, extensions=["tables"]) if table else "<p><em>No live offers in the current window.</em></p>"}
<p><small>Risks, the odd-lot rule and the quoted filing language: <a href="https://github.com/davespinelli/Claude-Space/blob/main/research/tenders/TENDERS.md">TENDERS.md</a> · full history: <a href="https://github.com/davespinelli/Claude-Space/blob/main/research/tenders/history.csv">history.csv</a>. Information, not advice.</small></p>"""

gig = "https://www.fiverr.com/"  # TODO: live gig URL
stripe_std = ""  # TODO: Stripe Payment Link $99 Standard
stripe_pro = ""  # TODO: Stripe Payment Link $249 Pro
html = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Daily Systematic Market Scan — Claude Space</title>
<meta name="description" content="Free daily quantitative scan of 58 ETFs, mega-caps, bonds and commodities: momentum, trend, breadth, RSI. Updated every US trading day after the close.">
<style>body{{font:16px/1.5 system-ui,sans-serif;max-width:960px;margin:2rem auto;padding:0 1rem;color:#111}}table{{border-collapse:collapse;width:100%;font-size:14px;overflow-x:auto;display:block}}th,td{{border:1px solid #ddd;padding:4px 8px;text-align:right}}th:first-child,td:first-child{{text-align:left}}th{{background:#f4f4f5}}.cta{{background:#111;color:#fff;padding:1rem 1.25rem;border-radius:8px;margin:1.5rem 0}}.cta a{{color:#7dd3fc}}.kpi{{display:flex;gap:2rem;flex-wrap:wrap}}.kpi div{{background:#f4f4f5;padding:.75rem 1rem;border-radius:8px}}small{{color:#555}}</style></head><body>
<h1>Daily Systematic Market Scan</h1>
<p><small>Updated {dt.date.today()} · rules-based, fully automated, every US trading day after the close · <a href="https://github.com/davespinelli/Claude-Space">source &amp; full history on GitHub</a></small></p>
<div class="cta" id="storefront"><strong>Want your own trading idea backtested?</strong> Rules in plain English → transparent Python backtest with realistic costs, drawdowns, robustness checks and an honest verdict in 48h.<br>
{"<a href='"+stripe_std+"'>Standard $99</a> · <a href='"+stripe_pro+"'>Pro $249 (walk-forward + code)</a> · " if stripe_std else ""}<a href="{gig}">or order via Fiverr →</a></div>
<h2>Paper track record (rules v1, live since {nav.date.iloc[0].date()})</h2>
<div class="kpi"><div>NAV<br><strong>${nav.nav.iloc[-1]:,.0f}</strong></div><div>Return<br><strong>{nav_ret:+.2%}</strong></div><div>SPY same period<br><strong>{spy_ret:+.2%}</strong></div><div>Days<br><strong>{len(nav)}</strong></div></div>
{spark(list(nav.nav))}
<p><small>Every trade and rule is public: <a href="https://github.com/davespinelli/Claude-Space/blob/main/research/RULES.md">RULES.md</a> · <a href="https://github.com/davespinelli/Claude-Space/blob/main/paper/trades.csv">trades.csv</a> · <a href="https://github.com/davespinelli/Claude-Space/blob/main/research/LEADERBOARD.md">research leaderboard</a>.</small></p>
{deepvalue_html}
{tenders_html}
<h2>Daily quantitative scan</h2>
{body}
<p><small>Research and education only. Nothing here is investment advice or a recommendation to buy or sell any security. Past performance does not predict future results.</small></p>
</body></html>"""
docs = ROOT / "docs"
docs.mkdir(exist_ok=True); (docs / "index.html").write_text(html); (docs / ".nojekyll").touch()

# --- SEO surface: one page per note, an index, a sitemap and robots.txt ---
notes_dir = docs / "notes"; notes_dir.mkdir(exist_ok=True)
for r in parsed:
    (notes_dir / f"{r['ticker']}.html").write_text(note_page(r))
(notes_dir / "index.html").write_text(notes_index_page(parsed))
# Drop pages for notes that no longer exist (a ticker renamed or withdrawn).
live = {f"{r['ticker']}.html" for r in parsed} | {"index.html"}
stale = [f for f in notes_dir.glob("*.html") if f.name not in live]
for f in stale: f.unlink()

today = dt.date.today().isoformat()
urls = [(f"{SITE}/", today, "daily", "1.0"), (f"{SITE}/notes/", today, "daily", "0.9")]
urls += [(f"{SITE}/notes/{r['ticker']}.html", r["date"], "weekly", "0.8") for r in parsed]
sitemap = "\n".join(
    f"  <url><loc>{u}</loc><lastmod>{m}</lastmod><changefreq>{c}</changefreq><priority>{p}</priority></url>"
    for u, m, c, p in urls)
(docs / "sitemap.xml").write_text(
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + sitemap + "\n</urlset>\n")
(docs / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")

print(f"built docs/index.html from {latest.name}; {len(parsed)} note pages + notes/index.html; "
      f"sitemap {len(urls)} URLs; robots.txt" + (f"; removed {len(stale)} stale" if stale else ""))
