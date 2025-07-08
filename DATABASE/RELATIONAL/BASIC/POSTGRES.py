from flask import Flask, g
import psycopg2

app = Flask(__name__)

# PostgreSQL DB connection details
DB_NAME = "testdb"
DB_USER = "postgres"
DB_PASSWORD = "your_password"
DB_HOST = "localhost"
DB_PORT = "5432"

# 1️⃣ Connect to PostgreSQL
def get_db():
    if 'db' not in g:
        g.db = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
    return g.db

# 2️⃣ Close DB connection after request
@app.teardown_appcontext    
def close_db(error):
    db = g.pop('db', None)
    if db is not None:
        db.close()

# 3️⃣ Home route
@app.route('/')
def home():
    return "👋 Hello! Flask + PostgreSQL Beginner CRUD"

# 4️⃣ Create table
@app.route('/create')
def create_table():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name TEXT,
            email TEXT
        )
    ''')
    db.commit()
    cursor.close()
    return "✅ Table created!"

# 5️⃣ Add a user (CREATE)
@app.route('/add')
def add_user():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", ("Charan", "charan@xyz.com"))
    db.commit()
    cursor.close()
    return "✅ User added!"

# 6️⃣ Show users (READ)
@app.route('/users')
def show_users():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    
    result = ""
    for user in users:
        result += f"ID: {user[0]}, Name: {user[1]}, Email: {user[2]}<br>"
    return result

# 7️⃣ Update user (UPDATE)
@app.route('/update/<int:user_id>')
def update_user(user_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("UPDATE users SET name = %s WHERE id = %s", ("UpdatedName", user_id))
    db.commit()
    cursor.close()
    return f"✏️ User with ID {user_id} updated!"

# 8️⃣ Delete user (DELETE)
@app.route('/delete/<int:user_id>')
def delete_user(user_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
    db.commit()
    cursor.close()
    return f"🗑️ User with ID {user_id} deleted!"

# 9️⃣ Run the app
if __name__ == '__main__':
    app.run(debug=True)
