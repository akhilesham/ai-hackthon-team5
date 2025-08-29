from flask import Flask, request, render_template_string
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import re
import streamlit as st
from langchain_openai import ChatOpenAI  
import os  
import httpx 
from langchain_core.messages import HumanMessage

app = Flask(__name__)
client = httpx.Client(verify=False)

# Initialize your LLM client (replace with your real API key and details)
llm = ChatOpenAI(
    base_url="https://genailab.tcs.in",
    model="azure/genailab-maas-gpt-4o-mini",
    api_key="sk-VHkpB_vIIyA1_9lWH3bt1w",
    http_client = client 
)

HTML_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Code Snippet Generator</title>
  <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500&display=swap" rel="stylesheet" />
  <style>
    body {
      font-family: 'Roboto', sans-serif;
      background-color: #f4f7fb;
      margin: 0; padding: 0; color: #333;
    }
    h1, h2 {
      color: #2E8B57;
      font-weight: 500;
    }
    h1 { font-size: 2.5em; margin-bottom: 20px; }
    h2 { font-size: 1.8em; margin-top: 20px; }
    .container {
      max-width: 900px;
      margin: 50px auto;
      padding: 40px;
      background: white;
      border-radius: 12px;
      box-shadow: 0 8px 16px rgba(0,0,0,0.1);
    }
    form {
      display: flex;
      flex-direction: column;
      gap: 20px;
    }
    label {
      font-size: 1.2em;
      font-weight: 500;
      color: #555;
    }
    select, textarea {
      font-size: 1.1em;
      padding: 15px;
      border: 1px solid #ddd;
      border-radius: 8px;
      background-color: #f9f9f9;
      transition: all 0.3s;
      resize: none;
    }
    select:focus, textarea:focus {
      border-color: #4CAF50;
      outline: none;
      background: white;
    }
    textarea {
      min-height: 150px;
    }
    button {
      padding: 15px;
      background: #4CAF50;
      color: white;
      border: none;
      border-radius: 8px;
      font-size: 1.2em;
      cursor: pointer;
      transition: background-color 0.3s;
    }
    button:hover {
      background: #45a049;
    }
    pre {
      background: #2C3E50;
      color: #ecf0f1;
      padding: 20px;
      border-radius: 8px;
      font-family: 'Courier New', monospace;
      font-size: 1.1em;
      white-space: pre-wrap;
      word-wrap: break-word;
      overflow-x: auto;
      box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .results { margin-top: 40px; }
    .error-message {
      color: #D9534F;
      background: #fff0f0;
      padding: 12px;
      border-radius: 5px;
      border: 1px solid #D9534F;
      font-weight: 500;
    }
    @media (max-width: 768px) {
      .container { padding: 20px; }
      h1 { font-size: 2.2em; }
      h2 { font-size: 1.6em; }
      button { font-size: 1em; }
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>Code Snippet Generator</h1>
    <form method="POST">
      <label for="language">Programming Language</label>
      <select id="language" name="language" required>
        <option value="Python" {% if language == "Python" %}selected{% endif %}>Python</option>
        <option value="Java" {% if language == "Java" %}selected{% endif %}>Java</option>
        <option value="Ruby" {% if language == "Ruby" %}selected{% endif %}>Ruby</option>
        <option value="C#" {% if language == "C#" %}selected{% endif %}>C#</option>
        <option value="C++" {% if language == "C++" %}selected{% endif %}>C++</option>
      </select>

      <label for="task">Task Description</label>
      <textarea id="task" name="task" required>{{ task }}</textarea>

      <button type="submit">Generate Code</button>
    </form>

    <div class="results">
      {% if code %}
        <h2>Generated Code</h2>
        <pre>{{ code }}</pre>
      {% endif %}
      {% if explanation %}
        <h2>Explanation</h2>
        <div>{{ explanation|safe }}</div>
      {% endif %}
      {% if error %}
        <div class="error-message">
          <p>Error: {{ error }}</p>
        </div>
      {% endif %}
    </div>
  </div>
</body>
</html>
"""

def extract_code_and_explanation(text):
    # Extract code block wrapped in ```
    code_match = re.search(r"```(?:\w+)?\n([\s\S]*?)```", text)
    code = code_match.group(1).strip() if code_match else "Code not found."
    # Extract explanation outside the code block
    parts = re.split(r"```(?:\w+)?\n[\s\S]*?```", text)
    explanation = parts[1].strip() if len(parts) > 1 else "Explanation not found."
    return code, explanation

def explanation_to_points(explanation_text):
    # Split explanation by new lines or periods into points
    lines = [line.strip() for line in explanation_text.split('\n') if line.strip()]
    if len(lines) <= 1:
        lines = [pt.strip() for pt in explanation_text.split('.') if pt.strip()]
    html_list = "<ul>\n"
    for line in lines:
        html_list += f"  <li>{line}</li>\n"
    html_list += "</ul>"
    return html_list

@app.route("/", methods=["GET", "POST"])
def index():
    code = explanation = error = ""
    language = task = ""

    if request.method == "POST":
        language = request.form.get("language", "")
        task = request.form.get("task", "")

        prompt = (
            f"Write a {language} code snippet that accomplishes the following task:\n"
            f"{task}\n\n"
            f"Also, provide a brief explanation of the code. Format your answer with the code in markdown ``` and explanation after it."
        )
        try:
            prompt_template = PromptTemplate(input_variables=["prompt"], template="{prompt}")
            chain = LLMChain(llm=llm, prompt=prompt_template)
            response_text = chain.run({"prompt": prompt})

            code, raw_explanation = extract_code_and_explanation(response_text)
            explanation = explanation_to_points(raw_explanation)

        except Exception as e:
            error = f"An error occurred: {str(e)}"

    return render_template_string(
        HTML_TEMPLATE,
        code=code,
        explanation=explanation,
        error=error,
        language=language,
        task=task,
    )

if __name__ == "__main__":
    app.run(debug=True)
