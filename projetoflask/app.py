from flask import Flask
from projetoflask.ext import configuration
from projetoflask.ext import appearance
from projetoflask.ext import database
from projetoflask.ext import auth
from projetoflask.ext import admin
from projetoflask.ext import commands
from projetoflask.ext import login

from projetoflask.blueprints import views
from projetoflask.blueprints import restapi



app = Flask(__name__)

configuration.init_app(app)
appearance.init_app(app)
database.init_app(app)
auth.init_app(app)
admin.init_app(app)
commands.init_app(app)
views.init_app(app)
login.init_app(app)
restapi.init_app(app)
