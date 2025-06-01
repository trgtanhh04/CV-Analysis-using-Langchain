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

# st.markdown("### CV Analytics")
# options = ["Upload CV", "Search Candidates"]
# choice = st.radio("Select an option:", options)

# if choice == "Upload CV":
#     upload_file = st.file_uploader(
#         "Choose one or multiple CV PDF files", 
#         type=["pdf"], 
#         accept_multiple_files=True
#     ) 
#     if upload_file is not None:
#         if st.button("Upload"):
#             success, fail = 0, 0
#             for file in upload_file:
#                 files = {"file": (file.name, file, "application/pdf")}
#                 response = requests.post("http://127.0.0.1:8000/candidates/", files=files)
#                 if response.status_code == 200:
#                     success += 1
#                     st.success(f"Upload successful: {file.name}")
#                     st.json(response.json())
#                 else:
#                     fail += 1
#                     st.error(f"Upload failed: {file.name} - {response.text}")
#             st.success(f"Upload successful: {success}, Failed: {fail}")

# elif choice == "Search Candidates":
#     st.markdown("#### Search Candidates")
#     job_title = st.text_input("Enter job title:")
#     skills = st.text_input("Enter skills (comma separated):")
#     exp_text = st.text_input("Enter experience (comma separated):")

#     if st.button("Search"):
#         if job_title or skills or exp_text:
#             response = requests.get("http://127.0.0.1:8000/candidates/search", params={
#                 "job_title": job_title,
#                 "skills": skills.split(",") if skills else None,
#                 "experience": exp_text.split(",") if exp_text else None
#             })
#             if response.status_code == 200:
#                 results = response.json()
#                 if results:
#                     for item in results:
#                         item['education'] = ", ".join([
#                             f"{edu.get('degree', 'N/A')} tại {edu.get('university', 'N/A')} ({edu.get('start_year', 'Unknown')} - {edu.get('end_year', 'Unknown')})"
#                             for edu in item.get('education', [])
#                         ])

#                         item['experience'] = ", ".join([
#                             f"{exp.get('job_title', 'N/A')} tại {exp.get('company', 'N/A')} ({exp.get('start_date', 'Unknown')} - {exp.get('end_date', 'Unknown')})"
#                             for exp in item.get('experience', [])
#                         ])

#                         item['certifications'] = ", ".join([
#                             f"{cert.get('certificate_name', 'N/A')} ({cert.get('organization', 'N/A')})"
#                             for cert in item.get('certifications', [])
#                         ])

#                         item['languages'] = ", ".join(item.get('languages', []))

#                         item['skills'] = ", ".join(item.get('skills', []))

#                     df = pd.DataFrame(results)
#                     st.dataframe(df)
#                 else:
#                     st.warning("Not found.")
#             else:
#                 st.error(f"Error: {response.text}")


API_URL = "http://127.0.0.1:8000"

def upload_cv(files):
    success, fail = 0, 0
    results = []
    for file in files:
        files_data = {"file": (file.name, file, "application/pdf")}
        response = requests.post(f"{API_URL}/candidates/", files=files_data)
        if response.status_code == 200:
            success += 1
            results.append(response.json())
        else:
            fail += 1
            st.error(f"Upload failed: {file.name} - {response.text}")
    return success, fail, results

def search_candidates(job_title, skills, experience):
    params = {
        "job_title": job_title,
        "skills": [s.strip() for s in skills.split(",")] if skills else None,
        "experience": [e.strip() for e in experience.split(",")] if experience else None
    }
    response = requests.get(f"{API_URL}/candidates/search", params=params)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error: {response.text}")
        return []

def candidate_detail(candidate):
    st.subheader(f"🧑‍💼 {candidate.get('name', 'N/A')}")
    st.write(f"**Email**: {candidate.get('email', 'N/A')}")
    st.write(f"**Phone**: {candidate.get('phone', 'N/A')}")
    st.write(f"**Skills**: {', '.join(candidate.get('skills', []))}")

    certifications = [
        f"{c.get('certificate_name', '')} ({c.get('organization', '')})"
        for c in candidate.get('certifications', [])
    ]
    st.write(f"**Certifications**: {', '.join(certifications)}")

    st.write("### 🎓 Education")
    for edu in candidate.get('education', []):
        st.markdown(f"- {edu.get('degree', 'N/A')} tại {edu.get('university', 'N/A')} ({edu.get('start_year', 'Unknown')} - {edu.get('end_year', 'Unknown')})")
    
    st.write("### 💼 Experience")
    for exp in candidate.get('experience', []):
        st.markdown(f"- {exp.get('job_title', 'N/A')} tại {exp.get('company', 'N/A')} ({exp.get('start_date', 'Unknown')} - {exp.get('end_date', 'Unknown')})")
        if exp.get('description'):
            st.caption(exp.get('description'))

def main():
    st.title("📄 CV Analytics System")
    st.write("Efficiently upload, analyze, and search candidate profiles.")
    
    st.sidebar.header("Main Menu")
    menu = st.sidebar.radio("Choose action", ["Upload CV", "Search Candidates"])

    if menu == "Upload CV":
        st.header("📤 Upload CVs")
        uploaded_files = st.file_uploader(
            "Chọn nhiều file CV PDF", 
            type=["pdf"], 
            accept_multiple_files=True
        )
        if uploaded_files:
            if st.button("Upload"):
                with st.spinner("Uploading and analyzing..."):
                    success, fail, results = upload_cv(uploaded_files)
                    st.success(f"Upload thành công: {success}, Thất bại: {fail}")
                    if results:
                        st.write("Thông tin CV mới upload:")
                        for candidate in results:
                            st.json(candidate)
    elif menu == "Search Candidates":
        st.header("🔎 Search Candidates")
        with st.sidebar:
            job_title = st.text_input("Job Title")
            skills = st.text_input("Skills (comma separated)")
            experience = st.text_input("Experience (comma separated)")
            search_btn = st.button("Search", key="search_btn")
        
        if search_btn or st.session_state.get("searched", False):
            st.session_state["searched"] = True
            with st.spinner("Searching..."):
                results = search_candidates(job_title, skills, experience)
                st.session_state["search_results"] = results
        
        # Display search results or detail
        if "selected_candidate" in st.session_state and st.session_state["selected_candidate"] is not None:
            idx = st.session_state["selected_candidate"]
            candidate = st.session_state["search_results"][idx]
            candidate_detail(candidate)
            if st.button("Back to list"):
                st.session_state["selected_candidate"] = None
                st.rerun()
        elif "search_results" in st.session_state and st.session_state["search_results"]:
            st.write("### 📋 Danh sách ứng viên phù hợp")
            results = st.session_state["search_results"]
            for idx, row in enumerate(results):
                col1, col2 = st.columns([1, 5])
                with col1:
                    st.markdown(f"#### {idx+1}")
                with col2:
                    st.markdown(f"**Tên:** {row.get('name', 'N/A')}")
                    st.markdown(f"**Email:** {row.get('email', 'N/A')}")
                    st.markdown(f"**Kỹ năng:** {', '.join(row.get('skills', []))}")
                    if st.button("Xem chi tiết", key=f"detail_{idx}"):
                        st.session_state["selected_candidate"] = idx
                        st.rerun()
        elif st.session_state.get("searched"):
            st.warning("Không tìm thấy ứng viên phù hợp.")

if __name__ == "__main__":
    main()


# streamlit run app/app.py