# tests/test_user.py

import unittest
from src.persistence.db import DBRepository
from src import create_app, db
from src.models.amenity import Amenity

class amenity_db_test(unittest.TestCase):
    def setUp(self) -> None:
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.repo = DBRepository()
        self.db = db
        self.wifi = Amenity("wifi")
        self.pool = Amenity("pool")


    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_amenity(self):
        #with self.app.app_context():
        self.repo.save(self.wifi)
        self.repo.save(self.pool)
        
        #db.session.refresh(user)
        amenities = self.repo.get_all(self.wifi)
        self.assertIn(self.wifi, amenities)
        self.assertIn(self.pool, amenities)

    def test_update_user(self):
        user = User(
            email="test2@example.com",
            first_name="Test",
            last_name="User",
            password="password123",
            is_admin=True
        )
        self.repo.save(user)
        user.first_name = "update_name"
        users = self.repo.get_all(user)
        self.assertIn(user, users)

    def test_delete_user(self):
        user = User(
            email="test3@example.com",
            first_name="Test",
            last_name="User",
            password="password123",
            is_admin=True
        )
        self.repo.save(user)
        #print(f"save user = {user}")
        users = self.repo.get_all(user)
        #print(f"users in db = {users}")
        #print(f"delete user = {user}")
        self.repo.delete(user)
        users = self.repo.get_all(user)
        #print(f"users in db = {users}")
        self.assertNotIn(user, users)


if __name__ == "__main__":
    unittest.main()
