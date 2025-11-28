from flask import Flask
from flask_login import LoginManager
from routes import main, auth
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'fallback-key')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.get_by_id(user_id)

app.register_blueprint(auth)
app.register_blueprint(main)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
