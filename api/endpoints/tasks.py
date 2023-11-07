from flask import abort, jsonify, request
from api.endpoints import api_views
from models import storage
from models.user import User
from models.task import Task
from flask_apispec import use_kwargs, marshal_with, doc
from api import schemas


@api_views.route("/<user_id>/tasks", strict_slashes=False)
@marshal_with(schemas.TaskResourceSchema(many=True))
@doc(tags=["task"], description="Returns all undone tasks of a user")
def undone_tasks(user_id):
    """Returns all undone tasks of a user"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    task_json = []
    for task in user.tasks:
        if task.status == "in progress":
            task_json.append(task.to_dict())
    [task.pop("__class__") for task in task_json]
    return jsonify(task_json)


@api_views.route("/<user_id>/tasks", methods=["POST"], strict_slashes=False)
@use_kwargs(schemas.TaskCreateSchema)
@marshal_with(None, 201)
@doc(tags=["task"], description="Creates a new task for a user")
def create_task(user_id, **kwargs):
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
    return jsonify({}), 201


@api_views.route("/<user_id>/tasks/<subordinate_id>", methods=["POST"],
                 strict_slashes=False)
@use_kwargs(schemas.TaskCreateSchema)
@marshal_with(None, 201)
@doc(tags=["task"], description="Creates a new task for a subordinate")
def create_subtask(user_id, subordinate_id, **kwargs):
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
    return jsonify({}), 201
