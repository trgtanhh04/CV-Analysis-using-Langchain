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
                    for item in results:
                        item['education'] = ", ".join([
                            f"{edu.get('degree', 'N/A')} tại {edu.get('university', 'N/A')} ({edu.get('start_year', 'Unknown')} - {edu.get('end_year', 'Unknown')})"
                            for edu in item.get('education', [])
                        ])

                        item['experience'] = ", ".join([
                            f"{exp.get('job_title', 'N/A')} tại {exp.get('company', 'N/A')} ({exp.get('start_date', 'Unknown')} - {exp.get('end_date', 'Unknown')})"
                            for exp in item.get('experience', [])
                        ])

                        item['certifications'] = ", ".join([
                            f"{cert.get('certificate_name', 'N/A')} ({cert.get('organization', 'N/A')})"
                            for cert in item.get('certifications', [])
                        ])

                        item['languages'] = ", ".join(item.get('languages', []))

                        item['skills'] = ", ".join(item.get('skills', []))

                    df = pd.DataFrame(results)
                    st.dataframe(df)
                else:
                    st.warning("Không tìm thấy kết quả nào.")
            else:
                st.error(f"Lỗi: {response.text}")

# streamlit run app/app.py