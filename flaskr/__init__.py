from flask import Flask, render_template, request, redirect, session
from .data_processing import create_index, get_document_text
from .chatbot import Chatbot
from .mongodb import mongo
from .config import load_app_config


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    # 🔧 Load env + config
    load_app_config(app, test_config)

    # 🔌 Init DB
    mongo.init_app(app)

    # 🤖 Lazy init chatbot
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
                        document_id = app.config['DOCUMENT_ID']
                        scopes = app.config['SCOPES']
                        index = create_index(get_document_text(document_id,scopes))
                        chatbot = Chatbot(index, "deepseek-r1:8b")
                    response = chatbot._query(user_message)

            return render_template("index.html", response=response, error=error)

        # Not authenticated? Check login
        message = None
        if request.method == "POST":
            user_key = request.form.get("key")
            if user_key == app.config["ACCESS_KEY"]:
                session["authenticated"] = True
                session.permanent = True
                return redirect("/")
            else:
                message = "Incorrect access key. Please try again."

        return render_template("login.html", message=message)

    # 📦 Register routes
    from .routes.database import database_bp
    from .routes.webhooks import webhook_bp
    app.register_blueprint(database_bp)
    app.register_blueprint(webhook_bp)

    return app