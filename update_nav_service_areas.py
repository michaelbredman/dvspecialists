#!/usr/bin/env python3
"""Update nav on all pages:
1. Change Service Areas dropdown button to a link to /service-areas (keeps dropdown on hover)
2. Add 'All Service Areas' link at top of dropdown menu
3. Add 'All Service Areas' link in mobile menu
"""
import glob, re

files = glob.glob('*.html') + glob.glob('*-template.html') + glob.glob('resources/*.html')
# Dedupe
files = list(set(files))
# Exclude service-areas.html itself (already has updated nav)
files = [f for f in files if f != 'service-areas.html']

updated = []

for f in files:
    with open(f, 'r') as fh:
        content = fh.read()

    original = content

    # 1. Replace the dropdown button with a link (desktop nav)
    # Old pattern: <button style="..." onmouseenter="..." onmouseleave="..." aria-haspopup="true">
    #   Service Areas <span class="dropdown-arrow">▼</span>
    # </button>
    # New: <a href="/service-areas" style="..." >Service Areas <span>▼</span></a>

    old_button = re.search(
        r'<button\s+style="background:none;border:none;cursor:pointer;font-family:\'Barlow Condensed\',sans-serif[^"]*"[^>]*aria-haspopup="true">\s*Service Areas\s*<span class="dropdown-arrow">[^<]*</span>\s*</button>',
        content, re.DOTALL
    )
    if old_button:
        new_link = '''<a href="/service-areas" style="background:none;border:none;cursor:pointer;font-family:'Barlow Condensed',sans-serif;font-weight:600;font-size:1.125rem;letter-spacing:.05em;color:#374151;display:flex;align-items:center;gap:.35rem;padding:0;text-decoration:none;" onmouseenter="this.style.color='#026766'" onmouseleave="this.style.color='#374151'">
          Service Areas <span class="dropdown-arrow">&#9660;</span>
        </a>'''
        content = content[:old_button.start()] + new_link + content[old_button.end():]

    # 2. Add "All Service Areas" at top of dropdown if not present
    if '📍</span> San Mateo</a>' in content and 'All Service Areas' not in content:
        content = content.replace(
            '<a href="/dryer-vent-cleaning-san-mateo"><span style="color:var(--orange);">📍</span> San Mateo</a>',
            '<a href="/service-areas"><span style="color:var(--orange);">&#128205;</span> All Service Areas</a>'
        )

    # 3. Add "All Service Areas" to mobile menu if not present
    if 'mobileCityLinks' in content and 'All Service Areas' not in content:
        # Add before the first city link in mobile menu
        mobile_marker = '<div id="mobileCityLinks" style="display:none;">'
        if mobile_marker in content:
            insert_after = mobile_marker + '\n'
            sa_mobile_link = '<a href="/service-areas" class="block py-1 pl-3" style="color:var(--orange);">&rarr; All Service Areas</a>\n'
            content = content.replace(mobile_marker, mobile_marker + '\n' + sa_mobile_link, 1)

    if content != original:
        with open(f, 'w') as fh:
            fh.write(content)
        updated.append(f)

print(f"Updated {len(updated)} files:")
for f in sorted(updated):
    print(f"  {f}")
