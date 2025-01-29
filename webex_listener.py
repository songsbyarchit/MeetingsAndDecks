import os
import json
from flask import Flask, request
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

WEBEX_ACCESS_TOKEN = os.getenv("WEBEX_ACCESS_TOKEN")

app = Flask(__name__)

@app.route("/webex", methods=["POST"])
def webex_webhook():
    data = request.json

    # Ensure it's a message event
    if data.get("resource") == "messages" and data.get("event") == "created":
        message_id = data["data"]["id"]
        process_webex_message(message_id)

    return {"status": "ok"}, 200

@app.route("/callback", methods=["GET"])
def oauth_callback():
    """Handles Webex or Google OAuth callback."""
    code = request.args.get("code")
    state = request.args.get("state")

    if not code:
        return "Error: No authorization code received.", 400

    print(f"Received OAuth Code: {code}")

    return "OAuth successful! You can close this window.", 200

def process_webex_message(message_id):
    """Fetches and processes a Webex message."""
    url = f"https://webexapis.com/v1/messages/{message_id}"
    headers = {"Authorization": f"Bearer {WEBEX_ACCESS_TOKEN}", "Content-Type": "application/json"}
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        message_text = response.json().get("text", "").lower()
        print(f"Received message: {message_text}")

        # TODO: Implement NLP to parse meeting details and call Google Calendar API

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)