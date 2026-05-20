"""
Generate large realistic job market dataset
500+ jobs, 30+ skills, 15+ job roles, 20+ locations
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime

def generate_large_dataset(n_records=500):
    """
    Generate realistic job market data
    
    Args:
        n_records: Number of job records to generate
    
    Returns:
        DataFrame with comprehensive job data
    """
    
    # Expanded job roles (22 roles)
    job_titles = [
        'Data Analyst', 'Data Scientist', 'Data Engineer', 'ML Engineer',
        'Business Analyst', 'Business Intelligence Analyst', 'Analytics Manager',
        'Data Architect', 'Database Administrator', 'Data Warehouse Engineer',
        'AI Research Scientist', 'Computer Vision Engineer', 'NLP Engineer',
        'Analytics Consultant', 'Data Product Manager', 'Data Governance Analyst',
        'Marketing Analyst', 'Financial Analyst', 'Operations Analyst',
        'Supply Chain Analyst', 'Healthcare Data Analyst', 'Sports Analyst'
    ]
    
    # Expanded skills (30+ skills)
    skills_list = {
        'Programming': ['Python', 'R', 'Java', 'Scala', 'SQL', 'JavaScript', 'C++', 'Julia'],
        'Data Analysis': ['Excel', 'Statistics', 'Probability', 'Linear Algebra', 'Data Visualization'],
        'ML/AI': ['Machine Learning', 'Deep Learning', 'TensorFlow', 'PyTorch', 'Scikit-learn', 
                  'Keras', 'NLP', 'Computer Vision', 'LLM', 'LangChain', 'RAG'],
        'Big Data': ['Spark', 'Hadoop', 'Hive', 'Kafka', 'Airflow', 'Flink', 'Beam'],
        'Cloud': ['AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes', 'Terraform', 'Jenkins'],
        'Databases': ['PostgreSQL', 'MySQL', 'MongoDB', 'Cassandra', 'Redis', 'Elasticsearch'],
        'BI Tools': ['Tableau', 'Power BI', 'Looker', 'QlikView', 'Metabase'],
        'Soft Skills': ['Communication', 'Leadership', 'Project Management', 'Storytelling', 'Agile']
    }
    
    # Flatten skills
    all_skills = []
    for category, skills in skills_list.items():
        all_skills.extend(skills)
    
    # Locations (23 cities)
    locations = [
        'New York', 'San Francisco', 'Chicago', 'Austin', 'Boston', 'Seattle', 
        'Los Angeles', 'Washington DC', 'Denver', 'Atlanta', 'Miami', 'Dallas',
        'Portland', 'Phoenix', 'Detroit', 'Minneapolis', 'San Diego', 'Philadelphia',
        'Pittsburgh', 'Raleigh', 'Salt Lake City', 'St. Louis', 'Nashville'
    ]
    
    # Industries
    industries = [
        'Technology', 'Finance', 'Healthcare', 'Retail', 'Manufacturing', 
        'Consulting', 'Education', 'Government', 'Media', 'Telecommunications',
        'Energy', 'Transportation', 'Real Estate', 'Insurance', 'Entertainment'
    ]
    
    # Company sizes
    company_sizes = ['Startup', 'Small (11-50)', 'Medium (51-200)', 'Large (201-1000)', 'Enterprise (1000+)']
    
    # Experience levels
    experience_levels = ['Entry', 'Junior', 'Mid', 'Senior', 'Lead', 'Principal', 'Director']
    
    # Education requirements
    education = ['Bachelor\'s', 'Master\'s', 'PhD', 'Associate', 'High School + Certification']
    
    # Remote policies
    remote_policies = ['Remote', 'Hybrid', 'On-site', 'Flexible']
    
    # Benefits
    benefits_list = [
        'Health Insurance', '401k', 'Remote Work', 'Stock Options', 'Learning Stipend', 
        'Gym Membership', 'Free Lunch', 'Unlimited PTO', 'Parental Leave', 'Tuition Reimbursement'
    ]
    
    # Generate records
    records = []
    
    for i in range(n_records):
        # Select job title
        job_title = random.choice(job_titles)
        
        # Determine experience level based on role seniority
        if 'Senior' in job_title or 'Lead' in job_title or 'Principal' in job_title or 'Manager' in job_title:
            exp_years = random.randint(5, 12)
            level = random.choice(['Senior', 'Lead', 'Manager', 'Principal'])
        elif 'Junior' in job_title:
            exp_years = random.randint(0, 2)
            level = 'Junior'
        else:
            exp_years = random.randint(2, 7)
            level = random.choice(['Mid', 'Senior'])
        
        # Select 3-6 skills for this job
        num_skills = random.randint(3, 6)
        job_skills = random.sample(all_skills, num_skills)
        skill_required = ', '.join(job_skills)
        
        # Determine skill category (primary)
        primary_skill = job_skills[0]
        skill_category = 'Technology'
        for category, skills in skills_list.items():
            if primary_skill in skills:
                skill_category = category
                break
        
        # Salary based on role, skills, location, experience
        base_salary = 60000
        
        # Role multiplier
        role_multipliers = {
            'Data Analyst': 1.0, 'Business Analyst': 0.95, 'Marketing Analyst': 0.92,
            'Data Scientist': 1.4, 'ML Engineer': 1.5, 'AI Research Scientist': 1.55,
            'Data Engineer': 1.3, 'Data Architect': 1.45, 'Analytics Manager': 1.35,
            'Data Product Manager': 1.4, 'Computer Vision Engineer': 1.48, 'NLP Engineer': 1.47
        }
        role_mult = role_multipliers.get(job_title, 1.1)
        
        # Skill premium
        skill_premium = 1.0
        high_value_skills = ['Machine Learning', 'Deep Learning', 'TensorFlow', 'PyTorch', 'Spark', 'AWS', 'Kubernetes']
        for skill in job_skills:
            if skill in high_value_skills:
                skill_premium += 0.05
        
        # Location multiplier
        location_multipliers = {
            'San Francisco': 1.45, 'New York': 1.4, 'Seattle': 1.35, 'Boston': 1.3,
            'Los Angeles': 1.25, 'Washington DC': 1.25, 'Austin': 1.2, 'Chicago': 1.15,
            'Denver': 1.1, 'Atlanta': 1.05, 'Dallas': 1.05, 'Miami': 1.02
        }
        loc_mult = location_multipliers.get(random.choice(locations), 1.0)
        
        # Experience multiplier
        exp_mult = 1 + (exp_years * 0.03)
        
        # Calculate salary
        avg_salary = base_salary * role_mult * skill_premium * loc_mult * exp_mult
        min_salary = int(avg_salary * 0.85)
        max_salary = int(avg_salary * 1.15)
        avg_salary = int(avg_salary)
        
        # Demand score (influenced by skills and role)
        base_demand = random.randint(65, 95)
        if 'Machine Learning' in skill_required or 'Deep Learning' in skill_required:
            base_demand += 10
        if 'Cloud' in skill_category or 'Big Data' in skill_category:
            base_demand += 5
        demand_score = min(100, base_demand + random.randint(-5, 10))
        
        # Remote policy
        remote_policy = random.choice(remote_policies)
        is_remote_friendly = 1 if remote_policy in ['Remote', 'Hybrid', 'Flexible'] else 0
        
        # Select 2-3 random benefits
        num_benefits = random.randint(2, 4)
        benefits = ', '.join(random.sample(benefits_list, num_benefits))
        
        record = {
            'job_id': i + 1,
            'job_title': job_title,
            'level': level,
            'company': f"Company_{random.choice(['Tech', 'Data', 'Cloud', 'AI', 'Analytics', 'Digital'])}{random.randint(1, 100)}",
            'location': random.choice(locations),
            'skill_required': skill_required,
            'skill_category': skill_category,
            'primary_skill': primary_skill,
            'num_skills': num_skills,
            'min_salary': min_salary,
            'max_salary': max_salary,
            'avg_salary': avg_salary,
            'experience_years': exp_years,
            'experience_level': level,
            'industry': random.choice(industries),
            'company_size': random.choice(company_sizes),
            'education_required': random.choice(education),
            'remote_policy': remote_policy,
            'is_remote_friendly': is_remote_friendly,
            'demand_score': demand_score,
            'posted_days_ago': random.randint(1, 30),
            'applicants_count': random.randint(5, 200),
            'benefits': benefits
        }
        records.append(record)
    
    df = pd.DataFrame(records)
    
    # Add derived columns
    df['salary_per_year'] = df['avg_salary']
    
    print(f"✅ Generated {len(df)} job records")
    print(f"   Unique Jobs: {df['job_title'].nunique()}")
    print(f"   Unique Skills: {df['skill_required'].nunique()}")
    print(f"   Unique Locations: {df['location'].nunique()}")
    print(f"   Salary Range: ${df['min_salary'].min():,} - ${df['max_salary'].max():,}")
    print(f"   Columns: {list(df.columns)}")
    
    return df

if __name__ == "__main__":
    # Generate dataset
    df = generate_large_dataset(500)
    
    # Save to CSV
    df.to_csv('data/raw/job_market_data.csv', index=False)
    print(f"\n💾 Saved to: data/raw/job_market_data.csv")
    
    # Display sample
    print("\n📋 Sample Records:")
    print(df[['job_title', 'skill_required', 'avg_salary', 'location', 'demand_score', 'remote_policy']].head(10))
    
    # Statistics
    print("\n📊 Dataset Statistics:")
    print(f"   Total Records: {len(df)}")
    print(f"   Average Salary: ${df['avg_salary'].mean():,.0f}")
    print(f"   Top Location: {df['location'].mode()[0]}")
    print(f"   Remote Friendly Jobs: {df['is_remote_friendly'].sum()} ({df['is_remote_friendly'].mean()*100:.1f}%)")