from flask import Flask, request, jsonify, make_response
from flask_wtf.csrf import CSRFProtect, generate_csrf
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret-key'

# Enable CORS for frontend (adjust origin as needed)
CORS(app, supports_credentials=True)

# Enable CSRF protection
csrf = CSRFProtect(app)

@app.after_request
def set_csrf_cookie(response):
    token = generate_csrf()
    response.set_cookie('csrf_token', token, httponly=False)  # Set to True for production
    return response

@app.route('/submit', methods=['POST'])
def handle_form():
    # Validate CSRF token
    token = request.headers.get('X-CSRFToken')
    if not token:
        return jsonify({"error": "Missing CSRF token"}), 400

    return jsonify({"message": "Form submitted securely!"})

@app.route('/')
def home():
    return jsonify({"message": "Backend running"})
