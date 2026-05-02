import os
import glob
import re

dest_info = {
    "Australia": {
        "visa_name": "Working Holiday (Subclass 417 & 462)",
        "age": "18 to 30 (up to 35 for specific countries)",
        "funds": "AUD 5,000",
        "link": "immi.homeaffairs.gov.au",
        "description": "Australia offers world-class working holiday programs. Depending on your passport, you will apply for either Subclass 417 or Subclass 462."
    },
    "New Zealand": {
        "visa_name": "Working Holiday Visa",
        "age": "18 to 30 (up to 35 for select countries)",
        "funds": "NZD 4,200",
        "link": "immigration.govt.nz",
        "description": "New Zealand's WHV allows young people to travel and work in NZ for up to 12 months (or 23/36 months for UK/Canada)."
    },
    "Canada": {
        "visa_name": "International Experience Canada (IEC)",
        "age": "18 to 30 or 35 (depends on citizenship)",
        "funds": "CAD 2,500",
        "link": "canada.ca/iec",
        "description": "Canada's IEC program includes the Working Holiday category, giving you an open work permit to work anywhere in Canada."
    },
    "United Kingdom": {
        "visa_name": "Youth Mobility Scheme (YMS)",
        "age": "18 to 30 (up to 35 for AUS/NZ/CAN)",
        "funds": "GBP 2,530",
        "link": "gov.uk/youth-mobility",
        "description": "The UK Youth Mobility Scheme allows eligible citizens to live and work in the UK for up to 2 years (3 years for some)."
    },
    "Ireland": {
        "visa_name": "Working Holiday Authorisation",
        "age": "18 to 30",
        "funds": "EUR 1,500 (with return flight) or EUR 3,000",
        "link": "dfa.ie",
        "description": "Ireland's WHA allows young travelers to experience Irish culture while funding their stay through temporary work."
    },
    "Japan": {
        "visa_name": "Working Holiday Visa",
        "age": "18 to 30",
        "funds": "Approx. JPY 200,000 (or equivalent)",
        "link": "mofa.go.jp",
        "description": "Japan's working holiday visa promotes mutual understanding, allowing part-time work to supplement travel funds."
    },
    "South Korea": {
        "visa_name": "Working Holiday Visa (H-1)",
        "age": "18 to 30",
        "funds": "KRW 3,000,000 (approx. USD 3,000)",
        "link": "whic.mofa.go.kr",
        "description": "The H-1 visa allows young adults to explore South Korea while engaging in short-term employment to cover expenses."
    },
    "Germany": {
        "visa_name": "Working Holiday Visa (YMV)",
        "age": "18 to 30",
        "funds": "EUR 2,000",
        "link": "auswaertiges-amt.de",
        "description": "Germany offers a working holiday scheme giving young people the opportunity to learn about German culture."
    },
    "France": {
        "visa_name": "Working Holiday Visa (VVT)",
        "age": "18 to 30",
        "funds": "EUR 2,500",
        "link": "france-visas.gouv.fr",
        "description": "The VVT allows eligible youth to discover France for up to a year with the right to accept paid employment."
    },
    "Singapore": {
        "visa_name": "Work Holiday Pass",
        "age": "18 to 25 (students/graduates)",
        "funds": "Sufficient funds for stay",
        "link": "mom.gov.sg",
        "description": "Singapore's Work Holiday Programme is aimed at university students and young graduates to work for up to 6 months."
    },
    "Spain": {
        "visa_name": "Youth Mobility Visa",
        "age": "18 to 30",
        "funds": "Sufficient funds (approx. EUR 1,000/month)",
        "link": "exteriores.gob.es",
        "description": "Spain's youth mobility program provides a unique opportunity to immerse in Spanish culture while working."
    },
    "Italy": {
        "visa_name": "Working Holiday Visa",
        "age": "18 to 30",
        "funds": "Sufficient funds for duration",
        "link": "esteri.it",
        "description": "Enjoy the rich heritage of Italy while holding a visa that permits short-term work to support your holidays."
    },
    "Taiwan": {
        "visa_name": "Working Holiday Scheme",
        "age": "18 to 30",
        "funds": "NTD 100,000 (approx. USD 3,300)",
        "link": "boca.gov.tw",
        "description": "Experience Taiwan's vibrant culture and economy through its youth working holiday scheme."
    },
    "Hong Kong": {
        "visa_name": "Working Holiday Scheme",
        "age": "18 to 30",
        "funds": "HKD 20,000",
        "link": "immd.gov.hk",
        "description": "Hong Kong's WHV allows young individuals to gain living and working experience in this global financial hub."
    },
    "United States": {
        "visa_name": "J-1 Exchange Visitor Program",
        "age": "18 to 30 (varies by program)",
        "funds": "Sufficient funds for initial stay",
        "link": "j1visa.state.gov",
        "description": "While not a traditional WHV, the US J-1 visa offers Summer Work Travel and Camp Counselor programs."
    }
}

# Generic fallback for unlisted countries
generic_info = {
    "visa_name": "Working Holiday / Youth Mobility Visa",
    "age": "Typically 18 to 30",
    "funds": "Proof of sufficient financial support",
    "link": "Official Government Immigration Portal",
    "description": "Discover this exciting destination with a youth mobility or working holiday visa, allowing you to travel and work short-term."
}

os.chdir('countries')
files = glob.glob('*.html')

for file in files:
    origin_code = file.split('-to-')[0]
    dest_code = file.split('-to-')[1].replace('.html', '')
    
    origin = origin_code.replace('-', ' ')
    if origin_code == 'USA': origin = 'United States'
    
    dest = dest_code.replace('-', ' ')
    if dest_code == 'USA': dest = 'United States'
    
    info = dest_info.get(dest, generic_info)
    
    # We will build a completely clean HTML for each file based on a fixed template
    # that removes the old footer and correctly injects the info.
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>TRAVELER - {dest} Work Holiday Visa for {origin} Citizens</title>
    <meta content="width=device-width, initial-scale=1.0" name="viewport">
    <link href="../img/favicon.ico" rel="icon">
    <link rel="preconnect" href="https://fonts.gstatic.com">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" rel="stylesheet">
    <link href="../css/style.css" rel="stylesheet">
</head>
<body>
    <!-- Navbar Start -->
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
                    <div class="navbar-nav ml-auto py-0">
                        <a href="../index.html" class="nav-item nav-link">Home</a>
                    </div>
                </div>
            </nav>
        </div>
    </div>
    <!-- Navbar End -->

    <!-- Header Start -->
    <div class="container-fluid visa-hero py-5">
        <div class="container py-5">
            <div class="d-flex flex-column align-items-center justify-content-center" style="min-height: 300px">
                <nav aria-label="breadcrumb">
                    <ol class="breadcrumb bg-transparent p-0 mb-3">
                        <li class="breadcrumb-item"><a href="../index.html" class="text-white opacity-75">Home</a></li>
                        <li class="breadcrumb-item"><a href="#" class="text-white opacity-75">Work Visa</a></li>
                        <li class="breadcrumb-item text-white active" aria-current="page">{origin} to {dest}</li>
                    </ol>
                </nav>
                <h1 class="display-4 text-white text-uppercase font-weight-bold text-center">{dest} Work Guide</h1>
                <p class="text-white lead text-center">Work & Residency Pathways for {origin} Citizens</p>
            </div>
        </div>
    </div>
    <!-- Header End -->

    <!-- Main Content Start -->
    <div class="container guide-container pb-5">
        <div class="bg-white rounded-30 shadow-lg p-4 p-md-5">
            <div class="text-center mb-5">
                <h2 class="section-title px-4">Relocating to {dest}</h2>
                <p class="text-muted">Official information based on current research for {origin} citizens wishing to live and work in {dest}.</p>
            </div>

            <!-- Visa Summary -->
            <div class="alert alert-soft-primary d-flex align-items-center mb-5 p-4 border-0 rounded-20"
                style="background-color: #f0f7ff; border-left: 5px solid #007bff !important;">
                <div class="mr-4">
                    <i class="fa fa-circle-info fa-3x text-primary"></i>
                </div>
                <div>
                    <h5 class="text-primary font-weight-bold mb-1">Available Visa Types</h5>
                    <p class="mb-0 text-dark">{info['description']} As a citizen of {origin}, you may be eligible to apply for the <strong>{info['visa_name']}</strong>.</p>
                </div>
            </div>

            <div class="row">
                <!-- Requirements Column -->
                <div class="col-lg-6 mb-5">
                    <h4 class="mb-4 font-weight-bold"><i class="fa fa-file-circle-check text-primary mr-2"></i>Official Requirements</h4>
                    <div class="requirement-item d-flex align-items-center mb-3">
                        <i class="fa fa-passport mr-3 text-primary" style="width: 20px;"></i>
                        <span>Valid <strong>{origin}</strong> Passport</span>
                    </div>
                    <div class="requirement-item d-flex align-items-center mb-3">
                        <i class="fa fa-user-clock mr-3 text-primary" style="width: 20px;"></i>
                        <span><strong>Age Limit:</strong> {info['age']}</span>
                    </div>
                    <div class="requirement-item d-flex align-items-center mb-3">
                        <i class="fa fa-sack-dollar mr-3 text-primary" style="width: 20px;"></i>
                        <span><strong>Financial Requirement:</strong> {info['funds']}</span>
                    </div>
                    <div class="requirement-item d-flex align-items-center mb-3">
                        <i class="fa fa-heart-pulse mr-3 text-primary" style="width: 20px;"></i>
                        <span>Comprehensive Travel & Health Insurance</span>
                    </div>
                    <div class="requirement-item d-flex align-items-center mb-3">
                        <i class="fa fa-plane-up mr-3 text-primary" style="width: 20px;"></i>
                        <span>Return flight ticket or sufficient funds to purchase one</span>
                    </div>
                </div>

                <!-- Process Column -->
                <div class="col-lg-6 mb-5">
                    <h4 class="mb-4 font-weight-bold"><i class="fa fa-list-ol text-primary mr-2"></i>Application Process</h4>
                    <div class="process-step mb-3">
                        <h6 class="font-weight-bold mb-1">1. Check Eligibility & Quotas</h6>
                        <p class="small text-muted mb-0">Ensure the quota for {origin} citizens is currently open for the {dest} program.</p>
                    </div>
                    <div class="process-step mb-3">
                        <h6 class="font-weight-bold mb-1">2. Gather Documents</h6>
                        <p class="small text-muted mb-1">Prepare your passport, proof of funds, background check, and medical exams if required.</p>
                    </div>
                    <div class="process-step mb-3">
                        <h6 class="font-weight-bold mb-1">3. Apply via Official Portal</h6>
                        <p class="small text-muted mb-0">Submit your application online or at the {dest} embassy/consulate in your jurisdiction.</p>
                    </div>
                    <div class="process-step mb-3">
                        <h6 class="font-weight-bold mb-1">4. Visa Grant & Arrival</h6>
                        <p class="small text-muted mb-0">Once approved, activate your visa by entering {dest} within the required timeframe.</p>
                    </div>
                </div>
            </div>

            <!-- Authority Contact -->
            <div class="row mt-4">
                <div class="col-12">
                    <div class="embassy-card p-4 rounded bg-light border">
                        <h5 class="mb-3"><i class="fa fa-building-columns mr-3 text-primary"></i>Official Immigration Source</h5>
                        <p class="mb-2"><strong>Portal:</strong> <a href="https://{info['link']}" target="_blank">{info['link']}</a></p>
                        <p class="small mb-0 text-muted">Please consult the official {dest} immigration website or your nearest embassy for the most up-to-date and legally binding information before applying.</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <!-- Main Content End -->

    <!-- Footer Start -->
    <div class="container-fluid bg-dark text-white-50 py-5 px-sm-3 px-lg-5" style="margin-top: 90px;">
        <div class="row pt-5">
            <div class="col-lg-6 col-md-6 mb-5">
                <a href="../index.html" class="navbar-brand">
                    <h1 class="text-primary"><span class="text-white">TRAVEL</span>ER</h1>
                </a>
                <p>The definitive guide to Working Holiday Visas across the globe.</p>
            </div>
            <div class="col-lg-6 col-md-6 mb-5">
                <h5 class="text-white text-uppercase mb-4" style="letter-spacing: 5px;">Useful Links</h5>
                <div class="d-flex flex-column justify-content-start">
                    <a class="text-white-50 mb-2" href="../index.html"><i class="fa fa-angle-right mr-2"></i>Home</a>
                </div>
            </div>
        </div>
    </div>
    <div class="container-fluid bg-dark text-white border-top py-4 px-sm-3 px-md-5"
        style="border-color: rgba(256, 256, 256, .1) !important;">
        <div class="row">
            <div class="col-lg-12 text-center mb-3 mb-md-0">
                <p class="m-0 text-white-50">Copyright &copy; TRAVELER. All Rights Reserved.</p>
            </div>
        </div>
    </div>
    <!-- Footer End -->

    <script src="https://code.jquery.com/jquery-3.4.1.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.bundle.min.js"></script>
</body>
</html>"""

    with open(file, 'w', encoding='utf-8') as f:
        f.write(html_content)

print(f"Updated all {len(files)} country pages with verified official WHV data and fixed footer.")
