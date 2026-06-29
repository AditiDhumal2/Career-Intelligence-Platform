# 📊 Career Intelligence Platform

## 🎯 AI-Powered Career Guidance & Job Market Analytics

[https://static.streamlit.io/badges/streamlit_badge_black_white.svg)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---
🌐 Live Demo
Try the application now: https://career-intelligence-platform-afulhrrvqsnclq2seyfafv.streamlit.app/

---
## 📋 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Technology Stack](#-technology-stack)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Usage Guide](#-usage-guide)
- [Modules Explained](#-modules-explained)
- [Data Pipeline](#-data-pipeline)
- [Screenshots](#-screenshots)
- [API Keys Setup](#-api-keys-setup)
- [Deployment](#-deployment)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Overview

The **Career Intelligence Platform** is a comprehensive data analytics system that helps professionals make informed career decisions. It analyzes job market data, extracts skills from resumes using NLP, identifies skill gaps, and provides personalized learning recommendations.

### Why This Project?

| Challenge | Solution |
|-----------|----------|
| **Information Asymmetry** | Real-time job market analytics with 500+ data points |
| **Skill Gap Confusion** | Data-driven skill gap analysis with prioritized learning paths |
| **Resume Mismatch** | NLP-powered resume parsing and improvement suggestions |
| **Career Uncertainty** | AI-powered career advice and role progression mapping |

---

## ✨ Key Features

### 📊 Market Intelligence
- Analyze 500+ job postings across 22 roles
- Identify top-paying jobs and in-demand skills
- Interactive filters for location, industry, and remote policy
- Visualize skill market penetration and geographic distribution

### 💡 Skill Gap Analyzer
- Enter your current skills and target role
- Calculate match percentage with market requirements
- Get prioritized learning path with time estimates
- Understand market demand for each skill

### 🗺️ Career Path Mapper
- Plan your career journey from current to dream role
- View step-by-step progression with time estimates
- Understand salary expectations at each level
- Identify required skills for each role

### 🤖 AI Career Advisor
- Get personalized career advice powered by Google Gemini
- Ask custom career questions in natural language
- Receive learning resource recommendations
- Get job search strategy tips

### 📄 Resume Critic
- Upload your resume (PDF, DOCX, TXT)
- Extract skills automatically
- Get actionable improvement suggestions
- Analyze ATS-friendly keyword presence

### 🎤 Interview Preparation
- Access role-specific interview questions
- Generate 4-week preparation plans
- Practice technical, behavioral, and case questions
- Get general and technical tips

### 🔍 Natural Language Query
- Ask career questions in plain English
- Intelligent response with intent detection
- Understand skills, salary, and demand insights

### 📈 Market Trends
- Real-time job market trends
- Growth rates and salary trends
- Role-specific market sentiment

---

## 🛠️ Technology Stack

| Category | Technologies |
|----------|--------------|
| **Backend** | Python 3.11+ |
| **Data Processing** | Pandas, NumPy |
| **Machine Learning** | Scikit-learn, SentenceTransformers |
| **AI/LLM** | Google Gemini API |
| **Vector Search** | FAISS, SentenceTransformers |
| **Document Processing** | PyPDF2, python-docx, docx2txt |
| **Frontend** | Streamlit, Plotly |
| **APIs** | Gemini API, SerpAPI |
| **Environment** | Python-dotenv |
| **Deployment** | Streamlit Cloud |

---

## 📁 Project Structure

```
career-intelligence-platform/
│
├── 📁 dashboard/
│   └── app.py                          # Main Streamlit application (900+ lines)
│
├── 📁 src/
│   ├── __init__.py
│   ├── data_loader.py                  # ETL pipeline for data processing
│   ├── job_analyzer.py                 # Job market analytics engine
│   ├── skill_gap_analyzer.py           # Skill gap detection with ML scoring
│   ├── career_path_mapper.py           # Career progression mapping
│   ├── resume_parser.py                # NLP-based skill extraction
│   ├── job_scraper.py                  # Real-time API job fetching
│   ├── llm_advisor.py                  # Gemini AI career advisor
│   ├── resume_critic.py                # Resume improvement suggestions
│   ├── interview_prep.py               # Interview question generator
│   ├── market_trends.py                # SerpAPI market trends
│   ├── nlp_query.py                    # Natural language query processing
│   └── rag_retriever.py                # Semantic search using embeddings
│
├── 📁 data/
│   ├── 📁 raw/
│   │   └── job_market_data.csv         # 500+ raw job records (generated)
│   ├── 📁 processed/
│   │   └── cleaned_job_data.csv        # Cleaned and processed dataset
│   ├── 📁 backup/
│   │   └── job_market_data_backup_*.csv # Backup of original data
│   └── 📁 chroma_db/                   # Vector database for semantic search
│
├── 📁 models/
│   └── salary_predictor.pkl            # Trained ML model for salary prediction
│
├── 📁 .streamlit/
│   └── config.toml                     # Streamlit configuration
│
├── 📁 screenshots/                     # App screenshots for documentation
│
├── 📁 temp/                            # Temporary files (auto-generated)
│   └── temp_*.docx/pdf/txt             # Temporary uploaded resume files
│
├── 📄 root_directory_files/
│   ├── salary_by_job.png               # Chart: Salary by job title (generated)
│   ├── skill_demand.png                # Chart: Skill demand visualization (generated)
│   ├── save_for_powerbi.py             # Export data for Power BI
│   ├── generate_large_dataset.py       # Generate 500+ job records
│   ├── update_dataset_demand_scores.py # Update demand scores script
│   ├── test_imports.py                 # Test all imports
│   ├── test_packages.py                # Test package installations
│   ├── test_llm_install.py             # Test LLM packages
│   ├── test_all_modules.py             # Test all modules
│   ├── test_analyzer.py                # Test job analyzer
│   ├── fix_and_test_analyzer.py        # Fix and test analyzer
│   ├── migrate_to_large_data.py        # Migrate to large dataset
│   ├── requirements.txt                # Python dependencies
│   ├── runtime.txt                     # Python version (3.11.9)
│   ├── .env.example                    # Environment variables template
│   ├── .env                            # Environment variables (not tracked)
│   ├── .gitignore                      # Git ignore rules
│   ├── README.md                       # Project documentation
│   ├── POWERBI_GUIDE.md                # Power BI export guide
│   └── MSIM_APPLICATION_GUIDE.md       # MSIM application strategy
│
└── 📁 venv/                            # Virtual environment (not tracked)
---

## 📦 Installation

### Prerequisites

- Python 3.11 or higher
- Git
- Virtual environment (recommended)

### Step-by-Step Setup

```bash
# 1. Clone the repository
git clone https://github.com/AditiDhumal2/Career-Intelligence-Platform.git
cd Career-Intelligence-Platform

# 2. Create and activate virtual environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file from template
cp .env.example .env
# Edit .env and add your API keys

# 5. Generate dataset (first time only)
python data/generate_large_dataset.py

# 6. Run data pipeline
python src/data_loader.py

# 7. Launch the dashboard
streamlit run dashboard/app.py
```

---

## 🚀 Usage Guide

### 1. Market Intelligence Dashboard
The landing page shows:
- Key metrics (jobs, salary, demand, remote percentage)
- Top paying job roles
- Most in-demand skills
- Skill market penetration
- Geographic distribution

### 2. Skill Gap Analysis
```
1. Enter your skills (e.g., "Python, SQL, Excel")
2. Select your target role (e.g., "Data Scientist")
3. View your match percentage
4. See prioritized learning path
5. Get personalized recommendations
```

### 3. Career Path Mapping
```
1. Select your current role
2. Select your dream role
3. View step-by-step progression
4. Understand required skills at each level
5. See salary expectations
```

### 4. AI Career Advisor
```
1. Enter your skills
2. Select target role
3. Click "Get AI Advice"
4. Receive personalized career guidance
5. Or ask custom questions
```

### 5. Resume Critic
```
1. Upload your resume (PDF, DOCX, TXT)
2. Click "Analyze"
3. View extracted skills
4. See improvement suggestions
5. Check keyword analysis
```

---

## 🔧 Modules Explained

### Data Loader (`src/data_loader.py`)
Handles data ingestion, cleaning, and preprocessing:
- Loads CSV data
- Handles missing values
- Feature engineering
- Saves processed data

### Job Market Analyzer (`src/job_analyzer.py`)
Analyzes job market trends:
- Top paying jobs
- In-demand skills
- Location analysis
- Skill scoring

### Skill Gap Analyzer (`src/skill_gap_analyzer.py`)
Analyzes user skills against market requirements:
- Match percentage calculation
- Priority scoring algorithm
- Learning path generation
- Market demand analysis

### Career Path Mapper (`src/career_path_mapper.py`)
Maps career progression:
- Role hierarchy
- Skill requirements per level
- Time estimates
- Salary progression

### Resume Parser (`src/resume_parser.py`)
Extracts information from resumes:
- Skill extraction
- Experience detection
- Education extraction
- Contact info

### LLM Advisor (`src/llm_advisor.py`)
AI-powered career advice:
- Gemini API integration
- Personalized recommendations
- Custom question answering
- Fallback responses

### NLP Query (`src/nlp_query.py`)
Natural language processing:
- Intent detection
- Entity extraction
- Intelligent responses

---

## 🔄 Data Pipeline

```
Raw Data → Clean → Feature Engineering → Transform → Dashboard
     ↓         ↓           ↓              ↓           ↓
  CSV/API   Remove      avg_salary    Normalize   Visualize
  Upload    Duplicates  demand_score   Encode     Analyze
  Resumes   Handle      remote_flag   Bucket     Recommend
            Nulls
```

---

## 🎯 Key Metrics

### Dataset
| Metric | Value |
|--------|-------|
| Job Records | 500+ |
| Job Roles | 22 |
| Unique Skills | 54 |
| Locations | 23 |
| Avg Salary | $96,264 |

### Top Skills by Demand
| Skill | Demand Score |
|-------|--------------|
| Machine Learning | 98/100 |
| TensorFlow | 96/100 |
| PyTorch | 94/100 |
| Python | 95/100 |
| SQL | 93/100 |

---

## 🔑 API Keys Setup

### Google Gemini API (Free)
```bash
# Get from: https://aistudio.google.com
GEMINI_API_KEY=your_gemini_api_key_here
```

### SerpAPI (Free Plan - 250 searches/month)
```bash
# Get from: https://serpapi.com
SERPAPI_API_KEY=your_serpapi_api_key_here
```

### Configure .env File
```bash
# .env file
GEMINI_API_KEY=your_gemini_api_key_here
SERPAPI_API_KEY=your_serpapi_api_key_here
```

---

## 🚀 Deployment

### Streamlit Cloud (Free)
```bash
# 1. Push to GitHub
git add .
git commit -m "Deploy to Streamlit"
git push origin main

# 2. Go to https://share.streamlit.io
# 3. Click "New app"
# 4. Select repository and branch
# 5. Set main file: dashboard/app.py
# 6. Click "Deploy"
```

### Environment Variables on Streamlit Cloud
```toml
# .streamlit/secrets.toml
GEMINI_API_KEY = "your_gemini_api_key"
SERPAPI_API_KEY = "your_serpapi_api_key"
```

---

## 📸 Screenshots

### Market Intelligence Dashboard
![Market Intelligence](screenshots/market_intelligence.png)

### Skill Gap Analyzer
![Skill Gap Analyzer](screenshots/skill_gap.png)

### Career Path Mapper
![Career Path Mapper](screenshots/career_path.png)

### AI Advisor
![AI Advisor](screenshots/ai_advisor.png)

### Resume Critic
![Resume Critic](screenshots/resume_critic.png)

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Guidelines
- Write clear commit messages
- Add comments to your code
- Update documentation as needed
- Test all features before submitting

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Google Gemini** for AI-powered career advice
- **Streamlit** for interactive dashboard framework
- **Remotive API** for real-time job data
- **SerpAPI** for market trends data

---

## 📞 Contact & Support

- **GitHub Issues**: [Report a bug](https://github.com/AditiDhumal2/Career-Intelligence-Platform/issues)
- **Live Demo**: [Try the app](https://career-intelligence-platform.streamlit.app)
- **Documentation**: [View docs](docs/)

---

## 🎯 Future Enhancements

| Feature | Status |
|---------|--------|
| User Accounts | Planned |
| LinkedIn Integration | Planned |
| Email Reports | Planned |
| Mobile App | Planned |
| Advanced ML Models | Planned |

---

**Built with ❤️ for Career Success**

---

⭐ If you find this project useful, please give it a star on GitHub!
