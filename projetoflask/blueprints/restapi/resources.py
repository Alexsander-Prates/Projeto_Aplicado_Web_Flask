from flask import jsonify, abort, request
from flask_restful import Resource
from projetoflask.ext.database import User
from projetoflask.ext.commands import save_user, delete_user


class UserResource(Resource):
    def get(self):
        users = User.query.all() or abort(204)
        return jsonify(
            {'users': [user.to_dict() for user in users]}
        )


class UserDataResource(Resource):
    def get(self, user_id):
        user = User.query.filter_by(id=user_id).first() or abort(404)
        return jsonify(user.to_dict())

class UserPostResource(Resource):

    def post(self):
        data = request.get_json()

        if "username" not in data or "email" not in data:
            return {"message": "Username and email are required"}, 400

        new_user = User(username=data["username"], email=data["email"], phone=data["phone"])

        try:
            save_user(new_user) 
            return {"message": "User created successfully"}, 201
        except Exception as e:
            return {"message": str(e)}, 500
        
class UserDataUpdateResource(Resource):
    def put(self, user_id):
        up_user = User.query.filter_by(id=user_id).first() or abort(404)
        data = request.get_json()

        try:
            if('username' in data):
                up_user.username = data["username"]

            if('email' in data):
                up_user.email = data["email"]

            if('phone' in data):
                up_user.phone = data["phone"]

            save_user(up_user)
            return {"message": "User update successfully"}, 201
        except Exception as e:
            return {"message": str(e)}, 500

class UserDeleteResource(Resource):
    def delete(self, user_id):
        del_user = User.query.filter_by(id=user_id).first() or abort(404)
        try:
            delete_user(del_user)
            return {"message": "User delete successfully"}, 201
        except Exception as e:
            return {"message": str(e)}, 500