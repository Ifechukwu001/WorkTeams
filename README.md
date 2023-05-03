## WorkTeams - Team Task Management System

This is a software which could use to track your personal or organisation's task processes.

## Index

- [Index](#index)
- [Use Cases](#use-cases)
- [Collaborators](#collaborators)
- [Technologies](#technologies)
- [API Endpoints](#api-endpoints)


### Use Cases

A Student wants to read his Chemistry textbook.
He/She could:
 - First create a list of topics to read.
 - Start the reading.
 - Ask self questions on the topics.
 - Finally, solve some past questions on the course.

An Engineer who wants to solve an engineering task.
He/She could:
 - Describe the engineering problem.
 - Research on previous success of others on the problem.
 - Research on technologies needed to solve the challenge.
 - Work on possible solutions
 - Finish initial MVP, etc

A Director could also define tasks for subordinates, leaving the decision of the steps for the subordinate to create.


### Collaborators

- **Ogidi Ifechukwu** Lead Backend Developer ([Github](https://github.com/Ifechukwu001))
- **Udechukwu Daniel** Frontend Developer ([Github](https://github.com/DanielUdechukwu))


### Technologies

| ***Languages*** | ***Framework*** |
|-----------------|-----------------|
| **Python**      | Flask           |
|                 | Flask-CORS      |
|                 | SQLAlchemy      |
|                 | Gunicorn        |
| **JavaScript**  | JQuery          |
| **CSS**         | TailWind CSS    |
| **HTML**        |                 |
| **MySQL**       |                 |


### API Endpoints

**Hosted on [PythonAnywhere](https://ifechukwu.pythonanywhere.com/)**

| Endpoint                                           | Method | Function                                             |
| :------------------------------------------------- | :----- | :--------------------------------------------------- |
| /api/v2/user                                       | POST   | Authenticates a user                                 |
| /api/v2/user/\<user_id>                            | GET    | Returns a user assigned to the id                    |
| /api/v2/user/\<user_id>                            | POST   | Create a new subordinate of the user                 |
| /api/v2/user/\<user_id>                            | PUT    | Updates the information of a user                    |
| /api/v2/\<user_id>/tasks                           | GET    | Returns all the undone tasks assigned to a user      |
| /api/v2/\<user_id>/tasks                           | POST   | Creates a new task for a user                        |
| /api/v2/\<user_id>/tasks/\<subordinate_id>         | POST   | Creates a new task for a subordinate                 |
| /api/v2/\<user_id>/task/\<task_id>                 | POST   | Creates a new step of a task                         |
| /api/v2/\<user_id>/task/\<task_id>/undone          | GET    | Returns all undone steps of a task                   |
| /api/v2/\<user_id>/task/\<task_id>/done            | GET    | Returns all done steps of a task                     |
| /api/v2/\<user_id>/task/\<task_id>/done/\<step_id> | PUT    | Update an undone step status                         |
| /api/v2/\<user_id>/subordinates                    | GET    | Returns all the subordinates of a user               |
| /api/v2/\<user_id>/subordinates/\<subordinate_id>  | GET    | Returns all the subordinates of a user’s subordinate |
| /api/v2/\<user_id>/reports                         | GET    | Returns all subordinates reports                     |
| /api/v2/\<user_id>/reports                         | POST   | Create a new report                                  |
| /api/v2/\<user_id>/reports/\<subordinate_id>       | GET    | Returns all subordinates reports                     |
| /api/v2/\<user_id>/notifications                   | GET    | Returns all the unread notifications (In Progress)   |
| /api/v2/\<user_id>/notifications                   | POST   | Create a new notification (In Progress)              | 
