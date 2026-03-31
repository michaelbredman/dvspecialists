#!/usr/bin/env python3
"""
Convert the mobile menu "Service Areas" section from a flat list
to a collapsible accordion on all HTML pages.
"""

import os
import glob

ROOT = "/Users/michaelredman/Documents/GitHub/dvspecialists"
SKIP_FILES = {
    "work-admin.html",
    "free-duct-promo.html",
    "free-duct-nextdoor.html",
    "ad-nextdoor.html",
    "book.html",
    "thank-you.html",
}

TOGGLE_BUTTON = (
    '<div id="mobileServiceAreasToggle" style="cursor:pointer;display:flex;align-items:center;'
    'justify-content:space-between;padding:.5rem 0 .25rem;" class="font-700 text-sm uppercase tracking-widest" '
    "onclick=\"var el=document.getElementById('mobileCityLinks');var arrow=document.getElementById('mobileCityArrow');"
    "if(el.style.display==='none'){el.style.display='block';arrow.textContent='\\u25B2';}else{"
    "el.style.display='none';arrow.textContent='\\u25BC';}\">\n"
    '  <span style="color:var(--teal-light);">Service Areas</span>\n'
    '  <span id="mobileCityArrow" style="color:var(--teal-light);font-size:.7rem;">\u25BC</span>\n'
    '</div>'
)

FIRST_CITY_MARKER = "dryer-vent-cleaning-san-mateo"
LAST_CITY_MARKER = "dryer-vent-cleaning-san-jose"

# Two known heading patterns
HEADING_PATTERNS = [
    'style="font-size:.8rem; font-weight:700; text-transform:uppercase; letter-spacing:.1em; padding:.5rem 0 .25rem; color:var(--teal-light);">Service Areas</div>',
    'class="font-700 text-sm uppercase tracking-widest pt-2 pb-1" style="color:var(--teal-light);">Service Areas</div>',
]


def find_heading_in_mobile_menu(content):
    """Find the Service Areas heading within the mobileMenu section."""
    mobile_menu_start = content.find('id="mobileMenu"')
    if mobile_menu_start == -1:
        return None, None

    for pattern in HEADING_PATTERNS:
        pos = content.find(pattern, mobile_menu_start)
        if pos != -1:
            # Find the start of this div tag
            div_start = content.rfind("<div", mobile_menu_start, pos)
            if div_start == -1:
                continue
            div_end = pos + len(pattern)
            return div_start, div_end

    return None, None


def find_city_links_block(content, after_pos):
    """Find the first and last city link lines after the heading."""
    # Find the first city link (san-mateo)
    first_link_pos = content.find(FIRST_CITY_MARKER, after_pos)
    if first_link_pos == -1:
        return None, None

    # Find the <a that starts this link
    first_a_start = content.rfind("<a ", after_pos, first_link_pos)
    if first_a_start == -1:
        return None, None

    # Find the last city link (san-jose)
    last_link_pos = content.find(LAST_CITY_MARKER, first_a_start)
    if last_link_pos == -1:
        return None, None

    # Find the end of the last link's </a> tag
    last_a_end_pos = content.find("</a>", last_link_pos)
    if last_a_end_pos == -1:
        return None, None
    last_a_end = last_a_end_pos + len("</a>")

    return first_a_start, last_a_end


def process_file(filepath):
    """Process a single HTML file."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Skip if already processed
    if "mobileCityLinks" in content:
        print(f"  SKIP (already has accordion): {os.path.basename(filepath)}")
        return False

    # Check for mobileMenu
    if 'id="mobileMenu"' not in content:
        print(f"  SKIP (no mobileMenu): {os.path.basename(filepath)}")
        return False

    # Check for Service Areas heading
    heading_start, heading_end = find_heading_in_mobile_menu(content)
    if heading_start is None:
        print(f"  SKIP (no Service Areas heading in mobileMenu): {os.path.basename(filepath)}")
        return False

    # Find city links block
    city_start, city_end = find_city_links_block(content, heading_end)
    if city_start is None:
        print(f"  SKIP (no city links found): {os.path.basename(filepath)}")
        return False

    # Extract parts
    before_heading = content[:heading_start]
    city_links = content[city_start:city_end]
    after_cities = content[city_end:]

    # Determine whitespace/indentation from the heading line
    # Find the indentation of the heading
    line_start = content.rfind("\n", 0, heading_start)
    if line_start == -1:
        indent = ""
    else:
        indent_text = content[line_start + 1:heading_start]
        indent = indent_text  # preserve leading whitespace

    # Build the new content
    new_content = (
        before_heading
        + indent + TOGGLE_BUTTON + "\n"
        + indent + '<div id="mobileCityLinks" style="display:none;">\n'
        + city_links + "\n"
        + indent + "</div>"
        + after_cities
    )

    # Verify it still ends with </html>
    stripped = new_content.rstrip()
    if not stripped.endswith("</html>"):
        print(f"  ERROR: result doesn't end with </html>: {os.path.basename(filepath)}")
        return False

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"  UPDATED: {os.path.basename(filepath)}")
    return True


def main():
    # Collect all HTML files in root and resources/
    html_files = glob.glob(os.path.join(ROOT, "*.html"))
    html_files += glob.glob(os.path.join(ROOT, "resources", "*.html"))

    updated = 0
    skipped = 0

    for filepath in sorted(html_files):
        basename = os.path.basename(filepath)
        if basename in SKIP_FILES:
            print(f"  SKIP (excluded): {basename}")
            skipped += 1
            continue

        if process_file(filepath):
            updated += 1
        else:
            skipped += 1

    print(f"\nDone. Updated: {updated}, Skipped: {skipped}")


if __name__ == "__main__":
    main()
