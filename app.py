from flask import Flask, Response, abort, render_template
from flask_restful import Resource, Api
from flask_jwt import JWT

import json

from security import authenticate, identity
from models.user import UserRegister
from models.item import Item, ItemList
from models.area import Area, AreaList
from models.validator import Validator

app = Flask (__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True 
app.secret_key = 'krys'
api = Api(app)

jwt = JWT(app, authenticate, identity) #/auth


@app.route('/') 
def hello_world() : 
    return render_template('home.html')

api.add_resource(UserRegister, '/register')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(Area, '/area/<string:location>')
api.add_resource(ItemList, '/items')
api.add_resource(AreaList, '/areas')
api.add_resource(Validator, '/validate')

if __name__ == '__main__' : 
    from db import Db
    Db.create_db()
    app.run(debug=True)