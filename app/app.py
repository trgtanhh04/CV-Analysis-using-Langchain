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
    job_title = st.text_input("Enter job title:")
    skills = st.text_input("Enter skills (comma separated):")
    exp_text = st.text_input("Enter experience (comma separated):")

    if st.button("Search"):
        if job_title or skills or exp_text:
            response = requests.get("http://127.0.0.1:8000/candidates/search", params={
                "job_title": job_title,
                "skills": skills.split(",") if skills else None,
                "experience": exp_text.split(",") if exp_text else None
            })
            if response.status_code == 200:
                results = response.json()
                if results:
                    df = pd.DataFrame(results)
                    st.dataframe(df)
                else:
                    st.warning("Không tìm thấy kết quả nào.")
            else:
                st.error(f"Lỗi: {response.text}")

# streamlit run app/app.py