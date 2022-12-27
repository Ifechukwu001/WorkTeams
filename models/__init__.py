from .user import User
from .engine.filestorage import FileStorage

storage = FileStorage()
storage.load()

admin = False
for obj in storage.all():
    if obj["__class__"] == "User" and obj.name == "admin":
        admin = True
if not admin:
    admin = User()
    admin.is_admin = True
    admin.update(name="admin", password="admin", email="admin@wt.com")
    storage.save()
