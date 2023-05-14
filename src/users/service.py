import uuid
from src import app
from src.models import User, UserRole
from datetime import datetime, timedelta
from src.utils.http_code import *
from src.utils.common import *
from .schema import SignupSchema, LoginSchema


def signup_service(payload):
    """
    It creates a new user

    :param request: The request object
    :param input_data: This is the data that is passed to the function
    :return: A response object
    """
    signup_schema = SignupSchema()
    errors = signup_schema.validate(payload)
    if errors:
        return generate_response(message=errors)
    
    name = payload.get('name')
    email = payload.get('email')
    password = payload.get('password')
    role = payload.get('role')
    role = role.upper() if role else role
    check_email_exist = User.find_by_email(email)
    
    if check_email_exist:
        return generate_response(
            message="Email already taken", status=HTTP_202_ACCEPTED
        )

    user = User(
        public_id=str(uuid.uuid4()), name=name,
        email=email, password=password, role=role
    )
    user.hash_password_hash()
    user.save_to_db()
    return generate_response(
        data=user.serialize, message="Successfully registered.", status=HTTP_201_CREATED
    )


def login_service(email, password):
    payload = {'email': email, 'password': password}
    login_schema = LoginSchema()
    errors = login_schema.validate(payload)

    if errors:
        return generate_response(message=errors)
    
    user = User.find_by_email(email)
    if user is None:
        return generate_response(message="User not found", status=HTTP_400_BAD_REQUEST)
    response = {'email': email}
    if user.check_password_hash(password):
        token = jwt.encode(
            {
                "public_id": user.public_id, "email": user.email, "name": user.name,
                "exp" : datetime.utcnow() + timedelta(minutes = 30)
            }, app.config.get("SECRET_KEY"), "HS256"
        )
        response["token"] = token
        return generate_response(
            data=response, message="User login successfully", status=HTTP_201_CREATED
        )
    else:
        return generate_response(
            message="Password is wrong", status=HTTP_400_BAD_REQUEST
        )

def get_user_service(id=None):
    if id:
        user = User.find_by_id(id)
        if user is None:
            return generate_response(
                message="No record found", status=HTTP_404_NOT_FOUND
            )
        return generate_response(
            data=user.serialize, message="User retrieved successfully", status=HTTP_200_OK
        )
    user_list_dict = dict_helper(User.find_all())
    return generate_response(
        data=user_list_dict, message="Books retrieved successfully", status=HTTP_200_OK
    )


def delete_user_service(id):
    user = User.find_by_id(id)
    if user is None:
        return generate_response(
            message="No record found", status=HTTP_404_NOT_FOUND
        )
    
    if user.role.name != UserRole.ADMIN.name:
        return generate_response(
            message="admin permission required to delete", status=HTTP_404_NOT_FOUND
        )
    user.delete_from_db()
    return generate_response(
        message="User was deleted", status=HTTP_204_NO_CONTENT
    )

"""
def login_service(email, password):
    payload = {'email': email, 'password': password}
    login_schema = LoginSchema()
    errors = login_schema.validate(payload)

    if errors:
        return generate_response(message=errors)
    
    user = User.find_by_username(email)
    if not user or user.password != password:
        return generate_response(message="Invalid username or password", status=HTTP_401_UNAUTHORIZED)
    access_token = create_access_token(identity={"email": user.email, "permission_level": user.permission_level.value})    
    return generate_response(
        data={"access_token": access_token}, message="User login successfully", status=HTTP_201_CREATED
    )
"""