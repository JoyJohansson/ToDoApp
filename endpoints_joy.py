from flask import Flask, request
import json

app = Flask(__name__)

tasks = []

def find_task_by_id(task_id):
    for task in tasks:
        if task['id'] == task_id:
            return task
    return None

# 1. `GET /tasks` Hämtar alla tasks. För VG: lägg till en parameter `completed` som kan filtrera på färdiga eller ofärdiga tasks.
@app.route('/tasks', methods=['GET'])
def get_tasks():
    completed_param = request.args.get('completed')
    
    if completed_param == 'true':
        completed_tasks = [task for task in tasks if task['status'] == 'completed']
        return json.dumps(completed_tasks), 200, {'Content-Type': 'application/json'}
    elif completed_param == 'false':
        incomplete_tasks = [task for task in tasks if task['status'] == 'pending']
        return json.dumps(incomplete_tasks), 200, {'Content-Type': 'application/json'}
    else:
        return json.dumps(tasks), 200, {'Content-Type': 'application/json'}


# 2. `POST /tasks` Lägger till en ny task. Tasken är ofärdig när den först läggs till.
@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    if not data or 'id' not in data or 'description' not in data or 'category' not in data:
        return "Invalid request data. Make sure to provide 'id', 'description', and 'category' in JSON format.", 400

    new_task = {
        'id': data['id'],
        'description': data['description'],
        'category': data['category'],
        'status': 'pending'
    }
    tasks.append(new_task)
    return json.dumps(new_task), 201, {'Content-Type': 'application/json'}


# 3. `GET /tasks/{task_id}` Hämtar en task med ett specifikt id.
@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = find_task_by_id(task_id)
    if task:
        return json.dumps(task), 200, {'Content-Type': 'application/json'}
    return "Task not found", 404

# 4. `DELETE /tasks/{task_id}` Tar bort en task med ett specifikt id.
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = find_task_by_id(task_id)
    if task:
        tasks.remove(task)
        return "Task deleted", 204
    return "Task not found", 404

if __name__ == '__main__':
    app.run(debug=True)
