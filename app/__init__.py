
from flask import Flask
from .extensions import db, migrate, login_manager, csrf
from .config import Config
from .models import seed_defaults

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)
    login_manager.login_view = "auth.login"

    @login_manager.user_loader
    def load_user(user_id):
        from .models import User
        try:
            return User.query.get(int(user_id))
        except Exception:
            return None

    from .routes.auth import auth_bp
    from .routes.assets import assets_bp
    from .routes.masters import masters_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(assets_bp)
    app.register_blueprint(masters_bp)

    with app.app_context():
        db.create_all()
        seed_defaults()

    return app
