from flask import Flask, request, g
from flask_restful import Resource, Api, reqparse, abort
import sqlite3
from sqlite3 import Error
from werkzeug.local import LocalProxy

app = Flask("flask_api")
api = Api(app)

user_post_args = reqparse.RequestParser()
user_post_args.add_argument("name", type=str, help="Name is required.", required=True)
user_post_args.add_argument("lastname", type=str, help="Last name is required.", required=True)
user_post_args.add_argument("email", type=str, help="Email is required.", required=True)
user_post_args.add_argument("phone", type=str, help="Phone is required", required=True)
user_post_args.add_argument("password", type=str, help="Password is required.", required=True)
user_post_args.add_argument("gender", type=str, help="Gender required", required=True)

class UserList(Resource):
    def get(self):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users
            (id INTEGER PRIMARY KEY, name TEXT, lastname TEXT, email TEXT,
             phone TEXT, password TEXT, gender TEXT)''')
        c.execute('SELECT * FROM users')
        rows = c.fetchall()
        users = {}
        for row in rows:
            users[row[0]] = {"name": row[1], "lastname": row[2], "email": row[3], "phone":row[4], "password": row[5], "gender": row[6]}
        conn.close()
        return users

class User(Resource):
    def get(self, user_id):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users
            (id INTEGER PRIMARY KEY, name TEXT, lastname TEXT, email TEXT, phone TEXT, password TEXT, gender TEXT)''')
        c.execute('SELECT * FROM users WHERE id=?', (user_id,))
        row = c.fetchone()
        if row is None:
            return f"Usuário com id {user_id} não encontrado."
        user = {"name": row[1], "lastname": row[2], "email": row[3], "phone":row[4], "password": row[5], "gender": row[6]}
        conn.close()
        return user
    
    def post(self, user_id):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()

        c.execute('''CREATE TABLE IF NOT EXISTS users
            (id INTEGER PRIMARY KEY, name TEXT, lastname TEXT, email TEXT, phone TEXT, password TEXT, gender TEXT)''')
        args = user_post_args.parse_args()
        c.execute('SELECT * FROM users WHERE id=?', (user_id,))
        row = c.fetchone()
        if row:
            return f"Usuário com id {user_id} já existe."
        c.execute('INSERT INTO users(id, name, lastname, email, phone, password, gender) VALUES (?, ?, ?, ?, ?, ?, ?)', (user_id, args["name"], args["lastname"], args["email"], args["phone"], args["password"], args["gender"]))
        conn.commit()
        user = {"name": args["name"], "lastname": args["lastname"], "email": args["email"], "phone": args["phone"], "password": args["password"], "gender": args["gender"]}
        conn.close()
        return user
        
api.add_resource(User, '/users/<user_id>')
api.add_resource(UserList, '/users')

if __name__ == '__main__':
    app.run(debug=True)
