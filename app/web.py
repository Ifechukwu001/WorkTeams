from flask import render_template, request, url_for
from flask import redirect, make_response
from app import create_app
import models

app = create_app()

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        usermail = request.form.get("usermail")
        sup_mail = request.form.get("superior")
        sup_pass = request.form.get("superiorpass")
        for user in models.storage.all("User"):
            if user.email == sup_mail and user.password == sup_pass:
                if user.is_admin:
                    user.create_subordinate(name=username, email=usermail)
                    return redirect(url_for("login"))
                else:
                    return render_template("register.html", error="Superior cannot have subordinates")
        return render_template("register.html", error="Invalid Superior name or email")
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["usermail"]
        password = request.form["password"]
        for user in models.storage.all("User"):
            if user.email == email and user.password == password:
                user_id = user.id
                print(user_id)
                response = make_response(redirect(url_for("home")))
                response.set_cookie("userID", user_id)
                return response
        return render_template("login.html", error="Invalid Email or password.")
    return render_template("login.html")

@app.route("/logout")
def logout():
    models.storage.save()
    response = make_response(redirect(url_for("login")))
    response.set_cookie("userID", "")
    response.set_cookie("taskID", "")
    return response

@app.route("/")
def home():
    user_id = request.cookies.get("userID")
    task_id = request.cookies.get("taskID")
    user = models.storage.get("User", user_id)
    if user:
        user_info = user.to_dict()
        tasks, undone_steps, done_steps, task_id = get_view(user_id, task_id)
        response = make_response(render_template("app.html",
                                                tasks=tasks,
                                                undone_steps=undone_steps,
                                                done_steps=done_steps,
                                                user=user_info,
                                                ))
        response.set_cookie("taskID", task_id)
        return response
    else:
        return "Unauthorized access"

@app.route("/new-task", methods=["POST", "GET"])
def new_task():
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        date = request.form.get("dline_date").split("-")
        date.reverse()
        time = request.form.get("dline_time").split(":")
        task_info = {"title": title,
                    "description": description,
                    "deadline": date + time,
                    }
        user_id = request.cookies.get("userID")
        if user_id:
            user = models.storage.get("User", user_id)
            if user:
                task_id = user.create_task(**task_info)
                response = make_response(redirect(url_for("home")))
                response.set_cookie("taskID", task_id)
                return response
    return render_template("new_task.html")

@app.route("/set-task/<id>")
def set_taskid(id):
    response = make_response(redirect(url_for("home")))
    response.set_cookie("taskID", id)
    return response

@app.route("/new-step", methods=["POST", "GET"])
def new_step():
    if request.method == "POST":
        step_info = request.form.get("info")
        task_id = request.cookies.get("taskID")
        user_id = request.cookies.get("userID")
        if task_id:
            task = models.storage.get("Task", task_id)
            if task:
                task.create_step(info=step_info, user_id=user_id)
                return redirect(url_for("home"))
    return render_template("new_step.html")

@app.route("/done-step/<id>", methods=["POST", "GET"])
def done_step(id):
    step = models.storage.get("Step", id)
    step.done()
    models.storage.save()
    return redirect(url_for("home"))

def get_view(user_id, task_id):
    tasks = []
    undone_steps = []
    done_steps = []
    if user_id:
        user = models.storage.get("User", user_id)
        if user:
            for task in user.tasks:
                if task.status == "in progress":
                    tasks.append(task.to_dict())
            curr_task  = None
            tsk_id = ""         
            if task_id:
                curr_task = models.storage.get("Task", task_id)
            elif tasks:
                curr_task = models.storage.get("Task", tasks[0]["id"])
            if curr_task:
                tsk_id = curr_task.id
                for step in curr_task.steps:
                    if step.status == "in progress":
                        undone_steps.append(step.to_dict())
                    elif step.status == "done":
                        done_steps.append(step.to_dict())

        return tasks, undone_steps, done_steps, tsk_id