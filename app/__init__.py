from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
csrf = CSRFProtect()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    csrf.init_app(app)

    from app.routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    return app

from app.models import User

@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
