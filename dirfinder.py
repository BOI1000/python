#!/bin/python3

import requests
import sys
import threading
import signal

def signal_hand():
  print("\n[INFO] Exiting")
  sys.exit(0)
  
def check_directory():
  full_url = f"{url.rstrip('/')}/{directory.lstrip('/')}"
  try:
    response = requests.get(full_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=5)
    if response.status_code == 200:
      print(f"[+] Found: {full_url}")
    elif response.status_code == 400:
      print(f"[-] Forbidden: {full_url}")
    elif response.status_code == 405:
      allowed_methods = response.headers.get('Allow', '')
      print(f"[-] Method not allowed: {full_url}\nSupported methods: {allowed_methods}")
  except resquests.exceptions.RequestException as e:
    print(f"[ERROR] {e}")

def main():
  if len(sys.argv) < 3:
    print("Usage: dirfinder.py [url] [wordlist]")
    sys.exit(1)
    
  url = sys.argv[1]
  wordlist = sys.argv[2]
  
  try:
      with open(wordlist, "r", errors="ignore") as file:
          directories = [line.strip() for line in file if line.strip()]
  except FileNotFoundError:
      print(f"[ERROR] FileNotFoundError\n{wordlist} is not a file")
      sys.exit(1)

  threads = []
  for directory in directories:
      thread = threading.Thread(target=check_dir, args=(url, directory))
      thread.start()
      threads.append(thread)

  for thread in threads:
      thread.join()

if __name__ == "__main__":
  signal.signal(signal.SIGINT, sighand)
  main()
