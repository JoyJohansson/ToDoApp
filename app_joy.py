from flask import Flask, request
import json

app = Flask(__name__)

tasks = []

def find_task_by_id(task_id):
    for task in tasks:
        if task['id'] == task_id:
            return task
    return None

@app.route('/tasks', methods=['GET'])
def get_tasks():
    completed_param = request.args.get('completed')

    if completed_param == 'true':
        completed_tasks = [task for task in tasks if task['status'] == 'completed']
        response = json.dumps(completed_tasks)
        return response, 200, {'Content-Type': 'application/json'}
    elif completed_param == 'false':
        incomplete_tasks = [task for task in tasks if task['status'] == 'pending']
        response = json.dumps(incomplete_tasks)
        return response, 200, {'Content-Type': 'application/json'}
    elif completed_param is None:
        response = json.dumps(tasks)
        return response, 200, {'Content-Type': 'application/json'}
    else:
        return "Felaktig parameter för 'completed'. Använd 'true' eller 'false' för att filtrera färdiga eller ofärdiga uppgifter.", 400

@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    if not data or 'id' not in data or 'description' not in data or 'category' not in data:
        return "Ogiltig begäran. Se till att tillhandahålla 'id', 'description' och 'category' i JSON-format.", 400

    new_task = {
        'id': data['id'],
        'description': data['description'],
        'category': data['category'],
        'status': 'pending'
    }
    tasks.append(new_task)
    response = json.dumps(new_task)
    return response, 201, {'Content-Type': 'application/json'}

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = find_task_by_id(task_id)
    if task:
        response = json.dumps(task)
        return response, 200, {'Content-Type': 'application/json'}
    return "Uppgiften hittades inte.", 418 # I´m a tea pot (404)

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = find_task_by_id(task_id)
    if task:
        tasks.remove(task)
        return "Uppgiften har tagits bort.", 204
    return "Uppgiften hittades inte.", 418 # I´m a tea pot (404)

if __name__ == '__main__':
    app.run(debug=True)
