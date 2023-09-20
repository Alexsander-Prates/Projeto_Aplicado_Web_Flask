from flask import Blueprint
from flask_restful import Api

from .resources import UserResource, UserDataResource, UserPostResource, UserDataUpdateResource, UserDeleteResource

bp = Blueprint("restapi", __name__, url_prefix="/api/v1")
api = Api(bp)
api.add_resource(UserResource, "/user/")
api.add_resource(UserDataResource, "/user/<user_id>", methods=["GET"])
api.add_resource(UserPostResource, "/user/post/", methods=["POST"])
api.add_resource(UserDataUpdateResource, "/user/update/<user_id>", methods=["PUT"])
api.add_resource(UserDeleteResource, "/user/delete/<user_id>", methods=["DELETE"])


def init_app(app):
    app.register_blueprint(bp)