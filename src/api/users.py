"""
This module contains the routes for the users endpoints.
"""
from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from src.models.user import User
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, jwt_required
from src.controllers.users import (
    create_user,
    delete_user,
    get_user_by_id,
    get_users,
    update_user,
)

api = Namespace("User", description="User related operations")

user_input_fields = api.model('UserInput', {
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user'),
    'first_name': fields.String(description='First name of the user'),
    'last_name': fields.String(description='Last name of the user'),
    'is_admin': fields.Boolean(description='Is admin')
})

user_fields = api.model('User', {
    'id': fields.Integer(description='ID of the user'),
    'email': fields.String(description='Email of the user'),
    'first_name': fields.String(description='First name of the user'),
    'last_name': fields.String(description='Last name of the user'),
    'is_admin': fields.Boolean(description='Is admin'),
    'created_at': fields.DateTime(description='User creation date'),
    'updated_at': fields.DateTime(description='User last update date')
})

@api.route('/')
class UserList(Resource):
    """Handles HTTP requests to URL: /users"""

    @api.marshal_list_with(user_fields)
    @jwt_required()
    def get(self):
        """Get all users"""
        return get_users()

    @api.expect(user_input_fields)
    @api.marshal_with(user_fields, code=201)
    @jwt_required()
    def post(self):
        """Create a new user"""
        return create_user(api.payload)


@api.route('/<int:user_id>')
@api.doc(params={'user_id': 'The ID of the user'})
class User(Resource):
    """Handles HTTP requests to URL: /users/<user_id>"""

    @api.marshal_with(user_fields)
    @jwt_required()
    def get(self, user_id):
        """Get a user by ID"""
        return get_user_by_id(user_id)

    @api.expect(user_input_fields)
    @api.marshal_with(user_fields)
    @jwt_required()
    def put(self, user_id):
        """Update a user by ID"""
        return update_user(user_id, api.payload)

    @api.response(204, 'User deleted')
    @jwt_required()
    def delete(self, user_id):
        """Delete a user by ID"""
        return delete_user(user_id)

