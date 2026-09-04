# Earnings call transcripts for US small/mid caps — source research

Researched 2026-09-03. Every "tested result" below is from a live request made
from this repo (`.venv/bin/python`, `requests`), not from vendor marketing copy.

**Bottom line up front:** there is **no free, no-key, terms-clean API that
serves earnings call transcripts for US small caps.** The free tier is thin.
The honest options are (a) SEC earnings press releases as a guaranteed
always-available substitute, (b) a free Alpha Vantage key as the only
plausible free source of *actual* transcripts, and (c) ~$25/mo if real
small-cap transcript coverage turns out to matter for the strategy.

---

## 1. APIs

| Source | Free? | Key? | Coverage | Terms verdict | Tested result |
|---|---|---|---|---|---|
| **Alpha Vantage** `EARNINGS_CALL_TRANSCRIPT` | Yes — free tier, 25 req/day, 5 req/min | Yes, but email-only, no card, ~20s | Claims 15+ yrs history, US listings. **Small-cap depth unverified** | OK — standard API ToS, internal research fine | `demo` key + `IBM 2024Q1` → HTTP 200, 57 KB speaker-tagged full transcript. Non-demo symbols return the generic "claim your free key" notice, **not** the "This is a premium endpoint" banner that `REALTIME_BULK_QUOTES` returns — strong evidence the endpoint is free-tier, not premium |
| **EarningsCall** (earningscall.biz) | Demo key free & public; real coverage is paid | `demo` works with no signup | **Demo = AAPL + MSFT only** (verified). Paid = 9,000+ companies | OK — public demo key is offered by the vendor | `/symbols-v2.txt?apikey=demo` → exactly 2 rows (AAPL, MSFT). AAPL transcript → 200, 46 KB full transcript. `CULP` → **HTTP 403**. `/pricing` → 404; pricing is sales-quoted only |
| **earningscalls.dev** | Free tier = limited preview only | Yes, `X-API-Key` required | 246k calls / 12,000+ companies incl. small caps | ⚠️ API OK; **HTML scraping prohibited** — ToS forbids "systematically scrape or bulk-download the archive" and restricts storing data | `/api/v1/...` without key → 404/401. robots.txt *does* allow AI bots on `/transcript/*`, but the ToS overrides robots. Pro $24.99/mo (5k req), Ultra $39.99/mo (25k) |
| **Financial Modeling Prep** | Free plan exists (250 req/day) but transcripts are effectively gated | Yes | Broad | OK if paid | `/stable/earning-call-transcript` and `/api/v3/earning_call_transcript` without key → **HTTP 401 Invalid API KEY**. No demo key accepted |
| **API Ninjas** | No — transcript endpoint is premium-only | Yes | Broad | OK if paid | `/v1/earningstranscript` → **HTTP 400 "Missing API Key"**. Docs mark the transcript endpoints premium |
| **Finnhub** | No — transcripts excluded from free tier | Yes | Broad | OK if paid | Docs: transcripts + live call audio are premium; free key (60 req/min) covers quotes/news/fundamentals only |
| **Quartr** | No public free tier | Sales-gated (`private.quartr.com`) | 13,000+ companies, 27 markets — genuinely good small-cap depth | OK if contracted | Enterprise sales only; no self-serve signup |
| **Benzinga** | No | Yes, enterprise | Global, real-time | OK if paid | Conference-call-transcripts product is enterprise sales |
| **Polygon.io** | n/a | Yes | **No first-party transcript endpoint found** — they resell Benzinga news | — | Not a transcript source |
| **EODHD** | Partial | Yes | Earnings *calendar* oriented, not deep transcripts | OK if paid | Not a viable transcript source |

### Key detail on Alpha Vantage (the one worth acting on)
Alpha Vantage flags premium endpoints explicitly. Compare, both with `apikey=demo`:

```
REALTIME_BULK_QUOTES     -> {"message": "This is a premium endpoint. ..."}
EARNINGS_CALL_TRANSCRIPT -> {"Information": "The **demo** API key is for demo purposes only..."}
NEWS_SENTIMENT           -> {"Information": "The **demo** API key is for demo purposes only..."}
```

`NEWS_SENTIMENT` is a known free-tier endpoint and returns the identical
message, so `EARNINGS_CALL_TRANSCRIPT` is almost certainly free-tier.
**This is inference, not proof** — it cannot be confirmed without a real key,
and no account was created for this research. Verifying it is a 2-minute job
and is the single highest-value open question here.

---

## 2. Public web pages — mostly NOT usable

| Site | robots.txt | Terms of use | Verdict |
|---|---|---|---|
| **Motley Fool** (`/earnings-call-transcripts/`) | Allows the path for `User-agent: *` | **Prohibits it.** "The Motley Fool's Rules" states: *"Use any automated means, including, without limitation, agents, robots, scripts, or spiders, to access, monitor, copy or harvest data from any part of our sites"* is forbidden, and *"You further agree not to create abstracts from or scrape our Content"*. Content licence is one copy, personal, non-commercial | ❌ **Do not scrape.** robots.txt permissiveness does not override the ToS. Also: small-cap coverage has thinned — `/quote/culp/`, `/quote/hurco/`, `/quote/nve-corp/`, `/quote/lakeland-industries/` all return 404 |
| **Seeking Alpha** | Blocks a long list of AI/crawler agents | Transcripts are behind the Premium paywall | ❌ Paywalled and bot-blocked |
| **Yahoo Finance** | Explicitly blocks `ClaudeBot`, `anthropic-ai`, `Claude-Web`, `GPTBot`, `CCBot`, `PerplexityBot`, etc. | — | ❌ No free transcript product, and we are in the blocked UA group |
| **Quartr (web)** | `Allow: /` | Transcripts live behind the app/API; commercial ToS | ❌ Use the paid API, don't scrape the site |
| **Koyfin** | — | Paid terminal, no public API | ❌ Not programmatic |
| **earningscalls.dev** | Allows AI bots on `/transcript/*` | ToS forbids systematic scraping / bulk download | ❌ for scraping, ✅ via their paid API |
| **Company IR sites** | Varies per company | Varies per company | ⚠️ Legally the cleanest (first-party, public), but there is no uniform structure. Fine for a hand-curated watchlist, not for a general pipeline |

---

## 3. The SEC substitute — measured, not assumed

Hypothesis tested: *"many small caps file prepared remarks as an EX-99 exhibit
to the earnings 8-K."*

**Result: this hypothesis is wrong for small caps.**

Sampled the latest 8-K carrying Item 2.02 (Results of Operations) for 16
small/micro caps via `data.sec.gov/submissions/CIK##########.json` with
`User-Agent: ClaudeSpace research dspinjr@gmail.com`:

`CULP, BSET, HURC, NVEC, LAKE, ESCA, UTMD, DAKT, JOUT, KELYA, MLR, PLPC, CMT, VIRC, BGSF, RGP`

| Measure | Count | Share |
|---|---|---|
| Had an EX-99.1 earnings **press release** | 16 / 16 | **100%** |
| Had a **second** EX-99 exhibit | 3 / 16 | 19% |
| Had **prepared remarks / call script / transcript** as an exhibit | **0 / 16** | **0%** |

All three second exhibits were inspected directly and all three are **investor
slide decks**, not prepared remarks:

- `LAKE` EX-99.2 → "Fiscal First Quarter 2027 Financial Results Conference Call" slide deck
- `KELYA` EX-99.2 → "Q2 2026" earnings release supplement deck
- `MLR` EX-99.2 → "Q2 2026 Investor Presentation"

**Conclusion:** the realistic SEC yield for a small cap is the **earnings press
release**, not the call. That is 100% available, free, key-free, and explicitly
permitted (SEC only asks for a descriptive User-Agent and ≤10 req/s). It is a
genuine substitute for the *prepared-remarks* content — CEO/CFO commentary,
guidance, segment colour — but it contains **no Q&A**, which is usually where
the analytically interesting material in a small-cap call actually is.

> Overlap note: `research/deepvalue/fetch_filings.py` already downloads 8-K
> Item 2.02 filings with their EX-99 exhibits. `fetch_transcript.py`'s SEC tier
> is not redundant with it — it picks the single best exhibit and, critically,
> **labels honestly** whether the result is a transcript, prepared remarks, or
> just a press release.

---

## 4. Audio route: IR webcast + local Whisper

**Compute cost — effectively free, and fast enough.** On an M-series Mac, use
`whisper.cpp` with Metal rather than `faster-whisper`: faster-whisper's
CTranslate2 backend has no Metal/GPU path on Apple Silicon and runs on CPU.

| Model | Throughput (M3/M4, Metal) | A 60-minute earnings call |
|---|---|---|
| `small` / `distil` | ~20–30× realtime | **~2–3 minutes** |
| `large-v3` | ~2–3× realtime | **~20–30 minutes** |

Marginal cash cost is $0. For a nightly batch of a few dozen names, `small` at
~2–3 min/call is entirely practical.

**The bottleneck is not transcription, it is getting the audio.** Small-cap
webcasts are hosted on third-party IR platforms behind registration forms and
JS players, and those platforms' ToS generally forbid automated downloading.
Many replays also carry explicit "no recording or rebroadcast" notices.

**Legality:** transcribing a public webcast you are entitled to listen to, for
your own internal, non-redistributed research, is a materially weaker risk than
republishing it — but it is *not* a blanket licence, and the hosting platform's
ToS is a separate constraint from the company's. Verdict: **viable
per-company with human care, not a clean programmatic path at scale.** Not
implemented in `fetch_transcript.py`.

---

## 5. Recommendation

1. **Keep SEC as the guaranteed floor.** It always works, needs no key, is
   unambiguously permitted, and yields the press release for ~100% of US
   small-cap filers. Accept that this is prepared-remarks-grade content with
   no Q&A, and make sure downstream prompts know that (the `content_type`
   header field exists for exactly this reason).

2. **Get the free Alpha Vantage key — the one action item.** Email only, no
   card, ~20 seconds, at <https://www.alphavantage.co/support/#api-key>. Then
   `export ALPHAVANTAGE_API_KEY=...`. First thing to check: does it actually
   return transcripts for names like `CULP`/`HURC`, or only for large caps?
   The 25 req/day cap means roughly 25 tickers/day — fine for a research
   pipeline that backfills gradually, not for a bulk historical pull.

3. **If small-cap transcript coverage proves load-bearing, budget ~$25/mo.**
   Cheapest self-serve option found is **earningscalls.dev Pro** ($24.99/mo,
   5,000 req/mo, 12,000+ companies). **earningscall.biz** is the more
   established vendor (9,000+ companies, real SDKs) but publishes no pricing —
   it requires emailing sales, so it cannot be evaluated in two minutes.
   **Quartr** has the best small-cap depth of anything surveyed but is
   enterprise-only.

4. **Do not scrape Motley Fool, Seeking Alpha, or Yahoo Finance.** Fool's terms
   forbid it in explicit language, Seeking Alpha paywalls transcripts and
   blocks the bot, and Yahoo blocks our user-agent by name. This is not a
   grey area.

**What David needs to sign up for:** exactly one thing — an Alpha Vantage free
API key. No account was created during this research.

---

## 6. Usage

```bash
.venv/bin/python research/deepvalue/fetch_transcript.py --list-sources
.venv/bin/python research/deepvalue/fetch_transcript.py CULP
.venv/bin/python research/deepvalue/fetch_transcript.py CULP --quarter 2026Q2
.venv/bin/python research/deepvalue/fetch_transcript.py CULP --source sec --force
```

Writes `research/deepvalue/filings/<TICKER>/transcript_<date>.md` with a header
declaring `content_type` (`full_transcript` / `prepared_remarks` /
`press_release` / `investor_presentation`), the source, and the source URL.
Exits **1** with actionable guidance when nothing is available, **2** on bad
usage.

**Source order** is `earningscall` → `alphavantage` → `sec`. SEC is deliberately
**last** rather than second: it always succeeds, so putting it earlier would
mask a genuinely better full transcript whenever a key is configured. Override
with `--source`.

### Tested results (2026-09-03, no API keys set)

| Ticker | Source used | content_type | Output |
|---|---|---|---|
| `CULP` (Culp Inc, ~$150M) | SEC EX-99.1 | `press_release` | `filings/CULP/transcript_2026-07-01.md` (37 KB) |
| `HURC` (Hurco, ~$150M) | SEC EX-99.1 | `press_release` | `filings/HURC/transcript_2026-06-05.md` (22 KB) |
| `LAKE` (Lakeland, ~$250M) | SEC EX-99.1 | `press_release` | `filings/LAKE/transcript_2026-06-09.md` (37 KB) |
| `AAPL` (control, full-transcript path) | EarningsCall demo key | `full_transcript` | `filings/AAPL/transcript_2026-07-30.md` |
| `ZZZZQQ` (control, failure path) | none | — | exit 1 + guidance |

For `LAKE` the tool correctly preferred the EX-99.1 press release over the
EX-99.2 slide deck.

> **Classifier caution:** an early version mislabelled CULP's press release as
> `prepared_remarks` because the release contains a "Management Commentary"
> heading. The classifier was tightened to require real spoken-call markers
> (operator cues, Q&A sections) and now errs toward `press_release`.
> Over-claiming that a press release is a transcript is the worst failure mode
> for this pipeline; if you extend the classifier, preserve that bias.
