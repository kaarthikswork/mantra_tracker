@main.route('/test_db')
def test_db():
    try:
        response = supabase.table('users').select('*').limit(1).execute()
        return f"Supabase linked! Sample data: {response.data}"
    except Exception as e:
        return f"Supabase not linked: {e}"
