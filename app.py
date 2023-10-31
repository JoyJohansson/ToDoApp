import json
from urllib import response
from flask import Flask, request

app = Flask(__name__)

#`PUT /tasks/{task_id}` Uppdaterar en task med ett specifikt id.
@app.route("/tasks/<task_id>", methods=["PUT"])
def update(task_id):
    with open("task.json") as f:
        content = json.load(f)

    for c in content:
        print(c["id"])
        if c["id"] == int(task_id):
            print(task_id)
            c.update(request.json)
            with open("task.json", "w", encoding="utf-8") as f:
                json.dump(content, f)
            return json.dumps(c)
    return json.dumps({"errorcode" : "404", "message" : "task not found"})
        
        

#`PUT /tasks/{task_id}/complete` Markerar en task som färdig.
@app.route("/tasks/<task_id>/complete", methods=["PUT"])
def mark_complete(task_id):
    with open("task.json") as f:
        content = json.load(f)

    for c in content:
        if c["id"] == int(task_id):
            c["status"] = "complete"
            with open("task.json", "w", encoding="utf-8") as f:
                json.dump(content, f)
            return json.dumps({"message":"Your task is now marked as completed"})

#`GET /tasks/categories/` Hämtar alla olika kategorier.
@app.route("/tasks/categories/", methods=["GET"])
def categories():
    with open("task.json") as f:
        content = json.load(f)
    categories = []
    for c in content:
        categories.append(c["category"])
    
    return json.dumps(categories)


#`GET /tasks/categories/{category_name}` Hämtar alla tasks från en specifik kategori.
@app.route("/tasks/categories/<category_name>", methods=["GET"])
def by_category(category_name):
    with open("task.json") as f:
        content = json.load(f)
    tasks = []
    for c in content:
        if c["category"] == str(category_name):
            tasks.append(c)
    
    return json.dumps(tasks)