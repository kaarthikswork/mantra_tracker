from flask import Flask
from flask_login import LoginManager
from auth import auth
from routes import main
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'fallback-key')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(username):
    from models import User  # Import here to avoid circular import
    return User.find_by_username(username)

app.register_blueprint(auth)
app.register_blueprint(main)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
