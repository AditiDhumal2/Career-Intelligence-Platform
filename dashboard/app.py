"""
Career Intelligence Platform - Complete Dashboard
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys
import time
import re
import os

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))

# Import local modules with error handling
try:
    from src.job_analyzer import JobMarketAnalyzer
    from src.skill_gap_analyzer import SkillGapAnalyzer
    from src.career_path_mapper import CareerPathMapper
    from src.resume_parser import ResumeParser
    from src.job_scraper import RealTimeJobScraper
except ImportError as e:
    st.error(f"⚠️ Error importing modules: {e}")
    st.info("Make sure all src files are present in the repository")
    sys.exit(1)

# Fix for PyArrow regex issue
pd.options.mode.string_storage = 'python'

# Page configuration
st.set_page_config(
    page_title="Career Intelligence Platform",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with animations
st.markdown("""
<style>
    /* Professional color scheme */
    :root {
        --primary: #1E88E5;
        --secondary: #0D47A1;
        --accent: #00ACC1;
        --success: #43A047;
        --warning: #FB8C00;
        --danger: #E53935;
        --dark: #263238;
        --light: #ECEFF1;
    }
    
    /* Keyframe animations */
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
    
    /* Header animations */
    .main-header {
        font-size: 2.5rem;
        background: linear-gradient(135deg, #1E88E5 0%, #0D47A1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
        animation: fadeInUp 0.8s ease-out;
    }
    
    .sub-header {
        font-size: 1rem;
        color: #546E7A;
        text-align: center;
        margin-bottom: 1.5rem;
        animation: fadeInUp 0.8s ease-out 0.2s both;
    }
    
    .section-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #1E88E5;
        margin-top: 0.5rem;
        margin-bottom: 1.5rem;
        border-left: 4px solid #1E88E5;
        padding-left: 1rem;
        animation: slideInLeft 0.6s ease-out;
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #1E88E5 0%, #0D47A1 100%);
        padding: 1rem;
        border-radius: 12px;
        text-align: center;
        color: white;
        transition: all 0.3s ease;
        animation: fadeInUp 0.6s ease-out;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        animation: pulse 0.5s ease;
        box-shadow: 0 10px 25px rgba(30,136,229,0.3);
    }
    
    .metric-card h3 {
        font-size: 0.85rem;
        margin: 0;
        opacity: 0.9;
        letter-spacing: 1px;
    }
    
    .metric-card h2 {
        font-size: 1.8rem;
        margin: 0.3rem 0;
        font-weight: 700;
    }
    
    .metric-card p {
        font-size: 0.75rem;
        margin: 0;
        opacity: 0.8;
    }
    
    /* Info boxes */
    .info-box {
        background: #E3F2FD;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1E88E5;
        margin: 1rem 0;
        animation: slideInRight 0.5s ease-out;
        transition: all 0.3s;
    }
    
    .info-box:hover {
        transform: translateX(5px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    .success-box {
        background: #E8F5E9;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #43A047;
        margin: 1rem 0;
        animation: slideInRight 0.5s ease-out;
        transition: all 0.3s;
    }
    
    .success-box:hover {
        transform: translateX(5px);
    }
    
    /* Skill badges */
    .skill-badge {
        display: inline-block;
        background: linear-gradient(135deg, #1E88E5 0%, #0D47A1 100%);
        color: white;
        padding: 5px 14px;
        border-radius: 25px;
        margin: 4px;
        font-size: 13px;
        font-weight: 500;
        transition: all 0.3s ease;
        animation: fadeInUp 0.4s ease-out;
        cursor: pointer;
    }
    
    .skill-badge:hover {
        transform: scale(1.08) translateY(-2px);
        box-shadow: 0 5px 15px rgba(30,136,229,0.4);
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #1E88E5 0%, #0D47A1 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.8rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(30,136,229,0.4);
        animation: pulse 0.5s;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
        border-right: 1px solid #dee2e6;
    }
    
    /* Radio button styling */
    .stRadio > div {
        gap: 0.5rem;
    }
    
    .stRadio label {
        padding: 0.5rem 1rem;
        border-radius: 10px;
        transition: all 0.3s ease;
    }
    
    .stRadio label:hover {
        background: #E3F2FD;
        transform: translateX(5px);
    }
    
    /* Chart containers */
    .chart-container {
        animation: fadeInUp 0.7s ease-out;
        background: white;
        border-radius: 12px;
        padding: 0.5rem;
    }
    
    /* Stats panel */
    .stats-panel {
        background: white;
        border-radius: 12px;
        padding: 1rem;
        margin-top: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for navigation
if 'page' not in st.session_state:
    st.session_state.page = "📊 Market Intelligence"

# Initialize components
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
    
    # SIDEBAR - Navigation at TOP, Stats below
    with st.sidebar:
        # Navigation Section - TOP of sidebar
        st.markdown("### 🧭 Navigation")
        
        page = st.radio(
            "",
            ["📊 Market Intelligence", "💡 Skill Gap Analyzer", "🗺️ Career Path Mapper", "📈 Analytics Hub", "🚀 Advanced Features"],
            label_visibility="collapsed",
            index=["📊 Market Intelligence", "💡 Skill Gap Analyzer", "🗺️ Career Path Mapper", "📈 Analytics Hub", "🚀 Advanced Features"].index(st.session_state.page)
        )
        
        st.session_state.page = page
        st.markdown("---")
        
        # Market Stats Section - BELOW navigation
        st.markdown("### 📊 Market Stats")
        
        total_jobs = len(analyzer.df)
        unique_skills = analyzer.df['skill_required'].nunique()
        unique_roles = analyzer.df['job_title'].nunique()
        
        st.markdown(f"""
        <div class="stats-panel">
            <p><strong>📈 Jobs Analyzed:</strong><br>{total_jobs:,}</p>
            <p><strong>🎨 Unique Skills:</strong><br>{unique_skills:,}</p>
            <p><strong>💼 Job Roles:</strong><br>{unique_roles:,}</p>
            <p><strong>📍 Locations:</strong><br>{analyzer.df['location'].nunique()}</p>
            <hr>
            <p><strong>💰 Avg Salary:</strong><br>${analyzer.df['avg_salary'].mean():,.0f}</p>
            <p><strong>📈 Avg Demand:</strong><br>{analyzer.df['demand_score'].mean():.0f}/100</p>
        </div>
        """, unsafe_allow_html=True)
        
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
    elif st.session_state.page == "🚀 Advanced Features":
        show_advanced_features(analyzer, skill_gap_analyzer, career_mapper)

def show_market_intelligence(analyzer):
    """Market intelligence dashboard"""
    
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
        elif 'remote_policy' in df_filtered.columns and len(df_filtered) > 0:
            remote_count = len(df_filtered[df_filtered['remote_policy'].isin(['Remote', 'Hybrid', 'Flexible'])])
            remote_pct = (remote_count / len(df_filtered) * 100)
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
    
    # Two column layout
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown("#### 💼 Top Paying Job Roles")
        top_jobs = analyzer.get_top_paying_jobs(8)
        fig = px.bar(
            top_jobs, x='avg_salary', y=top_jobs.index, orientation='h',
            title='Average Annual Salary by Role',
            labels={'avg_salary': 'Salary ($)', 'y': ''},
            color='avg_salary', color_continuous_scale='Blues', text='avg_salary'
        )
        fig.update_traces(texttemplate='${:,.0f}', textposition='outside', textfont=dict(size=11))
        fig.update_layout(height=450, showlegend=False, margin=dict(l=10, r=80, t=50, b=20), plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### 🎯 Most In-Demand Skills")
        skill_demand = analyzer.get_skills_by_demand(10)
        fig = px.bar(
            skill_demand, x='demand_score', y=skill_demand.index, orientation='h',
            title='Skill Demand Score (0-100)',
            labels={'demand_score': 'Demand Score', 'y': ''},
            color='demand_score', color_continuous_scale='Teal', text='demand_score'
        )
        fig.update_traces(texttemplate='%{text:.0f}', textposition='outside', textfont=dict(size=11))
        fig.update_layout(height=450, showlegend=False, margin=dict(l=10, r=50, t=50, b=20), plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
    
    # Skills percentage
    st.markdown("---")
    st.markdown("#### 📊 Skill Market Penetration")
    
    from collections import Counter
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
        skill_percent_df, x='Percentage', y='Skill', orientation='h',
        title='Top 15 Skills by Market Penetration',
        labels={'Percentage': '% of Job Postings', 'Skill': ''},
        color='Percentage', color_continuous_scale='Viridis', text='Percentage'
    )
    fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig.update_layout(height=550, margin=dict(l=10, r=80, t=50, b=20), plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)

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
            height=120
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

def show_career_path_mapper(career_mapper):
    """Career path mapper"""
    
    st.markdown('<div class="section-title">🗺️ Career Path Mapper</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
        🚀 Plan your career journey! Select your current role and dream role to visualize the complete career roadmap.
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    all_roles = career_mapper.get_all_available_roles()
    
    with col1:
        st.markdown("#### 📍 Current Position")
        current_role = st.selectbox("Where are you now?", all_roles, index=0)
    
    with col2:
        st.markdown("#### 🎯 Dream Position")
        target_role = st.selectbox("Where do you want to go?", all_roles, index=min(3, len(all_roles)-1))
    
    if st.button("🚀 Generate Career Path", type="primary", use_container_width=True):
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
                
                for i, step in enumerate(path_data['path'], 1):
                    with st.container():
                        col1, col2, col3, col4 = st.columns([1, 3, 2, 2])
                        with col1:
                            st.markdown(f"### Step {i}")
                        with col2:
                            st.markdown(f"**{step['role']}**")
                        with col3:
                            st.markdown(f"💰 {step['salary']}")
                        with col4:
                            st.markdown(f"⏰ {step['experience']} years")
                        
                        st.markdown(f"**Required Skills:** {', '.join(step['required_skills'][:5])}")
                        if i < len(path_data['path']):
                            st.markdown("⬇️ *Next Level* ⬇️")
                            st.markdown("---")
            else:
                st.error(path_data['error'])

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
        analyzer.df, x='avg_salary', nbins=30,
        title='Salary Distribution Across All Jobs',
        labels={'avg_salary': 'Annual Salary ($)', 'count': 'Number of Jobs'},
        color_discrete_sequence=['#1E88E5']
    )
    fig.update_layout(height=450, plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)

def show_advanced_features(analyzer, skill_gap_analyzer, career_mapper):
    """Advanced features including resume parser and API integration"""
    
    st.markdown('<div class="section-title">🚀 Advanced Features</div>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📄 Resume Parser", "🌐 Real-Time Jobs API"])
    
    with tab1:
        show_resume_parser(analyzer)
    
    with tab2:
        show_real_time_jobs(analyzer)

def show_resume_parser(analyzer):
    """Upload and parse resume"""
    st.markdown("""
    <div class="info-box">
        🤖 Upload your resume to automatically extract skills and get personalized career recommendations!
        <br>Supports PDF, DOCX, and TXT files.
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Choose your resume file", type=['pdf', 'docx', 'txt'])
    
    if uploaded_file is not None:
        temp_path = f"temp_{uploaded_file.name}"
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        with st.spinner("Parsing your resume..."):
            parser = ResumeParser()
            parsed_data = parser.parse_resume_file(temp_path)
            
            if 'error' not in parsed_data:
                st.success("✅ Resume parsed successfully!")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### 🎯 Your Skills")
                    skills_html = "".join([f'<span class="skill-badge">{skill}</span>' for skill in parsed_data['skills'][:15]])
                    st.markdown(f'<div style="margin: 10px 0;">{skills_html}</div>', unsafe_allow_html=True)
                    st.markdown(f"**Experience:** {parsed_data['experience_years']} years")
                    st.markdown(f"**Education:** {parsed_data['education']['highest_degree'] or 'Not specified'}")
                
                with col2:
                    st.markdown("#### 📊 Market Readiness")
                    readiness = parsed_data['market_readiness_score']
                    st.progress(readiness['score'] / 100)
                    st.metric("Readiness Score", f"{readiness['score']}/100")
                    st.info(readiness['level'])
                
                st.markdown("---")
                st.markdown("#### 🎯 Find Your Best Match")
                
                target_role = st.selectbox("Select target role:", sorted(analyzer.df['job_title'].unique()))
                
                if target_role:
                    role_data = analyzer.df[analyzer.df['job_title'] == target_role]
                    required_skills_set = set()
                    
                    for skills in role_data['skill_required']:
                        if ',' in str(skills):
                            for s in str(skills).split(','):
                                required_skills_set.add(s.strip().title())
                        else:
                            required_skills_set.add(str(skills).strip().title())
                    
                    required_skills = list(required_skills_set)[:30]
                    
                    match = parser.generate_match_analysis(target_role, required_skills)
                    
                    if 'error' not in match:
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Match Score", f"{match['match_percentage']}%")
                        with col2:
                            st.metric("Matched Skills", len(match['matched_skills']))
                        with col3:
                            st.metric("Skills to Learn", len(match['missing_skills']))
                        
                        if match['matched_skills']:
                            st.markdown("**✅ Skills You Have:**")
                            st.write(", ".join(match['matched_skills'][:10]))
                        
                        if match['missing_skills']:
                            st.markdown("**❌ Skills to Learn (Prioritized):**")
                            for skill in match['missing_skills'][:10]:
                                st.markdown(f"- {skill}")
                        
                        st.markdown("**📚 Recommendations:**")
                        for rec in match['recommendations']:
                            st.markdown(f"- {rec}")
                    else:
                        st.error(f"Match analysis error: {match.get('error', 'Unknown error')}")
            else:
                st.error(f"Error parsing resume: {parsed_data.get('error', 'Unknown error')}")
        
        if os.path.exists(temp_path):
            os.remove(temp_path)

def show_real_time_jobs(analyzer):
    """Display real-time jobs from API"""
    st.markdown("""
    <div class="info-box">
        🌐 Fetch real-time job listings from live APIs. Click the button below to get the latest opportunities!
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🔄 Fetch Latest Jobs", type="primary"):
        with st.spinner("Fetching real-time job data from APIs..."):
            scraper = RealTimeJobScraper()
            jobs_df = scraper.fetch_all_free_jobs(limit_per_source=20)
            
            if not jobs_df.empty:
                st.success(f"✅ Fetched {len(jobs_df)} real-time jobs!")
                st.dataframe(jobs_df[['job_title', 'company', 'location', 'source']])
                
                if st.button("📊 Merge with Existing Dataset"):
                    combined = scraper.merge_with_existing_data(analyzer.df, refresh_data=False)
                    st.info(f"📊 Combined dataset now has {len(combined)} jobs")
                    st.session_state.merged_data = combined
            else:
                st.warning("Could not fetch jobs. Check internet connection.")

if __name__ == "__main__":
    main()