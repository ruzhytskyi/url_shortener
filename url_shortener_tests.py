import os
from url_shortener import app, db
import unittest
import tempfile

class UrlShortenerTestCase(unittest.TestCase):
    
    def setUp(self):
        self.db_fd, self.db_fn = tempfile.mkstemp()
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + self.db_fn 
        app.config['TESTING'] = True
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(self.db_fn)

    def test_smth(self):
        assert True

if __name__ == '__main__':
    unittest.main()
