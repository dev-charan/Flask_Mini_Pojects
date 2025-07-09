from flask import Flask
from flask_jwt_extended import JWTManager
from config import Config
from model import db
from utils.token_blocklist import is_token_revoked
from routes.auth_routes import auth
from routes.user_routes import user

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
jwt = JWTManager(app)

# Setup token revocation check
@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    return is_token_revoked(jwt_payload)

# Register Blueprints
app.register_blueprint(auth)
app.register_blueprint(user)

@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
