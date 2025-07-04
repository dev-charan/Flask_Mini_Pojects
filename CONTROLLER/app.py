from flask import Flask
from controllers import task_controller

app = Flask(__name__)

@app.route("/tasks", methods=["GET"])
def list_tasks():
    return task_controller.get_all_tasks()

@app.route("/tasks", methods=["POST"])
def create_task():
    return task_controller.add_task()

if __name__ == "__main__":
    app.run(debug=True)
