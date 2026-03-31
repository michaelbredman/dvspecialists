#!/usr/bin/env python3
"""Comprehensive fix: replace desktop nav dropdown and mobile menu city links
on ALL pages with the complete 16-city list."""
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

NEW_CITY_SLUGS = {"palo-alto", "mountain-view", "sunnyvale", "santa-clara", "san-jose"}


def get_active_city(filename):
    for slug, name in ALL_CITIES:
        if filename == f'dryer-vent-cleaning-{slug}.html':
            return slug, name
    return None, None


def build_desktop_nav(active_slug):
    """Build correct desktop nav dropdown inner HTML."""
    lines = []
    lines.append('          <a href="/dryer-vent-cleaning-san-mateo"><span style="color:var(--orange);">📍</span> San Mateo</a>')
    lines.append('          <div class="menu-divider"></div>')
    for slug, name in ALL_CITIES:
        if slug == active_slug:
            lines.append(f'          <a href="/dryer-vent-cleaning-{slug}" class="active"><span style="color:var(--orange);">📍</span> {name}</a>')
        else:
            lines.append(f'          <a href="/dryer-vent-cleaning-{slug}">{name}</a>')
    return '\n'.join(lines)


def build_mobile_links(active_slug):
    """Build correct mobile menu city links."""
    lines = []
    for slug, name in ALL_CITIES:
        if slug == active_slug:
            lines.append(f'      <a href="/dryer-vent-cleaning-{slug}" class="block py-1 pl-3" style="color:var(--orange);">→ {name}</a>')
        else:
            lines.append(f'      <a href="/dryer-vent-cleaning-{slug}" class="block py-1 pl-3 hover:text-teal-DEFAULT">→ {name}</a>')
    return '\n'.join(lines)


def replace_nav_dropdown(content, active_slug):
    """Replace entire nav-dropdown-menu content."""
    marker = '<div class="nav-dropdown-menu">'
    start = content.find(marker)
    if start == -1:
        return content, False

    # Find matching </div>
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

    new_inner = build_desktop_nav(active_slug)
    replacement = '        ' + marker + '\n' + new_inner + '\n        </div>'
    content = content[:start] + replacement + content[end:]
    return content, True


def replace_mobile_menu(content, active_slug):
    """Replace mobile menu city links between 'Service Areas' heading and Reviews link."""
    # Find mobileMenu div
    mobile_start = content.find('id="mobileMenu"')
    if mobile_start == -1:
        return content, False

    # Find "Service Areas</div>" within mobile menu
    sa_marker = 'Service Areas</div>'
    sa_idx = content.find(sa_marker, mobile_start)
    if sa_idx == -1:
        return content, False

    # Start after the newline following "Service Areas</div>"
    links_start = content.find('\n', sa_idx)
    if links_start == -1:
        return content, False
    links_start += 1

    # Find the end boundary: the Reviews link (or "Our Work" or "Contact")
    # Look for the first link after the city links that doesn't have "dryer-vent-cleaning"
    # This is the "Reviews" or similar link
    end_patterns = [
        '<a href="/#reviews"',
        '<a href="/work"',
        '<a href="/contact"',
    ]

    # Find the earliest non-city link after our start
    end_idx = len(content)
    for pattern in end_patterns:
        idx = content.find(pattern, links_start)
        if idx != -1 and idx < end_idx:
            end_idx = idx

    if end_idx == len(content):
        return content, False

    # Walk back to start of the line
    line_start = content.rfind('\n', links_start, end_idx)
    if line_start == -1:
        line_start = links_start
    else:
        line_start += 1

    new_mobile = build_mobile_links(active_slug)
    content = content[:links_start] + new_mobile + '\n' + content[line_start:]
    return content, True


# Process files
skip = {'work-admin.html', 'free-duct-promo.html', 'free-duct-nextdoor.html',
        'ad-nextdoor.html', 'book.html', 'thank-you.html'}
html_files = sorted(glob.glob(os.path.join(BASE, '*.html')))

for filepath in html_files:
    filename = os.path.basename(filepath)
    if filename in skip:
        continue

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    active_slug, _ = get_active_city(filename)
    changes = []

    # Replace desktop nav dropdown
    content, ok = replace_nav_dropdown(content, active_slug)
    if ok:
        changes.append('desktop-nav')

    # Replace mobile menu
    content, ok = replace_mobile_menu(content, active_slug)
    if ok:
        changes.append('mobile-menu')

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'  FIXED ({", ".join(changes)}): {filename}')
    else:
        print(f'  OK: {filename}')

print('\nDone.')
