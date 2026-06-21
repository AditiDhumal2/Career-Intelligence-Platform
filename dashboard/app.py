"""
Career Intelligence Platform - Complete Dashboard
FIXED: Chart visibility, text visibility, Career Path Mapper
All deprecated parameters updated
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys
import time
import re
import os
from collections import Counter

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))

from src.job_analyzer import JobMarketAnalyzer
from src.skill_gap_analyzer import SkillGapAnalyzer
from src.career_path_mapper import CareerPathMapper
from src.resume_parser import ResumeParser
from src.job_scraper import RealTimeJobScraper

# ============================================
# LLM/AI IMPORTS
# ============================================
try:
    from src.llm_advisor import LLMCareerAdvisor
    LLM_AVAILABLE = True
except ImportError:
    LLM_AVAILABLE = False

try:
    from src.resume_critic import ResumeCritic
    RESUME_CRITIC_AVAILABLE = True
except ImportError:
    RESUME_CRITIC_AVAILABLE = False

try:
    from src.interview_prep import InterviewPrep
    INTERVIEW_PREP_AVAILABLE = True
except ImportError:
    INTERVIEW_PREP_AVAILABLE = False

try:
    from src.market_trends import MarketTrendAnalyzer
    MARKET_TRENDS_AVAILABLE = True
except ImportError:
    MARKET_TRENDS_AVAILABLE = False

try:
    from src.nlp_query import NLPQueryProcessor
    NLP_QUERY_AVAILABLE = True
except ImportError:
    NLP_QUERY_AVAILABLE = False

try:
    from src.rag_retriever import RAGRetriever
    RAG_AVAILABLE = True
except ImportError:
    RAG_AVAILABLE = False

# Fix for PyArrow regex issue
pd.options.mode.string_storage = 'python'

# Page configuration
st.set_page_config(
    page_title="Career Intelligence Platform",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# FIXED CSS - Full Text Visibility
# ============================================
st.markdown("""
<style>
    /* Force ALL text to be visible */
    .stApp, .stApp p, .stApp h1, .stApp h2, .stApp h3, .stApp h4, 
    .stApp label, .stApp div, .stApp span, .stApp li,
    .stApp .stMarkdown, .stApp .stText, .stApp .stCaption,
    .stApp .markdown-text-container {
        color: #1a1a2e !important;
    }
    
    /* Sidebar text */
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3, [data-testid="stSidebar"] h4,
    [data-testid="stSidebar"] div, [data-testid="stSidebar"] span {
        color: #1a1a2e !important;
    }
    
    /* Metric cards - WHITE text on dark background */
    .metric-card {
        background: linear-gradient(135deg, #1E88E5 0%, #0D47A1 100%);
        padding: 1rem;
        border-radius: 12px;
        text-align: center;
        color: white !important;
        transition: all 0.3s ease;
        animation: fadeInUp 0.6s ease-out;
    }
    .metric-card h2, .metric-card h3, .metric-card p {
        color: white !important;
    }
    
    /* Section titles */
    .section-title {
        color: #1E88E5 !important;
        font-weight: 700 !important;
        font-size: 1.5rem !important;
        border-left: 4px solid #1E88E5;
        padding-left: 1rem;
    }
    
    /* Main header */
    .main-header {
        font-size: 2.5rem;
        background: linear-gradient(135deg, #1E88E5 0%, #0D47A1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    .sub-header {
        font-size: 1rem;
        color: #546E7A !important;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    
    /* Radio buttons */
    [data-testid="stRadio"] label {
        background-color: #ffffff !important;
        border: 1px solid #c0c4c8 !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
        margin: 4px 0 !important;
        color: #1E88E5 !important;
        font-weight: 500 !important;
        width: 100% !important;
        cursor: pointer !important;
    }
    [data-testid="stRadio"] label p {
        color: #1E88E5 !important;
        font-weight: 500 !important;
    }
    [data-testid="stRadio"] [aria-checked="true"] + div {
        background: linear-gradient(135deg, #1E88E5 0%, #0D47A1 100%) !important;
        border: none !important;
    }
    [data-testid="stRadio"] [aria-checked="true"] + div p {
        color: white !important;
    }
    
    /* Buttons */
    .stButton > button {
        color: white !important;
        background: linear-gradient(135deg, #1E88E5 0%, #0D47A1 100%) !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.6rem 1.8rem !important;
        font-weight: 600 !important;
    }
    .stButton > button p {
        color: white !important;
    }
    
    /* Info boxes */
    .info-box {
        background: #E3F2FD !important;
        padding: 1rem !important;
        border-radius: 10px !important;
        border-left: 4px solid #1E88E5 !important;
        margin: 1rem 0 !important;
        color: #1a1a2e !important;
    }
    .info-box p {
        color: #1a1a2e !important;
    }
    
    /* Success boxes */
    .success-box {
        background: #E8F5E9 !important;
        padding: 1rem !important;
        border-radius: 10px !important;
        border-left: 4px solid #43A047 !important;
        margin: 1rem 0 !important;
        color: #1a1a2e !important;
    }
    .success-box p {
        color: #1a1a2e !important;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        color: #1a1a2e !important;
        font-weight: 700 !important;
    }
    [data-testid="stMetricLabel"] {
        color: #546E7A !important;
    }
    
    /* Sidebar background */
    [data-testid="stSidebar"] {
        background: #f0f2f6 !important;
        border-right: 1px solid #d0d4d8 !important;
    }
    
    /* App background */
    .stApp, .stApp > header, .stApp > div, .main, .block-container {
        background-color: #ffffff !important;
    }
    
    /* Skill badges */
    .skill-badge {
        display: inline-block;
        background: linear-gradient(135deg, #1E88E5 0%, #0D47A1 100%);
        color: white !important;
        padding: 5px 14px;
        border-radius: 25px;
        margin: 4px;
        font-size: 13px;
        font-weight: 500;
        cursor: pointer;
    }
    
    /* Animations */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-40px); }
        to { opacity: 1; transform: translateX(0); }
    }
    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(40px); }
        to { opacity: 1; transform: translateX(0); }
    }
    @keyframes pulse {
        0% { transform: scale(1); opacity: 1; }
        50% { transform: scale(1.05); opacity: 0.9; }
        100% { transform: scale(1); opacity: 1; }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = "📊 Market Intelligence"

@st.cache_resource
def load_components():
    """Load all analyzers with caching"""
    with st.spinner('🚀 Loading Career Intelligence Engine...'):
        time.sleep(0.5)
        analyzer = JobMarketAnalyzer()
        skill_gap_analyzer = SkillGapAnalyzer(analyzer.df)
        career_mapper = CareerPathMapper()
    return analyzer, skill_gap_analyzer, career_mapper

def main():
    """Main dashboard function"""
    
    # Header
    st.markdown('<div class="main-header">🎯 Career Intelligence Platform</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">AI-Powered Career Guidance | Real-time Market Intelligence | Personalized Recommendations</div>', unsafe_allow_html=True)
    
    # Load data
    with st.spinner('📊 Analyzing job market data...'):
        analyzer, skill_gap_analyzer, career_mapper = load_components()
    
    if analyzer.df is None:
        st.error("❌ Could not load data. Please generate dataset first!")
        st.info("Run: python data/generate_large_dataset.py")
        return
    
    # SIDEBAR
    with st.sidebar:
        st.markdown("### 🎯 Career Navigator")
        st.markdown("*Your personal career intelligence assistant*")
        st.markdown("---")
        
        selected_page = st.radio(
            "Navigation Menu",
            ["📊 Market Intelligence", "💡 Skill Gap Analyzer", "🗺️ Career Path Mapper", "📈 Analytics Hub", "🚀 Advanced AI Features"],
            key="main_navigation",
            label_visibility="collapsed",
            index=["📊 Market Intelligence", "💡 Skill Gap Analyzer", "🗺️ Career Path Mapper", "📈 Analytics Hub", "🚀 Advanced AI Features"].index(st.session_state.page)
        )
        st.session_state.page = selected_page
        
        st.markdown("---")
        
        st.markdown("### 📊 Market Stats")
        total_jobs = len(analyzer.df)
        unique_skills = analyzer.df['skill_required'].nunique()
        unique_roles = analyzer.df['job_title'].nunique()
        
        st.metric("Jobs Analyzed", f"{total_jobs:,}")
        st.metric("Unique Skills", f"{unique_skills:,}")
        st.metric("Job Roles", f"{unique_roles:,}")
        st.metric("Locations", f"{analyzer.df['location'].nunique()}")
        st.metric("Avg Salary", f"${analyzer.df['avg_salary'].mean():,.0f}")
        st.metric("Avg Demand", f"{analyzer.df['demand_score'].mean():.0f}/100")
        
        st.markdown("---")
        st.markdown("*Built with ❤️ for Career Success*")
    
    # Page routing
    if st.session_state.page == "📊 Market Intelligence":
        show_market_intelligence(analyzer)
    elif st.session_state.page == "💡 Skill Gap Analyzer":
        show_skill_gap_analyzer(analyzer, skill_gap_analyzer)
    elif st.session_state.page == "🗺️ Career Path Mapper":
        show_career_path_mapper(career_mapper)
    elif st.session_state.page == "📈 Analytics Hub":
        show_analytics_hub(analyzer)
    elif st.session_state.page == "🚀 Advanced AI Features":
        show_advanced_ai_features(analyzer, skill_gap_analyzer, career_mapper)

# ============================================
# MARKET INTELLIGENCE - FIXED CHARTS
# ============================================
def show_market_intelligence(analyzer):
    """Market intelligence dashboard - FIXED chart visibility"""
    
    st.markdown('<div class="section-title">📈 Market Intelligence Dashboard</div>', unsafe_allow_html=True)
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        locations = ['All'] + sorted(analyzer.df['location'].unique().tolist())
        selected_location = st.selectbox("📍 Filter by Location", locations)
    with col2:
        if 'industry' in analyzer.df.columns:
            industries = ['All'] + sorted(analyzer.df['industry'].unique().tolist())
            selected_industry = st.selectbox("🏭 Filter by Industry", industries)
        else:
            selected_industry = 'All'
    with col3:
        if 'remote_policy' in analyzer.df.columns:
            remote_options = ['All', 'Remote', 'Hybrid', 'On-site', 'Flexible']
            selected_remote = st.selectbox("🏠 Remote Policy", remote_options)
        else:
            selected_remote = 'All'
    
    # Apply filters
    df_filtered = analyzer.df.copy()
    if selected_location != 'All':
        df_filtered = df_filtered[df_filtered['location'] == selected_location]
    if selected_industry != 'All' and 'industry' in analyzer.df.columns:
        df_filtered = df_filtered[df_filtered['industry'] == selected_industry]
    if selected_remote != 'All' and 'remote_policy' in analyzer.df.columns:
        df_filtered = df_filtered[df_filtered['remote_policy'] == selected_remote]
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>📊 JOBS</h3>
            <h2>{len(df_filtered):,}</h2>
            <p>Total Openings</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        avg_salary = df_filtered['avg_salary'].mean() if len(df_filtered) > 0 else 0
        st.markdown(f"""
        <div class="metric-card">
            <h3>💰 SALARY</h3>
            <h2>${avg_salary:,.0f}</h2>
            <p>Average Annual</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        avg_demand = df_filtered['demand_score'].mean() if len(df_filtered) > 0 else 0
        st.markdown(f"""
        <div class="metric-card">
            <h3>📈 DEMAND</h3>
            <h2>{avg_demand:.0f}/100</h2>
            <p>Market Score</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        if 'is_remote_friendly' in df_filtered.columns and len(df_filtered) > 0:
            remote_pct = df_filtered['is_remote_friendly'].mean() * 100
        else:
            remote_pct = 0
        st.markdown(f"""
        <div class="metric-card">
            <h3>🏠 REMOTE</h3>
            <h2>{remote_pct:.0f}%</h2>
            <p>Remote Friendly</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ============================================
    # CHARTS - FIXED VISIBILITY
    # ============================================
    
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown("#### 💼 Top Paying Job Roles")
        top_jobs = analyzer.get_top_paying_jobs(8)
        
        fig = px.bar(
            top_jobs, 
            x='avg_salary', 
            y=top_jobs.index, 
            orientation='h',
            title='Average Annual Salary by Role',
            labels={'avg_salary': 'Salary ($)', 'y': ''},
            color='avg_salary', 
            color_continuous_scale='Blues',
            text='avg_salary'
        )
        fig.update_traces(
            texttemplate='${:,.0f}', 
            textposition='outside',
            textfont=dict(size=10, color='#1a1a2e'),
            cliponaxis=False
        )
        fig.update_layout(
            height=450,
            showlegend=False,
            xaxis=dict(
                tickformat='$,.0f',
                gridcolor='lightgray',
                title_font=dict(color='#1a1a2e'),
                tickfont=dict(color='#1a1a2e')
            ),
            yaxis=dict(
                automargin=True,
                tickfont=dict(color='#1a1a2e', size=11)
            ),
            title_font=dict(color='#1a1a2e'),
            margin=dict(l=10, r=80, t=50, b=20),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig, width='stretch')
    
    with col2:
        st.markdown("#### 🎯 Most In-Demand Skills")
        skill_demand = analyzer.get_skills_by_demand(10)
        
        fig = px.bar(
            skill_demand, 
            x='demand_score', 
            y=skill_demand.index, 
            orientation='h',
            title='Skill Demand Score (0-100)',
            labels={'demand_score': 'Demand Score', 'y': ''},
            color='demand_score', 
            color_continuous_scale='Teal',
            text='demand_score'
        )
        fig.update_traces(
            texttemplate='%{text:.0f}', 
            textposition='outside',
            textfont=dict(size=10, color='#1a1a2e'),
            cliponaxis=False
        )
        fig.update_layout(
            height=450,
            showlegend=False,
            xaxis=dict(
                range=[0, 105],
                gridcolor='lightgray',
                title_font=dict(color='#1a1a2e'),
                tickfont=dict(color='#1a1a2e')
            ),
            yaxis=dict(
                automargin=True,
                tickfont=dict(color='#1a1a2e', size=11)
            ),
            title_font=dict(color='#1a1a2e'),
            margin=dict(l=10, r=50, t=50, b=20),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig, width='stretch')
    
    # Skills percentage section
    st.markdown("---")
    st.markdown("#### 📊 Skill Market Penetration")
    
    all_skills = []
    for skills in analyzer.df['skill_required']:
        if isinstance(skills, str):
            if ',' in skills:
                all_skills.extend([s.strip() for s in skills.split(',')])
            else:
                all_skills.append(skills)
    
    skill_counts = Counter(all_skills)
    skill_percent_df = pd.DataFrame(skill_counts.items(), columns=['Skill', 'Count'])
    skill_percent_df['Percentage'] = (skill_percent_df['Count'] / len(analyzer.df)) * 100
    skill_percent_df = skill_percent_df.sort_values('Percentage', ascending=False).head(15)
    
    fig = px.bar(
        skill_percent_df,
        x='Percentage',
        y='Skill',
        orientation='h',
        title='Top 15 Skills by Market Penetration',
        labels={'Percentage': '% of Job Postings', 'Skill': ''},
        color='Percentage',
        color_continuous_scale='Viridis',
        text='Percentage'
    )
    fig.update_traces(
        texttemplate='%{text:.1f}%', 
        textposition='outside',
        textfont=dict(size=10, color='#1a1a2e'),
        cliponaxis=False
    )
    fig.update_layout(
        height=550,
        xaxis=dict(
            gridcolor='lightgray',
            title_font=dict(color='#1a1a2e'),
            tickfont=dict(color='#1a1a2e')
        ),
        yaxis=dict(
            automargin=True,
            tickfont=dict(color='#1a1a2e', size=11)
        ),
        title_font=dict(color='#1a1a2e'),
        margin=dict(l=10, r=80, t=50, b=20),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig, width='stretch')
    
    # Location distribution
    st.markdown("---")
    st.markdown("#### 🗺️ Geographic Distribution")
    
    location_stats = analyzer.df.groupby('location').size().reset_index(name='count')
    location_stats = location_stats.sort_values('count', ascending=False).head(12)
    
    fig = px.bar(
        location_stats, 
        x='count', 
        y='location', 
        orientation='h',
        title='Top 12 Locations by Job Opportunities',
        labels={'count': 'Number of Jobs', 'location': ''},
        color='count',
        color_continuous_scale='Reds',
        text='count'
    )
    fig.update_traces(
        texttemplate='%{text:,}', 
        textposition='outside',
        textfont=dict(size=10, color='#1a1a2e'),
        cliponaxis=False
    )
    fig.update_layout(
        height=450,
        xaxis=dict(
            gridcolor='lightgray',
            title_font=dict(color='#1a1a2e'),
            tickfont=dict(color='#1a1a2e')
        ),
        yaxis=dict(
            automargin=True,
            tickfont=dict(color='#1a1a2e', size=11)
        ),
        title_font=dict(color='#1a1a2e'),
        margin=dict(l=10, r=60, t=50, b=20),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig, width='stretch')

# ============================================
# SKILL GAP ANALYZER
# ============================================
def show_skill_gap_analyzer(analyzer, skill_gap_analyzer):
    """Interactive skill gap analyzer"""
    
    st.markdown('<div class="section-title">💡 AI-Powered Skill Gap Analyzer</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
        🤖 This tool analyzes your current skills against market requirements and provides personalized learning recommendations.
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 👤 Your Current Skills")
        user_skills_input = st.text_area(
            "",
            placeholder="Enter your skills (comma-separated)\nExample: Python, SQL, Excel, Machine Learning",
            height=120,
            label_visibility="collapsed"
        )
        user_skills = [s.strip().title() for s in user_skills_input.split(',')] if user_skills_input else []
        
        if user_skills:
            st.markdown("**Your Skills:**")
            skills_html = "".join([f'<span class="skill-badge">{skill}</span>' for skill in user_skills])
            st.markdown(f'<div style="margin: 10px 0;">{skills_html}</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### 🎯 Target Career")
        all_roles = sorted(analyzer.df['job_title'].unique())
        target_role = st.selectbox("Select your dream job", all_roles)
        
        role_data = analyzer.df[analyzer.df['job_title'] == target_role]
        avg_salary = role_data['avg_salary'].mean()
        demand = role_data['demand_score'].mean()
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("💰 Average Salary", f"${avg_salary:,.0f}")
        with col_b:
            st.metric("📈 Market Demand", f"{demand:.0f}/100")
    
    if user_skills and target_role:
        st.markdown("---")
        st.markdown("### 📊 Gap Analysis Results")
        
        with st.spinner('🔍 Analyzing your career fit...'):
            time.sleep(0.5)
            
            results = skill_gap_analyzer.analyze_gap(user_skills, target_role)
            
            if 'error' not in results:
                st.progress(results['match_percentage'] / 100, text=f"Overall Match: {results['match_percentage']}%")
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("✅ Matched", len(results['matched_skills']))
                with col2:
                    st.metric("❌ Missing", len(results['missing_skills']))
                with col3:
                    st.metric("📋 Required", results['required_skills_count'])
                with col4:
                    st.metric("📊 Match Score", f"{results['match_percentage']}%")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if results['matched_skills']:
                        st.markdown("#### ✅ Skills You Have")
                        for skill in results['matched_skills'][:10]:
                            st.success(f"✓ {skill}")
                    else:
                        st.warning("No matching skills found")
                
                with col2:
                    if results['missing_skills']:
                        st.markdown("#### 🎯 Prioritized Learning Path")
                        for i, skill_info in enumerate(results['learning_path'][:8], 1):
                            st.markdown(f"**{i}. {skill_info['priority_icon']} {skill_info['skill']}** - {skill_info['priority']} Priority")
                            st.caption(f"Est. {skill_info['estimated_time']} | Market Demand: {skill_info['market_demand']:.0f}/100")
                
                st.markdown("---")
                st.markdown("#### 📚 Recommendation")
                st.info(results['status']['message'])
            else:
                st.error(results['error'])

# ============================================
# CAREER PATH MAPPER - FIXED
# ============================================
def show_career_path_mapper(career_mapper):
    """Career path mapper - FIXED: Shows results properly"""
    
    st.markdown('<div class="section-title">🗺️ Career Path Mapper</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
        🚀 Plan your career journey! Select your current role and dream role to visualize the complete career roadmap.
    </div>
    """, unsafe_allow_html=True)
    
    # Get all available roles
    all_roles = career_mapper.get_all_available_roles()
    
    if not all_roles:
        st.error("No career paths available. Please check your data.")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📍 Current Position")
        current_role = st.selectbox("Where are you now?", all_roles, index=0)
    
    with col2:
        st.markdown("#### 🎯 Dream Position")
        target_role = st.selectbox("Where do you want to go?", all_roles, index=min(3, len(all_roles)-1))
    
    # Use width='stretch' instead of use_container_width
    if st.button("🚀 Generate Career Path", width="stretch", type="primary"):
        with st.spinner('🗺️ Mapping your career journey...'):
            time.sleep(0.5)
            
            path_data = career_mapper.get_career_path(current_role, target_role)
            
            if 'error' not in path_data:
                st.markdown("---")
                st.markdown("### 📍 Your Career Roadmap")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Steps", path_data['total_steps'])
                with col2:
                    st.metric("Estimated Time", path_data['estimated_time'])
                with col3:
                    st.metric("Career Track", path_data['track'])
                
                st.markdown("---")
                
                # Display each step
                for i, step in enumerate(path_data['path'], 1):
                    with st.container():
                        st.markdown(f"### Step {i}: {step['role']}")
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.markdown(f"💰 **{step['salary']}**")
                        with col2:
                            st.markdown(f"⏰ **{step['experience']}** years")
                        with col3:
                            st.markdown(f"📋 **Skills:** {', '.join(step['required_skills'][:3])}...")
                        
                        if i < len(path_data['path']):
                            st.markdown("⬇️ **Next Level**")
                            st.markdown("---")
            else:
                st.error(path_data['error'])

# ============================================
# ANALYTICS HUB
# ============================================
def show_analytics_hub(analyzer):
    """Analytics hub with insights"""
    
    st.markdown('<div class="section-title">📊 Analytics Hub</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 💡 Market Intelligence")
        top_skill = analyzer.get_skills_by_demand(1).index[0]
        top_role = analyzer.get_top_paying_jobs(1).index[0]
        top_location = analyzer.get_top_locations(1).index[0]
        
        insights = [
            f"🎯 **{top_skill}** is the most in-demand skill",
            f"💰 **{top_role}** offers highest average salary",
            f"📍 **{top_location}** has most job opportunities",
            f"📈 Average market demand: {analyzer.df['demand_score'].mean():.0f}/100"
        ]
        
        for insight in insights:
            st.info(insight)
    
    with col2:
        st.markdown("#### 🚀 Career Action Items")
        st.markdown("""
        - 📝 **Resume Optimization**: Highlight in-demand skills prominently
        - 🎓 **Learning Path**: Focus on top 3 missing skills
        - 🌍 **Location Strategy**: Target high-opportunity cities
        - 🤝 **Networking**: Connect with professionals in target roles
        - 📊 **Portfolio**: Build projects showcasing top skills
        """)
    
    # Salary distribution
    st.markdown("---")
    st.markdown("#### 📈 Salary Distribution Analysis")
    
    fig = px.histogram(
        analyzer.df, 
        x='avg_salary', 
        nbins=30,
        title='Salary Distribution Across All Jobs',
        labels={'avg_salary': 'Annual Salary ($)', 'count': 'Number of Jobs'},
        color_discrete_sequence=['#1E88E5']
    )
    fig.update_layout(
        height=450,
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_tickfont=dict(color='#1a1a2e'),
        yaxis_tickfont=dict(color='#1a1a2e'),
        title_font=dict(color='#1a1a2e')
    )
    st.plotly_chart(fig, width='stretch')

# ============================================
# ADVANCED AI FEATURES
# ============================================
def show_advanced_ai_features(analyzer, skill_gap_analyzer, career_mapper):
    """Show all AI-powered features"""
    
    st.markdown('<div class="section-title">🚀 Advanced AI Features</div>', unsafe_allow_html=True)
    
    tabs = ["💬 AI Advisor"]
    
    if RESUME_CRITIC_AVAILABLE:
        tabs.append("📄 Resume Critic")
    if INTERVIEW_PREP_AVAILABLE:
        tabs.append("🎤 Interview Prep")
    if MARKET_TRENDS_AVAILABLE:
        tabs.append("📈 Market Trends")
    if NLP_QUERY_AVAILABLE:
        tabs.append("🔍 NLP Query")
    if RAG_AVAILABLE:
        tabs.append("🧠 RAG Search")
    
    tab_objects = st.tabs(tabs)
    tab_index = 0
    
    with tab_objects[tab_index]:
        show_ai_advisor()
    tab_index += 1
    
    if RESUME_CRITIC_AVAILABLE and tab_index < len(tab_objects):
        with tab_objects[tab_index]:
            show_resume_critic(analyzer)
        tab_index += 1
    
    if INTERVIEW_PREP_AVAILABLE and tab_index < len(tab_objects):
        with tab_objects[tab_index]:
            show_interview_prep()
        tab_index += 1
    
    if MARKET_TRENDS_AVAILABLE and tab_index < len(tab_objects):
        with tab_objects[tab_index]:
            show_market_trends()
        tab_index += 1
    
    if NLP_QUERY_AVAILABLE and tab_index < len(tab_objects):
        with tab_objects[tab_index]:
            show_nlp_query(analyzer)
        tab_index += 1
    
    if RAG_AVAILABLE and tab_index < len(tab_objects):
        with tab_objects[tab_index]:
            show_rag_search(analyzer)

def show_ai_advisor():
    """LLM-powered career advisor"""
    st.markdown("#### 💬 AI Career Advisor")
    
    st.markdown("""
    <div class="info-box">
        🤖 Get personalized career advice from our AI advisor powered by Gemini.
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        user_skills = st.text_area(
            "Your Skills",
            placeholder="Enter your skills (comma-separated)",
            height=80
        )
        user_skills_list = [s.strip() for s in user_skills.split(',')] if user_skills else []
        
        target_role = st.selectbox(
            "Target Role",
            [''] + ['Data Scientist', 'Data Analyst', 'Data Engineer', 'ML Engineer', 'Business Analyst']
        )
    
    with col2:
        custom_question = st.text_area(
            "Ask a question",
            placeholder="What specific advice are you looking for?",
            height=100
        )
    
    if st.button("Get AI Advice", type="primary", width="stretch"):
        with st.spinner("🤔 AI is thinking..."):
            advisor = LLMCareerAdvisor()
            
            if custom_question:
                # Simulate response
                response = advisor._get_fallback_response(user_skills_list, target_role)
            else:
                response = advisor.get_career_advice(user_skills_list, target_role)
            
            if response.get('success'):
                st.markdown("#### 💡 AI Advice")
                st.markdown(response.get('advice'))
            else:
                st.error("AI service unavailable. Please try again later.")

def show_resume_critic(analyzer):
    """Resume critique"""
    st.markdown("#### 📄 Resume Critic & Improvement")
    
    st.markdown("""
    <div class="info-box">
        🔍 Upload your resume to get detailed feedback and improvement suggestions.
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Upload Resume", type=['pdf', 'docx', 'txt'])
    
    if uploaded_file is not None:
        temp_path = f"temp_resume_{uploaded_file.name}"
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        with st.spinner("Analyzing your resume..."):
            critic = ResumeCritic()
            analysis = critic.analyze_resume(temp_path)
            
            if 'error' not in analysis:
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Word Count", analysis.get('word_count', 0))
                with col2:
                    st.metric("Keywords Found", len(analysis.get('keywords_found', {}).get('data_science', [])))
                
                if analysis.get('suggestions'):
                    st.markdown("#### 📋 Improvement Suggestions")
                    for suggestion in analysis.get('suggestions', []):
                        st.warning(suggestion)
                else:
                    st.success("✅ Your resume looks great!")
            else:
                st.error(analysis['error'])
        
        if os.path.exists(temp_path):
            os.remove(temp_path)

def show_interview_prep():
    """Interview preparation"""
    st.markdown("#### 🎤 Interview Preparation")
    
    st.markdown("""
    <div class="info-box">
        🎯 Get role-specific interview questions and preparation tips.
    </div>
    """, unsafe_allow_html=True)
    
    prep = InterviewPrep()
    
    col1, col2 = st.columns(2)
    with col1:
        role_options = list(prep.question_bank.keys())
        target_role = st.selectbox("Select Target Role", role_options)
        question_count = st.slider("Number of Questions", 1, 10, 5)
    
    if st.button("Generate Interview Plan", type="primary", width="stretch"):
        plan = prep.generate_interview_plan(target_role)
        st.markdown(plan)
    
    questions = prep.get_questions(target_role, question_count)
    for category, q_list in questions.items():
        with st.expander(f"📌 {category.title()} Questions"):
            for q in q_list:
                st.markdown(f"• {q}")

def show_market_trends():
    """Market trends"""
    st.markdown("#### 📈 Real-Time Market Trends")
    
    role = st.selectbox(
        "Select Role",
        ["Data Scientist", "Data Analyst", "Data Engineer", "ML Engineer", "Business Analyst"]
    )
    
    if st.button("Fetch Trends", type="primary", width="stretch"):
        with st.spinner("Fetching market trends..."):
            analyzer = MarketTrendAnalyzer()
            trends = analyzer.fetch_trends(role)
            
            if trends:
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Job Growth Rate", trends['job_counts'].get('growth_rate', 'N/A'))
                with col2:
                    st.metric("Average Salary", f"${trends['salary_trends'].get('current_avg', 0):,.0f}")
                with col3:
                    st.metric("Salary Growth", trends['salary_trends'].get('growth', 'N/A'))
                
                st.info(trends.get('market_sentiment', 'Data being analyzed'))

def show_nlp_query(analyzer):
    """NLP Query"""
    st.markdown("#### 🔍 Natural Language Query")
    
    query = st.text_input(
        "Ask a question",
        placeholder="e.g., What skills do I need to become a Data Scientist?"
    )
    
    if query and st.button("Ask", type="primary", width="stretch"):
        with st.spinner("Processing your question..."):
            processor = NLPQueryProcessor(analyzer.df)
            response = processor.process_query(query)
            st.markdown(response.get('response', 'No response'))

def show_rag_search(analyzer):
    """RAG Search"""
    st.markdown("#### 🧠 RAG-Powered Semantic Search")
    
    query = st.text_input(
        "Search by meaning",
        placeholder="e.g., Find jobs that require Python and pay over $100k"
    )
    
    top_k = st.slider("Number of results", 1, 10, 5)
    
    if query and st.button("Search", type="primary", width="stretch"):
        with st.spinner("Searching with AI..."):
            retriever = RAGRetriever(analyzer.df)
            results = retriever.search(query, top_k)
            
            if results:
                for i, result in enumerate(results, 1):
                    with st.expander(f"Result {i}: {result.get('metadata', {}).get('job_title', 'Unknown')}"):
                        st.markdown(result.get('content', ''))
            else:
                st.warning("No results found.")

if __name__ == "__main__":
    main()