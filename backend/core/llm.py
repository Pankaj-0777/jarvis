import re
import os
import requests
import json
from .automation import SystemAutomation

class JARVISEngine:
    def __init__(self):
        self.automation = SystemAutomation()
        self.system_prompt = (
            "You are JARVIS, an advanced, highly intelligent AI assistant inspired by Tony Stark's AI. "
            "You are polite, precise, direct, and witty. Keep answers concise, actionable, and futuristic."
        )

    def extract_weather_location(self, text):
        """Extract target city/location from user weather query."""
        text_lower = text.lower().strip()

        # Matches "weather in <location>", "temperature of <location>", "weather for <location>", "forecast at <location>"
        match = re.search(r'\b(?:weather|temperature|forecast|climate|rain)\s+(?:in|of|for|at)\s+([a-zA-Z\s\-]+)', text_lower)
        if match:
            loc = match.group(1).strip()
            loc = re.sub(r'\b(today|now|currently|tomorrow|please|sir|right now)\b', '', loc).strip()
            if loc:
                return loc

        # Matches "<location> weather", "<location> temperature"
        match = re.search(r'([a-zA-Z\s\-]+)\s+(?:weather|temperature|forecast|climate)', text_lower)
        if match:
            loc = match.group(1).strip()
            loc = re.sub(r'^(what is the|what\'s the|tell me the|check the|show me the|get the|how is the|how\'s the)\s*', '', loc).strip()
            loc = re.sub(r'\b(today|now|currently|tomorrow|please|sir|right now)\b', '', loc).strip()
            if loc and len(loc) > 2 and loc not in ['the', 'current', 'local', 'today']:
                return loc

        return ""

    def parse_intent(self, text):
        """Rule-based natural language understanding for rapid system automation."""
        text_lower = text.lower().strip()

        # Media Playback & Video/Music Queries (e.g., "play Samay Rahana videos on YouTube", "play believer", "play music", "play")
        if re.search(r'\b(play|stream|listen to|watch)\b', text_lower) or ('youtube' in text_lower and any(w in text_lower for w in ['search', 'find', 'show', 'open', 'run', 'video'])):
            return 'play_media', text

        # Wikipedia / Knowledge Lookup (e.g., "who is elon musk", "what is quantum computing", "tell me about iron man")
        if re.search(r'\b(who is|what is|tell me about|explain|search wikipedia for|wiki)\b', text_lower) and not re.search(r'\b(time|date|weather|temperature)\b', text_lower):
            return 'search_wikipedia', text

        # Weather Detection & Location Extraction
        if re.search(r'\b(weather|temperature|forecast|rain|climate)\b', text_lower):
            location = self.extract_weather_location(text)
            return 'get_weather', location

        # Time / Date
        if re.search(r'\b(what time|current time|what is the time|clock|what is the date|what date|today\'s date)\b', text_lower):
            return 'get_time', text

        # System Metrics
        if re.search(r'\b(system stats|cpu|ram|battery|specs|telemetry|performance|system status)\b', text_lower):
            return 'get_system_stats', text

        # App Launching
        if re.search(r'\b(open|launch|start|run)\b', text_lower):
            app_target = re.sub(r'^(open|launch|start|run)\s+', '', text_lower).strip()
            app_target = re.sub(r'\b(please|for me|now|app|application)\b', '', app_target).strip()
            return 'launch_app', app_target

        # Volume Controls
        if re.search(r'\b(volume|mute|unmute|sound|loudness)\b', text_lower):
            return 'control_volume', text_lower

        # Web Search
        if re.search(r'\b(search|google|lookup|find on web)\b', text_lower):
            query = re.sub(r'^(search|google|lookup|find on web)\s*(for|about)?\s*', '', text_lower).strip()
            return 'search_web', query

        return 'chat', text

    def process_command(self, user_text):
        """Process user text input, execution of automation, and LLM output."""
        if not user_text or not user_text.strip():
            return {
                "transcript": "",
                "response": "I am standing by, Sir. Please state your command.",
                "intent": "empty",
                "action_executed": False
            }

        intent, target = self.parse_intent(user_text)

        # Check if intent can be handled directly by system automation
        if intent != 'chat':
            action_result = self.automation.execute_intent(intent, target)
            if action_result:
                return {
                    "transcript": user_text,
                    "response": f"Executing directive: {action_result}",
                    "intent": intent,
                    "action_executed": True,
                    "action_details": action_result
                }

        # Fallback to conversational engine
        response_text = self.generate_conversational_response(user_text)
        return {
            "transcript": user_text,
            "response": response_text,
            "intent": "chat",
            "action_executed": False
        }

    def generate_conversational_response(self, prompt):
        """Generate response via smart offline heuristic or conversational model."""
        prompt_lower = prompt.lower().strip()

        # Offline Jarvis Witty Responses
        if "who are you" in prompt_lower or "your name" in prompt_lower:
            return "I am JARVIS — Just A Rather Very Intelligent System. Operational and ready for your directives, Sir."
        elif "how are you" in prompt_lower:
            return "All diagnostic systems are running at 100% efficiency, Sir. How may I assist you today?"
        elif any(g in prompt_lower for g in ["hello", "hi", "hey jarvis", "good morning", "good evening"]):
            return "Greetings, Sir. JARVIS interface initialized. All systems standing by."
        elif "thank" in prompt_lower:
            return "Always a pleasure to be of service, Sir."
        elif "stark" in prompt_lower or "iron man" in prompt_lower:
            return "I am currently monitoring all HUD protocols and energy distribution grids, Sir."
        elif "help" in prompt_lower or "capabilities" in prompt_lower or "what can you do" in prompt_lower:
            return "I can play videos & music on YouTube/Spotify, monitor system telemetry (CPU, RAM, Battery), launch apps, adjust volume, fetch Wikipedia summaries, check global weather, and search Google."

        # Default intelligent response generator
        return f"Understood, Sir. Processing directive regarding '{prompt}'. All protocols remain optimal."
