"""
Machine Learning Salary Predictor
Predicts salary based on skills, location, and experience
This demonstrates ML skills - highly valued at UIUC
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error, r2_score
import joblib
from pathlib import Path

class SalaryPredictor:
    """
    ML model to predict salaries based on job characteristics
    """
    
    def __init__(self):
        self.model = None
        self.label_encoders = {}
        self.feature_columns = None
        
    def prepare_features(self, df):
        """
        Prepare features for ML model
        
        Args:
            df: DataFrame with job data
            
        Returns:
            X: Features, y: Target (salary)
        """
        # Select features for prediction
        feature_cols = ['skill_required', 'location', 'industry', 'experience_years', 'demand_score']
        
        # Create feature matrix
        X = df[feature_cols].copy()
        y = df['avg_salary'].copy()
        
        # Encode categorical variables
        for col in ['skill_required', 'location', 'industry']:
            le = LabelEncoder()
            X[col] = le.fit_transform(X[col])
            self.label_encoders[col] = le
        
        self.feature_columns = feature_cols
        return X, y
    
    def train_model(self, df):
        """
        Train Random Forest model for salary prediction
        
        Returns:
            dict: Model performance metrics
        """
        print("🤖 Training Salary Prediction Model...")
        
        # Prepare features
        X, y = self.prepare_features(df)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Train Random Forest model
        self.model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            n_jobs=-1
        )
        self.model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        # Feature importance
        feature_importance = dict(zip(
            self.feature_columns,
            self.model.feature_importances_
        ))
        
        print(f"✅ Model trained! R² Score: {r2:.3f}")
        print(f"📊 Mean Absolute Error: ${mae:,.0f}")
        
        return {
            'r2_score': r2,
            'mae': mae,
            'feature_importance': feature_importance
        }
    
    def predict_salary(self, skill, location, industry, experience_years, demand_score):
        """
        Predict salary for given parameters
        
        Args:
            skill: Skill name (e.g., 'Python')
            location: City name (e.g., 'New York')
            industry: Industry (e.g., 'Technology')
            experience_years: Years of experience
            demand_score: Market demand score (0-100)
            
        Returns:
            dict: Predicted salary and confidence interval
        """
        if self.model is None:
            return {'error': 'Model not trained yet'}
        
        # Encode categorical variables
        try:
            skill_encoded = self.label_encoders['skill_required'].transform([skill])[0]
            location_encoded = self.label_encoders['location'].transform([location])[0]
            industry_encoded = self.label_encoders['industry'].transform([industry])[0]
        except ValueError as e:
            return {'error': f'Unknown value: {e}'}
        
        # Create feature array
        features = np.array([[
            skill_encoded, location_encoded, industry_encoded,
            experience_years, demand_score
        ]])
        
        # Predict
        predicted_salary = self.model.predict(features)[0]
        
        # Calculate confidence (based on model's tree variance)
        # Simple heuristic: ±10% for demo
        confidence_low = predicted_salary * 0.9
        confidence_high = predicted_salary * 1.1
        
        return {
            'predicted_salary': round(predicted_salary, 2),
            'confidence_range': [round(confidence_low, 2), round(confidence_high, 2)],
            'input_parameters': {
                'skill': skill,
                'location': location,
                'industry': industry,
                'experience_years': experience_years,
                'demand_score': demand_score
            }
        }
    
    def save_model(self, path='models/salary_predictor.pkl'):
        """Save trained model"""
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        joblib.dump({
            'model': self.model,
            'encoders': self.label_encoders,
            'features': self.feature_columns
        }, path)
        print(f"💾 Model saved to {path}")
    
    def load_model(self, path='models/salary_predictor.pkl'):
        """Load trained model"""
        data = joblib.load(path)
        self.model = data['model']
        self.label_encoders = data['encoders']
        self.feature_columns = data['features']
        print(f"📂 Model loaded from {path}")


# Test the module
if __name__ == "__main__":
    from data_loader import DataLoader
    
    # Load data
    loader = DataLoader()
    df = loader.load_data()
    df_clean = loader.clean_data(df)
    
    # Train model
    predictor = SalaryPredictor()
    metrics = predictor.train_model(df_clean)
    
    print("\n🎯 Feature Importance:")
    for feature, importance in sorted(metrics['feature_importance'].items(), key=lambda x: x[1], reverse=True):
        print(f"   {feature}: {importance:.3f}")
    
    # Test prediction
    print("\n🔮 Sample Salary Prediction:")
    prediction = predictor.predict_salary(
        skill='Python',
        location='New York',
        industry='Technology',
        experience_years=3,
        demand_score=85
    )
    print(f"   Predicted Salary: ${prediction['predicted_salary']:,.0f}")
    print(f"   Confidence Range: ${prediction['confidence_range'][0]:,.0f} - ${prediction['confidence_range'][1]:,.0f}")