from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.capture import CaptureModel
from resources.detector import Detector

class Capture(Resource):
    TABLE_NAME = 'image_captures'

    parser = reqparse.RequestParser()
    
    # parse the json arguments that are going to arrive
    # url: /location
    # json: {
    #   "locationid": int,
    #   "capture_date": date,
    #   "image": blob
    # }
    

    parser.add_argument('image_url',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )

    parser.add_argument('valid_capture',
        type=int,
        required=True,
        help="This field cannot be left blank!"
    )

    @jwt_required()
    def get(self, device):
        
        device = CaptureModel.find_last_update(device)
        
        if device:
            return device.json()
            
        return {'message': 'Device not found'}, 404

    @jwt_required()
    def post(self, device):
        
        data = self.parser.parse_args()
        image = data['image_url'].replace('www.dropbox.com','dl.dropboxusercontent.com')
        # may need to parse again here to convert image to proper sqlite format
        
        detector = Detector(url=image)
        capture = CaptureModel(device, image_url=image, valid_capture=0, prediction_url=detector.url())
        

        try:
            capture.save_to_db()
            
        except:
           return {"message": "An error occurred inserting the device."}

        #return capture.json()
        return detector.detection()

class CaptureList(Resource):

    def get(self):
        return [capture.json() for capture in CaptureModel.query.all()]