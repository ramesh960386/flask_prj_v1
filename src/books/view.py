from flask import request, jsonify, make_response
from flask import Blueprint
from src.utils.common import *
from .service import (
    create_book_service, update_book_service, get_book_service, delete_book_service
)
from src.users.auth import token_required


book_bp = Blueprint('book', __name__, url_prefix='/book')


@book_bp.errorhandler(CustomException)
def handle_book_exception(e):
    return {"success": False, "error": e.message}, e.code

@book_bp.route('', methods=['POST'])
@token_required
def create_book(current_user):
    payload = request.get_json()
    response, status = create_book_service(payload)
    return make_response(response, status)


@book_bp.route('/<int:id>', methods=['PUT'])
@token_required
def update_book(current_user, id):
    payload = request.get_json()
    response, status = update_book_service(id, payload)
    return make_response(response, status)


@book_bp.route('/<int:id>', methods=['GET'])
@book_bp.route('', methods=['GET'])
@token_required
def get_book(current_user, id=None):
    response, status = get_book_service(id)
    return make_response(response, status)


@book_bp.route('/<int:id>', methods=['DELETE'])
@token_required
def delete_book(current_user, id):
    response, status = delete_book_service(id)
    return make_response(response, status)