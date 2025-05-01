#!/bin/python3
import requests
import sys
import threading
import signal

red = "\033[91m"
green = "\033[92m"
yellow = "\033[93m"
bold = "\033[1m"
reset = "\033[0m"
banner = r"""
.s5SSSs.                    .s5SSSs.                                             
      SS. s.  .s5SSSs.               s.  .s    s.  .s5SSSs.  .s5SSSs.  .s5SSSs.  
sS    S%S SS.       SS.     sS       SS.       SS.       SS.       SS.       SS. 
SS    S%S S%S sS    S%S     SS       S%S sSs.  S%S sS    S%S sS    `:; sS    S%S 
SS    S%S S%S SS .sS;:'     SSSs.    S%S SS `S.S%S SS    S%S SSSs.     SS .sS;:' 
SS    S%S S%S SS    ;,      SS       S%S SS  `sS%S SS    S%S SS        SS    ;,  
SS    `:; `:; SS    `:;     SS       `:; SS    `:; SS    `:; SS        SS    `:; 
SS    ;,. ;,. SS    ;,.     SS       ;,. SS    ;,. SS    ;,. SS    ;,. SS    ;,. 
;;;;;;;:' ;:' `:    ;:'     :;       ;:' :;    ;:' ;;;;;;;:' `:;;;;;:' `:    ;:'
"""

def signal_hand(signal, frame):
    print("\n[INFO] Exiting")
    sys.exit(0)

def check_directory(url, directory):
    full_url = f"{url.rstrip('/')}/{directory.lstrip('/')}"
    try:
        response = requests.get(full_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=5)
        if response.status_code == 200:
            print(f"{bold}{green}[+]{reset} Found: {full_url}")
        elif response.status_code == 400:
            print(f"{bold}{yellow}[-]{reset} Forbidden: {full_url}") 
        elif response.status_code == 405:
            allowed_methods = response.headers.get('Allow', '')
            print(f"{bold}{yellow}[-]{reset} Method not allowed: {full_url}\nSupported methods: {allowed_methods}")
    except requests.exceptions.RequestException as e:
        print(f"{bold}{red}[ERROR]{reset} {e}")

def main():
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} [url] [wordlist]")
        sys.exit(1)

    url = sys.argv[1]
    wordlist = sys.argv[2]
    try:
        with open(wordlist, "r", errors="ignore") as file:
            directories = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"{reset}{red}[ERROR]{reset} FileNotFoundError\n{wordlist} is not a file")
        sys.exit(1)

    threads = []
    for directory in directories:
        thread = threading.Thread(target=check_directory, args=(url, directory))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    print(f"{green}{banner}{reset}")
    signal.signal(signal.SIGINT, signal_hand)
    main()