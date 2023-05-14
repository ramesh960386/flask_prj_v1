from src.utils.http_code import *
from src.utils.common import *
from .schema import BookSchema
from src.models import Book, Author


def create_book_service(payload):
    book_schema = BookSchema()    
    errors = book_schema.validate(payload)
    if errors:
        return generate_response(message=errors)
    
    author = Author.find_by_id(payload.get('author_id'))
    if author is None:
        return generate_response(
           message="No author record found", status=HTTP_404_NOT_FOUND
        )
    
    book = Book(**payload)
    book.save_to_db()
    return generate_response(
        data=book.serialize, message="Successfully registered.", status=HTTP_201_CREATED
    )

def update_book_service(id, payload):
    book_schema = BookSchema()
    errors = book_schema.validate(payload)

    if errors:
        return generate_response(message=errors)

    book = Book.find_by_id(id)
    if book is None:
        return generate_response(
           message="No record found", status=HTTP_404_NOT_FOUND
        )
    
    author = Author.find_by_id(payload.get('author_id'))
    if author is None:
        return generate_response(
           message="No author record found", status=HTTP_404_NOT_FOUND
        )

    book.title = payload.get('title')
    book.author_id = author.id
    book.year_published = payload.get('year_published')
    book.params = payload.get('params')
    book.save_to_db()
    return generate_response(
        data=book.serialize, message="Book updated successfully", status=HTTP_200_OK
    )


def get_book_service(id=None):
    if id:
        book = Book.find_by_id(id)
        if book is None:
            return generate_response(
                message="No record found", status=HTTP_404_NOT_FOUND
            )
        return generate_response(
            data=book.serialize, message="Book retrieved successfully", status=HTTP_200_OK
        )
    book_list_dict = dict_helper(Book.find_all())
    return generate_response(
        data=book_list_dict, message="Books retrieved successfully", status=HTTP_200_OK
    )

def delete_book_service(id):
    book = Book.find_by_id(id)
    if book is None:
        return generate_response(
            message="No record found", status=HTTP_404_NOT_FOUND
        )
    book.delete_from_db()
    return generate_response(
        message="Book was deleted", status=HTTP_204_NO_CONTENT
    )