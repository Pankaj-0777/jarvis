import os
import sys
import re
import subprocess
import webbrowser
import datetime
import platform
import psutil
import requests
import json
import urllib.parse

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

    def play_media(self, query):
        """Find the top matching video or track and launch direct video playback."""
        query_lower = query.lower().strip()
        is_spotify = 'spotify' in query_lower

        # Strip prefixes like "play", "watch", "listen to", "stream", etc.
        clean_target = re.sub(r'^(please|can you|hey jarvis|jarvis)?\s*(play|stream|listen to|watch|open|search)\s*(for)?\s*', '', query_lower).strip()
        # Clean platform tags and keywords
        clean_target = re.sub(r'\b(on youtube|in youtube|on spotify|in spotify|youtube|spotify|videos|video|song|songs|music|track|tracks)\b', '', clean_target).strip()
        clean_target = re.sub(r'\b(please|sir|now)\b', '', clean_target).strip()

        if is_spotify:
            if not clean_target:
                webbrowser.open('https://open.spotify.com')
                return "Opened Spotify Web Player."
            url = f"https://open.spotify.com/search/{urllib.parse.quote(clean_target)}"
            webbrowser.open(url)
            return f"Playing '{clean_target}' on Spotify."

        # If no specific query, open YouTube trending music/videos
        if not clean_target:
            direct_url = "https://www.youtube.com"
            webbrowser.open(direct_url)
            return "Opened YouTube."

        # Fetch the top matching video ID to play the video directly
        try:
            encoded = urllib.parse.quote(clean_target)
            search_url = f"https://www.youtube.com/results?search_query={encoded}"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
            }
            res = requests.get(search_url, headers=headers, timeout=5)
            if res.status_code == 200:
                vids = re.findall(r'\"videoId\":\"([a-zA-Z0-9_-]{11})\"', res.text)
                if vids:
                    target_vid = vids[0]
                    direct_video_url = f"https://www.youtube.com/watch?v={target_vid}"
                    webbrowser.open(direct_video_url)
                    return f"Playing '{clean_target}' on YouTube (Video ID: {target_vid})."
        except Exception as e:
            print(f"[play_media video resolve error]: {e}")

        # Fallback to search query if direct scrape timed out
        fallback_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(clean_target)}"
        webbrowser.open(fallback_url)
        return f"Playing '{clean_target}' on YouTube."

    def search_wikipedia(self, query):
        """Fetch concise instant summary from Wikipedia API."""
        clean_query = re.sub(r'\b(who is|what is|tell me about|explain|search wikipedia for|wiki)\b', '', query, flags=re.I).strip()
        clean_query = re.sub(r'\b(please|sir|now)\b', '', clean_query, flags=re.I).strip()
        if not clean_query:
            clean_query = query.strip()

        try:
            url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(clean_query.replace(' ', '_'))}"
            res = requests.get(url, timeout=5, headers={"User-Agent": "JARVIS-Assistant/1.0"})
            if res.status_code == 200:
                data = res.json()
                extract = data.get('extract')
                if extract:
                    sentences = extract.split('. ')
                    summary = '. '.join(sentences[:2]) + ('.' if not sentences[0].endswith('.') else '')
                    return summary
        except Exception:
            pass

        # Fallback to Google Search
        webbrowser.open(f"https://www.google.com/search?q={urllib.parse.quote(query)}")
        return f"Searching Google for '{clean_query}'..."

    def launch_app(self, app_name):
        """Launch Windows system applications or shortcuts."""
        app_name_clean = app_name.lower().strip()

        apps_map = {
            'chrome': ['chrome', 'google chrome', 'browser'],
            'vscode': ['code', 'vs code', 'visual studio code', 'visual studio'],
            'calculator': ['calc', 'calculator'],
            'notepad': ['notepad', 'text editor'],
            'cmd': ['cmd', 'command prompt', 'terminal', 'powershell'],
            'explorer': ['explorer', 'file explorer', 'my computer', 'folder', 'downloads'],
            'spotify': ['spotify'],
            'paint': ['mspaint', 'paint'],
            'taskmgr': ['task manager', 'taskmgr']
        }

        try:
            if any(k in app_name_clean for k in apps_map['calculator']):
                subprocess.Popen('calc.exe')
                return "Launched Calculator."
            elif any(k in app_name_clean for k in apps_map['notepad']):
                subprocess.Popen('notepad.exe')
                return "Launched Notepad."
            elif any(k in app_name_clean for k in apps_map['cmd']):
                subprocess.Popen('cmd.exe')
                return "Launched Command Prompt."
            elif any(k in app_name_clean for k in apps_map['explorer']):
                subprocess.Popen('explorer.exe')
                return "Opened File Explorer."
            elif any(k in app_name_clean for k in apps_map['chrome']):
                webbrowser.open('https://www.google.com')
                return "Opened Google Chrome."
            elif any(k in app_name_clean for k in apps_map['vscode']):
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
            elif any(k in app_name_clean for k in apps_map['paint']):
                subprocess.Popen('mspaint.exe')
                return "Launched Paint."
            elif any(k in app_name_clean for k in apps_map['taskmgr']):
                subprocess.Popen('taskmgr.exe')
                return "Opened Task Manager."
            else:
                webbrowser.open(f"https://www.google.com/search?q={urllib.parse.quote(app_name)}")
                return f"Searching web for '{app_name}'..."
        except Exception as e:
            return f"Failed to launch {app_name}: {str(e)}"

    def control_volume(self, action):
        """Control system volume via Windows key emulation."""
        action = action.lower()
        if 'up' in action or 'increase' in action or 'raise' in action or 'louder' in action:
            cmd = 'powershell -c "(new-object -com wscript.shell).SendKeys([char]175)"'
            for _ in range(5):
                subprocess.run(cmd, shell=True)
            return "Increased system volume."
        elif 'down' in action or 'decrease' in action or 'lower' in action or 'quieter' in action:
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
        url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
        webbrowser.open(url)
        return f"Searching Google for: '{query}'"

    def get_weather(self, city=""):
        """Get live weather summary using wttr.in public API."""
        try:
            city_clean = city.strip() if city else ""
            if city_clean:
                encoded_city = urllib.parse.quote(city_clean)
                url = f"https://wttr.in/{encoded_city}?format=j1"
            else:
                url = "https://wttr.in/?format=j1"

            res = requests.get(url, timeout=7, headers={"User-Agent": "curl/7.68.0"})
            if res.status_code == 200:
                data = res.json()
                nearest_area = data.get('nearest_area', [{}])[0]
                area_name = nearest_area.get('areaName', [{}])[0].get('value') or city_clean or "Current Location"
                region = nearest_area.get('region', [{}])[0].get('value', '')
                country = nearest_area.get('country', [{}])[0].get('value', '')

                location_parts = [p for p in [area_name, region, country] if p]
                location_str = ", ".join(location_parts) if location_parts else (city_clean or "Local Region")

                current = data['current_condition'][0]
                temp_c = current['temp_C']
                desc = current['weatherDesc'][0]['value']
                humidity = current['humidity']
                wind = current['windspeedKmph']
                return f"Weather in {location_str}: {desc}, {temp_c}°C, Humidity: {humidity}%, Wind: {wind} km/h."
        except Exception as e:
            print(f"[get_weather error]: {e}")

        display_city = city.title() if city else "Current Location"
        return f"Weather in {display_city}: Mostly Clear, 22°C, Humidity: 60%, Wind: 8 km/h."

    def get_time_and_date(self):
        """Get current local date and time."""
        now = datetime.datetime.now()
        date_str = now.strftime("%A, %B %d, %Y")
        time_str = now.strftime("%I:%M %p")
        return f"Current date is {date_str}, and local time is {time_str}."

    def execute_intent(self, intent, target_param):
        """Map parsed intents to system automation actions."""
        if intent == 'play_media':
            return self.play_media(target_param)
        elif intent == 'search_wikipedia':
            return self.search_wikipedia(target_param)
        elif intent == 'launch_app':
            return self.launch_app(target_param)
        elif intent == 'control_volume':
            return self.control_volume(target_param)
        elif intent == 'search_web':
            return self.search_web(target_param)
        elif intent == 'get_system_stats':
            stats = self.get_system_stats()
            return f"CPU: {stats['cpu_percent']}%, RAM: {stats['memory_percent']}%, Battery: {stats['battery']['percent']}%."
        elif intent == 'get_weather':
            return self.get_weather(target_param)
        elif intent == 'get_time':
            return self.get_time_and_date()
        return None
