# 🧠 Document Research & Theme Identifier Chatbot

A Gen-AI-powered application that analyzes PDFs and images to extract and summarize key legal or regulatory themes. Users can upload multiple documents, ask questions, and receive page-level answers with citations and concise theme-based summaries.

---

## 🚀 Features

- 📤 Upload 75+ PDF or image files (JPG, PNG, etc.)
- 🧾 Extracts text from scanned images using Tesseract OCR
- 🔍 Embeds and searches text using Sentence Transformers + FAISS
- 🧠 Summarizes key themes using Hugging Face Zephyr 7B API
- 📑 Page-level document citations with answers
- ✅ Streamlit frontend with Flask backend integration

---

## 🏗️ Project Structure

 chatbot_theme_identifier/
├── backend/
│ ├── app/
│ │ ├── api/
│ │ ├── core/
│ │ ├── models/
│ │ ├── services/
│ │ └── main.py
│ └── requirements.txt
├── frontend/
│ ├── streamlit_app.py
│ └── requirements.txt
├── .env.example
└── README.md
## Install Dependencies
pip install -r backend/requirements.txt
pip install -r frontend/requirements.txt
## 🧠 Setup Tesseract OCR (For Image Support)
- Download and install Tesseract: https://github.com/tesseract-ocr/tesseract
- pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

## 🔐 Environment Variables
- Create a .env file inside the backend/ folder:
- HUGGINGFACE_API_KEY=hf_your_actual_token_here

## ▶️ Running the Project
- Start the Flask Backend
 - python -m backend.app.main
-  Start the Streamlit Frontend
-  streamlit run frontend/streamlit_app.py



## 🧠 Theme Summary
Theme 1 – Regulatory Non-Compliance: DOC001, DOC002  
Violation of SEBI norms and disclosure obligations.

Theme 2 – Penalty Justification: DOC001  
Fines imposed under Clause 15 explained and justified.


