import json
from flask import Flask, request, jsonify, make_response

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
        return "Ogiltig begäran. Se till att tillhandahålla 'id', 'description' och 'category' i JSON-format.", 400

    new_task = {
        'id': data['id'],
        'description': data['description'],
        'category': data['category'],
        'status': 'pending'
    }

    tasks = get_task()
    tasks.append(new_task)

    with open("task.json", "w", encoding="utf-8") as f:
        json.dump(tasks, f)

    response = json.dumps(new_task)
    return response, 201, {'Content-Type': 'application/json'}

# 3. `GET /tasks/{task_id}` Hämtar en task med ett specifikt id.
@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = find_task_by_id(task_id)
    if task:
        response = json.dumps(task)
        return response, 200, {'Content-Type': 'application/json'}
    return "Uppgiften hittades inte.", 418 # I´m a tea pot (404)

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
    print("HEllo")
    if not authenticate_token():
            return make_response(jsonify({"message": "Autentisering misslyckades."}), 401)
    tasks = get_tasks()
    task = next((t for t in tasks if t['id'] == task_id), None)

    if task:
        tasks.remove(task)

        with open("task.json", "w", encoding="utf-8") as f:
            json.dump(tasks, f, indent=4)

        return make_response(jsonify({"message": "Uppgiften har tagits bort."}), 202)
    return make_response(jsonify({"message": "Uppgiften hittades inte."}), 404)


# 5. `PUT /tasks/{task_id}` Uppdaterar en task med ett specifikt id.
@app.route("/tasks/<task_id>", methods=["PUT"])
def update(task_id):
    tasks = get_tasks()

    for c in tasks:
        print(c["id"])
        if c["id"] == int(task_id):
            c.update(request.json)
            with open("task.json", "w", encoding="utf-8") as f:
                json.dump(tasks, f)
            return json.dumps(c)
    return json.dumps({"errorcode" : "404", "message" : "task not found"})
        
    
# 6. `PUT /tasks/{task_id}/complete` Markerar en task som färdig.
@app.route("/tasks/<task_id>/complete", methods=["PUT"])
def mark_complete(task_id):
    tasks = get_tasks()

    for c in tasks:
        if c["id"] == int(task_id):
            c["status"] = "complete"
            with open("task.json", "w", encoding="utf-8") as f:
                json.dump(tasks, f)
            return json.dumps({"message":"Your task is now marked as completed"})


# 7. `GET /tasks/categories/` Hämtar alla olika kategorier.
@app.route("/tasks/categories/", methods=["GET"])
def categories():
    tasks = get_tasks()
    categories = []
    for c in tasks:
        categories.append(c["category"])
        #TODO gruppera kategorinamn
    
    return json.dumps(categories)


# 8.`GET /tasks/categories/{category_name}` Hämtar alla tasks från en specifik kategori.
@app.route("/tasks/categories/<category_name>", methods=["GET"])
def by_category(category_name):
    tasks = get_tasks()
    tasks_by_category = []
    for c in tasks:
        if c["category"] == str(category_name):
            tasks_by_category.append(c)
    
    return json.dumps(tasks)

if __name__ == '__main__':
    app.run(debug=True)