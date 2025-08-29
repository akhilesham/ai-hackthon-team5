import streamlit as st
from langchain_openai import ChatOpenAI  
import os  
import httpx 
from langchain_core.messages import HumanMessage

from fpdf import FPDF
import base64
from dotenv import load_dotenv
# Create Client for proxy
load_dotenv()
api_key = os.getenv("API_KEY")
gpt_model = os.getenv("GPT_MODEL")
ai_lab_base_url = os.getenv("AI_LAB_BASE_URL")

client = httpx.Client(verify=False)


llm = ChatOpenAI( 
    base_url=ai_lab_base_url,
    model = gpt_model, 
    api_key=api_key, 
    http_client = client 
) 

system_prompt = """
You are a helpful Python coding assistant. Your job is to:
1. Write clean, correct, and well-commented Python code snippets.
2. After generating code, provide a clear Chain-of-Thought explanation (why you wrote the code that way).
3. Then, ask the user if they want to optimize or expand the snippet.

Always follow this structure:
- Confirm the task
- Generate code
- Explain reasoning (CoT)
- Ask for improvement directions
"""

response = llm([HumanMessage(content=system_prompt)])
print(response)