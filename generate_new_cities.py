#!/usr/bin/env python3
"""Generate city service pages for Palo Alto, Mountain View, Sunnyvale, Santa Clara, San Jose."""

import re

# Read the Belmont template
with open('/Users/michaelredman/Documents/GitHub/dvspecialists/dryer-vent-cleaning-belmont.html', 'r', encoding='utf-8') as f:
    TEMPLATE = f.read()

CITIES = {
    "palo-alto": {
        "name": "Palo Alto",
        "zip": "94301",
        "lat": "37.4419",
        "lng": "-122.1430",
        "wiki": "https://en.wikipedia.org/wiki/Palo_Alto,_California",
        "hero_img": "images/san-mateo-downtown.jpg",
        "hero_img_alt": "Downtown Palo Alto, CA",
        "hero_img_tag": "images/san-mateo-downtown.jpg",
        "safety_banner": "DRYER FIRES CAUSE OVER 15,000 HOUSE FIRES EACH YEAR - PROTECT YOUR PALO ALTO HOME TODAY",
        "hero_subtitle": "Serving Palo Alto, CA · C-DET Certified · Same Day Service Available",
        "hero_desc": "Dryer Vent Specialists is a professional dryer vent cleaning company serving Palo Alto homeowners and multi-unit buildings throughout the Peninsula. We specialize in dryer vent cleaning, vent repair, duct replacement, and booster fan installation - C-DET certified, insured, and committed to the highest standards of service and safety.",
        "neighborhoods": [
            "Old Palo Alto & Crescent Park",
            "College Terrace & Evergreen Park",
            "Barron Park & Gunn-Arastradero",
            "Midtown & Southgate",
            "Downtown & University South",
            "Charleston Meadows & Fairmeadow"
        ],
        "nbhd_intro": "We provide prompt, expert service to all areas of Palo Alto, including:",
        "why_essential_intro": "Proper vent maintenance is a critical safety and financial investment for Palo Alto Peninsula residents.",
        "meta_desc": "Professional dryer vent cleaning in Palo Alto, CA. CDET-certified, veteran-owned. Serving all Palo Alto neighborhoods. Call (650) 484-4418 for same-day service.",
        "og_desc": "CDET-certified dryer vent cleaning in Palo Alto. Serving all Palo Alto neighborhoods - same-day service available.",
        "schema_desc": "Professional dryer vent cleaning in Palo Alto, CA, serving Old Palo Alto, Crescent Park, College Terrace, and all neighborhoods. CDET-certified, family-owned & veteran-operated. Reduce fire risk and improve dryer efficiency with same-day service.",
        "services": {
            "cleaning": "Palo Alto's diverse housing stock includes Eichler homes from the 1950s-60s in Fairmeadow and Greenmeadow, Craftsman bungalows in Old Palo Alto, and modern construction near Stanford. Many of these homes have vent systems running through walls and attic spaces that collect lint over decades. Our cleaning covers the dryer, hose, and full vent run with rotary brush and HEPA-filtered vacuum.",
            "repair": "Many Palo Alto homes - especially Eichlers with post-and-beam construction and slab foundations - have vent ducts routed through attic spaces or exterior walls where sections can disconnect or deteriorate over time. We replace damaged duct with fire-rated, UL-listed rigid metal that meets Santa Clara County building code.",
            "dryerjack": "Palo Alto's tree-lined neighborhoods face unique exterior vent challenges with varying rooflines and proximity to mature landscaping. We install DryerJack termination caps that seal tightly against debris and bird intrusion while maximizing exhaust airflow.",
            "magvent": "MagVent magnetic coupling is ideal for Palo Alto homes where the dryer sits in a hallway closet or compact laundry space common in Eichler and mid-century floor plans. The magnetic connection eliminates crushed hoses and improves airflow without requiring extra clearance.",
            "commercial": "Palo Alto's multi-unit properties, student housing near Stanford, and townhome communities require commercial-grade vent cleaning. We serve condo associations, apartment complexes, and property managers with bulk pricing, scheduled maintenance, and compliance documentation."
        },
        "faqs": [
            {
                "q": "How often should Palo Alto homeowners get their dryer vents cleaned?",
                "a": "The National Fire Protection Association (NFPA) recommends professional dryer vent cleaning at least once per year. In Palo Alto, many homes in neighborhoods like Old Palo Alto, College Terrace, and Barron Park were built in the mid-20th century with dryer vent systems routed through attic spaces, walls, or up to roof-level exits. These older configurations collect lint faster than modern short-run setups. Households with 4 or more occupants, shedding pets, or vent runs over 25 feet should clean every 6 months."
            },
            {
                "q": "How much does dryer vent cleaning cost in Palo Alto, CA?",
                "a": "Standard dryer vent cleaning in Palo Alto ranges from $149 to $249 for a single residential vent. Dryer Vent Specialists uses flat-rate pricing - the quoted price is the price you pay, with no hidden fees. Cost factors include vent length, number of bends, whether the vent terminates at the roof or sidewall, and whether the flexible transition hose needs replacement with a UL 2158A-compliant duct. Call (650) 484-4418 for an exact quote."
            },
            {
                "q": "What are the warning signs of a clogged dryer vent?",
                "a": "Common signs of a clogged dryer vent include: clothes requiring two or more cycles to dry, the dryer exterior feeling hot to the touch, a burning or musty odor during operation, excessive lint accumulating around the lint trap or on clothing, and the outside vent flap remaining closed while the dryer runs. The U.S. Fire Administration reports that lint buildup is the leading cause of approximately 2,900 home dryer fires per year. If you notice any of these symptoms, schedule a professional cleaning immediately."
            },
            {
                "q": "Does Dryer Vent Specialists clean dryer vents in Palo Alto condos and townhomes?",
                "a": "Yes. Dryer Vent Specialists serves single-family homes, condominiums, townhomes, and apartment buildings throughout Palo Alto. Multi-unit properties - including complexes near Stanford University and along El Camino Real - often have shared or extended vent systems that require commercial-grade equipment. Volume pricing is available for HOAs and property managers with 4 or more units."
            },
            {
                "q": "Can a dirty dryer vent increase my PG&E bill?",
                "a": "Yes. According to the U.S. Department of Energy, a clogged dryer vent can increase energy consumption by 30% or more per drying cycle by restricting airflow and forcing the dryer to run longer. For an average Palo Alto household running 4 to 5 loads per week, that can add $15 to $25 per month to your PG&E bill. Annual professional cleaning typically pays for itself in energy savings within a few months."
            },
            {
                "q": "Is same-day dryer vent cleaning available in Palo Alto?",
                "a": "Yes. Dryer Vent Specialists offers same-day and next-day dryer vent cleaning in Palo Alto, Monday through Saturday, 8:00 AM to 6:00 PM. Palo Alto is a short drive from our San Mateo headquarters. Most standard residential cleanings take 45 to 60 minutes. Book online at dvspecialists.com/book or call (650) 484-4418."
            }
        ],
        "warning_signs": {
            "intro": "If you notice any of these symptoms, your vent is likely partially or fully clogged and should be professionally cleaned as soon as possible. Palo Alto homes - especially Eichlers in Greenmeadow and Fairmeadow and older homes in College Terrace - often have vent systems running through attic spaces and walls that accumulate lint over time.",
            "cards": [
                {"detail": "In Palo Alto's mid-century Eichler homes with attic-routed vents, restricted airflow means moisture can't escape - your dryer runs two or three cycles per load."},
                {"detail": "Palo Alto homeowners: if the top or sides of your dryer feel excessively hot during operation, heat is building up inside due to restricted exhaust airflow."},
                {"detail": "This is a serious fire hazard - the U.S. Fire Administration links overheated lint to approximately 2,900 home fires per year. Stop using the dryer and call immediately."},
                {"detail": "In Palo Alto's older homes, lint bypasses the trap and accumulates in ductwork routed through attic spaces - this is one of the most overlooked fire risks."},
                {"detail": "A clogged vent pushes hot, moist air back into your laundry room. In Palo Alto homes with interior laundry closets, this can also promote mold growth."},
                {"detail": "Check the exterior vent flap on your Palo Alto home - if lint or debris is visible around the opening or the flap doesn't swing open during operation, the vent is restricted."}
            ]
        },
        "condo_faq_detail": "including complexes near Stanford University and along El Camino Real"
    },
    "mountain-view": {
        "name": "Mountain View",
        "zip": "94040",
        "lat": "37.3861",
        "lng": "-122.0839",
        "wiki": "https://en.wikipedia.org/wiki/Mountain_View,_California",
        "hero_img": "images/san-mateo-downtown.jpg",
        "hero_img_alt": "Mountain View, CA",
        "hero_img_tag": "images/san-mateo-downtown.jpg",
        "safety_banner": "DRYER FIRES CAUSE OVER 15,000 HOUSE FIRES EACH YEAR - PROTECT YOUR MOUNTAIN VIEW HOME TODAY",
        "hero_subtitle": "Serving Mountain View, CA · C-DET Certified · Same Day Service Available",
        "hero_desc": "Dryer Vent Specialists is a professional dryer vent cleaning company serving Mountain View homeowners and multi-unit buildings throughout the Peninsula. We specialize in dryer vent cleaning, vent repair, duct replacement, and booster fan installation - C-DET certified, insured, and committed to the highest standards of service and safety.",
        "neighborhoods": [
            "Old Mountain View & Downtown",
            "Cuesta Park & Waverly Park",
            "Rex Manor & Monta Loma",
            "Sylvan Park & Blossom Valley",
            "North Whisman & Shoreline West",
            "Gemello & Jackson Park"
        ],
        "nbhd_intro": "We provide prompt, expert service to all areas of Mountain View, including:",
        "why_essential_intro": "Proper vent maintenance is a critical safety and financial investment for Mountain View residents.",
        "meta_desc": "Professional dryer vent cleaning in Mountain View, CA. CDET-certified, veteran-owned. Serving all Mountain View neighborhoods. Call (650) 484-4418 for same-day service.",
        "og_desc": "CDET-certified dryer vent cleaning in Mountain View. Serving all Mountain View neighborhoods - same-day service available.",
        "schema_desc": "Professional dryer vent cleaning in Mountain View, CA, serving Old Mountain View, Cuesta Park, Rex Manor, and all neighborhoods. CDET-certified, family-owned & veteran-operated. Reduce fire risk and improve dryer efficiency with same-day service.",
        "services": {
            "cleaning": "Mountain View's housing includes 1950s-60s ranch homes in Rex Manor and Monta Loma, newer townhomes near downtown, and condos along El Camino Real. Many older homes have vent systems running through walls and crawl spaces that collect lint over decades. Our cleaning covers the dryer, hose, and full vent run with rotary brush and HEPA-filtered vacuum.",
            "repair": "Many Mountain View homes - especially ranch-style properties in Waverly Park and Cuesta Park - have vent ducts routed through crawl spaces and exterior walls where sections can disconnect or deteriorate over time. We replace damaged duct with fire-rated, UL-listed rigid metal that meets Santa Clara County building code.",
            "dryerjack": "Mountain View's varied rooflines and mature tree canopy create unique exterior vent challenges with debris accumulation and pest entry. We install DryerJack termination caps that seal tightly against wind and bird intrusion while maximizing exhaust airflow.",
            "magvent": "MagVent magnetic coupling is ideal for Mountain View homes where the dryer sits in a compact laundry closet or garage alcove common in mid-century ranch floor plans. The magnetic connection eliminates crushed hoses and improves airflow without requiring extra clearance.",
            "commercial": "Mountain View's growing number of apartment complexes, townhome communities near downtown, and multi-unit properties along El Camino Real require commercial-grade vent cleaning. We serve condo associations, apartment complexes, and property managers with bulk pricing, scheduled maintenance, and compliance documentation."
        },
        "faqs": [
            {
                "q": "How often should Mountain View homeowners get their dryer vents cleaned?",
                "a": "The National Fire Protection Association (NFPA) recommends professional dryer vent cleaning at least once per year. In Mountain View, many homes in neighborhoods like Rex Manor, Monta Loma, and Cuesta Park were built in the 1950s and 1960s with vent systems routed through walls, crawl spaces, or up to roof-level exits. These older configurations collect lint faster than modern short-run setups. Households with 4 or more occupants, shedding pets, or vent runs over 25 feet should clean every 6 months."
            },
            {
                "q": "How much does dryer vent cleaning cost in Mountain View, CA?",
                "a": "Standard dryer vent cleaning in Mountain View ranges from $149 to $249 for a single residential vent. Dryer Vent Specialists uses flat-rate pricing - the quoted price is the price you pay, with no hidden fees. Cost factors include vent length, number of bends, whether the vent terminates at the roof or sidewall, and whether the flexible transition hose needs replacement with a UL 2158A-compliant duct. Call (650) 484-4418 for an exact quote."
            },
            {
                "q": "What are the warning signs of a clogged dryer vent?",
                "a": "Common signs of a clogged dryer vent include: clothes requiring two or more cycles to dry, the dryer exterior feeling hot to the touch, a burning or musty odor during operation, excessive lint accumulating around the lint trap or on clothing, and the outside vent flap remaining closed while the dryer runs. The U.S. Fire Administration reports that lint buildup is the leading cause of approximately 2,900 home dryer fires per year. If you notice any of these symptoms, schedule a professional cleaning immediately."
            },
            {
                "q": "Does Dryer Vent Specialists clean dryer vents in Mountain View condos and townhomes?",
                "a": "Yes. Dryer Vent Specialists serves single-family homes, condominiums, townhomes, and apartment buildings throughout Mountain View. Multi-unit properties - including complexes near downtown and along El Camino Real - often have shared or extended vent systems that require commercial-grade equipment. Volume pricing is available for HOAs and property managers with 4 or more units."
            },
            {
                "q": "Can a dirty dryer vent increase my PG&E bill?",
                "a": "Yes. According to the U.S. Department of Energy, a clogged dryer vent can increase energy consumption by 30% or more per drying cycle by restricting airflow and forcing the dryer to run longer. For an average Mountain View household running 4 to 5 loads per week, that can add $15 to $25 per month to your PG&E bill. Annual professional cleaning typically pays for itself in energy savings within a few months."
            },
            {
                "q": "Is same-day dryer vent cleaning available in Mountain View?",
                "a": "Yes. Dryer Vent Specialists offers same-day and next-day dryer vent cleaning in Mountain View, Monday through Saturday, 8:00 AM to 6:00 PM. Mountain View is a short drive from our San Mateo headquarters. Most standard residential cleanings take 45 to 60 minutes. Book online at dvspecialists.com/book or call (650) 484-4418."
            }
        ],
        "warning_signs": {
            "intro": "If you notice any of these symptoms, your vent is likely partially or fully clogged and should be professionally cleaned as soon as possible. Mountain View homes built in the 1950s and 1960s - particularly in Rex Manor, Monta Loma, and Cuesta Park - often have vent systems running through walls and crawl spaces that accumulate lint over time.",
            "cards": [
                {"detail": "In Mountain View's mid-century ranch homes with crawl space or wall-routed vents, restricted airflow means moisture can't escape - your dryer runs two or three cycles per load."},
                {"detail": "Mountain View homeowners: if the top or sides of your dryer feel excessively hot during operation, heat is building up inside due to restricted exhaust airflow."},
                {"detail": "This is a serious fire hazard - the U.S. Fire Administration links overheated lint to approximately 2,900 home fires per year. Stop using the dryer and call immediately."},
                {"detail": "In Mountain View's older homes, lint bypasses the trap and accumulates in ductwork routed through crawl spaces - this is one of the most overlooked fire risks."},
                {"detail": "A clogged vent pushes hot, moist air back into your laundry room. In Mountain View homes with garage-adjacent laundry setups, this can also promote mold growth."},
                {"detail": "Check the exterior vent flap on your Mountain View home - if lint or debris is visible around the opening or the flap doesn't swing open during operation, the vent is restricted."}
            ]
        }
    },
    "sunnyvale": {
        "name": "Sunnyvale",
        "zip": "94086",
        "lat": "37.3688",
        "lng": "-122.0363",
        "wiki": "https://en.wikipedia.org/wiki/Sunnyvale,_California",
        "hero_img": "images/san-mateo-downtown.jpg",
        "hero_img_alt": "Sunnyvale, CA",
        "hero_img_tag": "images/san-mateo-downtown.jpg",
        "safety_banner": "DRYER FIRES CAUSE OVER 15,000 HOUSE FIRES EACH YEAR - PROTECT YOUR SUNNYVALE HOME TODAY",
        "hero_subtitle": "Serving Sunnyvale, CA · C-DET Certified · Same Day Service Available",
        "hero_desc": "Dryer Vent Specialists is a professional dryer vent cleaning company serving Sunnyvale homeowners and multi-unit buildings throughout the South Bay. We specialize in dryer vent cleaning, vent repair, duct replacement, and booster fan installation - C-DET certified, insured, and committed to the highest standards of service and safety.",
        "neighborhoods": [
            "Downtown Sunnyvale & Heritage District",
            "Cherry Chase & Lakewood Village",
            "Birdland & Ponderosa Park",
            "Raynor Park & Braly Park",
            "Ortega Park & Sunnyvale West",
            "East Sunnyvale & Fair Oaks"
        ],
        "nbhd_intro": "We provide prompt, expert service to all areas of Sunnyvale, including:",
        "why_essential_intro": "Proper vent maintenance is a critical safety and financial investment for Sunnyvale residents.",
        "meta_desc": "Professional dryer vent cleaning in Sunnyvale, CA. CDET-certified, veteran-owned. Serving all Sunnyvale neighborhoods. Call (650) 484-4418 for same-day service.",
        "og_desc": "CDET-certified dryer vent cleaning in Sunnyvale. Serving all Sunnyvale neighborhoods - same-day service available.",
        "schema_desc": "Professional dryer vent cleaning in Sunnyvale, CA, serving Cherry Chase, Lakewood Village, Birdland, and all neighborhoods. CDET-certified, family-owned & veteran-operated. Reduce fire risk and improve dryer efficiency with same-day service.",
        "services": {
            "cleaning": "Sunnyvale's housing includes postwar ranch homes in Cherry Chase and Lakewood Village, Eichler developments in Ponderosa Park, and newer townhomes near downtown. Many older homes have vent systems running through walls and attic spaces that collect lint over decades. Our cleaning covers the dryer, hose, and full vent run with rotary brush and HEPA-filtered vacuum.",
            "repair": "Many Sunnyvale homes - especially ranch-style properties in Birdland and Cherry Chase - have vent ducts routed through attic spaces and crawl spaces where sections can disconnect or deteriorate over time. We replace damaged duct with fire-rated, UL-listed rigid metal that meets Santa Clara County building code.",
            "dryerjack": "Sunnyvale's single-story ranch homes and Eichlers have exterior vents vulnerable to debris accumulation and pest intrusion. We install DryerJack termination caps that seal tightly against wind and wildlife while maximizing exhaust airflow.",
            "magvent": "MagVent magnetic coupling is ideal for Sunnyvale homes where the dryer sits in a garage alcove or compact laundry closet common in 1950s-60s ranch floor plans. The magnetic connection eliminates crushed hoses and improves airflow without requiring extra clearance.",
            "commercial": "Sunnyvale's large apartment complexes, townhome communities, and multi-unit properties along El Camino Real and Mathilda Avenue require commercial-grade vent cleaning. We serve condo associations, apartment complexes, and property managers with bulk pricing, scheduled maintenance, and compliance documentation."
        },
        "faqs": [
            {
                "q": "How often should Sunnyvale homeowners get their dryer vents cleaned?",
                "a": "The National Fire Protection Association (NFPA) recommends professional dryer vent cleaning at least once per year. In Sunnyvale, many homes in neighborhoods like Cherry Chase, Lakewood Village, and Birdland were built in the 1950s and 1960s with vent systems routed through walls, attic spaces, or up to roof-level exits. These older configurations collect lint faster than modern short-run setups. Households with 4 or more occupants, shedding pets, or vent runs over 25 feet should clean every 6 months."
            },
            {
                "q": "How much does dryer vent cleaning cost in Sunnyvale, CA?",
                "a": "Standard dryer vent cleaning in Sunnyvale ranges from $149 to $249 for a single residential vent. Dryer Vent Specialists uses flat-rate pricing - the quoted price is the price you pay, with no hidden fees. Cost factors include vent length, number of bends, whether the vent terminates at the roof or sidewall, and whether the flexible transition hose needs replacement with a UL 2158A-compliant duct. Call (650) 484-4418 for an exact quote."
            },
            {
                "q": "What are the warning signs of a clogged dryer vent?",
                "a": "Common signs of a clogged dryer vent include: clothes requiring two or more cycles to dry, the dryer exterior feeling hot to the touch, a burning or musty odor during operation, excessive lint accumulating around the lint trap or on clothing, and the outside vent flap remaining closed while the dryer runs. The U.S. Fire Administration reports that lint buildup is the leading cause of approximately 2,900 home dryer fires per year. If you notice any of these symptoms, schedule a professional cleaning immediately."
            },
            {
                "q": "Does Dryer Vent Specialists clean dryer vents in Sunnyvale condos and townhomes?",
                "a": "Yes. Dryer Vent Specialists serves single-family homes, condominiums, townhomes, and apartment buildings throughout Sunnyvale. Multi-unit properties - including complexes along El Camino Real and Mathilda Avenue - often have shared or extended vent systems that require commercial-grade equipment. Volume pricing is available for HOAs and property managers with 4 or more units."
            },
            {
                "q": "Can a dirty dryer vent increase my PG&E bill?",
                "a": "Yes. According to the U.S. Department of Energy, a clogged dryer vent can increase energy consumption by 30% or more per drying cycle by restricting airflow and forcing the dryer to run longer. For an average Sunnyvale household running 4 to 5 loads per week, that can add $15 to $25 per month to your PG&E bill. Annual professional cleaning typically pays for itself in energy savings within a few months."
            },
            {
                "q": "Is same-day dryer vent cleaning available in Sunnyvale?",
                "a": "Yes. Dryer Vent Specialists offers same-day and next-day dryer vent cleaning in Sunnyvale, Monday through Saturday, 8:00 AM to 6:00 PM. Sunnyvale is easily accessible from our San Mateo headquarters. Most standard residential cleanings take 45 to 60 minutes. Book online at dvspecialists.com/book or call (650) 484-4418."
            }
        ],
        "warning_signs": {
            "intro": "If you notice any of these symptoms, your vent is likely partially or fully clogged and should be professionally cleaned as soon as possible. Sunnyvale homes built in the 1950s and 1960s - particularly in Cherry Chase, Lakewood Village, and Birdland - often have vent systems running through walls and attic spaces that accumulate lint over time.",
            "cards": [
                {"detail": "In Sunnyvale's postwar ranch homes with attic or wall-routed vents, restricted airflow means moisture can't escape - your dryer runs two or three cycles per load."},
                {"detail": "Sunnyvale homeowners: if the top or sides of your dryer feel excessively hot during operation, heat is building up inside due to restricted exhaust airflow."},
                {"detail": "This is a serious fire hazard - the U.S. Fire Administration links overheated lint to approximately 2,900 home fires per year. Stop using the dryer and call immediately."},
                {"detail": "In Sunnyvale's older homes, lint bypasses the trap and accumulates in ductwork routed through attic spaces and crawl spaces - this is one of the most overlooked fire risks."},
                {"detail": "A clogged vent pushes hot, moist air back into your laundry room. In Sunnyvale homes with garage laundry setups, this can also promote mold growth in adjacent walls."},
                {"detail": "Check the exterior vent flap on your Sunnyvale home - if lint or debris is visible around the opening or the flap doesn't swing open during operation, the vent is restricted."}
            ]
        }
    },
    "santa-clara": {
        "name": "Santa Clara",
        "zip": "95050",
        "lat": "37.3541",
        "lng": "-121.9552",
        "wiki": "https://en.wikipedia.org/wiki/Santa_Clara,_California",
        "hero_img": "images/san-mateo-downtown.jpg",
        "hero_img_alt": "Santa Clara, CA",
        "hero_img_tag": "images/san-mateo-downtown.jpg",
        "safety_banner": "DRYER FIRES CAUSE OVER 15,000 HOUSE FIRES EACH YEAR - PROTECT YOUR SANTA CLARA HOME TODAY",
        "hero_subtitle": "Serving Santa Clara, CA · C-DET Certified · Same Day Service Available",
        "hero_desc": "Dryer Vent Specialists is a professional dryer vent cleaning company serving Santa Clara homeowners and multi-unit buildings throughout the South Bay. We specialize in dryer vent cleaning, vent repair, duct replacement, and booster fan installation - C-DET certified, insured, and committed to the highest standards of service and safety.",
        "neighborhoods": [
            "Old Quad & University Neighborhood",
            "Central Park & Cabrillo Park",
            "Northside & Agnew",
            "Rivermark & Montague",
            "Santa Clara Mission District",
            "Warburton & Washington"
        ],
        "nbhd_intro": "We provide prompt, expert service to all areas of Santa Clara, including:",
        "why_essential_intro": "Proper vent maintenance is a critical safety and financial investment for Santa Clara residents.",
        "meta_desc": "Professional dryer vent cleaning in Santa Clara, CA. CDET-certified, veteran-owned. Serving all Santa Clara neighborhoods. Call (650) 484-4418 for same-day service.",
        "og_desc": "CDET-certified dryer vent cleaning in Santa Clara. Serving all Santa Clara neighborhoods - same-day service available.",
        "schema_desc": "Professional dryer vent cleaning in Santa Clara, CA, serving Old Quad, Central Park, Northside, and all neighborhoods. CDET-certified, family-owned & veteran-operated. Reduce fire risk and improve dryer efficiency with same-day service.",
        "services": {
            "cleaning": "Santa Clara's housing ranges from postwar ranch homes in the Old Quad and Central Park neighborhoods to newer developments near Rivermark and Montague. Many older homes have vent systems running through walls and crawl spaces that collect lint over decades. Our cleaning covers the dryer, hose, and full vent run with rotary brush and HEPA-filtered vacuum.",
            "repair": "Many Santa Clara homes - especially mid-century properties near the Old Quad and Cabrillo Park - have vent ducts routed through crawl spaces and attic spaces where sections can disconnect or deteriorate over time. We replace damaged duct with fire-rated, UL-listed rigid metal that meets Santa Clara County building code.",
            "dryerjack": "Santa Clara's flat-roofed ranch homes and varied construction styles create exterior vent challenges with pest entry and debris accumulation. We install DryerJack termination caps that seal tightly against wind and bird intrusion while maximizing exhaust airflow.",
            "magvent": "MagVent magnetic coupling is ideal for Santa Clara homes where the dryer sits in a garage alcove or compact laundry area common in postwar floor plans. The magnetic connection eliminates crushed hoses and improves airflow without requiring extra clearance.",
            "commercial": "Santa Clara's large apartment complexes near Santa Clara University, townhome communities, and multi-unit properties along El Camino Real require commercial-grade vent cleaning. We serve condo associations, apartment complexes, and property managers with bulk pricing, scheduled maintenance, and compliance documentation."
        },
        "faqs": [
            {
                "q": "How often should Santa Clara homeowners get their dryer vents cleaned?",
                "a": "The National Fire Protection Association (NFPA) recommends professional dryer vent cleaning at least once per year. In Santa Clara, many homes in neighborhoods like Old Quad, Central Park, and Cabrillo Park were built in the 1950s and 1960s with vent systems routed through walls, crawl spaces, or up to roof-level exits. These older configurations collect lint faster than modern short-run setups. Households with 4 or more occupants, shedding pets, or vent runs over 25 feet should clean every 6 months."
            },
            {
                "q": "How much does dryer vent cleaning cost in Santa Clara, CA?",
                "a": "Standard dryer vent cleaning in Santa Clara ranges from $149 to $249 for a single residential vent. Dryer Vent Specialists uses flat-rate pricing - the quoted price is the price you pay, with no hidden fees. Cost factors include vent length, number of bends, whether the vent terminates at the roof or sidewall, and whether the flexible transition hose needs replacement with a UL 2158A-compliant duct. Call (650) 484-4418 for an exact quote."
            },
            {
                "q": "What are the warning signs of a clogged dryer vent?",
                "a": "Common signs of a clogged dryer vent include: clothes requiring two or more cycles to dry, the dryer exterior feeling hot to the touch, a burning or musty odor during operation, excessive lint accumulating around the lint trap or on clothing, and the outside vent flap remaining closed while the dryer runs. The U.S. Fire Administration reports that lint buildup is the leading cause of approximately 2,900 home dryer fires per year. If you notice any of these symptoms, schedule a professional cleaning immediately."
            },
            {
                "q": "Does Dryer Vent Specialists clean dryer vents in Santa Clara condos and townhomes?",
                "a": "Yes. Dryer Vent Specialists serves single-family homes, condominiums, townhomes, and apartment buildings throughout Santa Clara. Multi-unit properties - including complexes near Santa Clara University and along El Camino Real - often have shared or extended vent systems that require commercial-grade equipment. Volume pricing is available for HOAs and property managers with 4 or more units."
            },
            {
                "q": "Can a dirty dryer vent increase my PG&E bill?",
                "a": "Yes. According to the U.S. Department of Energy, a clogged dryer vent can increase energy consumption by 30% or more per drying cycle by restricting airflow and forcing the dryer to run longer. For an average Santa Clara household running 4 to 5 loads per week, that can add $15 to $25 per month to your PG&E bill. Annual professional cleaning typically pays for itself in energy savings within a few months."
            },
            {
                "q": "Is same-day dryer vent cleaning available in Santa Clara?",
                "a": "Yes. Dryer Vent Specialists offers same-day and next-day dryer vent cleaning in Santa Clara, Monday through Saturday, 8:00 AM to 6:00 PM. Santa Clara is easily accessible from our San Mateo headquarters. Most standard residential cleanings take 45 to 60 minutes. Book online at dvspecialists.com/book or call (650) 484-4418."
            }
        ],
        "warning_signs": {
            "intro": "If you notice any of these symptoms, your vent is likely partially or fully clogged and should be professionally cleaned as soon as possible. Santa Clara homes built in the 1950s and 1960s - particularly in the Old Quad, Central Park, and Cabrillo Park neighborhoods - often have vent systems running through walls and crawl spaces that accumulate lint over time.",
            "cards": [
                {"detail": "In Santa Clara's postwar ranch homes with crawl space or wall-routed vents, restricted airflow means moisture can't escape - your dryer runs two or three cycles per load."},
                {"detail": "Santa Clara homeowners: if the top or sides of your dryer feel excessively hot during operation, heat is building up inside due to restricted exhaust airflow."},
                {"detail": "This is a serious fire hazard - the U.S. Fire Administration links overheated lint to approximately 2,900 home fires per year. Stop using the dryer and call immediately."},
                {"detail": "In Santa Clara's older homes, lint bypasses the trap and accumulates in ductwork routed through crawl spaces - this is one of the most overlooked fire risks."},
                {"detail": "A clogged vent pushes hot, moist air back into your laundry room. In Santa Clara homes with garage-adjacent laundry setups, this can also promote mold growth."},
                {"detail": "Check the exterior vent flap on your Santa Clara home - if lint or debris is visible around the opening or the flap doesn't swing open during operation, the vent is restricted."}
            ]
        }
    },
    "san-jose": {
        "name": "San Jose",
        "zip": "95112",
        "lat": "37.3382",
        "lng": "-121.8863",
        "wiki": "https://en.wikipedia.org/wiki/San_Jose,_California",
        "hero_img": "images/san-mateo-downtown.jpg",
        "hero_img_alt": "San Jose, CA",
        "hero_img_tag": "images/san-mateo-downtown.jpg",
        "safety_banner": "DRYER FIRES CAUSE OVER 15,000 HOUSE FIRES EACH YEAR - PROTECT YOUR SAN JOSE HOME TODAY",
        "hero_subtitle": "Serving San Jose, CA · C-DET Certified · Same Day Service Available",
        "hero_desc": "Dryer Vent Specialists is a professional dryer vent cleaning company serving San Jose homeowners and multi-unit buildings throughout the South Bay. We specialize in dryer vent cleaning, vent repair, duct replacement, and booster fan installation - C-DET certified, insured, and committed to the highest standards of service and safety.",
        "neighborhoods": [
            "Willow Glen & Rose Garden",
            "Almaden Valley & Cambrian Park",
            "Japantown & Hensley",
            "Evergreen & Silver Creek",
            "Berryessa & North San Jose",
            "West San Jose & Campbell Border"
        ],
        "nbhd_intro": "We provide prompt, expert service to all areas of San Jose, including:",
        "why_essential_intro": "Proper vent maintenance is a critical safety and financial investment for San Jose residents.",
        "meta_desc": "Professional dryer vent cleaning in San Jose, CA. CDET-certified, veteran-owned. Serving Willow Glen, Almaden, and all San Jose neighborhoods. Call (650) 484-4418.",
        "og_desc": "CDET-certified dryer vent cleaning in San Jose. Serving Willow Glen, Almaden Valley, and all neighborhoods - same-day service available.",
        "schema_desc": "Professional dryer vent cleaning in San Jose, CA, serving Willow Glen, Almaden Valley, Rose Garden, Evergreen, and all neighborhoods. CDET-certified, family-owned & veteran-operated. Reduce fire risk and improve dryer efficiency with same-day service.",
        "services": {
            "cleaning": "San Jose's vast and varied housing stock includes Craftsman bungalows in Willow Glen, mid-century ranches in Cambrian Park, hillside homes in Almaden Valley, and newer construction in Evergreen and Berryessa. Many older homes have vent systems running through walls, crawl spaces, and attic spaces that collect lint over decades. Our cleaning covers the dryer, hose, and full vent run with rotary brush and HEPA-filtered vacuum.",
            "repair": "Many San Jose homes - especially older properties in Willow Glen and the Rose Garden district - have vent ducts routed through crawl spaces and foundation walls where sections can disconnect or deteriorate over time. We replace damaged duct with fire-rated, UL-listed rigid metal that meets Santa Clara County building code.",
            "dryerjack": "San Jose's diverse architecture from single-story ranches to hillside homes in Almaden creates varied exterior vent challenges. We install DryerJack termination caps that seal tightly against pests and debris while maximizing exhaust airflow.",
            "magvent": "MagVent magnetic coupling is ideal for San Jose homes where the dryer sits in a compact laundry closet or tight garage alcove common in Willow Glen bungalows and Cambrian Park ranches. The magnetic connection eliminates crushed hoses and improves airflow without requiring extra clearance.",
            "commercial": "San Jose's large apartment complexes, townhome developments, and multi-unit properties throughout downtown, Berryessa, and North San Jose require commercial-grade vent cleaning. We serve condo associations, apartment complexes, and property managers with bulk pricing, scheduled maintenance, and compliance documentation."
        },
        "faqs": [
            {
                "q": "How often should San Jose homeowners get their dryer vents cleaned?",
                "a": "The National Fire Protection Association (NFPA) recommends professional dryer vent cleaning at least once per year. In San Jose, many homes in neighborhoods like Willow Glen, Rose Garden, and Cambrian Park were built in the early to mid-20th century with vent systems routed through walls, crawl spaces, or up to roof-level exits. These older configurations collect lint faster than modern short-run setups. Households with 4 or more occupants, shedding pets, or vent runs over 25 feet should clean every 6 months."
            },
            {
                "q": "How much does dryer vent cleaning cost in San Jose, CA?",
                "a": "Standard dryer vent cleaning in San Jose ranges from $149 to $249 for a single residential vent. Dryer Vent Specialists uses flat-rate pricing - the quoted price is the price you pay, with no hidden fees. Cost factors include vent length, number of bends, whether the vent terminates at the roof or sidewall, and whether the flexible transition hose needs replacement with a UL 2158A-compliant duct. Call (650) 484-4418 for an exact quote."
            },
            {
                "q": "What are the warning signs of a clogged dryer vent?",
                "a": "Common signs of a clogged dryer vent include: clothes requiring two or more cycles to dry, the dryer exterior feeling hot to the touch, a burning or musty odor during operation, excessive lint accumulating around the lint trap or on clothing, and the outside vent flap remaining closed while the dryer runs. The U.S. Fire Administration reports that lint buildup is the leading cause of approximately 2,900 home dryer fires per year. If you notice any of these symptoms, schedule a professional cleaning immediately."
            },
            {
                "q": "Does Dryer Vent Specialists clean dryer vents in San Jose condos and townhomes?",
                "a": "Yes. Dryer Vent Specialists serves single-family homes, condominiums, townhomes, and apartment buildings throughout San Jose. Multi-unit properties - including complexes in downtown, Berryessa, and North San Jose - often have shared or extended vent systems that require commercial-grade equipment. Volume pricing is available for HOAs and property managers with 4 or more units."
            },
            {
                "q": "Can a dirty dryer vent increase my PG&E bill?",
                "a": "Yes. According to the U.S. Department of Energy, a clogged dryer vent can increase energy consumption by 30% or more per drying cycle by restricting airflow and forcing the dryer to run longer. For an average San Jose household running 4 to 5 loads per week, that can add $15 to $25 per month to your PG&E bill. Annual professional cleaning typically pays for itself in energy savings within a few months."
            },
            {
                "q": "Is same-day dryer vent cleaning available in San Jose?",
                "a": "Yes. Dryer Vent Specialists offers same-day and next-day dryer vent cleaning in San Jose, Monday through Saturday, 8:00 AM to 6:00 PM. San Jose is easily accessible from our San Mateo headquarters via Highway 101 or 280. Most standard residential cleanings take 45 to 60 minutes. Book online at dvspecialists.com/book or call (650) 484-4418."
            }
        ],
        "warning_signs": {
            "intro": "If you notice any of these symptoms, your vent is likely partially or fully clogged and should be professionally cleaned as soon as possible. San Jose homes - especially older properties in Willow Glen, the Rose Garden, and Cambrian Park - often have vent systems running through walls and crawl spaces that accumulate lint over time.",
            "cards": [
                {"detail": "In San Jose's older homes with crawl space or wall-routed vents, restricted airflow means moisture can't escape - your dryer runs two or three cycles per load."},
                {"detail": "San Jose homeowners: if the top or sides of your dryer feel excessively hot during operation, heat is building up inside due to restricted exhaust airflow."},
                {"detail": "This is a serious fire hazard - the U.S. Fire Administration links overheated lint to approximately 2,900 home fires per year. Stop using the dryer and call immediately."},
                {"detail": "In San Jose's older homes, lint bypasses the trap and accumulates in ductwork routed through crawl spaces and walls - this is one of the most overlooked fire risks."},
                {"detail": "A clogged vent pushes hot, moist air back into your laundry room. In San Jose's warm climate, this excess moisture can promote mold growth in adjacent walls and cabinetry."},
                {"detail": "Check the exterior vent flap on your San Jose home - if lint or debris is visible around the opening or the flap doesn't swing open during operation, the vent is restricted."}
            ]
        }
    }
}

# All cities for nav (existing + new)
ALL_CITIES_NAV = [
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

WARNING_SIGN_HEADERS = [
    ("&#128168;", "Clothes need multiple cycles to dry"),
    ("&#9888;&#65039;", "Dryer is very hot to the touch"),
    ("&#128293;", "Burning smell when dryer is running"),
    ("&#129656;", "Lint trap catches less lint than usual"),
    ("&#128167;", "Laundry room feels humid or warm"),
    ("&#128065;", "Visible lint around exterior vent"),
]


def build_nav_dropdown(active_slug):
    """Build the nav dropdown menu with all cities."""
    lines = [
        '          <a href="/dryer-vent-cleaning-san-mateo"><span style="color:var(--orange);">📍</span> San Mateo</a>',
        '          <div class="menu-divider"></div>',
    ]
    for slug, name in ALL_CITIES_NAV:
        if slug == active_slug:
            lines.append(f'          <a href="/dryer-vent-cleaning-{slug}" class="active"><span style="color:var(--orange);">📍</span> {name}</a>')
        else:
            lines.append(f'          <a href="/dryer-vent-cleaning-{slug}">{name}</a>')
    return '\n'.join(lines)


def build_mobile_menu(active_slug):
    """Build the mobile menu with all cities."""
    lines = []
    for slug, name in ALL_CITIES_NAV:
        if slug == active_slug:
            lines.append(f'      <a href="/dryer-vent-cleaning-{slug}" class="block py-1 pl-3" style="color:var(--orange);">→ {name}</a>')
        else:
            lines.append(f'      <a href="/dryer-vent-cleaning-{slug}" class="block py-1 pl-3 hover:text-teal-DEFAULT">→ {name}</a>')
    return '\n'.join(lines)


def build_footer_areas(active_slug):
    """Build the footer service areas list."""
    lines = []
    for slug, name in ALL_CITIES_NAV:
        if slug == active_slug:
            lines.append(f'          <li><a href="/dryer-vent-cleaning-{slug}" class="hover:text-white transition-colors duration-200" style="color:var(--teal-light);">{name}</a></li>')
        else:
            lines.append(f'          <li><a href="/dryer-vent-cleaning-{slug}" class="hover:text-white transition-colors duration-200">{name}</a></li>')
    lines.append('          <li><a href="/#service-areas" class="hover:text-white transition-colors duration-200">View All Areas →</a></li>')
    return '\n'.join(lines)


def generate_page(slug, data):
    """Generate a full city page from the Belmont template."""
    name = data['name']
    name_upper = name.upper()

    # Start from template
    page = TEMPLATE

    # Replace all Belmont references
    page = page.replace('Belmont, CA | Dryer Vent Specialists', f'{name}, CA | Dryer Vent Specialists')
    page = page.replace('dryer-vent-cleaning-belmont', f'dryer-vent-cleaning-{slug}')
    page = page.replace('"Belmont, CA"', f'"{name}, CA"')
    page = page.replace('"Belmont"', f'"{name}"')

    # Meta description
    page = page.replace(
        'Professional dryer vent cleaning in Belmont, CA. CDET-certified, veteran-owned. Serving all Belmont neighborhoods. Call (650) 484-4418 for same-day service.',
        data['meta_desc']
    )

    # OG description
    page = page.replace(
        'CDET-certified dryer vent cleaning in Belmont. Serving all Belmont neighborhoods - same-day service available.',
        data['og_desc']
    )
    page = page.replace(
        'CDET-certified dryer vent cleaning in Belmont. Family-owned, veteran-operated. Same-day service.',
        data['og_desc']
    )

    # Schema description
    page = page.replace(
        'Professional dryer vent cleaning in Belmont, CA, serving Belmont Hills, Carlmont, and all neighborhoods. CDET-certified, family-owned & veteran-operated. Reduce fire risk and improve dryer efficiency with same-day service.',
        data['schema_desc']
    )

    # Geo coordinates
    page = page.replace('"latitude": "37.5202", "longitude": "-122.2758"', f'"latitude": "{data["lat"]}", "longitude": "{data["lng"]}"')

    # Wiki link
    page = page.replace('https://en.wikipedia.org/wiki/Belmont,_California', data['wiki'])

    # ZIP code
    page = page.replace('94002', data['zip'])

    # Safety banner
    page = page.replace('PROTECT YOUR BELMONT HOME TODAY', f'PROTECT YOUR {name_upper} HOME TODAY')

    # Hero subtitle
    page = page.replace('Serving Belmont, CA', f'Serving {name}, CA')

    # Hero heading
    page = page.replace('<span style="color:var(--orange);">IN BELMONT</span>', f'<span style="color:var(--orange);">IN {name_upper}</span>')

    # Hero description
    page = page.replace(
        'Dryer Vent Specialists is a professional dryer vent cleaning company serving Belmont homeowners and multi-unit buildings throughout the Peninsula.',
        data['hero_desc'].split('.')[0] + '.'
    )

    # Hero CTA
    page = page.replace('Book Belmont Service', f'Book {name} Service')

    # Hero card image - replace Belmont-specific image
    page = page.replace('images/belmont-ralston-hall.webp', data['hero_img_tag'])
    page = page.replace('Ralston Hall Belmont, CA', data['hero_img_alt'])

    # Hero card location
    page = page.replace(f'📍 {name}, CA 94002', f'📍 {name}, CA {data["zip"]}')
    page = page.replace(f'Serving all Belmont neighborhoods', f'Serving all {name} neighborhoods')

    # Neighborhoods section
    page = page.replace('We Cover All of Belmont', f'We Cover All of {name}')
    page = page.replace('Belmont Neighborhoods We Serve', f'{name} Neighborhoods We Serve')

    # Replace neighborhood pills
    old_nbhd = '''      <span class="nbhd-pill">Belmont Hills & Cipriani</span>
      <span class="nbhd-pill">Sterling Downs & Homeview</span>
      <span class="nbhd-pill">Plateau-Skymont</span>
      <span class="nbhd-pill">Belmont Woods</span>
      <span class="nbhd-pill">Central & Downtown Belmont</span>
      <span class="nbhd-pill">Western Hills</span>'''
    new_nbhd = '\n'.join(f'      <span class="nbhd-pill">{n}</span>' for n in data['neighborhoods'])
    page = page.replace(old_nbhd, new_nbhd)

    # Why Essential section
    page = page.replace('Essential for Belmont Homes', f'Essential for {name} Homes')
    page = page.replace('Belmont Peninsula residents', f'{name} residents')

    # Recent work
    page = page.replace('Recent Jobs in Belmont', f'Recent Jobs in {name}')

    # Services section
    page = page.replace('What We Offer in Belmont', f'What We Offer in {name}')
    page = page.replace(f'Dryer Vent Services for Every {name} Home', f'Dryer Vent Services for Every {name} Home')
    page = page.replace('Dryer Vent Services for Every Belmont Home', f'Dryer Vent Services for Every {name} Home')

    # Replace service descriptions
    page = re.sub(
        r"Belmont homes built during the 1950s.*?HEPA-filtered vacuum\.",
        data['services']['cleaning'],
        page, count=1
    )
    page = re.sub(
        r"Many Belmont homes have vent ducts routed through crawl spaces.*?San Mateo County building code\.",
        data['services']['repair'],
        page, count=1
    )
    page = re.sub(
        r"Belmont's hillside properties face unique.*?maximizing exhaust airflow\.",
        data['services']['dryerjack'],
        page, count=1
    )
    page = re.sub(
        r"MagVent magnetic coupling is ideal for Belmont homes.*?requiring extra clearance\.",
        data['services']['magvent'],
        page, count=1
    )
    page = re.sub(
        r"Belmont's multi-unit properties and townhome.*?compliance documentation\.",
        data['services']['commercial'],
        page, count=1
    )

    # How It Works
    page = page.replace('most Belmont appointments', f'most {name} appointments')
    page = page.replace(f'appointments in Belmont are', f'appointments in {name} are')

    # Warning Signs section
    page = page.replace(
        re.search(r'If you notice any of these symptoms.*?accumulate lint over time\.', page).group(),
        data['warning_signs']['intro']
    )

    # Replace warning sign card details
    belmont_card_details = [
        "In postwar Belmont homes with under-floor or through-wall vent runs, restricted airflow means moisture can't escape - your dryer runs two or three cycles per load.",
        "Belmont homeowners: if the top or sides of your dryer feel excessively hot during operation, heat is building up inside due to restricted exhaust airflow.",
        "This is a serious fire hazard - the U.S. Fire Administration links overheated lint to approximately 2,900 home fires per year. Stop using the dryer and call immediately.",
        "In Belmont's mid-century homes, lint bypasses the trap and accumulates in older ductwork routed through crawl spaces - this is one of the most overlooked fire risks.",
        "A clogged vent pushes hot, moist air back into your laundry room. In Belmont's hillside homes with limited natural ventilation, this can also promote mold growth.",
        "Check the exterior vent flap on your Belmont home - if lint or debris is visible around the opening or the flap doesn't swing open during operation, the vent is restricted."
    ]
    for i, old_detail in enumerate(belmont_card_details):
        page = page.replace(old_detail, data['warning_signs']['cards'][i]['detail'])

    # FAQ section
    page = page.replace('Belmont Dryer Vent Cleaning FAQ', f'{name} Dryer Vent Cleaning FAQ')

    # Replace FAQ Q&As
    faq_section = re.search(r'<div class="space-y-4 fade-in">(.*?)</div>\s*</div>\s*</section>\s*<!-- CTA -->', page, re.DOTALL)
    if faq_section:
        new_faqs = '\n'.join(
            f'      <details class="faq-item"><summary>{faq["q"]} <span class="faq-icon">+</span></summary><div class="faq-body">{faq["a"]}</div></details>'
            for faq in data['faqs']
        )
        page = page.replace(faq_section.group(1).strip(), new_faqs)

    # CTA section
    page = page.replace(f'BOOK YOUR BELMONT<br/>SERVICE TODAY', f'BOOK YOUR {name_upper}<br/>SERVICE TODAY')
    page = page.replace(f'across Belmont and the Bay Area', f'across {name} and the Bay Area')
    page = page.replace(f'📍 Serving Belmont, CA 94002', f'📍 Serving {name}, CA {data["zip"]}')

    # Footer
    page = page.replace(f'serving Belmont &amp; the San Francisco Bay Area', f'serving {name} &amp; the San Francisco Bay Area')

    # PAGE_CITY JS variable
    page = page.replace('const PAGE_CITY = "Belmont"', f'const PAGE_CITY = "{name}"')

    # Update nav dropdown
    old_nav = re.search(r'<div class="nav-dropdown-menu">\s*(.*?)\s*</div>\s*</li>', page, re.DOTALL)
    if old_nav:
        new_nav_content = build_nav_dropdown(slug)
        page = page.replace(old_nav.group(1).strip(), new_nav_content)

    # Update mobile menu
    old_mobile_start = '      <a href="/dryer-vent-cleaning-san-mateo"'
    old_mobile_end = '      <a href="/dryer-vent-cleaning-half-moon-bay" class="block py-1 pl-3 hover:text-teal-DEFAULT">→ Half Moon Bay</a>'
    if old_mobile_start in page:
        mobile_section = re.search(
            r'(      <a href="/dryer-vent-cleaning-san-mateo.*?Half Moon Bay</a>)',
            page, re.DOTALL
        )
        if mobile_section:
            page = page.replace(mobile_section.group(1), build_mobile_menu(slug))

    # Update footer service areas
    footer_areas = re.search(
        r'(          <li><a href="/dryer-vent-cleaning-san-mateo.*?View All Areas →</a></li>)',
        page, re.DOTALL
    )
    if footer_areas:
        page = page.replace(footer_areas.group(1), build_footer_areas(slug))

    # Final remaining "Belmont" references that are generic
    page = page.replace('Belmont', name)

    return page


def main():
    for slug, data in CITIES.items():
        filepath = f'/Users/michaelredman/Documents/GitHub/dvspecialists/dryer-vent-cleaning-{slug}.html'
        content = generate_page(slug, data)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'  CREATED: {filepath}')


if __name__ == '__main__':
    main()
