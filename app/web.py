from app import create_app
from app.pages import page_views

app = create_app()
app.register_blueprint(page_views)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", threaded=True)

# @app.route("/new-task", methods=["POST", "GET"])
# def new_task():
#     if request.method == "POST":
#         title = request.form.get("title")
#         description = request.form.get("description")
#         date = request.form.get("dline_date").split("-")
#         date.reverse()
#         time = request.form.get("dline_time").split(":")
#         task_info = {"title": title,
#                     "description": description,
#                     "deadline": date + time,
#                     }
#         user_id = request.cookies.get("userID")
#         if user_id:
#             user = models.storage.get("User", user_id)
#             if user:
#                 task_id = user.create_task(**task_info)
#                 response = make_response(redirect(url_for("home")))
#                 response.set_cookie("taskID", task_id)
#                 return response
#     return render_template("new_task.html")

# @app.route("/set-task/<id>")
# def set_taskid(id):
#     response = make_response(redirect(url_for("home")))
#     response.set_cookie("taskID", id)
#     return response

# @app.route("/new-step", methods=["POST", "GET"])
# def new_step():
#     if request.method == "POST":
#         step_info = request.form.get("info")
#         task_id = request.cookies.get("taskID")
#         user_id = request.cookies.get("userID")
#         if task_id:
#             task = models.storage.get("Task", task_id)
#             if task:
#                 task.create_step(info=step_info, user_id=user_id)
#                 return redirect(url_for("home"))
#     return render_template("new_step.html")

# @app.route("/done-step/<id>", methods=["POST", "GET"])
# def done_step(id):
#     step = models.storage.get("Step", id)
#     step.done()
#     models.storage.save()
#     return redirect(url_for("home"))

# def get_view(user_id, task_id):
#     tasks = []
#     undone_steps = []
#     done_steps = []
#     if user_id:
#         user = models.storage.get("User", user_id)
#         if user:
#             for task in user.tasks:
#                 if task.status == "in progress":
#                     tasks.append(task.to_dict())
#             curr_task  = None
#             tsk_id = ""         
#             if task_id:
#                 curr_task = models.storage.get("Task", task_id)
#             elif tasks:
#                 curr_task = models.storage.get("Task", tasks[0]["id"])
#             if curr_task:
#                 tsk_id = curr_task.id
#                 for step in curr_task.steps:
#                     if step.status == "in progress":
#                         undone_steps.append(step.to_dict())
#                     elif step.status == "done":
#                         done_steps.append(step.to_dict())

#         return tasks, undone_steps, done_steps, tsk_id