from flask import Blueprint

public = Blueprint("public", __name__, template_folder="templates/public")

# noinspection PyPep8
from . import views