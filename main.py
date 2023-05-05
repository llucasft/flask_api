from flask import Flask, request, g
from flask_restful import Resource, Api, reqparse, abort
import sqlite3
from sqlite3 import Error
from werkzeug.local import LocalProxy

app = Flask("flask_api")
api = Api(app)

user_post_args = reqparse.RequestParser()
user_post_args.add_argument("name", type=str, help="Name is required.", required=True)
user_post_args.add_argument("email", type=str, help="Email is required.", required=True)
user_post_args.add_argument("password", type=str, help="Password is required.", required=True)

conn = sqlite3.connect('database.db')

class UserList(Resource):
    def get(self):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users
            (id INTEGER PRIMARY KEY, name TEXT, email TEXT, password TEXT)''')
        c.execute('SELECT * FROM users')
        rows = c.fetchall()
        users = {}
        for row in rows:
            users[row[0]] = {"name": row[1], "email": row[2], "password": row[3]}
        conn.close()
        return users

class User(Resource):
    def get(self, user_id):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users
            (id INTEGER PRIMARY KEY, name TEXT, email TEXT, password TEXT)''')
        c.execute('SELECT * FROM users WHERE id=?', (user_id,))
        row = c.fetchone()
        if row is None:
            return f"Usuário com id {user_id} não encontrado."
        user = {"name": row[1], "email": row[2], "password": row[3]}
        conn.close()
        return user
    
    def post(self, user_id):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()

        c.execute('''CREATE TABLE IF NOT EXISTS users
            (id INTEGER PRIMARY KEY, name TEXT, email TEXT, password TEXT)''')
        args = user_post_args.parse_args()
        c.execute('SELECT * FROM users WHERE id=?', (user_id,))
        row = c.fetchone()
        if row:
            return f"Usuário com id {user_id} já existe."
        c.execute('INSERT INTO users(id, name, email, password) VALUES (?, ?, ?, ?)', (user_id, args["name"], args["email"], args["password"]))
        conn.commit()
        user = {"name": args["name"], "email": args["email"], "password": args["password"]}
        conn.close()
        return user
        
api.add_resource(User, '/users/<user_id>')
api.add_resource(UserList, '/users')

if __name__ == '__main__':
    app.run(debug=True)
