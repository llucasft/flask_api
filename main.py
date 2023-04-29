from flask import Flask
from flask_restful import Resource, Api

app = Flask("flask_api")
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {'Felipe': 'Gay'}
    
api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(debug=True)
