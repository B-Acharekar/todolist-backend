from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.task import db, Task

tasks = Blueprint('tasks', __name__)

# Create Task
@tasks.route('/tasks', methods=['POST'])
@jwt_required()
def create_task():
    data = request.json
    user_id = get_jwt_identity()  # Get user ID from token
    title = data.get('title')
    description = data.get('description', '')
    due_date = data.get('due_date', None)
    priority = data.get('priority', 'Medium')

    new_task = Task(
        title=title,
        description=description,
        due_date=due_date,
        priority=priority,
        user_id=user_id  # Associate task with logged-in user
    )
    db.session.add(new_task)
    db.session.commit()

    return jsonify({"message": "Task created successfully!", "task_id": new_task.id}), 201
