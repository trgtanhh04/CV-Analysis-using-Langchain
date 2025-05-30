import os
import json
import fitz  # PyMuPDF for PDF extraction
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()
from config.config import OPENAI_API_KEY, LLM_MODEL_NAME

llm = ChatOpenAI(
    model_name=LLM_MODEL_NAME,  # vd: "gpt-3.5-turbo"
    temperature=0.2,
    openai_api_key=OPENAI_API_KEY
)

prompt_template = """
Extract the following candidate information fields from the CV content (as plain text) below in the exact JSON format:
{{
"full_name": "...",
"email": "...",
"phone": "...",
"education": [
    {{
    "degree": "...",
    "university": "...",
    "start_year": ...,
    "end_year": ...
    }}
],
"experience": [
    {{
    "job_title": "...",
    "company": "...",
    "start_date": "...",
    "end_date": "...",
    "description": "..."
    }}
],

"skills": ["...", "..."],
"certifications": [
    {{
    "certificate_name": "...",
    "organization": "..."
    }}
],
"languages": ["...", "..."]
}}

⚠️ Only include **real work experience** (e.g. internships, jobs at companies, freelance work) in the "experience" field.  
⚠️ **Do not include personal, academic, or side projects** in the experience section.

Only return the JSON content. Do not include any explanation.  
If any field cannot be found, set it to null or empty array.

CV content:
{text}
"""



def extract_text_from_pdf(file_path: str) -> str:
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text.strip()


def extract_info(text: str) -> dict:
    prompt = prompt_template.format(text=text)
    messages = [HumanMessage(content=prompt)]
    response = llm(messages)
    
    try:
        candidate_info = json.loads(response.content)

        # Lọc experience: bỏ các mục có company = None hoặc ""
        if "experience" in candidate_info and isinstance(candidate_info["experience"], list):
            filtered_exp = []
            for exp in candidate_info["experience"]:
                company = exp.get("company")
                if company not in [None, ""]:
                    filtered_exp.append(exp)
            candidate_info["experience"] = filtered_exp

    except Exception as e:
        print(f"Error parsing JSON: {e}\nLLM output: {response.content}")
        candidate_info = {}

    return candidate_info
