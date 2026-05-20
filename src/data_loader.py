"""
Data Loader Module
Purpose: Load and clean job market data
"""

import pandas as pd
import numpy as np
from pathlib import Path

class DataLoader:
    """
    Handles loading and preprocessing of job market data
    """
    
    def __init__(self):
        """Initialize with paths"""
        # Get the project root directory (where this file is located)
        self.project_root = Path(__file__).parent.parent
        self.raw_data_path = self.project_root / 'data' / 'raw' / 'job_market_data.csv'
        self.processed_data_path = self.project_root / 'data' / 'processed' / 'cleaned_job_data.csv'
        
    def load_data(self):
        """
        Load raw CSV data
        
        Returns:
            pandas DataFrame: Loaded data
        """
        print(f"Loading data from: {self.raw_data_path}")
        
        # Check if file exists
        if not self.raw_data_path.exists():
            raise FileNotFoundError(f"Data file not found at {self.raw_data_path}")
        
        # Load CSV file
        df = pd.read_csv(self.raw_data_path)
        
        print(f"✅ Loaded {len(df)} records")
        print(f"📊 Columns: {list(df.columns)}")
        
        return df
    
    def clean_data(self, df):
        """
        Clean and preprocess the data
        
        Args:
            df (pandas DataFrame): Raw data
            
        Returns:
            pandas DataFrame: Cleaned data
        """
        print("\n🔄 Cleaning data...")
        
        # Make a copy to avoid modifying original
        df_clean = df.copy()
        
        # 1. Remove any duplicate rows
        duplicates = df_clean.duplicated().sum()
        if duplicates > 0:
            df_clean = df_clean.drop_duplicates()
            print(f"   Removed {duplicates} duplicate rows")
        
        # 2. Check for missing values
        print(f"   Missing values before cleaning:\n{df_clean.isnull().sum()}")
        
        # 3. Fill missing values (if any)
        # For numeric columns, fill with median
        numeric_cols = df_clean.select_dtypes(include=[np.number]).columns
        df_clean[numeric_cols] = df_clean[numeric_cols].fillna(df_clean[numeric_cols].median())
        
        # For categorical columns, fill with mode (most frequent value)
        # Fixed: Include both 'object' and 'string' types to avoid warning
        categorical_cols = df_clean.select_dtypes(include=['object', 'string']).columns
        for col in categorical_cols:
            df_clean[col] = df_clean[col].fillna(df_clean[col].mode()[0] if not df_clean[col].mode().empty else 'Unknown')
        
        # 4. Create additional calculated columns
        # Average salary
        df_clean['avg_salary'] = (df_clean['min_salary'] + df_clean['max_salary']) / 2
        
        # Salary range (for analysis)
        df_clean['salary_range'] = df_clean['max_salary'] - df_clean['min_salary']
        
        print(f"✅ Data cleaned successfully")
        print(f"   Final shape: {df_clean.shape}")
        
        return df_clean
    
    def save_processed_data(self, df):
        """
        Save cleaned data to processed folder
        
        Args:
            df (pandas DataFrame): Cleaned data
        """
        # Create processed directory if it doesn't exist
        self.processed_data_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save to CSV
        df.to_csv(self.processed_data_path, index=False)
        print(f"\n💾 Saved cleaned data to: {self.processed_data_path}")
        
    def get_summary_stats(self, df):
        """
        Get summary statistics of the data
        
        Args:
            df (pandas DataFrame): Cleaned data
            
        Returns:
            dict: Summary statistics
        """
        summary = {
            'total_jobs': len(df),
            'unique_job_titles': df['job_title'].nunique(),
            'unique_companies': df['company'].nunique(),
            'unique_skills': df['skill_required'].nunique(),
            'avg_salary_overall': df['avg_salary'].mean(),
            'salary_range': (df['min_salary'].min(), df['max_salary'].max()),
            'top_locations': df['location'].value_counts().head(3).to_dict(),
            'top_skills': df['skill_required'].value_counts().head(5).to_dict()
        }
        
        return summary

# Test the code when run directly
if __name__ == "__main__":
    print("=" * 60)
    print("TESTING DATA LOADER MODULE")
    print("=" * 60)
    
    # Create instance
    loader = DataLoader()
    
    # Load data
    df = loader.load_data()
    
    # Clean data
    df_clean = loader.clean_data(df)
    
    # Get summary statistics
    summary = loader.get_summary_stats(df_clean)
    
    print("\n📈 SUMMARY STATISTICS:")
    for key, value in summary.items():
        print(f"   {key}: {value}")
    
    # Save processed data
    loader.save_processed_data(df_clean)
    
    print("\n" + "=" * 60)
    print("✅ DataLoader module is working correctly!")
    print("=" * 60)