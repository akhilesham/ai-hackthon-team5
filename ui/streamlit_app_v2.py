import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
import httpx
import re
import base64
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.prompts import SYSTEM_BASE_PROMPT, UNSAFE_PROMPTS


client = httpx.Client(verify=False)

from dotenv import load_dotenv
# Create Client for proxy
load_dotenv()
api_key = os.getenv("API_KEY")
gpt_model = os.getenv("GPT_MODEL")
ai_lab_base_url = os.getenv("AI_LAB_BASE_URL")


llm = ChatOpenAI(
    base_url=ai_lab_base_url,
    model = gpt_model, 
    api_key=api_key, 
    http_client = client 
)

# Guard rail: Filter out potentially harmful or inappropriate user inputs
def is_safe_input(text):
    unsafe_patterns = UNSAFE_PROMPTS
    for pattern in unsafe_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return False
    return True


system_prompt = SYSTEM_BASE_PROMPT

if "messages" not in st.session_state:
    st.session_state.messages = [SystemMessage(content=system_prompt)]

st.title("Application Development Code Snippet Generator Agent")

# Display chat history
for msg in st.session_state.messages[1:]:  # skip system prompt in display
    if isinstance(msg, HumanMessage):
        st.markdown(f"**You:** {msg.content}")
    else:
        st.markdown(f"**Assistant:**")

        # Extract Python code block from assistant response
        code_blocks = re.findall(r"```python(.*?)```", msg.content, re.DOTALL)
        if code_blocks:
            for i, code in enumerate(code_blocks):
                st.code(code.strip(), language="python")

            # Provide download button for the first code block only (can extend for multiple)
            code_for_download = code_blocks[0].strip()
            b64 = base64.b64encode(code_for_download.encode()).decode()
            href = f'<a href="data:file/python;base64,{b64}" download="snippet.py">⬇️ Download code</a>'
            st.markdown(href, unsafe_allow_html=True)

        # Show rest of the text excluding the code blocks
        # Remove all python code blocks before displaying text
        text_without_code = re.sub(r"```python(.*?)```", "", msg.content, flags=re.DOTALL).strip()
        if text_without_code:
            st.markdown(text_without_code)

# Improved UI: Add a sidebar for settings and instructions
with st.sidebar:
    st.header("Settings")
    st.write("Customize your experience:")
    st.markdown("- Model: azure/genailab-maas-gpt-4o-mini")
    st.markdown("- Base URL: https://genailab.tcs.in")
    st.write("Instructions:")
    st.markdown("Enter your request below and click **Send** to generate code snippets.")

st.markdown("---")
st.subheader("Your Message")
user_input = st.text_input("Enter your message here:")

if 'rerun' not in st.session_state:
    st.session_state['rerun'] = False

def rerun_app():
    st.session_state['rerun'] = not st.session_state['rerun']

if st.button("Send", on_click=rerun_app) and user_input:
    # Append user message
    if(is_safe_input(user_input)):
        st.session_state.messages.append(HumanMessage(content=user_input))

        # Call LLM with full conversation history
        response = llm(st.session_state.messages)
        st.session_state.messages.append(response)
    else:
        from langchain_core.messages import SystemMessage
        st.session_state.messages.append(SystemMessage(content="The Prompt has vulnerable asks, please refine."))

    st.rerun()
