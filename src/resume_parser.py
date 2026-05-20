"""
Resume Parser - Extract skills and experience from resumes
Demonstrates advanced text processing, pattern matching, and NLP capabilities
Supports PDF, DOCX, and text file formats with fallback mechanisms
"""

import re
import pandas as pd
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import os

# Try to import optional dependencies
try:
    import PyPDF2
    PDF_SUPPORT = True
except ImportError:
    PDF_SUPPORT = False
    print("⚠️ PyPDF2 not installed. PDF support limited. Install with: pip install PyPDF2")

try:
    import docx2txt
    DOCX_SUPPORT = True
except ImportError:
    DOCX_SUPPORT = False
    print("⚠️ docx2txt not installed. DOCX support limited. Install with: pip install docx2txt")

class ResumeParser:
    """
    Parse resumes to extract skills, experience, education, and contact information
    Supports PDF, DOCX, and text file formats
    """
    
    # Comprehensive skills database
    SKILLS_DATABASE = {
        'Programming Languages': {
            'Python': ['python', 'django', 'flask', 'numpy', 'pandas', 'python3'],
            'SQL': ['sql', 'mysql', 'postgresql', 'sqlite', 'mongodb', 'nosql'],
            'Java': ['java', 'spring', 'hibernate', 'maven', 'j2ee'],
            'JavaScript': ['javascript', 'react', 'node.js', 'nodejs', 'angular', 'vue', 'typescript'],
            'R': ['r', 'rstudio', 'ggplot2', 'dplyr', 'tidyverse'],
            'C++': ['c++', 'cpp', 'c plus plus', 'c11'],
            'Scala': ['scala', 'spark scala'],
            'Go': ['golang', 'go language', 'goprogramming']
        },
        'Data & Analytics': {
            'Excel': ['excel', 'spreadsheet', 'vba', 'pivot table', 'ms excel', 'microsoft excel'],
            'Tableau': ['tableau', 'data visualization', 'tableau desktop', 'tableau prep'],
            'Power BI': ['power bi', 'powerbi', 'microsoft bi', 'power query'],
            'Statistics': ['statistics', 'statistical analysis', 'hypothesis testing', 'regression', 'anova'],
            'Data Analysis': ['data analysis', 'exploratory data analysis', 'eda', 'data analytics'],
            'Data Visualization': ['data visualization', 'dashboard', 'reporting', 'visualization']
        },
        'Machine Learning & AI': {
            'Machine Learning': ['machine learning', 'ml', 'supervised learning', 'unsupervised learning', 'model training'],
            'Deep Learning': ['deep learning', 'neural network', 'neural networks', 'cnn', 'rnn', 'lstm'],
            'TensorFlow': ['tensorflow', 'tf', 'keras', 'tensorflow2'],
            'PyTorch': ['pytorch', 'torch', 'pytorch lightning'],
            'Scikit-Learn': ['scikit-learn', 'sklearn', 'scikit learn'],
            'NLP': ['nlp', 'natural language processing', 'text mining', 'llm', 'gpt', 'bert', 'transformers'],
            'Computer Vision': ['computer vision', 'image processing', 'opencv', 'image recognition'],
            'LLM': ['llm', 'large language model', 'gpt', 'bert', 'transformer', 'chatgpt']
        },
        'Cloud & DevOps': {
            'AWS': ['aws', 'amazon web services', 'ec2', 's3', 'lambda', 'cloudformation', 'aws cloud'],
            'Azure': ['azure', 'microsoft azure', 'azure devops', 'azure cloud'],
            'GCP': ['gcp', 'google cloud', 'google cloud platform', 'gcloud'],
            'Docker': ['docker', 'containerization', 'container', 'dockerfile', 'docker compose'],
            'Kubernetes': ['kubernetes', 'k8s', 'kubectl', 'kubernetes cluster'],
            'Git': ['git', 'github', 'gitlab', 'version control', 'bitbucket', 'git commands'],
            'CI/CD': ['ci/cd', 'jenkins', 'circleci', 'github actions', 'gitlab ci', 'continuous integration']
        },
        'Big Data': {
            'Spark': ['spark', 'apache spark', 'pyspark', 'spark sql'],
            'Hadoop': ['hadoop', 'hdfs', 'mapreduce', 'hadoop ecosystem', 'hive'],
            'Kafka': ['kafka', 'apache kafka', 'kafka streams'],
            'Airflow': ['airflow', 'apache airflow', 'workflow orchestration']
        },
        'Databases': {
            'PostgreSQL': ['postgresql', 'postgres', 'psql'],
            'MySQL': ['mysql', 'mysql database'],
            'MongoDB': ['mongodb', 'mongo', 'nosql database'],
            'Redis': ['redis', 'redis cache']
        },
        'Soft Skills': {
            'Leadership': ['leadership', 'team lead', 'management', 'team management', 'leading teams'],
            'Communication': ['communication', 'presentation', 'public speaking', 'written communication'],
            'Project Management': ['project management', 'agile', 'scrum', 'jira', 'kanban', 'project lead'],
            'Problem Solving': ['problem solving', 'analytical', 'critical thinking', 'troubleshooting'],
            'Teamwork': ['teamwork', 'collaboration', 'cross-functional', 'team player', 'coordination']
        }
    }
    
    # Education degree levels and keywords
    EDUCATION_KEYWORDS = {
        'PhD': ['phd', 'doctor of philosophy', 'doctorate', 'doctoral', 'ph.d'],
        'Master\'s': ['master', 'ms', 'm.s.', 'm.sc', 'masters', 'masters degree', 'mba', 'm.b.a'],
        'Bachelor\'s': ['bachelor', 'bs', 'b.s.', 'b.sc', 'bachelors', 'bachelors degree', 'ba', 'b.a.', 'btech', 'b.tech'],
        'Associate': ['associate', 'associates degree', 'aa degree'],
        'Certificate': ['certificate', 'certification', 'bootcamp', 'certified', 'professional certificate']
    }
    
    def __init__(self):
        self.parsed_data = {}
        
    def parse_resume_file(self, file_path: str) -> Dict:
        """
        Parse resume from file (PDF, DOCX, or TXT)
        
        Args:
            file_path: Path to resume file
            
        Returns:
            Dictionary with parsed information
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            return {'error': f'File not found: {file_path}'}
        
        # Extract text based on file type
        if file_path.suffix.lower() == '.pdf':
            text = self._extract_from_pdf(file_path)
        elif file_path.suffix.lower() in ['.docx', '.doc']:
            text = self._extract_from_docx(file_path)
        else:
            text = self._extract_from_txt(file_path)
        
        if not text:
            return {'error': 'Could not extract text from file'}
        
        # Parse the extracted text
        return self.parse_resume_text(text)
    
    def _extract_from_pdf(self, pdf_path: Path) -> str:
        """Extract text from PDF file"""
        if not PDF_SUPPORT:
            return self._extract_pdf_without_library(pdf_path)
        
        try:
            text = ""
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            return text
        except Exception as e:
            print(f"Error reading PDF with PyPDF2: {e}")
            return self._extract_pdf_without_library(pdf_path)
    
    def _extract_pdf_without_library(self, pdf_path: Path) -> str:
        """Fallback: Extract text from PDF using command line or return empty"""
        print(f"⚠️ Install PyPDF2 for better PDF parsing: pip install PyPDF2")
        return ""
    
    def _extract_from_docx(self, docx_path: Path) -> str:
        """Extract text from DOCX file"""
        if not DOCX_SUPPORT:
            return self._extract_docx_without_library(docx_path)
        
        try:
            text = docx2txt.process(docx_path)
            return text if text else ""
        except Exception as e:
            print(f"Error reading DOCX with docx2txt: {e}")
            return self._extract_docx_without_library(docx_path)
    
    def _extract_docx_without_library(self, docx_path: Path) -> str:
        """Fallback: Basic DOCX extraction or recommend installation"""
        print(f"⚠️ Install docx2txt for better DOCX parsing: pip install docx2txt")
        return ""
    
    def _extract_from_txt(self, txt_path: Path) -> str:
        """Extract text from TXT file"""
        try:
            with open(txt_path, 'r', encoding='utf-8') as file:
                return file.read()
        except UnicodeDecodeError:
            try:
                with open(txt_path, 'r', encoding='latin-1') as file:
                    return file.read()
            except Exception as e:
                print(f"Error reading TXT: {e}")
                return ""
    
    def parse_resume_text(self, text: str) -> Dict:
        """
        Parse resume text to extract all relevant information
        
        Args:
            text: Resume text content
            
        Returns:
            Dictionary with skills, experience, education, etc.
        """
        if not text or len(text.strip()) == 0:
            return {'error': 'No text content to parse'}
        
        text_lower = text.lower()
        
        # Extract skills
        skills = self._extract_skills(text_lower)
        
        # Extract experience years
        experience = self._extract_experience_years(text)
        
        # Extract education
        education = self._extract_education(text_lower)
        
        # Extract contact information
        contact = self._extract_contact_info(text)
        
        # Extract job titles mentioned
        job_titles = self._extract_job_titles(text)
        
        # Calculate skill scores
        skill_scores = self._calculate_skill_scores(skills)
        
        self.parsed_data = {
            'skills': skills,
            'skill_count': len(skills),
            'skills_by_category': self._group_skills_by_category(skills),
            'experience_years': experience,
            'education': education,
            'contact': contact,
            'mentioned_job_titles': job_titles,
            'skill_scores': skill_scores,
            'market_readiness_score': self._calculate_readiness_score(skills, experience)
        }
        
        return self.parsed_data
    
    def _extract_skills(self, text_lower: str) -> List[str]:
        """Extract all skills from text"""
        found_skills = []
        
        for category, skills_dict in self.SKILLS_DATABASE.items():
            for skill, keywords in skills_dict.items():
                for keyword in keywords:
                    if keyword in text_lower:
                        found_skills.append(skill)
                        break
        
        # Remove duplicates while preserving order
        return list(dict.fromkeys(found_skills))
    
    def _extract_experience_years(self, text: str) -> int:
        """Extract years of work experience"""
        text_lower = text.lower()
        
        # Pattern 1: "X+ years of experience"
        pattern1 = r'(\d+)\+?\s*years?\s*(?:of\s*)?experience'
        match = re.search(pattern1, text_lower, re.IGNORECASE)
        if match:
            return int(match.group(1))
        
        # Pattern 2: "experience of X years"
        pattern2 = r'experience\s*(?:of)?\s*(\d+)\+?\s*years?'
        match = re.search(pattern2, text_lower, re.IGNORECASE)
        if match:
            return int(match.group(1))
        
        # Pattern 3: Look for date ranges in work history
        date_pattern = r'(?:from|since)?\s*(\d{4})\s*(?:to|-|\s*until\s*)(?:\s*present|\s*current|\s*(\d{4}))'
        dates = re.findall(date_pattern, text, re.IGNORECASE)
        
        if dates:
            total_years = 0
            for start, end in dates:
                if end:
                    try:
                        total_years += int(end) - int(start)
                    except:
                        pass
                else:
                    # Present/current
                    try:
                        total_years += 2026 - int(start)
                    except:
                        pass
            if total_years > 0:
                return total_years
        
        return 0
    
    def _extract_education(self, text_lower: str) -> Dict:
        """Extract education information"""
        education = {'highest_degree': None, 'details': []}
        found_degrees = []
        
        for degree, keywords in self.EDUCATION_KEYWORDS.items():
            for keyword in keywords:
                if keyword in text_lower:
                    found_degrees.append(degree)
                    # Try to extract field of study
                    field_pattern = rf'{keyword}\s+(?:in|of)?\s*([a-z\s]+?)(?:\n|\.|,|$)'
                    match = re.search(field_pattern, text_lower, re.IGNORECASE)
                    if match:
                        education['details'].append({
                            'degree': degree,
                            'field': match.group(1).strip()
                        })
                        break
                    else:
                        education['details'].append({'degree': degree, 'field': None})
                    break
        
        # Determine highest degree
        degree_order = ['PhD', 'Master\'s', 'Bachelor\'s', 'Associate', 'Certificate']
        for degree in degree_order:
            if degree in found_degrees:
                education['highest_degree'] = degree
                break
        
        return education
    
    def _extract_contact_info(self, text: str) -> Dict:
        """Extract email, phone, LinkedIn from text"""
        contact = {'email': None, 'phone': None, 'linkedin': None}
        
        # Extract email
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        email_match = re.search(email_pattern, text)
        if email_match:
            contact['email'] = email_match.group()
        
        # Extract phone (US format and international)
        phone_patterns = [
            r'(\+?1[-.\s]?)?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}',  # US
            r'(\+\d{1,3}[-.\s]?)?\(?\d{2,4}\)?[-.\s]?\d{3,4}[-.\s]?\d{3,4}'  # International
        ]
        
        for pattern in phone_patterns:
            phone_match = re.search(pattern, text)
            if phone_match:
                contact['phone'] = phone_match.group()
                break
        
        # Extract LinkedIn
        linkedin_pattern = r'linkedin\.com/in/[a-zA-Z0-9\-_]+'
        linkedin_match = re.search(linkedin_pattern, text, re.IGNORECASE)
        if linkedin_match:
            contact['linkedin'] = linkedin_match.group()
        
        return contact
    
    def _extract_job_titles(self, text: str) -> List[str]:
        """Extract mentioned job titles from text"""
        common_titles = [
            'Data Scientist', 'Data Analyst', 'Data Engineer', 'ML Engineer', 'Machine Learning Engineer',
            'Business Analyst', 'Product Manager', 'Project Manager', 'Software Engineer', 'Software Developer',
            'Data Architect', 'Analytics Manager', 'Research Scientist', 'BI Analyst', 'BI Developer',
            'Database Administrator', 'Cloud Engineer', 'DevOps Engineer', 'Full Stack Developer',
            'Data Warehouse Engineer', 'Analytics Consultant', 'Data Product Manager', 'AI Researcher'
        ]
        
        found_titles = []
        text_lower = text.lower()
        
        for title in common_titles:
            if title.lower() in text_lower:
                found_titles.append(title)
        
        return found_titles
    
    def _group_skills_by_category(self, skills: List[str]) -> Dict:
        """Group skills by their category"""
        grouped = {}
        
        for category, skills_dict in self.SKILLS_DATABASE.items():
            category_skills = []
            for skill in skills:
                if skill in skills_dict:
                    category_skills.append(skill)
            if category_skills:
                grouped[category] = category_skills
        
        return grouped
    
    def _calculate_skill_scores(self, skills: List[str]) -> Dict:
        """Calculate demand score for each skill based on market data"""
        demand_scores = {
            'Python': 95, 'SQL': 93, 'Machine Learning': 98, 'Deep Learning': 96,
            'TensorFlow': 94, 'PyTorch': 94, 'AWS': 92, 'Spark': 91,
            'NLP': 91, 'LLM': 94, 'Docker': 89, 'Git': 87, 'Tableau': 87,
            'Power BI': 86, 'Azure': 87, 'Java': 85, 'JavaScript': 84,
            'Statistics': 88, 'Data Visualization': 86, 'Kubernetes': 88,
            'Excel': 85, 'R': 82, 'Scala': 78, 'MongoDB': 79,
            'PostgreSQL': 80, 'MySQL': 79, 'Hadoop': 80,
            'Communication': 85, 'Leadership': 82, 'Project Management': 80
        }
        
        scores = {}
        for skill in skills:
            scores[skill] = demand_scores.get(skill, 75)
        
        return scores
    
    def _calculate_readiness_score(self, skills: List[str], experience: int) -> Dict:
        """Calculate job market readiness score"""
        high_value_skills = ['Python', 'SQL', 'Machine Learning', 'TensorFlow', 'PyTorch', 'AWS', 'Spark']
        high_value_count = sum(1 for s in skills if s in high_value_skills)
        
        skill_score = min(50, high_value_count * 12) + min(20, len(skills) * 3)
        
        if experience >= 5:
            exp_score = 30
        elif experience >= 3:
            exp_score = 25
        elif experience >= 1:
            exp_score = 18
        elif experience > 0:
            exp_score = 10
        else:
            exp_score = 5
        
        total_score = min(100, skill_score + exp_score)
        
        if total_score >= 80:
            level = "Excellent (Ready for Senior Roles)"
            description = "You have strong skills and experience. Ready for leadership positions."
        elif total_score >= 65:
            level = "Good (Ready for Mid-Level Roles)"
            description = "Well-qualified for most mid-level positions. Focus on deepening expertise."
        elif total_score >= 45:
            level = "Developing (Ready for Junior Roles)"
            description = "Good foundation. Build project portfolio and consider certifications."
        else:
            level = "Beginner (Consider Internships/Entry Level)"
            description = "Start with foundational courses and build practical projects."
        
        return {'score': total_score, 'level': level, 'description': description}
    
    def generate_match_analysis(self, target_role: str, job_requirements: List[str]) -> Dict:
        """
        Generate skill match analysis against target job role
        
        Args:
            target_role: Target job title
            job_requirements: List of required skills for the role
            
        Returns:
            Match analysis with gaps and recommendations
        """
        if not self.parsed_data:
            return {'error': 'No resume parsed yet'}
        
        user_skills = set(self.parsed_data['skills'])
        required_skills = set(job_requirements)
        
        matched = user_skills & required_skills
        missing = required_skills - user_skills
        extra = user_skills - required_skills
        
        match_percentage = (len(matched) / len(required_skills) * 100) if required_skills else 0
        
        # Convert sets to lists for serialization
        matched_list = list(matched)
        missing_list = list(missing)
        extra_list = list(extra)
        
        # Categorize missing skills by priority
        high_priority_skills = ['Python', 'SQL', 'Machine Learning', 'AWS', 'Spark', 'TensorFlow', 'PyTorch']
        missing_priority = {
            'high': [s for s in missing_list if s in high_priority_skills],
            'medium': [s for s in missing_list if s not in high_priority_skills]
        }
        
        return {
            'target_role': target_role,
            'match_percentage': round(match_percentage, 1),
            'matched_skills': matched_list,
            'missing_skills': missing_list,
            'missing_skills_priority': missing_priority,
            'extra_skills': extra_list,
            'recommendations': self._generate_recommendations(missing_list, match_percentage)
        }
    
    def _generate_recommendations(self, missing_skills: List[str], match_score: float) -> List[str]:
        """
        Generate learning recommendations based on skill gaps
        
        Args:
            missing_skills: List of missing skills (NOT a set!)
            match_score: Match percentage score
            
        Returns:
            List of recommendation strings
        """
        recommendations = []
        
        if match_score >= 80:
            recommendations.append("🎉 You're well qualified! Focus on interview preparation and portfolio presentation.")
        elif match_score >= 60:
            recommendations.append("📈 Good match! Focus on learning the missing skills through online courses and projects.")
        elif match_score >= 40:
            recommendations.append("📚 Moderate gap. Consider a structured learning path and build projects to demonstrate skills.")
        else:
            recommendations.append("🚀 Significant growth opportunity. Start with foundational courses and consider entry-level positions.")
        
        if missing_skills:
            recommendations.append(f"\n🎯 Priority Skills to Learn ({len(missing_skills)} identified):")
            for skill in missing_skills[:10]:
                recommendations.append(f"   • {skill}: Take courses on Coursera/Udemy, build a project")
        
        recommendations.append("\n💡 Quick Action Plan:")
        recommendations.append("   1. Enroll in targeted courses for top 3 missing skills")
        recommendations.append("   2. Build portfolio projects demonstrating these skills")
        recommendations.append("   3. Update your resume to highlight matched skills")
        recommendations.append("   4. Start networking with professionals in your target role")
        
        return recommendations
    
    def generate_resume_report(self) -> str:
        """Generate a formatted report of parsed resume data"""
        if not self.parsed_data:
            return "No resume data available. Please parse a resume first."
        
        data = self.parsed_data
        
        report = "\n" + "="*70 + "\n"
        report += "📄 RESUME PARSING REPORT\n"
        report += "="*70 + "\n\n"
        
        # Skills section
        report += f"🎯 SKILLS ({data['skill_count']} skills found):\n"
        report += "-"*40 + "\n"
        
        if data['skills_by_category']:
            for category, skills in data['skills_by_category'].items():
                report += f"\n   📁 {category}:\n"
                for skill in skills:
                    skill_score = data['skill_scores'].get(skill, 75)
                    score_bar = "█" * int(skill_score / 10) + "░" * (10 - int(skill_score / 10))
                    report += f"      • {skill:<20} {score_bar} {skill_score}/100\n"
        else:
            report += "   No skills detected. Try using a more detailed resume format.\n"
        
        # Experience section
        report += f"\n💼 WORK EXPERIENCE:\n"
        report += "-"*40 + "\n"
        report += f"   Years of Experience: {data['experience_years']}\n"
        
        # Education section
        if data['education']['highest_degree']:
            report += f"\n🎓 EDUCATION:\n"
            report += "-"*40 + "\n"
            report += f"   Highest Degree: {data['education']['highest_degree']}\n"
        
        # Contact info
        if any(data['contact'].values()):
            report += f"\n📞 CONTACT INFORMATION:\n"
            report += "-"*40 + "\n"
            if data['contact']['email']:
                report += f"   Email: {data['contact']['email']}\n"
            if data['contact']['phone']:
                report += f"   Phone: {data['contact']['phone']}\n"
            if data['contact']['linkedin']:
                report += f"   LinkedIn: {data['contact']['linkedin']}\n"
        
        # Job titles mentioned
        if data['mentioned_job_titles']:
            report += f"\n💼 MENTIONED JOB TITLES:\n"
            report += "-"*40 + "\n"
            for title in data['mentioned_job_titles'][:5]:
                report += f"   • {title}\n"
        
        # Market Readiness
        report += f"\n📊 MARKET READINESS:\n"
        report += "-"*40 + "\n"
        report += f"   Score: {data['market_readiness_score']['score']}/100\n"
        report += f"   Level: {data['market_readiness_score']['level']}\n"
        report += f"   {data['market_readiness_score']['description']}\n"
        
        report += "\n" + "="*70 + "\n"
        
        return report


# Test the module
if __name__ == "__main__":
    print("="*70)
    print("TESTING RESUME PARSER")
    print("="*70)
    
    parser = ResumeParser()
    
    # Test with sample resume text
    sample_resume = """
    John Smith
    Data Scientist with 5 years of experience
    Contact: john.smith@email.com | (555) 123-4567
    LinkedIn: linkedin.com/in/johnsmith
    
    SKILLS
    Python, SQL, Machine Learning, TensorFlow, AWS, Tableau, Statistics
    
    WORK EXPERIENCE
    Senior Data Scientist | TechCorp | 2020-2025
    - Built ML models using PyTorch and Scikit-learn
    - Deployed solutions on AWS Cloud
    - Led data science team of 5
    
    Data Analyst | DataInsights | 2018-2020
    - Analyzed customer data using SQL and Python
    - Created dashboards in Tableau
    
    EDUCATION
    Master's in Data Science, Stanford University (2018)
    Bachelor's in Computer Science, UC Berkeley (2016)
    
    CERTIFICATIONS
    AWS Certified Solutions Architect
    TensorFlow Developer Certificate
    """
    
    # Parse the resume
    print("\n📄 Parsing sample resume...")
    parsed_data = parser.parse_resume_text(sample_resume)
    
    if 'error' not in parsed_data:
        print(f"\n✅ Parsed Resume Successfully!")
        print(f"👤 Skills Found ({len(parsed_data['skills'])}): {', '.join(parsed_data['skills'][:10])}")
        print(f"💼 Experience: {parsed_data['experience_years']} years")
        print(f"🎓 Education: {parsed_data['education']['highest_degree'] or 'Not found'}")
        print(f"📊 Market Readiness: {parsed_data['market_readiness_score']['score']}/100 - {parsed_data['market_readiness_score']['level']}")
        
        # Generate full report
        print(parser.generate_resume_report())
        
        # Test match analysis
        job_requirements = ['Python', 'SQL', 'Machine Learning', 'TensorFlow', 'PyTorch', 'AWS', 'Docker', 'Kubernetes']
        match = parser.generate_match_analysis('Data Scientist', job_requirements)
        
        print(f"\n🎯 JOB MATCH ANALYSIS:")
        print(f"   Target Role: {match['target_role']}")
        print(f"   Match Score: {match['match_percentage']}%")
        print(f"   ✅ Matched Skills: {match['matched_skills']}")
        print(f"   ❌ Missing Skills: {match['missing_skills'][:5]}")
        print(f"\n   📚 Recommendations:")
        for rec in match['recommendations'][:5]:
            print(f"      {rec}")
    else:
        print(f"❌ Error: {parsed_data['error']}")
    
    print("\n" + "="*70)
    print("✅ Resume Parser Test Complete!")
    print("="*70)