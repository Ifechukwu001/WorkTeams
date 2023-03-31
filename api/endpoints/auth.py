from flask import abort, jsonify, request
from api.endpoints import api_views
from models import storage
from models.user import User


@api_views.route("/user", methods=["POST"], strict_slashes=False)
def login_user():
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
