import streamlit as st
from langchain_openai import ChatOpenAI  
import os  
import httpx 
from langchain_core.messages import HumanMessage

from fpdf import FPDF
import base64
# Create Client for proxy
client = httpx.Client(verify=False)


llm = ChatOpenAI( 
    base_url="https://genailab.tcs.in" ,
    model = "azure/genailab-maas-gpt-4o-mini", 
    api_key="sk-VHkpB_vIIyA1_9lWH3bt1w", 
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
