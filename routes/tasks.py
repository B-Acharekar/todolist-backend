from flask import Blueprint, request, jsonify
from models.task import db, Task

tasks = Blueprint('tasks', __name__)

# Create Task
@tasks.route('/tasks', methods=['POST'])
def create_task():
    data = request.json
    title = data.get('title')
    description = data.get('description')
    due_date = data.get('due_date')
    priority = data.get('priority')

    new_task = Task(title=title, description=description, due_date=due_date, priority=priority)
    db.session.add(new_task)
    db.session.commit()

    return jsonify({"message": "Task created successfully!", "task": new_task.id}), 201

# Get All Tasks
@tasks.route('/tasks', methods=['GET'])
def get_tasks():
    sort_by = request.args.get('sort_by', 'priority')  # Sorting query parameter
    
    if sort_by not in ['priority', 'due_date']:
        return jsonify({"message": "Invalid sort criteria!"}), 400

    tasks = Task.query.order_by(getattr(Task, sort_by)).all()  # Sorting tasks by the specified field
    return jsonify({
        "tasks": [
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "due_date": task.due_date,
                "priority": task.priority,
                "status": task.status,
                "completed": task.completed
            }
            for task in tasks
        ]
    }), 200

# Get Single Task
@tasks.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = Task.query.get(task_id)
    if task:
        return jsonify({
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "due_date": task.due_date,
            "priority": task.priority,
            "status": task.status,
            "completed": task.completed
        }), 200
    else:
        return jsonify({"message": "Task not found!"}), 404

# Update Task (Including Marking Completion/Undo)
@tasks.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"message": "Task not found!"}), 404

    data = request.json
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.due_date = data.get('due_date', task.due_date)
    task.priority = data.get('priority', task.priority)
    task.status = data.get('status', task.status)
    task.completed = data.get('completed', task.completed)  # Updating completion status

    db.session.commit()
    return jsonify({"message": "Task updated successfully!"}), 200

# Delete Task
@tasks.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"message": "Task not found!"}), 404

    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted successfully!"}), 200

# Toggle Task Completion (Complete/Undo)
@tasks.route('/tasks/<int:task_id>/toggle-completion', methods=['PATCH'])
def toggle_task_completion(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"message": "Task not found!"}), 404

    task.completed = not task.completed  # Toggle completion status
    db.session.commit()
    return jsonify({
        "message": "Task completion status updated successfully!",
        "completed": task.completed
    }), 200
