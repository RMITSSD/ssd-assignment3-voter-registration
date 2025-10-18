import os
from flask import Flask
from dotenv import load_dotenv
from .extensions import db, migrate

def create_app():
    load_dotenv()  # loads .env into os.environ (local & docker with env_file)
    app = Flask(__name__, template_folder="templates", static_folder="static")

    # Core config
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-change-me")
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL is required. Set it in .env")
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["TEMPLATES_AUTO_RELOAD"] = True

    # Init extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    from .routes import bp as main_bp
    app.register_blueprint(main_bp)

    return app
