"""
Mini-Web Map Configuration
===========================

Educational configuration for the mini-web version of District-Maps.
Each layer includes civics education content to help users understand
the structure of the US federal government.
"""

# Map initialization settings
MAP_CONFIG = {
    'center': [39.8283, -98.5795],  # Geographic center of contiguous US
    'zoom_start': 4,
    'tiles': 'OpenStreetMap',
    'min_zoom': 3,
    'max_zoom': 10,  # Limited for educational viewing
}

# Educational layer definitions with civics content
LAYERS = {
    # ========== JUDICIAL BRANCH ==========

    'courts_of_appeals': {
        'name': 'US Courts of Appeals Circuits',
        'file': 'data/Courts_of_Appeals_Circuits.geojson',
        'branch': 'Judicial',
        'style': {
            'fillColor': '#4A90E2',
            'color': '#2C5AA0',
            'weight': 2.5,
            'fillOpacity': 0.35,
        },
        'highlight_style': {
            'fillColor': '#1E5A9E',
            'fillOpacity': 0.65,
        },
        'enabled_by_default': True,
        'education': {
            'title': 'Federal Appellate Courts',
            'description': 'The United States is divided into 12 regional circuits plus the DC Circuit and Federal Circuit (13 total). These courts hear appeals from district courts.',
            'purpose': 'Review decisions from district courts and ensure consistent application of federal law across the country.',
            'structure': '13 circuits covering all US states and territories',
            'established': '1891 (Evarts Act)',
            'why_it_matters': 'Circuit courts create binding precedents that affect millions of people. Conflicts between circuits often lead to Supreme Court review.',
        },
    },

    'bankruptcy_courts': {
        'name': 'US Bankruptcy Courts',
        'file': 'data/Bankruptcy_Courts.geojson',
        'branch': 'Judicial',
        'style': {
            'fillColor': '#7B68EE',
            'color': '#483D8B',
            'weight': 2,
            'fillOpacity': 0.3,
        },
        'highlight_style': {
            'fillColor': '#6A5ACD',
            'fillOpacity': 0.6,
        },
        'enabled_by_default': False,
        'education': {
            'title': 'Federal Bankruptcy System',
            'description': 'Specialized federal courts handling bankruptcy cases. Districts align with federal judicial districts.',
            'purpose': 'Provide relief to debtors and fair distribution to creditors under federal bankruptcy law.',
            'structure': '90 bankruptcy court districts across the US',
            'established': '1898 (Bankruptcy Act)',
            'why_it_matters': 'Over 400,000 bankruptcy cases are filed annually, affecting individuals, families, and businesses nationwide.',
        },
    },

    # ========== EXECUTIVE BRANCH - EMERGENCY MANAGEMENT ==========

    'fema_regions': {
        'name': 'FEMA Regions',
        'file': 'data/FEMA_Regions.geojson',
        'branch': 'Executive',
        'department': 'Homeland Security',
        'style': {
            'fillColor': '#FF6B6B',
            'color': '#C92A2A',
            'weight': 2.5,
            'fillOpacity': 0.35,
        },
        'highlight_style': {
            'fillColor': '#E03131',
            'fillOpacity': 0.65,
        },
        'enabled_by_default': True,
        'education': {
            'title': 'Federal Emergency Management',
            'description': 'FEMA divides the US into 10 regions to coordinate disaster response and emergency management.',
            'purpose': 'Coordinate federal disaster response, provide aid to states during emergencies, and support disaster preparedness.',
            'structure': '10 regional offices covering all states and territories',
            'established': '1979 (as independent agency, now part of DHS)',
            'why_it_matters': 'FEMA responds to hurricanes, floods, wildfires, and other disasters affecting millions of Americans annually.',
        },
    },

    'epa_regions': {
        'name': 'EPA Regions',
        'file': 'data/EPA_Regions.geojson',
        'branch': 'Executive',
        'department': 'Independent Agency',
        'style': {
            'fillColor': '#51CF66',
            'color': '#2F9E44',
            'weight': 2,
            'fillOpacity': 0.3,
        },
        'highlight_style': {
            'fillColor': '#37B24D',
            'fillOpacity': 0.6,
        },
        'enabled_by_default': False,
        'education': {
            'title': 'Environmental Protection',
            'description': 'The EPA uses 10 regions (same structure as FEMA/HHS) to enforce environmental laws and regulations.',
            'purpose': 'Protect human health and the environment by enforcing regulations on air, water, and land quality.',
            'structure': '10 regional offices - this is the foundational 10-region system used by many agencies',
            'established': '1970 (Nixon administration)',
            'why_it_matters': 'The EPA sets standards for clean air and water that affect every American, and enforces laws like the Clean Air Act.',
        },
    },

    # ========== EXECUTIVE BRANCH - ECONOMIC ==========

    'federal_reserve': {
        'name': 'Federal Reserve Districts',
        'file': 'data/Federal_Reserve_Districts.geojson',
        'branch': 'Executive',
        'department': 'Treasury',
        'style': {
            'fillColor': '#FFA94D',
            'color': '#E67700',
            'weight': 2.5,
            'fillOpacity': 0.35,
        },
        'highlight_style': {
            'fillColor': '#FD7E14',
            'fillOpacity': 0.65,
        },
        'enabled_by_default': True,
        'education': {
            'title': 'America\'s Central Bank',
            'description': 'The Federal Reserve System divides the US into 12 districts, each with a regional Federal Reserve Bank.',
            'purpose': 'Control monetary policy, supervise banks, maintain financial stability, and regulate the money supply.',
            'structure': '12 districts established in 1913, boundaries based on economic ties of that era',
            'established': '1913 (Federal Reserve Act)',
            'why_it_matters': 'The Fed controls interest rates and inflation, affecting every aspect of the American economy from home loans to employment.',
        },
    },

    # ========== EXECUTIVE BRANCH - CENSUS & DEMOGRAPHICS ==========

    'census_regions': {
        'name': 'Census Regions',
        'file': 'data/Census_Regions.geojson',
        'branch': 'Executive',
        'department': 'Commerce',
        'style': {
            'fillColor': '#FF8787',
            'color': '#C92A2A',
            'weight': 3,
            'fillOpacity': 0.25,
        },
        'highlight_style': {
            'fillColor': '#FA5252',
            'fillOpacity': 0.55,
        },
        'enabled_by_default': False,
        'education': {
            'title': 'National Demographics',
            'description': 'The Census Bureau divides the US into 4 major regions: Northeast, Midwest, South, and West.',
            'purpose': 'Organize demographic data collection and analysis for the constitutionally-mandated census.',
            'structure': '4 broad regions, further divided into 9 divisions',
            'established': '1910 (current boundaries)',
            'why_it_matters': 'Census data determines congressional representation, electoral votes, and distribution of $1.5 trillion in federal funds annually.',
        },
    },

    'census_divisions': {
        'name': 'Census Divisions',
        'file': 'data/Census_Divisions.geojson',
        'branch': 'Executive',
        'department': 'Commerce',
        'style': {
            'fillColor': '#FFB3B3',
            'color': '#E03131',
            'weight': 2,
            'fillOpacity': 0.25,
        },
        'highlight_style': {
            'fillColor': '#FF8787',
            'fillOpacity': 0.5,
        },
        'enabled_by_default': False,
        'education': {
            'title': 'Regional Demographics',
            'description': '9 divisions within the 4 census regions: New England, Middle Atlantic, East/West North Central, South Atlantic, East/West South Central, Mountain, and Pacific.',
            'purpose': 'Provide more detailed regional analysis of population, economy, and social characteristics.',
            'structure': '9 divisions nested within the 4 regions',
            'established': '1910 (current boundaries)',
            'why_it_matters': 'Division-level data helps understand regional economic and demographic trends across America.',
        },
    },

    # ========== EXECUTIVE BRANCH - EDUCATION ==========

    'education_regions': {
        'name': 'Department of Education Regions',
        'file': 'data/Education_Regions.geojson',
        'branch': 'Executive',
        'department': 'Education',
        'style': {
            'fillColor': '#74C0FC',
            'color': '#1C7ED6',
            'weight': 2,
            'fillOpacity': 0.3,
        },
        'highlight_style': {
            'fillColor': '#339AF0',
            'fillOpacity': 0.6,
        },
        'enabled_by_default': False,
        'education': {
            'title': 'Federal Education Administration',
            'description': 'The Department of Education uses the standard 10-region system (same as EPA/FEMA) to administer federal education programs.',
            'purpose': 'Distribute federal education funding, enforce civil rights in schools, and collect education data.',
            'structure': '10 regional offices aligned with EPA/FEMA regions',
            'established': '1980 (as cabinet-level department)',
            'why_it_matters': 'The department manages $68 billion in federal K-12 funding and student loan programs affecting millions of students.',
        },
    },

    # ========== EXECUTIVE BRANCH - INTERIOR ==========

    'blm_districts': {
        'name': 'Bureau of Land Management Districts',
        'file': 'data/BLM_Districts.geojson',
        'branch': 'Executive',
        'department': 'Interior',
        'style': {
            'fillColor': '#A0C287',
            'color': '#5F7C3E',
            'weight': 1.5,
            'fillOpacity': 0.3,
        },
        'highlight_style': {
            'fillColor': '#82A366',
            'fillOpacity': 0.6,
        },
        'enabled_by_default': False,
        'education': {
            'title': 'Public Lands Management',
            'description': 'The BLM manages 245 million acres of public land (about 1/8 of the entire US) through 12 state/district offices.',
            'purpose': 'Manage public lands for multiple uses: energy development, grazing, recreation, and conservation.',
            'structure': '12 state offices primarily in western states where most public land is located',
            'established': '1946 (merger of Grazing Service and General Land Office)',
            'why_it_matters': 'BLM manages more land than any other federal agency, balancing economic use with conservation.',
        },
    },

    # ========== MILITARY/DEFENSE ==========

    'coast_guard': {
        'name': 'Coast Guard Districts',
        'file': 'data/Coast_Guard_Districts.geojson',
        'branch': 'Military',
        'department': 'Homeland Security',
        'style': {
            'fillColor': '#4DABF7',
            'color': '#1971C2',
            'weight': 2.5,
            'fillOpacity': 0.35,
        },
        'highlight_style': {
            'fillColor': '#228BE6',
            'fillOpacity': 0.65,
        },
        'enabled_by_default': False,
        'education': {
            'title': 'Maritime Defense & Safety',
            'description': '9 Coast Guard districts covering US coastlines, Great Lakes, and inland waterways.',
            'purpose': 'Maritime law enforcement, search and rescue, environmental protection, and coastal security.',
            'structure': '9 districts plus sectors and stations along all US waters',
            'established': '1915 (merger of Revenue Cutter Service and Life-Saving Service)',
            'why_it_matters': 'The Coast Guard saves thousands of lives annually and enforces laws across 95,000 miles of coastline.',
        },
    },
}

# Color scheme for branch differentiation
BRANCH_COLORS = {
    'Judicial': '#4A90E2',    # Blue
    'Executive': '#51CF66',    # Green
    'Military': '#4DABF7',     # Light Blue
}

# Educational content about the three branches
BRANCH_INFO = {
    'Judicial': {
        'description': 'The Judicial Branch interprets laws and ensures they comply with the Constitution.',
        'structure': 'Supreme Court, Courts of Appeals, District Courts, and specialized courts.',
        'key_principle': 'Judicial independence - judges serve lifetime appointments to remain free from political pressure.',
    },
    'Executive': {
        'description': 'The Executive Branch enforces laws and administers federal programs.',
        'structure': '15 Cabinet departments, numerous independent agencies, and the Executive Office of the President.',
        'key_principle': 'Separation of powers - the President executes laws passed by Congress.',
    },
    'Military': {
        'description': 'The Military protects national security under civilian (Executive Branch) control.',
        'structure': 'Department of Defense and Department of Homeland Security (Coast Guard).',
        'key_principle': 'Civilian control of the military - military answers to elected civilian leaders.',
    },
}
