import pyttsx3
import threading
import os
import sys

class VoiceEngine:
    def __init__(self):
        self.tts_engine = None
        self._init_tts()

    def _init_tts(self):
        try:
            self.tts_engine = pyttsx3.init()
            # Set voice property to female or distinct voice if available
            voices = self.tts_engine.getProperty('voices')
            if voices:
                # Default to index 0 or 1
                for voice in voices:
                    if "zira" in voice.name.lower() or "david" in voice.name.lower() or "hazel" in voice.name.lower():
                        self.tts_engine.setProperty('voice', voice.id)
                        break
            self.tts_engine.setProperty('rate', 180) # Speaking speed
            self.tts_engine.setProperty('volume', 1.0) # Volume level 0.0 to 1.0
        except Exception as e:
            print(f"[VoiceEngine] pyttsx3 initialization warning: {e}")
            self.tts_engine = None

    def speak(self, text):
        """Synthesize and play speech output synchronously or in a thread."""
        if not text:
            return

        def _speak_thread():
            try:
                if self.tts_engine:
                    self.tts_engine.say(text)
                    self.tts_engine.runAndWait()
                else:
                    print(f"[JARVIS VOICE OUTPUT]: {text}")
            except Exception as e:
                print(f"[VoiceEngine] Speech error: {e}")

        # Run speech in thread to avoid blocking Flask API responses
        threading.Thread(target=_speak_thread, daemon=True).start()

    def listen(self):
        """Capture microphone input using SpeechRecognition."""
        try:
            import speech_recognition as sr
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.8)
                print("[VoiceEngine] Listening for user speech...")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                text = recognizer.recognize_google(audio)
                print(f"[VoiceEngine] Heard: {text}")
                return {"success": True, "text": text}
        except ImportError:
            return {"success": False, "error": "speech_recognition module or PyAudio not installed"}
        except Exception as e:
            return {"success": False, "error": str(e)}
