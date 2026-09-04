# JARVIS — Next-Gen AI Voice & System Automation Assistant

A futuristic, high-performance **JARVIS Voice & Text AI Assistant** built with Python Flask and a modern React HUD dashboard interface inspired by Tony Stark's Iron Man UI.

## Features

- 🎙️ **Real-time Voice & Text Commands**: Speech Recognition (Google Speech-to-Text) and Text-to-Speech (pyttsx3) synthesis.
- ⚡ **Futuristic React HUD UI**: Glowing SVG ARC Reactor core visualizer, cyberpunk terminal log transcript, and live system telemetry tiles.
- 🖥️ **Windows System Automation**: Launch applications (Chrome, VS Code, Calculator, Notepad, CMD, Spotify, YouTube), adjust system volume, capture screenshots, and query system stats (CPU, RAM, Disk, Battery via `psutil`).
- 🌐 **Web & Info Integration**: Search Google, get real-time weather via public API, retrieve current local time and date.
- 🤖 **Smart Intent Engine**: Fast rule-based intent parsing for offline automation with conversational fallback responses.

---

## Quick Start

### 1. Python Backend Setup
```bash
cd backend
python -m venv venv
# On Windows:
venv\Scripts\activate

pip install -r requirements.txt
python app.py
```
Backend runs on `http://localhost:5050`.

### 2. React HUD Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
Frontend runs on `http://localhost:3050`.

---

## Supported Commands
- `"Open Chrome"` / `"Launch VS Code"` / `"Open Calculator"` / `"Open Notepad"`
- `"System stats"` / `"Show performance"`
- `"Volume up"` / `"Volume down"` / `"Mute"`
- `"Weather"`
- `"What time is it"`
- `"Search for quantum computing"`
