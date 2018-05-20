from app import app
from create_tables import create_db

@app.before_first_request
def create_tables():
    create_db()
