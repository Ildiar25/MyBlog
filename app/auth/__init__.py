from flask import Blueprint

auth = Blueprint("auth", __name__, template_folder="templates/auth")

# noinspection PyPep8
from . import views
