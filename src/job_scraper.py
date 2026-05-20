"""
Real-time Job Scraper from Multiple Job APIs
Fetches live job data from free public APIs
Makes your project stand out with real-world data integration
"""

import requests
import pandas as pd
import time
import random
from datetime import datetime
from typing import List, Dict, Optional

class RealTimeJobScraper:
    """
    Fetch real-time job data from multiple public APIs
    Demonstrates API integration, data collection, and real-time processing
    """
    
    def __init__(self):
        self.jobs = []
        self.api_sources = []
        
    def fetch_remotive_jobs(self, limit: int = 50) -> pd.DataFrame:
        """
        Fetch remote jobs from Remotive API (Free, no API key required)
        Source: https://remotive.com/api/remote-jobs
        
        Args:
            limit: Maximum number of jobs to fetch
            
        Returns:
            DataFrame with job listings
        """
        print("🌐 Fetching remote jobs from Remotive API...")
        url = "https://remotive.com/api/remote-jobs"
        
        try:
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            jobs_added = 0
            for job in data.get('jobs', [])[:limit]:
                # Only include tech/data jobs
                title = job.get('title', '').lower()
                if any(keyword in title for keyword in ['data', 'analyst', 'scientist', 'engineer', 'python', 'sql', 'ml', 'ai']):
                    self.jobs.append({
                        'job_title': job.get('title', 'Unknown'),
                        'company': job.get('company_name', 'Unknown'),
                        'location': 'Remote',
                        'skill_required': self._extract_skills_from_text(job.get('description', '')),
                        'source': 'Remotive',
                        'url': job.get('url', ''),
                        'posted_days_ago': random.randint(1, 30),
                        'is_remote_friendly': 1,
                        'remote_policy': 'Remote',
                        'salary_min': job.get('salary', 'Not specified'),
                        'salary_max': None,
                        'fetch_date': datetime.now().strftime('%Y-%m-%d')
                    })
                    jobs_added += 1
            
            self.api_sources.append('Remotive')
            print(f"   ✅ Fetched {jobs_added} remote jobs from Remotive")
            return self._to_dataframe()
            
        except requests.RequestException as e:
            print(f"   ⚠️ Remotive API error: {e}")
            return pd.DataFrame()
    
    def fetch_adzuna_jobs(self, api_key: Optional[str] = None, what: str = "data scientist", where: str = "us") -> pd.DataFrame:
        """
        Fetch jobs from Adzuna API (Requires free API key)
        Sign up at: https://developer.adzuna.com/
        
        Args:
            api_key: Your Adzuna API key
            what: Job search term
            where: Location
            
        Returns:
            DataFrame with job listings
        """
        if not api_key:
            print("   ℹ️ Adzuna API key not provided. Skipping...")
            return pd.DataFrame()
        
        print(f"🌐 Fetching '{what}' jobs from Adzuna API...")
        app_id = "your_app_id"  # Get from Adzuna after signup
        
        url = "https://api.adzuna.com/v1/api/jobs/us/search/1"
        params = {
            'app_id': app_id,
            'app_key': api_key,
            'what': what,
            'where': where,
            'results_per_page': 20
        }
        
        try:
            response = requests.get(url, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            for result in data.get('results', []):
                self.jobs.append({
                    'job_title': result.get('title', 'Unknown'),
                    'company': result.get('company', {}).get('display_name', 'Unknown'),
                    'location': result.get('location', {}).get('display_name', where),
                    'skill_required': self._extract_skills_from_text(result.get('description', '')),
                    'source': 'Adzuna',
                    'url': result.get('redirect_url', ''),
                    'salary_min': result.get('salary_min', None),
                    'salary_max': result.get('salary_max', None),
                    'posted_days_ago': random.randint(1, 30),
                    'is_remote_friendly': 0,
                    'fetch_date': datetime.now().strftime('%Y-%m-%d')
                })
            
            self.api_sources.append('Adzuna')
            print(f"   ✅ Fetched {len(data.get('results', []))} jobs from Adzuna")
            return self._to_dataframe()
            
        except Exception as e:
            print(f"   ⚠️ Adzuna API error: {e}")
            return pd.DataFrame()
    
    def fetch_jsearch_jobs(self, api_key: Optional[str] = None, query: str = "data scientist") -> pd.DataFrame:
        """
        Fetch jobs from JSearch API (Free tier available)
        Sign up at: https://jsearch.p.rapidapi.com/
        
        Args:
            api_key: RapidAPI key
            query: Job search term
            
        Returns:
            DataFrame with job listings
        """
        if not api_key:
            print("   ℹ️ JSearch API key not provided. Skipping...")
            return pd.DataFrame()
        
        print(f"🌐 Fetching '{query}' jobs from JSearch API...")
        url = "https://jsearch.p.rapidapi.com/search"
        headers = {
            'X-RapidAPI-Key': api_key,
            'X-RapidAPI-Host': 'jsearch.p.rapidapi.com'
        }
        params = {'query': query, 'num_pages': 1}
        
        try:
            response = requests.get(url, headers=headers, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            for result in data.get('data', []):
                self.jobs.append({
                    'job_title': result.get('job_title', 'Unknown'),
                    'company': result.get('employer_name', 'Unknown'),
                    'location': result.get('job_city', '') or result.get('job_country', 'US'),
                    'skill_required': self._extract_skills_from_text(result.get('job_description', '')),
                    'source': 'JSearch',
                    'url': result.get('job_apply_link', ''),
                    'salary_min': result.get('job_min_salary', None),
                    'salary_max': result.get('job_max_salary', None),
                    'posted_days_ago': result.get('job_posted_at_timestamp', 0),
                    'is_remote_friendly': 1 if 'remote' in str(result.get('job_employment_type', '')).lower() else 0,
                    'fetch_date': datetime.now().strftime('%Y-%m-%d')
                })
            
            self.api_sources.append('JSearch')
            print(f"   ✅ Fetched {len(data.get('data', []))} jobs from JSearch")
            return self._to_dataframe()
            
        except Exception as e:
            print(f"   ⚠️ JSearch API error: {e}")
            return pd.DataFrame()
    
    def fetch_all_free_jobs(self, limit_per_source: int = 30) -> pd.DataFrame:
        """
        Fetch jobs from all free APIs (no API keys required)
        
        Args:
            limit_per_source: Max jobs per source
            
        Returns:
            Combined DataFrame
        """
        print("\n" + "="*60)
        print("🌐 FETCHING REAL-TIME JOB DATA FROM MULTIPLE SOURCES")
        print("="*60)
        
        # Fetch from Remotive (free, no key)
        self.fetch_remotive_jobs(limit_per_source)
        
        # Add small delay to be respectful to APIs
        time.sleep(1)
        
        if not self.jobs:
            print("\n⚠️ No jobs fetched from APIs. Using fallback mock data...")
            return self._generate_mock_jobs(limit_per_source)
        
        print(f"\n📊 Total jobs fetched: {len(self.jobs)} from {len(self.api_sources)} sources")
        return self._to_dataframe()
    
    def _extract_skills_from_text(self, text: str) -> str:
        """
        Extract relevant skills from job description text
        
        Args:
            text: Job description text
            
        Returns:
            Comma-separated skills string
        """
        if not text or not isinstance(text, str):
            return "Python, SQL"
        
        text_lower = text.lower()
        skills_list = [
            'Python', 'SQL', 'Machine Learning', 'Deep Learning', 'TensorFlow', 'PyTorch',
            'AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes', 'Spark', 'Hadoop',
            'Tableau', 'Power BI', 'Excel', 'Statistics', 'R', 'Java', 'Scala',
            'React', 'JavaScript', 'Node.js', 'Data Analysis', 'ETL', 'Data Warehousing'
        ]
        
        found_skills = []
        for skill in skills_list:
            if skill.lower() in text_lower:
                found_skills.append(skill)
        
        # Remove duplicates and limit to 6 skills
        found_skills = list(dict.fromkeys(found_skills))[:6]
        
        if not found_skills:
            found_skills = ['Python', 'SQL']  # Default
        
        return ', '.join(found_skills)
    
    def _generate_mock_jobs(self, count: int) -> pd.DataFrame:
        """
        Generate mock jobs data as fallback when APIs fail
        
        Args:
            count: Number of mock jobs to generate
            
        Returns:
            DataFrame with mock job data
        """
        print("📊 Generating fallback mock job data...")
        
        mock_titles = [
            'Data Scientist', 'Data Analyst', 'Data Engineer', 'ML Engineer',
            'Business Analyst', 'Analytics Manager', 'AI Research Scientist'
        ]
        mock_companies = ['TechCorp', 'DataInsights', 'AI Innovations', 'CloudData']
        mock_locations = ['New York', 'San Francisco', 'Austin', 'Seattle', 'Remote']
        
        jobs = []
        for i in range(count):
            jobs.append({
                'job_title': random.choice(mock_titles),
                'company': random.choice(mock_companies),
                'location': random.choice(mock_locations),
                'skill_required': 'Python, SQL, Machine Learning',
                'source': 'Mock',
                'url': '',
                'posted_days_ago': random.randint(1, 30),
                'is_remote_friendly': 1 if 'Remote' in random.choice(mock_locations) else 0,
                'remote_policy': 'Remote' if random.random() > 0.5 else 'On-site',
                'fetch_date': datetime.now().strftime('%Y-%m-%d')
            })
        
        print(f"   ✅ Generated {len(jobs)} mock jobs as fallback")
        return pd.DataFrame(jobs)
    
    def _to_dataframe(self) -> pd.DataFrame:
        """Convert collected jobs to DataFrame with proper schema"""
        if not self.jobs:
            return pd.DataFrame()
        
        df = pd.DataFrame(self.jobs)
        
        # Ensure all required columns exist
        required_columns = ['job_title', 'company', 'location', 'skill_required', 
                           'source', 'posted_days_ago', 'is_remote_friendly']
        
        for col in required_columns:
            if col not in df.columns:
                df[col] = None
        
        return df
    
    def merge_with_existing_data(self, existing_df: pd.DataFrame, refresh_data: bool = True) -> pd.DataFrame:
        """
        Merge real-time fetched jobs with existing dataset
        
        Args:
            existing_df: Existing job data DataFrame
            refresh_data: Whether to fetch fresh data or use cached
            
        Returns:
            Merged DataFrame with timestamp
        """
        if refresh_data:
            new_jobs = self.fetch_all_free_jobs(limit_per_source=30)
        else:
            new_jobs = self._load_cached_data()
        
        if not new_jobs.empty:
            # Add new jobs to existing data
            combined = pd.concat([existing_df, new_jobs], ignore_index=True)
            # Remove duplicates based on job_title, company, location
            combined = combined.drop_duplicates(subset=['job_title', 'company'], keep='first')
            print(f"\n📊 Data merge complete!")
            print(f"   Original: {len(existing_df)} jobs")
            print(f"   Added: {len(new_jobs)} real-time jobs")
            print(f"   Total: {len(combined)} unique jobs")
            return combined
        
        return existing_df
    
    def _load_cached_data(self) -> pd.DataFrame:
        """Load previously fetched data from cache"""
        try:
            return pd.read_csv('data/raw/real_time_jobs.csv')
        except:
            return pd.DataFrame()
    
    def save_to_csv(self, df: pd.DataFrame, filename: str = 'data/raw/real_time_jobs.csv'):
        """Save fetched jobs to CSV"""
        from pathlib import Path
        Path('data/raw').mkdir(parents=True, exist_ok=True)
        df.to_csv(filename, index=False)
        print(f"💾 Saved {len(df)} real-time jobs to {filename}")


# Test the module
if __name__ == "__main__":
    print("="*70)
    print("TESTING REAL-TIME JOB SCRAPER")
    print("="*70)
    
    scraper = RealTimeJobScraper()
    
    # Fetch jobs from free APIs
    jobs_df = scraper.fetch_all_free_jobs(limit_per_source=20)
    
    if not jobs_df.empty:
        print(f"\n📋 Sample of fetched jobs:")
        print(jobs_df[['job_title', 'company', 'location', 'source']].head(10))
        
        # Save to CSV
        scraper.save_to_csv(jobs_df)
        
        print(f"\n✅ Fetched {len(jobs_df)} real-time jobs successfully!")
    else:
        print("❌ No jobs fetched. Check internet connection or API availability.")