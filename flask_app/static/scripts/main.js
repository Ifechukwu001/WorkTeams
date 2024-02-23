//Get the User logged in
function getUser() {
    return document.cookie.split("=")[1]
}

// Updates the dashboard with user info
function updateInfo(id) {
    $.get(`https://workteams-api.onrender.com/api/user/${id}`, function (response) {
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
        $("section#tasks").find(`[task-id="${taskId}"]`).css("background-color", "#DB6715")
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

//Load reports
function loadReport(userid, subid="") {
    let reportViewContent = ""
    $.get(`http://0.0.0.0:5001/api/${userid}/reports/${subid}`, function (response) {
        response.forEach(reports => {
            reports.forEach(report => {
                let title = `<h3>${report["title"]}</h3>`;
                let desc = `<p>${report["summary"]}</p>`;
                let progress = ` <p id="report-task">${report["done_tasks"]}/${report["total_tasks"]} Tasks done</p>`;

                let reportItem = `<article class="reportItem">${title} ${desc} ${progress}</article>`;
                reportViewContent += reportItem;
            })
        })
        $("div.reportView").html(reportViewContent)
    })
}

//Load report form
function createReportForm () {
    let form = `<form id="report-form" class="form">
                <textarea name="summary" id="summary" placeholder="Summmarize your progress (optional)" cols="25" rows="6"></textarea> 
                <input type="submit" value="Create">
                </form>`
    $("div.reportView").html(form)
}

//Load subordinates
function loadSubs(userid) {
    let subordinatesContent = "";
    $.get(`http://0.0.0.0:5001/api/${userid}/subordinates`, (response) => {
        response.forEach(sub => {
            let subordinate = `<li>${sub["email"]}</li>`;
            subordinatesContent += subordinate;
        })
        $("#subordinates").html(subordinatesContent);
    })
}



//Dynamic Functionalities
$(window).on('load', function () {
    const userID = getUser();

    updateInfo(userID);
    loadSubs(userID);
    showTasks(userID);
    loadReport(userID);

    //Update page based on the task clicked
    $("#tasks").on("click", ".task", function () {
        let taskID = $(this).attr("task-id");
        $(".task").css("background-color", "#F57318")
        $(this).css("background-color", "#DB6715")
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
    //Remove the pop ups
    $(".exit").on("click", function () {
        $("#newTask").css("display", "none");
        $("#newStep").css("display", "none");
        $("#reports").css("display", "none");
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
                    alert("New task created!");
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

    //Popup Reports modal
    $("#report").on("click", function () {
        $("#reports").css("display", "block")
    })

    //Show all subordinate reports
    $("#all-reports").on("click", function() {
        $("#create-report").removeClass("selected");
        $(this).addClass("selected")
        loadReport(userID);
    })

    //Load create report form
    $("#create-report").on("click", function() {
        $("#all-reports").removeClass("selected");
        $(this).addClass("selected")
        createReportForm();
    })

    //Submit handler for create report
    $(".reportView").on("submit", "#report-form", function(e) {
        e.preventDefault()

        let summary = $("#summary").val()
        $.post({
            url: `http://0.0.0.0:5001/api/${userID}/reports`,
                contentType: "application/json",
                data: `{"summary": "${summary}"}`,
                success: function (response) {
                    $("#reports").css("display", "none");
                    alert("Report has been sent to your superiors.");
                }
        })
    })

    $("#subordinate").on("click", () => {
        $("#subordinates").toggle();
    })
})