# import streamlit as st
# from langchain_openai import ChatOpenAI  
# import os  
# import httpx 
# from langchain_core.messages import HumanMessage

# # from fpdf import FPDF
# import base64
# # Create Client for proxy
# client = httpx.Client(verify=False)


# llm = ChatOpenAI( 
#     base_url="https://genailab.tcs.in" ,
#     model = "azure/genailab-maas-gpt-4o-mini", 
#     api_key="sk-VHkpB_vIIyA1_9lWH3bt1w", 
#     http_client = client 
# ) 

# system_prompt = """
# You are a helpful Python coding assistant. Your job is to:
# 1. Write clean, correct, and well-commented Python code snippets.
# 2. After generating code, provide a clear Chain-of-Thought explanation (why you wrote the code that way).
# 3. Then, ask the user if they want to optimize or expand the snippet.

# Always follow this structure:
# - Confirm the task
# - Generate code
# - Explain reasoning (CoT)
# - Ask for improvement directions
# """

# response = llm([HumanMessage(content=system_prompt)])
# print(response)


#=====================

# import streamlit as st
# from langchain_openai import ChatOpenAI
# from langchain_core.messages import HumanMessage, SystemMessage
# import httpx

# client = httpx.Client(verify=False)

# llm = ChatOpenAI(
#     base_url="https://genailab.tcs.in",
#     model="azure/genailab-maas-gpt-4o-mini",
#     api_key="sk-VHkpB_vIIyA1_9lWH3bt1w",
#     http_client=client
# )

# system_prompt = """
# You are a helpful Python coding assistant. Your job is to:
# 1. Write clean, correct, and well-commented Python code snippets.
# 2. After generating code, provide a clear Chain-of-Thought explanation (why you wrote the code that way).
# 3. Then, ask the user if they want to optimize or expand the snippet.

# Always follow this structure:
# - Confirm the task
# - Generate code
# - Explain reasoning (CoT)
# - Ask for improvement directions
# """

# st.title("Application Development Code Snippet Generator Agent")

# if "messages" not in st.session_state:
#     # Initialize conversation history with system prompt
#     st.session_state.messages = [SystemMessage(content=system_prompt)]

# user_input = st.text_input("Describe the Python code snippet you want:")

# if st.button("Generate Code"):
#     if user_input.strip() == "":
#         st.warning("Please enter a description of the code snippet you want.")
#     else:
#         # Append user message to conversation
#         st.session_state.messages.append(HumanMessage(content=user_input))

#         # Get LLM response
#         response = llm(st.session_state.messages)
#         st.session_state.messages.append(response)

#         # Display output
#         st.markdown("### Assistant response:")
#         st.text(response.content)

#         # Ask for refinement
#         st.session_state.awaiting_feedback = True

# if st.session_state.get("awaiting_feedback", False):
#     refine = st.radio("Do you want to optimize or expand the snippet?", ("No", "Yes"))
#     if refine == "Yes":
#         feedback_input = st.text_area("What kind of optimization or expansion do you want?")
#         if st.button("Refine Code"):
#             if feedback_input.strip():
#                 st.session_state.messages.append(HumanMessage(content=f"Please {feedback_input}"))
#                 response = llm(st.session_state.messages)
#                 st.session_state.messages.append(response)
#                 st.markdown("### Refined assistant response:")
#                 st.text(response.content)
#             else:
#                 st.warning("Please enter your refinement request.")
#     else:
#         st.session_state.awaiting_feedback = False


#===============


import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
import httpx

client = httpx.Client(verify=False)

llm = ChatOpenAI(
    base_url="https://genailab.tcs.in",
    model="azure/genailab-maas-gpt-4o-mini",
    api_key="sk-VHkpB_vIIyA1_9lWH3bt1w",
    http_client=client
)

system_prompt = """
You are a helpful Python coding assistant. Your job is to:
1. Write clean, correct, and well-commented Python code snippets.
2. After generating code, provide a clear Chain-of-Thought explanation (why you wrote the code that way).
3. Then, ask the user if they want to optimize or expand the snippet.
"""

if "messages" not in st.session_state:
    st.session_state.messages = [SystemMessage(content=system_prompt)]

st.title("Application Development Code Snippet Generator Agent")

# Display chat history
for msg in st.session_state.messages[1:]:  # skip system prompt in display
    if isinstance(msg, HumanMessage):
        st.markdown(f"**You:** {msg.content}")
    else:
        st.markdown(f"**Assistant:** {msg.content}")

# Text input for user message
user_input = st.text_input("Enter your message here:")

if st.button("Send") and user_input:
    # Append user message
    st.session_state.messages.append(HumanMessage(content=user_input))

    # Call LLM with full conversation history
    response = llm(st.session_state.messages)
    st.session_state.messages.append(response)

    # Rerun to show updated chat
    st.experimental_rerun()
