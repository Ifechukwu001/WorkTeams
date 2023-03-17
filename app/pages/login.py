from flask import request, make_response, redirect, url_for, render_template
from models import storage
from models.user import User
from app.pages import page_views

@page_views.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["usermail"]
        password = request.form["password"]
        for user in storage.all(User):
            if user.email == email and user.password == password:
                user_id = user.id
                response = make_response(redirect(url_for("page_views.home")))
                response.set_cookie("userID", user_id)
                return response
        return render_template("login.html", error="Invalid Email or password.")
    return render_template("login.html")