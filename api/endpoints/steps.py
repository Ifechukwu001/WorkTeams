from flask import abort, jsonify, request
from api.endpoints import api_views
from models import storage
from models.user import User
from models.task import Task
from models.step import Step
from flask_apispec import use_kwargs, marshal_with, doc
from api import schemas


@api_views.route("/<user_id>/task/<task_id>", methods=["POST"],
                 strict_slashes=False)
@use_kwargs(schemas.StepCreateSchema)
@marshal_with(None, code=201)
@doc(tags=["step"], description="Creates a new step of a task")
def create_step(user_id, task_id, **kwargs):
    """Creates a new step of a task"""
    if request.content_type != "application/json":
        abort(400, description="Not a JSON")
    data = request.get_json()
    if "info" not in data:
        abort(400, description="Missing info")
    user = storage.get(User, user_id)
    task = storage.get(Task, task_id)
    if not user or not task:
        abort(404)
    task.create_step(
                    info=data["info"],
                    user_id=user_id,
                    )
    return jsonify({}), 201


@api_views.route("/<user_id>/task/<task_id>/undone", methods=["GET"],
                 strict_slashes=False)
@marshal_with(schemas.StepResourceSchema(many=True))
@doc(tags=["step"], description="Returns all undone steps of a task")
def steps_undone(user_id, task_id):
    """Returns all undone steps of a task"""
    user = storage.get(User, user_id)
    task = storage.get(Task, task_id)
    if not user or not task:
        abort(404)
    undone_json = []
    for step in task.steps:
        if step.status == "in progress":
            undone_json.append(step.to_dict())
    [step.pop("__class__") for step in undone_json]
    return jsonify(undone_json)


@api_views.route("/<user_id>/task/<task_id>/done", methods=["GET"],
                 strict_slashes=False)
@marshal_with(schemas.StepResourceSchema(many=True))
@doc(tags=["step"], description="Returns all done steps of a task")
def steps_done(user_id, task_id):
    """Returns all done steps of a task"""
    user = storage.get(User, user_id)
    task = storage.get(Task, task_id)
    if not user or not task:
        abort(404)
    done_json = []
    for step in task.steps:
        if step.status == "done":
            done_json.append(step.to_dict())
    [step.pop("__class__") for step in done_json]
    return jsonify(done_json)


@api_views.route("/<user_id>/task/<task_id>/done/<step_id>", methods=["PUT"],
                 strict_slashes=False)
@marshal_with(None, 200)
@doc(tags=["step"], description="Update an undone step status")
def update_step(user_id, task_id, step_id):
    """Update an undone step status"""
    user = storage.get(User, user_id)
    task = storage.get(Task, task_id)
    step = storage.get(Step, step_id)
    if not user or not task or not step:
        abort(404)
    task.step_done(step)
    for step in task.steps:
        if step.status == "in progress":
            storage.save()
            return jsonify({})
    task.done()
    storage.save()
    return jsonify({})
