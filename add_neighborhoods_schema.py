#!/usr/bin/env python3
"""Add neighborhood areaServed to LocalBusiness JSON-LD on all city template pages."""
import json, re, glob

CITY_NEIGHBORHOODS = {
    'dryer-vent-cleaning-belmont-template.html': [
        'Belmont Hills', 'Cipriani', 'Sterling Downs', 'Homeview',
        'Plateau-Skymont', 'Belmont Woods', 'Central Belmont', 'Downtown Belmont', 'Western Hills'
    ],
    'dryer-vent-cleaning-burlingame-template.html': [
        'Burlingame Hills', 'Easton Addition', 'Burlingame Park', 'Oak Grove',
        'Burlingame Terrace', 'Lyons Hoag', 'Mills Estate', 'Ray Park',
        'East of El Camino', 'Burlingame Gardens'
    ],
    'dryer-vent-cleaning-half-moon-bay-template.html': [
        'Arleta Park', "Frenchman's Creek", 'Ocean Colony', 'Miramar',
        'Canada Cove', 'Grandview Terrace', 'Casa Heights', 'Highland Park',
        'El Granada', 'Moss Beach'
    ],
    'dryer-vent-cleaning-hillsborough-template.html': [
        'Lower Hillsborough', 'Upper Hillsborough', 'Hillsborough Hills',
        'Hillsborough Park', 'Carolands', 'Skyline'
    ],
    'dryer-vent-cleaning-los-altos-template.html': [
        'North Los Altos', 'South Los Altos', 'Country Club',
        'Loyola Corners', 'Old Los Altos', 'Los Altos Hills'
    ],
    'dryer-vent-cleaning-menlo-park-template.html': [
        'West Menlo Park', 'Sharon Heights', 'Allied Arts', 'Downtown Menlo Park',
        'The Willows', 'Linfield Oaks', 'Belle Haven', 'Menlo Oaks',
        'Felton Gables', 'University Heights'
    ],
    'dryer-vent-cleaning-mountain-view-template.html': [
        'Old Mountain View', 'Downtown Mountain View', 'Cuesta Park', 'Waverly Park',
        'Rex Manor', 'Monta Loma', 'Sylvan Park', 'Blossom Valley',
        'North Whisman', 'Shoreline West', 'Gemello', 'Jackson Park'
    ],
    'dryer-vent-cleaning-palo-alto-template.html': [
        'Old Palo Alto', 'Crescent Park', 'College Terrace', 'Evergreen Park',
        'Barron Park', 'Gunn-Arastradero', 'Midtown', 'Southgate',
        'Downtown Palo Alto', 'University South', 'Charleston Meadows', 'Fairmeadow'
    ],
    'dryer-vent-cleaning-redwood-city-template.html': [
        'Emerald Hills', 'Farm Hills', 'Redwood Shores', 'Bair Island',
        'Mount Carmel', 'Edgewood Park', 'Centennial', 'Redwood Village',
        'Woodside Plaza', 'Roosevelt', 'Friendly Acres', 'Palm Park'
    ],
    'dryer-vent-cleaning-san-carlos-template.html': [
        'White Oaks', 'Clearfield Park', 'San Carlos Hills', 'Vista Park',
        'Howard Park', 'Cordes', 'Brittan Avenue', 'Elms',
        'Downtown San Carlos', 'The Laurels'
    ],
    'dryer-vent-cleaning-san-jose-template.html': [
        'Willow Glen', 'Rose Garden', 'Almaden Valley', 'Cambrian Park',
        'Japantown', 'Hensley', 'Evergreen', 'Silver Creek',
        'Berryessa', 'North San Jose', 'West San Jose', 'Campbell Border'
    ],
    'dryer-vent-cleaning-santa-clara-template.html': [
        'Old Quad', 'University Neighborhood', 'Central Park', 'Cabrillo Park',
        'Northside', 'Agnesi', 'Rivermark', 'Montague',
        'Santa Clara Mission District', 'Warburton', 'Washington'
    ],
    'dryer-vent-cleaning-south-san-francisco-template.html': [
        'Old Town', 'Downtown South San Francisco', 'Sunshine Gardens', 'Buri Buri',
        'Paradise Valley', 'Terrabay', 'Westborough', 'Sign Hill',
        'El Camino Corridor', 'Lindenville', 'Alta Loma', 'Avalon'
    ],
    'dryer-vent-cleaning-sunnyvale-template.html': [
        'Downtown Sunnyvale', 'Heritage District', 'Cherry Chase', 'Lakewood Village',
        'Birdland', 'Ponderosa Park', 'Raynor Park', 'Braly Park',
        'Ortega Park', 'Sunnyvale West', 'East Sunnyvale', 'Fair Oaks'
    ],
    'dryer-vent-cleaning-san-francisco-template.html': [
        'Marina', 'Cow Hollow', 'Pacific Heights', 'Russian Hill', 'North Beach',
        'Hayes Valley', 'The Castro', 'Noe Valley', 'Mission District', 'SoMa',
        'Richmond District', 'Sunset District', 'Sea Cliff', 'West Portal',
        'Dogpatch', 'Potrero Hill', 'Bernal Heights', 'Bayview',
        'Glen Park', 'Excelsior', 'Ingleside', 'Visitacion Valley'
    ],
    'dryer-vent-cleaning-san-mateo-template.html': [
        'Downtown San Mateo', 'Baywood', 'Hayward Park',
        'Shoreview', 'Los Prados', 'Bowie Estate',
        'San Mateo Park', 'Beresford Manor', 'Hillsdale',
        'Lauriedale', 'Sugarloaf', 'Westwood Oaks',
        'North Shoreview', 'Woodlake'
    ],
}

# City name extracted from filename
def city_from_filename(f):
    mapping = {
        'belmont': 'Belmont',
        'burlingame': 'Burlingame',
        'half-moon-bay': 'Half Moon Bay',
        'hillsborough': 'Hillsborough',
        'los-altos': 'Los Altos',
        'menlo-park': 'Menlo Park',
        'mountain-view': 'Mountain View',
        'palo-alto': 'Palo Alto',
        'redwood-city': 'Redwood City',
        'san-carlos': 'San Carlos',
        'san-jose': 'San Jose',
        'san-mateo': 'San Mateo',
        'san-francisco': 'San Francisco',
        'santa-clara': 'Santa Clara',
        'south-san-francisco': 'South San Francisco',
        'sunnyvale': 'Sunnyvale',
    }
    for key, val in mapping.items():
        if key in f:
            return val
    return None

updated = []

for filename, neighborhoods in CITY_NEIGHBORHOODS.items():
    city = city_from_filename(filename)
    if not city:
        print(f"  SKIP: Could not determine city for {filename}")
        continue

    with open(filename, 'r') as fh:
        content = fh.read()

    # Build the areaServed array with city + neighborhoods
    area_served = {
        "@type": "City",
        "name": city,
        "containedInPlace": {
            "@type": "State",
            "name": "California"
        }
    }

    neighborhood_areas = [
        {"@type": "Neighborhood", "name": n, "containedInPlace": {"@type": "City", "name": city}}
        for n in neighborhoods
    ]

    area_served_block = json.dumps([area_served] + neighborhood_areas, indent=6)
    # Fix indentation to match existing JSON-LD (4 spaces base)
    area_served_block = area_served_block.replace('\n', '\n    ')

    # Find existing areaServed in the LocalBusiness JSON-LD and replace it
    # Pattern: "areaServed": { ... } followed by a comma or closing brace
    # The existing areaServed is a single City object with containedInPlace
    old_pattern = r'"areaServed":\s*\{\s*"@type":\s*"City",\s*"name":\s*"' + re.escape(city) + r'"[^}]*"containedInPlace":\s*\{[^}]*\}\s*\}'

    match = re.search(old_pattern, content)
    if match:
        new_area = f'"areaServed": {area_served_block}'
        content = content[:match.start()] + new_area + content[match.end():]

        with open(filename, 'w') as fh:
            fh.write(content)
        updated.append(filename)
        print(f"  Updated {filename} ({len(neighborhoods)} neighborhoods)")
    else:
        print(f"  NO MATCH in {filename} - checking for alternate pattern...")
        # Try simpler pattern
        simple = re.search(r'"areaServed":\s*\{', content)
        if simple:
            # Find the matching closing brace
            start = simple.start()
            depth = 0
            end = start
            in_area = False
            for i in range(start, len(content)):
                if content[i] == '{':
                    depth += 1
                    in_area = True
                elif content[i] == '}':
                    depth -= 1
                    if in_area and depth == 0:
                        end = i + 1
                        break

            old_block = content[start:end]
            new_area = f'"areaServed": {area_served_block}'
            content = content[:start] + new_area + content[end:]

            with open(filename, 'w') as fh:
                fh.write(content)
            updated.append(filename)
            print(f"  Updated {filename} (fallback) ({len(neighborhoods)} neighborhoods)")
        else:
            print(f"  FAILED: No areaServed found in {filename}")

print(f"\nUpdated {len(updated)} of {len(CITY_NEIGHBORHOODS)} files")
