from flask import Flask, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    
@app.route('/create')
def create_table():
    db.create_all()  # creates tables from all defined models
    return "<h3>✅ Table created! <a href='/'>Back</a></h3>"

@app.route('/add', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        user = User(name=name, email=email)
        db.session.add(user)
        db.session.commit()
        return redirect('/users')
    return '''
        <h3>Add User</h3>
        <form method="post">
            Name: <input name="name"><br>
            Email: <input name="email"><br><br>
            <button type="submit">Add</button>
        </form>
        <a href="/">Back</a>
    '''
    
@app.route('/users')
def show_users():
    users = User.query.all()
    result = "<h3>Users List</h3><ul>"
    for user in users:
        result += f"<li>ID: {user.id}, Name: {user.name}, Email: {user.email} " \
                  f"<a href='/update/{user.id}'>✏️ Edit</a> | " \
                  f"<a href='/delete/{user.id}'>🗑️ Delete</a></li>"
    result += "</ul><a href='/'>Back</a>"
    return result

@app.route('/update/<int:user_id>', methods=['GET', 'POST'])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return "<h3>User not found</h3><a href='/users'>Back</a>"

    if request.method == 'POST':
        user.name = request.form['name']
        user.email = request.form['email']
        db.session.commit()
        return redirect('/users')

    return f'''
        <h3>Edit User</h3>
        <form method="post">
            Name: <input name="name" value="{user.name}"><br>
            Email: <input name="email" value="{user.email}"><br><br>
            <button type="submit">Update</button>
        </form>
        <a href="/users">Back</a>
    '''
@app.route('/delete/<int:user_id>')
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
    return redirect('/users')
