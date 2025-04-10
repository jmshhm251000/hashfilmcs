from flask import Flask, render_template, request, redirect, session
from dotenv import load_dotenv
import os

from .data_processing import create_index, get_document_text
from .chatbot import Chatbot
from .mongodb import mongo


def create_app(test_config=None):
    # Load .env
    load_dotenv()
    ACCESS_KEY = os.getenv("ACCESS_KEY")

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.urandom(24),  # Replace 'dev' with a real secret key
        MONGO_URI='mongodb://localhost:27017/mydatabase',
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SECURE=True,
        SESSION_COOKIE_SAMESITE='Lax',
        PERMANENT_SESSION_LIFETIME=900  # 15 min timeout
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    chatbot = None

    # ✅ Access-gate route
    @app.route('/', methods=["GET", "POST"])
    def gate():
        nonlocal chatbot
        if session.get("authenticated"):
            response = None
            error = None

            if request.method == "POST":
                user_message = request.form.get("message", "").strip()

                if not user_message:
                    error = "Please enter a message."
                elif len(user_message) > 100:
                    error = "Text must be less than 100 characters."
                else:
                    if chatbot is None:
                        index = create_index(get_document_text())
                        chatbot = Chatbot(index, "deepseek-r1:8b")
                    response = chatbot._query(user_message)

            return render_template("index.html", response=response, error=error)

        # Not authenticated? Check login
        message = None
        if request.method == "POST":
            user_key = request.form.get("key")
            if user_key == ACCESS_KEY:
                session["authenticated"] = True
                session.permanent = True
                return redirect("/")
            else:
                message = "Incorrect access key. Please try again."

        return render_template("login.html", message=message)

    return app