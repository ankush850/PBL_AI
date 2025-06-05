import re
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from PyPDF2 import PdfReader
from werkzeug.datastructures import FileStorage

# Ensure nltk data is downloaded once
def download_nltk_data():
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords')

download_nltk_data()

class PDFService:
    @staticmethod
    def extract_text_from_pdf(pdf_path):
        text = ""
        try:
            with open(pdf_path, 'rb') as file:
                reader = PdfReader(file)
                for page in reader.pages:
                    content = page.extract_text()
                    if content:
                        text += content
        except Exception as e:
            print("Error reading PDF:", e)
        return text

    @staticmethod
    def generate_summary(text, max_sentences=5):
        stop_words = set(stopwords.words("english"))
        words = word_tokenize(text.lower())
        freq_table = {}

        for word in words:
            if word not in stop_words and word.isalnum():
                freq_table[word] = freq_table.get(word, 0) + 1

        sentences = sent_tokenize(text)
        sentence_scores = {}

        for sentence in sentences:
            sentence_lower = sentence.lower()
            for word in freq_table:
                if word in sentence_lower:
                    sentence_scores[sentence] = sentence_scores.get(sentence, 0) + freq_table[word]

        # Sort sentences by score and return top `max_sentences`
        summarized_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:max_sentences]
        return ' '.join(summarized_sentences)

    @staticmethod
    def process_pdf(pdf_input):
        """Wrapper method to extract and summarize PDF content"""
        if isinstance(pdf_input, FileStorage):
            text = PDFService.extract_text(pdf_input)
        else:
            text = PDFService.extract_text_from_pdf(pdf_input)
        summary = PDFService.generate_summary(text)
        return summary

    @staticmethod
    def extract_text(file):
        try:
            reader = PdfReader(file.stream)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            return text
        except Exception as e:
            print(f"Error reading PDF: {e}")
            return ""
