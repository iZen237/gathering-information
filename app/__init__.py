import os
from flask import Flask

def create_app():
    app = Flask(__name__)

    # Config
    app.config['SECRET_KEY'] = 'super-secret-key'
    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), '..', 'uploads')
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Register blueprints
    from .routes import main
    app.register_blueprint(main)

    return app
