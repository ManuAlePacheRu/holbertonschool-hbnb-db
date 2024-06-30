""" Initialize the Flask app. """

from flask import Flask
from flask_cors import CORS
from src.persistence.repository import RepositoryManager


#############################################################
#                   IMPORT SQLALCHEMY                       #
#############################################################
from flask_sqlalchemy import SQLAlchemy
#from src.persistence.db import DBRepository
#from src.config import DevelopmentConfig




cors = CORS()
repo = RepositoryManager()
db = SQLAlchemy()


#################################################################
#                   ESTO ES LO MISMO????                        #
#def create_app(config_class=DevelopmentConfig) -> Flask:       #
#################################################################
def create_app(config_class="src.config.DevelopmentConfig") -> Flask:
    """
    Create a Flask app with the given configuration class.
    The default configuration class is DevelopmentConfig.
    """
    app = Flask(__name__)

##############################################################################################
#                                           SQLAlchemy                                       #
##############################################################################################
    #if app.debug:
    #from flask_sqlalchemy import SQLAlchemy
    #print("DEBUUUUUUUUUUUUUUUUUUUUUUUUUG MOOOOOOOODEEEEEEE")
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///development.db'

    

    

    from sqlalchemy import CheckConstraint
    class Place(db.Model):
        __tablename__ = 'places'

        id = db.Column(db.String(36), primary_key=True)
        created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
        updated_at = db.Column(db.DateTime, onupdate=db.func.current_timestamp())
        name = db.Column(db.String(120), nullable=False)
        description = db.Column(db.String(256))
        address = db.Column(db.String(256), nullable=False)
        latitude = db.Column(db.Float, nullable=False)
        longitude = db.Column(db.Float, nullable=False)
        host_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
        city_id = db.Column(db.String(36), db.ForeignKey('cities.id'), nullable=False)
        price_per_night = db.Column(db.Integer, nullable=False)
        number_of_rooms = db.Column(db.Integer, nullable=False)
        number_of_bathrooms = db.Column(db.Integer, nullable=False)
        max_guests = db.Column(db.Integer, nullable=False)

        __table_args__ = (
        CheckConstraint('price_per_night >= 0', name='check_price_per_night_non_negative'),
        CheckConstraint('max_guests >= 0', name='check_max_guests_non_negative'),
        #CheckConstraint('latitude >= -180', name='check_latitude_valid_values'),
        #CheckConstraint('latitude <= 180', name='check_latitude_valid_values'),
        )

    class Review(db.Model):
        __tablename__ = 'reviews'

        id = db.Column(db.String(36), primary_key=True)
        created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
        updated_at = db.Column(db.DateTime, onupdate=db.func.current_timestamp())
        place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)
        user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
        comment = db.Column(db.String(256))
        rating = db.Column(db.Float, nullable=False)

    class City(db.Model):
        __tablename__ = 'cities'

        id = db.Column(db.String(36), primary_key=True)
        created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
        updated_at = db.Column(db.DateTime, onupdate=db.func.current_timestamp())
        name = db.Column(db.String(120), nullable=False)
        country_code = db.Column(db.String(2), db.ForeignKey('countries.code'), nullable=False)

    class Country(db.Model):
        __tablename__ = 'countries'

        name = db.Column(db.String(120), nullable=False)
        code = db.Column(db.String(2), primary_key=True)

    class Amenity(db.Model):
        __tablename__ = 'amenities'

        id = db.Column(db.String(36), primary_key=True)
        created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
        updated_at = db.Column(db.DateTime, onupdate=db.func.current_timestamp())
        name = db.Column(db.String(120), nullable=False)


##############################################################################################
#                                           SQLAlchemy                                       #
##############################################################################################




    app.url_map.strict_slashes = False

    app.config.from_object(config_class)

    ########################################################################
    #                       VERIFICACIÓN DB URI                            #
    ########################################################################
    print(f"SQLALCHEMY_DATABASE_URI: {app.config['SQLALCHEMY_DATABASE_URI']}")



    register_extensions(app)
    register_routes(app)
    register_handlers(app)

    print(f"Using {repo.repo} repository")

    return app


def register_extensions(app: Flask) -> None:
    """Register the extensions for the Flask app"""
    cors.init_app(app, resources={r"/*": {"origins": "*"}})
    repo.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    # Further extensions can be added here


def register_routes(app: Flask) -> None:
    """Import and register the routes for the Flask app"""

    # Import the routes here to avoid circular imports
    from src.api import api_bp  

    # Register the blueprints in the app
    app.register_blueprint(api_bp)


def register_handlers(app: Flask) -> None:
    """Register the error handlers for the Flask app."""
    app.errorhandler(404)(lambda e: ({"error": "Not found", "message": str(e)}, 404))
    app.errorhandler(400)(lambda e: ({"error": "Bad request", "message": str(e)}, 400))
