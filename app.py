import streamlit as st
import pandas as pd
import numpy as np
import re
import os
import pydeck as pdk

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
</style>
""", unsafe_allow_html=True)

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
        "icon": "⚙️", "desc": "Power reliability, engineering cluster, skilled workforce"
    },
    "Food Processing": {
        "weights": {"Power":0.08,"Airport":0.07,"Water":0.35,"Ecosystem":0.25,"Workforce":0.15,"Incentive":0.10},
        "keywords": ["food","agro","dairy","grain","mill","spice","rice","flour","packaging","beverage"],
        "workforce_match": ["Unskilled (Agro-processing)","Unskilled / Semi-Skilled"],
        "icon": "🌾", "desc": "Water proximity critical; agro workforce and cluster valued"
    },
    "Logistics & Warehouse": {
        "weights": {"Power":0.07,"Airport":0.28,"Water":0.05,"Ecosystem":0.20,"Workforce":0.12,"Incentive":0.08},
        "keywords": [],
        "workforce_match": ["Unskilled (Logistics)","Mixed (Commuter)"],
        "icon": "📦", "desc": "Airport, ICD dry port, highway connectivity are primary"
    },
    "Textile / Garments": {
        "weights": {"Power":0.20,"Airport":0.08,"Water":0.15,"Ecosystem":0.30,"Workforce":0.17,"Incentive":0.10},
        "keywords": ["textile","yarn","weav","garment","spinning","knit","dyeing","bleach","apparel","cotton"],
        "workforce_match": ["Semi-Skilled (Textile)","Unskilled / Semi-Skilled"],
        "icon": "🧵", "desc": "Textile cluster, water for dyeing, garment workforce"
    },
    "Electronics / EV": {
        "weights": {"Power":0.25,"Airport":0.28,"Water":0.07,"Ecosystem":0.15,"Workforce":0.15,"Incentive":0.10},
        "keywords": ["electronics","auto","ev","electric","battery","semicon","pcb","motor","component","tech"],
        "workforce_match": ["Skilled (Digital)","Mixed (Manufacturing)","Skilled Professionals"],
        "icon": "⚡", "desc": "Airport for exports, reliable power, tech-skilled workforce"
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

    # Highway junctions — first token before comma is the name
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
            'LAND · INFRASTRUCTURE · ECOSYSTEM · WORKFORCE · INCENTIVES · INDUSTRY LOGIC</p>',
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


# ── SIDEBAR ───────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div style="font-family:Syne,sans-serif;font-weight:800;font-size:1.1rem;'
                'background:linear-gradient(90deg,#38bdf8,#818cf8);-webkit-background-clip:text;'
                '-webkit-text-fill-color:transparent;">⬡ CBE Engine</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-family:JetBrains Mono,monospace;font-size:0.6rem;color:#2a4060;'
                'letter-spacing:2px;margin-bottom:1rem;">INDUSTRIAL SITE INTELLIGENCE v3</div>', unsafe_allow_html=True)
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
    ]:
        dot = "🟢" if ok else "🔴"
        st.markdown(f'<div class="stat-row"><span class="stat-label">{dot} {name}</span>'
                    f'<span class="stat-val">{count}</span></div>', unsafe_allow_html=True)


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
</div>
<div style="font-family:JetBrains Mono,monospace;font-size:0.65rem;color:#2a4060;margin-top:0.5rem;">
  Hover any marker · Winner has glow ring · 10 intelligence layers active
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
CBE INDUSTRIAL INTELLIGENCE ENGINE v3 · 10 DATA LAYERS ·
LAND × INFRASTRUCTURE × ECOSYSTEM × WORKFORCE × INCENTIVES × ICD × INDUSTRY LOGIC
</div>""", unsafe_allow_html=True)