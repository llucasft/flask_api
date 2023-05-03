from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import sqlite3

app = Flask("flask_api")
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('name', required=True)
parser.add_argument('email', required=True)
parser.add_argument('password', required=True)

conn = sqlite3.connect('users.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, email TEXT NOT NULL, password TEXT NOT NULL
)''')
conn.commit()

class User(Resource):

    def get(self, user_id):
        if user_id == "all":
            c.execute('''SELECT * FROM users''')
            users = {}
            for row in c.fetchall():
                users[row[0]] = {'name': row[1]}, {'email': row[2]}, {'password': row[3]}
                conn.close()
                return users
        c.execute("SELECT * FROM users WHERE id=?", (user_id,))
        row = c.fetchone()
        conn.close()
        if row:
            return {row[0]: {'name': row[1], 'email': row[2], 'password': row[3]}}
        else:
            return {"message": "User not found"}, 404
    
    def put(self, user_id):
        args = parser.parse_args()
        new_user = {'name': args['name'], 'email': args['email'], 'password': args['password']}
        conn = sqlite3.connect('mydatabase.db')
        c = conn.cursor()
        c.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (args['name'], args['email'], args['password']))
        new_user_id = c.lastrowid
        conn.commit()
        conn.close()
        
        return {new_user_id: new_user}, 201
    
api.add_resource(User, '/users/<user_id>')

if __name__ == '__main__':
    app.run(debug=True)
