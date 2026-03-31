#!/usr/bin/env python3
"""Update nav dropdown, mobile menu, and footer service areas on all pages to include new cities."""

import os
import re
import glob

BASE = '/Users/michaelredman/Documents/GitHub/dvspecialists'

NEW_CITIES = [
    ("palo-alto", "Palo Alto"),
    ("mountain-view", "Mountain View"),
    ("sunnyvale", "Sunnyvale"),
    ("santa-clara", "Santa Clara"),
    ("san-jose", "San Jose"),
]

# The new links to add after Half Moon Bay in desktop nav
NEW_NAV_LINKS = '\n'.join(
    f'          <a href="/dryer-vent-cleaning-{slug}">{name}</a>'
    for slug, name in NEW_CITIES
)

# The new links to add after Half Moon Bay in mobile menu
NEW_MOBILE_LINKS = '\n'.join(
    f'      <a href="/dryer-vent-cleaning-{slug}" class="block py-1 pl-3 hover:text-teal-DEFAULT">→ {name}</a>'
    for slug, name in NEW_CITIES
)

# The new links to add after Half Moon Bay in footer
NEW_FOOTER_LINKS = '\n'.join(
    f'          <li><a href="/dryer-vent-cleaning-{slug}" class="hover:text-white transition-colors duration-200">{name}</a></li>'
    for slug, name in NEW_CITIES
)

# Files to update: all HTML files that have the nav dropdown
html_files = glob.glob(os.path.join(BASE, '*.html'))

# Skip the new city pages (they already have updated nav)
NEW_SLUGS = {s for s, _ in NEW_CITIES}
skip_files = {f'dryer-vent-cleaning-{s}.html' for s in NEW_SLUGS}

count = 0
for filepath in sorted(html_files):
    filename = os.path.basename(filepath)
    if filename in skip_files:
        continue

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    changed = False

    # Check if already has new cities
    if 'dryer-vent-cleaning-palo-alto' in content:
        print(f'  SKIP (already updated): {filename}')
        continue

    # 1. Desktop nav dropdown - add after Half Moon Bay
    hmb_nav = '<a href="/dryer-vent-cleaning-half-moon-bay">Half Moon Bay</a>'
    if hmb_nav in content:
        content = content.replace(
            hmb_nav,
            hmb_nav + '\n' + NEW_NAV_LINKS
        )
        changed = True

    # Also handle the active variant (for Half Moon Bay's own page)
    hmb_nav_active = '<a href="/dryer-vent-cleaning-half-moon-bay" class="active">'
    if hmb_nav_active in content:
        # Find the full line
        m = re.search(r'(<a href="/dryer-vent-cleaning-half-moon-bay" class="active">.*?</a>)', content)
        if m and NEW_NAV_LINKS not in content:
            content = content.replace(m.group(1), m.group(1) + '\n' + NEW_NAV_LINKS)
            changed = True

    # 2. Mobile menu - add after Half Moon Bay
    hmb_mobile = '<a href="/dryer-vent-cleaning-half-moon-bay" class="block py-1 pl-3 hover:text-teal-DEFAULT">→ Half Moon Bay</a>'
    if hmb_mobile in content:
        content = content.replace(
            hmb_mobile,
            hmb_mobile + '\n' + NEW_MOBILE_LINKS
        )
        changed = True

    # Also handle active variant
    hmb_mobile_active = 'dryer-vent-cleaning-half-moon-bay" class="block py-1 pl-3" style="color:var(--orange);">→ Half Moon Bay</a>'
    if hmb_mobile_active in content and 'dryer-vent-cleaning-palo-alto' not in content:
        m2 = re.search(r'(<a href="/dryer-vent-cleaning-half-moon-bay"[^>]*>→ Half Moon Bay</a>)', content)
        if m2:
            content = content.replace(m2.group(1), m2.group(1) + '\n' + NEW_MOBILE_LINKS)
            changed = True

    # 3. Footer service areas - add after Half Moon Bay
    hmb_footer = re.search(
        r'(<li><a href="/dryer-vent-cleaning-half-moon-bay"[^>]*>Half Moon Bay</a></li>)',
        content
    )
    if hmb_footer and 'dryer-vent-cleaning-palo-alto' not in content:
        content = content.replace(
            hmb_footer.group(1),
            hmb_footer.group(1) + '\n' + NEW_FOOTER_LINKS
        )
        changed = True

    if changed:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'  UPDATED: {filename}')
        count += 1
    else:
        print(f'  NO MATCH: {filename}')

print(f'\nUpdated {count} files.')
