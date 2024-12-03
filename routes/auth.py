from flask import Blueprint, request, jsonify
from models.task import db, User

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if User.query.filter_by(username=username).first():
        return jsonify({"message": "User already exists!"}), 400

    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully!"}), 201

@auth.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username, password=password).first()
    if user:
        return jsonify({"message": "User logged in successfully!"}), 200
    else:
        return jsonify({"message": "Invalid credentials!"}), 401

@auth.route('/logout', methods=['POST'])
def logout():
    return jsonify({"message": "User logged out successfully!"}), 200

@auth.route('/delete-account', methods=['DELETE'])
def delete_account():
    data = request.json
    username = data.get('username')
    user = User.query.filter_by(username=username).first()

    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User account deleted successfully!"}), 200
    else:
        return jsonify({"message": "User not found!"}), 404
