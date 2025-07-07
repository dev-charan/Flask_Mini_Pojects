from flask import Flask
from auth.route import auth_bp  # Import the blueprint

app = Flask(__name__)

# Register the blueprint
app.register_blueprint(auth_bp, url_prefix='/auth')

@app.route('/')
def home():
    return 'Welcome Home!'

if __name__ == '__main__':
    app.run(debug=True)
