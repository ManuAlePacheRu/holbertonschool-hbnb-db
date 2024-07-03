# tests/test_user.py

import unittest
from src.models.user import User
import uuid
from src.persistence.memory import MemoryRepository
from src.persistence.file import FileRepository
from src.persistence.db import DBRepository
from src.persistence.repository import RepositoryManager

from flask import Flask
from src import create_app, db
from src.config import DevelopmentConfig

class TestUser_module(unittest.TestCase):

    def setUp(self):
        """Set up test variables"""
        self.email = "test@example.com"
        self.first_name = "Test"
        self.last_name = "User"
        self.password = "password123"
        self.is_admin = True
        self.user_id = str(uuid.uuid4())

    def test_user_creation(self):
        """Test if the user is created correctly"""
        user = User(
            id=self.user_id,
            email=self.email,
            first_name=self.first_name,
            last_name=self.last_name,
            password=self.password,
            is_admin=self.is_admin,
        )

        #print("#############################")
        #print(user)
        #print(user.to_dict())
        #print(user.__dict__)

        self.assertEqual(user.id, self.user_id)
        self.assertEqual(user.email, self.email)
        self.assertEqual(user.first_name, self.first_name)
        self.assertEqual(user.last_name, self.last_name)
        self.assertEqual(user.password, self.password)
        self.assertEqual(user.is_admin, self.is_admin)

    def test_user_to_dict(self):
        """Test the to_dict method"""
        user = User(
            id=self.user_id,
            email=self.email,
            first_name=self.first_name,
            last_name=self.last_name,
            password=self.password,
            is_admin=self.is_admin,
        )

        user_dict = user.to_dict()
        self.assertEqual(user_dict['id'], self.user_id)
        self.assertEqual(user_dict['email'], self.email)
        self.assertEqual(user_dict['first_name'], self.first_name)
        self.assertEqual(user_dict['last_name'], self.last_name)
        self.assertEqual(user_dict['password'], self.password)
        self.assertEqual(user_dict['is_admin'], self.is_admin)
        self.assertIn('created_at', user_dict)
        self.assertIn('updated_at', user_dict)

#class TestUser_persistence(unittest.TestCase):

class TestUser_memory(unittest.TestCase):
    def setUp(self):
        """Set up test variables"""
        self.repo = MemoryRepository()
        self.email = "test@example.com"
        self.first_name = "Test"
        self.last_name = "User"
        self.password = "password123"
        self.is_admin = True
        self.user_id = str(uuid.uuid4())
        self.user = User(
            id=self.user_id,
            email=self.email,
            first_name=self.first_name,
            last_name=self.last_name,
            password=self.password,
            is_admin=self.is_admin,
        )

    def test_save_user(self):
        #print("memory user")
        #print(self.user)
        self.repo.save(self.user)
        users = self.repo.get_all("user")
        #print(users)
        self.assertIn(self.user, users)

class TestUser_file(unittest.TestCase):
    def setUp(self):
        """Set up test variables"""
        self.repo = DBRepository()
        self.email = "test@example.com"
        self.first_name = "Test"
        self.last_name = "User"
        self.password = "password123"
        self.is_admin = True
        self.user_id = str(uuid.uuid4())
        self.user = User(
            id=self.user_id,
            email=self.email,
            first_name=self.first_name,
            last_name=self.last_name,
            password=self.password,
            is_admin=self.is_admin,
        )

    def test_save_user(self):
        #print("file user")
        #print(self.user)
        self.repo.save(self.user)
        users = self.repo.get_all("user")
        #print(users)
        self.assertIn(self.user, users)

"""

class TestUser_db(unittest.TestCase):
    def setUp(self):
        self.repo = FileRepository()
        self.email = "test@example.com"
        self.first_name = "Test"
        self.last_name = "User"
        self.password = "password123"
        self.is_admin = True
        self.user_id = str(uuid.uuid4())
        self.user = User(
            id=self.user_id,
            email=self.email,
            first_name=self.first_name,
            last_name=self.last_name,
            password=self.password,
            is_admin=self.is_admin,
        )

    def test_save_user(self):
        print("db user")
        print(self.user)
        self.repo.save(self.user)
        users = self.repo.get_all("user")
        print(users)
        self.assertIn(self.user, users)
        """


class UserModelTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.app = create_app(config_class=DevelopmentConfig())
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.repo = RepositoryManager()
        self.db = db

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_user(self):
        with self.app.app_context():
            user = User(
                email="test@example.com",
                first_name="Test",
                last_name="User",
                password="password123",
                is_admin=True
            )
            #print("file user")
            #print(self.user)
            self.repo.save(user)
            users = self.repo.get_all("user")
            #print(users)
            self.assertIn(self.user, users)

        """with self.app_context():
            conect = db.engine.connect()
            tables = conect.execute("SHOW TABLES")

            print("Tablas:")
            for tabla in tables:
                print(tabla)

            conect.close()
            """
        
        """with self.app_context():
            db.session.add(user)
            db.session.commit()

            saved_user = User.query.filter_by(email="test@example.com").first()
            self.assertIsNotNone(saved_user)
            self.assertEqual(saved_user.email, "test@example.com")
            self.assertTrue(saved_user.is_admin)"""
        

            

if __name__ == "__main__":
    unittest.main()
