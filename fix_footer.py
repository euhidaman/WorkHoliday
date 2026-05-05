import os
import glob

# The old footer brand section in country pages (no social links)
OLD_FOOTER = '''    <div class="container-fluid bg-dark text-white-50 py-5 px-sm-3 px-lg-5" style="margin-top: 90px;">
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
    </div>'''

# The new unified footer
NEW_FOOTER = '''    <div class="container-fluid bg-dark text-white-50 py-5 px-sm-3 px-lg-5" style="margin-top: 90px;">
        <div class="row pt-5">
            <div class="col-lg-6 col-md-6 mb-5">
                <a href="../index.html" class="navbar-brand">
                    <h1 class="text-primary"><span class="text-white">TRAVEL</span>ER</h1>
                </a>
                <p>The definitive guide to Working Holiday Visas across the globe.</p>
                <h6 class="text-white text-uppercase mt-4 mb-3" style="letter-spacing: 5px;">Follow Us</h6>
                <div class="d-flex justify-content-start">
                    <a class="btn btn-outline-primary btn-square mr-2" href="#"><i class="fab fa-twitter"></i></a>
                    <a class="btn btn-outline-primary btn-square mr-2" href="#"><i class="fab fa-facebook-f"></i></a>
                    <a class="btn btn-outline-primary btn-square mr-2" href="#"><i class="fab fa-linkedin-in"></i></a>
                    <a class="btn btn-outline-primary btn-square" href="#"><i class="fab fa-instagram"></i></a>
                </div>
            </div>
            <div class="col-lg-6 col-md-6 mb-5">
                <h5 class="text-white text-uppercase mb-4" style="letter-spacing: 5px;">Useful Links</h5>
                <div class="d-flex flex-column justify-content-start">
                    <a class="text-white-50 mb-2" href="../index.html"><i class="fa fa-angle-right mr-2"></i>Home</a>
                </div>
            </div>
        </div>
    </div>'''

FA_CDN = '<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.10.0/css/all.min.css" rel="stylesheet">'

updated = 0
for filepath in glob.glob('countries/*.html'):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    changed = False

    # Add Font Awesome if missing (needed for social icons)
    if FA_CDN not in content and 'font-awesome' not in content:
        content = content.replace('</head>', f'    {FA_CDN}\n</head>', 1)
        changed = True

    # Replace old footer with new footer
    if OLD_FOOTER in content:
        content = content.replace(OLD_FOOTER, NEW_FOOTER)
        changed = True

    if changed:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        updated += 1

print(f"Updated {updated} country pages.")
