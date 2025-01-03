from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.yfinance import YFinanceTools
from phi.tools.googlesearch import GoogleSearch
import os
import openai
from dotenv import load_dotenv
#web search agent
load_dotenv()
openai.api_key=os.getenv("OPENAI_API_KEY")

class Myagent:
 
 def __init__(self):
   
   self.web_search_agent=Agent(
   name="web Search agent",
   description="You are a news agent that helps users find the latest news.",
   model=Groq(id="llama3-groq-70b-8192-tool-use-preview"),
   tools=[GoogleSearch()],
   instructions=["Given a topic by the user, respond with 4 latest news items about that topic.",
        "Search for 10 news items and select the top 4 unique items.",
        "Search in English"],
   show_tool_calls=True,
   markdown=True
)

   self.financial_agent=Agent(

    name="web Search agent",
    description="You are a news agent that helps users find the latest news.",
    model=Groq(id="llama3-groq-70b-8192-tool-use-preview"),
    tools=[YFinanceTools(
       stock_fundamentals=True,
       income_statements=True,
       company_info=True,
       analyst_recommendations=True
       )],
    instructions=[
        "Search in English"],
    additional_context="Please use a reliable news source like Google News",    
    show_tool_calls=True,
    markdown=True,
   )



 def process_agents(self,user_input):
 
    multi_agents=Agent(

    team=[self.web_search_agent,self.financial_agent],
    model=Groq(id="llama3-groq-70b-8192-tool-use-preview"),
    instructions=["allways sources and show data in table format"],
    response_format={ "type": "json_object" },
    show_tool_calls=True,
    markdown=True,
)    
    RunResponse=multi_agents.run(user_input)
    return self.extract_relevant_data(RunResponse)
 

 def extract_relevant_data(self, response):
        # Assuming the response includes structured data, like markdown or a table
        # Clean and format the output to get only the relevant part

        # For example, checking if the response includes a markdown table:
        if "Top Companies with Good Earnings" in response:
            # Extract the table data or structured content
            start_idx = response.find("Top Companies with Good Earnings")
            end_idx = response.find("Sources:", start_idx)

            # Get the relevant data (for example, earnings summary table)
            relevant_data = response[start_idx:end_idx].strip()

            # Format the output as markdown for better readability
            formatted_output = f"## {relevant_data}\n"
            return formatted_output
        
        # If no relevant data found, return a fallback message
        return "No relevant company earnings information found."