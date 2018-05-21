from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.area import AreaModel

class Area(Resource):
    TABLE_NAME = 'areas'

    parser = reqparse.RequestParser()
    
    # parse the json arguments that are going to arrive
    # url: /location
    # json: {
    #   "locationid": int,
    #   "capture_date": date,
    #   "image": blob
    # }
    parser.add_argument('locationid',
        type=int,
        required=True,
        help="This field cannot be left blank!"
    )
    
    parser.add_argument('date_captured',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('image',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )

    @jwt_required()
    def get(self, name):
        
        area = AreaModel.find_by_name(name)
        if area:
            return area.json()
            
        return {'message': 'Item not found'}, 404

    def post(self, location):
        if AreaModel.find_by_name(location):
            return {'message': "An item with area '{}' already exists.".format(location)}

        data = self.parser.parse_args()

        # may need to parse again here to convert image to proper sqlite format
        area = AreaModel(location, locationid=data['locationid'], date_captured=data['date_captured'], image=data['image'])

        try:
            area.save_to_db()
        except:
            return {"message": "An error occurred inserting the area."}

        return area.json()

   
    @jwt_required()
    def delete(self, location):

        if AreaModel.find_by_name(location) :
            AreaModel.delete_from_db()
            return {'message': 'Item deleted'}
        
        return {'message': 'Item not found'}


class AreaList(Resource):

    def get(self):
        return [area.json() for area in AreaModel.query.all()]