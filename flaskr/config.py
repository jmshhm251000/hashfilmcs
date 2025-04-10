#config.py
import os
from dotenv import load_dotenv


load_dotenv()  # load once here


def load_app_config(app, test_config=None):
    app.config.from_mapping(
        SECRET_KEY=os.urandom(24),
        MONGO_URI='mongodb://localhost:27017/hashfilmcs',
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SECURE=True,
        SESSION_COOKIE_SAMESITE='Lax',
        PERMANENT_SESSION_LIFETIME=900,
        ACCESS_KEY=os.getenv("ACCESS_KEY"),
        DOCUMENT_ID=os.getenv("DOCUMENT_ID"),
        SCOPES=['https://www.googleapis.com/auth/documents.readonly'],
        VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
    )

    if test_config:
        app.config.from_mapping(test_config)
    else:
        app.config.from_pyfile('config.py', silent=True)
