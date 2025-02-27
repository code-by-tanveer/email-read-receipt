from flask import Flask
from app.database import init_db
from app.routes import routes

def create_app():
    app = Flask(__name__)
    app.config.from_object("config")

    init_db(app)
    app.register_blueprint(routes)

    return app
