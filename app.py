import os
import re
import sqlite3
from flask import Flask, render_template, request, jsonify

# Use the exact folder names in your project.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "Templates"),
    static_folder=os.path.join(BASE_DIR, "Static")
)

DATA_DIR = os.environ.get("DB_DIR", BASE_DIR)

# Make relative database paths resolve from the project directory.
if not os.path.isabs(DATA_DIR):
    DATA_DIR = os.path.join(BASE_DIR, DATA_DIR)

DB_PATH = os.path.join(DATA_DIR, "messages.db")


def get_db_connection():
    os.makedirs(DATA_DIR, exist_ok=True)
    connection = sqlite3.connect(DB_PATH, timeout=15)
    connection.row_factory = sqlite3.Row
    return connection


def create_table():
    with get_db_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                company_name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT NOT NULL,
                consent INTEGER NOT NULL DEFAULT 1
            )
        """)


# Create the database table when the application starts.
create_table()


@app.route("/")
def index():
    return render_template("web.html")


@app.route("/api/messages", methods=["POST"])
def create_message():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "success": False,
            "message": "Invalid request data."
        }), 400

    full_name = str(data.get("full_name") or "").strip()
    company_name = str(data.get("company_name") or "").strip()
    email = str(data.get("email") or "").strip()
    phone = str(data.get("phone") or "").strip()
    consent = data.get("consent") is True

    if not all([full_name, company_name, email, phone]):
        return jsonify({
            "success": False,
            "message": "Please fill in all fields."
        }), 400

    if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
        return jsonify({
            "success": False,
            "message": "Please enter a valid email address."
        }), 400

    if not consent:
        return jsonify({
            "success": False,
            "message": "Please agree to the privacy policy."
        }), 400

    try:
        with get_db_connection() as connection:
            connection.execute("""
                INSERT INTO messages (
                    full_name,
                    company_name,
                    email,
                    phone,
                    consent
                )
                VALUES (?, ?, ?, ?, ?)
            """, (
                full_name,
                company_name,
                email,
                phone,
                1
            ))

        return jsonify({
            "success": True,
            "message": "Your message has been sent successfully!"
        }), 201

    except (sqlite3.Error, OSError):
        app.logger.exception("Failed to save contact form submission")
        return jsonify({
            "success": False,
            "message": "Unable to save your message. Please try again."
        }), 500


@app.route("/api/messages", methods=["GET"])
def get_messages():
    try:
        with get_db_connection() as connection:
            rows = connection.execute("""
                SELECT id, full_name, company_name,
                       email, phone, consent
                FROM messages
                ORDER BY id DESC
            """).fetchall()

        return jsonify([dict(row) for row in rows]), 200

    except (sqlite3.Error, OSError):
        app.logger.exception("Failed to retrieve messages")
        return jsonify({
            "success": False,
            "message": "Unable to retrieve messages."
        }), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)