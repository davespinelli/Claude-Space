#!/usr/bin/env python3
"""Fetch SEC filings + earnings-call material for the entire sub-$2B universe.

Reads `universe_under2b.csv` (written by `screen.py --universe-out`) and runs the
`fetch_filings.process` logic for every ticker, then attaches earnings-call
material via `fetch_transcript`. Everything lands under
`research/deepvalue/filings/<TICKER>/` so that a cloud agent with no internet can
research any name in the universe from the published bundle.

Two modes:

  --full          Refresh every ticker in the universe. Weekly. Also runs the
                  SEC press-release transcript fallback for every ticker that
                  still has no real transcript.

  --incremental   Nightly. For every ticker already in the manifest, GET its
                  submissions JSON (one request) and compare the newest
                  10-K / 10-Q / 8-K / DEF 14A / Form 4 accession numbers against
                  what the manifest recorded. Only tickers with a genuinely new
                  filing are re-fetched. Tickers that have newly entered
                  universe_under2b.csv are fetched in full. Costs ~1 request per
                  unchanged ticker instead of ~35.

Resume-safe: `filings/MANIFEST.json` records, per ticker, when it was fetched,
which files were written, whether it succeeded, the newest accession seen per
form type, and how many times a transcript has been attempted. A fresh manifest
entry never causes a skip unless the files are actually on disk, so an
interrupted run - or a CI checkout without `filings/` - picks up correctly.

Transcripts (see fetch_transcript.py for the source chain):
  * Alpha Vantage (FULL transcript, free tier = 25 requests/day) is spent on the
    highest-ranked tickers that still lack one. At most --transcript-budget
    tickers and --av-requests HTTP calls per run; the manifest records every
    attempt so the next run continues down the ranked list instead of retrying
    the same names.
  * In --full mode every other ticker gets the SEC 8-K Item 2.02 EX-99 fallback,
    which is usually the earnings press release rather than the call itself.

SEC traffic is capped globally at --rps requests/second across all worker
threads (SEC's published ceiling is 10/s).

Usage:
    fetch_all.py --full                     # weekly sweep
    fetch_all.py --incremental              # nightly delta
    fetch_all.py --full --limit 12          # smoke test
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import fetch_filings as ff          # noqa: E402
import fetch_transcript as ft       # noqa: E402

OUT_ROOT = HERE / "filings"
MANIFEST = OUT_ROOT / "MANIFEST.json"
RUNINFO = OUT_ROOT / ".last_run.json"
DEFAULT_UNIVERSE = HERE / "universe_under2b.csv"

REAL_TRANSCRIPT = {ft.FULL_TRANSCRIPT, ft.PREPARED_REMARKS}
CT_RE = re.compile(r"^- \*\*content_type:\*\* `([a-z_]+)`", re.M)

# Form families watched by --incremental, mapped to the label stored in the
# manifest. The tuples mirror fetch_filings' own preference lists so that "new
# filing" means "something fetch_filings would actually pick up".
WATCH_FORMS = {
    "10-K": ("10-K", "10-K405", "10-KSB", "20-F", "40-F"),
    "10-Q": ("10-Q",),
    "8-K": ("8-K", "8-K/A"),
    "DEF 14A": ("DEF 14A", "DEFM14A", "DEF 14C", "DEFA14A"),
    "4": ("4",),
}


def log(msg: str) -> None:
    print(f"[{dt.datetime.now():%H:%M:%S}] {msg}", flush=True)


# --------------------------------------------------------------------------
# global SEC rate limit (shared by every thread and both fetcher modules)
# --------------------------------------------------------------------------
class RateLimiter:
    """Token-slot limiter: hands out one slot per 1/rps seconds, globally."""

    def __init__(self, rps: float):
        self.min_interval = 1.0 / rps if rps > 0 else 0.0
        self._lock = threading.Lock()
        self._next = 0.0

    def wait(self) -> None:
        if self.min_interval <= 0:
            return
        with self._lock:
            now = time.monotonic()
            slot = max(now, self._next)
            self._next = slot + self.min_interval
        delay = slot - now
        if delay > 0:
            time.sleep(delay)


class Budget:
    """Hard cap on Alpha Vantage HTTP calls for the whole run."""

    def __init__(self, n: int):
        self.limit = n
        self.remaining = n
        self._lock = threading.Lock()

    def consume(self) -> None:
        with self._lock:
            if self.remaining <= 0:
                raise RuntimeError("Alpha Vantage request budget exhausted for this run")
            self.remaining -= 1

    @property
    def used(self) -> int:
        return self.limit - self.remaining


LIMITER = RateLimiter(8.0)
# Alpha Vantage's free key rejects bursts above ~1 request/second with a
# "spread out your requests" message that looks like a quota error and silently
# wastes budget. Workers therefore queue behind this second, much slower limiter.
AV_LIMITER = RateLimiter(0.8)
AV_BUDGET = Budget(0)


def install_rate_limits(rps: float, av_requests: int, av_quarters: int,
                        av_rps: float = 0.8) -> None:
    """Route every SEC request in both modules through one global limiter."""
    global LIMITER, AV_BUDGET, AV_LIMITER
    LIMITER = RateLimiter(rps)
    AV_LIMITER = RateLimiter(av_rps)
    AV_BUDGET = Budget(av_requests)

    ff._throttle = LIMITER.wait                      # fetch_filings calls this per request

    orig_session = ft.session

    def patched_session(ua):
        s = orig_session(ua)
        orig_get = s.get

        def get(url, *a, **kw):
            if "alphavantage.co" in url:
                AV_BUDGET.consume()                  # raises -> fetch_alphavantage bails out
                AV_LIMITER.wait()                    # <=1 req/s or the free key rejects it
            elif "sec.gov" in url:
                LIMITER.wait()
            return orig_get(url, *a, **kw)

        s.get = get
        return s

    ft.session = patched_session
    ft._sec = None                                   # force rebuild through the patch

    orig_quarters = ft.candidate_quarters
    ft.candidate_quarters = lambda n=av_quarters: orig_quarters(av_quarters)


# --------------------------------------------------------------------------
# manifest
# --------------------------------------------------------------------------
_manifest_lock = threading.Lock()


def load_manifest() -> dict:
    if MANIFEST.exists():
        try:
            m = json.loads(MANIFEST.read_text())
            if isinstance(m, dict) and "tickers" in m:
                return m
        except Exception as exc:  # noqa: BLE001
            log(f"! MANIFEST.json unreadable ({exc}); starting a fresh one")
    return {"version": 2, "updated_at": None, "universe_size": 0, "tickers": {}}


def save_manifest(man: dict) -> None:
    man["updated_at"] = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    tmp = MANIFEST.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(man, indent=1, sort_keys=True) + "\n")
    tmp.replace(MANIFEST)


def _age_days(iso: str | None) -> float:
    if not iso:
        return 1e9
    try:
        return (dt.datetime.now() - dt.datetime.fromisoformat(iso)).total_seconds() / 86400.0
    except Exception:  # noqa: BLE001
        return 1e9


def filings_are_present(ticker: str, rec: dict) -> bool:
    """A fresh manifest entry is worthless if the files are not actually on disk.

    CI checks out a repo without `filings/` (it is gitignored and shipped as a
    release bundle instead), so the manifest alone must never cause a skip.
    """
    d = OUT_ROOT / ticker
    if not (d / "meta.json").exists():
        return False
    files = rec.get("files") or []
    return bool(files) and all((d / f).exists() for f in files)


# --------------------------------------------------------------------------
# submissions polling (the cheap half of --incremental)
# --------------------------------------------------------------------------
def latest_forms(sub: dict) -> dict:
    """Newest filingDate/accession per watched form family. `recent` is newest-first."""
    r = (sub.get("filings") or {}).get("recent") or {}
    forms = r.get("form") or []
    out = {}
    for label, family in WATCH_FORMS.items():
        for i, f in enumerate(forms):
            if f in family:
                out[label] = {"filingDate": r["filingDate"][i],
                              "accession": r["accessionNumber"][i]}
                break
    return out


def poll_submissions(ticker: str, tries: int = 3) -> tuple[int, dict]:
    """Fetch submissions JSON fresh (never from cache) and seed fetch_filings' cache.

    Writing the response into <TICKER>/raw/submissions_<cik>.json under exactly the
    name fetch_filings.get_submissions expects means a ticker we decide to
    re-fetch costs no second submissions request.
    """
    cik, _name = ff.ticker_to_cik(ticker, OUT_ROOT / "_shared" / "raw")
    url = f"https://data.sec.gov/submissions/CIK{cik:010d}.json"
    last_err = None
    for attempt in range(tries):
        LIMITER.wait()
        try:
            r = ff._session.get(url, timeout=45)
            if r.status_code == 200:
                raw_dir = OUT_ROOT / ticker / "raw"
                raw_dir.mkdir(parents=True, exist_ok=True)
                (raw_dir / f"submissions_{cik}.json").write_bytes(r.content)
                return cik, json.loads(r.content)
            last_err = f"HTTP {r.status_code}"
        except Exception as exc:  # noqa: BLE001
            last_err = f"{type(exc).__name__}: {exc}"
        time.sleep(2 ** (attempt + 1))
    raise RuntimeError(f"submissions poll failed: {last_err}")


def diff_forms(old: dict | None, new: dict) -> list[str]:
    """Form labels whose newest accession changed (or that we have never seen)."""
    old = old or {}
    changed = []
    for label, cur in new.items():
        prev = old.get(label)
        if not prev or prev.get("accession") != cur.get("accession"):
            changed.append(label)
    return changed


# --------------------------------------------------------------------------
# transcript state
# --------------------------------------------------------------------------
def existing_transcript(ticker: str) -> tuple[Path | None, str]:
    """Newest transcript_*.md for a ticker and its declared content_type."""
    d = OUT_ROOT / ticker
    if not d.is_dir():
        return None, ""
    best: tuple[Path | None, str] = (None, "")
    for p in sorted(d.glob("transcript_*.md"), reverse=True):
        try:
            head = p.read_text(errors="replace")[:2000]
        except Exception:  # noqa: BLE001
            continue
        m = CT_RE.search(head)
        ct = m.group(1) if m else ""
        if best[0] is None:
            best = (p, ct)
        if ct in REAL_TRANSCRIPT:
            return p, ct
    return best


def has_real_transcript(ticker: str) -> bool:
    return existing_transcript(ticker)[1] in REAL_TRANSCRIPT


# --------------------------------------------------------------------------
# per-ticker work
# --------------------------------------------------------------------------
def do_filings(ticker: str, rec: dict, tries: int = 3) -> bool:
    """Run fetch_filings.process with backoff. Returns True on success."""
    last_err = None
    for attempt in range(tries):
        try:
            res = ff.process(ticker)
            rec.update(
                ok=True,
                error=None,
                fetched_at=dt.datetime.now().isoformat(timespec="seconds"),
                files=sorted(n for n, _ in res["written"]),
                n_files=len(res["written"]),
                bytes=sum(s for _, s in res["written"]),
                problems=res["problems"],
            )
            return True
        except Exception as exc:  # noqa: BLE001
            last_err = f"{type(exc).__name__}: {exc}"
            if attempt < tries - 1:
                time.sleep(2 ** (attempt + 1))       # 2s, 4s
    rec.update(ok=False, error=last_err,
               fetched_at=dt.datetime.now().isoformat(timespec="seconds"))
    return False


def do_transcript(ticker: str, rec: dict, use_av: bool) -> bool:
    """Attach earnings-call material. Returns True if a file was written."""
    tr = dict(rec.get("transcript") or {})
    if has_real_transcript(ticker):
        p, ct = existing_transcript(ticker)
        tr.update(status=ct, file=p.name if p else None)
        rec["transcript"] = tr
        return False

    today = dt.date.today().isoformat()
    order = ["alphavantage", "sec"] if use_av else ["sec"]
    if use_av:
        tr["av_attempts"] = int(tr.get("av_attempts") or 0) + 1
        tr["last_av_attempt"] = today
    tr["attempts"] = int(tr.get("attempts") or 0) + 1
    tr["last_attempt"] = today

    wrote = False
    for name in order:
        got = None
        try:
            got = ft.SOURCES[name](ticker, None)
        except Exception as exc:  # noqa: BLE001
            tr["error"] = f"{name}: {type(exc).__name__}: {exc}"
        if got:
            try:
                p = ft.write_output(ticker, got, force=True)
                tr.update(status=got.content_type, file=p.name, source=name,
                          event_date=got.event_date, error=None)
                wrote = True
            except Exception as exc:  # noqa: BLE001
                tr["error"] = f"{name} write: {exc}"
            break
    if not wrote:
        tr.setdefault("status", "none")
    rec["transcript"] = tr
    return wrote


def fetch_one(ticker: str, rank: int, job: dict, man: dict) -> tuple[dict, bool]:
    """One ticker of work. Never raises. Returns (record, changed_anything)."""
    rec = dict(man["tickers"].get(ticker) or {})
    rec["rank"] = rank
    t0 = time.time()
    changed = False

    if job.get("poll"):
        try:
            cik, sub = poll_submissions(ticker)
            new_latest = latest_forms(sub)
            rec["cik"] = f"{cik:010d}"
            moved = diff_forms(rec.get("latest"), new_latest)
            rec["latest_polled_at"] = dt.datetime.now().isoformat(timespec="seconds")
            if not filings_are_present(ticker, rec):
                moved = moved or ["files-missing"]
            if moved:
                job["filings"] = True
                rec["last_change"] = {"at": dt.date.today().isoformat(), "forms": moved}
            rec["latest"] = new_latest
        except Exception as exc:  # noqa: BLE001
            rec.update(poll_error=f"{type(exc).__name__}: {exc}")
            job["filings"] = True                    # poll failed -> be safe, re-fetch

    if job.get("filings"):
        ok = do_filings(ticker, rec)
        changed = True
        if not ok:
            rec["runtime_s"] = round(time.time() - t0, 1)
            return rec, changed
        # record the newest accession per form from the cache process() just used
        if "latest" not in rec:
            try:
                cikp = next((OUT_ROOT / ticker / "raw").glob("submissions_*.json"))
                rec["latest"] = latest_forms(json.loads(cikp.read_text()))
            except Exception:  # noqa: BLE001
                pass

    if job.get("transcript"):
        if do_transcript(ticker, rec, use_av=job.get("av", False)):
            changed = True

    rec["runtime_s"] = round(time.time() - t0, 1)
    return rec, changed


# --------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------
def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Fetch filings for the whole sub-$2B universe.")
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--full", action="store_true",
                      help="refresh every ticker in the universe (weekly sweep)")
    mode.add_argument("--incremental", action="store_true",
                      help="poll submissions and re-fetch only tickers with new filings")
    ap.add_argument("--universe", default=str(DEFAULT_UNIVERSE),
                    help="universe CSV from screen.py --universe-out")
    ap.add_argument("--limit", type=int, help="only process the top N ranked tickers")
    ap.add_argument("--force", action="store_true",
                    help="re-fetch everything, ignoring freshness and the submissions poll")
    ap.add_argument("--max-age-days", type=float, default=7.0,
                    help="in --full, skip tickers fetched more recently than this")
    ap.add_argument("--workers", type=int, default=6,
                    help="concurrent tickers; the global SEC rate limit still applies")
    ap.add_argument("--rps", type=float, default=8.0,
                    help="global SEC requests/second ceiling (default 8, SEC allows 10)")
    ap.add_argument("--transcript-budget", type=int, default=24,
                    help="tickers allowed to try Alpha Vantage this run (free tier = 25/day)")
    ap.add_argument("--av-requests", type=int, default=24,
                    help="hard ceiling on Alpha Vantage HTTP calls this run")
    ap.add_argument("--av-quarters", type=int, default=3,
                    help="quarters probed per ticker on Alpha Vantage")
    ap.add_argument("--av-rps", type=float, default=0.8,
                    help="Alpha Vantage requests/second (free key rejects bursts over ~1/s)")
    ap.add_argument("--max-8k", type=int, default=6,
                    help="most recent 8-Ks kept per ticker (0 = unlimited)")
    ap.add_argument("--max-form4", type=int, default=12,
                    help="most recent Form 4s parsed per ticker (0 = unlimited)")
    ap.add_argument("--no-transcripts", action="store_true", help="filings only")
    ap.add_argument("--progress-every", type=int, default=25)
    args = ap.parse_args(argv)

    incremental = args.incremental and not args.force
    mode_name = "incremental" if incremental else "full"

    upath = Path(args.universe)
    if not upath.exists():
        log(f"! universe file not found: {upath}")
        log("  run: python research/deepvalue/screen.py --universe-out "
            "research/deepvalue/universe_under2b.csv")
        return 2

    df = pd.read_csv(upath)
    if "rank" not in df.columns or "ticker" not in df.columns:
        log(f"! {upath} has no rank/ticker columns")
        return 2
    df = df.sort_values("rank")
    if args.limit:
        df = df.head(args.limit)
    universe = [(int(r.rank), str(r.ticker).upper()) for r in df.itertuples()]
    rank_of = {tk: rk for rk, tk in universe}
    log(f"mode: {mode_name.upper()}  |  universe: {len(universe)} tickers from {upath}")

    ff.MAX_8K = args.max_8k or None
    ff.MAX_FORM4 = args.max_form4 or None
    install_rate_limits(args.rps, args.av_requests, args.av_quarters, args.av_rps)
    # one shared ticker->CIK map fetch before the pool starts (avoids a write race)
    ff.ticker_to_cik(universe[0][1], OUT_ROOT / "_shared" / "raw")
    ft.ticker_to_cik(universe[0][1])

    man = load_manifest()
    man["universe_size"] = len(universe)
    man["mode_last_run"] = mode_name

    # ---------------- build the job list ----------------
    jobs: dict[str, dict] = {}
    n_new = n_poll = n_skip = 0
    for rank, tk in universe:
        rec = man["tickers"].get(tk) or {}
        known = bool(rec) and filings_are_present(tk, rec)
        if args.force:
            jobs[tk] = {"filings": True}
        elif incremental:
            if not known:
                jobs[tk] = {"filings": True}         # new to the universe, or files gone
                n_new += 1
            else:
                jobs[tk] = {"poll": True}            # 1 request; may escalate to a re-fetch
                n_poll += 1
        else:  # full
            fresh = _age_days(rec.get("fetched_at")) < args.max_age_days and rec.get("ok")
            if fresh and known:
                n_skip += 1
            else:
                jobs[tk] = {"filings": True}

    if incremental:
        log(f"{n_new} new/missing tickers to fetch outright, "
            f"{n_poll} to poll for new filings (1 request each)")
    else:
        log(f"{len(jobs)} to fetch, {n_skip} skipped "
            f"(fetched within {args.max_age_days:g}d and files present)")

    # ---------------- transcript assignment ----------------
    av_set: set[str] = set()
    if not args.no_transcripts:
        need = [(rank, tk) for rank, tk in universe if not has_real_transcript(tk)]

        def key(item):
            rank, tk = item
            tr = (man["tickers"].get(tk) or {}).get("transcript") or {}
            return (int(tr.get("av_attempts") or 0), tr.get("last_av_attempt") or "", rank)

        # fewest previous Alpha Vantage attempts first, then oldest attempt, then
        # best rank -> successive runs walk down the list instead of retrying.
        need.sort(key=key)
        av_set = {tk for _, tk in need[:max(0, args.transcript_budget)]}

        for _, tk in need:
            if tk in av_set:
                jobs.setdefault(tk, {})["transcript"] = True
                jobs[tk]["av"] = True
            elif not incremental:
                # full mode only: SEC press-release fallback for everyone else
                jobs.setdefault(tk, {})["transcript"] = True
        log(f"{len(need)} tickers lack a full transcript; Alpha Vantage assigned to "
            f"{len(av_set)} (<= {args.av_requests} API calls)"
            + ("" if incremental
               else f", SEC press-release fallback for {len(need)-len(av_set)} more"))

    joblist = sorted(((rank_of.get(tk, 10**9), tk, j) for tk, j in jobs.items()),
                     key=lambda x: x[0])
    if not joblist:
        log("nothing to do")
        save_manifest(man)
        RUNINFO.write_text(json.dumps({"mode": mode_name, "changed": False,
                                       "tickers_changed": 0}, indent=1) + "\n")
        print("CHANGED=0")
        return 0

    t0 = time.time()
    done = n_ok = n_err = n_changed = n_refetched = 0
    log(f"starting: {len(joblist)} jobs, {args.workers} workers, <= {args.rps:g} SEC req/s, "
        f"8-K cap {ff.MAX_8K}, Form 4 cap {ff.MAX_FORM4}")

    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as ex:
        futs = {ex.submit(fetch_one, tk, rank, j, man): tk
                for rank, tk, j in joblist}
        for fut in as_completed(futs):
            tk = futs[fut]
            try:
                rec, changed = fut.result()
            except Exception as exc:  # noqa: BLE001
                log(f"! worker crashed on {tk}: {exc}")
                continue
            with _manifest_lock:
                man["tickers"][tk] = rec
                done += 1
                if rec.get("ok") is False:
                    n_err += 1
                else:
                    n_ok += 1
                if changed:
                    n_changed += 1
                if jobs[tk].get("filings"):
                    n_refetched += 1
                if done % args.progress_every == 0 or done == len(joblist):
                    el = time.time() - t0
                    rate = done / el if el else 0
                    eta = (len(joblist) - done) / rate if rate else 0
                    log(f"  {done}/{len(joblist)}  ok={n_ok} err={n_err} "
                        f"refetched={n_refetched}  {el/60:.1f}m elapsed, "
                        f"{el/done:.2f}s/ticker, ETA {eta/60:.1f}m  "
                        f"(AV left: {AV_BUDGET.remaining})")
                    save_manifest(man)

    save_manifest(man)
    el = time.time() - t0

    ok = [t for t, r in man["tickers"].items() if r.get("ok")]
    tr_full = sum(1 for r in man["tickers"].values()
                  if (r.get("transcript") or {}).get("status") in REAL_TRANSCRIPT)
    tr_pr = sum(1 for r in man["tickers"].values()
                if (r.get("transcript") or {}).get("status") == ft.PRESS_RELEASE)

    RUNINFO.write_text(json.dumps(
        {"mode": mode_name, "changed": n_changed > 0, "tickers_changed": n_changed,
         "tickers_refetched": n_refetched, "jobs": len(joblist),
         "finished_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")},
        indent=1) + "\n")

    print()
    log(f"done in {el/60:.1f} min "
        f"({el/max(1,len(joblist)):.2f}s per job over {len(joblist)} jobs; "
        f"{n_refetched} full re-fetches)")
    log(f"manifest: {len(man['tickers'])} tickers, {len(ok)} ok, "
        f"{len(man['tickers'])-len(ok)} errored")
    log(f"transcripts: {tr_full} full/prepared, {tr_pr} press-release fallback")
    log(f"Alpha Vantage calls used: {AV_BUDGET.used}/{AV_BUDGET.limit}")
    log(f"wrote {MANIFEST}")

    errs = [(t, r.get("error")) for t, r in man["tickers"].items() if r.get("ok") is False]
    if errs:
        print("\nerrors:")
        for t, e in sorted(errs)[:20]:
            print(f"  {t}: {e}")
        if len(errs) > 20:
            print(f"  ... and {len(errs)-20} more")

    # signal for the workflow: only rebuild/upload the bundle when something moved
    print(f"CHANGED={1 if n_changed else 0}")
    gh_out = os.environ.get("GITHUB_OUTPUT")
    if gh_out:
        with open(gh_out, "a") as fh:
            fh.write(f"changed={'true' if n_changed else 'false'}\n")
            fh.write(f"tickers_changed={n_changed}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
