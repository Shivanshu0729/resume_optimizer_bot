ResumeIQ — ATS Resume Optimizer
An AI-powered resume analyzer that scores your resume against any job description, identifies skill gaps, and generates a professionally optimized version. Available as both a Telegram Bot and a Streamlit Web App.

What It Does:
Paste any job description and upload your resume to receive a detailed ATS score, keyword gap analysis, and a fully optimized resume — in seconds.

ATS Scoring — 5-dimension score covering Keywords, Role Alignment, Format, Action Verbs, and Quantification
Gap Analysis — Identifies missing keywords and skills required for the role
AI Optimization — Rewrites your resume to better match the job description without fabricating experience
4 PDF Templates — Single Page, Two Page, ATS Plain, Executive
Telegram Bot — Full conversational interface on Telegram
Web UI — Clean and responsive Streamlit dashboard


Tech Stack:
Language — Python 3.11
AI Model — Groq API with LLaMA 3.3 70B
Telegram — python-telegram-bot
Web UI — Streamlit
PDF Parsing — PyMuPDF
DOCX Parsing — python-docx
PDF Generation — ReportLab
Environment Management — python-dotenv


Project Structure
resume_optimizer_bot/
├── main.py
├── app.py
├── requirements.txt
├── .env
├── .gitignore
├── file_parser_mod/
│   ├── __init__.py
│   └── file_parser.py
├── scorer/
│   ├── __init__.py
│   └── ats_scorer.py
├── optimizer/
│   ├── __init__.py
│   └── resume_optimizer.py
└── renderer/
    ├── __init__.py
    └── pdf_renderer.py

Getting Started:
1. Clone the repository
git clone https://github.com/Shivanshu0729/resume_optimizer_bot
cd resumeiq-ats-optimizer
2. Install dependencies
pip install -r requirements.txt
3. Configure environment variables
Create a .env file in the root folder and add the following:
TELEGRAM_TOKEN=your_telegram_bot_token
GROQ_API_KEY=your_groq_api_key
How to get your keys:

Telegram Token — Open Telegram, search @BotFather, send /newbot, follow the steps, and copy the token
Groq API Key — Sign up for free at console.groq.com, go to API Keys, and create a new key

4. Run the Telegram Bot
python main.py
5. Run the Web UI
streamlit run app.py
The web app will open at http://localhost:8501

How to Use->
Telegram Bot:
Search your bot by username on Telegram
Send /start
Paste the full job description as a message
Upload your resume as a PDF, DOCX, or TXT file
Receive your ATS score report and optimized resume PDF
Use the format buttons to choose between Single Page, Two Page, ATS Plain, or Executive

Web App:
Paste the job description in the left panel
Upload your resume file
Click Analyze Resume
Review the score breakdown, keyword analysis, strengths, and improvement suggestions
Select a resume format and download the optimized PDF


Scoring Breakdown:
Keyword Match — 30% — Measures how many required keywords from the JD appear in your resume
Role Alignment — 35% — Measures how well your experience matches the job role
Format Score — 15% — Evaluates resume structure and readability
Action Verbs — 10% — Checks for the use of strong, impactful action verbs
Quantification — 10% — Checks for measurable achievements and numbers

Score interpretation:
75 to 100 — Strong Match
55 to 74 — Partial Match
0 to 54 — Needs Improvement


Environment Variables:
TELEGRAM_TOKEN — Your Telegram bot token from @BotFather
GROQ_API_KEY — Your Groq API key from console.groq.com


Security:
Do not commit your .env file. It is included in .gitignore by default.
If your Telegram token is accidentally exposed, regenerate it immediately from @BotFather.
The Groq free tier provides sufficient quota for development and testing without requiring billing.


Requirements
python-telegram-bot==20.7
groq
PyMuPDF==1.24.0
python-docx==1.1.0
reportlab
python-dotenv==1.0.1
streamlit