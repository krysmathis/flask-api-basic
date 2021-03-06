from flask import Flask, Response, abort, render_template, request
from flask_restful import Resource, Api
from flask_jwt import JWT

import json

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.area import Area, AreaList
from resources.validator import Validator
from resources.capture import Capture
from resources.device import Device
from models.capture import CaptureModel

app = Flask (__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True 
app.secret_key = 'krys'
api = Api(app)

jwt = JWT(app, authenticate, identity) #/auth

# @app.before_first_request
# def local_build():
#     print(request.url_root)
#     if request.url_root == 'http://localhost:5000/': 
#         db.create_all()


@app.route('/') 
def hello_world() : 
    # get data from database - call api return json
    rows = [capture.json() for capture in CaptureModel.query.all()]
    # populate the  page with the data
    return render_template('home.html', title='Shelf-Flask-API', rows=rows)

@app.route('/status')
def db_status(): 
    return render_template('status.html')

api.add_resource(UserRegister, '/register')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(Area, '/area/<string:location>')
api.add_resource(Capture, '/capture/<string:device>')
api.add_resource(Device, '/device/<string:device>')
api.add_resource(ItemList, '/items')
api.add_resource(AreaList, '/areas')
api.add_resource(Validator, '/validate')

if __name__ == '__main__' : 
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)