import json
import requests
import re
import os

REPO = "romanmakin92-dot/coin-clicker"
GITHUB_TOKEN = os.environ.get("TOKEN_FOR_ACTIONS")

print(f"Токен найден: {'да' if GITHUB_TOKEN else 'нет'}")

def get_issues():
    if not GITHUB_TOKEN:
        print("Ошибка: токен не найден в переменных окружения")
        return []
    
    url = f"https://api.github.com/repos/{REPO}/issues"
    headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/json"}
    params = {"state": "all", "per_page": 100}
    
    all_issues = []
    page = 1
    while True:
        params["page"] = page
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            print(f"Ошибка API: {response.status_code}")
            break
        issues = response.json()
        if not issues:
            break
        all_issues.extend(issues)
        page += 1
        if len(issues) < 100:
            break
    
    print(f"Найдено Issues: {len(all_issues)}")
    return all_issues

def parse_value(body, pattern):
    match = re.search(pattern, body)
    if not match:
        return 0
    val_str = match.group(1)
    multiplier = 1
    if 'К' in val_str or 'к' in val_str:
        multiplier = 1000
        val_str = re.sub(r'[Кк]', '', val_str).strip()
    elif 'М' in val_str or 'м' in val_str:
        multiplier = 1000000
        val_str = re.sub(r'[Мм]', '', val_str).strip()
    elif 'Т' in val_str or 'т' in val_str:
        multiplier = 1000000000000
        val_str = re.sub(r'[Тт]', '', val_str).strip()
    try:
        return int(float(val_str) * multiplier)
    except:
        return 0

def extract_name(body):
    match = re.search(r'👤 Игрок: (.+?)(?:\n|$)', body)
    if match:
        return match.group(1).strip()
    return None

def update_leaderboard():
    issues = get_issues()
    players_data = {}
    
    for issue in issues:
        body = issue.get("body", "")
        name = extract_name(body)
        if not name:
            continue
        
        coins = parse_value(body, r'💰 Монет: ([\d\.]+[КМТ]?)')
        prestige = parse_value(body, r'⭐ Престиж: (\d+)')
        mega = parse_value(body, r'🔥 Мега: (\d+)')
        hyper = parse_value(body, r'🌈 Гипер: (\d+)')
        
        if name not in players_data:
            players_data[name] = {"coins": 0, "prestige": 0, "mega": 0, "hyper": 0}
        
        if coins > players_data[name]["coins"]:
            players_data[name]["coins"] = coins
        if prestige > players_data[name]["prestige"]:
            players_data[name]["prestige"] = prestige
        if mega > players_data[name]["mega"]:
            players_data[name]["mega"] = mega
        if hyper > players_data[name]["hyper"]:
            players_data[name]["hyper"] = hyper
    
    leaderboard = {
        "coins": [],
        "prestige": [],
        "mega": [],
        "hyper": []
    }
    
    for name, data in players_data.items():
        if data["coins"] > 0:
            leaderboard["coins"].append({"name": name, "value": data["coins"]})
        if data["prestige"] > 0:
            leaderboard["prestige"].append({"name": name, "value": data["prestige"]})
        if data["mega"] > 0:
            leaderboard["mega"].append({"name": name, "value": data["mega"]})
        if data["hyper"] > 0:
            leaderboard["hyper"].append({"name": name, "value": data["hyper"]})
    
    for key in leaderboard:
        leaderboard[key].sort(key=lambda x: x["value"], reverse=True)
        leaderboard[key] = leaderboard[key][:50]
    
    with open("leaderboard.json", "w", encoding="utf-8") as f:
        json.dump(leaderboard, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Топ обновлён: {len(players_data)} игроков")

if __name__ == "__main__":
    update_leaderboard()
