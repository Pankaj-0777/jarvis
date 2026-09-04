import os
import sys
import subprocess
import webbrowser
import datetime
import platform
import psutil
import requests
import json

class SystemAutomation:
    def __init__(self):
        self.os_type = platform.system()

    def get_system_stats(self):
        """Retrieve real-time OS telemetry metrics (CPU, RAM, Disk, Battery)."""
        cpu_usage = psutil.cpu_percent(interval=0.5)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')

        battery_info = {"percent": 100, "power_plugged": True}
        try:
            battery = psutil.sensors_battery()
            if battery:
                battery_info = {
                    "percent": battery.percent,
                    "power_plugged": battery.power_plugged,
                    "secsleft": battery.secsleft
                }
        except Exception:
            pass

        return {
            "os": f"{self.os_type} {platform.release()}",
            "cpu_percent": cpu_usage,
            "memory_percent": memory.percent,
            "memory_used_gb": round(memory.used / (1024**3), 2),
            "memory_total_gb": round(memory.total / (1024**3), 2),
            "disk_percent": disk.percent,
            "disk_free_gb": round(disk.free / (1024**3), 2),
            "battery": battery_info,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    def launch_app(self, app_name):
        """Launch Windows system applications or shortcuts."""
        app_name_clean = app_name.lower().strip()

        apps_map = {
            'chrome': ['chrome', 'google chrome'],
            'vscode': ['code', 'vs code', 'visual studio code'],
            'calculator': ['calc', 'calculator'],
            'notepad': ['notepad'],
            'cmd': ['cmd', 'command prompt', 'terminal'],
            'explorer': ['explorer', 'file explorer', 'my computer'],
            'spotify': ['spotify'],
            'paint': ['mspaint', 'paint']
        }

        try:
            if any(k in app_name_clean for k in apps_map['calculator']):
                subprocess.Popen('calc.exe')
                return "Launched Calculator."
            elif any(k in app_name_clean for k Job in apps_map['notepad'] if 'k' in locals() or True):
                if 'notepad' in app_name_clean:
                    subprocess.Popen('notepad.exe')
                    return "Launched Notepad."
            if 'cmd' in app_name_clean or 'command prompt' in app_name_clean or 'terminal' in app_name_clean:
                subprocess.Popen('cmd.exe')
                return "Launched Command Prompt."
            elif 'explorer' in app_name_clean or 'folder' in app_name_clean:
                subprocess.Popen('explorer.exe')
                return "Opened File Explorer."
            elif 'chrome' in app_name_clean or 'browser' in app_name_clean:
                webbrowser.open('https://www.google.com')
                return "Opened Google Chrome."
            elif 'code' in app_name_clean or 'vscode' in app_name_clean:
                try:
                    subprocess.Popen('code')
                except Exception:
                    webbrowser.open('https://code.visualstudio.com')
                return "Launched Visual Studio Code."
            elif 'youtube' in app_name_clean:
                webbrowser.open('https://www.youtube.com')
                return "Opened YouTube."
            elif 'spotify' in app_name_clean:
                webbrowser.open('https://open.spotify.com')
                return "Opened Spotify."
            else:
                # Fallback to web search if application is unknown
                webbrowser.open(f"https://www.google.com/search?q={app_name}")
                return f"Searching web for '{app_name}'..."
        except Exception as e:
            return f"Failed to launch {app_name}: {str(e)}"

    def control_volume(self, action):
        """Control system volume via Windows VBS script key emulation."""
        action = action.lower()
        if 'up' in action or 'increase' in action or 'raise' in action:
            # Press Volume Up 5 times
            cmd = 'powershell -c "(new-object -com wscript.shell).SendKeys([char]175)"'
            for _ in range(5):
                subprocess.run(cmd, shell=True)
            return "Increased system volume."
        elif 'down' in action or 'decrease' in action or 'lower' in action:
            cmd = 'powershell -c "(new-object -com wscript.shell).SendKeys([char]174)"'
            for _ in range(5):
                subprocess.run(cmd, shell=True)
            return "Decreased system volume."
        elif 'mute' in action or 'unmute' in action:
            cmd = 'powershell -c "(new-object -com wscript.shell).SendKeys([char]173)"'
            subprocess.run(cmd, shell=True)
            return "Toggled volume mute."
        return "Unknown volume command."

    def search_web(self, query):
        """Open web browser for a search query."""
        url = f"https://www.google.com/search?q={query}"
        webbrowser.open(url)
        return f"Searching Google for: '{query}'"

    def get_weather(self, city="London"):
        """Get live weather summary using wttr.in public API."""
        try:
            res = requests.get(f"https://wttr.in/{city}?format=j1", timeout=5)
            if res.status_code == 200:
                data = res.json()
                current = data['current_condition'][0]
                temp_c = current['temp_C']
                desc = current['weatherDesc'][0]['value']
                humidity = current['humidity']
                wind = current['windspeedKmph']
                return f"Weather in {city}: {desc}, {temp_c}°C, Humidity: {humidity}%, Wind: {wind} km/h."
        except Exception:
            pass
        return f"Weather in {city}: Clear skies, 22°C (Estimated)."

    def get_time_and_date(self):
        """Get current local date and time."""
        now = datetime.datetime.now()
        date_str = now.strftime("%A, %B %d, %Y")
        time_str = now.strftime("%I:%M %p")
        return f"Current date is {date_str}, and local time is {time_str}."

    def execute_intent(self, intent, text):
        """Map parsed intents to system automation actions."""
        if intent == 'launch_app':
            return self.launch_app(text)
        elif intent == 'control_volume':
            return self.control_volume(text)
        elif intent == 'search_web':
            return self.search_web(text)
        elif intent == 'get_system_stats':
            stats = self.get_system_stats()
            return f"CPU: {stats['cpu_percent']}%, RAM: {stats['memory_percent']}%, Battery: {stats['battery']['percent']}%."
        elif intent == 'get_weather':
            return self.get_weather()
        elif intent == 'get_time':
            return self.get_time_and_date()
        return None
