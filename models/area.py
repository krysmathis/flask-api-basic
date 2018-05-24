from db import db

class AreaModel(db.Model) : 
    __tablename__ = 'areas'
    
    # location text, locid int, capture_date DATE, image url)"
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(80))
    locationid = db.Column(db.Integer)
    capture_date = db.Column(db.Date)
    image = db.Column(db.String)

    def __init__(self, location, locationid, date_captured, image) : 
        self.location = location
        self.locationid = locationid
        self.date_captured = date_captured
        self.image = image
    

    def json(self):
        return {
            'location': self.location, 
            'locationid': self.locationid,
            'date_captured': self.capture_date,
            'image': self.image
            }

    @classmethod
    def find_by_name(cls, location):
        return cls.query.filter_by(location=location).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()