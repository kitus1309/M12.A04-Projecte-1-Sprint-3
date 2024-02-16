from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'), override=True)

class Config:
    """Base config."""
    SECRET_KEY = environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')
    if (SQLALCHEMY_DATABASE_URI is None or SQLALCHEMY_DATABASE_URI == ""):
        SQLALCHEMY_DATABASE_URI = "sqlite:///" + path.join(basedir, environ.get('SQLITE_FILE_RELATIVE_PATH'))
    
    MAIL_SENDER_NAME = environ.get('MAIL_SENDER_NAME')
    MAIL_SENDER_ADDR = environ.get('MAIL_SENDER_ADDR')
    MAIL_SENDER_PASSWORD = environ.get('MAIL_SENDER_PASSWORD')
    MAIL_SMTP_SERVER = environ.get('MAIL_SMTP_SERVER')
    MAIL_SMTP_PORT = int(environ.get('MAIL_SMTP_PORT'))

    CONTACT_ADDR = environ.get('CONTACT_ADDR')

    EXTERNAL_URL = environ.get('EXTERNAL_URL')