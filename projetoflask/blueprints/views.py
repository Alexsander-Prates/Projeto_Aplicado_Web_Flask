from flask import abort, render_template
from projetoflask.ext.database import User

def init_app(app):
    @app.route("/")
    def index():
        users = User.query.all()
        print(users)
        return render_template("index.html", users=users)


    @app.route("/user/<user_id>")
    def user(user_id):
        user = User.query.filter_by(id=user_id).first()or abort(
            404, "User not found"
        )
        return render_template("user.html", user=user)