from flask import abort, jsonify, request
from api.endpoints import api_views
from models import storage
from models.user import User

@api_views.route("/user/<user_id>", strict_slashes=False)
def user(user_id):
    """Returns a user assigned to an id"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    user_data = user.to_dict()
    user_data.pop("password")
    return jsonify(user_data)

@api_views.route("/user/<user_id>", methods=["POST"], strict_slashes=False)
def create_user(user_id):
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
def subordinates(user_id):
    """Returns all subordinates of a user"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    subs_json = []
    for sub in user.subordinates:
        subs_json.append(sub.to_dict())
    subs_data = [data.pop("password") for data in subs_json]
    return jsonify(subs_data)

@api_views.route("/<user_id>/subordinates/<subordinate_id>", strict_slashes=False)
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
    return jsonify(subs_json)