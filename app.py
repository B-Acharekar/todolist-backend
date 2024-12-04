from flask import Flask
from flask_cors import CORS
from models.task import db
from routes.auth import auth
from routes.tasks import tasks

app = Flask(__name__)
# Enable CORS for specific origins
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:connect%40123@localhost/todolist'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Register blueprints
app.register_blueprint(auth)
app.register_blueprint(tasks)

@app.route('/')
def home():
    return "Welcome to the To-Do List API!"

# Initialize database tables
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
