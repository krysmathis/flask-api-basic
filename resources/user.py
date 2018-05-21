import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel as User

class UserRegister(Resource) : 
    
    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type=str,
        required=True,
        help="This field cannot be blank."    
    )
    parser.add_argument('password',
        type=str,
        required=True,
        help="This field cannot be blank."    
    )

    def post(self) :

        # get the data from the json payload
        data = UserRegister.parser.parse_args()

        # no duplicate usernames
        if User.find_by_username(data['username']) :
            return {"message": "Username already exists"}, 400

        user = User(data['username'], data['password'])
        user.save_to_db()

        return {"message": "User created successfully"}, 201