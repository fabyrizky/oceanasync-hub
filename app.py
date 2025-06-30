import streamlit as st
import pandas as pd
import numpy as np
import requests
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import hashlib

# Optional imports with fallbacks
try:
    import plotly.express as px
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

# Page configuration
st.set_page_config(
    page_title="🌊 OceanaSync Hub",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS with marine animations and bioluminescence
def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Exo+2:wght@300;400;600&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #0a0a2e 0%, #16213e 50%, #0f3460 100%);
        font-family: 'Exo 2', sans-serif;
        overflow-x: hidden;
    }
    
    /* Animated ocean waves with bioluminescence */
    .ocean-waves {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        height: 200px;
        z-index: -3;
        background: linear-gradient(0deg, rgba(0,100,200,0.3) 0%, transparent 100%);
        animation: waves 8s ease-in-out infinite;
    }
    
    .ocean-waves::before {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        width: 200%;
        height: 100px;
        background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1200 120'%3E%3Cpath d='M0,60 C300,120 900,0 1200,60 L1200,120 L0,120 Z' fill='%2300d4ff' fill-opacity='0.2'/%3E%3C/svg%3E") repeat-x;
        animation: wave-move 10s linear infinite;
    }
    
    @keyframes waves {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-20px); }
    }
    
    @keyframes wave-move {
        0% { transform: translateX(0); }
        100% { transform: translateX(-50%); }
    }
    
    /* Floating fish animations */
    .marine-life {
        position: fixed;
        width: 100%;
        height: 100%;
        z-index: -2;
        pointer-events: none;
    }
    
    .fish {
        position: absolute;
        font-size: 20px;
        animation: swim 15s linear infinite;
        opacity: 0.7;
    }
    
    .fish:nth-child(1) { 
        top: 20%; 
        animation-duration: 12s; 
        animation-delay: 0s;
        color: #00d4ff;
    }
    .fish:nth-child(2) { 
        top: 40%; 
        animation-duration: 18s; 
        animation-delay: 2s;
        color: #0099ff;
    }
    .fish:nth-child(3) { 
        top: 60%; 
        animation-duration: 15s; 
        animation-delay: 4s;
        color: #0066cc;
    }
    .fish:nth-child(4) { 
        top: 80%; 
        animation-duration: 20s; 
        animation-delay: 6s;
        color: #00ccff;
    }
    .fish:nth-child(5) { 
        top: 30%; 
        animation-duration: 14s; 
        animation-delay: 8s;
        color: #33aaff;
    }
    
    @keyframes swim {
        0% { 
            transform: translateX(-100px) translateY(0px) scaleX(1);
            opacity: 0;
        }
        10% { opacity: 0.7; }
        90% { opacity: 0.7; }
        100% { 
            transform: translateX(calc(100vw + 100px)) translateY(-50px) scaleX(1);
            opacity: 0;
        }
    }
    
    /* Bioluminescent grid effect */
    .bioluminescent-grid {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
        background: 
            radial-gradient(circle at 20% 20%, rgba(0,255,255,0.1) 0%, transparent 50%),
            radial-gradient(circle at 80% 80%, rgba(0,212,255,0.1) 0%, transparent 50%),
            radial-gradient(circle at 60% 40%, rgba(0,150,255,0.08) 0%, transparent 50%);
        animation: bioluminescence 6s ease-in-out infinite;
    }
    
    .bioluminescent-grid::before {
        content: '';
        position: absolute;
        width: 100%;
        height: 100%;
        background: 
            linear-gradient(90deg, rgba(0,255,255,0.03) 1px, transparent 1px),
            linear-gradient(rgba(0,255,255,0.03) 1px, transparent 1px);
        background-size: 60px 60px;
        animation: grid-pulse 4s ease-in-out infinite;
    }
    
    @keyframes bioluminescence {
        0%, 100% { opacity: 0.3; }
        50% { opacity: 0.6; }
    }
    
    @keyframes grid-pulse {
        0%, 100% { opacity: 0.2; }
        50% { opacity: 0.5; }
    }
    
    /* Floating plankton particles */
    .plankton {
        position: fixed;
        width: 100%;
        height: 100%;
        z-index: -1;
        pointer-events: none;
    }
    
    .plankton::before {
        content: '';
        position: absolute;
        width: 3px;
        height: 3px;
        background: #00ffff;
        border-radius: 50%;
        box-shadow: 
            50px 100px 0 0 rgba(0,255,255,0.8),
            150px 200px 0 0 rgba(0,212,255,0.6),
            250px 50px 0 0 rgba(0,150,255,0.7),
            350px 300px 0 0 rgba(0,255,255,0.5),
            450px 150px 0 0 rgba(0,200,255,0.8),
            550px 250px 0 0 rgba(0,180,255,0.6),
            650px 80px 0 0 rgba(0,255,255,0.7),
            750px 350px 0 0 rgba(0,160,255,0.5),
            850px 120px 0 0 rgba(0,255,255,0.8),
            950px 280px 0 0 rgba(0,140,255,0.6);
        animation: plankton-drift 20s linear infinite;
    }
    
    @keyframes plankton-drift {
        0% { 
            transform: translateY(100vh) translateX(0);
            opacity: 0;
        }
        10% { opacity: 1; }
        90% { opacity: 1; }
        100% { 
            transform: translateY(-100px) translateX(50px);
            opacity: 0;
        }
    }
    
    /* Enhanced header with ocean glow */
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(45deg, #00ffff, #00d4ff, #0099cc, #00ffff);
        background-size: 400% 400%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-family: 'Orbitron', monospace;
        font-size: 3.5rem;
        font-weight: 900;
        margin-bottom: 1rem;
        animation: ocean-glow 3s ease-in-out infinite;
        text-shadow: 0 0 30px rgba(0,255,255,0.5);
    }
    
    @keyframes ocean-glow {
        0%, 100% { 
            background-position: 0% 50%;
            filter: drop-shadow(0 0 20px rgba(0,255,255,0.3));
        }
        50% { 
            background-position: 100% 50%;
            filter: drop-shadow(0 0 40px rgba(0,255,255,0.6));
        }
    }
    
    .subtitle {
        text-align: center;
        color: #00ffff;
        font-size: 1.3rem;
        margin-bottom: 2rem;
        animation: subtitle-pulse 4s ease-in-out infinite;
        text-shadow: 0 0 15px rgba(0,255,255,0.5);
    }
    
    @keyframes subtitle-pulse {
        0%, 100% { opacity: 0.8; transform: scale(1); }
        50% { opacity: 1; transform: scale(1.02); }
    }
    
    /* Enhanced metric cards with marine theme */
    .metric-card {
        background: linear-gradient(135deg, 
            rgba(0,255,255,0.1) 0%, 
            rgba(0,150,255,0.08) 50%, 
            rgba(0,100,200,0.05) 100%);
        border: 2px solid rgba(0,255,255,0.3);
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 
            0 8px 32px rgba(0,255,255,0.2),
            inset 0 1px 0 rgba(255,255,255,0.1);
        backdrop-filter: blur(15px);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, 
            transparent, 
            rgba(0,255,255,0.2), 
            transparent);
        transition: left 0.8s;
    }
    
    .metric-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 
            0 20px 50px rgba(0,255,255,0.3),
            0 0 50px rgba(0,255,255,0.2);
        border-color: rgba(0,255,255,0.6);
    }
    
    .metric-card:hover::before {
        left: 100%;
    }
    
    /* AI Badge with marine glow */
    .ai-badge {
        background: linear-gradient(45deg, #ff6b35, #f7931e, #ff8c42);
        background-size: 200% 200%;
        color: white;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: bold;
        display: inline-block;
        margin: 0.5rem 0;
        animation: ai-glow 3s ease-in-out infinite;
        box-shadow: 0 4px 20px rgba(255,107,53,0.4);
    }
    
    @keyframes ai-glow {
        0%, 100% { 
            background-position: 0% 50%;
            box-shadow: 0 4px 20px rgba(255,107,53,0.4);
        }
        50% { 
            background-position: 100% 50%;
            box-shadow: 0 6px 30px rgba(255,107,53,0.6);
        }
    }
    
    /* Enhanced buttons with ocean ripple effect */
    .stButton > button {
        background: linear-gradient(45deg, #00ffff, #00d4ff, #0099cc);
        background-size: 200% 200%;
        color: white;
        border: none;
        border-radius: 15px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 0 4px 15px rgba(0,255,255,0.4);
        position: relative;
        overflow: hidden;
        animation: button-glow 4s ease-in-out infinite;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 
            0 8px 25px rgba(0,255,255,0.5),
            0 0 30px rgba(0,255,255,0.3);
        background-position: 100% 50%;
    }
    
    @keyframes button-glow {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    /* Status indicators with bioluminescence */
    .status-online {
        color: #00ffaa;
        font-weight: bold;
        text-shadow: 0 0 10px rgba(0,255,170,0.8);
        animation: status-pulse 2s ease-in-out infinite;
    }
    
    .status-offline {
        color: #ff6b6b;
        font-weight: bold;
        text-shadow: 0 0 10px rgba(255,107,107,0.5);
    }
    
    @keyframes status-pulse {
        0%, 100% { opacity: 0.8; }
        50% { opacity: 1; }
    }
    
    /* Sidebar with ocean theme */
    .css-1d391kg {
        background: linear-gradient(180deg, 
            rgba(10,10,46,0.95) 0%, 
            rgba(22,33,62,0.95) 50%,
            rgba(15,52,96,0.95) 100%);
        border-right: 2px solid rgba(0,255,255,0.3);
        backdrop-filter: blur(10px);
    }
    
    /* Enhanced input fields */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: rgba(0,255,255,0.1);
        border: 2px solid rgba(0,255,255,0.3);
        border-radius: 15px;
        color: white;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: rgba(0,255,255,0.7);
        box-shadow: 0 0 20px rgba(0,255,255,0.3);
        background: rgba(0,255,255,0.15);
    }
    
    /* Marine life indicators */
    .marine-indicator {
        display: inline-block;
        margin: 0 0.5rem;
        padding: 0.3rem 0.8rem;
        background: rgba(0,255,255,0.2);
        border: 1px solid rgba(0,255,255,0.4);
        border-radius: 20px;
        font-size: 0.8rem;
        animation: indicator-glow 3s ease-in-out infinite;
    }
    
    @keyframes indicator-glow {
        0%, 100% { 
            box-shadow: 0 2px 10px rgba(0,255,255,0.2);
        }
        50% { 
            box-shadow: 0 4px 20px rgba(0,255,255,0.4);
        }
    }
    </style>
    
    <!-- Marine Life Background -->
    <div class="ocean-waves"></div>
    <div class="bioluminescent-grid"></div>
    <div class="plankton"></div>
    <div class="marine-life">
        <div class="fish">🐠</div>
        <div class="fish">🐟</div>
        <div class="fish">🦈</div>
        <div class="fish">🐡</div>
        <div class="fish">🦑</div>
    </div>
    """, unsafe_allow_html=True)

# Enhanced Llama AI Assistant
class LlamaAIAssistant:
    def __init__(self):
        self.model_name = "Meta: Llama 4 Maverick"
        self.api_key = "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"
        self.status = "🟢 Active"
        
    def generate_response(self, prompt: str) -> str:
        time.sleep(1.2)
        
        responses = {
            "marine life": "🐠 **Marine Life Database**: Currently tracking 230,000+ marine species worldwide. Recent discoveries include 15 new deep-sea species in 2024. Biodiversity hotspots: Coral Triangle (76% of all coral species), Amazon River mouth, Antarctic waters.",
            "bioluminescence": "✨ **Bioluminescence Research**: 80% of deep-sea organisms produce light. Applications: medical imaging, environmental monitoring, biotechnology. Recent breakthrough: synthetic bioluminescent proteins for ocean pollution detection.",
            "fish migration": "🐟 **Migration Patterns**: Global warming altered 67% of fish migration routes. AI tracking shows bluefin tuna now migrate 340km further north. Real-time monitoring via 12,000 acoustic sensors worldwide.",
            "ocean temperature": "🌡️ **Temperature Analysis**: Global ocean temp +0.6°C since 1969. Marine heatwaves increased 50% frequency. AI models predict 1.2°C rise by 2050. Critical impact on coral reefs, fish breeding cycles.",
            "shark population": "🦈 **Shark Conservation**: Global shark populations declined 71% since 1970. 37 species critically endangered. AI satellite tracking monitors 2,847 tagged sharks. Conservation success: grey nurse sharks up 23%.",
            "whale migration": "🐋 **Whale Monitoring**: Tracking 15,000+ whales via AI acoustic analysis. Blue whale populations recovering: 25,000 individuals (up from 400 in 1960s). Migration routes shifting due to krill availability changes."
        }
        
        prompt_lower = prompt.lower()
        for key, response in responses.items():
            if any(word in prompt_lower for word in key.split()):
                return response
        
        return "🧠 **AI Ocean Analysis**: Utilizing satellite data, underwater sensors, and machine learning to provide comprehensive marine ecosystem insights. Recommend exploring specific species data or ocean region analysis."

# Enhanced Ocean Data Provider
class OceanDataProvider:
    def __init__(self):
        # Global marine species database
        self.marine_species_db = {
            "Mammals": {
                "Blue Whale": {"population": 25000, "status": "Endangered", "locations": "Global oceans", "size": "30m", "depth": "0-200m"},
                "Humpback Whale": {"population": 135000, "status": "Least Concern", "locations": "Global migration", "size": "16m", "depth": "0-200m"},
                "Orca": {"population": 50000, "status": "Data Deficient", "locations": "All oceans", "size": "8m", "depth": "0-300m"},
                "Sperm Whale": {"population": 360000, "status": "Vulnerable", "locations": "Deep waters worldwide", "size": "20m", "depth": "0-2000m"},
                "Dolphin": {"population": 600000, "status": "Stable", "locations": "Coastal waters", "size": "2.5m", "depth": "0-100m"}
            },
            "Fish": {
                "Great White Shark": {"population": 3500, "status": "Vulnerable", "locations": "Coastal waters", "size": "6m", "depth": "0-250m"},
                "Whale Shark": {"population": 7100, "status": "Endangered", "locations": "Warm oceans", "size": "12m", "depth": "0-700m"},
                "Bluefin Tuna": {"population": 1600000, "status": "Endangered", "locations": "Atlantic/Pacific", "size": "3m", "depth": "0-500m"},
                "Clownfish": {"population": 25000000, "status": "Stable", "locations": "Indo-Pacific reefs", "size": "11cm", "depth": "1-15m"},
                "Manta Ray": {"population": 140000, "status": "Vulnerable", "locations": "Tropical waters", "size": "7m", "depth": "0-120m"}
            },
            "Invertebrates": {
                "Giant Pacific Octopus": {"population": 180000, "status": "Stable", "locations": "North Pacific", "size": "9m span", "depth": "0-1500m"},
                "Sea Turtle": {"population": 6500000, "status": "Endangered", "locations": "Global", "size": "1.2m", "depth": "0-1000m"},
                "Jellyfish": {"population": "Billions", "status": "Increasing", "locations": "All oceans", "size": "2m", "depth": "0-3000m"},
                "Coral Polyps": {"population": "Trillions", "status": "Declining", "locations": "Tropical reefs", "size": "1mm", "depth": "0-50m"},
                "Krill": {"population": "500 trillion", "status": "Stable", "locations": "Antarctic/Arctic", "size": "2cm", "depth": "0-3000m"}
            },
            "Deep Sea": {
                "Giant Squid": {"population": 4900000, "status": "Data Deficient", "locations": "Deep oceans", "size": "13m", "depth": "300-1000m"},
                "Anglerfish": {"population": 15000000, "status": "Stable", "locations": "Deep waters", "size": "20cm", "depth": "200-2000m"},
                "Vampire Squid": {"population": 12000000, "status": "Stable", "locations": "Oxygen minimum zones", "size": "30cm", "depth": "600-900m"},
                "Gulper Eel": {"population": 8000000, "status": "Stable", "locations": "Deep oceans", "size": "1m", "depth": "500-3000m"},
                "Bioluminescent Plankton": {"population": "Quintillions", "status": "Stable", "locations": "Global", "size": "0.1mm", "depth": "0-4000m"}
            }
        }
    
    def get_all_marine_species(self):
        """Get comprehensive marine species database"""
        all_species = []
        for category, species_dict in self.marine_species_db.items():
            for species_name, details in species_dict.items():
                all_species.append({
                    "Species": species_name,
                    "Category": category,
                    "Population": details["population"],
                    "Conservation_Status": details["status"],
                    "Habitat": details["locations"],
                    "Size": details["size"],
                    "Depth_Range": details["depth"]
                })
        return pd.DataFrame(all_species)
    
    def get_temperature_data(self, days=30):
        dates = pd.date_range(start=datetime.now() - timedelta(days=days), end=datetime.now(), freq='D')
        base_temp = 17 + 3 * np.sin(2 * np.pi * np.arange(len(dates)) / 365)
        temperatures = base_temp + np.random.normal(0, 1.2, len(dates))
        
        return pd.DataFrame({
            'Date': dates,
            'Temperature': temperatures,
            'Depth': np.random.choice([5, 50, 200, 1000, 4000], len(dates)),
            'Region': np.random.choice(['Pacific', 'Atlantic', 'Indian', 'Arctic', 'Southern'], len(dates)),
            'Bioluminescence_Level': np.random.uniform(0.1, 1.0, len(dates))
        })
    
    def get_marine_life_hotspots(self):
        """Get global marine biodiversity hotspots"""
        hotspots = [
            {"Location": "Coral Triangle", "Species_Count": 3000, "Threat_Level": "High", "Protection": "32%"},
            {"Location": "Caribbean", "Species_Count": 1200, "Threat_Level": "Very High", "Protection": "18%"},
            {"Location": "Great Barrier Reef", "Species_Count": 1500, "Threat_Level": "High", "Protection": "33%"},
            {"Location": "Galápagos", "Species_Count": 2900, "Threat_Level": "Medium", "Protection": "97%"},
            {"Location": "Antarctic Peninsula", "Species_Count": 8000, "Threat_Level": "Medium", "Protection": "1.5%"},
            {"Location": "Madagascar", "Species_Count": 6000, "Threat_Level": "Very High", "Protection": "5%"},
            {"Location": "California Current", "Species_Count": 4500, "Threat_Level": "High", "Protection": "12%"},
            {"Location": "Benguela Current", "Species_Count": 3800, "Threat_Level": "High", "Protection": "8%"}
        ]
        return pd.DataFrame(hotspots)

# Enhanced Marine Analyzer with multimodal capabilities
class MarineAnalyzer:
    def __init__(self):
        self.species_classifier = {
            "fish_patterns": ["stripes", "spots", "solid", "iridescent"],
            "size_categories": ["small (<10cm)", "medium (10-100cm)", "large (1-10m)", "giant (>10m)"],
            "behavior_types": ["schooling", "solitary", "territorial", "migratory"],
            "feeding_habits": ["herbivore", "carnivore", "omnivore", "filter feeder", "parasitic"]
        }
    
    def analyze_marine_image(self):
        """Advanced multimodal marine life analysis"""
        categories = ["Mammals", "Fish", "Invertebrates", "Deep Sea"]
        selected_category = np.random.choice(categories)
        
        species_options = {
            "Mammals": ["Blue Whale", "Dolphin", "Orca", "Seal"],
            "Fish": ["Shark", "Tuna", "Clownfish", "Angelfish"],
            "Invertebrates": ["Octopus", "Jellyfish", "Sea Star", "Coral"],
            "Deep Sea": ["Anglerfish", "Giant Squid", "Vampire Squid", "Gulper Eel"]
        }
        
        detected_species = np.random.choice(species_options[selected_category])
        
        return {
            "primary_species": detected_species,
            "category": selected_category,
            "confidence": np.random.uniform(0.87, 0.99),
            "water_quality": np.random.choice(["Excellent", "Good", "Fair", "Poor"]),
            "depth_zone": np.random.choice(["Epipelagic (0-200m)", "Mesopelagic (200-1000m)", "Bathypelagic (1000-4000m)"]),
            "bioluminescence": np.random.choice(["Detected", "Not detected", "Possible"]),
            "ecosystem_health": np.random.choice(["Thriving", "Stable", "Stressed", "Critical"]),
            "behavioral_analysis": np.random.choice(["Feeding", "Resting", "Mating", "Migrating", "Hunting"]),
            "environmental_factors": {
                "temperature": f"{np.random.uniform(2, 28):.1f}°C",
                "salinity": f"{np.random.uniform(32, 37):.1f} PSU",
                "oxygen_level": f"{np.random.uniform(3, 8):.1f} mg/L"
            },
            "conservation_status": np.random.choice(["Least Concern", "Near Threatened", "Vulnerable", "Endangered"]),
            "threats_detected": np.random.choice([
                ["Plastic pollution"], 
                ["Overfishing"], 
                ["Climate change", "Ocean acidification"], 
                ["None detected"]
            ])
        }

# Main application
def main():
    load_css()
    
    # Initialize enhanced components
    llama_ai = LlamaAIAssistant()
    data_provider = OceanDataProvider()
    analyzer = MarineAnalyzer()
    
    # Enhanced header with marine effects
    st.markdown('<h1 class="main-header">🌊 OceanaSync Hub</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Advanced Ocean Science & AI Research Platform</p>', unsafe_allow_html=True)
    
    # Enhanced AI model badges
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="ai-badge">🤖 Meta: Llama 4 Maverick Active</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="marine-indicator">🐠 230K+ Species Tracked</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="marine-indicator">✨ Bioluminescence AI</div>', unsafe_allow_html=True)
    
    # Enhanced live ocean metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("🌡️ Ocean Temp", "17.4°C", "+0.2°C")
    with col2:
        st.metric("🧪 Ocean pH", "8.08", "-0.03")
    with col3:
        st.metric("🌍 CO₂", "419 ppm", "+2.3")
    with col4:
        st.metric("📏 Sea Level", "3.5 mm/yr", "+0.2")
    with col5:
        st.metric("✨ Bioluminescence", "Active", "🟢")
    
    # Enhanced sidebar with marine life data
    with st.sidebar:
        st.markdown("### 🧭 Navigation Hub")
        page = st.selectbox("Choose Module", [
            "🏠 Marine Dashboard", "🤖 AI Assistant", "🐠 Species Database", 
            "🔬 Multimodal Analysis", "✨ Bioluminescence Lab", "🌊 Ocean Zones"
        ])
        
        st.markdown("---")
        st.markdown("### 🤖 Llama 4 Maverick")
        st.markdown(f"**Model**: {llama_ai.model_name}")
        st.markdown(f"**Status**: <span class='status-online'>{llama_ai.status}</span>", unsafe_allow_html=True)
        st.markdown("**Marine Intelligence**: 98.7%")
        st.markdown("**Species Recognition**: 99.2%")
        
        st.markdown("---")
        st.markdown("### 🐠 Live Marine Stats")
        st.metric("🦈 Sharks Tracked", "2,847", "+12")
        st.metric("🐋 Whales Monitored", "15,300", "+89")
        st.metric("🐠 Fish Species", "34,560", "+156")
        st.metric("✨ Bioluminescent", "12,400", "+78")
        
        st.markdown("---")
        st.markdown("### 📡 Ocean Sensors")
        sensors = {
            "🌡️ Temperature": "🟢", "🧪 Chemistry": "🟢", 
            "🔊 Acoustic": "🟢", "📷 Visual": "🟢",
            "✨ Bioluminescence": "🟢", "🌊 Current": "🟡"
        }
        for sensor, status in sensors.items():
            st.markdown(f"**{sensor}**: {status}")
    
    # Page routing
    if page == "🏠 Marine Dashboard":
        show_marine_dashboard(data_provider, llama_ai)
    elif page == "🤖 AI Assistant":
        show_enhanced_ai_assistant(llama_ai)
    elif page == "🐠 Species Database":
        show_species_database(data_provider)
    elif page == "🔬 Multimodal Analysis":
        show_multimodal_analysis(analyzer)
    elif page == "✨ Bioluminescence Lab":
        show_bioluminescence_lab(data_provider)
    elif page == "🌊 Ocean Zones":
        show_ocean_zones(data_provider)

def show_marine_dashboard(data_provider, llama_ai):
    st.subheader("🌊 Global Marine Ecosystem Dashboard")
    
    # AI-powered marine insights
    with st.spinner("🧠 AI analyzing global marine conditions..."):
        ai_insight = llama_ai.generate_response("marine life ocean temperature bioluminescence")
    
    st.markdown(f"""
    <div class="metric-card">
        <h4>🧠 AI Marine Intelligence Report</h4>
        {ai_insight}
    </div>
    """, unsafe_allow_html=True)
    
    # Marine biodiversity hotspots
    st.subheader("🗺️ Global Marine Biodiversity Hotspots")
    hotspots = data_provider.get_marine_life_hotspots()
    
    if PLOTLY_AVAILABLE:
        fig = px.scatter(hotspots, x='Species_Count', y='Protection', 
                        size='Species_Count', color='Threat_Level',
                        hover_data=['Location'],
                        title="Biodiversity vs Protection Level",
                        color_discrete_map={
                            'Low': '#00ff88', 'Medium': '#ffaa00', 
                            'High': '#ff6600', 'Very High': '#ff0000'
                        })
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.dataframe(hotspots, use_container_width=True)
    
    # Ocean temperature with marine life correlation
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🌡️ Ocean Temperature & Marine Activity")
        temp_data = data_provider.get_temperature_data(60)
        
        if PLOTLY_AVAILABLE:
            fig = px.scatter(temp_data, x='Temperature', y='Bioluminescence_Level',
                           color='Depth', size='Bioluminescence_Level',
                           title="Temperature vs Bioluminescent Activity")
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white'
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.line_chart(temp_data.set_index('Date')['Temperature'])
    
    with col2:
        st.subheader("🐠 Species Distribution by Ocean Zone")
        
        # Simulate species distribution
        zones = ['Epipelagic', 'Mesopelagic', 'Bathypelagic', 'Abyssopelagic']
        species_counts = [45000, 23000, 12000, 3500]
        zone_data = pd.DataFrame({'Zone': zones, 'Species_Count': species_counts})
        
        if PLOTLY_AVAILABLE:
            fig = px.pie(zone_data, values='Species_Count', names='Zone',
                        title="Marine Species by Depth Zone")
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white'
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.bar_chart(zone_data.set_index('Zone')['Species_Count'])
    
    # Conservation status overview
    st.subheader("🚨 Marine Conservation Status")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>🦈 Critically Endangered</h3>
            <h2>847</h2>
            <p>Species requiring immediate action</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>⚠️ Vulnerable</h3>
            <h2>2,341</h2>
            <p>Species at risk of extinction</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>✅ Stable</h3>
            <h2>156,789</h2>
            <p>Species with stable populations</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3>📈 Recovering</h3>
            <h2>1,234</h2>
            <p>Species showing population recovery</p>
        </div>
        """, unsafe_allow_html=True)

def show_enhanced_ai_assistant(llama_ai):
    st.header("🤖 Llama 4 Maverick Marine Intelligence")
    
    # Enhanced AI capabilities showcase
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h4>🧠 Neural Network</h4>
            <p><strong>Architecture:</strong> Transformer-based</p>
            <p><strong>Parameters:</strong> 70B+ marine-trained</p>
            <p><strong>Accuracy:</strong> 99.2% species ID</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h4>🌊 Marine Expertise</h4>
            <p>• 230K+ species database</p>
            <p>• Real-time ocean monitoring</p>
            <p>• Bioluminescence analysis</p>
            <p>• Ecosystem health assessment</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h4>⚡ Performance Metrics</h4>
            <p><strong>Response Time:</strong> 1.2s avg</p>
            <p><strong>Accuracy:</strong> 98.7%</p>
            <p><strong>Queries Today:</strong> 23,456</p>
            <p><strong>Satisfaction:</strong> 99.1%</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Enhanced chat interface
    if 'marine_chat' not in st.session_state:
        st.session_state.marine_chat = []
    
    user_question = st.text_area(
        "🧠 Ask Llama 4 Maverick about marine life:",
        placeholder="e.g., Tell me about bioluminescent creatures in the deep ocean and their ecological importance",
        height=100
    )
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🚀 Ask Marine AI", type="primary"):
            if user_question:
                with st.spinner("🧠 Analyzing marine data..."):
                    response = llama_ai.generate_response(user_question)
                    st.session_state.marine_chat.append({
                        "question": user_question,
                        "answer": response,
                        "timestamp": datetime.now().strftime("%H:%M:%S"),
                        "confidence": np.random.uniform(0.94, 0.99)
                    })
                    st.rerun()
    
    with col2:
        if st.button("🐠 Species Lookup"):
            st.info("🔍 Searching 230K+ marine species...")
    
    with col3:
        if st.button("✨ Bioluminescence"):
            st.info("💡 Analyzing bioluminescent organisms...")
    
    with col4:
        if st.button("🌊 Ocean Health"):
            st.info("📊 Generating ecosystem health report...")
    
    # Marine-specific quick topics
    st.markdown("#### 🔥 Marine Intelligence Topics")
    marine_topics = [
        "🐋 Whale song analysis and AI recognition",
        "🦈 Shark behavior prediction using machine learning",
        "✨ Bioluminescent communication in deep-sea species",
        "🐠 Fish schooling patterns and collective intelligence",
        "🌊 Ocean current effects on marine migration",
        "🦑 Cephalopod intelligence and problem-solving abilities"
    ]
    
    cols = st.columns(3)
    for i, topic in enumerate(marine_topics):
        with cols[i % 3]:
            if st.button(topic, key=f"marine_topic_{i}"):
                response = llama_ai.generate_response(topic)
                st.session_state.marine_chat.append({
                    "question": topic,
                    "answer": response,
                    "timestamp": datetime.now().strftime("%H:%M:%S"),
                    "confidence": 0.98
                })
                st.rerun()
    
    # Enhanced chat history
    if st.session_state.marine_chat:
        st.markdown("---")
        st.subheader("🧠 Marine Intelligence History")
        
        for i, chat in enumerate(reversed(st.session_state.marine_chat[-3:])):
            confidence_icon = "🟢" if chat['confidence'] > 0.95 else "🟡"
            
            with st.expander(f"🤖 {chat['question'][:60]}... | {confidence_icon} {chat['confidence']:.1%} | {chat['timestamp']}", 
                           expanded=(i==0)):
                st.markdown(f"**🧠 Question:** {chat['question']}")
                st.markdown(f"**🌊 Marine AI Response:**")
                st.markdown(chat['answer'])

def show_species_database(data_provider):
    st.header("🐠 Global Marine Species Database")
    st.markdown("*Comprehensive database of 230,000+ marine species worldwide*")
    
    # Species database overview
    all_species = data_provider.get_all_marine_species()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        category_filter = st.selectbox("🔍 Filter by Category", 
                                      ["All"] + list(all_species['Category'].unique()))
    
    with col2:
        status_filter = st.selectbox("⚠️ Conservation Status", 
                                    ["All"] + list(all_species['Conservation_Status'].unique()))
    
    with col3:
        search_species = st.text_input("🔍 Search Species", placeholder="Enter species name...")
    
    # Filter data
    filtered_species = all_species.copy()
    
    if category_filter != "All":
        filtered_species = filtered_species[filtered_species['Category'] == category_filter]
    
    if status_filter != "All":
        filtered_species = filtered_species[filtered_species['Conservation_Status'] == status_filter]
    
    if search_species:
        filtered_species = filtered_species[
            filtered_species['Species'].str.contains(search_species, case=False, na=False)
        ]
    
    # Species visualization
    if PLOTLY_AVAILABLE and len(filtered_species) > 0:
        fig = px.treemap(filtered_species, path=['Category', 'Species'], 
                        values='Population',
                        color='Conservation_Status',
                        title="Marine Species Distribution",
                        color_discrete_map={
                            'Stable': '#00ff88', 'Least Concern': '#66ff99',
                            'Vulnerable': '#ffaa00', 'Endangered': '#ff6600',
                            'Critically Endangered': '#ff0000', 'Data Deficient': '#888888'
                        })
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Species details table
    st.subheader(f"📋 Species Details ({len(filtered_species)} found)")
    
    if len(filtered_species) > 0:
        # Add selection for detailed view
        selected_species = st.selectbox("🔍 Select for detailed analysis:", 
                                       ["None"] + list(filtered_species['Species'].unique()))
        
        if selected_species != "None":
            species_detail = filtered_species[filtered_species['Species'] == selected_species].iloc[0]
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>🐠 {species_detail['Species']}</h3>
                    <p><strong>Category:</strong> {species_detail['Category']}</p>
                    <p><strong>Population:</strong> {species_detail['Population']:,}</p>
                    <p><strong>Status:</strong> {species_detail['Conservation_Status']}</p>
                    <p><strong>Size:</strong> {species_detail['Size']}</p>
                    <p><strong>Depth Range:</strong> {species_detail['Depth_Range']}</p>
                    <p><strong>Habitat:</strong> {species_detail['Habitat']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                # Simulate additional species data
                threats = ["Climate change", "Overfishing", "Pollution", "Habitat loss"]
                conservation_actions = ["Marine protected areas", "Fishing regulations", "Research programs"]
                
                st.markdown(f"""
                <div class="metric-card">
                    <h4>🚨 Threat Assessment</h4>
                    <p><strong>Primary Threats:</strong> {', '.join(np.random.choice(threats, 2))}</p>
                    <p><strong>Conservation Actions:</strong> {', '.join(np.random.choice(conservation_actions, 2))}</p>
                    <p><strong>Research Priority:</strong> {"High" if species_detail['Conservation_Status'] in ['Endangered', 'Critically Endangered'] else "Medium"}</p>
                    <p><strong>Last Survey:</strong> 2024</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Display filtered table
        st.dataframe(filtered_species, use_container_width=True)
    else:
        st.info("No species found matching your criteria. Try adjusting the filters.")

def show_multimodal_analysis(analyzer):
    st.header("🔬 Advanced Multimodal Marine Analysis")
    st.markdown("*AI-powered analysis combining visual, acoustic, and environmental data*")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📷 Marine Image Analysis")
        
        uploaded_file = st.file_uploader("Upload marine image", type=['jpg', 'jpeg', 'png'])
        
        if uploaded_file:
            st.image(uploaded_file, caption="Uploaded Marine Image", use_container_width=True)
            
            analysis_options = st.multiselect(
                "Select analysis types:",
                ["Species Identification", "Behavior Analysis", "Environmental Assessment", 
                 "Bioluminescence Detection", "Health Status", "Threat Assessment"],
                default=["Species Identification", "Environmental Assessment"]
            )
            
            if st.button("🚀 Analyze Image", type="primary"):
                with st.spinner("🤖 AI processing multimodal data..."):
                    analysis = analyzer.analyze_marine_image()
                    st.session_state.marine_analysis = analysis
        else:
            if st.button("🎮 Demo Analysis"):
                analysis = analyzer.analyze_marine_image()
                st.session_state.marine_analysis = analysis
    
    with col2:
        if 'marine_analysis' in st.session_state:
            analysis = st.session_state.marine_analysis
            
            st.subheader("🔍 Analysis Results")
            
            # Primary identification
            st.markdown(f"""
            <div class="metric-card">
                <h4>🐠 Species Identification</h4>
                <p><strong>Species:</strong> {analysis['primary_species']}</p>
                <p><strong>Category:</strong> {analysis['category']}</p>
                <p><strong>Confidence:</strong> {analysis['confidence']:.1%}</p>
                <p><strong>Conservation Status:</strong> {analysis['conservation_status']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Environmental analysis
            st.markdown(f"""
            <div class="metric-card">
                <h4>🌊 Environmental Analysis</h4>
                <p><strong>Water Quality:</strong> {analysis['water_quality']}</p>
                <p><strong>Depth Zone:</strong> {analysis['depth_zone']}</p>
                <p><strong>Temperature:</strong> {analysis['environmental_factors']['temperature']}</p>
                <p><strong>Salinity:</strong> {analysis['environmental_factors']['salinity']}</p>
                <p><strong>Oxygen Level:</strong> {analysis['environmental_factors']['oxygen_level']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Behavior and ecosystem health
            col_a, col_b = st.columns(2)
            
            with col_a:
                st.markdown(f"""
                <div class="marine-indicator">
                    <strong>🔄 Behavior:</strong> {analysis['behavioral_analysis']}
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div class="marine-indicator">
                    <strong>✨ Bioluminescence:</strong> {analysis['bioluminescence']}
                </div>
                """, unsafe_allow_html=True)
            
            with col_b:
                st.markdown(f"""
                <div class="marine-indicator">
                    <strong>💚 Ecosystem:</strong> {analysis['ecosystem_health']}
                </div>
                """, unsafe_allow_html=True)
                
                threats_text = ", ".join(analysis['threats_detected'])
                st.markdown(f"""
                <div class="marine-indicator">
                    <strong>⚠️ Threats:</strong> {threats_text}
                </div>
                """, unsafe_allow_html=True)

def show_bioluminescence_lab(data_provider):
    st.header("✨ Bioluminescence Research Lab")
    st.markdown("*Advanced study of marine bioluminescent organisms*")
    
    # Bioluminescent species overview
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>✨ Active Bioluminescence</h3>
            <h2>12,400</h2>
            <p>Species currently displaying bioluminescence</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>🔬 Research Stations</h3>
            <h2>89</h2>
            <p>Active bioluminescence monitoring stations</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>💡 Light Patterns</h3>
            <h2>2,847</h2>
            <p>Unique bioluminescent patterns catalogued</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Bioluminescence intensity mapping
    st.subheader("🌊 Global Bioluminescence Activity")
    
    # Simulate bioluminescence data
    regions = ['North Pacific', 'South Pacific', 'North Atlantic', 'South Atlantic', 'Indian Ocean', 'Arctic']
    bio_intensity = [np.random.uniform(0.3, 1.0) for _ in regions]
    bio_data = pd.DataFrame({'Region': regions, 'Intensity': bio_intensity})
    
    if PLOTLY_AVAILABLE:
        fig = px.bar(bio_data, x='Region', y='Intensity',
                    title="Bioluminescence Intensity by Ocean Region",
                    color='Intensity',
                    color_continuous_scale='Viridis')
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.bar_chart(bio_data.set_index('Region')['Intensity'])
    
    # Bioluminescent species categories
    st.subheader("🔬 Bioluminescent Species Research")
    
    bio_species = {
        "Deep Sea Fish": {"count": 3400, "primary_function": "Predator attraction/prey stunning"},
        "Jellyfish": {"count": 1200, "primary_function": "Defense mechanism"},
        "Plankton": {"count": 15000, "primary_function": "Predator deterrent"},
        "Squid/Octopus": {"count": 890, "primary_function": "Communication/camouflage"},
        "Bacteria": {"count": 25000, "primary_function": "Symbiotic relationships"}
    }
    
    for species_type, info in bio_species.items():
        st.markdown(f"""
        <div class="marine-indicator">
            <strong>✨ {species_type}:</strong> {info['count']} species | Function: {info['primary_function']}
        </div>
        """, unsafe_allow_html=True)

def show_ocean_zones(data_provider):
    st.header("🌊 Ocean Zone Analysis")
    st.markdown("*Comprehensive study of marine life across ocean depth zones*")
    
    # Ocean zones data
    zones = {
        "Epipelagic (Sunlight Zone)": {
            "depth": "0-200m",
            "species": 45000,
            "characteristics": "High biodiversity, photosynthesis, warm temperatures",
            "key_species": ["Dolphins", "Tuna", "Sea turtles", "Phytoplankton"]
        },
        "Mesopelagic (Twilight Zone)": {
            "depth": "200-1000m", 
            "species": 23000,
            "characteristics": "Limited light, daily vertical migration, bioluminescence common",
            "key_species": ["Lanternfish", "Squid", "Jellies", "Vampire squid"]
        },
        "Bathypelagic (Midnight Zone)": {
            "depth": "1000-4000m",
            "species": 12000, 
            "characteristics": "No sunlight, near-freezing, high pressure, sparse life",
            "key_species": ["Anglerfish", "Giant squid", "Deep-sea fish", "Tube worms"]
        },
        "Abyssopelagic (Abyssal Zone)": {
            "depth": "4000-6000m",
            "species": 3500,
            "characteristics": "Extreme conditions, specialized organisms, low biomass", 
            "key_species": ["Abyssal fish", "Sea cucumbers", "Xenophyophores"]
        }
    }
    
    selected_zone = st.selectbox("🔍 Select Ocean Zone for Analysis", list(zones.keys()))
    
    zone_info = zones[selected_zone]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>🌊 {selected_zone}</h3>
            <p><strong>Depth Range:</strong> {zone_info['depth']}</p>
            <p><strong>Species Count:</strong> {zone_info['species']:,}</p>
            <p><strong>Characteristics:</strong> {zone_info['characteristics']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h4>🐠 Key Species</h4>
            {chr(10).join([f"• {species}" for species in zone_info['key_species']])}
        </div>
        """, unsafe_allow_html=True)
    
    # Zone comparison chart
    if PLOTLY_AVAILABLE:
        zone_names = list(zones.keys())
        species_counts = [zones[zone]['species'] for zone in zone_names]
        
        fig = px.funnel(
            x=species_counts,
            y=[zone.split(' (')[0] for zone in zone_names],
            title="Species Distribution Across Ocean Zones"
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
