from supabase import create_client, Client
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import os

# Supabase setup
SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_ANON_KEY')
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# User model
class User(UserMixin):
    def __init__(self, username, password_hash=None):
        self.username = username
        self.password_hash = password_hash
        self.id = username  # Flask-Login uses 'id' for identification

    @staticmethod
    def find_by_username(username):
        try:
            response = supabase.table('users').select('*').eq('username', username).execute()
            data = response.data
            if data:
                user_data = data[0]
                return User(user_data['username'], user_data['password_hash'])
            return None
        except Exception as e:
            print(f"Error finding user: {e}")
            return None

    def save(self):
        try:
            supabase.table('users').insert({
                'username': self.username,
                'password_hash': self.password_hash
            }).execute()
            print(f"User {self.username} saved successfully.")
        except Exception as e:
            print(f"Error saving user: {e}")
            raise

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
        self.id = None  # Will be set after save

    def save(self):
        try:
            response = supabase.table('mantras').insert({
                'user_id': self.user_id,
                'name': self.name,
                'syllables': self.syllables,
                'purascharana_count': self.purascharana_count,
                'current_status': self.current_status
            }).execute()
            self.id = response.data[0]['id']  # Get the inserted ID
            print(f"Mantra {self.name} saved successfully.")
        except Exception as e:
            print(f"Error saving mantra: {e}")
            raise

    @staticmethod
    def find_by_user(user_id):
        try:
            response = supabase.table('mantras').select('*').eq('user_id', user_id).execute()
            return response.data
        except Exception as e:
            print(f"Error finding mantras: {e}")
            return []

    @staticmethod
    def find_by_id(mantra_id):
        try:
            response = supabase.table('mantras').select('*').eq('id', mantra_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error finding mantra: {e}")
            return None

    def add_entry(self, date, count):
        try:
            supabase.table('entries').insert({
                'mantra_id': self.id,
                'date': date,
                'count': count
            }).execute()
            # Update current status
            response = supabase.table('entries').select('count').eq('mantra_id', self.id).execute()
            total = sum(entry['count'] for entry in response.data)
            supabase.table('mantras').update({'current_status': total}).eq('id', self.id).execute()
            print(f"Entry added for mantra {self.id}.")
        except Exception as e:
            print(f"Error adding entry: {e}")
            raise
