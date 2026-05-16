"""
add_dest_tabs.py  (v4)

Layout:
- <=10 destinations  → flat pill row, no grouping
- >10 destinations   → continent buttons in a horizontal row;
  clicking a continent shows its country pills in a panel below the row.
  No vertical expansion, no emojis, clean design.
"""
import os, re

COUNTRIES_DIR = r"c:\Users\User\Desktop\Freelancing\WorkHoliday\countries"

TABS_CSS = """\
    <style id="dest-tabs-css">
    .wh-nav-wrap {
        margin-bottom: 2rem;
        padding-bottom: 1.5rem;
        border-bottom: 1.5px solid #eef1f5;
    }
    .wh-nav-label {
        font-size: .68rem;
        font-weight: 700;
        color: #bbb;
        text-transform: uppercase;
        letter-spacing: .1em;
        margin-bottom: .8rem;
    }

    /* flat pill row */
    .wh-pills {
        display: flex;
        flex-wrap: wrap;
        gap: .4rem;
    }

    /* continent selector row — indigo/navy palette */
    .wh-cont-row {
        display: flex;
        flex-wrap: wrap;
        gap: .5rem;
        margin-bottom: .75rem;
    }
    .wh-cont-btn {
        display: inline-flex;
        align-items: center;
        gap: .45rem;
        padding: .48rem 1.2rem;
        border-radius: 8px;
        font-size: .78rem;
        font-weight: 600;
        color: #3d4f6e;
        background: #eef1f8;
        border: 1.5px solid #c8d3e8;
        cursor: pointer;
        transition: background .13s, color .13s, border-color .13s, box-shadow .13s;
        white-space: nowrap;
        letter-spacing: .01em;
    }
    .wh-cont-btn:hover {
        background: #dde4f5;
        border-color: #9aadd4;
        color: #1f3361;
    }
    .wh-cont-btn.wh-cont-active {
        background: #2d4fa3;
        color: #fff;
        border-color: #2d4fa3;
        box-shadow: 0 3px 12px rgba(45,79,163,.25);
    }
    .wh-cont-count {
        font-size: .67rem;
        font-weight: 600;
        background: rgba(0,0,0,.1);
        border-radius: 99px;
        padding: .05rem .45rem;
        line-height: 1.5;
    }
    .wh-cont-btn.wh-cont-active .wh-cont-count {
        background: rgba(255,255,255,.22);
    }

    /* country pills panel — shown/hidden via JS */
    .wh-country-panel {
        display: none;
        flex-wrap: wrap;
        gap: .4rem;
        margin-top: .65rem;
        padding-top: .65rem;
        border-top: 1px solid #eef1f5;
        animation: wh-fade-in .18s ease;
    }
    @keyframes wh-fade-in { from { opacity: 0; transform: translateY(-4px); } to { opacity: 1; transform: none; } }

    /* country pills — warm teal palette */
    .wh-pill {
        display: inline-flex;
        align-items: center;
        padding: .35rem .95rem;
        border-radius: 8px;
        font-size: .79rem;
        font-weight: 500;
        color: #2e6065;
        background: #eef8f8;
        border: 1.5px solid #b8dde0;
        cursor: pointer;
        white-space: nowrap;
        transition: background .13s, color .13s, border-color .13s, box-shadow .13s;
        text-decoration: none;
        line-height: 1.4;
    }
    .wh-pill:hover {
        background: #d6f0f2;
        color: #1a484c;
        border-color: #7fc5cb;
        box-shadow: 0 2px 6px rgba(30,120,130,.12);
        text-decoration: none;
    }
    .wh-pill.wh-active {
        background: #1a7a82;
        color: #fff;
        border-color: #1a7a82;
        font-weight: 600;
        box-shadow: 0 3px 10px rgba(26,122,130,.28);
    }

    /* content fade */
    #wh-content-panel { transition: opacity .18s; }
    #wh-content-panel.wh-loading { opacity: .3; pointer-events: none; }
    .wh-spinner {
        display: flex; justify-content: center; align-items: center; min-height: 180px;
    }
    .wh-spinner::after {
        content: ''; width: 32px; height: 32px;
        border: 3px solid #e0e0e0; border-top-color: #1a7a82;
        border-radius: 50%; animation: wh-spin .65s linear infinite;
    }
    @keyframes wh-spin { to { transform: rotate(360deg); } }
    </style>"""

TABS_PLACEHOLDER = '    <div id="wh-tabs-placeholder"></div>'

TABS_JS_TEMPLATE = """
    <script id="dest-tabs-js">
    (function () {{
        var ORIGIN   = {origin_js};
        var CURRENT  = {dest_js};
        var EXISTING = {existing_js};
        var REGION_ORDER = ['Asia-Pacific','Europe','Americas'];
        var REGION_LABEL = {{'Asia-Pacific':'Asia-Pacific','Europe':'Europe','Americas':'Americas'}};

        function slug(n) {{ return n === 'United States' ? 'USA' : n.replace(/ /g, '-'); }}

        var eligibility = (typeof WHV_ELIGIBILITY !== 'undefined') ? WHV_ELIGIBILITY[ORIGIN] : null;
        if (!eligibility) return;

        var regions = {{}}, total = 0;
        REGION_ORDER.forEach(function (r) {{
            var list = (eligibility[r] || []).filter(function (d) {{
                return EXISTING.indexOf(slug(ORIGIN) + '-to-' + slug(d)) !== -1;
            }}).sort(function (a, b) {{ return a.localeCompare(b); }});
            if (list.length) {{ regions[r] = list; total += list.length; }}
        }});
        if (total <= 1) return;

        var useGroups = total > 10 && Object.keys(regions).length > 1;

        var wrap = document.createElement('div');
        wrap.className = 'wh-nav-wrap';

        var lbl = document.createElement('div');
        lbl.className = 'wh-nav-label';
        lbl.textContent = 'Where can ' + ORIGIN + ' citizens go?';
        wrap.appendChild(lbl);

        var allPills = [];

        if (useGroups) {{
            /* ── GROUPED MODE: continent tabs, country pills hidden until clicked ── */
            var contRow = document.createElement('div');
            contRow.className = 'wh-cont-row';

            var countryPanel = document.createElement('div');
            countryPanel.className = 'wh-country-panel';
            countryPanel.style.display = 'none';   /* hidden by default */

            var openRegion = null;

            /* build pills per region */
            var regionPills = {{}};
            REGION_ORDER.forEach(function (r) {{
                if (!regions[r]) return;
                regionPills[r] = regions[r].map(function (dest) {{
                    var btn = document.createElement('button');
                    btn.className = 'wh-pill' + (dest === CURRENT ? ' wh-active' : '');
                    btn.textContent = dest;
                    btn.dataset.dest = dest;
                    btn.addEventListener('click', function () {{ loadDest(dest, btn); }});
                    allPills.push(btn);
                    return btn;
                }});
            }});

            function showRegion(r) {{
                if (openRegion === r) {{
                    /* clicking active continent again collapses it */
                    contRow.querySelectorAll('.wh-cont-btn').forEach(function (b) {{
                        b.classList.remove('wh-cont-active');
                    }});
                    countryPanel.style.display = 'none';
                    openRegion = null;
                    return;
                }}
                openRegion = r;
                contRow.querySelectorAll('.wh-cont-btn').forEach(function (b) {{
                    b.classList.toggle('wh-cont-active', b.dataset.region === r);
                }});
                countryPanel.innerHTML = '';
                (regionPills[r] || []).forEach(function (pill) {{
                    countryPanel.appendChild(pill);
                }});
                countryPanel.style.display = 'flex';
            }}

            /* find which region the current destination belongs to */
            var currentRegion = REGION_ORDER.find(function (r) {{
                return regions[r] && regions[r].indexOf(CURRENT) !== -1;
            }});

            REGION_ORDER.forEach(function (r) {{
                if (!regions[r]) return;
                var btn = document.createElement('button');
                btn.className = 'wh-cont-btn';
                btn.dataset.region = r;
                btn.innerHTML = REGION_LABEL[r] +
                    ' <span class="wh-cont-count">' + regions[r].length + '</span>';
                btn.addEventListener('click', function () {{ showRegion(r); }});
                contRow.appendChild(btn);
            }});

            wrap.appendChild(contRow);
            wrap.appendChild(countryPanel);

            /* highlight the current destination's continent but keep pills hidden */
            if (currentRegion) {{
                var activeContinentBtn = contRow.querySelector('[data-region="' + currentRegion + '"]');
                if (activeContinentBtn) activeContinentBtn.classList.add('wh-cont-active');
            }}

        }} else {{
            /* ── FLAT MODE: just pills ── */
            var row = document.createElement('div');
            row.className = 'wh-pills';
            REGION_ORDER.forEach(function (r) {{
                if (!regions[r]) return;
                regions[r].forEach(function (dest) {{
                    var btn = document.createElement('button');
                    btn.className = 'wh-pill' + (dest === CURRENT ? ' wh-active' : '');
                    btn.textContent = dest;
                    btn.dataset.dest = dest;
                    btn.addEventListener('click', function () {{ loadDest(dest, btn); }});
                    allPills.push(btn);
                    row.appendChild(btn);
                }});
            }});
            wrap.appendChild(row);
        }}

        var placeholder = document.getElementById('wh-tabs-placeholder');
        if (placeholder) placeholder.replaceWith(wrap);

        /* ── content swapping ── */
        var panel = document.getElementById('wh-content-panel');
        var cache = {{}};
        if (panel) cache[CURRENT] = panel.innerHTML;

        function loadDest(dest, btn) {{
            if (btn.classList.contains('wh-active')) return;
            allPills.forEach(function (p) {{ p.classList.remove('wh-active'); }});
            btn.classList.add('wh-active');

            if (history.pushState)
                history.pushState({{ dest: dest }}, '', slug(ORIGIN) + '-to-' + slug(dest) + '.html');
            document.title = 'TRAVELER - ' + dest + ' Work Holiday Visa for ' + ORIGIN + ' Citizens';
            var h1 = document.querySelector('.visa-hero h1');
            if (h1) h1.textContent = dest.toUpperCase() + ' WORK GUIDE';
            var p  = document.querySelector('.visa-hero .lead');
            if (p)  p.textContent  = 'Work & Residency Pathways for ' + ORIGIN + ' Citizens';
            var bc = document.querySelector('.breadcrumb-item.active');
            if (bc) bc.textContent = ORIGIN + ' to ' + dest;

            if (!panel) return;
            if (cache[dest]) {{ panel.innerHTML = cache[dest]; return; }}

            panel.classList.add('wh-loading');
            panel.innerHTML = '<div class="wh-spinner"></div>';

            fetch(slug(ORIGIN) + '-to-' + slug(dest) + '.html')
                .then(function (r) {{ return r.text(); }})
                .then(function (html) {{
                    var doc = new DOMParser().parseFromString(html, 'text/html');
                    var src = doc.getElementById('wh-content-panel');
                    var out = src ? src.innerHTML
                                  : '<p class="text-muted text-center py-4">Content unavailable.</p>';
                    cache[dest] = out;
                    panel.innerHTML = out;
                    panel.classList.remove('wh-loading');
                }})
                .catch(function () {{
                    panel.innerHTML = '<p class="text-muted text-center py-4">Could not load content.</p>';
                    panel.classList.remove('wh-loading');
                }});
        }}

        window.addEventListener('popstate', function (e) {{
            if (e.state && e.state.dest) {{
                var b = allPills.find(function (p) {{ return p.dataset.dest === e.state.dest; }});
                if (b) loadDest(e.state.dest, b);
            }}
        }});
    }})();
    </script>"""

# ── helpers ───────────────────────────────────────────────────────────────────
def slug_to_name(s):
    return 'United States' if s == 'USA' else s.replace('-', ' ')

def build_existing_set(d):
    return {f[:-5] for f in os.listdir(d) if f.endswith('.html')}

def strip_old(content):
    content = re.sub(r'\s*<style id="dest-tabs-css">.*?</style>', '', content, count=1, flags=re.DOTALL)
    content = re.sub(r'\s*<script id="dest-tabs-js">.*?</script>', '', content, count=1, flags=re.DOTALL)
    content = re.sub(r'\s*<!-- Destination Tabs Bar -->.*?<!-- Destination Tabs Bar End -->', '', content, count=1, flags=re.DOTALL)
    for old in [
        '\n    <div id="wh-tabs-placeholder"></div>\n            <div id="wh-content-panel">',
        '\n    <div id="wh-tabs-placeholder"></div>',
        '            </div><!-- /wh-content-panel -->\n',
        '<div id="dest-tabs-bar"></div>',
    ]:
        content = content.replace(old, '', 1)
    content = content.replace('<div id="dest-main-content">\n        <div class="bg-white', '<div class="bg-white', 1)
    content = content.replace('        </div><!-- /dest-main-content -->', '', 1)
    return content

def process_file(filepath, existing_set):
    filename = os.path.basename(filepath)
    m = re.match(r'^(.+?)-to-(.+?)\.html$', filename)
    if not m:
        return False
    origin = slug_to_name(m.group(1))
    dest   = slug_to_name(m.group(2))

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    content = strip_old(content)

    # CSS
    if 'dest-tabs-css' not in content:
        content = content.replace('</head>', TABS_CSS + '\n</head>', 1)

    # Placeholder + content panel inside white card
    card_open = '<div class="bg-white rounded-30 shadow-lg p-4 p-md-5">'
    if card_open in content and 'wh-tabs-placeholder' not in content:
        content = content.replace(
            card_open,
            card_open + '\n' + TABS_PLACEHOLDER + '\n            <div id="wh-content-panel">',
            1
        )
        content = content.replace(
            '    </div>\n\n    <!-- Main Content End -->',
            '            </div><!-- /wh-content-panel -->\n    </div>\n\n    <!-- Main Content End -->',
            1
        )

    # JS
    existing_for_origin = sorted([k for k in existing_set if k.startswith(m.group(1) + '-to-')])
    tabs_js = TABS_JS_TEMPLATE.format(
        origin_js=repr(origin),
        dest_js=repr(dest),
        existing_js=repr(existing_for_origin)
    )
    content = content.replace('</body>', tabs_js + '\n</body>', 1)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    return True

def main():
    existing_set = build_existing_set(COUNTRIES_DIR)
    files = sorted([f for f in os.listdir(COUNTRIES_DIR) if f.endswith('.html')])
    updated = skipped = 0
    for filename in files:
        if process_file(os.path.join(COUNTRIES_DIR, filename), existing_set):
            updated += 1
        else:
            skipped += 1
    print(f'Done. Updated: {updated}, Skipped: {skipped}')

if __name__ == '__main__':
    main()
