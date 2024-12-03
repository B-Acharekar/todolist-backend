from flask import Flask
from flask_cors import CORS
from models.task import db, User, Task  # Updated import path
from routes.auth import auth
from routes.tasks import tasks

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:connect%40123@localhost/todolist'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)  # Initialize the db with the app

app.register_blueprint(auth)
app.register_blueprint(tasks)  # Register the tasks blueprint to the app route prefix '/tasks'

@app.route('/')
def home():
    return "Welcome to the To-Do List API!"

# Create database tables within the application context
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
