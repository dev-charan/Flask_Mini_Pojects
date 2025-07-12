from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])  # allow only this origin

@app.route("/data")
def get_data():
    return {"message": "CORS success!"}
