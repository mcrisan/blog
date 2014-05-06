from flask import Blueprint
service = Blueprint('service', __name__, template_folder='templates')


from service import rest_service