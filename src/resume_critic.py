"""
Resume Critic & Improvement Suggestion
Analyzes resumes and provides actionable feedback
"""

import re
from typing import Dict, List
import PyPDF2
import docx2txt

class ResumeCritic:
    """
    Analyzes resumes and provides improvement suggestions
    """
    
    def __init__(self):
        self.ats_keywords = {
            'data_science': [
                'python', 'sql', 'machine learning', 'statistics', 'data visualization',
                'pandas', 'numpy', 'scikit-learn', 'tensorflow', 'pytorch',
                'deep learning', 'nlp', 'cloud computing', 'aws', 'azure'
            ],
            'soft_skills': [
                'leadership', 'communication', 'problem solving', 'teamwork',
                'project management', 'critical thinking', 'collaboration'
            ],
            'metrics': [
                'increased', 'improved', 'reduced', 'optimized', 'achieved',
                'led', 'managed', 'developed', 'implemented', 'created'
            ]
        }
    
    def analyze_resume(self, file_path: str) -> Dict:
        """
        Analyze a resume and provide improvement suggestions
        
        Args:
            file_path: Path to resume file
            
        Returns:
            Dict with analysis and suggestions
        """
        # Extract text from resume
        text = self._extract_text(file_path)
        
        if not text:
            return {"error": "Could not extract text from file"}
        
        # Analyze
        analysis = {
            "word_count": len(text.split()),
            "has_contact_info": self._check_contact_info(text),
            "has_education": self._check_education(text),
            "has_experience": self._check_experience(text),
            "has_skills_section": self._check_skills_section(text),
            "action_verbs": self._extract_action_verbs(text),
            "keywords_found": self._extract_keywords(text),
            "suggestions": []
        }
        
        # Generate suggestions
        analysis["suggestions"] = self._generate_suggestions(analysis)
        
        return analysis
    
    def _extract_text(self, file_path: str) -> str:
        """Extract text from PDF or DOCX"""
        try:
            if file_path.endswith('.pdf'):
                with open(file_path, 'rb') as f:
                    reader = PyPDF2.PdfReader(f)
                    return '\n'.join([page.extract_text() for page in reader.pages])
            elif file_path.endswith('.docx'):
                return docx2txt.process(file_path)
            else:
                with open(file_path, 'r') as f:
                    return f.read()
        except Exception as e:
            return ""
    
    def _check_contact_info(self, text: str) -> Dict:
        """Check if resume has contact info"""
        email = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
        phone = re.search(r'(\+?1[-.\s]?)?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}', text)
        
        return {
            "has_email": bool(email),
            "has_phone": bool(phone),
            "score": 50 if (email and phone) else 25 if (email or phone) else 0
        }
    
    def _check_education(self, text: str) -> Dict:
        """Check for education section"""
        education_keywords = ['bachelor', 'master', 'phd', 'degree', 'university', 'college']
        found = any(keyword in text.lower() for keyword in education_keywords)
        return {"has_education": found, "score": 100 if found else 0}
    
    def _check_experience(self, text: str) -> Dict:
        """Check for experience section"""
        exp_keywords = ['experience', 'worked', 'employed', 'intern', 'internship']
        found = any(keyword in text.lower() for keyword in exp_keywords)
        return {"has_experience": found, "score": 100 if found else 0}
    
    def _check_skills_section(self, text: str) -> Dict:
        """Check for skills section"""
        skills_keywords = ['skills', 'technical skills', 'core competencies']
        found = any(keyword in text.lower() for keyword in skills_keywords)
        return {"has_skills_section": found, "score": 100 if found else 0}
    
    def _extract_action_verbs(self, text: str) -> List[str]:
        """Extract action verbs from resume"""
        verbs = self.ats_keywords['metrics']
        found = []
        for verb in verbs:
            if verb in text.lower():
                found.append(verb)
        return found
    
    def _extract_keywords(self, text: str) -> Dict:
        """Extract keywords from resume"""
        all_keywords = []
        for category, keywords in self.ats_keywords.items():
            for keyword in keywords:
                if keyword in text.lower():
                    all_keywords.append(keyword)
        
        # Group by category
        result = {}
        for category, keywords in self.ats_keywords.items():
            result[category] = [k for k in keywords if k in text.lower()]
        
        return result
    
    def _generate_suggestions(self, analysis: Dict) -> List[str]:
        """Generate improvement suggestions"""
        suggestions = []
        
        # Contact info suggestions
        contact = analysis.get("has_contact_info", {})
        if not contact.get("has_email"):
            suggestions.append("📧 Add a professional email address to your resume header")
        if not contact.get("has_phone"):
            suggestions.append("📱 Add a phone number for recruiters to reach you")
        
        # Section suggestions
        if not analysis.get("has_education", {}).get("has_education"):
            suggestions.append("🎓 Add an education section with your degrees and GPA")
        
        if not analysis.get("has_experience", {}).get("has_experience"):
            suggestions.append("💼 Add work experience or relevant projects")
        
        if not analysis.get("has_skills_section", {}).get("has_skills_section"):
            suggestions.append("📋 Add a dedicated skills section")
        
        # Action verb suggestions
        if len(analysis.get("action_verbs", [])) < 3:
            suggestions.append("📝 Use more action verbs like 'Led', 'Developed', 'Created'")
        
        # Keyword suggestions
        keywords = analysis.get("keywords_found", {})
        all_keywords = []
        for category, skills in keywords.items():
            all_keywords.extend(skills)
        
        if len(all_keywords) < 10:
            suggestions.append("🔑 Add more industry keywords to pass ATS filters")
        
        # Word count suggestion
        if analysis.get("word_count", 0) < 200:
            suggestions.append("📄 Expand your resume - aim for 300-500 words")
        elif analysis.get("word_count", 0) > 800:
            suggestions.append("📄 Consider condensing your resume - keep it to 1-2 pages")
        
        return suggestions