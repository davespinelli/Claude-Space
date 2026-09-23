"""Maryland monthly casino gaming revenue by casino (2012-01 .. latest).

Sources
-------
* Maryland Lottery and Gaming Control Agency (MLGCA), mdgaming.com. Every month the agency
  publishes a press release "Maryland Casinos Generate $X Million in Gaming Revenue During
  <Month>" in the WordPress category "Casino Financial Reporting" (category id 5). The full
  archive (Oct 2010 onward) is read through the public WordPress REST API:
    https://www.mdgaming.com/wp-json/wp/v2/posts?categories=5&per_page=100&page=N
  (cached as cache/md/posts_cat5_p{N}.json).
* The detailed tables used for the numbers:
    - 2012-06 .. 2016-06: HTML tables inside the press-release body ("VLT Gaming Revenue - <casino>",
      "Table Games Revenue - <casino>", monthly / calendar-YTD / fiscal-YTD columns).
    - 2016-07 .. 2026-02: PDF attached to each release (…/wp-content/uploads/YYYY/MM/*.pdf), one page
      per casino and game type ("VLT Gaming Revenue - <casino>" / "Table Game(s) Revenue - <casino>"),
      first figure after "Gross Terminal Revenue" = the month.
    - 2026-03 .. latest: new two-page "Casino Revenue Worksheets" PDF (slot page + table page with a
      row "<casino> / <Month YYYY>").
    - 2012-01 .. 2012-05 (two slot-only casinos): narrative sentence "<casino> generated $X in <month>".
  PDFs are cached in cache/md/ as <upload-year>_<upload-month>_<original file name>.

Measure
-------
GGR = slot "gross terminal revenue" (VLT win) + table-games gross revenue (banked + non-banked,
i.e. incl. poker). Dollars, not thousands. Sports wagering is published in a separate category and is
not included. `slots` = VLT gross terminal revenue, `tables` = table-games revenue (blank before tables
existed at a casino: Perryville from 2013-03, Maryland Live 2013-04, Rocky Gap 2013-05 opening,
Horseshoe 2014-08 opening, MGM National Harbor 2016-12 opening, Ocean Downs 2017-12; a few months
show tables=0 where the agency printed an empty table page).
__STATE_TOTAL__ = the agency's own "VLT Gaming Revenue - Total" + "Table Game Revenue - Total" tables;
the headline statewide number of the release (first full-dollar amount in the text) is used when no
Total tables exist (2012-01..05, 2026 worksheets without a total) or when the Total tables are
visibly wrong while the headline agrees with the casinos (2013-03: Total table omitted table games;
2015-11 and 2021-08: typo in the agency's VLT Total table, headline = sum of casinos).

Units (unit_id <- names used by the regulator over time; renames linked)
------------------------------------------------------------------------
MD_HOLLYWOOD_PERRYVILLE  "Hollywood Casino Perryville" (Penn National)
MD_OCEAN_DOWNS           "Casino at Ocean Downs" -> "Ocean Downs Casino"
MD_LIVE                  "Maryland LIVE" / "Casino at Maryland Live" -> "Live! Casino & Hotel" (Cordish)
MD_ROCKY_GAP             "Rocky Gap" / "Casino at Rocky Gap" -> "Rocky Gap Resort Casino"
MD_HORSESHOE_BALTIMORE   "Horseshoe" (opened 2014-08-26)
MD_MGM_NATIONAL_HARBOR   "MGM National Harbor" (opened 2016-12-08)
The `unit` column carries the name printed on that month's slot (VLT) table.

Publication date
----------------
pub_date = WordPress post date of the monthly press release (pub_source=press_release). For 6 months
(2018-01..04, 2018-09, 2018-10) the post date is 4-12 days after the attached PDF's CreationDate
(releases re-posted after the 2018 site move), so the PDF CreationDate is used (pub_source =
pdf_metadata). Elsewhere post date = PDF CreationDate (median difference 0 days). Typical lag: 5 days
after month-end (range 3-15; e.g. Aug 2026 data published 2026-09-08). Note: a few months' PDFs were
later replaced by revised/re-uploaded files (Jan/Feb 2017 "Rev 3.29", Nov/Dec 2017 "1.30.18",
Dec 2016 re-uploaded 2020, Apr 2017 re-uploaded 2021, Aug 2018 re-uploaded 2019); values come from
the file now linked, and the statewide headline in the original release text still equals their sum.

Quirks
------
* COVID-19: all six casinos closed 2020-03-16 and reopened 2020-06-19. The April and May 2020
  releases have no data tables (closure) -> ggr=slots=tables=0 for every casino.
* Early (2012-01..05) releases give values only in the narrative; Maryland Live opened 2012-06-06.
* Several PDFs were re-uploaded later (file paths with a later upload year, e.g. Dec 2016 in
  2020/05); the month is taken from the release, the file name is kept in source_file.
* mdgaming.com rate-limits (HTTP 429) bursts; downloader sleeps 1.5 s and backs off.

Spot checks (run 2026-09-23)
----------------------------
Sum of casinos vs the regulator statewide total for every month 2012-01..2026-08 (176 months) in
data/state_md_checks.csv.gz: max |diff| = 0.000%. The headline number in the release text also equals
the sum of casinos in every month where it was parsed (2016-12's first amount is MGM's opening month,
not a total). Month/month jumps > 3x: Rocky Gap 2013-06 (opened 2013-05-22) and Horseshoe 2014-09
(opened 2014-08-26) - both real openings. COVID: 2020-04 and 2020-05 are 0 for all casinos; 2020-03
and 2020-06 are partial months. Units are dollars (cents kept). Independent check vs the per-casino
narrative sentences of the 2013-06..2016-06 releases ("<casino> generated $X"): 169 of 170 equal the
parsed value to $1.5; the one exception (Horseshoe 2016-03, narrative $2,763,169 vs table
$27,631,695) is a dropped digit in the release text.
"""
import os, re, json, time, html, sys
from datetime import date
from urllib.parse import urljoin
import requests
import pandas as pd
import pymupdf

ROOT = '/Users/davidspinelli/Documents/Claude Space/research/nowcast/gaming'
CACHE = os.path.join(ROOT, 'cache', 'md')
DATA = os.path.join(ROOT, 'data')
UA = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
                    '(KHTML, like Gecko) Chrome/124.0 Safari/537.36'}
S = requests.Session(); S.headers.update(UA)
MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august',
          'september', 'october', 'november', 'december']


def fetch(url, fn):
    p = os.path.join(CACHE, fn)
    if os.path.exists(p) and os.path.getsize(p) > 0:
        return p
    for a in range(5):
        try:
            time.sleep(1.5)
            r = S.get(url, timeout=60)
            if r.status_code == 200:
                open(p, 'wb').write(r.content)
                return p
            print('HTTP', r.status_code, url)
            if r.status_code == 404:
                return None
        except Exception as e:
            print('err', e, url)
        time.sleep(20 * (a + 1))
    return None


def pdf_links(content):
    out = []
    for m in re.findall(r'href="([^"]+\.pdf)"', content, re.I):
        u = urljoin('https://www.mdgaming.com/', html.unescape(m))
        u = u.replace('http://gaming.mdlottery.com', 'https://www.mdgaming.com')
        u = u.replace('mdgaming.wpenginepowered.com', 'www.mdgaming.com')
        fn = u.split('/wp-content/uploads/')[-1].replace('/', '_')
        if (u, fn) not in out:
            out.append((u, fn))
    return out


def download():
    os.makedirs(CACHE, exist_ok=True)
    posts = []
    pg = 1
    while True:
        fn = f'posts_cat5_p{pg}.json'
        # the newest page is always re-fetched so new months are picked up
        if pg == 1 and os.path.exists(os.path.join(CACHE, fn)):
            age = time.time() - os.path.getmtime(os.path.join(CACHE, fn))
            if age > 86400 * 7:
                os.remove(os.path.join(CACHE, fn))
        p = fetch(f'https://www.mdgaming.com/wp-json/wp/v2/posts?categories=5&per_page=100&page={pg}', fn)
        if p is None:
            break
        d = json.load(open(p))
        if not d:
            break
        for x in d:
            x['_file'] = fn
        posts += d
        if len(d) < 100:
            break
        pg += 1
    for p in posts:
        for u, fn in pdf_links(p['content']['rendered']):
            if fetch(u, fn) is None:
                print('FAILED', u)
    return posts


def text_of(h):
    h = re.sub(r'(?is)<script.*?</script>|<style.*?</style>', ' ', h)
    t = re.sub(r'<[^>]+>', ' ', h)
    t = html.unescape(t).replace('\xa0', ' ')
    return re.sub(r'\s+', ' ', t)


AMT = r'\(?-?\$\s*\(?-?[\d,]+(?:\.\d+)?\)?|\$\s*-(?![\d])'


def money(s):
    s = s.strip()
    neg = '(' in s or '-' in s.replace('$', '').strip()[:1]
    v = re.sub(r'[^\d.]', '', s)
    if v in ('', '.'):
        return 0.0
    v = float(v)
    return -v if neg else v


def unit_id(name):
    n = name.lower()
    if 'total' == n.strip():
        return '__STATE_TOTAL__'
    if 'perryville' in n or 'hollywood' in n:
        return 'MD_HOLLYWOOD_PERRYVILLE'
    if 'ocean downs' in n:
        return 'MD_OCEAN_DOWNS'
    if 'rocky gap' in n:
        return 'MD_ROCKY_GAP'
    if 'horseshoe' in n or 'horshoe' in n:
        return 'MD_HORSESHOE_BALTIMORE'
    if 'mgm' in n or 'national harbor' in n:
        return 'MD_MGM_NATIONAL_HARBOR'
    if 'live' in n:
        return 'MD_LIVE'
    raise ValueError('unknown casino ' + name)


def clean_name(s):
    s = re.sub(r'\s+', ' ', s).strip(' -–%')
    return s


TITLE = re.compile(r'(VLT Gaming|Table Games?|Slot Machine)\s+Revenue\s*[–-]\s*')


def parse_sections_html(t):
    """HTML-era tables. Returns {(kind, uid): (name, value)}."""
    res = {}
    ms = list(TITLE.finditer(t))
    for i, m in enumerate(ms):
        end = ms[i + 1].start() if i + 1 < len(ms) else len(t)
        sec = t[m.end():end]
        # name ends at '%' or a month name or 'Calendar'
        mm = re.search(r'\s*(%|\b(?:' + '|'.join(MONTHS) + r')\b|Calendar|Number of)', sec, re.I)
        name = clean_name(sec[:mm.start()] if mm else sec[:40])
        kind = 'vlt' if m.group(1).startswith(('VLT', 'Slot')) else 'tg'
        uid = unit_id(name)
        g = re.search(r'Gross Terminal Revenue[^$(]*?(' + AMT + ')', sec)
        nb = re.search(r'Non-?\s?bank(?:ed|ing)\s+(?:Games|Tables)[^$(]{0,25}?(' + AMT + ')', sec, re.I)
        b = re.search(r'(?<!Non-)(?<!Non)\bbank(?:ed|ing)\s+(?:Games|Tables)[^$(]{0,25}?(' + AMT + ')', sec, re.I)
        tot = re.search(r'\bTotal\s+(' + AMT + ')', sec, re.I)
        if kind == 'vlt' and g:
            val = money(g.group(1))
        elif kind == 'tg' and (nb or b):
            val = (money(nb.group(1)) if nb else 0) + (money(b.group(1)) if b else 0)
        elif g:
            val = money(g.group(1))
        elif tot:
            val = money(tot.group(1))
        else:
            continue
        if (kind, uid) not in res:
            res[(kind, uid)] = (name, val)
    return res


def parse_pdf_pages(path):
    res = {}
    d = pymupdf.open(path)
    for page in d:
        t = page.get_text()
        tt = re.sub(r'[ \t]+', ' ', t)
        m = re.search(r'(VLT Gaming|Table Games?|Slot Machine)\s+Revenue\s*[–-]\s*([^\n]+)', tt)
        if not m:
            continue
        name = clean_name(m.group(2))
        kind = 'vlt' if m.group(1).startswith(('VLT', 'Slot')) else 'tg'
        uid = unit_id(name)
        flat = re.sub(r'\s+', ' ', t)
        g = re.search(r'Gross Terminal Revenue[^$(]*?(' + AMT + ')', flat)
        if not g:
            continue
        res[(kind, uid)] = (name, money(g.group(1)))
    return res


def parse_worksheet(path, month_label):
    """2026+ worksheet PDFs: page 1 slots, page 2 tables."""
    res = {}
    d = pymupdf.open(path)
    for pno, page in enumerate(d):
        lines = [l.strip() for l in page.get_text().splitlines()]
        head = ' '.join([l for l in lines if l][:8]).upper()
        kind = 'vlt' if 'SLOT' in head else ('tg' if 'TABLE' in head else None)
        if kind is None:
            continue
        ml = month_label.lower().replace(' ', '')
        for i in range(1, len(lines)):
            if lines[i].lower().replace(' ', '') != ml:
                continue
            name = clean_name(lines[i - 1])
            if name.lower().startswith('total'):
                name, uid = 'Total', '__STATE_TOTAL__'
            else:
                uid = unit_id(name)
            vals = []
            for l in lines[i + 1:i + 16]:
                if re.fullmatch(AMT, l):
                    vals.append(money(l))
                elif l.lower().replace(' ', '') == ml or 'to date' in l.lower():
                    break
            if kind == 'vlt':
                v = vals[1] if uid != '__STATE_TOTAL__' else vals[0]
            else:
                v = vals[4] if uid != '__STATE_TOTAL__' else vals[2]
            res[(kind, uid)] = (name, v)
        # total rows are labelled "Total August 2026" / "TOTAL August 2026" on one line
        for i, l in enumerate(lines):
            if re.fullmatch(r'total\s*' + re.escape(ml), l.replace(' ', ''), re.I):
                vals = [money(x) for x in lines[i + 1:i + 12] if re.fullmatch(AMT, x)]
                res[(kind, '__STATE_TOTAL__')] = ('Total', vals[0] if kind == 'vlt' else vals[2])
    return res


def parse_narrative_early(t):
    """2012-01..05: '<casino> generated $X' sentences + statewide total."""
    res = {}
    for m in re.finditer(r'(Hollywood Casino Perryville|Casino at Ocean Downs|Ocean Downs)\s+generated\s+(' + AMT + ')', t):
        name = clean_name(m.group(1)); uid = unit_id(name)
        if ('vlt', uid) not in res:
            res[('vlt', uid)] = (name, money(m.group(2)))
    m = re.search(r'statewide revenue totaled\s+(' + AMT + ')', t)
    if m:
        res[('vlt', '__STATE_TOTAL__')] = ('Total', money(m.group(1)))
    return res


def headline_total(t):
    """First full-dollar amount (>= $1,000,000, not '$x.x million') in the release = statewide month total."""
    for m in re.finditer(r'\$\s*(\d{1,3}(?:,\d{3}){2,}(?:\.\d\d)?)(?!\d)(?!\s*million)', t):
        return float(m.group(1).replace(',', ''))
    return None


def month_of_post(p):
    d = date.fromisoformat(p['date'][:10])
    y, m = (d.year, d.month - 1) if d.month > 1 else (d.year - 1, 12)
    title = html.unescape(p['title']['rendered']).lower()
    for i, mn in enumerate(MONTHS):
        if re.search(r'during\s+' + mn, title) or re.search(r'in\s+' + mn, title):
            if i + 1 != m:
                print('WARN month mismatch', p['date'], title)
    return f'{y:04d}-{m:02d}'


def main():
    posts = download()
    rows, checks = [], []
    seen = set()
    for p in sorted(posts, key=lambda x: x['date']):
        month = month_of_post(p)
        if month < '2012-01' or month in seen:
            continue
        seen.add(month)
        pub = p['date'][:10]
        pub_src = 'press_release'
        content = p['content']['rendered']
        t = text_of(content)
        links = pdf_links(content)
        y, mo = int(month[:4]), int(month[5:])
        label = f'{MONTHS[mo - 1].capitalize()} {y}'
        src = f"{p['_file']}#post{p['id']}"
        if month in ('2020-04', '2020-05'):
            res = {}  # closure
        elif month < '2012-06':
            res = parse_narrative_early(t)
        elif links:
            fn = links[0][1]
            path = os.path.join(CACHE, fn)
            src = fn
            if 'Worksheet' in fn:
                res = parse_worksheet(path, label)
            else:
                res = parse_pdf_pages(path)
            # WordPress dates of some releases (esp. Nov 2017 - Apr 2018, re-posted after the 2018 site
            # move) are later than the attached PDF's creation date; if the PDF was created within 45 days
            # after month end and > 3 days before the post date, the PDF date is taken instead.
            cm = re.search(r'D:(\d{8})', pymupdf.open(path).metadata.get('creationDate') or '')
            if cm:
                cdate = date(int(cm.group(1)[:4]), int(cm.group(1)[4:6]), int(cm.group(1)[6:]))
                mend = (pd.Timestamp(month + '-01') + pd.offsets.MonthEnd(0)).date()
                if 0 < (cdate - mend).days <= 45 and (date.fromisoformat(pub) - cdate).days > 3:
                    pub, pub_src = cdate.isoformat(), 'pdf_metadata'
        else:
            res = parse_sections_html(t)
        units = {}
        for (kind, uid), (name, v) in res.items():
            if uid == '__STATE_TOTAL__':
                continue
            u = units.setdefault(uid, {'unit': None, 'vlt': None, 'tg': None})
            u[kind] = v
            if kind == 'vlt' or u['unit'] is None:
                u['unit'] = name
        if month in ('2020-04', '2020-05'):
            prev = [r for r in rows if r['month'] == '2020-03' and r['unit_level'] == 'property']
            for r in prev:
                units[r['unit_id']] = {'unit': r['unit'], 'vlt': 0.0, 'tg': 0.0}
        tot_v = res.get(('vlt', '__STATE_TOTAL__'), (None, None))[1]
        tot_t = res.get(('tg', '__STATE_TOTAL__'), (None, None))[1]
        for uid, u in sorted(units.items()):
            ggr = (u['vlt'] or 0) + (u['tg'] or 0)
            rows.append(dict(state='MD', unit=u['unit'], unit_id=uid, unit_level='property', month=month,
                             ggr=round(ggr, 2), slots=u['vlt'], tables=u['tg'], n_casinos=None,
                             measure='GGR', pub_date=pub, pub_source=pub_src, source_file=src))
        s = sum((u['vlt'] or 0) + (u['tg'] or 0) for u in units.values())
        head = headline_total(t)
        pages = (tot_v + (tot_t or 0)) if tot_v is not None else None
        note = []
        closed = month in ('2020-04', '2020-05')
        if closed:
            state_total, st_s, st_t = 0.0, 0.0, 0.0
            note.append('casinos closed (COVID)')
        else:
            # regulator statewide total: the agency's statewide "Total" tables (slots + tables); the
            # headline number of the release (first full-dollar amount) is used when no Total tables
            # exist, or when the Total tables disagree with the casinos while the headline agrees
            # (= typo in the Total table).
            st_s, st_t = tot_v, tot_t
            rel = lambda a, b: abs(a - b) / b if b else 1.0
            if pages is None:
                state_total = head
                note.append('regulator_total=headline')
            elif head is not None and rel(s, pages) > 1e-4 and rel(s, head) < 1e-4:
                state_total = head
                st_s = st_t = None
                note.append(f'agency Total tables {pages:,.2f} disagree with casinos ({(s - pages) / pages * 100:+.2f}%) '
                            f'but headline {head:,.0f} agrees: typo in regulator Total table; regulator_total=headline')
            else:
                state_total = pages
                note.append('regulator_total=Total tables')
                if head is not None:
                    note.append(f'headline diff {(s - head) / head * 100:+.3f}%')
        rows.append(dict(state='MD', unit='__STATE_TOTAL__', unit_id='MD__STATE_TOTAL__', unit_level='state_total',
                         month=month, ggr=state_total, slots=st_s, tables=st_t,
                         n_casinos=len(units), measure='GGR', pub_date=pub, pub_source=pub_src,
                         source_file=src))
        checks.append(dict(month=month, sum_of_units=round(s, 2), regulator_total=state_total,
                           diff_pct=(round((s - state_total) / state_total * 100, 4) if state_total else 0.0 if closed else None),
                           note='; '.join(note)))
    df = pd.DataFrame(rows)
    ck = pd.DataFrame(checks)
    # sanity checks
    assert not df.duplicated(['unit_id', 'month']).any()
    prop = df[df.unit_level == 'property'].sort_values(['unit_id', 'month'])
    prop['prev'] = prop.groupby('unit_id').ggr.shift()
    prop['ratio'] = prop.ggr / prop.prev
    odd = prop[((prop.ratio > 3) | (prop.ratio < 1 / 3)) & ~prop.month.between('2020-03', '2020-07')]
    print('jumps >3x or <1/3 outside COVID:')
    print(odd[['unit_id', 'month', 'prev', 'ggr']].to_string())
    print('checks: n', len(ck), 'max |diff| %', ck.diff_pct.abs().max())
    print(ck[ck.diff_pct.abs() > 0.01].to_string())
    print('months', df.month.min(), df.month.max(), 'n months', df.month.nunique())
    df.to_csv(os.path.join(DATA, 'state_md.csv.gz'), index=False, compression='gzip')
    ck.to_csv(os.path.join(DATA, 'state_md_checks.csv.gz'), index=False, compression='gzip')
    return df, ck


if __name__ == '__main__':
    main()
