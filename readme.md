⚡ ResumeIQ — ATS Resume Optimizer
AI-powered resume analyzer that scores your resume against any job description, identifies gaps, and generates a professionally optimized version — available as both a Telegram Bot and a Streamlit Web App.

🎯 What It Does
Paste any job description + upload your resume → get a detailed ATS score + download an AI-optimized resume in seconds.

📊 ATS Scoring — 5-dimension score: Keywords, Role Alignment, Format, Action Verbs, Quantification
🔍 Gap Analysis — Identifies missing keywords and skills
✍️ AI Optimization — Rewrites resume to match JD without fabricating experience
📄 4 PDF Templates — Single Page, Two Page, ATS Plain, Executive
🤖 Telegram Bot — Full conversational interface
🌐 Web UI — Beautiful Streamlit dashboard


🛠️ Tech Stack:

Language — Python 3.11
AI Model — Groq API with LLaMA 3.3 70B
Telegram — python-telegram-bot
Web UI — Streamlit
PDF Parsing — PyMuPDF
DOCX Parsing — python-docx
PDF Generation — ReportLab
Environment — python-dotenv


🚀 Getting Started
1. Clone the repo
git clone https://github.com/Shivanshu0729/resume_optimizer_bot
cd resumeiq-ats-optimizer
2. Install dependencies
pip install -r requirements.txt
3. Set up API keys
Create a .env file in the root folder:
TELEGRAM_TOKEN=your_telegram_bot_token
GROQ_API_KEY=your_groq_api_key
Get your keys:

Telegram Token → Open Telegram → search @BotFather → /newbot → copy token
Groq API Key → Sign up free at console.groq.com → API Keys → Create Key

4. Run the Telegram Bot
python main.py
5. Run the Web UI
streamlit run app.py

📖 How to Use
Telegram Bot:

Search your bot on Telegram
Send /start
Paste the job description
Upload your resume (PDF, DOCX, or TXT)
Receive your ATS score report + optimized resume PDF
Choose from 4 format templates using the buttons

Web App:

Paste job description in the left panel
Upload your resume file
Click Analyze Resume
View score breakdown, keyword gaps, strengths
Select a format and download your optimized resume


📊 Scoring Breakdown:

Keyword Match — 30% — How many JD keywords appear in resume
Role Alignment — 35% — How well your experience matches the role
Format Score — 15% — Resume structure and readability
Action Verbs — 10% — Use of strong action verbs
Quantification — 10% — Presence of measurable achievements

Score ranges:

75 to 100 — Strong Match
55 to 74 — Partial Match
0 to 54 — Needs Improvement


⚙️ Environment Variables:

TELEGRAM_TOKEN — Telegram bot token — get from @BotFather
GROQ_API_KEY — Groq LLM API key — get from console.groq.com

