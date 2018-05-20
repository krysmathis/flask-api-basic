from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3


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
    
    parser.add_argument('date',
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
        
        area = self.find_by_name(name)
        if area:
            return area
        return {'message': 'Item not found'}, 404

    @classmethod
    def find_by_name(cls, location):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM {table} WHERE location=?".format(table=cls.TABLE_NAME)
        result = cursor.execute(query, (location,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'search': {'location': row[1], 'date_captured': row[3]}}

    def post(self, area):
        # if self.find_by_name(area):
        #     return {'message': "An item with area '{}' already exists.".format(area)}

        print(Area.parser)
        data = Area.parser.parse_args()

        # may need to parse again here to convert image to proper sqlite format

        area = {'location': area, 'locationid': data['locationid'], 'captured_date': data['captured_date'], 'image': data['image']}

        try:
            Item.insert(area)
        except:
            return {"message": "An error occurred inserting the area."}

        return area

    @classmethod
    def insert(cls, area):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO {table} VALUES(NULL, ?, ?, ?, ?)".format(table=cls.TABLE_NAME)
        cursor.execute(query, (area['location'], area['locationid'], area['captured_date'], area['image']))

        connection.commit()
        connection.close()

    @jwt_required()
    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM {table} WHERE name=?".format(table=self.TABLE_NAME)
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()

        return {'message': 'Item deleted'}

    # @jwt_required()
    # def put(self, name):
    #     data = Item.parser.parse_args()
    #     item = self.find_by_name(name)
    #     updated_item = {'name': data['name'], 'price': data['price']}
    #     if item is None:
    #         try:
    #             Item.insert(updated_item)
    #         except:
    #             return {"message": "An error occurred inserting the item."}
    #     else:
    #         try:
    #             Item.update(updated_item)
    #         except:
    #             raise
    #             return {"message": "An error occurred updating the item."}
    #     return updated_item

    # @classmethod
    # def update(cls, item):
    #     connection = sqlite3.connect('data.db')
    #     cursor = connection.cursor()

    #     query = "UPDATE {table} SET price=? WHERE name=?".format(table=cls.TABLE_NAME)
    #     cursor.execute(query, (item['price'], item['name']))

    #     connection.commit()
    #     connection.close()


class AreaList(Resource):
    TABLE_NAME = 'areas'

    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM {table}".format(table=self.TABLE_NAME)
        result = cursor.execute(query)
        areas = []
        #for row in result:
            # TODO:
            #Areas.append({'name': row[1], 'price': row[2]})
        connection.close()

        return {'areas': areas}