from flask import Flask
from flask_bootstrap import Bootstrap
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from .forms import images

def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')
    Bootstrap(app)

    configure_uploads(app, images)
    patch_request_class(app)

    with app.app_context():
        # Imports
        from . import routes
        app.register_blueprint(routes.main_bp)

        # # Create tables for our models
        # db.create_all()

        return app