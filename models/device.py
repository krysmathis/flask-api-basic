from db import db
from datetime import datetime

class DeviceModel(db.Model) :
    __tablename__ = "devices"

        # location text, locid int, capture_date DATE, image url)"
    id = db.Column(db.Integer, primary_key=True)
    device = db.Column(db.String(80))
    location = db.Column(db.String(15))
    area = db.Column(db.String(50))
    install_date = db.Column(db.Date)
    updated_date = db.Column(db.Date)

    def __init__(self, device, location, area, install_date) : 
        self.device = device
        self.location = location
        self.area = area
        self.install_date = datetime.strptime(install_date, '%Y-%m-%d')
        self.updated_date = datetime.now()

    def json(self):
    
        return {
            'device': self.device, 
            'location': self.location,
            'area': self.area,
            'install_date':self.install_date.isoformat(),
            'updated_date': self.updated_date.isoformat()
    }

    @classmethod
    def find_by_name(cls, device):
        return cls.query.filter_by(device=device).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()