from flask import Flask
import sqlite3
from flask import g, request

app = Flask(__name__)

# 1️⃣ Home route
@app.route('/')
def home():
    return "👋 Hello! This is a beginner-level CRUD app with Flask + SQLite."

# 2️⃣ Define the database file
DATABASE = 'database.db'

# 3️⃣ Get or create DB connection
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
    return g.db

# 4️⃣ Close the DB connection after request
@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
    if db is not None:
        db.close()

# 5️⃣ Create users table
@app.route('/create')
def create_table():
    db = get_db()
    db.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT
        )
    ''')
    db.commit()
    return "✅ Table created!"

# 6️⃣ Add a user (CREATE)
@app.route('/add')
def add_user():
    db = get_db()
    db.execute("INSERT INTO users (name, email) VALUES (?, ?)", ("Charan", "charan@xyz.com"))
    db.commit()
    return "✅ User added!"

# 7️⃣ Show all users (READ)
@app.route('/users')
def show_users():
    db = get_db()
    cursor = db.execute("SELECT * FROM users")
    users = cursor.fetchall()
    result = ""
    for user in users:
        result += f"ID: {user[0]}, Name: {user[1]}, Email: {user[2]}<br>"
    return result

# 8️⃣ Update user name by ID (UPDATE)
@app.route('/update/<int:user_id>')
def update_user(user_id):
    db = get_db()
    db.execute("UPDATE users SET name = ? WHERE id = ?", ("UpdatedName", user_id))
    db.commit()
    return f"✏️ User with ID {user_id} updated!"

# 9️⃣ Delete user by ID (DELETE)
@app.route('/delete/<int:user_id>')
def delete_user(user_id):
    db = get_db()
    db.execute("DELETE FROM users WHERE id = ?", (user_id,))
    db.commit()
    return f"🗑️ User with ID {user_id} deleted!"

# 🔟 Run the app
if __name__ == '__main__':
    app.run(debug=True)
