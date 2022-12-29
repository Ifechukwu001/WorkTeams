import os
from .user import User
from .engine.filestorage import FileStorage

storage = FileStorage()
storage.load()

admin = False
home = "{}/WTeams".format(os.getenv("HOME"))
if len(storage.all()) == 0:
    admin = User()
    admin.is_admin = True
    print("Creating admin user and work directory...")
    admin.update(name="admin", password="admin", email="admin@wt.com", workspace="{}/admin".format(home))
    storage.save()

__all__ = ["storage", "home"]
