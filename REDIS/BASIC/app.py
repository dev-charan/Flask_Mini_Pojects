from flask import Flask, jsonify
import redis
import sqlite3
import time
import json

app = Flask(__name__)

# Redis setup
cache = redis.Redis(host='localhost', port=6379, db=0)

# SQLite DB file
DB_NAME = 'users.db'

# Connect to SQLite
def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

# Setup database with sample users
def setup_database():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL
        )
    ''')
    # Add dummy data
    cursor.execute("INSERT OR IGNORE INTO users (id, name, email) VALUES (1, 'Charan', 'charan@example.com')")
    cursor.execute("INSERT OR IGNORE INTO users (id, name, email) VALUES (2, 'John', 'john@example.com')")
    conn.commit()
    conn.close()

@app.route('/user/<int:user_id>')
def get_user(user_id):
    cache_key = f"user:{user_id}"

    start = time.time()

    # Check Redis first
    if cache.exists(cache_key):
        print("✅ Redis Hit")
        user_data = json.loads(cache.get(cache_key))
    else:
        print("❌ Redis Miss → Querying SQLite")
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        conn.close()

        if not user:
            return jsonify({"error": "User not found"}), 404

        user_data = dict(user)
        # Store in Redis for next time (expires in 60s)
        cache.setex(cache_key, 60, json.dumps(user_data))

    duration = round((time.time() - start) * 1000, 2)  # in ms
    return jsonify({"user": user_data, "fetched_in_ms": duration})

if __name__ == '__main__':
    setup_database()
    app.run(debug=True)
