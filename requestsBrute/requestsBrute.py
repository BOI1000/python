#!/usr/bin/env python3
import requests
import sys
import os
def brutus_one(url, wordlists):
    with open(wordlists, "r", errors="ignore") as file:
        if "?" in url:
            url, data = url.split("?", 1)
        else:
            sys.exit(1)
        lines = file.readlines()
        if "HIT" in data:
            for line in lines:
                line = line.strip()
                hitter = data.replace("HIT", f"{line}")
                if not line:
                    continue
                try:
                    response = requests.post(url, headers={"User-Agent": "Mozilla/5.0"}, data=f"{hitter}", timeout=5)
                    if response.status_code == 200:
                        print(f"[HIT] {url}?{hitter}")
                except requests.exceptions.RequestException as e:
                    print(f"[ERROR] {e}")
if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(1)
    url = sys.argv[1]
    wordlists = sys.argv[2]
    if not os.path.isfile(wordlists):
        sys.exit(1)
    brutus_one(url, wordlists)
sys.exit(0)