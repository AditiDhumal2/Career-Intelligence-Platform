"""
Export data for Power BI Dashboard
Run this to prepare data for Power BI visualization
"""

import pandas as pd
from pathlib import Path
from src.data_loader import DataLoader

def export_for_powerbi():
    """Export cleaned data to Excel for Power BI"""
    
    print("="*60)
    print("EXPORTING DATA FOR POWER BI")
    print("="*60)
    
    # Load data
    loader = DataLoader()
    df = loader.load_data()
    df_clean = loader.clean_data(df)
    
    # Create processed folder if it doesn't exist
    output_path = Path('data/processed/job_market_data_powerbi.xlsx')
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Save to Excel
    df_clean.to_excel(output_path, index=False)
    
    print(f"\n✅ Data exported successfully!")
    print(f"📁 Location: {output_path.absolute()}")
    print(f"📊 Rows: {len(df_clean)}")
    print(f"📋 Columns: {list(df_clean.columns)}")
    
    # Display preview
    print("\n📋 Data Preview:")
    print(df_clean[['job_title', 'skill_required', 'avg_salary', 'location']].head())
    
    print("\n" + "="*60)
    print("You can now import this file into Power BI!")
    print("="*60)
    
    return df_clean

if __name__ == "__main__":
    export_for_powerbi()