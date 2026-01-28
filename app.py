from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import datetime
from dateutil import parser

# Load environment variables
load_dotenv()

app = Flask(__name__)

# MongoDB Configuration
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client.webhook_db
events_collection = db.events

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok"}), 200

@app.route('/webhook', methods=['POST'])
def webhook():
    event_type = request.headers.get('X-GitHub-Event')
    payload = request.json
    
    if not payload:
        return jsonify({"error": "No payload received"}), 400

    data = None
    
    try:
        if event_type == 'push':
            # Extract branch name from ref (e.g., refs/heads/main -> main)
            ref = payload.get('ref', '')
            branch = ref.split('/')[-1] if ref else ''
            
            data = {
                "request_id": payload.get('head_commit', {}).get('id'),
                "author": payload.get('pusher', {}).get('name'),
                "action": "PUSH",
                "from_branch": "",
                "to_branch": branch,
                "timestamp": payload.get('head_commit', {}).get('timestamp')
            }

        elif event_type == 'pull_request':
            pr = payload.get('pull_request', {})
            action = payload.get('action')
            
            # Check for Merge
            if action == 'closed' and pr.get('merged') is True:
                data = {
                    "request_id": str(pr.get('id')),
                    "author": pr.get('user', {}).get('login'),
                    "action": "MERGE",
                    "from_branch": pr.get('head', {}).get('ref'),
                    "to_branch": pr.get('base', {}).get('ref'),
                    "timestamp": pr.get('merged_at') or datetime.datetime.utcnow().isoformat()
                }
            # Check for Open
            elif action == 'opened':
                data = {
                    "request_id": str(pr.get('id')),
                    "author": pr.get('user', {}).get('login'),
                    "action": "PULL_REQUEST",
                    "from_branch": pr.get('head', {}).get('ref'),
                    "to_branch": pr.get('base', {}).get('ref'),
                    "timestamp": pr.get('created_at')
                }
        
        if data:
            # Ensure timestamp is standard ISO format if possible, but spec says "UTC datetime string"
            # MongoDB handles strings fine, but for sorting, consisteny helps.
            # Using the string directly from GitHub is usually ISO 8601.
            events_collection.insert_one(data)
            return jsonify({"status": "success"}), 200
        else:
            # We ignore other actions (like PR sync, etc.) as per spec "Store only required data"
            return jsonify({"status": "ignored"}), 200

    except Exception as e:
        print(f"Error processing webhook: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

@app.route('/events', methods=['GET'])
def get_events():
    # Returns latest 20 events, sorted by timestamp descending
    cursor = events_collection.find({}, {'_id': 0}).sort("timestamp", -1).limit(20)
    events = list(cursor)
    return jsonify(events)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
