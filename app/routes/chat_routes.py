from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from app.services.gemini_service import GeminiService
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import traceback

# Ensure required NLTK data is available
nltk.download('punkt')
nltk.download('stopwords')

chat = Blueprint('chat', __name__)
gemini_service = GeminiService()

@chat.route("/")
def index():
    return redirect(url_for('chat.chat_page'))

@chat.route("/chat")
def chat_page():
    return render_template('chat.html')

@chat.route('/api/chat', methods=['POST'])
def chat_message():
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({'error': 'No message provided'}), 400
    
    try:
        response = gemini_service.generate_response(data['message'])
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@chat.route('/api/voice', methods=['POST'])
def voice_input():
    try:
        response = gemini_service.handle_voice_input()
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@chat.route('/api/summarize', methods=['POST'])
def summarize():
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'Missing "text" in request'}), 400

        text = data['text']
        stopWords = set(stopwords.words("english"))
        words = word_tokenize(text)

        freqTable = {}
        for word in words:
            word = word.lower()
            if word not in stopWords:
                freqTable[word] = freqTable.get(word, 0) + 1

        sentences = sent_tokenize(text)
        sentenceValue = {}
        for sentence in sentences:
            for word, freq in freqTable.items():
                if word in sentence.lower():
                    sentenceValue[sentence] = sentenceValue.get(sentence, 0) + freq

        # Get summary (top 30% scored sentences)
        summary_sentences = sorted(sentenceValue, key=sentenceValue.get, reverse=True)
        summary = ' '.join(summary_sentences[:max(1, int(len(sentences) * 0.3))])

        return jsonify({'summary': summary})

    except Exception as e:
        print("Error:", e)
        traceback.print_exc()
        return jsonify({'error': 'Internal Server Error'}), 500
