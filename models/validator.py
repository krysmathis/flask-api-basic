from flask_restful import Resource

class Validator(Resource) :

    def get(self):
        return {'message': 'This is working'}, 200