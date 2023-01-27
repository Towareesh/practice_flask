import os
os.environ['DATABASE_URL'] = 'sqlite://'

from datetime import datetime, timedelta
import unittest
from app import app, db
from app.models import User, Post
from app.views import user_write_db, user_del_db


class UserModel(unittest.TestCase):
    # def setUp(self):
    #     self.app_context = app.app_context()
    #     self.app_context.push()
    #     db.create_all()
    
    # def tearDown(self):
    #     db.session.remove()
    #     db.drop_all()
    #     self.app_context.pop()
    #     print('COMPLETE')
    
    def test_password_hashing(self):
        user = User(username='NoNAME_1')
        user.set_password('password')
        self.assertTrue(user.check_password('password'))
        self.assertFalse(user.check_password('false_password'))
    
    def test_avatar(self):
        user = User(username='john', email='john@example.com')
        self.assertEqual(user.avatar(128), ('https://www.gravatar.com/avatar/d4c74594d841139328695756648b6bd6?d=identicon&s=128'))

if __name__ == '__main__':
    unittest.main(verbosity=2)