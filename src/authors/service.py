from src.utils.http_code import *
from src.utils.common import *
from .schema import AuthorSchema
from src.models import Author


def create_author_service(payload):
    author_schema = AuthorSchema()
    errors = author_schema.validate(payload)
    if errors:
        return generate_response(message=errors)
    author = Author(**payload)
    author.save_to_db()
    return generate_response(
        data=author.serialize, message="Successfully registered.", status=HTTP_201_CREATED
    )

def update_author_service(id, payload):
    author_schema = AuthorSchema()
    errors = author_schema.validate(payload)

    if errors:
        return generate_response(message=errors)

    author = Author.find_by_id(id)
    if author is None:
        return generate_response(
            message="No record found", status=HTTP_404_NOT_FOUND
        )
    
    author.name = payload.get('name')
    author.save_to_db()
    return generate_response(
        data=author.serialize, message="Book updated successfully", status=HTTP_200_OK
    )


def get_author_service(id=None):
    if id:
        author = Author.find_by_id(id)
        if author is None:
            # raise CustomException(f'author {id} not found', 404)
            return generate_response(
                message="No record found", status=HTTP_404_NOT_FOUND
            )
        return generate_response(
            data=author.serialize, message="Author retrieved successfully", status=HTTP_200_OK
        )
    author_list_dict = dict_helper(Author.find_all())
    return generate_response(
        data=author_list_dict, message="Author retrieved successfully", status=HTTP_200_OK
    )

def delete_author_service(id):
    author = Author.find_by_id(id)
    if author is None:
        return generate_response(
            message="No record found", status=HTTP_404_NOT_FOUND
        )
    author.delete_from_db()
    return generate_response(
        message="Author was deleted", status=HTTP_204_NO_CONTENT
    )