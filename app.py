import streamlit as st
import pandas as pd
import numpy as np
import re
import os
import pydeck as pdk
import requests

st.set_page_config(page_title="CBE Industrial Intelligence Engine",
                   layout="wide", initial_sidebar_state="expanded", page_icon="🏭")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');
html,body,[class*="css"]{font-family:'Syne',sans-serif;background:#060b18;color:#dde3f0;}
.main{background:#060b18;}.block-container{padding-top:1.5rem!important;max-width:1400px;}
section[data-testid="stSidebar"]{background:linear-gradient(180deg,#0b1526,#060b18);border-right:1px solid #162035;}
h1{font-family:'Syne',sans-serif!important;font-weight:800!important;font-size:2rem!important;
   background:linear-gradient(100deg,#38bdf8,#818cf8,#f472b6);-webkit-background-clip:text;
   -webkit-text-fill-color:transparent;background-clip:text;letter-spacing:-0.5px;margin-bottom:0!important;}
h2,h3{font-family:'Syne',sans-serif!important;font-weight:700!important;color:#c8d8f0!important;}
.search-wrapper{background:linear-gradient(135deg,#0b1a2e,#0d1f38);border:1px solid #1e4080;
  border-radius:14px;padding:1.2rem 1.5rem;margin-bottom:0.8rem;box-shadow:0 4px 24px #0066ff12;}
.search-title{font-family:'JetBrains Mono',monospace;font-size:0.62rem;color:#38bdf8;
  letter-spacing:3px;text-transform:uppercase;margin-bottom:0.5rem;}
.search-examples{font-family:'JetBrains Mono',monospace;font-size:0.68rem;color:#475a7a;line-height:1.9;margin-top:0.5rem;}
.search-examples span{color:#38bdf8;}
.pill-row{display:flex;flex-wrap:wrap;gap:6px;margin:0.6rem 0;}
.pill{display:inline-flex;align-items:center;gap:4px;font-family:'JetBrains Mono',monospace;
  font-size:0.68rem;padding:4px 12px;border-radius:20px;letter-spacing:0.5px;}
.pill-ok{background:#052e20;color:#34d399;border:1px solid #065f46;}
.pill-warn{background:#2d1500;color:#fb923c;border:1px solid #7c2d12;}
.pill-info{background:#0c1d3e;color:#60a5fa;border:1px solid #1e40af;}
.winner-card{background:linear-gradient(135deg,#091522,#0d1e35,#091522);border:1px solid #1e4a7a;
  border-radius:20px;padding:2rem 2.2rem;margin:1.5rem 0;position:relative;overflow:hidden;
  box-shadow:0 0 60px #0066ff0d,0 8px 32px #00000040;}
.winner-card::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;
  background:linear-gradient(90deg,#38bdf8,#818cf8,#f472b6,#38bdf8);}
.winner-eyebrow{font-family:'JetBrains Mono',monospace;font-size:0.6rem;letter-spacing:4px;
  color:#38bdf8;text-transform:uppercase;margin-bottom:0.6rem;display:flex;align-items:center;gap:8px;}
.winner-eyebrow::before{content:'';display:inline-block;width:8px;height:8px;border-radius:50%;
  background:#38bdf8;box-shadow:0 0 8px #38bdf8;}
.winner-name{font-family:'Syne',sans-serif;font-size:2.4rem;font-weight:800;color:#fff;line-height:1.1;margin-bottom:0.3rem;}
.winner-meta{font-family:'JetBrains Mono',monospace;font-size:0.78rem;color:#4a6080;}
.winner-score{font-family:'JetBrains Mono',monospace;font-size:0.68rem;color:#38bdf8;
  background:#0c2240;border:1px solid #1e4a7a;border-radius:6px;padding:2px 10px;margin-left:12px;}
.metric-grid{display:grid;grid-template-columns:repeat(7,1fr);gap:8px;margin:1.2rem 0;}
.metric-card{background:#0b1526;border:1px solid #162035;border-radius:12px;padding:0.75rem 0.5rem;text-align:center;}
.metric-icon{font-size:1.1rem;margin-bottom:0.2rem;}
.metric-label{font-family:'JetBrains Mono',monospace;font-size:0.52rem;color:#38bdf8;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:0.3rem;}
.metric-value{font-family:'Syne',sans-serif;font-size:1.2rem;font-weight:700;color:#fff;line-height:1;}
.metric-unit{font-family:'JetBrains Mono',monospace;font-size:0.58rem;color:#4a6080;margin-top:0.1rem;}
.metric-status-g{color:#34d399;font-size:0.58rem;margin-top:0.1rem;font-family:'JetBrains Mono',monospace;}
.metric-status-y{color:#fbbf24;font-size:0.58rem;margin-top:0.1rem;font-family:'JetBrains Mono',monospace;}
.metric-status-r{color:#f87171;font-size:0.58rem;margin-top:0.1rem;font-family:'JetBrains Mono',monospace;}
.reasoning-card{background:#0b1526;border:1px solid #162035;border-left:3px solid #818cf8;
  border-radius:12px;padding:1.4rem 1.6rem;margin-top:0.5rem;}
.reasoning-section{font-family:'JetBrains Mono',monospace;font-size:0.65rem;color:#38bdf8;
  letter-spacing:2px;text-transform:uppercase;margin:1rem 0 0.5rem;}
.reasoning-section:first-child{margin-top:0;}
.reasoning-row{display:flex;align-items:flex-start;gap:10px;padding:0.35rem 0;
  border-bottom:1px solid #0f1d30;font-family:'JetBrains Mono',monospace;font-size:0.76rem;color:#7a90b0;}
.reasoning-row:last-child{border-bottom:none;}
.reasoning-dot{width:6px;height:6px;border-radius:50%;flex-shrink:0;margin-top:5px;}
.dot-green{background:#34d399;box-shadow:0 0 6px #34d399;}
.dot-yellow{background:#fbbf24;box-shadow:0 0 6px #fbbf24;}
.dot-orange{background:#fb923c;box-shadow:0 0 6px #fb923c;}
.rval{color:#dde3f0;font-weight:600;}.rtag-g{color:#34d399;}.rtag-y{color:#fbbf24;}.rtag-o{color:#fb923c;}
.rank-card{background:#0b1526;border:1px solid #162035;border-radius:14px;padding:1rem 1.2rem;
  margin-bottom:0.8rem;display:flex;align-items:flex-start;gap:1rem;transition:border-color 0.2s;}
.rank-card:hover{border-color:#1e4080;}
.rank-card.rank-1{border-color:#f472b630;background:linear-gradient(90deg,#1a0a1e,#0b1526);}
.rank-number{font-family:'Syne',sans-serif;font-size:1.8rem;font-weight:800;color:#1a2a40;width:2.2rem;flex-shrink:0;text-align:center;padding-top:2px;}
.rank-card.rank-1 .rank-number{color:#f472b6;}
.rank-info{flex:1;min-width:0;}
.rank-name{font-family:'Syne',sans-serif;font-size:1rem;font-weight:700;color:#dde3f0;}
.rank-survey{font-family:'JetBrains Mono',monospace;font-size:0.66rem;color:#4a6080;margin-top:2px;}
.rank-badges{display:flex;flex-wrap:wrap;gap:4px;align-items:center;margin-top:6px;}
.badge{font-family:'JetBrains Mono',monospace;font-size:0.6rem;padding:2px 7px;border-radius:4px;letter-spacing:0.4px;white-space:nowrap;}
.b-eco{background:#052e20;color:#34d399;border:1px solid #065f46;}
.b-pwr{background:#170f40;color:#818cf8;border:1px solid #2d2380;}
.b-air{background:#1c1000;color:#fb923c;border:1px solid #7c3500;}
.b-rail{background:#0a1828;color:#38bdf8;border:1px solid #0c3060;}
.b-water{background:#001a2e;color:#22d3ee;border:1px solid #0c4060;}
.b-wf{background:#1a1000;color:#fbbf24;border:1px solid #7c5000;}
.b-inc{background:#1a0a1e;color:#f472b6;border:1px solid #7c2f6e;}
.b-icd{background:#001a10;color:#4ade80;border:1px solid #065f30;}
.b-hwy{background:#1a1000;color:#ff8c00;border:1px solid #7c4000;}
.map-legend{display:flex;flex-wrap:wrap;gap:12px;padding:0.8rem 1.2rem;
  background:#0b1526;border:1px solid #162035;border-radius:10px;margin-top:0.8rem;}
.legend-item{display:flex;align-items:center;gap:6px;font-family:'JetBrains Mono',monospace;font-size:0.68rem;color:#6a80a0;}
.legend-dot{width:11px;height:11px;border-radius:50%;flex-shrink:0;}
.sidebar-label{font-family:'JetBrains Mono',monospace;font-size:0.6rem;color:#38bdf8;
  letter-spacing:3px;text-transform:uppercase;margin-bottom:0.5rem;margin-top:0.8rem;display:block;}
.stat-row{display:flex;justify-content:space-between;align-items:center;padding:0.28rem 0;
  border-bottom:1px solid #0f1d30;font-family:'JetBrains Mono',monospace;font-size:0.68rem;}
.stat-label{color:#4a6080;}.stat-val{color:#dde3f0;font-weight:600;}
.section-header{display:flex;align-items:center;gap:12px;margin:1.8rem 0 1rem;}
.section-icon{font-size:1.1rem;}
.section-title{font-family:'Syne',sans-serif;font-size:1.15rem;font-weight:700;color:#c8d8f0;}
.section-line{flex:1;height:1px;background:linear-gradient(90deg,#162035,transparent);}
.parse-box{background:#060f1e;border:1px solid #0c3060;border-radius:12px;padding:0.9rem 1.2rem;margin-bottom:1.2rem;}
.parse-header{font-family:'JetBrains Mono',monospace;font-size:0.62rem;color:#38bdf8;letter-spacing:3px;text-transform:uppercase;margin-bottom:0.6rem;}
.parse-note{font-family:'JetBrains Mono',monospace;font-size:0.65rem;color:#2a4060;margin-top:0.5rem;}
[data-testid="stMetric"]{background:#0b1526!important;border:1px solid #162035!important;border-radius:12px!important;padding:0.8rem!important;}
div[data-testid="stTextInput"] input{background:#0b1526!important;border:1px solid #1e4080!important;border-radius:10px!important;color:#dde3f0!important;font-family:'JetBrains Mono',monospace!important;font-size:0.85rem!important;padding:0.7rem 1rem!important;}
div[data-testid="stTextInput"] input:focus{border-color:#38bdf8!important;box-shadow:0 0 0 2px #38bdf820!important;}
div[data-testid="stTextInput"] input::placeholder{color:#2a4060!important;}
.stExpander{border:1px solid #162035!important;border-radius:12px!important;background:#0b1526!important;}
hr{border-color:#0f1d30!important;margin:1.5rem 0!important;}

/* Google Maps panel styles */
.gmaps-panel{background:linear-gradient(135deg,#080f1e,#0b1829);border:1px solid #1a3a6a;
  border-radius:16px;padding:1.4rem 1.6rem;margin:1rem 0;position:relative;overflow:hidden;}
.gmaps-panel::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;
  background:linear-gradient(90deg,#4285f4,#34a853,#fbbc05,#ea4335);}
.gmaps-eyebrow{font-family:'JetBrains Mono',monospace;font-size:0.58rem;letter-spacing:4px;
  color:#4285f4;text-transform:uppercase;margin-bottom:0.8rem;}
.place-card{background:#060f1e;border:1px solid #0c2040;border-radius:10px;
  padding:0.7rem 1rem;margin:0.4rem 0;display:flex;align-items:flex-start;gap:10px;}
.place-name{font-family:'Syne',sans-serif;font-size:0.85rem;font-weight:600;color:#dde3f0;}
.place-meta{font-family:'JetBrains Mono',monospace;font-size:0.62rem;color:#4a6080;margin-top:2px;}
.place-dist{font-family:'JetBrains Mono',monospace;font-size:0.68rem;color:#38bdf8;
  background:#0c2240;border:1px solid #1e4a7a;border-radius:4px;padding:2px 7px;white-space:nowrap;margin-left:auto;}
.cat-header{font-family:'JetBrains Mono',monospace;font-size:0.6rem;color:#34d399;
  letter-spacing:3px;text-transform:uppercase;margin:0.8rem 0 0.4rem;display:flex;align-items:center;gap:6px;}
.drive-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin:0.8rem 0;}
.drive-card{background:#060f1e;border:1px solid #0c2040;border-radius:10px;padding:0.8rem;text-align:center;}
.drive-label{font-family:'JetBrains Mono',monospace;font-size:0.55rem;color:#4285f4;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:0.3rem;}
.drive-val{font-family:'Syne',sans-serif;font-size:1.3rem;font-weight:700;color:#fff;}
.drive-unit{font-family:'JetBrains Mono',monospace;font-size:0.55rem;color:#4a6080;margin-top:2px;}
.no-key-box{background:#0b1526;border:1px dashed #1e4080;border-radius:12px;padding:1.2rem 1.5rem;
  text-align:center;font-family:'JetBrains Mono',monospace;font-size:0.72rem;color:#2a4060;margin:1rem 0;}
.reverse-place{background:#060f1e;border:1px solid #0c2040;border-radius:10px;
  padding:0.6rem 1rem;margin:0.3rem 0;font-family:'JetBrains Mono',monospace;font-size:0.72rem;color:#7a90b0;}
.reverse-place strong{color:#dde3f0;}
.insight-box{background:linear-gradient(135deg,#050e1c,#070f1a);border:1px solid #0c2a50;
  border-left:3px solid #4285f4;border-radius:10px;padding:1rem 1.2rem;margin-top:0.8rem;
  font-family:'JetBrains Mono',monospace;font-size:0.72rem;color:#6a85a8;line-height:1.8;}
.insight-box strong{color:#38bdf8;}
</style>
""", unsafe_allow_html=True)


# ── GOOGLE MAPS API KEY ──────────────────────────────────────────────────────────
GOOGLE_MAPS_API_KEY = "AIzaSyD7imxilq1bYpXLU5EEz_C9aLS94tSnkso"

# ── CONSTANTS ────────────────────────────────────────────────────────────────────
AIRPORT = (11.0305, 77.0435)

KNOWN_SUBSTATIONS = [
    (11.101, 77.118, "Arasur 400kV"),     (10.944, 76.977, "Kurichi 400kV"),
    (10.924, 77.027, "Rasipalayam 400kV"),(11.063, 76.975, "Neelambur 110kV"),
    (11.054, 77.068, "Sulur 110kV"),      (11.081, 77.035, "Kalapatti 110kV"),
    (11.021, 77.020, "Singanallur 110kV"),(11.038, 77.000, "Saravanampatti 110kV"),
    (10.916, 77.097, "Irugur 110kV"),     (11.098, 77.001, "Annur 110kV"),
    (11.109, 77.213, "Avinashi 110kV"),   (10.860, 77.008, "Mettupalayam 110kV"),
    (10.665, 77.018, "Pollachi 110kV"),
]

INCENTIVE_GEOCOORDS = {
    "Annur": (11.098, 77.001), "Kinathukadavu": (10.740, 77.049),
    "Sultanpet": (10.800, 77.030), "Sulur": (11.030, 77.130),
    "Karamadai": (11.243, 76.959), "Madukkarai": (10.895, 76.956),
    "Periyanaickenpalayam": (11.075, 76.941), "Sarcarsamakulam": (11.030, 77.050),
    "Thondamuthur": (10.980, 76.850), "Pollachi North": (10.660, 77.018),
    "Pollachi South": (10.620, 77.010), "Anaimalai": (10.580, 76.940),
}

HIGHWAY_COORDS_MAP = {
    "Neelambur Junction": (11.063, 76.975),
    "L&T Bypass Junction": (11.015, 77.000),
    "Madukkarai Junction": (10.895, 76.956),
    "Avinashi Junction": (11.109, 77.213),
    "Periyanaickenpalayam Junction": (11.075, 76.941),
    "Sulur Junction": (11.030, 77.130),
}

DENSITY_SCORE = {
    "very high (4000+ workers)": 1.0, "high (4000+ workers)": 0.85,
    "very high": 1.0, "medium (3000+ workers)": 0.65, "high": 0.75, "medium": 0.55, "low": 0.30,
}
INCENTIVE_TIER_SCORE = {"backward": 1.0, "standard": 0.60}

INDUSTRY_DNA = {
    "Precision Engineering": {
        "weights": {"Power":0.30,"Airport":0.15,"Water":0.05,"Ecosystem":0.25,"Workforce":0.15,"Incentive":0.10},
        "keywords": ["engineering","foundry","machine","tool","fabricat","casting","forge","metal","machining","pump"],
        "workforce_match": ["Semi-Skilled (Industrial)","Skilled (Mechanical)","Semi-Skilled (Foundry)","Semi-Skilled (Technician)"],
        "icon": "⚙️", "desc": "Power reliability, engineering cluster, skilled workforce",
        # Google Places types to search for this industry
        "places_types": ["factory","storage","hardware_store","electrician"],
        "places_keywords": ["machine shop","metal fabrication","foundry","engineering","industrial supplier"],
    },
    "Food Processing": {
        "weights": {"Power":0.08,"Airport":0.07,"Water":0.35,"Ecosystem":0.25,"Workforce":0.15,"Incentive":0.10},
        "keywords": ["food","agro","dairy","grain","mill","spice","rice","flour","packaging","beverage"],
        "workforce_match": ["Unskilled (Agro-processing)","Unskilled / Semi-Skilled"],
        "icon": "🌾", "desc": "Water proximity critical; agro workforce and cluster valued",
        "places_types": ["storage","food","grocery_or_supermarket"],
        "places_keywords": ["cold storage","agro processing","food packaging","flour mill","rice mill"],
    },
    "Logistics & Warehouse": {
        "weights": {"Power":0.07,"Airport":0.28,"Water":0.05,"Ecosystem":0.20,"Workforce":0.12,"Incentive":0.08},
        "keywords": [],
        "workforce_match": ["Unskilled (Logistics)","Mixed (Commuter)"],
        "icon": "📦", "desc": "Airport, ICD dry port, highway connectivity are primary",
        "places_types": ["storage","moving_company","transit_station"],
        "places_keywords": ["warehouse","freight","logistics","transport","courier","cargo"],
    },
    "Textile / Garments": {
        "weights": {"Power":0.20,"Airport":0.08,"Water":0.15,"Ecosystem":0.30,"Workforce":0.17,"Incentive":0.10},
        "keywords": ["textile","yarn","weav","garment","spinning","knit","dyeing","bleach","apparel","cotton"],
        "workforce_match": ["Semi-Skilled (Textile)","Unskilled / Semi-Skilled"],
        "icon": "🧵", "desc": "Textile cluster, water for dyeing, garment workforce",
        "places_types": ["clothing_store","factory","laundry"],
        "places_keywords": ["textile","spinning mill","garment","yarn","dyeing","weaving"],
    },
    "Electronics / EV": {
        "weights": {"Power":0.25,"Airport":0.28,"Water":0.07,"Ecosystem":0.15,"Workforce":0.15,"Incentive":0.10},
        "keywords": ["electronics","auto","ev","electric","battery","semicon","pcb","motor","component","tech"],
        "workforce_match": ["Skilled (Digital)","Mixed (Manufacturing)","Skilled Professionals"],
        "icon": "⚡", "desc": "Airport for exports, reliable power, tech-skilled workforce",
        "places_types": ["electronics_store","factory","car_repair"],
        "places_keywords": ["electronics","EV","battery","components","PCB","motor winding"],
    },
}

DIMENSION_ALIASES = {
    "airport":   ["airport","air port","aerodrome","airfield"],
    "power":     ["power supply","sub station","substation","power","electricity","tneb","eb","transformer","grid"],
    "water":     ["water source","water body","water","lake","river","pond","reservoir","canal","stream"],
    "railway":   ["railway station","rail station","railroad","railway","rail","train","station"],
    "sidco":     ["industrial estate","industrial park","industrial zone","sidco","estate"],
    "highway":   ["national highway","bypass","highway","junction","expressway","nh"],
    "icd":       ["icd","inland container depot","container depot","dry port","customs"],
    "workforce": ["labour","labor","workforce","workers","manpower"],
}
DIM_TO_COL = {
    "airport":"airport_dist","power":"power_dist","water":"water_dist",
    "railway":"rail_dist","sidco":"sidco_dist","highway":"highway_dist","icd":"icd_dist",
}

# ─────────────────────────────────────────────────────────────────────────────
# GOOGLE MAPS API HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def get_gmaps_key():
    """Return the Google Maps API key from the global variable."""
    return GOOGLE_MAPS_API_KEY


def gmaps_nearby_search(lat, lon, keyword, radius=8000, api_key=""):
    """
    Call Google Places Nearby Search API.
    Returns list of place dicts with name, vicinity, rating, distance.
    """
    if not api_key:
        return []
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": f"{lat},{lon}",
        "radius": radius,
        "keyword": keyword,
        "key": api_key,
    }
    try:
        resp = requests.get(url, params=params, timeout=8)
        data = resp.json()
        places = []
        for p in data.get("results", [])[:6]:
            plat = p["geometry"]["location"]["lat"]
            plon = p["geometry"]["location"]["lng"]
            dist_km = haversine(lat, lon, plat, plon)
            places.append({
                "name": p.get("name", "Unknown"),
                "vicinity": p.get("vicinity", ""),
                "rating": p.get("rating", None),
                "dist_km": dist_km,
                "lat": plat,
                "lon": plon,
                "types": p.get("types", []),
            })
        # Sort by distance
        places.sort(key=lambda x: x["dist_km"])
        return places
    except Exception:
        return []


def gmaps_distance_matrix(origin_lat, origin_lon, destinations, api_key=""):
    """
    Call Google Distance Matrix API to get drive times from origin to multiple destinations.
    destinations: list of (lat, lon, label) tuples
    Returns list of dicts with label, distance_text, duration_text, duration_seconds
    """
    if not api_key or not destinations:
        return []
    origin = f"{origin_lat},{origin_lon}"
    dest_str = "|".join([f"{d[0]},{d[1]}" for d in destinations])
    url = "https://maps.googleapis.com/maps/api/distancematrix/json"
    params = {
        "origins": origin,
        "destinations": dest_str,
        "mode": "driving",
        "key": api_key,
    }
    try:
        resp = requests.get(url, params=params, timeout=10)
        data = resp.json()
        results = []
        rows = data.get("rows", [{}])
        elements = rows[0].get("elements", []) if rows else []
        for i, el in enumerate(elements):
            label = destinations[i][2] if i < len(destinations) else f"Dest {i+1}"
            if el.get("status") == "OK":
                results.append({
                    "label": label,
                    "distance_text": el["distance"]["text"],
                    "duration_text": el["duration"]["text"],
                    "duration_seconds": el["duration"]["value"],
                })
            else:
                results.append({
                    "label": label,
                    "distance_text": "N/A",
                    "duration_text": "N/A",
                    "duration_seconds": 9999,
                })
        return results
    except Exception:
        return []


def gmaps_reverse_geocode(lat, lon, api_key=""):
    """Get a human-readable address for coordinates."""
    if not api_key:
        return ""
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {"latlng": f"{lat},{lon}", "key": api_key}
    try:
        resp = requests.get(url, params=params, timeout=6)
        data = resp.json()
        results = data.get("results", [])
        if results:
            return results[0].get("formatted_address", "")
        return ""
    except Exception:
        return ""


def render_ecosystem_scan(lat, lon, industry, api_key):
    """Render the Live Ecosystem Scan panel for a given coordinate."""
    dna = INDUSTRY_DNA[industry]
    keywords_list = dna.get("places_keywords", [])

    st.markdown(f"""
<div class="gmaps-panel">
  <div class="gmaps-eyebrow">🛰️ Live Ecosystem Scan · Google Places API · {industry}</div>
""", unsafe_allow_html=True)

    if not api_key:
        st.markdown("""
<div class="no-key-box">
  ⚙️ Set your Google Maps API key in the <code>GOOGLE_MAPS_API_KEY</code> variable at the top of <code>app.py</code> to activate live scans.
</div>
""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        return

    all_places = []
    seen = set()

    with st.spinner("Scanning live business ecosystem via Google Places…"):
        for kw in keywords_list[:4]:  # limit API calls
            places = gmaps_nearby_search(lat, lon, kw, radius=8000, api_key=api_key)
            for p in places:
                if p["name"] not in seen:
                    seen.add(p["name"])
                    p["search_kw"] = kw
                    all_places.append(p)

    if not all_places:
        st.markdown('<div class="no-key-box">No businesses found nearby via Places API. Check your API key or try a different location.</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        return

    # Group by keyword category
    kw_groups = {}
    for p in all_places:
        kw = p["search_kw"]
        kw_groups.setdefault(kw, []).append(p)

    col1, col2 = st.columns(2)
    group_items = list(kw_groups.items())

    for gi, (kw, places) in enumerate(group_items):
        target_col = col1 if gi % 2 == 0 else col2
        with target_col:
            st.markdown(f'<div class="cat-header">📍 {kw.title()} ({len(places)} found)</div>', unsafe_allow_html=True)
            for p in places[:3]:
                rating_str = f"⭐ {p['rating']}" if p['rating'] else "No rating"
                st.markdown(f"""
<div class="place-card">
  <div style="flex:1;">
    <div class="place-name">{p['name']}</div>
    <div class="place-meta">{p['vicinity']} · {rating_str}</div>
  </div>
  <div class="place-dist">{p['dist_km']:.1f} km</div>
</div>""", unsafe_allow_html=True)

    # Ecosystem insight summary
    total = len(all_places)
    cluster_label = "Strong cluster" if total >= 10 else "Emerging cluster" if total >= 4 else "Sparse / greenfield"
    closest = min(all_places, key=lambda x: x["dist_km"])

    st.markdown(f"""
<div class="insight-box">
  <strong>Ecosystem Summary:</strong> {total} relevant businesses found within 8 km ·
  Cluster strength: <strong>{cluster_label}</strong><br>
  Closest match: <strong>{closest['name']}</strong> at {closest['dist_km']:.1f} km ·
  Industry fit: <strong>{industry}</strong>
</div>
""", unsafe_allow_html=True)

    # Add live places to map
    if all_places:
        places_df = pd.DataFrame([{
            "lat": p["lat"], "lon": p["lon"],
            "label": f"📍 {p['name']} ({p['dist_km']:.1f}km)",
            "color": [255, 215, 0, 220], "radius": 160
        } for p in all_places[:20]])
        st.session_state["live_places_df"] = places_df

    st.markdown("</div>", unsafe_allow_html=True)


def render_drive_times(lat, lon, api_key, substations, icd_points, highway_coords, highway_junctions):
    """Render real drive times to key infrastructure using Distance Matrix API."""
    st.markdown("""
<div class="gmaps-panel">
  <div class="gmaps-eyebrow">🚗 Real Drive Times · Google Distance Matrix API</div>
""", unsafe_allow_html=True)

    if not api_key:
        st.markdown('<div class="no-key-box">API key required for real drive times.</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        return

    destinations = [
        (AIRPORT[0], AIRPORT[1], "✈️ Coimbatore Airport"),
    ]
    # Nearest substation
    if substations:
        sub_dists = [(haversine(lat, lon, s[0], s[1]), s[0], s[1], KNOWN_SUBSTATIONS[i][2])
                     for i, s in enumerate(substations)]
        nearest_sub = min(sub_dists, key=lambda x: x[0])
        destinations.append((nearest_sub[1], nearest_sub[2], f"⚡ {nearest_sub[3]}"))

    # Nearest ICD
    if icd_points:
        icd_sorted = sorted(icd_points, key=lambda p: haversine(lat, lon, p[0], p[1]))
        destinations.append((icd_sorted[0][0], icd_sorted[0][1], f"🚢 {icd_sorted[0][2]}"))

    # Nearest highway junction
    if highway_coords and highway_junctions:
        hw_sorted = sorted(
            [(haversine(lat, lon, c[0], c[1]), c, highway_junctions[i])
             for i, c in enumerate(highway_coords) if i < len(highway_junctions)],
            key=lambda x: x[0]
        )
        if hw_sorted:
            destinations.append((hw_sorted[0][1][0], hw_sorted[0][1][1], f"🛣️ {hw_sorted[0][2]}"))

    with st.spinner("Fetching real drive times from Google…"):
        results = gmaps_distance_matrix(lat, lon, destinations, api_key=api_key)

    if not results:
        st.markdown('<div class="no-key-box">Could not fetch drive times. Check API key and Distance Matrix API is enabled.</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        return

    drive_cards = ""
    for r in results:
        drive_cards += f"""
<div class="drive-card">
  <div class="drive-label">{r['label']}</div>
  <div class="drive-val">{r['duration_text']}</div>
  <div class="drive-unit">{r['distance_text']}</div>
</div>"""

    st.markdown(f'<div class="drive-grid">{drive_cards}</div>', unsafe_allow_html=True)
    st.markdown(
        '<div style="font-family:JetBrains Mono,monospace;font-size:0.6rem;color:#1a3050;margin-top:0.5rem;">'
        'Real road travel times · Driving mode · Google Distance Matrix API</div>',
        unsafe_allow_html=True
    )
    st.markdown("</div>", unsafe_allow_html=True)


def generate_industry_insight(findings, industry, logistics, water_dist, power_dist, workforce_score):
    """
    Convert raw API signals into industry-specific reasoning.
    Returns (why_list, challenges_list).
    """
    dna = INDUSTRY_DNA.get(industry, {})
    why = []
    challenges = []

    # ── Cluster strength from Places findings ────────────────────────────────
    total_places = sum(len(v) for v in findings.values())
    if total_places >= 10:
        cluster_label = "Strong"
        cluster_note  = f"{total_places} relevant businesses detected within scan radius"
    elif total_places >= 5:
        cluster_label = "Moderate"
        cluster_note  = f"{total_places} supporting businesses found — growing ecosystem"
    else:
        cluster_label = "Weak / Greenfield"
        cluster_note  = f"Only {total_places} relevant units nearby — early-mover territory"

    # ── Logistics signals ────────────────────────────────────────────────────
    airport_time  = next((r for r in logistics if "Airport" in r["label"]), None)
    icd_time      = next((r for r in logistics if "ICD" in r["label"]), None)
    highway_time  = next((r for r in logistics if "Junction" in r["label"] or "Highway" in r["label"]), None)

    airport_mins  = airport_time["duration_seconds"] // 60 if airport_time and airport_time["duration_seconds"] != 9999 else 9999
    icd_mins      = icd_time["duration_seconds"] // 60    if icd_time    and icd_time["duration_seconds"]    != 9999 else 9999
    highway_mins  = highway_time["duration_seconds"] // 60 if highway_time and highway_time["duration_seconds"] != 9999 else 9999

    # ── Industry-specific reasoning ──────────────────────────────────────────
    if industry == "Food Processing":
        # Water is king
        if water_dist < 2:
            why.append(f"Exceptional water proximity ({water_dist:.1f} km) — critical for processing, cleaning & boiler ops")
        elif water_dist < 6:
            why.append(f"Reliable water access ({water_dist:.1f} km) — supports daily production requirements")
        else:
            challenges.append(f"Water body is {water_dist:.1f} km away — piping/borewell investment likely needed")

        if cluster_label == "Strong":
            why.append(f"Strong agro-processing cluster — {cluster_note}; vendor network & cold-chain already present")
        elif cluster_label == "Moderate":
            why.append(f"Emerging food cluster — {cluster_note}; room to anchor the local supply chain")
        else:
            challenges.append(f"Sparse ecosystem — {cluster_note}; raw material procurement may depend on long hauls")

        if highway_mins < 15:
            why.append(f"Fast highway access (~{highway_mins} min) — efficient farm-to-factory logistics")
        elif highway_mins < 30:
            why.append(f"Moderate highway connectivity (~{highway_mins} min drive) — manageable inbound logistics")
        else:
            challenges.append(f"Highway is ~{highway_mins} min away — transportation costs for perishables will be elevated")

        if workforce_score > 0.7:
            why.append("High availability of semi-skilled agro-processing labour in the zone")
        elif workforce_score > 0.5:
            why.append("Adequate unskilled / semi-skilled workforce for production lines")
        else:
            challenges.append("Workforce density is low — labour recruitment may require incentives or housing")

        challenges.append("Seasonal dependency on raw materials — storage or diversification strategy needed")
        if cluster_label == "Strong":
            challenges.append("Labour competition is higher in dense food clusters — wage pressure expected")
        challenges.append("Water scarcity risk during dry seasons — rainwater harvesting or ETP planning required")

    elif industry == "Precision Engineering":
        if power_dist < 3:
            why.append(f"Substation within {power_dist:.1f} km — low latency power access for CNC & heat-treatment ops")
        elif power_dist < 7:
            why.append(f"Power substation at {power_dist:.1f} km — reliable supply for precision machinery")
        else:
            challenges.append(f"Substation is {power_dist:.1f} km away — voltage fluctuation risk; DG backup essential")

        if cluster_label in ("Strong", "Moderate"):
            why.append(f"Engineering cluster active — {cluster_note}; tooling, sub-contractors & raw stock accessible locally")
        else:
            challenges.append(f"Weak engineering ecosystem — {cluster_note}; supply chain must be built from scratch")

        if airport_mins < 25:
            why.append(f"Airport within ~{airport_mins} min — supports precision export shipments & import of raw stock")
        else:
            challenges.append(f"Airport access is ~{airport_mins} min — longer turnaround on time-sensitive exports")

        if workforce_score > 0.7:
            why.append("Strong presence of skilled mechanical / ITI-trained workforce in the area")
        else:
            challenges.append("Skilled workforce (machinist, fabricator) may be scarce — training partnerships needed")

        challenges.append("Power outages during peak demand can damage precision tooling mid-cycle — UPS/AVR critical")
        challenges.append("Cluster competition for skilled labour may push attrition rates higher")

    elif industry == "Logistics & Warehouse":
        if highway_mins < 10:
            why.append(f"Exceptional highway connectivity (~{highway_mins} min) — ideal for multi-hub distribution")
        elif highway_mins < 20:
            why.append(f"Good highway access (~{highway_mins} min) — viable for regional distribution operations")
        else:
            challenges.append(f"Highway is ~{highway_mins} min away — increases last-mile and hub turnaround time")

        if airport_mins < 20:
            why.append(f"Airport reachable in ~{airport_mins} min — supports air freight & express cargo ops")
        elif airport_mins < 40:
            why.append(f"Airport accessible in ~{airport_mins} min — suitable for scheduled cargo runs")
        else:
            challenges.append(f"Airport ~{airport_mins} min away — air freight logistics cost will be above benchmark")

        if icd_mins < 20:
            why.append(f"ICD Dry Port within ~{icd_mins} min — direct customs clearance; reduces dwell time significantly")
        elif icd_mins < 40:
            why.append(f"ICD accessible in ~{icd_mins} min — viable for container movements")
        else:
            challenges.append(f"ICD is ~{icd_mins} min drive — container logistics add to transit cost")

        if cluster_label in ("Strong", "Moderate"):
            why.append(f"Supporting logistics ecosystem — {cluster_note}; freight brokers, packers & FTL operators nearby")
        else:
            challenges.append(f"Thin logistics cluster — {cluster_note}; limited co-loading or 3PL partnerships locally")

        challenges.append("Land cost appreciation near highway nodes — lease rates may rise with demand")
        challenges.append("Driver fatigue regulations and toll costs on long-haul routes need route optimisation")

    elif industry == "Textile / Garments":
        if water_dist < 3:
            why.append(f"Water source within {water_dist:.1f} km — essential for dyeing, bleaching & finishing ops")
        elif water_dist < 8:
            why.append(f"Water access at {water_dist:.1f} km — feasible for textile wet-processing with piping investment")
        else:
            challenges.append(f"Water body {water_dist:.1f} km away — wet-process units will face high water-procurement cost")

        if power_dist < 5:
            why.append(f"Power substation at {power_dist:.1f} km — supports spinning, weaving & loom electricity demand")
        else:
            challenges.append(f"Substation {power_dist:.1f} km away — power cost & reliability risk for continuous looms")

        if cluster_label == "Strong":
            why.append(f"Strong textile cluster — {cluster_note}; yarn suppliers, embroidery units & job-workers nearby")
        elif cluster_label == "Moderate":
            why.append(f"Emerging textile ecosystem — {cluster_note}; vendor development possible over short term")
        else:
            challenges.append(f"Weak textile cluster — {cluster_note}; full backward integration required")

        if workforce_score > 0.65:
            why.append("Adequate semi-skilled textile workforce (stitching, knitting, quality check) available")
        else:
            challenges.append("Textile skill gap present — tailoring & quality-control training will be necessary")

        challenges.append("Effluent treatment (ETP) is mandatory for dyeing units — compliance cost is significant")
        challenges.append("Cotton price volatility can impact margins — raw material hedging strategy needed")
        challenges.append("Labour-intensive operations face disruption from seasonal festival-related absenteeism")

    elif industry == "Electronics / EV":
        if airport_mins < 20:
            why.append(f"Airport in ~{airport_mins} min — critical for PCB/component imports & export of finished goods")
        elif airport_mins < 35:
            why.append(f"Airport ~{airport_mins} min away — usable for scheduled air-cargo cycles")
        else:
            challenges.append(f"Airport ~{airport_mins} min away — time-sensitive supply chains will face disruption risk")

        if power_dist < 3:
            why.append(f"Substation within {power_dist:.1f} km — stable clean power for sensitive electronics assembly")
        elif power_dist < 6:
            why.append(f"Power at {power_dist:.1f} km — adequate with surge protection and UPS systems")
        else:
            challenges.append(f"Substation {power_dist:.1f} km away — power quality risk for PCB & EV battery assembly")

        if cluster_label in ("Strong", "Moderate"):
            why.append(f"Electronics/EV ecosystem forming — {cluster_note}; component vendors & EMS players accessible")
        else:
            challenges.append(f"Greenfield for electronics — {cluster_note}; component supply chain must be entirely imported")

        if workforce_score > 0.7:
            why.append("Skilled / diploma-level technical workforce available — suitable for SMT & EV assembly lines")
        else:
            challenges.append("Technical skill gap — ITI/polytechnic graduates need targeted hiring; training cost high")

        challenges.append("ESD-sensitive operations require controlled environment investment (cleanroom, humidity control)")
        challenges.append("Battery logistics (for EV) classified as hazardous — special transport compliance required")

    else:
        # Generic fallback
        if cluster_label != "Weak / Greenfield":
            why.append(f"Active industrial ecosystem — {cluster_note}")
        else:
            challenges.append(f"Sparse ecosystem — {cluster_note}")
        if highway_mins < 20:
            why.append(f"Good highway connectivity (~{highway_mins} min)")
        if power_dist < 5:
            why.append(f"Power infrastructure within {power_dist:.1f} km")
        if water_dist < 5:
            why.append(f"Water body within {water_dist:.1f} km")
        challenges.append("Industry-specific infrastructure requirements should be assessed on-site")

    return why, challenges


def render_reverse_analysis(api_key, company_row=None, selected_industry=None):
    """
    Render the Reverse Location Analysis panel.
    If company_row is provided, uses its coordinates automatically (no manual input).
    Generates industry-specific reasoning using Industry DNA.
    """
    st.markdown("""
<div class="gmaps-panel">
  <div class="gmaps-eyebrow">🔍 Reverse Location Analysis · Industry-Specific Site Intelligence</div>
""", unsafe_allow_html=True)

    if not api_key:
        st.markdown('<div class="no-key-box">API key required for reverse location analysis.</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        return

    # ── Coordinate source: auto from company row OR manual input ─────────────
    if company_row is not None:
        r_lat = float(company_row["lat"])
        r_lon = float(company_row["lon"])
        st.markdown(
            f'<div style="font-family:JetBrains Mono,monospace;font-size:0.7rem;color:#34d399;margin-bottom:0.6rem;">'
            f'📌 Using parcel coordinates: <strong>{r_lat:.5f}, {r_lon:.5f}</strong></div>',
            unsafe_allow_html=True
        )
    else:
        col_lat, col_lon = st.columns(2)
        with col_lat:
            r_lat = st.number_input("Latitude", value=11.054, format="%.5f", key="rev_lat",
                                    help="Paste the latitude of a competitor plant or industry location")
        with col_lon:
            r_lon = st.number_input("Longitude", value=77.068, format="%.5f", key="rev_lon",
                                    help="Paste the longitude of a competitor plant or industry location")

    scan_radius = st.slider("Search radius (km)", 2, 20, 10, key="rev_radius")
    rev_industry = selected_industry  # passed from caller; falls back to None

    if st.button("🔍 Analyse This Location", key="rev_btn"):
        with st.spinner(f"Reverse-engineering site selection logic for {rev_industry or 'this industry'}…"):

            # Geocode
            address = gmaps_reverse_geocode(r_lat, r_lon, api_key)

            # Industry-specific keyword categories
            dna_local = INDUSTRY_DNA.get(rev_industry, {})
            ind_keywords = dna_local.get("places_keywords", [])
            base_categories = [
                ("freight & logistics", "freight logistics transport"),
                ("raw material vendors", "industrial supplier raw material"),
                ("labour & workforce", "industrial workers labour contractor"),
                ("fuel & utilities", "fuel station diesel"),
            ]
            # Add industry-specific keyword searches
            ind_categories = [(kw, kw) for kw in ind_keywords[:3]]
            search_categories = base_categories + ind_categories

            findings = {}
            for cat_label, kw in search_categories:
                places = gmaps_nearby_search(r_lat, r_lon, kw, radius=scan_radius * 1000, api_key=api_key)
                if places:
                    findings[cat_label] = places[:3]

            # Drive times to CBE infrastructure
            infra_dests = [
                (AIRPORT[0], AIRPORT[1], "✈️ Airport"),
                (11.016, 77.016, "🚢 ICD Irugur"),
                (11.063, 76.975, "🛣️ Neelambur Junction"),
            ]
            drive_results = gmaps_distance_matrix(r_lat, r_lon, infra_dests, api_key=api_key)

            # Straight-line water & power distances for reasoning
            water_d = min_dist(r_lat, r_lon,
                               list(zip(water["latitude"], water["longitude"]))) \
                      if water is not None and not water.empty else 8.0
            power_d = min_dist(r_lat, r_lon, substations) if substations else 5.0

            # Workforce proxy: use nearest parcel's score if available
            wf_score = 0.55
            if not df.empty:
                nearest_idx = df.apply(lambda r: haversine(r_lat, r_lon, r["lat"], r["lon"]), axis=1).idxmin()
                wf_score = df.loc[nearest_idx, "workforce_score"] if "workforce_score" in df.columns else 0.55

        # ── Display address ───────────────────────────────────────────────────
        if address:
            st.markdown(
                f'<div style="font-family:JetBrains Mono,monospace;font-size:0.7rem;color:#38bdf8;margin:0.5rem 0;">'
                f'📌 {address}</div>', unsafe_allow_html=True)

        # ── Infrastructure drive times ─────────────────────────────────────────
        if drive_results:
            st.markdown('<div class="cat-header">🏗️ Infrastructure Accessibility</div>', unsafe_allow_html=True)
            drive_cards = "".join([
                f'<div class="drive-card"><div class="drive-label">{r["label"]}</div>'
                f'<div class="drive-val">{r["duration_text"]}</div>'
                f'<div class="drive-unit">{r["distance_text"]}</div></div>'
                for r in drive_results
            ])
            st.markdown(f'<div class="drive-grid">{drive_cards}</div>', unsafe_allow_html=True)

        # ── Ecosystem findings ─────────────────────────────────────────────────
        if findings:
            st.markdown('<div class="cat-header">🧩 Ecosystem Signals Detected</div>', unsafe_allow_html=True)
            for cat, places in findings.items():
                nearest = places[0]
                st.markdown(f"""
<div class="reverse-place">
  ✦ <strong>{cat.title()}</strong> — {nearest['name']} is {nearest['dist_km']:.1f} km away
  <span style="color:#2a4060;"> · {nearest['vicinity']}</span>
</div>""", unsafe_allow_html=True)

        # ── Cluster score banner ───────────────────────────────────────────────
        total_places = sum(len(v) for v in findings.values())
        if total_places >= 10:
            cluster_col, cluster_txt = "#34d399", f"Strong Cluster · {total_places} relevant units"
        elif total_places >= 5:
            cluster_col, cluster_txt = "#fbbf24", f"Moderate Cluster · {total_places} units found"
        else:
            cluster_col, cluster_txt = "#fb923c", f"Weak / Greenfield · {total_places} units found"

        st.markdown(
            f'<div style="font-family:JetBrains Mono,monospace;font-size:0.7rem;color:{cluster_col};'
            f'background:#060f1e;border:1px solid {cluster_col}40;border-radius:8px;padding:0.5rem 1rem;'
            f'margin:0.6rem 0;">🏭 Cluster Strength: <strong>{cluster_txt}</strong></div>',
            unsafe_allow_html=True
        )

        # ── Industry-Specific Insight ──────────────────────────────────────────
        if rev_industry:
            why_list, challenge_list = generate_industry_insight(
                findings, rev_industry, drive_results, water_d, power_d, wf_score
            )

            why_html = "".join(
                f'<div class="reasoning-row">'
                f'<div class="reasoning-dot dot-green"></div>'
                f'<span style="color:#c8d8f0;">{point}</span></div>'
                for point in why_list
            )
            challenge_html = "".join(
                f'<div class="reasoning-row">'
                f'<div class="reasoning-dot dot-orange"></div>'
                f'<span style="color:#c8d8f0;">{point}</span></div>'
                for point in challenge_list
            )

            ind_icon = INDUSTRY_DNA.get(rev_industry, {}).get("icon", "🏭")
            st.markdown(f"""
<div class="reasoning-card" style="margin-top:1rem;border-left-color:#34d399;">
  <div style="font-family:JetBrains Mono,monospace;font-size:0.62rem;color:#34d399;
       letter-spacing:3px;text-transform:uppercase;margin-bottom:0.8rem;">
    {ind_icon} {rev_industry} · Industry-Specific Analysis
  </div>

  <div class="reasoning-section">🧠 Why This Location Works</div>
  {why_html if why_html else '<div class="reasoning-row"><span style="color:#4a6080;">Insufficient data to generate strengths — try increasing scan radius.</span></div>'}

  <div class="reasoning-section" style="margin-top:1rem;">⚠️ Challenges</div>
  {challenge_html if challenge_html else '<div class="reasoning-row"><span style="color:#4a6080;">No challenges flagged at this scan radius.</span></div>'}
</div>""", unsafe_allow_html=True)
        else:
            # Generic fallback if no industry selected
            reasons = list(findings.keys())
            insight = f"This location appears chosen for: {', '.join(reasons[:3])}. "
            insight += ("Mature ecosystem suggests deliberate clustering." if len(findings) >= 3
                        else "Emerging ecosystem — early mover advantage likely.")
            st.markdown(f'<div class="insight-box"><strong>Site Selection Insight:</strong> {insight}</div>',
                        unsafe_allow_html=True)

        if not findings:
            st.markdown(
                '<div class="no-key-box">No significant ecosystem found at this radius. '
                'Try increasing the scan radius or verify coordinates.</div>',
                unsafe_allow_html=True
            )

    st.markdown("</div>", unsafe_allow_html=True)


# ── UTILS ────────────────────────────────────────────────────────────────────────
def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    lat1,lon1,lat2,lon2 = map(np.radians,[lat1,lon1,lat2,lon2])
    dlat,dlon = lat2-lat1, lon2-lon1
    a = np.sin(dlat/2)**2 + np.cos(lat1)*np.cos(lat2)*np.sin(dlon/2)**2
    return R*(2*np.arcsin(np.sqrt(a)))

def detect_col(df, candidates):
    cols_lower = {c.lower():c for c in df.columns}
    for c in candidates:
        if c.lower() in cols_lower: return cols_lower[c.lower()]
    return None

def normalize(series):
    mn,mx = series.min(), series.max()
    if mx==mn: return pd.Series(np.zeros(len(series)), index=series.index)
    return (series-mn)/(mx-mn)

def min_dist(lat, lon, points):
    if not points: return np.nan
    return min(haversine(lat,lon,p[0],p[1]) for p in points)

def load_wkt_csv(filepath):
    rows = []
    try:
        with open(filepath,'r',encoding='utf-8') as f:
            f.readline()
            for line in f:
                line = line.strip()
                if not line: continue
                wm = re.match(r'^"([^"]+)",(.*)', line)
                if wm:
                    wkt_str = wm.group(1)
                    rest = wm.group(2).split(',')
                    name = rest[0] if rest else ''
                else:
                    parts = line.split(',')
                    wkt_str = parts[0]; name = parts[1] if len(parts)>1 else ''
                m = re.match(r'POINT\s*\(\s*([\d.\-]+)\s+([\d.\-]+)\s*\)', wkt_str)
                if m: rows.append({'name':name.strip(),'_lat':float(m.group(2)),'_lon':float(m.group(1))})
    except Exception: pass
    return pd.DataFrame(rows)


# ── NLP PARSER ──────────────────────────────────────────────────────────────────
NUM_PAT  = r"(\d+(?:\.\d+)?)"
UNIT_PAT = r"(km|kms|k\.m\.|kilometers?|kilometres?|m\b|meters?|metres?|mtrs?)?"
PREP_PAT = r"(?:from|of|away|to|at|within|in|upto|up\s*to|around|near|by)?"
KW_PAT   = r"([a-z][a-z ]{1,35})"
PATTERNS = [
    re.compile(rf"^(?:within|in|upto|up\s*to)\s+{NUM_PAT}\s*{UNIT_PAT}\s*(?:of\s*)?{KW_PAT}$", re.I),
    re.compile(rf"^{NUM_PAT}\s*{UNIT_PAT}\s*{PREP_PAT}\s*{KW_PAT}$", re.I),
    re.compile(rf"^{KW_PAT}\s+{PREP_PAT}\s*{NUM_PAT}\s*{UNIT_PAT}$", re.I),
    re.compile(rf"^{KW_PAT}\s+(?:within|in|upto|up\s*to|at|from)\s+{NUM_PAT}\s*{UNIT_PAT}$", re.I),
]
QUALITATIVE = {"next to":0.8,"adjacent to":0.8,"beside":0.8,"very close":1.5,"close to":3.0,"near":4.0,"nearby":4.0}

def to_km(value, unit):
    u = str(unit or "km").lower().strip().replace(".","").replace(" ","")
    return float(value)/1000.0 if u in ("m","meter","meters","metre","metres","mtr","mtrs") else float(value)

def match_dimension(text):
    t = " " + text.lower().strip() + " "
    for dim,aliases in DIMENSION_ALIASES.items():
        for alias in sorted(aliases,key=len,reverse=True):
            if alias in t: return dim
    return None

def parse_query(raw):
    if not raw or not raw.strip(): return {"constraints":{},"interpreted":[],"raw":raw}
    constraints,interpreted = {},[]
    for seg in re.split(r"[,;]|\band\b", raw.lower(), flags=re.I):
        seg = seg.strip().rstrip(".,;")
        if not seg: continue
        matched = False
        for pat in PATTERNS:
            m = pat.match(seg)
            if not m: continue
            groups = [g for g in m.groups() if g is not None]
            try:
                if pat in (PATTERNS[0],PATTERNS[1]):
                    num_str=groups[0]; unit_str=groups[1] if len(groups)>2 else None; kw_str=groups[-1]
                else:
                    kw_str=groups[0]; num_str=groups[-2] if len(groups)>2 else groups[-1]; unit_str=groups[-1] if len(groups)>2 else None
                dim = match_dimension(kw_str)
                if dim:
                    km = to_km(num_str, unit_str)
                    constraints[dim] = min(constraints.get(dim,9999), km)
                    interpreted.append(f"{dim.title()} ≤ {km:.2g} km")
                    matched = True; break
            except Exception: continue
        if not matched:
            for qual,km_val in sorted(QUALITATIVE.items(),key=lambda x:-len(x[0])):
                if qual in seg:
                    after = seg[seg.find(qual)+len(qual):].strip()
                    dim = match_dimension(after) or match_dimension(seg)
                    if dim and dim not in constraints:
                        constraints[dim]=km_val; interpreted.append(f"{dim.title()} ≤ {km_val:.1f} km ('{qual}')"); break
    return {"constraints":constraints,"interpreted":interpreted,"raw":raw}

def constraint_penalty(row, constraints):
    penalty = 0.0
    for dim,max_km in constraints.items():
        col = DIM_TO_COL.get(dim)
        if col and col in row.index:
            actual = row[col]
            if actual > max_km:
                ratio = (actual-max_km)/max(max_km,0.1)
                penalty += min(ratio*0.40, 0.50)
    return penalty

def check_compliance(row, constraints):
    result = {}
    for dim,max_km in constraints.items():
        col = DIM_TO_COL.get(dim)
        if col and col in row.index:
            actual = row[col]
            result[dim] = {"actual":actual,"limit":max_km,"ok":actual<=max_km}
    return result


# ── DATA LOADING ─────────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def load_all():
    problems = []

    # Land
    land = None
    try:
        land = pd.read_csv("empty_land.csv", on_bad_lines="skip", engine="python")
        land.columns = [c.strip().lower() for c in land.columns]
        lat_c = detect_col(land,["lat","latitude"]); lon_c = detect_col(land,["lon","longitude","long"])
        if lat_c and lat_c!="lat": land=land.rename(columns={lat_c:"lat"})
        if lon_c and lon_c!="lon": land=land.rename(columns={lon_c:"lon"})
        land["lat"]=pd.to_numeric(land["lat"],errors="coerce"); land["lon"]=pd.to_numeric(land["lon"],errors="coerce")
        land = land.dropna(subset=["lat","lon"])
    except Exception as e: problems.append(f"empty_land.csv: {e}")

    # Water
    water = None
    try:
        water = pd.read_csv("water_bodies.csv", on_bad_lines="skip", engine="python")
        water.columns = [c.strip().lower() for c in water.columns]
        wlat=detect_col(water,["lat","latitude"]); wlon=detect_col(water,["lon","longitude","long"])
        if wlat and wlat!="latitude": water=water.rename(columns={wlat:"latitude"})
        if wlon and wlon!="longitude": water=water.rename(columns={wlon:"longitude"})
        water["latitude"]=pd.to_numeric(water["latitude"],errors="coerce")
        water["longitude"]=pd.to_numeric(water["longitude"],errors="coerce")
        water = water.dropna(subset=["latitude","longitude"])
    except Exception as e: problems.append(f"water_bodies.csv: {e}")

    # Corridors
    corridor_frames = []
    for fname in ["corridor_1.csv","corridor_2.csv"]:
        try:
            d = pd.read_csv(fname, on_bad_lines="skip", engine="python")
            d.columns = [c.strip().lower() for c in d.columns]
            clat=detect_col(d,["lat","latitude"]); clon=detect_col(d,["lon","longitude","long"])
            if clat: d=d.rename(columns={clat:"latitude"})
            if clon: d=d.rename(columns={clon:"longitude"})
            d["latitude"]=pd.to_numeric(d.get("latitude",pd.Series(dtype=float)),errors="coerce")
            d["longitude"]=pd.to_numeric(d.get("longitude",pd.Series(dtype=float)),errors="coerce")
            d = d.dropna(subset=["latitude","longitude"]); corridor_frames.append(d)
        except Exception as e: problems.append(f"{fname}: {e}")
    corridor = pd.concat(corridor_frames,ignore_index=True) if corridor_frames else pd.DataFrame()
    if not corridor.empty:
        ind_col = detect_col(corridor,["industry","industry category","industrial sector","business type","business","sector","type","category","activity"])
        if ind_col and ind_col!="industry": corridor=corridor.rename(columns={ind_col:"industry"})
        if "industry" not in corridor.columns:
            str_cols=[c for c in corridor.columns if corridor[c].dtype==object]
            corridor["industry"]=corridor[str_cols[0]] if str_cols else ""

    # Substations
    substations = [(r[0],r[1]) for r in KNOWN_SUBSTATIONS]
    sub_names   = [r[2] for r in KNOWN_SUBSTATIONS]
    sub_full    = list(KNOWN_SUBSTATIONS)

    # Railway
    rail_stations, rail_df = [], pd.DataFrame()
    try:
        rail_candidates=["Railway_stations.csv","railway_stations.csv","Railway_Stations.csv"]
        rail_file = next((f for f in rail_candidates if os.path.isfile(f)),None)
        if not rail_file: raise FileNotFoundError("No Railway file")
        rail_df = load_wkt_csv(rail_file)
        if not rail_df.empty:
            rail_df["station_name"]=rail_df["name"].fillna("Railway Station")
            rail_stations = list(zip(rail_df["_lat"],rail_df["_lon"]))
    except Exception as e: problems.append(f"Railway: {e}")

    # SIDCO
    sidco = pd.DataFrame()
    try:
        sidco_candidates=["SIDCO_industrial_estates_coimbatore.csv","SIDCO_industrial_estates_coimbatore_xlsx.csv","sidco_estates.csv"]
        sidco_file = next((f for f in sidco_candidates if os.path.isfile(f)),None)
        if not sidco_file: raise FileNotFoundError("No SIDCO file")
        sidco = load_wkt_csv(sidco_file)
        if not sidco.empty: sidco=sidco.rename(columns={"_lat":"latitude","_lon":"longitude"})
    except Exception as e: problems.append(f"SIDCO: {e}")

    # Highway junctions
    highway_junctions, highway_coords = [], []
    try:
        with open("Highway_junctions.csv","r",encoding="utf-8") as f:
            f.readline()
            for line in f:
                line=line.strip()
                if not line: continue
                name = line.split(",")[0].strip()
                if name: highway_junctions.append(name)
        highway_coords = [(HIGHWAY_COORDS_MAP[n][0],HIGHWAY_COORDS_MAP[n][1])
                          for n in highway_junctions if n in HIGHWAY_COORDS_MAP]
    except Exception as e: problems.append(f"Highway: {e}")

    # ICD
    icd_points = []
    try:
        icd_candidates=["icd_irugur.csv","ICD_irugur.csv","icd.csv"]
        icd_file = next((f for f in icd_candidates if os.path.isfile(f)),None)
        if icd_file:
            icd_df=pd.read_csv(icd_file,on_bad_lines="skip",engine="python")
            icd_df.columns=[c.strip().lower() for c in icd_df.columns]
            lat_c=detect_col(icd_df,["latitude","lat"]); lon_c=detect_col(icd_df,["longitude","lon","long"])
            name_c=detect_col(icd_df,["location_name","name","location"])
            if lat_c and lon_c:
                for _,row in icd_df.iterrows():
                    try: icd_points.append((float(row[lat_c]),float(row[lon_c]),str(row[name_c]) if name_c else "ICD"))
                    except Exception: pass
        else: problems.append("icd_irugur.csv not found")
    except Exception as e: problems.append(f"ICD: {e}")

    # Workforce
    workforce_df = pd.DataFrame()
    try:
        wf_candidates=["cbe_workforce_detailed.csv","workforce.csv"]
        wf_file = next((f for f in wf_candidates if os.path.isfile(f)),None)
        if wf_file:
            workforce_df=pd.read_csv(wf_file,on_bad_lines="skip",engine="python")
            workforce_df.columns=[c.strip().lower() for c in workforce_df.columns]
            anc=detect_col(workforce_df,["area_name","area","location","name"])
            if anc and anc!="area_name": workforce_df=workforce_df.rename(columns={anc:"area_name"})
            workforce_df["area_name"]=workforce_df["area_name"].str.strip()
        else: problems.append("cbe_workforce_detailed.csv not found")
    except Exception as e: problems.append(f"Workforce: {e}")

    # Incentive zones
    incentive_df = pd.DataFrame()
    try:
        inc_candidates=["cbe_incentive_clean.csv","incentive.csv"]
        inc_file = next((f for f in inc_candidates if os.path.isfile(f)),None)
        if inc_file:
            incentive_df=pd.read_csv(inc_file,on_bad_lines="skip",engine="python")
            incentive_df.columns=[c.strip().lower() for c in incentive_df.columns]
            bc=detect_col(incentive_df,["geographic_block","block","area","location"])
            if bc and bc!="geographic_block": incentive_df=incentive_df.rename(columns={bc:"geographic_block"})
            incentive_df["geographic_block"]=incentive_df["geographic_block"].str.strip()
            incentive_df["_lat"]=incentive_df["geographic_block"].map(lambda b: INCENTIVE_GEOCOORDS.get(b,(None,None))[0])
            incentive_df["_lon"]=incentive_df["geographic_block"].map(lambda b: INCENTIVE_GEOCOORDS.get(b,(None,None))[1])
        else: problems.append("cbe_incentive_clean.csv not found")
    except Exception as e: problems.append(f"Incentive: {e}")

    return (land, water, corridor, substations, sub_names, sub_full,
            rail_stations, rail_df, sidco, highway_junctions, highway_coords,
            icd_points, workforce_df, incentive_df, problems)


# ── HEADER ────────────────────────────────────────────────────────────────────────
st.title("CBE Industrial Intelligence Engine")
st.markdown('<p style="font-family:JetBrains Mono,monospace;font-size:0.72rem;color:#38bdf850;'
            'letter-spacing:2px;margin-top:-0.3rem;">'
            'LAND · INFRASTRUCTURE · ECOSYSTEM · WORKFORCE · INCENTIVES · INDUSTRY LOGIC · LIVE MAPS</p>',
            unsafe_allow_html=True)

with st.spinner("🔄 Loading all intelligence layers…"):
    (land, water, corridor, substations, sub_names, sub_full,
     rail_stations, rail_df, sidco, highway_junctions, highway_coords,
     icd_points, workforce_df, incentive_df, problems) = load_all()

if problems:
    with st.expander("⚠️ Data notices", expanded=False):
        for p in problems: st.caption(f"• {p}")

if land is None or land.empty:
    st.error("❌ Cannot load empty_land.csv."); st.stop()

# Load API key once
GMAPS_KEY = get_gmaps_key()


# ── SIDEBAR ───────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div style="font-family:Syne,sans-serif;font-weight:800;font-size:1.1rem;'
                'background:linear-gradient(90deg,#38bdf8,#818cf8);-webkit-background-clip:text;'
                '-webkit-text-fill-color:transparent;">⬡ CBE Engine</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-family:JetBrains Mono,monospace;font-size:0.6rem;color:#2a4060;'
                'letter-spacing:2px;margin-bottom:1rem;">INDUSTRIAL SITE INTELLIGENCE v4 · MAPS EDITION</div>', unsafe_allow_html=True)
    st.divider()

    st.markdown('<span class="sidebar-label">Industry Type</span>', unsafe_allow_html=True)
    industry = st.selectbox("", list(INDUSTRY_DNA.keys()),
                            format_func=lambda x: f"{INDUSTRY_DNA[x]['icon']}  {x}",
                            label_visibility="collapsed")
    dna = INDUSTRY_DNA[industry]
    st.markdown(f'<div style="font-family:JetBrains Mono,monospace;font-size:0.66rem;color:#38bdf870;'
                f'background:#060f1e;border:1px solid #0c2040;border-radius:8px;padding:0.5rem 0.8rem;'
                f'margin-top:0.4rem;line-height:1.6;">{dna["desc"]}</div>', unsafe_allow_html=True)

    st.divider()
    st.markdown('<span class="sidebar-label">Weight Profile</span>', unsafe_allow_html=True)
    weight_labels = {"Power ⚡":"Power","Airport ✈":"Airport","Water 💧":"Water",
                     "Ecosystem 🏭":"Ecosystem","Workforce 👷":"Workforce","Incentives 🏷️":"Incentive"}
    for label,key in weight_labels.items():
        val = dna["weights"].get(key,0); pct = int(val*100)
        st.markdown(
            f'<div style="display:flex;align-items:center;gap:8px;margin-bottom:5px;">'
            f'<div style="font-family:JetBrains Mono,monospace;font-size:0.6rem;color:#4a6080;width:100px;">{label}</div>'
            f'<div style="flex:1;background:#0b1526;border-radius:4px;height:5px;">'
            f'<div style="width:{pct}%;background:linear-gradient(90deg,#38bdf8,#818cf8);height:5px;border-radius:4px;"></div></div>'
            f'<div style="font-family:JetBrains Mono,monospace;font-size:0.6rem;color:#dde3f0;width:26px;text-align:right;">{pct}%</div>'
            f'</div>', unsafe_allow_html=True)

    st.divider()
    st.markdown('<span class="sidebar-label">Data Layers</span>', unsafe_allow_html=True)
    for name,count,ok in [
        ("Land Parcels",       f"{len(land)} parcels",                        True),
        ("Water Bodies",       f"{len(water) if water is not None else 0}",   water is not None and not water.empty),
        ("Corridor Companies", f"{len(corridor)} cos",                         not corridor.empty),
        ("Substations",        f"{len(substations)} nodes",                   True),
        ("Railway Stations",   f"{len(rail_stations)} stations",              len(rail_stations)>0),
        ("SIDCO Estates",      f"{len(sidco)} estates",                       not sidco.empty),
        ("Highway Junctions",  f"{len(highway_junctions)} junctions",         len(highway_junctions)>0),
        ("ICD / Dry Port",     f"{len(icd_points)} depot(s)",                 len(icd_points)>0),
        ("Workforce Zones",    f"{len(workforce_df)} areas",                  not workforce_df.empty),
        ("Incentive Blocks",   f"{len(incentive_df)} blocks",                 not incentive_df.empty),
        ("Google Maps API",    "Connected" if GMAPS_KEY else "No key set",    bool(GMAPS_KEY)),
    ]:
        dot = "🟢" if ok else "🔴"
        st.markdown(f'<div class="stat-row"><span class="stat-label">{dot} {name}</span>'
                    f'<span class="stat-val">{count}</span></div>', unsafe_allow_html=True)

    if not GMAPS_KEY:
        st.divider()
        st.markdown('<span class="sidebar-label">Google Maps Key</span>', unsafe_allow_html=True)
        st.caption("Set in `app.py` at the top:")
        st.code('GOOGLE_MAPS_API_KEY = "your-key-here"', language="python")


# ── SEARCH BAR ────────────────────────────────────────────────────────────────────
st.markdown('<div class="search-wrapper"><div class="search-title">🔍 Natural Language Site Search</div></div>',
            unsafe_allow_html=True)
query = st.text_input("", placeholder="e.g. 5km airport, substation 2km, water 500m, icd within 3km, railway 5km",
                      label_visibility="collapsed", key="main_search")
st.markdown('<div class="search-examples">Try: <span>5km airport</span> · <span>water 500m</span> · '
            '<span>substation 2km</span> · <span>icd within 3km</span> · '
            '<span>railway 5km</span> · <span>close to sidco</span></div>', unsafe_allow_html=True)

parsed = parse_query(query); constraints = parsed["constraints"]
if query.strip():
    if parsed["interpreted"]:
        pills = "".join(f'<span class="pill pill-info">✓ {i}</span>' for i in parsed["interpreted"])
        st.markdown(f'<div class="parse-box"><div class="parse-header">Search Interpreted As</div>'
                    f'<div class="pill-row">{pills}</div>'
                    f'<div class="parse-note">Applied as soft preferences — best match returned even if not fully met.</div>'
                    f'</div>', unsafe_allow_html=True)
    else:
        st.info("💬 Could not extract constraints. Try: **'5km airport, 2km power, water 500m'**")

st.divider()


# ── DISTANCES ─────────────────────────────────────────────────────────────────────
df = land.copy()
df["airport_dist"] = df.apply(lambda r: haversine(r["lat"],r["lon"],*AIRPORT), axis=1)
df["power_dist"]   = df.apply(lambda r: min_dist(r["lat"],r["lon"],substations), axis=1)
df["rail_dist"]    = df.apply(lambda r: min_dist(r["lat"],r["lon"],rail_stations), axis=1) if rail_stations else np.nan
df["water_dist"]   = df.apply(lambda r: min_dist(r["lat"],r["lon"],list(zip(water["latitude"],water["longitude"]))), axis=1) \
                     if water is not None and not water.empty else np.nan
df["sidco_dist"]   = df.apply(lambda r: min_dist(r["lat"],r["lon"],list(zip(sidco["latitude"],sidco["longitude"]))), axis=1) \
                     if not sidco.empty else np.nan
df["highway_dist"] = df.apply(lambda r: min_dist(r["lat"],r["lon"],highway_coords), axis=1) if highway_coords else np.nan
df["icd_dist"]     = df.apply(lambda r: min_dist(r["lat"],r["lon"],[(p[0],p[1]) for p in icd_points]), axis=1) if icd_points else np.nan

for col,default in [("water_dist",8.0),("rail_dist",12.0),("sidco_dist",15.0),("highway_dist",10.0),("icd_dist",20.0)]:
    df[col] = df[col].fillna(df[col].mean() if df[col].notna().any() else default)


# ── WORKFORCE SCORING ─────────────────────────────────────────────────────────────
def get_workforce_score(row):
    if workforce_df.empty: return 0.5, "No workforce data", 0.5
    area = str(row.get("area","")).strip().lower()
    match = workforce_df[workforce_df["area_name"].str.lower()==area]
    if match.empty:
        match = workforce_df[workforce_df["area_name"].str.lower().str.contains(area[:5],na=False)]
    if match.empty: match = workforce_df.head(1)
    wrow = match.iloc[0]
    density_raw = str(wrow.get("worker_density","medium")).lower()
    density_score = next((v for k,v in DENSITY_SCORE.items() if k in density_raw), 0.5)
    workforce_cat = str(wrow.get("primary_workforce_category",""))
    fit_score = 1.0 if any(cat.lower() in workforce_cat.lower() for cat in dna.get("workforce_match",[])) else 0.4
    spatial_weight = float(wrow.get("spatial_weight_index",0.7))
    cluster_type = str(wrow.get("industrial_cluster_type","General"))
    combined = density_score*0.35 + fit_score*0.40 + spatial_weight*0.25
    return combined, f"{workforce_cat} · {cluster_type}", spatial_weight

df["workforce_score"],df["workforce_label"],df["spatial_weight"] = zip(*df.apply(get_workforce_score, axis=1))


# ── INCENTIVE SCORING ─────────────────────────────────────────────────────────────
def get_incentive_info(row):
    if incentive_df.empty: return 0.5, "No incentive data", "Standard", ""
    best_dist,best_row = float("inf"),None
    for _,irow in incentive_df.iterrows():
        ilat,ilon = irow.get("_lat"),irow.get("_lon")
        if pd.isna(ilat) or pd.isna(ilon): continue
        d = haversine(row["lat"],row["lon"],float(ilat),float(ilon))
        if d < best_dist: best_dist,best_row = d,irow
    if best_row is None: return 0.5,"No nearby block","Standard",""
    tier  = str(best_row.get("incentive_tier","Standard")).strip()
    block = str(best_row.get("geographic_block","")).strip()
    scheme = str(best_row.get("scheme","")).strip()
    subsidies = str(best_row.get("top_subsidies","")).strip()
    anchor = str(best_row.get("infrastructure_anchor","")).strip()
    tier_score = INCENTIVE_TIER_SCORE.get(tier.lower(),0.6)
    proximity_factor = max(0.3, 1.0-(best_dist/30.0))
    score = tier_score * proximity_factor
    label = f"{block} ({tier}) · {scheme}"
    detail = f"{subsidies} | Anchor: {anchor}"
    return score, label, tier, detail

df["incentive_score"],df["incentive_label"],df["incentive_tier"],df["incentive_detail"] = zip(
    *df.apply(get_incentive_info, axis=1))


# ── ECOSYSTEM ─────────────────────────────────────────────────────────────────────
keywords = dna["keywords"]
def ecosystem_score(row):
    score = 0
    if not corridor.empty:
        nearby = corridor[(np.abs(corridor["latitude"]-row["lat"])<0.045) &
                          (np.abs(corridor["longitude"]-row["lon"])<0.045)]
        if not nearby.empty:
            if industry=="Logistics & Warehouse":
                score += int(np.log1p(len(nearby))*6)
            elif keywords:
                hits = nearby["industry"].str.lower().str.contains("|".join(keywords),na=False,regex=True).sum()
                score += int(hits*2) + int(np.log1p(len(nearby)))
            else:
                score += int(np.log1p(len(nearby))*4)
    if not sidco.empty:
        score += len(sidco[(np.abs(sidco["latitude"]-row["lat"])<0.03)&
                            (np.abs(sidco["longitude"]-row["lon"])<0.03)])*4
    if highway_junctions and 10.8<row["lat"]<11.3 and 76.8<row["lon"]<77.4: score+=1
    if icd_points and industry=="Logistics & Warehouse":
        icd_d = min_dist(row["lat"],row["lon"],[(p[0],p[1]) for p in icd_points])
        score += 5 if icd_d<5 else 2 if icd_d<10 else 0
    return score

df["ecosystem"] = df.apply(ecosystem_score, axis=1)


# ── SCORING ───────────────────────────────────────────────────────────────────────
weights = dna["weights"]
df["n_power"]     = normalize(df["power_dist"])
df["n_airport"]   = normalize(df["airport_dist"])
df["n_water"]     = normalize(df["water_dist"])
df["n_eco"]       = normalize(df["ecosystem"])
df["n_rail"]      = normalize(df["rail_dist"])
df["n_sidco"]     = normalize(df["sidco_dist"])
df["n_highway"]   = normalize(df["highway_dist"])
df["n_icd"]       = normalize(df["icd_dist"])
df["n_workforce"] = normalize(df["workforce_score"])
df["n_incentive"] = normalize(df["incentive_score"])

df["base_score"] = (
    weights["Power"]               * df["n_power"]               +
    weights["Airport"]             * df["n_airport"]             +
    weights["Water"]               * df["n_water"]               -
    weights["Ecosystem"]           * df["n_eco"]                 +
    weights.get("Workforce",0.10)  * (1-df["n_workforce"])       +
    weights.get("Incentive",0.08)  * (1-df["n_incentive"])       +
    0.04 * df["n_rail"]   +
    0.03 * df["n_sidco"]  +
    0.03 * df["n_highway"]+
    0.02 * df["n_icd"]
)

df["search_penalty"] = df.apply(lambda r: constraint_penalty(r,constraints), axis=1) if constraints else 0.0
df["final_score"] = df["base_score"] + df["search_penalty"]
df = df.sort_values("final_score").reset_index(drop=True)

area_col   = detect_col(df,["area","location","name","place","parcel_name"]) or df.columns[0]
survey_col = detect_col(df,["survey_no","survey","parcel_id","id","plot_no"]) or df.columns[1]
top = df.head(min(3,len(df))).copy()
winner = df.iloc[0]


# ── WINNER CARD ───────────────────────────────────────────────────────────────────
score_pct = max(0,min(100,int((1-winner["final_score"])*100)))
st.markdown(f"""
<div class="winner-card">
  <div class="winner-eyebrow">Top Recommended Site · {dna['icon']} {industry}</div>
  <div class="winner-name">{winner[area_col]}</div>
  <div class="winner-meta">Survey No. {winner[survey_col]}
    <span class="winner-score">Suitability Score {score_pct}/100</span>
  </div>
</div>""", unsafe_allow_html=True)

def dist_cls(v,t1,t2): return ("g" if v<t1 else "y" if v<t2 else "r"), ("🟢 Excellent" if v<t1 else "🟡 Good" if v<t2 else "🟠 Moderate")
a_cls,a_lbl = dist_cls(winner["airport_dist"],10,20)
p_cls,p_lbl = dist_cls(winner["power_dist"],3,7)
w_cls,w_lbl = dist_cls(winner["water_dist"],1,5)
r_cls,r_lbl = dist_cls(winner["rail_dist"],5,12)
h_cls,h_lbl = dist_cls(winner["highway_dist"],3,10)
i_cls,i_lbl = dist_cls(winner["icd_dist"],5,15)
eco_cls = "g" if winner["ecosystem"]>=5 else "y" if winner["ecosystem"]>=2 else "r"
eco_lbl = "🟢 Strong" if winner["ecosystem"]>=5 else "🟡 Emerging" if winner["ecosystem"]>=2 else "⚪ Greenfield"

st.markdown(f"""
<div class="metric-grid">
  <div class="metric-card"><div class="metric-icon">✈️</div><div class="metric-label">Airport</div>
    <div class="metric-value">{winner['airport_dist']:.1f}</div><div class="metric-unit">km</div>
    <div class="metric-status-{a_cls}">{a_lbl}</div></div>
  <div class="metric-card"><div class="metric-icon">⚡</div><div class="metric-label">Substation</div>
    <div class="metric-value">{winner['power_dist']:.1f}</div><div class="metric-unit">km</div>
    <div class="metric-status-{p_cls}">{p_lbl}</div></div>
  <div class="metric-card"><div class="metric-icon">💧</div><div class="metric-label">Water</div>
    <div class="metric-value">{winner['water_dist']:.1f}</div><div class="metric-unit">km</div>
    <div class="metric-status-{w_cls}">{w_lbl}</div></div>
  <div class="metric-card"><div class="metric-icon">🚂</div><div class="metric-label">Railway</div>
    <div class="metric-value">{winner['rail_dist']:.1f}</div><div class="metric-unit">km</div>
    <div class="metric-status-{r_cls}">{r_lbl}</div></div>
  <div class="metric-card"><div class="metric-icon">🛣️</div><div class="metric-label">Highway</div>
    <div class="metric-value">{winner['highway_dist']:.1f}</div><div class="metric-unit">km</div>
    <div class="metric-status-{h_cls}">{h_lbl}</div></div>
  <div class="metric-card"><div class="metric-icon">🚢</div><div class="metric-label">ICD Port</div>
    <div class="metric-value">{winner['icd_dist']:.1f}</div><div class="metric-unit">km</div>
    <div class="metric-status-{i_cls}">{i_lbl}</div></div>
  <div class="metric-card"><div class="metric-icon">🏭</div><div class="metric-label">Ecosystem</div>
    <div class="metric-value">{int(winner['ecosystem'])}</div><div class="metric-unit">cluster pts</div>
    <div class="metric-status-{eco_cls}">{eco_lbl}</div></div>
</div>""", unsafe_allow_html=True)

if constraints:
    comp=check_compliance(winner,constraints); all_ok=all(v["ok"] for v in comp.values())
    pills="".join(f'<span class="pill {"pill-ok" if v["ok"] else "pill-warn"}">{"✔" if v["ok"] else "✘"} '
                  f'{dim.title()}: {v["actual"]:.2f}km {"≤" if v["ok"] else ">"} {v["limit"]}km</span>'
                  for dim,v in comp.items())
    st.markdown(f'<div style="margin:0.8rem 0"><div class="pill-row">{pills}</div>'
                f'<div style="font-family:JetBrains Mono,monospace;font-size:0.68rem;color:#4a6080;margin-top:4px;">'
                f'{"✅ Meets all constraints" if all_ok else "🔶 Best available — some constraints relaxed"}'
                f'</div></div>', unsafe_allow_html=True)

st.divider()


# ── WHY THIS SITE + TOP 3 ─────────────────────────────────────────────────────────
col_left,col_right = st.columns([1.1,1],gap="large")

with col_left:
    st.markdown('<div class="section-header"><span class="section-icon">🧠</span>'
                '<span class="section-title">Why This Site?</span><div class="section-line"></div></div>',
                unsafe_allow_html=True)

    sub_dists = [(haversine(winner["lat"],winner["lon"],s[0],s[1]),s[2]) for s in sub_full]
    nearest_sub = min(sub_dists,key=lambda x:x[0])[1] if sub_full else "Substation"

    factor_scores = {
        "Power proximity":      weights["Power"]                *(1-winner["n_power"]),
        "Airport access":       weights["Airport"]              *(1-winner["n_airport"]),
        "Water proximity":      weights["Water"]                *(1-winner["n_water"]),
        "Ecosystem cluster":    weights["Ecosystem"]            *winner["n_eco"],
        "Workforce quality":    weights.get("Workforce",0.10)   *winner["n_workforce"],
        "Incentive advantage":  weights.get("Incentive",0.08)   *winner["n_incentive"],
    }
    dominant = max(factor_scores,key=factor_scores.get)

    def dc(v,t1,t2): return "dot-green" if v<t1 else "dot-yellow" if v<t2 else "dot-orange"
    def tc(v,t1,t2): return "rtag-g" if v<t1 else "rtag-y" if v<t2 else "rtag-o"
    def ds(v,t1,t2): return "Excellent" if v<t1 else "Good" if v<t2 else "Moderate"

    pwr_val=winner["power_dist"]; air_val=winner["airport_dist"]; wat_val=winner["water_dist"]
    ral_val=winner["rail_dist"]; sdc_val=winner["sidco_dist"]; hwy_val=winner["highway_dist"]
    icd_val=winner["icd_dist"]; eco_val=int(winner["ecosystem"])
    wf_score=winner["workforce_score"]; wf_lbl=winner["workforce_label"]
    inc_lbl=winner["incentive_label"]; inc_det=winner["incentive_detail"]; inc_tier=winner["incentive_tier"]
    kw_str=", ".join(keywords[:5]) if keywords else "Industrial density"
    hwy_str=", ".join(highway_junctions[:3]) if highway_junctions else "Not loaded"
    icd_note=f"ICD Irugur {icd_val:.1f}km — {'direct dry port access' if icd_val<5 else 'customs hub nearby'}"

    st.markdown(f"""
<div class="reasoning-card">
  <div style="font-family:JetBrains Mono,monospace;font-size:0.72rem;color:#38bdf8;margin-bottom:1rem;">
    Primary advantage: <strong style="color:#fff;">{dominant}</strong>
  </div>

  <div class="reasoning-section">Infrastructure Snapshot</div>
  <div class="reasoning-row"><div class="reasoning-dot {dc(pwr_val,3,7)}"></div>
    <span>Power substation</span>&nbsp;<span class="rval">{pwr_val:.2f} km</span>&nbsp;
    <span class="{tc(pwr_val,3,7)}">({nearest_sub})</span></div>
  <div class="reasoning-row"><div class="reasoning-dot {dc(air_val,10,20)}"></div>
    <span>Airport</span>&nbsp;<span class="rval">{air_val:.2f} km</span>&nbsp;
    <span class="{tc(air_val,10,20)}">{ds(air_val,10,20)}</span></div>
  <div class="reasoning-row"><div class="reasoning-dot {dc(wat_val,1,5)}"></div>
    <span>Water body</span>&nbsp;<span class="rval">{wat_val:.2f} km</span>&nbsp;
    <span class="{tc(wat_val,1,5)}">{ds(wat_val,1,5)}</span></div>
  <div class="reasoning-row"><div class="reasoning-dot {dc(ral_val,5,12)}"></div>
    <span>Railway</span>&nbsp;<span class="rval">{ral_val:.2f} km</span>&nbsp;
    <span class="{tc(ral_val,5,12)}">{ds(ral_val,5,12)}</span></div>
  <div class="reasoning-row"><div class="reasoning-dot {dc(hwy_val,3,10)}"></div>
    <span>Highway junction</span>&nbsp;<span class="rval">{hwy_val:.2f} km</span>&nbsp;
    <span style="font-size:0.7rem;color:#4a6080;">{hwy_str}</span></div>
  <div class="reasoning-row"><div class="reasoning-dot {'dot-green' if icd_val<5 else 'dot-yellow' if icd_val<15 else 'dot-orange'}"></div>
    <span>ICD / Dry Port</span>&nbsp;<span class="rval">{icd_note}</span></div>
  <div class="reasoning-row"><div class="reasoning-dot dot-green"></div>
    <span>SIDCO estate</span>&nbsp;<span class="rval">{sdc_val:.1f} km{'  — zone ready' if sdc_val<8 else ''}</span></div>

  <div class="reasoning-section">Workforce Intelligence</div>
  <div class="reasoning-row"><div class="reasoning-dot {'dot-green' if wf_score>0.75 else 'dot-yellow' if wf_score>0.55 else 'dot-orange'}"></div>
    <span>Profile</span>&nbsp;<span class="rval" style="font-size:0.7rem;">{wf_lbl}</span></div>
  <div class="reasoning-row"><div class="reasoning-dot dot-green"></div>
    <span>Fit score</span>&nbsp;<span class="rval">{wf_score:.2f} / 1.00</span></div>

  <div class="reasoning-section">Incentive Zone</div>
  <div class="reasoning-row"><div class="reasoning-dot {'dot-green' if inc_tier.lower()=='backward' else 'dot-yellow'}"></div>
    <span>Block</span>&nbsp;<span class="rval" style="font-size:0.7rem;">{inc_lbl}</span></div>
  <div class="reasoning-row"><div class="reasoning-dot dot-green"></div>
    <span>Subsidies</span>&nbsp;<span class="rval" style="font-size:0.7rem;">{inc_det[:90]}{'…' if len(inc_det)>90 else ''}</span></div>

  <div class="reasoning-section">Ecosystem Intelligence</div>
  <div class="reasoning-row"><div class="reasoning-dot {'dot-green' if eco_val>=5 else 'dot-yellow' if eco_val>=2 else 'dot-orange'}"></div>
    <span>Cluster strength</span>&nbsp;<span class="rval">{'Strong' if eco_val>=5 else 'Emerging' if eco_val>=2 else 'Greenfield'} ({eco_val} pts)</span></div>
  <div class="reasoning-row"><div class="reasoning-dot dot-green"></div>
    <span>Keywords</span>&nbsp;<span class="rval" style="font-size:0.7rem;">{kw_str}</span></div>

  <div class="reasoning-section">Scoring Logic</div>
  <div class="reasoning-row"><div class="reasoning-dot dot-green"></div>
    <span>Weights</span>&nbsp;
    <span class="rval" style="font-size:0.68rem;">
      Pwr {int(weights['Power']*100)}% · Air {int(weights['Airport']*100)}% ·
      H₂O {int(weights['Water']*100)}% · Eco {int(weights['Ecosystem']*100)}% ·
      WF {int(weights.get('Workforce',0)*100)}% · Inc {int(weights.get('Incentive',0)*100)}%
    </span></div>
  <div class="reasoning-row"><div class="reasoning-dot dot-green"></div>
    <span>Final score</span>&nbsp;<span class="rval">{winner['final_score']:.4f}</span>
    <span style="color:#4a6080;font-size:0.68rem;"> (lower = better)</span></div>
</div>""", unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="section-header"><span class="section-icon">🏆</span>'
                '<span class="section-title">Top 3 Ranked Parcels</span><div class="section-line"></div></div>',
                unsafe_allow_html=True)

    for i,row in top.iterrows():
        rank=i+1; rank_cls="rank-1" if rank==1 else ""
        if constraints:
            comp=check_compliance(row,constraints); meets=all(v["ok"] for v in comp.values())
            tag='<span class="pill pill-ok" style="font-size:0.58rem;">✓ All met</span>' if meets else \
                '<span class="pill pill-warn" style="font-size:0.58rem;">~ Best fit</span>'
        else: tag=""
        r_score=max(0,min(100,int((1-row["final_score"])*100)))
        wf_pct=int(row["workforce_score"]*100)
        inc_short="Backward" if row["incentive_tier"].lower()=="backward" else "Standard"
        st.markdown(f"""
<div class="rank-card {rank_cls}">
  <div class="rank-number">#{rank}</div>
  <div class="rank-info">
    <div class="rank-name">{row[area_col]}</div>
    <div class="rank-survey">Survey {row[survey_col]} · Score {r_score}/100 {tag}</div>
    <div class="rank-badges">
      <span class="badge b-eco">🏭 {int(row['ecosystem'])}pts</span>
      <span class="badge b-pwr">⚡ {row['power_dist']:.1f}km</span>
      <span class="badge b-air">✈ {row['airport_dist']:.1f}km</span>
      <span class="badge b-rail">🚂 {row['rail_dist']:.1f}km</span>
      <span class="badge b-water">💧 {row['water_dist']:.1f}km</span>
      <span class="badge b-hwy">🛣️ {row['highway_dist']:.1f}km</span>
      <span class="badge b-icd">🚢 {row['icd_dist']:.1f}km</span>
      <span class="badge b-wf">👷 {wf_pct}%</span>
      <span class="badge b-inc">🏷️ {inc_short}</span>
    </div>
  </div>
</div>""", unsafe_allow_html=True)

st.divider()


# ═══════════════════════════════════════════════════════════════════════════════
# ── GOOGLE MAPS INTELLIGENCE SECTION ──────────────────────────────────────────
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-header"><span class="section-icon">🛰️</span>'
            '<span class="section-title">Google Maps Intelligence</span><div class="section-line"></div></div>',
            unsafe_allow_html=True)

gmaps_tab1, gmaps_tab2, gmaps_tab3 = st.tabs([
    "📍 Live Ecosystem Scan",
    "🚗 Real Drive Times",
    "🔍 Reverse Location Analysis",
])

with gmaps_tab1:
    st.markdown(
        '<div style="font-family:JetBrains Mono,monospace;font-size:0.68rem;color:#4a6080;margin-bottom:1rem;">'
        'Scans Google Places API in real time to find what businesses are actually operating near the top-ranked site. '
        'Upgrades your static ecosystem score with live data.</div>',
        unsafe_allow_html=True
    )

    # Parcel selector
    parcel_names = df[area_col].tolist()
    selected_parcel = st.selectbox(
        "Select parcel to scan",
        parcel_names,
        index=0,
        key="eco_scan_parcel",
        help="Defaults to the top-ranked parcel"
    )
    scan_row = df[df[area_col] == selected_parcel].iloc[0]
    scan_lat, scan_lon = scan_row["lat"], scan_row["lon"]

    st.caption(f"📌 Coordinates: {scan_lat:.5f}, {scan_lon:.5f}")

    if st.button("🛰️ Run Live Ecosystem Scan", key="eco_scan_btn"):
        render_ecosystem_scan(scan_lat, scan_lon, industry, GMAPS_KEY)

with gmaps_tab2:
    st.markdown(
        '<div style="font-family:JetBrains Mono,monospace;font-size:0.68rem;color:#4a6080;margin-bottom:1rem;">'
        'Replaces straight-line (haversine) distances with real road travel times to key infrastructure. '
        'A site 4km as the crow flies could be 25 min by road — this tells you the truth.</div>',
        unsafe_allow_html=True
    )

    dt_parcel = st.selectbox(
        "Select parcel for drive times",
        parcel_names,
        index=0,
        key="dt_parcel",
    )
    dt_row = df[df[area_col] == dt_parcel].iloc[0]
    dt_lat, dt_lon = dt_row["lat"], dt_row["lon"]
    st.caption(f"📌 Coordinates: {dt_lat:.5f}, {dt_lon:.5f}")

    if st.button("🚗 Get Real Drive Times", key="dt_btn"):
        render_drive_times(dt_lat, dt_lon, GMAPS_KEY, substations, icd_points, highway_coords, highway_junctions)

with gmaps_tab3:
    st.markdown(
        '<div style="font-family:JetBrains Mono,monospace;font-size:0.68rem;color:#4a6080;margin-bottom:1rem;">'
        'Select any ranked parcel below — the engine will automatically use its coordinates to reverse-engineer '
        'why that location was chosen, using <strong style="color:#38bdf8;">industry-specific reasoning</strong> '
        f'tuned for <strong style="color:#818cf8;">{industry}</strong>.</div>',
        unsafe_allow_html=True
    )

    rev_mode = st.radio(
        "Analysis mode",
        ["📋 Use a ranked parcel (auto coordinates)", "📍 Enter coordinates manually"],
        key="rev_mode",
        horizontal=True,
        label_visibility="collapsed"
    )

    if rev_mode.startswith("📋"):
        rev_parcel = st.selectbox(
            "Select parcel to analyse",
            parcel_names,
            index=0,
            key="rev_parcel_select",
            help="Coordinates are pulled automatically from the dataset"
        )
        rev_row = df[df[area_col] == rev_parcel].iloc[0]
        st.caption(f"📌 Coordinates locked: {rev_row['lat']:.5f}, {rev_row['lon']:.5f}")
        render_reverse_analysis(GMAPS_KEY, company_row=rev_row, selected_industry=industry)
    else:
        render_reverse_analysis(GMAPS_KEY, company_row=None, selected_industry=industry)

st.divider()


# ── MAP ───────────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-header"><span class="section-icon">🗺️</span>'
            '<span class="section-title">Site Intelligence Map</span><div class="section-line"></div></div>',
            unsafe_allow_html=True)

land_map_rows=[]
for idx,row in df.iterrows():
    if idx==0:   color,radius,lp=[255,60,80,255],520,"🥇 #1 WINNER"
    elif idx==1: color,radius,lp=[255,160,20,240],380,"🥈 #2"
    elif idx==2: color,radius,lp=[160,80,255,220],300,"🥉 #3"
    else:        color,radius,lp=[40,100,200,130],180,f"#{idx+1}"
    label=(f"{lp}: {row[area_col]} | Pwr:{row['power_dist']:.1f}km Air:{row['airport_dist']:.1f}km "
           f"H₂O:{row['water_dist']:.1f}km Rail:{row['rail_dist']:.1f}km "
           f"Hwy:{row['highway_dist']:.1f}km ICD:{row['icd_dist']:.1f}km WF:{int(row['workforce_score']*100)}%")
    land_map_rows.append({"lat":row["lat"],"lon":row["lon"],"color":color,"radius":radius,"label":label})

map_land_df = pd.DataFrame(land_map_rows)
layers=[pdk.Layer("ScatterplotLayer",data=map_land_df,get_position="[lon,lat]",get_color="color",
                  get_radius="radius",pickable=True,auto_highlight=True,highlight_color=[255,255,255,80])]

# Glow ring
layers.insert(0,pdk.Layer("ScatterplotLayer",
    data=pd.DataFrame([{"lat":df.iloc[0]["lat"],"lon":df.iloc[0]["lon"],"color":[255,60,80,50],"radius":900,"label":""}]),
    get_position="[lon,lat]",get_color="color",get_radius="radius",pickable=False))

# Substations
layers.append(pdk.Layer("ScatterplotLayer",
    data=pd.DataFrame([{"lat":s[0],"lon":s[1],"label":f"⚡ {n}","color":[255,200,0,200],"radius":220}
                        for s,n in zip(substations,sub_names)]),
    get_position="[lon,lat]",get_color="color",get_radius="radius",pickable=True))

# Railway
if not rail_df.empty and "_lat" in rail_df.columns:
    rm=rail_df[["_lat","_lon","station_name"]].copy(); rm.columns=["lat","lon","label"]
    rm["label"]="🚂 "+rm["label"]; rm["color"]=[[0,220,140,220]]*len(rm); rm["radius"]=250
    layers.append(pdk.Layer("ScatterplotLayer",data=rm,get_position="[lon,lat]",get_color="color",get_radius="radius",pickable=True))

# SIDCO
if not sidco.empty:
    sm=sidco[["latitude","longitude","name"]].copy(); sm.columns=["lat","lon","label"]
    sm["label"]="🏭 "+sm["label"]; sm["color"]=[[0,200,255,200]]*len(sm); sm["radius"]=320
    layers.append(pdk.Layer("ScatterplotLayer",data=sm,get_position="[lon,lat]",get_color="color",get_radius="radius",pickable=True))

# Water
if water is not None and not water.empty:
    wm=water[["latitude","longitude"]].copy(); wm.columns=["lat","lon"]
    wnc=detect_col(water,["name","wkt"]); wm["label"]=("💧 "+water[wnc]).values if wnc else "💧 Water Body"
    wm["color"]=[[20,180,230,140]]*len(wm); wm["radius"]=180
    layers.append(pdk.Layer("ScatterplotLayer",data=wm,get_position="[lon,lat]",get_color="color",get_radius="radius",pickable=True))

# ICD
if icd_points:
    icd_map=pd.DataFrame([{"lat":p[0],"lon":p[1],"label":f"🚢 {p[2]} — Inland Container Depot",
                            "color":[80,255,140,240],"radius":420} for p in icd_points])
    layers.append(pdk.Layer("ScatterplotLayer",data=icd_map,get_position="[lon,lat]",get_color="color",get_radius="radius",pickable=True))

# Highway junctions
if highway_coords:
    hm=pd.DataFrame([{"lat":c[0],"lon":c[1],
                       "label":f"🛣️ {highway_junctions[i] if i<len(highway_junctions) else 'Junction'}",
                       "color":[255,140,0,200],"radius":220} for i,c in enumerate(highway_coords)])
    layers.append(pdk.Layer("ScatterplotLayer",data=hm,get_position="[lon,lat]",get_color="color",get_radius="radius",pickable=True))

# ── Live Places layer (from ecosystem scan if run) ────────────────────────────
if "live_places_df" in st.session_state and not st.session_state["live_places_df"].empty:
    layers.append(pdk.Layer("ScatterplotLayer",
        data=st.session_state["live_places_df"],
        get_position="[lon,lat]",get_color="color",get_radius="radius",pickable=True))

tooltip={"html":'<div style="font-family:JetBrains Mono,monospace;font-size:11px;background:#0b1526;'
                'color:#dde3f0;border:1px solid #1e4080;border-radius:8px;padding:10px 14px;'
                'max-width:380px;line-height:1.7;">{label}</div>',
         "style":{"backgroundColor":"transparent","border":"none"}}

st.pydeck_chart(pdk.Deck(layers=layers,
    initial_view_state=pdk.ViewState(latitude=df["lat"].mean(),longitude=df["lon"].mean(),zoom=11,pitch=40),
    tooltip=tooltip, map_style="https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json"))

st.markdown("""
<div class="map-legend">
  <div class="legend-item"><div class="legend-dot" style="background:#ff3c50;box-shadow:0 0 8px #ff3c50;"></div>#1 Winner</div>
  <div class="legend-item"><div class="legend-dot" style="background:#ffa014;"></div>#2 Site</div>
  <div class="legend-item"><div class="legend-dot" style="background:#a050ff;"></div>#3 Site</div>
  <div class="legend-item"><div class="legend-dot" style="background:#2864c8;opacity:0.6;"></div>Other Parcels</div>
  <div class="legend-item"><div class="legend-dot" style="background:#ffc800;"></div>Substations</div>
  <div class="legend-item"><div class="legend-dot" style="background:#00dc8c;"></div>Railway Stations</div>
  <div class="legend-item"><div class="legend-dot" style="background:#00c8ff;"></div>SIDCO Estates</div>
  <div class="legend-item"><div class="legend-dot" style="background:#14b4e6;opacity:0.7;"></div>Water Bodies</div>
  <div class="legend-item"><div class="legend-dot" style="background:#50ff8c;"></div>ICD Dry Port</div>
  <div class="legend-item"><div class="legend-dot" style="background:#ff8c00;"></div>Highway Junctions</div>
  <div class="legend-item"><div class="legend-dot" style="background:#ffd700;"></div>Live Places (Maps)</div>
</div>
<div style="font-family:JetBrains Mono,monospace;font-size:0.65rem;color:#2a4060;margin-top:0.5rem;">
  Hover any marker · Winner has glow ring · 11 intelligence layers active · Google Maps live layer when scanned
</div>""", unsafe_allow_html=True)

st.divider()


# ── FULL TABLE ────────────────────────────────────────────────────────────────────
with st.expander("📋 Full Ranked Data Table (All Parcels)"):
    dcols=[area_col,survey_col,"airport_dist","power_dist","water_dist","rail_dist",
           "highway_dist","icd_dist","sidco_dist","ecosystem","workforce_score","incentive_score","final_score"]
    dcols=[c for c in dcols if c in df.columns]
    display_df=df[dcols].copy(); display_df.insert(0,"rank",range(1,len(display_df)+1))
    rename_map={"rank":"Rank",area_col:"Area",survey_col:"Survey No.",
                "airport_dist":"Airport (km)","power_dist":"Power (km)","water_dist":"Water (km)",
                "rail_dist":"Railway (km)","highway_dist":"Highway (km)","icd_dist":"ICD (km)",
                "sidco_dist":"SIDCO (km)","ecosystem":"Ecosystem","workforce_score":"Workforce",
                "incentive_score":"Incentive","final_score":"Score ↓"}
    fmt_map={"Airport (km)":"{:.2f}","Power (km)":"{:.2f}","Water (km)":"{:.2f}","Railway (km)":"{:.2f}",
             "Highway (km)":"{:.2f}","ICD (km)":"{:.2f}","SIDCO (km)":"{:.2f}","Ecosystem":"{:.0f}",
             "Workforce":"{:.2f}","Incentive":"{:.2f}","Score ↓":"{:.4f}"}
    st.dataframe(display_df.rename(columns=rename_map).style.format(fmt_map),
                 use_container_width=True, hide_index=True)

st.markdown("""
<div style="text-align:center;margin-top:2rem;padding:1rem;font-family:JetBrains Mono,monospace;
font-size:0.62rem;color:#1a2840;letter-spacing:2px;">
CBE INDUSTRIAL INTELLIGENCE ENGINE v4 · 11 DATA LAYERS · GOOGLE MAPS EDITION ·
LAND × INFRASTRUCTURE × ECOSYSTEM × WORKFORCE × INCENTIVES × ICD × INDUSTRY LOGIC × LIVE PLACES × DRIVE TIMES
</div>""", unsafe_allow_html=True)
