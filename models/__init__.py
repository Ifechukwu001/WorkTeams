import os

storage_t = os.getenv("WT_STORAGE")

if storage_t == "db":
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.filestorage import FileStorage
    storage = FileStorage()

storage.load()
storage.save()

admin = False
home = "{}/WTeams".format(os.getenv("HOME"))

from models.user import User
if len(storage.all()) == 0:
    admin = User()
    admin.is_admin = True
    print("Creating admin user and work directory...")
    admin.update(name="admin", password="admin", email="admin@wt.com", workspace="{}/admin".format(home))
    storage.save()

