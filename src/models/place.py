"""
Place related functionality
"""

from src import repo, db
from src.persistence.db import DBRepository
from src.models.base import Base
from src.models.city import City
from src.models.user import User
from src.models.amenity import Amenity, PlaceAmenity
from sqlalchemy import CheckConstraint
        
class Place(Base, db.Model):
    """Place representation"""

    #__tablename__ = 'places'

    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(256))
    address = db.Column(db.String(256), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    #host_id = db.Column(db.String(36), db.ForeignKey('user.id'), ondelete='CASCADE', nullable=False)
    #city_id = db.Column(db.String(36), db.ForeignKey('city.id'), ondelete='CASCADE', nullable=False)
    host_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    city_id = db.Column(db.String(36), db.ForeignKey('city.id'), nullable=False)
    price_per_night = db.Column(db.Integer, nullable=False)
    number_of_rooms = db.Column(db.Integer, nullable=False)
    number_of_bathrooms = db.Column(db.Integer, nullable=False)
    max_guests = db.Column(db.Integer, nullable=False)

    #amenities = db.relationship("place_amenity", cascade="all, delete-orpahn")
    #reviews = db.relationship("review", cascade="all, delete-orpahn")


    __table_args__ = (
    CheckConstraint('price_per_night >= 0', name='check_price_per_night_non_negative'),
    CheckConstraint('max_guests >= 0', name='check_max_guests_non_negative'),
    CheckConstraint('latitude >= -90', name='check_latitude_valid_values'),
    CheckConstraint('latitude <= 90', name='check_latitude_valid_values'),
    CheckConstraint('longitude <= 180', name='check_longitude_valid_values'),
    CheckConstraint('longitude <= 180', name='check_longitude_valid_values'),
    CheckConstraint('number_of_rooms >= 0', name='check_number_of_rooms_non_negative'),
    CheckConstraint('number_of_bathrooms >= 0', name='check_number_of_bathrooms_non_negative'),
    CheckConstraint('max_guests >= 0', name='check_max_guests_non_negative'),
    )

    """name: str
    description: str
    address: str
    latitude: float
    longitude: float
    host_id: str
    city_id: str
    price_per_night: int
    number_of_rooms: int
    number_of_bathrooms: int
    max_guests: int"""

    def __init__(self, data: dict | None = None, **kw) -> None:
        """Dummy init"""
        super().__init__(**kw)

        if not data:
            return

        self.name = data.get("name", "")
        self.description = data.get("description", "")
        self.address = data.get("address", "")
        self.city_id = data["city_id"]
        self.latitude = float(data.get("latitude", 0.0))
        self.longitude = float(data.get("longitude", 0.0))
        self.host_id = data["host_id"]
        self.price_per_night = int(data.get("price_per_night", 0))
        self.number_of_rooms = int(data.get("number_of_rooms", 0))
        self.number_of_bathrooms = int(data.get("number_of_bathrooms", 0))
        self.max_guests = int(data.get("max_guests", 0))
        
        """self.amenity_ids = []
        
        for valid_amenity in data.get("amenity_ids", []):
            if valid_amenity in repo.get_all(Amenity):
                new_place_amenity = PlaceAmenity(self.id, valid_amenity)
                repo.save(new_place_amenity)
                self.amenity_ids.append(valid_amenity)"""



    def __repr__(self) -> str:
        """Dummy repr"""
        return f"<Place {self.id} ({self.name})>"

    def to_dict(self) -> dict:
        """Dictionary representation of the object"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "address": self.address,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "city_id": self.city_id,
            "host_id": self.host_id,
            "price_per_night": self.price_per_night,
            "number_of_rooms": self.number_of_rooms,
            "number_of_bathrooms": self.number_of_bathrooms,
            "max_guests": self.max_guests,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @staticmethod
    def create(data: dict) -> "Place":
        """Create a new place"""
        user: User | None = User.get(data["host_id"])
        if not user:
            raise ValueError(f"User with ID {data['host_id']} not found")

        city: City | None = City.get(data["city_id"])
        if not city:
            raise ValueError(f"City with ID {data['city_id']} not found")

        amenity_ids_list: list | None = data.get["amenity_ids"]

        if amenity_ids_list:
            
            for amenity_id in amenity_ids_list:
                amenity: Amenity | None = Amenity.get(amenity_id)
                if not amenity:
                    raise ValueError(f"Amenity with ID {amenity_id} not found")
            
            """pre_charged_amenities = repo.get_all(Amenity)
            pre_charged_amenities_ids = [amenity.id for amenity in pre_charged_amenities]

            for amenity_id in data.get("amenity_ids", []):
                if amenity_id not in pre_charged_amenities_ids:
                    new_place_amenity = PlaceAmenity(id, amenity_id)
                    repo.save(new_place_amenity)
                    amenity_ids.append(amenity_id)"""

        new_place = Place(data=data)
        repo.save(new_place)

        if amenity_ids_list:

            for amenity_id in amenity_ids_list:
                new_place_amenity = PlaceAmenity(new_place.id, amenity_id)
                repo.save(new_place_amenity)

        return new_place

    @staticmethod
    def update(place_id: str, data: dict) -> "Place | None":
        """Update an existing place"""
        place: Place | None = Place.get(place_id)

        if not place:
            return None

        for key, value in data.items():
            setattr(place, key, value)

        repo.update(place)

        return place

    #@staticmethod
    def delete(cls, id) -> bool:
        """
        Delete a Place and his references in
        Place_Amenity
        """
        place = cls.get(id)

        if not place:
            return False

        place_amenities = PlaceAmenity.get_all()
        for references in place_amenities:
            if place == references.place_id:
                PlaceAmenity.delete(place, references.amenity_id)

        """if not repo == DBRepository:
            
            only necesary in file/memory storage,
            in class PlaceAmenity is already set with
            ondelete="CASCADE" for autodelete on
            DBRepository tables
            
            place_amenities = repo.get_all(PlaceAmenity)
            for p_a in place_amenities:
                if p_a.place_id == place.id:
                    repo.delete(p_a)"""


        return repo.delete(place)
