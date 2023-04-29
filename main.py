from flask import Flask
from flask_restful import Resource, Api

app = Flask("flask_api")
api = Api(app)

users = {
    'user1': { 'name': 'João'}
}

class User(Resource):
    def get(self):
        return {'Felipe': 'Gay'}
    
api.add_resource(User, '/')

if __name__ == '__main__':
    app.run(debug=True)
