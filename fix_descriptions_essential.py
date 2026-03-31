#!/usr/bin/env python3
"""Fix duplicate meta descriptions and make 'Why Essential' section unique per city."""
import re

CITY_DATA = {
    'dryer-vent-cleaning-san-mateo-template.html': {
        'city': 'San Mateo',
        'desc': 'Dryer vent cleaning in San Mateo, CA. CDET-certified, veteran-owned. Serving Baywood, Hillsdale, and all neighborhoods. Call (650) 484-4418.',
        'essential': [
            ('Fire Prevention', 'San Mateo Fire Department data shows dryer lint is a top cause of residential fires. Our rotary brush and HEPA vacuum system removes accumulated lint from your entire vent run, eliminating the fuel source before it becomes a hazard.'),
            ('Lower Energy Costs', 'A restricted vent forces your dryer to work harder and longer. San Mateo homeowners typically see PG&E savings of $15 to $25 per month after cleaning, with most dryers returning to single-cycle performance immediately.'),
            ('Appliance Longevity', 'Overheating from poor airflow is the leading cause of dryer component failure. Regular vent cleaning reduces strain on heating elements, thermostats, and motors, extending the life of your dryer by years.'),
            ('Moisture Control', 'Blocked vents push hot, humid air back into your laundry area. In San Mateo homes near the bay with limited ventilation, this trapped moisture can lead to mold growth inside walls and around the dryer area.'),
        ],
    },
    'dryer-vent-cleaning-san-francisco-template.html': {
        'city': 'San Francisco',
        'desc': 'Dryer vent cleaning in San Francisco. CDET-certified service for row houses, Victorians, and multi-unit buildings. Same-day appointments. (650) 484-4418.',
        'essential': [
            ('Fire Prevention', 'San Francisco row houses and multi-unit buildings have some of the most complex dryer vent configurations in the Bay Area. Long vertical runs through multiple floors collect lint in hidden bends, creating serious fire risk that only professional cleaning can address.'),
            ('Lower Energy Costs', 'With San Francisco electricity rates among the highest in California, a clogged vent wasting 30% more energy per load adds up fast. Annual cleaning typically pays for itself within months through reduced PG&E bills.'),
            ('Appliance Longevity', 'The compact laundry setups in San Francisco apartments and flats often mean dryers are pushed tight against walls, crushing transition hoses. Our service inspects and corrects these issues, preventing premature dryer failure.'),
            ('Moisture Control', 'San Francisco fog and humidity combined with a blocked vent creates ideal conditions for mold and mildew. Proper vent cleaning restores exhaust airflow, keeping moisture out of your walls and living spaces.'),
        ],
    },
    'dryer-vent-cleaning-south-san-francisco-template.html': {
        'city': 'South San Francisco',
        'desc': 'Dryer vent cleaning in South San Francisco. CDET-certified techs serving Westborough, Sunshine Gardens, and all SSF areas. (650) 484-4418.',
        'essential': [
            ('Fire Prevention', 'South San Francisco homes in Sunshine Gardens and Buri Buri were largely built in the 1950s and 1960s with dryer vents routed through crawl spaces and wall cavities. These older configurations trap lint in hard-to-reach areas that only professional rotary brush cleaning can clear.'),
            ('Lower Energy Costs', 'A restricted dryer vent forces your dryer to run longer per load. SSF homeowners running 4 to 5 loads weekly can save $15 to $25 per month on energy bills after professional cleaning restores full airflow.'),
            ('Appliance Longevity', 'Overheating from blocked airflow is the leading cause of dryer component failure. Regular cleaning reduces strain on heating elements and motors, extending the useful life of your dryer by several years.'),
            ('Moisture Control', 'South San Francisco sits in a coastal microclimate with frequent fog. When a blocked vent pushes humid exhaust back into your home, it compounds existing moisture issues and can promote mold growth in laundry areas.'),
        ],
    },
    'dryer-vent-cleaning-burlingame-template.html': {
        'city': 'Burlingame',
        'desc': 'Dryer vent cleaning in Burlingame, CA. Craftsman and Tudor home specialists. CDET-certified, veteran-owned. Same-day service. (650) 484-4418.',
        'essential': [
            ('Fire Prevention', 'Burlingame Craftsman and Tudor homes often have dryer vents that were retrofitted into existing wall cavities during remodels. These complex vent paths with multiple bends trap lint in hidden areas, creating fire hazards that standard cleaning cannot reach.'),
            ('Lower Energy Costs', 'A clogged vent can increase drying time and energy usage by 30% per load. For Burlingame households with high PG&E rates, annual cleaning typically saves $150 to $300 per year in electricity costs alone.'),
            ('Appliance Longevity', 'When airflow is restricted, your dryer overheats with every cycle. This accelerates wear on heating elements, thermal fuses, and motors. Burlingame homeowners who clean annually report significantly fewer service calls and longer appliance lifespans.'),
            ('Moisture Control', 'Burlingame homes in the Easton Addition and near the bay experience higher ambient humidity. A blocked vent traps moisture inside your home, potentially causing mold in laundry rooms and inside wall cavities around the vent path.'),
        ],
    },
    'dryer-vent-cleaning-hillsborough-template.html': {
        'city': 'Hillsborough',
        'desc': 'Dryer vent cleaning for Hillsborough estates. CDET-certified techs experienced with long vent runs and roof terminations. (650) 484-4418.',
        'essential': [
            ('Fire Prevention', 'Hillsborough estates often have dryer vents running 30 to 50 feet through multiple floors and attic spaces before reaching a roof termination. These long runs accumulate lint in areas invisible to homeowners, creating significant fire risk without professional intervention.'),
            ('Lower Energy Costs', 'Large Hillsborough homes with extended vent runs experience more airflow resistance, causing dryers to run longer and consume more energy. Professional cleaning restores full airflow and can reduce drying times by half.'),
            ('Appliance Longevity', 'High-end dryers in Hillsborough homes represent a significant investment. Restricted airflow forces these machines to overheat, shortening their lifespan. Annual cleaning protects your equipment and prevents costly repairs or premature replacement.'),
            ('Moisture Control', 'Multi-level Hillsborough homes with long vent runs are especially susceptible to condensation buildup inside the ductwork. This trapped moisture can damage structural elements and promote mold growth in walls and ceilings along the vent path.'),
        ],
    },
    'dryer-vent-cleaning-belmont-template.html': {
        'city': 'Belmont',
        'desc': 'Dryer vent cleaning in Belmont, CA. Hillside home specialists. CDET-certified, veteran-owned. Serving Cipriani to Sterling Downs. (650) 484-4418.',
        'essential': [
            ('Fire Prevention', 'Belmont hillside homes often have dryer vents running at steep angles through foundations and crawl spaces. These configurations collect lint at bends and low points where airflow slows, creating concentrated fire hazards that only professional rotary brush cleaning can address.'),
            ('Lower Energy Costs', 'A restricted vent can increase your dryer energy consumption by 30% or more per load. Belmont homeowners who clean their vents annually typically recoup the cost within a few months through lower PG&E bills.'),
            ('Appliance Longevity', 'When lint restricts exhaust airflow, your dryer runs hotter and longer every cycle. This accelerates wear on heating elements, bearings, and sensors. Regular cleaning in Belmont homes with complex vent routes prevents premature appliance failure.'),
            ('Moisture Control', 'Belmont homes in Western Hills and Plateau-Skymont sit in areas with morning fog and limited natural ventilation. A blocked dryer vent pushes humid air back into your laundry area, creating conditions for mold and wood damage.'),
        ],
    },
    'dryer-vent-cleaning-san-carlos-template.html': {
        'city': 'San Carlos',
        'desc': 'Dryer vent cleaning in San Carlos, CA. CDET-certified service for homes in White Oaks, Howard Park, and San Carlos Hills. (650) 484-4418.',
        'essential': [
            ('Fire Prevention', 'San Carlos homes in neighborhoods like White Oaks and Howard Park feature a mix of 1940s to 1960s construction with dryer vents routed through walls, under floors, and up to roof exits. Lint accumulates at every turn, creating fire hazards only professional cleaning can eliminate.'),
            ('Lower Energy Costs', 'San Carlos homeowners running 4 to 5 loads per week with a restricted vent can waste $15 to $25 monthly on excess energy. Professional cleaning restores full airflow and typically cuts drying time in half.'),
            ('Appliance Longevity', 'Dryers in San Carlos homes with longer vent runs work harder every cycle to push air through lint-restricted ducts. This constant strain shortens appliance life. Annual cleaning reduces wear and prevents costly breakdowns.'),
            ('Moisture Control', 'San Carlos properties on the hillside and in The Laurels area can experience trapped moisture when dryer vents are blocked. Humid exhaust pushed back into the home promotes mold and can damage drywall and framing near the vent path.'),
        ],
    },
    'dryer-vent-cleaning-redwood-city-template.html': {
        'city': 'Redwood City',
        'desc': 'Dryer vent cleaning in Redwood City, CA. CDET-certified techs serving Emerald Hills, Redwood Shores, and all neighborhoods. (650) 484-4418.',
        'essential': [
            ('Fire Prevention', 'Redwood City has a diverse housing mix from mid-century ranches in Woodside Plaza to newer construction in Redwood Shores. Each building type presents unique vent configurations where lint accumulates. Professional cleaning removes buildup throughout the entire vent system.'),
            ('Lower Energy Costs', 'A blocked dryer vent wastes energy by forcing your dryer to run multiple cycles. Redwood City homeowners see an immediate improvement after cleaning, with most dryers returning to single-cycle performance and lower utility bills.'),
            ('Appliance Longevity', 'Restricted airflow causes dryers to overheat, wearing out heating elements, thermal fuses, and drum bearings prematurely. Annual vent cleaning in Redwood City homes protects your investment and extends appliance life.'),
            ('Moisture Control', 'Redwood City properties near the bay and in low-lying areas of Bair Island are more susceptible to humidity issues. A clogged vent compounds this by trapping moisture in your laundry area and inside wall cavities.'),
        ],
    },
    'dryer-vent-cleaning-menlo-park-template.html': {
        'city': 'Menlo Park',
        'desc': 'Dryer vent cleaning in Menlo Park, CA. CDET-certified service for homes in Sharon Heights, The Willows, and Belle Haven. (650) 484-4418.',
        'essential': [
            ('Fire Prevention', 'Menlo Park mid-century homes in The Willows and Linfield Oaks frequently have dryer vents running through crawl spaces and interior walls with multiple elbows. Lint trapped at each bend creates cumulative fire risk that professional rotary brush cleaning eliminates.'),
            ('Lower Energy Costs', 'With Menlo Park energy rates above the state average, a dryer vent running at 30% reduced efficiency costs real money. Annual cleaning restores full airflow and typically pays for itself in energy savings within three to four months.'),
            ('Appliance Longevity', 'Menlo Park homeowners invest in quality appliances. Restricted vent airflow forces dryers to overheat every cycle, degrading components and shortening machine life. Regular cleaning is the simplest way to protect that investment.'),
            ('Moisture Control', 'Menlo Park homes near San Francisquito Creek and in low-lying areas of Belle Haven experience higher ambient moisture. A blocked vent pushing humid exhaust back inside amplifies the problem, potentially causing mold in laundry areas and adjacent rooms.'),
        ],
    },
    'dryer-vent-cleaning-palo-alto-template.html': {
        'city': 'Palo Alto',
        'desc': 'Dryer vent cleaning in Palo Alto, CA. Eichler and pre-war home specialists. CDET-certified, veteran-owned. Same-day service. (650) 484-4418.',
        'essential': [
            ('Fire Prevention', 'Palo Alto Eichler homes with post-and-beam construction and slab foundations route dryer vents horizontally under or through the slab. These long, low-slope runs are especially prone to lint accumulation and require professional rotary brush cleaning to clear completely.'),
            ('Lower Energy Costs', 'A restricted dryer vent can increase energy use by 30% per cycle. Palo Alto homeowners on the city utility system see direct savings after cleaning, with most dryers returning to efficient single-cycle operation immediately.'),
            ('Appliance Longevity', 'Pre-war homes in Old Palo Alto and Crescent Park often have retrofitted vent systems with tight bends that strain dryer motors and heating elements. Annual cleaning reduces this strain and extends appliance life by years.'),
            ('Moisture Control', 'Palo Alto homes with slab foundations are particularly vulnerable to moisture issues from blocked vents. Humid exhaust pushed back into the home has nowhere to drain, promoting mold growth in laundry areas and adjacent walls.'),
        ],
    },
    'dryer-vent-cleaning-los-altos-template.html': {
        'city': 'Los Altos',
        'desc': 'Dryer vent cleaning in Los Altos and Los Altos Hills. CDET-certified techs for ranch homes and estates. Same-day service. (650) 484-4418.',
        'essential': [
            ('Fire Prevention', 'Los Altos ranch homes from the 1950s and 1960s in Country Club and Loyola Corners typically have dryer vents running 15 to 25 feet through crawl spaces before reaching an exterior wall. Lint accumulates along these horizontal runs and must be professionally removed.'),
            ('Lower Energy Costs', 'Los Altos homeowners on Silicon Valley Power or PG&E can save $150 to $300 annually by maintaining clear dryer vent airflow. A single professional cleaning often cuts drying time in half and eliminates wasted energy.'),
            ('Appliance Longevity', 'Ranch-style homes in Los Altos put dryers at floor level with vents running under the house. Restricted airflow in these crawl space runs forces dryers to overheat, wearing out components faster. Annual cleaning prevents premature appliance failure.'),
            ('Moisture Control', 'Los Altos homes with crawl spaces are susceptible to condensation in dryer vent ducts during cooler months. Lint-blocked vents trap this moisture, which can lead to rust, duct deterioration, and mold in the crawl space.'),
        ],
    },
    'dryer-vent-cleaning-mountain-view-template.html': {
        'city': 'Mountain View',
        'desc': 'Dryer vent cleaning in Mountain View, CA. Slab home and townhome specialists. CDET-certified, veteran-owned. Same-day service. (650) 484-4418.',
        'essential': [
            ('Fire Prevention', 'Mountain View homes in Monta Loma and Rex Manor were built on slab foundations with dryer vents running horizontally through or under the slab. These long, low-slope configurations are prone to lint accumulation and represent a significant fire risk without annual professional cleaning.'),
            ('Lower Energy Costs', 'Mountain View residents on Silicon Valley Power pay competitive rates, but a clogged vent still wastes 30% or more energy per cycle. Annual cleaning restores efficient airflow and reduces drying times, saving money on every load.'),
            ('Appliance Longevity', 'Newer townhomes in North Whisman and Shoreline West often have dryers in interior closets with vents routed vertically through upper floors. This configuration requires the dryer to push air harder, accelerating wear. Professional cleaning keeps these systems running efficiently.'),
            ('Moisture Control', 'Mountain View sits near the bay with higher ambient humidity. Blocked dryer vents trap moist exhaust in interior laundry closets common in newer construction, creating conditions for mold and mildew that proper vent cleaning prevents.'),
        ],
    },
    'dryer-vent-cleaning-sunnyvale-template.html': {
        'city': 'Sunnyvale',
        'desc': 'Dryer vent cleaning in Sunnyvale, CA. Ranch home and multi-unit specialists. CDET-certified. Serving Cherry Chase to Fair Oaks. (650) 484-4418.',
        'essential': [
            ('Fire Prevention', 'Sunnyvale ranch homes in Cherry Chase, Birdland, and Ponderosa Park have dryer vents running 15 to 30 feet through crawl spaces. These long horizontal runs accumulate lint at every joint and bend, requiring professional rotary brush cleaning to eliminate the fire risk.'),
            ('Lower Energy Costs', 'Sunnyvale electricity costs add up quickly when a clogged vent forces your dryer to run extra cycles. Professional cleaning restores full airflow and typically reduces energy consumption by 30% per load, paying for itself within months.'),
            ('Appliance Longevity', 'Post-war ranch homes in Sunnyvale often have dryers in garages with transition hoses crushed between the dryer and the wall. This double restriction, combined with a lint-filled vent, dramatically shortens dryer life. Our service addresses both issues.'),
            ('Moisture Control', 'Sunnyvale homes with slab foundations and interior laundry rooms are vulnerable to moisture problems when dryer vents are blocked. Humid exhaust pushed back into the home can promote mold growth, particularly in enclosed laundry areas with limited ventilation.'),
        ],
    },
    'dryer-vent-cleaning-santa-clara-template.html': {
        'city': 'Santa Clara',
        'desc': 'Dryer vent cleaning in Santa Clara, CA. CDET-certified service for homes near SCU, Old Quad, and Rivermark. Same-day available. (650) 484-4418.',
        'essential': [
            ('Fire Prevention', 'Santa Clara homes in the Old Quad and Washington neighborhoods date to the 1940s through 1960s and often have dryer vents with non-standard routing through walls and attic spaces. These older configurations trap lint in areas invisible to homeowners, creating fire hazards only professional cleaning can address.'),
            ('Lower Energy Costs', 'Santa Clara homeowners on Silicon Valley Power benefit from competitive electricity rates, but a clogged dryer vent still wastes significant energy. Annual cleaning restores efficient airflow and reduces drying time, saving money on every load.'),
            ('Appliance Longevity', 'The mix of older homes and newer construction in Santa Clara means dryer vent configurations vary widely. In both cases, restricted airflow from lint buildup forces dryers to overheat and wear out faster. Regular cleaning extends appliance life regardless of home age.'),
            ('Moisture Control', 'Santa Clara apartment buildings and condos near the university often have interior laundry rooms with limited ventilation. When dryer vents are blocked, moisture has nowhere to go, promoting mold growth in closets and adjacent walls.'),
        ],
    },
    'dryer-vent-cleaning-san-jose-template.html': {
        'city': 'San Jose',
        'desc': 'Dryer vent cleaning in San Jose, CA. CDET-certified techs serving Willow Glen, Almaden, Evergreen, and all neighborhoods. (650) 484-4418.',
        'essential': [
            ('Fire Prevention', 'The San Jose Fire Department responds to dozens of dryer-related fires annually. Homes in Willow Glen, Rose Garden, and the East Foothills have diverse vent configurations where lint accumulates in hidden bends and junctions. Professional cleaning removes this fuel source completely.'),
            ('Lower Energy Costs', 'San Jose households running 4 to 5 loads per week with a restricted vent can waste $20 to $30 monthly in excess energy. Professional cleaning restores full airflow and reduces drying times, with most homeowners noticing the difference immediately.'),
            ('Appliance Longevity', 'San Jose homes range from pre-war bungalows in Japantown to modern townhomes in North San Jose. All share the same risk: restricted airflow forces dryers to overheat and fail prematurely. Annual cleaning is the most cost-effective way to protect your dryer.'),
            ('Moisture Control', 'San Jose has a warmer, drier climate than the coastal Peninsula, but blocked dryer vents still create localized moisture problems. Homes in Cambrian Park and Almaden Valley with interior laundry rooms are particularly susceptible to mold when vents are restricted.'),
        ],
    },
    'dryer-vent-cleaning-half-moon-bay-template.html': {
        'city': 'Half Moon Bay',
        'desc': 'Dryer vent cleaning in Half Moon Bay, CA. Coastal home specialists. CDET-certified. Serving Ocean Colony, Miramar, and El Granada. (650) 484-4418.',
        'essential': [
            ('Fire Prevention', 'Half Moon Bay homes face unique dryer vent challenges from coastal salt air and wind exposure. Exterior vent covers corrode faster, and lint-packed ducts combined with degraded components create elevated fire risk. Annual professional cleaning and inspection is critical in the coastal environment.'),
            ('Lower Energy Costs', 'Coastal humidity in Half Moon Bay means dryers work harder to remove moisture from clothes, making efficient vent airflow even more important. Professional cleaning ensures your dryer exhausts properly, reducing cycle times and energy consumption by up to 30%.'),
            ('Appliance Longevity', 'Salt air accelerates corrosion of dryer vent components in Half Moon Bay homes. Regular cleaning and inspection catches deteriorating duct connections, rusted vent caps, and damaged seals before they cause appliance problems or safety hazards.'),
            ('Moisture Control', 'Half Moon Bay constant coastal fog and humidity make moisture control critical. A blocked dryer vent compounds the problem by trapping humid exhaust inside your home, creating ideal conditions for mold growth that can spread through wall cavities and ceiling spaces.'),
        ],
    },
}

ESSENTIAL_ICONS = ['&#128293;', '&#9889;', '&#9881;', '&#128167;']  # fire, lightning, gear, water
ESSENTIAL_HEADINGS = ['Fire Prevention', 'Lower Energy Costs', 'Appliance Longevity', 'Moisture Control']

updated = []

for filename, data in CITY_DATA.items():
    try:
        with open(filename, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"  SKIP: {filename}")
        continue

    original = content
    city = data['city']

    # 1. Fix meta description
    desc_pattern = r'<meta name="description" content="[^"]*"'
    new_desc = f'<meta name="description" content="{data["desc"]}"'
    content = re.sub(desc_pattern, new_desc, content, count=1)

    # 2. Fix "Why Essential" section cards
    # Match each of the 4 cards and replace their description text
    for i, (heading, new_text) in enumerate(data['essential']):
        # Find the card by its heading text
        card_pattern = rf'(<h3[^>]*>{re.escape(ESSENTIAL_HEADINGS[i])}</h3>\s*<p[^>]*>)(.*?)(</p>)'
        match = re.search(card_pattern, content, re.DOTALL)
        if match:
            content = content[:match.start(2)] + new_text + content[match.end(2):]

    if content != original:
        with open(filename, 'w') as f:
            f.write(content)
        updated.append(filename)
        print(f"  {filename}: Updated description + essential section")
    else:
        print(f"  {filename}: No changes needed")

print(f"\nUpdated {len(updated)} files")
