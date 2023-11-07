from flask import abort, jsonify, request
from api.endpoints import api_views
from models import storage
from models.user import User
from flask_apispec import use_kwargs, marshal_with, doc
from api import schemas


@api_views.route("/user", methods=["POST"], strict_slashes=False)
@use_kwargs(schemas.UserLoginSchema)
@marshal_with(schemas.UserIDSchema, code=200)
@doc(tags=["user"], description="Logs in a user")
def login_user(**kwargs):
    """Logs in a user"""
    if request.content_type != "application/json":
        abort(400, description="Not a JSON")
    data = request.get_json()
    if "email" not in data:
        abort(400, description="Missing email")
    if "password" not in data:
        abort(400, description="Missing password")
    users = storage.all(User)
    for user in users:
        if user.email == data["email"] and user.password == data["password"]:
            return jsonify({"user": user.id})
    return jsonify({"error": "invalid email or password"})
