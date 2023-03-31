from flask_app.web import app as web
from api.app import app as api

if __name__ == "__main__":
    web.run()
    api.run()