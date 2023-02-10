from flask import abort, jsonify, request
from api.endpoints import api_views
from models import storage
from models.user import User
from models.task import Task

@api_views.route("/<user_id>/tasks", strict_slashes=False)
def undone_tasks(user_id):
    """Returns all undone tasks of a user"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    task_json = []
    for task in user.tasks:
        if task.status == "in progress":
            task_json.append(task.to_dict())
    return jsonify(task_json)

@api_views.route("/<user_id>/tasks", methods=["POST"], strict_slashes=False)
def create_task(user_id):
    """Creates a new task for a user"""
    if request.content_type != "application/json":
        abort(400, description="Not a JSON")
    data = request.get_json()
    if "title" not in data:
        abort(400, description="Missing title")
    if "deadline" not in data:
        abort(400, description="Missing deadline")
    if "description" not in data:
        data["description"] = ""
    if "steps" not in data:
        data["steps"] = []
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    user.create_task(
                    title=data["title"], 
                    description=data["description"], 
                    deadline=data["deadline"], 
                    steps=data["steps"],
                    )
    return jsonify({})

@api_views.route("/<user_id>/tasks/<subordinate_id>", methods=["POST"], strict_slashes=False)
def create_subtask(user_id, subordinate_id):
    """Creates a new task for a subordinate"""
    if request.content_type != "application/json":
        abort(400, description="Not a JSON")
    data = request.get_json()
    if "title" not in data:
        abort(400, description="Missing title")
    if "deadline" not in data:
        abort(400, description="Missing deadline")
    if "description" not in data:
        data["description"] = ""
    if "steps" not in data:
        data["steps"] = []
    user = storage.get(User, user_id)
    subordinate = storage.get(User, subordinate_id)
    if not user or not subordinate:
        abort(404)
    user.add_subtask(
                    title=data["title"], 
                    description=data["description"], 
                    deadline=data["deadline"], 
                    steps=data["steps"],
                    subordinate=subordinate.email
                    )
    return jsonify({})
