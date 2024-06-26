""" Repository pattern for data access layer """

from abc import ABC, abstractmethod
from typing import Any

from flask import Flask

from src.persistence import get_repo


class Repository(ABC):
    """Abstract class for repository pattern"""

    @abstractmethod
    def reload(self) -> None:
        """Reload data to the repository"""

    @abstractmethod
    def get_all(self, model_name: str) -> list:
        """Get all objects of a model"""

    @abstractmethod
    def get(self, model_name: str, id: str) -> None:
        """Get an object by id"""

    @abstractmethod
    def save(self, obj) -> None:
        """Save an object"""

    @abstractmethod
    def update(self, obj) -> None:
        """Update an object"""

    @abstractmethod
    def delete(self, obj) -> bool:
        """Delete an object"""


class RepositoryManager:
    """Manages the initialization of the repository in the Flask App"""

    def __init__(self) -> None:
        pass

    def init_app(self, app: Flask) -> None:
        """ """
        self.app = app

        self.repo = get_repo(app.config["REPOSITORY"])

    def get(self, model_name: str, obj_id: str) -> None:
        return self.repo.get(model_name, obj_id)

    def get_all(self, model_name: str) -> list:
        return self.repo.get_all(model_name)

    def save(self, obj) -> None:
        return self.repo.save(obj)

    def update(self, obj) -> None:
        return self.repo.update(obj)

    def delete(self, obj) -> bool:
        return self.repo.delete(obj)
