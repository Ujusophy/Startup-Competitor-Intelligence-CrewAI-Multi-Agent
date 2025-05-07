# 🚀 Startup Competitor Intelligence Crew
The Startup Competitor Intelligence Crew is an AI-powered tool that helps entrepreneurs and startups quickly analyze their competitive landscape. 

Simply describe your startup idea, and our crew of AI agents will:
- Identify your closest competitors

- Analyze their features and positioning

- Suggest unique differentiation strategies

- Recommend go-to-market tactics

Built with CrewAI, Groq, and Google Custom Search, this tool provides actionable competitive intelligence in minutes rather than days.

## 🛠 How It Works
- The AI Crew Structure
- Market Researcher: Finds and analyzes competitors

- Feature Analyst: Compares features and identifies gaps

- Differentiation Strategist: Suggests unique positioning

- GTM Coach: Recommends launch strategies

## Prerequisites
- Python 3.8+
- Google Custom Search JSON API key
- Groq API key

## Setup
Clone the repository:
```
git clone https://github.com/Ujusophy/Startup-Competitor-Intelligence-CrewAI-Mult.git
cd Startup-Competitor-Intelligence-CrewAI-Mult
```
Install dependencies:
```
pip install -r requirements.txt
```
Create a .env file:
```
GOOGLE_API_KEY=your_google_api_key
GOOGLE_CSE_ID=your_custom_search_engine_id
GROQ_API_KEY=your_groq_api_key
```
Run the Streamlit app:
```
streamlit run app.py
```

In the web interface:
- Enter your startup idea
- Click "Analyze Competition"
- View and download your report

Example Input:
```
Notion-like tool for video creators to organize clips and scripts
```


## 🛠 Tech Stack
#### Component---------------Technology
AI Orchestration----------CrewAI


LLM Provider--------------Groq


Search Engine-------------Google Custom Search JSON API


UI Framework--------------Streamlit


Language------------------Python 3.10
