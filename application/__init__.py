"""
Main Flask Application Initialization
"""
# application/__init__.py

from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf import CSRFProtect
from application.database.models import User
from application.database import db
from application.bp.homepage import bp_homepage
from application.bp.authentication import authentication
import config

migrate = Migrate()
csrf = CSRFProtect()
login_manager = LoginManager()

def init_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(config.Config())

    csrf.init_app(app)
    Bootstrap5(app)

    login_manager.login_view = "authentication.login"
    login_manager.init_app(app)

    db.init_app(app)
    migrate.init_app(app, db)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    with app.app_context():
        blueprints = [bp_homepage, authentication]
        for blueprint in blueprints:
            app.register_blueprint(blueprint)
        return app
