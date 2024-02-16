import os
from flask import Flask


ENV_LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")


def create_app():
    app = Flask(__name__)
    app.logger.setLevel(ENV_LOG_LEVEL)
    # Import and register blueprints
    # Import the module dynamically
    from api import main_bp

    app.register_blueprint(main_bp)
    return app


if __name__ == "__main__":
    create_app().run()
