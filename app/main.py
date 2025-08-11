from flask import Flask, jsonify
from flask_cors import CORS
from .config import settings
from .routes.chat import chat_bp
from .routes.documents import documents_bp
from .routes.classification import classification_bp
from .routes.conflict import conflict_bp

def create_app():
    app = Flask(
        __name__,
        static_folder=None,
        template_folder=None
    )
    app.config['APP_TITLE'] = "IP Filing Co-Pilot (ZA)"
    app.config['APP_DESCRIPTION'] = "Assistive tool for preparing CIPC trademark filing packages. Not a law firm."
    app.config['APP_VERSION'] = "0.1.0"

    # Enable CORS
    CORS(app, supports_credentials=True)

    # Register blueprints (modular routes)
    app.register_blueprint(chat_bp, url_prefix='/api/triage')
    app.register_blueprint(classification_bp, url_prefix='/api/classify')
    app.register_blueprint(conflict_bp, url_prefix='/api')
    app.register_blueprint(documents_bp, url_prefix='/api/documents')

    @app.route("/", methods=["GET"])
    def health():
        return jsonify({"status": "ok", "env": settings.app_env})

    return app