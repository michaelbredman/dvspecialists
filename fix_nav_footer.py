#!/usr/bin/env python3
"""Fix nav dropdown, mobile menu, and footer on all pages.

Strategy for new city pages:
- Desktop nav: replace entire nav-dropdown-menu div content
- Mobile menu: replace all city links between "Service Areas</div>" and "Reviews" link
  within the mobileMenu div
- Footer: replace the Service Areas <ul> within the <footer> tag

Strategy for existing pages:
- Footer: add 5 new cities after Half Moon Bay
"""
import os, re, glob

BASE = '/Users/michaelredman/Documents/GitHub/dvspecialists'

ALL_CITIES = [
    ("san-mateo", "San Mateo"),
    ("san-francisco", "San Francisco"),
    ("south-san-francisco", "South San Francisco"),
    ("san-carlos", "San Carlos"),
    ("burlingame", "Burlingame"),
    ("hillsborough", "Hillsborough"),
    ("belmont", "Belmont"),
    ("redwood-city", "Redwood City"),
    ("menlo-park", "Menlo Park"),
    ("los-altos", "Los Altos"),
    ("half-moon-bay", "Half Moon Bay"),
    ("palo-alto", "Palo Alto"),
    ("mountain-view", "Mountain View"),
    ("sunnyvale", "Sunnyvale"),
    ("santa-clara", "Santa Clara"),
    ("san-jose", "San Jose"),
]

NEW_CITIES = [
    ("palo-alto", "Palo Alto"),
    ("mountain-view", "Mountain View"),
    ("sunnyvale", "Sunnyvale"),
    ("santa-clara", "Santa Clara"),
    ("san-jose", "San Jose"),
]
NEW_CITY_SLUGS = {s for s, _ in NEW_CITIES}


def get_active_city(filename):
    for slug, name in ALL_CITIES:
        if filename == f'dryer-vent-cleaning-{slug}.html':
            return slug, name
    return None, None


def fix_desktop_nav(content, active_slug):
    """Replace entire nav-dropdown-menu with correct content."""
    nav_links = []
    nav_links.append('          <a href="/dryer-vent-cleaning-san-mateo"><span style="color:var(--orange);">📍</span> San Mateo</a>')
    nav_links.append('          <div class="menu-divider"></div>')
    for slug, name in ALL_CITIES:
        if slug == active_slug:
            nav_links.append(f'          <a href="/dryer-vent-cleaning-{slug}" class="active"><span style="color:var(--orange);">📍</span> {name}</a>')
        else:
            nav_links.append(f'          <a href="/dryer-vent-cleaning-{slug}">{name}</a>')

    marker = '<div class="nav-dropdown-menu">'
    start = content.find(marker)
    if start == -1:
        return content, False

    # Find matching </div> by depth counting
    pos = start + len(marker)
    depth = 1
    end = -1
    while depth > 0 and pos < len(content):
        next_open = content.find('<div', pos)
        next_close = content.find('</div>', pos)
        if next_close == -1:
            break
        if next_open != -1 and next_open < next_close:
            depth += 1
            pos = next_open + 4
        else:
            depth -= 1
            if depth == 0:
                end = next_close + len('</div>')
            pos = next_close + 6

    if end == -1:
        return content, False

    replacement = '        ' + marker + '\n' + '\n'.join(nav_links) + '\n        </div>'
    content = content[:start] + replacement + content[end:]
    return content, True


def fix_mobile_menu(content, active_slug):
    """Replace all city links in mobile menu with correct full list."""
    # Build full mobile menu city links
    mobile_links = []
    for slug, name in ALL_CITIES:
        if slug == active_slug:
            mobile_links.append(f'      <a href="/dryer-vent-cleaning-{slug}" class="block py-1 pl-3" style="color:var(--orange);">→ {name}</a>')
        else:
            mobile_links.append(f'      <a href="/dryer-vent-cleaning-{slug}" class="block py-1 pl-3 hover:text-teal-DEFAULT">→ {name}</a>')
    new_content = '\n'.join(mobile_links)

    # Find mobileMenu div first to scope our search
    mobile_start = content.find('id="mobileMenu"')
    if mobile_start == -1:
        return content, False

    # Find "Service Areas</div>" within mobile menu
    sa_marker = 'Service Areas</div>'
    sa_idx = content.find(sa_marker, mobile_start)
    if sa_idx == -1:
        return content, False
    # Start after the newline following "Service Areas</div>"
    links_start = content.find('\n', sa_idx) + 1

    # Find the Reviews link within mobile menu (end of city links)
    reviews_marker = '<a href="/#reviews"'
    reviews_idx = content.find(reviews_marker, links_start)
    if reviews_idx == -1:
        return content, False
    # Walk back to find start of that line
    line_start = content.rfind('\n', links_start, reviews_idx) + 1

    content = content[:links_start] + new_content + '\n' + content[line_start:]
    return content, True


def fix_footer_service_areas(content, active_slug):
    """Replace footer Service Areas <ul> content entirely."""
    # Build correct footer list
    footer_items = []
    for slug, name in ALL_CITIES:
        if slug == active_slug:
            footer_items.append(f'          <li><a href="/dryer-vent-cleaning-{slug}" class="hover:text-white transition-colors duration-200" style="color:var(--teal-light);">{name}</a></li>')
        else:
            footer_items.append(f'          <li><a href="/dryer-vent-cleaning-{slug}" class="hover:text-white transition-colors duration-200">{name}</a></li>')
    footer_items.append('          <li><a href="/#service-areas" class="hover:text-white transition-colors duration-200">View All Areas →</a></li>')
    new_content = '\n'.join(footer_items)

    # Scope to <footer> section
    footer_start = content.find('<footer')
    if footer_start == -1:
        return content, False

    # Find "Service Areas" heading within footer
    sa_heading = '>Service Areas</div>'
    sa_idx = content.find(sa_heading, footer_start)
    if sa_idx == -1:
        # Try alternate format
        sa_heading = '>Service Areas</div>'
        sa_idx = content.find(sa_heading, footer_start)
        if sa_idx == -1:
            return content, False

    # Find the <ul> after this heading
    ul_marker = '<ul class="space-y-2 text-sm">'
    ul_idx = content.find(ul_marker, sa_idx)
    if ul_idx == -1:
        return content, False

    inner_start = ul_idx + len(ul_marker)
    # Skip newline if present
    if inner_start < len(content) and content[inner_start] == '\n':
        inner_start += 1

    # Find closing </ul>
    ul_end = content.find('</ul>', inner_start)
    if ul_end == -1:
        return content, False

    content = content[:inner_start] + new_content + '\n        ' + content[ul_end:]
    return content, True


def fix_existing_footer_append(content, active_slug):
    """Add 5 new cities after Half Moon Bay in footer (for existing pages)."""
    footer_start = content.find('<footer')
    if footer_start == -1:
        return content, False

    # Check if already has new cities in footer
    footer_section = content[footer_start:]
    if 'dryer-vent-cleaning-palo-alto' in footer_section:
        return content, False

    # Build new links
    new_links = []
    for slug, name in NEW_CITIES:
        new_links.append(f'          <li><a href="/dryer-vent-cleaning-{slug}" class="hover:text-white transition-colors duration-200">{name}</a></li>')
    new_links_str = '\n'.join(new_links)

    # Find Half Moon Bay in footer
    hmb = re.search(
        r'(<li><a href="/dryer-vent-cleaning-half-moon-bay"[^>]*>Half Moon Bay</a></li>)',
        footer_section
    )
    if hmb:
        abs_end = footer_start + hmb.end()
        content = content[:abs_end] + '\n' + new_links_str + content[abs_end:]
        return content, True

    return content, False


# Process files
skip = {'work-admin.html', 'free-duct-promo.html', 'free-duct-nextdoor.html'}
html_files = sorted(glob.glob(os.path.join(BASE, '*.html')))

for filepath in html_files:
    filename = os.path.basename(filepath)
    if filename in skip:
        continue

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    active_slug, _ = get_active_city(filename)
    is_new_city = active_slug in NEW_CITY_SLUGS if active_slug else False
    changes = []

    if is_new_city:
        content, ok = fix_desktop_nav(content, active_slug)
        if ok: changes.append('desktop-nav')

        content, ok = fix_mobile_menu(content, active_slug)
        if ok: changes.append('mobile-menu')

        content, ok = fix_footer_service_areas(content, active_slug)
        if ok: changes.append('footer')
    else:
        content, ok = fix_existing_footer_append(content, active_slug)
        if ok: changes.append('footer')

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'  FIXED ({", ".join(changes)}): {filename}')
    else:
        print(f'  OK: {filename}')

print('\nDone.')
