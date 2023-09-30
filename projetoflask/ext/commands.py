
from projetoflask.ext.database import db


def init_app(app):
    def create_db():
        """Creates database"""
        db.create_all()

    def drop_db():
        """Cleans database"""
        db.drop_all()

    
def save_user(user):
    db.session.add(user)
    db.session.commit()

def delete_user(user):
    db.session.delete(user)
    db.session.commit()

def save_cpf_age(card):
    db.session.add(card)
    db.session.commit()

def save_adress(address):
    db.session.add(address)
    db.session.commit()

def save_carteira_user(carteira_user):
    db.session.add(carteira_user)
    db.session.commit()