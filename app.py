import streamlit as st
from crewai import Agent, Task, Crew, LLM
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
from googleapiclient.discovery import build
from dotenv import load_dotenv
import os
import time

# Load environment variables
load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")
google_cse_id = os.getenv("GOOGLE_CSE_ID")
groq_api_key = os.getenv("GROQ_API_KEY")

# Streamlit UI Setup
st.set_page_config(page_title="Startup Competitor Intelligence", page_icon="🚀")
st.title("🚀 Startup Competitor Intelligence Crew")
st.markdown("""
Enter your startup idea below and get:
1. Competitor analysis
2. Feature comparison
3. Differentiation strategies
4. Go-to-market recommendations
""")

# Initialize session state
if 'results' not in st.session_state:
    st.session_state.results = None
if 'running' not in st.session_state:
    st.session_state.running = False

# Tool Definition
class GoogleSearchInput(BaseModel):
    """Input schema for GoogleSearchTool."""
    query: str = Field(..., description="Search query to look up")
    num_results: int = Field(default=5, description="Number of results to return")

class GoogleSearchTool(BaseTool):
    name: str = "Google Search Tool"
    description: str = "Searches Google using Custom Search JSON API"
    args_schema: Type[BaseModel] = GoogleSearchInput

    def _run(self, query: str, num_results: int = 5) -> str:
        try:
            service = build("customsearch", "v1", developerKey=google_api_key)
            res = service.cse().list(q=query, cx=google_cse_id, num=num_results).execute()
            items = res.get('items', [])
            
            results = []
            for item in items:
                results.append(f"{item['title']}: {item['link']}")
            
            return "\n".join(results) if results else "No results found"
        except Exception as e:
            return f"Error performing search: {str(e)}"

# Initialize LLM and Agents
def initialize_crew():
    llm = LLM(
        model="groq/llama-3.3-70b-versatile", 
        api_key=groq_api_key, 
        temperature=0.7
    )
    
    google_search_tool = GoogleSearchTool()

    market_researcher = Agent(
        role="Market Researcher",
        goal="Find competitors and analyze their positioning",
        backstory="Expert in scraping data and identifying market trends",
        tools=[google_search_tool],
        llm=llm,
        verbose=True
    )

    feature_comparator = Agent(
        role="Feature Analyst",
        goal="Compare features and identify gaps",
        backstory="Product manager with 10+ years in competitive analysis",
        llm=llm,
        verbose=True
    )

    differentiation_strategist = Agent(
        role="Differentiation Strategist",
        goal="Suggest unique positioning and differentiation strategies",
        backstory="Marketing expert specializing in competitive differentiation",
        llm=llm,
        verbose=True
    )

    gtm_coach = Agent(
        role="Go-To-Market Coach",
        goal="Analyze competitors' GTM strategies and suggest improvements",
        backstory="Growth hacker with experience in launching 50+ startups",
        llm=llm,
        verbose=True
    )

    # Create tasks
    research_task = Task(
        description="Find 5 competitors for {startup_idea}",
        expected_output="List of competitors with names and URLs",
        agent=market_researcher
    )

    analysis_task = Task(
        description="Analyze features of found competitors",
        expected_output="Feature comparison table with gaps identified",
        agent=feature_comparator,
        context=[research_task]
    )

    differentiation_task = Task(
        description="Suggest how to differentiate {startup_idea} from competitors found in previous tasks",
        expected_output="3-5 unique positioning strategies with rationale",
        agent=differentiation_strategist,
        context=[research_task, analysis_task]
    )

    gtm_task = Task(
        description="Propose a go-to-market strategy based on competitor weaknesses",
        expected_output="1. Competitor GTM analysis 2. 3 actionable launch tactics",
        agent=gtm_coach,
        context=[research_task, analysis_task]
    )

    return Crew(
        agents=[market_researcher, feature_comparator, differentiation_strategist, gtm_coach],
        tasks=[research_task, analysis_task, differentiation_task, gtm_task],
        verbose=True
    )

# Input Form
with st.form("startup_form"):
    startup_idea = st.text_area("Describe your startup idea:", 
                              placeholder="e.g., Notion-like tool for video creators to organize clips and scripts",
                              height=150)
    
    submitted = st.form_submit_button("Analyze Competition")
    
    if submitted and startup_idea.strip():
        st.session_state.running = True
        st.session_state.results = None
        
        with st.spinner("🧠 Analyzing your competition (this may take 2-3 minutes)..."):
            try:
                crew = initialize_crew()
                result = crew.kickoff(inputs={"startup_idea": startup_idea})
                # Convert CrewOutput to string if needed
                st.session_state.results = str(result)
                st.session_state.running = False
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                st.session_state.running = False

# Display Results
if st.session_state.results:
    st.success("Analysis Complete!")
    
    with st.expander("📊 Full Analysis Report", expanded=True):
        st.markdown(st.session_state.results)
    
    # Download button with proper string conversion
    st.download_button(
        label="📥 Download Report",
        data=st.session_state.results,
        file_name="competitor_analysis.md",
        mime="text/markdown"
    )

if st.session_state.running:
    with st.empty():
        for seconds in range(180):  # 3 minute timeout
            if not st.session_state.running:
                break
            time.sleep(1)
            st.write(f"⏳ Analyzing... {seconds} seconds elapsed")

# Sidebar Info
st.sidebar.markdown("""
### How It Works
1. Enter your startup idea
2. Our AI crew will:
   - Find competitors
   - Compare features
   - Suggest differentiators
   - Recommend GTM strategies

### Agents Working For You
- 🔍 Market Researcher
- 📊 Feature Analyst
- 🎯 Differentiation Strategist
- 🚀 GTM Coach
""")

# Footer
st.markdown("---")
st.caption("Powered by CrewAI, Groq, and Google Custom Search")
