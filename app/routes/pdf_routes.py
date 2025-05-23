from flask import Blueprint, request, jsonify, render_template
from werkzeug.utils import secure_filename
import os
from app.services.pdf_service import PDFService
from config import Config

pdf = Blueprint('pdf', __name__)
pdf_service = PDFService()

@pdf.route('/')
def index():
    return render_template('index.html')

@pdf.route('/api/summarize', methods=['POST'])
def summarize_pdf():
    """Handle PDF upload and summarization."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not file.filename.endswith('.pdf'):
        return jsonify({'error': 'File must be a PDF'}), 400
    
    try:
        # Extract text and generate summary separately to get lengths
        text = pdf_service.extract_text(file)
        summary = pdf_service.generate_summary(text)
        response = {
            'summary': summary,
            'original_length': len(text),
            'summary_length': len(summary)
        }
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
