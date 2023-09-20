
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