import google.generativeai as genai
import speech_recognition as sr
import time
from config import Config
import pyttsx3
import threading
import queue

class GeminiService:
    def __init__(self):
        self.model = None
        self.recognizer = sr.Recognizer()
        self.engine = None
        self.last_request_time = 0
        self.min_request_interval = 2  # Minimum seconds between requests
        self.is_speaking = False
        self.speech_queue = queue.Queue()
        self._initialize_model()
        # Start speech queue processor
        self.start_speech_processor()

    def _initialize_model(self):
        try:
            genai.configure(api_key=Config.GENAI_API_KEY)
            self.model = genai.GenerativeModel("gemini-1.5-flash")
        except Exception as e:
            print(f"Error initializing model: {e}")
            self.model = None

    def _wait_for_rate_limit(self):
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        if time_since_last_request < self.min_request_interval:
            time.sleep(self.min_request_interval - time_since_last_request)
        self.last_request_time = time.time()

    def start_speech_processor(self):
        def process_speech_queue():
            while True:
                try:
                    text = self.speech_queue.get()
                    if text is None:  # Shutdown signal
                        break
                    self._speak_text(text)
                    self.speech_queue.task_done()
                except Exception as e:
                    print(f"Error in speech processor: {e}")
                    self.speech_queue.task_done()

        self.speech_processor = threading.Thread(target=process_speech_queue, daemon=True)
        self.speech_processor.start()

    def _speak_text(self, text):
        try:
            self.is_speaking = True
            # Create a new engine instance for each speech
            engine = pyttsx3.init()
            # Set properties for better speech
            engine.setProperty('rate', 150)    # Speed of speech
            engine.setProperty('volume', 1.0)  # Volume (0.0 to 1.0)
            clean_text = text.replace('*', '')
            engine.say(clean_text)
            engine.runAndWait()
        except Exception as e:
            print(f"Error in _speak_text: {e}")
        finally:
            self.is_speaking = False
            try:
                engine.stop()
            except:
                pass

    def listen(self):
        with sr.Microphone() as source:
            print("Listening...")
            audio = self.recognizer.listen(source)
            try:
                question = self.recognizer.recognize_google(audio)
                print("You asked:", question)
                return question
            except sr.UnknownValueError:
                print("Sorry, I could not understand the audio.")
                return None
            except sr.RequestError:
                print("Could not request results from Google Speech Recognition service.")
                return None

    def stop_current_speech(self):
        if self.is_speaking:
            try:
                # Create a new engine to stop the current speech
                temp_engine = pyttsx3.init()
                temp_engine.stop()
            except:
                pass
            self.is_speaking = False
            # Clear the speech queue
            while not self.speech_queue.empty():
                try:
                    self.speech_queue.get_nowait()
                    self.speech_queue.task_done()
                except queue.Empty:
                    break

    def speak(self, text):
        # Stop any ongoing speech
        self.stop_current_speech()
        # Add new text to speech queue
        self.speech_queue.put(text)

    def generate_response(self, user_input):
        if not user_input:
            return None, "No input provided"

        if self.model is None:
            return None, "Model not initialized"

        try:
            # Generate response first
            self._wait_for_rate_limit()
            response = self.model.generate_content(user_input)
            bot_reply = response.text if hasattr(response, 'text') else "Sorry, I couldn't understand."
            
            # Format response for display
            display_reply = f"*{bot_reply}*"
            
            # Start speech in a separate thread
            def speak_response():
                try:
                    self.speak(bot_reply)
                except Exception as e:
                    print(f"Error speaking response: {e}")
            
            threading.Thread(target=speak_response, daemon=True).start()
            
            return display_reply, None
            
        except Exception as e:
            error_message = str(e)
            if "429" in error_message:
                return None, "Rate limit exceeded. Please wait a moment before trying again."
            print(f"Error: {e}")
            return None, str(e) 