"""
  Now is easy to implement the database repository. The DBRepository
  should implement the Repository (Storage) interface and the methods defined
  in the abstract class Storage.

  The methods to implement are:
    - get_all
    - get
    - save
    - update
    - delete
    - reload (which can be empty)
"""

from src.models.base import Base
from src.persistence.repository import Repository
#from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Session

from src import db

class DBRepository(Repository):
    """Dummy DB repository"""

    #db = SQLAlchemy()


    """class DataManager:
        def save_user(self, user):
            if app.config['USE_DATABASE']:
                db.session.add(user)
                db.session.commit()
            else:
                # Implement file-based save logic
                pass"""

    def __init__(self) -> None:
        pass

    def get_all(self, model_name: str) -> list:
        """Get all objects of a given model"""
        return model_name.query.all()
        #return []

    def get(self, model_name: str, obj_id: str) -> Base | None:
        """Get an object by its ID"""
        #return model_name.query.filter_by(id=obj_id).first()
        return model_name.query.get(obj_id)
        # también se puede así, ya que id es una primarykey


    def reload(self) -> None:
        """Not implemented"""

    def save(self, obj: Base) -> None:
        """Save an object in db"""
        db.session.add(obj)
        db.session.commit()

    def update(self, obj: Base) -> Base | None:
        """Update an object in db"""
        o = self.get(obj.__class__, obj.id)
        if o:
            self.save(obj)

    def delete(self, obj: Base) -> bool:
        """Delete an object in db"""
        db.session.delete(obj)
        db.session.commit()
        #return False
        return True
