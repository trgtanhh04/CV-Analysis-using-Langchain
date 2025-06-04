# CV Analysis using Langchain
**Building an Intelligent CV Analysis and Candidate Database System**

## Mục lục
- [Giới thiệu](#giới-thiệu)
- [Công nghệ sử dụng](#công-nghệ-sử-dụng)
- [Workflow hệ thống](#workflow-hệ-thống)
- [Các chức năng chính](#các-chức-năng-chính)
- [Kiến trúc dữ liệu & Database](#kiến-trúc-dữ-liệu--database)
- [API tìm kiếm ứng viên](#api-tìm-kiếm-ứng-viên)
- [Triển khai hệ thống](#triển-khai-hệ-thống)
- [Hướng dẫn cài đặt & sử dụng](#hướng-dẫn-cài-đặt--sử-dụng)
---

## Giới thiệu

CV Analysis using Langchain là hệ thống phân tích, quản lý & tìm kiếm ứng viên thông minh, hỗ trợ doanh nghiệp và nhà tuyển dụng tự động hóa quy trình xử lý hồ sơ (CV). Hệ thống sử dụng AI, NLP & các công nghệ hiện đại để trích xuất, lưu trữ, tìm kiếm và so sánh hồ sơ ứng viên từ file PDF.

## Công nghệ sử dụng

- **Programming Language:** Python
- **Backend Framework:** FastAPI
- **PDF Processing & NLP:** PyMuPDF
- **AI & LLM:** Langchain, OpenAI API (gpt-3.5-turbo)
- **Vector Database:** FAISS
- **ORM:** SQLAlchemy
- **Database:** PostgreSQL
- **Frontend:** Streamlit
- **Cloud Platform:** 
  - Backend: Render
  - Frontend: Streamlit Cloud

## Workflow hệ thống
<p align="center">
  <img src="https://raw.githubusercontent.com/trgtanhh04/CV-Analysis-using-Langchain/main/images/work_flow.png" width="100%" alt="airflow">
</p>


1. **Người dùng tải lên CV (PDF)**  
   - Hệ thống tiếp nhận file PDF từ người dùng qua giao diện web.

2. **Xử lý nội dung CV bằng LangChain & LLM**  
   - LangChain & OpenAI API phân tích, trích xuất thông tin ứng viên (cá nhân, học vấn, kinh nghiệm, kỹ năng, chứng chỉ, ngôn ngữ...) ra định dạng JSON chuẩn.

3. **Sinh Embedding & Lưu trữ dữ liệu**  
   - Chuyển thông tin vừa trích xuất thành vector embedding (bằng FAISS) và lưu vào Vector Database để phục vụ tìm kiếm nhanh, đồng thời lưu dữ liệu gốc vào PostgreSQL.

4. **Tìm kiếm ứng viên**  
   - Khi có nhu cầu tìm kiếm, hệ thống lọc ứng viên bằng truy vấn SQL trên PostgreSQL, sau đó sử dụng vector similarity để xếp hạng độ tương đồng và trả về top ứng viên phù hợp nhất.

## Các chức năng chính

- Upload & trích xuất nội dung CV từ PDF (hỗ trợ nhiều file, nhiều ngôn ngữ).
- Chuẩn hóa & lưu trữ thông tin ứng viên ở dạng JSON & Database.
- API tìm kiếm ứng viên (theo job_title, kỹ năng...).
- Xem chi tiết hồ sơ ứng viên.
- Triển khai hệ thống lên Cloud (backend & frontend độc lập).

## Kiến trúc dữ liệu & Database
<p align="center">
  <img src="https://raw.githubusercontent.com/trgtanhh04/CV-Analysis-using-Langchain/main/images/erd_for_db.png" width="100%" alt="airflow">
</p>

- **ORM:** Sử dụng SQLAlchemy, các bảng được ánh xạ thành các class Python, hỗ trợ cascade delete cho quan hệ 1-nhiều (Education, Experience, Certifications...).
- **Chuẩn hóa bảng Skills & Languages** giúp tránh trùng lặp, dễ mở rộng & phân tích.

### Ví dụ dữ liệu ứng viên (JSON mẫu)
```json
{
  "full_name": "Nguyen Van A",
  "email": "nguyenvana@example.com",
  "phone": "0912345678",
  "job_title": "Backend Developer",
  "education": [
    {
      "degree": "Cử nhân Khoa học Máy tính",
      "university": "ĐH Khoa học Tự nhiên",
      "start_year": 2022,
      "end_year": 2026
    }
  ],
  "experience": [
    {
      "job_title": "Intern Python Developer",
      "company": "FPT Software",
      "start_date": "06/2023",
      "end_date": "08/2023",
      "description": "Tham gia dự án AI chatbot bằng Flask."
    }
  ],
  "skills": ["Python", "Machine Learning", "SQL", "Git", "Linux"],
  "certifications": [
    {
      "certificate_name": "Google Data Analytics",
      "organization": "Coursera"
    }
  ],
  "languages": ["English", "Vietnamese"]
}
```

## API tìm kiếm ứng viên
<p align="center">
  <img src="https://raw.githubusercontent.com/trgtanhh04/CV-Analysis-using-Langchain/main/images/ui_search_candidate.png" width="100%" alt="airflow">
</p>
<p align="center">
  <img src="https://raw.githubusercontent.com/trgtanhh04/CV-Analysis-using-Langchain/main/images/ui_detail_candidates.png" width="100%" alt="airflow">
</p>

- **Thêm mới/cập nhật hồ sơ từ file PDF**
- **Tìm kiếm theo:**  
  - Vị trí ứng tuyển (`job_title`)
  - Kỹ năng (`skills`)
- **Kết quả:**  
  - Trả về top 5 ứng viên có độ tương đồng cao nhất, dữ liệu ở dạng JSON, xem chi tiết từng ứng viên trên web.

## Triển khai hệ thống

- **Backend:** FastAPI + PostgreSQL, deploy trên Render.
- **Frontend:** Streamlit, deploy trên Streamlit Cloud.

**Demo & liên kết:**
- GitHub: [https://github.com/trgtanhh04/CV-Analysis-using-Langchain.git](https://github.com/trgtanhh04/CV-Analysis-using-Langchain.git)
- Thử nghiệm Streamlit: [https://cv-analysis-using-langchain.streamlit.app/](https://cv-analysis-using-langchain.streamlit.app/)
- Video demo: (bổ sung link Google Drive nếu có)

## Hướng dẫn cài đặt & sử dụng

### 1. Clone project về máy
```bash
git clone https://github.com/trgtanhh04/CV-Analysis-using-Langchain.git
```

### 2. Khởi chạy Docker cho PostgreSQL & PgAdmin4
```bash
docker compose up -d
```

### 3. Khởi chạy FastAPI (backend)
```bash
uvicorn scripts.main:app --reload
```

### 4. Khởi chạy frontend bằng Streamlit
```bash
streamlit run app/app.py
```

**Lưu ý:**  
- OpenAI API key không được public vì lý do bảo mật.  
- Bạn cần tự tạo [API key tại đây](https://platform.openai.com/account/api-keys) và thêm vào code trước khi chạy.

