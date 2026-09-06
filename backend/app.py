from flask import Flask, request, jsonify
from flask_cors import CORS
import time
import os
import sys
import tempfile
import uuid

from config import Config
from core.llm import JARVISEngine
from core.voice import VoiceEngine
from core.automation import SystemAutomation

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

# Initialize Core Services
jarvis_engine = JARVISEngine()
voice_engine = VoiceEngine()
system_automation = SystemAutomation()

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "healthy",
        "system": "JARVIS AI Voice & Automation Assistant",
        "version": "1.0.0",
        "voice_engine": "ready"
    })

@app.route('/api/system-status', methods=['GET'])
def get_system_status():
    """Returns HUD system telemetry for frontend charts and status indicators."""
    try:
        stats = system_automation.get_system_stats()
        return jsonify({
            "status": "success",
            "data": stats
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/command', methods=['POST'])
def handle_command():
    """Main route for user text and voice commands."""
    try:
        data = request.json or {}
        command_text = data.get('command', '')
        should_speak = data.get('speak', True)

        result = jarvis_engine.process_command(command_text)

        # Trigger speech output if enabled
        if should_speak and result.get('response'):
            voice_engine.speak(result['response'])

        return jsonify({
            "status": "success",
            "data": result
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/voice-audio', methods=['POST'])
def handle_voice_audio():
    """Process uploaded microphone WAV audio recording directly from browser."""
    if 'audio' not in request.files:
        return jsonify({"status": "error", "message": "No audio file attached"}), 400

    audio_file = request.files['audio']
    should_speak = request.form.get('speak', 'true').lower() == 'true'

    temp_path = os.path.join(tempfile.gettempdir(), f"jarvis_voice_{uuid.uuid4().hex}.wav")
    audio_file.save(temp_path)

    try:
        import speech_recognition as sr
        recognizer = sr.Recognizer()
        with sr.AudioFile(temp_path) as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.3)
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)

        if not text or not text.strip():
            return jsonify({
                "status": "warning",
                "message": "Speech was too quiet or could not be recognized. Please try speaking closer to the microphone.",
                "heard_text": ""
            })

        result = jarvis_engine.process_command(text)

        if should_speak and result.get('response'):
            voice_engine.speak(result['response'])

        return jsonify({
            "status": "success",
            "heard_text": text,
            "data": result
        })
    except sr.UnknownValueError:
        return jsonify({
            "status": "warning",
            "message": "Could not understand audio clearly. Please try speaking again.",
            "heard_text": ""
        })
    except sr.RequestError as e:
        return jsonify({
            "status": "error",
            "message": f"Speech recognition service error: {str(e)}",
            "heard_text": ""
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception:
                pass

@app.route('/api/voice-listen', methods=['POST'])
def voice_listen():
    """Trigger server-side microphone listening if PyAudio is present."""
    try:
        listen_res = voice_engine.listen()
        if not listen_res.get('success'):
            return jsonify({
                "status": "warning",
                "message": listen_res.get('error', 'Could not process audio from microphone'),
                "text": ""
            })

        heard_text = listen_res['text']
        result = jarvis_engine.process_command(heard_text)

        # Speak back
        voice_engine.speak(result['response'])

        return jsonify({
            "status": "success",
            "heard_text": heard_text,
            "data": result
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/speak', methods=['POST'])
def trigger_speech():
    """Trigger explicit TTS voice utterance."""
    try:
        data = request.json or {}
        text = data.get('text', '')
        if text:
            voice_engine.speak(text)
            return jsonify({"status": "success", "message": f"Speaking: '{text}'"})
        return jsonify({"status": "error", "message": "No text provided"}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/quick-actions', methods=['GET'])
def get_quick_actions():
    """List preset HUD shortcut commands."""
    actions = [
        {"id": 1, "label": "Open Chrome", "command": "open chrome", "category": "app"},
        {"id": 2, "label": "VS Code", "command": "open code", "category": "app"},
        {"id": 3, "label": "Calculator", "command": "open calculator", "category": "app"},
        {"id": 4, "label": "System Telemetry", "command": "system stats", "category": "system"},
        {"id": 5, "label": "Weather Report", "command": "weather", "category": "info"},
        {"id": 6, "label": "Volume Up", "command": "volume up", "category": "system"},
        {"id": 7, "label": "Volume Down", "command": "volume down", "category": "system"},
        {"id": 8, "label": "Current Time", "command": "what time is it", "category": "info"}
    ]
    return jsonify({"status": "success", "actions": actions})

if __name__ == '__main__':
    print(f"JARVIS AI Backend listening on http://{Config.HOST}:{Config.PORT}")
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
