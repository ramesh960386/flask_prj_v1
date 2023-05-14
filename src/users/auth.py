from flask import request, jsonify
from functools import wraps
import jwt
from src import app
from src.models import User
# from flask_jwt_extended import (
#     JWTManager, jwt_required, create_access_token,
#     get_jwt_identity
# )

# decorator for verifying the JWT
def token_required(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		token = None
		# jwt is passed in the request header
		if 'x-access-token' in request.headers:
			token = request.headers['x-access-token']
		# return 401 if token is not passed
		if not token:
			return jsonify({'message' : 'Token is missing !!'}), 401

		try:
			# decoding the payload to fetch the stored details
			data = jwt.decode(token, app.config.get("SECRET_KEY"), algorithms=["HS256"])
			current_user = User.find_by_public_id(data['public_id'])
		except:
			return jsonify({
				'message' : 'Token is invalid !!'
			}), 401
		# returns the current logged in users context to the routes
		return f(current_user, *args, **kwargs)

	return decorated

"""
def requires_permission(permission_level):
    def decorator(f):
        @wraps(f)
        @jwt_required
        def wrapper(*args, **kwargs):
            current_user_permission = get_jwt_identity().get('permission_level')
            if current_user_permission < permission_level.value:
                return jsonify({"message": "You don't have permission to access this resource"}), 403
            return f(*args, **kwargs)
        return wrapper
    return decorator
"""