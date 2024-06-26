"""
Users controller module
"""

from flask import abort
from src.models.user import User
from utils.functions import validate_email


def get_users():
    """Returns all users"""
    users: list[User] = User.get_all()

    return [user.to_dict() for user in users]


def create_user(data: dict):
    """Creates a new user"""

    email: str = data.get("email", "")

    valid_email = validate_email(email)

    if not valid_email:
        abort(400, "Invalid email")

    try:
        user = User.create(data)
    except KeyError as e:
        abort(400, f"Missing field: {e}")
    except ValueError as e:
        abort(400, str(e))

    if user is None:
        abort(400, "User already exists")

    return user.to_dict(), 201


def get_user_by_id(user_id: str):
    """Returns a user by ID"""
    user: User | None = User.get(user_id)

    if not user:
        abort(404, f"User with ID {user_id} not found")

    return user.to_dict(), 200


def update_user(user_id: str, data: dict):
    """Updates a user by ID"""
    try:
        user = User.update(user_id, data)
    except ValueError as e:
        abort(400, str(e))

    if user is None:
        abort(404, f"User with ID {user_id} not found")

    return user.to_dict(), 200


def delete_user(user_id: str):
    """Deletes a user by ID"""
    if not User.delete(user_id):
        abort(404, f"User with ID {user_id} not found")

    return "", 204
