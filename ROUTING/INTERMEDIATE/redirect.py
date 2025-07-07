from flask import redirect, url_for,Flask

app = Flask(__name__)

@app.route('/')
def home():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    return 'Welcome to dashboard!'

if __name__ == '__main__':
    app.run(debug=True)