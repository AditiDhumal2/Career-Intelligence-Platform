"""
Update Dataset Demand Scores
Makes demand scores more realistic for better skill prioritization
"""

import pandas as pd
import random

def update_demand_scores():
    """Update demand scores in the dataset to realistic values"""
    
    print("="*60)
    print("UPDATING DATASET DEMAND SCORES")
    print("="*60)
    
    # Load existing data
    df = pd.read_csv('data/raw/job_market_data.csv')
    
    print(f"\n📊 Original Dataset:")
    print(f"   Records: {len(df)}")
    print(f"   Demand Score Range: {df['demand_score'].min()} - {df['demand_score'].max()}")
    print(f"   Average Demand: {df['demand_score'].mean():.1f}")
    
    # Define realistic demand scores for key skills
    skill_demand_map = {
        # Programming Languages
        'Python': 95, 'SQL': 92, 'R': 82, 'Java': 80, 'Scala': 78, 'Julia': 75,
        'JavaScript': 76, 'C++': 74,
        
        # ML/AI (Highest Demand)
        'Machine Learning': 98, 'Deep Learning': 96, 'TensorFlow': 94, 'PyTorch': 93,
        'Scikit-Learn': 92, 'Keras': 91, 'NLP': 91, 'LLM': 94, 'Computer Vision': 90,
        
        # Data Analysis
        'Statistics': 85, 'Excel': 88, 'Data Visualization': 89, 'Probability': 82,
        'Linear Algebra': 80,
        
        # BI Tools
        'Tableau': 87, 'Power BI': 86, 'Looker': 82, 'QlikView': 78,
        
        # Cloud & DevOps
        'AWS': 90, 'Azure': 87, 'GCP': 86, 'Docker': 89, 'Kubernetes': 88,
        'Terraform': 84, 'Jenkins': 82,
        
        # Big Data
        'Spark': 91, 'Hadoop': 85, 'Kafka': 87, 'Airflow': 87, 'Flink': 82,
        
        # Databases
        'PostgreSQL': 84, 'MySQL': 83, 'MongoDB': 82, 'Cassandra': 78,
        'Redis': 77, 'Elasticsearch': 79,
        
        # Soft Skills (High demand but hard to measure)
        'Communication': 92, 'Leadership': 88, 'Project Management': 86,
        'Problem Solving': 90, 'Teamwork': 85, 'Agile': 84, 'Storytelling': 82,
        
        # Data Engineering
        'ETL': 88, 'Data Warehousing': 86, 'Data Modeling': 85,
    }
    
    # Update demand scores
    def get_demand_score(row):
        """Get demand score based on skills in the row"""
        skill_required = str(row['skill_required']) if pd.notna(row['skill_required']) else ''
        primary_skill = str(row['primary_skill']) if pd.notna(row['primary_skill']) else ''
        job_title = str(row['job_title']) if pd.notna(row['job_title']) else ''
        
        # Check all skills in skill_required
        highest_score = 75  # Default minimum
        
        for skill, demand in skill_demand_map.items():
            if skill.lower() in skill_required.lower() or skill.lower() in primary_skill.lower():
                highest_score = max(highest_score, demand)
        
        # Boost for specific job titles
        if 'Data Scientist' in job_title or 'ML Engineer' in job_title:
            highest_score = min(highest_score + 5, 100)
        elif 'Data Engineer' in job_title:
            highest_score = min(highest_score + 3, 100)
        
        # Add some randomness (±3)
        highest_score += random.randint(-3, 3)
        return min(max(highest_score, 70), 98)  # Keep between 70-98
    
    # Apply update
    df['demand_score'] = df.apply(get_demand_score, axis=1)
    
    print(f"\n✅ Updated Demand Scores:")
    print(f"   New Range: {df['demand_score'].min()} - {df['demand_score'].max()}")
    print(f"   New Average: {df['demand_score'].mean():.1f}")
    
    # Show sample of updated scores
    print(f"\n📋 Sample of Updated Demand Scores:")
    sample_cols = ['job_title', 'primary_skill', 'demand_score']
    print(df[sample_cols].head(15).to_string())
    
    # Save updated data
    df.to_csv('data/raw/job_market_data.csv', index=False)
    print(f"\n💾 Saved updated dataset to: data/raw/job_market_data.csv")
    
    # Show statistics by skill category
    print(f"\n📊 Demand Score by Skill Category:")
    
    # Define categories
    categories = {
        'ML/AI': ['Machine Learning', 'Deep Learning', 'TensorFlow', 'PyTorch', 'Scikit-Learn', 'NLP', 'LLM'],
        'Programming': ['Python', 'SQL', 'R', 'Java', 'Scala'],
        'Cloud/DevOps': ['AWS', 'Azure', 'Docker', 'Kubernetes', 'Terraform'],
        'Big Data': ['Spark', 'Hadoop', 'Kafka', 'Airflow'],
        'BI/Visualization': ['Tableau', 'Power BI', 'Data Visualization'],
        'Soft Skills': ['Communication', 'Leadership', 'Project Management']
    }
    
    for category, skills in categories.items():
        category_scores = []
        for skill in skills:
            skill_data = df[df['skill_required'].str.contains(skill, case=False, na=False)]
            if len(skill_data) > 0:
                avg_score = skill_data['demand_score'].mean()
                category_scores.append(avg_score)
        if category_scores:
            avg_cat = sum(category_scores) / len(category_scores)
            print(f"   {category}: {avg_cat:.1f}/100")
    
    print("\n" + "="*60)
    print("✅ Update Complete! Run 'python src/data_loader.py' to refresh processed data")
    print("="*60)
    
    return df

if __name__ == "__main__":
    update_demand_scores()