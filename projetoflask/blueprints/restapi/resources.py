from flask import jsonify, abort, request
from flask_login import LoginManager, login_user, current_user
from flask_restful import Resource
from projetoflask.ext.database import User, CarteiraUser, DadosUserCard, Address
from projetoflask.ext.commands import save_user, delete_user, save_cpf_age, save_adress, save_carteira_user
from projetoflask.ext.login import login_manager


@login_manager.user_loader
def load_user(id):
    user = User.query.filter_by(user_id=id).first()
    return user

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

        if "username" not in data or "email" not in data or "senha" not in data:
            return {"message": "Username and email are required"}, 400

        new_user = User(username=data["username"], email=data["email"], phone=data["phone"], senha=data["senha"])

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

            if('senha' in data):
                up_user.senha = data["senha"]

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
        

class CardResource(Resource):
    def get(self):
        cards = CarteiraUser.query.all() or abort(204)
        return jsonify(
            {'cards': [card.to_dict() for card in cards]}
        )
    

class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(username=data["username"]).first()
        if user and user.senha == data["senha"]:
            login_user(user)
            
            return {"message": "User Login successfully"}, 201
        else:
            return {"message": "User Login error"}

class DataCardPostResource(Resource):
    def post(self):
        data = request.get_json()
        if "cpf" not in data or "age" not in data or "email" not in data:
            return {"message": "Cpf, Age and E-mail are required"}, 400

        user = User.query.filter_by(email=data["email"]).first()
        if user:
            user_id = user.id
            new_cpf_age = DadosUserCard(cpf=data["cpf"], age=data["age"], user_id=user_id)
            try:
                save_cpf_age(new_cpf_age) 
                return {"message": "Dados Usar Card created successfully"}, 201
            except Exception as e:
                return {"message": str(e)}, 500

        else:
            return {"message": str(e)}, 500
        
class DataAddressUser(Resource):
    def post(self):
        data = request.get_json()
        if "street" not in data or "number" not in data or "city" not in data or "state" not in data or "postal_code" not in data:
            return {"message": "Street, Number, City, State, and Postal Code are required for address"}, 400

        #consulta para trazer o id do user com email "preciso mudar isso para busca pelo current_user"
        user = User.query.filter_by(email=data["email"]).first()
        if user:
            user_id = user.id
            # atributos de endereço estão presentes em data?
            if "street" in data and "number" in data and "city" in data and "state" in data and "postal_code" in data:
                new_address = Address(
                    street=data["street"],
                    number=data["number"],
                    city=data["city"],
                    state=data["state"],
                    postal_code=data["postal_code"],
                    user_id = user_id
                )
                try:
                    save_adress(new_address)
                    return {"message": "User Address created successfully"}, 201
                except Exception as e:
                    return {"message": str(e)}, 500
            else:
                return {"message": "Street, Number, City, State, and Postal Code are required for address"}, 400
        else:
            return {"message": "User not found"}, 404
        
class DataCarteiraUser(Resource):
    def post(self):
        data = request.get_json()

        if "user_idolo" not in data or "email" not in data:
            return {"message": "Idolo not found"}, 400

        user = User.query.filter_by(email=data["email"]).first()
        if user:
            first_data_user_card = user.data_user_card[0] if user.data_user_card else None

            if first_data_user_card:
                # Recuperando CPF com o relationship
                cpf = first_data_user_card.cpf
            user_id = user.id
            
            address = Address.query.filter(Address.id == user_id).first()
            if cpf or address:
                cpf_id = cpf
                address_id = address.id

                if "user_idolo" in data:
                    new_carteira_user = CarteiraUser(user_idolo=data["user_idolo"], user_id=user_id, cpf_id=cpf_id, address_id=address_id)
                    try:
                        save_carteira_user(new_carteira_user)
                        return {"message": "User Address created successfully"}, 201
                    except Exception as e:
                        return {"message": str(e)}, 500
                else:
                    return {"message": "User Idolo not provided"}, 400
            else:
                return {"message": "CPF or Address not found"}, 400
        else:
            return {"message": "User not found"}, 404
