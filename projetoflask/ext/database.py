from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy_serializer import SerializerMixin





db = SQLAlchemy()

class User(db.Model, SerializerMixin, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(80), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    
    # relação para a classe DataUserCard
    data_user_card = db.relationship('DadosUserCard', backref='user')
    # relação para a classe Address
    addresses = db.relationship('Address', backref='user')
    # relação para a classe CarteiraUser
    carteira_users = db.relationship('CarteiraUser', backref='user')
    

    def to_dict(self):
       return {
           'id': self.id,
           'username': self.username,
           'email': self.email,
           'phone': self.phone,
           'senha': self.senha
       }
    
    


class DadosUserCard(db.Model):
    cpf = db.Column(db.BigInteger, primary_key=True)
    age = db.Column(db.String(2), nullable=False)
    
    # chave estrangeira para a classe User
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def to_dict(self):
        return {
            'cpf': self.cpf,
            'age': self.age,
            'user_id': self.user_id  
        }

class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(100), nullable=False)
    number = db.Column(db.String(10), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(2), nullable=False)
    postal_code = db.Column(db.String(10), nullable=False)
    
    # chave estrangeira para a classe User
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def to_dict(self):
        return {
            'id': self.id,
            'street': self.street,
            'number': self.number,
            'city': self.city,
            'state': self.state,
            'postal_code': self.postal_code,
            'user_id': self.user_id  
        }

class CarteiraUser(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_idolo = db.Column(db.String(80), unique=True, nullable=False)

    # chaves estrangeiras para a class User, DadosUserCard e Address
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    cpf_id = db.Column(db.BigInteger, db.ForeignKey('dados_user_card.cpf'))
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'))

    def to_dict(self):
        return {
            'id': self.id,
            'user_idolo': self.user_idolo,
            'user_id': self.user_id,
            'cpf_id': self.cpf_id,
            'address_id': self.address_id
        }
    
def init_app(app):
    db.init_app(app)

    




