"""
LLM-Powered Career Advisor using Gemini API (FREE)
"""

import os
from typing import List, Dict

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ .env file loaded")
except ImportError:
    print("⚠️ python-dotenv not installed")

# Try to import google.genai
try:
    from google import genai
    GENAI_AVAILABLE = True
    print("✅ google-genai available")
except ImportError:
    GENAI_AVAILABLE = False
    print("⚠️ google-genai not installed. Install with: pip install google-genai")

class LLMCareerAdvisor:
    """
    AI-powered career advisor using Google Gemini (FREE)
    """
    
    def __init__(self):
        """Initialize Gemini client"""
        self.client = None
        self.model = "gemini-2.0-flash-exp"
        
        if not GENAI_AVAILABLE:
            print("⚠️ Gemini SDK not available. Using fallback mode.")
            return
        
        # Get API key from environment
        api_key = os.getenv('GEMINI_API_KEY')
        
        if not api_key:
            print("⚠️ GEMINI_API_KEY not found in .env file.")
            print("   Please create a .env file with: GEMINI_API_KEY=your_key_here")
            return
        
        try:
            self.client = genai.Client(api_key=api_key)
            print("✅ Gemini initialized successfully!")
        except Exception as e:
            print(f"⚠️ Gemini init failed: {e}")
            self.client = None
    
    def get_career_advice(self, user_skills: List[str], target_role: str) -> Dict:
        """Get personalized career advice"""
        
        # If no client, use fallback
        if not self.client:
            return self._get_fallback_response(user_skills, target_role)
        
        # Build prompt
        skills_text = ', '.join(user_skills) if user_skills else 'None specified'
        
        prompt = f"""
        You are a career advisor with expertise in data science and analytics careers.
        
        User Information:
        - Current Skills: {skills_text}
        - Target Role: {target_role if target_role else 'Not specified'}
        
        Please provide a comprehensive career advice response with these sections:
        
        1. **Career Transition Assessment**: Evaluate the user's current skills against the target role
        2. **Skill Gap Analysis**: List specific skills they need to learn, prioritized by importance
        3. **Learning Path**: Recommend specific courses, certifications, or resources
        4. **Project Ideas**: Suggest 3-5 portfolio projects to build
        5. **Job Search Strategy**: Tips for networking, resume optimization, and interview prep
        
        Be specific, actionable, and encouraging. Keep the response clear and well-structured.
        """
        
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            return {
                "success": True,
                "advice": response.text,
                "source": "Gemini"
            }
        except Exception as e:
            print(f"⚠️ Gemini API error: {e}")
            return self._get_fallback_response(user_skills, target_role)
    
    def _get_fallback_response(self, user_skills: List[str], target_role: str) -> Dict:
        """Fallback when Gemini is unavailable"""
        skills_text = ', '.join(user_skills) if user_skills else 'not specified'
        return {
            "success": True,
            "advice": f"""
📋 Career Advice for {target_role or 'your target role'}

Based on your skills ({skills_text}), here are my recommendations:

**1. Career Transition Assessment**
Your current skills provide a foundation for transitioning to {target_role or 'your target role'}. 
Focus on building the missing skills listed below.

**2. Skill Gap Analysis**
• **Priority 1 (Critical)**: Python, SQL, Statistics
• **Priority 2 (Important)**: Machine Learning, Data Visualization
• **Priority 3 (Nice to have)**: Cloud Computing, Big Data Tools

**3. Learning Path**
• Enroll in "Python for Data Science" on Coursera
• Complete "SQL for Data Analysis" on DataCamp
• Take "Machine Learning Specialization" on Coursera

**4. Project Ideas**
1. Customer churn prediction using Python
2. Sales dashboard with Tableau/Power BI
3. ETL pipeline with Python and SQL
4. Sentiment analysis of customer reviews

**5. Job Search Strategy**
• Update LinkedIn profile with new skills
• Build a GitHub portfolio with 3-5 projects
• Network with professionals in {target_role or 'your target role'}
• Prepare for technical interviews (LeetCode, HackerRank)
""",
            "source": "Fallback"
        }