"""
Career Intelligence Platform - Complete Dashboard
RAG temporarily disabled for deployment compatibility
All other features: Market Intelligence, Skill Gap Analyzer, Career Path Mapper, 
Analytics Hub, AI Advisor, NLP Query, Resume Critic, Interview Prep, Market Trends
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
# LLM/AI IMPORTS - RAG DISABLED FOR DEPLOYMENT
# ============================================

# RAG is disabled for now due to ChromaDB compatibility issues
RAG_AVAILABLE = False

# Create dummy RAGRetriever class for when RAG is disabled
class DummyRAGRetriever:
    def __init__(self, *args, **kwargs):
        pass
    def search(self, *args, **kwargs):
        return []
    def get_job_recommendations(self, *args, **kwargs):
        return []

# Use dummy class if RAG is not available
RAGRetriever = DummyRAGRetriever

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
# SIMPLE CLEAN CSS
# ============================================
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        text-align: center;
        color: #1E88E5;
        font-weight: 700;
        margin-bottom: 0.3rem;
    }
    .sub-header {
        font-size: 0.95rem;
        text-align: center;
        color: #666;
        margin-bottom: 1.5rem;
    }
    .section-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #1E88E5;
        border-left: 4px solid #1E88E5;
        padding-left: 1rem;
        margin: 1rem 0;
    }
    .metric-card {
        background: linear-gradient(135deg, #1E88E5, #0D47A1);
        border-radius: 10px;
        padding: 0.8rem;
        text-align: center;
        color: white;
        min-height: 100px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    .metric-card h3 {
        font-size: 0.7rem;
        margin: 0;
        opacity: 0.8;
        color: white;
        font-weight: 400;
        letter-spacing: 0.5px;
    }
    .metric-card h2 {
        font-size: 1.5rem;
        margin: 0.1rem 0;
        color: white;
        font-weight: 700;
    }
    .metric-card p {
        font-size: 0.6rem;
        margin: 0;
        opacity: 0.7;
        color: white;
    }
    .info-box {
        background: #E3F2FD;
        padding: 0.8rem 1rem;
        border-radius: 8px;
        border-left: 4px solid #1E88E5;
        margin: 0.8rem 0;
        color: #1a1a2e;
    }
    .skill-badge {
        display: inline-block;
        background: #1E88E5;
        color: white;
        padding: 3px 12px;
        border-radius: 20px;
        margin: 3px;
        font-size: 12px;
        font-weight: 500;
    }
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #f5f7f9;
    }
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] label {
        color: #1a1a2e !important;
    }
    /* Radio buttons */
    [data-testid="stRadio"] label {
        background: white;
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 8px 14px;
        margin: 3px 0;
        color: #1E88E5;
        font-weight: 500;
        width: 100%;
        cursor: pointer;
    }
    [data-testid="stRadio"] [aria-checked="true"] + div {
        background: #1E88E5;
        color: white;
        border: none;
    }
    [data-testid="stRadio"] [aria-checked="true"] + div p {
        color: white;
    }
    /* Buttons */
    .stButton > button {
        background: #1E88E5;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
    }
    .stButton > button:hover {
        background: #1565C0;
    }
    /* Metrics in sidebar */
    [data-testid="stMetricValue"] {
        color: #1a1a2e !important;
        font-weight: 700 !important;
    }
    [data-testid="stMetricLabel"] {
        color: #666 !important;
    }
    /* Expander */
    .streamlit-expanderHeader {
        color: #1a1a2e !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = "📊 Market Intelligence"

@st.cache_resource
def load_components():
    with st.spinner('🚀 Loading...'):
        analyzer = JobMarketAnalyzer()
        skill_gap_analyzer = SkillGapAnalyzer(analyzer.df)
        career_mapper = CareerPathMapper()
    return analyzer, skill_gap_analyzer, career_mapper

def main():
    # Header
    st.markdown('<div class="main-header">🎯 Career Intelligence Platform</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">AI-Powered Career Guidance | Real-time Market Intelligence</div>', unsafe_allow_html=True)
    
    # Load data
    analyzer, skill_gap_analyzer, career_mapper = load_components()
    
    if analyzer.df is None:
        st.error("❌ Could not load data. Run: python data/generate_large_dataset.py")
        return
    
    # SIDEBAR
    with st.sidebar:
        st.markdown("### 🎯 Career Navigator")
        st.markdown("---")
        
        selected_page = st.radio(
            "Navigation",
            ["📊 Market Intelligence", "💡 Skill Gap Analyzer", "🗺️ Career Path Mapper", "📈 Analytics Hub", "🚀 Advanced AI Features"],
            label_visibility="collapsed",
            index=0
        )
        st.session_state.page = selected_page
        
        st.markdown("---")
        st.markdown("### 📊 Stats")
        st.metric("Jobs", f"{len(analyzer.df):,}")
        st.metric("Skills", f"{analyzer.df['skill_required'].nunique():,}")
        st.metric("Roles", f"{analyzer.df['job_title'].nunique():,}")
        st.metric("Avg Salary", f"${analyzer.df['avg_salary'].mean():,.0f}")
        
        st.markdown("---")
        st.markdown("*Built with ❤️*")
    
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
# MARKET INTELLIGENCE
# ============================================
def show_market_intelligence(analyzer):
    st.markdown('<div class="section-title">📈 Market Intelligence</div>', unsafe_allow_html=True)
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        locations = ['All'] + sorted(analyzer.df['location'].unique().tolist())
        selected_location = st.selectbox("📍 Location", locations)
    with col2:
        if 'industry' in analyzer.df.columns:
            industries = ['All'] + sorted(analyzer.df['industry'].unique().tolist())
            selected_industry = st.selectbox("🏭 Industry", industries)
        else:
            selected_industry = 'All'
    with col3:
        if 'remote_policy' in analyzer.df.columns:
            remote_options = ['All', 'Remote', 'Hybrid', 'On-site']
            selected_remote = st.selectbox("🏠 Remote", remote_options)
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
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 💼 Top Paying Jobs")
        top_jobs = analyzer.get_top_paying_jobs(8)
        
        fig = px.bar(
            top_jobs,
            x='avg_salary',
            y=top_jobs.index,
            orientation='h',
            labels={'avg_salary': 'Salary ($)', 'y': ''},
            color='avg_salary',
            color_continuous_scale='Blues',
            text='avg_salary'
        )
        fig.update_traces(
            texttemplate='${:,.0f}',
            textposition='outside',
            textfont=dict(size=10)
        )
        fig.update_layout(
            height=400,
            showlegend=False,
            margin=dict(l=10, r=80, t=10, b=10),
            xaxis_tickformat='$,.0f',
            yaxis_automargin=True,
            plot_bgcolor='white'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### 🎯 Most In-Demand Skills")
        skill_demand = analyzer.get_skills_by_demand(10)
        
        fig = px.bar(
            skill_demand,
            x='demand_score',
            y=skill_demand.index,
            orientation='h',
            labels={'demand_score': 'Demand Score', 'y': ''},
            color='demand_score',
            color_continuous_scale='Teal',
            text='demand_score'
        )
        fig.update_traces(
            texttemplate='%{text:.0f}',
            textposition='outside',
            textfont=dict(size=10)
        )
        fig.update_layout(
            height=400,
            showlegend=False,
            xaxis=dict(range=[0, 105]),
            margin=dict(l=10, r=50, t=10, b=10),
            yaxis_automargin=True,
            plot_bgcolor='white'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Skill Penetration
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
    skill_df = pd.DataFrame(skill_counts.items(), columns=['Skill', 'Count'])
    skill_df['Percentage'] = (skill_df['Count'] / len(analyzer.df)) * 100
    skill_df = skill_df.sort_values('Percentage', ascending=False).head(15)
    
    fig = px.bar(
        skill_df,
        x='Percentage',
        y='Skill',
        orientation='h',
        labels={'Percentage': '% of Jobs', 'Skill': ''},
        color='Percentage',
        color_continuous_scale='Viridis',
        text='Percentage'
    )
    fig.update_traces(
        texttemplate='%{text:.1f}%',
        textposition='outside',
        textfont=dict(size=10)
    )
    fig.update_layout(
        height=500,
        margin=dict(l=10, r=80, t=10, b=10),
        yaxis_automargin=True,
        plot_bgcolor='white'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Locations
    st.markdown("---")
    st.markdown("#### 🗺️ Top Locations")
    
    loc_stats = analyzer.df.groupby('location').size().reset_index(name='count')
    loc_stats = loc_stats.sort_values('count', ascending=False).head(12)
    
    fig = px.bar(
        loc_stats,
        x='count',
        y='location',
        orientation='h',
        labels={'count': 'Jobs', 'location': ''},
        color='count',
        color_continuous_scale='Reds',
        text='count'
    )
    fig.update_traces(
        texttemplate='%{text:,}',
        textposition='outside',
        textfont=dict(size=10)
    )
    fig.update_layout(
        height=400,
        margin=dict(l=10, r=60, t=10, b=10),
        yaxis_automargin=True,
        plot_bgcolor='white'
    )
    st.plotly_chart(fig, use_container_width=True)

# ============================================
# SKILL GAP ANALYZER
# ============================================
def show_skill_gap_analyzer(analyzer, skill_gap_analyzer):
    st.markdown('<div class="section-title">💡 Skill Gap Analyzer</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
        🤖 Enter your skills and target role to get personalized learning recommendations.
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 👤 Your Skills")
        skills_input = st.text_area(
            "",
            placeholder="Python, SQL, Excel, Machine Learning",
            height=80,
            label_visibility="collapsed"
        )
        user_skills = [s.strip().title() for s in skills_input.split(',')] if skills_input else []
        
        if user_skills:
            skills_html = "".join([f'<span class="skill-badge">{s}</span>' for s in user_skills])
            st.markdown(f'<div style="margin: 10px 0;">{skills_html}</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### 🎯 Target Role")
        all_roles = sorted(analyzer.df['job_title'].unique())
        target_role = st.selectbox("Select your dream job", all_roles)
    
    if user_skills and target_role:
        st.markdown("---")
        
        with st.spinner('🔍 Analyzing...'):
            results = skill_gap_analyzer.analyze_gap(user_skills, target_role)
            
            if 'error' not in results:
                st.progress(results['match_percentage'] / 100, text=f"Match: {results['match_percentage']}%")
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("✅ Matched", len(results['matched_skills']))
                with col2:
                    st.metric("❌ Missing", len(results['missing_skills']))
                with col3:
                    st.metric("📋 Required", results['required_skills_count'])
                with col4:
                    st.metric("📊 Score", f"{results['match_percentage']}%")
                
                col1, col2 = st.columns(2)
                with col1:
                    if results['matched_skills']:
                        st.markdown("#### ✅ Skills You Have")
                        for skill in results['matched_skills'][:10]:
                            st.success(f"✓ {skill}")
                with col2:
                    if results['missing_skills']:
                        st.markdown("#### 🎯 Skills to Learn")
                        for i, skill_info in enumerate(results['learning_path'][:6], 1):
                            st.markdown(f"**{i}. {skill_info['priority_icon']} {skill_info['skill']}**")
                            st.caption(f"{skill_info['priority']} | {skill_info['estimated_time']}")
                
                st.info(results['status']['message'])

# ============================================
# CAREER PATH MAPPER
# ============================================
def show_career_path_mapper(career_mapper):
    st.markdown('<div class="section-title">🗺️ Career Path Mapper</div>', unsafe_allow_html=True)
    
    all_roles = career_mapper.get_all_available_roles()
    
    if not all_roles:
        st.error("No career paths available.")
        return
    
    col1, col2 = st.columns(2)
    with col1:
        current_role = st.selectbox("📍 Current Position", all_roles, index=0)
    with col2:
        target_role = st.selectbox("🎯 Dream Position", all_roles, index=min(3, len(all_roles)-1))
    
    if st.button("🚀 Generate Career Path", use_container_width=True):
        with st.spinner('🗺️ Mapping...'):
            path_data = career_mapper.get_career_path(current_role, target_role)
            
            if 'error' not in path_data:
                st.markdown("---")
                st.markdown("### 📍 Your Career Roadmap")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Steps", path_data['total_steps'])
                with col2:
                    st.metric("Time", path_data['estimated_time'])
                with col3:
                    st.metric("Track", path_data['track'])
                
                st.markdown("---")
                
                for i, step in enumerate(path_data['path'], 1):
                    with st.container():
                        st.markdown(f"**Step {i}: {step['role']}**")
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.markdown(f"💰 {step['salary']}")
                        with col2:
                            st.markdown(f"⏰ {step['experience']} years")
                        with col3:
                            st.markdown(f"📋 {', '.join(step['required_skills'][:3])}")
                        if i < len(path_data['path']):
                            st.markdown("↓")
                            st.markdown("---")

# ============================================
# ANALYTICS HUB
# ============================================
def show_analytics_hub(analyzer):
    st.markdown('<div class="section-title">📊 Analytics Hub</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 💡 Market Insights")
        top_skill = analyzer.get_skills_by_demand(1).index[0]
        top_role = analyzer.get_top_paying_jobs(1).index[0]
        top_loc = analyzer.get_top_locations(1).index[0]
        
        st.info(f"🎯 **{top_skill}** is the most in-demand skill")
        st.info(f"💰 **{top_role}** offers highest salary")
        st.info(f"📍 **{top_loc}** has most jobs")
    
    with col2:
        st.markdown("#### 🚀 Quick Actions")
        st.markdown("""
        - 📝 Update resume with in-demand skills
        - 🎓 Take courses for missing skills
        - 🌍 Target high-opportunity locations
        - 🤝 Network with professionals
        """)
    
    st.markdown("---")
    st.markdown("#### 📈 Salary Distribution")
    
    fig = px.histogram(
        analyzer.df,
        x='avg_salary',
        nbins=30,
        labels={'avg_salary': 'Salary ($)', 'count': 'Jobs'},
        color_discrete_sequence=['#1E88E5']
    )
    fig.update_layout(height=400, plot_bgcolor='white')
    st.plotly_chart(fig, use_container_width=True)

# ============================================
# ADVANCED AI FEATURES - RAG DISABLED
# ============================================
def show_advanced_ai_features(analyzer, skill_gap_analyzer, career_mapper):
    """Show all AI-powered features - RAG temporarily disabled"""
    
    st.markdown('<div class="section-title">🚀 Advanced AI Features</div>', unsafe_allow_html=True)
    
    # Only include available tabs (RAG is disabled)
    tabs = ["💬 AI Advisor"]
    
    if RESUME_CRITIC_AVAILABLE:
        tabs.append("📄 Resume Critic")
    if INTERVIEW_PREP_AVAILABLE:
        tabs.append("🎤 Interview Prep")
    if MARKET_TRENDS_AVAILABLE:
        tabs.append("📈 Market Trends")
    if NLP_QUERY_AVAILABLE:
        tabs.append("🔍 NLP Query")
    # RAG is disabled - don't add it
    
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
    
    # RAG tab is removed - no need to handle

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
    
    if st.button("Get AI Advice", type="primary", use_container_width=True):
        with st.spinner("🤔 AI is thinking..."):
            advisor = LLMCareerAdvisor()
            
            if custom_question:
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
    st.markdown("#### 📄 Resume Critic")
    
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
    
    if st.button("Generate Interview Plan", type="primary", use_container_width=True):
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
    
    if st.button("Fetch Trends", type="primary", use_container_width=True):
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
    
    if query and st.button("Ask", type="primary", use_container_width=True):
        with st.spinner("Processing your question..."):
            processor = NLPQueryProcessor(analyzer.df)
            response = processor.process_query(query)
            st.markdown(response.get('response', 'No response'))

if __name__ == "__main__":
    main()