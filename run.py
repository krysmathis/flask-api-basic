from app import app
from db import db
# image manager to clear out the images file

db.init_app(app)

@app.before_first_request
def create_tables() : 
    db.create_all()
