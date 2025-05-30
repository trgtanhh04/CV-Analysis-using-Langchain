import os
import json
import fitz  # PyMuPDF for PDF extraction
from langchain.llms import openai
from langchain.prompts import PromptTemplate
from config.config import OPENAI_API_KEY, LLM_MODEL_NAME

llm = openai.OpenAI(
    model=LLM_MODEL_NAME,
    temperature=0.2,
    api_key=OPENAI_API_KEY
)

prompt_template = """
Extract the following candidate information fields from the CV content (as plain text) below in the exact JSON format:
{
"full_name": "...",
"email": "...",
"phone": "...",
"education": [
    {
    "degree": "...",
    "university": "...",
    "start_year": ...,
    "end_year": ...
    }
],
"experience": [
    {
    "job_title": "...",
    "company": "...",
    "start_date": "...",
    "end_date": "...",
    "description": "..."
    }
],
"skills": ["...", "..."],
"certifications": [
    {
    "certificate_name": "...",
    "organization": "..."
    }
],
"languages": ["...", "..."]
}
Only return the JSON content. Do not include any explanations.  
If any field cannot be found, set its value to null or an empty array.

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
    prompt = PromptTemplate(
        input_variables=["text"],
        template=prompt_template
    ).format(text=text)
    response = llm(prompt)
    try:
        candidate_info = json.loads(response)
    except Exception as e:
        print(f"Error parsing JSON: {e}\nLLM output: {response}")
        candidate_info = {}
    return candidate_info