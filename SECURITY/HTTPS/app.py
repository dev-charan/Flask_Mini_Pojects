from flask import Flask
from flask_talisman import Talisman

app = Flask(__name__)
Talisman(app)  # Redirects all traffic to HTTPS and sets security headers

@app.route('/')
def home():
    return "This is a secure page."

if __name__ == '__main__':
    app.run(debug=True)
