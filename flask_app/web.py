from flask import render_template
from flask_app import create_app

app = create_app()

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/")
def home():
    return render_template("app.html", 
                    tasks=[{"title": "Test", "description": "Just testing"}], 
                    undone_steps=[{"info": "Trying"}], 
                    done_steps=[{"info": "Done trying"}])
