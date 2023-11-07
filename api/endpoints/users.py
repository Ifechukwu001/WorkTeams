from flask import abort, jsonify, request
from api.endpoints import api_views
from models import storage
from models.user import User
from flask_apispec import use_kwargs, marshal_with, doc
from api import schemas


@api_views.route("/user/<user_id>", strict_slashes=False)
@marshal_with(schemas.UserResourceSchema, code=200)
@doc(tags=["user"], description="Returns a user assigned to an id")
def user(user_id):
    """Returns a user assigned to an id"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    user_data = user.to_dict()
    user_data.pop("password")
    user_data.pop("__class__")
    return jsonify(user_data)


@api_views.route("/user/<user_id>", methods=["POST"], strict_slashes=False)
@use_kwargs(schemas.UserCreateSchema)
@marshal_with(None, code=201)
@doc(tags=["subordinate"], description="Creates a new subordinate of a user")
def create_user(user_id, **kwargs):
    """Creates a new subordinate of a user"""
    if request.content_type != "application/json":
        abort(400, description="Not a JSON")
    data = request.get_json()
    if "name" not in data:
        abort(400, description="Missing name")
    if "email" not in data:
        abort(400, description="Missing email")
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    user.create_subordinate(name=data["name"], email=data["email"])
    return jsonify({})


@api_views.route("/<user_id>/subordinates", strict_slashes=False)
@marshal_with(schemas.UserResourceSchema(many=True))
@doc(tags=["subordinate"], description="Returns all subordinates of a user")
def subordinates(user_id):
    """Returns all subordinates of a user"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    subs_json = []
    for sub in user.subordinates:
        subs_json.append(sub.to_dict())
    [data.pop("password") for data in subs_json]  # Modifies the original list
    [data.pop("__class__") for data in subs_json]  # Modifies the original list
    return jsonify(subs_json)


@api_views.route("/<user_id>/subordinates/<subordinate_id>",
                 strict_slashes=False)
@marshal_with(schemas.UserResourceSchema(many=True))
@doc(tags=["subordinate"],
     description="Returns all subordinates of a subordinate")
def sub_subordinates(user_id, subordinate_id):
    """Returns all subordinates of a subordinate"""
    user = storage.get(User, user_id)
    subordinate = storage.get(User, subordinate_id)
    if not user or not subordinate:
        abort(404)
    if subordinate not in user.subordinates:
        abort(404)
    subs_json = []
    for sub in subordinate.subordinates:
        subs_json.append(sub.to_dict())
    [data.pop("password") for data in subs_json]  # Modifies the original list
    [data.pop("__class__") for data in subs_json]  # Modifies the original list
    return jsonify(subs_json)
