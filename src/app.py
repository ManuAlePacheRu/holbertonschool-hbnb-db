from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configurar una clave para JWT
app.config['JWT_SECRET_KEY'] = 'abc.1234'

# Inicializa las extensiones
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Inicialización de JWTManager
jwt = JWTManager(app)

# Ruta para crear un token de acceso
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    
    # Parte lógica para verificar el nombre de usuario y la clave
    if username != 'test' or password != 'test':
        return jsonify({"msg": "Wrong username or password"}), 401

    # Se crea un nuevo token de acceso
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)

# Ruta protegida por JWT
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    # Para acceder a la identidad del usuario
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

if __name__ == '__main__':
    app.run()
