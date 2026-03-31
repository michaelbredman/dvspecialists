#!/usr/bin/env python3
"""Add contextual internal links within FAQ answer text on city pages.
Only replaces first occurrence of each city name within faq-body content."""
import re

LINK_STYLE = 'color:var(--teal-dark);text-decoration:underline;'

# For each city page, define which neighboring city names to link (and to what slug)
# We'll search faq-body content for these city names and link the first occurrence
CITY_TO_SLUG = {
    'San Mateo': '/dryer-vent-cleaning-san-mateo',
    'San Francisco': '/dryer-vent-cleaning-san-francisco',
    'South San Francisco': '/dryer-vent-cleaning-south-san-francisco',
    'Burlingame': '/dryer-vent-cleaning-burlingame',
    'Hillsborough': '/dryer-vent-cleaning-hillsborough',
    'Belmont': '/dryer-vent-cleaning-belmont',
    'San Carlos': '/dryer-vent-cleaning-san-carlos',
    'Redwood City': '/dryer-vent-cleaning-redwood-city',
    'Menlo Park': '/dryer-vent-cleaning-menlo-park',
    'Palo Alto': '/dryer-vent-cleaning-palo-alto',
    'Los Altos': '/dryer-vent-cleaning-los-altos',
    'Mountain View': '/dryer-vent-cleaning-mountain-view',
    'Sunnyvale': '/dryer-vent-cleaning-sunnyvale',
    'Santa Clara': '/dryer-vent-cleaning-santa-clara',
    'San Jose': '/dryer-vent-cleaning-san-jose',
    'Half Moon Bay': '/dryer-vent-cleaning-half-moon-bay',
}

# For each page, which 2-3 cities to try linking (in priority order)
PAGE_LINKS = {
    'dryer-vent-cleaning-belmont-template.html': ['San Mateo', 'San Carlos'],
    'dryer-vent-cleaning-burlingame-template.html': ['San Mateo', 'Hillsborough'],
    'dryer-vent-cleaning-hillsborough-template.html': ['Burlingame', 'San Mateo'],
    'dryer-vent-cleaning-san-carlos-template.html': ['Redwood City', 'Belmont'],
    'dryer-vent-cleaning-redwood-city-template.html': ['San Carlos', 'Menlo Park'],
    'dryer-vent-cleaning-menlo-park-template.html': ['Palo Alto', 'Redwood City'],
    'dryer-vent-cleaning-palo-alto-template.html': ['Menlo Park', 'Mountain View'],
    'dryer-vent-cleaning-los-altos-template.html': ['Palo Alto', 'Mountain View'],
    'dryer-vent-cleaning-mountain-view-template.html': ['Sunnyvale', 'Palo Alto'],
    'dryer-vent-cleaning-sunnyvale-template.html': ['Mountain View', 'Santa Clara'],
    'dryer-vent-cleaning-santa-clara-template.html': ['Sunnyvale', 'San Jose'],
    'dryer-vent-cleaning-san-jose-template.html': ['Santa Clara', 'Sunnyvale'],
    'dryer-vent-cleaning-san-francisco-template.html': ['South San Francisco', 'San Mateo'],
    'dryer-vent-cleaning-south-san-francisco-template.html': ['San Francisco', 'San Mateo'],
    'dryer-vent-cleaning-san-mateo-template.html': ['Burlingame', 'Belmont'],
    'dryer-vent-cleaning-half-moon-bay-template.html': ['San Mateo', 'Redwood City'],
}

updated = []

for filename, target_cities in PAGE_LINKS.items():
    try:
        with open(filename, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"  SKIP: {filename}")
        continue

    original = content
    links_added = 0

    for target_city in target_cities:
        slug = CITY_TO_SLUG[target_city]
        link_html = f'<a href="{slug}" style="{LINK_STYLE}">{target_city}</a>'

        # Find all faq-body sections
        # Pattern: <div class="faq-body">...</div></details>
        parts = content.split('<div class="faq-body">')

        if len(parts) <= 1:
            continue

        # Try to link the first occurrence of target_city in any faq-body
        linked = False
        new_parts = [parts[0]]
        for part in parts[1:]:
            if not linked:
                # Split at </div></details> to isolate the faq body content
                end_idx = part.find('</div></details>')
                if end_idx > 0:
                    body = part[:end_idx]
                    rest = part[end_idx:]

                    # Check if city name exists and isn't already a link
                    if target_city in body and f'>{target_city}</a>' not in body:
                        # Replace first occurrence only
                        body = body.replace(target_city, link_html, 1)
                        linked = True
                        links_added += 1

                    new_parts.append(body + rest)
                else:
                    new_parts.append(part)
            else:
                new_parts.append(part)

        content = '<div class="faq-body">'.join(new_parts)

    if content != original:
        with open(filename, 'w') as f:
            f.write(content)
        updated.append(filename)
        print(f"  {filename}: Added {links_added} contextual links")
    else:
        print(f"  {filename}: No matching text found for links")

print(f"\nUpdated {len(updated)} files with contextual FAQ links")
