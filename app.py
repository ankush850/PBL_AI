from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import google.generativeai as genai
import speech_recognition as sr
import pyttsx3
import threading

app = Flask(__name__)
CORS(app)

GENAI_API_KEY = "AIzaSyA1XruBxEJRNBrKneQtSfvQfQxYtH2sxRc" 
genai.configure(api_key=GENAI_API_KEY)

try:
    model = genai.GenerativeModel("gemini-1.5-flash")


except Exception as e:
    print(f"Error initializing model: {e}")
    model = None  

recognizer = sr.Recognizer()
engine = pyttsx3.init()

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            question = recognizer.recognize_google(audio)
            print("You asked:", question)
            return question
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
            return None
        except sr.RequestError:
            print("Could not request results from Google Speech Recognition service.")
            return None

def speak(text):
    def run():
        engine.say(text)
        engine.runAndWait()
    
    threading.Thread(target=run).start()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("message", "").strip()

    if not user_input:
        return jsonify({"error": "No input provided"}), 400

    if model is None:
        return jsonify({"error": "Model not initialized"}), 500

    try:
        response = model.generate_content(user_input)
        bot_reply = response.text if hasattr(response, 'text') else "Sorry, I couldn't understand."
        speak(bot_reply)

        return jsonify({"response": bot_reply})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/voice", methods=["POST"])
def voice():
    user_input = listen()
    if user_input:
        data = {"message": user_input}
        return chat()
    else:
        return jsonify({"error": "No input recognized"}), 400

if __name__ == "__main__":
    app.run(debug=True)