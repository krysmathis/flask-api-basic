from flask import Flask, Response, abort, render_template
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required, current_identity

import json

from security import authenticate, identity

app = Flask (__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True 
app.secret_key = 'krys'
api = Api(app)

jwt = JWT(app, authenticate, identity) #/auth

books = [{
    'id': 33,
    'title': 'The Raven',
    'author_id': 1,
}]


@app.route('/')
def hello_world() : 
    return render_template('home.html')


@app.route('/book')
def book_list() : 
    """Enable a user to retrieve a book list from the api."""
    response = Response(
        json.dumps(books), status = 200)
    return response



if __name__ == '__main__' : 
    app.run(debug=True)