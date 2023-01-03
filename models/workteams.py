"""Module containing the command line class"""

import cmd
import getpass
import os
import models
from datetime import datetime
from models.user import User
from models.report import Report
from models.task import Task
from models.step import Step

#if current_user:
#   prompt = "{} ({})$ ".format(current_user.name, current_user.email)
#else:
#   prompt = "WorkTeams (wt@WT)$ "


class WTCMD(cmd.Cmd):
    """Command line for WorkTeams"""
    prompt = "WorkTeams (wt@WT)$ "
    current_user = None
    command = True

    def precmd(self, line):
        """Process command before running it"""
        if line.startswith("EOF"):
            return "EOF"
        elif self.current_user:
            if not self.command and not line.startswith("command"):
                line = "shell {}".format(line)
            return line
        elif line.startswith("login"):
            return line
        else:
            return ""

    def emptyline(self):
        """Executes on an empty input"""
        return "" 

    def do_shell(self, arg):
        """Executes os commands"""
        args = arg.split()
        child = os.fork()
        if child == 0:
            os.chdir(self.current_user.workspace)
            try:
                os.execvpe(args[0], args, os.environ)
            except FileNotFoundError:
                print("Command invalid: Try `command` to toggle the command type")
        else:
            os.wait()


    def do_login(self, arg):
        """Login as a user"""
        password = getpass.unix_getpass()
        for user in models.storage.all(User):
            if user.name == arg and user.password == password:
                self.current_user = user
                if not self.current_user.last_login:
                    self.change_password()

                self.current_user.logged()
                models.storage.save()
                self.user_info(self.current_user)
                self.prompt = "{} ({})$ ".format(self.current_user.name, self.current_user.email)

    def do_logout(self, arg):
        """Logout of WorkTeams"""
        self.current_user.logged()
        models.storage.save()
        self.current_user = None
        self.prompt = "WorkTeams (wt@WT)$ "

    def do_command(self, arg):
        """Make subsequent commands to the app"""
        if self.command:
            self.command = False
        else:
            self.command = True

    def do_task(self, arg):
        """Create a new task"""
        try:
            title = input("Task Title: ")
            desc = input("Task Description: ")
            deadline = input("Task Deadline(day month year /optional( hour minute ): ").split(" ")
        except EOFError:
            print()
            print("Invalid Input")
        else:
            if len(title) < 4:
                print()
                print("Couldn't create task: Title is too short")
                return False
            try:
                deadline = [int(num) for num in deadline]
                if len(deadline) < 3:
                    raise ValueError
                if deadline[0] > 31 or deadline[1] > 12:
                    raise ValueError
                if len(deadline) > 3 and deadline[3] > 23:
                    raise ValueError
                if len(deadline) > 4 and deadline[4] > 59:
                    raise ValueError
            except ValueError:
                print()
                print("Couldn't create task: Invalid date")
                return False
            steps = []
            print("Steps to achieve task:")
            num = 1
            try:
                while True:
                    step = input("{}. ".format(num))
                    if step:
                        steps.append(step)
                    else:
                        break
                    num += 1
            except EOFError:
                print()
                print("Couldn't create task: Invalid step")
            else:
                self.current_user.create_task(title=title, description=desc, deadline=deadline, steps=steps)

    def do_tasks(self, arg):
        """Display all the tasks of a user"""
        if arg:
            for task in self.current_user.tasks:
                if task.title == arg:
                    print("=====================================================")
                    print("Task Title: {} ({})".format(task.title, task.status))
                    print("Task Description: {}".format(task.description))
                    print("Deadline: {}".format(task.deadline))
                    print("Steps:")
                    i = 1
                    for step in task.steps:
                        print("{}. {} ({})".format(i, step.info, step.status))
                        i += 1
        else:
            for task in self.current_user.tasks:
                print("=====================================================")
                print("Task Title: {} ({})".format(task.title, task.status))
                print("Task Description: {}".format(task.description))
                print("Deadline: {}".format(task.deadline))
                print("Steps:")
                i = 1
                for step in task.steps:
                    print("{}. {} ({})".format(i, step.info, step.status))
                    i += 1

    def do_done(self, arg):
        """Sets an 'in progress' step of a task to 'done'"""
        if arg:
            for task in self.current_user.tasks:
                if task.title == arg:
                    for step in task.steps:
                        if step.status == "in progress":
                            task.step_done(step)
                            if step == task.steps[-1]:
                                task.done()
                            return False

    def do_abandon(self, arg):
        """Abandons a task"""
        if arg:
            for task in self.current_user.tasks:
                if task.title == arg:
                    task.abandon()

    def do_report(self, arg):
        """Create a new report"""
        try:
            summary = input("Report Summary: ")
        except EOFError:
            print()
            print("Invalid Input")
        else:
            Report.generate(self.current_user, summary=summary)

    def do_reports(self, arg):
        """Display all the user's reports"""
        date = [int(i) for i in arg.split()]
        date.reverse()
        if len(date) == 3:
            for report in self.current_user.reports:
                if report.time_generated > datetime(*date):
                    print("=====================================================")
                    print("Report Title: {}".format(report.title))
                    print("Summary: {}".format(report.summary))
                    print("Tasks done: {}/{}".format(report.done_tasks, report.total_tasks))
                    print("Tasks:")
                    for task in report.tasks:
                        print("    * {} ({})".format(task.title, task.status))
        else:
            for report in self.current_user.reports:
                print("=====================================================")
                print("Report Title: {}".format(report.title))
                print("Summary: {}".format(report.summary))
                print("Tasks done: {}/{}".format(report.done_tasks, report.total_tasks))
                print("Tasks:")
                for task in report.tasks:
                    print("    * {} ({})".format(task.title, task.status))

    def do_subordinate(self, arg):
        """Creates a new subordinate"""
        if self.current_user.is_admin:
            name = input("Name: ")
            email = input("Email: ")
            if not email:
                print("You did not give subordinate email")
                return False
            superior = input("Superior's Email (Press ENTER if direct subordinate: ")
            superior_id = None
            if superior:
                for subordinate in self.current_user.subordinates:
                    if subordinate.email == superior and subordinate.is_admin:
                            superior_id = subordinate.id
                    else:
                        print("{} ({}) is not authorised to have subordinate".format(subordinate.name, superior))
                        return False
            self.current_user.create_subordinate(name=name, email=email, admin_id=superior_id)
        else:
            print("You do not have authorization")

    def do_subordinates(self, arg):
        """Displays all subordinates of the current user"""
        for subordinate in self.current_user.subordinates:
            print("=> {} ({})".format(subordinate.name, subordinate.email))

    def do_make_admin(self, arg):
        """Make a user an admin"""
        email = input("Subordinate's email: ")
        if self.current_user.is_admin:
            for subordinate in self.current_user.subordinates:
                if subordinate.email == email:
                    self.current_user.create_admin(subordinate)

    def do_EOF(self, arg):
        """EOF method"""
        if self.current_user:
            self.current_user.logged()
            models.storage.save()
            self.current_user = None
        print()
        return True

    def user_info(self, user):
        """Displays the information of a user"""
        print("================================")
        print("================================")
        print("= Username: {}".format(user.name))
        print("= Usermail: {}".format(user.email))
        print("================================")
        print("= Tasks:")
        for task in user.tasks:
            if task.status == "in progress":
                print("=    * {}".format(task.title))
        print("================================")

    def change_password(self):
        """Changes the password of a new user"""
        print("Change your Password")
        while True:
            password = getpass.getpass()
            check = getpass.getpass("Confirm Password: ")
            if password == check:
                self.current_user.update(password=password)
                break
            print("Password mismatch")
