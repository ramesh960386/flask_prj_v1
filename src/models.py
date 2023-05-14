from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON, UUID
from werkzeug.security import generate_password_hash, check_password_hash
from typing import List
from src import app
import uuid
from enum import Enum

db = SQLAlchemy(app)

class UserRole(str, Enum):
    USER = "USER"
    ADMIN = "ADMIN"

class PermissionLevels(Enum):
    ADMIN = 1
    MANAGER = 2
    USER = 3

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    public_id = db.Column(db.String(50), unique = True)
    # public_id = db.Column(UUID(as_uuid=True))
    name = db.Column(db.String(100))
    email = db.Column(db.String(70), unique = True)
    password = db.Column(db.String(120))
    # role = db.Column(db.String(10), nullable=False)
    role: str = db.Column(db.Enum(UserRole), default=UserRole.USER)
    # permission_level: int = db.Column(db.Enum(PermissionLevels), default=UserRole.USER)
        
    def __repr__(self):
        return 'User(id=%s, name=%s)' % (self.id, self.name)

    @property
    def get_editable_fields(self):
        return ['name']
    
    @property
    def serialize(self):
        return {
            "id": self.id, "public_id": self.public_id,
            "name": self.name, "email": self.email, "role": self.role
        }

    @property
    def get_editable_fields(self):
        return ['name']

    @classmethod
    def find_by_name(cls, name) -> "User":
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, _id) -> "User":
        return cls.query.filter_by(id=_id).first()
    
    @classmethod
    def find_by_email(cls, _email) -> "User":
        return cls.query.filter_by(email=_email).first()
    
    @classmethod
    def find_by_public_id(cls, _public_id) -> "User":
        return cls.query.filter_by(public_id=_public_id).first()

    @classmethod
    def find_all(cls) -> List["User"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
    
    def hash_password_hash(self):
        self.password = generate_password_hash(self.password, method='sha256') #.encode().decode("utf8")
    
    def check_password_hash(self, password):
        return check_password_hash(self.password, password)
    
    @classmethod
    def find_by_username(cls, username):
        # This is just an example. In production, you should query a database instead.
        users = [
            User("admin", "admin", PermissionLevels.ADMIN),
            User("manager", "manager", PermissionLevels.MANAGER),
            User("user", "user", PermissionLevels.USER),
        ]
        return next((u for u in users if u.username == username), None)
        
        
class Author(db.Model):
    """Data model for Author."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    
    def __repr__(self):
        return 'Author(id=%s, name=%s)' % (self.id, self.name)

    @property
    def get_editable_fields(self):
        return ['name']
    
    @property
    def serialize(self):
        return {
            "id": self.id, 
            "name": self.name
        }

    @property
    def get_editable_fields(self):
        return ['name']

    @classmethod
    def find_by_name(cls, name) -> "Author":
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, _id) -> "Author":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls) -> List["Author"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

class Book(db.Model):
    """Data model for Book."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    author = db.relationship('Author', backref=db.backref('books', lazy=True))
    year_published = db.Column(db.Integer)
    params = db.Column(JSON)

    def __repr__(self):
        return 'Book(id=%s, name=%s)' % (self.id, self.title)
    
    @property
    def get_editable_fields(self):
        return ['title', 'author_id', 'author', 'year_published', 'params']
    
    @property
    def serialize(self):
        return {
            "id": self.id, 
            "title": self.title,
            "author":self.author.serialize,
            "year_published":self.year_published, 
            "params":self.params
        }

    @classmethod
    def find_by_name(cls, name) -> "Book":
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, _id) -> "Book":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls) -> List["Book"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()