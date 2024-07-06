"""
User related functionality
"""

from src import repo, db
from typing import Optional
from src.models.base import Base
from datetime import datetime


class User(Base, db.Model):
#class User(Base):
    """User representation"""

    #class User(db.Model):
    #__tablename__ = 'users'

    email = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    #places = db.relationship("place", cascade="all, delete-orpahn")
    #reviews = db.relationship("review", cascade="all, delete-orpahn")
    
    
    """email: str
    password: str | None
    first_name: str
    last_name: str"""

    def __init__(
        self,
        email: str,
        first_name: str,
        last_name: str,
        password: str,
        is_admin: Optional[bool] = None,
        **kw,
    ):
        """Dummy init"""
        super().__init__(**kw)
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.is_admin = is_admin

    def __repr__(self) -> str:
        """Dummy repr"""
        return f"<User {self.id} ({self.email})>"

    def to_dict(self) -> dict:
        """Dictionary representation of the object"""
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "password": self.password,
            "is_admin": self.is_admin,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @staticmethod
    def create(user: dict) -> "User":
        """Create a new user"""
        users: list["User"] = User.get_all()

        for u in users:
            if u.email == user["email"]:
                raise ValueError("User already exists")

        new_user = User(**user)
        repo.save(new_user)

        return new_user

    @staticmethod
    def update(user_id: str, data: dict) -> "User | None":
        """Update an existing user"""
        user: User | None = User.get(user_id)

        if not user:
            return None

        for key, value in data.items():
            setattr(user, key, value)
        
        
        """if "email" in data:
            user.email = data["email"]
        if "first_name" in data:
            user.first_name = data["first_name"]
        if "last_name" in data:
            user.last_name = data["last_name"]
        
        #####################################
        if "password" in data:
            user.password = data["password"]
        if "is_admin" in data:
            user.is_admin = data["is_admin"]"""

        repo.update(user)

        return user

#User.query.all()
# pepe = User("asljdlaskjd@.comasd", "pepe", "señor", id=3)
#User.query.filter_by(id=3).first()##
