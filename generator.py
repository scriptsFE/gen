import random
import requests
import time
import sys
import os

URL_LOGIN = "https://auth.roblox.com/v2/login"
URL_MAIN = "https://www.roblox.com"

GITHUB_USER = "scriptsFE"
URL_COOKIES = f"https://raw.githubusercontent.com/{GITHUB_USER}/gen/main/cookies.txt"

def print_gradient_banner():
    os.system('clear')
    banner = [
        "  ██████  ██ ▄█▀ ██▓▓█████▄ ▓█████▄ ▓█████ ▓█████▄ ",
        "▒██    ▒  ██▄█▒ ▓██▒▒██▀ ██▌▒██▀ ██▌▓█   ▀ ▒██▀ ██▌",
        "░ ▓██▄   ▓███▄░ ▒██▒░██   █▌░██   █▌▒███   ░██   █▌",
        "  ▒   ██▒▓██ █▄ ░██░░▓█▄   ▌░▓█▄   ▌▒▓█  ▄ ░▓█▄   ▌",
        "▒██████▒▒▒██▒ █▄░██░░▒████▓ ░▒████▓ ░▒████▒░▒████▓ ",
        "▒ ▒▓▒ ▒ ░▒ ▒▒ ▓▒░▓   ▒▒▓  ▒  ▒▒▓  ▒ ░░ ▒░ ░ ▒▒▓  ▒ ",
        "░ ░▒  ░ ░░ ░▒ ▒░ ▒ ░ ░ ▒  ▒  ░ ▒  ▒  ░ ░  ░ ░ ▒  ▒ ",
        "░  ░  ░  ░ ░░ ░  ▒ ░ ░ ░  ░  ░ ░  ░    ░    ░ ░  ░ ",
        "      ░  ░  ░    ░     ░       ░       ░  ░   ░    ",
        "                     ░       ░              ░      "
    ]
    for line in banner:
        colored_line = ""
        for i, char in enumerate(line):
            r = int(140 + (i * 2.5))
            g = int(0)
            b = int(255 - (i * 2.5))
            r = max(0, min(255, r))
            b = max(0, min(255, b))
            colored_line += f"\033[38;2;{r};{g};{b}m{char}"
        print(colored_line + "\033[0m")
        
    print("\n\t\033[35m</> Author: scripts_fe | Roblox Utility \033[0m")
    print("\033[38;5;204m===============================================================\033[0m")
    print("\t\t\t\033[35mTelegram: @scripts_fe\033[0m")
    print("\033[38;5;204m===============================================================\033[0m")
    print("\n\033[32m[!]\033[0m System loaded cleanly. Ready to target.")

def load_cookies():
    try:
        res = requests.get(URL_COOKIES, timeout=10)
        if res.status_code == 200:
            lines = res.text.splitlines()
            cookies = []
            for line in lines:
                clean = line.strip()
                if clean:
                    if ".ROBLOSECURITY=" in clean:
                        clean = clean.split(".ROBLOSECURITY=")[1].split(";")[0]
                    cookies.append(clean)
            print(f" -> Pulled {len(cookies)} sessions from configuration")
            return cookies
        print(f" -> Sync issue: {res.status_code}")
        return []
    except Exception as e:
        print(f" -> Network failure reading source: {e}")
        return []

def get_csrf(cookie):
    headers = {
        "User-Agent": "Mozilla/5.0 (Android; Mobile; rv:132.0) Gecko/132.0 Firefox/132.0",
        "Origin": URL_MAIN,
        "Referer": URL_MAIN,
        "Cookie": f".ROBLOSECURITY={cookie}"
    }
    try:
        r = requests.post(URL_LOGIN, json={}, headers=headers, timeout=10)
        return r.headers.get("X-CSRF-TOKEN") or r.headers.get("x-csrf-token")
    except:
        return None

def start_botting():
    cookies = load_cookies()
    if not cookies:
        print(" -> Action aborted: Missing credentials file")
        return

    target = input("\nEnter Target ID > ").strip()
    if not target.isdigit():
        print(" -> Error: Numeric ID format required")
        return

    url_follow = f"https://friends.roblox.com/v1/users/{target}/follow"
    success = 0

    print("\033[38;5;239m---------------------------------------------------------------\033[0m")
    for i, cookie in enumerate(cookies, 1):
        print(f"[{i}/{len(cookies)}] Routing connection parameters...")
        token = get_csrf(cookie)
        
        if not token:
            print(" -> Skipped: Verification failed")
            continue

        headers = {
            "User-Agent": "Mozilla/5.0 (Android; Mobile; rv:132.0) Gecko/132.0 Firefox/132.0",
            "Content-Type": "application/json;charset=UTF-8",
            "X-CSRF-TOKEN": token,
            "Cookie": f".ROBLOSECURITY={cookie}",
            "Origin": URL_MAIN,
            "Referer": f"https://www.roblox.com/users/{target}/profile"
        }

        try:
            res = requests.post(url_follow, json={}, headers=headers, timeout=10)
            if res.status_code == 200:
                success += 1
                print(" -> Status: Complete")
            elif res.status_code == 403:
                print(" -> Status: Blocked by checkpoint limit")
            else:
                print(f" -> Status: Code {res.status_code}")
        except Exception as e:
            print(f" -> Status: Drop {e}")

        if i < len(cookies):
            delay = random.randint(3, 7)
            time.sleep(delay)

    print("\033[38;5;239m---------------------------------------------------------------\033[0m")
    print(f"Operation complete. Dispatched updates: {success}\n")

def main():
    print_gradient_banner()
    while True:
        try:
            cmd = input("\n$ ").strip()
            if cmd == "! start":
                start_botting()
            elif cmd == "exit":
                sys.exit()
            elif cmd == "":
                continue
            else:
                print("Command unrecognized. Use '! start' or 'exit'")
        except (KeyboardInterrupt, EOFError):
            sys.exit()

if __name__ == "__main__":
    main()
