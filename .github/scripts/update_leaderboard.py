import json
import random
from datetime import datetime

LEADERBOARD_FILE = "leaderboard.json"

def update_leaderboard():
    new_scores = [
        {"name": "Игрок1", "score": random.randint(1000, 100000), "date": str(datetime.now())},
        {"name": "Игрок2", "score": random.randint(1000, 100000), "date": str(datetime.now())},
        {"name": "Игрок3", "score": random.randint(1000, 100000), "date": str(datetime.now())},
    ]
    
    new_scores.sort(key=lambda x: x["score"], reverse=True)
    
    with open(LEADERBOARD_FILE, "w", encoding="utf-8") as f:
        json.dump(new_scores, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Топ обновлён: {len(new_scores)} записей")

if __name__ == "__main__":
    update_leaderboard()
