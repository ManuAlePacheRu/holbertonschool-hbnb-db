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

    from src.models import amenity, city, country, place, review, user

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