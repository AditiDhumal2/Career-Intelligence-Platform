"""
Natural Language Query Processing using Gemini
"""

import re
from typing import Dict, List
import os

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Try to import google.genai
try:
    from google import genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False

class NLPQueryProcessor:
    """Processes natural language queries about careers using Gemini"""
    
    def __init__(self, df):
        self.df = df
        self.client = None
        
        if not GENAI_AVAILABLE:
            return
        
        api_key = os.getenv('GEMINI_API_KEY')
        if api_key:
            try:
                self.client = genai.Client(api_key=api_key)
                self.model = "gemini-2.0-flash-exp"
                print("✅ NLP Query - Gemini initialized!")
            except Exception as e:
                print(f"Gemini init failed: {e}")
    
    def process_query(self, query: str) -> Dict:
        """Process natural language query"""
        
        # If we have Gemini client, use it for intelligent responses
        if self.client:
            try:
                prompt = f"""
                You are a career intelligence assistant. Answer this career-related question accurately and helpfully.
                
                Question: "{query}"
                
                If the question is about:
                - Skills needed for a role → List specific skills with prioritization
                - Salary information → Provide realistic salary ranges
                - Job demand → Give current market trends and outlook
                - Career advice → Provide actionable steps
                
                If the question is not career-related, politely redirect to career topics.
                Be concise, specific, and actionable.
                """
                
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt
                )
                
                return {
                    'intent': 'gemini',
                    'response': response.text,
                    'source': 'Gemini'
                }
            except Exception as e:
                print(f"Gemini query error: {e}")
                return self._fallback_response(query)
        
        return self._fallback_response(query)
    
    def _fallback_response(self, query: str) -> Dict:
        """Fallback response when Gemini unavailable"""
        
        # Try to extract role from query
        role = None
        roles = ['Data Scientist', 'Data Analyst', 'Data Engineer', 'ML Engineer', 
                 'Business Analyst', 'Data Architect', 'Analytics Manager']
        
        query_lower = query.lower()
        for r in roles:
            if r.lower() in query_lower:
                role = r
                break
        
        # Try to detect question type
        if 'skill' in query_lower:
            if role:
                return self._fallback_skills_response(role)
            return self._fallback_general_response(query)
        
        elif 'salary' in query_lower or 'pay' in query_lower:
            if role:
                return self._fallback_salary_response(role)
            return self._fallback_general_response(query)
        
        elif 'demand' in query_lower or 'job' in query_lower:
            if role:
                return self._fallback_demand_response(role)
            return self._fallback_general_response(query)
        
        else:
            return self._fallback_general_response(query)
    
    def _fallback_skills_response(self, role: str) -> Dict:
        return {
            'intent': 'skills',
            'response': f"""
🎯 Skills Needed for {role}

Based on market analysis, here are the key skills for {role}:

**Critical Skills (Must Have):**
• Python - For data manipulation and analysis
• SQL - For database querying
• Statistics - For data interpretation
• Machine Learning - For predictive modeling
• Data Visualization - For presenting insights

**Important Skills (Good to Have):**
• Cloud Computing (AWS/Azure/GCP)
• Big Data Tools (Spark, Hadoop)
• Deep Learning (TensorFlow, PyTorch)
• NLP/LLM (for advanced AI roles)

💡 **Action Plan:**
1. Start with Python and SQL
2. Take courses on Machine Learning
3. Build portfolio projects
4. Network with professionals
""",
            'source': 'Fallback'
        }
    
    def _fallback_salary_response(self, role: str) -> Dict:
        return {
            'intent': 'salary',
            'response': f"""
💰 Salary Information for {role}

Average Salary Ranges (US):
• Entry Level (0-2 years): $75,000 - $95,000
• Mid Level (3-5 years): $95,000 - $130,000
• Senior Level (5+ years): $130,000 - $170,000

📍 Location Premiums:
• San Francisco: +30-40%
• New York: +25-35%
• Austin: +15-20%

💡 Tip: Salaries vary by industry, company size, and location.
""",
            'source': 'Fallback'
        }
    
    def _fallback_demand_response(self, role: str) -> Dict:
        return {
            'intent': 'demand',
            'response': f"""
📈 Market Demand for {role}

Current Demand Outlook:
• Job Growth: +15-20% over next 5 years
• Market Sentiment: High demand, talent shortage
• Top Industries: Technology, Finance, Healthcare

Key Drivers:
1. AI and ML adoption across industries
2. Data-driven decision making
3. Digital transformation initiatives

💡 Tip: {role} skills are in high demand across all major industries.
""",
            'source': 'Fallback'
        }
    
    def _fallback_general_response(self, query: str) -> Dict:
        return {
            'intent': 'general',
            'response': f"""
🤔 I can help you with career questions!

Try asking about:
• **Skills**: "What skills do I need to become a Data Scientist?"
• **Salary**: "How much does a Data Analyst make?"
• **Demand**: "Is Machine Learning in demand?"
• **Career Advice**: "How to transition to Data Engineering?"

Your question: "{query}"
""",
            'source': 'Fallback'
        }