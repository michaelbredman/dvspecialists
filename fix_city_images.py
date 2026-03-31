#!/usr/bin/env python3
"""Update new city pages with city-specific hero images and OG/meta images."""
import os

BASE = '/Users/michaelredman/Documents/GitHub/dvspecialists'

CITY_IMAGES = {
    'dryer-vent-cleaning-palo-alto.html': {
        'img': 'images/palo-alto-downtown.jpg',
        'alt': 'Downtown Palo Alto, CA',
        'og': 'https://www.dvspecialists.com/images/palo-alto-downtown.jpg',
    },
    'dryer-vent-cleaning-mountain-view.html': {
        'img': 'images/mountain-view-castro-street.jpg',
        'alt': 'Castro Street, Mountain View, CA',
        'og': 'https://www.dvspecialists.com/images/mountain-view-castro-street.jpg',
    },
    'dryer-vent-cleaning-sunnyvale.html': {
        'img': 'images/sunnyvale-murphy-avenue.jpg',
        'alt': 'Historic Murphy Avenue, Sunnyvale, CA',
        'og': 'https://www.dvspecialists.com/images/sunnyvale-murphy-avenue.jpg',
    },
    'dryer-vent-cleaning-santa-clara.html': {
        'img': 'images/santa-clara-mission.jpg',
        'alt': 'Mission Santa Clara de Asis, Santa Clara, CA',
        'og': 'https://www.dvspecialists.com/images/santa-clara-mission.jpg',
    },
    'dryer-vent-cleaning-san-jose.html': {
        'img': 'images/san-jose-skyline.jpg',
        'alt': 'Downtown San Jose Skyline, CA',
        'og': 'https://www.dvspecialists.com/images/san-jose-skyline.jpg',
    },
}

for filename, data in CITY_IMAGES.items():
    filepath = os.path.join(BASE, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Replace hero image src and alt
    # The hero image is: <img src="images/san-mateo-downtown.jpg" alt="Downtown CITY, CA"
    content = content.replace(
        'src="images/san-mateo-downtown.jpg"',
        f'src="{data["img"]}"'
    )

    # Fix the alt text for the hero image
    # Find the img in the hero section (near the city card)
    import re
    content = re.sub(
        r'(src="' + re.escape(data['img']) + r'"[^>]*alt=")[^"]*(")',
        r'\1' + data['alt'] + r'\2',
        content
    )

    # Replace OG image
    content = content.replace(
        'https://www.dvspecialists.com/images/san-mateo-downtown.jpg',
        data['og']
    )

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'  UPDATED: {filename} → {data["img"]}')
    else:
        print(f'  NO CHANGE: {filename}')

print('\nDone.')
