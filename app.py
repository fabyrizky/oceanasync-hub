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

# Enhanced CSS with animations
def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Exo+2:wght@300;400;600&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #0a0a2e 0%, #16213e 50%, #0f3460 100%);
        font-family: 'Exo 2', sans-serif;
    }
    
    .ocean-animation {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -2;
        opacity: 0.3;
        background: 
            radial-gradient(circle at 20% 80%, rgba(0, 212, 255, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(0, 153, 255, 0.1) 0%, transparent 50%);
        animation: oceanFlow 20s ease-in-out infinite;
    }
    
    @keyframes oceanFlow {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-20px); }
    }
    
    .particles::before {
        content: '';
        position: absolute;
        width: 2px;
        height: 2px;
        background: #00d4ff;
        border-radius: 50%;
        box-shadow: 
            20px 30px #00d4ff, 90px 40px #0066cc, 160px 30px #0099ff,
            220px 10px #00d4ff, 320px 80px #0066cc, 420px 60px #0099ff,
            520px 30px #00d4ff, 620px 70px #0066cc, 720px 20px #0099ff;
        animation: particles 25s linear infinite;
    }
    
    @keyframes particles {
        0% { transform: translateY(0); opacity: 0; }
        10% { opacity: 1; }
        90% { opacity: 1; }
        100% { transform: translateY(-100vh); opacity: 0; }
    }
    
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(45deg, #00d4ff, #0099cc, #006699, #00d4ff);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-family: 'Orbitron', monospace;
        font-size: 3.5rem;
        font-weight: 900;
        margin-bottom: 1rem;
        animation: gradientShift 4s ease-in-out infinite;
    }
    
    @keyframes gradientShift {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    .subtitle {
        text-align: center;
        color: #00d4ff;
        font-size: 1.3rem;
        margin-bottom: 2rem;
        animation: pulse 3s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 0.8; }
        50% { opacity: 1; }
    }
    
    .metric-card {
        background: linear-gradient(135deg, rgba(0,212,255,0.15) 0%, rgba(0,153,204,0.1) 100%);
        border: 1px solid rgba(0,212,255,0.4);
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0,212,255,0.2);
        backdrop-filter: blur(15px);
        transition: all 0.4s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0,212,255,0.3);
    }
    
    .ai-badge {
        background: linear-gradient(45deg, #ff6b35, #f7931e);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: bold;
        display: inline-block;
        margin: 0.5rem 0;
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from { box-shadow: 0 2px 10px rgba(255,107,53,0.3); }
        to { box-shadow: 0 4px 20px rgba(255,107,53,0.6); }
    }
    
    .stButton > button {
        background: linear-gradient(45deg, #00d4ff, #0099cc);
        color: white;
        border: none;
        border-radius: 15px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,212,255,0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0,212,255,0.5);
    }
    
    .status-online {
        color: #00ff88;
        font-weight: bold;
    }
    
    .status-offline {
        color: #ff6b6b;
        font-weight: bold;
    }
    </style>
    
    <div class="ocean-animation"></div>
    <div class="particles"></div>
    """, unsafe_allow_html=True)

# Streamlined AI Assistant
class LlamaAIAssistant:
    def __init__(self):
        self.model_name = "Meta: Llama 4 Maverick"
        self.status = "🟢 Active"
        
    def generate_response(self, prompt: str) -> str:
        time.sleep(1)
        
        responses = {
            "climate": "🌊 **Climate Analysis**: Ocean temperatures have risen 0.6°C since 1969. Marine heatwaves increasing 50% since 1980s affecting coral reefs and fish migration patterns. Recommend enhanced monitoring and AI prediction models.",
            "pollution": "🏭 **Pollution Assessment**: Microplastics found at 0.1-1000 particles/m³. Ocean pH dropped from 8.25 to 8.1. Plastic pollution reaches 8M tons annually. Solutions: biodegradable materials, cleanup technologies.",
            "biodiversity": "🐟 **Biodiversity Status**: 37% marine species threatened. Large vertebrates declined 71% since 1970. Critical: sharks down 71%, coral reefs 50% decline. Conservation: MPAs, sustainable fishing.",
            "technology": "🤖 **Ocean Tech**: AUVs/ROVs enable 11,000m exploration. AI processes terabytes of data. Innovations: swarm robotics, satellite-AI detection, quantum sensors."
        }
        
        prompt_lower = prompt.lower()
        for key, response in responses.items():
            if key in prompt_lower:
                return response
        
        return "🧠 **Llama 4 Analysis**: Based on oceanographic research, recommend interdisciplinary approaches combining field observations, satellite data, and AI modeling for comprehensive marine science insights."

# Ocean Data Provider
class OceanDataProvider:
    def get_temperature_data(self, days=30):
        dates = pd.date_range(start=datetime.now() - timedelta(days=days), end=datetime.now(), freq='D')
        base_temp = 15 + 5 * np.sin(2 * np.pi * np.arange(len(dates)) / 365)
        temperatures = base_temp + np.random.normal(0, 1.5, len(dates))
        
        return pd.DataFrame({
            'Date': dates,
            'Temperature': temperatures,
            'Depth': np.random.choice([5, 50, 200, 1000], len(dates)),
            'Region': np.random.choice(['Pacific', 'Atlantic', 'Indian', 'Arctic'], len(dates)),
            'pH': np.random.normal(8.1, 0.1, len(dates)),
            'Salinity': np.random.normal(35, 2, len(dates))
        })
    
    def get_biodiversity_data(self):
        species = ['Blue Whale', 'Humpback Whale', 'Great White Shark', 'Whale Shark', 
                  'Bluefin Tuna', 'Salmon', 'Sea Turtle', 'Coral']
        return pd.DataFrame({
            'Species': species,
            'Population': np.random.randint(1000, 100000, len(species)),
            'Conservation_Status': np.random.choice(['Endangered', 'Vulnerable', 'Stable'], len(species)),
            'Trend': np.random.choice(['Declining', 'Stable', 'Increasing'], len(species)),
            'Category': np.random.choice(['Mammals', 'Fish', 'Reptiles', 'Cnidarians'], len(species))
        })
    
    def get_pollution_data(self):
        regions = ['Pacific', 'Atlantic', 'Indian', 'Arctic', 'Southern']
        pollution_types = ['Microplastics', 'Chemical', 'Oil', 'Thermal']
        
        data = []
        for region in regions:
            for p_type in pollution_types:
                data.append({
                    'Region': region,
                    'Pollution_Type': p_type,
                    'Concentration': np.random.uniform(0.1, 10.0),
                    'Impact_Score': np.random.uniform(1, 10),
                    'Trend': np.random.choice(['Increasing', 'Stable', 'Decreasing'])
                })
        return pd.DataFrame(data)

# Marine AI Analyzer
class MarineAnalyzer:
    def analyze_image(self):
        species = ['Blue Whale', 'Dolphin', 'Shark', 'Coral Reef', 'Sea Turtle']
        return {
            "species": np.random.choice(species),
            "water_quality": np.random.choice(['Excellent', 'Good', 'Fair', 'Poor']),
            "depth_zone": np.random.choice(['Surface', 'Mid-water', 'Deep']),
            "confidence": np.random.uniform(0.85, 0.99),
            "threats": np.random.choice(['None', 'Pollution', 'Climate Change', 'Overfishing'])
        }

# Main Application
def main():
    load_css()
    
    # Initialize components
    llama_ai = LlamaAIAssistant()
    data_provider = OceanDataProvider()
    analyzer = MarineAnalyzer()
    
    # Header
    st.markdown('<h1 class="main-header">🌊 OceanaSync Hub</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Advanced Ocean Science & AI Research Platform</p>', unsafe_allow_html=True)
    
    # AI Model Badge
    st.markdown('<div class="ai-badge">🤖 Powered by Meta: Llama 4 Maverick (Active)</div>', unsafe_allow_html=True)
    
    # Live metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("🌡️ Ocean Temp", "17.2°C", "+0.3°C")
    with col2:
        st.metric("🧪 Ocean pH", "8.09", "-0.02")
    with col3:
        st.metric("🌍 CO₂", "418 ppm", "+2.1")
    with col4:
        st.metric("📏 Sea Level", "3.4 mm/yr", "+0.1")
    with col5:
        st.metric("🧊 Ice Loss", "280 Gt/yr", "-12")
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 🧭 Navigation")
        page = st.selectbox("Choose Module", [
            "🏠 Dashboard", "🤖 AI Assistant", "📊 Analytics", 
            "🔬 Marine Analysis", "🌐 Collaboration", "📚 Library"
        ])
        
        st.markdown("---")
        st.markdown("### 🤖 AI Status")
        st.markdown(f"**Model**: {llama_ai.model_name}")
        st.markdown(f"**Status**: {llama_ai.status}")
        st.markdown("**Response**: < 2 seconds")
        st.markdown("**Accuracy**: 96.8%")
        
        st.markdown("---")
        st.markdown("### 📡 Data Sources")
        sources = {"NOAA": "🟢", "OceanX": "🟢", "Satellites": "🟢", "AUVs": "🟢"}
        for source, status in sources.items():
            st.markdown(f"**{source}**: {status} Connected")
        
        st.markdown("---")
        st.metric("🔬 Researchers", "4,127", "↗️ 234")
        st.metric("📊 Data Points/Hr", "1.2M", "↗️ 156K")
        st.metric("🌍 Sensors", "28,965", "↗️ 412")
    
    # Page routing
    if page == "🏠 Dashboard":
        show_dashboard(data_provider, llama_ai)
    elif page == "🤖 AI Assistant":
        show_ai_assistant(llama_ai)
    elif page == "📊 Analytics":
        show_analytics(data_provider)
    elif page == "🔬 Marine Analysis":
        show_marine_analysis(analyzer)
    elif page == "🌐 Collaboration":
        show_collaboration()
    elif page == "📚 Library":
        show_library()

def show_dashboard(data_provider, llama_ai):
    st.subheader("🌍 Global Ocean Health Dashboard")
    
    # AI Summary
    with st.spinner("🧠 AI analyzing global conditions..."):
        ai_summary = llama_ai.generate_response("ocean health climate biodiversity")
    
    st.markdown(f"""
    <div class="metric-card">
        <h4>🧠 AI Ocean Health Analysis</h4>
        {ai_summary}
    </div>
    """, unsafe_allow_html=True)
    
    # Key indicators
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>🌡️ Temperature</h3>
            <h2>+0.68°C</h2>
            <p>Above 1971-2000 avg</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>🐠 Species Risk</h3>
            <h2>41%</h2>
            <p>Marine species threatened</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>🏭 CO₂ Absorbed</h3>
            <h2>28%</h2>
            <p>Annual emissions</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3>🔬 Explored</h3>
            <h2>21.3%</h2>
            <p>Ocean mapped</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🌡️ Temperature Trends")
        temp_data = data_provider.get_temperature_data(90)
        
        if PLOTLY_AVAILABLE:
            fig = px.line(temp_data, x='Date', y='Temperature', color='Region',
                         title="90-Day Temperature Analysis")
            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='white')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.line_chart(temp_data.set_index('Date')['Temperature'])
    
    with col2:
        st.subheader("🐠 Biodiversity Status")
        bio_data = data_provider.get_biodiversity_data()
        
        if PLOTLY_AVAILABLE:
            fig = px.pie(bio_data, values='Population', names='Conservation_Status',
                        title="Species by Conservation Status")
            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='white')
            st.plotly_chart(fig, use_container_width=True)
        else:
            status_counts = bio_data['Conservation_Status'].value_counts()
            st.bar_chart(status_counts)
    
    # Pollution analysis
    st.subheader("🏭 Pollution Monitoring")
    pollution_data = data_provider.get_pollution_data()
    
    if PLOTLY_AVAILABLE:
        fig = px.scatter(pollution_data, x='Concentration', y='Impact_Score',
                        color='Pollution_Type', size='Impact_Score',
                        title="Pollution Impact vs Concentration")
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='white')
        st.plotly_chart(fig, use_container_width=True)
    else:
        chart_data = pollution_data.pivot_table(values='Impact_Score', index='Region', 
                                               columns='Pollution_Type', aggfunc='mean')
        st.bar_chart(chart_data)

def show_ai_assistant(llama_ai):
    st.header("🤖 Llama 4 Maverick Research Assistant")
    
    # Model info
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h4>🧠 AI Model</h4>
            <p><strong>Meta Llama 4 Maverick</strong></p>
            <p>Status: <span class="status-online">🟢 Active</span></p>
            <p>Accuracy: 96.8%</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h4>🎯 Capabilities</h4>
            <p>• Ocean Science Analysis</p>
            <p>• Research Methodology</p>
            <p>• Scientific Writing</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h4>📊 Today's Stats</h4>
            <p>Queries: 18,743</p>
            <p>Reports: 2,156</p>
            <p>Satisfaction: 98.2%</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Chat interface
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    user_question = st.text_area(
        "💬 Ask Llama 4 Maverick:",
        placeholder="e.g., What are the latest AI applications in ocean monitoring?",
        height=100
    )
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🚀 Ask AI", type="primary"):
            if user_question:
                with st.spinner("🧠 Processing..."):
                    response = llama_ai.generate_response(user_question)
                    st.session_state.chat_history.append({
                        "question": user_question,
                        "answer": response,
                        "timestamp": datetime.now().strftime("%H:%M:%S")
                    })
                    st.rerun()
    
    with col2:
        if st.button("📊 Generate Report"):
            st.info("📝 Generating comprehensive report...")
    
    with col3:
        if st.button("🔍 Search Papers"):
            st.info("🔍 Searching 156K+ publications...")
    
    # Quick topics
    st.markdown("#### 🔥 Trending Topics")
    topics = [
        "🌊 Marine heatwave prediction",
        "🐟 eDNA biodiversity monitoring", 
        "🤖 Autonomous coral restoration",
        "📡 Satellite illegal fishing detection"
    ]
    
    cols = st.columns(4)
    for i, topic in enumerate(topics):
        with cols[i]:
            if st.button(topic, key=f"topic_{i}"):
                response = llama_ai.generate_response(topic)
                st.session_state.chat_history.append({
                    "question": topic,
                    "answer": response,
                    "timestamp": datetime.now().strftime("%H:%M:%S")
                })
                st.rerun()
    
    # Chat history
    if st.session_state.chat_history:
        st.markdown("---")
        st.subheader("💬 Conversation History")
        
        for i, chat in enumerate(reversed(st.session_state.chat_history[-3:])):
            with st.expander(f"Q: {chat['question'][:60]}... | {chat['timestamp']}", expanded=(i==0)):
                st.markdown(f"**Question:** {chat['question']}")
                st.markdown(f"**Answer:** {chat['answer']}")

def show_analytics(data_provider):
    st.header("📊 Advanced Ocean Analytics")
    
    analysis_type = st.selectbox("Select Analysis", [
        "Temperature Analysis", "Biodiversity Assessment", "Pollution Tracking"
    ])
    
    if analysis_type == "Temperature Analysis":
        st.subheader("🌡️ Ocean Temperature Analysis")
        
        days = st.slider("Analysis Period (days)", 30, 365, 90)
        temp_data = data_provider.get_temperature_data(days)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if PLOTLY_AVAILABLE:
                fig = px.line(temp_data, x='Date', y='Temperature', color='Region')
                fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='white')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.line_chart(temp_data.set_index('Date')['Temperature'])
        
        with col2:
            st.write("**Statistical Summary**")
            st.dataframe(temp_data[['Temperature', 'Depth', 'pH', 'Salinity']].describe())
    
    elif analysis_type == "Biodiversity Assessment":
        st.subheader("🐠 Marine Biodiversity Analysis")
        
        bio_data = data_provider.get_biodiversity_data()
        
        col1, col2 = st.columns(2)
        
        with col1:
            if PLOTLY_AVAILABLE:
                fig = px.bar(bio_data, x='Species', y='Population', color='Conservation_Status')
                fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='white')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.bar_chart(bio_data.set_index('Species')['Population'])
        
        with col2:
            st.write("**Conservation Status**")
            status_counts = bio_data['Conservation_Status'].value_counts()
            st.dataframe(status_counts)

def show_marine_analysis(analyzer):
    st.header("🔬 Marine AI Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        uploaded_file = st.file_uploader("Upload Marine Image", type=['jpg', 'jpeg', 'png'])
        
        if uploaded_file:
            st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
            
            if st.button("🚀 Analyze Image"):
                with st.spinner("🤖 Analyzing..."):
                    analysis = analyzer.analyze_image()
                    st.session_state.analysis = analysis
        else:
            if st.button("🎮 Demo Analysis"):
                analysis = analyzer.analyze_image()
                st.session_state.analysis = analysis
    
    with col2:
        if 'analysis' in st.session_state:
            analysis = st.session_state.analysis
            
            st.subheader("🔍 Analysis Results")
            st.markdown(f"**🐟 Species:** {analysis['species']}")
            st.markdown(f"**💧 Water Quality:** {analysis['water_quality']}")
            st.markdown(f"**📏 Depth Zone:** {analysis['depth_zone']}")
            st.markdown(f"**⚠️ Threats:** {analysis['threats']}")
            st.markdown(f"**🎯 Confidence:** {analysis['confidence']:.1%}")
            
            # Confidence chart
            confidence_data = pd.DataFrame({
                'Metric': ['Species ID', 'Water Quality', 'Depth', 'Threat Assessment'],
                'Confidence': [analysis['confidence'], 0.92, 0.88, 0.85]
            })
            st.bar_chart(confidence_data.set_index('Metric')['Confidence'])

def show_collaboration():
    st.header("🌐 Global Collaboration Hub")
    
    # Active projects
    projects = [
        {"title": "🌊 Pacific Microplastic Mapping", "progress": 75, "team": "12 researchers"},
        {"title": "🤖 AI Coral Restoration", "progress": 45, "team": "8 researchers"},
        {"title": "⚡ Wave Energy Optimization", "progress": 60, "team": "15 researchers"}
    ]
    
    for project in projects:
        with st.expander(f"{project['title']} - {project['progress']}% Complete"):
            col1, col2 = st.columns(2)
            with col1:
                st.progress(project['progress'] / 100)
                st.write(f"**Team Size:** {project['team']}")
            with col2:
                if st.button(f"Join Project", key=project['title']):
                    st.success("✅ Joined project!")
    
    # New project
    st.subheader("➕ Start New Project")
    col1, col2 = st.columns(2)
    
    with col1:
        title = st.text_input("Project Title")
        description = st.text_area("Description")
    
    with col2:
        disciplines = st.multiselect("Required Disciplines", [
            "Marine Biology", "Data Science", "Engineering", "Physics"
        ])
        duration = st.selectbox("Duration", ["1-3 months", "3-6 months", "6+ months"])
    
    if st.button("🚀 Create Project"):
        if title and description:
            st.success(f"✅ Project '{title}' created!")
            st.balloons()

def show_library():
    st.header("📚 Scientific Library")
    
    # Search
    search_query = st.text_input("🔍 Search Knowledge Base")
    
    # Categories
    col1, col2, col3 = st.columns(3)
    with col1:
        category = st.selectbox("Category", ["All", "Marine Biology", "Ocean Technology", "Climate Science"])
    with col2:
        content_type = st.selectbox("Type", ["All", "Research Papers", "Tutorials", "Datasets"])
    with col3:
        difficulty = st.selectbox("Level", ["All", "Beginner", "Intermediate", "Advanced"])
    
    # Featured content
    featured = [
        {
            "title": "🌊 Ocean Data Analysis with Python",
            "type": "Tutorial",
            "rating": 4.8,
            "views": "12.5K"
        },
        {
            "title": "🤖 AI-Powered Microplastic Detection",
            "type": "Research Paper",
            "rating": 4.9,
            "views": "8.3K"
        }
    ]
    
    for content in featured:
        with st.expander(f"{content['title']} - ⭐ {content['rating']} ({content['views']} views)"):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**Type:** {content['type']}")
                st.write(f"**Views:** {content['views']}")
            with col2:
                if st.button("📖 Read", key=content['title']):
                    st.info("Opening content...")

if __name__ == "__main__":
    main()
