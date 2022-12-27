"""Module containing the command line class"""

import cmd
import getpass
import models
from models.user import User
from models.report import Report
from models.task import Task
from models.step import Step

current_user = None
#if current_user:
#   prompt = "{} ({})$ ".format(current_user.name, current_user.email)
#else:
#   prompt = "WorkTeams (wt@WT)$ "


class WTCMD(cmd.Cmd):
    """Command line for WorkTeams"""
    prompt = "WorkTeams (wt@WT)$ "

    def precmd(self, line):
        """Process command before running it"""
        if current_user:
            return line
        elif line.startswith("login"):
            return line
        elif line.startswith("EOF"):
            return "EOF"
        else:
            return ""

    def emptyline(self):
        """Executes on an empty input"""
        return "" 

    def do_login(self, arg):
        """Login as a user"""
        args = arg.split(" ")
        password = getpass.unix_getpass()
        for user in models.storage.all(User):
            if user.name == args[0] and user.password == password:
                current_user = user
                self.prompt = "{} ({})$ ".format(current_user.name, current_user.email)


    def do_EOF(self, arg):
        """EOF method"""
        print()
        return True
