from os import environ, path, getenv
basedir = path.abspath(path.dirname(__file__))


class Config:
    """Set Flask configuration vars from .env file."""

    # General Config
    SECRET_KEY = environ.get('SECRET_KEY')
    FLASK_APP = environ.get('FLASK_APP')
    FLASK_DEBUG = environ.get('FLASK_DEBUG')
    FLASK_ENV = environ.get('FLASK_ENV')
    UPLOADED_IMAGES_DEST = environ.get('UPLOADED_IMAGES_DEST')
