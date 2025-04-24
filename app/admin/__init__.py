from flask import Blueprint

admin = Blueprint("admin", __name__, template_folder="templates/admin")

# noinspection PyPep8
from . import views
