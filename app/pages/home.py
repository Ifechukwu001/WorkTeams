from flask import request, make_response, render_template
from models import storage
from models.user import User
from app.pages import page_views

@page_views.route("/")
def home():
    user_id = request.cookies.get("userID")
    task_id = request.cookies.get("taskID")
    user = storage.get(User, user_id)
    if user:
        user_info = user.to_dict()
        response = make_response(render_template("app.html"))
        #response.set_cookie("taskID", task_id)
        return response
    else:
        return "Unauthorized access"