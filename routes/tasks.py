from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.task import db, Task

tasks = Blueprint('tasks', __name__)

# Create Task
@tasks.route('/tasks', methods=['POST'])
@jwt_required()
def create_task():
    try:
        data = request.json

        # Validate required fields
        if not data or not data.get('title'):
            return jsonify({"error": "Title is required!"}), 400

        user_id = get_jwt_identity()  # Get user ID from token
        title = data.get('title')
        description = data.get('description', '')
        due_date = data.get('due_date', None)
        priority = data.get('priority', 'Medium')

        # Create and save the task
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

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Get All Tasks
@tasks.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    user_id = get_jwt_identity()  # Get user ID from token
    user_tasks = Task.query.filter_by(user_id=user_id).all()  # Filter tasks by user_id

    return jsonify([{
        "id": task.id,
        "title": task.title or "Untitled Task",
        "description": task.description or "",
        "due_date": task.due_date or None,
        "priority": task.priority or "Medium",
        "completed": task.completed or False,
    } for task in user_tasks]), 200

# Get Single Task
@tasks.route('/tasks/<int:task_id>', methods=['GET'])
@jwt_required()
def get_task(task_id):
    user_id = get_jwt_identity()  # Get user ID from token
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()  # Filter by task ID and user ID

    if task:
        return jsonify({
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "due_date": task.due_date,
            "priority": task.priority,
            "completed": task.completed
        }), 200
    else:
        return jsonify({"message": "Task not found or unauthorized!"}), 404

# Update Task
@tasks.route('/tasks/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    user_id = get_jwt_identity()  # Get user ID from token
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()  # Filter by task ID and user ID

    if not task:
        return jsonify({"message": "Task not found or unauthorized!"}), 404

    data = request.json
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.due_date = data.get('due_date', task.due_date)
    task.priority = data.get('priority', task.priority)
    task.completed = data.get('completed', task.completed)

    db.session.commit()
    return jsonify({"message": "Task updated successfully!"}), 200

# Delete Task
@tasks.route('/tasks/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    user_id = get_jwt_identity()  # Get user ID from token
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()  # Filter by task ID and user ID

    if not task:
        return jsonify({"message": "Task not found or unauthorized!"}), 404

    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted successfully!"}), 200
