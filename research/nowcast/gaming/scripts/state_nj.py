"""New Jersey (DGE) monthly Atlantic City casino win by casino -> data/state_nj.csv.gz

Usage:  python3 scripts/state_nj.py [download]      (NJ_REFRESH=1 re-reads the two listing pages to pick up new
        months; PDFs are cached in cache/nj/ and never re-downloaded; 404s of guessed URLs kept in cache/nj/_404.json)

SOURCES
  * DGE monthly press releases (PDF). 2016+ linked from https://www.njoag.gov/about/divisions-and-offices/
    division-of-gaming-enforcement-home/financial-and-statistical-information/monthly-press-releases-and-statistical-summaries/
    (e.g. https://www.nj.gov/oag/ge/docs/Financials/PressRelease2026/August2026.pdf). 2012-2015 are no longer
    linked but still served: https://www.nj.gov/oag/ge/docs/Financials/PressRel2012/January2012pressrelease.pdf,
    .../PressRel2014/March2014PressRelease.pdf, .../PressRel2015/June2015PressRelease.pdf (names found via the
    Wayback CDX index).
  * Monthly Gross Revenue Reports (form DGE-101, one page per casino), https://www.nj.gov/oag/ge/docs/Financials/
    MGR2014/201409revenue.pdf ... MGR2026/July2026.pdf (listing .../monthly-gross-revenue-reports/). Used for the
    slot/table split where the release does not split by casino, and to split "Discontinued Operators".

MEASURE  ggr = casino win = slot machine win + table game win (incl. poker), current-month column of the release's
  per-casino table (layouts: "CASINO WIN ANALYSIS" slot/table/total 2012-01..2014-08 and 2025-01+; "MONTHLY WIN
  COMPARISON"/"MONTHLY COMPARISON" casino win / internet / [sports] / total 2014-09..2024-12). Internet gaming and
  sports wagering are excluded; internet-only licensees (Caesars Interactive NJ, Resorts Digital, GNOG, CIENJ,
  Trump Plaza (Internet)) and racetracks (Meadowlands, Monmouth Park, Freehold) are dropped.
  slots/tables: from the release when split, else from the casino's MGR form matched to the release casino by casino
  win (within 0.5%; Bally's Nov 2020 = sum of two licensee forms, Bally's Park Place + Premier). Blank for 3
  casino-months: 2015-09 Golden Nugget (MGR page is a scanned image), 2020-01 Tropicana and 2024-01 Golden Nugget
  (MGR differs 1-3% from the release, i.e. amended). 2017-01 Harrah's and 2018-07 Resorts: slots+tables differ
  from ggr by <= $9.5k (release vs MGR amendment).
  __STATE_TOTAL__ = industry casino-win total row ("Total", "Total: Industry", "Total: Casino Industry", "Grand
  Total"); statewide slot/table from the release summary page ("Slot Machine Win", "Table Game Win").

MONTHS  2012-01 .. 2026-08 (all 176 releases found).

UNITS  14 casinos, unit_level=property; `unit` = release label. Renames linked: ACH / ACH (Atlantic Club) /
  Atlantic Club -> NJ_ATLANTIC_CLUB; Bally's AC / Bally's / Bally's (Premier) / Bally's (CEI) -> NJ_BALLYS_AC
  (both labels summed in 2020-21, label shown = the one with current-month win); Trump Marina -> NJ_GOLDEN_NUGGET
  (renamed May 2011, only zero rows in range); Ocean Resort -> Ocean Casino -> NJ_OCEAN. Same buildings but kept as
  separate ids (new licence after years closed): Revel (NJ_REVEL) vs Ocean (NJ_OCEAN); Trump Taj Mahal
  (NJ_TRUMP_TAJ_MAHAL) vs Hard Rock (NJ_HARD_ROCK).
  Openings/closings (rows before first / after last non-zero month dropped): Revel preview 2012-03, opened Apr 2
  2012, closed Sep 2 2014; Atlantic Club closed Jan 13 2014; Showboat closed Aug 31 2014; Trump Plaza closed Sep 16
  2014; Trump Taj Mahal closed Oct 10 2016; Hard Rock and Ocean opened Jun 27/28 2018. "Discontinued Operators"
  rows were split with the MGR forms (sum verified): 2014-08 Showboat 15,063,185; 2014-09 Revel 142,262 + Trump
  Plaza 1,302,152 (DISC_UNITS). COVID: all casinos closed Mar 16 - Jul 2 2020, Apr-Jun 2020 kept as 0.

PUBLICATION DATES  pub_source=report_text: "For Immediate Release: <date>" on page 1 of each release. Fixes: the
  Dec-2016 release prints "January 12, 2016" (-> 2017-01-12, PDF created 2017-01-11); "April12, 2018" (missing
  space). Median lag 14 days after month end (range 9-19).

SPOT CHECKS (data/state_nj_checks.csv.gz, all 176 months): sum of casino ggr = regulator industry total, max |diff|
  0.0 %; slot and table sums vs statewide split in the note (0 except the 3 blank splits and 2017-01 -$9,453).
  MGR casino win matched the release for every other casino-month. Dollars, not thousands. Jumps >3x/<1/3 outside
  Mar-Aug 2020 are only the openings/closings above.
"""
import os, re, sys, time, json, html
import requests
import pandas as pd
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, 'cache', 'nj')
DATA = os.path.join(ROOT, 'data')
UA = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/124.0 Safari/537.36')
FIN = 'https://www.nj.gov/oag/ge/docs/Financials/'
LISTING = ('https://www.njoag.gov/about/divisions-and-offices/division-of-gaming-enforcement-home/'
           'financial-and-statistical-information/')
os.makedirs(CACHE, exist_ok=True)
os.makedirs(DATA, exist_ok=True)
MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September',
          'October', 'November', 'December']
REFRESH = os.environ.get('NJ_REFRESH') == '1'

_last = [0.0]
NEG_PATH = os.path.join(CACHE, '_404.json')
_neg = set(json.load(open(NEG_PATH))) if os.path.exists(NEG_PATH) else set()


def fetch(url, fname, refresh=False, use_neg=True):
    """Download url to cache/nj/fname unless cached (404s of guessed URLs remembered in _404.json). <=1 req/s."""
    path = os.path.join(CACHE, fname)
    if os.path.exists(path) and os.path.getsize(path) > 0 and not refresh:
        return path
    if url in _neg and use_neg and not refresh:
        return None
    for attempt in range(4):
        wait = 1.0 - (time.time() - _last[0])
        if wait > 0:
            time.sleep(wait)
        _last[0] = time.time()
        try:
            r = requests.get(url, headers={'User-Agent': UA}, timeout=60)
            ok = r.status_code == 200 and (not url.lower().endswith('.pdf') or r.content[:4] == b'%PDF')
            if ok:
                with open(path, 'wb') as f:
                    f.write(r.content)
                return path
            if r.status_code == 404 or (r.status_code == 200 and url.lower().endswith('.pdf')):
                _neg.add(url)
                json.dump(sorted(_neg), open(NEG_PATH, 'w'))
                return None
            print('HTTP', r.status_code, url, file=sys.stderr)
        except Exception as e:  # noqa
            print('ERR', e, url, file=sys.stderr)
        time.sleep(2 ** attempt)
    return None


def listing_links():
    p = fetch(LISTING + 'monthly-press-releases-and-statistical-summaries/', 'listing_press_releases.html',
              refresh=REFRESH)
    s = open(p, encoding='utf-8', errors='ignore').read()
    return sorted(set(re.findall(r'href="(https?://[^"]+/Financials/Press[^"]+\.pdf)"', s)))


def press_release_urls(last_month):
    """{YYYY-MM: [candidate urls]} for monthly press releases 2012-01..last_month."""
    links = listing_links()
    out = {}
    for per in pd.period_range('2012-01', last_month, freq='M'):
        mon, y = MONTHS[per.month - 1], per.year
        cands = [l for l in links if re.search(r'/%s%d(PressRelease|pressrelease)?\.pdf$' % (mon, y), l)]
        folder = 'PressRel%d' % y if y <= 2020 else 'PressRelease%d' % y
        for name in ('%s%dpressrelease.pdf' % (mon, y), '%s%dPressRelease.pdf' % (mon, y),
                     '%s%dpressrelease.pdf' % (mon.lower(), y), '%s%d.pdf' % (mon, y)):
            u = FIN + folder + '/' + name
            if u not in cands:
                cands.append(u)
        out[str(per)] = cands
    return out


def get_press_release(month, cands, listed=()):
    for u in cands:
        p = fetch(u, 'pr_%s.pdf' % month, use_neg=u not in listed)
        if p:
            return p, u
    return None, None


if __name__ == '__main__' and 'download' in sys.argv:
    urls = press_release_urls(sys.argv[2] if len(sys.argv) > 2 else '2026-08')
    for m, c in urls.items():
        p, u = get_press_release(m, c)
        print(m, u if p else 'MISSING')


# ----------------------------------------------------------------------------------------------
# Press-release parsing (per-casino monthly comparison table)
# ----------------------------------------------------------------------------------------------
import pymupdf

NUM_RE = re.compile(r'^\(?-?\$?[\d,]+(\.\d+)?\)?%?$')


def page_rows(page, ytol=3.0):
    """Group words into text rows by y-coordinate; returns list of lists of (x0, text)."""
    words = page.get_text('words')  # x0, y0, x1, y1, word, block, line, wordno
    if page.rotation:  # landscape tables in some 2012 releases: map to display coordinates
        M = page.rotation_matrix
        words = [tuple(pymupdf.Rect(w[:4]) * M) + tuple(w[4:]) for w in words]
    words.sort(key=lambda w: ((w[1] + w[3]) / 2, w[0]))
    rows, cur, cy = [], [], None
    for w in words:
        yc = (w[1] + w[3]) / 2
        if cy is None or abs(yc - cy) <= ytol:
            cur.append(w)
            cy = yc if cy is None else (cy * (len(cur) - 1) + yc) / len(cur)
        else:
            rows.append(sorted(cur, key=lambda z: z[0]))
            cur, cy = [w], yc
    if cur:
        rows.append(sorted(cur, key=lambda z: z[0]))
    return [[(w[0], w[4]) for w in r] for r in rows]


def to_num(tok):
    t = tok.replace('$', '').replace(',', '')
    if t in ('-', '--', '—', '–'):
        return 0.0
    neg = t.startswith('(') and t.endswith(')')
    t = t.strip('()')
    try:
        v = float(t.rstrip('%'))
    except ValueError:
        return None
    return -v if neg else v


def split_row(r):
    """-> (label, [numeric tokens as float or nan for n/a]) ; ignores '$' and footnote markers."""
    label, vals = [], []
    for x, t in r:
        if t in ('$',) or re.fullmatch(r'\([a-z]\)', t):
            continue
        if t.lower() in ('n/a', 'na', 'n/m'):
            vals.append(np.nan)
            continue
        v = to_num(t) if (NUM_RE.match(t) or t in ('-', '--', '—', '–')) else None
        if v is None:
            if vals:  # text after numbers: stop label collection
                continue
            label.append(t)
        else:
            vals.append(v)
    return ' '.join(label).strip(), vals


UNIT_IDS = {  # normalised press-release label -> stable id (None = not a land-based casino)
    'ach': 'NJ_ATLANTIC_CLUB', 'atlanticclub': 'NJ_ATLANTIC_CLUB', 'achatlanticclub': 'NJ_ATLANTIC_CLUB',
    'ballysac': 'NJ_BALLYS_AC', 'ballys': 'NJ_BALLYS_AC', 'ballyspremier': 'NJ_BALLYS_AC', 'ballyscei': 'NJ_BALLYS_AC',
    'borgata': 'NJ_BORGATA',
    'caesars': 'NJ_CAESARS',
    'goldennugget': 'NJ_GOLDEN_NUGGET', 'trumpmarina': 'NJ_GOLDEN_NUGGET',
    'harrahs': 'NJ_HARRAHS',
    'resorts': 'NJ_RESORTS',
    'revel': 'NJ_REVEL',
    'showboat': 'NJ_SHOWBOAT',
    'tropicana': 'NJ_TROPICANA',
    'trumpplaza': 'NJ_TRUMP_PLAZA',
    'trumptajmahal': 'NJ_TRUMP_TAJ_MAHAL', 'tajmahal': 'NJ_TRUMP_TAJ_MAHAL',
    'hardrock': 'NJ_HARD_ROCK',
    'oceancasino': 'NJ_OCEAN', 'oceanresort': 'NJ_OCEAN', 'ocean': 'NJ_OCEAN', 'oceanresortcasino': 'NJ_OCEAN',
    'oceancasinoresort': 'NJ_OCEAN',
    # internet-only licensees / racetracks: no casino win
    'caesarsinteractivenj': None, 'resortsdigital': None, 'trumpplazainternet': None, 'meadowlands': None,
    'monmouthpark': None, 'monmouth': None, 'freehold': None, 'freeholdraceway': None, 'gnog': None,
    'cienj': None, 'cienjtropicana': None, 'cienjharrahs': None,
}
TOTAL_LABELS = {'total': 3, 'totalcurrentoperators': 1, 'totalindustry': 5, 'totalcasinoindustry': 4,
                'grandtotal': 2, 'totalwoatlanticclub': 0}
DISC_LABELS = {'discontinuedoperators'}


def norm(lab):
    return re.sub(r'[^a-z]', '', lab.lower())


def parse_press_release(path, month):
    """Per-casino current-month casino win (+ slot/table when the table is split) and totals."""
    d = pymupdf.open(path)
    per = pd.Period(month, 'M')
    mname = per.strftime('%B').upper()
    for pno, page in enumerate(d):
        rows = page_rows(page)
        text = ' '.join(' '.join(t for _, t in r) for r in rows).upper()
        if 'BORGATA' not in text or 'CASINO WIN' not in text:
            continue
        units, totals, disc = {}, {}, None
        layout = None
        started = False
        for r in rows:
            lab, vals = split_row(r)
            L = lab.upper()
            if ('YEAR-TO-DATE' in L or 'YEAR TO DATE' in L or L.startswith('YTD')) and started:
                break  # second (YTD) table on the same page
            if 'SLOT MACHINE WIN' in L:
                layout = 'split'
            elif 'CASINO WIN' in L and layout is None and ('INTERNET' in L or 'TOTAL GAMING' in L):
                layout = 'casino'
            if len(vals) < 6:
                continue
            n = norm(lab)
            if n in UNIT_IDS or n in TOTAL_LABELS or n in DISC_LABELS:
                started = True
                if layout == 'split':
                    rec = {'slots': vals[0], 'tables': vals[3], 'ggr': vals[6], 'prior': vals[7]}
                else:
                    rec = {'ggr': vals[0], 'prior': vals[1], 'slots': np.nan, 'tables': np.nan}
                if n in UNIT_IDS:
                    if UNIT_IDS[n] is not None and not np.isnan(rec['ggr']):  # nan = closed (e.g. Atlantic Club 2014)
                        units[lab] = rec
                elif n in TOTAL_LABELS:
                    totals[n] = rec
                else:
                    disc = rec
            elif re.search(r'[A-Za-z]', lab) and len(lab) < 40 and not lab.lower().startswith(('result', 'current', 'discont', 'casino licensee', 'racetrack', 'casino')):
                print('NJ %s: unknown row %r %s' % (month, lab, vals[:3]), file=sys.stderr)
        if units:
            if layout is None:
                continue
            # the page must be the monthly table for this month
            if mname not in text and per.strftime('%b').upper() not in text:
                print('NJ %s: month name not found on page %d' % (month, pno + 1), file=sys.stderr)
            return {'units': units, 'totals': totals, 'disc': disc, 'layout': layout, 'page': pno + 1}
    raise ValueError('no casino table in %s' % path)


# ----------------------------------------------------------------------------------------------
# Monthly Gross Revenue Reports (DGE-101, one form per casino): slot/table split + closing casinos
# ----------------------------------------------------------------------------------------------
def mgr_urls(last_month):
    p = fetch(LISTING + 'monthly-gross-revenue-reports/', 'listing_mgr.html', refresh=REFRESH)
    s = open(p, encoding='utf-8', errors='ignore').read()
    links = sorted(set(re.findall(r'href="(https?://[^"]+/Financials/MGR\d{4}/[^"]+\.pdf)"', s)))
    out = {}
    for per in pd.period_range('2012-01', last_month, freq='M'):
        y, mm, mon = per.year, per.month, MONTHS[per.month - 1]
        c = [l for l in links if re.search(r'/MGR%d/(%d%02d[Rr]evenue|%s%d)\.pdf$' % (y, y, mm, mon, y), l)]
        c.append('%sMGR%d/%d%02drevenue.pdf' % (FIN, y, y, mm))
        out[str(per)] = list(dict.fromkeys(c))
    return out


def _n(s):
    s = s.replace(',', '').replace('$', '').strip()
    if s in ('-', ''):
        return 0.0
    neg = s.startswith('(')
    return -float(s.strip('()')) if neg else float(s)


def parse_mgr(path):
    """-> list of {'page', 'name', 'ggr', 'slots', 'tables'} (one per casino form)."""
    d = pymupdf.open(path)
    out = []
    NUMP = r'(?:\$\s*)?(\(?[\d,]+\)?|-)'
    for i, page in enumerate(d):
        t = ' | '.join(l.strip() for l in page.get_text().split('\n') if l.strip())
        t = re.sub(r'\| \$ \|', '|', t)
        tot = re.search(r'Total Casino Win \| ' + NUMP, t)
        if not tot:
            continue
        sl = re.search(r'(?:Total - Slot Machines|Slot Machine Win|\d \| Slot Machines) \| [\d,]+ \| ' + NUMP, t)
        tb = re.search(r'(?:Total - {1,2}Table and Other Games|Total Table Game Win) \| [\d,]+ \| ' + NUMP, t)
        if not sl:
            print('NJ MGR %s p%d: slot line not parsed' % (os.path.basename(path), i + 1), file=sys.stderr)
        name = re.search(r'\| ([A-Z][A-Za-z\'&.,() -]{3,60}) \| MONTHLY GROSS REVENUE REPORT', t)
        ggr = _n(tot.group(1))
        slots = _n(sl.group(1)) if sl else np.nan
        tables = _n(tb.group(1)) if tb else (ggr - slots if sl else np.nan)
        out.append({'page': i + 1, 'name': name.group(1).strip() if name else '', 'ggr': ggr,
                    'slots': slots, 'tables': tables})
    return out


# discontinued-operator rows (casinos that closed during the month) are split with the MGR forms
DISC_UNITS = {'2014-08': {'NJ_SHOWBOAT': 'Showboat'},
              '2014-09': {'NJ_REVEL': 'Revel', 'NJ_TRUMP_PLAZA': 'Trump Plaza'}}
MGR_NAME_HINT = {'NJ_SHOWBOAT': r'SHOWBOAT', 'NJ_REVEL': r'REVEL', 'NJ_TRUMP_PLAZA': r'TRUMP PLAZA'}


def statewide_split(path):
    """Statewide slot / table win for the month from the summary page ('Slot Machine Win', 'Table Game Win')."""
    d = pymupdf.open(path)
    got = {}
    for page in d:
        for r in page_rows(page):
            lab, vals = split_row(r)
            k = norm(lab)
            if k in ('slotmachinewin', 'tablegamewin') and k not in got and len(vals) >= 2:
                got[k] = vals[0]
        if len(got) == 2:
            return got['slotmachinewin'], got['tablegamewin']
    return np.nan, np.nan


def release_date(path, month=None):
    d = pymupdf.open(path)
    t = ' '.join(d[0].get_text().split())
    m = re.search(r'For Immediate Release:?\s*([A-Z][a-z]+\.?\s*\d{1,2},\s*\d{4})', t)
    if m:
        dt = pd.to_datetime(re.sub(r'([A-Za-z])(\d)', r'\1 \2', m.group(1).replace('.', '')))  # 'April12, 2018'
        if month is not None:  # typo guard: 'December 2016' release dated 'January 12, 2016'
            end = pd.Period(month, 'M').end_time.normalize()
            if dt < end and 0 <= (dt + pd.DateOffset(years=1) - end).days <= 60:
                print('NJ %s: release date %s corrected by +1 year' % (month, dt.date()), file=sys.stderr)
                dt = dt + pd.DateOffset(years=1)
        return dt.strftime('%Y-%m-%d'), 'report_text'
    cd = d.metadata.get('creationDate', '')
    if cd.startswith('D:'):
        return '%s-%s-%s' % (cd[2:6], cd[6:8], cd[8:10]), 'pdf_metadata'
    return '', ''


def latest_month():
    links = listing_links()
    ms = []
    for l in links:
        m = re.search(r'/(%s)(\d{4})(?:PressRelease|pressrelease)?\.pdf$' % '|'.join(MONTHS), l)
        if m:
            ms.append(pd.Period('%s-%02d' % (m.group(2), MONTHS.index(m.group(1)) + 1), 'M'))
    return str(max(ms))


def build():
    last = latest_month()
    pr_urls = press_release_urls(last)
    listed = set(listing_links())
    mg_urls = mgr_urls(last)
    rows, tot_rows, notes = [], [], {}
    for month, cands in pr_urls.items():
        path, url = get_press_release(month, cands, listed)
        if path is None:
            print('NJ press release missing', month, file=sys.stderr)
            continue
        pdate, psrc = release_date(path, month)
        r = parse_press_release(path, month)
        fn = os.path.basename(path)
        # aggregate labels mapping to the same casino (e.g. "Bally's (Premier)" + "Bally's (CEI)", 2020-21)
        agg = {}
        for lab, rec in r['units'].items():
            uid = UNIT_IDS[norm(lab)]
            a = agg.setdefault(uid, {'labels': [], 'ggr': 0.0, 'slots': 0.0, 'tables': 0.0})
            if rec['ggr'] != 0 or not a['labels']:
                a['labels'].append(lab)
            a['ggr'] += rec['ggr']
            a['slots'] += rec['slots']
            a['tables'] += rec['tables']
        # MGR forms: slot/table split and closing casinos
        mgr = []
        for u in mg_urls.get(month, []):
            mp = fetch(u, 'mgr_%s.pdf' % month)
            if mp:
                mgr = parse_mgr(mp)
                mfn = os.path.basename(mp)
                break
        used = set()
        for uid, a in agg.items():
            a['src'] = fn
            if a['ggr'] == 0:  # closed all month (COVID Apr-Jun 2020)
                a['slots'], a['tables'] = 0.0, 0.0
                continue
            if not np.isnan(a['slots']) or not mgr:
                continue
            tol = max(2.0, 0.005 * abs(a['ggr']))
            best = min(range(len(mgr)), key=lambda i: abs(mgr[i]['ggr'] - a['ggr']))
            hit = [best] if abs(mgr[best]['ggr'] - a['ggr']) <= tol and best not in used else None
            if hit is None:  # two licensees in one month (Bally's AC, Nov 2020: Bally's Park Place + Premier)
                free = [i for i in range(len(mgr)) if i not in used]
                pairs = [(i, j) for k, i in enumerate(free) for j in free[k + 1:]
                         if abs(mgr[i]['ggr'] + mgr[j]['ggr'] - a['ggr']) <= 2]
                hit = list(pairs[0]) if len(pairs) == 1 else None
            if hit and all(not np.isnan(mgr[i]['slots']) for i in hit):
                used.update(hit)
                a['slots'] = sum(mgr[i]['slots'] for i in hit)
                a['tables'] = sum(mgr[i]['tables'] for i in hit)
                a['src'] = fn + ';' + mfn
            else:
                print('NJ %s: no MGR match for %s (%.0f)' % (month, uid, a['ggr']), file=sys.stderr)
        disc = r['disc']['ggr'] if r['disc'] else 0.0
        if disc:
            want = DISC_UNITS.get(month)
            if not want:
                raise ValueError('NJ %s: discontinued operators %.0f not allocated' % (month, disc))
            matched_ggr = {agg[u]['ggr'] for u in agg}
            free = [m for i, m in enumerate(mgr) if i not in used and
                    all(abs(m['ggr'] - g) > 2 for g in matched_ggr)]
            alloc = {}
            for uid, lab in want.items():
                hit = [m for m in free if re.search(MGR_NAME_HINT[uid], m['name'].upper())]
                if len(hit) == 1:
                    alloc[uid] = hit[0]
                    free.remove(hit[0])
            left = [u for u in want if u not in alloc]
            if len(left) == 1 and len(free) == 1:
                alloc[left[0]] = free[0]
            s = sum(m['ggr'] for m in alloc.values())
            if len(alloc) != len(want) or abs(s - disc) > 2:
                raise ValueError('NJ %s: discontinued split failed (%s vs %.0f)' % (month, s, disc))
            for uid, m in alloc.items():
                agg[uid] = {'labels': [want[uid]], 'ggr': m['ggr'], 'slots': m['slots'], 'tables': m['tables'],
                            'src': fn + ';' + mfn}
            notes[month] = 'discontinued operators %.0f split via MGR: %s' % (
                disc, ', '.join('%s %.0f' % (u, m['ggr']) for u, m in alloc.items()))
        for uid, a in agg.items():
            rows.append({'state': 'NJ', 'unit': ' / '.join(a['labels']), 'unit_id': uid, 'unit_level': 'property',
                         'month': month, 'ggr': a['ggr'], 'slots': a['slots'], 'tables': a['tables'],
                         'n_casinos': np.nan, 'measure': 'casino win (slot win + table game win)',
                         'pub_date': pdate, 'pub_source': psrc, 'source_file': a['src']})
        tk = max(r['totals'], key=lambda k: TOTAL_LABELS[k])
        t = dict(r['totals'][tk])
        if np.isnan(t['slots']):
            ss, st = statewide_split(path)
            if abs(ss + st - t['ggr']) <= 2:
                t['slots'], t['tables'] = ss, st
            elif t['ggr'] == 0:
                t['slots'], t['tables'] = 0.0, 0.0
            else:
                print('NJ %s: statewide slot/table split not found (%s, %s)' % (month, ss, st), file=sys.stderr)
        tot_rows.append({'state': 'NJ', 'unit': '__STATE_TOTAL__', 'unit_id': '__STATE_TOTAL__',
                         'unit_level': 'state_total', 'month': month, 'ggr': t['ggr'], 'slots': t['slots'],
                         'tables': t['tables'], 'n_casinos': np.nan,
                         'measure': 'casino win (slot win + table game win)', 'pub_date': pdate,
                         'pub_source': psrc, 'source_file': fn})
    df = pd.DataFrame(rows).sort_values(['unit_id', 'month'])
    keep = []
    for uid, g in df.groupby('unit_id', sort=False):  # drop zero rows before opening / after closing
        pos = g[g.ggr > 0]
        if len(pos):
            keep.append(g[(g.month >= pos.month.min()) & (g.month <= pos.month.max())])
    df = pd.concat(keep + [pd.DataFrame(tot_rows)], ignore_index=True)
    return df, notes


def checks(df, notes):
    tot = df[df.unit_level == 'state_total'].set_index('month')
    units = df[df.unit_level == 'property']
    rows = []
    for m in sorted(df.month.unique()):
        u = units[units.month == m]
        su = u.ggr.sum()
        reg = tot.ggr.get(m, np.nan)
        note = 'slots diff %.0f, tables diff %.0f (units with split: %d/%d)' % (
            u.slots.sum() - tot.slots.get(m, np.nan), u.tables.sum() - tot.tables.get(m, np.nan),
            u.slots.notna().sum(), len(u))
        if notes.get(m):
            note += '; ' + notes[m]
        rows.append({'month': m, 'sum_of_units': su, 'regulator_total': reg,
                     'diff_pct': 100 * (su - reg) / reg if reg else (0.0 if su == 0 else np.nan), 'note': note})
    return pd.DataFrame(rows)


def jump_scan(df):
    out = []
    for uid, g in df[df.unit_level == 'property'].groupby('unit_id'):
        g = g.sort_values('month')
        r = g.ggr / g.ggr.shift(1)
        for m, x, v in zip(g.month, r, g.ggr):
            if '2020-03' <= m <= '2020-08':
                continue
            if pd.notna(x) and (x > 3 or x < 1 / 3):
                out.append((uid, m, round(x, 3), v))
    return out


if __name__ == '__main__' and 'download' not in sys.argv:
    df, notes = build()
    chk = checks(df, notes)
    cols = ['state', 'unit', 'unit_id', 'unit_level', 'month', 'ggr', 'slots', 'tables', 'n_casinos', 'measure',
            'pub_date', 'pub_source', 'source_file']
    df = df[cols].sort_values(['unit_level', 'unit_id', 'month']).reset_index(drop=True)
    assert not df.duplicated(['unit_id', 'month']).any()
    df.to_csv(os.path.join(DATA, 'state_nj.csv.gz'), index=False, compression='gzip')
    chk.to_csv(os.path.join(DATA, 'state_nj_checks.csv.gz'), index=False, compression='gzip')
    p = df[df.unit_level == 'property']
    print('rows', len(df), 'units', p.unit_id.nunique(), 'months', df.month.min(), df.month.max(), df.month.nunique())
    print('max |diff_pct|', chk.diff_pct.abs().max())
    print('split missing rows:', int(p.slots.isna().sum()),
          'split != ggr (>$2):', int(((p.slots + p.tables - p.ggr).abs() > 2).sum()))
    lag = (pd.to_datetime(df.pub_date) - pd.PeriodIndex(df.month, freq='M').end_time.normalize()).dt.days
    print('pub lag days median/min/max', lag.median(), lag.min(), lag.max(), df.pub_source.value_counts().to_dict())
    print('jumps:', jump_scan(df))
