"""
Skill Gap Analyzer Module
Compares user skills with job requirements and provides learning recommendations
Prioritizes skills based on job role requirements and market demand
UPDATED: Uses actual demand scores from dataset
"""

import pandas as pd
import numpy as np
from pathlib import Path
from collections import Counter
import re

class SkillGapAnalyzer:
    """
    Analyzes skill gaps between user and job requirements
    """
    
    def __init__(self, df):
        """
        Initialize with job data
        
        Args:
            df: DataFrame with job postings
        """
        self.df = df
        # First calculate market demand USING ACTUAL DATASET SCORES
        self.skill_market_demand = self._calculate_market_demand()
        # Then build role skills database (which uses market demand)
        self.role_skills = self._build_role_skills_database()
        
        # Define critical skills for each role type
        self.critical_skills_map = {
            'Data Scientist': ['Python', 'Machine Learning', 'Statistics', 'Sql', 'Deep Learning', 
                              'Tensorflow', 'Pytorch', 'R', 'Data Visualization', 'Scikit-Learn',
                              'NLP', 'LLM', 'Computer Vision'],
            'Data Analyst': ['Sql', 'Excel', 'Python', 'Tableau', 'Statistics', 'Power Bi', 
                            'Data Visualization', 'Communication', 'Problem Solving'],
            'Data Engineer': ['Python', 'Sql', 'Spark', 'Aws', 'Docker', 'Kubernetes', 'Airflow',
                            'Cloud Computing', 'Etl', 'Data Warehousing', 'Scala'],
            'ML Engineer': ['Python', 'Machine Learning', 'Tensorflow', 'Pytorch', 'Docker', 
                          'Kubernetes', 'Aws', 'Git', 'Ci/Cd', 'Scikit-Learn', 'Deep Learning'],
            'Business Analyst': ['Excel', 'Sql', 'Tableau', 'Power Bi', 'Communication', 
                                'Problem Solving', 'Requirements Analysis', 'Data Visualization'],
            'Analytics Manager': ['Leadership', 'Project Management', 'Sql', 'Tableau', 
                                 'Communication', 'Strategy', 'People Management', 'Data Strategy'],
            'Data Architect': ['Sql', 'Data Modeling', 'Aws', 'Azure', 'Data Warehousing', 
                              'Etl', 'Database Design', 'Python', 'Cloud Architecture'],
            'AI Research Scientist': ['Python', 'Machine Learning', 'Deep Learning', 'Tensorflow',
                                     'Pytorch', 'Research', 'Mathematics', 'Statistics', 'NLP', 'LLM'],
        }
        
    def _build_role_skills_database(self):
        """
        Build database of required skills for each role with frequency analysis
        
        Returns:
            dict: Role -> {skills: {skill: frequency}, total_postings: int}
        """
        role_skills = {}
        
        print("📊 Building role skills database...")
        
        for role in self.df['job_title'].unique():
            role_data = self.df[self.df['job_title'] == role]
            skills = []
            
            for skill_text in role_data['skill_required']:
                if pd.notna(skill_text):
                    if ',' in str(skill_text):
                        skills.extend([s.strip().title() for s in skill_text.split(',')])
                    else:
                        skills.append(str(skill_text).strip().title())
            
            # Count skill frequency for this role
            skill_counts = Counter(skills)
            
            # Calculate percentage for each skill
            total_postings = len(role_data)
            skill_percentages = {}
            
            for skill, count in skill_counts.items():
                # Get market demand from dataset (UPDATED: uses actual scores)
                market_demand = self._get_skill_market_demand(skill)
                
                skill_percentages[skill] = {
                    'count': count,
                    'percentage': (count / total_postings) * 100,
                    'demand_score': market_demand  # This now uses actual dataset scores
                }
            
            role_skills[role] = {
                'skills': skill_percentages,
                'total_postings': total_postings,
                'all_skills': list(skill_counts.keys())
            }
        
        print(f"   ✅ Built database for {len(role_skills)} roles")
        return role_skills
    
    def _calculate_market_demand(self):
        """
        Calculate market demand score for each skill USING ACTUAL DATASET DEMAND SCORES
        
        Returns:
            dict: Skill -> market demand score
        """
        market_demand = {}
        
        # Get all unique skills
        all_skills = []
        for skill_text in self.df['skill_required']:
            if pd.notna(skill_text):
                if ',' in str(skill_text):
                    all_skills.extend([s.strip().title() for s in skill_text.split(',')])
                else:
                    all_skills.append(str(skill_text).strip().title())
        
        skill_counts = Counter(all_skills)
        total_jobs = len(self.df)
        
        print("📊 Calculating market demand scores from dataset...")
        
        for skill, count in skill_counts.items():
            # Get ALL job postings containing this skill
            try:
                skill_data = self.df[self.df['skill_required'].str.contains(
                    re.escape(skill), case=False, na=False, regex=False
                )]
            except re.error:
                skill_data = self.df[self.df['skill_required'].str.contains(
                    skill, case=False, na=False, regex=False
                )]
            
            if len(skill_data) > 0:
                # Use ACTUAL demand_score from dataset (UPDATED: now uses your updated scores)
                actual_demand_scores = skill_data['demand_score'].tolist()
                avg_demand_score = np.mean(actual_demand_scores)
                
                # Get average salary for context
                avg_salary = skill_data['avg_salary'].mean() if len(skill_data) > 0 else 80000
                salary_normalized = min((avg_salary - 60000) / (180000 - 60000) * 100, 100)
                
                # Frequency percentage
                frequency_pct = (count / total_jobs) * 100
                
                # Final market score (weighted)
                # 50% - Actual demand score from dataset
                # 30% - Frequency in job postings
                # 20% - Salary premium
                market_score = (avg_demand_score * 0.5) + (frequency_pct * 0.3) + (salary_normalized * 0.2)
                
                market_demand[skill] = {
                    'frequency': count,
                    'frequency_percentage': round(frequency_pct, 1),
                    'demand_score': round(avg_demand_score, 1),
                    'avg_salary': round(avg_salary, 0),
                    'market_score': round(market_score, 1)
                }
            else:
                market_demand[skill] = {
                    'frequency': count,
                    'frequency_percentage': round((count / total_jobs) * 100, 1),
                    'demand_score': 75.0,  # Default
                    'avg_salary': 85000,
                    'market_score': 75.0
                }
        
        print(f"   ✅ Calculated demand for {len(market_demand)} unique skills")
        
        # Print top skills by demand for verification
        top_skills = sorted(market_demand.items(), key=lambda x: x[1]['demand_score'], reverse=True)[:10]
        print(f"\n   📊 Top 10 Skills by Market Demand (from dataset):")
        for skill, data in top_skills:
            print(f"      {skill}: {data['demand_score']:.1f}/100 ({data['frequency']} occurrences)")
        
        return market_demand
    
    def _get_skill_market_demand(self, skill):
        """
        Get market demand score for a specific skill from the dataset
        
        Args:
            skill (str): Skill name
            
        Returns:
            float: Demand score (0-100) from actual data
        """
        if not hasattr(self, 'skill_market_demand'):
            return 75.0
        
        # Direct match
        if skill in self.skill_market_demand:
            return self.skill_market_demand[skill]['demand_score']
        
        # Case-insensitive match
        for existing_skill in self.skill_market_demand.keys():
            if skill.lower() == existing_skill.lower():
                return self.skill_market_demand[existing_skill]['demand_score']
        
        # Partial match
        for existing_skill in self.skill_market_demand.keys():
            try:
                if skill.lower() in existing_skill.lower() or existing_skill.lower() in skill.lower():
                    return self.skill_market_demand[existing_skill]['demand_score']
            except:
                continue
        
        # Default if not found
        return 75.0
    
    def analyze_gap(self, user_skills, target_role):
        """
        Analyze skill gap between user skills and target role requirements
        
        Args:
            user_skills (list): List of user's current skills
            target_role (str): Target job role
            
        Returns:
            dict: Gap analysis results with prioritized learning path
        """
        # Clean user skills
        user_skills = [skill.strip().title() for skill in user_skills]
        
        # Get required skills for target role
        if target_role not in self.role_skills:
            # Try fuzzy matching
            matching_roles = self._find_matching_roles(target_role)
            if matching_roles:
                target_role = matching_roles[0]
            else:
                available_roles = list(self.role_skills.keys())[:10]
                return {'error': f"Role '{target_role}' not found. Available roles: {available_roles}"}
        
        role_data = self.role_skills[target_role]
        required_skills_info = role_data['skills']
        required_skills_set = set(required_skills_info.keys())
        user_skills_set = set(user_skills)
        
        # Get critical skills for this role
        critical_for_role = self.critical_skills_map.get(target_role, [])
        critical_for_role = [c.lower() for c in critical_for_role]
        
        # Calculate gaps with priority scores
        matched_skills = []
        missing_skills = []
        
        # Find matched skills
        for skill in user_skills_set:
            match_found = False
            for req_skill in required_skills_set:
                if skill.lower() == req_skill.lower():
                    matched_skills.append({
                        'skill': req_skill,
                        'frequency': required_skills_info[req_skill]['count'],
                        'percentage': required_skills_info[req_skill]['percentage'],
                        'demand_score': required_skills_info[req_skill]['demand_score']
                    })
                    match_found = True
                    break
            if not match_found and skill in required_skills_set:
                matched_skills.append({
                    'skill': skill,
                    'frequency': required_skills_info[skill]['count'],
                    'percentage': required_skills_info[skill]['percentage'],
                    'demand_score': required_skills_info[skill]['demand_score']
                })
        
        # Find missing skills with priority calculation
        for skill in required_skills_set:
            if skill.lower() not in [s.lower() for s in user_skills_set]:
                # Get skill details
                role_frequency = required_skills_info[skill]['count']
                role_percentage = required_skills_info[skill]['percentage']
                
                # UPDATED: Use actual market demand from dataset
                market_demand = self._get_skill_market_demand(skill)
                
                # Check if skill is critical for this role
                is_critical = 1 if skill.lower() in critical_for_role else 0
                
                # Calculate priority score (UPDATED with better weighting)
                # 40% - Role frequency (how often it appears in this role)
                # 35% - Market demand (from dataset)
                # 25% - Critical skill boost
                priority_score = (
                    (role_percentage * 0.4) + 
                    (market_demand * 0.35) + 
                    (45 if is_critical else 0)
                )
                
                # Additional boost for high-demand skills
                if market_demand >= 90:
                    priority_score += 10
                elif market_demand >= 85:
                    priority_score += 5
                
                missing_skills.append({
                    'skill': skill,
                    'frequency_in_role': role_frequency,
                    'percentage_in_role': round(role_percentage, 2),
                    'market_demand_score': round(market_demand, 1),
                    'priority_score': round(min(priority_score, 100), 1),
                    'is_critical': is_critical,
                    'priority_level': self._get_priority_level(priority_score, is_critical, market_demand)
                })
        
        # Sort missing skills by priority score (highest first)
        missing_skills_sorted = sorted(missing_skills, key=lambda x: x['priority_score'], reverse=True)
        
        # Calculate match percentage
        if len(required_skills_set) > 0:
            match_percentage = (len(matched_skills) / len(required_skills_set)) * 100
        else:
            match_percentage = 0
        
        # Generate learning path
        learning_path = self._generate_learning_path(missing_skills_sorted, target_role)
        
        return {
            'target_role': target_role,
            'required_skills': list(required_skills_set),
            'required_skills_count': len(required_skills_set),
            'user_skills': user_skills,
            'matched_skills': [m['skill'] for m in matched_skills],
            'matched_skills_details': matched_skills,
            'missing_skills': [m['skill'] for m in missing_skills_sorted],
            'missing_skills_details': missing_skills_sorted,
            'match_percentage': round(match_percentage, 1),
            'learning_path': learning_path,
            'status': self._get_status(match_percentage),
            'role_summary': {
                'total_postings': role_data['total_postings'],
                'unique_skills': len(required_skills_set)
            }
        }
    
    def _get_priority_level(self, score, is_critical=False, market_demand=75):
        """
        Get priority level based on score and market demand
        
        Args:
            score (float): Priority score
            is_critical (bool): Whether skill is critical for the role
            market_demand (float): Market demand score
            
        Returns:
            dict: Priority level information
        """
        # Override if critical
        if is_critical:
            return {'level': 'CRITICAL', 'icon': '🔴', 'color': '#D32F2F', 'order': 0}
        
        if score >= 75 or market_demand >= 90:
            return {'level': 'High', 'icon': '🟠', 'color': '#FB8C00', 'order': 1}
        elif score >= 55 or market_demand >= 80:
            return {'level': 'Medium', 'icon': '🟡', 'color': '#FDD835', 'order': 2}
        elif score >= 35:
            return {'level': 'Low', 'icon': '🟢', 'color': '#43A047', 'order': 3}
        else:
            return {'level': 'Optional', 'icon': '⚪', 'color': '#9E9E9E', 'order': 4}
    
    def _find_matching_roles(self, search_term):
        """
        Find roles that match search term
        
        Args:
            search_term (str): Role to search for
            
        Returns:
            list: Matching role names
        """
        search_lower = search_term.lower()
        matches = [role for role in self.role_skills.keys() 
                  if search_lower in role.lower()]
        return matches
    
    def _generate_learning_path(self, missing_skills, target_role):
        """
        Generate prioritized learning path with estimated timelines
        
        Args:
            missing_skills (list): Missing skills with details
            target_role (str): Target role
            
        Returns:
            list: Prioritized learning path
        """
        if not missing_skills:
            return []
        
        learning_path = []
        
        for skill_info in missing_skills:
            skill = skill_info['skill']
            priority = skill_info['priority_level']
            market_demand = skill_info['market_demand_score']
            
            # Estimate learning time based on skill complexity and market demand
            learning_time = self._estimate_learning_time(skill, market_demand)
            
            # Get learning resources
            resources = self._get_learning_resources(skill)
            
            learning_path.append({
                'skill': skill,
                'priority': priority['level'],
                'priority_icon': priority['icon'],
                'priority_color': priority['color'],
                'priority_score': skill_info['priority_score'],
                'estimated_time': learning_time,
                'market_demand': skill_info['market_demand_score'],
                'frequency_in_role': skill_info['percentage_in_role'],
                'resources': resources[:3],
                'order': priority['order']
            })
        
        # Sort by priority order
        return sorted(learning_path, key=lambda x: x['order'])
    
    def _estimate_learning_time(self, skill, market_demand):
        """
        Estimate learning time for a skill
        
        Args:
            skill (str): Skill name
            market_demand (float): Market demand score
            
        Returns:
            str: Estimated learning time
        """
        skill_lower = skill.lower()
        
        # High demand complex skills take longer
        if market_demand >= 90:
            if any(adv in skill_lower for adv in ['machine learning', 'deep learning', 'tensorflow', 'pytorch', 'kubernetes', 'aws']):
                return "8-12 weeks"
            return "6-8 weeks"
        elif market_demand >= 80:
            return "4-6 weeks"
        else:
            return "2-4 weeks"
    
    def _get_learning_resources(self, skill):
        """
        Get learning resources for a skill
        
        Args:
            skill (str): Skill name
            
        Returns:
            list: Recommended learning resources
        """
        resources_db = {
            'Python': [
                '🐍 Google IT Automation with Python (Coursera)',
                '🐍 Python for Everybody (freeCodeCamp)',
                '🐍 100 Days of Code (Udemy)'
            ],
            'SQL': [
                '📊 SQL for Data Science (Coursera)',
                '📊 SQL Tutorial (W3Schools)',
                '📊 Practice SQL on LeetCode'
            ],
            'Machine Learning': [
                '🤖 Andrew Ng ML Course (Coursera)',
                '🤖 Fast.ai Practical Deep Learning',
                '🤖 Kaggle Learn ML'
            ],
            'Deep Learning': [
                '🧠 Deep Learning Specialization (Coursera)',
                '🧠 Fast.ai Deep Learning',
                '🧠 PyTorch Tutorials'
            ],
            'Tensorflow': [
                '⚡ TensorFlow Developer Certificate (Coursera)',
                '⚡ TensorFlow Official Tutorials',
                '⚡ Zero to Mastery TensorFlow'
            ],
            'Pytorch': [
                '🔥 PyTorch for Deep Learning (freeCodeCamp)',
                '🔥 Learn PyTorch (Official)',
                '🔥 Deep Learning with PyTorch (Udemy)'
            ],
            'Statistics': [
                '📐 Statistics with R/Python (Coursera)',
                '📐 Khan Academy Statistics',
                '📐 Practical Statistics for Data Scientists'
            ],
            'Excel': [
                '📑 Excel Skills for Business (Coursera)',
                '📑 Excel Is Fun (YouTube)',
                '📑 Advanced Excel Formulas'
            ],
            'Tableau': [
                '📈 Tableau Training on Official Site',
                '📈 Data Visualization with Tableau (Coursera)',
                '📈 Tableau Public Practice'
            ],
            'Power Bi': [
                '📊 Power BI Data Analyst Certification (Microsoft)',
                '📊 Power BI Tutorial (LinkedIn Learning)',
                '📊 Power BI Desktop Practice'
            ],
            'AWS': [
                '☁️ AWS Cloud Practitioner (AWS Training)',
                '☁️ Solutions Architect Course (Udemy)',
                '☁️ AWS Free Tier Hands-on'
            ],
            'Docker': [
                '🐳 Docker Mastery (Udemy)',
                '🐳 Docker Curriculum (Official)',
                '🐳 Docker Hands-on Labs'
            ],
            'Kubernetes': [
                '⎈ Kubernetes Course (KodeKloud)',
                '⎈ Certified Kubernetes Administrator',
                '⎈ Kubernetes Workshop'
            ],
            'Spark': [
                '⚡ Apache Spark with Python (Databricks)',
                '⚡ Spark Programming (Udemy)',
                '⚡ PySpark Tutorials'
            ],
            'Git': [
                '📦 Git & GitHub Crash Course',
                '📦 Pro Git Book (Free)',
                '📦 Git Branching Practice'
            ],
            'NLP': [
                '💬 Natural Language Processing (Coursera)',
                '💬 Hugging Face NLP Course',
                '💬 spaCy Tutorials'
            ],
            'Scikit-Learn': [
                '📚 Scikit-learn Documentation',
                '📚 Machine Learning with Scikit-learn (DataCamp)',
                '📚 Hands-on ML with Scikit-learn'
            ],
            'Communication': [
                '💬 Effective Communication (Coursera)',
                '💬 Toastmasters International',
                '💬 Business Communication Skills'
            ],
            'Leadership': [
                '👥 Leadership Principles (Harvard Online)',
                '👥 Leading People and Teams (Coursera)',
                '👥 Crucial Conversations'
            ]
        }
        
        # Try exact match (case insensitive)
        for key, resources in resources_db.items():
            if skill.lower() == key.lower():
                return resources
        
        # Try partial match
        for key, resources in resources_db.items():
            if skill.lower() in key.lower() or key.lower() in skill.lower():
                return resources
        
        # Default resources
        return [
            '📚 Coursera / Udemy courses',
            '📚 YouTube tutorials',
            '📚 Official documentation',
            '📚 Practice projects'
        ]
    
    def _get_status(self, match_percentage):
        """
        Get status based on match percentage
        
        Args:
            match_percentage (float): Match percentage
            
        Returns:
            dict: Status information
        """
        if match_percentage >= 80:
            return {
                'level': 'Excellent',
                'message': "🎉 You're well qualified! Start applying now!",
                'icon': '🎉',
                'action': 'Apply confidently',
                'color': '#43A047'
            }
        elif match_percentage >= 60:
            return {
                'level': 'Good',
                'message': "📈 Good match! Learn missing skills to become top candidate.",
                'icon': '📈',
                'action': 'Upskill 4-6 weeks',
                'color': '#FB8C00'
            }
        elif match_percentage >= 40:
            return {
                'level': 'Moderate',
                'message': "⚠️ You meet some requirements. Focus on priority skills.",
                'icon': '⚠️',
                'action': 'Upskill 8-12 weeks',
                'color': '#FDD835'
            }
        else:
            return {
                'level': 'Significant Gap',
                'message': "📚 Focus on learning CRITICAL skills first. Consider entry-level roles as stepping stones.",
                'icon': '📚',
                'action': 'Upskill 3-6 months',
                'color': '#E53935'
            }
    
    def get_role_requirements_preview(self, target_role):
        """
        Get preview of role requirements for display
        
        Args:
            target_role (str): Job role
            
        Returns:
            dict: Role requirements preview
        """
        if target_role not in self.role_skills:
            return None
        
        role_data = self.role_skills[target_role]
        skills_info = role_data['skills']
        
        # Get top skills by frequency
        top_skills = sorted(
            [{'skill': s, 'percentage': info['percentage'], 'demand': info['demand_score']} 
             for s, info in skills_info.items()],
            key=lambda x: x['percentage'],
            reverse=True
        )[:10]
        
        return {
            'role': target_role,
            'total_postings': role_data['total_postings'],
            'total_skills': len(skills_info),
            'top_skills': top_skills,
            'skills_list': list(skills_info.keys())
        }
    
    def get_comprehensive_recommendations(self, user_skills, target_role):
        """
        Get comprehensive career recommendations
        
        Args:
            user_skills (list): User's current skills
            target_role (str): Target job role
            
        Returns:
            dict: Complete recommendations
        """
        gap_analysis = self.analyze_gap(user_skills, target_role)
        
        if 'error' in gap_analysis:
            return gap_analysis
        
        # Find alternative roles if gap is too large
        alternative_roles = []
        if gap_analysis['match_percentage'] < 40:
            alternative_roles = self._find_alternative_roles(user_skills)
        
        # Calculate ROI for missing skills
        roi_analysis = self._calculate_skill_roi(gap_analysis['missing_skills_details'])
        
        return {
            **gap_analysis,
            'alternative_roles': alternative_roles,
            'roi_analysis': roi_analysis
        }
    
    def _find_alternative_roles(self, user_skills):
        """
        Find alternative roles that match user's current skills
        
        Args:
            user_skills (list): User's skills
            
        Returns:
            list: Alternative role suggestions
        """
        alternatives = []
        user_set = set([s.title() for s in user_skills])
        
        for role, role_data in self.role_skills.items():
            required_set = set(role_data['all_skills'])
            matched = len(user_set & required_set)
            total = len(required_set)
            
            if total > 0:
                match_pct = (matched / total) * 100
                if 35 <= match_pct < 70:
                    alternatives.append({
                        'role': role,
                        'match_percentage': round(match_pct, 1),
                        'matched_skills': list(user_set & required_set)[:5],
                        'gap_skills': list(required_set - user_set)[:5]
                    })
        
        return sorted(alternatives, key=lambda x: x['match_percentage'], reverse=True)[:3]
    
    def _calculate_skill_roi(self, missing_skills):
        """
        Calculate ROI for learning missing skills
        
        Args:
            missing_skills (list): Missing skills with details
            
        Returns:
            list: ROI analysis for each skill
        """
        roi_results = []
        
        for skill_info in missing_skills:
            skill = skill_info['skill']
            market_demand = skill_info['market_demand_score']
            role_frequency = skill_info['percentage_in_role']
            priority_score = skill_info['priority_score']
            is_critical = skill_info.get('is_critical', False)
            
            # Get salary premium for this skill
            if skill in self.skill_market_demand:
                avg_salary = self.skill_market_demand[skill]['avg_salary']
                salary_boost_pct = 0.20 if is_critical else 0.10
            else:
                avg_salary = 85000
                salary_boost_pct = 0.15 if is_critical else 0.08
            
            roi_results.append({
                'skill': skill,
                'avg_salary': avg_salary,
                'market_demand': market_demand,
                'role_frequency': role_frequency,
                'priority_score': priority_score,
                'is_critical': is_critical,
                'estimated_salary_boost': round(avg_salary * salary_boost_pct, 0),
                'roi_score': round((priority_score * 0.6) + (market_demand * 0.4), 1)
            })
        
        return sorted(roi_results, key=lambda x: x['roi_score'], reverse=True)


# Test the module
if __name__ == "__main__":
    from src.data_loader import DataLoader
    
    print("="*70)
    print("TESTING SKILL GAP ANALYZER (UPDATED DEMAND SCORES)")
    print("="*70)
    
    # Load data
    loader = DataLoader()
    df = loader.load_data()
    df_clean = loader.clean_data(df)
    
    # Initialize analyzer
    print("\n📊 Initializing Skill Gap Analyzer with updated demand scores...")
    analyzer = SkillGapAnalyzer(df_clean)
    
    # Test with different scenarios
    test_cases = [
        (['Python', 'Excel', 'SQL'], 'Data Scientist'),
        (['Python', 'SQL', 'Machine Learning'], 'Data Scientist'),
        (['Excel', 'SQL', 'Tableau'], 'Data Analyst'),
        (['Python', 'SQL', 'Spark', 'AWS'], 'Data Engineer'),
    ]
    
    for user_skills, target_role in test_cases:
        print(f"\n{'='*70}")
        print(f"👤 User Skills: {user_skills}")
        print(f"🎯 Target Role: {target_role}")
        print("-"*70)
        
        results = analyzer.analyze_gap(user_skills, target_role)
        
        if 'error' not in results:
            print(f"\n📈 Match Percentage: {results['match_percentage']}%")
            print(f"✅ Matched Skills: {results['matched_skills']}")
            print(f"❌ Missing Skills Count: {len(results['missing_skills'])}")
            
            print(f"\n📚 Prioritized Learning Path:")
            for i, skill_info in enumerate(results['learning_path'][:8], 1):
                print(f"   {i}. {skill_info['priority_icon']} {skill_info['skill']} - {skill_info['priority']} Priority")
                print(f"      Score: {skill_info['priority_score']:.1f} | Est: {skill_info['estimated_time']}")
                print(f"      Market Demand: {skill_info['market_demand']:.0f}/100 | Role Frequency: {skill_info['frequency_in_role']:.1f}%")
            
            print(f"\n💡 Status: {results['status']['message']}")
            print(f"🎯 Action: {results['status']['action']}")
        else:
            print(f"❌ Error: {results['error']}")
    
    print("\n" + "="*70)
    print("✅ Skill Gap Analyzer Test Complete!")
    print("="*70)