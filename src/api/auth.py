# src/api/auth.py
from flask import request, jsonify
from flask_restx import Namespace, Resource
from flask_jwt_extended import create_access_token
from src.models import User
from app import bcrypt, db

api = Namespace('Auth', description='Authentication related operations')

login_fields = api.model('Login', {
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
})

@api.route('/login')
class Login(Resource):
    @api.expect(login_fields)
    def post(self):
        email = request.json.get('email')
        password = request.json.get('password')
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            access_token = create_access_token(identity=email)
            return jsonify(access_token=access_token)
        return jsonify({"msg": "Bad email or password"}), 401

@api.route('/register')
class Register(Resource):
    @api.expect(login_fields)
    def post(self):
        email = request.json.get('email')
        password = request.json.get('password')
        if User.query.filter_by(email=email).first():
            return jsonify({"msg": "User already exists"}), 400
        user = User(email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return jsonify({"msg": "User created successfully"}), 201
