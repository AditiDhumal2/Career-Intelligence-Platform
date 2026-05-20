"""
Module 1: Job Market Analyzer
Purpose: Analyze job market data to find trends, top skills, and salary insights
"""

# Set matplotlib backend to avoid Tcl/Tk error on Windows
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

class JobMarketAnalyzer:
    """
    Analyzes job market data to provide career intelligence
    """
    
    def __init__(self):
        """Initialize the analyzer with processed data"""
        self.project_root = Path(__file__).parent.parent
        self.data_path = self.project_root / 'data' / 'processed' / 'cleaned_job_data.csv'
        self.df = None
        self.load_data()
    
    def load_data(self):
        """Load the cleaned job market data"""
        try:
            self.df = pd.read_csv(self.data_path)
            print(f"✅ Loaded {len(self.df)} job records")
            return True
        except FileNotFoundError:
            print(f"❌ Data file not found. Please run src/data_loader.py first")
            return False
    
    def get_top_paying_jobs(self, top_n=5):
        """
        Find the highest paying job titles
        
        Args:
            top_n (int): Number of top jobs to return
            
        Returns:
            DataFrame: Top paying jobs with salary info
        """
        # Group by job title and calculate average salary
        top_jobs = self.df.groupby('job_title').agg({
            'avg_salary': 'mean',
            'max_salary': 'max',
            'demand_score': 'mean',
            'job_title': 'count'
        }).rename(columns={'job_title': 'job_count'})
        
        # Sort by average salary descending
        top_jobs = top_jobs.sort_values('avg_salary', ascending=False).head(top_n)
        
        return top_jobs
    
    def get_skills_by_demand(self, top_n=10):
        """
        Identify most in-demand skills
        
        Args:
            top_n (int): Number of top skills to return
            
        Returns:
            DataFrame: Skills ranked by demand
        """
        # Count frequency of each skill
        skill_demand = self.df.groupby('skill_required').agg({
            'demand_score': 'mean',
            'avg_salary': 'mean',
            'skill_required': 'count'
        }).rename(columns={'skill_required': 'occurrences'})
        
        # Sort by demand score
        skill_demand = skill_demand.sort_values('demand_score', ascending=False).head(top_n)
        
        return skill_demand
    
    def get_top_locations(self, top_n=5):
        """
        Find best locations for jobs
        
        Args:
            top_n (int): Number of top locations
            
        Returns:
            DataFrame: Top locations with job counts and average salary
        """
        location_stats = self.df.groupby('location').agg({
            'job_title': 'count',
            'avg_salary': 'mean',
            'demand_score': 'mean'
        }).rename(columns={'job_title': 'job_count'})
        
        return location_stats.sort_values('job_count', ascending=False).head(top_n)
    
    def get_skills_by_location(self, location):
        """
        Get top skills for a specific location
        
        Args:
            location (str): City name (e.g., 'New York')
            
        Returns:
            DataFrame: Top skills in that location
        """
        location_df = self.df[self.df['location'] == location]
        
        if len(location_df) == 0:
            print(f"No data found for {location}")
            return None
        
        skills = location_df.groupby('skill_required').agg({
            'demand_score': 'mean',
            'avg_salary': 'mean'
        }).sort_values('demand_score', ascending=False)
        
        return skills.head(10)
    
    def calculate_skill_score(self, skill_name):
        """
        Calculate a comprehensive score for a skill
        
        Score factors:
        - Demand score (40%)
        - Average salary (30%)
        - Number of job postings (20%)
        - Industry spread (10%)
        
        Args:
            skill_name (str): Name of the skill to analyze
            
        Returns:
            dict: Comprehensive skill score and insights
        """
        # Filter data for this skill
        skill_data = self.df[self.df['skill_required'] == skill_name]
        
        if len(skill_data) == 0:
            return {'error': f'Skill "{skill_name}" not found'}
        
        # Calculate metrics
        avg_demand = skill_data['demand_score'].mean()
        avg_salary = skill_data['avg_salary'].mean()
        job_count = len(skill_data)
        unique_industries = skill_data['industry'].nunique()
        
        # Calculate weighted score (0-100)
        demand_weight = 0.4
        salary_weight = 0.3
        count_weight = 0.2
        industry_weight = 0.1
        
        # Normalize salary (assuming range 60k-180k from our data)
        salary_normalized = (avg_salary - 60000) / (180000 - 60000) * 100
        
        # Normalize job count (assuming max 5 jobs per skill in our sample)
        count_normalized = min(job_count / 5 * 100, 100)
        
        # Normalize industry spread (assuming max 5 industries)
        industry_normalized = min(unique_industries / 5 * 100, 100)
        
        total_score = (
            avg_demand * demand_weight +
            salary_normalized * salary_weight +
            count_normalized * count_weight +
            industry_normalized * industry_weight
        )
        
        return {
            'skill': skill_name,
            'score': round(total_score, 2),
            'demand_score': round(avg_demand, 2),
            'avg_salary': round(avg_salary, 2),
            'job_postings': job_count,
            'industries': unique_industries,
            'recommendation': self._get_recommendation(total_score)
        }
    
    def _get_recommendation(self, score):
        """Generate recommendation based on score"""
        if score >= 80:
            return "🚀 High priority - Learn this skill immediately!"
        elif score >= 60:
            return "📈 Good investment - Strongly recommended"
        elif score >= 40:
            return "⚠️ Moderate priority - Consider learning"
        else:
            return "📊 Low priority - Focus on other skills first"
    
    def generate_career_recommendation(self, user_interest=None):
        """
        Generate personalized career recommendations
        
        Args:
            user_interest (str): Optional skill or job title interest
            
        Returns:
            dict: Career recommendations
        """
        recommendations = {
            'top_skills': self.get_skills_by_demand(5),
            'top_jobs': self.get_top_paying_jobs(5),
            'top_locations': self.get_top_locations(3),
            'skills_to_learn': []
        }
        
        # If user has interest, provide specific advice
        if user_interest:
            skill_score = self.calculate_skill_score(user_interest)
            if 'error' not in skill_score:
                recommendations['user_interest_analysis'] = skill_score
        
        return recommendations
    
    def create_salary_visualization(self):
        """
        Create a bar chart of average salary by job title
        """
        plt.figure(figsize=(12, 6))
        
        salary_by_job = self.df.groupby('job_title')['avg_salary'].mean().sort_values()
        
        bars = plt.barh(range(len(salary_by_job)), salary_by_job.values, color='skyblue')
        plt.yticks(range(len(salary_by_job)), salary_by_job.index)
        plt.xlabel('Average Salary ($)')
        plt.title('Average Salary by Job Title', fontsize=14, fontweight='bold')
        plt.grid(axis='x', alpha=0.3)
        
        # Add value labels on bars
        for i, bar in enumerate(bars):
            width = bar.get_width()
            plt.text(width + 1000, bar.get_y() + bar.get_height()/2, 
                    f'${width:,.0f}', ha='left', va='center', fontsize=9)
        
        plt.tight_layout()
        plt.savefig('salary_by_job.png', dpi=100, bbox_inches='tight')
        # plt.show()  # Disabled to avoid Tcl/Tk error on Windows
        print("✅ Salary visualization saved as 'salary_by_job.png'")
    
    def create_skill_demand_chart(self):
        """
        Create a horizontal bar chart of top skills by demand
        """
        plt.figure(figsize=(12, 6))
        
        top_skills = self.get_skills_by_demand(10)
        
        bars = plt.barh(range(len(top_skills)), top_skills['demand_score'], 
                        color='coral')
        plt.yticks(range(len(top_skills)), top_skills.index)
        plt.xlabel('Demand Score (0-100)')
        plt.title('Most In-Demand Skills', fontsize=14, fontweight='bold')
        plt.grid(axis='x', alpha=0.3)
        
        # Add value labels
        for i, bar in enumerate(bars):
            width = bar.get_width()
            plt.text(width + 1, bar.get_y() + bar.get_height()/2, 
                    f'{width:.0f}', ha='left', va='center', fontsize=9)
        
        plt.tight_layout()
        plt.savefig('skill_demand.png', dpi=100, bbox_inches='tight')
        # plt.show()  # Disabled to avoid Tcl/Tk error on Windows
        print("✅ Skill demand chart saved as 'skill_demand.png'")
    
    def generate_report(self):
        """
        Generate a complete market analysis report
        """
        print("\n" + "="*70)
        print("CAREER INTELLIGENCE REPORT")
        print("="*70)
        
        # Top Paying Jobs
        print("\n📊 TOP PAYING JOBS:")
        print("-"*40)
        top_jobs = self.get_top_paying_jobs()
        for job, row in top_jobs.iterrows():
            print(f"   {job}: ${row['avg_salary']:,.0f} (Demand: {row['demand_score']:.0f}/100)")
        
        # Top Skills
        print("\n🎯 MOST IN-DEMAND SKILLS:")
        print("-"*40)
        top_skills = self.get_skills_by_demand()
        for skill, row in top_skills.iterrows():
            print(f"   {skill}: Demand {row['demand_score']:.0f}/100 | ${row['avg_salary']:,.0f}")
        
        # Top Locations
        print("\n📍 BEST LOCATIONS FOR JOBS:")
        print("-"*40)
        top_locations = self.get_top_locations()
        for loc, row in top_locations.iterrows():
            print(f"   {loc}: {row['job_count']:.0f} jobs | ${row['avg_salary']:,.0f}")
        
        # Skill Analysis
        print("\n💡 SKILL INVESTMENT ANALYSIS (Sample):")
        print("-"*40)
        sample_skills = ['Python', 'SQL', 'Machine Learning']
        for skill in sample_skills:
            if skill in self.df['skill_required'].values:
                analysis = self.calculate_skill_score(skill)
                print(f"\n   {skill}: Score {analysis['score']}/100")
                print(f"   → {analysis['recommendation']}")
        
        print("\n" + "="*70)
        print("📈 ACTIONABLE INSIGHTS:")
        print("="*70)
        print("1. Focus on high-demand skills like Python and SQL")
        print("2. Consider relocating to tech hubs (NY, SF, Chicago)")
        print("3. Data Science and ML roles offer highest salaries")
        print("4. Build projects demonstrating these skills")
        print("="*70)


# Test the module
if __name__ == "__main__":
    print("🔍 TESTING JOB MARKET ANALYZER")
    print("="*70)
    
    # Create analyzer instance
    analyzer = JobMarketAnalyzer()
    
    if analyzer.df is not None:
        # Test individual functions
        print("\n📊 Testing get_top_paying_jobs():")
        print(analyzer.get_top_paying_jobs())
        
        print("\n🎯 Testing get_skills_by_demand():")
        print(analyzer.get_skills_by_demand())
        
        print("\n📍 Testing get_top_locations():")
        print(analyzer.get_top_locations())
        
        print("\n💡 Testing skill score for Python:")
        python_score = analyzer.calculate_skill_score('Python')
        for key, value in python_score.items():
            print(f"   {key}: {value}")
        
        # Generate full report
        analyzer.generate_report()
        
        # Create visualizations (saves files without displaying)
        analyzer.create_salary_visualization()
        analyzer.create_skill_demand_chart()
        
        print("\n✅ All tests completed successfully!")
        print("\n📁 Check your project folder for these files:")
        print("   - salary_by_job.png")
        print("   - skill_demand.png")