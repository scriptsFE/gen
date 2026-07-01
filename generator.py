import random
import requests
import time
import sys
import os

URL_SIGNUP = "https://auth.roblox.com/v2/signup"
URL_LOGIN = "https://auth.roblox.com/v2/login"
URL_MAIN = "https://www.roblox.com"

def get_download_path():
    base_path = "/sdcard/Download"
    folder_path = os.path.join(base_path, "roblox accs")
    
    if not os.path.exists(base_path):
        folder_path = os.path.join(os.path.expanduser("~"), "roblox_accs")
        
    if not os.path.exists(folder_path):
        try:
            os.makedirs(folder_path)
        except:
            folder_path = os.path.expanduser("~")
            
    return os.path.join(folder_path, "accs.txt")

def print_gradient_banner():
    banner = [
        "   _____ _tp_       ",
        "  / ____| |  (_)    ",
        " | (___ | | ___  _  ",
        "  \\___ \\| |/ / | | |",
        "  ____) |   <| | |_|",
        " |_____/|_|\\_\\_|\\__,|"
    ]
    
    for line in banner:
        colored_line = ""
        for i, char in enumerate(line):
            r = int(140 + (i * 4.5))
            g = int(0)
            b = int(255 - (i * 4.5))
            r = max(0, min(255, r))
            b = max(0, min(255, b))
            colored_line += f"\033[38;2;{r};{g};{b}m{char}"
        print(colored_line + "\033[0m")

def get_user():
    pre = ["Xx_", "ii_", "v_", ""]
    w1 = ["Night", "Royal", "Dark", "Shadow", "Ghost", "Cyber", "Nova", "Alpha", "Hyper"]
    w2 = ["Nova", "Driver", "Blade", "Wolf", "Phantom", "Knight", "Hunter", "Viper", "Echo"]
    
    p = random.choice(pre)
    word1 = random.choice(w1)
    word2 = random.choice(w2)
    
    while word1 == word2:
        word2 = random.choice(w2)
        
    num = random.randint(100, 9999)
    s = ""
    if p == "Xx_": s = "_xX"
    elif p == "ii_": s = "_ii"
    
    name = f"{p}{word1}{word2}{num}{s}"
    return name[:20]

def get_csrf():
    headers = {
        "User-Agent": "Mozilla/5.0 (Android; Mobile; rv:132.0) Gecko/132.0 Firefox/132.0",
        "Origin": URL_MAIN,
        "Referer": URL_MAIN
    }
    try:
        r = requests.post(URL_LOGIN, json={}, headers=headers, timeout=10)
        return r.headers.get("X-CSRF-TOKEN") or r.headers.get("x-csrf-token")
    except:
        return None

def run_generator():
    created = 0
    target = 1
    file_dest = get_download_path()
    
    print(f"\n[!] Starting generation for {target} accounts...")
    
    while created < target:
        username = get_user()
        password = "Sugi pula"
        token = get_csrf()
        
        if not token:
            print("[!] Token error, retrying in 3s...")
            time.sleep(3)
            continue
            
        headers = {
            "User-Agent": "Mozilla/5.0 (Android; Mobile; rv:132.0) Gecko/132.0 Firefox/132.0",
            "Content-Type": "application/json;charset=UTF-8",
            "X-CSRF-TOKEN": token,
            "Origin": URL_MAIN,
            "Referer": URL_MAIN
        }
        
        payload = {
            "username": username,
            "password": password,
            "birthday": "2002-01-01",
            "gender": 1,
            "isCheckUsernameOnly": False
        }
        
        print(f" -> Trying: {username}")
        
        try:
            res = requests.post(URL_SIGNUP, json=payload, headers=headers, timeout=10)
            
            if res.status_code == 200:
                created += 1
                print(f"[+] Success ({created}/{target})")
                with open(file_dest, "a") as f:
                    f.write(f"Username: {username} | Password: {password}\n")
            elif res.status_code == 403 or "Rblx-Challenge-Metadata" in res.headers:
                print(" -> Hit captcha or rate limit, skipping name...")
            else:
                print(f" -> Error code: {res.status_code}")
                
        except Exception as e:
            print(f" -> Connection drop: {e}")
            
        delay = random.randint(8, 15)
        print(f" -> Waiting {delay}s before next request...")
        time.sleep(delay)
        
    print("[==== DONE ====]")
    print(f"[!] Saved to Downloads/roblox accs/accs.txt\n")

def main():
    print_gradient_banner()
    print("Type '! start' to create 4 accounts, or 'exit' to close.")
    
    while True:
        try:
            cmd = input("> ").strip()
            if cmd == "! start":
                run_generator()
            elif cmd == "exit":
                print("Exiting...")
                sys.exit()
            elif cmd == "":
                continue
            else:
                print("Unknown command. Use '! start'")
        except (KeyboardInterrupt, EOFError):
            print("\nExiting...")
            sys.exit()

if __name__ == "__main__":
    main()
