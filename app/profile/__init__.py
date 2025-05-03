from flask import Blueprint

profile = Blueprint("profile", __name__, template_folder="templates/profile")

# noinspection PyPep8
from . import views
