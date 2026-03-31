#!/usr/bin/env python3
"""Add 5 new cities to desktop nav and mobile menu on existing pages.
These were lost when the pages were reverted during the fix process."""
import os, re, glob

BASE = '/Users/michaelredman/Documents/GitHub/dvspecialists'

NEW_CITIES = [
    ("palo-alto", "Palo Alto"),
    ("mountain-view", "Mountain View"),
    ("sunnyvale", "Sunnyvale"),
    ("santa-clara", "Santa Clara"),
    ("san-jose", "San Jose"),
]
NEW_CITY_SLUGS = {s for s, _ in NEW_CITIES}

# New desktop nav links (no arrows, standard dropdown format)
NEW_NAV_LINKS = '\n'.join(
    f'          <a href="/dryer-vent-cleaning-{slug}">{name}</a>'
    for slug, name in NEW_CITIES
)

# New mobile menu links (with arrows)
NEW_MOBILE_LINKS = '\n'.join(
    f'      <a href="/dryer-vent-cleaning-{slug}" class="block py-1 pl-3 hover:text-teal-DEFAULT">→ {name}</a>'
    for slug, name in NEW_CITIES
)

skip = {'work-admin.html', 'free-duct-promo.html', 'free-duct-nextdoor.html'}
# Only process pages that are NOT the new city pages (those are already fixed)
new_city_files = {f'dryer-vent-cleaning-{s}.html' for s in NEW_CITY_SLUGS}

html_files = sorted(glob.glob(os.path.join(BASE, '*.html')))

for filepath in html_files:
    filename = os.path.basename(filepath)
    if filename in skip or filename in new_city_files:
        continue

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    changes = []

    # Skip if already has new cities in nav
    if 'dryer-vent-cleaning-palo-alto' in content.split('<footer')[0] if '<footer' in content else 'dryer-vent-cleaning-palo-alto' in content:
        print(f'  SKIP (already has new cities): {filename}')
        continue

    # 1. Desktop nav dropdown - add after Half Moon Bay
    # Match the HMB link in the nav dropdown (not in mobile menu)
    # The desktop nav uses plain <a> without class="block py-1 pl-3"
    hmb_nav_plain = '<a href="/dryer-vent-cleaning-half-moon-bay">Half Moon Bay</a>'
    if hmb_nav_plain in content:
        content = content.replace(hmb_nav_plain, hmb_nav_plain + '\n' + NEW_NAV_LINKS, 1)
        changes.append('desktop-nav')

    # Also handle the active variant (for Half Moon Bay's own page)
    hmb_nav_active = re.search(
        r'(<a href="/dryer-vent-cleaning-half-moon-bay" class="active">.*?</a>)',
        content
    )
    if hmb_nav_active and 'desktop-nav' not in changes:
        content = content.replace(
            hmb_nav_active.group(1),
            hmb_nav_active.group(1) + '\n' + NEW_NAV_LINKS,
            1
        )
        changes.append('desktop-nav')

    # 2. Mobile menu - add after Half Moon Bay
    # The mobile menu uses <a ... class="block py-1 pl-3 ...">→ Half Moon Bay</a>
    hmb_mobile = re.search(
        r'(<a href="/dryer-vent-cleaning-half-moon-bay" class="block py-1 pl-3[^"]*"[^>]*>→ Half Moon Bay</a>)',
        content
    )
    if hmb_mobile:
        content = content.replace(
            hmb_mobile.group(1),
            hmb_mobile.group(1) + '\n' + NEW_MOBILE_LINKS,
            1
        )
        changes.append('mobile-menu')

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'  FIXED ({", ".join(changes)}): {filename}')
    else:
        print(f'  OK: {filename}')

print('\nDone.')
