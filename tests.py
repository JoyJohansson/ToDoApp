import json
import unittest
from unittest.mock import patch, mock_open
from flask import Flask, request, jsonify

app = Flask(__name__)

# Hjälpfunktion för att hämta uppgifter från fil
def get_tasks():
    try:
        with open("task.json") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_tasks(tasks):
    with open("task.json", "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=4)

# 1. `GET /tasks` Hämtar alla uppgifter. För VG: lägg till en parameter `completed`
# som kan filtrera på färdiga eller ofärdiga uppgifter.
@app.route('/tasks', methods=['GET'])
def get_all_tasks():
    tasks = get_tasks()

    completed_param = request.args.get('completed')

    if completed_param == 'true':
        completed_tasks = [task for task in tasks if task['status'] == 'completed']
        return jsonify(completed_tasks)
    elif completed_param == 'false':
        incomplete_tasks = [task for task in tasks if task['status'] == 'pending']
        return jsonify(incomplete_tasks)
    else:
        return jsonify(tasks)

# 2. `POST /tasks` Lägger till en ny uppgift. Uppgiften är ofärdig när den först läggs till.
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
    tasks.append(new_task)
    save_tasks(tasks)

    return jsonify(new_task), 201

# 3. `GET /tasks/{task_id}` Hämtar en uppgift med ett specifikt id.
@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = next((t for t in get_tasks() if t['id'] == task_id), None)

    if task:
        return jsonify(task)
    return jsonify({"message": "Uppgiften hittades inte."}), 404

# 4. `DELETE /tasks/{task_id}` Tar bort en uppgift med ett specifikt id.
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    tasks = get_tasks()
    task = next((t for t in tasks if t['id'] == task_id), None)

    if task:
        tasks.remove(task)
        save_tasks(tasks)

        return jsonify({"message": "Uppgiften har tagits bort."}), 202
    return jsonify({"message": "Uppgiften hittades inte."}), 404

# 5. `PUT /tasks/{task_id}` Uppdaterar en uppgift med ett specifikt id.
@app.route("/tasks/<task_id>", methods=["PUT"])
def update(task_id):
    tasks = get_tasks()

    for c in tasks:
        if c["id"] == int(task_id):
            c.update(request.json)
            save_tasks(tasks)
            return jsonify(c)
    return jsonify({"errorcode": "404", "message": "uppgiften hittades inte"})

# 6. `PUT /tasks/{task_id}/complete` Markerar en uppgift som färdig.
@app.route("/tasks/<task_id>/complete", methods=["PUT"])
def mark_complete(task_id):
    tasks = get_tasks()

    for c in tasks:
        if c["id"] == int(task_id):
            c["status"] = "completed"
            save_tasks(tasks)
            return jsonify({"message": "Din uppgift är nu markerad som färdig"})

# 7. `GET /tasks/categories/` Hämtar alla olika kategorier.
@app.route("/tasks/categories/", methods=["GET"])
def categories():
    tasks = get_tasks()
    categories = set()
    for c in tasks:
        categories.add(c["category"])
    
    return jsonify(list(categories))

# 8. `GET /tasks/categories/{category_name}` Hämtar alla uppgifter från en specifik kategori.
@app.route("/tasks/categories/<category_name>", methods=["GET"])
def by_category(category_name):
    tasks = get_tasks()
    tasks_by_category = [task for task in tasks if task["category"] == category_name]
    
    return jsonify(tasks_by_category)

class TestApp(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps([]))
    def test_get_all_tasks(self, mock_file):
        response = self.app.get('/tasks')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, [])

    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps([]))
    def test_add_task(self, mock_file):
        new_task = {'id': 1, 'description': 'Test task', 'category': 'Test category'}
        response = self.app.post('/tasks', json=new_task)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data, new_task)

        # Check that the file was not modified
        mock_file.assert_called_with('task.json', 'r')
        mock_file().write.assert_not_called()

    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps([]))
    def test_get_task(self, mock_file):
        task_id = 1
        response = self.app.get(f'/tasks/{task_id}')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data, {"message": "Uppgiften hittades inte."})

    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps([]))
    def test_delete_task(self, mock_file):
        task_id = 1
        response = self.app.delete(f'/tasks/{task_id}')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data, {"message": "Uppgiften hittades inte."})

    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps([]))
    def test_update(self, mock_file):
        task_id = 1
        update_data = {'description': 'Updated task'}
        response = self.app.put(f'/tasks/{task_id}', json=update_data)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data, {"errorcode": "404", "message": "uppgiften hittades inte"})

    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps([]))
    def test_mark_complete(self, mock_file):
        task_id = 1
        response = self.app.put(f'/tasks/{task_id}/complete')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data, {"errorcode": "404", "message": "uppgiften hittades inte"})

    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps([]))
    def test_categories(self, mock_file):
        response = self.app.get('/tasks/categories/')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, [])

    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps([]))
    def test_by_category(self, mock_file):
        category_name = 'Test Category'
        response = self.app.get(f'/tasks/categories/{category_name}')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, [])


import my_module  # Importera modulen som innehåller filhanteringskoden

class TestMockFile(unittest.TestCase):
    @patch('builtins.open', new_callable=mock_open, read_data='{"key": "value"}')
    def test_read_data(self, mock_file):
        # Anropa en funktion som läser från filen
        data = my_module.read_data_from_file('mock_file.json')
        self.assertEqual(data, {"key": "value"})

    @patch('builtins.open', new_callable=mock_open)
    def test_write_data(self, mock_file):
        # Skapa testdata
        data_to_write = {"new_key": "new_value"}

        # Anropa en funktion som skriver till filen
        my_module.write_data_to_file('mock_file.json', data_to_write)

        # Verifiera att rätt data har skrivits till mock-filen
        mock_file().write.assert_called_once_with(json.dumps(data_to_write, indent=4))

if __name__ == '__main__':
    unittest.main()
