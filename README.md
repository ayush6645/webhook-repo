# GitHub Webhook Tracker

A clean, production-ready **GitHub Webhook → Flask → MongoDB Atlas → UI** project.

This project listens to GitHub webhook events (`push`, `pull_request`, `merge`), stores **minimal structured data** in **MongoDB Atlas**, and displays recent repository activity on a simple UI that polls the backend every 15 seconds.

## 🧱 Tech Stack

*   **Backend**: Python 3.10+, Flask
*   **Database**: MongoDB Atlas (Managed Cloud DB)
*   **Frontend**: HTML5 + Vanilla JavaScript
*   **Integration**: GitHub Webhooks
*   **Tunneling**: Ngrok

## 📐 Architecture

1.  **GitHub**: Triggers a webhook (`POST /webhook`) whenever code is pushed or a PR is changed.
2.  **Ngrok**: Exposes the local Flask server to the public internet so GitHub can reach it.
3.  **Flask App**:
    *   Validates the event type.
    *   Parses strictly required fields (Author, Branch, Timestamp, Action).
    *   Saves the clean data document to MongoDB.
4.  **MongoDB Atlas**: persistently stores the event logs.
5.  **Frontend**:
    *   Polls `GET /events` every 15 seconds.
    *   Updates the DOM with new events in real-time.

## 🚀 Setup & Usage

### 1. Prerequisites
*   Python 3.10+ installed.
*   A MongoDB Atlas account & cluster.
*   An Ngrok account (free tier is fine).

### 2. Installation
```bash
# Clone the repo
git clone <repo-url>
cd github-webhook-tracker

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration
1.  Copy `.env.example` to `.env`:
    ```bash
    cp .env.example .env
    ```
2.  Open `.env` and paste your MongoDB Connection String:
    ```env
    MONGO_URI=mongodb+srv://<user>:<password>@cluster0.mongodb.net/webhook_db?retryWrites=true&w=majority
    ```

### 4. Running the App
Start the Flask backend:
```bash
python app.py
```
It will run on `http://localhost:5000`.

### 5. Exposing to the Internet
Open a new terminal and run:
```bash
ngrok http 5000
```
Copy the forwarding URL (e.g., `https://<id>.ngrok-free.app`).

### 6. GitHub Webhook Setup
1.  Go to your Repository **Settings** > **Webhooks**.
2.  Click **Add webhook**.
3.  **Payload URL**: `https://<your-ngrok-url>/webhook`
4.  **Content type**: `application/json`
5.  **Events**: Select **Push** and **Pull requests**.
6.  Click **Add webhook**.

## ✅ Verified Output

The system successfully captures:
- **Push events** (Green)
- **Pull request events** (Orange)
- **Merge events** (Purple)

Events are displayed in real-time on the UI and persisted in MongoDB Atlas.

## 🧪 Testing

1.  **Push Code**: Commit and push to your repo -> Watch it appear on `localhost:5000` (Green).
2.  **Open PR**: Create a Pull Request -> Watch it appear (Orange).
3.  **Merge PR**: Merge the Pull Request -> Watch it appear (Purple).

## 📂 Project Structure
```
github-webhook-tracker/
├── app.py                  # Main Flask application & Logic
├── requirements.txt        # Python dependencies
├── .env                    # Secrets (Excluded from Git)
├── .env.example            # Template for secrets
├── templates/
│   └── index.html          # UI Structure
└── static/
    └── main.js             # Polling & DOM Manipulation
```
