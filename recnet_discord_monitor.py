import requests
import time
def main():
    last_profile = None
    last_games = set()
    while True:
        profile = get_profile()
        games = get_games()
        print("Profile data:", profile)
        print("Games data:", games)
        games_set = set(game.get("GameName", "") for game in games)
        # ... rest of your code ...

RECNET_PROFILE_URL = "https://api.rec.net/api/users/{user_id}"
RECNET_GAMES_URL = "https://api.rec.net/api/users/{user_id}/games"
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1398556517493637211/D-h8q2YuLiX-hq29e-gfo2nO5fKvXkN1Ayry6aY9LWT8yycK_Jc6gXLZj8Vsx2J51XM_"

USER_ID = "558764785"  # yy.Zero's user ID!
POLL_INTERVAL = 60  # seconds

def get_profile():
    r = requests.get(RECNET_PROFILE_URL.format(user_id=USER_ID))
    return r.json()

def get_games():
    r = requests.get(RECNET_GAMES_URL.format(user_id=USER_ID))
    return r.json()

def send_discord_message(content):
    payload = {
        "content": content
    }
    requests.post(DISCORD_WEBHOOK_URL, json=payload)

def main():
    last_profile = None
    last_games = set()
    while True:
        profile = get_profile()
        games = get_games()
        games_set = set(game.get("GameName", "") for game in games)

        # Profile changes
        if last_profile:
            if profile.get("displayName") != last_profile.get("displayName"):
                send_discord_message(f"Display name changed from '{last_profile.get('displayName')}' to '{profile.get('displayName')}'")
            if profile.get("username") != last_profile.get("username"):
                send_discord_message(f"Username changed from '{last_profile.get('username')}' to '{profile.get('username')}'")
            if profile.get("bio") != last_profile.get("bio"):
                send_discord_message(f"Bio changed from '{last_profile.get('bio')}' to '{profile.get('bio')}'")
            if profile.get("status") != last_profile.get("status"):
                send_discord_message(f"Status changed from '{last_profile.get('status')}' to '{profile.get('status')}'")

        # Games joined
        new_games = games_set - last_games
        for game in new_games:
            send_discord_message(f"Player @{profile.get('username')} has joined ^{game}")

        last_profile = profile
        last_games = games_set

        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    main()
