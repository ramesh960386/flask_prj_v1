from flask import request, jsonify, make_response
from flask import Blueprint
from src.utils.common import *
from .service import (
    create_author_service, update_author_service, get_author_service, delete_author_service
)
from src.users.auth import token_required


author_bp = Blueprint('author', __name__, url_prefix='/author')


@author_bp.errorhandler(CustomException)
def handle_author_exception(e):
    return {"success": False, "error": e.message}, e.code

@author_bp.route('', methods=['POST'])
@token_required
def create_author(current_user):
    payload = request.get_json()
    response, status = create_author_service(payload)
    return make_response(response, status)


@author_bp.route('/<int:id>', methods=['PUT'])
@token_required
def update_author(current_user, id):
    payload = request.get_json()
    response, status = update_author_service(id, payload)
    return make_response(response, status)


@author_bp.route('/<int:id>', methods=['GET'])
@author_bp.route('', methods=['GET'])
@token_required
def get_author(current_user, id=None):
    response, status = get_author_service(id)
    return make_response(response, status)


@author_bp.route('/<int:id>', methods=['DELETE'])
@token_required
def delete_author(current_user, id):
    response, status = delete_author_service(id)
    return make_response(response, status)