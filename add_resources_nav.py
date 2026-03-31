#!/usr/bin/env python3
"""Add a 'Resources' link to the desktop nav and mobile menu on all HTML pages."""

import glob
import os

PROJECT_DIR = "/Users/michaelredman/Documents/GitHub/dvspecialists"
SKIP_FILES = {
    "work-admin.html",
    "free-duct-promo.html",
    "free-duct-nextdoor.html",
    "ad-nextdoor.html",
    "book.html",
    "thank-you.html",
}

# Desktop nav: insert after "Our Work" li, before "Contact" li
DESKTOP_SEARCH = '<li><a href="/work" class="hover:text-teal-DEFAULT transition-colors duration-200">Our Work</a></li>\n      <li><a href="/contact"'
DESKTOP_REPLACE = '<li><a href="/work" class="hover:text-teal-DEFAULT transition-colors duration-200">Our Work</a></li>\n      <li><a href="/resources" class="transition-colors duration-200" style="color:var(--orange);">Resources</a></li>\n      <li><a href="/contact"'

# Mobile menu patterns - there are two variants across pages

# Variant 1 (city pages): class-based styling
MOBILE_SEARCH_V1 = '<a href="/work" class="block py-1 hover:text-teal-DEFAULT">Our Work</a>\n      <a href="/contact"'
MOBILE_REPLACE_V1 = '<a href="/work" class="block py-1 hover:text-teal-DEFAULT">Our Work</a>\n      <a href="/resources" class="block py-1" style="color:var(--orange);">Resources</a>\n      <a href="/contact"'

# Variant 2 (index.html): inline style
MOBILE_SEARCH_V2 = """<a href="/work" style="display:block; padding:.25rem 0; color:inherit; text-decoration:none;">Our Work</a>\n      <a href="/contact" style="display:block; padding:.25rem 0; color:var(--orange); text-decoration:none;">Contact Us</a>"""
MOBILE_REPLACE_V2 = """<a href="/work" style="display:block; padding:.25rem 0; color:inherit; text-decoration:none;">Our Work</a>\n      <a href="/resources" class="block py-1" style="color:var(--orange);">Resources</a>\n      <a href="/contact" style="display:block; padding:.25rem 0; color:var(--orange); text-decoration:none;">Contact Us</a>"""

# Variant 3 (work.html): "Our Work" is active page with different styling
DESKTOP_SEARCH_V3 = '<li><a href="/work" class="transition-colors duration-200" style="color:var(--teal-dark);">Our Work</a></li>\n      <li><a href="/contact"'
DESKTOP_REPLACE_V3 = '<li><a href="/work" class="transition-colors duration-200" style="color:var(--teal-dark);">Our Work</a></li>\n      <li><a href="/resources" class="transition-colors duration-200" style="color:var(--orange);">Resources</a></li>\n      <li><a href="/contact"'

MOBILE_SEARCH_V3 = '<a href="/work" class="block py-1" style="color:var(--teal-dark);">Our Work</a>\n      <a href="/contact"'
MOBILE_REPLACE_V3 = '<a href="/work" class="block py-1" style="color:var(--teal-dark);">Our Work</a>\n      <a href="/resources" class="block py-1" style="color:var(--orange);">Resources</a>\n      <a href="/contact"'

html_files = glob.glob(os.path.join(PROJECT_DIR, "*.html"))
updated = []
skipped_already = []
skipped_admin = []
no_match = []

for filepath in sorted(html_files):
    filename = os.path.basename(filepath)

    if filename in SKIP_FILES:
        skipped_admin.append(filename)
        continue

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Skip if already has /resources in nav
    if '"/resources"' in content or "'/resources'" in content:
        skipped_already.append(filename)
        continue

    original = content
    desktop_done = False
    mobile_done = False

    # Desktop nav replacement
    if DESKTOP_SEARCH in content:
        content = content.replace(DESKTOP_SEARCH, DESKTOP_REPLACE, 1)
        desktop_done = True
    elif DESKTOP_SEARCH_V3 in content:
        content = content.replace(DESKTOP_SEARCH_V3, DESKTOP_REPLACE_V3, 1)
        desktop_done = True

    # Mobile menu replacement - try variant 1 first, then variant 2, then variant 3
    if MOBILE_SEARCH_V1 in content:
        content = content.replace(MOBILE_SEARCH_V1, MOBILE_REPLACE_V1, 1)
        mobile_done = True
    elif MOBILE_SEARCH_V2 in content:
        content = content.replace(MOBILE_SEARCH_V2, MOBILE_REPLACE_V2, 1)
        mobile_done = True
    elif MOBILE_SEARCH_V3 in content:
        content = content.replace(MOBILE_SEARCH_V3, MOBILE_REPLACE_V3, 1)
        mobile_done = True

    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        status = []
        if desktop_done:
            status.append("desktop")
        if mobile_done:
            status.append("mobile")
        updated.append((filename, status))
    else:
        no_match.append(filename)

print("=== UPDATED ===")
for fn, parts in updated:
    print(f"  {fn}: {', '.join(parts)}")

print(f"\n=== SKIPPED (already has /resources) ===")
for fn in skipped_already:
    print(f"  {fn}")

print(f"\n=== SKIPPED (admin/promo) ===")
for fn in skipped_admin:
    print(f"  {fn}")

if no_match:
    print(f"\n=== NO MATCH (patterns not found) ===")
    for fn in no_match:
        print(f"  {fn}")

print(f"\nTotal updated: {len(updated)}")
print(f"Total skipped: {len(skipped_already) + len(skipped_admin)}")
if no_match:
    print(f"Total no match: {len(no_match)}")
