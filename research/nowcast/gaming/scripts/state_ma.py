"""Massachusetts monthly casino gaming revenue by casino (2015-06 .. latest), Mass. Gaming Commission.

Sources
-------
* Massachusetts Gaming Commission (MGC), https://massgaming.com/regulations/revenue/ . Every month
  the MGC uploads one PDF per casino, e.g.
    https://massgaming.com/wp-content/uploads/Revenue-Plainridge-Park-Casino-August-2026.pdf
    https://massgaming.com/wp-content/uploads/Revenue-MGM-Springfield-August-2026.pdf
    https://massgaming.com/wp-content/uploads/Revenue-Encore-Boston-Harbor-August-2026.pdf
  Each PDF is cumulative: every month since the casino opened (coin in, slot GGR, hold, table GGR,
  total GGR, taxes). The newest file per casino supplies the whole series.
* The list of all uploaded revenue PDFs and their upload dates comes from the site's public
  WordPress media API: https://massgaming.com/wp-json/wp/v2/media?search=revenue&per_page=100&page=N
  (cached as cache/ma/media_revenue_p{N}.json).
* Statewide totals: the combined monthly "MGC Revenue Report" PDF (MGC-Revenue-Report-<Month>-<Year>.pdf
  and older names, from June 2023), page 1 casino table, column "TABLE AND SLOTS GGR", TOTAL row.
* Older per-casino files ("Revenue-Report-<m>-<yyyy>.pdf", "Revenue-PPC-<m>-<yyyy>.pdf",
  "Revenue-MGM-..", "Revenue-Encore-..") are downloaded for December of each year 2015-2022 as
  vintage checks (see Spot checks).
All PDFs cached in cache/ma/ under their original file names.

Measure
-------
GGR (slot GGR + table GGR, "Total Slot and Table GGR"); dollars. Plainridge Park is a slots-only
(Category 2) casino, tables blank. Sports wagering (separate "Cat. 1/Cat. 3 Sports Wagering" reports and
the sports lines of the combined report) and daily fantasy are excluded.

Units
-----
MA_PLAINRIDGE_PARK   "Plainridge Park Casino" (Penn National/PENN), opened 2015-06-24 (June = 7 days)
MA_MGM_SPRINGFIELD   "MGM Springfield", opened 2018-08-24 (Aug = 8 days)
MA_ENCORE_BOSTON     "Encore Boston Harbor" (Wynn), opened 2019-06-23 (June = 8 days)
No renames.

Publication date
----------------
pub_date = upload date (WordPress media "date") of that month's first per-casino revenue PDF (or the
combined report / early "Revenue-Report-m-d-yy" file when earlier); pub_source = listing_page (dated
media listing of the regulator's site). Revised re-uploads are ignored. A file is assigned to the month
in its name only if that is 1-2 months before the upload month, else to upload month - 1 (some names
are wrong, e.g. Feb 2019 data uploaded 2019-03-15 as "Revenue-Report-PPC-3-2019.pdf"). 2020-01 has no
upload in the media listing -> blank. Typical lag ~15-22 days
after month end (mid-month through 2024, ~20th from 2025; e.g. Aug 2026 uploaded 2026-09-21).

Quirks
------
* COVID-19: all casinos closed 2020-03-15 and reopened July 2020; April-June 2020 are 0.
* Month labels in the PDFs often omit the year ("August", "September", ...); the year is carried
  forward and incremented when the month number wraps.
* __STATE_TOTAL__: 2015-06..2018-07 Plainridge was the only casino, so the regulator's Plainridge
  report is the statewide total (note in checks); 2018-08..2023-05 the MGC published no statewide
  figure in these files -> ggr blank; 2023-06 onward from the combined MGC Revenue Report.

Spot checks (run 2026-09-23; data/state_ma_checks.csv.gz)
----------------------------------------------------------
* vs the combined MGC Revenue Report, 39 months 2023-06..2026-08: 35 exact (0.000%); the 4 others
  are errors/revisions on the regulator side, each noted in the checks file:
  2023-09 +3.78% (MGM Springfield first published as an estimate, "slots from CMS, table games
  through 9/6" during MGM's cyber incident, $17.44m; revised to $20.86m in the casino file);
  2026-01 +0.07% (Plainridge revised +$64k after the combined report);
  2026-06 -3.24% (combined report TOTAL does not equal the sum of its own casino rows; the rows
  equal ours); 2026-07 +2.84% (combined report repeats Encore's June figure).
* Vintage check: 91 casino-months (every month in the December 2015-2022 per-casino files as first
  published) equal the newest cumulative files to 0.000% -> no silent revisions before 2023.
* No month/month jumps > 3x outside COVID (openings are partial months but not > 3x jumps).
"""
import os, re, sys, time, json
from datetime import date, datetime
import requests
import pandas as pd
import numpy as np
import pymupdf

ROOT = '/Users/davidspinelli/Documents/Claude Space/research/nowcast/gaming'
CACHE = os.path.join(ROOT, 'cache', 'ma')
DATA = os.path.join(ROOT, 'data')
UA = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
                    '(KHTML, like Gecko) Chrome/124.0 Safari/537.36'}
S = requests.Session(); S.headers.update(UA)
MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september',
          'october', 'november', 'december']
CASINOS = {'MA_PLAINRIDGE_PARK': ('Plainridge Park Casino', r'(Plainridge-Park-Casino|PPC)'),
           'MA_MGM_SPRINGFIELD': ('MGM Springfield', r'MGM'),
           'MA_ENCORE_BOSTON': ('Encore Boston Harbor', r'Encore')}


def get(url, tries=4):
    for a in range(tries):
        try:
            time.sleep(0.8)
            r = S.get(url, timeout=120)
            if r.status_code == 200:
                return r
            print('HTTP', r.status_code, url)
            if r.status_code == 404:
                return None
        except Exception as e:
            print('err', e)
        time.sleep(10 * (a + 1))
    return None


def media_list():
    os.makedirs(CACHE, exist_ok=True)
    out, pg, tp = [], 1, 1
    while pg <= tp:
        p = os.path.join(CACHE, f'media_revenue_p{pg}.json')
        if pg == 1 and os.path.exists(p) and time.time() - os.path.getmtime(p) > 7 * 86400:
            for f in os.listdir(CACHE):
                if f.startswith('media_revenue_p'):
                    os.remove(os.path.join(CACHE, f))
        if not os.path.exists(p):
            r = get(f'https://massgaming.com/wp-json/wp/v2/media?search=revenue&per_page=100&page={pg}'
                    '&_fields=id,date,slug,source_url,mime_type')
            json.dump({'total_pages': int(r.headers.get('X-WP-TotalPages', 1)), 'items': r.json()}, open(p, 'w'))
        d = json.load(open(p))
        tp = d['total_pages']
        out += d['items']
        pg += 1
    return out


def fetch(url):
    fn = url.split('/')[-1]
    p = os.path.join(CACHE, fn)
    if not os.path.exists(p):
        r = get(url)
        if r is None:
            return None
        open(p, 'wb').write(r.content)
    return fn


def month_from_name(fn, upload):
    """Month a revenue PDF reports on: from 'Month-YYYY' or 'm-YYYY' in the name, else upload month - 1."""
    b = fn.lower()
    m = re.search(r'(' + '|'.join(MONTHS) + r')-?(\d{4})?', b)
    if m and m.group(2):
        return f'{int(m.group(2)):04d}-{MONTHS.index(m.group(1)) + 1:02d}'
    m = re.search(r'-(\d{1,2})-(20\d\d)\.pdf$', b)
    if m:
        return f'{int(m.group(2)):04d}-{int(m.group(1)):02d}'
    m = re.search(r'-(\d{1,2})\.(\d\d)\.pdf$', b)  # Encore-Revenue-4.20.pdf
    if m:
        return f'20{m.group(2)}-{int(m.group(1)):02d}'
    m = re.search(r'(\d{1,2})\.1\.(20\d\d)-', b)  # MGM-Revenue-3.1.2020-3.15.2020.pdf
    if m:
        return f'{m.group(2)}-{int(m.group(1)):02d}'
    d = pd.Timestamp(upload[:10]).replace(day=1) - pd.Timedelta(days=1)
    return f'{d.year:04d}-{d.month:02d}'


MLAB = re.compile(r'^\W*(' + '|'.join(MONTHS) + r')\b[^$]*$', re.I)


def money(s):
    s = s.replace('$', '').replace(',', '').strip()
    neg = s.startswith('(') or s.startswith('-')
    s = s.strip('()-').strip()
    if s in ('', 'N/A'):
        return None
    return -float(s) if neg else float(s)


def parse_casino_pdf(fn):
    """Cumulative per-casino report -> DataFrame(month, slots, tables, ggr)."""
    d = pymupdf.open(os.path.join(CACHE, fn))
    tk = [x.strip() for pg in d for x in pg.get_text().split('\n') if x.strip()]
    rows, year, prev_m = [], None, None
    i = 0
    while i < len(tk):
        t = tk[i]
        m = MLAB.match(t)
        if not m:
            i += 1
            continue
        mn = MONTHS.index(m.group(1).lower()) + 1
        y = re.search(r'(20\d\d)', t)
        if y:
            year = int(y.group(1))
        elif prev_m is not None and mn <= prev_m:
            year += 1
        if year is None:
            i += 1
            continue
        vals = []
        j = i + 1
        while j < len(tk) and not MLAB.match(tk[j]) and len(vals) < 12:
            if tk[j].startswith('$') or tk[j].startswith('($') or tk[j].startswith('-$'):
                vals.append(money(tk[j]))
            elif re.search(r'[A-Za-z]{4,}', tk[j]) and not re.fullmatch(r'N/A', tk[j]) and 'FY' not in tk[j]:
                break
            j += 1
        if len(vals) >= 3:
            rows.append(dict(month=f'{year:04d}-{mn:02d}', vals=vals, label=t))
            prev_m = mn
        i = j
    return rows


def casino_series(fn, uid):
    out = []
    for r in parse_casino_pdf(fn):
        v = r['vals']
        if uid == 'MA_PLAINRIDGE_PARK':
            slots, tables = v[1], np.nan
            ggr = slots
        else:
            slots, tables, ggr = v[1], v[2], v[3]
            if abs(slots + tables - ggr) > 1.0:
                print('WARN slot+table != total', fn, r['month'], v[:4])
        out.append(dict(month=r['month'], slots=slots, tables=tables, ggr=ggr))
    df = pd.DataFrame(out).drop_duplicates('month', keep='last')
    return df


def combined_total(fn):
    """TOTAL of the 'TABLE AND SLOTS GGR' column on page 1 of the combined MGC Revenue Report."""
    d = pymupdf.open(os.path.join(CACHE, fn))
    W = d[0].get_text('words')
    hdr = None
    for i in range(len(W) - 3):
        if [w[4].upper() for w in W[i:i + 4]] == ['TABLE', 'AND', 'SLOTS', 'GGR']:
            hdr = (W[i][0], W[i + 3][2], W[i][3])
            break
    if hdr is None:
        return None, None
    x0, x1, y = hdr
    foot = [w[1] for w in W if w[4].upper() in ('TOTAL', 'COLLECTED') and w[1] > y + 150]
    ymax = min(foot) if foot else 1e9
    col = [w for w in W if w[4].startswith('$') and w[0] >= x0 - 120 and w[2] <= x1 + 120 and y < w[1] < ymax + 60]
    col = sorted(col, key=lambda w: w[1])
    if len(col) < 2:
        return None, None
    vals = [money(w[4]) for w in col]
    return vals[-1], vals[:-1]


def main():
    media = media_list()
    media = [m for m in media if m['source_url'].lower().endswith('.pdf')]
    for m in media:
        m['fn'] = m['source_url'].split('/')[-1]
    casino_media = [m for m in media if not re.search(r'sports|wagering|dfs|rhdf|cat\.|attachment|actuals|analysis|city-of|lottery',
                                                       m['fn'], re.I)]
    # publication date per month = earliest non-revised upload of a revenue report for that month
    pub = {}
    for m in casino_media:
        if re.search(r'revised|trueup', m['fn'], re.I):
            continue
        # file names are occasionally wrong (e.g. Feb-2019 data uploaded 2019-03-15 as "...-3-2019"), so the
        # name's month is used only if it is 1-2 months before the upload month; otherwise upload month - 1
        up = pd.Timestamp(m['date'][:10]).replace(day=1)
        up1 = (up - pd.Timedelta(days=1)).strftime('%Y-%m')
        up2 = (up - pd.Timedelta(days=32)).strftime('%Y-%m')
        mo = month_from_name(m['fn'], m['date'])
        if mo not in (up1, up2):
            mo = up1
        d = m['date'][:10]
        if mo not in pub or d < pub[mo][0]:
            pub[mo] = (d, m['fn'])
    # newest cumulative file per casino
    series = {}
    for uid, (name, pat) in CASINOS.items():
        cands = [m for m in casino_media if re.search(pat, m['fn']) and re.match(r'(Revenue-|.*-Revenue-)', m['fn'])
                 and not re.search(r'revised', m['fn'], re.I) and 'MGC' not in m['fn']]
        newest = max(cands, key=lambda m: (m['date'], m['fn']))
        fn = fetch(newest['source_url'])
        df = casino_series(fn, uid)
        df['unit_id'], df['unit'], df['src'] = uid, name, fn
        series[uid] = df
        print(uid, fn, df.month.min(), df.month.max(), len(df))
    units = pd.concat(series.values())
    # statewide totals from the combined MGC Revenue Reports (June 2023 on)
    comb = {}
    for m in casino_media:
        if not re.search(r'(MGC-.*Revenue-Report|Revenue-Report-Final|Rev-Report|Revenue-Report-Final-Copy)', m['fn']):
            continue
        if re.match(r'Revenue-Report-\d', m['fn']):
            continue
        mo = month_from_name(m['fn'], m['date'])
        if mo < '2023-01':
            continue
        fn = fetch(m['source_url'])
        tot, parts = combined_total(fn)
        if tot is None:
            print('no total parsed', fn)
            continue
        # keep the latest (revised) upload of a month
        if mo not in comb or m['date'] > comb[mo][2]:
            comb[mo] = (tot, fn, m['date'], parts)
    # vintage checks: December files of each year 2015-2022
    vint = {}
    for m in casino_media:
        mo = month_from_name(m['fn'], m['date'])
        if not (mo.endswith('-12') and mo <= '2022-12') or 'MGC' in m['fn'] or re.search(r'revised', m['fn'], re.I):
            continue
        uid = next((u for u, (n, pat) in CASINOS.items() if re.search(pat, m['fn'])), 'MA_PLAINRIDGE_PARK')
        fn = fetch(m['source_url'])
        try:
            df = casino_series(fn, uid)
        except Exception as e:
            print('vintage parse fail', fn, e); continue
        for _, r in df.iterrows():
            vint.setdefault((uid, r.month), (r.ggr, fn))
    rows, checks = [], []
    months = sorted(units.month.unique())
    for mo in months:
        d = units[units.month == mo]
        pdv, pfn = pub.get(mo, ('', ''))
        for _, r in d.iterrows():
            rows.append(dict(state='MA', unit=r.unit, unit_id=r.unit_id, unit_level='property', month=mo,
                             ggr=r.ggr, slots=r.slots, tables=r.tables, n_casinos=np.nan, measure='GGR',
                             pub_date=pdv, pub_source='listing_page' if pdv else '', source_file=r.src))
        s = d.ggr.sum()
        note = ''
        if mo in comb:
            tot, cfn, _, parts = comb[mo]
            note = f'regulator_total = combined MGC Revenue Report ({cfn})'
            if len(parts) == 3:
                own = [d[d.unit_id == u].ggr.sum() for u in ('MA_ENCORE_BOSTON', 'MA_MGM_SPRINGFIELD', 'MA_PLAINRIDGE_PARK')]
                bad = [f'{u} {pv:,.2f} vs casino report {ov:,.2f}' for u, pv, ov in
                       zip(('EBH', 'MGM', 'PPC'), parts, own) if abs(pv - ov) > 1]
                if bad:
                    note += '; combined report casino rows differ: ' + ', '.join(bad)
                if abs(sum(parts) - tot) > 1:
                    note += f'; combined report TOTAL {tot:,.2f} != sum of its own casino rows {sum(parts):,.2f} (regulator arithmetic error)'
        elif mo < '2018-08':
            tot, cfn = s, d.src.iloc[0]
            note = 'Plainridge only casino: its regulator report is the statewide total'
        else:
            tot, cfn = np.nan, ''
        rows.append(dict(state='MA', unit='__STATE_TOTAL__', unit_id='MA__STATE_TOTAL__', unit_level='state_total',
                         month=mo, ggr=tot, slots=np.nan, tables=np.nan, n_casinos=len(d), measure='GGR',
                         pub_date=pdv, pub_source='listing_page' if pdv else '', source_file=cfn))
        vv = [vint.get((u, mo)) for u in d.unit_id]
        if all(v is not None for v in vv) and len(vv):
            vs = sum(v[0] for v in vv)
            note += ('; ' if note else '') + f'vintage check vs casino reports as published in {sorted(set(v[1] for v in vv))}: {(s - vs) / vs * 100 if vs else 0:+.4f}%'
        checks.append(dict(month=mo, sum_of_units=round(s, 2), regulator_total=tot,
                           diff_pct=round((s - tot) / tot * 100, 4) if pd.notna(tot) and tot else (0.0 if tot == 0 else np.nan),
                           note=note))
    df = pd.DataFrame(rows)
    ck = pd.DataFrame(checks)
    assert not df.duplicated(['unit_id', 'month']).any()
    prop = df[df.unit_level == 'property'].sort_values(['unit_id', 'month']).copy()
    prop['prev'] = prop.groupby('unit_id').ggr.shift()
    prop['ratio'] = prop.ggr / prop.prev
    odd = prop[((prop.ratio > 3) | (prop.ratio < 1 / 3)) & ~prop.month.between('2020-03', '2020-08')]
    print('jumps:'); print(odd[['unit_id', 'month', 'prev', 'ggr']].to_string())
    real = ck[ck.note.str.contains('combined')]
    print('combined-report checks n', len(real), 'max |diff| %', real.diff_pct.abs().max())
    print(ck[ck.diff_pct.abs() > 0.01].to_string())
    vc = ck[ck.note.str.contains('vintage')].copy()
    vc['vd'] = vc.note.str.extract(r'vintage[^:]*: ([+-][\d.]+)%').astype(float)
    print('vintage checks n', len(vc), 'max |diff| %', vc.vd.abs().max())
    print(vc[vc.vd.abs() > 0.01][['month', 'vd']].to_string())
    print('months', df.month.min(), df.month.max())
    df.to_csv(os.path.join(DATA, 'state_ma.csv.gz'), index=False, compression='gzip')
    ck.to_csv(os.path.join(DATA, 'state_ma_checks.csv.gz'), index=False, compression='gzip')
    return df, ck


if __name__ == '__main__':
    main()
