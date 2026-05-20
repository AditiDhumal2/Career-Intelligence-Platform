"""
Career Path Mapper Module
Maps career progression and required skills for each level
"""

import json
from typing import Dict, List

class CareerPathMapper:
    """
    Maps career progression paths and skill requirements
    """
    
    def __init__(self):
        """Initialize career path database"""
        self.career_paths = self._load_career_paths()
        self.skill_hierarchy = self._load_skill_hierarchy()
    
    def _load_career_paths(self):
        """
        Define career progression paths
        Returns dict of career paths and skill requirements
        """
        return {
            'Data Analytics Track': {
                'description': 'Path from data analyst to data leader',
                'levels': {
                    'Junior Data Analyst': {
                        'required_skills': ['Excel', 'SQL', 'Statistics', 'Data Visualization'],
                        'preferred_skills': ['Python Basics', 'Tableau'],
                        'experience_years': 0-2,
                        'avg_salary': '60k-80k',
                        'next_roles': ['Data Analyst', 'Business Analyst']
                    },
                    'Data Analyst': {
                        'required_skills': ['Python', 'SQL', 'Excel', 'Statistics', 'Data Visualization', 'Pandas'],
                        'preferred_skills': ['R', 'Tableau', 'Power BI', 'Communication'],
                        'experience_years': 2-4,
                        'avg_salary': '75k-95k',
                        'next_roles': ['Senior Data Analyst', 'Data Scientist']
                    },
                    'Senior Data Analyst': {
                        'required_skills': ['Advanced Python', 'Advanced SQL', 'Statistical Analysis', 'Data Storytelling', 'Project Management'],
                        'preferred_skills': ['Machine Learning Basics', 'Leadership', 'A/B Testing'],
                        'experience_years': 4-6,
                        'avg_salary': '90k-120k',
                        'next_roles': ['Lead Data Analyst', 'Data Science Manager']
                    },
                    'Lead Data Analyst': {
                        'required_skills': ['Team Leadership', 'Data Strategy', 'Advanced Analytics', 'Stakeholder Management', 'Data Architecture'],
                        'preferred_skills': ['Mentoring', 'Strategic Planning', 'Data Governance'],
                        'experience_years': 6-8,
                        'avg_salary': '110k-150k',
                        'next_roles': ['Data Science Manager', 'Director of Analytics']
                    }
                }
            },
            'Data Science Track': {
                'description': 'Path from data scientist to AI leader',
                'levels': {
                    'Junior Data Scientist': {
                        'required_skills': ['Python', 'SQL', 'Statistics', 'Machine Learning Basics', 'Data Wrangling'],
                        'preferred_skills': ['R', 'Tableau', 'Git', 'Linear Algebra'],
                        'experience_years': 0-2,
                        'avg_salary': '80k-100k',
                        'next_roles': ['Data Scientist', 'Machine Learning Engineer']
                    },
                    'Data Scientist': {
                        'required_skills': ['Python', 'SQL', 'Machine Learning', 'Statistical Modeling', 'Data Visualization', 'TensorFlow/PyTorch'],
                        'preferred_skills': ['Big Data Tools', 'Cloud Computing', 'Deep Learning', 'NLP'],
                        'experience_years': 2-5,
                        'avg_salary': '100k-140k',
                        'next_roles': ['Senior Data Scientist', 'ML Engineer']
                    },
                    'Senior Data Scientist': {
                        'required_skills': ['Advanced ML', 'Deep Learning', 'Model Deployment', 'Research', 'Experimentation', 'Mentoring'],
                        'preferred_skills': ['LLMs', 'Computer Vision', 'ML Ops', 'Leadership'],
                        'experience_years': 5-8,
                        'avg_salary': '130k-170k',
                        'next_roles': ['Lead Data Scientist', 'AI Research Scientist']
                    },
                    'Lead Data Scientist': {
                        'required_skills': ['AI Strategy', 'Team Management', 'Project Leadership', 'Advanced Research', 'Cross-functional Collaboration'],
                        'preferred_skills': ['Product Sense', 'Business Strategy', 'Technical Architecture'],
                        'experience_years': 8-12,
                        'avg_salary': '160k-220k',
                        'next_roles': ['Director of Data Science', 'Chief Data Officer']
                    }
                }
            },
            'Data Engineering Track': {
                'description': 'Path from data engineer to data architect',
                'levels': {
                    'Junior Data Engineer': {
                        'required_skills': ['Python', 'SQL', 'ETL Basics', 'Database Concepts', 'Linux'],
                        'preferred_skills': ['Shell Scripting', 'Airflow Basics', 'Docker'],
                        'experience_years': 0-2,
                        'avg_salary': '70k-90k',
                        'next_roles': ['Data Engineer', 'BI Developer']
                    },
                    'Data Engineer': {
                        'required_skills': ['Python', 'SQL', 'ETL Pipelines', 'Data Warehousing', 'Spark', 'Airflow'],
                        'preferred_skills': ['AWS/Azure/GCP', 'Kafka', 'Docker', 'Kubernetes'],
                        'experience_years': 2-5,
                        'avg_salary': '90k-120k',
                        'next_roles': ['Senior Data Engineer', 'Data Architect']
                    },
                    'Senior Data Engineer': {
                        'required_skills': ['Big Data Technologies', 'Data Architecture', 'Streaming Data', 'ML Ops', 'Team Leadership'],
                        'preferred_skills': ['Data Governance', 'Security', 'Optimization', 'Mentoring'],
                        'experience_years': 5-8,
                        'avg_salary': '120k-160k',
                        'next_roles': ['Lead Data Engineer', 'Data Architect']
                    },
                    'Data Architect': {
                        'required_skills': ['Enterprise Architecture', 'Data Strategy', 'Data Modeling', 'System Design', 'Data Governance'],
                        'preferred_skills': ['Business Strategy', 'Vendor Management', 'Team Management'],
                        'experience_years': 8-12,
                        'avg_salary': '150k-200k',
                        'next_roles': ['Director of Data Engineering', 'CTO']
                    }
                }
            }
        }
    
    def _load_skill_hierarchy(self):
        """
        Define skill hierarchy for progressive learning
        """
        return {
            'Python': {
                'level': 'Foundation',
                'prerequisites': ['Basic Programming Concepts'],
                'next_skills': ['Pandas', 'NumPy', 'Scikit-learn', 'TensorFlow']
            },
            'SQL': {
                'level': 'Foundation',
                'prerequisites': ['Database Concepts'],
                'next_skills': ['Advanced SQL', 'Database Optimization']
            },
            'Statistics': {
                'level': 'Foundation',
                'prerequisites': ['Basic Math'],
                'next_skills': ['Statistical Modeling', 'A/B Testing', 'Machine Learning']
            },
            'Pandas': {
                'level': 'Intermediate',
                'prerequisites': ['Python'],
                'next_skills': ['Data Wrangling', 'Data Analysis']
            },
            'Machine Learning': {
                'level': 'Advanced',
                'prerequisites': ['Python', 'Statistics', 'Linear Algebra'],
                'next_skills': ['Deep Learning', 'NLP', 'Computer Vision']
            }
        }
    
    def get_role_requirements(self, role_name):
        """
        Get requirements for a specific role
        
        Args:
            role_name (str): Name of the role
            
        Returns:
            dict: Role requirements or None if not found
        """
        for track in self.career_paths.values():
            if role_name in track['levels']:
                return track['levels'][role_name]
        return None
    
    def get_career_path(self, start_role, end_role):
        """
        Get career path from start to end role
        
        Args:
            start_role (str): Starting role
            end_role (str): Target role
            
        Returns:
            dict: Career path with intermediate steps
        """
        # Find tracks containing both roles
        path = []
        found_start = False
        found_end = False
        
        for track_name, track in self.career_paths.items():
            levels = track['levels']
            level_names = list(levels.keys())
            
            if start_role in level_names and end_role in level_names:
                start_idx = level_names.index(start_role)
                end_idx = level_names.index(end_role)
                
                if start_idx < end_idx:
                    # Forward progression
                    path = level_names[start_idx:end_idx+1]
                    found_start = True
                    found_end = True
                    break
        
        if not path:
            return {'error': f'No direct path found from {start_role} to {end_role}'}
        
        # Build detailed path
        detailed_path = []
        for role in path:
            role_info = self.get_role_requirements(role)
            detailed_path.append({
                'role': role,
                'required_skills': role_info['required_skills'],
                'experience': role_info['experience_years'],
                'salary': role_info['avg_salary']
            })
        
        return {
            'track': track_name,
            'total_steps': len(path),
            'estimated_time': self._calculate_estimated_time(path),
            'path': detailed_path
        }
    
    def _calculate_estimated_time(self, path):
        """
        Calculate estimated time to complete career path
        
        Args:
            path (list): List of roles
            
        Returns:
            str: Estimated time
        """
        total_years = 0
        for role in path:
            role_info = self.get_role_requirements(role)
            if role_info:
                exp_range = role_info['experience_years']
                if isinstance(exp_range, tuple):
                    total_years += (exp_range[0] + exp_range[1]) / 2
                else:
                    total_years += 2
        
        if total_years < 2:
            return "< 2 years"
        elif total_years < 5:
            return "2-5 years"
        elif total_years < 8:
            return "5-8 years"
        else:
            return "8+ years"
    
    def get_skill_progression(self, skill):
        """
        Get learning progression for a specific skill
        
        Args:
            skill (str): Skill name
            
        Returns:
            dict: Skill progression information
        """
        if skill in self.skill_hierarchy:
            return self.skill_hierarchy[skill]
        return None
    
    def get_all_available_roles(self):
        """
        Get all available roles across all tracks
        
        Returns:
            list: All role names
        """
        all_roles = []
        for track in self.career_paths.values():
            all_roles.extend(track['levels'].keys())
        return all_roles
    
    def get_tracks_info(self):
        """
        Get information about all career tracks
        
        Returns:
            dict: Career tracks summary
        """
        tracks_info = {}
        for track_name, track in self.career_paths.items():
            levels = track['levels']
            tracks_info[track_name] = {
                'description': track['description'],
                'entry_level': list(levels.keys())[0],
                'senior_level': list(levels.keys())[-1],
                'total_levels': len(levels),
                'salary_range': f"{levels[list(levels.keys())[0]]['avg_salary']} - {levels[list(levels.keys())[-1]]['avg_salary']}"
            }
        return tracks_info
    
    def generate_path_visualization(self, start_role, end_role):
        """
        Generate text-based visualization of career path
        
        Args:
            start_role (str): Starting role
            end_role (str): Target role
            
        Returns:
            str: ASCII art career path
        """
        path_data = self.get_career_path(start_role, end_role)
        
        if 'error' in path_data:
            return path_data['error']
        
        visualization = "\n" + "="*70 + "\n"
        visualization += f"🏗️  CAREER PATH: {start_role} → {end_role}\n"
        visualization += "="*70 + "\n\n"
        
        for i, step in enumerate(path_data['path']):
            arrow = " → " if i < len(path_data['path']) - 1 else ""
            visualization += f"📌 Step {i+1}: {step['role']}\n"
            visualization += f"   Skills: {', '.join(step['required_skills'][:3])}...\n"
            visualization += f"   Experience: {step['experience']} years\n"
            visualization += f"   Salary: {step['salary']}\n"
            if arrow:
                visualization += f"   {arrow}\n"
            visualization += "\n"
        
        visualization += f"\n⏰ Estimated Time: {path_data['estimated_time']}\n"
        visualization += "="*70 + "\n"
        
        return visualization


# Test the module
if __name__ == "__main__":
    mapper = CareerPathMapper()
    
    print("\n" + "="*70)
    print("CAREER PATH MAPPING - TEST")
    print("="*70)
    
    # Show available tracks
    print("\n📊 Available Career Tracks:")
    for track_name, info in mapper.get_tracks_info().items():
        print(f"\n{track_name}:")
        print(f"   Description: {info['description']}")
        print(f"   Entry Level: {info['entry_level']}")
        print(f"   Senior Level: {info['senior_level']}")
        print(f"   Salary Range: {info['salary_range']}")
    
    # Test path from Data Analyst to Data Scientist
    print("\n" + mapper.generate_path_visualization('Data Analyst', 'Data Scientist'))
    
    # Test path from Junior Data Scientist to Lead Data Scientist
    print(mapper.generate_path_visualization('Junior Data Scientist', 'Lead Data Scientist'))