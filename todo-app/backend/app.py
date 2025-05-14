from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    due_date = db.Column(db.String(20))
    category = db.Column(db.String(50))
    completed = db.Column(db.Boolean, default=False)

@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([{
        'id': t.id,
        'text': t.text,
        'dueDate': t.due_date,
        'category': t.category,
        'completed': t.completed
    } for t in tasks])

@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.json
    task = Task(text=data['text'], due_date=data.get('dueDate'), category=data.get('category'))
    db.session.add(task)
    db.session.commit()
    return jsonify({'message': 'Task added'}), 201

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def toggle_complete(task_id):
    task = Task.query.get(task_id)
    task.completed = not task.completed
    db.session.commit()
    return jsonify({'message': 'Task updated'})

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    Task.query.filter_by(id=task_id).delete()
    db.session.commit()
    return jsonify({'message': 'Task deleted'})

# Make sure to wrap this
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000)
