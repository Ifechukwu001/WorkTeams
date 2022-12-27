"""Module containing the file storage model"""
import json
from models.user import User
from models.task import Task
from models.report import Report
from models.step import Step

classes = {"User": User, "Task": Task, "Report": Report, "Step": Step}


class FileStorage:
    """file storage engine"""
    __file_path = "file.wt.json"
    __objects = {}

    def all(self, cls=None):
        """Returns a list of all objects of a class or all classes"""
        objs = []
        if cls:
            for key, obj in self.__objects.items():
                if key.startswith(cls.__name__):
                    objs.append(obj)
        else:
            for key, obj in self.__objects.items():
                objs.append(obj)
        return objs

    def new(self, obj):
        """Add a new object to the storage"""
        if obj:
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            self.__objects[key] = obj

    def save(self):
        """Saves the current state of the engine to the file"""
        objs = {}
        for key, obj in self.__objects.items():
            objs[key] = obj.to_dict()
        with open(self.__file_path, "w", encoding="utf8") as file:
            obj_str = json.dumps(objs)
            file.write(obj_str)

    def load(self):
        """Loads the objects from the file to the engine"""
        objs = {}
        try:
            with open(self.__file_path, encoding="utf8") as file:
                objs = json.loads(file.read())
            for key, value in objs.items():
                self.__objects[key] = classes[value["__class__"]](**value)
        except:
            pass
