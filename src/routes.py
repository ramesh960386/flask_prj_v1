from flask import Blueprint
from src.users.view import user_bp
from src.authors.view import author_bp
from src.books.view import book_bp


api_router = Blueprint("api_v1", __name__, url_prefix="/api/v1")


api_router.register_blueprint(user_bp)
api_router.register_blueprint(author_bp)
api_router.register_blueprint(book_bp)
