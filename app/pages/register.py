from flask import request, redirect, url_for, render_template
from models import storage
from models.user import User
from app.pages import page_views

@page_views.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        usermail = request.form.get("usermail")
        sup_mail = request.form.get("superior")
        sup_pass = request.form.get("superiorpass")
        for user in storage.all(User):
            if user.email == sup_mail and user.password == sup_pass:
                if user.is_admin:
                    user.create_subordinate(name=username, email=usermail)
                    return redirect(url_for("page_views.login"))
                else:
                    return render_template("register.html", error="Superior cannot have subordinates")
        return render_template("register.html", error="Invalid Superior name or email")
    return render_template("register.html")