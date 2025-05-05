from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

def create_app():
    app = Flask(__name__)
    
    # Enable CORS with specific configuration
    CORS(app, resources={
        r"/*": {
            "origins": ["http://localhost:3000", "http://recipe-app-frontend-1:3000"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization", "Accept"],
            "supports_credentials": True
        }
    })

    # Set JWT secret key
    app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Replace with env var in production
    jwt = JWTManager(app)

    # Import and register auth blueprint
    from .auth import auth_bp
    app.register_blueprint(auth_bp)

    # ✅ Import and register main blueprint
    from .routes import main
    app.register_blueprint(main)

    return app
