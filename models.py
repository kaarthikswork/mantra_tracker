import firebase_admin
from firebase_admin import credentials, firestore
import os
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin  # Added for Flask-Login

# Initialize Firebase (with error handling)
try:
    cred = credentials.Certificate({
        "type": "service_account",
        "project_id": os.environ.get('FIREBASE_PROJECT_ID'),
        "private_key_id": os.environ.get('FIREBASE_PRIVATE_KEY_ID'),
        "private_key": os.environ.get('FIREBASE_PRIVATE_KEY').replace('\\n', '\n'),
        "client_email": os.environ.get('FIREBASE_CLIENT_EMAIL'),
        "client_id": os.environ.get('FIREBASE_CLIENT_ID'),
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": os.environ.get('FIREBASE_CLIENT_X509_CERT_URL')
    })
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    print("Firebase initialized successfully.")  # Debug log
except Exception as e:
    print(f"Firebase initialization failed: {e}")
    db = None  # Prevent crashes

# User model (now inherits from UserMixin for Flask-Login)
class User(UserMixin):
    def __init__(self, username, password_hash=None):
        self.username = username
        self.password_hash = password_hash
        self.id = username  # Flask-Login uses 'id' for user identification

    @staticmethod
    def find_by_username(username):
        if db is None:
            return None
        try:
            doc = db.collection('users').document(username).get()
            if doc.exists:
                data = doc.to_dict()
                return User(data['username'], data['password_hash'])
            return None
        except Exception as e:
            print(f"Error finding user: {e}")
            return None

    def save(self):
        if db is None:
            raise Exception("Database not initialized")
        try:
            db.collection('users').document(self.username).set({
                'username': self.username,
                'password_hash': self.password_hash
            })
            print(f"User {self.username} saved successfully.")  # Debug log
        except Exception as e:
            print(f"Error saving user: {e}")
            raise

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Mantra model (unchanged, but added error handling)
class Mantra:
    def __init__(self, user_id, name, syllables):
        self.user_id = user_id
        self.name = name
        self.syllables = syllables
        self.purascharana_count = syllables * 100000
        self.current_status = 0

    def save(self):
        if db is None:
            raise Exception("Database not initialized")
        try:
            doc_ref = db.collection('mantras').document()
            self._id = doc_ref.id
            doc_ref.set({
                'id': self._id,
                'user_id': self.user_id,
                'name': self.name,
                'syllables': self.syllables,
                'purascharana_count': self.purascharana_count,
                'current_status': self.current_status
            })
            print(f"Mantra {self.name} saved successfully.")  # Debug log
        except Exception as e:
            print(f"Error saving mantra: {e}")
            raise

    @staticmethod
    def find_by_user(user_id):
        if db is None:
            return []
        try:
            docs = db.collection('mantras').where('user_id', '==', user_id).stream()
            return [doc.to_dict() for doc in docs]
        except Exception as e:
            print(f"Error finding mantras: {e}")
            return []

    @staticmethod
    def find_by_id(mantra_id):
        if db is None:
            return None
        try:
            doc = db.collection('mantras').document(mantra_id).get()
            return doc.to_dict() if doc.exists else None
        except Exception as e:
            print(f"Error finding mantra: {e}")
            return None

    def add_entry(self, date, count):
        if db is None:
            raise Exception("Database not initialized")
        try:
            db.collection('entries').add({
                'mantra_id': str(self._id),
                'date': date,
                'count': count
            })
            # Update current status
            entries = db.collection('entries').where('mantra_id', '==', str(self._id)).stream()
            total = sum(entry.to_dict()['count'] for entry in entries)
            db.collection('mantras').document(self._id).update({'current_status': total})
            print(f"Entry added for mantra {self._id}.")  # Debug log
        except Exception as e:
            print(f"Error adding entry: {e}")
            raise
