from flask import make_response, redirect, url_for
from models import storage
from flask_app.pages import page_views

@page_views.route("/logout")
def logout():
    storage.save()
    response = make_response(redirect(url_for("page_views.login")))
    response.delete_cookie("userID")
    return response