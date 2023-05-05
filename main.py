from flask import Flask, request
from flask_restful import Resource, Api, reqparse, abort
import sqlite3

app = Flask("flask_api")
api = Api(app)

users = {
    1: {"name": "Lucas", "email": "lucas@example.com", "password": "1234"},
    2: {"name": "Jose", "email": "jose@example.com", "password": "4321"},
    3: {"name": "Maria", "email": "maria@example.com", "password": "abcd"}
}

user_post_args = reqparse.RequestParser()
user_post_args.add_argument("name", type=str, help="Name is required.", required=True)
user_post_args.add_argument("email", type=str, help="Email is required.", required=True)
user_post_args.add_argument("password", type=str, help="Password is required.", required=True)

class UserList(Resource):
    def get(self):
        return users

class User(Resource):
    def get(self, user_id):
        user_id = int(user_id)
        return users[user_id]
    
    def post(self, user_id):
        user_id = int(user_id)
        args = user_post_args.parse_args()
        if user_id in users:
            abort(409, "Usuário com id já existente.")
        users[user_id] = {"name": args["name"], "email": args["email"], "password": args["password"]}    
        return users[user_id]        
    
api.add_resource(User, '/users/<user_id>')
api.add_resource(UserList, '/users')

if __name__ == '__main__':
    app.run(debug=True)
