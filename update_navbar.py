import os
import re

BASE = r"c:\Users\User\Desktop\Freelancing\WorkHoliday\countries"

NAVBAR_CSS = """    <style>
        /* ---- Navbar Search Bar ---- */
        .navbar-search {
            display: flex;
            align-items: center;
            gap: 10px;
            flex: 1;
            justify-content: center;
            padding: 8px 0;
        }
        .navbar-search .nav-label {
            font-size: 0.9rem;
            font-weight: 600;
            color: #555;
            white-space: nowrap;
        }
        .navbar-search .cs-wrapper {
            min-width: 200px;
            max-width: 260px;
        }
        .navbar-search .select-wrapper {
            min-width: 200px;
            max-width: 260px;
        }
        .navbar-search .btn-nav-go {
            height: 48px;
            border-radius: 10px;
            font-weight: 700;
            font-size: 0.9rem;
            background: #7AB730;
            border: none;
            color: white;
            padding: 0 22px;
            white-space: nowrap;
            transition: background 0.3s;
        }
        .navbar-search .btn-nav-go:hover { background: #6aa128; }
        @media (max-width: 991.98px) {
            .navbar-search { flex-direction: column; gap: 10px; padding: 15px 0; }
            .navbar-search .cs-wrapper,
            .navbar-search .select-wrapper { min-width: 100%; max-width: 100%; }
        }
        /* ---- Searchable Dropdown ---- */
        .cs-wrapper { position: relative; flex: 1; min-width: 250px; }
        .cs-display {
            height: 48px;
            border-radius: 10px;
            border: 2px solid #f0f0f0;
            background-color: #f8fbff;
            font-family: 'Poppins', sans-serif;
            font-weight: 500;
            color: #444;
            cursor: pointer;
            padding: 0 38px 0 14px;
            display: flex;
            align-items: center;
            transition: all 0.3s ease;
            user-select: none;
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%237AB730' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
            background-repeat: no-repeat;
            background-position: right 10px center;
            background-size: 16px;
            font-size: 0.9rem;
        }
        .cs-display:hover, .cs-display.open {
            border-color: #7AB730;
            box-shadow: 0 0 0 3px rgba(122,183,48,0.15);
            background-color: #fff;
        }
        .cs-panel {
            position: absolute;
            top: calc(100% + 6px);
            left: 0; right: 0;
            background: #fff;
            border-radius: 12px;
            box-shadow: 0 20px 50px rgba(0,0,0,0.18);
            z-index: 99999;
            display: none;
            overflow: hidden;
            max-height: 300px;
            flex-direction: column;
            border: 1px solid #e8f5e9;
        }
        .cs-panel.open { display: flex; }
        .cs-search-wrap { padding: 10px 12px; border-bottom: 1px solid #f0f0f0; flex-shrink: 0; }
        .cs-search {
            width: 100%; height: 38px;
            border: 2px solid #e8f5e9; border-radius: 8px;
            padding: 0 12px;
            font-family: 'Poppins', sans-serif; font-size: 0.85rem;
            outline: none; transition: border-color 0.2s;
        }
        .cs-search:focus { border-color: #7AB730; }
        .cs-list { overflow-y: auto; flex: 1; }
        .cs-group-label {
            padding: 6px 14px 4px; font-size: 0.68rem; font-weight: 700;
            letter-spacing: 1px; color: #7AB730; text-transform: uppercase;
            background: #f9fff4; position: sticky; top: 0;
        }
        .cs-option {
            padding: 9px 16px; cursor: pointer;
            font-family: 'Poppins', sans-serif; font-size: 0.88rem; color: #444;
            transition: background 0.15s;
        }
        .cs-option:hover, .cs-option.highlighted { background: #f0fae5; color: #5a8a24; }
        .cs-option.active { background: #e6f4d5; font-weight: 600; color: #4a7a1e; }
        .cs-no-result { padding: 14px; text-align: center; color: #aaa; font-size: 0.88rem; }
        /* Destination select */
        .select-wrapper { flex: 1; min-width: 250px; position: relative; }
        .custom-select-premium {
            height: 48px !important;
            border-radius: 10px !important;
            border: 2px solid #f0f0f0 !important;
            background-color: #f8fbff !important;
            font-family: 'Poppins', sans-serif;
            font-weight: 500; color: #444 !important;
            transition: all 0.3s; cursor: pointer;
            appearance: none !important; -webkit-appearance: none !important;
            padding-right: 38px !important; font-size: 0.9rem !important;
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%237AB730' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E") !important;
            background-repeat: no-repeat !important;
            background-position: right 12px center !important;
            background-size: 16px !important;
        }
        .custom-select-premium:focus {
            border-color: #7AB730 !important;
            box-shadow: 0 0 0 3px rgba(122,183,48,0.15) !important;
            background-color: #fff !important; outline: none;
        }
    </style>"""

NAVBAR_HTML = """    <!-- Navbar Start -->
    <div class="container-fluid position-relative nav-bar p-0">
        <div class="container-lg position-relative p-0 px-lg-3" style="z-index: 9;">
            <nav class="navbar navbar-expand-lg bg-light navbar-light shadow-lg py-3 py-lg-0 pl-3 pl-lg-5">
                <a href="../index.html" class="navbar-brand">
                    <h1 class="m-0 text-primary"><span class="text-dark">TRAVEL</span>ER</h1>
                </a>
                <button type="button" class="navbar-toggler" data-toggle="collapse" data-target="#navbarCollapse">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse justify-content-between px-3" id="navbarCollapse">
                    <div class="navbar-search">
                        <span class="nav-label">From:</span>
                        <div class="cs-wrapper" id="originWrapper">
                            <select id="originSelect" style="display:none"></select>
                            <div class="cs-display" id="originDisplay" tabindex="0">Select country</div>
                            <div class="cs-panel" id="originPanel">
                                <div class="cs-search-wrap">
                                    <input class="cs-search" id="originSearch" type="text" placeholder="Search country..." autocomplete="off">
                                </div>
                                <div class="cs-list" id="originList"></div>
                            </div>
                        </div>
                        <span class="nav-label">To:</span>
                        <div class="select-wrapper">
                            <select id="destinationSelect" class="custom-select custom-select-premium px-4">
                                <option value="">Select destination</option>
                            </select>
                        </div>
                        <button id="submitBtn" class="btn btn-nav-go" type="button">
                            Go <i class="fa fa-arrow-right ml-1"></i>
                        </button>
                    </div>
                    <div class="navbar-nav ml-auto py-0">
                        <a href="../index.html" class="nav-item nav-link">Home</a>
                    </div>
                </div>
            </nav>
        </div>
    </div>
    <!-- Navbar End -->"""

NAVBAR_JS = """    <script src="../js/whv-data.js"></script>
    <script>
        const ALL_COUNTRIES = [
            "Afghanistan","Albania","Algeria","Andorra","Angola","Antigua and Barbuda","Argentina","Armenia",
            "Australia","Austria","Azerbaijan","Bahamas","Bahrain","Bangladesh","Barbados","Belarus","Belgium",
            "Belize","Benin","Bhutan","Bolivia","Bosnia and Herzegovina","Botswana","Brazil","Brunei","Bulgaria",
            "Cambodia","Cameroon","Canada","Cape Verde","Chile","Colombia","Costa Rica","Croatia","Cuba","Cyprus",
            "Czech Republic","Denmark","Djibouti","Dominican Republic","Ecuador","Egypt","El Salvador","Estonia",
            "Ethiopia","Finland","France","Georgia","Germany","Ghana","Greece","Guatemala","Honduras","Hong Kong",
            "Hungary","Iceland","India","Indonesia","Iran","Iraq","Ireland","Israel","Italy","Jamaica","Japan",
            "Jordan","Kazakhstan","Kenya","Kuwait","Latvia","Lebanon","Libya","Lithuania","Luxembourg","Macau",
            "Madagascar","Malaysia","Maldives","Malta","Mexico","Moldova","Monaco","Mongolia","Morocco",
            "Mozambique","Myanmar","Nepal","Netherlands","New Zealand","Nicaragua","Nigeria","North Korea",
            "Norway","Oman","Pakistan","Panama","Paraguay","Peru","Philippines","Poland","Portugal","Qatar",
            "Romania","Russia","Rwanda","San Marino","Saudi Arabia","Senegal","Serbia","Singapore","Slovakia",
            "Slovenia","Somalia","South Africa","South Korea","Spain","Sri Lanka","Sudan","Sweden","Switzerland",
            "Syria","Taiwan","Tanzania","Thailand","Trinidad and Tobago","Tunisia","Turkey","Uganda","Ukraine",
            "United Arab Emirates","United Kingdom","Uruguay","Uzbekistan","Venezuela","Vietnam","Zambia","Zimbabwe"
        ].sort((a, b) => a.localeCompare(b));

        const LANG_COUNTRY_MAP = {
            'de':['Germany','Austria','Switzerland','Luxembourg'],'fr':['France','Belgium','Switzerland','Luxembourg','Canada'],
            'es':['Spain','Mexico','Argentina','Colombia','Chile','Peru','Uruguay','Costa Rica'],
            'pt':['Portugal','Brazil'],'it':['Italy','Switzerland'],'nl':['Netherlands','Belgium'],
            'zh':['Mainland China','Taiwan','Hong Kong','Singapore'],'ja':['Japan'],'ko':['South Korea'],
            'pl':['Poland'],'sv':['Sweden'],'da':['Denmark'],'fi':['Finland'],'nb':['Norway'],'no':['Norway'],
            'el':['Greece'],'cs':['Czech Republic'],'sk':['Slovakia'],'hu':['Hungary'],'ro':['Romania'],
            'id':['Indonesia'],'ms':['Malaysia'],'th':['Thailand'],'vi':['Vietnam'],'hi':['India'],
        };
        function getLanguageHints() {
            const lang = (navigator.language || '').toLowerCase().split('-')[0];
            return LANG_COUNTRY_MAP[lang] || [];
        }

        const originSelect = document.getElementById('originSelect');
        const originDisplay = document.getElementById('originDisplay');
        const originPanel = document.getElementById('originPanel');
        const originSearch = document.getElementById('originSearch');
        const originList = document.getElementById('originList');
        const destinationSelect = document.getElementById('destinationSelect');
        let currentOrigin = '';

        function buildOriginList(filter) {
            originList.innerHTML = '';
            const q = (filter || '').trim().toLowerCase();
            const hints = getLanguageHints();
            if (!q && hints.length) {
                const pinned = hints.filter(c => ALL_COUNTRIES.includes(c));
                if (pinned.length) {
                    const grp = document.createElement('div');
                    grp.className = 'cs-group-label'; grp.textContent = '🌐 Suggested for you';
                    originList.appendChild(grp);
                    pinned.forEach(c => appendOriginOption(c));
                    const all = document.createElement('div');
                    all.className = 'cs-group-label'; all.textContent = 'All Countries';
                    originList.appendChild(all);
                }
            }
            const filtered = q ? ALL_COUNTRIES.filter(c => c.toLowerCase().includes(q)) : ALL_COUNTRIES;
            if (!filtered.length) {
                const d = document.createElement('div'); d.className = 'cs-no-result';
                d.textContent = 'No country found'; originList.appendChild(d); return;
            }
            filtered.forEach(c => appendOriginOption(c));
        }
        function appendOriginOption(country) {
            const item = document.createElement('div');
            item.className = 'cs-option' + (country === currentOrigin ? ' active' : '');
            item.textContent = country; item.dataset.value = country;
            item.addEventListener('mousedown', e => { e.preventDefault(); selectOrigin(country); });
            originList.appendChild(item);
        }
        function selectOrigin(country) {
            currentOrigin = country;
            originDisplay.textContent = country;
            originSelect.value = country;
            closeOriginPanel();
            updateDestinationOptions();
        }
        function openOriginPanel() {
            originDisplay.classList.add('open'); originPanel.classList.add('open');
            originSearch.value = ''; buildOriginList(''); originSearch.focus();
            const active = originList.querySelector('.active');
            if (active) active.scrollIntoView({ block: 'center' });
        }
        function closeOriginPanel() {
            originDisplay.classList.remove('open'); originPanel.classList.remove('open');
        }
        originDisplay.addEventListener('click', () => originPanel.classList.contains('open') ? closeOriginPanel() : openOriginPanel());
        originDisplay.addEventListener('keydown', e => {
            if (e.key === 'Enter' || e.key === ' ') openOriginPanel();
            if (e.key === 'Escape') closeOriginPanel();
        });
        originSearch.addEventListener('input', () => buildOriginList(originSearch.value));
        document.addEventListener('click', e => {
            if (!document.getElementById('originWrapper').contains(e.target)) closeOriginPanel();
        });

        function getCountryCode(name) {
            if (!name) return '';
            if (name === 'United States') return 'USA';
            return name.replace(/ /g, '-');
        }
        function navigate(origin, dest) {
            if (!origin || !dest) return;
            window.location.href = `../countries/${getCountryCode(origin)}-to-${getCountryCode(dest)}.html`;
        }
        function updateDestinationOptions() {
            destinationSelect.innerHTML = '<option value="">Select destination...</option>';
            const eligibility = WHV_ELIGIBILITY[currentOrigin];
            if (!eligibility || !Object.keys(eligibility).length) {
                const opt = document.createElement('option');
                opt.value = ''; opt.textContent = 'No eligible destinations'; opt.disabled = true;
                destinationSelect.appendChild(opt); return;
            }
            let total = 0, singleDest = null;
            Object.keys(eligibility).sort().forEach(continent => {
                const countries = [...(eligibility[continent] || [])].sort((a,b) => a.localeCompare(b));
                if (!countries.length) return;
                const optgroup = document.createElement('optgroup');
                optgroup.label = continent;
                countries.forEach(country => {
                    const opt = document.createElement('option');
                    opt.value = country; opt.textContent = country;
                    optgroup.appendChild(opt); total++; singleDest = country;
                });
                destinationSelect.appendChild(optgroup);
            });
            if (total === 1) navigate(currentOrigin, singleDest);
        }
        destinationSelect.addEventListener('change', () => {
            const dest = destinationSelect.value;
            if (dest) navigate(currentOrigin, dest);
        });
        document.getElementById('submitBtn').addEventListener('click', () => {
            if (!currentOrigin) { alert('Please select your citizenship country.'); return; }
            const dest = destinationSelect.value;
            if (!dest) { alert('Please select a destination country.'); return; }
            navigate(currentOrigin, dest);
        });

        // Auto geo-detect
        async function autoDetectLocation() {
            try {
                const res = await fetch('https://ipapi.co/json/');
                const data = await res.json();
                if (data && data.country_name && ALL_COUNTRIES.includes(data.country_name)) {
                    selectOrigin(data.country_name);
                }
            } catch(e) {}
        }
        window.addEventListener('load', () => setTimeout(autoDetectLocation, 800));
    </script>"""

OLD_NAVBAR_PATTERN = re.compile(
    r'    <!-- Navbar Start -->.*?    <!-- Navbar End -->',
    re.DOTALL
)

updated = 0
for fname in os.listdir(BASE):
    if not fname.endswith('.html'):
        continue
    fpath = os.path.join(BASE, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Replace old navbar HTML
    new_content = OLD_NAVBAR_PATTERN.sub(NAVBAR_HTML, content)

    # 2. Inject CSS before </head> if not already present
    if 'navbar-search' not in new_content:
        new_content = new_content.replace('</head>', NAVBAR_CSS + '\n</head>', 1)
    elif NAVBAR_CSS not in new_content:
        # already has some navbar-search css — replace the existing style block
        new_content = re.sub(r'<style>.*?</style>', NAVBAR_CSS, new_content, count=1, flags=re.DOTALL)

    # 3. Inject JS before </body> if not already present
    if 'whv-data.js' not in new_content:
        new_content = new_content.replace(
            '<script src="https://code.jquery.com/jquery-3.4.1.min.js"></script>',
            NAVBAR_JS + '\n    <script src="https://code.jquery.com/jquery-3.4.1.min.js"></script>',
            1
        )

    if new_content != content:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        updated += 1

print(f"Updated: {updated} files")
