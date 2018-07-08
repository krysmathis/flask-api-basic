from db import db
import time, datetime

class CaptureModel(db.Model) :
    __tablename__ = "image_captures"

        # location text, locid int, capture_date DATE, image url)"
    id = db.Column(db.Integer, primary_key=True)
    device = db.Column(db.String(80))
    capture_date = db.Column(db.Date)
    capture_time = db.Column(db.String)
    image_url = db.Column(db.String)
    prediction_url = db.Column(db.String)
    valid_capture = db.Column(db.Integer)


    def __init__(self, device, image_url, valid_capture, prediction_url) : 
        self.device = device
        self.capture_date = datetime.datetime.now()
        self.capture_time = time.strftime("%H:%M:%S")
        self.image_url = image_url
        self.valid_capture = valid_capture
        self.prediction_url = prediction_url

    def json(self):
        
        _time = time.strftime("%H:%M:%S")
        
        return {
            'device': self.device, 
            'capture_date': str(self.capture_date),
            'capture_time': str(self.capture_time),
            'image_url': self.image_url,
            'valid_capture': self.valid_capture,
            'prediction_url': self.prediction_url
        }

    @classmethod
    def find_last_update(cls, device):
        return cls.query.filter_by(device=device).order_by(cls.capture_date.desc(), cls.capture_time.desc()).first()

    def save_to_db(self):
        print(self.json())
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()