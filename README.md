# 📄 PDF Summarizer using Gemini API

A simple web application that lets you upload PDF files and get short, clear summaries using **Google Gemini API**. Built with **Flask** and **Python**.

---

## 🚀 What this project does

- Upload a PDF file  
- Extract text from the PDF  
- Send text to Gemini API  
- Get an AI-generated summary  

---

## ✨ Features

- PDF upload support  
- Automatic text extraction  
- Fast AI summarization  
- Simple Flask web interface  

---

## 🧰 Tech Stack

- Python  
- Flask  
- PyMuPDF (PDF text extraction)  
- Google Gemini API  
- python-dotenv  

---

## 📁 Project Structure

```
PDF-Summarizer-using-Gemini-API/
│
├── app/
│   ├── __init__.py
│   ├── routes.py
│   └── utils.py
│
├── templates/
│   └── index.html
│
├── static/
│
├── run.py
├── test_pdf_upload.py
├── requirements.txt
└── .env
```

---

## ⚙️ Setup (Run Locally)

### 1️⃣ Clone the repository

```bash
git clone https://github.com/ankush850/-PDF-Summarizer-using-Gemini-API.git
cd -PDF-Summarizer-using-Gemini-API
```

---

### 2️⃣ Create virtual environment

```bash
python -m venv venv
```

Activate it:

**Windows**
```bash
venv\Scripts\activate
```

**Linux / macOS**
```bash
source venv/bin/activate
```

---

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Add Gemini API Key

Create a `.env` file in the root folder:

```env
GEMINI_API_KEY=your_api_key_here
```

---

## ▶️ Run the Application

```bash
python run.py
```

Open browser and go to:

```
http://127.0.0.1:5000/
```

---

## 🧪 Test PDF Upload

```bash
python test_pdf_upload.py
```

---

## ⚠️ Notes

- Internet connection is required  
- Large PDFs may take more time  
- Invalid API key will cause summarization failure  

---

## 👥 Contributors

- Ankush Rawat  
- Shivansh  
- Jay  

---
