import time
import datetime

def format_timestamp():
    return datetime.datetime.now().strftime("%H:%M:%S")

def sanitize_command(text):
    if not text:
        return ""
    return text.strip().replace('\n', ' ')
