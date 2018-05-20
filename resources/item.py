from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel
import sqlite3


class Item(Resource):
    
    TABLE_NAME = 'items'

    parser = reqparse.RequestParser()
    
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )
    

    @jwt_required()
    def get(self, name):
        
        item = ItemModel.find_by_name(name)
        if item:
            return item
        return {'message': 'Item not found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}

        print(Item.parser)
        data = self.parser.parse_args()

        item = {'name': name, 'price': data['price']}

        try:
            ItemModel.insert(item)
        except:
            return {"message": "An error occurred inserting the item."}

        return item

    
    @jwt_required()
    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM {table} WHERE name=?".format(table=self.TABLE_NAME)
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()

        return {'message': 'Item deleted'}

    @jwt_required()
    def put(self, name):
        data = self.parser.parse_args()
        item = ItemModel.find_by_name(name)
        updated_item = {'name': data['name'], 'price': data['price']}
        if item is None:
            try:
                ItemModel.insert(updated_item)
            except:
                return {"message": "An error occurred inserting the item."}
        else:
            try:
                ItemModel.update(updated_item)
            except:
                raise
                return {"message": "An error occurred updating the item."}
        return updated_item

    

class ItemList(Resource):
    TABLE_NAME = 'items'

    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM {table}".format(table=self.TABLE_NAME)
        result = cursor.execute(query)
        items = []
        for row in result:
            items.append({'name': row[1], 'price': row[2]})
        connection.close()

        return {'items': items}