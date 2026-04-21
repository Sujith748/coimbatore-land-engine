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
/* ═══════════════════════════════════════════════════════════════════
   LANDS & LANDS · INDUSTRIAL INTELLIGENCE ENGINE
   Brand palette: Deep Navy (#080d1a) · Gold (#c9a84c) · Copper (#a07840)
   White (#f0ece4) · Muted gold text (#7a6a40)
   ═══════════════════════════════════════════════════════════════════ */
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

/* ── BRAND TOKENS ─────────────────────────────────────────────── */
:root {
  --gold:       #c9a84c;
  --gold-light: #e2c97a;
  --gold-dim:   #7a6030;
  --gold-glow:  #c9a84c30;
  --copper:     #a07840;
  --navy:       #080d1a;
  --navy-2:     #0c1220;
  --navy-3:     #101828;
  --navy-border:#1e2a3a;
  --navy-card:  #0d1525;
  --cream:      #e8e0d0;
  --text-dim:   #6a7080;
  --text-mid:   #a0a8b8;
  --green:      #4ade80;
  --amber:      #fbbf24;
  --red:        #f87171;
}

html,body,[class*="css"]{font-family:'Syne',sans-serif;background:var(--navy);color:var(--cream);}
.main{background:var(--navy);}.block-container{padding-top:1.5rem!important;max-width:1400px;}
section[data-testid="stSidebar"]{background:linear-gradient(180deg,var(--navy-2),var(--navy));border-right:1px solid #1a2030;}
h1{font-family:'Syne',sans-serif!important;font-weight:800!important;font-size:2rem!important;
   background:linear-gradient(100deg,var(--gold-light),var(--gold),var(--copper));-webkit-background-clip:text;
   -webkit-text-fill-color:transparent;background-clip:text;letter-spacing:-0.5px;margin-bottom:0!important;}
h2,h3{font-family:'Syne',sans-serif!important;font-weight:700!important;color:var(--cream)!important;}

/* ── SEARCH ──────────────────────────────────────────────────── */
.search-wrapper{background:linear-gradient(135deg,var(--navy-2),var(--navy-3));border:1px solid var(--gold-dim);
  border-radius:14px;padding:1.2rem 1.5rem;margin-bottom:0.8rem;box-shadow:0 4px 24px #c9a84c08;}
.search-title{font-family:'JetBrains Mono',monospace;font-size:0.62rem;color:var(--gold);
  letter-spacing:3px;text-transform:uppercase;margin-bottom:0.5rem;}
.search-examples{font-family:'JetBrains Mono',monospace;font-size:0.68rem;color:#475060;line-height:1.9;margin-top:0.5rem;}
.search-examples span{color:var(--gold);}

/* ── PILLS ───────────────────────────────────────────────────── */
.pill-row{display:flex;flex-wrap:wrap;gap:6px;margin:0.6rem 0;}
.pill{display:inline-flex;align-items:center;gap:4px;font-family:'JetBrains Mono',monospace;
  font-size:0.68rem;padding:4px 12px;border-radius:20px;letter-spacing:0.5px;}
.pill-ok{background:#0d2a14;color:#4ade80;border:1px solid #1e5028;}
.pill-warn{background:#2a1400;color:#fbbf24;border:1px solid #7c4a00;}
.pill-info{background:#1a1200;color:var(--gold);border:1px solid var(--gold-dim);}

/* ── WINNER CARD ─────────────────────────────────────────────── */
.winner-card{background:linear-gradient(135deg,#0a1018,#0e1a28,#0a1018);border:1px solid #2a2010;
  border-radius:20px;padding:2rem 2.2rem;margin:1.5rem 0;position:relative;overflow:hidden;
  box-shadow:0 0 60px #c9a84c08,0 8px 32px #00000050;}
.winner-card::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;
  background:linear-gradient(90deg,var(--gold-dim),var(--gold),var(--gold-light),var(--gold),var(--gold-dim));}
.winner-eyebrow{font-family:'JetBrains Mono',monospace;font-size:0.6rem;letter-spacing:4px;
  color:var(--gold);text-transform:uppercase;margin-bottom:0.6rem;display:flex;align-items:center;gap:8px;}
.winner-eyebrow::before{content:'';display:inline-block;width:8px;height:8px;border-radius:50%;
  background:var(--gold);box-shadow:0 0 10px var(--gold);}
.winner-name{font-family:'Syne',sans-serif;font-size:2.4rem;font-weight:800;color:#fff;line-height:1.1;margin-bottom:0.3rem;}
.winner-meta{font-family:'JetBrains Mono',monospace;font-size:0.78rem;color:var(--text-dim);}
.winner-score{font-family:'JetBrains Mono',monospace;font-size:0.68rem;color:var(--gold);
  background:#1a1400;border:1px solid var(--gold-dim);border-radius:6px;padding:2px 10px;margin-left:12px;}

/* ── METRIC GRID ─────────────────────────────────────────────── */
.metric-grid{display:grid;grid-template-columns:repeat(7,1fr);gap:8px;margin:1.2rem 0;}
.metric-card{background:var(--navy-card);border:1px solid var(--navy-border);border-radius:12px;padding:0.75rem 0.5rem;text-align:center;}
.metric-icon{font-size:1.1rem;margin-bottom:0.2rem;}
.metric-label{font-family:'JetBrains Mono',monospace;font-size:0.52rem;color:var(--gold);letter-spacing:1.5px;text-transform:uppercase;margin-bottom:0.3rem;}
.metric-value{font-family:'Syne',sans-serif;font-size:1.2rem;font-weight:700;color:#fff;line-height:1;}
.metric-unit{font-family:'JetBrains Mono',monospace;font-size:0.58rem;color:var(--text-dim);margin-top:0.1rem;}
.metric-status-g{color:var(--green);font-size:0.58rem;margin-top:0.1rem;font-family:'JetBrains Mono',monospace;}
.metric-status-y{color:var(--amber);font-size:0.58rem;margin-top:0.1rem;font-family:'JetBrains Mono',monospace;}
.metric-status-r{color:var(--red);font-size:0.58rem;margin-top:0.1rem;font-family:'JetBrains Mono',monospace;}

/* ── REASONING CARD ──────────────────────────────────────────── */
.reasoning-card{background:var(--navy-card);border:1px solid var(--navy-border);border-left:3px solid var(--gold-dim);
  border-radius:12px;padding:1.4rem 1.6rem;margin-top:0.5rem;}
.reasoning-section{font-family:'JetBrains Mono',monospace;font-size:0.65rem;color:var(--gold);
  letter-spacing:2px;text-transform:uppercase;margin:1rem 0 0.5rem;}
.reasoning-section:first-child{margin-top:0;}
.reasoning-row{display:flex;align-items:flex-start;gap:10px;padding:0.35rem 0;
  border-bottom:1px solid #141c28;font-family:'JetBrains Mono',monospace;font-size:0.76rem;color:var(--text-mid);}
.reasoning-row:last-child{border-bottom:none;}
.reasoning-dot{width:6px;height:6px;border-radius:50%;flex-shrink:0;margin-top:5px;}
.dot-green{background:var(--green);box-shadow:0 0 6px var(--green);}
.dot-yellow{background:var(--amber);box-shadow:0 0 6px var(--amber);}
.dot-orange{background:#fb923c;box-shadow:0 0 6px #fb923c;}
.rval{color:var(--cream);font-weight:600;}.rtag-g{color:var(--green);}.rtag-y{color:var(--amber);}.rtag-o{color:#fb923c;}

/* ── RANK CARDS ──────────────────────────────────────────────── */
.rank-card{background:var(--navy-card);border:1px solid var(--navy-border);border-radius:14px;padding:1rem 1.2rem;
  margin-bottom:0.8rem;display:flex;align-items:flex-start;gap:1rem;transition:border-color 0.2s;}
.rank-card:hover{border-color:var(--gold-dim);}
.rank-card.rank-1{border-color:#3a2a0a;background:linear-gradient(90deg,#120e04,var(--navy-card));}
.rank-number{font-family:'Syne',sans-serif;font-size:1.8rem;font-weight:800;color:#1a2030;width:2.2rem;flex-shrink:0;text-align:center;padding-top:2px;}
.rank-card.rank-1 .rank-number{color:var(--gold);}
.rank-info{flex:1;min-width:0;}
.rank-name{font-family:'Syne',sans-serif;font-size:1rem;font-weight:700;color:var(--cream);}
.rank-survey{font-family:'JetBrains Mono',monospace;font-size:0.66rem;color:var(--text-dim);margin-top:2px;}
.rank-badges{display:flex;flex-wrap:wrap;gap:4px;align-items:center;margin-top:6px;}

/* ── BADGES ──────────────────────────────────────────────────── */
.badge{font-family:'JetBrains Mono',monospace;font-size:0.6rem;padding:2px 7px;border-radius:4px;letter-spacing:0.4px;white-space:nowrap;}
.b-eco{background:#0d2014;color:#4ade80;border:1px solid #1e4028;}
.b-pwr{background:#1a1200;color:var(--gold-light);border:1px solid var(--gold-dim);}
.b-air{background:#1c1000;color:#fb923c;border:1px solid #7c3500;}
.b-rail{background:#0a1420;color:#93c5fd;border:1px solid #1e3060;}
.b-water{background:#001820;color:#67e8f9;border:1px solid #0c3a48;}
.b-wf{background:#1a1200;color:var(--amber);border:1px solid #7c5000;}
.b-inc{background:#1a1000;color:var(--gold);border:1px solid var(--gold-dim);}
.b-icd{background:#001810;color:#86efac;border:1px solid #1a5030;}
.b-hwy{background:#1a1200;color:#fdba74;border:1px solid #7c4000;}

/* ── MAP LEGEND ──────────────────────────────────────────────── */
.map-legend{display:flex;flex-wrap:wrap;gap:12px;padding:0.8rem 1.2rem;
  background:var(--navy-card);border:1px solid var(--navy-border);border-radius:10px;margin-top:0.8rem;}
.legend-item{display:flex;align-items:center;gap:6px;font-family:'JetBrains Mono',monospace;font-size:0.68rem;color:var(--text-dim);}
.legend-dot{width:11px;height:11px;border-radius:50%;flex-shrink:0;}

/* ── SIDEBAR ─────────────────────────────────────────────────── */
.sidebar-label{font-family:'JetBrains Mono',monospace;font-size:0.6rem;color:var(--gold);
  letter-spacing:3px;text-transform:uppercase;margin-bottom:0.5rem;margin-top:0.8rem;display:block;}
.stat-row{display:flex;justify-content:space-between;align-items:center;padding:0.28rem 0;
  border-bottom:1px solid #141c28;font-family:'JetBrains Mono',monospace;font-size:0.68rem;}
.stat-label{color:var(--text-dim);}.stat-val{color:var(--cream);font-weight:600;}

/* ── SECTION HEADER ──────────────────────────────────────────── */
.section-header{display:flex;align-items:center;gap:12px;margin:1.8rem 0 1rem;}
.section-icon{font-size:1.1rem;}
.section-title{font-family:'Syne',sans-serif;font-size:1.15rem;font-weight:700;color:var(--cream);}
.section-line{flex:1;height:1px;background:linear-gradient(90deg,var(--gold-dim),transparent);}

/* ── PARSE BOX ───────────────────────────────────────────────── */
.parse-box{background:#0c1018;border:1px solid var(--gold-dim);border-radius:12px;padding:0.9rem 1.2rem;margin-bottom:1.2rem;}
.parse-header{font-family:'JetBrains Mono',monospace;font-size:0.62rem;color:var(--gold);letter-spacing:3px;text-transform:uppercase;margin-bottom:0.6rem;}
.parse-note{font-family:'JetBrains Mono',monospace;font-size:0.65rem;color:#2a3040;margin-top:0.5rem;}

/* ── STREAMLIT OVERRIDES ─────────────────────────────────────── */
[data-testid="stMetric"]{background:var(--navy-card)!important;border:1px solid var(--navy-border)!important;border-radius:12px!important;padding:0.8rem!important;}
div[data-testid="stTextInput"] input{background:var(--navy-card)!important;border:1px solid var(--gold-dim)!important;border-radius:10px!important;color:var(--cream)!important;font-family:'JetBrains Mono',monospace!important;font-size:0.85rem!important;padding:0.7rem 1rem!important;}
div[data-testid="stTextInput"] input:focus{border-color:var(--gold)!important;box-shadow:0 0 0 2px #c9a84c20!important;}
div[data-testid="stTextInput"] input::placeholder{color:#2a3040!important;}
.stExpander{border:1px solid var(--navy-border)!important;border-radius:12px!important;background:var(--navy-card)!important;}
hr{border-color:#141c28!important;margin:1.5rem 0!important;}

/* ── GOOGLE MAPS PANELS ──────────────────────────────────────── */
.gmaps-panel{background:linear-gradient(135deg,#0a1018,#0c1520);border:1px solid #2a2010;
  border-radius:16px;padding:1.4rem 1.6rem;margin:1rem 0;position:relative;overflow:hidden;}
.gmaps-panel::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;
  background:linear-gradient(90deg,var(--gold-dim),var(--gold),var(--gold-light),var(--gold),var(--gold-dim));}
.gmaps-eyebrow{font-family:'JetBrains Mono',monospace;font-size:0.58rem;letter-spacing:4px;
  color:var(--gold);text-transform:uppercase;margin-bottom:0.8rem;}
.place-card{background:#0a1018;border:1px solid #1a2030;border-radius:10px;
  padding:0.7rem 1rem;margin:0.4rem 0;display:flex;align-items:flex-start;gap:10px;}
.place-name{font-family:'Syne',sans-serif;font-size:0.85rem;font-weight:600;color:var(--cream);}
.place-meta{font-family:'JetBrains Mono',monospace;font-size:0.62rem;color:var(--text-dim);margin-top:2px;}
.place-dist{font-family:'JetBrains Mono',monospace;font-size:0.68rem;color:var(--gold);
  background:#1a1200;border:1px solid var(--gold-dim);border-radius:4px;padding:2px 7px;white-space:nowrap;margin-left:auto;}
.cat-header{font-family:'JetBrains Mono',monospace;font-size:0.6rem;color:var(--gold);
  letter-spacing:3px;text-transform:uppercase;margin:0.8rem 0 0.4rem;display:flex;align-items:center;gap:6px;}
.drive-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin:0.8rem 0;}
.drive-card{background:#0a1018;border:1px solid #1a2030;border-radius:10px;padding:0.8rem;text-align:center;}
.drive-label{font-family:'JetBrains Mono',monospace;font-size:0.55rem;color:var(--gold);letter-spacing:1.5px;text-transform:uppercase;margin-bottom:0.3rem;}
.drive-val{font-family:'Syne',sans-serif;font-size:1.3rem;font-weight:700;color:#fff;}
.drive-unit{font-family:'JetBrains Mono',monospace;font-size:0.55rem;color:var(--text-dim);margin-top:2px;}
.no-key-box{background:var(--navy-card);border:1px dashed var(--gold-dim);border-radius:12px;padding:1.2rem 1.5rem;
  text-align:center;font-family:'JetBrains Mono',monospace;font-size:0.72rem;color:#2a3040;margin:1rem 0;}
.reverse-place{background:#0a1018;border:1px solid #1a2030;border-radius:10px;
  padding:0.6rem 1rem;margin:0.3rem 0;font-family:'JetBrains Mono',monospace;font-size:0.72rem;color:var(--text-mid);}
.reverse-place strong{color:var(--cream);}
.insight-box{background:linear-gradient(135deg,#09100e,#0a1210);border:1px solid #2a2010;
  border-left:3px solid var(--gold-dim);border-radius:10px;padding:1rem 1.2rem;margin-top:0.8rem;
  font-family:'JetBrains Mono',monospace;font-size:0.72rem;color:var(--text-dim);line-height:1.8;}
.insight-box strong{color:var(--gold);}
.company-card{background:linear-gradient(135deg,#0a1018,#0c1520);border:1px solid #2a2010;
  border-radius:14px;padding:1.1rem 1.4rem;margin:0.6rem 0;position:relative;overflow:hidden;}
.company-card::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;
  background:linear-gradient(90deg,var(--gold-dim),var(--gold),var(--copper),var(--gold-dim));}
.company-name{font-family:'Syne',sans-serif;font-size:1rem;font-weight:700;color:var(--cream);margin-bottom:0.2rem;}
.company-meta{font-family:'JetBrains Mono',monospace;font-size:0.63rem;color:var(--text-dim);margin-top:2px;line-height:1.6;}
.company-badges{display:flex;flex-wrap:wrap;gap:6px;margin-top:0.5rem;}
.company-rank{font-family:'JetBrains Mono',monospace;font-size:0.58rem;color:var(--gold);
  background:#1a1200;border:1px solid var(--gold-dim);border-radius:4px;padding:2px 8px;}
.companies-header{font-family:'JetBrains Mono',monospace;font-size:0.62rem;color:var(--gold);
  letter-spacing:3px;text-transform:uppercase;margin:1rem 0 0.5rem;display:flex;align-items:center;gap:8px;}

/* ── NEW FEATURE CARDS ────────────────────────────────────────── */
.wins-card{background:linear-gradient(135deg,#091208,#0b1a0c);border:1px solid #1e3a18;
  border-left:3px solid #4ade80;border-radius:16px;padding:1.4rem 1.6rem;margin:1rem 0;position:relative;overflow:hidden;}
.wins-card::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;
  background:linear-gradient(90deg,#4ade80,var(--gold),#4ade80);}
.wins-eyebrow{font-family:'JetBrains Mono',monospace;font-size:0.6rem;letter-spacing:4px;
  color:#4ade80;text-transform:uppercase;margin-bottom:0.8rem;}
.wins-item{display:flex;align-items:flex-start;gap:10px;padding:0.4rem 0;
  border-bottom:1px solid #0d1a0a;font-family:'JetBrains Mono',monospace;font-size:0.76rem;color:#90b890;}
.wins-item:last-child{border-bottom:none;}
.wins-dot{width:7px;height:7px;border-radius:50%;background:#4ade80;box-shadow:0 0 8px #4ade80;flex-shrink:0;margin-top:5px;}

.missing-card{background:linear-gradient(135deg,#180c04,#200e06);border:1px solid #5a2808;
  border-left:3px solid #fb923c;border-radius:16px;padding:1.4rem 1.6rem;margin:1rem 0;position:relative;overflow:hidden;}
.missing-card::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;
  background:linear-gradient(90deg,#fb923c,var(--copper),#fb923c);}
.missing-eyebrow{font-family:'JetBrains Mono',monospace;font-size:0.6rem;letter-spacing:4px;
  color:#fb923c;text-transform:uppercase;margin-bottom:0.8rem;}
.missing-item{display:flex;align-items:flex-start;gap:10px;padding:0.4rem 0;
  border-bottom:1px solid #200e06;font-family:'JetBrains Mono',monospace;font-size:0.76rem;color:#c89870;}
.missing-item:last-child{border-bottom:none;}
.missing-dot{width:7px;height:7px;border-radius:50%;background:#fb923c;box-shadow:0 0 8px #fb923c;flex-shrink:0;margin-top:5px;}

.cluster-insight-card{background:linear-gradient(135deg,#0a1018,#0d1628);border:1px solid #2a2010;
  border-left:3px solid var(--gold);border-radius:14px;padding:1.2rem 1.5rem;margin:1rem 0;position:relative;overflow:hidden;}
.cluster-insight-card::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;
  background:linear-gradient(90deg,var(--gold-dim),var(--gold),var(--gold-light),var(--gold),var(--gold-dim));}
.cluster-insight-eyebrow{font-family:'JetBrains Mono',monospace;font-size:0.6rem;letter-spacing:4px;
  color:var(--gold);text-transform:uppercase;margin-bottom:0.6rem;}
.cluster-insight-text{font-family:'JetBrains Mono',monospace;font-size:0.76rem;color:var(--text-mid);line-height:1.9;}
.cluster-stat-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin:0.8rem 0;}
.cluster-stat{background:#0a1018;border:1px solid #1a2030;border-radius:8px;padding:0.6rem;text-align:center;}
.cluster-stat-label{font-family:'JetBrains Mono',monospace;font-size:0.52rem;color:var(--text-dim);letter-spacing:1px;text-transform:uppercase;margin-bottom:0.3rem;}
.cluster-stat-val{font-family:'Syne',sans-serif;font-size:1.1rem;font-weight:700;color:var(--gold);}

.compare-table-card{background:var(--navy-card);border:1px solid var(--navy-border);border-radius:16px;padding:1.4rem 1.6rem;margin:1rem 0;}
.compare-header{font-family:'JetBrains Mono',monospace;font-size:0.6rem;letter-spacing:3px;
  color:var(--gold);text-transform:uppercase;margin-bottom:1rem;}
.compare-table{width:100%;border-collapse:collapse;font-family:'JetBrains Mono',monospace;font-size:0.72rem;}
.compare-table th{color:var(--text-dim);font-weight:600;text-align:left;padding:0.5rem 0.8rem;
  border-bottom:2px solid var(--navy-border);font-size:0.6rem;letter-spacing:1px;text-transform:uppercase;}
.compare-table td{padding:0.55rem 0.8rem;border-bottom:1px solid #141c28;color:var(--cream);vertical-align:middle;}
.compare-table tr:last-child td{border-bottom:none;}
.compare-table tr.winner-row td{background:#0d1a0a;color:#4ade80;}
.compare-val-best{color:#4ade80;font-weight:700;}
.compare-val-mid{color:var(--amber);}
.compare-val-worst{color:#fb923c;}
.recommend-row{display:flex;gap:10px;margin-top:0.8rem;flex-wrap:wrap;}
.recommend-pill{background:#0a1018;border:1px solid var(--gold-dim);border-radius:8px;padding:0.5rem 0.9rem;
  font-family:'JetBrains Mono',monospace;font-size:0.68rem;color:var(--text-mid);flex:1;min-width:180px;}
.recommend-pill strong{color:var(--gold);display:block;margin-bottom:3px;}

.decision-mode-card{background:linear-gradient(135deg,#0a1018,#0c1420);border:1px solid #3a2a08;
  border-left:3px solid var(--gold);border-radius:14px;padding:1.2rem 1.5rem;margin:1rem 0;position:relative;overflow:hidden;}
.decision-mode-card::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;
  background:linear-gradient(90deg,var(--gold-dim),var(--gold),var(--gold-light));}
.decision-eyebrow{font-family:'JetBrains Mono',monospace;font-size:0.6rem;letter-spacing:4px;
  color:var(--gold);text-transform:uppercase;margin-bottom:0.5rem;}
.decision-parsed{font-family:'JetBrains Mono',monospace;font-size:0.72rem;color:var(--text-mid);line-height:1.8;margin-top:0.5rem;}
.decision-weight-bar{display:flex;align-items:center;gap:8px;margin-bottom:4px;}
.decision-weight-label{font-family:'JetBrains Mono',monospace;font-size:0.6rem;color:var(--text-dim);width:90px;}
.decision-weight-track{flex:1;background:var(--navy-card);border-radius:4px;height:5px;}

.hidden-tradeoffs-card{background:linear-gradient(135deg,#120c08,#180e0a);border:1px solid #4a2808;
  border-left:3px solid var(--copper);border-radius:12px;padding:1.1rem 1.4rem;margin:0.8rem 0;}
.hidden-tradeoffs-eyebrow{font-family:'JetBrains Mono',monospace;font-size:0.6rem;letter-spacing:3px;
  color:var(--copper);text-transform:uppercase;margin-bottom:0.6rem;}
.tradeoff-item{display:flex;align-items:flex-start;gap:8px;padding:0.3rem 0;
  border-bottom:1px solid #180e0a;font-family:'JetBrains Mono',monospace;font-size:0.73rem;color:#a08060;}
.tradeoff-item:last-child{border-bottom:none;}

.conclusion-card{background:linear-gradient(135deg,#0a1018,#0c1420);border:1px solid #2a2010;
  border-left:3px solid var(--gold-light);border-radius:12px;padding:1.1rem 1.4rem;margin:0.8rem 0;}
.conclusion-eyebrow{font-family:'JetBrains Mono',monospace;font-size:0.6rem;letter-spacing:3px;
  color:var(--gold-light);text-transform:uppercase;margin-bottom:0.5rem;}
.conclusion-text{font-family:'JetBrains Mono',monospace;font-size:0.76rem;color:var(--text-mid);line-height:1.8;}
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


def fetch_top_companies(lat, lon, industry, api_key):
    """
    Fetch real companies from Google Places API for a given industry.
    Uses INDUSTRY_DNA[industry]["places_keywords"] to run multiple searches.
    Returns top 10 deduplicated companies sorted by rating (desc) then distance (asc).
    """
    if not api_key:
        return []

    dna_entry = INDUSTRY_DNA.get(industry, {})
    keywords_list = dna_entry.get("places_keywords", [])
    if not keywords_list:
        keywords_list = [industry.lower()]

    all_companies = []
    seen_names = set()

    for kw in keywords_list[:3]:  # limit to 3 keywords to stay within API budget
        places = gmaps_nearby_search(lat, lon, kw, radius=15000, api_key=api_key)
        for p in places:
            name_key = p["name"].strip().lower()
            if name_key not in seen_names:
                seen_names.add(name_key)
                all_companies.append({
                    "name": p["name"],
                    "lat": p["lat"],
                    "lon": p["lon"],
                    "rating": p.get("rating") or 0.0,
                    "vicinity": p.get("vicinity", ""),
                    "dist_km": p["dist_km"],
                    "search_kw": kw,
                })

    # Sort: rating descending, then distance ascending
    all_companies.sort(key=lambda x: (-x["rating"], x["dist_km"]))
    return all_companies[:10]


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


# ── FEATURE 1 & 2: WHY THIS LAND WINS + WHAT'S MISSING ─────────────────────
def compute_why_wins_and_missing(winner_row, all_parcels_df, industry, weights):
    """
    Dynamically compare winner against all parcels and the industry DNA thresholds.
    Returns (strengths_list, missing_list).
    """
    dna = INDUSTRY_DNA.get(industry, {})
    strengths = []
    missing = []

    # Thresholds for "ideal" per dimension
    IDEAL = {
        "water_dist": 2.0, "power_dist": 3.0, "highway_dist": 3.0,
        "airport_dist": 10.0, "icd_dist": 5.0, "rail_dist": 5.0,
    }
    WEAK_THRESHOLDS = {
        "water_dist": 8.0, "power_dist": 8.0, "highway_dist": 10.0,
        "airport_dist": 20.0, "icd_dist": 15.0, "rail_dist": 15.0,
    }
    DIM_LABELS = {
        "water_dist": "water body", "power_dist": "power substation",
        "highway_dist": "highway junction", "airport_dist": "airport",
        "icd_dist": "ICD dry port", "rail_dist": "railway station",
        "ecosystem": "ecosystem density", "workforce_score": "workforce quality",
        "incentive_score": "incentive score",
    }

    n = len(all_parcels_df)

    # ── Distance-based comparisons (lower = better) ──────────────────────────
    for col in ["water_dist", "power_dist", "highway_dist", "airport_dist", "icd_dist", "rail_dist"]:
        if col not in winner_row.index or col not in all_parcels_df.columns:
            continue
        val = winner_row[col]
        rank_among = int((all_parcels_df[col] >= val).sum())  # how many >= winner (higher=closer)
        percentile = rank_among / n

        weight_key = {"water_dist": "Water", "power_dist": "Power",
                      "highway_dist": "Ecosystem", "airport_dist": "Airport",
                      "icd_dist": "Ecosystem", "rail_dist": "Ecosystem"}.get(col, "Ecosystem")
        w = weights.get(weight_key, 0.05)
        label = DIM_LABELS[col]

        if percentile >= 0.75 and w >= 0.07:
            strengths.append(f"Closest to {label} among top parcels — {val:.1f} km (top {int((1-percentile)*100)+1}%)")
        elif val > WEAK_THRESHOLDS.get(col, 20) and w >= 0.07:
            missing.append(f"{label.title()} too far — {val:.1f} km (industry ideal: <{IDEAL.get(col, 5):.0f} km)")

    # ── Ecosystem / cluster ──────────────────────────────────────────────────
    if "ecosystem" in winner_row.index and "ecosystem" in all_parcels_df.columns:
        eco_val = winner_row["ecosystem"]
        eco_rank = int((all_parcels_df["ecosystem"] <= eco_val).sum()) / n
        if eco_rank >= 0.75 and weights.get("Ecosystem", 0) >= 0.15:
            strengths.append(f"Highest ecosystem density among shortlisted parcels — {int(eco_val)} cluster points")
        elif eco_val < 2 and weights.get("Ecosystem", 0) >= 0.15:
            missing.append("Weak cluster score — sparse industrial ecosystem; greenfield risk")

    # ── Workforce ────────────────────────────────────────────────────────────
    if "workforce_score" in winner_row.index and "workforce_score" in all_parcels_df.columns:
        wf_val = winner_row["workforce_score"]
        wf_rank = int((all_parcels_df["workforce_score"] <= wf_val).sum()) / n
        if wf_rank >= 0.75:
            strengths.append(f"Best workforce quality match — score {wf_val:.2f}/1.00 (top {int((1-wf_rank)*100)+1}%)")
        elif wf_val < 0.45:
            missing.append(f"Workforce score is weak ({wf_val:.2f}) — labour recruitment may be difficult")

    # ── Incentive ────────────────────────────────────────────────────────────
    if "incentive_score" in winner_row.index and "incentive_tier" in winner_row.index:
        if str(winner_row.get("incentive_tier", "")).lower() == "backward":
            strengths.append("Located in Backward Incentive Zone — maximum government subsidies available")
        elif winner_row.get("incentive_score", 0) < 0.4:
            missing.append("Standard incentive tier only — limited subsidy advantage vs backward zone alternatives")

    # ── Industry-specific gap analysis vs DNA weights ─────────────────────────
    priority_dim = max(weights, key=weights.get)  # e.g. "Water" for Food Processing
    dim_col_map = {"Water": "water_dist", "Power": "power_dist", "Airport": "airport_dist"}
    priority_col = dim_col_map.get(priority_dim)
    if priority_col and priority_col in winner_row.index:
        val = winner_row[priority_col]
        if val > WEAK_THRESHOLDS.get(priority_col, 10):
            if not any(priority_dim.lower() in m.lower() for m in missing):
                missing.append(f"Top priority for {industry} is {priority_dim} access — {val:.1f} km is above recommended threshold")

    # Deduplicate and trim
    strengths = list(dict.fromkeys(strengths))[:5]
    missing = list(dict.fromkeys(missing))[:4]

    return strengths, missing


# ── FEATURE 3: CLUSTER STRATEGY INSIGHT ─────────────────────────────────────
def compute_cluster_strategy_insight(companies, winner_lat, winner_lon, industry,
                                     substations, icd_points, highway_coords,
                                     water_lat_lons):
    """
    Analyse fetched companies' locations vs key infrastructure.
    Returns (stats_dict, insight_text).
    """
    if not companies:
        return {}, ""

    dists_highway, dists_water, dists_airport = [], [], []

    for c in companies:
        clat, clon = c["lat"], c["lon"]
        # Highway
        if highway_coords:
            dh = min(haversine(clat, clon, h[0], h[1]) for h in highway_coords)
            dists_highway.append(dh)
        # Water
        if water_lat_lons:
            dw = min(haversine(clat, clon, w[0], w[1]) for w in water_lat_lons)
            dists_water.append(dw)
        # Airport
        dists_airport.append(haversine(clat, clon, AIRPORT[0], AIRPORT[1]))

    avg_hwy = sum(dists_highway) / len(dists_highway) if dists_highway else None
    avg_water = sum(dists_water) / len(dists_water) if dists_water else None
    avg_airport = sum(dists_airport) / len(dists_airport) if dists_airport else None
    total_eco = len(companies)

    stats = {
        "avg_highway_km": avg_hwy,
        "avg_water_km": avg_water,
        "avg_airport_km": avg_airport,
        "total_companies": total_eco,
    }

    # Generate narrative insight
    lines = []
    if avg_hwy is not None:
        lines.append(f"Most {industry} companies are located within {avg_hwy:.1f} km of a highway junction")
    if avg_water is not None:
        if avg_water < 5:
            lines.append(f"strong water proximity (avg {avg_water:.1f} km) suggests supply-chain-driven location logic")
        else:
            lines.append(f"water distance averages {avg_water:.1f} km — less critical for this cluster's operations")
    if avg_airport is not None:
        lines.append(f"average airport drive distance is {avg_airport:.1f} km")

    if avg_hwy is not None and avg_water is not None:
        if avg_water < 4 and avg_hwy < 8:
            pattern = "dual-dependency pattern (water + highway) — consistent with supply-chain-driven site selection"
        elif avg_hwy < 8:
            pattern = "highway-first location logic — distribution speed and freight access dominate site decisions"
        elif avg_water < 4:
            pattern = "water-first location logic — process requirements (washing, cooling, boiling) govern site choice"
        else:
            pattern = "balanced location pattern — no single dominant infrastructure driver detected"
        lines.append(f"indicating a {pattern}")

    insight = (", ".join(lines[:2]).capitalize() + ". " + ". ".join(lines[2:])).strip(" .")
    if insight:
        insight += "."

    return stats, insight


# ── FEATURE 5: DECISION MODE PARSER ─────────────────────────────────────────
DECISION_KEYWORDS = {
    "export":       {"Airport": +0.12, "ICD": +0.08},
    "export-driven":{"Airport": +0.12, "ICD": +0.08},
    "air cargo":    {"Airport": +0.15},
    "port":         {"ICD": +0.12},
    "icd":          {"ICD": +0.10},
    "manufacturing":{"Power": +0.10, "Ecosystem": +0.08},
    "production":   {"Power": +0.08, "Water": +0.05},
    "heavy industry":{"Power": +0.12, "Ecosystem": +0.08},
    "agro":         {"Water": +0.15, "Ecosystem": +0.08},
    "agri":         {"Water": +0.12},
    "food":         {"Water": +0.15, "Ecosystem": +0.08},
    "water":        {"Water": +0.12},
    "power":        {"Power": +0.12},
    "energy":       {"Power": +0.10},
    "logistics":    {"Airport": +0.10, "ICD": +0.10, "Ecosystem": +0.05},
    "warehouse":    {"Airport": +0.08, "ICD": +0.08},
    "textile":      {"Water": +0.08, "Ecosystem": +0.10, "Workforce": +0.08},
    "garment":      {"Water": +0.06, "Ecosystem": +0.10, "Workforce": +0.08},
    "electronics":  {"Airport": +0.10, "Power": +0.08},
    "ev":           {"Power": +0.10, "Airport": +0.08},
    "labour":       {"Workforce": +0.12},
    "workforce":    {"Workforce": +0.10},
    "cost":         {"Incentive": +0.12, "Workforce": +0.06},
    "cheap":        {"Incentive": +0.12},
    "incentive":    {"Incentive": +0.15},
    "subsidy":      {"Incentive": +0.12},
}

def parse_decision_mode(text):
    """
    Parse free-text decision intent into weight adjustments.
    Returns (adjustments_dict, detected_keywords_list, narrative_str).
    """
    if not text or not text.strip():
        return {}, [], ""
    t = text.lower()
    adjustments = {}
    detected = []
    for kw, deltas in DECISION_KEYWORDS.items():
        if kw in t:
            detected.append(kw)
            for factor, delta in deltas.items():
                adjustments[factor] = adjustments.get(factor, 0) + delta

    narrative_parts = []
    if "Airport" in adjustments and adjustments["Airport"] > 0.08:
        narrative_parts.append("boosting Airport weight (export/air-freight priority)")
    if "ICD" in adjustments and adjustments["ICD"] > 0.06:
        narrative_parts.append("boosting ICD weight (container/port logistics)")
    if "Power" in adjustments and adjustments["Power"] > 0.07:
        narrative_parts.append("increasing Power weight (manufacturing/heavy ops)")
    if "Water" in adjustments and adjustments["Water"] > 0.07:
        narrative_parts.append("raising Water weight (process/agro requirements)")
    if "Incentive" in adjustments and adjustments["Incentive"] > 0.08:
        narrative_parts.append("maximising Incentive weight (cost-sensitive strategy)")
    if "Workforce" in adjustments and adjustments["Workforce"] > 0.07:
        narrative_parts.append("prioritising Workforce quality")
    if "Ecosystem" in adjustments and adjustments["Ecosystem"] > 0.06:
        narrative_parts.append("strengthening Ecosystem cluster weight")

    narrative = "Decision Mode active — " + ", ".join(narrative_parts) if narrative_parts else ""
    return adjustments, detected, narrative


def apply_decision_weights(base_weights, adjustments):
    """Merge decision mode adjustments into the industry base weights (normalised)."""
    merged = dict(base_weights)
    for k, delta in adjustments.items():
        if k in merged:
            merged[k] = min(merged[k] + delta, 0.55)
    # Renormalise to sum = 1
    total = sum(merged.values())
    if total > 0:
        merged = {k: v / total for k, v in merged.items()}
    return merged


# ── FEATURE 6 HELPERS: UPGRADED REVERSE ANALYSIS ────────────────────────────
def generate_hidden_tradeoffs(industry, water_dist, power_dist, airport_mins,
                               icd_mins, highway_mins, cluster_label, workforce_score):
    """Generate hidden trade-offs not obvious from surface-level analysis."""
    tradeoffs = []
    dna = INDUSTRY_DNA.get(industry, {})

    if industry == "Food Processing":
        if water_dist < 2:
            tradeoffs.append("Proximity to water body increases ETP (effluent treatment) compliance obligation")
        if airport_mins > 30:
            tradeoffs.append("Airport distance limits export of perishables — cold-chain shelf-life risk")
        if cluster_label == "Strong":
            tradeoffs.append("Dense food cluster → wage inflation risk; labour poaching from competitors")
        tradeoffs.append("Water scarcity in peak summer months can force production shutdowns")

    elif industry == "Precision Engineering":
        if power_dist < 3:
            tradeoffs.append("Grid proximity increases exposure to industrial-load voltage fluctuations — AVR/UPS mandatory")
        if cluster_label == "Strong":
            tradeoffs.append("Engineering cluster increases subcontractor dependency — margin pressure in peak demand")
        tradeoffs.append("Skilled ITI labour is scarce; high-density clusters drive up wage benchmarks")

    elif industry == "Logistics & Warehouse":
        if highway_mins < 10:
            tradeoffs.append("Highway proximity → high land lease/acquisition cost; rate escalation likely within 3 years")
        if icd_mins < 15:
            tradeoffs.append("ICD proximity creates customs congestion risk during peak import/export cycles")
        tradeoffs.append("Toll cost on National Highways adds ~₹80–200/trip to FCL/LCL runs — route planning critical")

    elif industry == "Textile / Garments":
        if water_dist < 3:
            tradeoffs.append("ETP cost for dyeing units near water: ₹50–150L capex + ₹5–15L/yr opex")
        tradeoffs.append("Labour-intensive ops face 15–25% seasonal absenteeism (harvest, festival periods)")
        tradeoffs.append("Yarn price volatility (cotton futures) creates 8–20% margin swings quarterly")

    elif industry == "Electronics / EV":
        tradeoffs.append("ESD-sensitive assembly requires cleanroom investment (₹30–80L depending on class)")
        if airport_mins > 30:
            tradeoffs.append("Delayed air-freight access slows component import cycles — JIT disruption risk")
        tradeoffs.append("Battery logistics classified as hazardous — special permits, insurance & handling add cost")

    else:
        tradeoffs.append("Verify site-specific zoning regulations before committing to capex")
        tradeoffs.append("Infrastructure adequacy must be validated through local authority site inspection")

    return tradeoffs[:3]


def generate_location_conclusion(company_name, industry, why_list, challenge_list,
                                  water_dist, power_dist, airport_mins, cluster_label):
    """Generate a concise 2-3 sentence location strategy conclusion."""
    n_why = len(why_list)
    n_challenges = len(challenge_list)

    if n_why >= 3 and n_challenges <= 1:
        strength_str = "strong strategic fit"
        verdict = "This is a well-optimised industrial site."
    elif n_why >= n_challenges:
        strength_str = "moderate strategic fit with manageable trade-offs"
        verdict = "Site selection appears deliberate with accepted operational trade-offs."
    else:
        strength_str = "constrained site with notable gaps"
        verdict = "Location likely chosen for cost or early-mover advantage despite infrastructure gaps."

    dna = INDUSTRY_DNA.get(industry, {})
    priority_dim = max(dna.get("weights", {"Ecosystem": 0.2}), key=dna.get("weights", {}).get)

    if cluster_label == "Strong":
        eco_context = "a mature cluster ecosystem supporting vendor access and labour supply"
    elif cluster_label == "Moderate":
        eco_context = "an emerging ecosystem with growing vendor and labour infrastructure"
    else:
        eco_context = "a greenfield or early-mover position with limited local ecosystem support"

    conclusion = (
        f"This {industry} location demonstrates {strength_str}. "
        f"Site selection logic is anchored around {priority_dim.lower()} access, "
        f"positioned within {eco_context}. "
        f"{verdict}"
    )
    return conclusion


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
    auto_mode = company_row is not None

    if auto_mode:
        r_lat = float(company_row["lat"])
        r_lon = float(company_row["lon"])
        st.markdown(
            f'<div style="font-family:JetBrains Mono,monospace;font-size:0.7rem;color:#4ade80;margin-bottom:0.6rem;">'
            f'📌 Auto-coordinates: <strong>{r_lat:.5f}, {r_lon:.5f}</strong></div>',
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

    scan_radius = st.slider("Search radius (km)", 2, 20, 10,
                            key=f"rev_radius_{str(company_row.get('name', 'parcel') if isinstance(company_row, dict) else 'parcel') if auto_mode else 'manual'}")
    rev_industry = selected_industry  # passed from caller; falls back to None

    # Auto-run when triggered from a company button; manual mode requires button click
    should_run = auto_mode
    if not auto_mode:
        should_run = st.button("🔍 Analyse This Location", key="rev_btn")

    if should_run:
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
                f'<div style="font-family:JetBrains Mono,monospace;font-size:0.7rem;color:#c9a84c;margin:0.5rem 0;">'
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
  <span style="color:#3a2a10;"> · {nearest['vicinity']}</span>
</div>""", unsafe_allow_html=True)

        # ── Cluster score banner ───────────────────────────────────────────────
        total_places = sum(len(v) for v in findings.values())
        if total_places >= 10:
            cluster_col, cluster_txt = "#4ade80", f"Strong Cluster · {total_places} relevant units"
        elif total_places >= 5:
            cluster_col, cluster_txt = "#fbbf24", f"Moderate Cluster · {total_places} units found"
        else:
            cluster_col, cluster_txt = "#fb923c", f"Weak / Greenfield · {total_places} units found"

        st.markdown(
            f'<div style="font-family:JetBrains Mono,monospace;font-size:0.7rem;color:{cluster_col};'
            f'background:#0a1018;border:1px solid {cluster_col}40;border-radius:8px;padding:0.5rem 1rem;'
            f'margin:0.6rem 0;">🏭 Cluster Strength: <strong>{cluster_txt}</strong></div>',
            unsafe_allow_html=True
        )

        # ── Industry-Specific Insight ──────────────────────────────────────────
        if rev_industry:
            why_list, challenge_list = generate_industry_insight(
                findings, rev_industry, drive_results, water_d, power_d, wf_score
            )

            # Compute drive mins for hidden tradeoffs + conclusion
            airport_time  = next((r for r in drive_results if "Airport" in r["label"]), None)
            icd_time      = next((r for r in drive_results if "ICD" in r["label"]), None)
            highway_time  = next((r for r in drive_results if "Junction" in r["label"] or "Highway" in r["label"]), None)
            airport_mins_r  = airport_time["duration_seconds"] // 60 if airport_time and airport_time["duration_seconds"] != 9999 else 9999
            icd_mins_r      = icd_time["duration_seconds"] // 60    if icd_time    and icd_time["duration_seconds"]    != 9999 else 9999
            highway_mins_r  = highway_time["duration_seconds"] // 60 if highway_time and highway_time["duration_seconds"] != 9999 else 9999
            cluster_label_r = "Strong" if total_places >= 10 else "Moderate" if total_places >= 5 else "Weak / Greenfield"

            # Feature 6 — company-specific tone for WHY
            company_name_r = company_row.get("name", "This company") if isinstance(company_row, dict) else "This company"

            why_html = "".join(
                f'<div class="reasoning-row">'
                f'<div class="reasoning-dot dot-green"></div>'
                f'<span style="color:#e0d8c0;"><strong style="color:#c9a84c60;">{company_name_r}</strong> — {point}</span></div>'
                for point in why_list
            ) if why_list else ""

            challenge_html = "".join(
                f'<div class="reasoning-row">'
                f'<div class="reasoning-dot dot-orange"></div>'
                f'<span style="color:#e0d8c0;">{point}</span></div>'
                for point in challenge_list
            )

            ind_icon = INDUSTRY_DNA.get(rev_industry, {}).get("icon", "🏭")
            st.markdown(f"""
<div class="reasoning-card" style="margin-top:1rem;border-left-color:#4ade80;">
  <div style="font-family:JetBrains Mono,monospace;font-size:0.62rem;color:#4ade80;
       letter-spacing:3px;text-transform:uppercase;margin-bottom:0.8rem;">
    {ind_icon} {rev_industry} · Company-Specific Location Analysis · {company_name_r}
  </div>

  <div class="reasoning-section">🧠 Why This Location Was Chosen</div>
  {why_html if why_html else '<div class="reasoning-row"><span style="color:#4a6080;">Insufficient data to generate strengths — try increasing scan radius.</span></div>'}

  <div class="reasoning-section" style="margin-top:1rem;">⚠️ Operational Challenges</div>
  {challenge_html if challenge_html else '<div class="reasoning-row"><span style="color:#4a6080;">No challenges flagged at this scan radius.</span></div>'}
</div>""", unsafe_allow_html=True)

            # Feature 6 — Hidden Trade-offs section
            tradeoffs = generate_hidden_tradeoffs(
                rev_industry, water_d, power_d, airport_mins_r,
                icd_mins_r, highway_mins_r, cluster_label_r, wf_score
            )
            tradeoffs_html = "".join(
                f'<div class="tradeoff-item"><div style="width:7px;height:7px;border-radius:50%;'
                f'background:#a855f7;box-shadow:0 0 6px #a855f7;flex-shrink:0;margin-top:5px;"></div>'
                f'<span>{t}</span></div>'
                for t in tradeoffs
            )
            st.markdown(f"""
<div class="hidden-tradeoffs-card">
  <div class="hidden-tradeoffs-eyebrow">⚠️ Hidden Trade-offs · {rev_industry}</div>
  {tradeoffs_html}
</div>""", unsafe_allow_html=True)

            # Feature 6 — Location Strategy Conclusion
            conclusion_text = generate_location_conclusion(
                company_name_r, rev_industry, why_list, challenge_list,
                water_d, power_d, airport_mins_r, cluster_label_r
            )
            st.markdown(f"""
<div class="conclusion-card">
  <div class="conclusion-eyebrow">🎯 Location Strategy Conclusion</div>
  <div class="conclusion-text">{conclusion_text}</div>
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


# ── BRANDING HEADER ── Lands & Lands · Deep Navy + Gold ─────────────────────────
st.markdown("""
<div style="position:relative;overflow:hidden;border-radius:20px;margin-bottom:1rem;background:linear-gradient(135deg,#0a0e18 0%,#0e1520 50%,#0a0e18 100%);border:1px solid #2a2010;box-shadow:0 8px 48px #00000060;">
  <div style="position:absolute;top:0;left:0;right:0;height:3px;background:linear-gradient(90deg,#3a2a08,#c9a84c,#e2c97a,#c9a84c,#3a2a08);"></div>
  <div style="display:flex;align-items:center;gap:1.5rem;padding:1.2rem 2rem;">
    <div style="flex:1;min-width:0;">
      <div style="font-family:Georgia,serif;font-size:1rem;font-weight:700;color:#c9a84c;letter-spacing:3px;margin-bottom:0.25rem;">LANDS &amp; LANDS</div>
      <div style="font-family:Syne,sans-serif;font-size:1.8rem;font-weight:800;color:#e2c97a;letter-spacing:-0.5px;line-height:1.05;margin-bottom:0.25rem;">Industrial Intelligence Engine</div>
      <div style="font-family:monospace;font-size:0.65rem;color:#5a5040;letter-spacing:0.8px;">AI-powered industrial site selection &amp; cluster intelligence platform</div>
    </div>
    <div style="flex-shrink:0;text-align:right;border-left:1px solid #2a2010;padding-left:1.5rem;">
      <div style="font-family:monospace;font-size:0.52rem;color:#3a2e14;letter-spacing:2.5px;text-transform:uppercase;line-height:2.2;">
        <span style="color:#c9a84c;font-size:0.7rem;font-weight:600;">CBE</span><br>
        Industrial Site<br>Selection Platform<br>
        <span style="color:#c9a84c;font-size:0.6rem;">&#9658; v1.0</span>
      </div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)


# ── HEADER ────────────────────────────────────────────────────────────────────────
st.title("CBE Industrial Intelligence Engine")
st.markdown('<p style="font-family:JetBrains Mono,monospace;font-size:0.72rem;color:#c9a84c40;'
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
                'background:linear-gradient(90deg,#c9a84c,#a07840);-webkit-background-clip:text;'
                '-webkit-text-fill-color:transparent;">⬡ CBE Engine</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-family:JetBrains Mono,monospace;font-size:0.6rem;color:#3a2a10;'
                'letter-spacing:2px;margin-bottom:1rem;">INDUSTRIAL SITE INTELLIGENCE v4 · MAPS EDITION</div>', unsafe_allow_html=True)
    st.divider()

    st.markdown('<span class="sidebar-label">Industry Type</span>', unsafe_allow_html=True)
    industry = st.selectbox("", list(INDUSTRY_DNA.keys()),
                            format_func=lambda x: f"{INDUSTRY_DNA[x]['icon']}  {x}",
                            label_visibility="collapsed")
    dna = INDUSTRY_DNA[industry]
    st.markdown(f'<div style="font-family:JetBrains Mono,monospace;font-size:0.66rem;color:#c9a84c60;'
                f'background:#0a1018;border:1px solid #0c2040;border-radius:8px;padding:0.5rem 0.8rem;'
                f'margin-top:0.4rem;line-height:1.6;">{dna["desc"]}</div>', unsafe_allow_html=True)

    st.divider()
    # ── FEATURE 5: DECISION MODE ──────────────────────────────────────────────
    st.markdown('<span class="sidebar-label">🎯 Decision Mode</span>', unsafe_allow_html=True)
    decision_input = st.text_input(
        "",
        placeholder="e.g. food processing export unit",
        label_visibility="collapsed",
        key="decision_mode_input",
        help="Type your business intent — the engine will auto-adjust scoring weights."
    )
    dm_adjustments, dm_keywords, dm_narrative = parse_decision_mode(decision_input)
    if dm_adjustments:
        st.markdown(
            f'<div style="font-family:JetBrains Mono,monospace;font-size:0.62rem;color:#c9a84c;'
            f'background:#0e0520;border:1px solid #3a1a50;border-radius:8px;padding:0.5rem 0.8rem;'
            f'margin-top:0.3rem;line-height:1.7;">'
            f'🔑 Keywords: {", ".join(dm_keywords)}<br>'
            f'⚖️ {dm_narrative if dm_narrative else "Weights adjusted"}</div>',
            unsafe_allow_html=True
        )
    elif decision_input.strip():
        st.markdown(
            '<div style="font-family:JetBrains Mono,monospace;font-size:0.62rem;color:#3a2a10;'
            'margin-top:0.3rem;">No keywords detected — try: export, agro, manufacturing, cost…</div>',
            unsafe_allow_html=True
        )
    st.divider()
    st.markdown('<span class="sidebar-label">Weight Profile</span>', unsafe_allow_html=True)
    weight_labels = {"Power ⚡":"Power","Airport ✈":"Airport","Water 💧":"Water",
                     "Ecosystem 🏭":"Ecosystem","Workforce 👷":"Workforce","Incentives 🏷️":"Incentive"}
    for label,key in weight_labels.items():
        val = dna["weights"].get(key,0); pct = int(val*100)
        st.markdown(
            f'<div style="display:flex;align-items:center;gap:8px;margin-bottom:5px;">'
            f'<div style="font-family:JetBrains Mono,monospace;font-size:0.6rem;color:#4a6080;width:100px;">{label}</div>'
            f'<div style="flex:1;background:#0d1525;border-radius:4px;height:5px;">'
            f'<div style="width:{pct}%;background:linear-gradient(90deg,#c9a84c,#a07840);height:5px;border-radius:4px;"></div></div>'
            f'<div style="font-family:JetBrains Mono,monospace;font-size:0.6rem;color:#e8e0d0;width:26px;text-align:right;">{pct}%</div>'
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

# Feature 5: Apply Decision Mode weight adjustments if active
if dm_adjustments:
    weights = apply_decision_weights(weights, dm_adjustments)
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


# ── FEATURE 5: DECISION MODE BANNER ──────────────────────────────────────────
if dm_adjustments and dm_narrative:
    adjusted_display = " · ".join(
        f"{k} {'+' if v > 0 else ''}{v*100:.0f}%" for k, v in dm_adjustments.items()
    )
    st.markdown(f"""
<div class="decision-mode-card">
  <div class="decision-eyebrow">🎯 Decision Mode Active · Custom Weight Profile Applied</div>
  <div class="decision-parsed">
    <strong style="color:#c9a84c;">Intent detected:</strong> {', '.join(dm_keywords)}<br>
    <strong style="color:#a07840;">Weight adjustments:</strong> {adjusted_display}<br>
    <strong style="color:#c9a84c;">Effect:</strong> {dm_narrative}
  </div>
</div>""", unsafe_allow_html=True)


# ── FEATURE 1 & 2: WHY THIS LAND WINS + WHAT'S MISSING ──────────────────────
wins_strengths, wins_missing = compute_why_wins_and_missing(winner, df, industry, weights)

feat_col_a, feat_col_b = st.columns(2, gap="large")

with feat_col_a:
    st.markdown('<div class="section-header"><span class="section-icon">🏆</span>'
                '<span class="section-title">Why This Land Wins</span><div class="section-line"></div></div>',
                unsafe_allow_html=True)
    if wins_strengths:
        items_html = "".join(
            f'<div class="wins-item"><div class="wins-dot"></div><span>{s}</span></div>'
            for s in wins_strengths
        )
        st.markdown(f"""
<div class="wins-card">
  <div class="wins-eyebrow">🏆 Top strengths vs all ranked parcels</div>
  {items_html}
</div>""", unsafe_allow_html=True)
    else:
        st.markdown('<div class="wins-card"><div class="wins-eyebrow">🏆 Why This Land Wins</div>'
                    '<div class="wins-item"><span style="color:#4a6080;">Winner beats all parcels across multiple dimensions — see metrics above.</span></div></div>',
                    unsafe_allow_html=True)

with feat_col_b:
    st.markdown('<div class="section-header"><span class="section-icon">⚠️</span>'
                '<span class="section-title">What\'s Missing / Trade-offs</span><div class="section-line"></div></div>',
                unsafe_allow_html=True)
    if wins_missing:
        items_html = "".join(
            f'<div class="missing-item"><div class="missing-dot"></div><span>{m}</span></div>'
            for m in wins_missing
        )
        st.markdown(f"""
<div class="missing-card">
  <div class="missing-eyebrow">⚠️ Gaps vs ideal industry DNA</div>
  {items_html}
</div>""", unsafe_allow_html=True)
    else:
        st.markdown('<div class="missing-card"><div class="missing-eyebrow">⚠️ What\'s Missing</div>'
                    '<div class="missing-item"><span style="color:#4a6080;">No significant gaps vs ideal industry thresholds.</span></div></div>',
                    unsafe_allow_html=True)

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
  <div style="font-family:JetBrains Mono,monospace;font-size:0.72rem;color:#c9a84c;margin-bottom:1rem;">
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
        f'Fetches real <strong style="color:#c9a84c;">{industry}</strong> companies from Google Places, '
        'then reverse-engineers why each location was chosen — using industry-specific reasoning. '
        'Click any company card to instantly run the analysis.</div>',
        unsafe_allow_html=True
    )

    rev_mode = st.radio(
        "Analysis source",
        ["🏢 Real Companies (Google Places)", "📋 Use a ranked parcel", "📍 Enter coordinates manually"],
        key="rev_mode",
        horizontal=True,
        label_visibility="collapsed"
    )

    if rev_mode.startswith("🏢"):
        # ── NEW: Fetch real companies from Google Places ───────────────────
        st.markdown(
            f'<div class="companies-header">🏢 Real {industry} Companies · Google Places API</div>',
            unsafe_allow_html=True
        )

        # Use winner parcel as reference point for nearby search
        ref_lat = winner["lat"]
        ref_lon = winner["lon"]

        if not GMAPS_KEY:
            st.markdown(
                '<div class="no-key-box">⚙️ Set <code>GOOGLE_MAPS_API_KEY</code> in app.py to fetch real companies.</div>',
                unsafe_allow_html=True
            )
        else:
            # Cache companies in session_state per industry to avoid re-fetching on every interaction
            cache_key = f"companies_{industry}"
            if cache_key not in st.session_state:
                with st.spinner(f"Fetching real {industry} companies from Google Places…"):
                    st.session_state[cache_key] = fetch_top_companies(ref_lat, ref_lon, industry, GMAPS_KEY)

            companies = st.session_state[cache_key]

            if not companies:
                st.markdown(
                    '<div class="no-key-box">No companies found. Check your API key or try a different industry.</div>',
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f'<div style="font-family:JetBrains Mono,monospace;font-size:0.65rem;color:#3a2a10;margin-bottom:1rem;">'
                    f'Found {len(companies)} real companies within 15 km · Sorted by rating · Click to analyse</div>',
                    unsafe_allow_html=True
                )

                # Display each company card with a Reverse Analysis button
                for i, company in enumerate(companies):
                    rating_stars = f"⭐ {company['rating']:.1f}" if company['rating'] else "No rating"
                    ind_icon = INDUSTRY_DNA.get(industry, {}).get("icon", "🏭")

                    st.markdown(f"""
<div class="company-card">
  <div style="display:flex;align-items:flex-start;gap:12px;">
    <div style="font-family:'Syne',sans-serif;font-size:1.4rem;font-weight:800;color:#1a2a40;
                width:1.8rem;flex-shrink:0;padding-top:2px;">#{i+1}</div>
    <div style="flex:1;min-width:0;">
      <div class="company-name">{ind_icon} {company['name']}</div>
      <div class="company-meta">
        📍 {company['vicinity']}<br>
        {rating_stars} &nbsp;·&nbsp; 📏 {company['dist_km']:.1f} km from reference &nbsp;·&nbsp;
        🔑 Found via: <em>{company['search_kw']}</em>
      </div>
    </div>
  </div>
</div>""", unsafe_allow_html=True)

                    btn_key = f"rev_company_btn_{i}_{industry}"
                    if st.button(f"🔍 Reverse Location Analysis — {company['name']}", key=btn_key):
                        st.session_state[f"selected_company_{industry}"] = i

                # Run analysis for the selected company
                selected_key = f"selected_company_{industry}"
                if selected_key in st.session_state:
                    sel_idx = st.session_state[selected_key]
                    if 0 <= sel_idx < len(companies):
                        sel_company = companies[sel_idx]
                        st.divider()
                        st.markdown(
                            f'<div style="font-family:JetBrains Mono,monospace;font-size:0.72rem;'
                            f'color:#a07840;margin-bottom:0.5rem;">📊 Analysing: '
                            f'<strong style="color:#fff;">{sel_company["name"]}</strong>'
                            f' · {sel_company["vicinity"]}</div>',
                            unsafe_allow_html=True
                        )
                        render_reverse_analysis(
                            api_key=GMAPS_KEY,
                            company_row={
                                "lat": sel_company["lat"],
                                "lon": sel_company["lon"],
                                "name": sel_company["name"],
                            },
                            selected_industry=industry
                        )

                # Button to refresh company list
                if st.button("🔄 Refresh Company List", key="refresh_companies"):
                    if cache_key in st.session_state:
                        del st.session_state[cache_key]
                    if f"selected_company_{industry}" in st.session_state:
                        del st.session_state[f"selected_company_{industry}"]
                    st.rerun()

    elif rev_mode.startswith("📋"):
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


# ── FEATURE 4: COMPARE TOP 3 LANDS ───────────────────────────────────────────
st.markdown('<div class="section-header"><span class="section-icon">📊</span>'
            '<span class="section-title">Compare Top 3 Lands</span><div class="section-line"></div></div>',
            unsafe_allow_html=True)

top3 = df.head(min(3, len(df))).copy()

def _cls3(vals, col_series, higher_is_better=False):
    """Return CSS class for top/mid/worst value in a list of 3."""
    if len(vals) < 2:
        return ["compare-val-best"] * len(vals)
    if higher_is_better:
        sorted_v = sorted(vals, reverse=True)
    else:
        sorted_v = sorted(vals)
    classes = []
    for v in vals:
        if v == sorted_v[0]:
            classes.append("compare-val-best")
        elif len(sorted_v) > 2 and v == sorted_v[-1]:
            classes.append("compare-val-worst")
        else:
            classes.append("compare-val-mid")
    return classes

water_vals  = [r["water_dist"]    for _, r in top3.iterrows()]
power_vals  = [r["power_dist"]    for _, r in top3.iterrows()]
hwy_vals    = [r["highway_dist"]  for _, r in top3.iterrows()]
eco_vals    = [r["ecosystem"]     for _, r in top3.iterrows()]
wf_vals     = [r["workforce_score"] for _, r in top3.iterrows()]
airport_vals= [r["airport_dist"]  for _, r in top3.iterrows()]
icd_vals    = [r["icd_dist"]      for _, r in top3.iterrows()]

water_cls   = _cls3(water_vals,  None, higher_is_better=False)
power_cls   = _cls3(power_vals,  None, higher_is_better=False)
hwy_cls     = _cls3(hwy_vals,    None, higher_is_better=False)
eco_cls3    = _cls3(eco_vals,    None, higher_is_better=True)
wf_cls      = _cls3(wf_vals,     None, higher_is_better=True)
airport_cls = _cls3(airport_vals,None, higher_is_better=False)
icd_cls     = _cls3(icd_vals,    None, higher_is_better=False)

rows_html = ""
rank_labels = ["🥇 #1 Winner", "🥈 #2", "🥉 #3"]
for i, (_, r) in enumerate(top3.iterrows()):
    row_class = "winner-row" if i == 0 else ""
    score_pct3 = max(0, min(100, int((1 - r["final_score"]) * 100)))
    rows_html += f"""
<tr class="{row_class}">
  <td><strong>{rank_labels[i]}</strong><br>
    <span style="font-size:0.65rem;color:#4a6080;">{r[area_col]}</span><br>
    <span style="font-size:0.6rem;color:#c9a84c;">{score_pct3}/100</span>
  </td>
  <td class="{water_cls[i]}">{r['water_dist']:.1f} km</td>
  <td class="{power_cls[i]}">{r['power_dist']:.1f} km</td>
  <td class="{hwy_cls[i]}">{r['highway_dist']:.1f} km</td>
  <td class="{airport_cls[i]}">{r['airport_dist']:.1f} km</td>
  <td class="{icd_cls[i]}">{r['icd_dist']:.1f} km</td>
  <td class="{eco_cls3[i]}">{int(r['ecosystem'])} pts</td>
  <td class="{wf_cls[i]}">{r['workforce_score']:.2f}</td>
</tr>"""

st.markdown(f"""
<div class="compare-table-card">
  <div class="compare-header">📊 Side-by-Side Comparison · Top 3 Ranked Parcels · Green = Best · Orange = Weakest</div>
  <table class="compare-table">
    <thead>
      <tr>
        <th>Parcel</th>
        <th>💧 Water</th>
        <th>⚡ Power</th>
        <th>🛣️ Highway</th>
        <th>✈️ Airport</th>
        <th>🚢 ICD Port</th>
        <th>🏭 Ecosystem</th>
        <th>👷 Workforce</th>
      </tr>
    </thead>
    <tbody>
      {rows_html}
    </tbody>
  </table>
</div>""", unsafe_allow_html=True)

# ── Recommendation by use-case ────────────────────────────────────────────────
def _best_for(top3_df, area_col, priority_cols, higher_is_better_flags):
    """Return name of parcel that scores best on given priority columns."""
    scores = []
    for _, r in top3_df.iterrows():
        s = 0
        for col, hib in zip(priority_cols, higher_is_better_flags):
            if col in r.index:
                s += (r[col] if hib else -r[col])
        scores.append(s)
    best_idx = scores.index(max(scores))
    return top3_df.iloc[best_idx][area_col]

prod_best   = _best_for(top3, area_col, ["power_dist", "water_dist"], [False, False])
export_best = _best_for(top3, area_col, ["airport_dist", "icd_dist"], [False, False])
cost_best   = _best_for(top3, area_col, ["incentive_score", "workforce_score"], [True, True])

st.markdown(f"""
<div class="recommend-row">
  <div class="recommend-pill">
    <strong>⚙️ Best for Production-Heavy</strong>
    {prod_best} — closest to power & water; ideal for high-throughput manufacturing ops
  </div>
  <div class="recommend-pill">
    <strong>✈️ Best for Export-Heavy</strong>
    {export_best} — shortest combined airport + ICD distance; fastest cargo turnaround
  </div>
  <div class="recommend-pill">
    <strong>💰 Best for Cost-Sensitive</strong>
    {cost_best} — highest incentive + workforce score combination; lower opex baseline
  </div>
</div>""", unsafe_allow_html=True)

st.divider()


# ── FEATURE 3: CLUSTER STRATEGY INSIGHT ──────────────────────────────────────
# (Rendered after ecosystem scan is triggered — injected via session state)
st.markdown('<div class="section-header"><span class="section-icon">🧠</span>'
            '<span class="section-title">Cluster Strategy Insight</span><div class="section-line"></div></div>',
            unsafe_allow_html=True)

if "live_places_df" in st.session_state and not st.session_state["live_places_df"].empty:
    # Reuse companies fetched by ecosystem scan (stored in session_state)
    cache_key_cs = f"companies_{industry}"
    companies_for_cluster = st.session_state.get(cache_key_cs, [])
    water_ll = list(zip(water["latitude"], water["longitude"])) if water is not None and not water.empty else []
    cluster_stats, cluster_insight = compute_cluster_strategy_insight(
        companies_for_cluster, winner["lat"], winner["lon"], industry,
        substations, icd_points, highway_coords, water_ll
    )

    if cluster_stats:
        def fmt_stat(v, unit="km"):
            return f"{v:.1f} {unit}" if v is not None else "N/A"

        stat_html = f"""
<div class="cluster-stat-grid">
  <div class="cluster-stat">
    <div class="cluster-stat-label">Avg Highway Dist</div>
    <div class="cluster-stat-val">{fmt_stat(cluster_stats.get('avg_highway_km'))}</div>
  </div>
  <div class="cluster-stat">
    <div class="cluster-stat-label">Avg Water Dist</div>
    <div class="cluster-stat-val">{fmt_stat(cluster_stats.get('avg_water_km'))}</div>
  </div>
  <div class="cluster-stat">
    <div class="cluster-stat-label">Avg Airport Dist</div>
    <div class="cluster-stat-val">{fmt_stat(cluster_stats.get('avg_airport_km'))}</div>
  </div>
  <div class="cluster-stat">
    <div class="cluster-stat-label">Companies Scanned</div>
    <div class="cluster-stat-val">{cluster_stats.get('total_companies', 0)}</div>
  </div>
</div>"""

        st.markdown(f"""
<div class="cluster-insight-card">
  <div class="cluster-insight-eyebrow">🧠 Cluster Strategy Insight · {industry} · Based on {cluster_stats.get('total_companies', 0)} live companies</div>
  {stat_html}
  <div class="cluster-insight-text">{cluster_insight if cluster_insight else "Run the Live Ecosystem Scan to generate cluster strategy data."}</div>
</div>""", unsafe_allow_html=True)
    else:
        st.markdown("""
<div class="cluster-insight-card">
  <div class="cluster-insight-eyebrow">🧠 Cluster Strategy Insight</div>
  <div class="cluster-insight-text">No company data loaded yet. Run the <strong>Live Ecosystem Scan</strong> in the Google Maps Intelligence tab to generate cluster insights.</div>
</div>""", unsafe_allow_html=True)
else:
    st.markdown("""
<div class="cluster-insight-card">
  <div class="cluster-insight-eyebrow">🧠 Cluster Strategy Insight · Awaiting Live Data</div>
  <div class="cluster-insight-text">
    Run the <strong style="color:#a07840;">Live Ecosystem Scan</strong> (Google Maps Intelligence → 📍 Live Ecosystem Scan) to unlock cluster strategy analysis.
    The engine will compute avg distances to highway, water and airport across all detected companies,
    then generate a data-driven insight into the location logic of this industry cluster.
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

# ── Live Places layer (from ecosystem scan if run) ────────────────────────────
if "live_places_df" in st.session_state and not st.session_state["live_places_df"].empty:
    layers.append(pdk.Layer("ScatterplotLayer",
        data=st.session_state["live_places_df"],
        get_position="[lon,lat]",get_color="color",get_radius="radius",pickable=True))

tooltip={"html":'<div style="font-family:JetBrains Mono,monospace;font-size:11px;background:#0d1525;'
                'color:#e8e0d0;border:1px solid #3a2a10;border-radius:8px;padding:10px 14px;'
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
<div style="font-family:JetBrains Mono,monospace;font-size:0.65rem;color:#3a2a10;margin-top:0.5rem;">
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
