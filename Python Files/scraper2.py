import requests
import json
import time
import os

# GitHub repository details
OWNER = "ethereum"
REPO = "EIPs"
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
        #if page == 51: break

    except requests.exceptions.Timeout:
        print(f"Request timed out while fetching PRs from {prs_url}. Retrying...")
        time.sleep(5)  # Wait before retrying
        continue
    except requests.exceptions.RequestException as e:
        print(f"Error fetching PRs: {e}")
        break
    print("PRs page", page,"fetched successfully")

# Step 2: Extract key information (including reviewers & commenters)
filtered_prs = []
for pr in all_prs:
    pr_number = pr["number"]

    # Check if rate limit is hit
    if int(prs_response.headers.get("X-RateLimit-Remaining", 1)) == 0:
        reset_time = int(prs_response.headers.get("X-RateLimit-Reset", time.time())) - time.time()
        print(f"Rate limit reached. Waiting {reset_time:.2f} seconds...")
        time.sleep(reset_time + 1)  # Wait for rate limit reset
        continue


    try:
        # Fetch reviewers
        reviews_url = f"https://api.github.com/repos/{OWNER}/{REPO}/pulls/{pr_number}/reviews"
        reviews_response = requests.get(reviews_url, headers=HEADERS, timeout=TIMEOUT)
        reviews_response.raise_for_status()
        reviews = reviews_response.json()
        reviewers = list({review["user"]["login"] for review in reviews if review.get("user")})

        # Fetch commenters
        comments_url = f"https://api.github.com/repos/{OWNER}/{REPO}/issues/{pr_number}/comments"
        comments_response = requests.get(comments_url, headers=HEADERS, timeout=TIMEOUT)
        comments_response.raise_for_status()
        comments = comments_response.json()
        commenters = list({comment["user"]["login"] for comment in comments if comment.get("user")})

        # Add data to filtered list
        filtered_prs.append({
            "title": pr["title"],
            "number": pr["number"],
            "user": pr["user"]["login"],
            "state" : pr["state"],
            "created_at": pr["created_at"],
            "closed_at" : pr["closed_at"],
            "url": pr["html_url"],
            "admin?": pr["user"]["site_admin"],
            "reviewers": reviewers,
            "commenters": commenters
        })

    except requests.exceptions.Timeout:
        print(f"Timeout error fetching details for PR #{pr_number}. Skipping...")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching details for PR #{pr_number}: {e}")

# Step 3: Save to JSON
filename = "filtered_prs_ETC_pg2_5.json"
with open(filename, "w") as json_file:
    json.dump(filtered_prs, json_file, indent=4)

print(f"Saved {len(filtered_prs)} pull requests to {filename} ✅")
