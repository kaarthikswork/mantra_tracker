from flask import Flask
from flask_login import LoginManager, UserMixin
from auth import auth
from routes import main
from models import User
import os  # Add this import if not already present

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'fallback-key')  # Use env var for SECRET_KEY too

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(username):
    user = User.find_by_username(username)
    return user if user else None

app.register_blueprint(auth)
app.register_blueprint(main)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Use Render's PORT env var, default to 5000 locally
    app.run(host='0.0.0.0', port=port, debug=False)  # Bind to 0.0.0.0, disable debug for production
