"""
leaderboard.py - Local Persistent Leaderboard for Quantum Heist
Author: Qiskit Fall Fest 2026 Hackathon Team (Track 1)

Handles local persistent leaderboard storage using JSON.
Clearly scoped as a local leaderboard for this installation.
"""

import json
import os
from datetime import datetime

LEADERBOARD_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "leaderboard.json")


def load_leaderboard() -> list:
    """
    Loads leaderboard entries from local JSON file.
    Returns list of dicts sorted by score (descending), then time_seconds (ascending).
    """
    if not os.path.exists(LEADERBOARD_FILE):
        # Default starter baseline records for demonstration
        default_entries = [
            {
                "player_name": "Ada_Lovelace",
                "score": 650,
                "time_seconds": 38,
                "mistakes": 0,
                "timestamp": "2026-10-10 20:30",
                "rank_title": "Grandmaster Quantum Infiltrator"
            },
            {
                "player_name": "Erwin_S",
                "score": 580,
                "time_seconds": 55,
                "mistakes": 1,
                "timestamp": "2026-10-10 21:15",
                "rank_title": "Senior Circuit Specialist"
            },
            {
                "player_name": "John_Bell",
                "score": 520,
                "time_seconds": 72,
                "mistakes": 2,
                "timestamp": "2026-10-10 22:00",
                "rank_title": "Entanglement Operative"
            }
        ]
        save_leaderboard(default_entries)
        return default_entries

    try:
        with open(LEADERBOARD_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Sort by score descending, then time ascending
            data.sort(key=lambda x: (-x.get("score", 0), x.get("time_seconds", 9999)))
            return data
    except Exception:
        return []


def save_leaderboard(entries: list):
    """Saves leaderboard entries to local JSON file."""
    try:
        with open(LEADERBOARD_FILE, "w", encoding="utf-8") as f:
            json.dump(entries, f, indent=2)
    except Exception as e:
        print(f"Leaderboard save error: {e}")


def add_leaderboard_entry(player_name: str, score: int, time_seconds: int, mistakes: int) -> int:
    """
    Adds a new run result to the leaderboard, saves to disk, and returns the player's 1-indexed rank.
    """
    entries = load_leaderboard()
    
    # Determine rank title based on score & mistakes
    if mistakes == 0 and score >= 600:
        rank_title = "Grandmaster Quantum Infiltrator"
    elif mistakes <= 1 and score >= 500:
        rank_title = "Senior Circuit Specialist"
    elif score >= 400:
        rank_title = "Entanglement Operative"
    else:
        rank_title = "Quantum Recruit"

    new_entry = {
        "player_name": player_name.strip() or "Anonymous_Hacker",
        "score": max(0, score),
        "time_seconds": max(1, time_seconds),
        "mistakes": mistakes,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "rank_title": rank_title
    }

    entries.append(new_entry)
    # Sort: highest score first, then fastest completion time
    entries.sort(key=lambda x: (-x.get("score", 0), x.get("time_seconds", 9999)))
    
    save_leaderboard(entries)
    
    # Find 1-indexed rank of this entry
    for idx, e in enumerate(entries, 1):
        if e is new_entry:
            return idx
    return len(entries)
