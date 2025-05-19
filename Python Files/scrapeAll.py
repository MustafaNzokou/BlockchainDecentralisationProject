import requests
import json
import time
import os

# GitHub repository details
OWNER = "bitcoin"
REPO = "bips"
TOKEN = ""  # Use a personal access token for authentication

HEADERS = {"Authorization": f"token {TOKEN}"}
TIMEOUT = 2  # Timeout in seconds
MAX_RETRIES = 3  # Number of retries for failed requests
SLEEP_TIME = 5  # Pause between retries (in seconds)

# Step 1: Get all PRs with pagination
all_prs = []
page = 1
per_page = 100  

while True:
    prs_url = f"https://api.github.com/repos/{OWNER}/{REPO}/pulls?state=all&per_page={per_page}&page={page}"
    
    try:
        prs_response = requests.get(prs_url, headers=HEADERS, timeout=TIMEOUT)
        prs_response.raise_for_status()  # Raise an error for HTTP issues

        # Check if rate limit is hit
        if int(prs_response.headers.get("X-RateLimit-Remaining", 1)) == 0:
            reset_time = int(prs_response.headers.get("X-RateLimit-Reset", time.time())) - time.time()
            print(f"Rate limit reached. Waiting {reset_time:.2f} seconds...")
            time.sleep(reset_time + 1)  # Wait for rate limit reset
            continue


        prs = prs_response.json()
        if not prs:
            break  # No more PRs, exit loop

        all_prs.extend(prs)
        page += 1  

    except requests.exceptions.Timeout:
        print(f"Request timed out while fetching PRs from {prs_url}. Retrying...")
        time.sleep(5)  # Wait before retrying
        continue
    except requests.exceptions.RequestException as e:
        print(f"Error fetching PRs: {e}")
        break
    print("PRs page", page,"fetched successfully")

    with open("all_prs.json", "w") as json_file:
        json.dump(all_prs, json_file, indent=4)