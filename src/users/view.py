from flask import request, jsonify, make_response
from flask import Blueprint
from src.utils.common import CustomException
from src.models import User, PermissionLevels
from .service import signup_service, login_service, get_user_service, delete_user_service
from .auth import token_required


user_bp = Blueprint('user', __name__, url_prefix='/user')

@user_bp.errorhandler(CustomException)
def handle_user_exception(e):
    return {"success": False, "error": e.message}, e.code


@user_bp.route('/signup', methods =['POST'])
def signup():
	payload = request.get_json()
	response, status = signup_service(payload)
	return make_response(response, status)


@user_bp.route('/login', methods =['POST'])
def login():
	email = request.json.get('email')
	password = request.json.get('password')
	response, status = login_service(email, password)
	return make_response(response, status)


@user_bp.route('/<int:id>', methods=['GET'])
@user_bp.route('', methods=['GET'])
@token_required
def get_user(current_user, id=None):
    response, status = get_user_service(id)
    return make_response(response, status)

@user_bp.route('/<int:id>', methods=['DELETE'])
@token_required
def delete_user(current_user, id):
    response, status = delete_user_service(id)
    return make_response(response, status)

"""
@user_bp.route('/admin-only')
@requires_permission(PermissionLevels.ADMIN)
def admin_only():
    return jsonify({"message": "You have admin permission to access this resource"})

@user_bp.route('/manager-only')
@requires_permission(PermissionLevels.MANAGER)
def manager_only():
    return jsonify({"message": "You have manager permission to access this resource"})

@user_bp.route('/user-only')
@requires_permission(PermissionLevels.USER)
def user_only():
    return jsonify({"message": "You have user permission to access this resource"})
"""