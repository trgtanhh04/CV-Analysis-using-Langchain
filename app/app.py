import streamlit as st
import os
import pandas as pd
from dotenv import load_dotenv
import requests

load_dotenv()

st.set_page_config(
    page_title="CV Analytics", 
    layout="wide"
)

st.markdown("### CV Analytics")
options = ["Upload CV", "Search Candidates"]
choice = st.radio("Select an option:", options)

if choice == "Upload CV":
    upload_file = st.file_uploader("Chọn 1 file CV PDF", type=["pdf"]) 
    if upload_file is not None:
        if st.button("Upload"):
            files = {"file": (upload_file.name, upload_file, "application/pdf")}
            response = requests.post("http://127.0.0.1:8000/candidates/", files=files)  
            if response.status_code == 200:
                st.success("Upload thành công!")
                st.json(response.json())
            else:
                st.error(f"Lỗi: {response.text}")
            
elif choice == "Search Candidates":
    st.markdown("#### Search Candidates")
    query = st.text_input("Enter search query:")
    skills = st.text_input("Enter skills (comma separated):")
    job_title = st.text_input("Enter job title:")
    

# streamlit run app/app.py