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
        self.entries = []

    def save(self):
        try:
            response = supabase.table('mantras').insert({
                'name': self.name,
                'syllables': self.syllables,
                'purascharana_count': self.purascharana_count,
                'current_status': 0
            }).execute()
            self.id = response.data[0]['id']
        except Exception as e:
            print(f"Error saving mantra: {e}")
            raise

    def update(self, name, syllables):
        try:
            self.name = name
            self.syllables = syllables
            self.purascharana_count = syllables * 100000
            supabase.table('mantras').update({
                'name': self.name,
                'syllables': self.syllables,
                'purascharana_count': self.purascharana_count
            }).eq('id', self.id).execute()
        except Exception as e:
            print(f"Error updating mantra: {e}")
            raise

    @staticmethod
    def delete(mantra_id):
        try:
            supabase.table('entries').delete().eq('mantra_id', mantra_id).execute()  # Delete entries first
            supabase.table('mantras').delete().eq('id', mantra_id).execute()
        except Exception as e:
            print(f"Error deleting mantra: {e}")

    @staticmethod
    def delete_entry(entry_id):
        try:
            supabase.table('entries').delete().eq('id', entry_id).execute()
        except Exception as e:
            print(f"Error deleting entry: {e}")

    @staticmethod
    def get_all():
        try:
            response = supabase.table('mantras').select('*').execute()
            mantras = []
            for data in response.data:
                mantra = Mantra(data['name'], data['syllables'], data['id'])
                mantra.entries = mantra.get_entries()
                mantras.append(mantra)
            return mantras
        except Exception as e:
            print(f"Error getting mantras: {e}")
            return []

    @staticmethod
    def get_by_id(mantra_id):
        try:
            response = supabase.table('mantras').select('*').eq('id', mantra_id).execute()
            if response.data:
                data = response.data[0]
                mantra = Mantra(data['name'], data['syllables'], data['id'])
                mantra.entries = mantra.get_entries()
                return mantra
            return None
        except Exception as e:
            print(f"Error getting mantra by ID: {e}")
            return None

    def get_entries(self):
        try:
            response = supabase.table('entries').select('*').eq('mantra_id', self.id).execute()
            return response.data
        except Exception as e:
            print(f"Error getting entries: {e}")
            return []

    def add_entry(self, date, count):
        try:
            supabase.table('entries').insert({
                'mantra_id': self.id,
                'date': date,
                'count': count
            }).execute()
        except Exception as e:
            print(f"Error adding entry: {e}")
            raise

def get_current_status():
    try:
        response = supabase.table('entries').select('count').execute()
        total = sum(entry['count'] for entry in response.data)
        return total
    except Exception as e:
        print(f"Error getting current status: {e}")
        return 0
