from supabase import create_client, Client
from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import os

# Supabase setup
SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_ANON_KEY')
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# SQLAlchemy setup (for local ORM if needed, but we'll use Supabase directly for simplicity)
Base = declarative_base()

class User(Base, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password_hash = generate_password_hash(password)

    @staticmethod
    def find_by_username(username):
        response = supabase.table('users').select('*').eq('username', username).execute()
        data = response.data
        if data:
            user_data = data[0]
            return User(user_data['username'], '')  # Password hash loaded separately
        return None

    def save(self):
        supabase.table('users').insert({
            'username': self.username,
            'password_hash': self.password_hash
        }).execute()

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Mantra(Base):
    __tablename__ = 'mantras'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    name = Column(String, nullable=False)
    syllables = Column(Integer, nullable=False)
    purascharana_count = Column(Integer, nullable=False)
    current_status = Column(Integer, default=0)

    def __init__(self, user_id, name, syllables):
        self.user_id = user_id
        self.name = name
        self.syllables = syllables
        self.purascharana_count = syllables * 100000
        self.current_status = 0

    def save(self):
        response = supabase.table('mantras').insert({
            'user_id': self.user_id,
            'name': self.name,
            'syllables': self.syllables,
            'purascharana_count': self.purascharana_count,
            'current_status': self.current_status
        }).execute()
        self.id = response.data[0]['id']  # Get inserted ID

    @staticmethod
    def find_by_user(user_id):
        response = supabase.table('mantras').select('*').eq('user_id', user_id).execute()
        return response.data

    @staticmethod
    def find_by_id(mantra_id):
        response = supabase.table('mantras').select('*').eq('id', mantra_id).execute()
        return response.data[0] if response.data else None

    def add_entry(self, date, count):
        supabase.table('entries').insert({
            'mantra_id': self.id,
            'date': date,
            'count': count
        }).execute()
        # Update current status
        response = supabase.table('entries').select('count').eq('mantra_id', self.id).execute()
        total = sum(entry['count'] for entry in response.data)
        supabase.table('mantras').update({'current_status': total}).eq('id', self.id).execute()

# Entries table (no class needed, handled in add_entry)
