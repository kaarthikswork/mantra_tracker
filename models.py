from supabase import create_client
import os

# Supabase setup
SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_ANON_KEY')
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

class Mantra:
    def __init__(self, name, syllables, id=None):
        self.id = id
        self.name = name
        self.syllables = syllables
        self.purascharana_count = syllables * 100000
        self.entries = []  # Loaded separately

    def save(self):
        response = supabase.table('mantras').insert({
            'name': self.name,
            'syllables': self.syllables,
            'purascharana_count': self.purascharana_count,
            'current_status': 0
        }).execute()
        self.id = response.data[0]['id']

    @staticmethod
    def get_all():
        response = supabase.table('mantras').select('*').execute()
        mantras = []
        for data in response.data:
            mantra = Mantra(data['name'], data['syllables'], data['id'])
            mantra.entries = mantra.get_entries()
            mantras.append(mantra)
        return mantras

    @staticmethod
    def get_by_id(mantra_id):
        response = supabase.table('mantras').select('*').eq('id', mantra_id).execute()
        if response.data:
            data = response.data[0]
            mantra = Mantra(data['name'], data['syllables'], data['id'])
            mantra.entries = mantra.get_entries()
            return mantra
        return None

    def get_entries(self):
        response = supabase.table('entries').select('*').eq('mantra_id', self.id).execute()
        return response.data

    def add_entry(self, date, count):
        supabase.table('entries').insert({
            'mantra_id': self.id,
            'date': date,
            'count': count
        }).execute()

def get_current_status():
    response = supabase.table('entries').select('count').execute()
    total = sum(entry['count'] for entry in response.data)
    return total
