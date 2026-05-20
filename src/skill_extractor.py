"""
Skill Extraction Module
Extracts and analyzes skills from job descriptions
"""

import pandas as pd
import re
from collections import Counter

class SkillExtractor:
    """
    Extracts and analyzes skills from job data
    """
    
    def __init__(self, df):
        """
        Initialize with job data DataFrame
        
        Args:
            df: DataFrame with job postings
        """
        self.df = df
        # Common tech skills dictionary
        self.skills_dict = {
            'Programming': ['Python', 'Java', 'JavaScript', 'C++', 'C#', 'R', 'Go', 'Ruby', 'PHP', 'Swift', 'Kotlin'],
            'Data & Analytics': ['SQL', 'Excel', 'Tableau', 'Power BI', 'Looker', 'SAS', 'SPSS', 'MATLAB'],
            'AI & ML': ['Machine Learning', 'Deep Learning', 'TensorFlow', 'PyTorch', 'Keras', 'Scikit-learn', 'NLP', 'Computer Vision', 'LLM', 'AI'],
            'Cloud & DevOps': ['AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes', 'Jenkins', 'Git', 'CI/CD', 'Terraform'],
            'Databases': ['PostgreSQL', 'MongoDB', 'MySQL', 'Oracle', 'Redis', 'Cassandra', 'Elasticsearch'],
            'Data Engineering': ['Spark', 'Hadoop', 'Airflow', 'Kafka', 'ETL', 'Data Warehousing', 'Big Data'],
            'Soft Skills': ['Communication', 'Leadership', 'Problem Solving', 'Teamwork', 'Project Management', 'Agile']
        }
        
        # Flatten skills list
        self.all_skills = [skill.lower() for category in self.skills_dict.values() for skill in category]
        
    def extract_skills_from_text(self, text):
        """
        Extract skills from text description
        
        Args:
            text (str): Job description text
            
        Returns:
            list: Extracted skills
        """
        if pd.isna(text) or not isinstance(text, str):
            return []
        
        text_lower = text.lower()
        found_skills = []
        
        for skill in self.all_skills:
            if skill in text_lower:
                # Get original case version
                for category in self.skills_dict.values():
                    for orig_skill in category:
                        if orig_skill.lower() == skill:
                            found_skills.append(orig_skill)
                            break
                    else:
                        continue
                    break
        
        return list(set(found_skills))
    
    def get_skill_frequencies(self):
        """
        Calculate skill frequencies across all job postings
        
        Returns:
            DataFrame: Skills with frequency and percentage
        """
        all_skills = []
        
        # Extract skills from skill_required column
        for skills in self.df['skill_required']:
            if pd.notna(skills):
                # Split multiple skills if needed
                if ',' in skills:
                    skill_list = [s.strip() for s in skills.split(',')]
                else:
                    skill_list = [skills]
                all_skills.extend(skill_list)
        
        # Count frequencies
        skill_counts = Counter(all_skills)
        
        # Create DataFrame
        skill_df = pd.DataFrame(skill_counts.items(), columns=['Skill', 'Count'])
        skill_df['Percentage'] = (skill_df['Count'] / len(self.df)) * 100
        skill_df = skill_df.sort_values('Count', ascending=False)
        
        return skill_df
    
    def get_skill_percentages(self, top_n=20):
        """
        Get top skills with percentages
        
        Args:
            top_n (int): Number of top skills to return
            
        Returns:
            DataFrame: Top skills with percentages
        """
        skill_df = self.get_skill_frequencies()
        top_skills = skill_df.head(top_n)
        
        # Add category information
        top_skills['Category'] = top_skills['Skill'].apply(self.get_skill_category)
        
        return top_skills
    
    def get_skill_category(self, skill):
        """
        Get category of a skill
        
        Args:
            skill (str): Skill name
            
        Returns:
            str: Skill category
        """
        for category, skills in self.skills_dict.items():
            if skill in skills:
                return category
        return "Other"
    
    def get_skills_by_role(self, role):
        """
        Get skills required for specific role
        
        Args:
            role (str): Job title
            
        Returns:
            list: Required skills
        """
        role_data = self.df[self.df['job_title'].str.contains(role, case=False, na=False)]
        
        if len(role_data) == 0:
            return []
        
        all_skills = []
        for skills in role_data['skill_required']:
            if pd.notna(skills):
                if ',' in skills:
                    skill_list = [s.strip() for s in skills.split(',')]
                else:
                    skill_list = [skills]
                all_skills.extend(skill_list)
        
        skill_counts = Counter(all_skills)
        return dict(skill_counts.most_common())
    
    def generate_skill_report(self):
        """
        Generate comprehensive skill report
        
        Returns:
            str: Formatted skill report
        """
        skill_df = self.get_skill_percentages(20)
        
        report = "\n" + "="*70 + "\n"
        report += "📊 SKILL MARKET ANALYSIS REPORT\n"
        report += "="*70 + "\n\n"
        
        report += f"Total Jobs Analyzed: {len(self.df)}\n"
        report += f"Unique Skills Found: {len(skill_df)}\n\n"
        
        report += "🏆 TOP 10 SKILLS WITH PERCENTAGES:\n"
        report += "-"*40 + "\n"
        
        for idx, row in skill_df.head(10).iterrows():
            report += f"{idx+1}. {row['Skill']:<20} {row['Count']:>3} jobs ({row['Percentage']:.1f}%)\n"
        
        report += "\n📈 SKILLS BY CATEGORY:\n"
        report += "-"*40 + "\n"
        
        category_stats = skill_df.groupby('Category')['Count'].sum().sort_values(ascending=False)
        for category, count in category_stats.items():
            report += f"• {category}: {count} occurrences\n"
        
        report += "\n💡 KEY INSIGHTS:\n"
        report += "-"*40 + "\n"
        
        top_skill = skill_df.iloc[0]['Skill']
        top_pct = skill_df.iloc[0]['Percentage']
        report += f"• {top_skill} appears in {top_pct:.1f}% of job postings\n"
        
        if 'Python' in skill_df['Skill'].values:
            python_pct = skill_df[skill_df['Skill'] == 'Python']['Percentage'].values[0]
            report += f"• Python appears in {python_pct:.1f}% of jobs\n"
        
        if 'SQL' in skill_df['Skill'].values:
            sql_pct = skill_df[skill_df['Skill'] == 'SQL']['Percentage'].values[0]
            report += f"• SQL appears in {sql_pct:.1f}% of jobs\n"
        
        report += "="*70 + "\n"
        
        return report

# Test the module
if __name__ == "__main__":
    # Load data
    from data_loader import DataLoader
    
    loader = DataLoader()
    df = loader.load_data()
    df_clean = loader.clean_data(df)
    
    # Extract skills
    extractor = SkillExtractor(df_clean)
    
    # Get skill percentages
    print("\n📊 Top Skills with Percentages:")
    print(extractor.get_skill_percentages(10))
    
    # Generate report
    print(extractor.generate_skill_report())