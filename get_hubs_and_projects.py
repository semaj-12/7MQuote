import json
import requests

# Load the access token from file
with open("user_token.json") as f:
    token_data = json.load(f)

access_token = token_data["access_token"]

# Prepare headers for the API request
headers = {
    "Authorization": f"Bearer {access_token}"
}

# STEP 1: Get list of hubs
print("\n🔹 Fetching hubs...\n")
hubs_response = requests.get("https://developer.api.autodesk.com/project/v1/hubs", headers=headers)
hubs_response.raise_for_status()
hubs = hubs_response.json()["data"]

for hub in hubs:
    print(f"Hub Name: {hub['attributes']['name']}")
    print(f"Hub ID:   {hub['id']}\n")

# (Optional) After finding your desired hubId, paste it below to get its projects:
hub_id = input("📥 Enter a hubId to list its projects: ")

# STEP 2: Get projects inside that hub
print("\n🔹 Fetching projects...\n")
projects_response = requests.get(f"https://developer.api.autodesk.com/project/v1/hubs/{hub_id}/projects", headers=headers)
projects_response.raise_for_status()
projects = projects_response.json()["data"]

for project in projects:
    print(f"Project Name: {project['attributes']['name']}")
    print(f"Project ID:   {project['id']}\n")
