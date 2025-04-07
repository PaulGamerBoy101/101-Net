# history.py
import json
import os
from datetime import datetime

def track_history(self, url):
    """Save visited URLs to history.json."""
    if url.isEmpty():
        return  # Ignore empty URLs

    url_str = url.toString()

    # Load existing history
    history = self.load_history()

    # Append new entry
    history.append({"url": url_str, "timestamp": datetime.utcnow().isoformat()})

    # Save updated history
    with open("history.json", "w") as f:
        json.dump(history, f, indent=4)

def load_history(self):
    """Load browsing history from history.json file."""
    if os.path.exists("history.json"):
        with open("history.json", "r") as f:
            return json.load(f)
    return []  # Return empty list if no history file exists