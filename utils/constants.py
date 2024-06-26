""" Export constants for the application """

from enum import Enum

API_VERSION_PATH = "/v1"

REPOSITORY_ENV_VAR = "REPO"


class Repos(Enum):
    """Enum for the different repository types"""

    DB = "db"
    FILE = "file"
    PICKLE = "pickle"
    MEMORY = "memory"


DEFAULT_REPOSITORY = Repos.FILE.value

FILE_STORAGE_FILENAME = "data.json"
PICKLE_STORAGE_FILENAME = "data.pkl"
