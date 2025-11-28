from flask import Flask
from routes import main

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'

app.register_blueprint(main)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
