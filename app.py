import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import requests
import json
import time
from typing import Dict, List, Optional
import base64
from io import BytesIO
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
import hashlib

# Page configuration
st.set_page_config(
    page_title="OceanaSync Hub",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern, futuristic UI with animated grid
def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Exo+2:wght@300;400;600&display=swap');
    
    /* Global styles */
    .stApp {
        background: linear-gradient(135deg, #0a0a2e 0%, #16213e 50%, #0f3460 100%);
        font-family: 'Exo 2', sans-serif;
    }
    
    /* Animated grid background */
    .grid-container {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
        opacity: 0.1;
        background: 
            linear-gradient(rgba(0,255,255,0.1) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0,255,255,0.1) 1px, transparent 1px);
        background-size: 50px 50px;
        animation: gridMove 20s linear infinite;
    }
    
    @keyframes gridMove {
        0% { transform: translate(0, 0); }
        100% { transform: translate(50px, 50px); }
    }
    
    /* Header styles */
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(45deg, #00d4ff, #0099cc, #006699);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-family: 'Orbitron', monospace;
        font-size: 3rem;
        font-weight: 900;
        text-shadow: 0 0 20px rgba(0,212,255,0.5);
        margin-bottom: 1rem;
    }
    
    .subtitle {
        text-align: center;
        color: #00d4ff;
        font-size: 1.2rem;
        margin-bottom: 2rem;
        text-shadow: 0 0 10px rgba(0,212,255,0.3);
    }
    
    /* Card styles */
    .metric-card {
        background: linear-gradient(135deg, rgba(0,212,255,0.1) 0%, rgba(0,153,204,0.1) 100%);
        border: 1px solid rgba(0,212,255,0.3);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0,212,255,0.1);
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0,212,255,0.2);
        border-color: rgba(0,212,255,0.5);
    }
    
    /* Button styles */
    .stButton > button {
        background: linear-gradient(45deg, #00d4ff, #0099cc);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,212,255,0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,212,255,0.4);
    }
    
    /* Sidebar styles */
    .css-1d391kg {
        background: linear-gradient(180deg, rgba(10,10,46,0.9) 0%, rgba(22,33,62,0.9) 100%);
        border-right: 1px solid rgba(0,212,255,0.3);
    }
    
    /* Input styles */
    .stTextInput > div > div > input {
        background: rgba(0,212,255,0.1);
        border: 1px solid rgba(0,212,255,0.3);
        border-radius: 10px;
        color: white;
    }
    
    .stSelectbox > div > div > select {
        background: rgba(0,212,255,0.1);
        border: 1px solid rgba(0,212,255,0.3);
        border-radius: 10px;
        color: white;
    }
    
    /* Chart containers */
    .chart-container {
        background: rgba(0,212,255,0.05);
        border-radius: 15px;
        padding: 1rem;
        border: 1px solid rgba(0,212,255,0.2);
        margin: 1rem 0;
    }
    
    /* Status indicators */
    .status-online {
        color: #00ff88;
        font-weight: bold;
    }
    
    .status-offline {
        color: #ff6b6b;
        font-weight: bold;
    }
    
    /* Loading animation */
    .loading-spinner {
        border: 3px solid rgba(0,212,255,0.3);
        border-top: 3px solid #00d4ff;
        border-radius: 50%;
        width: 30px;
        height: 30px;
        animation: spin 1s linear infinite;
        margin: 0 auto;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    </style>
    
    <div class="grid-container"></div>
    """, unsafe_allow_html=True)

# Data simulation functions
class OceanDataSimulator:
    def __init__(self):
        self.data_cache = {}
        
    def generate_ocean_temperature_data(self, days=30):
        """Generate realistic ocean temperature data"""
        dates = pd.date_range(start=datetime.now() - timedelta(days=days), end=datetime.now(), freq='D')
        
        # Simulate temperature with seasonal variation and random fluctuation
        base_temp = 15  # Base temperature in Celsius
        seasonal_variation = 5 * np.sin(2 * np.pi * np.arange(len(dates)) / 365)
        random_variation = np.random.normal(0, 1, len(dates))
        
        temperatures = base_temp + seasonal_variation + random_variation
        
        return pd.DataFrame({
            'Date': dates,
            'Temperature': temperatures,
            'Depth': np.random.uniform(0, 200, len(dates)),
            'Location': np.random.choice(['Pacific', 'Atlantic', 'Indian', 'Arctic'], len(dates))
        })
    
    def generate_marine_biodiversity_data(self):
        """Generate marine biodiversity data"""
        species_data = {
            'Species': ['Dolphins', 'Whales', 'Sharks', 'Tuna', 'Coral', 'Jellyfish', 'Sea Turtles', 'Octopus'],
            'Population': np.random.randint(1000, 10000, 8),
            'Threat_Level': np.random.choice(['Low', 'Medium', 'High', 'Critical'], 8),
            'Ocean_Region': np.random.choice(['Pacific', 'Atlantic', 'Indian', 'Arctic'], 8),
            'Conservation_Status': np.random.choice(['Stable', 'Declining', 'Recovering'], 8)
        }
        return pd.DataFrame(species_data)
    
    def generate_pollution_data(self):
        """Generate ocean pollution data"""
        pollution_types = ['Plastic', 'Chemical', 'Oil', 'Thermal', 'Noise']
        regions = ['North Pacific', 'South Pacific', 'North Atlantic', 'South Atlantic', 'Indian Ocean']
        
        data = []
        for region in regions:
            for pollution_type in pollution_types:
                data.append({
                    'Region': region,
                    'Pollution_Type': pollution_type,
                    'Concentration': np.random.uniform(0.1, 10.0),
                    'Impact_Score': np.random.uniform(1, 10),
                    'Trend': np.random.choice(['Increasing', 'Decreasing', 'Stable'])
                })
        
        return pd.DataFrame(data)

# Mock RAG system for ocean data
class MockOceanRAG:
    def __init__(self):
        self.knowledge_base = {
            "microplastic": "Microplastics are small plastic debris in the environment resulting from disposal and breakdown of consumer products. They pose significant threats to marine ecosystems and food chains.",
            "coral bleaching": "Coral bleaching occurs when corals expel symbiotic algae due to stress from temperature changes, pollution, or ocean acidification, leading to coral death.",
            "ocean acidification": "Ocean acidification is the ongoing decrease in ocean pH caused by absorption of CO2 from the atmosphere, affecting marine organisms with calcium carbonate shells.",
            "marine biodiversity": "Marine biodiversity encompasses the variety of life in ocean ecosystems, crucial for maintaining ecological balance and supporting human livelihoods.",
            "deep sea exploration": "Deep sea exploration involves studying ocean depths beyond 200 meters, revealing unique ecosystems and potential resources while facing extreme conditions.",
            "wave energy": "Wave energy harnesses the power of ocean waves to generate electricity, offering a renewable energy source with high potential in coastal regions.",
            "auv": "Autonomous Underwater Vehicles (AUVs) are unmanned submersibles used for oceanographic research, environmental monitoring, and underwater mapping."
        }
    
    def query(self, question: str) -> str:
        """Simulate RAG response"""
        question_lower = question.lower()
        
        # Simple keyword matching for demonstration
        for key, value in self.knowledge_base.items():
            if key in question_lower:
                return f"🤖 **AI Analysis**: {value}\n\n📊 **Current Research Status**: Active studies ongoing\n🔬 **Recommended Action**: Continue monitoring and data collection"
        
        return "🤖 **AI Analysis**: This is an interesting oceanographic question. Based on current research trends, interdisciplinary collaboration between marine biology, engineering, and data science is crucial for advancing our understanding of ocean systems.\n\n📊 **Suggested Research Areas**: Consider exploring AI-driven monitoring systems, sustainable ocean technologies, and ecosystem modeling approaches."

# AI Multimodal Analysis (Mock)
class MultimodalOceanAnalyzer:
    @staticmethod
    def analyze_image(image_data):
        """Mock image analysis for ocean-related content"""
        # In real implementation, this would use computer vision models
        analysis_results = {
            "detected_objects": ["Marine life", "Water surface", "Underwater terrain"],
            "water_quality": np.random.choice(["Excellent", "Good", "Fair", "Poor"]),
            "estimated_depth": f"{np.random.randint(5, 500)} meters",
            "marine_life_count": np.random.randint(0, 20),
            "pollution_indicators": np.random.choice(["None detected", "Minimal", "Moderate", "High"])
        }
        return analysis_results

# Main application
def main():
    load_css()
    
    # Initialize data simulator and AI models
    data_sim = OceanDataSimulator()
    rag_system = MockOceanRAG()
    multimodal_analyzer = MultimodalOceanAnalyzer()
    
    # Header
    st.markdown('<h1 class="main-header">🌊 OceanaSync Hub</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Multidisciplinary Ocean Science & AI Platform</p>', unsafe_allow_html=True)
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown("### 🧭 Navigation")
        page = st.selectbox(
            "Choose Module",
            ["🏠 Dashboard", "🤖 AI Research Assistant", "📊 Data Analytics", "🔬 Multimodal Analysis", "🌐 Collaboration Hub", "📚 Knowledge Base"]
        )
        
        st.markdown("---")
        st.markdown("### 📡 System Status")
        st.markdown('<span class="status-online">🟢 AI Systems: Online</span>', unsafe_allow_html=True)
        st.markdown('<span class="status-online">🟢 Data Streams: Active</span>', unsafe_allow_html=True)
        st.markdown('<span class="status-online">🟢 Ocean Sensors: Connected</span>', unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("### 🎯 Quick Stats")
        st.metric("Active Researchers", "1,247", "↗️ 23")
        st.metric("Data Points Collected", "2.1M", "↗️ 15K")
        st.metric("AI Models Deployed", "12", "↗️ 2")
    
    # Main content based on selected page
    if page == "🏠 Dashboard":
        show_dashboard(data_sim)
    elif page == "🤖 AI Research Assistant":
        show_ai_assistant(rag_system)
    elif page == "📊 Data Analytics":
        show_data_analytics(data_sim)
    elif page == "🔬 Multimodal Analysis":
        show_multimodal_analysis(multimodal_analyzer)
    elif page == "🌐 Collaboration Hub":
        show_collaboration_hub()
    elif page == "📚 Knowledge Base":
        show_knowledge_base()

def show_dashboard(data_sim):
    """Main dashboard with overview metrics and charts"""
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>🌡️ Ocean Temperature</h3>
            <h2>15.3°C</h2>
            <p>↗️ +0.2°C from last week</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>🐠 Species Monitored</h3>
            <h2>2,847</h2>
            <p>↗️ +127 new entries</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>🔬 Research Projects</h3>
            <h2>156</h2>
            <p>🔄 23 active collaborations</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3>🌊 Data Quality</h3>
            <h2>98.5%</h2>
            <p>✅ All sensors operational</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Charts section
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("🌡️ Ocean Temperature Trends")
        
        temp_data = data_sim.generate_ocean_temperature_data(30)
        fig = px.line(temp_data, x='Date', y='Temperature', 
                     title="30-Day Temperature Analysis",
                     color_discrete_sequence=['#00d4ff'])
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("🐠 Marine Biodiversity Distribution")
        
        bio_data = data_sim.generate_marine_biodiversity_data()
        fig = px.pie(bio_data, values='Population', names='Species',
                    title="Species Population Distribution",
                    color_discrete_sequence=px.colors.sequential.Blues_r)
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Pollution monitoring
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("🏭 Ocean Pollution Monitoring")
    
    pollution_data = data_sim.generate_pollution_data()
    fig = px.scatter(pollution_data, x='Concentration', y='Impact_Score',
                    color='Pollution_Type', size='Concentration',
                    hover_data=['Region', 'Trend'],
                    title="Pollution Impact Analysis Across Ocean Regions")
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white'
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

def show_ai_assistant(rag_system):
    """AI Research Assistant with RAG capabilities"""
    st.header("🤖 AI Research Assistant")
    st.markdown("*Powered by Advanced RAG & Multimodal AI*")
    
    # Chat interface
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # User input
    user_question = st.text_input("💬 Ask about oceanographic research, marine biology, or ocean technology:", 
                                 placeholder="e.g., What are the effects of microplastic pollution on marine ecosystems?")
    
    col1, col2 = st.columns([1, 4])
    
    with col1:
        if st.button("🚀 Ask AI", type="primary"):
            if user_question:
                with st.spinner("🧠 AI is thinking..."):
                    time.sleep(1)  # Simulate processing time
                    response = rag_system.query(user_question)
                    
                    st.session_state.chat_history.append({"question": user_question, "answer": response})
    
    # Display chat history
    if st.session_state.chat_history:
        st.markdown("---")
        st.subheader("💬 Conversation History")
        
        for i, chat in enumerate(reversed(st.session_state.chat_history[-5:])):  # Show last 5 conversations
            with st.expander(f"Q: {chat['question'][:60]}..." if len(chat['question']) > 60 else f"Q: {chat['question']}", expanded=(i==0)):
                st.markdown(f"**Question:** {chat['question']}")
                st.markdown(f"**Answer:** {chat['answer']}")
    
    # AI Model Status
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h4>🧠 RAG Model</h4>
            <p class="status-online">Status: Active</p>
            <p>Qwen-3 Turbo</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h4>🔍 Knowledge Base</h4>
            <p class="status-online">12,847 Documents</p>
            <p>Last Updated: Today</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h4>⚡ Response Time</h4>
            <p class="status-online">< 2 seconds</p>
            <p>99.9% Uptime</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Quick Questions
    st.markdown("---")
    st.subheader("🎯 Quick Research Topics")
    
    quick_questions = [
        "🔬 What are the latest advances in deep-sea exploration technology?",
        "🌊 How does ocean acidification affect coral reef ecosystems?",
        "🤖 What role can AI play in marine conservation efforts?",
        "⚡ What are the prospects for ocean wave energy harvesting?",
        "🐟 How are AUVs revolutionizing marine research?"
    ]
    
    cols = st.columns(len(quick_questions))
    for i, question in enumerate(quick_questions):
        with cols[i]:
            if st.button(question, key=f"quick_q_{i}"):
                response = rag_system.query(question)
                st.session_state.chat_history.append({"question": question, "answer": response})
                st.rerun()

def show_data_analytics(data_sim):
    """Advanced data analytics dashboard"""
    st.header("📊 Ocean Data Analytics")
    st.markdown("*Real-time Analysis & Predictive Modeling*")
    
    # Data selection
    analysis_type = st.selectbox(
        "🔍 Select Analysis Type",
        ["Temperature Analysis", "Biodiversity Monitoring", "Pollution Assessment", "Climate Modeling"]
    )
    
    if analysis_type == "Temperature Analysis":
        st.subheader("🌡️ Ocean Temperature Analysis")
        
        # Time period selection
        days = st.slider("📅 Analysis Period (days)", 7, 365, 30)
        depth_filter = st.slider("🌊 Depth Range (meters)", 0, 1000, (0, 200))
        
        # Generate and filter data
        temp_data = data_sim.generate_ocean_temperature_data(days)
        filtered_data = temp_data[(temp_data['Depth'] >= depth_filter[0]) & 
                                 (temp_data['Depth'] <= depth_filter[1])]
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Temperature trend
            fig = px.line(filtered_data, x='Date', y='Temperature', 
                         color='Location',
                         title=f"Temperature Trends - Last {days} Days")
            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='white')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Temperature distribution by location
            fig = px.box(filtered_data, x='Location', y='Temperature',
                        title="Temperature Distribution by Ocean")
            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='white')
            st.plotly_chart(fig, use_container_width=True)
        
        # Statistical summary
        st.subheader("📈 Statistical Summary")
        summary_stats = filtered_data.groupby('Location')['Temperature'].agg(['mean', 'std', 'min', 'max']).round(2)
        st.dataframe(summary_stats, use_container_width=True)
    
    elif analysis_type == "Biodiversity Monitoring":
        st.subheader("🐠 Marine Biodiversity Analysis")
        
        bio_data = data_sim.generate_marine_biodiversity_data()
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Population by species
            fig = px.bar(bio_data.sort_values('Population', ascending=False), 
                        x='Species', y='Population',
                        color='Conservation_Status',
                        title="Species Population by Conservation Status")
            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='white')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Threat level distribution
            threat_counts = bio_data['Threat_Level'].value_counts()
            fig = px.pie(values=threat_counts.values, names=threat_counts.index,
                        title="Species by Threat Level")
            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='white')
            st.plotly_chart(fig, use_container_width=True)
        
        # Detailed data table
        st.subheader("📋 Species Details")
        st.dataframe(bio_data, use_container_width=True)
    
    # Export functionality
    st.markdown("---")
    st.subheader("💾 Export Data")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 Export as CSV"):
            st.success("✅ Data exported successfully!")
    
    with col2:
        if st.button("📊 Export as Excel"):
            st.success("✅ Excel file generated!")
    
    with col3:
        if st.button("🔗 Generate API Link"):
            api_link = f"https://api.oceanasync.com/data/{hashlib.md5(str(datetime.now()).encode()).hexdigest()[:8]}"
            st.code(api_link)

def show_multimodal_analysis(multimodal_analyzer):
    """Multimodal AI analysis for images and data"""
    st.header("🔬 Multimodal Ocean Analysis")
    st.markdown("*AI-Powered Image & Data Analysis*")
    
    # Analysis type selection
    analysis_mode = st.radio(
        "🎯 Select Analysis Mode",
        ["📷 Image Analysis", "🌊 Sensor Data Fusion", "🎥 Video Processing"]
    )
    
    if analysis_mode == "📷 Image Analysis":
        st.subheader("📸 Ocean Image Analysis")
        
        # File uploader
        uploaded_file = st.file_uploader(
            "Upload ocean image for AI analysis",
            type=['jpg', 'jpeg', 'png'],
            help="Upload images of marine life, ocean conditions, or underwater scenes"
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            if uploaded_file is not None:
                # Display uploaded image
                st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
                
                if st.button("🚀 Analyze Image", type="primary"):
                    with st.spinner("🤖 AI is analyzing the image..."):
                        time.sleep(2)  # Simulate analysis time
                        analysis = multimodal_analyzer.analyze_image(uploaded_file)
                        
                        st.session_state.image_analysis = analysis
            else:
                st.info("👆 Upload an ocean-related image to begin AI analysis")
        
        with col2:
            if 'image_analysis' in st.session_state:
                st.subheader("🔍 Analysis Results")
                analysis = st.session_state.image_analysis
                
                st.markdown(f"**🎯 Detected Objects:** {', '.join(analysis['detected_objects'])}")
                st.markdown(f"**💧 Water Quality:** {analysis['water_quality']}")
                st.markdown(f"**📏 Estimated Depth:** {analysis['estimated_depth']}")
                st.markdown(f"**🐠 Marine Life Count:** {analysis['marine_life_count']}")
                st.markdown(f"**⚠️ Pollution Indicators:** {analysis['pollution_indicators']}")
                
                # Confidence visualization
                confidence_data = {
                    'Metric': ['Water Quality', 'Depth Estimation', 'Life Detection', 'Pollution Analysis'],
                    'Confidence': [92, 87, 94, 89]
                }
                
                fig = px.bar(confidence_data, x='Metric', y='Confidence',
                           title="AI Analysis Confidence Scores",
                           color='Confidence',
                           color_continuous_scale='Blues')
                fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='white')
                st.plotly_chart(fig, use_container_width=True)
    
    elif analysis_mode == "🌊 Sensor Data Fusion":
        st.subheader("🌐 Multi-Sensor Data Integration")
        
        # Simulate sensor data
        sensor_types = ['Temperature', 'Salinity', 'pH', 'Dissolved Oxygen', 'Turbidity']
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📡 Active Sensors")
            for sensor in sensor_types:
                value = np.random.uniform(0, 100)
                status = "🟢 Online" if value > 20 else "🔴 Offline"
                st.markdown(f"**{sensor}:** {value:.1f} units - {status}")
        
        with col2:
            st.markdown("### 📊 Sensor Correlation Matrix")
            # Generate correlation data
            correlation_data = np.random.rand(len(sensor_types), len(sensor_types))
            correlation_data = (correlation_data + correlation_data.T) / 2  # Make symmetric
            np.fill_diagonal(correlation_data, 1)  # Perfect self-correlation
            
            fig = px.imshow(correlation_data, 
                          x=sensor_types,
                          y=sensor_types,
                          color_continuous_scale='Blues',
                          title="Sensor Data Correlation")
            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='white')
            st.plotly_chart(fig, use_container_width=True)
        
        # Real-time data simulation
        st.markdown("### 📈 Real-time Sensor Feeds")
        if st.button("🔄 Refresh Data"):
            # Generate time series data for sensors
            timestamps = pd.date_range(start=datetime.now() - timedelta(hours=24), 
                                     end=datetime.now(), freq='H')
            
            sensor_data = pd.DataFrame({
                'Timestamp': timestamps,
                'Temperature': 15 + 5 * np.sin(np.linspace(0, 4*np.pi, len(timestamps))) + np.random.normal(0, 0.5, len(timestamps)),
                'Salinity': 35 + 2 * np.cos(np.linspace(0, 2*np.pi, len(timestamps))) + np.random.normal(0, 0.3, len(timestamps)),
                'pH': 8.1 + 0.3 * np.sin(np.linspace(0, 3*np.pi, len(timestamps))) + np.random.normal(0, 0.1, len(timestamps))
            })
            
            fig = px.line(sensor_data, x='Timestamp', y=['Temperature', 'Salinity', 'pH'],
                         title="24-Hour Sensor Data Trends")
            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='white')
            st.plotly_chart(fig, use_container_width=True)

def show_collaboration_hub():
    """Collaboration and project management hub"""
    st.header("🌐 Collaboration Hub")
    st.markdown("*Connect, Collaborate, and Innovate Together*")
    
    # Active projects section
    st.subheader("🚀 Active Research Projects")
    
    projects = [
        {
            "title": "🌊 Pacific Microplastic Mapping",
            "lead": "Dr. Sarah Chen - Marine Biology",
            "collaborators": ["Mechanical Eng", "Data Science", "Environmental Sci"],
            "progress": 75,
            "status": "Active",
            "deadline": "2025-08-15"
        },
        {
            "title": "🤖 AI-Powered Coral Restoration",
            "lead": "Prof. James Rodriguez - Biotechnology",
            "collaborators": ["AI/ML", "Marine Biology", "Robotics"],
            "progress": 45,
            "status": "Active",
            "deadline": "2025-09-30"
        },
        {
            "title": "⚡ Wave Energy Optimization",
            "lead": "Dr. Maya Patel - Mechanical Engineering",
            "collaborators": ["Electrical Eng", "Physics", "Tech Management"],
            "progress": 60,
            "status": "Active",
            "deadline": "2025-07-20"
        }
    ]
    
    for project in projects:
        with st.expander(f"{project['title']} - {project['progress']}% Complete"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**Project Lead:** {project['lead']}")
                st.markdown(f"**Collaborating Disciplines:** {', '.join(project['collaborators'])}")
                st.markdown(f"**Deadline:** {project['deadline']}")
                
                # Progress bar
                st.progress(project['progress'] / 100)
                
            with col2:
                st.markdown("**Quick Actions:**")
                if st.button(f"📝 Update Progress", key=f"update_{project['title']}"):
                    st.success("Progress updated!")
                if st.button(f"💬 Join Discussion", key=f"join_{project['title']}"):
                    st.info("Redirecting to project chat...")
                if st.button(f"📊 View Analytics", key=f"analytics_{project['title']}"):
                    st.info("Opening project analytics...")
    
    # Create new project
    st.markdown("---")
    st.subheader("➕ Start New Collaboration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        project_title = st.text_input("🎯 Project Title")
        project_description = st.text_area("📝 Project Description")
        project_lead = st.text_input("👤 Project Lead")
    
    with col2:
        disciplines_needed = st.multiselect(
            "🔬 Required Disciplines",
            ["Marine Biology", "Mechanical Engineering", "Electrical Engineering", 
             "Data Science", "AI/ML", "Physics", "Biotechnology", "Environmental Science",
             "Technology Management", "Robotics", "Chemistry"]
        )
        project_duration = st.selectbox("⏱️ Expected Duration", 
                                       ["1-3 months", "3-6 months", "6-12 months", "1+ years"])
        funding_needed = st.selectbox("💰 Funding Requirements", 
                                     ["Self-funded", "< $10K", "$10K - $50K", "$50K - $100K", "$100K+"])
    
    if st.button("🚀 Create Project", type="primary"):
        if project_title and project_description:
            st.success(f"✅ Project '{project_title}' created successfully!")
            st.balloons()
        else:
            st.error("Please fill in required fields")
    
    # Researcher network
    st.markdown("---")
    st.subheader("👥 Researcher Network")
    
    # Sample researcher profiles
    researchers = [
        {"name": "Dr. Sarah Chen", "discipline": "Marine Biology", "expertise": "Microplastic Analysis", "projects": 3, "location": "Stanford University"},
        {"name": "Prof. James Rodriguez", "discipline": "Biotechnology", "expertise": "Coral Restoration", "projects": 2, "location": "MIT"},
        {"name": "Dr. Maya Patel", "discipline": "Mechanical Engineering", "expertise": "Wave Energy", "projects": 4, "location": "UC Berkeley"},
        {"name": "Dr. Alex Kim", "discipline": "Data Science", "expertise": "Ocean Modeling", "projects": 5, "location": "Woods Hole"},
        {"name": "Prof. Lisa Zhang", "discipline": "AI/ML", "expertise": "Computer Vision", "projects": 3, "location": "CMU"}
    ]
    
    # Display researcher cards
    cols = st.columns(3)
    for i, researcher in enumerate(researchers):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="metric-card">
                <h4>👤 {researcher['name']}</h4>
                <p><strong>🔬 {researcher['discipline']}</strong></p>
                <p>🎯 {researcher['expertise']}</p>
                <p>📍 {researcher['location']}</p>
                <p>🚀 {researcher['projects']} Active Projects</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Communication tools
    st.markdown("---")
    st.subheader("💬 Communication & Tools")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📧 Send Message"):
            st.info("Opening messaging interface...")
    
    with col2:
        if st.button("🎥 Start Video Call"):
            st.info("Launching video conference...")
    
    with col3:
        if st.button("📁 Share Files"):
            st.info("Opening file sharing...")
    
    with col4:
        if st.button("📅 Schedule Meeting"):
            st.info("Opening calendar...")

def show_knowledge_base():
    """Comprehensive knowledge base and documentation"""
    st.header("📚 Ocean Science Knowledge Base")
    st.markdown("*Comprehensive Documentation & Research Library*")
    
    # Search functionality
    search_query = st.text_input("🔍 Search Knowledge Base", 
                                placeholder="Enter keywords, topics, or research areas...")
    
    # Category filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        category = st.selectbox("📂 Category", 
                               ["All", "Marine Biology", "Ocean Technology", "Climate Science", 
                                "Data Analysis", "AI/ML Applications", "Conservation"])
    
    with col2:
        content_type = st.selectbox("📄 Content Type",
                                   ["All", "Research Papers", "Tutorials", "Case Studies", 
                                    "Technical Docs", "Videos", "Datasets"])
    
    with col3:
        difficulty = st.selectbox("🎯 Difficulty Level",
                                 ["All", "Beginner", "Intermediate", "Advanced", "Expert"])
    
    # Featured content
    st.markdown("---")
    st.subheader("⭐ Featured Content")
    
    featured_content = [
        {
            "title": "🌊 Introduction to Ocean Data Analysis with Python",
            "type": "Tutorial",
            "category": "Data Analysis",
            "difficulty": "Beginner",
            "description": "Complete guide to analyzing oceanographic data using Python, Pandas, and visualization libraries.",
            "author": "Dr. Sarah Chen",
            "rating": 4.8,
            "views": "12.5K"
        },
        {
            "title": "🤖 AI-Powered Microplastic Detection",
            "type": "Research Paper",
            "category": "AI/ML Applications",
            "difficulty": "Advanced",
            "description": "Novel computer vision approach for automated microplastic classification in marine samples.",
            "author": "Prof. James Rodriguez",
            "rating": 4.9,
            "views": "8.3K"
        },
        {
            "title": "🐠 Coral Reef Restoration Case Study",
            "type": "Case Study",
            "category": "Conservation",
            "difficulty": "Intermediate",
            "description": "Successful implementation of AI-guided coral restoration in the Great Barrier Reef.",
            "author": "Dr. Maya Patel",
            "rating": 4.7,
            "views": "15.2K"
        }
    ]
    
    for content in featured_content:
        with st.expander(f"{content['title']} - ⭐ {content['rating']} ({content['views']} views)"):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"**📝 Description:** {content['description']}")
                st.markdown(f"**👤 Author:** {content['author']}")
                st.markdown(f"**📂 Category:** {content['category']}")
                st.markdown(f"**🎯 Difficulty:** {content['difficulty']}")
                
            with col2:
                st.markdown(f"**📄 Type:** {content['type']}")
                st.markdown(f"**👀 Views:** {content['views']}")
                if st.button(f"📖 Read", key=f"read_{content['title']}"):
                    st.info("Opening content...")
                if st.button(f"⭐ Bookmark", key=f"bookmark_{content['title']}"):
                    st.success("Bookmarked!")
    
    # Quick access sections
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🚀 Quick Start Guides")
        quick_guides = [
            "🐍 Python for Ocean Data Analysis",
            "🤖 Setting up AI Development Environment",
            "📊 Creating Ocean Data Visualizations",
            "🌊 Understanding Ocean Sensor Networks",
            "🔬 Multimodal AI for Marine Research"
        ]
        
        for guide in quick_guides:
            if st.button(guide, key=f"guide_{guide}"):
                st.info(f"Loading guide: {guide}")
    
    with col2:
        st.subheader("📊 Popular Datasets")
        datasets = [
            "🌡️ Global Ocean Temperature Archive",
            "🐠 Marine Biodiversity Database",
            "🏭 Ocean Pollution Monitoring Data",
            "🌊 Wave Energy Measurement Records",
            "🤖 Labeled Marine Image Collections"
        ]
        
        for dataset in datasets:
            if st.button(dataset, key=f"dataset_{dataset}"):
                st.info(f"Accessing dataset: {dataset}")
    
    # Contribution section
    st.markdown("---")
    st.subheader("➕ Contribute to Knowledge Base")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📝 Submit Content")
        content_title = st.text_input("📋 Content Title")
        content_author = st.text_input("👤 Author Name")
        content_category = st.selectbox("📂 Category", 
                                       ["Marine Biology", "Ocean Technology", "Climate Science", 
                                        "Data Analysis", "AI/ML Applications", "Conservation"])
        content_description = st.text_area("📝 Description")
        
    with col2:
        st.markdown("### 📤 Upload Files")
        uploaded_file = st.file_uploader("Choose file", type=['pdf', 'docx', 'ipynb', 'py'])
        content_tags = st.text_input("🏷️ Tags (comma-separated)")
        
        if st.button("📤 Submit Contribution", type="primary"):
            if content_title and content_author:
                st.success("✅ Content submitted for review!")
                st.info("📧 You'll receive notification once approved.")
            else:
                st.error("Please fill in required fields")

# Additional utility functions
def generate_api_documentation():
    """Generate API documentation for the platform"""
    api_docs = {
        "endpoints": [
            {
                "method": "GET",
                "path": "/api/v1/ocean-data/temperature",
                "description": "Retrieve ocean temperature data",
                "parameters": ["start_date", "end_date", "location", "depth_range"]
            },
            {
                "method": "POST",
                "path": "/api/v1/ai/analyze-image",
                "description": "Submit image for AI analysis",
                "parameters": ["image_file", "analysis_type"]
            },
            {
                "method": "GET",
                "path": "/api/v1/research/projects",
                "description": "Get list of active research projects",
                "parameters": ["status", "discipline", "limit"]
            }
        ]
    }
    return api_docs

def create_deployment_guide():
    """Create deployment guide for the application"""
    guide = """
    # 🚀 OceanaSync Hub Deployment Guide
    
    ## Prerequisites
    - Python 3.8+
    - Miniconda/Anaconda
    - Git
    
    ## Local Development Setup
    
    1. **Clone Repository**
    ```bash
    git clone https://github.com/oceanasync/hub.git
    cd oceanasync-hub
    ```
    
    2. **Create Conda Environment**
    ```bash
    conda create -n oceanasync python=3.9
    conda activate oceanasync
    ```
    
    3. **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```
    
    4. **Run Application**
    ```bash
    streamlit run app.py
    ```
    
    ## Production Deployment
    
    ### Option 1: Streamlit Cloud
    1. Push code to GitHub
    2. Connect to Streamlit Cloud
    3. Deploy with one click
    
    ### Option 2: Docker
    ```bash
    docker build -t oceanasync-hub .
    docker run -p 8501:8501 oceanasync-hub
    ```
    
    ### Option 3: AWS/Azure/GCP
    - Use container services
    - Configure load balancing
    - Set up monitoring
    
    ## Environment Variables
    ```
    OPENROUTER_API_KEY=your_api_key
    DATABASE_URL=your_database_url
    REDIS_URL=your_redis_url
    ```
    
    ## Monitoring & Maintenance
    - Health checks endpoint: /health
    - Metrics endpoint: /metrics
    - Logs: Check application logs for errors
    """
    return guide

# Run the application
if __name__ == "__main__":
    main()