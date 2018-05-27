from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.device import DeviceModel
from datetime import datetime

class Device(Resource):
    TABLE_NAME = 'devices'

    """
    return {
        'device': self.device, 
        'location': self.location,
        'area': self.area,
        'install_date': self.install_date,
        'updated_date': self.updated_date
    }
    """
    parser = reqparse.RequestParser()
    

    parser.add_argument('location',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )

    parser.add_argument('area',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )

    parser.add_argument('install_date',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )

    @jwt_required()
    def get(self, device):
        
        device = DeviceModel.find_last_update(device)
        
        if device:
            return device.json()
            
        return {'message': 'Device not found'}, 404

    @jwt_required()
    def post(self, device):

        data = self.parser.parse_args()

        _device = DeviceModel.find_by_name(device)
       
        if _device is None:
            _device = DeviceModel(device, location=data['location'], area=data['area'], install_date=data['install_date'])
   
        else: 
            _device.device = device
            _device.location = data['location']
            _device.area = data['area']
            _device.install_date= datetime.strptime(data['install_date'], '%Y-%m-%d')

        try:
            _device.save_to_db()    
        except:
            return {"message": "An error occurred inserting the device."}

        return _device.json()
