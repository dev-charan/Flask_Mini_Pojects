from flask import request, jsonify
from models.task import Task

# Simulated in-memory DB
tasks = []
task_id_counter = 1

def get_all_tasks():
    return jsonify([task.to_dict() for task in tasks])

def add_task():
    global task_id_counter
    data = request.get_json()
    title = data.get("title")

    if not title:
        return jsonify({"error": "Title is required"}), 400

    task = Task(task_id_counter, title)
    tasks.append(task)
    task_id_counter += 1

    return jsonify(task.to_dict()), 201
