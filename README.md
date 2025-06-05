This project is a PDF Summarizer powered by Google Gemini API. It allows users to upload PDF documents and receive concise summaries using advanced generative AI. This project was developed as part of a Project-Based Learning (PBL) initiative.

🚀 Features
📄 Upload and parse PDF files

✨ Summarize content using Gemini API

🧠 Uses generative AI to understand and condense large texts

🌐 Simple Flask-based web interface



🔥 Flask – web framework

📄 PyMuPDF – for PDF parsing

🌐 Google Gemini API – for AI summarization

🔑 Setup Instructions
Clone the Repository

bash
Copy
Edit
git clone https://github.com/ankush850/PBL_AI.git
cd PBL_AI
Create Virtual Environment

bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
Install Dependencies

bash
Copy
Edit
pip install -r requirements.txt
Set Gemini API Key

Create a .env file in the root folder:

env
Copy
Edit
GEMINI_API_KEY=your_api_key_here
Run the Application

bash
Copy
Edit
python run.py
Open in Browser

Navigate to http://127.0.0.1:5000/ to use the app.

📌 Example Use Case
Upload a PDF (e.g., research paper or notes).

The app extracts the content.

Gemini API summarizes the content in natural language.

Summary is shown on the web interface.

👨‍💻 Contributors
@ankush850

@Shivans2002

@Jay2849
