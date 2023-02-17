//Get the User logged in
function getUser() {
    return document.cookie.split("=")[1]
}

// Updates the dashboard with user info
function updateInfo(id) {
    $.get(`http://0.0.0.0:5001/api/user/${id}`, function (response) {
        username = response["name"];
        email = `(${response["email"]})`;
        $("ul #username").text(username);
        $("ul #usermail").text(email);
    })
}

// Loads all the undone tasks
function showTasks (userid, taskid=null) {
    $.get(`http://0.0.0.0:5001/api/${userid}/tasks`, function (response) {
        let sectionContent = ""
        let taskId = taskid;
        response.forEach(task => {
            let title = `<h4>${task["title"]}</h4>`;
            let desc = `<p>${task["description"]}</p>`;
            if (taskId === null) {
                taskId = task["id"];
            }

            let taskContent = `<div class="card task" task-id=${task["id"]}>${title}<hr>${desc}</div>`;
            sectionContent += taskContent;
        });
        $("section#tasks").html(sectionContent);
        loadUndone(userid, taskId)
        loadDone(userid, taskId)
    })
    
}

//Loads all the undone steps
function loadUndone (userid, taskid) {
    $.get(`http://0.0.0.0:5001/api/${userid}/task/${taskid}/undone`, function (response) {
        let sectionContent = "";
        let img = `<img src="/static/images/tick.png">`;
        response.forEach(step => {
            stepContent = `<p class="card step undone" task-id=${taskid} step-id=${step["id"]}> ${step["info"]} ${img} </p>`;
            sectionContent += stepContent;
        });
        $("section#undones").html(sectionContent)
        $("#new_step").attr("task-id", taskid)
    })
}

//Loads all done steps
function loadDone (userid, taskid) {
    $.get(`http://0.0.0.0:5001/api/${userid}/task/${taskid}/done`, function (response) {
        let sectionContent = "";
        let img = `<img src="/static/images/tick2.png">`;
        response.forEach(step => {
            stepContent = `<p class="card step done" task-id=${taskid} step-id=${step["id"]}> ${step["info"]} ${img} </p>`;
            sectionContent += stepContent;
        });
        $("section#dones").html(sectionContent)
    })
}

$(window).on('load', function () {
    const userID = getUser();

    updateInfo(userID);
    showTasks(userID);

    //Update page based on the task clicked
    $("#tasks").on("click", ".task", function () {
        let taskID = $(this).attr("task-id");
        loadUndone(userID, taskID);
        loadDone(userID, taskID)
    })

    //Update a task as done
    $("#undones").on("click", "img", function () {
        let taskId = $(this).parent().attr("task-id")
        let stepId = $(this).parent().attr("step-id")
        $.ajax({
            type: "PUT",
            url: `http://0.0.0.0:5001/api/${userID}/task/${taskId}/done/${stepId}`
        });
        showTasks(userID, taskId);
    })

    //Pop up a new task window
    $("p#new_task").on("click", function () {
        $("#newTask").css("display", "block");
    })
    //Pop up a new step window
    $("p#new_step").on("click", function () {
        $("#newStep").css("display", "block");
    })
    //Remove the pop up
    $(".exit").on("click", function () {
        $("#newTask").css("display", "none");
        $("#newStep").css("display", "none");
    })

    //Submit handler for new task
    $("#createTask").on("click", function () {
        let title = $("#title").val();
        let desc = $("#desc").val();
        let dl = $("#date").val().split("-");
        let tm = $("#time").val();
        dl.reverse();

        $("p#titleError").text("");
        $("p#deadlineError").text("");
        if (title === "") {
            $("p#titleError").text("No Title");
        } else if (dl.includes("")) {
            $("p#deadlineError").text("Invalid Date");
        } else {
            tm = tm.split(":");
            if (tm.includes("")) {
                tm = ["06", "00"];
            }
            $.post({
                url:`http://0.0.0.0:5001/api/${userID}/tasks`,
                contentType: "application/json",
                data: `{"title": "${title}", "description": "${desc}", "deadline": ["${dl[0]}","${dl[1]}","${dl[2]}","${tm[0]}","${tm[1]}"]}`,
                success: function (response) {
                    $("#newTask").css("display", "none");
                    if (response === "{}") {
                        alert("New task created!")
                    }
                }
            })
            showTasks(userID)
        }
        return false;
    });

    //Submit handler for new step
    $("#createStep").on("click", function () {
        let info = $("#info").val()
        let taskId = $("#new_step").attr("task-id");
        if (info === "") {
            $("p#infoError").text("No Info");
        } else {
            $.post({
                url: `http://0.0.0.0:5001/api/${userID}/task/${taskId}`,
                contentType: "application/json",
                data: `{"info": "${info}"}`,
                success: function (response) {
                    $("#newStep").css("display", "none");
                    if (response === "{}") {
                        alert("New task created!")
                    }
                }
            })
            showTasks(userID, taskId);
        }
        return false;
    })
})