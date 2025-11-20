from flask import Flask
from flask_login import LoginManager, UserMixin
from auth import auth
from routes import main
from models import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # Change to a random string

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
    app.run(debug=True)
