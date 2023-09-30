from flask import Blueprint
from flask_restful import Api

from .resources import UserResource, UserDataResource, UserPostResource, \
    UserDataUpdateResource, UserDeleteResource, CardResource, UserLogin, \
    DataCardPostResource, DataAddressUser, DataCarteiraUser

bp = Blueprint("restapi", __name__, url_prefix="/api/v1")
api = Api(bp)
api.add_resource(UserResource, "/user/")
api.add_resource(UserDataResource, "/user/<user_id>", methods=["GET"])
api.add_resource(UserPostResource, "/user/post/", methods=["POST"])
api.add_resource(UserDataUpdateResource, "/user/update/<user_id>", methods=["PUT"])
api.add_resource(UserDeleteResource, "/user/delete/<user_id>", methods=["DELETE"])

api.add_resource(UserLogin, "/user/login/", methods=["POST"])

api.add_resource(CardResource, "/card/")

api.add_resource(DataCardPostResource, "/card/data_user/", methods=["POST"])

api.add_resource(DataAddressUser, "/user/address/", methods=["POST"])

api.add_resource(DataCarteiraUser, "/user/card/", methods=["POST"])



def init_app(app):
    app.register_blueprint(bp)