import json
from flask import Flask, request, jsonify, make_response, render_template

app = Flask(__name__)

def get_tasks():
    with open("./ToDoApp/task.json") as f:
        return json.load(f)

def find_task_by_id(task_id):
    tasks = get_tasks()
    for task in tasks:
        if task['id'] == task_id:
            return task
    return None

# 1. `GET /tasks` Hämtar alla tasks. För VG: lägg till en parameter `completed` 
# som kan filtrera på färdiga eller ofärdiga tasks.
@app.route('/tasks', methods=['GET'])
def get_all_tasks():
    tasks = get_tasks()
    render_template('tasks.html', tasks=tasks)

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
        

# 2. `POST /tasks` Lägger till en ny task. Tasken är ofärdig när den först läggs till.
@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    if not data or 'id' not in data or 'description' not in data or 'category' not in data:
        return jsonify({"message": "Ogiltig begäran. Se till att tillhandahålla 'id', 'description' och 'category' i JSON-format."}), 400

    new_task = {
        'id': data['id'],
        'description': data['description'],
        'category': data['category'],
        'status': 'pending'
    }

    tasks = get_tasks()
    if any(task['id'] == new_task['id'] for task in tasks):
        return jsonify({"message": "En uppgift med samma ID finns redan."}), 400

    tasks.append(new_task)

    with open("./ToDoApp/task.json", "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=4)

    return jsonify(new_task), 201

# 3. `GET /tasks/{task_id}` Hämtar en task med ett specifikt id.
@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = find_task_by_id(task_id)
    if task:
        return jsonify(task), 200
    return jsonify({"message": "Uppgiften hittades inte."}), 418 # I´m a tea pot (404)

SECRET_TOKEN = "my_secret_token"
def authenticate_token():
    token = request.headers.get("Authorization")

    if token == f"Bearer {SECRET_TOKEN}":
        return True

    return False

def check_authentication():
    if request.endpoint != "authenticate":
        if not authenticate_token():
            return make_response(jsonify({"message": "Autentisering misslyckades."}), 401)

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    if not authenticate_token():
        return make_response(jsonify({"message": "Autentisering misslyckades."}), 401)
    tasks = get_tasks()
    task = next((t for t in tasks if t['id'] == task_id), None)

    if task:
        tasks.remove(task)

        with open("./ToDoApp/task.json", "w", encoding="utf-8") as f:
            json.dump(tasks, f, indent=4)

        return jsonify({"message": "Uppgiften har tagits bort."}), 202
    return jsonify({"message": "Uppgiften hittades inte."}), 418 # I´m a tea pot (404)

# 5. `PUT /tasks/{task_id}` Uppdaterar en task med ett specifikt id.
@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update(task_id):
    tasks = get_tasks()

    for task in tasks:
        if task['id'] == task_id:
            data = request.get_json()
            task.update(data)
            with open("./ToDoApp/task.json", "w", encoding="utf-8") as f:
                json.dump(tasks, f, indent=4)
            return jsonify(task)
    return jsonify({"message": "Uppgiften hittades inte."}), 418 # I´m a tea pot (404)

# 6. `PUT /tasks/{task_id}/complete` Markerar en task som färdig.
@app.route("/tasks/<int:task_id>/complete", methods=["PUT"])
def mark_complete(task_id):
    tasks = get_tasks()

    for task in tasks:
        if task['id'] == task_id:
            task["status"] = "completed"
            with open("./ToDoApp/task.json", "w", encoding="utf-8") as f:
                json.dump(tasks, f, indent=4)
            return jsonify({"message": "Din uppgift är nu markerad som avslutad."})

# 7. `GET /tasks/categories/` Hämtar alla olika kategorier.
@app.route("/tasks/categories/", methods=["GET"])
def categories():
    tasks = get_tasks()
    categories = set(task["category"] for task in tasks)
    return jsonify(list(categories))

# 8. `GET /tasks/categories/{category_name}` Hämtar alla tasks från en specifik kategori.
@app.route("/tasks/categories/<category_name>", methods=["GET"])
def by_category(category_name):
    tasks = get_tasks()
    tasks_by_category = [task for task in tasks if task["category"] == category_name]
    if tasks_by_category:
        return jsonify(tasks_by_category), 200
    return jsonify({"message": "Inga uppgifter hittades i den angivna kategorin."}), 418 # I´m a tea pot (404)

if __name__ == '__main__':
    app.run(debug=True)
