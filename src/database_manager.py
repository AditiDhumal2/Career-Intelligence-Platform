"""
Database Manager - SQLite/PostgreSQL Integration
Shows database skills - critical for MSIM
"""

import sqlite3
import pandas as pd
from pathlib import Path
from contextlib import contextmanager

class DatabaseManager:
    """
    Manages database operations for job market data
    Demonstrates SQL and database design skills
    """
    
    def __init__(self, db_path='data/career_intelligence.db'):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database with schema"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Create jobs table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS jobs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    job_title TEXT NOT NULL,
                    company TEXT,
                    location TEXT,
                    skill_required TEXT,
                    min_salary INTEGER,
                    max_salary INTEGER,
                    avg_salary REAL,
                    experience_years INTEGER,
                    industry TEXT,
                    demand_score INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create skills table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS skills (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    skill_name TEXT UNIQUE,
                    category TEXT,
                    demand_score REAL,
                    avg_salary REAL
                )
            ''')
            
            # Create user_queries table (tracking user interests)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_queries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT,
                    user_skills TEXT,
                    target_role TEXT,
                    match_percentage REAL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            print("✅ Database initialized successfully")
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
        finally:
            conn.close()
    
    def insert_jobs(self, df):
        """Insert job data into database"""
        with self.get_connection() as conn:
            df.to_sql('jobs', conn, if_exists='replace', index=False)
            print(f"✅ Inserted {len(df)} jobs into database")
    
    def get_top_skills_sql(self, limit=10):
        """Get top skills using SQL query"""
        query = '''
            SELECT 
                skill_required,
                COUNT(*) as job_count,
                AVG(demand_score) as avg_demand,
                AVG(avg_salary) as avg_salary
            FROM jobs
            GROUP BY skill_required
            ORDER BY job_count DESC
            LIMIT ?
        '''
        with self.get_connection() as conn:
            return pd.read_sql_query(query, conn, params=[limit])
    
    def get_salary_by_location_sql(self):
        """Get salary statistics by location"""
        query = '''
            SELECT 
                location,
                COUNT(*) as job_count,
                AVG(avg_salary) as avg_salary,
                MIN(min_salary) as min_salary,
                MAX(max_salary) as max_salary
            FROM jobs
            GROUP BY location
            ORDER BY avg_salary DESC
        '''
        with self.get_connection() as conn:
            return pd.read_sql_query(query, conn)
    
    def search_jobs_sql(self, skill=None, location=None, min_salary=None):
        """Search jobs with filters using SQL"""
        query = "SELECT * FROM jobs WHERE 1=1"
        params = []
        
        if skill:
            query += " AND skill_required = ?"
            params.append(skill)
        if location:
            query += " AND location = ?"
            params.append(location)
        if min_salary:
            query += " AND avg_salary >= ?"
            params.append(min_salary)
        
        query += " LIMIT 50"
        
        with self.get_connection() as conn:
            return pd.read_sql_query(query, conn, params=params)
    
    def log_user_query(self, session_id, user_skills, target_role, match_percentage):
        """Log user queries for analytics"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO user_queries (session_id, user_skills, target_role, match_percentage)
                VALUES (?, ?, ?, ?)
            ''', (session_id, user_skills, target_role, match_percentage))
            conn.commit()
    
    def get_query_analytics(self):
        """Get analytics on user queries"""
        query = '''
            SELECT 
                target_role,
                COUNT(*) as query_count,
                AVG(match_percentage) as avg_match,
                DATE(timestamp) as query_date
            FROM user_queries
            GROUP BY target_role, DATE(timestamp)
            ORDER BY query_date DESC
            LIMIT 20
        '''
        with self.get_connection() as conn:
            return pd.read_sql_query(query, conn)


# Test the module
if __name__ == "__main__":
    from data_loader import DataLoader
    
    # Initialize database
    db = DatabaseManager()
    
    # Load and insert data
    loader = DataLoader()
    df = loader.load_data()
    df_clean = loader.clean_data(df)
    db.insert_jobs(df_clean)
    
    # Test queries
    print("\n📊 Top Skills (SQL Query):")
    print(db.get_top_skills_sql(5))
    
    print("\n📍 Salary by Location:")
    print(db.get_salary_by_location_sql())