from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

# MongoDB connection (replace with your Atlas URI)
client = MongoClient(os.getenv('MONGO_URI', 'mongodb+srv://your-username:your-password@cluster.mongodb.net/mantra_tracker'))
db = client['mantra_tracker']

# User model
class User:
    def __init__(self, username, password):
        self.username = username
        self.password_hash = generate_password_hash(password)

    @staticmethod
    def find_by_username(username):
        return db.users.find_one({'username': username})

    def save(self):
        db.users.insert_one({'username': self.username, 'password_hash': self.password_hash})

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Mantra model
class Mantra:
    def __init__(self, user_id, name, syllables):
        self.user_id = user_id
        self.name = name
        self.syllables = syllables
        self.purascharana_count = syllables * 100000
        self.current_status = 0  # Will be updated with sum of entries

    def save(self):
        db.mantras.insert_one({
            'user_id': self.user_id,
            'name': self.name,
            'syllables': self.syllables,
            'purascharana_count': self.purascharana_count,
            'current_status': self.current_status
        })

    @staticmethod
    def find_by_user(user_id):
        return list(db.mantras.find({'user_id': user_id}))

    @staticmethod
    def find_by_id(mantra_id):
        return db.mantras.find_one({'_id': mantra_id})

    def add_entry(self, date, count):
        db.entries.insert_one({
            'mantra_id': str(self._id),
            'date': date,
            'count': count
        })
        # Update current status
        total = sum(entry['count'] for entry in db.entries.find({'mantra_id': str(self._id)}))
        db.mantras.update_one({'_id': self._id}, {'$set': {'current_status': total}})
