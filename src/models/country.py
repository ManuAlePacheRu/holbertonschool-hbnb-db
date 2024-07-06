"""
Country related functionality
"""

from src import repo, db

class Country(db.Model):
    """
    Country representation

    This class does NOT inherit from Base, you can't delete or update a country

    This class is used to get and list countries
    """
    #__tablename__ = 'countries'

    name = db.Column(db.String(120), nullable=False)
    code = db.Column(db.String(2), primary_key=True)

    #cities = db.relationship("city", cascade="all, delete-orpahn")


    """name: str
    code: str
    cities: list"""

    def __init__(self, name: str, code: str, **kw) -> None:
        """Dummy init"""
        super().__init__(**kw)
        self.name = name
        self.code = code

    def __repr__(self) -> str:
        """Dummy repr"""
        return f"<Country {self.code} ({self.name})>"

    def to_dict(self) -> dict:
        """Returns the dictionary representation of the country"""
        return {
            "name": self.name,
            "code": self.code,
        }

    @staticmethod
    def get_all() -> list["Country"]:
        """Get all countries"""
        countries: list["Country"] = repo.get_all("country")

        return countries

    @staticmethod
    def get(code: str) -> "Country | None":
        """Get a country by its code"""
        for country in Country.get_all():
            if country.code == code:
                return country
        return None

    @staticmethod
    def create(name: str, code: str) -> "Country":
        """Create a new country"""
        country = Country(name, code)

        repo.save(country)

        return country
