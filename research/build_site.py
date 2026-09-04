#!/usr/bin/env python3
"""Build docs/index.html (GitHub Pages) from the newest scan report + paper NAV. Zero JS deps."""
import datetime as dt
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
deepvalue_html = f"""<h2>Deep Value Desk — researched ideas, tracked forever</h2>
<p><small>Small and mid-cap edge cases. Every note is built from the 10-K, 10-Q, proxy, 8-Ks, insider filings and the earnings call or press release, with citations, base/bear/bull valuation and pre-registered kill criteria. Every verdict, including rejections, is tracked from publication. <a href="https://github.com/davespinelli/Claude-Space/blob/main/research/deepvalue/README.md">Methodology</a>.</small></p>
{markdown.markdown(track_md.split("\n", 1)[1] if track_md else "_Track record starts with the first published verdict._", extensions=["tables"])}
{ls_html}
<h3>Latest research notes</h3><ul>{note_links or "<li><em>First notes publishing shortly.</em></li>"}</ul>"""
# Idea B2 — odd-lot tender offers. Show only the live-share-tender table from
# TENDERS.md (the first markdown table) plus a link to the full file.
tenders_path = ROOT / "research" / "tenders" / "TENDERS.md"
tenders_html = ""
if tenders_path.exists():
    tmd = tenders_path.read_text()
    sub = tmd.split("## Live share tenders", 1)[-1].split("\n## ", 1)[0]
    table = "\n".join(l for l in sub.splitlines() if l.startswith("|"))
    stamp = next((l.strip() for l in tmd.splitlines() if l.startswith("_Generated")), "")
    tenders_html = f"""<h2>Tender offers with odd-lot priority</h2>
<p><small>Issuer self-tenders (SEC Schedule TO-I) that buy back stock at a premium. Most give <strong>odd-lot priority</strong>: a holder of fewer than 100 shares who tenders all of them is bought in full, ahead of the proration that hits everyone else. Profit shown is for a 99-share position. {markdown.markdown(stamp)}</small></p>
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
<div class="cta"><strong>Want your own trading idea backtested?</strong> Rules in plain English → transparent Python backtest with realistic costs, drawdowns, robustness checks and an honest verdict in 48h.<br>
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
(ROOT / "docs").mkdir(exist_ok=True); (ROOT / "docs" / "index.html").write_text(html); (ROOT / "docs" / ".nojekyll").touch()
print("built docs/index.html from", latest.name)
