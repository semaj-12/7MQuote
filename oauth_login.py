import os
import json
import requests
import webbrowser
from flask import Flask, request, redirect
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("FORGE_CLIENT_ID")
CLIENT_SECRET = os.getenv("FORGE_CLIENT_SECRET")
REDIRECT_URI = "http://localhost:3000/api/callback"
SCOPES = "data:read data:write data:create viewables:read account:read"

app = Flask(__name__)
tokens = {}

@app.route("/")
def login():
    auth_url = (
        f"https://developer.api.autodesk.com/authentication/v2/authorize"
        f"?response_type=code"
        f"&client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&scope={SCOPES.replace(' ', '%20')}"
    )
    return redirect(auth_url)

@app.route("/api/callback")
def callback():
    code = request.args.get("code")
    token_url = "https://developer.api.autodesk.com/authentication/v2/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI
    }

    res = requests.post(token_url, headers=headers, data=data)
    res.raise_for_status()
    token_info = res.json()

    # Save token to file
    with open("user_token.json", "w") as f:
        json.dump(token_info, f, indent=2)

    return "✅ Login successful! You may now close this window."

def start_oauth_flow():
    print("Launching browser for user login...")
    webbrowser.open("http://localhost:3000")
    app.run(port=3000)

if __name__ == "__main__":
    start_oauth_flow()
