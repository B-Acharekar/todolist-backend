from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from models.task import db, User

auth = Blueprint('auth', __name__)

# User Registration
@auth.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if User.query.filter_by(username=username).first():
        return jsonify({"message": "User already exists!"}), 400

    # Hash password before saving
    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully!"}), 201

# User Login
@auth.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):  # Check if password is correct
        # Create JWT token with user id
        access_token = create_access_token(identity=user.id)
        return jsonify({"message": "User logged in successfully!", "access_token": access_token}), 200
    else:
        return jsonify({"message": "Invalid credentials!"}), 401
