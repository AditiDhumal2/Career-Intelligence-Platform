"""
Interview Preparation Module
Provides role-specific interview questions and tips
"""

import random
from typing import Dict, List

class InterviewPrep:
    """
    Provides interview preparation resources
    """
    
    def __init__(self):
        self.question_bank = {
            'Data Scientist': {
                'technical': [
                    "What's the difference between L1 and L2 regularization?",
                    "Explain how Random Forest works.",
                    "How would you handle imbalanced data?",
                    "What is the curse of dimensionality?",
                    "Explain the difference between bagging and boosting."
                ],
                'behavioral': [
                    "Tell me about a time you failed and what you learned.",
                    "How do you handle tight deadlines?",
                    "Describe your experience working in teams.",
                    "Why are you interested in data science?",
                    "Where do you see yourself in 5 years?"
                ],
                'case': [
                    "How would you build a recommendation system?",
                    "Design an A/B testing framework.",
                    "How would you detect fraud in transactions?",
                    "Build a customer churn prediction model."
                ]
            },
            'Data Analyst': {
                'technical': [
                    "What's the difference between SQL and NoSQL?",
                    "Explain different types of joins.",
                    "What is a pivot table?",
                    "How do you handle missing data?",
                    "What's the difference between correlation and causation?"
                ],
                'behavioral': [
                    "Tell me about a data project you worked on.",
                    "How do you communicate insights to non-technical stakeholders?",
                    "Describe a time you used data to solve a problem."
                ],
                'case': [
                    "Analyze this dataset and provide insights.",
                    "How would you improve a company's dashboard?",
                    "Design a sales forecasting model."
                ]
            }
        }
        
        self.tips = {
            'general': [
                "Research the company thoroughly",
                "Prepare questions to ask the interviewer",
                "Practice your elevator pitch",
                "Review your resume and projects",
                "Arrive 10-15 minutes early",
                "Follow up with a thank-you email within 24 hours"
            ],
            'technical': [
                "Practice coding problems on LeetCode/HackerRank",
                "Review fundamental algorithms and data structures",
                "Be prepared to explain your thought process",
                "Write clean, readable code",
                "Test your code with edge cases"
            ],
            'behavioral': [
                "Use the STAR method (Situation, Task, Action, Result)",
                "Be specific and provide concrete examples",
                "Show enthusiasm and curiosity",
                "Be honest about your experience"
            ]
        }
    
    def get_questions(self, role: str, count: int = 5) -> Dict:
        """
        Get interview questions for a specific role
        
        Args:
            role: Job role
            count: Number of questions per category
            
        Returns:
            Dict with questions by category
        """
        if role not in self.question_bank:
            # Try to find similar role
            for key in self.question_bank.keys():
                if key.lower() in role.lower():
                    role = key
                    break
            else:
                role = list(self.question_bank.keys())[0]
        
        questions = self.question_bank[role]
        
        return {
            'technical': random.sample(questions['technical'], min(count, len(questions['technical']))),
            'behavioral': random.sample(questions['behavioral'], min(count, len(questions['behavioral']))),
            'case': random.sample(questions['case'], min(count, len(questions['case'])))
        }
    
    def get_tips(self) -> Dict:
        """Get interview tips"""
        return self.tips
    
    def generate_interview_plan(self, role: str) -> str:
        """
        Generate an interview preparation plan
        
        Args:
            role: Target role
            
        Returns:
            str: Interview preparation plan
        """
        plan = f"""
📋 Interview Preparation Plan for {role}

📚 Week 1: Technical Foundation
- Review core concepts in {role}
- Practice coding problems daily (2-3 problems)
- Watch tutorials on key topics

📚 Week 2: Applied Skills
- Build a small project relevant to {role}
- Practice case studies
- Review common interview questions

📚 Week 3: Behavioral Preparation
- Prepare STAR stories (5-7 examples)
- Practice your elevator pitch
- Research the company

📚 Week 4: Mock Interviews
- Do mock interviews with friends
- Record yourself answering questions
- Get feedback and improve
        """
        
        # Add role-specific questions
        questions = self.get_questions(role, 3)
        plan += "\n\n🎯 Sample Questions to Practice:\n"
        for category, q_list in questions.items():
            plan += f"\n{category.upper()}:\n"
            for q in q_list:
                plan += f"  • {q}\n"
        
        return plan