#!/usr/bin/env python3
"""Update service section descriptions on city pages to be localized for AEO/GEO."""

import os
import re

# City-specific service localizations
city_data = {
    "san-mateo": {
        "city": "San Mateo",
        "heading": "Dryer Vent Services for Every San Mateo Home",
        "sub": "What We Offer in San Mateo",
        "cleaning": "Clogged dryer vents are a leading cause of home fires in San Mateo County. Our professional cleaning delivers a complete solution for San Mateo homes — from 1940s Baywood-Knolls bungalows to modern Hillsdale condos. We clean the dryer, transition hose, and entire vent run using rotary brush and HEPA-filtered vacuum. Most San Mateo jobs are done in under an hour.",
        "repair": "Many San Mateo homes built between the 1940s and 1970s have aging vent systems with crushed ducts, disconnected joints, or non-compliant foil hoses routed through walls and crawl spaces. We replace damaged sections with fire-rated, UL-listed rigid metal duct that meets current San Mateo County building code.",
        "dryerjack": "San Mateo's coastal proximity means exterior vent caps face salt air and moisture. We install DryerJack high-efficiency termination caps that seal tightly when inactive — keeping out pests, moisture, and back-draft while maximizing exhaust airflow.",
        "magvent": "MagVent magnetic coupling systems are ideal for San Mateo laundry closets where space is tight. The magnetic connection eliminates crushed hoses behind the dryer, improves airflow, and allows easy disconnection for future cleanings — no tools required.",
        "commercial": "San Mateo's multi-unit buildings along El Camino Real, in the Fiesta Gardens area, and near Marina Lagoon require commercial-grade vent cleaning. We serve apartment complexes, condos, and HOA communities with bulk pricing, compliance documentation, and scheduled maintenance contracts.",
    },
    "burlingame": {
        "city": "Burlingame",
        "heading": "Dryer Vent Services for Every Burlingame Home",
        "sub": "What We Offer in Burlingame",
        "cleaning": "Burlingame's 1920s–1950s homes in Burlingame Hills, Easton Addition, and Ray Park often have vintage vent configurations that accumulate lint faster than modern systems. Our professional cleaning covers the dryer, transition hose, and full vent run using rotary brush and HEPA-filtered vacuum. Most Burlingame jobs are done in under an hour.",
        "repair": "Older Burlingame homes frequently have vent systems routed through plaster walls and tight crawl spaces with non-compliant flexible hoses. We replace damaged sections with fire-rated, UL-listed rigid metal duct that meets current San Mateo County building code requirements.",
        "dryerjack": "Burlingame's tree-lined neighborhoods mean exterior vent caps can attract nesting birds and debris. We install DryerJack termination caps that seal tightly when inactive, keeping out pests and back-draft while maximizing exhaust airflow from your dryer.",
        "magvent": "MagVent magnetic coupling is perfect for Burlingame's older homes where dryers are tucked into closets or tight utility spaces. The magnetic connection eliminates crushed hoses, improves airflow, and allows the dryer to sit flush against the wall.",
        "commercial": "Burlingame's multi-unit properties along California Drive, Broadway, and El Camino Real require commercial-grade vent cleaning. We serve apartment buildings, condo associations, and property managers with bulk pricing and compliance documentation.",
    },
    "hillsborough": {
        "city": "Hillsborough",
        "heading": "Dryer Vent Services for Every Hillsborough Estate",
        "sub": "What We Offer in Hillsborough",
        "cleaning": "Hillsborough's large estate homes — including properties in Carolands and Upper Hillsborough — often feature 30- to 50-foot vent runs through multiple floors with roof terminations. Our professional cleaning uses commercial-grade rotary brush systems and HEPA-filtered vacuum equipment designed for these extended runs.",
        "repair": "Hillsborough estates frequently have complex vent routing through multiple stories, requiring specialized repair work. We replace damaged or deteriorated duct sections with fire-rated, UL-listed rigid metal duct, and can re-route systems to reduce overall vent length and improve airflow efficiency.",
        "dryerjack": "Hillsborough homes with roof-exit vents face unique weathering challenges. We install DryerJack high-efficiency termination caps rated for exposed roof installations — sealing tightly against rain, wind, and wildlife while maintaining maximum exhaust flow.",
        "magvent": "For Hillsborough homes with premium laundry rooms, MagVent magnetic coupling provides a clean, professional connection that eliminates the crushed hose behind the dryer. Easy disconnection means future cleanings take less time and cause zero disruption.",
        "commercial": "Hillsborough property managers overseeing estate maintenance trust our detailed service reports with before-and-after airflow measurements. We provide documentation suitable for home sale disclosures, insurance records, and annual property maintenance files.",
    },
    "belmont": {
        "city": "Belmont",
        "heading": "Dryer Vent Services for Every Belmont Home",
        "sub": "What We Offer in Belmont",
        "cleaning": "Belmont homes built during the 1950s–1960s postwar boom — particularly in Belmont Village, Hallmark, and the Carlmont area — have vent systems running through walls and under floors that collect lint over decades. Our cleaning covers the dryer, hose, and full vent run with rotary brush and HEPA-filtered vacuum.",
        "repair": "Many Belmont homes have vent ducts routed through crawl spaces and hillside foundations where sections can disconnect or deteriorate over time. We replace damaged duct with fire-rated, UL-listed rigid metal that meets San Mateo County building code.",
        "dryerjack": "Belmont's hillside properties face unique exterior vent challenges with varying wall angles and weather exposure. We install DryerJack termination caps that seal tightly against hillside wind and moisture while maximizing exhaust airflow.",
        "magvent": "MagVent magnetic coupling is ideal for Belmont homes where the dryer sits in a closet or tight laundry space near Ralston Avenue or the Carlmont area. The magnetic connection eliminates crushed hoses and improves airflow without requiring extra clearance.",
        "commercial": "Belmont's multi-unit properties and townhome communities require commercial-grade vent cleaning. We serve condo associations, apartment complexes, and property managers with bulk pricing, scheduled maintenance, and compliance documentation.",
    },
    "san-carlos": {
        "city": "San Carlos",
        "heading": "Dryer Vent Services for Every San Carlos Home",
        "sub": "What We Offer in San Carlos",
        "cleaning": "San Carlos homes in White Oaks, Devonshire, and the Crestview area — many with raised foundations — have vent systems routed through crawl spaces that collect lint over time. Our cleaning covers the complete system using rotary brush and HEPA-filtered vacuum. Most San Carlos jobs are done in under an hour.",
        "repair": "Raised-foundation homes in San Carlos often have vent ducts running beneath the house where they can disconnect, sag, or accumulate moisture. We replace damaged sections with fire-rated, UL-listed rigid metal duct that meets San Mateo County building code.",
        "dryerjack": "San Carlos exterior vent caps need to handle the area's warm inland temperatures and occasional wildlife intrusion. We install DryerJack termination caps that seal tightly when inactive, keeping out pests and back-draft while maximizing dryer exhaust flow.",
        "magvent": "MagVent magnetic coupling works well in San Carlos homes where dryers are in garage-adjacent laundry areas. The magnetic connection eliminates crushed hoses, improves airflow, and makes future cleanings faster and tool-free.",
        "commercial": "San Carlos multi-unit properties along Laurel Street and the Industrial Road area require commercial-grade vent cleaning. We serve apartment buildings, condo associations, and property managers with bulk pricing and HOA-approved documentation.",
    },
    "redwood-city": {
        "city": "Redwood City",
        "heading": "Dryer Vent Services for Every Redwood City Home",
        "sub": "What We Offer in Redwood City",
        "cleaning": "Redwood City's diverse housing — from 1950s ranches in Woodside Plaza to modern condos in Redwood Shores — each have unique venting needs. Our cleaning covers the dryer, transition hose, and full vent run with rotary brush and HEPA-filtered vacuum. The Redwood City Fire Department recommends annual vent cleaning.",
        "repair": "Redwood City homes across multiple eras have varying vent configurations — some compliant, many not. We replace damaged or non-compliant duct sections with fire-rated, UL-listed rigid metal duct that meets San Mateo County building code.",
        "dryerjack": "Redwood City's warmer climate and occasional high winds mean exterior vent caps face specific weathering. We install DryerJack termination caps that seal tightly when inactive, preventing pest intrusion and back-draft while maximizing exhaust flow.",
        "magvent": "MagVent magnetic coupling is a smart upgrade for Redwood City homes and condos where space behind the dryer is limited. The magnetic connection eliminates crushed hoses, improves airflow, and allows the dryer to sit closer to the wall.",
        "commercial": "Redwood City and Redwood Shores have significant multi-unit housing that requires commercial-grade vent cleaning. We serve apartment complexes, condo buildings, and laundromats with bulk pricing, scheduled maintenance contracts, and compliance documentation.",
    },
    "menlo-park": {
        "city": "Menlo Park",
        "heading": "Dryer Vent Services for Every Menlo Park Home",
        "sub": "What We Offer in Menlo Park",
        "cleaning": "Menlo Park homes span from 1930s cottages in The Willows to modern builds in Sharon Heights, each with unique venting configurations. Our professional cleaning covers the dryer, transition hose, and full vent run using rotary brush and HEPA-filtered vacuum. Most Menlo Park jobs are done in under an hour.",
        "repair": "Older Menlo Park homes in Allied Arts and The Willows often have vent systems that predate current building codes. We replace damaged or non-compliant duct sections with fire-rated, UL-listed rigid metal duct that meets San Mateo County standards.",
        "dryerjack": "Menlo Park's mature tree canopy means exterior vent caps can attract birds and collect debris. We install DryerJack termination caps that seal tightly when inactive, keeping out pests, leaves, and moisture while maximizing exhaust airflow.",
        "magvent": "MagVent magnetic coupling is ideal for Menlo Park homes where laundry is in a closet or tight utility space. The tool-free magnetic connection eliminates crushed hoses behind the dryer, improving airflow and making future cleanings effortless.",
        "commercial": "Menlo Park's multi-unit properties and Belle Haven apartment communities require commercial-grade vent cleaning. We serve property managers, condo associations, and landlords with bulk pricing and detailed compliance documentation.",
    },
    "half-moon-bay": {
        "city": "Half Moon Bay",
        "heading": "Dryer Vent Services for Every Coastside Home",
        "sub": "What We Offer on the Coastside",
        "cleaning": "Half Moon Bay's coastal environment — including Miramar, El Granada, Princeton-by-the-Sea, and Moss Beach — exposes dryer vents to salt air and humidity that accelerate lint buildup and corrosion. Our cleaning removes compacted, moisture-laden lint using rotary brush and HEPA-filtered vacuum designed for coastal conditions.",
        "repair": "Coastside homes face accelerated vent deterioration from salt air corrosion. Galvanized steel ducts can rust through in as little as 5–7 years in the Half Moon Bay microclimate. We replace corroded sections with marine-grade, fire-rated rigid metal duct built to withstand coastal conditions.",
        "dryerjack": "Half Moon Bay's salt air, fog, and coastal winds make exterior vent cap selection critical. We install DryerJack termination caps with corrosion-resistant finishes that seal tightly against ocean-driven moisture, wind, and salt spray while maintaining maximum exhaust flow.",
        "magvent": "MagVent magnetic coupling helps Half Moon Bay homeowners maintain proper airflow in humid conditions. The tool-free magnetic connection eliminates crushed hoses where moisture can condense, and allows easy disconnection for the more frequent cleanings coastal homes require.",
        "commercial": "Half Moon Bay's vacation rentals, bed-and-breakfasts, and small multi-unit properties along Highway 1 require reliable vent maintenance. We provide scheduled cleaning contracts and compliance documentation for commercial property operators on the Coastside.",
    },
    "san-francisco": {
        "city": "San Francisco",
        "heading": "Dryer Vent Services for Every SF Home &amp; Building",
        "sub": "What We Offer in San Francisco",
        "cleaning": "San Francisco's Victorian and Edwardian row houses, TICs, and multi-unit buildings — particularly in the Sunset, Richmond, Noe Valley, and Mission — present unique venting challenges with long runs through shared walls and multiple floors. Our cleaning handles even the most complex SF vent systems with commercial-grade rotary brush and HEPA-filtered vacuum.",
        "repair": "San Francisco's dense housing stock means vent systems are often routed through shared walls, tight crawl spaces, and multiple stories. We replace damaged or non-compliant duct sections with fire-rated, UL-listed rigid metal duct that meets San Francisco building code requirements.",
        "dryerjack": "San Francisco's fog, wind, and salt air mean exterior vent caps face significant weathering. We install DryerJack termination caps that seal tightly against the elements — critical in Sunset and Richmond district homes where ocean-facing vents take a beating.",
        "magvent": "MagVent magnetic coupling is essential for San Francisco's compact living spaces where dryers are crammed into closets or alcoves. The magnetic connection eliminates crushed hoses, improves airflow in tight spaces, and allows the dryer to sit flush against the wall.",
        "commercial": "San Francisco's apartment buildings, TICs, condo associations, and laundromats require commercial-grade vent cleaning. We serve multi-unit properties across all SF neighborhoods with bulk pricing, SFFD-compliant documentation, and scheduled maintenance contracts.",
    },
    "south-san-francisco": {
        "city": "South San Francisco",
        "heading": "Dryer Vent Services for Every South City Home",
        "sub": "What We Offer in South San Francisco",
        "cleaning": "South San Francisco homes in Westborough, Sunshine Gardens, and the Sign Hill area — many built during the mid-century housing boom — have vent systems that accumulate decades of lint. Our cleaning covers the dryer, hose, and full vent run with rotary brush and HEPA-filtered vacuum.",
        "repair": "Mid-century South San Francisco homes frequently have aging vent systems with non-compliant flexible hoses and deteriorated duct joints. We replace damaged sections with fire-rated, UL-listed rigid metal duct that meets current San Mateo County building code.",
        "dryerjack": "South San Francisco's windy hillside neighborhoods mean exterior vent caps need to resist back-draft and debris intrusion. We install DryerJack termination caps that seal tightly when inactive while maintaining maximum exhaust flow during operation.",
        "magvent": "MagVent magnetic coupling is a smart upgrade for South San Francisco homes where dryers are in tight laundry closets or garage-adjacent spaces. The tool-free magnetic connection eliminates crushed hoses and improves airflow efficiency.",
        "commercial": "South San Francisco's multi-unit housing communities and commercial properties along El Camino Real and Grand Avenue require commercial-grade vent cleaning. We serve property managers and HOAs with bulk pricing, scheduled maintenance, and compliance documentation.",
    },
    "los-altos": {
        "city": "Los Altos",
        "heading": "Dryer Vent Services for Every Los Altos Home",
        "sub": "What We Offer in Los Altos",
        "cleaning": "Los Altos ranch-style homes in Country Club, Loyola Corners, and North Los Altos — many built in the 1950s and 1960s — often have vent systems running through attics and crawl spaces. Our cleaning covers the complete system with rotary brush and HEPA-filtered vacuum. We also serve Los Altos Hills.",
        "repair": "Los Altos homes with attic-routed vents face unique repair challenges — disconnected joints, sagging duct, and bird nest obstruction are common. We replace damaged sections with fire-rated, UL-listed rigid metal duct that meets Santa Clara County building code.",
        "dryerjack": "Los Altos's warm, dry climate and mature tree canopy mean exterior vent caps can attract birds and accumulate debris. We install DryerJack termination caps that seal tightly when inactive, preventing pest intrusion while maintaining maximum exhaust airflow.",
        "magvent": "MagVent magnetic coupling is ideal for Los Altos homes where the dryer is in a garage or dedicated laundry room. The magnetic connection eliminates crushed hoses, improves airflow, and makes future cleanings faster with tool-free disconnection.",
        "commercial": "Los Altos and Los Altos Hills property managers trust our detailed service reports for estate maintenance records, home sale disclosures, and insurance documentation. We also serve small multi-unit properties with scheduled maintenance contracts.",
    },
}


def update_services(filepath, slug):
    """Update service descriptions with city-specific content."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    data = city_data[slug]
    city = data["city"]

    # Update the section subtitle
    old_sub = f'What We Offer in {city}'
    if old_sub in content:
        content = content.replace(old_sub, data["sub"])

    # Update heading - "Our Services" -> city-specific heading
    # Find the services section heading specifically
    # Pattern: within services section, replace "Our Services" h2
    old_heading_pattern = re.compile(
        r'(<!-- SERVICES -->.*?<h2[^>]*>)(Our Services)(</h2>)',
        re.DOTALL
    )
    if old_heading_pattern.search(content):
        content = old_heading_pattern.sub(
            lambda m: m.group(1) + data["heading"] + m.group(3),
            content
        )
    else:
        # Try the full-page format
        old_heading_pattern2 = re.compile(
            r'(<!-- ── SERVICES ── -->.*?<h2[^>]*>)(Our Services)(</h2>)',
            re.DOTALL
        )
        if old_heading_pattern2.search(content):
            content = old_heading_pattern2.sub(
                lambda m: m.group(1) + data["heading"] + m.group(3),
                content
            )

    # Update Residential Cleaning description
    cleaning_pattern = re.compile(
        r'(<h3[^>]*>Residential Dryer Vent Cleaning</h3>\s*<p[^>]*>)(.*?)(</p>)',
        re.DOTALL
    )
    content = cleaning_pattern.sub(
        lambda m: m.group(1) + data["cleaning"] + m.group(3),
        content
    )

    # Update Repair description
    repair_pattern = re.compile(
        r'(<h3[^>]*>Dryer Vent Repair &amp; Replacement</h3>\s*<p[^>]*>)(.*?)(</p>)',
        re.DOTALL
    )
    content = repair_pattern.sub(
        lambda m: m.group(1) + data["repair"] + m.group(3),
        content
    )

    # Update DryerJack description
    dryerjack_pattern = re.compile(
        r'(<h3[^>]*>DryerJack Termination Install</h3>\s*<p[^>]*>)(.*?)(</p>)',
        re.DOTALL
    )
    content = dryerjack_pattern.sub(
        lambda m: m.group(1) + data["dryerjack"] + m.group(3),
        content
    )

    # Update MagVent description
    magvent_pattern = re.compile(
        r'(<h3[^>]*>MagVent Installation</h3>\s*<p[^>]*>)(.*?)(</p>)',
        re.DOTALL
    )
    content = magvent_pattern.sub(
        lambda m: m.group(1) + data["magvent"] + m.group(3),
        content
    )

    # Update Commercial description
    commercial_pattern = re.compile(
        r'(<h3[^>]*>Commercial &amp; Multi-Unit Cleaning</h3>\s*<p[^>]*>)(.*?)(</p>)',
        re.DOTALL
    )
    content = commercial_pattern.sub(
        lambda m: m.group(1) + data["commercial"] + m.group(3),
        content
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"  DONE: {filepath}")
    return True


def main():
    base_dir = '/Users/michaelredman/Documents/GitHub/dvspecialists'
    for slug in city_data:
        filepath = os.path.join(base_dir, f'dryer-vent-cleaning-{slug}.html')
        if os.path.exists(filepath):
            update_services(filepath, slug)
        else:
            print(f"  NOT FOUND: {filepath}")


if __name__ == '__main__':
    main()
