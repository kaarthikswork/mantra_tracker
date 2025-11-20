import firebase_admin
from firebase_admin import credentials, firestore
import os
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Initialize Firebase (use env var for key)
cred = credentials.Certificate({
    "type": "service_account",
    "project_id": os.environ.get('FIREBASE_PROJECT_ID'),
    "private_key_id": os.environ.get('FIREBASE_PRIVATE_KEY_ID'),
    "private_key": os.environ.get('FIREBASE_PRIVATE_KEY').replace('\\n', '\n'),  # Handle newlines
    "client_email": os.environ.get('FIREBASE_CLIENT_EMAIL'),
    "client_id": os.environ.get('FIREBASE_CLIENT_ID'),
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": os.environ.get('FIREBASE_CLIENT_X509_CERT_URL')
})
firebase_admin.initialize_app(cred)
db = firestore.client()

# User model
class User:
    def __init__(self, username, password):
        self.username = username
        self.password_hash = generate_password_hash(password)

    @staticmethod
    def find_by_username(username):
        doc = db.collection('users').document(username).get()
        return doc.to_dict() if doc.exists else None

    def save(self):
        db.collection('users').document(self.username).set({
            'username': self.username,
            'password_hash': self.password_hash
        })

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Mantra model
class Mantra:
    def __init__(self, user_id, name, syllables):
        self.user_id = user_id
        self.name = name
        self.syllables = syllables
        self.purascharana_count = syllables * 100000
        self.current_status = 0

    def save(self):
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

    @staticmethod
    def find_by_user(user_id):
        docs = db.collection('mantras').where('user_id', '==', user_id).stream()
        return [doc.to_dict() for doc in docs]

    @staticmethod
    def find_by_id(mantra_id):
        doc = db.collection('mantras').document(mantra_id).get()
        return doc.to_dict() if doc.exists else None

    def add_entry(self, date, count):
        db.collection('entries').add({
            'mantra_id': str(self._id),
            'date': date,
            'count': count
        })
        # Update current status
        entries = db.collection('entries').where('mantra_id', '==', str(self._id)).stream()
        total = sum(entry.to_dict()['count'] for entry in entries)
        db.collection('mantras').document(self._id).update({'current_status': total})
