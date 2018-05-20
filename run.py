from app import app
from db import Db

@app.before_first_request
def create_tables():
    Db.create_db()
