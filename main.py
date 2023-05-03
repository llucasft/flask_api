from flask import Flask, request
from flask_restful import Resource, Api, reqparse

app = Flask("flask_api")
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('name', required=True)

users = {
    'user1': {'name': 'João'},
    'user2': {'name': 'Marcos'}
}

class User(Resource):

    def get(self, user_id):
        if user_id == "all":
            return users
        return users[user_id]
    
    def put(self, user_id):
        args = parser.parse_args()
        new_user = {'name': args['name']}
        users[user_id] = new_user
        
        users[f"user{len(users)+1}"] = new_user

        return {user_id: users[user_id]}, 201
    
api.add_resource(User, '/users/<user_id>')

if __name__ == '__main__':
    app.run(debug=True)
